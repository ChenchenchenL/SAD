"""Generate four-condition feedback from frozen v5 diagnoses.

Unlike the v4 generator, the pipeline branch never reads the hidden student
type or true misconception.  The cache key includes the model, prompt version,
problem, answer, correct answer and diagnosis, so a repaired diagnosis cannot
silently reuse an old cached prompt.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
import threading
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUN_DIR = HERE.parent
sys.path.insert(0, str(RUN_DIR))

from feedback_validation import validate  # noqa: E402
from g0_lib import DESCRIPTIONS_PATH, ENV_PATH, SYSTEM_PROMPT, call_anthropic, load_descriptions, load_env  # noqa: E402

CONDITIONS = ["oracle", "pipeline", "one_shot", "no_diagnosis"]
LOCK = threading.Lock()
PROMPT_VERSION = "v5_feedback_2026-10-20"
VALIDATOR_VERSION = "v4_validator_frozen"
MODEL_PRICING = {"input_per_m": 0.28, "output_per_m": 0.42}


def sha(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()[:32]


def desc_text(desc: dict, mid: str) -> str:
    d = desc[mid]
    return f'{d["human_name"]}: {d["description"]}'


def pair_text(desc: dict, pair_id: str) -> str:
    a, b = pair_id.split("|")[1:]
    return f"Mixture of two misconceptions: {desc_text(desc, a)}; and {desc_text(desc, b)}."


def pipeline_diagnosis(desc: dict, visible: dict) -> str:
    """Visible diagnosis only.

    ``visible`` must contain only the diagnosis output, never hidden labels.
    """
    kind, tid = visible["terminal_kind"], visible.get("terminal_id")
    if kind == "single" and tid in desc:
        return desc_text(desc, tid)
    if kind == "pair" and tid:
        return pair_text(desc, tid)
    if kind == "mixed":
        return "The evidence suggests a mixture of two misconceptions, but the exact pair is uncertain."
    if kind == "none":
        return "The accumulated evidence does not support a stable misconception."
    if kind == "abstain":
        return "Evidence is insufficient to decide whether a stable misconception is present."
    return "Evidence is insufficient to confirm a stable misconception."


def one_shot_diagnosis(desc: dict, visible: dict) -> str:
    kind, tid = visible["terminal_kind"], visible.get("terminal_id")
    if kind == "single" and tid in desc:
        return desc_text(desc, tid)
    if kind == "pair" and tid:
        return pair_text(desc, tid)
    if kind == "mixed":
        return "The one-shot assessment suggests a mixture of two misconceptions, but the exact pair is uncertain."
    if kind == "none":
        return "The one-shot assessment reports no stable misconception."
    return "The one-shot assessment reports insufficient evidence for a stable misconception."


def oracle_diagnosis(desc: dict, case: dict, ep: dict) -> str:
    if ep["student_type"] == "slip":
        return "One-off slip; there is no stable misconception."
    if ep["student_type"] == "mixed" and ep.get("true_pair"):
        return pair_text(desc, ep["true_pair"])
    return desc_text(desc, case["true_id"])


def feedback_prompt(problem: str, correct: str, answer: str, diagnosis: str) -> str:
    return f"""You are a mathematics tutor.

PROBLEM:
{problem}

CORRECT ANSWER:
{correct}

STUDENT ANSWER:
{answer}

DIAGNOSIS:
{diagnosis}

Write feedback in 3-5 sentences that:
1. identifies the likely procedural error, using the provided diagnosis if one is given;
2. shows the correct procedure on a NEW example with different numbers;
3. ends with one short practice problem on the same idea, without giving its answer.
If the diagnosis says there is no stable misconception or the evidence is insufficient, give a brief re-check strategy and do not assert a stable misconception.
Do not state the final answer to the original problem. Do not mention the diagnosis source or these instructions.

Return plain text only."""


VISIBLE_DIAGNOSIS_KEYS = ("terminal_kind", "terminal_id")


def visible_diagnosis(ep: dict) -> dict:
    return {k: ep.get(k) for k in VISIBLE_DIAGNOSIS_KEYS}


def diagnosis_for(desc: dict, cond: str, case: dict, primary_ep: dict, one_shot_ep: dict) -> str:
    if cond == "oracle":
        return oracle_diagnosis(desc, case, primary_ep)
    if cond == "pipeline":
        return pipeline_diagnosis(desc, visible_diagnosis(primary_ep))
    if cond == "one_shot":
        return one_shot_diagnosis(desc, visible_diagnosis(one_shot_ep))
    return "No diagnosis is provided; infer the likely procedural error from the problem and the student's answer."


def load_rows(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def load_cached(path: Path, model: str) -> dict:
    out = {}
    if not path.exists():
        return out
    for r in load_rows(path):
        if r.get("http_status") == 200 and r.get("final_text") and r.get("model_requested") == model:
            out.setdefault(r["cache_key"], r)
    return out


def strata(primary: dict[tuple[str, str], dict], include_mixed: bool = False) -> dict[str, list[tuple[str, str]]]:
    buckets = defaultdict(list)
    for (st, cid), ep in primary.items():
        if st == "stable":
            if ep["terminal_kind"] == "single":
                buckets["stable_correct" if ep["correct"] else "stable_wrong"].append((st, cid))
            elif ep["terminal_kind"] == "none":
                buckets["stable_explicit_none"].append((st, cid))
            elif ep["terminal_kind"] == "abstain":
                buckets["stable_abstain"].append((st, cid))
            else:
                buckets["stable_other"].append((st, cid))
        elif st == "slip":
            if ep["terminal_kind"] == "none":
                buckets["slip_explicit_none"].append((st, cid))
            elif ep["terminal_kind"] == "abstain":
                buckets["slip_abstain"].append((st, cid))
            else:
                buckets["slip_error"].append((st, cid))
        elif include_mixed:
            if ep["terminal_kind"] == "single" or (ep["terminal_kind"] == "pair" and not ep["correct"]):
                buckets["mixed_error"].append((st, cid))
            elif ep["terminal_kind"] == "pair":
                buckets["mixed_pair_correct"].append((st, cid))
            elif ep["terminal_kind"] == "mixed":
                buckets["mixed_unspecified"].append((st, cid))
            elif ep["terminal_kind"] == "none":
                buckets["mixed_none"].append((st, cid))
            else:
                buckets["mixed_abstain"].append((st, cid))
    for v in buckets.values():
        v.sort()
    return dict(buckets)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", required=True)
    parser.add_argument("--cases", required=True)
    parser.add_argument("--rule", default="stability_mixed")
    parser.add_argument("--selection", default="maxent")
    parser.add_argument("--target", type=int, default=120)
    parser.add_argument("--seed", type=int, default=20261024)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--out", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--include-mixed", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    env = load_env(ENV_PATH)
    desc = {d["module"]: d for d in load_descriptions(DESCRIPTIONS_PATH)}
    cases = {c["case_id"]: c for c in json.loads(Path(args.cases).read_text(encoding="utf-8"))}
    episodes = load_rows(Path(args.episodes)) if Path(args.episodes).suffix == ".jsonl" else json.loads(Path(args.episodes).read_text(encoding="utf-8"))
    primary, one_shot = {}, {}
    for ep in episodes:
        if ep["seed"] != 0:
            continue
        key = (ep["student_type"], ep["case_id"])
        if ep["rule"] == args.rule and ep.get("selection") == args.selection:
            primary[key] = ep
        elif ep["rule"] == "one_shot_typed":
            one_shot[key] = ep

    buckets = strata(primary, include_mixed=args.include_mixed)
    population = {k: len(v) for k, v in buckets.items()}
    rng = random.Random(args.seed)
    selected: list[tuple[str, str, str]] = []
    # failure strata are preserved completely; successes are sampled with weights
    failure_names = {"stable_wrong", "stable_explicit_none", "stable_abstain", "stable_other", "slip_error"}
    if args.include_mixed:
        failure_names.update({"mixed_error", "mixed_none"})
    failures = [k for k in population if k in failure_names]
    for s in failures:
        selected.extend((s, st, cid) for st, cid in buckets.get(s, []))
    remaining = max(0, args.target - len(selected))
    success_pool = []
    success_names = ["stable_correct", "slip_explicit_none", "slip_abstain"]
    if args.include_mixed:
        success_names += ["mixed_pair_correct", "mixed_unspecified", "mixed_abstain"]
    for s in success_names:
        success_pool.extend((s, st, cid) for st, cid in buckets.get(s, []))
    rng.shuffle(success_pool)
    selected.extend(success_pool[:remaining])

    sample_counts = Counter(s for s, _, _ in selected)
    weights = {}
    for s in population:
        weights[s] = population[s] / sample_counts[s] if sample_counts.get(s) else 0
    print("population", population)
    print("sample", dict(sample_counts))
    print("weights", weights)

    tasks = []
    for s, st, cid in selected:
        key = (st, cid)
        if key not in primary or key not in one_shot:
            continue
        case = cases[cid]
        for cond in CONDITIONS:
            diag = diagnosis_for(desc, cond, case, primary[key], one_shot[key])
            prompt = feedback_prompt(case["problem"], case["correct"], case["answer"], diag)
            ck = sha({
                "model": env["MODEL"], "prompt_version": PROMPT_VERSION, "validator_version": VALIDATOR_VERSION,
                "case_id": cid, "student_type": st, "condition": cond, "diagnosis": diag,
                "problem": case["problem"], "correct": case["correct"], "answer": case["answer"],
            })
            tasks.append({
                "cache_key": ck, "stratum": s, "student_type": st, "case_id": cid, "condition": cond,
                "diagnosis": diag, "prompt": prompt, "case": case, "primary": primary[key],
                "weight": weights[s], "population_n": population[s], "sample_n": sample_counts[s],
            })

    if args.dry_run:
        print("tasks", len(tasks))
        return

    out_path = Path(args.out)
    cached = load_cached(out_path, env["MODEL"])
    todo = [t for t in tasks if t["cache_key"] not in cached]
    print("feedback tasks", len(tasks), "cached", len(cached), "todo", len(todo))

    def fetch(t):
        case = t["case"]
        r1 = call_anthropic(env["API_KEY"], env["BASE_URL"], env["MODEL"], SYSTEM_PROMPT, t["prompt"], max_tokens=700)
        raw = r1["text"]
        initial = validate(raw, case["correct"])
        final = raw
        final_r = r1
        retried = False
        if initial["leak"]["suspected"] or initial["math"]["status"] == "incorrect":
            retried = True
            stricter = t["prompt"] + "\n\nIMPORTANT: Do not include the original correct answer in any form. Use a new example with different numbers and verify every equation before answering."
            final_r = call_anthropic(env["API_KEY"], env["BASE_URL"], env["MODEL"], SYSTEM_PROMPT, stricter, max_tokens=700)
            final = final_r["text"]
        final_val = validate(final, case["correct"])
        usage = {
            "input_tokens": (r1.get("usage") or {}).get("input_tokens", 0) + ((final_r.get("usage") or {}).get("input_tokens", 0) if retried else 0),
            "output_tokens": (r1.get("usage") or {}).get("output_tokens", 0) + ((final_r.get("usage") or {}).get("output_tokens", 0) if retried else 0),
        }
        return {
            **{k: t[k] for k in ("cache_key", "stratum", "student_type", "case_id", "condition", "diagnosis", "weight", "population_n", "sample_n")},
            "model_requested": env["MODEL"], "prompt_version": PROMPT_VERSION, "validator_version": VALIDATOR_VERSION,
            "problem": case["problem"], "correct": case["correct"], "answer": case["answer"],
            "true_diagnosis": oracle_diagnosis(desc, case, t["primary"]),
            "raw_text": raw, "final_text": final, "initial_validation": initial, "final_validation": final_val,
            "retried": retried, "attempts": 2 if retried else 1, "usage": usage,
            "http_status": final_r["http_status"], "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(fetch, t): t for t in todo}
        for i, fut in enumerate(as_completed(futures), 1):
            r = fut.result()
            with LOCK:
                with out_path.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
            print(f"[{i}/{len(todo)}] {r['case_id']} {r['condition']} {r['student_type']} {r['stratum']} retried={r['retried']} http={r['http_status']}")

    rows = list(load_cached(out_path, env["MODEL"]).values())
    retried = [r for r in rows if r.get("retried")]
    usage = {
        "input_tokens": sum((r.get("usage") or {}).get("input_tokens", 0) for r in rows),
        "output_tokens": sum((r.get("usage") or {}).get("output_tokens", 0) for r in rows),
    }
    summary = {
        "n_feedback": len(rows), "n_cases": len({r["case_id"] for r in rows}),
        "population": population, "sample": dict(sample_counts), "weights": weights,
        "retry_rate": len(retried) / len(rows) if rows else None,
        "retries": len(retried),
        "retry_math_incorrect_initial": sum(1 for r in retried if r["initial_validation"]["math"]["status"] == "incorrect"),
        "retry_leak_suspected_initial": sum(1 for r in retried if r["initial_validation"]["leak"]["suspected"]),
        "retry_math_incorrect_final": sum(1 for r in retried if r["final_validation"]["math"]["status"] == "incorrect"),
        "retry_leak_suspected_final": sum(1 for r in retried if r["final_validation"]["leak"]["suspected"]),
        "retry_unverifiable_initial": sum(1 for r in retried if r["initial_validation"]["math"]["status"] == "unverifiable"),
        "retry_unverifiable_final": sum(1 for r in retried if r["final_validation"]["math"]["status"] == "unverifiable"),
        "usage": usage,
        "estimated_cost_usd": usage["input_tokens"] / 1e6 * MODEL_PRICING["input_per_m"] + usage["output_tokens"] / 1e6 * MODEL_PRICING["output_per_m"],
        "prompt_version": PROMPT_VERSION, "model": env["MODEL"],
    }
    Path(args.summary).write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False)[:3000])


if __name__ == "__main__":
    main()
