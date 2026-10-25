"""Render final v5 audit tables from the two audit JSON files."""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
AUD = OUT / "final_audit"

D = json.loads((AUD / "diagnosis_audit.json").read_text(encoding="utf-8"))
F = json.loads((AUD / "feedback_audit.json").read_text(encoding="utf-8"))


def pct(x, nd=1):
    return "—" if x is None else f"{100*x:.{nd}f}%"


def pct_ci(x):
    if not x or x.get("ci_low") is None:
        return pct(x["mean"]) if x and x.get("mean") is not None else "—"
    return f"{100*x['mean']:.1f}% [{100*x['ci_low']:.1f}, {100*x['ci_high']:.1f}]"


def num(x, nd=2):
    return "—" if x is None else f"{x:.{nd}f}"


def num_ci(x):
    if not x or x.get("ci_low") is None:
        return num(x["mean"]) if x and x.get("mean") is not None else "—"
    return f"{x['mean']:.2f} [{x['ci_low']:.2f}, {x['ci_high']:.2f}]"


def pp_ci(x):
    if not x or x.get("ci_low") is None:
        return "—"
    return f"{100*x['mean']:+.1f} pp [{100*x['ci_low']:+.1f}, {100*x['ci_high']:+.1f}]"


def diff_ci(x):
    if not x or x.get("ci_low") is None:
        return "—"
    return f"{x['mean']:+.2f} [{x['ci_low']:+.2f}, {x['ci_high']:+.2f}]"


L = []
L.append("# v5 统一复算表（从冻结 episodes / judge 原始记录生成）\n")
L.append("所有诊断数字从 `test_category_eps05_corrected_episodes.json` 重算；feedback 从 `feedback_v5.jsonl` 与两份 judge JSONL 重算。"
         " 诊断 CI 用 36 个 template family 有放回重采样（2000 次），案例先在 5 个 seeds 上平均；feedback CI 用 template family 有放回重采样。\n")
L.append("口径：`stable_correct_stop` = 停止且正确（预注册正确停止率）；`stable_correct` = 所有 stable episode 中终态为正确 single；"
         "`stable_coverage` = 终态 single/pair/mixed 的比例；`slip_error` = false remediation；`n_inquiries` = n_obs − 1；"
         "J5/J10 = n_obs + λ·false remediation（含 initial observation）。\n")

L.append("## 0. 分母与样本范围\n")
m = D["meta"]
L.append("| 项目 | protocol-valid | 原始 90-case |\n|---|---:|---:|\n")
L.append(f"| cases | {m['n_cases_protocol_valid']} | {m['n_cases_original']} |\n")
L.append(f"| true labels | {m['n_true_labels_protocol_valid']} | {m['n_true_labels_original']} |\n")
L.append(f"| template families | {m['n_families_protocol_valid']} | {m['n_families_original']} |\n")
L.append(f"| episodes | {m['n_episodes_protocol_valid']} | {m['n_episodes_original']} |\n")
L.append(f"| diagnosis bootstrap | {m['bootstrap']}，{m['bootstrap_unit']} | 同 |\n")
fm = F["meta"]
L.append("\nFeedback 分母：\n\n")
L.append("| 项目 | n |\n|---|---:|\n")
for k, label in (
    ("n_feedback_records_full", "原始反馈记录（120 episodes×4）"),
    ("n_feedback_records_valid", "protocol-valid 反馈记录（116×4）"),
    ("n_deepseek_final", "DeepSeek judge final 记录（全部）"),
    ("n_deepseek_final_valid", "DeepSeek judge final protocol-valid"),
    ("n_glm_final_unique", "GLM judge final 唯一记录（60×4，请求）"),
    ("n_glm_final_parsed", "GLM judge final 可解析记录"),
    ("n_glm_final_missing_parsed", "GLM final 缺失解析"),
    ("n_common_pointwise", "共同子集 pointwise 可解析记录"),
    ("n_glm_pairwise_requested_comparisons", "GLM pairwise 请求比较数（60×3）"),
    ("n_glm_pairwise_complete_comparisons", "GLM pairwise 完整双序比较"),
    ("n_common_pairwise_comparisons", "共同子集 pairwise 完整双序比较"),
):
    L.append(f"| {label} | {fm[k]} |\n")
L.append(f"| DeepSeek pairwise 有效完整双序比较（116×3） | {F['pairwise']['deepseek_full']['n_comparisons']} |\n")
L.append("| GLM pairwise 缺失记录（15 条；影响 14 个完整比较） | pipeline_vs_none 8；pipeline_vs_one_shot 5；oracle_vs_pipeline 2 |\n")

L.append("\n## 1. 诊断主表\n")
L.append("### 1.1 stable\n")
L.append("| method | n episodes | correct stop | correct | coverage | abstain | inquiries |\n")
L.append("|---|---:|---:|---:|---:|---:|---:|\n")
for r in D["rules"]:
    rid = r["id"]
    t = D["table"][rid]["stable"]
    cs = "—" if (rid.startswith("one_shot") or rid in ("random_k3", "fixed_k3", "maxent_k3")) else pct_ci(t["correct_stop"])
    L.append(f"| {r['label']} | {t['n_episodes']} | {cs} | {pct_ci(t['correct'])} | {pct_ci(t['diagnosed'])} | "
             f"{pct_ci(t['abstain'])} | {num_ci(t['n_inquiries'])} |\n")

L.append("\n### 1.2 slip\n")
L.append("| method | n episodes | error (false remediation) | explicit none | abstain | inquiries |\n")
L.append("|---|---:|---:|---:|---:|---:|\n")
for r in D["rules"]:
    t = D["table"][r["id"]]["slip"]
    L.append(f"| {r['label']} | {t['n_episodes']} | {pct_ci(t['false'])} | {pct_ci(t['none'])} | "
             f"{pct_ci(t['abstain'])} | {num_ci(t['n_inquiries'])} |\n")

L.append("\n### 1.3 mixed（压力测试，不作为主成绩）\n")
L.append("| method | n episodes | error | detected | exact pair | none | abstain | inquiries |\n")
L.append("|---|---:|---:|---:|---:|---:|---:|---:|\n")
for r in D["rules"]:
    t = D["table"][r["id"]]["mixed"]
    L.append(f"| {r['label']} | {t['n_episodes']} | {pct_ci(t['false'])} | {pct_ci(t['detected'])} | "
             f"{pct_ci(t['pair'])} | {pct_ci(t['none'])} | {pct_ci(t['abstain'])} | {num_ci(t['n_inquiries'])} |\n")

L.append("\n## 2. 稳定性停止 vs fixed3（同 maxent 选题）\n")
c_by = {st: D["contrasts"][f"stability_mixed_maxent_minus_fixed3/{st}"] for st in ("stable", "slip", "mixed")}
L.append("| 指标 | stability_mixed/maxent | fixed3/maxent | 配对差 [95% family-cluster CI] |\n")
L.append("|---|---:|---:|---:|\n")
for st, metric, label in (
    ("stable", "correct_stop", "stable 正确停止率"),
    ("stable", "correct", "stable 诊断正确率"),
    ("stable", "diagnosed", "stable 诊断覆盖率"),
    ("stable", "abstain", "stable 拒诊率"),
    ("stable", "wrong_single", "stable 错误 single 率"),
    ("stable", "n_inquiries", "stable 追加提问数"),
    ("slip", "false", "slip 错误补救率"),
    ("slip", "none", "slip 明确 none 率"),
    ("slip", "abstain", "slip 拒诊率"),
    ("slip", "n_inquiries", "slip 追加提问数"),
    ("mixed", "false", "mixed 错误补救率"),
    ("mixed", "n_inquiries", "mixed 追加提问数"),
):
    a = D["table"]["stability_mixed_maxent"][st][metric]
    b = D["table"]["fixed3"][st][metric]
    if metric in ("n_inquiries",):
        av, bv = num_ci(a), num_ci(b)
    else:
        av, bv = pct(a["mean"]), pct(b["mean"])
    L.append(f"| {label} | {av} | {bv} | {diff_ci(c_by[st][metric]) if metric == 'n_inquiries' else pp_ci(c_by[st][metric])} |\n")

L.append("\n## 3. 关键对照\n")
L.append("| contrast | outcome | 配对差 [95% family-cluster CI] |\n")
L.append("|---|---|---:|\n")
contrast_labels = [
    ("one_shot_typed_minus_one_shot_forced", "stable", "correct", "typed one-shot − forced one-shot · stable correct"),
    ("one_shot_typed_minus_one_shot_forced", "slip", "false", "typed one-shot − forced one-shot · slip error"),
    ("one_shot_typed_minus_one_shot_forced", "mixed", "false", "typed one-shot − forced one-shot · mixed error"),
    ("maxent_k3_minus_random_k3", "stable", "correct", "maxent k3 − random k3 · stable correct"),
    ("maxent_k3_minus_random_k3", "slip", "false", "maxent k3 − random k3 · slip error"),
    ("maxent_k3_minus_fixed_k3", "stable", "correct", "maxent k3 − fixed-order k3 · stable correct"),
    ("maxent_k3_minus_fixed_k3", "slip", "false", "maxent k3 − fixed-order k3 · slip error"),
    ("stability_mixed_maxent_minus_fixed3", "slip", "false", "stability_mixed − fixed3 · slip error"),
    ("stability_mixed_targeted_minus_stability_mixed_maxent", "stable", "correct", "targeted − maxent (stability_mixed) · stable correct"),
    ("stability_mixed_targeted_minus_stability_mixed_maxent", "slip", "false", "targeted − maxent (stability_mixed) · slip error"),
    ("stability_maxent_minus_stability_mixed_maxent", "stable", "correct", "stability − stability_mixed (maxent) · stable correct"),
    ("stability_maxent_minus_stability_mixed_maxent", "slip", "false", "stability − stability_mixed (maxent) · slip error"),
    ("stability_maxent_minus_stability_mixed_maxent", "mixed", "false", "stability − stability_mixed (maxent) · mixed error"),
    ("stability_mixed_heldout_maxent_minus_stability_mixed_maxent", "stable", "correct", "held-out − stability_mixed · stable correct"),
    ("stability_mixed_heldout_maxent_minus_stability_mixed_maxent", "mixed", "false", "held-out − stability_mixed · mixed error"),
    ("stability_mixed_heldout_maxent_minus_stability_mixed_maxent", "mixed", "n_inquiries", "held-out − stability_mixed · mixed inquiries"),
]
for a, st, metric, label in contrast_labels:
    x = D["contrasts"][f"{a}/{st}"][metric]
    val = diff_ci(x) if metric in ("n_inquiries",) else pp_ci(x)
    L.append(f"| {label} | {metric} | {val} |\n")

L.append("\n## 4. J5 / J10 与 always-abstain 参照\n")
L.append("### 4.1 分类型 J5/J10\n")
L.append("| method | stable J5 | slip J5 | mixed J5 | stable J10 | slip J10 | mixed J10 |\n")
L.append("|---|---:|---:|---:|---:|---:|---:|\n")
for r in D["rules"]:
    j = D["j_sensitivity"].get(r["id"])
    if not j:
        continue
    pt = j["per_type"]
    L.append(f"| {r['label']} | {num(pt['stable']['J5'])} | {num(pt['slip']['J5'])} | {num(pt['mixed']['J5'])} | "
             f"{num(pt['stable']['J10'])} | {num(pt['slip']['J10'])} | {num(pt['mixed']['J10'])} |\n")
pt = D["j_sensitivity"]["always_abstain"]["per_type"]
L.append(f"| **always abstain（透明参照）** | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |\n")

L.append("\n### 4.2 类型比例敏感性\n")
L.append("| method | J5 50:50 | J5 70:30 | J5 30:70 | J5 50:25:25 | J10 50:50 | J10 70:30 | J10 30:70 | J10 50:25:25 |\n")
L.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|\n")
for rid in ("one_shot_typed", "fixed3", "stability_maxent", "stability_mixed_maxent",
            "stability_mixed_heldout_maxent", "always_abstain"):
    j = D["j_sensitivity"][rid]
    vals = []
    for lam in ("J5", "J10"):
        for mix in ("stable_slip_50_50", "stable_slip_70_30", "stable_slip_30_70", "all_50_25_25"):
            vals.append(num(j[mix][lam]))
    label = next((r["label"] for r in D["rules"] if r["id"] == rid), rid)
    L.append(f"| {label} | " + " | ".join(vals) + " |\n")

L.append("\n### 4.3 事后探索性拒诊惩罚（50:50；c = 对 stable/mixed 的 none/abstain 每个加罚）\n")
L.append("| method | J5 c=0 | J5 c=1 | J5 c=2 | J5 c=5 | J10 c=0 | J10 c=1 | J10 c=2 | J10 c=5 |\n")
L.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|\n")
for rid in ("one_shot_typed", "fixed3", "stability_maxent", "stability_mixed_maxent",
            "stability_mixed_heldout_maxent", "always_abstain"):
    j = D["j_penalty_exploratory"][rid]
    vals = []
    for lam in (5, 10):
        for c_pen in (1, 2, 5):
            vals.append(num(j[f"lambda{lam}_c{c_pen}"]["stable_slip_50_50"]))
        # insert c=0 at proper position
    # rebuild columns explicitly
    vals = []
    for lam in (5, 10):
        vals.append(num(D["j_sensitivity"][rid]["stable_slip_50_50"][f"J{lam}"]))
        for c_pen in (1, 2, 5):
            vals.append(num(j[f"lambda{lam}_c{c_pen}"]["stable_slip_50_50"]))
    label = next((r["label"] for r in D["rules"] if r["id"] == rid), rid)
    L.append(f"| {label} | " + " | ".join(vals) + " |\n")

L.append("\n## 5. 分类别与逐误区失败\n")
L.append("### 5.1 stability_mixed/maxent 分类别\n")
L.append("| category | stable n | correct stop | slip n | slip error [95% CI] | mixed error |\n")
L.append("|---|---:|---:|---:|---:|---:|\n")
for cat in sorted(D["per_category"]):
    x = D["per_category"][cat]
    L.append(f"| {cat} | {x['stable']['n_cases']} | {pct(x['stable']['correct_stop']['mean'])} | "
             f"{x['slip']['n_cases']} | {pct_ci(x['slip']['false'])} | {pct(x['mixed']['false']['mean'])} |\n")

L.append("\n### 5.2 逐误区（stability_mixed/maxent；每行 3 cases×5 seeds=15 episodes）\n")
L.append("| misconception | stable correct /15 | slip error /15 | mixed detected /15 | mixed error /15 |\n")
L.append("|---|---:|---:|---:|---:|\n")
for hid, x in sorted(D["per_label"].items(), key=lambda kv: (-(kv[1]["slip_rate"] or 0), kv[0])):
    L.append(f"| {hid} | {x['stable_correct']}/{x['stable_n']} | {x['slip_error']}/{x['slip_n']} | "
             f"{x['mixed_detected']}/{x['mixed_n']} | {x['mixed_error']}/{x['mixed_n']} |\n")

L.append("\n## 6. 原始 90-case 与 protocol-valid 87-case 并列\n")
L.append("| method | scope | stable correct stop | stable correct | slip error | J5 slip | mixed error |\n")
L.append("|---|---|---:|---:|---:|---:|---:|\n")
for rid, v in D["original_vs_corrected"].items():
    label = next((r["label"] for r in D["rules"] if r["id"] == rid), rid)
    for scope, name in (("original_90", "original 90"), ("protocol_valid_87", "protocol-valid 87")):
        x = v[scope]
        cs = "—" if (rid.startswith("one_shot") or rid == "maxent_k3") else pct(x['stable/correct_stop']['mean'])
        L.append(f"| {label} | {name} | {cs} | {pct(x['stable/correct']['mean'])} | "
                 f"{pct_ci(x['slip/false'])} | {num(x['slip/J5']['mean'])} | {pct(x['mixed/false']['mean'])} |\n")

L.append("\n## 7. 噪声敏感性（protocol-valid；点估计）\n")
L.append("| eps | method | stable correct | stable correct stop | slip error | slip none | slip abstain | mixed error |\n")
L.append("|---:|---|---:|---:|---:|---:|---:|---:|\n")
for eps in ("0.0", "0.05", "0.10"):
    for rid in ("one_shot_typed", "fixed3", "stability_mixed_maxent", "stability_mixed_heldout_maxent"):
        x = D["noise"][eps][rid]
        L.append(f"| {eps} | {rid} | {pct(x['stable_correct'])} | {pct(x['stable_correct_stop'])} | "
                 f"{pct(x['slip_error'])} | {pct(x['slip_none'])} | {pct(x['slip_abstain'])} | {pct(x['mixed_error'])} |\n")
L.append("\n注：one-shot 的 `one_shot_episode` 不接收 eps 参数，因此 one-shot 三行相同；噪声敏感性只对自适应规则解释。\n")

L.append("\n## 8. Prior 与探索性全库规则\n")
L.append("| prior | n cases | top-1 | top-10 | cost USD |\n")
L.append("|---|---:|---:|---:|---:|\n")
for key, label in (("category_corrected", "category-conditioned (87)"),
                   ("category_original", "category-conditioned (original 90)"),
                   ("full_corrected", "full-library prompt (87)"),
                   ("full_original", "full-library prompt (original 90)"),
                   ("nodomain_corrected", "category-free full prompt (87)")):
    p = D["priors"][key]
    L.append(f"| {label} | {p['n_ok']} | {pct(p['top1_global'])} | {pct(p['top10_global_recall'])} | {p['estimated_cost_usd']:.4f} |\n")

L.append("\n| experiment | rule | stable correct | stable abstain | slip error | slip none | slip abstain |\n")
L.append("|---|---|---:|---:|---:|---:|---:|\n")
for key, label in (("nodomain_category", "domain-free prior, category candidates"),
                   ("nodomain_global", "domain-free prior, all 102 candidates"),
                   ("globalprior_category", "full prior, category candidates"),
                   ("globalprior_global", "full prior, all 102 candidates")):
    for rid, x in D["exploratory_prior_rules"][key].items():
        L.append(f"| {label} | {rid} | {pct(x['stable_correct'])} | {pct(x['stable_abstain'])} | "
                 f"{pct(x['slip_error'])} | {pct(x['slip_none'])} | {pct(x['slip_abstain'])} |\n")

L.append("\n## 9. Feedback pointwise（加权，权重和=174）\n")
for jkey, label in (("deepseek_full", "DeepSeek full (116 episodes)"),
                    ("glm_subset", "GLM subset (60 episodes; per-condition parsed n below)")):
    L.append(f"\n### {label}\n")
    L.append("| condition | n | target hit | misleading | answer leak | math | actionability | overclaim | overall |\n")
    L.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|\n")
    for cond in ("oracle", "pipeline", "one_shot", "no_diagnosis"):
        x = F["pointwise"][jkey][cond]
        L.append(f"| {cond} | {x['n']} | {pct(x['true_target_hit']['weighted'])} | {pct(x['misleading']['weighted'])} | "
                 f"{pct(x['answer_leak']['weighted'])} | {num(x['math_correct']['weighted'])} | "
                 f"{num(x['actionable_next_step']['weighted'])} | {pct(x['overclaims_misconception']['weighted'])} | "
                 f"{num(x['overall']['weighted'])} |\n")

L.append("\n## 10. Feedback 配对差：family-cluster vs episode bootstrap\n")
L.append("| scope | comparison | n pairs | target hit (cluster) | target hit (episode) | overall (cluster) | misleading (cluster) |\n")
L.append("|---|---|---:|---:|---:|---:|---:|\n")
for scope, label in (("deepseek_full", "DeepSeek full"), ("glm_subset", "GLM subset")):
    for other in ("one_shot", "no_diagnosis", "oracle"):
        p = F["paired"][scope][other]
        n = p["true_target_hit"]["n_pairs"]
        def cc(field):
            x = p[field]["cluster"]
            return f"{x['mean']:+.3f} [{x['ci_low']:+.3f}, {x['ci_high']:+.3f}]"
        def ee(field):
            x = p[field]["episode"]
            return f"{x['mean']:+.3f} [{x['ci_low']:+.3f}, {x['ci_high']:+.3f}]"
        L.append(f"| {label} | pipeline − {other} | {n} | {cc('true_target_hit')} | {ee('true_target_hit')} | "
                 f"{cc('overall')} | {cc('misleading')} |\n")

L.append("\n共同 60-episode 子集上的 judge 直接比较：\n\n")
L.append("| judge | comparison | n pairs | target hit | overall | misleading |\n")
L.append("|---|---|---:|---:|---:|---:|\n")
for who, label in (("deepseek", "DeepSeek"), ("glm", "GLM")):
    for other in ("one_shot", "no_diagnosis", "oracle"):
        p = F["paired"]["common"][who][other]
        L.append(f"| {label} | pipeline − {other} | {p['true_target_hit']['n_pairs']} | "
                 f"{p['true_target_hit']['cluster']['mean']:+.3f} [{p['true_target_hit']['cluster']['ci_low']:+.3f}, {p['true_target_hit']['cluster']['ci_high']:+.3f}] | "
                 f"{p['overall']['cluster']['mean']:+.3f} [{p['overall']['cluster']['ci_low']:+.3f}, {p['overall']['cluster']['ci_high']:+.3f}] | "
                 f"{p['misleading']['cluster']['mean']:+.3f} [{p['misleading']['cluster']['ci_low']:+.3f}, {p['misleading']['cluster']['ci_high']:+.3f}] |\n")

L.append("\n### 10.1 设计权重敏感性（success strata 合并抽样）\n")
L.append("| scope | comparison | target hit [cluster CI] |\n")
L.append("|---|---|---:|\n")
for scope, label in (("deepseek_full", "DeepSeek full"), ("glm_subset", "GLM subset")):
    for other, x in F["design_weight_sensitivity"][scope].items():
        L.append(f"| {label} | pipeline − {other} | {x['mean']:+.3f} [{x['ci_low']:+.3f}, {x['ci_high']:+.3f}] |\n")

L.append("\n## 11. Pairwise A/B（双序；每比较计一次；下表为未加权计数）\n")
L.append("| judge | student type | comparison | pipeline | comparator | tie | inconsistent | n |\n")
L.append("|---|---|---|---:|---:|---:|---:|---:|\n")
for jkey, label in (("deepseek_full", "DeepSeek"), ("glm_subset", "GLM")):
    counts = {}
    comps = set()
    for x in F["pairwise"][jkey]["counts"]:
        counts[(x["student_type"], x["comparison"], x["outcome"])] = x["n"]
        comps.add((x["student_type"], x["comparison"]))
    for st, comp in sorted(comps):
        first, second = comp.split("_vs_")
        if first == "pipeline":
            pipe = counts.get((st, comp, first), 0)
            other = counts.get((st, comp, second), 0)
        else:
            pipe = counts.get((st, comp, second), 0)
            other = counts.get((st, comp, first), 0)
        tie = counts.get((st, comp, "tie"), 0)
        inc = counts.get((st, comp, "inconsistent"), 0)
        L.append(f"| {label} | {st} | {comp} | {pipe} | {other} | {tie} | {inc} | {pipe+other+tie+inc} |\n")

L.append("\n## 12. 跨 judge（共同子集）\n")
cp = F["cross_pointwise"]
L.append(f"- pointwise 共同可解析记录：n={cp['n']}（请求为 60×4=240；GLM 缺 5 条解析）。\n")
L.append(f"- overall MAE={cp['fields']['overall']['mae']:.3f}，Pearson r={cp['fields']['overall']['pearson']:.3f}，exact agreement={pct(cp['fields']['overall']['exact_agreement'])}。\n")
L.append(f"- target-hit exact agreement={pct(cp['fields']['true_target_hit']['exact_agreement'])}；actionability exact agreement={pct(cp['fields']['actionable_next_step']['exact_agreement'])}。\n")
xp = F["cross_pairwise"]
L.append(f"- pairwise：完整双序比较 n={xp['n_comparisons']}（请求 180；GLM 缺 14 个完整比较，即 15 条记录）；outcome agreement={pct(xp['outcome_agreement'])}，Cohen's κ={xp['cohen_kappa']:.3f}；"
         f"per-order agreement={pct(xp['per_order_agreement'])}（n={xp['per_order_n']}）；tie={pct(xp['ties'])}，inconsistent={pct(xp['inconsistent'])}。\n")

L.append("\n## 13. Validator retry 与分母（flag 计数仅针对重试记录）\n")
L.append("| scope | n records | retried | initial math incorrect | final math incorrect | initial leak suspected | final leak suspected | initial unverifiable | final unverifiable |\n")
L.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|\n")
for key, label in (("full_480", "full 480"), ("protocol_valid_464", "protocol-valid 464"), ("glm_episode_subset_240", "GLM episode subset 240")):
    x = F["retry"][key]
    L.append(f"| {label} | {x['n_records']} | {x['n_retried']} | {x['init_math_incorrect']} | {x['final_math_incorrect']} | "
             f"{x['init_leak_suspected']} | {x['final_leak_suspected']} | {x['init_math_unverifiable']} | {x['final_math_unverifiable']} |\n")

L.append("\n| judge subset | n | raw overall | final overall | raw target hit | final target hit | raw leak | final leak |\n")
L.append("|---|---:|---:|---:|---:|---:|---:|---:|\n")
for key, label in (("deepseek_full_96", "DeepSeek retry full 96"), ("deepseek_valid_88", "DeepSeek retry valid 88"), ("glm_subset_54", "GLM retry subset 54")):
    x = F["retry_quality"][key]
    L.append(f"| {label} | {x['n']} | {num(x['raw_overall'])} | {num(x['final_overall'])} | {pct(x['raw_true_target_hit'])} | "
             f"{pct(x['final_true_target_hit'])} | {pct(x['raw_answer_leak'])} | {pct(x['final_answer_leak'])} |\n")

L.append("\n## 14. 成本（按 token usage 与既有单价估算）\n")
L.append("| 阶段 | USD |\n|---|---:|\n")
L.append(f"| feedback generation 480 | {F['cost']['feedback_generation_480']['usd']:.4f} |\n")
L.append(f"| DeepSeek judge 1296 calls | {F['cost']['deepseek_judge_1296']['usd']:.4f} |\n")
L.append(f"| GLM judge 681 calls | {F['cost']['glm_judge_681']['usd']:.4f} |\n")
L.append(f"| dev category prior | {0.005046160000000001:.4f} |\n")
for key, label in (("category_corrected", "test category prior"), ("full_corrected", "test full-library prior"), ("nodomain_corrected", "category-free full prior")):
    L.append(f"| {label} | {D['priors'][key]['estimated_cost_usd']:.4f} |\n")
total = (F['cost']['feedback_generation_480']['usd'] + F['cost']['deepseek_judge_1296']['usd'] +
         F['cost']['glm_judge_681']['usd'] + 0.005046160000000001 +
         D['priors']['category_corrected']['estimated_cost_usd'] +
         D['priors']['full_corrected']['estimated_cost_usd'] +
         D['priors']['nodomain_corrected']['estimated_cost_usd'])
L.append(f"| **合计** | **{total:.4f}** |\n")

(AUD / "final_tables.md").write_text("\n".join(x.rstrip("\n") for x in L) + "\n", encoding="utf-8")
print(AUD / "final_tables.md")
