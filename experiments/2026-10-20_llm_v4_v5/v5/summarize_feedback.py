"""Render protocol-valid feedback judge summary to Markdown."""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
d = json.loads((OUT / "feedback_v5_protocol_valid_summary.json").read_text(encoding="utf-8"))
lines = []
models = list(d["pointwise"])
for m in models:
    if not d["pointwise"][m].get("oracle", {}).get("n"):
        continue
    lines.append(f"\n### Judge: {m}\n")
    lines.append("| condition | n | target hit | misleading | answer leak | math | actionability | overclaim | overall |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for c in ("oracle", "pipeline", "one_shot", "no_diagnosis"):
        v = d["pointwise"][m][c]
        lines.append("| {} | {} | {:.3f} | {:.3f} | {:.3f} | {:.2f} | {:.2f} | {:.3f} | {:.2f} |".format(
            c, v["n"], v["weighted_true_target_hit"], v["weighted_misleading"], v["weighted_answer_leak"],
            v["weighted_math_correct"], v["weighted_actionable_next_step"], v["weighted_overclaims_misconception"], v["weighted_overall"]))
    lines.append("\n**Pairwise A/B double-order results**\n")
    lines.append("| student type | comparison | unweighted counts | episode weights |")
    lines.append("|---|---|---:|---:|")
    counts = d["pairwise"][m]["counts"]
    weights = d["pairwise"][m].get("weighted", {})
    keys = sorted(set(counts) | set(weights))
    for k in keys:
        st, pair, winner = k.split("/", 2)
        lines.append(f"| {st} | {pair} | {winner}:{counts.get(k, 0)} | {weights.get(k, 0):.1f} |")

cross = d.get("cross", {})
if cross.get("n"):
    lines.append("\n### Cross-judge agreement\n")
    for field, value in cross.items():
        if field == "pairwise":
            continue
        lines.append(f"- {field}: {value}")
    if cross.get("pairwise"):
        for field, value in cross["pairwise"].items():
            lines.append(f"- pairwise {field}: {value}")

ci_path = OUT / "feedback_v5_paired_judge_CIs.json"
if ci_path.exists():
    cis = json.loads(ci_path.read_text(encoding="utf-8"))
    lines.append("\n### Paired weighted episode bootstrap CIs (episode clusters)\n")
    lines.append("| judge | comparison | target hit | overall | misleading |")
    lines.append("|---|---|---:|---:|---:|")
    for m, x in cis.items():
        for other in ("one_shot", "no_diagnosis", "oracle"):
            parts = []
            for field in ("true_target_hit", "overall", "misleading"):
                k = f"pipeline_minus_{other}_{field}"
                if k not in x: continue
                y = x[k]
                parts.append(f"{y['diff']:+.3f} [{y['ci_low']:+.3f}, {y['ci_high']:+.3f}]")
            lines.append(f"| {m} | pipeline - {other} | {' | '.join(parts)} |")

retry = d.get("retry_ablation", {})
lines.append("\n### Validator retry ablation\n")
lines.append("| judge | n | raw overall | final overall | raw math | final math | raw leak | final leak |")
lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
for m, x in retry.items():
    if not x.get("n"):
        continue
    lines.append("| {} | {} | {:.2f} | {:.2f} | {:.2f} | {:.2f} | {:.3f} | {:.3f} |".format(
        m, x["n"], x.get("raw_overall") or 0, x.get("final_overall") or 0,
        x.get("raw_math_correct") or 0, x.get("final_math_correct") or 0,
        x.get("raw_answer_leak") or 0, x.get("final_answer_leak") or 0))
text = "\n".join(lines)
(OUT / "feedback_v5_tables.md").write_text(text, encoding="utf-8")
print(text)
