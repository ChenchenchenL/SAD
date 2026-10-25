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
CAPS = (1, 2, 3, 6)

ARMS = {"one_shot_forced": {"kind": "one_shot", "cap": 0}}
for _k in CAPS:
    ARMS[f"fixed_k{_k}"] = {"kind": "fixed", "cap": _k}
    ARMS[f"sm_b{_k}"] = {"kind": "sm", "cap": _k}
    ARMS[f"e_b{_k}"] = {"kind": "ablation", "arm": "posterior_plus_E", "cap": _k}
    ARMS[f"posterior_b{_k}"] = {"kind": "ablation", "arm": "posterior_only", "cap": _k}
ARMS["fixed_k3_gate"] = {"kind": "fixed_gate", "cap": 3}

METRICS = tuple(ablation.METRICS) + (
    "stop_rate",
    "budget_exhausted_rate",
    "coverage",
)
CONTRAST_METRICS = tuple(ablation.METRICS)

CAP_LABEL = {0: "one-shot", 1: "1", 2: "2", 3: "3", 6: "6"}

CROSS_PAIRS = [
    ("e_b2", "sm_b6"),
    ("e_b3", "sm_b6"),
    ("sm_b6", "fixed_k3"),
]

# E1 strict 2x2: decision rule vs adaptive stopping, with MaxEnt selection
# held fixed. A=fixed_k3 (direct commitment), B=fixed_k3_gate (same SM gate
# applied once after exactly 3 inquiries; failure -> none/abstain), C=sm_b6
# (full SM: same gate + adaptive stopping, cap 6). B-A isolates the gate,
# C-B isolates adaptive stopping, C-A reproduces the mainline contrast.
# sm_b3 - fixed_k3_gate is the same-cap (3) adaptive-stopping contrast.
E1_ARMS = ("fixed_k3", "fixed_k3_gate", "sm_b6", "sm_b3")
E1_PAIRS = [
    ("fixed_k3_gate", "fixed_k3"),
    ("sm_b6", "fixed_k3_gate"),
    ("sm_b6", "fixed_k3"),
    ("sm_b3", "fixed_k3_gate"),
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


def run_fixed_gate_episode(model, prior, case, student_type, k, seed, eps):
    """Fixed k MaxEnt inquiries, then the full SM stop rule.

    The gate is applied once after exactly k additional questions. If it does
    not fire, the episode abstains; explicit none is still returned by the
    gate's own none rules. stopped=False marks this as a fixed-budget method.
    """
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
            model, student_type, nidx, true_id, true_pair, case["case_id"], seed, eps
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


def run_arm(model, prior, case, student_type, arm, seed, eps):
    spec = ARMS[arm]
    kind = spec["kind"]
    cap = spec["cap"]
    if kind == "one_shot":
        return eng.one_shot_episode(model, prior, case, student_type, seed=seed, typed=False)
    if kind == "fixed":
        return eng.run_budget_episode(
            model, prior, case, student_type, "maxent", cap, seed=seed, eps=eps
        )
    if kind == "fixed_gate":
        return run_fixed_gate_episode(model, prior, case, student_type, cap, seed, eps)
    if kind == "sm":
        return eng.run_episode(
            model,
            prior,
            case,
            student_type,
            "stability_mixed",
            selection="maxent",
            on_budget="abstain",
            seed=seed,
            eps=eps,
            max_obs=cap + 1,
        )
    if kind == "ablation":
        return ablation.run_episode_ablation(
            model,
            prior,
            case,
            student_type,
            spec["arm"],
            seed=seed,
            eps=eps,
            max_obs=cap + 1,
        )
    raise KeyError(arm)


def episode_to_dict(res, arm: str, seed: int) -> dict:
    return {
        "arm": arm,
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


def fmt_num(cell, ci=False):
    if isinstance(cell, dict):
        if ci and cell.get("ci_low") is not None:
            return f"{cell['mean']:.2f} [{cell['ci_low']:.2f}, {cell['ci_high']:.2f}]"
        return f"{cell['mean']:.2f}"
    return f"{cell:.2f}"


def fmt_diff(cell, pct=True):
    scale = 100.0 if pct else 1.0
    return f"{scale * cell['mean']:+.1f} [{scale * cell['ci_low']:+.1f}, {scale * cell['ci_high']:+.1f}]"


def render_tables(summary: dict) -> str:
    agg = summary["aggregates"]
    lines = [
        "# Question budget curve for stability-aware diagnosis",
        "",
        "Same frozen v5 cases, LLM prior, pair-augmented hypothesis space, MaxEnt selection, "
        "eps=0.05, and 5 seeds. Only the cap on additional inquiries changes "
        "(cap=1/2/3/6 means max_obs=2/3/4/7 including the initial item).",
        "",
        "## SM budget curve",
        "",
        "| cap | stable inquiries | slip inquiries | stopped before cap | budget exhausted | slip false | slip none | slip abstain | stable correct | stable correct stop | stable abstain |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for k in CAPS:
        a = agg[f"sm_b{k}"]
        st = a["stable"]
        sl = a["slip"]
        stop_pooled = np.mean([a[t]["stop_rate"]["mean"] for t in STUDENT_TYPES])
        exhausted_pooled = np.mean([a[t]["budget_exhausted_rate"]["mean"] for t in STUDENT_TYPES])
        lines.append(
            f"| {k} | {fmt_num(st['n_inquiries'])} | {fmt_num(sl['n_inquiries'])} | "
            f"{100 * stop_pooled:.1f} | {100 * exhausted_pooled:.1f} | "
            f"{fmt_pct(sl['false'])} | {fmt_pct(sl['none'], ci=False)} | {fmt_pct(sl['abstain'], ci=False)} | "
            f"{fmt_pct(st['correct'])} | {fmt_pct(st['correct_stop'], ci=False)} | "
            f"{fmt_pct(st['abstain'], ci=False)} |"
        )
    lines += [
        "",
        "Inquiries are additional questions after the initial item. `stopped`/`exhausted` are "
        "pooled equally across stable/slip/mixed. Cap=1 has no pre-budget stop by construction "
        "(the stop check occurs after the budget check); its terminal diagnosis is still scored "
        "by `stable correct` / `slip false`, but `stable correct stop` is zero. At higher caps, "
        "`stable correct stop` counts only episodes that stop before the cap; budget-final "
        "correct diagnoses are in `stable correct`.",
        "",
        "## Same-cap comparison (point estimates)",
        "",
        "| cap | method | slip false | slip abstain | stable correct | stable abstain | stable inquiries | slip inquiries |",
        "|---:|---|---:|---:|---:|---:|---:|---:|",
        ]
    for k in CAPS:
        for arm, label in [
            (f"fixed_k{k}", "fixed-k"),
            (f"sm_b{k}", "SM"),
            (f"e_b{k}", "E-only"),
            (f"posterior_b{k}", "posterior-only"),
        ]:
            a = agg[arm]
            lines.append(
                f"| {k} | {label} | {fmt_pct(a['slip']['false'])} | "
                f"{fmt_pct(a['slip']['abstain'], ci=False)} | {fmt_pct(a['stable']['correct'])} | "
                f"{fmt_pct(a['stable']['abstain'], ci=False)} | {fmt_num(a['stable']['n_inquiries'])} | "
                f"{fmt_num(a['slip']['n_inquiries'])} |"
            )
    lines += [
        "",
        "Fixed-k uses exactly k additional MaxEnt questions and then commits from the posterior "
        "(single/none, never abstain). SM uses the same selection but may stop earlier, return "
        "none, or abstain; its actual inquiries can be below the cap.",
        "",
        "## Same-cap paired contrasts",
        "",
        "| cap | contrast | slip false | stable correct | stable abstain | inquiries |",
        "|---:|---|---:|---:|---:|---:|",
    ]
    for k in CAPS:
        for a, b in [
            (f"sm_b{k}", f"fixed_k{k}"),
            (f"e_b{k}", f"sm_b{k}"),
            (f"posterior_b{k}", f"e_b{k}"),
            (f"sm_b{k}", f"posterior_b{k}"),
        ]:
            c = summary["same_cap_contrasts"].get(f"{a} - {b}", {})
            st = c.get("stable", {})
            sl = c.get("slip", {})
            lines.append(
                f"| {k} | {a} - {b} | "
                f"{fmt_diff(sl['false']) if sl else '—'} | "
                f"{fmt_diff(st['correct']) if st else '—'} | "
                f"{fmt_diff(st['abstain']) if st else '—'} | "
                f"{fmt_diff(sl['n_inquiries'], pct=False) if sl else '—'} |"
            )
    lines += [
        "",
        "## Marginal change with more budget",
        "",
        "| family | comparison | slip false | stable correct | slip inquiries |",
        "|---|---|---:|---:|---:|",
    ]
    for family in ("sm", "e", "posterior"):
        for a, b in [("b1", "b2"), ("b2", "b3"), ("b3", "b6"), ("b1", "b6")]:
            c = summary["cap_contrasts"].get(f"{family}_{a} - {family}_{b}", {})
            st = c.get("stable", {})
            sl = c.get("slip", {})
            lines.append(
                f"| {family} | {a} -> {b} | "
                f"{fmt_diff(sl['false']) if sl else '—'} | "
                f"{fmt_diff(st['correct']) if st else '—'} | "
                f"{fmt_diff(sl['n_inquiries'], pct=False) if sl else '—'} |"
            )
    lines += [
        "",
        "The comparison is earlier/smaller-budget minus later/larger-budget. For slip false, "
        "negative means the larger budget has higher error; positive means more budget reduces "
        "error. For stable correct, negative means the larger budget improves coverage.",
        "",
        "## Selected cross-budget comparisons",
        "",
        "| contrast | slip false | stable correct | stable abstain | stable inquiries | slip inquiries |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for a, b in CROSS_PAIRS:
        c = summary["cross_contrasts"].get(f"{a} - {b}", {})
        st = c.get("stable", {})
        sl = c.get("slip", {})
        lines.append(
            f"| {a} - {b} | {fmt_diff(sl['false']) if sl else '—'} | "
            f"{fmt_diff(st['correct']) if st else '—'} | "
            f"{fmt_diff(st['abstain']) if st else '—'} | "
            f"{fmt_diff(st['n_inquiries'], pct=False) if st else '—'} | "
            f"{fmt_diff(sl['n_inquiries'], pct=False) if sl else '—'} |"
        )
    lines += [
        "",
        "`e_b3 - sm_b6` asks whether a 3-question E-gated single-diagnosis policy can match "
        "or beat the full 6-question SM; `sm_b6 - fixed_k3` reproduces the original v5 "
        "SM-vs-fixed3 comparison (fixed3 uses MaxEnt and 3 additional questions).",
        "",
        "## E1: strict 2x2 decomposition of SM vs fixed3",
        "",
        "MaxEnt selection, prior, hypothesis space, eps and seeds are held fixed. "
        "A = `fixed_k3`: 3 inquiries, then commit from the posterior (single/none, never "
        "abstain). B = `fixed_k3_gate`: the same 3 inquiries, then the full SM stability "
        "gate applied once; gate failure abstains, gate none-rules still return none. "
        "C = `sm_b6`: full SM, same gate with adaptive stopping under a cap of 6. "
        "B-A isolates the decision rule at a fixed budget; C-B isolates adaptive stopping "
        "on top of the gate (note C's cap is 6, not 3); C-A reproduces the mainline "
        "contrast. `sm_b3 - fixed_k3_gate` is the same-cap adaptive-stopping contrast.",
        "",
        "| arm | slip false | slip none | slip abstain | stable correct | stable abstain | stable inq | slip inq |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for arm, label in [
        ("fixed_k3", "A fixed_k3"),
        ("fixed_k3_gate", "B fixed_k3_gate"),
        ("sm_b3", "C' sm_b3 (adaptive, cap 3)"),
        ("sm_b6", "C sm_b6 (adaptive, cap 6)"),
    ]:
        a = agg[arm]
        lines.append(
            f"| {label} | {fmt_pct(a['slip']['false'])} | {fmt_pct(a['slip']['none'], ci=False)} | "
            f"{fmt_pct(a['slip']['abstain'], ci=False)} | {fmt_pct(a['stable']['correct'])} | "
            f"{fmt_pct(a['stable']['abstain'], ci=False)} | {fmt_num(a['stable']['n_inquiries'])} | "
            f"{fmt_num(a['slip']['n_inquiries'])} |"
        )
    lines += [
        "",
        "### E1 paired contrasts",
        "",
        "| contrast | slip false | stable correct | stable abstain | stable inq | slip inq |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for a, b in E1_PAIRS:
        c = summary["e1_contrasts"].get(f"{a} - {b}", {})
        st_ = c.get("stable", {})
        sl = c.get("slip", {})
        lines.append(
            f"| {a} - {b} | {fmt_diff(sl['false']) if sl else '—'} | "
            f"{fmt_diff(st_['correct']) if st_ else '—'} | "
            f"{fmt_diff(st_['abstain']) if st_ else '—'} | "
            f"{fmt_diff(st_['n_inquiries'], pct=False) if st_ else '—'} | "
            f"{fmt_diff(sl['n_inquiries'], pct=False) if sl else '—'} |"
        )
    lines += [
        "",
        "## SM slip false remediation by category (point estimates)",
        "",
        "| category | cap 1 | cap 3 | cap 6 |",
        "|---|---:|---:|---:|",
    ]
    for cat in CATEGORY_ORDER:
        vals = []
        for k in (1, 3, 6):
            v = summary["per_category"][f"sm_b{k}"]["slip"].get(cat, {}).get("false")
            vals.append(f"{100 * v:.1f}" if v is not None else "—")
        lines.append(f"| {cat} | " + " | ".join(vals) + " |")
    lines += [
        "",
        "## Reproduction check",
        "",
        "| check | result |",
        "|---|---|",
        f"| SM at cap=6 vs frozen v5 `stability_mixed/maxent` | "
        f"{summary['reproduction']['episode_mismatches']} mismatches / "
        f"{summary['reproduction']['n_compared']} episodes |",
        "| max absolute aggregate difference | "
        + (
            f"{summary['reproduction']['max_abs_aggregate_diff']:.3e} |"
            if summary["reproduction"]["max_abs_aggregate_diff"] is not None
            else "— |"
        ),
        "",
        "## Scope",
        "",
        "- Post-hoc budget curve on the frozen v5 protocol-valid 87-case test set; no "
        "thresholds were tuned on these results.",
        "- All arms use the LLM category prior and the same MaxEnt selection; this is not a "
        "prior ablation.",
        "- `stable correct stop` is not comparable across caps: cap=1 cannot stop before "
        "budget, and budget-final correct diagnoses are counted in `stable correct` but not "
        "in `stable correct stop`.",
        "- Fixed-k is a budget-matched reference that always commits after k questions; SM "
        "may stop earlier or abstain. `fixed_k3_gate` (E1 arm B) resolves this confound by "
        "applying the SM gate once after exactly 3 questions.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(HERE / "config.json"))
    parser.add_argument("--run-name", default="budget_ablation")
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
    models = {
        cat: eng.build_model(cat, banks[cat], singles[cat], with_pairs=True, eps=float(cfg["eps"]))
        for cat in CATEGORY_ORDER
    }

    seeds = int(cfg["seeds"])
    eps = float(cfg["eps"])

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
                for arm in ARMS:
                    res = run_arm(models[cat], prior, case, st, arm, seed, eps)
                    if res is None:
                        skipped[f"{arm}/{st}"] += 1
                        continue
                    ed = episode_to_dict(res, arm, seed)
                    episodes.append(ed)
                    by[(arm, st)].append(ed)

    cb = ablation.ClusterBoot(
        family_of_case,
        n_boot=int(cfg["bootstrap"]),
        seed=int(cfg["bootstrap_seed"]),
    )

    aggregates = {}
    for arm in ARMS:
        aggregates[arm] = {}
        for st in STUDENT_TYPES:
            rows = by.get((arm, st), [])
            if rows:
                aggregates[arm][st] = summarize(rows, cb)

    same_cap_contrasts = {}
    for k in CAPS:
        for a, b in [
            (f"sm_b{k}", f"fixed_k{k}"),
            (f"e_b{k}", f"sm_b{k}"),
            (f"posterior_b{k}", f"e_b{k}"),
            (f"sm_b{k}", f"posterior_b{k}"),
        ]:
            key = f"{a} - {b}"
            same_cap_contrasts[key] = {}
            for st in STUDENT_TYPES:
                same_cap_contrasts[key][st] = {}
                for metric in CONTRAST_METRICS:
                    same_cap_contrasts[key][st][metric] = cb.diff_ci(
                        ablation.case_means(by[(a, st)], metric),
                        ablation.case_means(by[(b, st)], metric),
                    )

    cap_contrasts = {}
    for family in ("sm", "e", "posterior"):
        for a, b in [("b1", "b2"), ("b2", "b3"), ("b3", "b6"), ("b1", "b6")]:
            key = f"{family}_{a} - {family}_{b}"
            cap_contrasts[key] = {}
            for st in STUDENT_TYPES:
                cap_contrasts[key][st] = {}
                for metric in CONTRAST_METRICS:
                    cap_contrasts[key][st][metric] = cb.diff_ci(
                        ablation.case_means(by[(f"{family}_{a}", st)], metric),
                        ablation.case_means(by[(f"{family}_{b}", st)], metric),
                    )

    cross_contrasts = {}
    for a, b in CROSS_PAIRS:
        key = f"{a} - {b}"
        cross_contrasts[key] = {}
        for st in STUDENT_TYPES:
            cross_contrasts[key][st] = {}
            for metric in CONTRAST_METRICS:
                cross_contrasts[key][st][metric] = cb.diff_ci(
                    ablation.case_means(by[(a, st)], metric),
                    ablation.case_means(by[(b, st)], metric),
                )

    e1_contrasts = {}
    for a, b in E1_PAIRS:
        key = f"{a} - {b}"
        e1_contrasts[key] = {}
        for st in STUDENT_TYPES:
            e1_contrasts[key][st] = {}
            for metric in CONTRAST_METRICS:
                e1_contrasts[key][st][metric] = cb.diff_ci(
                    ablation.case_means(by[(a, st)], metric),
                    ablation.case_means(by[(b, st)], metric),
                )

    per_category = {}
    for (arm, st), rows in by.items():
        for cat in CATEGORY_ORDER:
            sub = [e for e in rows if e["category"] == cat]
            if sub:
                per_category.setdefault(arm, {}).setdefault(st, {})[cat] = {
                    m: point_metric(sub, m) for m in ablation.METRICS
                }
                per_category[arm][st][cat]["n_episodes"] = len(sub)

    frozen_path = (
        HERE.parent / "2026-10-20_llm_v4_v5" / "v5" / "out" / "test_category_eps05_corrected_episodes.json"
    )
    reproduction = {
        "frozen_episodes": str(frozen_path.relative_to(ROOT)),
        "n_compared": 0,
        "episode_mismatches": 0,
        "mismatch_examples": [],
        "max_abs_aggregate_diff": None,
    }
    if frozen_path.exists():
        frozen = [
            e for e in load_json(frozen_path)
            if e["rule"] == "stability_mixed" and e["selection"] == "maxent"
        ]
        frozen_by = {(e["case_id"], e["student_type"], e["seed"]): e for e in frozen}
        fields = ("terminal_kind", "terminal_id", "n_obs", "stopped", "budget_exhausted", "correct", "false_remediation")
        for st in STUDENT_TYPES:
            for e in by.get(("sm_b6", st), []):
                key = (e["case_id"], e["student_type"], e["seed"])
                f = frozen_by.get(key)
                reproduction["n_compared"] += 1
                if f is None:
                    reproduction["episode_mismatches"] += 1
                    continue
                diffs = {field: (e[field], f[field]) for field in fields if e[field] != f[field]}
                if diffs:
                    reproduction["episode_mismatches"] += 1
                    if len(reproduction["mismatch_examples"]) < 5:
                        reproduction["mismatch_examples"].append({"key": key, "diffs": diffs})
        audit_path = HERE.parent / "2026-10-20_llm_v4_v5" / "v5" / "out" / "final_audit" / "diagnosis_audit.json"
        if audit_path.exists():
            audit = load_json(audit_path)["table"]["stability_mixed_maxent"]
            max_diff = 0.0
            for st, metric, audit_key in [
                ("stable", "correct_stop", "correct_stop"),
                ("stable", "correct", "correct"),
                ("slip", "false", "false"),
                ("stable", "n_inquiries", "n_inquiries"),
                ("slip", "n_inquiries", "n_inquiries"),
            ]:
                ours = aggregates["sm_b6"][st][metric]["mean"]
                frozen_val = float(audit[st][audit_key]["mean"])
                max_diff = max(max_diff, abs(ours - frozen_val))
            reproduction["max_abs_aggregate_diff"] = max_diff

    summary = {
        "settings": {
            "experiment": cfg["experiment"],
            "cases": cfg["cases"],
            "priors": cfg["priors"],
            "seeds": seeds,
            "eps": eps,
            "caps": list(CAPS),
            "arms": list(ARMS),
            "bootstrap": int(cfg["bootstrap"]),
            "bootstrap_seed": int(cfg["bootstrap_seed"]),
        },
        "status": "ok",
        "duration_seconds": round(time.time() - started, 2),
        "manifest": manifest,
        "skipped": dict(skipped),
        "n_cases": len(cases),
        "n_episodes": len(episodes),
        "aggregates": aggregates,
        "same_cap_contrasts": same_cap_contrasts,
        "cap_contrasts": cap_contrasts,
        "cross_contrasts": cross_contrasts,
        "e1_contrasts": e1_contrasts,
        "per_category": per_category,
        "reproduction": reproduction,
    }

    out_dir = run_dir / "outputs"
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    (out_dir / "episodes.json").write_text(json.dumps(episodes, ensure_ascii=False), encoding="utf-8")
    (out_dir / "tables.md").write_text(render_tables(summary), encoding="utf-8")
    with (out_dir / "budget_curve.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["arm", "cap", "student_type", "metric", "mean", "ci_low", "ci_high"])
        for arm in ARMS:
            for st in STUDENT_TYPES:
                for metric in METRICS:
                    cell = aggregates.get(arm, {}).get(st, {}).get(metric)
                    if cell:
                        writer.writerow([arm, ARMS[arm]["cap"], st, metric, cell["mean"], cell.get("ci_low"), cell.get("ci_high")])
    (out_dir / "status.json").write_text(
        json.dumps(
            {
                "status": "ok",
                "run_id": run_dir.name,
                "episodes": len(episodes),
                "duration_seconds": summary["duration_seconds"],
                "reproduction": reproduction,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print(f"wrote {run_dir.relative_to(ROOT)}")
    print(f"episodes={len(episodes)} skipped={dict(skipped)}")
    print(
        "reproduction mismatches="
        f"{reproduction['episode_mismatches']}/{reproduction['n_compared']} "
        f"max_abs_agg_diff={reproduction['max_abs_aggregate_diff']}"
    )
    for k in CAPS:
        a = aggregates[f"sm_b{k}"]
        print(
            f"SM cap={k}: slip_false={a['slip']['false']['mean']:.3f} "
            f"slip_abstain={a['slip']['abstain']['mean']:.3f} "
            f"stable_correct={a['stable']['correct']['mean']:.3f} "
            f"stable_abstain={a['stable']['abstain']['mean']:.3f} "
            f"inq={a['mixed']['n_inquiries']['mean']:.2f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
