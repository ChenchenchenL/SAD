from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
EXP = ROOT / "experiments/2026-10-22_independent_templates_v6b"
RUN = EXP / "runs/20261022T015122Z_v6b_arms_final"
OUT = ROOT / "results/figures/qa/three_experiments_source_audit.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mean_ci(values, families, seed=20261028):
    names = sorted(set(families.values()))
    sums = np.array([sum(v for c, v in values.items() if families[c] == f) for f in names])
    sizes = np.array([sum(families[c] == f for c in values) for f in names])
    draws = np.random.default_rng(seed).integers(0, len(names), (2000, len(names)))
    reps = sums[draws].sum(axis=1) / sizes[draws].sum(axis=1)
    low, high = np.percentile(reps, [2.5, 97.5])
    return {"mean": float(np.mean(list(values.values()))), "ci_low": float(low), "ci_high": float(high)}


def case_values(rows, metric):
    by_case = defaultdict(list)
    for e in rows:
        if metric == "correct":
            v = e["terminal_kind"] == "single" and e["terminal_id"] == e["true_id"]
        elif metric == "false":
            v = e["terminal_kind"] in {"single", "pair", "mixed"}
        elif metric in {"none", "abstain"}:
            v = e["terminal_kind"] == metric
        else:
            v = e[metric]
        by_case[e["case_id"]].append(float(v))
    return {c: float(np.mean(v)) for c, v in by_case.items()}


def audit_v6b():
    s = load(RUN / "outputs/summary.json")
    episodes = load(RUN / "outputs/episodes.json")
    arm_names = {"stability_mixed_reference": "full_sm", "posterior_plus_E": "e_only",
                 "posterior_plus_E_LR_pairguard_extra_none": "simplified_sm", "fixed3": "fixed3"}
    episodes = [dict(e, arm=arm_names[e["arm"]]) for e in episodes]
    families = {e["case_id"]: e["family"] for e in episodes}
    checks = []
    for arm in ("full_sm", "e_only", "simplified_sm", "fixed3"):
        for typ, metrics in (("stable", ("correct", "n_inquiries")),
                             ("slip", ("false", "none", "abstain", "n_inquiries"))):
            rows = [e for e in episodes if e["arm"] == arm and e["student_type"] == typ]
            for metric in metrics:
                actual = mean_ci(case_values(rows, metric), families)
                expected = s["aggregates"]["v6b"][arm][typ][metric]
                delta = max(abs(actual[k] - expected[k]) for k in actual)
                checks.append({"arm": arm, "type": typ, "metric": metric,
                               "computed": actual, "max_abs_error": delta})
                assert delta < 1e-12, (arm, typ, metric, actual, expected)
    paired = []
    for a, b in (("full_sm", "fixed3"), ("e_only", "fixed3"),
                 ("simplified_sm", "full_sm"), ("full_sm", "e_only")):
        for typ, metric in (("stable", "correct"), ("slip", "false"), ("slip", "n_inquiries")):
            av = case_values([e for e in episodes if e["arm"] == a and e["student_type"] == typ], metric)
            bv = case_values([e for e in episodes if e["arm"] == b and e["student_type"] == typ], metric)
            assert set(av) == set(bv)
            actual = mean_ci({c: av[c] - bv[c] for c in av}, families)
            key = f"{a} - {b}/{typ}"
            expected = s["contrasts"]["v6b"][key][metric]
            delta = max(abs(actual[k] - expected[k]) for k in actual)
            assert delta < 1e-12, (key, metric, actual, expected)
            paired.append({"contrast": key, "metric": metric, "computed": actual, "max_abs_error": delta})
    manifest = load(RUN / "manifest.json")
    mapping = {"config": EXP / "config.json",
               "v6b_cases": EXP / "data/cases_test_v6b.json",
               "v6b_priors": EXP / "data/priors_v6b_category.jsonl",
               "v6b_freeze": EXP / "data/v6b_freeze.json",
               "v6b_audit": EXP / "data/v6b_data_audit.json",
               "v5_cases": EXP / "data/reference_v5/cases_test_v5_exclusion_corrected.json",
               "v5_priors": EXP / "data/reference_v5/priors_test_category.jsonl",
               "v5_frozen_episodes": EXP / "data/reference_v5/test_category_eps05_corrected_episodes.json",
               "published_ablation": ROOT / "experiments/2026-10-21_stability_ablation/runs/20261021T065513Z_ablation_ext/outputs/summary.json"}
    hashes = []
    for key, expected in manifest["sha256"].items():
        role, filename = key.split(":", 1)
        if role == "code":
            path = EXP / ("run.py" if filename == "run.py" else f"src/{filename}")
        elif role.startswith("v6b_bank"):
            path = EXP / "data" / filename
        elif role.startswith("v5_bank"):
            path = EXP / "data/reference_v5" / filename
        else:
            path = mapping[role]
        actual = sha(path)
        hashes.append({"key": key, "path": str(path.relative_to(ROOT)), "expected": expected,
                       "actual": actual, "match": actual == expected})
        assert actual == expected, (key, path)
    keys = [(e["arm"], e["student_type"], e["case_id"], e["seed"]) for e in episodes]
    assert len(keys) == len(set(keys)) == 5400
    assert load(EXP / "config.json") == load(RUN / "config.snapshot.json") == s["protocol"]
    return {"run": str(RUN.relative_to(ROOT)), "episodes": len(episodes),
            "cases": len(families), "families": len(set(families.values())),
            "duplicate_episode_keys": len(keys) - len(set(keys)),
            "config_identity": True, "manifest_checks": hashes,
            "aggregate_checks": checks, "paired_checks": paired,
            "formal_output_hashes": {str(p.relative_to(ROOT)): sha(p) for p in RUN.rglob("*") if p.is_file()},
            "boundary": "README PASS and point-estimate -5pp criterion are not noninferiority evidence; final accuracy CI crosses -5pp; corrected v6b only; v5 from this summary uses the same four arms."}


def pointer(parts):
    return "/" + "/".join(str(p).replace("~", "~0").replace("/", "~1") for p in parts)


def write_csv(name, rows):
    path = ROOT / "results/figures/data" / name
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return {"path": str(path.relative_to(ROOT)), "rows": len(rows), "sha256": sha(path)}


def formal_record(run, name, expected_count):
    summary = load(run / "outputs/summary.json")
    episodes = load(run / "outputs/episodes.json")
    is_noise = name == "noise"
    keys = [(e.get("condition"), e["arm"], e["student_type"], e["case_id"], e["seed"]) for e in episodes]
    assert len(keys) == len(set(keys)) == expected_count
    cfg = load(run / "config.snapshot.json")
    exp = run.parents[1]
    config = exp / ("config_eps010.json" if name == "selection_eps010" else "config.json")
    assert cfg == load(config)
    for key in ("bootstrap", "bootstrap_seed", "seeds"):
        assert summary["settings"][key] == cfg[key]
    manifest = load(run / "manifest.json")
    manifest_checks = []
    for entry in manifest["inputs"]:
        path = ROOT / entry["path"]
        actual = sha(path)
        match = actual == entry["sha256"]
        known_conflict = name == "selection_eps005" and path == exp / "run.py"
        assert match or known_conflict, (name, path)
        manifest_checks.append({"path": entry["path"], "expected": entry["sha256"], "actual": actual,
                                "match": match, "historical_conflict": known_conflict and not match})
    families = {e["case_id"]: e["family"] for e in episodes}
    assert len(families) == 87 and len(set(families.values())) == 36
    assert all(n == 5 for n in Counter((e.get("condition"), e["arm"], e["student_type"], e["case_id"]) for e in episodes).values())
    checks = []
    metrics = {"stable": ("correct", "n_inquiries"), "slip": ("false", "none", "abstain", "n_inquiries")}
    grouped = defaultdict(list)
    for e in episodes:
        if e["student_type"] not in metrics:
            continue
        if is_noise and not e["condition"].startswith("iid_"):
            continue
        grouped[(e.get("condition"), e["arm"], e["student_type"])].append(e)
    for (condition, arm, typ), rows in grouped.items():
        group_key = f"{condition}|{arm}|{typ}" if is_noise else arm
        for metric in metrics[typ]:
            computed = mean_ci(case_values(rows, metric), families, seed=cfg["bootstrap_seed"])
            expected = summary["aggregates"][group_key][metric] if is_noise else summary["aggregates"][arm][typ][metric]
            error = max(abs(computed[k] - expected[k]) for k in computed)
            assert error < 1e-12, (name, group_key, metric, computed, expected)
            checks.append({"condition": condition, "arm": arm, "type": typ, "metric": metric,
                           "computed": computed, "max_abs_error": error})
    report = {"run": str(run.relative_to(ROOT)), "episodes": len(episodes), "cases": len(families),
              "families": len(set(families.values())), "duplicate_episode_keys": 0,
              "config_identity": True, "manifest_checks": manifest_checks, "aggregate_checks": checks,
              "formal_output_hashes": {str(p.relative_to(ROOT)): sha(p) for p in run.rglob("*") if p.is_file()}}
    return summary, report


def extract_selection(run, summary, epsilon):
    rows, differences = [], []
    source = str((run / "outputs/summary.json").relative_to(ROOT))
    for arm, groups in summary["aggregates"].items():
        if arm == "k3_random_legacy":
            continue
        block = "fixed3" if arm.startswith("k3_") else "sm"
        method = arm.split("_", 1)[1].replace("fixed_order", "fixed")
        for typ in ("stable", "slip"):
            for metric in ("correct", "false", "none", "abstain", "n_inquiries", "correct_stop"):
                cell = groups[typ][metric]
                rows.append({"epsilon": epsilon, "block": block, "arm": method, "student_type": typ,
                             "metric": metric, **cell, "unit": "inquiries" if metric == "n_inquiries" else "proportion",
                             "n_families": 36, "n_seeds": 5, "bootstrap_seed": 20261026,
                             "source_file": source, "source_pointer": pointer(["aggregates", arm, typ, metric])})
    for contrast, cells in summary["contrasts"].items():
        if "legacy" in contrast:
            continue
        for key, cell in cells.items():
            typ, metric = key.split("/", 1)
            if metric not in {"correct", "false", "n_inquiries", "none", "abstain"}:
                continue
            differences.append({"epsilon": epsilon, "contrast": contrast, "student_type": typ,
                                "metric": metric, **cell, "n_families": 36, "bootstrap_seed": 20261026,
                                "source_file": source, "source_pointer": pointer(["contrasts", contrast, key])})
    return rows, differences


def extract_noise(run, summary):
    rows, differences = [], []
    source = str((run / "outputs/summary.json").relative_to(ROOT))
    for key, cells in summary["aggregates"].items():
        condition, arm, typ = key.split("|")
        if not condition.startswith("iid_") or typ == "mixed":
            continue
        for metric in ("correct", "false", "none", "abstain", "n_inquiries"):
            rows.append({"condition": condition, "epsilon": float(condition.split("_")[1]),
                         "diagnostician_epsilon": .05, "arm": arm, "student_type": typ, "metric": metric,
                         **cells[metric], "n_families": 36, "n_seeds": 5, "bootstrap_seed": 20261026,
                         "source_file": source, "source_pointer": pointer(["aggregates", key, metric])})
    for section in ("within_contrasts", "condition_contrasts"):
        for contrast, groups in summary[section].items():
            for typ in ("stable", "slip"):
                for metric in ("correct", "false", "n_inquiries"):
                    differences.append({"section": section, "contrast": contrast, "student_type": typ,
                                        "metric": metric, **groups[typ][metric], "n_families": 36,
                                        "bootstrap_seed": 20261026, "source_file": source,
                                        "source_pointer": pointer([section, contrast, typ, metric])})
    return rows, differences


def main():
    selection_root = ROOT / "experiments/2026-10-21_selection_comparison/runs"
    run_a = selection_root / "20261022T010936Z_selection_eps005"
    run_b = selection_root / "20261022T011015Z_selection_eps010b"
    run_n = ROOT / "experiments/2026-10-22_noise_misspecification/runs/20261022T011153Z_noise_misspecification"
    a, ar = formal_record(run_a, "selection_eps005", 7830)
    b, br = formal_record(run_b, "selection_eps010", 7830)
    n, nr = formal_record(run_n, "noise", 31320)
    am, ac = extract_selection(run_a, a, .05)
    bm, bc = extract_selection(run_b, b, .10)
    nm, nc = extract_noise(run_n, n)
    report = {"scope": "Read-only verification of saved formal data; no simulation or API calls.",
              "v6b": audit_v6b(), "selection_eps005": ar, "selection_eps010": br, "noise": nr,
              "source_csv": [write_csv("selection_comparison_means.csv", am + bm),
                             write_csv("selection_comparison_contrasts.csv", ac + bc),
                             write_csv("noise_misspecification_means.csv", nm),
                             write_csv("noise_misspecification_contrasts.csv", nc)],
              "display_scope": {"fig1": "eps .05, four nonlegacy strategies, stable/slip only; matched .10 stored as sensitivity, not drawn",
                                "fig5": "Four iid conditions only; mixed and stationary-restart burst excluded from main curves as requested; all formal episodes retained",
                                "composition": "Mutually exclusive false/none/abstain point estimates; component CIs retained in means CSV but not drawn on stacks"},
              "historical_issues": ["Selection eps .05 run.py differs from historical manifest; exact historical script bytes unrecovered. Input/data hashes and stored statistics match.",
                                    "v6b README PASS is a descriptive point-estimate rule, not noninferiority evidence. Old correct-stop fixed3 is N/A.",
                                    "Noise data README inherits an old engine hash; current burst engine matches formal manifest.",
                                    "Inherited v5 freeze mentions original 90/30 scope; formal v5 analyses use corrected 87/29.",
                                    "One inherited single-answer item has nonnormalized per-hypothesis likelihood; formal MaxEnt/IG paths did not select it (prior review); these results do not establish arbitrary-bank IG validity."]}
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(OUT.relative_to(ROOT)),
                      "aggregate_CI_checks": sum(len(report[k]["aggregate_checks"]) for k in ("v6b", "selection_eps005", "selection_eps010", "noise")),
                      "v6b_paired_CI_checks": len(report["v6b"]["paired_checks"]),
                      "csv": report["source_csv"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
