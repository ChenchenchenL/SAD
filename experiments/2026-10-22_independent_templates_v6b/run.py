"""Run the four-arm comparison on the v6 independent template set and on the
v5 reference set, with paired family-cluster bootstrap contrasts and the
pre-registered replication criteria.

Arms:
  full_sm        v5 stability_mixed (via the verified ablation reference arm)
  e_only         posterior + E gate only
  simplified_sm  full single gate + extra-none, pair/mixed terminals off
  fixed3         maxent, exactly three additional inquiries
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "src"))

import ablation as ab  # noqa: E402
import v5_engine as eng  # noqa: E402
from g0_lib import prior_weights  # noqa: E402

CATEGORIES = ["subtraction", "fractions", "decimals", "negative_numbers",
              "order_of_operations", "percentages"]
TYPES = ("stable", "slip", "mixed")
ARMS = ("full_sm", "e_only", "simplified_sm", "fixed3")
ARM_MAP = {
    "full_sm": "stability_mixed_reference",
    "e_only": "posterior_plus_E",
    "simplified_sm": "posterior_plus_E_LR_pairguard_extra_none",
}
METRICS = ("correct", "correct_stop", "false", "n_inquiries", "none", "abstain", "J5")
CONTRAST_PAIRS = [
    ("full_sm", "fixed3"),
    ("e_only", "fixed3"),
    ("simplified_sm", "fixed3"),
    ("full_sm", "e_only"),
    ("simplified_sm", "full_sm"),
]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_priors(path: Path) -> dict:
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get("http_status") == 200 and r.get("top10"):
            # Last row wins, matching the frozen v5 loader used to generate the
            # published episodes. The cached files are frozen, so this is
            # deterministic; duplicate prompts keep their final cached response.
            out[r["key"]] = r
    return out


def load_dataset(name: str, cases_path: Path, priors_path: Path, bank_dir: Path,
                 prefix: str, eps: float, seeds: int):
    cases = load_json(cases_path)
    priors = load_priors(priors_path)
    models = {}
    banks = {}
    for cat in CATEGORIES:
        bank = load_json(bank_dir / f"{prefix}{cat}.json")
        banks[cat] = bank
        singles = [h["id"] for h in bank["hypotheses"]]
        models[cat] = eng.build_model(cat, bank["items"], singles, with_pairs=True, eps=eps)
    return {"name": name, "cases": cases, "priors": priors, "models": models,
            "banks": banks, "seeds": seeds, "eps": eps}


def episode_from_result(res, seed: int, arm: str) -> dict:
    return {
        "arm": arm, "selection": res.selection, "student_type": res.student_type,
        "case_id": res.case_id, "family": res.family, "category": res.category,
        "true_id": res.true_id, "true_pair": res.true_pair,
        "terminal_kind": res.terminal_kind, "terminal_id": res.terminal_id,
        "terminal_p": float(res.terminal_p), "n_obs": int(res.n_obs),
        "n_inquiries": int(res.n_inquiries), "stopped": bool(res.stopped),
        "budget_exhausted": bool(res.budget_exhausted), "correct": bool(res.correct),
        "false_remediation": bool(res.false_remediation), "seed": int(seed),
        "J5": float(res.n_obs + 5.0 * float(res.false_remediation)),
        "J10": float(res.n_obs + 10.0 * float(res.false_remediation)),
    }


def run_dataset(ds) -> dict:
    episodes = defaultdict(list)
    skipped = Counter()
    for case in ds["cases"]:
        row = ds["priors"].get(case.get("key"))
        if row is None:
            skipped["missing_prior"] += 1
            continue
        cat = case["category"]
        model = ds["models"][cat]
        weights = prior_weights(row["top10"], model.singles)
        prior = model.prior(weights)
        for st in TYPES:
            for seed in range(ds["seeds"]):
                for arm in ARMS:
                    if arm == "fixed3":
                        res = eng.run_budget_episode(model, prior, case, st, "maxent", 3,
                                                     partner=None, seed=seed, eps=ds["eps"])
                    else:
                        res = ab.run_episode_ablation(model, prior, case, st, ARM_MAP[arm],
                                                      partner=None, seed=seed, eps=ds["eps"],
                                                      max_obs=7)
                    if res is None:
                        skipped[f"{arm}/{st}"] += 1
                        continue
                    if arm == "fixed3":
                        episodes[(arm, st)].append(episode_from_result(res, seed, arm))
                    else:
                        episodes[(arm, st)].append(ab.episode_to_dict(res, seed))
    return {"episodes": episodes, "skipped": dict(skipped)}


def summarize(episodes: dict, cb: ab.ClusterBoot) -> dict:
    out = {}
    for (arm, st), rows in episodes.items():
        out.setdefault(arm, {})[st] = ab.summarize_arm(rows, cb)
    return out


def contrasts(episodes: dict, cb: ab.ClusterBoot) -> dict:
    return ab.arm_contrasts(episodes, CONTRAST_PAIRS, list(METRICS) + ["J10"], cb)


def prior_quality(ds) -> dict:
    ok = 0
    top1 = 0
    top10 = 0
    for case in ds["cases"]:
        row = ds["priors"].get(case.get("key"))
        if row is None:
            continue
        ok += 1
        ids = row.get("top10") or []
        cat_ids = [x for x in ids if x.split(".")[0] == case["category"]]
        top10 += case["true_id"] in cat_ids
        top1 += bool(cat_ids) and cat_ids[0] == case["true_id"]
    return {"n_cases_with_prior": ok, "top1_category": top1 / ok if ok else None,
            "top10_category": top10 / ok if ok else None}


def verify_against_frozen(v5_run: dict, frozen_path: Path) -> dict:
    frozen = load_json(frozen_path)
    ref = {(e["case_id"], e["student_type"], e["seed"]): e
           for e in frozen if e.get("rule") == "stability_mixed" and e.get("selection") == "maxent"}
    got = {}
    for st in TYPES:
        for e in v5_run["episodes"][("full_sm", st)]:
            got[(e["case_id"], e["student_type"], e["seed"])] = e
    common = sorted(set(ref) & set(got))
    mism = 0
    examples = []
    for k in common:
        a, b = ref[k], got[k]
        fields = ("terminal_kind", "terminal_id", "n_obs", "n_inquiries", "stopped",
                  "budget_exhausted", "correct", "false_remediation")
        bad = [f for f in fields if a[f] != b[f]]
        if bad:
            mism += 1
            if len(examples) < 5:
                examples.append({"key": list(k), "fields": bad})
    return {"n_frozen": len(ref), "n_got": len(got), "n_common": len(common),
            "n_mismatch": mism, "examples": examples, "pass": mism == 0 and len(common) == len(ref) == len(got)}


def verify_against_published(v5_summary: dict, published_path: Path) -> dict:
    pub = load_json(published_path)["aggregates"]
    checks = []
    worst = 0.0
    for arm, pub_arm in (("full_sm", "stability_mixed_reference"),
                         ("e_only", "posterior_plus_E"),
                         ("simplified_sm", "posterior_plus_E_LR_pairguard_extra_none")):
        for st in TYPES:
            for metric in ("correct", "correct_stop", "false", "n_inquiries"):
                ours = v5_summary[arm][st][metric]["mean"]
                theirs = pub[pub_arm][st][metric]["mean"]
                d = abs(ours - theirs)
                worst = max(worst, d)
                if d > 1e-9:
                    checks.append({"arm": arm, "type": st, "metric": metric, "ours": ours, "published": theirs, "diff": d})
    return {"worst_abs_diff": worst, "n_mismatch": len(checks), "mismatches": checks[:10], "pass": not checks}


def eval_replication(v6_contrasts: dict, criteria: dict) -> dict:
    def c(a, b, st, metric):
        return v6_contrasts[f"{a} - {b}/{st}"][metric]
    out = {}
    r1_false = c("full_sm", "fixed3", "slip", "false")
    r1_stop = c("full_sm", "fixed3", "stable", "correct_stop")
    r1_correct = c("full_sm", "fixed3", "stable", "correct")
    out["R1_full_sm_vs_fixed3"] = {
        "slip_false": r1_false, "stable_correct_stop": r1_stop,
        "stable_correct": r1_correct,
        "pass": (r1_false["mean"] <= criteria["R1_full_sm_vs_fixed3"]["slip_false_diff_max"]
                 and r1_false["ci_high"] < 0
                 and r1_stop["mean"] >= criteria["R1_full_sm_vs_fixed3"]["stable_correct_stop_diff_min"]),
        "pass_substantive": (r1_false["mean"] <= criteria["R1_full_sm_vs_fixed3"]["slip_false_diff_max"]
                             and r1_false["ci_high"] < 0
                             and r1_correct["mean"] >= criteria["R1_full_sm_vs_fixed3"].get("stable_correct_diff_min", -0.05)),
    }
    r2_false = c("e_only", "fixed3", "slip", "false")
    r2_stop = c("e_only", "fixed3", "stable", "correct_stop")
    r2_correct = c("e_only", "fixed3", "stable", "correct")
    out["R2_e_only_vs_fixed3"] = {
        "slip_false": r2_false, "stable_correct_stop": r2_stop,
        "stable_correct": r2_correct,
        "pass": (r2_false["mean"] <= criteria["R2_e_only_vs_fixed3"]["slip_false_diff_max"]
                 and r2_stop["mean"] >= criteria["R2_e_only_vs_fixed3"]["stable_correct_stop_diff_min"]),
        "pass_substantive": (r2_false["mean"] <= criteria["R2_e_only_vs_fixed3"]["slip_false_diff_max"]
                             and r2_correct["mean"] >= criteria["R2_e_only_vs_fixed3"].get("stable_correct_diff_min", -0.05)),
    }
    r3_inq = c("full_sm", "e_only", "slip", "n_inquiries")
    r3_stop = c("full_sm", "e_only", "stable", "correct_stop")
    out["R3_full_sm_vs_e_only"] = {
        "slip_inquiries": r3_inq, "stable_correct_stop": r3_stop,
        "pass": (r3_inq["mean"] <= criteria["R3_full_sm_vs_e_only"]["slip_inquiries_diff_max"]
                 and abs(r3_stop["mean"]) <= criteria["R3_full_sm_vs_e_only"]["abs_stable_correct_stop_diff_max"]),
    }
    r4_false = c("simplified_sm", "full_sm", "slip", "false")
    r4_inq = c("simplified_sm", "full_sm", "slip", "n_inquiries")
    out["R4_simplified_sm_vs_full_sm"] = {
        "slip_false": r4_false, "slip_inquiries": r4_inq,
        "pass": (r4_false["mean"] <= criteria["R4_simplified_sm_vs_full_sm"]["slip_false_diff_max"]
                 and r4_inq["mean"] <= criteria["R4_simplified_sm_vs_full_sm"]["slip_inquiries_diff_max"]),
    }
    out["all_pass"] = all(v["pass"] for k, v in out.items() if k not in ("all_pass", "all_pass_substantive"))
    out["all_pass_substantive"] = all(
        v.get("pass_substantive", v.get("pass", True)) for k, v in out.items()
        if k not in ("all_pass", "all_pass_substantive"))
    return out


def fmt(x, d=3):
    return "—" if x is None else f"{x:.{d}f}"


def ci(c):
    return f"{c['mean']:.3f} [{c['ci_low']:.3f}, {c['ci_high']:.3f}]"


def diff(c):
    return f"{c['mean']:+.3f} [{c['ci_low']:+.3f}, {c['ci_high']:+.3f}]"


def build_tables(name: str, summary: dict) -> list[str]:
    lines = [f"## {name}", "",
             "| arm | stable correct | stable correct-stop | stable inquiries | slip false | slip none | slip abstain | slip inquiries | mixed false | slip J5 |",
             "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for arm in ARMS:
        s = summary[arm]
        stop = "N/A" if arm == "fixed3" else fmt(s["stable"]["correct_stop"]["mean"])
        lines.append("| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
            arm, ci(s["stable"]["correct"]), stop,
            fmt(s["stable"]["n_inquiries"]["mean"], 2), ci(s["slip"]["false"]),
            fmt(s["slip"]["none"]["mean"]), fmt(s["slip"]["abstain"]["mean"]),
            fmt(s["slip"]["n_inquiries"]["mean"], 2), fmt(s["mixed"]["false"]["mean"]),
            fmt(s["slip"]["J5"]["mean"], 2)))
    lines += ["", "Note: fixed3 has no adaptive correct-stop (budget exhausted); use stable correct for the substantive comparison.", ""]
    return lines


def build_figure(v6_summary, v5_summary, v6_contrasts, out_png, out_pdf):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
    colors = {"full_sm": "#1f77b4", "e_only": "#2ca02c", "simplified_sm": "#9467bd", "fixed3": "#d62728"}
    for ax, (metric, xlabel, ylabel) in zip(axes, [
        ("false", "slip false remediation", "stable correct"),
        ("n_inquiries", "slip additional inquiries", "stable correct"),
    ]):
        for arm in ARMS:
            for summary, filled, label_suffix in ((v6_summary, True, " v6"), (v5_summary, False, " v5")):
                xs = summary[arm]["slip"][metric]["mean"]
                ys = summary[arm]["stable"]["correct"]["mean"]
                ax.scatter([xs], [ys], s=90 if filled else 60, marker="o" if filled else "s",
                           color=colors[arm], edgecolor="black" if not filled else colors[arm],
                           facecolor=colors[arm] if filled else "none", linewidth=1.2,
                           label=f"{arm}{label_suffix}" if metric == "false" else None)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(f"{ylabel} vs {xlabel}")
    axes[0].legend(fontsize=8, loc="best")
    fig.suptitle("Four-arm replication: v6b second item bank (filled) vs v5 reference (hollow)")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(out_png, dpi=200)
    fig.savefig(out_pdf)
    plt.close(fig)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=str(HERE / "config.json"))
    ap.add_argument("--run-name", default="v6_arms")
    args = ap.parse_args()
    cfg = load_json(Path(args.config))
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = HERE / "runs" / f"{ts}_{args.run_name}"
    out = run_dir / "outputs"
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    manifest = {"generated_at": ts, "sha256": {}}
    input_paths = {
        "config": Path(args.config),
        "v6b_cases": HERE / "data/cases_test_v6b.json",
        "v6b_priors": HERE / "data/priors_v6b_category.jsonl",
        "v6b_freeze": HERE / "data/v6b_freeze.json",
        "v6b_audit": HERE / "data/v6b_data_audit.json",
        "v5_cases": HERE / "data/reference_v5/cases_test_v5_exclusion_corrected.json",
        "v5_priors": HERE / "data/reference_v5/priors_test_category.jsonl",
        "v5_frozen_episodes": HERE / "data/reference_v5/test_category_eps05_corrected_episodes.json",
        "published_ablation": HERE.parent / "2026-10-21_stability_ablation/runs/20261021T065513Z_ablation_ext/outputs/summary.json",
    }
    for cat in CATEGORIES:
        input_paths[f"v6b_bank_{cat}"] = HERE / f"data/bank_v6b_{cat}.json"
        input_paths[f"v5_bank_{cat}"] = HERE / f"data/reference_v5/bank_v5_{cat}.json"
    for name, p in input_paths.items():
        manifest["sha256"][f"{name}:{p.name}"] = sha(p)
    for code in sorted((HERE / "src").glob("*.py")):
        manifest["sha256"][f"code:{code.name}"] = sha(code)
    manifest["sha256"]["code:run.py"] = sha(Path(__file__))
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    (run_dir / "config.snapshot.json").write_text(json.dumps(cfg, indent=1), encoding="utf-8")

    v6 = load_dataset("v6b", HERE / "data/cases_test_v6b.json", HERE / "data/priors_v6b_category.jsonl",
                      HERE / "data", "bank_v6b_", cfg["eps"], cfg["seeds"])
    v5 = load_dataset("v5", HERE / "data/reference_v5/cases_test_v5_exclusion_corrected.json",
                      HERE / "data/reference_v5/priors_test_category.jsonl",
                      HERE / "data/reference_v5", "bank_v5_", cfg["eps"], cfg["seeds"])

    v6_run = run_dataset(v6)
    v6_episodes = [e for rows in v6_run["episodes"].values() for e in rows]
    (out / "episodes.json").write_text(json.dumps(v6_episodes, ensure_ascii=False), encoding="utf-8")
    v5_run = run_dataset(v5)

    # ---- self-checks ----
    check_frozen = verify_against_frozen(v5_run, input_paths["v5_frozen_episodes"])
    v5_cb = ab.ClusterBoot({c["case_id"]: c["template_family"] for c in v5["cases"]},
                           n_boot=cfg["bootstrap"], seed=cfg["bootstrap_seed"])
    v5_summary = summarize(v5_run["episodes"], v5_cb)
    check_published = verify_against_published(v5_summary, input_paths["published_ablation"])
    expected_v6 = len(v6["cases"]) * len(TYPES) * cfg["seeds"] * len(ARMS)
    n_v6_episodes = sum(len(v) for v in v6_run["episodes"].values())
    check_counts = {"expected": expected_v6, "got": n_v6_episodes,
                    "per_arm_type": {f"{a}/{t}": len(v6_run["episodes"][(a, t)]) for a in ARMS for t in TYPES},
                    "pass": n_v6_episodes == expected_v6}
    checks_ok = check_frozen["pass"] and check_published["pass"] and check_counts["pass"]

    status = {"timestamp": ts, "checks": {"v5_full_sm_vs_frozen": check_frozen,
                                          "v5_arms_vs_published_ablation": check_published,
                                          "v6_episode_counts": check_counts},
              "checks_pass": checks_ok, "v6_skipped": v6_run["skipped"], "v5_skipped": v5_run["skipped"],
              "elapsed_s": round(time.time() - t0, 1)}
    if not checks_ok:
        (out / "status.json").write_text(json.dumps(status, indent=1), encoding="utf-8")
        print("SELF-CHECK FAILED - no result tables", json.dumps(status)[:2000])
        sys.exit(1)

    v6_cb = ab.ClusterBoot({c["case_id"]: c["template_family"] for c in v6["cases"]},
                           n_boot=cfg["bootstrap"], seed=cfg["bootstrap_seed"])
    v6_summary = summarize(v6_run["episodes"], v6_cb)
    v6_contrasts = contrasts(v6_run["episodes"], v6_cb)
    v5_contrasts = contrasts(v5_run["episodes"], v5_cb)
    replication = eval_replication(v6_contrasts, cfg["replication_criteria"])
    prior_v6 = prior_quality(v6)
    prior_v5 = prior_quality(v5)

    audit = load_json(HERE / "data/v6b_data_audit.json")
    tables = ["# 四臂对比：v6b 第二套题库 vs v5 参照", ""]
    tables += build_tables("v6b 第二套题库（90 cases / 32 families；与 v5 部分结构重叠）", v6_summary) + [""]
    tables += build_tables("v5 参照（87 protocol-valid cases / 36 families）", v5_summary) + [""]
    tables += ["## 配对差（family-cluster bootstrap 95% CI）", "",
               "| contrast | type | metric | v6 | v5 |", "|---|---|---|---:|---:|"]
    for a, b in CONTRAST_PAIRS:
        for st in TYPES:
            for metric in ("false", "correct_stop", "n_inquiries"):
                key = f"{a} - {b}/{st}"
                if key in v6_contrasts and metric in v6_contrasts[key]:
                    tables.append(f"| {a} − {b} | {st} | {metric} | {diff(v6_contrasts[key][metric])} | {diff(v5_contrasts[key][metric])} |")
    tables += ["", "## 预注册复现判据（v6b）", ""]
    for k, v in replication.items():
        if k in ("all_pass", "all_pass_substantive"):
            continue
        detail = "; ".join(f"{m}: {diff(c)}" for m, c in v.items() if isinstance(c, dict) and "mean" in c)
        verdict = 'PASS' if v['pass'] else 'FAIL'
        if "pass_substantive" in v:
            verdict += f"; substantive={'PASS' if v['pass_substantive'] else 'FAIL'}"
        tables.append(f"- **{k}**: {verdict} — {detail}")
    tables += ["", f"**ALL PASS (original criteria): {replication['all_pass']}**",
               f"**ALL PASS (substantive stable-correct criteria): {replication['all_pass_substantive']}**", "",
               "## 先验质量", "",
               "| dataset | n with prior | top-1 (category) | top-10 (category) |", "|---|---:|---:|---:|",
               f"| v6b | {prior_v6['n_cases_with_prior']} | {prior_v6['top1_category']:.3f} | {prior_v6['top10_category']:.3f} |",
               f"| v5 | {prior_v5['n_cases_with_prior']} | {prior_v5['top1_category']:.3f} | {prior_v5['top10_category']:.3f} |"]
    so = audit["structural_overlap_with_v5"]
    tables += ["", "## 结构重叠审计（v5）", "",
               f"- text-parsed correct-answer issues: {audit['text_audit']['n_issues']}",
               f"- v6b items with a matching v5 structural signature: {so['n_v6_items_with_matching_v5_signature']} / {so['n_v6_items']}",
               f"- v6b cases with a matching v5 structural signature: {so['n_v6_cases_with_matching_v5_signature']} / {audit['n_cases']}",
               f"- v6b families with a matching v5 signature: {so['n_v6_families_with_matching_v5_signature']}",
               f"- matching families: {', '.join(so['families']) if so['families'] else '—'}",
               "- v6b is a second item bank / partial structural extension, not a strict unseen-structure holdout."]
    (out / "tables.md").write_text("\n".join(tables), encoding="utf-8")
    build_figure(v6_summary, v5_summary, v6_contrasts, out / "four_arm_replication.png", out / "four_arm_replication.pdf")

    summary = {
        "experiment": "independent_templates_v6b",
        "timestamp": ts,
        "protocol": cfg,
        "checks": status["checks"],
        "data": {"v6b": {"n_cases": len(v6["cases"]),
                         "n_families": len({c["template_family"] for c in v6["cases"]}),
                         "n_labels": len({c["true_id"] for c in v6["cases"]}),
                         "n_episodes": len(v6_episodes),
                         "audit": {k: audit[k] for k in ("correct_audit", "text_audit",
                                                         "independent_bug_audit", "library_audit",
                                                         "case_audit", "overlap_with_v4_v5",
                                                         "structural_overlap_with_v5")}},
                 "v5": {"n_cases": len(v5["cases"]),
                        "n_families": len({c["template_family"] for c in v5["cases"]})}},
        "priors": {"v6b": prior_v6, "v5": prior_v5},
        "aggregates": {"v6b": v6_summary, "v5": v5_summary},
        "contrasts": {"v6b": v6_contrasts, "v5": v5_contrasts},
        "replication": replication,
        "skipped": {"v6": v6_run["skipped"], "v5": v5_run["skipped"]},
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False), encoding="utf-8")
    status["outputs"] = sorted(p.name for p in out.iterdir())
    (out / "status.json").write_text(json.dumps(status, indent=1), encoding="utf-8")
    print("checks:", checks_ok, "| frozen:", check_frozen["n_mismatch"], "| published worst:", check_published["worst_abs_diff"])
    print("v6b priors:", prior_v6)
    print("replication:", {k: (v["pass"] if isinstance(v, dict) and "pass" in v else v) for k, v in replication.items()})
    print("DONE", round(time.time() - t0, 1), "s ->", out)


if __name__ == "__main__":
    main()
