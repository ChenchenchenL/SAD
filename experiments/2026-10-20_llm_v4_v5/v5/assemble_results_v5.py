"""Assemble docs/results_v5.md from the generated final tables plus audit prose."""
from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent
AUD = HERE / "out" / "final_audit"
DOCS = HERE.parents[2] / "docs"

tables = (AUD / "final_tables.md").read_text(encoding="utf-8")
parts = tables.split("\n## ")
sections = ["## " + p for p in parts[1:]]

header = """# 结果 v5：最终统计审计与报告收尾

日期：2026-10-20

状态：冻结方法的只读复算。没有启动新的付费 API 调用，没有调参，没有改变冻结方法，没有覆盖任何原始 episode、feedback 或 judge 记录。所有数字由 `v5/final_audit_v5.py`、`v5/feedback_audit_v5.py` 从原始文件重算，再由 `v5/render_final_tables.py` 生成本文表格。

主范围：**stable vs slip；mixed 只做压力测试**。本文不把 efficient、accuracy、safety 模式的最佳分项拼成同一个系统成绩。

## 核心结论（先看这里）

1. **稳定性停止 vs 固定 3 次（同 maxent 选题）**：slip 错误补救率 9.9% vs 47.8%，配对差 **−37.9 pp [−49.7, −26.1]**（template-family 有放回聚类 bootstrap）。stable 正确停止率 95.4% vs 97.0%，差 **−1.6 pp [−3.3, +0.0]**；stable 诊断正确率 95.6% vs 97.0%，差 **−1.4 pp [−3.0, +0.2]**。两个方法的 stable 正确停止率都高于预注册的 90% 门槛（95% CI 下界分别 93.3%、94.9%）；但两方法之间没有预注册非劣效 margin，不能把“CI 跨 0”写成等效或非劣效。
2. **slip 门槛**：点估计 **9.9%**；原报告（family 集合重采样）95% CI **[7.8%, 12.2%]**；按 family 有放回多重量采样修正后 95% CI **[6.9%, 12.9%]**，单侧 95% 上界 **12.25%**。点估计满足 ≤10% 门槛，但统计证据不支持“风险上限 ≤10%”。分类别看，order_of_operations 18.3% [12.0, 26.0]、decimals 15.0% [6.7, 20.0]，总体均值掩盖了较高风险类别。
3. **原始 90 与协议有效 87 并列**：stability_mixed 的 stable 正确率 92.4%（原始 90）vs 95.6%（协议有效 87）；正确停止率 92.2% vs 95.4%。原始 90 的 95% CI 下界 85.0%，协议有效 87 为 93.3%。三例排除是冻结后实施修正（`v5test:0013–0015`，共 4 个被抽 feedback episode：3 个 stable episode 全为 abstain，另 1 个为 slip episode），不是方法或阈值变化；原始分析完整保留并并列报告，不隐藏。
4. **J5/J10 不能单独用来证明普遍优越**：始终拒诊参照的 J5=J10=1.00，低于所有方法。λ=5、stable:slip=50:50 时 typed one-shot J5 3.79、stability_mixed 3.81，几乎相同；70:30 时 typed 更低；30:70 时 stability_mixed 略低；λ=10 时 stability_mixed 在各比例下都更低。加入事后探索性拒诊惩罚后排名还会变化。报告 J 必须同时报告 stable correct、slip error、拒诊率和提问成本，并说明 λ、类型比例和惩罚系数。
5. **反馈**：pipeline 相对公平 typed one-shot 的 target-hit 收益在 family 聚类后仍成立：DeepSeek 全量 **+24.2 pp [12.6, 35.7]**，GLM 子集 **+28.8 pp [15.3, 43.2]**；相对 no-diagnosis 为 +36.2 / +40.0 pp。overall 分别 +0.71 / +0.71。**pipeline 与 oracle 的差距不是跨 judge 稳健结论**：DeepSeek 全量 −12.1 pp [−21.1, −2.8]，GLM 子集 −9.3 pp [−22.9, +3.8]，共同子集 DeepSeek −10.3 pp [−23.3, +2.4]。**misleading 相对 one-shot 的下降也不是跨 judge 稳健**：DeepSeek −22.5 pp，GLM −12.2 pp（CI 跨 0）；相对 no-diagnosis 的 misleading 下降才是两者都成立的。
6. **GLM 子集的分母与旧 summary 不一致**：当前原始 judge 文件为 60 episodes（240 请求 pointwise，235 可解析；180 请求 pairwise，166 完整双序）。旧报告里的 n=63/61/59/63 与当前原始文件不一致，本文不使用旧 summary。GLM 权重必须按 GLM 自己的抽样层 25/2/16/7/10 重算，不能沿用 DeepSeek 的 54/2/34/16/10 权重。
7. **mixed 仍未解决**：stability_mixed 的 mixed 错误 62.3%，pair 识别 1.8%；held-out 错误 19.3%，pair 识别 0.2%。safety 的代价是 stable 正确率 −9.4 pp、追加提问 +1.51。mixed 不进入主成绩。
8. **验证器重试保留负结果**：protocol-valid 88/464 触发重试；explicit math incorrect 41→27、suspected leak 57→30，但 unverifiable 36→49；DeepSeek overall 3.61→3.47（88 条）或 3.68→3.50（全量 96 条），GLM 3.83→3.74。不能把 validator 当作已验证贡献。

## 本版修正摘要

- 原诊断 bootstrap 的实现用 `set()` 去重抽到的 family，等价于无放回子抽样，低估了 family 内相关性；本版改为 family 有放回、带 multiplicity 的聚类 bootstrap。主要 CI 因此变宽（例：stability_mixed − fixed3 slip **−37.9 pp [−49.7, −26.1]**，旧版 [−47.3, −28.9]）。
- 旧表把 `stability_mixed_maxent_minus_fixed3 · stable` 的 outcome 写成 `false`，并用 stable false-remediation 的 −0.7 pp 去说明“stable 准确率保持”。这是指标名错位。本版分开报告 stable 正确停止率、stable 诊断正确率、stable 错误 single 率和 stable 拒诊率。
- 旧决策文档的 J5 5.16 / J10 5.66 来自原始 90-case；协议有效 87 为 5.20 / 5.69。fixed3 的 8.62 也来自原始 90；协议有效 87 为 8.78。本版统一以 87 为主，原始 90 并列。
- 旧反馈 GLM 表把 DeepSeek 的分层权重套在 GLM 子集上，且 n=63/61/59/63 无法从当前原始文件复现。本版按 GLM 自己的抽样层重算（n=60/58/57/60；pairwise 166/180）。
- 旧跨 judge pointwise n=294 混入了 raw/final 两个 variant；pairwise n=360 是 per-order 记录数。本版共同子集 pointwise 为 235 条可解析记录（60 episodes，240 请求），pairwise 为 166 个完整双序比较（332 条 per-order）。
- per-label 的 mixed 分母旧实现重复计数；本版统一为每误区 3 cases×5 seeds = 15 个 mixed episodes。
- 新增 always-abstain 透明参照、J 的类型比例与拒诊惩罚敏感性、GLM 缺失解析与重复评分披露、原始 90 与 87 并列。

"""

footer = """

## 15. 统计解释边界

- **聚类单位**：36 个 template families；案例不是独立学生，5 个 simulation seeds 也不是独立学生。诊断和反馈均按 family 有放回重采样；GLM 共同子集为 31 个 families。
- **测试集**：v5 是人工编写/程序构建的新结构模板测试，不是真实学生数据，也不是跨真实课堂泛化。dev/test family overlap 为 0。
- **类别条件**：主实验和当前全库先验实验的 prompt 都提供 `DOMAIN: category`；所有对照获得相同 category。domain-free 先验是单独探索，不是主实验。
- **mixed**：只作为压力测试/风险暴露，不作为“方法已解决”的证据。
- **LLM judge**：不是人工金标准。两个 judge 的 absolute calibration 不同（GLM overall 系统性高约 0.4），pairwise outcome agreement 65.1%、κ=0.520，32.5% 的比较至少一方双序不一致。本文只把 target-hit/overall 的方向性收益作为跨 judge 证据；misleading 和 oracle gap 不作跨 judge 强主张。
- **GLM 子集**：60 episodes 请求，235/240 pointwise 可解析、166/180 pairwise 完整；pointwise 缺失为 pipeline 2、one_shot 3；pairwise 缺失按比较类型为 pipeline_vs_none 8、pipeline_vs_one_shot 5、oracle_vs_pipeline 2。未插补、未补调用。23 个 final record key 有重复评分，主分析取第一次；取最后一次的 unweighted overall 变化 ≤0.06，方向不变。
- **J5/J10**：`n_obs + λ·false remediation`，包含 initial observation；不是教学成本，也不是 API token 成本。J 对 λ、类型比例、拒诊惩罚敏感；始终拒诊的 J=1 说明 J 本身偏好拒诊。
- **stable 门槛**：预注册门槛是 stable 正确停止率 ≥90%。协议有效 87 中 stability_mixed 95.4% [93.3, 97.4]、fixed3 97.0% [94.9, 98.7]，两者都支持超过 90%；原始 90 中 stability_mixed 92.2% [85.0, 97.0]，点估计过线但 CI 下界低于 90。是否把 87 作为 primary 取决于是否接受冻结后排除规则修正；本文明确并列，不用 87 隐藏 90。
- **slip 门槛**：预注册门槛是 slip false remediation ≤10%。协议有效 87 点估计 9.9%，但 95% CI 上界 12.9%（修正后）/12.2%（旧集合重采样），单侧 95% 上界 12.25%。只能写“点估计满足门槛”，不能写“风险上限已被统计证明 ≤10%”。
- **非劣效/等效**：没有为 stable 准确率或 targeted vs maxent 预注册非劣效 margin。CI 跨 0 只能说明“未检测到差异”，不能证明等效或非劣效。本文不使用“差异不显著所以等效”的措辞。
- **原始 90 的 three-case 排除**：排除的是全局预测向量完全相同的 `fractions.add_numerators_denominators`（与 `fractions.common_denominator_numerator` 不可区分）。这是冻结后对已冻结排除规则的实现修正，改变了分母/样本范围，但没有改变方法、阈值或指标定义。原始 90 的 episode、summary、feedback 全部保留。
- **数据缺失**：GLM 5 条 pointwise、15 条 pairwise 记录未解析；没有新的付费调用，因此不能补。若论文要把 GLM 作为完整独立复现，这仍是缺口。
- **人工教学效果**：没有独立人工 rubric；pipeline feedback 的“质量”目前只是 LLM judge 代理。不能主张真实教学收益。
- **全库**：domain-free full prior + all-102 candidates 的 stable 97.2%、slip 3.7% 伴随 96.3% abstain，且跨类别候选没有可执行题面；不是全库、类别无关、端到端诊断成功。

## 16. 旧版数值与修正清单（审计轨迹）

| 项目 | 旧版/旧决策 | 本版（协议有效 87，除注明） | 原因 |
|---|---|---|---|
| stability_mixed − fixed3 slip error | −37.9 pp [−47.3, −28.9] | −37.9 pp [−49.7, −26.1] | family 有放回重采样 |
| stability_mixed − fixed3 stable | 旧表 outcome=`false`, −0.7 pp；决策文档称“stable false remediation” | 正确停止 −1.6 pp [−3.3, +0.0]；诊断正确 −1.4 pp [−3.0, +0.2]；错误 single −0.7 pp [−2.0, +0.5] | 指标名错位，拆开报告 |
| stability_mixed slip error CI | [7.8, 12.2] | 修正后 [6.9, 12.9]；旧口径仍并列 | 集合重采样 vs 有放回多重量采样 |
| stability_mixed slip J5 / J10 | 5.16 / 5.66（原始 90） | 5.20 / 5.69 | 原始 90 与 87 混用 |
| fixed3 slip J5 / J10 | 6.39 / 8.62（J10 原始 90） | 6.39 / 8.78 | 原始 90 与 87 混用 |
| stability_mixed stable correct | 95.6%（87）；旧决策未并列 90 | 87: 95.6%；90: 92.4% | 原始 90 未披露 |
| GLM pointwise n | 63/61/59/63 | 60/58/57/60（请求 60/条件；235/240 可解析） | 旧 summary 与原始 judge 文件不一致 |
| GLM weights | DeepSeek 层权重 | GLM 25/2/16/7/10 层权重（3.4/1.0/3.0/4.14/1.0） | 子集抽样设计不同 |
| GLM pipeline target hit | 0.672 | 0.756 | 权重修正 |
| cross-judge pointwise n | 294 | 235（final-only 共同可解析） | 旧版混入 raw/final |
| pairwise n | 360 per-order | 166 comparisons / 332 per-order | 旧版把 per-order 当比较数 |
| per-label mixed n | /15 | /15（修正重复计数后） | 实现重复计数 |
| always-abstain | 无 | J5=J10=1.00，stable correct 0，slip error 0，abstain 100% | 新增透明参照 |
| stability vs stability_mixed | 旧版未在主表强调 | stable +2.1 pp；slip error −5.1 pp；mixed error +13.8 pp | 解耦 MIXED 假设的代价/收益 |

## 17. 可复现性与文件

新增审计脚本与输出（原始文件未改）：

- [final_audit_v5.py](file:///./experiments/2026-10-20_llm_v4_v5/v5/final_audit_v5.py)
- [feedback_audit_v5.py](file:///./experiments/2026-10-20_llm_v4_v5/v5/feedback_audit_v5.py)
- [render_final_tables.py](file:///./experiments/2026-10-20_llm_v4_v5/v5/render_final_tables.py)
- [assemble_results_v5.py](file:///./experiments/2026-10-20_llm_v4_v5/v5/assemble_results_v5.py)
- [diagnosis_audit.json](file:///./experiments/2026-10-20_llm_v4_v5/v5/out/final_audit/diagnosis_audit.json)
- [feedback_audit.json](file:///./experiments/2026-10-20_llm_v4_v5/v5/out/final_audit/feedback_audit.json)
- [final_tables.md](file:///./experiments/2026-10-20_llm_v4_v5/v5/out/final_audit/final_tables.md)

原始冻结文件：

- [cases_test_v5.json](file:///./experiments/2026-10-20_llm_v4_v5/v5/data/cases_test_v5.json)
- [cases_test_v5_exclusion_corrected.json](file:///./experiments/2026-10-20_llm_v4_v5/v5/data/cases_test_v5_exclusion_corrected.json)
- [test_category_eps05_episodes.json](file:///./experiments/2026-10-20_llm_v4_v5/v5/out/test_category_eps05_episodes.json)
- [test_category_eps05_corrected_episodes.json](file:///./experiments/2026-10-20_llm_v4_v5/v5/out/test_category_eps05_corrected_episodes.json)
- [feedback_v5.jsonl](file:///./experiments/2026-10-20_llm_v4_v5/v5/out/feedback_v5.jsonl)
- [judge_v5_deepseek_v4_1_flash.jsonl](file:///./experiments/2026-10-20_llm_v4_v5/v5/out/judge_v5_deepseek_v4_1_flash.jsonl)
- [judge_v5_glm_5_3_flash_v5j_fast_2026_10_20.jsonl](file:///./experiments/2026-10-20_llm_v4_v5/v5/out/judge_v5_glm_5_3_flash_v5j_fast_2026_10_20.jsonl)
- [v5_freeze.json](file:///./experiments/2026-10-20_llm_v4_v5/v5/config/v5_freeze.json)
- [v5_exclusion_correction.json](file:///./experiments/2026-10-20_llm_v4_v5/v5/config/v5_exclusion_correction.json)

## 18. 结论

主结果可以进入写作，但必须按以下范围写：

- 可以主张：在类别条件、可执行误区库、人工结构模板测试上，稳定性感知停止相对 fixed3 显著降低 slip 错误补救；maxent 选题在固定 k=3 下有独立增益；公平 typed one-shot 证明旧 forced one-shot 的 100% 是定义产物；pipeline 反馈相对公平 one-shot 和 no-diagnosis 的 target-hit/overall 收益跨两个 judge 家族成立。
- 不能主张：slip 风险上限已被统计证明 ≤10%；stable 两方法非劣效/等效；pipeline 与 oracle 的差距跨 judge 稳健；pipeline 相对 one-shot 的 misleading 下降跨 judge 稳健；mixed 已解决；全库跨域端到端；真实学生泛化；validator retry 提升质量；LLM judge 等于人工金标准。
- 仍需补证据：若要写“风险认证/门槛保证”，需要更多 template families 或正式单侧设计；若要写“教学反馈质量”，需要独立人工 rubric；若要写“全库/跨域”，需要为跨类别误区补可执行 item predictions；若要写 mixed，需要把 pair identification 作为单独风险暴露实验；若要把 GLM 作为完整独立复现，需要补齐 5 条 pointwise 记录与 15 条 pairwise 记录（影响 14 个比较；本轮不启动付费调用）。

"""

body = header + "\n".join(sections) + footer
DOCS.joinpath("results_v5.md").write_text(body, encoding="utf-8")
print(DOCS / "results_v5.md")
