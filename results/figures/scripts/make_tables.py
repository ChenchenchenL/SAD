#!/usr/bin/env python
"""Table 1  Diagnosis main table (protocol-valid 87 cases).

Answers: on the same 87-case / 435-episode-per-type denominators, how do the
methods compare on stable correct-stop, stable correct, slip false remediation,
abstention and additional inquiries?  All methods are listed; no best-of-each
metric is spliced together.
Run:  python make_tables.py
"""
from __future__ import annotations

import os
import json
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

import matplotlib as mpl
import style
from style import C

# mandatory editable-text + publication font settings
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
})

TAB_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tables"))
os.makedirs(TAB_DIR, exist_ok=True)

df = pd.read_csv(style.data_col("diagnosis_main.csv")).set_index("rule_id")
audit_path = Path(__file__).resolve().parents[3] / "experiments/2026-10-20_llm_v4_v5/v5/out/final_audit/diagnosis_audit.json"
diagnosis_audit = json.loads(audit_path.read_text(encoding="utf-8"))

ROWS = [
    ("one_shot_typed", "Fair typed one-shot"),
    ("fixed_k3", "Fixed-order k=3"),
    ("maxent_k3", "Fixed-3 (MaxEnt)"),
    ("stability_maxent", "Stability (MaxEnt)"),
    ("stability_mixed_maxent", "SM (MaxEnt)"),
    ("stability_mixed_heldout_maxent", "Held-out safety"),
]


def pct_ci(rec, mean, lo, hi):
    return f"{rec[mean]*100:.1f} [{rec[lo]*100:.1f}, {rec[hi]*100:.1f}]"


records = []
for rid, disp in ROWS:
    r = df.loc[rid]
    records.append({
        "Method": disp,
        "Adaptive correct-stop (%)": (
            "—" if rid in {"one_shot_forced", "one_shot_typed", "random_k3", "fixed_k3", "maxent_k3"}
            else pct_ci(r, "stable_correct_stop_mean", "stable_correct_stop_ci_low", "stable_correct_stop_ci_high")
        ),
        "Stable correct (%)": pct_ci(r, "stable_correct_mean", "stable_correct_ci_low", "stable_correct_ci_high"),
        "Slip false remediation (%)": pct_ci(r, "slip_false_mean", "slip_false_ci_low", "slip_false_ci_high"),
        "Stable no-stable-evidence (%)": f"{diagnosis_audit['table'][rid]['stable']['none']['mean']*100:.1f}",
        "Slip no-stable-evidence (%)": f"{diagnosis_audit['table'][rid]['slip']['none']['mean']*100:.1f}",
        "Stable abstain (%)": f"{r['stable_abstain_mean']*100:.1f}",
        "Slip abstain (%)": f"{r['slip_abstain_mean']*100:.1f}",
        "Stable inquiries": f"{r['stable_inquiries_mean']:.2f}",
        "Slip inquiries": f"{r['slip_inquiries_mean']:.2f}",
    })

tbl = pd.DataFrame(records)
gate_summary_path = Path(__file__).resolve().parents[3] / 'experiments/2026-10-21_stability_ablation/runs/20261021T065513Z_ablation_ext/outputs/summary.json'
gate_aggregates = json.loads(gate_summary_path.read_text(encoding='utf-8'))['aggregates']
for arm, label in [('posterior_plus_E_LR_pairguard_extra_none', 'Simplified SM'), ('posterior_plus_E', 'E-only')]:
    s, p = gate_aggregates[arm]['stable'], gate_aggregates[arm]['slip']
    def frozen_pct(v):
        return f"{100*v['mean']:.1f} [{100*v['ci_low']:.1f}, {100*v['ci_high']:.1f}]"
    records.append({'Method':label, 'Adaptive correct-stop (%)':frozen_pct(s['correct_stop']),
                    'Stable correct (%)':frozen_pct(s['correct']), 'Slip false remediation (%)':frozen_pct(p['false']),
                    'Stable no-stable-evidence (%)':f"{100*s['none']['mean']:.1f}",
                    'Slip no-stable-evidence (%)':f"{100*p['none']['mean']:.1f}",
                    'Stable abstain (%)':f"{100*s['abstain']['mean']:.1f}",
                    'Slip abstain (%)':f"{100*p['abstain']['mean']:.1f}",
                    'Stable inquiries':f"{s['n_inquiries']['mean']:.2f}", 'Slip inquiries':f"{p['n_inquiries']['mean']:.2f}"})
tbl = pd.DataFrame(records)
method_order = ['Fair typed one-shot','Fixed-order k=3','Fixed-3 (MaxEnt)','Stability (MaxEnt)','SM (MaxEnt)','Simplified SM','E-only','Held-out safety']
tbl = tbl.set_index('Method').loc[method_order].reset_index()
GROUPED_COLUMNS = [
    'Method', 'Adaptive correct-stop (%)', 'Stable correct (%)',
    'Stable no-stable-evidence (%)', 'Stable abstain (%)', 'Stable inquiries',
    'Slip false remediation (%)', 'Slip no-stable-evidence (%)',
    'Slip abstain (%)', 'Slip inquiries',
]
tbl = tbl[GROUPED_COLUMNS]
csv_path = os.path.join(TAB_DIR, "table1_diagnosis_main.csv")
tbl.to_csv(csv_path, index=False, encoding="utf-8")
print("wrote", csv_path)

md = ["# Table 1 | Diagnosis performance and cost (protocol-valid 87 cases)", ""]
md.append("Student types analysed separately; each type has 87 cases x 5 simulation seeds = 435 episodes. "
          "Means with 95% template-family cluster bootstrap CIs (36 families, 2000 resamples). "
          "Inquiries = observations minus the initial item. Fixed-3 (MaxEnt) adds three questions "
          "after the initial item, for four observations in total. Adaptive correct-stop is not "
          "applicable to one-shot or fixed-budget methods (—). SM denotes Stability-Mixed. "
          "No-stable-evidence denotes the explicit none terminal state within the rule library, "
          "separate from abstention. Random k=3 is retained only in the historical figure, "
          "not as a standard random comparator in this table. "
          "SM minus Fixed-3 paired differences: slip false remediation −37.9 pp "
          "[95% CI −49.7, −26.1]; stable correct −1.4 pp [−3.0, +0.2]. "
          "Before the identifiability exclusion, SM on all 90 cases had stable correct "
          "92.4% [85.2, 97.2] and slip false remediation 10.0% [7.1, 12.9]; "
          "the 87-case results are 95.6% [93.5, 97.7] and 9.9% [6.9, 12.9]. "
          "Original Fixed-3 has no pair hypotheses (pair prior mass 0; single mass .95); "
          "E1 arm A retains pairs (pair mass .10; single mass .85). Their individual "
          "decisions differ but aggregate correct/error counts coincide. Default SM CIs "
          "are harmonized across displays using 2000 family draws with seed 20261026.")
md.append('Simplified SM and E-only retain the same pair hypothesis space as full SM. Simplified SM disables pair/mixed terminals; E-only uses posterior + E and the basic none rule. They are not the no-pair Stability baseline. All table intervals retain the frozen 2,000-draw analyses.')
md.append("")
md.append("| " + " | ".join(tbl.columns) + " |")
md.append("|" + "---|" * len(tbl.columns))
for _, row in tbl.iterrows():
    md.append("| " + " | ".join(str(x) for x in row.values) + " |")
md_path = os.path.join(TAB_DIR, "table1_diagnosis_main.md")
with open(md_path, "w", encoding="utf-8") as fh:
    fh.write("\n".join(md) + "\n")
print("wrote", md_path)

# Grouped two-level header: stable outcomes first, then slip outcomes.
fig, ax = plt.subplots(figsize=(7.2, 3.2))
ax.axis("off")
ncol = len(tbl.columns)
col_labels = ["Method", "Adaptive\ncorrect-stop (%)", "Diagnosis\naccuracy (%)",
              "None\n(%)", "Abstain\n(%)", "Inquiries",
              "False\nremediation (%)", "None\n(%)", "Abstain\n(%)", "Inquiries"]
table = ax.table(cellText=tbl.values.tolist(), colLabels=col_labels,
                 bbox=[0.01, 0.04, 0.98, 0.77], cellLoc="center")
table.auto_set_font_size(False)
table.set_fontsize(6.0)
main_row = [d for _, d in ROWS].index("SM (MaxEnt)")
nrow = len(tbl) + 1
widths = [0.19, 0.135, 0.135, 0.07, 0.07, 0.07, 0.135, 0.065, 0.065, 0.065]
cells = table.get_celld()
for (r, c), cell in cells.items():
    cell.set_edgecolor("none")
    cell.set_linewidth(0)
    cell.set_facecolor("none")
    cell.set_width(widths[c])
    if r == 0:
        cell.set_text_props(fontweight="bold")

# Horizontal rules distinguish the two student groups without a cell grid.
bx, by, bw, bh = 0.01, 0.04, 0.98, 0.77
rh = bh / nrow
for yy, lw in ((0.94, 1.0), (by + bh - rh, 0.8), (by, 0.9)):
    ax.plot([bx, bx + bw], [yy, yy], transform=ax.transAxes, color="#4D4D4D",
            linewidth=lw, solid_capstyle="butt")
stable_left = bx + bw * widths[0]
stable_right = bx + bw * sum(widths[:6])
slip_right = bx + bw
for left, right, label in [(stable_left, stable_right, 'Stable-misconception students'),
                            (stable_right, slip_right, 'One-off-slip students')]:
    ax.text((left+right)/2, 0.885, label, transform=ax.transAxes,
            ha='center', va='center', fontsize=6.7, fontweight='bold')
    ax.plot([left+.004, right-.004], [.835, .835], transform=ax.transAxes,
            color=C['neutral'], linewidth=.65, solid_capstyle='butt')

ax.set_title("Table 1 | Diagnosis performance and cost (protocol-valid 87 cases)",
             fontsize=7.0, pad=8)

from audit_panel_alignment import require_matplotlib_panel_alignment

base = style.out_base(os.path.join("..", "tables", "table1_diagnosis_main"))
require_matplotlib_panel_alignment(
    fig, json_out=style.artifact_path(base, ".alignment.json"), overlay_svg=style.artifact_path(base, ".alignment.svg"))
fig.savefig(style.artifact_path(base, ".svg"), bbox_inches="tight")
fig.savefig(style.artifact_path(base, ".pdf"), bbox_inches="tight")
fig.savefig(style.artifact_path(base, ".tiff"), dpi=600, bbox_inches="tight")
fig.savefig(style.artifact_path(base, ".png"), dpi=600, bbox_inches="tight")
plt.close(fig)
print("done.")
