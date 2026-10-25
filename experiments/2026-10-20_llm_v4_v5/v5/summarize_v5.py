"""Build compact tables for docs/results_v5.md."""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"

def load(p):
    return json.loads((OUT / p).read_text(encoding="utf-8"))

def fmt_rate(x):
    return "—" if x is None else f"{x:.3f}"

def fmt_num(x):
    return "—" if x is None else f"{x:.2f}"

def fmt(x, d=3):
    return fmt_rate(x)

def ci(c):
    if not c:
        return "—"
    if c["ci_low"] == c["ci_high"] == c["mean"]:
        return f"{c['mean']:.3f}"
    return f"[{c['ci_low']:.3f}, {c['ci_high']:.3f}]"

def diff_ci(c):
    if not c:
        return "—"
    if c["ci_low"] == c["ci_high"] == c["diff"]:
        return f"{c['diff']:+.3f}"
    return f"{c['diff']:+.3f} [{c['ci_low']:+.3f}, {c['ci_high']:+.3f}]"

S = load("test_category_eps05_corrected_summary.json")
S_ORIG = load("test_category_eps05_summary.json")
A = S["aggregates"]
C = S["case_clustered_CIs"]
K = S["contrasts"]

rows = [
    ("one_shot_forced", "one_shot_forced", "历史强制分类"),
    ("one_shot_typed", "one_shot_typed", "公平 typed"),
    ("random_k3", "random_k3", "随机 + k=3"),
    ("fixed_k3", "fixed_k3", "固定顺序 + k=3"),
    ("maxent_k3", "maxent_k3", "maxent + k=3"),
    ("fixed3", "fixed3", "maxent + 固定3次停止"),
    ("posterior_abstain", "posterior_abstain", "maxent + posterior + budget abstain"),
    ("entropy_abstain", "entropy_abstain", "maxent + entropy + budget abstain"),
    ("stability_maxent", "stability_maxent", "maxent + stability"),
    ("stability_targeted", "stability_targeted", "targeted + stability"),
    ("stability_mixed_maxent", "stability_mixed_maxent", "maxent + stability_mixed"),
    ("stability_mixed_targeted", "stability_mixed_targeted", "targeted + stability_mixed"),
    ("stability_mixed_heldout_maxent", "stability_mixed_heldout_maxent", "maxent + held-out safety"),
]

lines = []
lines.append("| method | stable correct [CI] | stable inquiries | slip error [CI] | slip none | slip abstain | slip inquiries | mixed error [CI] | mixed detected | pair exact |")
lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
for rid, key, label in rows:
    sa = A.get(f"{key}/stable", {})
    sl = A.get(f"{key}/slip", {})
    mx = A.get(f"{key}/mixed", {})
    lines.append(
        "| {} | {} {} | {} | {} {} | {} | {} | {} | {} {} | {} | {} |".format(
            label,
            fmt(sa.get("stable_correct_diagnosed")), ci(C.get(f"{key}/stable", {}).get("correct")),
            fmt_num(sa.get("avg_inquiries")),
            fmt(sl.get("slip_error_rate")), ci(C.get(f"{key}/slip", {}).get("false")),
            fmt(sl.get("slip_explicit_none_rate")), fmt(sl.get("slip_abstain_rate")),
            fmt_num(sl.get("avg_inquiries")),
            fmt(mx.get("mixed_error_rate")), ci(C.get(f"{key}/mixed", {}).get("false")),
            fmt(mx.get("mixed_detected_rate")), fmt(mx.get("pair_identified_rate")),
        )
    )

for metric in ("J5", "J10"):
    lines.append(f"\n### {metric} by type\n")
    lines.append("| method | stable | slip | mixed |")
    lines.append("|---|---:|---:|---:|")
    for _, key, label in rows:
        vals = []
        for st in ("stable", "slip", "mixed"):
            agg = A.get(f"{key}/{st}")
            vals.append(f"{agg[f'J_lambda{metric[1:]}']:.3f}" if agg else "—")
        lines.append(f"| {label} | {' | '.join(vals)} |")

lines.append("\n### Contrasts\n")
lines.append("| contrast | outcome | estimate [95% CI] |")
lines.append("|---|---|---:|")
contrast_keys = [
    ("one_shot_typed_minus_one_shot_forced", "stable", "correct"),
    ("one_shot_typed_minus_one_shot_forced", "slip", "false"),
    ("one_shot_typed_minus_one_shot_forced", "mixed", "false"),
    ("maxent_k3_minus_random_k3", "stable", "correct"),
    ("maxent_k3_minus_random_k3", "slip", "false"),
    ("maxent_k3_minus_fixed_k3", "stable", "correct"),
    ("stability_mixed_maxent_minus_fixed3", "stable", "false"),
    ("stability_mixed_maxent_minus_fixed3", "slip", "false"),
    ("stability_mixed_maxent_minus_fixed3", "mixed", "false"),
    ("stability_mixed_targeted_minus_stability_mixed_maxent", "stable", "correct"),
    ("stability_mixed_targeted_minus_stability_mixed_maxent", "slip", "false"),
    ("stability_targeted_minus_stability_maxent", "stable", "correct"),
    ("stability_targeted_minus_stability_maxent", "slip", "false"),
    ("stability_mixed_heldout_maxent_minus_stability_mixed_maxent", "stable", "correct"),
    ("stability_mixed_heldout_maxent_minus_stability_mixed_maxent", "mixed", "false"),
    ("stability_mixed_heldout_maxent_minus_stability_mixed_maxent", "mixed", "n_inquiries"),
]
for name, st, metric in contrast_keys:
    k = f"{name}/{st}"
    if k in K and metric in K[k]:
        lines.append(f"| {name} · {st} | {metric} | {diff_ci(K[k][metric])} |")

lines.append("\n### Type-proportion sensitivity (J5)\n")
lines.append("| method | stable/slip 50:50 | 70:30 | 30:70 | all 50:25:25 |")
lines.append("|---|---:|---:|---:|---:|")
for _, key, label in rows:
    x = S["j_sensitivity"][key]
    lines.append("| {} | {:.3f} | {:.3f} | {:.3f} | {:.3f} |".format(
        label,
        x["stable_slip_equal"]["J5"], x["stable_heavy_70_30"]["J5"],
        x["slip_heavy_30_70"]["J5"], x["all_50_25_25"]["J5"]))

# prior summaries
prior_cat = json.loads((OUT / "priors_test_category_corrected_summary.json").read_text(encoding="utf-8"))
prior_full = json.loads((OUT / "priors_test_full_corrected_summary.json").read_text(encoding="utf-8"))
lines.append("\n### Priors\n")
lines.append("| prior | n | top-1 | top-10 | category-filtered top-1 | category-filtered top-10 | estimated cost USD |")
lines.append("|---|---:|---:|---:|---:|---:|---:|")
for name, s in (("category", prior_cat), ("full library", prior_full)):
    lines.append("| {} | {} | {:.3f} | {:.3f} | {:.3f} | {:.3f} | {:.4f} |".format(
        name, s["n_ok"], s["top1_global"], s["top10_global_recall"],
        s["top1_category_rank"], s["top10_category_recall"], s["estimated_cost_usd"]))

# global prior / global candidate
G = json.loads((OUT / "test_globalprior_category_corrected_summary.json").read_text(encoding="utf-8"))
GG = json.loads((OUT / "test_globalprior_globalmodel_corrected_summary.json").read_text(encoding="utf-8"))
NDG = json.loads((OUT / "test_nodomainprior_category_summary.json").read_text(encoding="utf-8"))
NDGG = json.loads((OUT / "test_nodomainprior_global_summary.json").read_text(encoding="utf-8"))
nd_prior = json.loads((OUT / "priors_test_full_nodomain_summary.json").read_text(encoding="utf-8"))
lines.append("\n### Exploratory category-free full-library prior\n")
lines.append("Prior prompt removes DOMAIN; candidate model either category-filtered or all 102. This is separate from the main category-conditioned experiment.\n")
lines.append(f"Category-free prior: n={nd_prior['n_ok']}, top-1={nd_prior['top1_global']:.3f}, top-10={nd_prior['top10_global_recall']:.3f}, estimated cost=${nd_prior['estimated_cost_usd']:.4f}.\n")
lines.append("| experiment | rule | stable correct | slip error | slip none | slip abstain |")
lines.append("|---|---|---:|---:|---:|---:|")
for source, name, keys in (
    (NDG, "domain-free prior, category candidates", ("one_shot_typed", "maxent_k3", "stability_mixed_maxent")),
    (NDGG, "domain-free prior, all 102 candidates", ("one_shot_typed", "maxent_k3", "stability_maxent")),
):
    for key in keys:
        a = source["aggregates"][f"{key}/stable"]
        b = source["aggregates"][f"{key}/slip"]
        lines.append(f"| {name} | {key} | {a['stable_correct_diagnosed']:.3f} | {b['slip_error_rate']:.3f} | {b['slip_explicit_none_rate']:.3f} | {b['slip_abstain_rate']:.3f} |")
lines.append("\n### Full-library prior: category-filtered candidates vs global candidates\n")
lines.append("| experiment | rule | stable correct | slip error | slip none | slip abstain |")
lines.append("|---|---|---:|---:|---:|---:|")
for source, name, keys in (
    (G, "full prior, category candidates", ("one_shot_typed", "fixed3", "stability_mixed_maxent")),
    (GG, "full prior, all 102 candidates", ("one_shot_typed", "fixed3", "stability_maxent")),
):
    for key in keys:
        a = source["aggregates"][f"{key}/stable"]
        b = source["aggregates"][f"{key}/slip"]
        lines.append(f"| {name} | {key} | {a['stable_correct_diagnosed']:.3f} | {b['slip_error_rate']:.3f} | {b['slip_explicit_none_rate']:.3f} | {b['slip_abstain_rate']:.3f} |")

# noise sensitivity
N = {}
for eps in ("0.0", "0.05", "0.10"):
    name = "test_category_eps05_corrected_summary.json" if eps == "0.05" else f"test_category_eps{eps}_corrected_summary.json"
    N[eps] = json.loads((OUT / name).read_text(encoding="utf-8"))
lines.append("\n### Noise sensitivity\n")
lines.append("| eps | method | stable correct | slip error | slip none | slip abstain | mixed error |")
lines.append("|---:|---|---:|---:|---:|---:|---:|")
for eps, summary in N.items():
    for key in ("one_shot_typed", "fixed3", "stability_mixed_maxent", "stability_mixed_heldout_maxent"):
        sa = summary["aggregates"][f"{key}/stable"]
        sl = summary["aggregates"][f"{key}/slip"]
        mx = summary["aggregates"].get(f"{key}/mixed", {})
        lines.append("| {} | {} | {:.3f} | {:.3f} | {:.3f} | {:.3f} | {} |".format(
            eps, key, sa["stable_correct_diagnosed"], sl["slip_error_rate"],
            sl["slip_explicit_none_rate"], sl["slip_abstain_rate"],
            f"{mx['mixed_error_rate']:.3f}" if mx else "—"))

# categories
lines.append("\n### Category results for stability_mixed/maxent\n")
lines.append("| category | n stable | stable correct | slip error | mixed error |")
lines.append("|---|---:|---:|---:|---:|")
cats = S["per_category"]["stability_mixed_maxent/stable"]
for cat, v in sorted(cats.items()):
    slip = S["per_category"]["stability_mixed_maxent/slip"].get(cat, {})
    mixed = S["per_category"]["stability_mixed_maxent/mixed"].get(cat, {})
    lines.append(f"| {cat} | {v['n']} | {v['stable_correct_diagnosed']:.3f} | {slip.get('slip_error_rate', float('nan')):.3f} | {mixed.get('mixed_error_rate', float('nan')):.3f} |")

# per true label
E_for_labels = json.loads((OUT / "test_category_eps05_corrected_episodes.json").read_text(encoding="utf-8"))
case_map = {c["case_id"]: c for c in json.loads((HERE / "data" / "cases_test_v5_exclusion_corrected.json").read_text(encoding="utf-8"))}
def per_label(rule, st):
    vals = {}
    for e in E_for_labels:
        if e["rule"] != rule or e["student_type"] != st or e["selection"] != "maxent":
            continue
        hid = e["true_id"] or case_map[e["case_id"]]["true_id"]
        vals.setdefault(hid, []).append(e)
    return {hid: rows for hid, rows in sorted(vals.items())}
lines.append("\n### Per misconception: stability_mixed/maxent\n")
lines.append("| misconception | stable correct / n | slip remediation error / n | mixed detected / n | mixed error / n |")
lines.append("|---|---:|---:|---:|---:|")
stable_labels = per_label("stability_mixed", "stable")
slip_labels = per_label("stability_mixed", "slip")
mixed_labels = per_label("stability_mixed", "mixed")
for hid in sorted(set(stable_labels) | set(slip_labels) | set(mixed_labels)):
    def rate(rows, field, inverse=False):
        if not rows: return "—"
        if field == "correct":
            v = sum(bool(r["correct"]) for r in rows)
        elif field == "false":
            v = sum(bool(r["false_remediation"]) for r in rows)
        elif field == "mixed_detected":
            v = sum(bool(r["terminal_kind"] == "mixed" or (r["terminal_kind"] == "pair" and r["correct"])) for r in rows)
        return f"{v / len(rows):.3f} / {len(rows)}"
    lines.append("| {} | {} | {} | {} | {} |".format(
        hid, rate(stable_labels.get(hid, []), "correct"),
        rate(slip_labels.get(hid, []), "false"),
        rate(mixed_labels.get(hid, []), "mixed_detected"),
        rate(mixed_labels.get(hid, []), "false"),
    ))

# failures
E = json.loads((OUT / "test_category_eps05_corrected_episodes.json").read_text(encoding="utf-8"))
CASES = {c["case_id"]: c for c in json.loads((HERE / "data" / "cases_test_v5_exclusion_corrected.json").read_text(encoding="utf-8"))}
def examples(rule, st, kind=None, wrong=False, limit=6):
    seen = set()
    out = []
    for e in E:
        if e["rule"] != rule or e["student_type"] != st or e["selection"] != "maxent":
            continue
        if kind and e["terminal_kind"] != kind:
            continue
        if wrong and e["correct"]:
            continue
        # mixed/slip episodes intentionally omit true_id for some rows
        if e["case_id"] in seen:
            continue
        seen.add(e["case_id"])
        c = CASES[e["case_id"]]
        out.append(
            f"{e['case_id']} · {e['category']} · true={e['true_id'] or c['true_id']} · answer={c['answer']} · "
            f"terminal={e['terminal_kind']}:{e['terminal_id'] or '—'} · n_obs={e['n_obs']} · seed={e['seed']}"
        )
        if len(out) >= limit:
            break
    return out

lines.append("\n### Failure examples (deduplicated by case across all seeds)\n")
lines.append("Stable wrong single: " + "; ".join(examples("stability_mixed", "stable", "single", wrong=True)) + "\n")
lines.append("Stable explicit none: " + "; ".join(examples("stability_mixed", "stable", "none")) + "\n")
lines.append("Stable abstain: " + "; ".join(examples("stability_mixed", "stable", "abstain")) + "\n")
lines.append("Slip remediation error: " + "; ".join(examples("stability_mixed", "slip", "single")) + "\n")
lines.append("Mixed single commit: " + "; ".join(examples("stability_mixed", "mixed", "single")) + "\n")
lines.append("Mixed false none: " + "; ".join(examples("stability_mixed", "mixed", "none")) + "\n")

# v4 repair table
R = json.loads((OUT / "v4_repair_category_eps05_summary.json").read_text(encoding="utf-8"))
lines.append("\n### v4 repair-impact rerun\n")
lines.append("| method | stable correct | slip error | mixed error |")
lines.append("|---|---:|---:|---:|")
for key in ("one_shot_forced", "one_shot_typed", "maxent_k3", "stability_mixed_maxent", "stability_mixed_heldout_maxent"):
    a = R["aggregates"][f"{key}/stable"]; b = R["aggregates"][f"{key}/slip"]; c = R["aggregates"][f"{key}/mixed"]
    lines.append(f"| {key} | {a['stable_correct_diagnosed']:.3f} | {b['slip_error_rate']:.3f} | {c['mixed_error_rate']:.3f} |")

lines.append("\n| repair contrast | estimate [CI] |")
lines.append("|---|---:|")
for name, st, metric in [
    ("one_shot_typed_minus_one_shot_forced", "slip", "false"),
    ("stability_mixed_targeted_minus_stability_mixed_maxent", "stable", "correct"),
    ("stability_mixed_targeted_minus_stability_mixed_maxent", "slip", "false"),
]:
    lines.append(f"| {name} · {st} | {diff_ci(R['contrasts'][f'{name}/{st}'][metric])} |")

table_path = OUT / "v5_result_tables.md"
table_path.write_text("\n".join(lines), encoding="utf-8")
print(table_path)
