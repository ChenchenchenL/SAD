from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import numpy as np
import pandas as pd
from PIL import Image

import style
from style import C
from audit_panel_alignment import require_matplotlib_panel_alignment

mpl.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
                     "svg.fonttype": "none", "pdf.fonttype": 42, "font.size": 7,
                     "legend.fontsize": 6.3, "axes.labelsize": 7, "xtick.labelsize": 6.3,
                     "ytick.labelsize": 6.3})

FIGURES = Path(__file__).resolve().parents[1]
METHODS = ["maxent", "ig", "random", "fixed"]
METHOD_NAMES = ["MaxEnt", "IG", "Random", "Fixed order"]
METHOD_COLORS = [C["ours"], C["fair_base"], C["safety"], C["budget_dk"]]
METHOD_MARKERS = ["o", "s", "^", "D"]
NOISE_ARMS = ["fixed_k3", "fixed_k3_gate", "sm_b6", "e_b6"]
NOISE_NAMES = ["Fixed-3, direct", "Fixed-3, gated", "Full SM", "E-only"]
NOISE_COLORS = [C["budget_dk"], C["safety"], C["ours"], C["fair_base"]]
NOISE_MARKERS = ["D", "^", "o", "s"]
STATES = ["false", "none", "abstain"]
STATE_NAMES = ["False remediation", "Explicit none", "Abstention"]
STATE_COLORS = [C["signal_bad"], C["fair_base"], "#D6D6D6"]


def select(df, **filters):
    out = df
    for k, v in filters.items():
        out = out[out[k] == v]
    assert len(out) == 1, (filters, len(out))
    return out.iloc[0]


def errors(row, factor=1):
    return np.array([[row["mean"] - row["ci_low"]], [row["ci_high"] - row["mean"]]]) * factor


def setup(width_mm=183):
    fig, axes = plt.subplots(1, 3, figsize=(width_mm / 25.4, 86 / 25.4))
    fig.subplots_adjust(left=.095, right=.985, top=.76, bottom=.27, wspace=.58)
    for ax, label in zip(axes, "abc"):
        ax.annotate(label, xy=(0, 1), xycoords="axes fraction", xytext=(-15, 13),
                    textcoords="offset points", fontsize=8, fontweight="bold", va="bottom")
    return fig, axes


def legends(fig, names, colors, markers):
    handles = [Line2D([], [], color=c, marker=m, markersize=4, linewidth=.9, label=n)
               for n, c, m in zip(names, colors, markers)]
    fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(.52, .985),
               ncol=4, columnspacing=1.5, handlelength=1.2)
    handles = [Patch(facecolor=c, edgecolor="none", label=n) for n, c in zip(STATE_NAMES, STATE_COLORS)]
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(.52, .01),
               ncol=3, columnspacing=1.5, handlelength=1)


def stack(ax, rows, labels):
    y = np.arange(len(rows))
    left = np.zeros(len(rows))
    for state, color in zip(STATES, STATE_COLORS):
        vals = np.array([r[state] for r in rows]) * 100
        ax.barh(y, vals, left=left, height=.57, color=color, linewidth=.4, edgecolor="white")
        for yy, l, v in zip(y, left, vals):
            if v >= 14:
                ax.text(l + v / 2, yy, f"{v:.1f}", ha="center", va="center", fontsize=6.2,
                        color="white" if state == "false" else "#202020")
        left += vals
    assert np.allclose(left, 100)
    ax.set_yticks(y, labels)
    ax.set_xlim(0, 100)
    ax.set_xticks([0, 50, 100])
    ax.set_ylim(len(rows) - .45, -.6)
    ax.set_xlabel("Slip terminal\ncomposition (%)")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)


def save(fig, name):
    base = FIGURES / name
    require_matplotlib_panel_alignment(fig, json_out=FIGURES / "qa" / f"{name}.alignment.json",
                                      overlay_svg=FIGURES / "qa" / f"{name}.alignment.svg",
                                      tolerance_pt=1.5, gutter_tolerance_pt=1.5,
                                      require_panel_labels=True, strict=True)
    for suffix in (".png", ".pdf", ".svg", ".tiff"):
        fig.savefig(style.artifact_path(base, suffix), dpi=600, facecolor="white")
    screen_resolution = 96
    with Image.open(style.artifact_path(base, ".png")) as image:
        dimensions = tuple(round(v * screen_resolution / 600) for v in image.size)
        image.resize(dimensions, Image.Resampling.LANCZOS).save(
            FIGURES / "qa" / f"{name}.final_size_96dpi.png", dpi=(screen_resolution, screen_resolution))
    plt.close(fig)
    print(name)


def selection():
    df = pd.read_csv(FIGURES / "data/selection_comparison_means.csv")
    df = df[df["epsilon"] == .05]
    # Match the manuscript scale closely enough to retain >=5 pt figure text.
    fig, axes = setup(width_mm=160)
    for method, color, marker in zip(METHODS, METHOD_COLORS, METHOD_MARKERS):
        x = select(df, block="fixed3", arm=method, student_type="slip", metric="false")
        y = select(df, block="fixed3", arm=method, student_type="stable", metric="correct")
        axes[0].errorbar(x["mean"] * 100, y["mean"] * 100, xerr=errors(x, 100), yerr=errors(y, 100),
                         fmt=marker, color=color, markersize=4.4, capsize=1.8, elinewidth=.7,
                         markerfacecolor="white" if method == "ig" else color, zorder=4 if method == "ig" else 3)
        x = select(df, block="sm", arm=method, student_type="stable", metric="n_inquiries")
        y = select(df, block="sm", arm=method, student_type="stable", metric="correct")
        axes[1].errorbar(x["mean"], y["mean"] * 100, xerr=errors(x), yerr=errors(y, 100),
                         fmt=marker, color=color, markersize=4.4, capsize=1.8, elinewidth=.7,
                         markerfacecolor="white" if method == "ig" else color, zorder=4 if method == "ig" else 3)
    axes[0].set(xlim=(25, 100), ylim=(65, 101), xlabel="Slip false remediation\nrate (%)",
                ylabel="Stable final diagnosis\naccuracy (%)")
    axes[1].set(ylim=(35, 101), xlabel="Stable mean additional\ninquiries",
                ylabel="Stable final diagnosis\naccuracy (%)")
    inquiry = df[(df["block"] == "sm") & (df["student_type"] == "stable") & (df["metric"] == "n_inquiries")]
    axes[1].set_xlim(max(0, inquiry["ci_low"].min() - .2), inquiry["ci_high"].max() + .2)
    axes[0].set_title("Fixed budget: 3 inquiries", pad=14)
    axes[1].set_title("Full SM: adaptive, cap 6", pad=14)
    axes[2].set_title("Full SM: slip outcomes", pad=14)
    rows = [{state: select(df, block="sm", arm=m, student_type="slip", metric=state)["mean"]
             for state in STATES} for m in METHODS]
    stack(axes[2], rows, ["MaxEnt", "IG", "Random", "Fixed order"])
    legends(fig, METHOD_NAMES, METHOD_COLORS, METHOD_MARKERS)
    save(fig, "fig1_selection_comparison")


def noise():
    df = pd.read_csv(FIGURES / "data/noise_misspecification_means.csv")
    rates = [.01, .05, .10, .20]
    fig, axes = setup()
    for arm, color, marker in zip(NOISE_ARMS, NOISE_COLORS, NOISE_MARKERS):
        for ax, typ, metric in ((axes[0], "slip", "false"), (axes[1], "stable", "correct")):
            rows = [select(df, arm=arm, epsilon=rate, student_type=typ, metric=metric) for rate in rates]
            means = np.array([r["mean"] for r in rows]) * 100
            errs = np.column_stack([errors(r, 100).ravel() for r in rows])
            ax.errorbar(rates, means, yerr=errs, color=color, marker=marker, markersize=3.8,
                        linewidth=1.3 if arm == "sm_b6" else .9, elinewidth=.65, capsize=1.8,
                        zorder=5 if arm == "sm_b6" else 3)
    for ax in axes[:2]:
        ax.set_xticks(rates, ["0.01", "0.05", "0.10", "0.20"])
        ax.set_xlim(0, .215)
        ax.set_xlabel("True iid noise rate")
        ax.axvline(.05, linestyle=":", color=C["neutral_lt"], linewidth=.7, zorder=0)
    axes[0].set_ylim(0, 105)
    axes[1].set_ylim(40, 102)
    axes[0].set_ylabel("Slip false remediation\nrate (%)")
    axes[1].set_ylabel("Stable final diagnosis\naccuracy (%)")
    axes[0].set_title("Risk at assumed noise = 0.05", pad=14)
    axes[1].set_title("Stable diagnosis", pad=14)
    axes[2].set_title("Full SM: slip outcomes", pad=14)
    for rate in (.10, .20):
        r = select(df, arm="sm_b6", epsilon=rate, student_type="slip", metric="false")
        axes[0].annotate(f"{100*r['mean']:.1f}%", (rate, 100*r["ci_high"]),
                         xytext=(-2 if rate == .20 else 0, 4), textcoords="offset points",
                         ha="right" if rate == .20 else "center", va="bottom", fontsize=6.3, color=C["ours"])
    rows = [{state: select(df, arm="sm_b6", epsilon=rate, student_type="slip", metric=state)["mean"]
             for state in STATES} for rate in rates]
    stack(axes[2], rows, ["0.01", "0.05", "0.10", "0.20"])
    axes[2].set_ylabel("True iid noise rate")
    legends(fig, NOISE_NAMES, NOISE_COLORS, NOISE_MARKERS)
    save(fig, "fig5_noise_misspecification")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("figure", choices=["selection", "noise", "all"], default="all", nargs="?")
    args = parser.parse_args()
    if args.figure in {"selection", "all"}:
        selection()
    if args.figure in {"noise", "all"}:
        noise()
