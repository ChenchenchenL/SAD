"""Figure 4: paired second-bank replication and descriptive slip terminals."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True

import style
from artifact_paths import artifact_path
from style import C, panel_label
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "experiments/2026-10-22_independent_templates_v6b/runs/20261022T015122Z_v6b_arms_final/outputs/summary.json"
BASE = Path(style.out_base("fig4_second_bank_replication"))
QA = BASE.parent / "qa"
PREFIX = BASE.name
DATASETS = ("v5", "v6b")
ARMS = ("full_sm", "e_only", "simplified_sm", "fixed3")
ARM_NAMES = {"full_sm": "Full SM", "e_only": "E-only", "simplified_sm": "Simplified SM", "fixed3": "Fixed-3"}
ARM_COLORS = {"full_sm": C["ours"], "e_only": C["fair_base"], "simplified_sm": C["safety"], "fixed3": C["budget"]}
COMPARISONS = (("full_sm", "fixed3"), ("e_only", "fixed3"), ("simplified_sm", "full_sm"), ("full_sm", "e_only"))
PANELS = (("slip", "false", "Slip false remediation", "Paired difference (pp)", (-76, 14), [-75, -50, -25, 0]),
          ("stable", "correct", "Stable final correct", "Paired difference (pp)", (-6.3, 4.2), [-6, -4, -2, 0, 2, 4]),
          ("slip", "n_inquiries", "Slip inquiry burden", "Paired difference (inquiries)", (-2.9, 3.3), [-2, -1, 0, 1, 2, 3]))
TERMINALS = ("false", "none", "abstain")
TERMINAL_COLORS = {"false": C["signal_bad"], "none": C["fair_base"], "abstain": C["historical"]}
COUNT_METRICS = {"n_inquiries", "J5", "J10"}


def qa_path(suffix):
    return QA / f"{PREFIX}.{suffix}"


def write_json(path, payload):
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def pointer(*keys):
    return "/" + "/".join(str(key).replace("~", "~0").replace("/", "~1") for key in keys)


def resolve_pointer(document, value):
    for key in value.split("/")[1:]:
        document = document[key.replace("~1", "/").replace("~0", "~")]
    return document


def estimate_valid(value, expected_n):
    assert set(("mean", "ci_low", "ci_high", "n_cases")).issubset(value)
    assert value["n_cases"] == expected_n
    assert all(math.isfinite(value[key]) for key in ("mean", "ci_low", "ci_high"))
    assert value["ci_low"] <= value["ci_high"]


def source_data():
    original = SOURCE.read_bytes()
    document = json.loads(original)
    assert document["experiment"] == "independent_templates_v6b"
    assert set(document["aggregates"]) == set(DATASETS)
    assert set(document["contrasts"]) == set(DATASETS)
    assert document["protocol"]["seeds"] == 5
    assert document["protocol"]["bootstrap"] == 2000
    assert document["protocol"]["bootstrap_seed"] == 20261028
    assert [(document["data"][ds]["n_cases"], document["data"][ds]["n_families"]) for ds in DATASETS] == [(87, 36), (90, 32)]
    for ds in DATASETS:
        expected_n = document["data"][ds]["n_cases"]
        assert set(document["aggregates"][ds]) == set(ARMS)
        for arm in ARMS:
            assert set(document["aggregates"][ds][arm]) == {"stable", "slip", "mixed"}
            for estimates in document["aggregates"][ds][arm].values():
                assert estimates["n_cases"] == expected_n
                assert estimates["n_episodes"] == expected_n * 5
                for metric, value in estimates.items():
                    if isinstance(value, dict):
                        estimate_valid(value, expected_n)
                        if metric not in COUNT_METRICS:
                            assert all(0 <= value[key] <= 1 for key in ("mean", "ci_low", "ci_high"))
            stack = [document["aggregates"][ds][arm]["slip"][key]["mean"] for key in TERMINALS]
            assert math.isclose(sum(stack), 1, abs_tol=1e-12)
        for comparison, estimates in document["contrasts"][ds].items():
            pair, typ = comparison.split("/")
            first, second = pair.split(" - ")
            for metric, value in estimates.items():
                estimate_valid(value, expected_n)
                marginal_difference = document["aggregates"][ds][first][typ][metric]["mean"] - document["aggregates"][ds][second][typ][metric]["mean"]
                assert math.isclose(value["mean"], marginal_difference, abs_tol=1e-12)
    return document, hashlib.sha256(original).hexdigest()


def export_source_csv(document, digest):
    common_fields = ["dataset", "type", "metric", "mean", "ci_low", "ci_high", "n_cases", "n_families", "n_seeds", "n_episodes_per_arm_type", "ci_level", "bootstrap_resamples", "bootstrap_seed", "estimator", "resampling_unit", "family_multiplicity", "display_scale", "display_unit", "mean_display", "ci_low_display", "ci_high_display", "plotted_panels", "source_path", "source_json_pointer", "source_sha256"]
    records = {"means": [], "contrasts": []}

    def record(ds, typ, metric, value, source_pointer, kind, panels):
        scale = 1 if metric in COUNT_METRICS else 100
        unit = "inquiries" if metric == "n_inquiries" else ("score" if metric in COUNT_METRICS else ("pp" if kind == "contrasts" else "%"))
        assert resolve_pointer(document, source_pointer) == value
        return dict(dataset=ds, type=typ, metric=metric, **value,
                    n_families=document["data"][ds]["n_families"], n_seeds=5,
                    n_episodes_per_arm_type=value["n_cases"] * 5, ci_level=0.95,
                    bootstrap_resamples=2000, bootstrap_seed=20261028,
                    estimator="case-level seed mean, then case mean",
                    resampling_unit="template family", family_multiplicity="preserved",
                    display_scale=scale, display_unit=unit,
                    mean_display=value["mean"] * scale, ci_low_display=value["ci_low"] * scale,
                    ci_high_display=value["ci_high"] * scale, plotted_panels=panels,
                    source_path=SOURCE.as_posix(), source_json_pointer=source_pointer, source_sha256=digest)

    for ds in DATASETS:
        for arm in ARMS:
            for typ, estimates in document["aggregates"][ds][arm].items():
                for metric, value in estimates.items():
                    if not isinstance(value, dict):
                        continue
                    row = record(ds, typ, metric, value, pointer("aggregates", ds, arm, typ, metric), "means", "d" if ds == "v6b" and typ == "slip" and metric in TERMINALS else "")
                    records["means"].append(dict(arm=arm, **row))
        for comparison, estimates in document["contrasts"][ds].items():
            pair, typ = comparison.split("/")
            first, second = pair.split(" - ")
            for metric, value in estimates.items():
                plotted = ""
                if (first, second) in COMPARISONS:
                    plotted = next(("abc"[i] for i, panel in enumerate(PANELS) if (typ, metric) == panel[:2]), "")
                row = record(ds, typ, metric, value, pointer("contrasts", ds, comparison, metric), "contrasts", plotted)
                records["contrasts"].append(dict(comparison=pair, first_arm=first, second_arm=second, **row))
    for kind, id_fields in (("means", ["arm"]), ("contrasts", ["comparison", "first_arm", "second_arm"])):
        path = BASE.parent / "data" / f"second_bank_replication_{kind}.csv"
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=["dataset", *id_fields, *common_fields[1:]])
            writer.writeheader()
            writer.writerows(records[kind])
        with path.open(encoding="utf-8", newline="") as handle:
            restored = list(csv.DictReader(handle))
        assert len(restored) == len(records[kind])
        for row in restored:
            value = resolve_pointer(document, row["source_json_pointer"])
            for field in ("mean", "ci_low", "ci_high", "n_cases"):
                assert float(row[field]) == value[field]
    return {key: len(rows) for key, rows in records.items()}


def contrast(document, ds, first, second, typ, metric):
    return document["contrasts"][ds][f"{first} - {second}/{typ}"][metric]


def panel_heading(ax, letter, title):
    panel_label(ax, letter, x=0, y=1.245, fontsize=8)
    ax.text(0.10, 1.245, title, transform=ax.transAxes, fontsize=7.5, ha="left", va="bottom")


def forest(ax, document, index):
    typ, metric, title, xlabel, limits, ticks = PANELS[index]
    scale = 1 if metric == "n_inquiries" else 100
    ax.axvline(0, color=C["neutral_lt"], lw=0.8, ls=(0, (3, 2)), zorder=0)
    for row, (first, second) in enumerate(COMPARISONS):
        for ds, offset, marker in (("v5", 0.17, "o"), ("v6b", -0.17, "s")):
            value = contrast(document, ds, first, second, typ, metric)
            mean, low, high = [value[key] * scale for key in ("mean", "ci_low", "ci_high")]
            assert limits[0] < low <= high < limits[1]
            color = ARM_COLORS[first]
            ax.errorbar(mean, 3 - row + offset, xerr=np.array([[mean - low], [high - mean]]),
                        fmt=marker, color=color, markerfacecolor="white" if ds == "v5" else color,
                        markeredgecolor=color, markeredgewidth=0.9, markersize=4.4,
                        elinewidth=1.0, capsize=2.0, capthick=0.8, zorder=3)
    ax.set(xlim=limits, ylim=(-0.65, 3.65), xlabel=xlabel)
    ax.set_xticks(ticks)
    ax.set_yticks([3, 2, 1, 0], [f"{ARM_NAMES[first]} − {ARM_NAMES[second]}" for first, second in COMPARISONS])
    ax.tick_params(axis="y", length=0, pad=5, labelsize=6.5)
    ax.tick_params(axis="x", labelsize=6.5)
    ax.spines["left"].set_visible(False)
    panel_heading(ax, "abc"[index], title)
    if index == 1:
        value = contrast(document, "v6b", "full_sm", "fixed3", "stable", "correct")
        interval = f"{value['mean'] * 100:.1f} pp (95% CI {value['ci_low'] * 100:.1f} to {value['ci_high'] * 100:.1f})".replace("-", "−")
        text = f"Bank 2 Full SM − Fixed-3\n{interval}"
        ax.text(0, 1.025, text, transform=ax.transAxes, fontsize=6.5,
                color=C["signal_bad"], ha="left", va="bottom", linespacing=1.15)
    else:
        ax.text(0, 1.045, "Negative: less false remediation" if index == 0 else "Negative: fewer inquiries",
                transform=ax.transAxes, fontsize=6.5, color=C["neutral"], ha="left", va="bottom")


def composition(ax, document):
    for row, arm in enumerate(ARMS):
        left = 0.0
        for metric in TERMINALS:
            share = document["aggregates"]["v6b"][arm]["slip"][metric]["mean"] * 100
            ax.barh(3 - row, share, left=left, height=0.50, color=TERMINAL_COLORS[metric],
                    edgecolor="white", linewidth=0.55)
            if share > 0:
                above = metric == "false"
                label_x = max(left + share / 2, 4) if above else left + share / 2
                ax.text(label_x, 3 - row + (0.42 if above else 0), f"{share:.1f}",
                        color=C["signal_bad"] if above else "#222222", fontsize=6.5,
                        ha="center", va="center")
            left += share
        assert math.isclose(left, 100, abs_tol=1e-10)
    ax.set(xlim=(0, 100), ylim=(-0.65, 3.65), xlabel="Share of slip cases (%)")
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_yticks([3, 2, 1, 0], [ARM_NAMES[arm] for arm in ARMS])
    ax.tick_params(axis="y", length=0, pad=5, labelsize=6.5)
    ax.tick_params(axis="x", labelsize=6.5)
    ax.spines["left"].set_visible(False)
    panel_heading(ax, "d", "Bank 2 slip terminal composition")
    ax.legend(handles=[Patch(facecolor=TERMINAL_COLORS[key], edgecolor="none", label=label)
                       for key, label in zip(TERMINALS, ("False", "None", "Abstain"))],
              loc="lower left", bbox_to_anchor=(0, 1.025), ncol=3, fontsize=6.5,
              handlelength=1, handletextpad=0.4, columnspacing=1.2, borderaxespad=0)


def render(document, qa_scripts):
    sys.path.insert(0, str(qa_scripts))
    from audit_panel_alignment import require_matplotlib_panel_alignment

    mpl.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"],
                         "svg.fonttype": "none", "pdf.fonttype": 42,
                         "font.size": 7, "axes.labelsize": 7,
                         "xtick.labelsize": 6.5, "ytick.labelsize": 6.5,
                         "legend.fontsize": 7.2, "savefig.bbox": None})
    font = font_manager.findfont(font_manager.FontProperties(family=["sans-serif"]))
    fig, axes = plt.subplots(2, 2, figsize=(7.204724409448819, 6.6))
    fig.subplots_adjust(left=0.185, right=0.975, bottom=0.15, top=0.80, wspace=0.80, hspace=0.75)
    for index, ax in enumerate((axes[0, 0], axes[0, 1], axes[1, 0])):
        forest(ax, document, index)
    composition(axes[1, 1], document)
    handles = [Line2D([], [], color=C["neutral"], marker=marker, markersize=5,
                      markerfacecolor=face, markeredgewidth=1, lw=1, label=label)
               for marker, face, label in (("o", "white", "Bank 1: 87 cases / 36 families"),
                                           ("s", C["neutral"], "Bank 2: 90 cases / 32 families"))]
    fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.52, 0.98), ncol=2,
               fontsize=7.2, handlelength=2.1, handletextpad=0.7, columnspacing=2.8)
    fig.canvas.draw()
    alignment = require_matplotlib_panel_alignment(
        fig, json_out=artifact_path(BASE, ".alignment.json"),
        overlay_svg=artifact_path(BASE, ".alignment.svg"),
        tolerance_pt=1.5, gutter_tolerance_pt=1.5, require_panel_labels=True, strict=True)
    fig.savefig(artifact_path(BASE, ".pdf"), dpi=600)
    fig.savefig(artifact_path(BASE, ".svg"), dpi=600)
    fig.savefig(artifact_path(BASE, ".png"), dpi=600)
    fig.savefig(artifact_path(BASE, ".tiff"), dpi=600, pil_kwargs={"compression": "tiff_lzw"})
    screen_resolution = 96
    with Image.open(artifact_path(BASE, ".png")) as image:
        screen_size = tuple(round(value * screen_resolution / 600) for value in image.size)
        image.resize(screen_size, Image.Resampling.LANCZOS).save(
            qa_path("final-size-96dpi.png"), dpi=(screen_resolution, screen_resolution))
    panel_geometry = []
    for letter, ax in zip("abcd", axes.flat):
        bbox = ax.get_position()
        panel_geometry.append({"panel": letter, "plot_bbox_figure_fraction": list(bbox.bounds),
                               "plot_width_pt": bbox.width * fig.get_figwidth() * 72,
                               "plot_height_pt": bbox.height * fig.get_figheight() * 72})
    plt.close(fig)
    return alignment, font, panel_geometry


def run_json_audit(command, destination):
    process = subprocess.run([sys.executable, *map(str, command)], capture_output=True, text=True,
                             encoding="utf-8", env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONIOENCODING": "utf-8"})
    if process.stderr:
        print(process.stderr, file=sys.stderr)
    if process.stdout:
        result = json.loads(process.stdout)
        write_json(destination, result)
    else:
        raise RuntimeError(f"Audit produced no JSON: {command}")
    return result, process.returncode


def audit_and_report(document, digest, counts, qa_scripts, source_audit, alignment, font, panel_geometry):
    pdf = Path(artifact_path(BASE, ".pdf"))
    pdf_audit, text_code = run_json_audit([qa_scripts / "audit_pdf_text.py", pdf, "--min-pt", "5", "--json"], qa_path("pdf-text.json"))
    collisions, collision_code = run_json_audit([qa_scripts / "audit_figure_collisions.py", pdf,
        "--json", "--json-out", qa_path("pdf.collision-audit.json"), "--overlay-pdf", qa_path("pdf.collision-audit.pdf")], qa_path("pdf.collision-audit.json"))
    if not collisions["findings"]:
        sys.path.insert(0, str(qa_scripts))
        from audit_figure_collisions import write_overlay_pdf
        write_overlay_pdf(pdf, qa_path("pdf.collision-audit.pdf"), collisions["findings"])
    import pymupdf
    with pymupdf.open(pdf) as pdf_document:
        page = pdf_document[0]
        physical_mm = [page.rect.width / 72 * 25.4, page.rect.height / 72 * 25.4]
        fonts = sorted({span["font"] for block in page.get_text("dict")["blocks"] if "lines" in block
                        for line in block["lines"] for span in line["spans"]})
        pdf_text = page.get_text()
        assert all(phrase in pdf_text for phrase in ("Full SM", "E-only", "Simplified SM", "Fixed-3", "Abstain", "None"))
    raster = {}
    for suffix in (".png", ".tiff"):
        with Image.open(artifact_path(BASE, suffix)) as image:
            raster[suffix] = {"pixels": list(image.size), "dpi": [float(value) for value in image.info.get("dpi", [])]}
            assert image.width >= 4320
            assert all(value >= 599.9 for value in image.info["dpi"])
    assert abs(physical_mm[0] - 183) < 0.01
    warnings = [{"code": item["check_id"], "reason": item["message"]} for item in source_audit["findings"] if item["level"] == "WARN"]
    warnings.extend([
        {"code": "DESCRIPTIVE-STACK", "reason": "Panel d displays a composition without CIs. All source marginal intervals remain in the means CSV; no independence of segments is assumed."},
        {"code": "VISUAL-REVIEW-PENDING", "reason": "The image reader in this session cannot display PNG files. Final-size preview is provided for the main agent's panel-by-panel visual review; automated checks are not a visual approval."}])
    warnings.extend({"code": "COLLISION-WARN", "reason": finding} for finding in collisions["findings"] if finding.get("severity") == "WARN")
    summary = {
        "figure": PREFIX, "automated_checks_passed": text_code == 0 and collision_code == 0 and source_audit["summary"]["ready"],
        "human_visual_approval": False, "warnings": warnings,
        "contract": {"archetype": "quantitative grid", "question": "Does the four-arm slip-risk, stable-accuracy and inquiry-burden trade-off replicate in the second bank?",
                     "conclusion": "Full SM reduces slip false remediation versus Fixed-3 in both banks, loses stable final accuracy in Bank 2, and uses fewer slip inquiries than E-only; terminal compositions distinguish explicit none from abstention.",
                     "panel_roles": {"a": "paired slip false remediation", "b": "stable final-correct loss boundary", "c": "paired slip inquiry burden", "d": "descriptive Bank 2 terminal decomposition"}},
        "source": {"path": SOURCE.as_posix(), "sha256": digest, "experiment": document["experiment"], "timestamp": document["timestamp"],
                   "datasets": {ds: {key: document["data"][ds][key] for key in ("n_cases", "n_families")} for ds in DATASETS},
                   "n_types": 3, "n_seeds": 5, "bootstrap_resamples": 2000, "bootstrap_seed": 20261028,
                   "estimator": "Seeds averaged within each case; family bootstrap with multiplicity.",
                   "ci_origin": "All intervals copied from the formal summary. Paired intervals use contrasts only; no marginal CI subtraction or raw-run resampling.",
                   "csv_rows": counts, "csv_scope": "All estimate objects for both datasets, all four arms and three types, and all five formal contrasts; n_cases/n_episodes scalar metadata retained as CSV columns.",
                   "exclusions": "None within the formal summary. Plot subsets are marked by plotted_panels in both CSVs."},
        "semantics": {"arm_priors": "All four arms use the pair-space SM prior.",
                      "full_sm": "Posterior + E + LR + pair guard + extra-none + pair/mixed terminals.",
                      "e_only": "Posterior + E; no LR, guard, extra-none, or pair/mixed terminals.",
                      "simplified_sm": "Pair-space prior preserved; pair/mixed terminals disabled.",
                      "fixed3": "Three additional inquiries; final output is a leading single or none, with no pair terminal or adaptive abstention.",
                      "none": "Explicit none terminal; distinct from abstain.", "abstain": "No committed terminal diagnosis.",
                      "no_independence_assumption_for_stack": True},
        "size": {"width_mm": physical_mm[0], "height_mm": physical_mm[1], "raster": raster, "final_size_preview_dpi": 96},
        "style": {"inheritance": "style-only", "shared_style_path": (ROOT / "results/figures/scripts/style.py").as_posix(),
                  "shared_style_modified": False, "font_file": font, "pdf_fonts": fonts,
                  "minimum_configured_font_pt": 6.5, "minimum_pdf_font_pt": pdf_audit["minimum_found_pt"],
                  "arm_colors": ARM_COLORS, "terminal_colors": TERMINAL_COLORS,
                  "dataset_markers": {"v5": "open circle", "v6b": "filled square"},
                  "no_significance_or_noninferiority_badges": True, "vector_text_editable": True},
        "qa": {"scripts": qa_scripts.as_posix(), "source_validation": source_audit["summary"],
               "alignment_verdict": alignment["verdict"], "alignment_tolerance_pt": 1.5, "gutter_tolerance_pt": 1.5,
               "pdf_text": pdf_audit, "collision_verdict": collisions["verdict"], "collision_summary": collisions["summary"],
               "panel_geometry": panel_geometry,
               "panel_visual_review": [{"panel": p, "status": "pending main-agent visual review", "preview": qa_path("final-size-96dpi.png").as_posix()} for p in "abcd"]},
        "outputs": {"png": artifact_path(BASE, ".png"), "pdf": str(pdf), "svg": artifact_path(BASE, ".svg"),
                    "tiff": artifact_path(BASE, ".tiff"), "means_csv": str(BASE.parent / "data/second_bank_replication_means.csv"),
                    "contrasts_csv": str(BASE.parent / "data/second_bank_replication_contrasts.csv")}}
    write_json(qa_path("qa-summary.json"), summary)
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == digest
    print(json.dumps({"automated_checks_passed": summary["automated_checks_passed"], "size_mm": physical_mm,
                      "csv_rows": counts, "minimum_pdf_font_pt": pdf_audit["minimum_found_pt"],
                      "alignment": alignment["verdict"], "collisions": collisions["verdict"], "warnings": warnings}, ensure_ascii=False, indent=2))
    if text_code or collision_code or not source_audit["summary"]["ready"]:
        raise SystemExit(1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--qa-scripts", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    qa_scripts = args.qa_scripts.resolve()
    for name in ("validate_figure.py", "audit_panel_alignment.py", "audit_pdf_text.py", "audit_figure_collisions.py"):
        assert (qa_scripts / name).is_file(), qa_scripts / name
    source_audit, validation_code = run_json_audit([qa_scripts / "validate_figure.py", Path(__file__).resolve(), "--json"], qa_path("source-validation.json"))
    if validation_code:
        print(json.dumps(source_audit, indent=2))
        raise SystemExit(validation_code)
    document, digest = source_data()
    counts = export_source_csv(document, digest)
    alignment, font, panel_geometry = render(document, qa_scripts)
    audit_and_report(document, digest, counts, qa_scripts, source_audit, alignment, font, panel_geometry)


if __name__ == "__main__":
    main()
