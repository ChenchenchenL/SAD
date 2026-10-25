"""Collect LLM priors for v5 authored cases with version-aware cache keys."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import threading
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import sys

HERE = Path(__file__).resolve().parent
RUN_DIR = HERE.parent
os.environ.setdefault("SIM_ROOT", str(HERE.parents[2]))
sys.path.insert(0, str(RUN_DIR))

from g0_lib import (
    CATEGORIES,
    DESCRIPTIONS_PATH,
    ENV_PATH,
    SYSTEM_PROMPT,
    build_library_text,
    build_prior_prompt,
    call_anthropic,
    estimated_cost_usd,
    load_descriptions,
    load_env,
    parse_prior,
)

LOCK = threading.Lock()
PROMPT_VERSION = "v6_independent_prior_2026-10-21"


def cache_key(case_key: str, model: str, mode: str, prompt_sha: str) -> str:
    return hashlib.sha256(f"{case_key}|{model}|{mode}|{prompt_sha}|{PROMPT_VERSION}".encode()).hexdigest()[:32]


def load_cached(path: Path, model: str, mode: str) -> dict:
    if not path.exists():
        return {}
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("http_status") == 200 and row.get("parsed_top10") and row.get("model_requested") == model and row.get("library_mode") == mode:
            # Last row wins, matching run.py's loader. The old v6 summary used
            # first-row-wins; v6b keeps the loader consistent across summary and run.
            out[row["cache_key"]] = row
    return out


def build_nodomain_prompt(problem: str, answer: str, correct: str, library: str) -> str:
    return f"""A student solved the problem below and produced the final answer shown.
Their reasoning is not visible.

PROBLEM:
{problem}

CORRECT ANSWER:
{correct}

STUDENT FINAL ANSWER:
{answer}

MISCONCEPTION LIBRARY ({library.count(chr(10)) + 1} entries; identifier | name: description):
{library}

Rank the 10 misconceptions from the library that most plausibly explain the student's answer.
Do not assume any domain, topic, or category. Consider the arithmetic relationship between
the operands, correct answer, and student answer. Include every plausible candidate consistent
with the answer. Also state whether the evidence looks like one stable misconception, a mixture,
a one-off slip, or unsure. Use only identifiers from the library. Do not solve the problem.
Return strict JSON:
{{"top10": ["id1", "id2", "... up to 10"], "stable_or_mixed": "stable|mixed|slip|unsure", "confidence": 0.0, "reason": "one sentence"}}"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--library-mode", choices=["category", "full", "full_nodomain"], default="category")
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--dataset-version", default="v6b")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    env = load_env(ENV_PATH)
    descriptions = load_descriptions(DESCRIPTIONS_PATH)
    valid_ids = [d["module"] for d in descriptions]
    if args.library_mode == "category":
        library = {cat: build_library_text([d for d in descriptions if d["category"] == cat]) for cat in CATEGORIES}
    else:
        library = build_library_text(descriptions)
    cases = json.loads(Path(args.cases).read_text(encoding="utf-8"))
    rows = []
    for case in cases:
        if args.library_mode == "full_nodomain":
            user = build_nodomain_prompt(case["problem"], case["answer"], case["correct"], library)
        else:
            user = build_prior_prompt(case["problem"], case["answer"], case["correct"], case["category"],
                                      library if args.library_mode == "full" else library[case["category"]])
        prompt_sha = hashlib.sha256(user.encode("utf-8")).hexdigest()[:16]
        ck = cache_key(case["key"], env["MODEL"], args.library_mode, prompt_sha)
        rows.append((case, user, prompt_sha, ck))

    out_path = Path(args.out)
    cached = load_cached(out_path, env["MODEL"], args.library_mode)
    todo = [x for x in rows if x[3] not in cached]
    if args.limit:
        todo = todo[:args.limit]
    cat_tokens = sum(len(library[case["category"]]) if args.library_mode == "category" else len(library)
                     for case, _, _, _ in rows) if args.library_mode == "category" else sum(len(library) for _ in rows)
    print(f"cases={len(rows)} cached={len(cached)} todo={len(todo)} model={env['MODEL']} mode={args.library_mode}")
    print(f"approx_library_chars={cat_tokens} rough_input_tokens={cat_tokens // 3}")
    if args.dry_run:
        return

    def fetch(item):
        case, user, prompt_sha, ck = item
        result = call_anthropic(env["API_KEY"], env["BASE_URL"], env["MODEL"], SYSTEM_PROMPT, user)
        parsed = parse_prior(result["text"], valid_ids)
        usage = dict(result.get("usage") or {})
        calls = 1
        if not parsed["parsed"] and result["http_status"] == 200:
            user2 = user + "\n\nYour previous reply was not valid JSON. Return only the JSON object with the required keys."
            r2 = call_anthropic(env["API_KEY"], env["BASE_URL"], env["MODEL"], SYSTEM_PROMPT, user2)
            parsed = parse_prior(r2["text"], valid_ids)
            result = r2
            usage = {
                "input_tokens": (usage.get("input_tokens") or 0) + (r2.get("usage", {}).get("input_tokens") or 0),
                "output_tokens": (usage.get("output_tokens") or 0) + (r2.get("usage", {}).get("output_tokens") or 0),
            }
            calls = 2
        return {
            **case, "cache_key": ck, "library_mode": args.library_mode,
            "dataset_version": args.dataset_version,
            "prompt_version": PROMPT_VERSION, "model_requested": env["MODEL"],
            "top10": parsed["top10"], "parsed_top10": parsed["parsed"],
            "stable_or_mixed": parsed["stable_or_mixed"], "confidence": parsed["confidence"],
            "reason": parsed["reason"], "http_status": result["http_status"], "usage": usage,
            "calls": calls, "model": result.get("model"), "response_text": result["text"][:20000],
            "prompt_sha": prompt_sha,
        }

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(fetch, x): x for x in todo}
        for i, fut in enumerate(as_completed(futures), 1):
            row = fut.result()
            with LOCK:
                with out_path.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(row, ensure_ascii=False) + "\n")
            print(f"[{i}/{len(todo)}] {row['case_id']} http={row['http_status']} top1={row['top10'][:1]} true={row['true_id']}")

    all_rows, by_key = [], {}
    for line in out_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            if r.get("http_status") == 200 and r.get("parsed_top10") and r.get("model_requested") == env["MODEL"] and r.get("library_mode") == args.library_mode:
                all_rows.append(r)
                # Last row wins, matching run.py's loader.
                by_key[r["cache_key"]] = r
    # Multiple cases can share one (problem, answer, correct) prior. Metrics are
    # case-level; usage is summed over all successful API rows (not deduplicated).
    by_case_key = {r["key"]: r for r in by_key.values()}
    ok = [(c, by_case_key[c["key"]]) for c in cases if c["key"] in by_case_key]
    n_ok = len(ok)
    hit10 = sum(1 for c, r in ok if c["true_id"] in (r["top10"] or []))
    hit1 = sum(1 for c, r in ok if r["top10"] and r["top10"][0] == c["true_id"])
    cat_top10 = sum(1 for c, r in ok if c["true_id"] in
                    [x for x in r["top10"] if x.split(".")[0] == c["category"]])
    cat_top1 = sum(1 for c, r in ok if
                   next((x for x in r["top10"] if x.split(".")[0] == c["category"]), None) == c["true_id"])
    usage = {
        "input_tokens": sum((r.get("usage", {}) or {}).get("input_tokens") or 0 for r in all_rows),
        "output_tokens": sum((r.get("usage", {}) or {}).get("output_tokens") or 0 for r in all_rows),
    }
    summary = {
        "cases": args.cases, "priors": args.out, "library_mode": args.library_mode,
        "dataset_version": args.dataset_version,
        "model": env["MODEL"], "prompt_version": PROMPT_VERSION,
        "n_ok": n_ok, "n_successful_rows": len(all_rows), "n_unique_prior_keys": len(by_key),
        "top10_global_recall": hit10 / n_ok if n_ok else None,
        "top1_global": hit1 / n_ok if n_ok else None,
        "top10_category_recall": cat_top10 / n_ok if n_ok else None,
        "top1_category_rank": cat_top1 / n_ok if n_ok else None,
        "type_counts": dict(Counter(r.get("stable_or_mixed") for c, r in ok)),
        "usage": usage, "estimated_cost_usd": estimated_cost_usd(usage),
    }
    Path(args.summary).write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
