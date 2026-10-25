#!/usr/bin/env python
"""Extract clean CSV source data for all manuscript figures/tables.

Every value is read from the frozen v5 audit JSONs produced by
``final_audit_v5.py`` and ``feedback_audit_v5.py``. Nothing is hand-typed.

Statistical unit:
  * diagnosis panels: paired comparisons, template-family cluster bootstrap
    (36 families, with replacement and multiplicity, 2000 resamples);
  * feedback panels: paired feedback episodes, family-cluster bootstrap;
  * 95% CIs are the ``cluster`` CIs from the audit files.

Run:  python extract_source_data.py
"""
from __future__ import annotations

import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.dirname(HERE)                      # results/figures
DATA_DIR = os.path.join(FIG_DIR, "data")
V5 = os.path.abspath(os.path.join(FIG_DIR, "..", "..", "experiments", "2026-10-20_llm_v4_v5", "v5"))
DIAG = os.path.join(V5, "out", "final_audit", "diagnosis_audit.json")
FEED = os.path.join(V5, "out", "final_audit", "feedback_audit.json")

os.makedirs(DATA_DIR, exist_ok=True)


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def write_csv(name, header, rows):
    path = os.path.join(DATA_DIR, name)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)
    print(f"wrote {path}  ({len(rows)} rows)")


# ORDER = display order for method rows (main -> baseline -> historical).
METHOD_ORDER = [
    "one_shot_forced",
    "one_shot_typed",
    "random_k3",
    "fixed_k3",
    "maxent_k3",
    "fixed3",
    "stability_maxent",
    "stability_targeted",
    "stability_mixed_maxent",
    "stability_mixed_targeted",
    "stability_mixed_heldout_maxent",
]


def cell(rec, key):
    v = rec.get(key)
    if not isinstance(v, dict):
        return ("", "", "", "")
    return (
        f"{v.get('mean', '')}",
        f"{v.get('ci_low', '')}",
        f"{v.get('ci_high', '')}",
        f"{v.get('n_episodes', '')}",
    )


def extract_diagnosis(d):
    labels = {r["id"]: r["label"] for r in d["rules"]}
    table = d["table"]
    header = [
        "rule_id", "label",
        "stable_correct_mean", "stable_correct_ci_low", "stable_correct_ci_high", "stable_n_episodes",
        "stable_correct_stop_mean", "stable_correct_stop_ci_low", "stable_correct_stop_ci_high",
        "stable_abstain_mean", "stable_abstain_ci_low", "stable_abstain_ci_high",
        "stable_inquiries_mean", "stable_inquiries_ci_low", "stable_inquiries_ci_high",
        "slip_false_mean", "slip_false_ci_low", "slip_false_ci_high", "slip_n_episodes",
        "slip_none_mean", "slip_none_ci_low", "slip_none_ci_high",
        "slip_abstain_mean", "slip_abstain_ci_low", "slip_abstain_ci_high",
        "slip_inquiries_mean", "slip_inquiries_ci_low", "slip_inquiries_ci_high",
        "mixed_false_mean", "mixed_detected_mean", "mixed_pair_mean",
        "mixed_inquiries_mean", "n_cases", "n_episodes_per_type",
    ]
    rows = []
    for rid in METHOD_ORDER:
        rec = table[rid]
        s, sl, mx = rec["stable"], rec["slip"], rec["mixed"]
        sc = cell(s, "correct")
        scs = cell(s, "correct_stop")
        sa = cell(s, "abstain")
        si = cell(s, "n_inquiries")
        sf = cell(sl, "false")
        sn = cell(sl, "none")
        sla = cell(sl, "abstain")
        sli = cell(sl, "n_inquiries")
        rows.append([
            rid, labels[rid],
            sc[0], sc[1], sc[2], sc[3],
            scs[0], scs[1], scs[2],
            sa[0], sa[1], sa[2],
            si[0], si[1], si[2],
            sf[0], sf[1], sf[2], sf[3],
            sn[0], sn[1], sn[2],
            sla[0], sla[1], sla[2],
            sli[0], sli[1], sli[2],
            mx["false"]["mean"], mx["detected"]["mean"], mx["pair"]["mean"],
            mx["n_inquiries"]["mean"], rec["stable"]["n_cases"], rec["stable"]["n_episodes"],
        ])
    write_csv("diagnosis_main.csv", header, rows)


CONTRASTS_OF_INTEREST = {
    "stability_mixed_maxent_minus_fixed3": "stability_mixed/maxent minus fixed3/maxent",
    "maxent_k3_minus_random_k3": "maxent k3 minus random k3",
    "maxent_k3_minus_fixed_k3": "maxent k3 minus fixed-order k3",
    "one_shot_typed_minus_one_shot_forced": "typed one-shot minus forced one-shot",
    "stability_mixed_heldout_maxent_minus_stability_mixed_maxent": "held-out minus stability_mixed",
    "stability_maxent_minus_stability_mixed_maxent": "stability minus stability_mixed",
    "stability_mixed_targeted_minus_stability_mixed_maxent": "targeted minus maxent (stability_mixed)",
    "stability_targeted_minus_stability_maxent": "targeted minus maxent (stability)",
}
CONTRAST_METRICS = ["correct", "false", "correct_stop", "abstain", "none", "n_inquiries", "J5", "J10"]


def extract_contrasts(d):
    c = d["contrasts"]
    header = ["contrast_id", "contrast_label", "student_type", "metric", "mean_diff", "ci_low", "ci_high"]
    rows = []
    for cid, clabel in CONTRASTS_OF_INTEREST.items():
        for stype in ("stable", "slip", "mixed"):
            key = f"{cid}/{stype}"
            if key not in c:
                continue
            for metric in CONTRAST_METRICS:
                if metric not in c[key]:
                    continue
                m = c[key][metric]
                rows.append([cid, clabel, stype, metric, m["mean"], m["ci_low"], m["ci_high"]])
    write_csv("diagnosis_contrasts.csv", header, rows)


def extract_categories(d):
    pc = d["per_category"]
    header = ["category", "stable_n_episodes", "stable_correct_stop_mean",
              "stable_correct_stop_ci_low", "stable_correct_stop_ci_high",
              "slip_n_episodes", "slip_false_mean", "slip_false_ci_low", "slip_false_ci_high",
              "mixed_false_mean"]
    rows = []
    for cat, rec in sorted(pc.items()):
        cs = rec["stable"]["correct_stop"]
        sf = rec["slip"]["false"]
        rows.append([
            cat,
            rec["stable"].get("n_episodes", ""),
            cs["mean"], cs["ci_low"], cs["ci_high"],
            rec["slip"].get("n_episodes", ""),
            sf["mean"], sf["ci_low"], sf["ci_high"],
            rec["mixed"]["false"]["mean"],
        ])
    write_csv("diagnosis_categories.csv", header, rows)


def extract_mixed_stress(d):
    table = d["table"]
    label = {r["id"]: r["label"] for r in d["rules"]}
    header = ["rule_id", "label", "mixed_false_mean", "mixed_false_ci_low", "mixed_false_ci_high",
              "mixed_detected_mean", "mixed_detected_ci_low", "mixed_detected_ci_high",
              "mixed_pair_mean", "mixed_pair_ci_low", "mixed_pair_ci_high",
              "mixed_none_mean", "mixed_abstain_mean", "mixed_inquiries_mean"]
    order = ["stability_maxent", "stability_mixed_maxent", "stability_mixed_heldout_maxent"]
    rows = []
    for rid in order:
        mx = table[rid]["mixed"]
        rows.append([
            rid, label[rid],
            mx["false"]["mean"], mx["false"]["ci_low"], mx["false"]["ci_high"],
            mx["detected"]["mean"], mx["detected"]["ci_low"], mx["detected"]["ci_high"],
            mx["pair"]["mean"], mx["pair"]["ci_low"], mx["pair"]["ci_high"],
            mx["none"]["mean"], mx["abstain"]["mean"], mx["n_inquiries"]["mean"],
        ])
    write_csv("mixed_stress.csv", header, rows)


def extract_sensitivity_90_87(d):
    ov = d["original_vs_corrected"]
    label = {r["id"]: r["label"] for r in d["rules"]}
    header = ["rule_id", "label", "scope", "metric", "mean", "ci_low", "ci_high"]
    metrics = ["stable/correct", "stable/correct_stop", "slip/false", "mixed/false"]
    rows = []
    for rid, rec in ov.items():
        for scope in ("original_90", "protocol_valid_87"):
            sc = rec.get(scope, {})
            for metric in metrics:
                if metric not in sc:
                    continue
                m = sc[metric]
                rows.append([rid, label.get(rid, rid), scope, metric, m["mean"], m["ci_low"], m["ci_high"]])
    write_csv("sensitivity_90_87.csv", header, rows)


def extract_j(d):
    js = d["j_sensitivity"]
    header = ["rule_id", "ratio", "J5", "J10"]
    rows = []
    for rid, rec in js.items():
        for ratio in ("stable_slip_50_50", "stable_slip_70_30", "stable_slip_30_70", "all_50_25_25"):
            if ratio in rec:
                rows.append([rid, ratio, rec[ratio]["J5"], rec[ratio]["J10"]])
    write_csv("j_sensitivity.csv", header, rows)


def extract_feedback_pointwise(d):
    pw = d["pointwise"]
    thead = ["scope", "condition", "n", "target_hit_weighted", "target_hit_ci_low", "target_hit_ci_high",
             "misleading_weighted", "misleading_ci_low", "misleading_ci_high",
             "overall_weighted", "overall_ci_low", "overall_ci_high"]
    rows = []
    for scope in ("deepseek_full", "glm_subset"):
        for cond, rec in pw[scope].items():
            th, ml, ov = rec["true_target_hit"], rec["misleading"], rec["overall"]
            rows.append([scope, cond, rec["n"],
                         th["weighted"], th["ci_low"], th["ci_high"],
                         ml["weighted"], ml["ci_low"], ml["ci_high"],
                         ov["weighted"], ov["ci_low"], ov["ci_high"]])
    write_csv("feedback_pointwise.csv", thead, rows)


COMPARISONS = ["one_shot", "no_diagnosis", "oracle"]
COMP_LABEL = {"one_shot": "pipeline minus fair one-shot",
              "no_diagnosis": "pipeline minus no-diagnosis",
              "oracle": "pipeline minus oracle"}
FEED_METRICS = ["true_target_hit", "overall", "misleading"]
SCOPES = {
    "deepseek_full": "DeepSeek full (116 ep)",
    "glm_subset": "GLM subset (60 ep)",
    "common_deepseek": "Common subset DeepSeek (60 ep)",
    "common_glm": "Common subset GLM (60 ep)",
}


def extract_feedback_paired(d):
    paired = d["paired"]
    header = ["scope", "scope_label", "comparison", "comparison_label", "metric", "n_pairs",
              "mean", "ci_low", "ci_high"]
    rows = []

    def add(scope_key, scope_label, blob):
        for comp in COMPARISONS:
            if comp not in blob:
                continue
            for metric in FEED_METRICS:
                if metric not in blob[comp]:
                    continue
                m = blob[comp][metric]
                cl = m.get("cluster", {})
                rows.append([scope_key, scope_label, comp, COMP_LABEL[comp], metric,
                             m.get("n_pairs", ""), cl.get("mean", ""), cl.get("ci_low", ""), cl.get("ci_high", "")])

    add("deepseek_full", SCOPES["deepseek_full"], paired["deepseek_full"])
    add("glm_subset", SCOPES["glm_subset"], paired["glm_subset"])
    add("common_deepseek", SCOPES["common_deepseek"], paired["common"]["deepseek"])
    add("common_glm", SCOPES["common_glm"], paired["common"]["glm"])
    write_csv("feedback_paired.csv", header, rows)


def extract_feedback_cross(d):
    cp = d["cross_pointwise"]
    xp = d["cross_pairwise"]
    header = ["item", "value"]
    rows = [["n_common_pointwise", cp["n"]],
            ["n_common_pairwise_comparisons", xp.get("n_comparisons", "")]]
    for field, rec in cp.get("fields", {}).items():
        rows.append([f"pointwise_{field}_exact_agreement", rec.get("exact_agreement", "")])
    for k in ("outcome_agreement", "cohen_kappa", "per_order_agreement"):
        if k in xp:
            rows.append([k, xp[k]])
    write_csv("feedback_cross.csv", header, rows)


def extract_retry(d):
    rq = d["retry_quality"]
    header = ["subset", "n", "raw_overall", "final_overall", "raw_target_hit", "final_target_hit",
              "raw_leak", "final_leak"]
    rows = []
    for subset, rec in rq.items():
        rows.append([subset, rec["n"], rec["raw_overall"], rec["final_overall"],
                     rec["raw_true_target_hit"], rec["final_true_target_hit"],
                     rec["raw_answer_leak"], rec["final_answer_leak"]])
    write_csv("validator_retry.csv", header, rows)
    rt = d["retry"]
    header2 = ["scope", "n_records", "n_retried", "init_math_incorrect", "final_math_incorrect",
               "init_leak_suspected", "final_leak_suspected", "init_unverifiable", "final_unverifiable"]
    rows2 = []
    for scope, rec in rt.items():
        rows2.append([scope, rec["n_records"], rec["n_retried"], rec["init_math_incorrect"],
                      rec["final_math_incorrect"], rec["init_leak_suspected"], rec["final_leak_suspected"],
                      rec["init_math_unverifiable"], rec["final_math_unverifiable"]])
    write_csv("validator_counts.csv", header2, rows2)


def main():
    diag = load(DIAG)
    feed = load(FEED)
    extract_diagnosis(diag)
    extract_contrasts(diag)
    extract_categories(diag)
    extract_mixed_stress(diag)
    extract_sensitivity_90_87(diag)
    extract_j(diag)
    extract_feedback_pointwise(feed)
    extract_feedback_paired(feed)
    extract_feedback_cross(feed)
    extract_retry(feed)
    print("done.")


if __name__ == "__main__":
    main()
