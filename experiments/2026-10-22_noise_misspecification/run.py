"""Noise misspecification and bursty slips.

The diagnostician always assumes eps=0.05 in its likelihood and gates. The
simulated student's true noise changes across conditions, including a
two-state inattention chain that produces streaks of wrong answers at the
same marginal rate as iid noise. All arms share prior, hypothesis space,
MaxEnt selection, seeds and caps.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import shutil
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(HERE / "src"))

from sim_workbench.provenance import snapshot, write_manifest  # noqa: E402

import ablation  # noqa: E402
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
STUDENT_TYPES = ("stable", "slip", "mixed")

ARMS = {
    "sm_b6": {"kind": "sm", "cap": 6},
    "fixed_k3": {"kind": "fixed", "cap": 3},
    "fixed_k3_gate": {"kind": "fixed_gate", "cap": 3},
    "e_b6": {"kind": "ablation", "arm": "posterior_plus_E", "cap": 6},
}

# Student-side noise conditions. The diagnostician's eps is fixed at 0.05.
# burst_0.20_r{3,6}: lapse rate 0.20, mean lapse run length 3/6, so the
# marginal error rate equals iid_0.20 and only autocorrelation changes.
CONDITIONS = [
    {"name": "iid_0.01", "student_eps": 0.01, "burst": None},
    {"name": "iid_0.05", "student_eps": 0.05, "burst": None},
    {"name": "iid_0.10", "student_eps": 0.10, "burst": None},
    {"name": "iid_0.20", "student_eps": 0.20, "burst": None},
    {"name": "burst_0.20_r3", "student_eps": 0.20, "burst": {"p": 0.20, "mean_run": 3.0}},
    {"name": "burst_0.20_r6", "student_eps": 0.20, "burst": {"p": 0.20, "mean_run": 6.0}},
]
CONDITION_BY_NAME = {c["name"]: c for c in CONDITIONS}
MATCHED = "iid_0.05"

WITHIN_PAIRS = [
    ("sm_b6", "fixed_k3"),
    ("fixed_k3_gate", "fixed_k3"),
    ("sm_b6", "fixed_k3_gate"),
    ("e_b6", "fixed_k3"),
]

# Matched -> mismatched penalties and burst-vs-iid correlation contrasts.
CONDITION_PAIRS = [
    ("iid_0.01", "iid_0.05"),
    ("iid_0.10", "iid_0.05"),
    ("iid_0.20", "iid_0.05"),
    ("burst_0.20_r3", "iid_0.20"),
    ("burst_0.20_r6", "iid_0.20"),
]

METRICS = tuple(ablation.METRICS) + (
    "stop_rate",
    "budget_exhausted_rate",
    "coverage",
)
CONTRAST_METRICS = tuple(ablation.METRICS)


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


def make_process(case: dict, student_type: str, seed: int, condition: dict):
    burst = condition["burst"]
    if burst is None:
        return None
    return eng.InattentionProcess(
        case["case_id"], seed, student_type, float(burst["p"]), float(burst["mean_run"])
    )


def run_fixed_gate_episode(model, prior, case, student_type, k, seed, eps, process=None):
    """Fixed k MaxEnt inquiries, then the full SM stop rule applied once."""
    true_id = case["true_id"]
    item_idx = int(case["item_idx"])
    item = model.items[item_idx]
    answer = case["answer"]
    if answer not in item["answers"]:
        return None
    if student_type == "slip" and answer == item["correct"]:
        return None
    if student_type in ("stable", "mixed") and model.effective_pred(item_idx, true_id) != answer:
        return None
    if student_type in ("stable", "mixed") and true_id not in model.index:
        return None

    true_pair = None
    if student_type == "mixed":
        partner = eng._choose_partner(model, case, seed)
        if partner is None:
            return None
        true_pair = eng.pair_id(true_id, partner)

    post = prior.copy()
    history = [(item_idx, answer)]
    used = {item_idx}
    for _ in range(k):
        available = [i for i in range(len(model.items)) if i not in used]
        if not available:
            break
        nidx = model.select_maxent(post, available)
        outcome = eng.observe(
            model, student_type, nidx, true_id, true_pair, case["case_id"], seed, eps, process
        )
        used.add(nidx)
        history.append((nidx, outcome))
        post = model.update(post, nidx, outcome)

    cand = eng._stop_check(model, post, history, "stability_mixed")
    kind, tid, tp = cand if cand else ("abstain", None, float(post.max()))
    return eng.V5Result(
        rule=f"fixed_k{k}_gate",
        selection="maxent",
        student_type=student_type,
        case_id=case["case_id"],
        family=case.get("family") or case.get("template_family") or str(case.get("library_template")),
        category=case["category"],
        true_id=true_id if student_type == "stable" else None,
        true_pair=true_pair,
        terminal_kind=kind,
        terminal_id=tid,
        terminal_p=tp,
        n_obs=len(history),
        stopped=False,
        budget_exhausted=True,
        verifications=0,
        history=[(model.items[i]["text"], o) for i, o in history],
    )


def run_arm(model, prior, case, student_type, arm, seed, condition, eps_diag):
    spec = ARMS[arm]
    kind = spec["kind"]
    cap = spec["cap"]
    eps_s = float(condition["student_eps"])
    process = make_process(case, student_type, seed, condition)
    if kind == "fixed":
        return eng.run_budget_episode(
            model, prior, case, student_type, "maxent", cap,
            seed=seed, eps=eps_s, process=process,
        )
    if kind == "fixed_gate":
        return run_fixed_gate_episode(
            model, prior, case, student_type, cap, seed, eps_s, process
        )
    if kind == "sm":
        return eng.run_episode(
            model, prior, case, student_type, "stability_mixed",
            selection="maxent", on_budget="abstain",
            seed=seed, eps=eps_s, max_obs=cap + 1, process=process,
        )
    if kind == "ablation":
        return ablation.run_episode_ablation(
            model, prior, case, student_type, spec["arm"],
            seed=seed, eps=eps_s, max_obs=cap + 1, process=process,
        )
    raise KeyError(arm)


def episode_to_dict(res, arm: str, seed: int, condition: dict) -> dict:
    return {
        "arm": arm,
        "condition": condition["name"],
        "student_eps": float(condition["student_eps"]),
        "burst": condition["burst"],
        "cap": ARMS[arm]["cap"],
        "student_type": res.student_type,
        "case_id": res.case_id,
        "family": res.family,
        "category": res.category,
        "true_id": res.true_id,
        "true_pair": res.true_pair,
        "terminal_kind": res.terminal_kind,
        "terminal_id": res.terminal_id,
        "terminal_p": float(res.terminal_p),
        "n_obs": int(res.n_obs),
        "n_inquiries": int(res.n_inquiries),
        "stopped": bool(res.stopped),
        "budget_exhausted": bool(res.budget_exhausted),
        "correct": bool(res.correct),
        "false_remediation": bool(res.false_remediation),
        "seed": int(seed),
        "J5": float(res.n_obs + 5.0 * float(res.false_remediation)),
        "J10": float(res.n_obs + 10.0 * float(res.false_remediation)),
    }


def point_metric(rows: list[dict], metric: str) -> float:
    if metric == "stop_rate":
        return float(np.mean([e["stopped"] for e in rows]))
    if metric == "budget_exhausted_rate":
        return float(np.mean([e["budget_exhausted"] for e in rows]))
    if metric == "coverage":
        return float(np.mean([e["terminal_kind"] in ("single", "pair", "mixed") for e in rows]))
    return float(np.mean([ablation.episode_metric(e, metric) for e in rows]))


def summarize(rows: list[dict], cb) -> dict:
    out = ablation.summarize_arm(rows, cb)
    for metric in ("stop_rate", "budget_exhausted_rate", "coverage"):
        out[metric] = {
            "mean": point_metric(rows, metric),
            "ci_low": None,
            "ci_high": None,
            "n_cases": len({e["case_id"] for e in rows}),
        }
    out["n_cases"] = len({e["case_id"] for e in rows})
    out["n_episodes"] = len(rows)
    return out


def fmt_pct(cell, ci=True):
    if isinstance(cell, dict):
        if cell.get("ci_low") is not None and ci:
            return f"{100 * cell['mean']:.1f} [{100 * cell['ci_low']:.1f}, {100 * cell['ci_high']:.1f}]"
        return f"{100 * cell['mean']:.1f}"
    return f"{100 * cell:.1f}"


def fmt_num(cell):
    if isinstance(cell, dict):
        return f"{cell['mean']:.2f}"
    return f"{cell:.2f}"


def fmt_diff(cell, pct=True):
    scale = 100.0 if pct else 1.0
    return f"{scale * cell['mean']:+.1f} [{scale * cell['ci_low']:+.1f}, {scale * cell['ci_high']:+.1f}]"


def render_tables(summary: dict) -> str:
    agg = summary["aggregates"]
    conds = [c["name"] for c in CONDITIONS]
    lines = [
        "# Noise misspecification and bursty slips",
        "",
        "Diagnostician likelihood/gates always assume eps=0.05. The simulated "
        "student's true noise changes across conditions. `burst_0.20_r3/r6` use a "
        "two-state inattention chain with marginal lapse rate 0.20 and mean lapse "
        "run length 3/6, so they are comparable to `iid_0.20`: only the temporal "
        "correlation of wrong answers changes. All arms share the category prior, "
        "pair-augmented hypothesis space, MaxEnt selection, 5 seeds and caps "
        "(SM/E-only: 6; fixed-k/gate: 3).",
        "",
        "## SM across student-noise conditions",
        "",
        "| condition | slip false | slip abstain | slip none | stable correct | stable abstain | stable inq | slip inq |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for cond in conds:
        sl = agg[f"{cond}|sm_b6|slip"]
        st_ = agg[f"{cond}|sm_b6|stable"]
        lines.append(
            f"| {cond} | {fmt_pct(sl['false'])} | {fmt_pct(sl['abstain'], ci=False)} | "
            f"{fmt_pct(sl['none'], ci=False)} | {fmt_pct(st_['correct'])} | "
            f"{fmt_pct(st_['abstain'], ci=False)} | {fmt_num(st_['n_inquiries'])} | "
            f"{fmt_num(sl['n_inquiries'])} |"
        )
    lines += [
        "",
        "## Arm comparison within each condition (point estimates)",
        "",
        "| condition | method | slip false | stable correct | stable abstain | stable inq | slip inq |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    labels = {"sm_b6": "SM", "fixed_k3": "fixed3", "fixed_k3_gate": "fixed3+gate", "e_b6": "E-only"}
    for cond in conds:
        for arm in ARMS:
            sl = agg[f"{cond}|{arm}|slip"]
            st_ = agg[f"{cond}|{arm}|stable"]
            lines.append(
                f"| {cond} | {labels[arm]} | {fmt_pct(sl['false'])} | "
                f"{fmt_pct(st_['correct'])} | {fmt_pct(st_['abstain'], ci=False)} | "
                f"{fmt_num(st_['n_inquiries'])} | {fmt_num(sl['n_inquiries'])} |"
            )
    lines += [
        "",
        "## SM - fixed3 within each condition",
        "",
        "| condition | slip false | stable correct | stable inq | slip inq |",
        "|---|---:|---:|---:|---:|",
    ]
    for cond in conds:
        c = summary["within_contrasts"][f"{cond}|sm_b6 - fixed_k3"]
        st_ = c["stable"]
        sl = c["slip"]
        lines.append(
            f"| {cond} | {fmt_diff(sl['false'])} | {fmt_diff(st_['correct'])} | "
            f"{fmt_diff(st_['n_inquiries'], pct=False)} | {fmt_diff(sl['n_inquiries'], pct=False)} |"
        )
    lines += [
        "",
        "## Mismatch penalty and burst effect (paired, condition - reference)",
        "",
        "| arm | contrast | slip false | stable correct | stable inq | slip inq |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for arm in ARMS:
        for a, b in CONDITION_PAIRS:
            c = summary["condition_contrasts"][f"{arm}|{a} - {b}"]
            st_ = c["stable"]
            sl = c["slip"]
            lines.append(
                f"| {labels[arm]} | {a} - {b} | {fmt_diff(sl['false'])} | "
                f"{fmt_diff(st_['correct'])} | {fmt_diff(st_['n_inquiries'], pct=False)} | "
                f"{fmt_diff(sl['n_inquiries'], pct=False)} |"
            )
    lines += [
        "",
        "`iid_* - iid_0.05` rows are mismatch penalties relative to the matched "
        "condition; `burst_* - iid_0.20` rows isolate temporal correlation at the "
        "same marginal error rate. Positive slip-false differences mean more false "
        "remediation; negative stable-correct differences mean lower coverage.",
        "",
        "## Burst vs iid at the same marginal rate: all arms",
        "",
        "| condition - iid_0.20 | arm | slip false | stable correct | stable abstain | slip none |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for cond in ("burst_0.20_r3", "burst_0.20_r6"):
        for arm in ARMS:
            c = summary["condition_contrasts"][f"{arm}|{cond} - iid_0.20"]
            st_ = c["stable"]
            sl = c["slip"]
            lines.append(
                f"| {cond} | {labels[arm]} | {fmt_diff(sl['false'])} | "
                f"{fmt_diff(st_['correct'])} | {fmt_diff(st_['abstain'])} | "
                f"{fmt_diff(sl['none'])} |"
            )
    lines += [
        "",
        "## Reproduction and process checks",
        "",
        "| check | result |",
        "|---|---|",
        f"| SM iid_0.05 vs frozen v5 `stability_mixed/maxent` | "
        f"{summary['reproduction']['frozen_v5']['episode_mismatches']} mismatches / "
        f"{summary['reproduction']['frozen_v5']['n_compared']} episodes |",
    ]
    for check in summary["reproduction"]["budget_e1"]:
        lines.append(
            f"| {check['arm']} iid_0.05 vs budget-ablation E1 run | "
            f"{check['episode_mismatches']} mismatches / {check['n_compared']} episodes |"
        )
    lines += [
        f"| burst marginal wrong rate (6 draws, slip) | "
        f"{summary['burst_rate_check']['wrong_rate']:.3f} vs nominal "
        f"{summary['burst_rate_check']['nominal']:.3f} |",
        "",
        "## Scope",
        "",
        "- Post-hoc robustness run on the frozen v5 protocol-valid 87-case test set; "
        "no thresholds tuned on these results.",
        "- The diagnostician uses eps=0.05 everywhere; only the student-side process "
        "changes. The burst chain is an inattention model, not estimated from real "
        "students.",
        "- In burst conditions stable/mixed students also lapse (emit a random wrong "
        "answer instead of their misconception prediction), so the condition tests "
        "the iid assumption rather than slip students alone.",
        "- Mixed students remain a pressure test with near-zero pair identification; "
        "no mixed claim is made here.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(HERE / "config.json"))
    parser.add_argument("--run-name", default="noise_misspecification")
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
        HERE / "src" / "applicability.py",
        HERE / "src" / "ablation.py",
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

    banks, singles = {}, {}
    for cat in CATEGORY_ORDER:
        bank = load_json(HERE / cfg["bank_dir"] / f"{cfg['bank_prefix']}{cat}.json")
        banks[cat] = bank["items"]
        singles[cat] = [h["id"] for h in bank["hypotheses"]]
    eps_diag = float(cfg["diagnostician_eps"])
    models = {
        cat: eng.build_model(cat, banks[cat], singles[cat], with_pairs=True, eps=eps_diag)
        for cat in CATEGORY_ORDER
    }

    seeds = int(cfg["seeds"])
    episodes = []
    by = defaultdict(list)
    skipped = Counter()
    started = time.time()

    for case in cases:
        prior_row = priors.get(case["key"])
        if prior_row is None:
            skipped["missing_prior"] += 1
            continue
        cat = case["category"]
        prior = models[cat].prior(prior_weights(prior_row.get("top10") or [], singles[cat]))
        for st in STUDENT_TYPES:
            for seed in range(seeds):
                for condition in CONDITIONS:
                    for arm in ARMS:
                        res = run_arm(models[cat], prior, case, st, arm, seed, condition, eps_diag)
                        if res is None:
                            skipped[f"{arm}/{st}/{condition['name']}"] += 1
                            continue
                        ed = episode_to_dict(res, arm, seed, condition)
                        episodes.append(ed)
                        by[(condition["name"], arm, st)].append(ed)

    cb = ablation.ClusterBoot(
        family_of_case,
        n_boot=int(cfg["bootstrap"]),
        seed=int(cfg["bootstrap_seed"]),
    )

    aggregates = {}
    for condition in CONDITIONS:
        for arm in ARMS:
            for st in STUDENT_TYPES:
                rows = by.get((condition["name"], arm, st), [])
                if rows:
                    aggregates[(condition["name"], arm, st)] = summarize(rows, cb)

    within_contrasts = {}
    for condition in CONDITIONS:
        for a, b in WITHIN_PAIRS:
            key = f"{condition['name']}|{a} - {b}"
            within_contrasts[key] = {}
            for st in STUDENT_TYPES:
                within_contrasts[key][st] = {
                    metric: cb.diff_ci(
                        ablation.case_means(by[(condition["name"], a, st)], metric),
                        ablation.case_means(by[(condition["name"], b, st)], metric),
                    )
                    for metric in CONTRAST_METRICS
                }

    condition_contrasts = {}
    for arm in ARMS:
        for a, b in CONDITION_PAIRS:
            key = f"{arm}|{a} - {b}"
            condition_contrasts[key] = {}
            for st in STUDENT_TYPES:
                condition_contrasts[key][st] = {
                    metric: cb.diff_ci(
                        ablation.case_means(by[(a, arm, st)], metric),
                        ablation.case_means(by[(b, arm, st)], metric),
                    )
                    for metric in CONTRAST_METRICS
                }

    reproduction = {
        "frozen_v5": {"path": "", "n_compared": 0, "episode_mismatches": 0},
        "budget_e1": [
            {"arm": "fixed_k3", "path": "", "n_compared": 0, "episode_mismatches": 0},
            {"arm": "fixed_k3_gate", "path": "", "n_compared": 0, "episode_mismatches": 0},
            {"arm": "e_b6", "path": "", "n_compared": 0, "episode_mismatches": 0},
        ],
    }
    frozen_path = (
        HERE.parent / "2026-10-20_llm_v4_v5" / "v5" / "out" / "test_category_eps05_corrected_episodes.json"
    )
    fields = ("terminal_kind", "terminal_id", "n_obs", "stopped", "budget_exhausted", "correct", "false_remediation")
    if frozen_path.exists():
        reproduction["frozen_v5"]["path"] = str(frozen_path.relative_to(ROOT))
        frozen = [
            e for e in load_json(frozen_path)
            if e["rule"] == "stability_mixed" and e["selection"] == "maxent"
        ]
        frozen_by = {(e["case_id"], e["student_type"], e["seed"]): e for e in frozen}
        for st in STUDENT_TYPES:
            for e in by[("iid_0.05", "sm_b6", st)]:
                f = frozen_by.get((e["case_id"], e["student_type"], e["seed"]))
                reproduction["frozen_v5"]["n_compared"] += 1
                if f is None or any(e[field] != f[field] for field in fields):
                    reproduction["frozen_v5"]["episode_mismatches"] += 1

    budget_e1_path = (
        HERE.parent / "2026-10-21_budget_ablation" / "runs" / "20261021T115028Z_budget_ablation_e1"
        / "outputs" / "episodes.json"
    )
    if budget_e1_path.exists():
        budget_by = {
            (e["arm"], e["case_id"], e["student_type"], e["seed"]): e
            for e in load_json(budget_e1_path)
        }
        for check in reproduction["budget_e1"]:
            check["path"] = str(budget_e1_path.relative_to(ROOT))
            arm = check["arm"]
            for st in STUDENT_TYPES:
                for e in by[("iid_0.05", arm, st)]:
                    b = budget_by.get((arm, e["case_id"], e["student_type"], e["seed"]))
                    check["n_compared"] += 1
                    if b is None or any(e[field] != b[field] for field in fields):
                        check["episode_mismatches"] += 1

    # Marginal lapse rate check for the burst chain (slip students, six draws).
    wrong = total = 0
    for case in cases:
        for st in STUDENT_TYPES:
            for seed in range(seeds):
                condition = CONDITION_BY_NAME["burst_0.20_r3"]
                process = make_process(case, st, seed, condition)
                for _ in range(6):
                    wrong += int(process.draw())
                    total += 1
    burst_rate_check = {
        "nominal": 0.20,
        "wrong_rate": wrong / total if total else None,
        "n_draws": total,
    }

    summary = {
        "settings": {
            "experiment": cfg["experiment"],
            "cases": cfg["cases"],
            "priors": cfg["priors"],
            "diagnostician_eps": eps_diag,
            "seeds": seeds,
            "arms": list(ARMS),
            "conditions": CONDITIONS,
            "bootstrap": int(cfg["bootstrap"]),
            "bootstrap_seed": int(cfg["bootstrap_seed"]),
        },
        "status": "ok",
        "duration_seconds": round(time.time() - started, 2),
        "manifest": manifest,
        "skipped": dict(skipped),
        "n_cases": len(cases),
        "n_episodes": len(episodes),
        "aggregates": {f"{cond}|{arm}|{st}": v for (cond, arm, st), v in aggregates.items()},
        "within_contrasts": within_contrasts,
        "condition_contrasts": condition_contrasts,
        "reproduction": reproduction,
        "burst_rate_check": burst_rate_check,
    }

    out_dir = run_dir / "outputs"
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    (out_dir / "episodes.json").write_text(json.dumps(episodes, ensure_ascii=False), encoding="utf-8")
    (out_dir / "tables.md").write_text(render_tables(summary), encoding="utf-8")
    with (out_dir / "noise_curve.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["condition", "arm", "student_type", "metric", "mean", "ci_low", "ci_high"])
        for condition in CONDITIONS:
            for arm in ARMS:
                for st in STUDENT_TYPES:
                    cell_arm = aggregates.get((condition["name"], arm, st))
                    if not cell_arm:
                        continue
                    for metric in METRICS:
                        cell = cell_arm.get(metric)
                        if cell:
                            writer.writerow([
                                condition["name"], arm, st, metric,
                                cell["mean"], cell.get("ci_low"), cell.get("ci_high"),
                            ])
    (out_dir / "status.json").write_text(
        json.dumps(
            {
                "status": "ok",
                "run_id": run_dir.name,
                "episodes": len(episodes),
                "duration_seconds": summary["duration_seconds"],
                "reproduction": reproduction,
                "burst_rate_check": burst_rate_check,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print(f"wrote {run_dir.relative_to(ROOT)}")
    print(f"episodes={len(episodes)} skipped={dict(skipped)}")
    e1_checks = ", ".join(
        f"{c['episode_mismatches']}/{c['n_compared']}" for c in reproduction["budget_e1"]
    )
    print(
        "reproduction: frozen_v5 "
        f"{reproduction['frozen_v5']['episode_mismatches']}/{reproduction['frozen_v5']['n_compared']}, "
        f"budget_e1 [{e1_checks}]"
    )
    print(
        "burst wrong rate="
        f"{burst_rate_check['wrong_rate']:.3f} (nominal 0.200, n={burst_rate_check['n_draws']})"
    )
    for condition in CONDITIONS:
        a = aggregates[(condition["name"], "sm_b6", "slip")]
        s = aggregates[(condition["name"], "sm_b6", "stable")]
        print(
            f"SM {condition['name']}: slip_false={a['false']['mean']:.3f} "
            f"slip_abstain={a['abstain']['mean']:.3f} stable_correct={s['correct']['mean']:.3f} "
            f"stable_inq={s['n_inquiries']['mean']:.2f} slip_inq={a['n_inquiries']['mean']:.2f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
