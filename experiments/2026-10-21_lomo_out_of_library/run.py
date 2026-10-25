from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import sys
import time
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(HERE / "src"))

from sim_workbench.provenance import snapshot, write_manifest  # noqa: E402

import ablation  # noqa: E402
import lomo  # noqa: E402
import v5_engine as eng  # noqa: E402

CATEGORY_ORDER = [
    "subtraction",
    "fractions",
    "decimals",
    "negative_numbers",
    "order_of_operations",
    "percentages",
]

CONTRAST_PAIRS = [
    ("posterior_plus_E", "posterior_only"),
    ("stability_mixed_reference", "posterior_only"),
    ("stability_mixed_reference", "posterior_plus_E"),
]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_priors(path: Path) -> dict:
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("http_status") == 200 and row.get("top10"):
            out[row["key"]] = row
    return out


def fmt_pct(cell: dict, ci: bool = True) -> str:
    mean = 100.0 * cell["mean"]
    if ci:
        return f"{mean:.1f} [{100.0 * cell['ci_low']:.1f}, {100.0 * cell['ci_high']:.1f}]"
    return f"{mean:.1f}"


def fmt_num(cell: dict, ci: bool = False) -> str:
    mean = cell["mean"]
    if ci:
        return f"{mean:.2f} [{cell['ci_low']:.2f}, {cell['ci_high']:.2f}]"
    return f"{mean:.2f}"


def fmt_diff(cell: dict, pct: bool) -> str:
    scale = 100.0 if pct else 1.0
    return f"{scale * cell['mean']:+.1f} [{scale * cell['ci_low']:+.1f}, {scale * cell['ci_high']:+.1f}]"


def summarize_arm(rows: list[dict], cb) -> dict:
    out = {}
    for metric in lomo.METRICS:
        out[metric] = cb.mean_ci(lomo.case_means(rows, metric))
    out["n_cases"] = len({e["case_id"] for e in rows})
    out["n_episodes"] = len(rows)
    return out


def overlap_bucket(count: int | None) -> str:
    if count is None:
        return "unknown"
    if count == 0:
        return "0"
    if count == 1:
        return "1"
    return ">=2"


def render_tables(summary: dict) -> str:
    agg = summary["aggregates"]
    arms = summary["settings"]["arms"]
    types = summary["settings"]["student_types"]
    eps_val = float(summary["settings"]["eps"])

    lines = [
        "# LOMO out-of-library student experiment",
        "",
        f"eps={eps_val:g}; removed-rule students (stable_ool: deterministic; "
        "slip_ool: eps random errors on top of the removed rule); MaxEnt "
        "selection; max_obs=7; 5 seeds; frozen category-conditioned cached "
        "prior with the removed rule dropped from the weights. Every "
        "single/pair/mixed terminal is a false commitment because the true "
        "rule is not in the hypothesis space.",
        "",
        "## Main table",
        "",
        "| arm | student | false commit (any) | single commit | pair/mixed commit | none | abstain | inquiries | J5 |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for arm in arms:
        for st in types:
            a = agg.get(arm, {}).get(st)
            if not a:
                continue
            lines.append(
                f"| {arm} | {st} | {fmt_pct(a['false_commit'])} | "
                f"{fmt_pct(a['false_single'], ci=False)} | "
                f"{fmt_pct(a['false_pair_mixed'], ci=False)} | "
                f"{fmt_pct(a['none'], ci=False)} | {fmt_pct(a['abstain'], ci=False)} | "
                f"{fmt_num(a['n_inquiries'])} | {fmt_num(a['J5'])} |"
            )
    lines += [
        "",
        "Rates are percentages of episodes; bracketed intervals are 95% "
        "template-family cluster bootstrap intervals (2000 draws, with "
        "replacement and multiplicity). false commit = any library commitment "
        "(single, pair, or mixed terminal). none = explicit no-in-library-"
        "stable-misconception output; abstain = insufficient evidence.",
        "",
        "## Paired contrasts (same case and seed)",
        "",
        "| contrast | student | false commit | none | abstain | inquiries | J5 |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for arm_a, arm_b in CONTRAST_PAIRS:
        for st in types:
            key = f"{arm_a} - {arm_b}/{st}"
            c = summary["contrasts"].get(key)
            if not c:
                continue
            lines.append(
                f"| {arm_a} - {arm_b} | {st} | {fmt_diff(c['false_commit'], True)} | "
                f"{fmt_diff(c['none'], True)} | {fmt_diff(c['abstain'], True)} | "
                f"{fmt_diff(c['n_inquiries'], False)} | {fmt_diff(c['J5'], False)} |"
            )
    lines += [
        "",
        "Negative false-commit differences mean the first arm is safer on "
        "out-of-library students.",
        "",
        "## Gate counterfactual at single stops",
        "",
        "Gate states at the terminal step of episodes whose terminal is a "
        "single commitment. `E pass` = at least two observed consistent wrong "
        "answers matching the committed rule; `LR pass` = slip likelihood "
        "ratio >= 10; `pair guard pass` = committed single beats the top pair.",
        "",
        "| student | arm | n single stops | E pass | LR pass | pair guard pass | any gate fail |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for st in types:
        for arm in arms:
            g = summary["gate_counterfactual"].get(st, {}).get(arm)
            if not g or not g["n_single_stops"]:
                continue
            def p(v):
                return "—" if v is None else f"{100.0 * v:.1f}"
            lines.append(
                f"| {st} | {arm} | {g['n_single_stops']} | {p(g['pct_E_pass'])} | "
                f"{p(g['pct_LR_pass'])} | {p(g['pct_pair_guard_pass'])} | "
                f"{p(g['pct_any_gate_fail'])} |"
            )
    lines += [
        "",
        f"Minimum log slip-LR at a posterior_only single stop: "
        f"{summary['gate_counterfactual_min_log_lr']}",
        "",
        "## Misdiagnosis targets (stable_ool, single terminals)",
        "",
        "Which library rule receives the false single diagnosis.",
        "",
        "| arm | top blamed rules (count) |",
        "|---|---|",
    ]
    for arm in arms:
        t = summary["targets"].get(arm, {}).get("stable_ool", {}).get("single_targets", {})
        if not t:
            lines.append(f"| {arm} | — |")
            continue
        top = ", ".join(f"{k} ({v})" for k, v in list(t.items())[:6])
        lines.append(f"| {arm} | {top} |")
    lines += [
        "",
        "## Removed-rule overlap vs false commitment (stable_ool)",
        "",
        "Labels bucketed by the maximum number of triggering items shared "
        "with any remaining rule in the category bank.",
        "",
        "| arm | max-overlap bucket | n labels | n episodes | false commit | none | abstain |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for arm in arms:
        for st in types:
            buckets = summary["overlap_buckets"].get(arm, {}).get(st, {})
            for b in ("0", "1", ">=2"):
                cell = buckets.get(b)
                if not cell:
                    continue
                lines.append(
                    f"| {arm} | {st} | {b} | {cell['n_labels']} | {cell['n_episodes']} | "
                    f"{fmt_pct(cell['false_commit'], ci=False)} | "
                    f"{fmt_pct(cell['none'], ci=False)} | {fmt_pct(cell['abstain'], ci=False)} |"
                )
    lines += [
        "",
        "## False commitment by category (point estimates, stable_ool)",
        "",
        "| category | posterior_only | posterior_plus_E | stability_mixed_reference |",
        "|---|---:|---:|---:|",
    ]
    for cat in CATEGORY_ORDER:
        cells = []
        for arm in arms:
            v = summary["per_category"].get(arm, {}).get("stable_ool", {}).get(cat, {}).get("false_commit")
            cells.append(f"{100.0 * v:.1f}" if v is not None else "—")
        lines.append(f"| {cat} | " + " | ".join(cells) + " |")
    lines += [
        "",
        "Category cells are exploratory (12-18 cases per category).",
        "",
        "## Scope",
        "",
        "- Post-hoc experiment on the frozen v5 protocol-valid 87-case test "
        "set; no thresholds were tuned on these results.",
        "- The LLM prior cache was computed while the removed rule was still "
        "in the prompt library; the rule is dropped from the weights and the "
        "remaining ranks are kept, which slightly flattens the prior relative "
        "to a true out-of-library call.",
        "- Every commitment is false by construction, so correct-diagnosis "
        "rates are undefined here; the question is how the system fails.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(HERE / "config.json"))
    parser.add_argument("--run-name", default="lomo")
    args = parser.parse_args()

    config_path = Path(args.config).resolve()
    cfg = load_json(config_path)
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = HERE / "runs" / f"{stamp}_{args.run_name}"
    run_dir.mkdir(parents=True, exist_ok=False)
    (run_dir / "outputs").mkdir()
    (run_dir / "logs").mkdir()
    shutil.copy2(config_path, run_dir / "config.snapshot.json")

    inputs = [
        config_path,
        HERE / cfg["cases"],
        HERE / cfg["priors"],
        *[HERE / cfg["bank_dir"] / f"{cfg['bank_prefix']}{cat}.json" for cat in CATEGORY_ORDER],
        HERE / "src" / "g0_lib.py",
        HERE / "src" / "v5_engine.py",
        HERE / "src" / "ablation.py",
        HERE / "src" / "lomo.py",
        HERE / "run.py",
    ]
    manifest = write_manifest(
        run_dir / "manifest.json",
        {
            "experiment": HERE.name,
            "run_id": run_dir.name,
            "config": str(config_path.relative_to(ROOT)),
            "inputs": snapshot(inputs),
        },
    )

    cases = load_json(HERE / cfg["cases"])
    priors = load_priors(HERE / cfg["priors"])
    family_of_case = {c["case_id"]: c["template_family"] for c in cases}

    banks = {}
    singles_full = {}
    for cat in CATEGORY_ORDER:
        bank = load_json(HERE / cfg["bank_dir"] / f"{cfg['bank_prefix']}{cat}.json")
        banks[cat] = bank
        singles_full[cat] = lomo.effective_singles(bank)

    overlap_report = lomo.uniqueness_and_overlap(banks, cases)
    if overlap_report["violations"]:
        summary = {
            "status": "blocked_uniqueness_violation",
            "overlap_report": overlap_report,
        }
        (run_dir / "outputs" / "summary.json").write_text(
            json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print("BLOCKED: uniqueness violations", overlap_report["violations"])
        return 1

    arms = list(cfg["arms"])
    types = list(cfg["student_types"])
    seeds = int(cfg["seeds"])
    eps = float(cfg["eps"])
    max_obs = int(cfg["max_obs"])

    model_cache: dict[tuple[str, str], object] = {}

    def model_for(cat: str, removed: str):
        key = (cat, removed)
        if key not in model_cache:
            singles = [h for h in singles_full[cat] if h != removed]
            model_cache[key] = eng.build_model(
                cat, banks[cat]["items"], singles, with_pairs=True, eps=eps
            )
        return model_cache[key]

    episodes = []
    skipped: dict[str, int] = defaultdict(int)
    started = time.time()

    for case in cases:
        prior_row = priors.get(case["key"])
        if prior_row is None:
            skipped["missing_prior"] += 1
            continue
        cat = case["category"]
        removed = case["true_id"]
        model = model_for(cat, removed)
        singles = [h for h in singles_full[cat] if h != removed]
        prior = lomo.build_prior_for_case(prior_row, singles, model)
        for st in types:
            for seed in range(seeds):
                for arm in arms:
                    res = lomo.run_episode_ool(
                        model, prior, case, st, arm, seed=seed, eps=eps, max_obs=max_obs
                    )
                    if res is None:
                        skipped[f"{arm}/{st}"] += 1
                        continue
                    episodes.append(lomo.episode_to_dict(res, seed))

    cb = ablation.ClusterBoot(
        family_of_case, n_boot=int(cfg["bootstrap"]), seed=int(cfg["bootstrap_seed"])
    )

    by_arm_type = defaultdict(list)
    for e in episodes:
        by_arm_type[(e["arm"], e["student_type"])].append(e)

    aggregates = {arm: {} for arm in arms}
    for arm in arms:
        for st in types:
            rows = by_arm_type.get((arm, st), [])
            if rows:
                aggregates[arm][st] = summarize_arm(rows, cb)

    contrasts = {}
    for arm_a, arm_b in CONTRAST_PAIRS:
        for st in types:
            a = by_arm_type.get((arm_a, st))
            b = by_arm_type.get((arm_b, st))
            if not a or not b:
                continue
            key = f"{arm_a} - {arm_b}/{st}"
            contrasts[key] = {
                m: cb.diff_ci(lomo.case_means(a, m), lomo.case_means(b, m))
                for m in lomo.METRICS
            }

    gate_cf = {st: {} for st in types}
    min_lr = None
    for st in types:
        rows = by_arm_type.get(("posterior_only", st), [])
        cf = lomo.gate_counterfactual(rows, arms=tuple(arms))
        gate_cf[st] = cf
        val = cf.get("posterior_only", {}).get("min_log_lr_at_stop")
        if val is not None:
            min_lr = val if min_lr is None else min(min_lr, val)

    targets = {}
    for arm in arms:
        for st in types:
            rows = by_arm_type.get((arm, st), [])
            if rows:
                targets.setdefault(arm, {})[st] = lomo.terminal_targets(rows)

    overlap_buckets = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))
    for e in episodes:
        info = overlap_report["labels"][e["removed_rule"]]
        overlap_buckets[e["arm"]][e["student_type"]][overlap_bucket(info["max_overlap_count"])]["episodes"].append(e)
    bucket_out = {}
    for arm in arms:
        for st in types:
            for b, cell in overlap_buckets.get(arm, {}).get(st, {}).items():
                rows = cell["episodes"]
                labels = {e["removed_rule"] for e in rows}
                bucket_out.setdefault(arm, {}).setdefault(st, {})[b] = {
                    "n_labels": len(labels),
                    "n_episodes": len(rows),
                    "false_commit": {
                        "mean": float(np.mean([e["false_commit"] for e in rows])),
                    },
                    "none": {"mean": float(np.mean([e["none"] for e in rows]))},
                    "abstain": {"mean": float(np.mean([e["abstain"] for e in rows]))},
                }

    per_category = {}
    for (arm, st), rows in by_arm_type.items():
        for cat in CATEGORY_ORDER:
            sub = [e for e in rows if e["category"] == cat]
            if sub:
                per_category.setdefault(arm, {}).setdefault(st, {})[cat] = {
                    "n_episodes": len(sub),
                    "false_commit": float(np.mean([e["false_commit"] for e in sub])),
                    "none": float(np.mean([e["none"] for e in sub])),
                    "abstain": float(np.mean([e["abstain"] for e in sub])),
                }

    fooled_rows = {}
    for arm in arms:
        for st in types:
            rows = by_arm_type.get((arm, st), [])
            if rows:
                fooled_rows.setdefault(arm, {})[st] = lomo.fooled_by_label(rows, overlap_report)

    n_labels = len({c["true_id"] for c in cases})
    summary = {
        "settings": {
            "experiment": cfg["experiment"],
            "cases": cfg["cases"],
            "priors": cfg["priors"],
            "seeds": seeds,
            "eps": eps,
            "max_obs": max_obs,
            "arms": arms,
            "student_types": types,
            "posterior_thresholds": ablation.POSTERIOR,
            "min_consistent_wrong": ablation.MIN_CONSISTENT_WRONG,
            "lr_slip_threshold": ablation.LR_SLIP_THRESHOLD,
            "pair_guard_margin": ablation.PAIR_GUARD_MARGIN,
            "bootstrap": int(cfg["bootstrap"]),
            "bootstrap_seed": int(cfg["bootstrap_seed"]),
            "prior_source": (
                "frozen deepseek-v4.1-flash category-conditioned cached prior; "
                "removed rule dropped from weights, remaining ranks kept"
            ),
            "hidden_label_boundary": "removed rule used only for simulation and scoring",
        },
        "status": "ok",
        "duration_seconds": round(time.time() - started, 2),
        "manifest": manifest,
        "skipped": dict(skipped),
        "n_cases": len(cases),
        "n_removed_labels": n_labels,
        "n_episodes": len(episodes),
        "uniqueness_check": {
            "n_labels_checked": len(overlap_report["labels"]),
            "violations": overlap_report["violations"],
            "labels_with_max_overlap_ge2": sum(
                1 for v in overlap_report["labels"].values() if v["max_overlap_count"] >= 2
            ),
        },
        "aggregates": aggregates,
        "contrasts": contrasts,
        "gate_counterfactual": gate_cf,
        "gate_counterfactual_min_log_lr": min_lr,
        "targets": targets,
        "overlap_buckets": bucket_out,
        "per_category": per_category,
        "fooled_by_label": fooled_rows,
    }

    out_dir = run_dir / "outputs"
    (out_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (out_dir / "episodes.json").write_text(
        json.dumps(episodes, ensure_ascii=False), encoding="utf-8"
    )
    (out_dir / "overlap_report.json").write_text(
        json.dumps(overlap_report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (out_dir / "tables.md").write_text(render_tables(summary), encoding="utf-8")
    (out_dir / "status.json").write_text(
        json.dumps(
            {
                "status": "ok",
                "run_id": run_dir.name,
                "episodes": len(episodes),
                "duration_seconds": summary["duration_seconds"],
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print(f"wrote {run_dir.relative_to(ROOT)}")
    print(f"episodes={len(episodes)} skipped={dict(skipped)} labels={n_labels}")
    for arm in arms:
        for st in types:
            a = aggregates.get(arm, {}).get(st)
            if not a:
                continue
            print(
                f"{arm}/{st}: false_commit={a['false_commit']['mean']:.3f} "
                f"none={a['none']['mean']:.3f} abstain={a['abstain']['mean']:.3f} "
                f"inq={a['n_inquiries']['mean']:.2f}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
