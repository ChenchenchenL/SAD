#!/usr/bin/env python
"""Fig. 3  Feedback paired differences (pipeline minus baseline).

Answers: relative to fair typed one-shot, no-diagnosis and oracle, how much does
pipeline feedback improve target-hit / overall (and change misleading), and does
the direction hold across judge scopes?

Three judge scopes are separated: DeepSeek full (116 episodes), GLM subset
(60 episodes, 31 families), and the common 60-episode subset (DeepSeek).
Estimates are paired differences with 95% family-cluster bootstrap CIs.
Open markers mark CIs that cross zero (not a robust, claimable difference).
Run:  python fig3_feedback_forest.py
"""
from __future__ import annotations

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator

import matplotlib as mpl
import style
from style import C, SCOPE_STYLE, panel_label

# mandatory editable-text + publication font settings
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "font.size": 7.5,
    "axes.labelsize": 7.5,
    "xtick.labelsize": 7.5,
    "ytick.labelsize": 7.5,
})

df = pd.read_csv(style.data_col("feedback_paired.csv"))

COMPS = [("one_shot", "One-shot\ndiagnosis"),
         ("no_diagnosis", "No diagnosis"),
         ("oracle", "Oracle")]
SCOPES = ["deepseek_full", "glm_subset", "common_deepseek"]
OFF = {"deepseek_full": 0.24, "glm_subset": 0.0, "common_deepseek": -0.24}
SCALE = {"true_target_hit": 100.0, "overall": 1.0, "misleading": 100.0}
PANELS = [("true_target_hit", "Target-hit rate\ndifference (pp)"),
          ("overall", "Overall-rating\ndifference (1–5 scale)"),
          ("misleading", "Misleading-feedback\nrate difference (pp)")]
SCOPE_LABELS = {
    "deepseek_full": "DeepSeek: full evaluation (116 scenarios)",
    "glm_subset": "GLM: common subset (60 scenarios)",
    "common_deepseek": "DeepSeek: common subset (60 scenarios)",
}

fig, axes = plt.subplots(1, 3, figsize=(131 / 25.4, 106 / 25.4), sharey=True)
fig.subplots_adjust(top=.91, bottom=.40, left=.22, right=.985, wspace=.30)

for i, (metric, xlabel) in enumerate(PANELS):
    ax = axes[i]
    sub = df[df.metric == metric]
    ax.axvline(0, color="#767676", linestyle=(0, (4, 2)), linewidth=0.9, zorder=1)
    for r, (comp, _) in enumerate(COMPS):
        ybase = len(COMPS) - 1 - r
        for scope in SCOPES:
            row = sub[(sub.scope == scope) & (sub.comparison == comp)]
            if row.empty:
                continue
            m = float(row["mean"].iloc[0]) * SCALE[metric]
            lo = float(row["ci_low"].iloc[0]) * SCALE[metric]
            hi = float(row["ci_high"].iloc[0]) * SCALE[metric]
            _, color, marker = SCOPE_STYLE[scope]
            y = ybase + OFF[scope]
            ax.plot([lo, hi], [y, y], color=color, lw=1.1, solid_capstyle="butt", zorder=3)
            crosses = lo < 0 < hi
            ax.plot(m, y, marker=marker, ms=4.2, zorder=4,
                    markerfacecolor="white" if crosses else color,
                    markeredgecolor=color, markeredgewidth=0.9)
    ax.set_xlabel(xlabel)
    ax.set_yticks(range(len(COMPS)))
    ax.set_yticklabels([lab for _, lab in COMPS][::-1], fontsize=7.5)
    ax.set_ylim(-0.6, len(COMPS) - 1 + 0.6)
    ax.margins(x=0.10)
    ax.xaxis.set_major_locator(MaxNLocator(nbins=3))
    panel_label(ax, "abc"[i], x=0, y=1.05, fontsize=8)

handles = [Line2D([], [], color=c, marker=m, markersize=4.2, lw=1.1, label=SCOPE_LABELS[k],
                  markerfacecolor="white", markeredgecolor=c)
           for k, (lab, c, m) in SCOPE_STYLE.items() if k in SCOPES]
handles.append(Line2D([], [], color="#767676", marker="o", markersize=4.2, lw=0,
                      markerfacecolor="white", markeredgecolor="#767676",
                      label="Open marker: 95% CI includes zero"))
fig.legend(handles=handles, loc="lower center", ncol=1, frameon=False,
           bbox_to_anchor=(.53, .015), fontsize=7.5, handletextpad=.7,
           labelspacing=.65)

from audit_panel_alignment import require_matplotlib_panel_alignment

base = style.out_base("fig3_feedback_forest")
require_matplotlib_panel_alignment(
    fig, json_out=style.artifact_path(base, ".alignment.json"), overlay_svg=style.artifact_path(base, ".alignment.svg"),
    tolerance_pt=1.5, gutter_tolerance_pt=1.5, require_panel_labels=True, strict=True)
fig.savefig(style.artifact_path(base, ".svg"))
fig.savefig(style.artifact_path(base, ".pdf"))
fig.savefig(style.artifact_path(base, ".tiff"), dpi=600)
fig.savefig(style.artifact_path(base, ".png"), dpi=600)
plt.close(fig)
print("saved", base)
