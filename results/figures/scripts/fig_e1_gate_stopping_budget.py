"""Four-arm component comparison: risk control, stable diagnosis, and burden.

Source: e1_four_arms.csv, extracted from the saved component experiment.
All panels use 87 cases x 5 seeds; CIs are 36-family cluster bootstrap CIs.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import style
from style import C, panel_label
from audit_panel_alignment import require_matplotlib_panel_alignment

mpl.rcParams.update({'font.family': 'sans-serif',
                     'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans', 'Liberation Sans'],
                     'svg.fonttype': 'none', 'pdf.fonttype': 42})

df = pd.read_csv(style.data_col('e1_four_arms.csv')).set_index('arm')
order = ['fixed_k3', 'fixed_k3_gate', 'sm_b3', 'sm_b6']
names = ['A: Fixed-3, direct', 'B: Fixed-3, gated', "C': Adaptive, cap 3", 'C: SM, cap 6']
colors = [C['budget'], C['safety'], C['fair_base'], C['ours']]
y = np.arange(len(order))
fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.65), sharey=True)
fig.subplots_adjust(left=.18, right=.985, top=.85, bottom=.25, wspace=.30)


def values(prefix):
    mean = df.loc[order, prefix + '_mean'].to_numpy(float)
    err = np.vstack([mean - df.loc[order, prefix + '_ci_low'].to_numpy(float),
                     df.loc[order, prefix + '_ci_high'].to_numpy(float) - mean])
    return mean, err


for ax, metric, label, xmax in [(axes[0], 'slip_false', 'Slip false\nremediation rate (%)', 70),
                                (axes[1], 'stable_correct', 'Stable final diagnosis\naccuracy (%)', 100)]:
    mean, err = values(metric)
    ax.barh(y, mean, height=.56, color=colors, edgecolor=C['neutral'], linewidth=.55,
            xerr=err, error_kw=dict(elinewidth=.8, capsize=2, capthick=.8))
    ax.set_xlim(0, xmax)
    ax.set_xlabel(label)

for prefix, offset, color, label in [('stable_n_inquiries', -.16, C['ours'], 'Stable'),
                                      ('slip_n_inquiries', .16, C['signal_bad'], 'Slip')]:
    mean, err = values(prefix)
    axes[2].barh(y + offset, mean, height=.28, color=color, edgecolor=C['neutral'], linewidth=.55,
                 label=label, xerr=err, error_kw=dict(elinewidth=.8, capsize=2, capthick=.8))
axes[2].set_xlim(0, 4.6)
axes[2].set_xlabel('Mean additional\ninquiries')
axes[2].legend(loc='upper right', bbox_to_anchor=(1.04, 1.23), fontsize=6.2,
               ncol=2, columnspacing=.7, handlelength=.8)
axes[0].set_yticks(y, names, fontsize=6.4)
axes[0].set_ylim(3.55, -.6)
for i, ax in enumerate(axes):
    panel_label(ax, 'abc'[i], x=0, y=1.08)
    ax.tick_params(axis='x', labelsize=6.4)
base = style.out_base('fig_e1_gate_stopping_budget')
require_matplotlib_panel_alignment(fig, json_out=style.artifact_path(base, '.alignment.json'),
                                  overlay_svg=style.artifact_path(base, '.alignment.svg'),
                                  tolerance_pt=1.5, gutter_tolerance_pt=1.5,
                                  require_panel_labels=True, strict=True)
fig.savefig(style.artifact_path(base, '.svg'), bbox_inches='tight')
fig.savefig(style.artifact_path(base, '.pdf'), bbox_inches='tight')
fig.savefig(style.artifact_path(base, '.png'), dpi=600, bbox_inches='tight')
fig.savefig(style.artifact_path(base, '.tiff'), dpi=600, bbox_inches='tight')
plt.close(fig)
print(base)
