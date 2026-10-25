"""Six-row OOL table: false commitments, explicit none, abstention and burden."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import style
from style import C
from audit_panel_alignment import require_matplotlib_panel_alignment

mpl.rcParams.update({'font.family': 'sans-serif',
                     'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans', 'Liberation Sans'],
                     'svg.fonttype': 'none', 'pdf.fonttype': 42})

data = pd.read_csv(style.data_col('ool_false_commit.csv'))
labels = {'posterior_only': 'Posterior gate', 'posterior_plus_E': 'Posterior gate + E',
          'stability_mixed_reference': 'SM'}
students = {'stable_ool': 'Deterministic rule', 'slip_ool': 'Noisy rule'}
cells = []
for _, row in data.iterrows():
    cells.append([students[row['student_type']], labels[row['arm']],
                  f"{row['false_commit_mean']:.1f} [{row['false_commit_ci_low']:.1f}, {row['false_commit_ci_high']:.1f}]",
                  f"{row['none']:.1f}", f"{row['abstain']:.1f}", f"{row['n_inquiries']:.2f}"])
out = Path(__file__).resolve().parents[2] / 'tables'
data.to_csv(out / 'table3_out_of_library.csv', index=False)
fig, ax = plt.subplots(figsize=(7.2, 2.45))
ax.axis('off')
headers = ['Student condition', 'Method', 'False commitment (%)\n[95% CI]',
           'None (%)', 'Abstain (%)', 'Additional\ninquiries']
table = ax.table(cellText=cells, colLabels=headers, cellLoc='center', bbox=[.01,.04,.98,.83])
table.auto_set_font_size(False)
table.set_fontsize(6.3)
widths = [.19,.22,.27,.095,.095,.13]
for (r,c), cell in table.get_celld().items():
    cell.set_edgecolor('none')
    cell.set_linewidth(0)
    cell.set_width(widths[c])
    if r == 0:
        cell.set_text_props(fontweight='bold')
top, bottom = .87, .04
for yy, lw in [(top, .9), (top-(top-bottom)/7, .8), (bottom,.9)]:
    ax.plot([.01,.99], [yy,yy], transform=ax.transAxes, color=C['neutral'], linewidth=lw)
ax.set_title('Table 4 | Commitments and exits with the true rule omitted', fontsize=7.5, pad=7)
base = str(out / 'table3_out_of_library')
require_matplotlib_panel_alignment(fig, json_out=style.artifact_path(base, '.alignment.json'),
                                  overlay_svg=style.artifact_path(base, '.alignment.svg'), strict=True)
fig.savefig(style.artifact_path(base, '.pdf'), bbox_inches='tight')
fig.savefig(style.artifact_path(base, '.svg'), bbox_inches='tight')
fig.savefig(style.artifact_path(base, '.png'), dpi=600, bbox_inches='tight')
fig.savefig(style.artifact_path(base, '.tiff'), dpi=600, bbox_inches='tight')
plt.close(fig)
print(base)
