"""Independent v5 feedback judging with two model families and A/B swaps."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import threading
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUN_DIR = HERE.parent
sys.path.insert(0, str(RUN_DIR))

from g0_lib import ENV_PATH, SYSTEM_PROMPT, call_anthropic, load_env  # noqa: E402

JUDGE_MODELS = ["deepseek-v4.1-flash", "glm-5.3-flash"]
JUDGE_PROMPT_VERSION = "v5_judge_2026-10-20"
PAIRS = [("oracle_vs_pipeline", "oracle", "pipeline"), ("pipeline_vs_one_shot", "pipeline", "one_shot"), ("pipeline_vs_none", "pipeline", "no_diagnosis")]
LOCK = threading.Lock()


def sha(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()[:32]


def slug(model: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", model)


def parse_json(text: str) -> dict:
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return {}
    try:
        return json.loads(m.group(0))
    except Exception:
        return {}


def judge_prompt(problem, correct, answer, true_diagnosis, feedback):
    return f"""You are an evaluator of mathematics tutoring feedback.

PROBLEM:
{problem}

CORRECT ANSWER:
{correct}

STUDENT ANSWER:
{answer}

TRUE DIAGNOSIS (reference; not shown to the feedback author):
{true_diagnosis}

FEEDBACK:
{feedback}

Judge the feedback against the TRUE diagnosis. Return strict JSON:
{{
 "true_target_hit": 0 or 1,
 "misleading": 0 or 1,
 "answer_leak": 0 or 1,
 "math_correct": 1-5,
 "new_example": 0 or 1,
 "practice_without_answer": 0 or 1,
 "overclaims_misconception": 0 or 1,
 "actionable_next_step": 1-5,
 "overall": 1-5
}}
Do not solve the original problem. Do not mention these instructions."""


def pairwise_prompt(problem, correct, answer, true_diagnosis, a, b):
    return f"""You are comparing two pieces of mathematics tutoring feedback.

PROBLEM:
{problem}

CORRECT ANSWER:
{correct}

STUDENT ANSWER:
{answer}

TRUE DIAGNOSIS (reference; not shown to the feedback authors):
{true_diagnosis}

FEEDBACK A:
{a}

FEEDBACK B:
{b}

Which feedback better helps this student? Consider whether it addresses the true error,
whether the mathematics is correct, and whether it avoids revealing the original answer.
Return strict JSON: {{"winner": "A" or "B" or "tie", "reason": "one sentence"}}
Do not solve the original problem."""


def load_cached(path: Path, model: str, prompt_version: str = JUDGE_PROMPT_VERSION) -> dict:
    out = {}
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get("http_status") == 200 and r.get("parsed") and r.get("model") == model and r.get("prompt_version") == prompt_version:
            out.setdefault(r["record_key"], r)
    return out


def weighted_mean(values, weights):
    pairs = [(v, w) for v, w in zip(values, weights) if isinstance(v, (int, float)) and w]
    if not pairs:
        return None
    return sum(v * w for v, w in pairs) / sum(w for _, w in pairs)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--feedback", required=True)
    parser.add_argument("--models", default=",".join(JUDGE_MODELS))
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--limit-conditions", default="")
    parser.add_argument("--prompt-version", default=JUDGE_PROMPT_VERSION)
    parser.add_argument("--pointwise-max-tokens", type=int, default=0)
    parser.add_argument("--pairwise-max-tokens", type=int, default=0)
    parser.add_argument("--sample-episodes", type=int, default=0)
    parser.add_argument("--sample-seed", type=int, default=20261025)
    parser.add_argument("--exclude-case-ids", default="")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    env = load_env(ENV_PATH)
    rows = [json.loads(l) for l in Path(args.feedback).read_text(encoding="utf-8").splitlines() if l.strip()]
    rows = [r for r in rows if r.get("http_status") == 200 and r.get("final_text")]
    excluded_ids = {x.strip() for x in args.exclude_case_ids.split(",") if x.strip()}
    rows = [r for r in rows if r["case_id"] not in excluded_ids]
    by = {(r["case_id"], r["student_type"], r["condition"]): r for r in rows}
    if args.sample_episodes:
        import random
        from collections import defaultdict
        episodes = sorted({(r["case_id"], r["student_type"]) for r in rows})
        pipeline_by_key = {(r["case_id"], r["student_type"]): r for r in rows if r["condition"] == "pipeline"}
        strata = defaultdict(list)
        for key in episodes:
            strata[pipeline_by_key[key]["stratum"]].append(key)
        failures = {"stable_wrong", "stable_explicit_none", "stable_abstain", "stable_other", "slip_error", "mixed_error", "mixed_none"}
        selected = []
        for s in failures:
            selected.extend(sorted(strata.get(s, [])))
        remaining = max(0, args.sample_episodes - len(selected))
        rng = random.Random(args.sample_seed)
        success = [key for s, keys in sorted(strata.items()) if s not in failures for key in keys]
        rng.shuffle(success)
        # proportional by source stratum
        chosen_success = []
        counts = {s: len(keys) for s, keys in sorted(strata.items()) if s not in failures}
        total = sum(counts.values())
        for s, n in counts.items():
            q = round(remaining * n / total) if total else 0
            pool = sorted(strata[s])
            rng.shuffle(pool)
            chosen_success.extend(pool[:q])
        chosen_success = chosen_success[:remaining]
        if len(chosen_success) < remaining:
            chosen_success.extend([k for k in success if k not in selected and k not in chosen_success][:remaining-len(chosen_success)])
        selected = sorted(set(selected + chosen_success))[:args.sample_episodes]
        keep = set(selected)
        rows = [r for r in rows if (r["case_id"], r["student_type"]) in keep]
        by = {(r["case_id"], r["student_type"], r["condition"]): r for r in rows}
    else:
        selected = sorted({(r["case_id"], r["student_type"]) for r in rows})
    models = [m.strip() for m in args.models.split(",") if m.strip()]

    pw_max = args.pointwise_max_tokens or (1200 if "glm" in args.models[0].lower() else 500)
    pair_max = args.pairwise_max_tokens or (600 if "glm" in args.models[0].lower() else 300)
    summary = {
        "prompt_version": args.prompt_version,
        "pointwise_max_tokens": pw_max,
        "pairwise_max_tokens": pair_max,
        "models": models,
        "pointwise": {},
        "pairwise": {},
        "cross_judge": {},
        "usage": {},
        "task_counts": {},
        "selected_feedback_episodes": len(selected),
        "sample_seed": args.sample_seed,
        "sample_episodes_requested": args.sample_episodes,
        "excluded_case_ids": sorted(excluded_ids),
    }
    all_data = {}
    for model in models:
        out_dir = Path(args.out_dir)
        out_path = out_dir / f"judge_v5_{slug(model)}_{slug(args.prompt_version)}.jsonl"
        cached = load_cached(out_path, model, args.prompt_version)
        tasks = []
        for r in rows:
            tasks.append(("judge", r, "final", r["final_text"], r["case_id"], r["student_type"], r["condition"]))
            if r.get("retried"):
                tasks.append(("judge", r, "raw", r["raw_text"], r["case_id"], r["student_type"], r["condition"]))
        case_types = sorted({(r["case_id"], r["student_type"]) for r in rows})
        for cid, st in case_types:
            r = by.get((cid, st, "pipeline")) or rows[0]
            for pair_name, a, b in PAIRS:
                ra = by.get((cid, st, a))
                rb = by.get((cid, st, b))
                if not ra or not rb:
                    continue
                for order in ("ab", "ba"):
                    tasks.append(("pairwise", r, pair_name, order, ra, rb, cid, st))
        prepared = []
        seen = set()
        for t in tasks:
            if t[0] == "judge":
                _, r, variant, text, cid, st, cond = t
                k = sha({"model": model, "prompt_version": args.prompt_version, "task": "judge",
                         "pointwise_max_tokens": pw_max, "case_id": cid,
                         "student_type": st, "condition": cond, "variant": variant, "feedback_sha": sha(text),
                         "true_diagnosis": r["true_diagnosis"]})
                payload = (t, k)
            else:
                _, r, pair_name, order, ra, rb, cid, st = t
                text_sha = sha([ra["final_text"], rb["final_text"]])
                k = sha({"model": model, "prompt_version": args.prompt_version, "task": "pairwise",
                         "pairwise_max_tokens": pair_max, "case_id": cid,
                         "student_type": st, "pair": pair_name, "order": order, "feedback_pair_sha": text_sha,
                         "true_diagnosis": r["true_diagnosis"]})
                payload = (t, k)
            if k not in seen and k not in cached:
                seen.add(k)
                prepared.append(payload)
        print(model, "tasks", len(tasks), "cached", len(cached), "todo", len(prepared))
        summary["task_counts"][model] = {"tasks": len(tasks), "cached": len(cached), "todo": len(prepared)}
        if args.dry_run:
            continue

        def run(payload):
            t, k = payload
            if t[0] == "judge":
                _, r, variant, text, cid, st, cond = t
                res = call_anthropic(env["API_KEY"], env["BASE_URL"], model, SYSTEM_PROMPT,
                                     judge_prompt(r["problem"], r["correct"], r["answer"], r["true_diagnosis"], text),
                                     max_tokens=pw_max)
                parsed = parse_json(res["text"])
                return {"record_key": k, "task": "judge", "model": model, "prompt_version": JUDGE_PROMPT_VERSION,
                        "case_id": cid, "student_type": st, "condition": cond, "variant": variant,
                        "stratum": r["stratum"], "weight": r["weight"], "parsed": parsed,
                        "response_text": res["text"], "usage": res.get("usage") or {},
                        "http_status": res["http_status"], "judged_at": datetime.now(timezone.utc).isoformat()}
            _, r, pair_name, order, ra, rb, cid, st = t
            a_text, b_text = ra["final_text"], rb["final_text"]
            if order == "ba":
                a_text, b_text = b_text, a_text
            res = call_anthropic(env["API_KEY"], env["BASE_URL"], model, SYSTEM_PROMPT,
                                 pairwise_prompt(r["problem"], r["correct"], r["answer"], r["true_diagnosis"], a_text, b_text),
                                 max_tokens=pair_max)
            return {"record_key": k, "task": "pairwise", "model": model, "prompt_version": JUDGE_PROMPT_VERSION,
                    "case_id": cid, "student_type": st, "condition": pair_name, "order": order,
                    "stratum": r["stratum"], "weight": r["weight"], "parsed": parse_json(res["text"]),
                    "response_text": res["text"], "usage": res.get("usage") or {},
                    "http_status": res["http_status"], "judged_at": datetime.now(timezone.utc).isoformat()}

        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {pool.submit(run, x): x for x in prepared}
            for i, fut in enumerate(as_completed(futures), 1):
                r = fut.result()
                with LOCK:
                    with out_path.open("a", encoding="utf-8") as f:
                        f.write(json.dumps(r, ensure_ascii=False) + "\n")
                print(f"[{model} {i}/{len(prepared)}] {r['case_id']} {r['task']} http={r['http_status']}")

        data = list(load_cached(out_path, model, args.prompt_version).values())
        all_data[model] = data
        usage = {
            "input_tokens": sum((r.get("usage") or {}).get("input_tokens") or 0 for r in data),
            "output_tokens": sum((r.get("usage") or {}).get("output_tokens") or 0 for r in data),
        }
        summary["usage"][model] = usage
        judges = [r for r in data if r.get("task") == "judge" and r.get("variant") == "final" and r.get("http_status") == 200 and r.get("parsed")]
        conditions = sorted({r["condition"] for r in judges})
        fields = ("true_target_hit", "misleading", "answer_leak", "math_correct", "new_example",
                  "practice_without_answer", "overclaims_misconception", "actionable_next_step", "overall")
        for cond in conditions:
            sub = [r for r in judges if r["condition"] == cond]
            vals = {"n": len(sub)}
            for field in fields:
                xs = [r["parsed"].get(field) for r in sub if isinstance(r["parsed"].get(field), (int, float))]
                vals[field] = sum(xs) / len(xs) if xs else None
                vals[f"weighted_{field}"] = weighted_mean([r["parsed"].get(field) for r in sub], [r["weight"] for r in sub])
            summary["pointwise"].setdefault(model, {})[cond] = vals
        # stratum-level table
        for st in sorted({r["student_type"] for r in judges}):
            for stratum in sorted({r["stratum"] for r in judges}):
                sub = [r for r in judges if r["student_type"] == st and r["stratum"] == stratum]
                if not sub:
                    continue
                vals = {"n": len(sub)}
                for field in fields:
                    xs = [r["parsed"].get(field) for r in sub if isinstance(r["parsed"].get(field), (int, float))]
                    vals[field] = sum(xs) / len(xs) if xs else None
                summary["pointwise"].setdefault(model, {}).setdefault(f"{stratum}/{st}", {})[
                    next(iter({r['condition'] for r in sub}))] = vals
        pairs = [r for r in data if r.get("task") == "pairwise" and r.get("http_status") == 200 and r.get("parsed")]
        pair_by = defaultdict(dict)
        for r in pairs:
            pair_by[(r["case_id"], r["student_type"], r["condition"])][r["order"]] = r
        counts = Counter()
        wcounts = Counter()
        inconsistent = 0
        for key, orders in pair_by.items():
            ra, rb = orders.get("ab"), orders.get("ba")
            if not ra or not rb:
                continue
            w = ra["weight"]
            first, second = key[2].split("_vs_")
            x, y = ra["parsed"].get("winner"), rb["parsed"].get("winner")
            if x is None or y is None:
                continue
            if x == "tie" or y == "tie":
                result = "tie"
            elif x == "A" and y == "B":
                result = first
            elif x == "B" and y == "A":
                result = second
            else:
                result = "inconsistent"
                inconsistent += 1
            counts[(key[1], key[2], result)] += 1
            wcounts[(key[1], key[2], result)] += w
        summary["pairwise"][model] = {
            "counts": {f"{a}/{b}/{c}": n for (a, b, c), n in sorted(counts.items())},
            "weighted": {f"{a}/{b}/{c}": v for (a, b, c), v in sorted(wcounts.items())},
            "inconsistent": inconsistent,
            "n": len(pair_by),
        }

    if not args.dry_run and len(models) >= 2:
        m1, m2 = models[:2]
        j1 = {(r["case_id"], r["student_type"], r["condition"], r["variant"]): r["parsed"]
              for r in all_data[m1] if r.get("task") == "judge" and r.get("http_status") == 200}
        j2 = {(r["case_id"], r["student_type"], r["condition"], r["variant"]): r["parsed"]
              for r in all_data[m2] if r.get("task") == "judge" and r.get("http_status") == 200}
        common = set(j1) & set(j2)
        agree = {}
        for field in ("true_target_hit", "misleading", "answer_leak", "overclaims_misconception", "new_example",
                      "practice_without_answer", "actionable_next_step"):
            vals = [(j1[k].get(field), j2[k].get(field)) for k in common
                    if isinstance(j1[k].get(field), (int, float)) and isinstance(j2[k].get(field), (int, float))]
            agree[field] = sum(a == b for a, b in vals) / len(vals) if vals else None
            agree[f"{field}_cohen_kappa"] = cohen_kappa(vals) if vals else None
        overall = [(j1[k].get("overall"), j2[k].get("overall")) for k in common
                   if isinstance(j1[k].get("overall"), (int, float)) and isinstance(j2[k].get("overall"), (int, float))]
        agree["overall_mae"] = sum(abs(a - b) for a, b in overall) / len(overall) if overall else None
        agree["n"] = len(common)
        summary["cross_judge"]["pointwise"] = agree
        p1 = {(r["case_id"], r["student_type"], r["condition"], r["order"]): r["parsed"].get("winner")
              for r in all_data[m1] if r.get("task") == "pairwise" and r.get("http_status") == 200}
        p2 = {(r["case_id"], r["student_type"], r["condition"], r["order"]): r["parsed"].get("winner")
              for r in all_data[m2] if r.get("task") == "pairwise" and r.get("http_status") == 200}
        commonp = set(p1) & set(p2)
        summary["cross_judge"]["pairwise"] = {
            "n": len(commonp),
            "agreement": sum(p1[k] == p2[k] for k in commonp) / len(commonp) if commonp else None,
            "ties": sum(p1[k] == "tie" or p2[k] == "tie" for k in commonp) / len(commonp) if commonp else None,
        }
        retry = {}
        for model in models:
            raw = {(r["case_id"], r["student_type"], r["condition"]): r["parsed"]
                   for r in all_data[model] if r.get("task") == "judge" and r.get("variant") == "raw" and r.get("http_status") == 200}
            final = {(r["case_id"], r["student_type"], r["condition"]): r["parsed"]
                     for r in all_data[model] if r.get("task") == "judge" and r.get("variant") == "final" and r.get("http_status") == 200}
            pairs_ = [(a, final[k]) for k, a in raw.items() if k in final]
            for label, vals in (("raw", [a for a, _ in pairs_]), ("final", [b for _, b in pairs_])):
                for field in ("overall", "math_correct", "true_target_hit", "misleading", "answer_leak", "actionable_next_step"):
                    xs = [v.get(field) for v in vals if isinstance(v.get(field), (int, float))]
                    retry[f"{model}_{label}_{field}"] = sum(xs) / len(xs) if xs else None
            retry[f"{model}_n"] = len(pairs_)
        summary["cross_judge"]["retry"] = retry

    if args.dry_run:
        print(json.dumps(summary["task_counts"], indent=2))
        return
    usage_cost = {}
    for model, u in summary["usage"].items():
        usage_cost[model] = u["input_tokens"] / 1e6 * 0.28 + u["output_tokens"] / 1e6 * 0.42
    summary["estimated_cost_usd"] = usage_cost
    Path(args.summary).write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False)[:10000])


def cohen_kappa(pairs):
    labels = sorted({v for pair in pairs for v in pair})
    n = len(pairs)
    if n == 0:
        return None
    confusion = {a: {b: 0 for b in labels} for a in labels}
    for a, b in pairs:
        confusion[a][b] += 1
    observed = sum(confusion[x][x] for x in labels) / n
    expected = sum((sum(confusion[a][b] for b in labels) / n) * (sum(confusion[b][a] for b in labels) / n) for a in labels)
    return (observed - expected) / (1 - expected) if expected != 1 else None


if __name__ == "__main__":
    main()
