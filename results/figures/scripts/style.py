"""Shared publication style and palette for manuscript figures.

Backend: Python (matplotlib) only. Keeps text editable in SVG/PDF, white
background, low-saturation palette (in the spirit of the supplied example).
"""
from __future__ import annotations

import os
import sys
from artifact_paths import artifact_path

import matplotlib
matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.pyplot as plt

# --- mandatory editable-text + font rules --------------------------------
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"]
plt.rcParams["svg.fonttype"] = "none"   # keep <text> nodes
plt.rcParams["pdf.fonttype"] = 42       # editable TrueType text

mpl.rcParams.update({
    "font.size": 7,
    "axes.labelsize": 7,
    "axes.titlesize": 7.5,
    "xtick.labelsize": 6.5,
    "ytick.labelsize": 6.5,
    "legend.fontsize": 6.5,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
    "xtick.major.size": 2.5,
    "ytick.major.size": 2.5,
    "legend.frameon": False,
    "axes.grid": False,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
})

# --- low-saturation palette ----------------------------------------------
C = {
    "ours":       "#2E5F8A",   # proposed method (stability_mixed) — hero
    "ours_soft":  "#7FA6C9",
    "stability":  "#5B8DB8",
    "budget":     "#8C8C8C",   # fixed-budget baselines (neutral)
    "budget_dk":  "#5A5A5A",
    "random":     "#BFBFBF",   # weakest baseline, de-emphasised
    "fair_base":  "#4F9A94",   # fair typed one-shot (teal)
    "historical": "#D6D6D6",   # forced one-shot (historical / pale)
    "safety":     "#7E6BA8",   # held-out safety (violet)
    "signal_bad": "#BE5A50",   # error / drop cue (muted red)
    "signal_good":"#5E8C57",   # gain cue (muted green)
    "neutral":    "#4D4D4D",
    "neutral_lt": "#9A9A9A",
    "grid":       "#E4E4E4",
}

# method -> (display label, colour)
METHOD_STYLE = {
    "one_shot_forced":                  ("One-shot forced (historical)", C["historical"]),
    "one_shot_typed":                   ("Fair typed one-shot", C["fair_base"]),
    "random_k3":                        ("Random, k=3", C["random"]),
    "fixed_k3":                         ("Fixed order, k=3", C["budget_dk"]),
    "maxent_k3":                        ("Maxent, k=3", C["budget"]),
    "fixed3":                           ("Fixed-3 (maxent)", C["budget"]),
    "stability_maxent":                 ("Stability (maxent)", C["stability"]),
    "stability_targeted":               ("Stability (targeted)", C["stability"]),
    "stability_mixed_maxent":           ("Stability+Mixed (maxent)", C["ours"]),
    "stability_mixed_targeted":         ("Stability+Mixed (targeted)", C["ours_soft"]),
    "stability_mixed_heldout_maxent":   ("Held-out safety (maxent)", C["safety"]),
}

# scopes for the feedback forest
SCOPE_STYLE = {
    "deepseek_full":    ("DeepSeek, full (116 ep)",   C["ours"],       "o"),
    "glm_subset":       ("GLM, common subset (60 ep)",       C["fair_base"],  "s"),
    "common_deepseek":  ("DeepSeek, common subset (60 ep)", C["safety"], "D"),
}


def panel_label(ax, label, x=0.0, y=1.02, fontsize=8):
    """Bold lowercase panel label at the axes top-left with a fixed offset."""
    ax.text(x, y, label, transform=ax.transAxes,
            fontsize=fontsize, fontweight="bold", ha="left", va="bottom")


def data_col(name):
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(os.path.dirname(here), "data", name)


def out_base(name):
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(os.path.dirname(here), name)

