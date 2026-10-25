"""Local threshold envelope and E trade-off; no threshold is selected.

Panel a: full min/max point-estimate changes over each prespecified OFAT grid.
Panel b: final correct rate vs false remediation for E=1,2,3, with 95% CIs.
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

ranges = pd.read_csv(style.data_col('e6_threshold_ranges.csv')).set_index('factor')
sweep = pd.read_csv(style.data_col('e6_threshold_sweep.csv'))
factors = ['u1', 'margin', 'S', 'P', 'N', 'E', 'LR', 'pair_guard']
fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.25))
fig.subplots_adjust(left=.12, right=.98, top=.88, bottom=.24, wspace=.33)
y = np.arange(len(factors))
for metric, offset, color, marker, label in [('slip_false', -.13, C['signal_bad'], 'o', 'Slip false remediation'),
                                          ('stable_correct', .13, C['ours'], 's', 'Stable diagnosis accuracy')]:
    lo = ranges.loc[factors, metric + '_delta_min'].to_numpy(float)
    hi = ranges.loc[factors, metric + '_delta_max'].to_numpy(float)
    axes[0].hlines(y + offset, lo, hi, color=color, linewidth=1.6)
    axes[0].scatter(lo, y + offset, s=12, marker=marker, color=color, label=label, zorder=3)
    axes[0].scatter(hi, y + offset, s=12, marker=marker, color=color, zorder=3)
axes[0].axvline(0, color=C['neutral_lt'], linestyle='--', linewidth=.7, zorder=0)
axes[0].set_yticks(y, [r'$u_1$', 'Margin', r'$S$', r'$P$', r'$N$', r'$E$', 'LR', 'Pair guard'], fontsize=6.7)
axes[0].set_ylim(7.55, -.65)
axes[0].set_xlim(-7.6, 14)
axes[0].set_xticks([-6, 0, 6, 12])
axes[0].set_xlabel('Change from pre-set default (pp)')
axes[0].legend(loc='upper right', fontsize=6.1, handlelength=1.0, labelspacing=.5)

es = sweep[sweep['factor'] == 'E'].sort_values('value', key=lambda v: v.astype(float))
for (_, r), color, marker in zip(es.iterrows(), [C['signal_bad'], C['ours'], C['safety']], ['^', 'o', 's']):
    x, v = r['stable_correct_mean'], r['slip_false_mean']
    axes[1].errorbar(x, v, xerr=[[x-r['stable_correct_ci_low']], [r['stable_correct_ci_high']-x]],
                     yerr=[[v-r['slip_false_ci_low']], [r['slip_false_ci_high']-v]],
                     fmt=marker, color=color, markersize=4.8, elinewidth=.8, capsize=2,
                     label=f"E={int(r['value'])}{' (pre-set)' if int(r['value']) == 2 else ''}; {r['stable_n_inquiries_mean']:.2f} inquiries")
axes[1].set_xlim(79, 100)
axes[1].set_ylim(0, 35)
axes[1].set_xlabel('Stable final diagnosis accuracy (%)')
axes[1].set_ylabel('Slip false remediation rate (%)')
axes[1].set_xticks([80, 85, 90, 95, 100])
fig.legend(*axes[1].get_legend_handles_labels(), loc='lower center',
           bbox_to_anchor=(.51, .012), ncol=3, frameon=False,
           fontsize=6.2, columnspacing=1.1, handlelength=1)
for i, ax in enumerate(axes):
    panel_label(ax, 'ab'[i], x=0, y=1.06)
    ax.tick_params(axis='both', labelsize=6.5)
# Keep the mathematical subscript above the 5 pt glyph floor.
axes[0].get_yticklabels()[0].set_fontsize(7.4)
base = style.out_base('fig_e6_threshold_sensitivity')
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
