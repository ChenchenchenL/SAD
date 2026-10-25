"""Run v5 (or repaired v4) diagnosis experiments with separated selection/stop."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
RUN_DIR = HERE.parent
ROOT = RUN_DIR.parents[1]
sys.path.insert(0, str(RUN_DIR))
sys.path.insert(0, str(HERE))

from g0_lib import DESCRIPTIONS_PATH, estimated_cost_usd, load_descriptions, prior_weights  # noqa: E402
from v5_engine import aggregate, bootstrap_diff, bootstrap_mean, build_model, one_shot_episode, run_budget_episode, run_episode, usable_singles  # noqa: E402

CATEGORY_ORDER = ["subtraction", "fractions", "decimals", "negative_numbers", "order_of_operations", "percentages"]

RULES = {
    "one_shot_forced": {"kind": "one_shot", "typed": False},
    "one_shot_typed": {"kind": "one_shot", "typed": True},
    "random_k1": {"kind": "budget", "policy": "random", "k": 1},
    "random_k2": {"kind": "budget", "policy": "random", "k": 2},
    "random_k3": {"kind": "budget", "policy": "random", "k": 3},
    "fixed_k1": {"kind": "budget", "policy": "fixed", "k": 1},
    "fixed_k2": {"kind": "budget", "policy": "fixed", "k": 2},
    "fixed_k3": {"kind": "budget", "policy": "fixed", "k": 3},
    "maxent_k1": {"kind": "budget", "policy": "maxent", "k": 1},
    "maxent_k2": {"kind": "budget", "policy": "maxent", "k": 2},
    "maxent_k3": {"kind": "budget", "policy": "maxent", "k": 3},
    "fixed3": {"kind": "episode", "stop": "fixed3", "selection": "maxent", "on_budget": "force"},
    "posterior_force": {"kind": "episode", "stop": "posterior", "selection": "maxent", "on_budget": "force"},
    "posterior_abstain": {"kind": "episode", "stop": "posterior", "selection": "maxent", "on_budget": "abstain"},
    "entropy_force": {"kind": "episode", "stop": "entropy", "selection": "maxent", "on_budget": "force"},
    "entropy_abstain": {"kind": "episode", "stop": "entropy", "selection": "maxent", "on_budget": "abstain"},
    "stability_maxent": {"kind": "episode", "stop": "stability", "selection": "maxent", "on_budget": "abstain"},
    "stability_targeted": {"kind": "episode", "stop": "stability", "selection": "targeted", "on_budget": "abstain"},
    "stability_mixed_maxent": {"kind": "episode", "stop": "stability_mixed", "selection": "maxent", "on_budget": "abstain"},
    "stability_mixed_targeted": {"kind": "episode", "stop": "stability_mixed", "selection": "targeted", "on_budget": "abstain"},
    "stability_mixed_heldout_maxent": {"kind": "episode", "stop": "stability_mixed_heldout", "selection": "maxent", "on_budget": "abstain"},
    "stability_mixed_heldout_targeted": {"kind": "episode", "stop": "stability_mixed_heldout", "selection": "targeted", "on_budget": "abstain"},
    "stability_mixed_conditional_maxent": {"kind": "episode", "stop": "stability_mixed_conditional", "selection": "maxent", "on_budget": "abstain"},
}
PAIR_STOPS = {"stability_mixed", "stability_mixed_heldout", "stability_mixed_conditional"}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_priors(path: str) -> dict:
    out = {}
    if not path:
        return out
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get("http_status") == 200 and r.get("top10"):
            out[r["key"]] = r
    return out


def episode_to_dict(res, seed: int) -> dict:
    return {
        "rule": res.rule,
        "selection": res.selection,
        "student_type": res.student_type,
        "case_id": res.case_id,
        "family": res.family,
        "category": res.category,
        "true_id": res.true_id,
        "true_pair": res.true_pair,
        "terminal_kind": res.terminal_kind,
        "terminal_id": res.terminal_id,
        "terminal_p": res.terminal_p,
        "n_obs": res.n_obs,
        "n_inquiries": res.n_inquiries,
        "stopped": res.stopped,
        "budget_exhausted": res.budget_exhausted,
        "verifications": res.verifications,
        "correct": res.correct,
        "false_remediation": res.false_remediation,
        "seed": seed,
        "J5": res.n_obs + 5.0 * float(res.false_remediation),
        "J10": res.n_obs + 10.0 * float(res.false_remediation),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", required=True)
    parser.add_argument("--bank-dir", default=str(HERE / "data"))
    parser.add_argument("--bank-prefix", default="bank_v5_")
    parser.add_argument("--priors", default="")
    parser.add_argument("--library-mode", choices=["category", "global"], default="category")
    parser.add_argument("--model-file", default=str(ROOT / "data/library/malrule_descriptions.json"))
    parser.add_argument("--out", required=True)
    parser.add_argument("--episodes", required=True)
    parser.add_argument("--rules", default=",".join(RULES))
    parser.add_argument("--seeds", type=int, default=5)
    parser.add_argument("--eps", type=float, default=0.05)
    parser.add_argument("--max-obs", type=int, default=7)
    parser.add_argument("--bootstrap", type=int, default=2000)
    parser.add_argument("--uniform-prior", action="store_true")
    parser.add_argument("--save-history", action="store_true")
    args = parser.parse_args()

    cases = load_json(Path(args.cases))
    priors = {} if args.uniform_prior else load_priors(args.priors)
    banks = {}
    for cat in CATEGORY_ORDER:
        path = Path(args.bank_dir) / f"{args.bank_prefix}{cat}.json"
        if path.exists():
            banks[cat] = load_json(path)["items"]
    if args.library_mode == "global":
        singles_global = [d["module"] for d in load_descriptions(Path(args.model_file))]
    else:
        singles_global = None

    models_np, models_p = {}, {}
    for cat, items in banks.items():
        singles = [h["id"] for h in load_json(Path(args.bank_dir) / f"{args.bank_prefix}{cat}.json")["hypotheses"]]
        models_np[cat] = build_model(cat, items, singles, with_pairs=False, eps=args.eps)
        models_p[cat] = build_model(cat, items, singles, with_pairs=True, eps=args.eps)
    if args.library_mode == "global":
        # one model per category containing all library hypotheses, no pairs
        models_global = {}
        for cat, items in banks.items():
            models_global[cat] = build_model(cat, items, singles_global, with_pairs=False, eps=args.eps)

    rule_ids = [r.strip() for r in args.rules.split(",") if r.strip()]
    results = defaultdict(list)
    episodes = []
    skipped = Counter()
    for ci, case in enumerate(cases):
        prior_row = priors.get(case.get("key"))
        if not args.uniform_prior and prior_row is None:
            skipped["missing_prior"] += 1
            continue
        cat = case["category"]
        top10 = (prior_row or {}).get("top10") or []
        if args.library_mode == "global":
            singles = singles_global
            model_np = models_global[cat]
            weights = prior_weights(top10, singles) if top10 else {h: 1.0 / len(singles) for h in singles}
            prior_np = model_np.prior(weights)
            model_p = None
            prior_p = None
        else:
            singles = models_np[cat].singles
            weights = prior_weights(top10, singles) if top10 else {h: 1.0 / len(singles) for h in singles}
            model_np = models_np[cat]
            prior_np = model_np.prior(weights)
            prior_p = models_p[cat].prior(weights)
            model_p = models_p[cat]
        for st in ("stable", "slip", "mixed"):
            partner = None
            if st == "mixed":
                if args.library_mode == "global":
                    skipped["global_no_pair_model"] += 1
                    continue
                options = [h for h in usable_singles(model_p, 1) if h != case["true_id"]]
                if not options:
                    skipped["mixed_no_partner"] += 1
                    continue
                # partner deterministic by case/seed; engine chooses if passed None
            for seed in range(args.seeds):
                for rid in rule_ids:
                    spec = RULES[rid]
                    use_pairs = spec.get("stop") in PAIR_STOPS
                    if args.library_mode == "global" and use_pairs:
                        skipped["global_no_pair_rule"] += 1
                        continue
                    model = (model_p if use_pairs else model_np) if args.library_mode == "category" else model_np
                    prior = (prior_p if use_pairs else prior_np) if args.library_mode == "category" else prior_np
                    if spec["kind"] == "one_shot":
                        res = one_shot_episode(model, prior, case, st, partner=partner, seed=seed,
                                               typed=spec["typed"], prior_meta=prior_row)
                    elif spec["kind"] == "budget":
                        res = run_budget_episode(model, prior, case, st, spec["policy"], spec["k"],
                                                 partner=partner, seed=seed, eps=args.eps)
                    else:
                        res = run_episode(model, prior, case, st, spec["stop"], selection=spec["selection"],
                                          on_budget=spec["on_budget"], partner=partner, seed=seed,
                                          eps=args.eps, max_obs=args.max_obs)
                    if res is None:
                        skipped[f"{rid}/{st}"] += 1
                        continue
                    results[(rid, st)].append(res)
                    ed = episode_to_dict(res, seed)
                    if args.save_history:
                        ed["history"] = res.history
                    episodes.append(ed)

    aggregates = {}
    for (rid, st), rows in results.items():
        aggregates[f"{rid}/{st}"] = aggregate(rows)

    cis = {}
    for (rid, st), rows in results.items():
        cis[f"{rid}/{st}"] = {}
        for metric in ("correct", "false", "n_obs", "n_inquiries", "J5", "J10"):
            point, lo, hi = bootstrap_mean(rows, metric, n_boot=args.bootstrap)
            cis[f"{rid}/{st}"][metric] = {"mean": point, "ci_low": lo, "ci_high": hi}

    contrasts = {}
    primary_contrasts = [
        ("one_shot_typed", "one_shot_forced"),
        ("maxent_k3", "random_k3"),
        ("maxent_k3", "fixed_k3"),
        ("stability_mixed_maxent", "fixed3"),
        ("stability_mixed_maxent", "stability_maxent"),
        ("stability_targeted", "stability_maxent"),
        ("stability_mixed_targeted", "stability_mixed_maxent"),
        ("stability_mixed_heldout_maxent", "stability_mixed_maxent"),
    ]
    for a, b in primary_contrasts:
        for st in ("stable", "slip", "mixed"):
            if (a, st) not in results or (b, st) not in results:
                continue
            key = f"{a}_minus_{b}/{st}"
            contrasts[key] = {}
            for metric in ("correct", "false", "n_obs", "n_inquiries", "J5", "J10"):
                point, lo, hi = bootstrap_diff(results[(a, st)], results[(b, st)], metric, n_boot=args.bootstrap)
                contrasts[key][metric] = {"diff": point, "ci_low": lo, "ci_high": hi}

    # category breakdown for the primary rule
    per_category = {}
    primary = "stability_mixed_maxent"
    for cat in set(r.category for rows in results.values() for r in rows):
        for (rid, st), rows in results.items():
            sub = [r for r in rows if r.category == cat]
            if sub:
                per_category.setdefault(f"{rid}/{st}", {})[cat] = aggregate(sub)

    # J sensitivity to student-type proportions
    j_sensitivity = {}
    for rid in rule_ids:
        vals = {}
        for st in ("stable", "slip", "mixed"):
            rows = results.get((rid, st))
            vals[st] = {"J5": aggregate(rows)["J_lambda5"] if rows else None,
                        "J10": aggregate(rows)["J_lambda10"] if rows else None}
        def weighted(ps):
            out = {}
            for lam in (5, 10):
                total = sum(w * (vals.get(st, {}).get(f"J{lam}") or 0) for st, w in ps.items() if vals.get(st, {}).get(f"J{lam}") is not None)
                norm = sum(w for st, w in ps.items() if vals.get(st, {}).get(f"J{lam}") is not None)
                out[f"J{lam}"] = total / norm if norm else None
            return out
        j_sensitivity[rid] = {
            "per_type": vals,
            "stable_slip_equal": weighted({"stable": .5, "slip": .5, "mixed": 0}),
            "stable_heavy_70_30": weighted({"stable": .7, "slip": .3, "mixed": 0}),
            "slip_heavy_30_70": weighted({"stable": .3, "slip": .7, "mixed": 0}),
            "all_50_25_25": weighted({"stable": .5, "slip": .25, "mixed": .25}),
        }

    api_cost = None
    if priors:
        usage = {
            "input_tokens": sum((p.get("usage", {}) or {}).get("input_tokens") or 0 for p in priors.values()),
            "output_tokens": sum((p.get("usage", {}) or {}).get("output_tokens") or 0 for p in priors.values()),
        }
        total_cost = estimated_cost_usd(usage)
        episodes_per_case = args.seeds * len([s for s in ("stable", "slip", "mixed") if any(True for r in results.values() if r[1] == s)])
        api_cost = {
            "prior_cases": len(priors),
            "input_tokens": usage["input_tokens"],
            "output_tokens": usage["output_tokens"],
            "estimated_cost_usd_total": total_cost,
            "estimated_cost_usd_per_case": total_cost / len(priors) if priors else None,
            # The same prior is amortised across every rule/type/seed; report it explicitly.
            "estimated_cost_usd_per_prior_case_per_rule": None,
        }

    summary = {
        "settings": vars(args),
        "n_cases": len(cases),
        "n_prior_rows": len(priors),
        "skipped": dict(skipped),
        "aggregates": aggregates,
        "case_clustered_CIs": cis,
        "contrasts": contrasts,
        "per_category": per_category,
        "j_sensitivity": j_sensitivity,
        "api_cost": api_cost,
        "hidden_label_boundary": {
            "student_type_true_id_true_pair_allowed_for": ["student simulation", "sampling strata", "final scoring"],
            "diagnosis_and_pipeline_prompt_reads_hidden_labels": False,
        },
    }
    Path(args.out).write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    Path(args.episodes).write_text(json.dumps(episodes, ensure_ascii=False), encoding="utf-8")
    print("episodes", len(episodes), "rules/types", len(results))
    for rid in rule_ids:
        parts = []
        for st in ("stable", "slip", "mixed"):
            a = aggregates.get(f"{rid}/{st}")
            if not a:
                continue
            if st == "stable":
                parts.append(f"stable correct={a['stable_correct_diagnosed']:.3f} obs={a['avg_obs']:.2f}")
            elif st == "slip":
                parts.append(f"slip err={a['slip_error_rate']:.3f} none={a['slip_explicit_none_rate']:.3f} abst={a['slip_abstain_rate']:.3f}")
            else:
                parts.append(f"mixed err={a['mixed_error_rate']:.3f} det={a['mixed_detected_rate']:.3f}")
        print(rid, " | ".join(parts))


if __name__ == "__main__":
    main()
