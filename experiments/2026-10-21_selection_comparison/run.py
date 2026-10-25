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
import selection as sel  # noqa: E402
import v5_engine as eng  # noqa: E402
from g0_lib import prior_weights  # noqa: E402

CATEGORY_ORDER = [
    "subtraction",
    "fractions",
    "decimals",
    "negative_numbers",
    "order_of_operations",
    "percentages",
]

CONTRAST_PAIRS = [
    ("sm_ig", "sm_maxent"),
    ("sm_random", "sm_maxent"),
    ("sm_fixed_order", "sm_maxent"),
    ("sm_ig", "sm_random"),
    ("k3_ig", "k3_maxent"),
    ("k3_random", "k3_maxent"),
    ("k3_fixed_order", "k3_maxent"),
    ("k3_random_legacy", "k3_maxent"),
    ("k3_ig", "k3_random"),
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
    for metric in sel.METRICS:
        out[metric] = cb.mean_ci(_case_means(rows, metric))
    out["n_cases"] = len({e["case_id"] for e in rows})
    out["n_episodes"] = len(rows)
    return out


def _case_means(episodes: list[dict], metric: str) -> dict:
    by_case = defaultdict(list)
    for e in episodes:
        by_case[e["case_id"]].append(sel.episode_metric(e, metric))
    return {cid: float(np.mean(vals)) for cid, vals in by_case.items()}


def render_tables(summary: dict) -> str:
    agg = summary["aggregates"]
    lines = [
        "# Selection-strategy comparison",
        "",
        "Unified per block: frozen v5 category prior, same hypothesis space, "
        "same outcomes (common random numbers), eps=0.05, 5 seeds. Adaptive "
        "block = full SM stopping with max_obs=7 and pair-augmented space; "
        "fixed block = frozen Fixed-3 convention (no pairs, exactly 3 "
        "inquiries, posterior commit, never abstain).",
        "",
        "## Adaptive full SM (max_obs=7)",
        "",
        "| strategy | stable correct | stable correct stop | stable false single | stable pair/mixed | slip false remediation | slip none | slip abstain | stable inquiries | slip inquiries | stable J5 | slip J5 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for arm in summary["settings"]["adaptive_arms"]:
        s = agg[arm]["stable"]
        p = agg[arm]["slip"]
        lines.append(
            f"| {arm} | {fmt_pct(s['correct'])} | {fmt_pct(s['correct_stop'], ci=False)} | "
            f"{fmt_pct(s['false'], ci=False)} | {fmt_pct(s['pair_mixed'], ci=False)} | "
            f"{fmt_pct(p['false'])} | {fmt_pct(p['none'], ci=False)} | {fmt_pct(p['abstain'], ci=False)} | "
            f"{fmt_num(s['n_inquiries'])} | {fmt_num(p['n_inquiries'])} | "
            f"{fmt_num(s['J5'])} | {fmt_num(p['J5'])} |"
        )
    lines += [
        "",
        "## Fixed budget k=3 (Fixed-3 convention)",
        "",
        "| strategy | stable correct | stable false single | stable pair/mixed | slip false remediation | slip none | stable J5 | slip J5 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for arm in summary["settings"]["k3_arms"]:
        s = agg[arm]["stable"]
        p = agg[arm]["slip"]
        lines.append(
            f"| {arm} | {fmt_pct(s['correct'])} | {fmt_pct(s['false'])} | "
            f"{fmt_pct(s['pair_mixed'], ci=False)} | {fmt_pct(p['false'])} | "
            f"{fmt_pct(p['none'], ci=False)} | {fmt_num(s['J5'])} | {fmt_num(p['J5'])} |"
        )
    lines += [
        "",
        "Rates are percentages; bracketed intervals are 95% template-family "
        "cluster bootstrap intervals (2000 draws, with replacement and "
        "multiplicity). `k3_random_legacy` is the historical reseeded-random "
        "implementation, kept only to reproduce the frozen numbers and "
        "measure the correction; it is not a standard random baseline.",
        "",
        "## Paired contrasts (same case and seed)",
        "",
        "| contrast | stable correct | slip false | slip none | slip abstain | stable inquiries | slip inquiries | slip J5 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for arm_a, arm_b in CONTRAST_PAIRS:
        c = summary["contrasts"].get(f"{arm_a} - {arm_b}")
        if not c:
            continue
        lines.append(
            f"| {arm_a} − {arm_b} | {fmt_diff(c['stable/correct'], True)} | "
            f"{fmt_diff(c['slip/false'], True)} | {fmt_diff(c['slip/none'], True)} | "
            f"{fmt_diff(c['slip/abstain'], True)} | {fmt_diff(c['stable/n_inquiries'], False)} | "
            f"{fmt_diff(c['slip/n_inquiries'], False)} | {fmt_diff(c['slip/J5'], False)} |"
        )
    lines += [
        "",
        "Positive stable-correct and negative slip-false differences favor the "
        "first strategy.",
        "",
        "## Selection agreement",
        "",
        "### First selected item (adaptive block; all strategies share the same "
        "initial state)",
        "",
        "| pair | student | n | agreement |",
        "|---|---|---:|---:|",
    ]
    for st in summary["settings"]["student_types"]:
        for pair, cell in summary["step1_agreement"].get(st, {}).items():
            lines.append(f"| {pair} | {st} | {cell['n']} | {100.0 * cell['agreement']:.1f}% |")
    lines += [
        "",
        "### Full 3-item sequence identity (fixed k=3)",
        "",
        "| pair | student | n | identical sequences |",
        "|---|---|---:|---:|",
    ]
    for st in summary["settings"]["student_types"]:
        for pair, cell in summary["k3_sequence_identity"].get(st, {}).items():
            lines.append(f"| {pair} | {st} | {cell['n']} | {100.0 * cell['identity']:.1f}% |")
    lines += [
        "",
        "## Reproduction checks against frozen v5 episodes",
        "",
        "| check | mismatches |",
        "|---|---|",
    ]
    for key, cell in summary["reproduction"].items():
        lines.append(f"| {key} | {cell['mismatches']} / {cell['n_compared']} |")
    lines += [
        "",
        "The reference arms use the same engine code and frozen inputs as the "
        "v5 pipeline; identical episodes prove the harness before any new "
        "strategy is compared.",
        "",
        "## Slip false remediation by category (point estimates)",
        "",
        "| category | sm_maxent | sm_ig | sm_random | sm_fixed_order | k3_maxent | k3_ig | k3_random | k3_fixed_order |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for cat in CATEGORY_ORDER:
        cells = []
        for arm in (
            "sm_maxent", "sm_ig", "sm_random", "sm_fixed_order",
            "k3_maxent", "k3_ig", "k3_random", "k3_fixed_order",
        ):
            v = summary["per_category"].get(arm, {}).get("slip", {}).get(cat)
            cells.append(f"{100.0 * v:.1f}" if v is not None else "—")
        lines.append(f"| {cat} | " + " | ".join(cells) + " |")
    lines += [
        "",
        "Category cells are exploratory (12-18 cases per category).",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(HERE / "config.json"))
    parser.add_argument("--run-name", default="selection")
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
        HERE / "src" / "selection.py",
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
    for cat in CATEGORY_ORDER:
        bank = load_json(HERE / cfg["bank_dir"] / f"{cfg['bank_prefix']}{cat}.json")
        banks[cat] = bank["items"]
        bank_hyps = [h["id"] for h in bank["hypotheses"]]

    models_np, models_p = {}, {}
    for cat in CATEGORY_ORDER:
        bank = load_json(HERE / cfg["bank_dir"] / f"{cfg['bank_prefix']}{cat}.json")
        singles = [h["id"] for h in bank["hypotheses"]]
        models_np[cat] = eng.build_model(cat, banks[cat], singles, with_pairs=False, eps=float(cfg["eps"]))
        models_p[cat] = eng.build_model(cat, banks[cat], singles, with_pairs=True, eps=float(cfg["eps"]))

    seeds = int(cfg["seeds"])
    eps = float(cfg["eps"])
    max_obs = int(cfg["max_obs"])
    k_fixed = int(cfg["k_fixed"])
    adaptive_arms = list(cfg["adaptive_arms"])
    k3_arms = list(cfg["k3_arms"])
    types = list(cfg["student_types"])

    episodes = []
    skipped: dict[str, int] = defaultdict(int)
    started = time.time()

    for case in cases:
        prior_row = priors.get(case["key"])
        if prior_row is None:
            skipped["missing_prior"] += 1
            continue
        cat = case["category"]
        top10 = prior_row.get("top10") or []
        singles = models_np[cat].singles
        weights = prior_weights(top10, singles) if top10 else {h: 1.0 / len(singles) for h in singles}
        prior_np = models_np[cat].prior(weights)
        prior_p = models_p[cat].prior(weights)

        for st in types:
            for seed in range(seeds):
                for arm in adaptive_arms:
                    res = sel.run_adaptive(
                        models_p[cat], prior_p, case, st, arm,
                        sel.ADAPTIVE_ARMS[arm], seed=seed, eps=eps, max_obs=max_obs,
                    )
                    if res is None:
                        skipped[f"{arm}/{st}"] += 1
                        continue
                    episodes.append(sel.episode_to_dict(res, seed))
                for arm in k3_arms:
                    res = sel.run_fixed_k(
                        models_np[cat], prior_np, case, st, arm,
                        sel.K3_ARMS[arm], seed=seed, eps=eps, k=k_fixed,
                    )
                    if res is None:
                        skipped[f"{arm}/{st}"] += 1
                        continue
                    episodes.append(sel.episode_to_dict(res, seed))

    by_arm_type = defaultdict(list)
    for e in episodes:
        by_arm_type[(e["arm"], e["student_type"])].append(e)

    cb = ablation.ClusterBoot(family_of_case, n_boot=int(cfg["bootstrap"]), seed=int(cfg["bootstrap_seed"]))
    all_arms = adaptive_arms + k3_arms
    aggregates = {}
    for arm in all_arms:
        aggregates[arm] = {}
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
            contrasts[f"{arm_a} - {arm_b}"] = contrasts.get(f"{arm_a} - {arm_b}", {})
            contrasts[f"{arm_a} - {arm_b}"][f"{st}/correct"] = cb.diff_ci(
                _case_means(a, "correct"), _case_means(b, "correct"))
            for metric in ("false", "none", "abstain", "n_inquiries", "J5"):
                contrasts[f"{arm_a} - {arm_b}"][f"{st}/{metric}"] = cb.diff_ci(
                    _case_means(a, metric), _case_means(b, metric))

    step1 = {st: sel.step1_agreement(by_arm_type, adaptive_arms, st) for st in types}
    k3_seq = {st: sel.sequence_identity(by_arm_type, k3_arms, st) for st in types}

    per_category = {}
    for (arm, st), rows in by_arm_type.items():
        for cat in CATEGORY_ORDER:
            sub = [e for e in rows if e["category"] == cat]
            if sub:
                per_category.setdefault(arm, {}).setdefault(st, {})[cat] = float(
                    np.mean([e["false_remediation"] for e in sub])
                )

    frozen_dir = ROOT / "experiments" / "2026-10-20_llm_v4_v5" / "v5" / "out"
    if abs(eps - 0.05) < 1e-9:
        frozen_path = frozen_dir / "test_category_eps05_corrected_episodes.json"
    elif abs(eps - 0.10) < 1e-9:
        frozen_path = frozen_dir / "test_category_eps0.10_corrected_episodes.json"
    elif abs(eps) < 1e-9:
        frozen_path = frozen_dir / "test_category_eps0.0_corrected_episodes.json"
    else:
        frozen_path = frozen_dir / "test_category_eps05_corrected_episodes.json"
    frozen_checks = {
        "sm_maxent vs frozen stability_mixed/maxent": ("sm_maxent", "stability_mixed", "maxent", ("terminal_kind", "terminal_id", "n_obs", "stopped", "budget_exhausted", "correct", "false_remediation")),
        "k3_maxent vs frozen maxent_k3": ("k3_maxent", "maxent_k3", None, ("terminal_kind", "terminal_id", "n_obs", "correct", "false_remediation")),
        "k3_fixed_order vs frozen fixed_k3": ("k3_fixed_order", "fixed_k3", None, ("terminal_kind", "terminal_id", "n_obs", "correct", "false_remediation")),
        "k3_random_legacy vs frozen random_k3": ("k3_random_legacy", "random_k3", None, ("terminal_kind", "terminal_id", "n_obs", "correct", "false_remediation")),
    }
    reproduction = {}
    if frozen_path.exists():
        frozen = load_json(frozen_path)
        for label, (our_arm, frozen_rule, frozen_selection, fields) in frozen_checks.items():
            f_rows = [
                e for e in frozen
                if e["rule"] == frozen_rule
                and (frozen_selection is None or e["selection"] == frozen_selection)
                and e["student_type"] in types
            ]
            frozen_by = {(e["case_id"], e["student_type"], e["seed"]): e for e in f_rows}
            ours = []
            for st in types:
                ours.extend(by_arm_type.get((our_arm, st), []))
            mism = 0
            examples = []
            for e in ours:
                key = (e["case_id"], e["student_type"], e["seed"])
                f = frozen_by.get(key)
                if f is None:
                    mism += 1
                    if len(examples) < 3:
                        examples.append({"key": key, "reason": "missing"})
                    continue
                diffs = {k: (e[k], f[k]) for k in fields if e[k] != f[k]}
                if diffs:
                    mism += 1
                    if len(examples) < 3:
                        examples.append({"key": key, "diffs": diffs})
            reproduction[label] = {
                "n_compared": len(ours),
                "mismatches": mism,
                "examples": examples,
            }

    summary = {
        "settings": {
            "experiment": cfg["experiment"],
            "cases": cfg["cases"],
            "priors": cfg["priors"],
            "seeds": seeds,
            "eps": eps,
            "max_obs": max_obs,
            "k_fixed": k_fixed,
            "adaptive_arms": adaptive_arms,
            "k3_arms": k3_arms,
            "student_types": types,
            "bootstrap": int(cfg["bootstrap"]),
            "bootstrap_seed": int(cfg["bootstrap_seed"]),
            "random_correction": (
                "one RNG stream per episode advanced per step; legacy arm "
                "re-seeds the same stream every step as in frozen v5"
            ),
            "prior_source": "frozen deepseek-v4.1-flash category-conditioned cached prior",
        },
        "status": "ok",
        "duration_seconds": round(time.time() - started, 2),
        "manifest": manifest,
        "skipped": dict(skipped),
        "n_cases": len(cases),
        "n_episodes": len(episodes),
        "aggregates": aggregates,
        "contrasts": contrasts,
        "step1_agreement": step1,
        "k3_sequence_identity": k3_seq,
        "per_category": per_category,
        "reproduction": reproduction,
    }

    out_dir = run_dir / "outputs"
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    (out_dir / "episodes.json").write_text(json.dumps(episodes, ensure_ascii=False), encoding="utf-8")
    (out_dir / "tables.md").write_text(render_tables(summary), encoding="utf-8")
    (out_dir / "status.json").write_text(
        json.dumps({"status": "ok", "run_id": run_dir.name, "episodes": len(episodes),
                    "duration_seconds": summary["duration_seconds"]}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"wrote {run_dir.relative_to(ROOT)}")
    print(f"episodes={len(episodes)} skipped={dict(skipped)}")
    for label, cell in reproduction.items():
        print(f"{label}: {cell['mismatches']} mismatches / {cell['n_compared']}")
    for arm in all_arms:
        for st in types:
            a = aggregates.get(arm, {}).get(st)
            if not a:
                continue
            print(
                f"{arm}/{st}: correct={a['correct']['mean']:.3f} false={a['false']['mean']:.3f} "
                f"none={a['none']['mean']:.3f} abstain={a['abstain']['mean']:.3f} "
                f"inq={a['n_inquiries']['mean']:.2f}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
