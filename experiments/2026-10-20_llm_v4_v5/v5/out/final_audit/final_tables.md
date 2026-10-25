# v5 统一复算表（从冻结 episodes / judge 原始记录生成）
所有诊断数字从 `test_category_eps05_corrected_episodes.json` 重算；feedback 从 `feedback_v5.jsonl` 与两份 judge JSONL 重算。 诊断 CI 用 36 个 template family 有放回重采样（2000 次），案例先在 5 个 seeds 上平均；feedback CI 用 template family 有放回重采样。
口径：`stable_correct_stop` = 停止且正确（预注册正确停止率）；`stable_correct` = 所有 stable episode 中终态为正确 single；`stable_coverage` = 终态 single/pair/mixed 的比例；`slip_error` = false remediation；`n_inquiries` = n_obs − 1；J5/J10 = n_obs + λ·false remediation（含 initial observation）。
## 0. 分母与样本范围
| 项目 | protocol-valid | 原始 90-case |
|---|---:|---:|
| cases | 87 | 90 |
| true labels | 29 | 30 |
| template families | 36 | 36 |
| episodes | 30015 | 31050 |
| diagnosis bootstrap | 2000，template_family (36), with replacement and multiplicity | 同 |

Feedback 分母：
| 项目 | n |
|---|---:|
| 原始反馈记录（120 episodes×4） | 480 |
| protocol-valid 反馈记录（116×4） | 464 |
| DeepSeek judge final 记录（全部） | 480 |
| DeepSeek judge final protocol-valid | 464 |
| GLM judge final 唯一记录（60×4，请求） | 240 |
| GLM judge final 可解析记录 | 235 |
| GLM final 缺失解析 | 5 |
| 共同子集 pointwise 可解析记录 | 235 |
| GLM pairwise 请求比较数（60×3） | 180 |
| GLM pairwise 完整双序比较 | 166 |
| 共同子集 pairwise 完整双序比较 | 166 |
| DeepSeek pairwise 有效完整双序比较（116×3） | 348 |
| GLM pairwise 缺失记录（15 条；影响 14 个完整比较） | pipeline_vs_none 8；pipeline_vs_one_shot 5；oracle_vs_pipeline 2 |

## 1. 诊断主表
### 1.1 stable
| method | n episodes | correct stop | correct | coverage | abstain | inquiries |
|---|---:|---:|---:|---:|---:|---:|
| one-shot forced (historical) | 435 | — | 63.2% [51.0, 75.3] | 100.0% [100.0, 100.0] | 0.0% [0.0, 0.0] | 0.00 [0.00, 0.00] |
| one-shot typed (fair) | 435 | — | 56.3% [44.0, 68.9] | 87.4% [78.2, 94.4] | 9.2% [2.9, 17.8] | 0.00 [0.00, 0.00] |
| random+k3 | 435 | — | 86.0% [79.2, 91.6] | 98.6% [97.3, 99.7] | 0.0% [0.0, 0.0] | 3.00 [3.00, 3.00] |
| fixed-order+k3 | 435 | — | 82.5% [72.1, 91.1] | 99.5% [98.8, 100.0] | 0.0% [0.0, 0.0] | 3.00 [3.00, 3.00] |
| maxent+k3 | 435 | — | 97.0% [94.9, 98.7] | 98.6% [97.3, 99.7] | 0.0% [0.0, 0.0] | 3.00 [3.00, 3.00] |
| maxent+fixed3 | 435 | 97.0% [94.9, 98.7] | 97.0% [94.9, 98.7] | 98.6% [97.3, 99.7] | 0.0% [0.0, 0.0] | 3.00 [3.00, 3.00] |
| maxent+posterior+budget abstain | 435 | 96.6% | 96.6% [95.1, 98.1] | 97.2% | 2.8% | 1.61 [1.47, 1.76] |
| maxent+entropy+budget abstain | 435 | 95.4% | 95.4% [93.5, 97.2] | 96.1% | 3.9% | 2.22 [2.10, 2.35] |
| maxent+stability | 435 | 97.7% [95.7, 99.3] | 97.7% [95.7, 99.3] | 98.2% [96.6, 99.4] | 1.4% [0.4, 2.8] | 1.40 [1.25, 1.57] |
| targeted+stability | 435 | 97.7% [95.7, 99.3] | 97.7% [95.7, 99.3] | 98.4% [96.9, 99.6] | 1.1% [0.2, 2.4] | 1.48 [1.28, 1.71] |
| maxent+stability_mixed | 435 | 95.4% [93.3, 97.4] | 95.6% [93.5, 97.7] | 98.2% [96.7, 99.3] | 0.5% [0.0, 1.2] | 1.37 [1.23, 1.53] |
| targeted+stability_mixed | 435 | 95.9% [93.7, 97.8] | 96.1% [93.9, 98.0] | 98.2% [96.8, 99.3] | 0.2% [0.0, 0.8] | 1.44 [1.25, 1.66] |
| maxent+held-out safety | 435 | 86.2% [82.7, 89.8] | 86.2% [82.7, 89.8] | 92.2% [89.3, 94.9] | 6.2% [3.6, 9.1] | 3.41 [3.25, 3.58] |

### 1.2 slip
| method | n episodes | error (false remediation) | explicit none | abstain | inquiries |
|---|---:|---:|---:|---:|---:|
| one-shot forced (historical) | 435 | 100.0% [100.0, 100.0] | 0.0% [0.0, 0.0] | 0.0% [0.0, 0.0] | 0.00 [0.00, 0.00] |
| one-shot typed (fair) | 435 | 87.4% [78.2, 94.4] | 3.4% [0.0, 7.6] | 9.2% [2.9, 17.8] | 0.00 [0.00, 0.00] |
| random+k3 | 435 | 88.7% [83.7, 93.0] | 11.3% [7.0, 16.3] | 0.0% [0.0, 0.0] | 3.00 [3.00, 3.00] |
| fixed-order+k3 | 435 | 89.4% [81.5, 95.8] | 10.6% [4.2, 18.5] | 0.0% [0.0, 0.0] | 3.00 [3.00, 3.00] |
| maxent+k3 | 435 | 47.8% [34.9, 61.0] | 52.2% [39.0, 65.1] | 0.0% [0.0, 0.0] | 3.00 [3.00, 3.00] |
| maxent+fixed3 | 435 | 47.8% [34.9, 61.0] | 52.2% [39.0, 65.1] | 0.0% [0.0, 0.0] | 3.00 [3.00, 3.00] |
| maxent+posterior+budget abstain | 435 | 22.1% [15.3, 29.0] | 0.0% | 77.9% | 5.29 [5.06, 5.51] |
| maxent+entropy+budget abstain | 435 | 6.4% [2.7, 9.5] | 0.0% | 93.6% | 5.86 [5.80, 5.92] |
| maxent+stability | 435 | 4.8% [2.4, 7.3] | 35.9% [22.5, 49.2] | 59.3% [45.5, 73.1] | 5.57 [5.39, 5.73] |
| targeted+stability | 435 | 4.1% [1.9, 6.6] | 34.3% [21.4, 47.5] | 61.6% [47.7, 75.4] | 5.59 [5.41, 5.75] |
| maxent+stability_mixed | 435 | 9.9% [6.9, 12.9] | 57.5% [43.9, 70.2] | 32.6% [20.9, 45.1] | 3.70 [3.27, 4.12] |
| targeted+stability_mixed | 435 | 9.9% [7.0, 13.0] | 58.6% [44.9, 71.5] | 31.5% [19.0, 44.2] | 3.66 [3.21, 4.11] |
| maxent+held-out safety | 435 | 7.4% [4.8, 10.0] | 57.5% [44.2, 70.1] | 35.2% [23.7, 46.8] | 3.80 [3.36, 4.24] |

### 1.3 mixed（压力测试，不作为主成绩）
| method | n episodes | error | detected | exact pair | none | abstain | inquiries |
|---|---:|---:|---:|---:|---:|---:|---:|
| one-shot forced (historical) | 435 | 100.0% [100.0, 100.0] | 0.0% [0.0, 0.0] | 0.0% [0.0, 0.0] | 0.0% [0.0, 0.0] | 0.0% [0.0, 0.0] | 0.00 [0.00, 0.00] |
| one-shot typed (fair) | 435 | 80.5% [71.1, 88.4] | 6.9% [2.4, 12.1] | 0.0% [0.0, 0.0] | 3.4% [0.0, 7.6] | 9.2% [2.9, 17.8] | 0.00 [0.00, 0.00] |
| random+k3 | 435 | 94.7% [92.5, 96.8] | 0.0% [0.0, 0.0] | 0.0% [0.0, 0.0] | 5.3% [3.2, 7.5] | 0.0% [0.0, 0.0] | 3.00 [3.00, 3.00] |
| fixed-order+k3 | 435 | 94.9% [92.1, 97.2] | 0.0% [0.0, 0.0] | 0.0% [0.0, 0.0] | 5.1% [2.8, 7.9] | 0.0% [0.0, 0.0] | 3.00 [3.00, 3.00] |
| maxent+k3 | 435 | 87.8% [83.0, 92.4] | 0.0% [0.0, 0.0] | 0.0% [0.0, 0.0] | 12.2% [7.6, 17.0] | 0.0% [0.0, 0.0] | 3.00 [3.00, 3.00] |
| maxent+fixed3 | 435 | 87.8% [83.0, 92.4] | 0.0% [0.0, 0.0] | 0.0% [0.0, 0.0] | 12.2% [7.6, 17.0] | 0.0% [0.0, 0.0] | 3.00 [3.00, 3.00] |
| maxent+posterior+budget abstain | 435 | 77.0% [73.5, 80.4] | 0.0% | 0.0% | 0.0% | 23.0% | 2.81 [2.62, 2.99] |
| maxent+entropy+budget abstain | 435 | 55.2% [49.1, 60.4] | 0.0% | 0.0% | 0.0% | 44.8% | 4.01 [3.80, 4.26] |
| maxent+stability | 435 | 76.1% [71.3, 80.5] | 0.0% [0.0, 0.0] | 0.0% [0.0, 0.0] | 5.5% [2.9, 9.0] | 18.4% [14.3, 23.0] | 2.84 [2.60, 3.09] |
| targeted+stability | 435 | 76.3% [71.4, 80.7] | 0.0% [0.0, 0.0] | 0.0% [0.0, 0.0] | 6.2% [3.4, 9.6] | 17.5% [13.3, 22.4] | 2.93 [2.65, 3.22] |
| maxent+stability_mixed | 435 | 62.3% [58.0, 66.4] | 20.2% [16.6, 24.1] | 1.8% [0.2, 4.2] | 12.9% [8.3, 18.0] | 4.6% [2.3, 7.4] | 2.29 [2.10, 2.46] |
| targeted+stability_mixed | 435 | 60.9% [56.2, 65.5] | 20.7% [16.7, 25.0] | 1.6% [0.2, 3.8] | 13.8% [9.3, 18.9] | 4.6% [2.3, 7.4] | 2.34 [2.12, 2.56] |
| maxent+held-out safety | 435 | 19.3% [14.9, 23.9] | 41.4% [36.3, 45.9] | 0.2% [0.0, 0.7] | 14.3% [9.7, 19.3] | 25.1% [19.4, 30.9] | 3.80 [3.60, 3.98] |

## 2. 稳定性停止 vs fixed3（同 maxent 选题）
| 指标 | stability_mixed/maxent | fixed3/maxent | 配对差 [95% family-cluster CI] |
|---|---:|---:|---:|
| stable 正确停止率 | 95.4% | 97.0% | -1.6 pp [-3.3, +0.0] |
| stable 诊断正确率 | 95.6% | 97.0% | -1.4 pp [-3.0, +0.2] |
| stable 诊断覆盖率 | 98.2% | 98.6% | -0.5 pp [-1.4, +0.4] |
| stable 拒诊率 | 0.5% | 0.0% | +0.5 pp [+0.0, +1.2] |
| stable 错误 single 率 | 0.9% | 1.6% | -0.7 pp [-2.0, +0.5] |
| stable 追加提问数 | 1.37 [1.23, 1.53] | 3.00 [3.00, 3.00] | -1.63 [-1.77, -1.47] |
| slip 错误补救率 | 9.9% | 47.8% | -37.9 pp [-49.7, -26.1] |
| slip 明确 none 率 | 57.5% | 52.2% | +5.3 pp [+1.2, +10.0] |
| slip 拒诊率 | 32.6% | 0.0% | +32.6 pp [+20.9, +45.1] |
| slip 追加提问数 | 3.70 [3.27, 4.12] | 3.00 [3.00, 3.00] | +0.70 [+0.27, +1.12] |
| mixed 错误补救率 | 62.3% | 87.8% | -25.5 pp [-30.1, -21.5] |
| mixed 追加提问数 | 2.29 [2.10, 2.46] | 3.00 [3.00, 3.00] | -0.71 [-0.90, -0.54] |

## 3. 关键对照
| contrast | outcome | 配对差 [95% family-cluster CI] |
|---|---|---:|
| typed one-shot − forced one-shot · stable correct | correct | -6.9 pp [-12.5, -2.2] |
| typed one-shot − forced one-shot · slip error | false | -12.6 pp [-21.8, -5.6] |
| typed one-shot − forced one-shot · mixed error | false | -19.5 pp [-28.9, -11.6] |
| maxent k3 − random k3 · stable correct | correct | +11.0 pp [+5.5, +17.6] |
| maxent k3 − random k3 · slip error | false | -40.9 pp [-52.6, -28.8] |
| maxent k3 − fixed-order k3 · stable correct | correct | +14.5 pp [+6.2, +24.4] |
| maxent k3 − fixed-order k3 · slip error | false | -41.6 pp [-55.7, -27.3] |
| stability_mixed − fixed3 · slip error | false | -37.9 pp [-49.7, -26.1] |
| targeted − maxent (stability_mixed) · stable correct | correct | +0.5 pp [-0.3, +1.4] |
| targeted − maxent (stability_mixed) · slip error | false | -0.0 pp [-1.5, +1.4] |
| stability − stability_mixed (maxent) · stable correct | correct | +2.1 pp [+0.8, +3.5] |
| stability − stability_mixed (maxent) · slip error | false | -5.1 pp [-7.6, -2.8] |
| stability − stability_mixed (maxent) · mixed error | false | +13.8 pp [+10.7, +16.7] |
| held-out − stability_mixed · stable correct | correct | -9.4 pp [-12.1, -7.0] |
| held-out − stability_mixed · mixed error | false | -43.0 pp [-48.5, -37.4] |
| held-out − stability_mixed · mixed inquiries | n_inquiries | +1.51 [+1.33, +1.70] |

## 4. J5 / J10 与 always-abstain 参照
### 4.1 分类型 J5/J10
| method | stable J5 | slip J5 | mixed J5 | stable J10 | slip J10 | mixed J10 |
|---|---:|---:|---:|---:|---:|---:|
| one-shot forced (historical) | 2.84 | 6.00 | 6.00 | 4.68 | 11.00 | 11.00 |
| one-shot typed (fair) | 2.21 | 5.37 | 5.02 | 3.41 | 9.74 | 9.05 |
| random+k3 | 4.63 | 8.44 | 8.74 | 5.26 | 12.87 | 13.47 |
| fixed-order+k3 | 4.85 | 8.47 | 8.75 | 5.70 | 12.94 | 13.49 |
| maxent+k3 | 4.08 | 6.39 | 8.39 | 4.16 | 8.78 | 12.78 |
| maxent+fixed3 | 4.08 | 6.39 | 8.39 | 4.16 | 8.78 | 12.78 |
| maxent+posterior+budget abstain | 2.65 | 7.40 | 7.66 | 2.68 | 8.50 | 11.51 |
| maxent+entropy+budget abstain | 3.25 | 7.18 | 7.77 | 3.29 | 7.50 | 10.53 |
| maxent+stability | 2.42 | 6.81 | 7.64 | 2.44 | 7.05 | 11.45 |
| targeted+stability | 2.51 | 6.79 | 7.74 | 2.55 | 7.00 | 11.56 |
| maxent+stability_mixed | 2.42 | 5.20 | 6.40 | 2.46 | 5.69 | 9.51 |
| targeted+stability_mixed | 2.47 | 5.15 | 6.38 | 2.49 | 5.65 | 9.43 |
| maxent+held-out safety | 4.43 | 5.17 | 5.76 | 4.46 | 5.54 | 6.73 |
| **always abstain（透明参照）** | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

### 4.2 类型比例敏感性
| method | J5 50:50 | J5 70:30 | J5 30:70 | J5 50:25:25 | J10 50:50 | J10 70:30 | J10 30:70 | J10 50:25:25 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| one-shot typed (fair) | 3.79 | 3.16 | 4.42 | 3.70 | 6.57 | 5.31 | 7.84 | 6.40 |
| maxent+fixed3 | 5.24 | 4.77 | 5.70 | 5.74 | 6.47 | 5.55 | 7.40 | 7.47 |
| maxent+stability | 4.61 | 3.74 | 5.49 | 4.82 | 4.75 | 3.83 | 5.67 | 5.85 |
| maxent+stability_mixed | 3.81 | 3.25 | 4.36 | 4.11 | 4.08 | 3.43 | 4.72 | 5.03 |
| maxent+held-out safety | 4.80 | 4.65 | 4.95 | 4.95 | 5.00 | 4.78 | 5.21 | 5.29 |
| always_abstain | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

### 4.3 事后探索性拒诊惩罚（50:50；c = 对 stable/mixed 的 none/abstain 每个加罚）
| method | J5 c=0 | J5 c=1 | J5 c=2 | J5 c=5 | J10 c=0 | J10 c=1 | J10 c=2 | J10 c=5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| one-shot typed (fair) | 3.79 | 3.85 | 3.91 | 4.10 | 6.57 | 6.64 | 6.70 | 6.89 |
| maxent+fixed3 | 5.24 | 5.24 | 5.25 | 5.27 | 6.47 | 6.48 | 6.49 | 6.51 |
| maxent+stability | 4.61 | 4.62 | 4.63 | 4.66 | 4.75 | 4.76 | 4.76 | 4.79 |
| maxent+stability_mixed | 3.81 | 3.82 | 3.83 | 3.85 | 4.08 | 4.09 | 4.10 | 4.12 |
| maxent+held-out safety | 4.80 | 4.84 | 4.88 | 5.00 | 5.00 | 5.04 | 5.07 | 5.19 |
| always_abstain | 1.00 | 1.50 | 2.00 | 3.50 | 1.00 | 1.50 | 2.00 | 3.50 |

## 5. 分类别与逐误区失败
### 5.1 stability_mixed/maxent 分类别
| category | stable n | correct stop | slip n | slip error [95% CI] | mixed error |
|---|---:|---:|---:|---:|---:|
| decimals | 12 | 98.3% | 12 | 15.0% [6.7, 20.0] | 61.7% |
| fractions | 18 | 98.9% | 18 | 5.6% [2.7, 9.3] | 61.1% |
| negative_numbers | 15 | 90.7% | 15 | 9.3% [1.5, 16.4] | 60.0% |
| order_of_operations | 12 | 91.7% | 12 | 18.3% [12.0, 26.0] | 61.7% |
| percentages | 12 | 96.7% | 12 | 6.7% [0.0, 11.4] | 58.3% |
| subtraction | 18 | 95.6% | 18 | 7.8% [1.3, 15.0] | 68.9% |

### 5.2 逐误区（stability_mixed/maxent；每行 3 cases×5 seeds=15 episodes）
| misconception | stable correct /15 | slip error /15 | mixed detected /15 | mixed error /15 |
|---|---:|---:|---:|---:|
| subtraction.always_borrow_left | 14/15 | 4/15 | 5/15 | 10/15 |
| decimals.longer_is_larger | 14/15 | 3/15 | 1/15 | 12/15 |
| decimals.shorter_is_larger | 15/15 | 3/15 | 4/15 | 9/15 |
| negative_numbers.multiplication_rule_for_addition | 14/15 | 3/15 | 3/15 | 8/15 |
| order_of_operations.addition_before_subtraction_always | 15/15 | 3/15 | 4/15 | 9/15 |
| order_of_operations.ignore_parentheses | 14/15 | 3/15 | 3/15 | 7/15 |
| order_of_operations.strict_left_to_right | 13/15 | 3/15 | 2/15 | 12/15 |
| decimals.ignore_decimal_point | 15/15 | 2/15 | 4/15 | 9/15 |
| fractions.denominator_comparison_error | 14/15 | 2/15 | 1/15 | 10/15 |
| fractions.ignore_denominators | 15/15 | 2/15 | 2/15 | 12/15 |
| negative_numbers.two_negatives_always_positive | 15/15 | 2/15 | 2/15 | 11/15 |
| order_of_operations.multiplication_before_division_always | 13/15 | 2/15 | 4/15 | 9/15 |
| percentages.add_percentages_directly | 14/15 | 2/15 | 4/15 | 7/15 |
| subtraction.smaller_from_larger | 15/15 | 2/15 | 5/15 | 9/15 |
| decimals.right_align_decimals | 15/15 | 1/15 | 4/15 | 7/15 |
| fractions.multiply_across_for_division | 15/15 | 1/15 | 3/15 | 9/15 |
| negative_numbers.larger_absolute_value_always_wins | 12/15 | 1/15 | 3/15 | 9/15 |
| negative_numbers.negative_swaps_operation | 13/15 | 1/15 | 3/15 | 9/15 |
| percentages.percent_equals_decimal | 15/15 | 1/15 | 1/15 | 11/15 |
| percentages.percentage_as_index | 15/15 | 1/15 | 4/15 | 10/15 |
| subtraction.diff_0_n_equals_n | 14/15 | 1/15 | 4/15 | 8/15 |
| fractions.keep_common_denominator_for_multiplication | 15/15 | 0/15 | 3/15 | 6/15 |
| fractions.natural_number_bias_numerator_only | 15/15 | 0/15 | 1/15 | 9/15 |
| fractions.subtract_across | 15/15 | 0/15 | 1/15 | 9/15 |
| negative_numbers.negative_times_negative_negative | 14/15 | 0/15 | 4/15 | 8/15 |
| percentages.reverse_percentage_error | 14/15 | 0/15 | 5/15 | 7/15 |
| subtraction.borrow_from_bottom | 14/15 | 0/15 | 1/15 | 13/15 |
| subtraction.borrow_no_decrement | 15/15 | 0/15 | 5/15 | 10/15 |
| subtraction.stops_borrow_at_zero | 15/15 | 0/15 | 2/15 | 12/15 |

## 6. 原始 90-case 与 protocol-valid 87-case 并列
| method | scope | stable correct stop | stable correct | slip error | J5 slip | mixed error |
|---|---|---:|---:|---:|---:|---:|
| one-shot forced (historical) | original 90 | — | 64.4% | 100.0% [100.0, 100.0] | 6.00 | 100.0% |
| one-shot forced (historical) | protocol-valid 87 | — | 63.2% | 100.0% [100.0, 100.0] | 6.00 | 100.0% |
| one-shot typed (fair) | original 90 | — | 57.8% | 87.8% [78.8, 94.7] | 5.39 | 81.1% |
| one-shot typed (fair) | protocol-valid 87 | — | 56.3% | 87.4% [78.2, 94.4] | 5.37 | 80.5% |
| maxent+k3 | original 90 | — | 97.1% | 46.2% [33.3, 59.4] | 6.31 | 87.1% |
| maxent+k3 | protocol-valid 87 | — | 97.0% | 47.8% [34.9, 61.0] | 6.39 | 87.8% |
| maxent+fixed3 | original 90 | 97.1% | 97.1% | 46.2% [33.3, 59.4] | 6.31 | 87.1% |
| maxent+fixed3 | protocol-valid 87 | 97.0% | 97.0% | 47.8% [34.9, 61.0] | 6.39 | 87.8% |
| maxent+stability_mixed | original 90 | 92.2% | 92.4% | 10.0% [7.1, 12.9] | 5.16 | 60.2% |
| maxent+stability_mixed | protocol-valid 87 | 95.4% | 95.6% | 9.9% [6.9, 12.9] | 5.20 | 62.3% |
| maxent+held-out safety | original 90 | 83.3% | 83.3% | 7.6% [5.1, 10.1] | 5.13 | 18.7% |
| maxent+held-out safety | protocol-valid 87 | 86.2% | 86.2% | 7.4% [4.8, 10.0] | 5.17 | 19.3% |

## 7. 噪声敏感性（protocol-valid；点估计）
| eps | method | stable correct | stable correct stop | slip error | slip none | slip abstain | mixed error |
|---:|---|---:|---:|---:|---:|---:|---:|
| 0.0 | one_shot_typed | 56.3% | 0.0% | 87.4% | 3.4% | 9.2% | 80.5% |
| 0.0 | fixed3 | 100.0% | 100.0% | 41.4% | 58.6% | 0.0% | 51.5% |
| 0.0 | stability_mixed_maxent | 100.0% | 100.0% | 0.0% | 62.1% | 37.9% | 67.4% |
| 0.0 | stability_mixed_heldout_maxent | 100.0% | 100.0% | 0.0% | 60.9% | 39.1% | 25.7% |
| 0.05 | one_shot_typed | 56.3% | 0.0% | 87.4% | 3.4% | 9.2% | 80.5% |
| 0.05 | fixed3 | 97.0% | 97.0% | 47.8% | 52.2% | 0.0% | 87.8% |
| 0.05 | stability_mixed_maxent | 95.6% | 95.4% | 9.9% | 57.5% | 32.6% | 62.3% |
| 0.05 | stability_mixed_heldout_maxent | 86.2% | 86.2% | 7.4% | 57.5% | 35.2% | 19.3% |
| 0.10 | one_shot_typed | 56.3% | 0.0% | 87.4% | 3.4% | 9.2% | 80.5% |
| 0.10 | fixed3 | 94.7% | 94.7% | 71.5% | 28.5% | 0.0% | 92.9% |
| 0.10 | stability_mixed_maxent | 92.4% | 92.4% | 10.8% | 51.7% | 37.5% | 56.1% |
| 0.10 | stability_mixed_heldout_maxent | 73.6% | 73.6% | 4.8% | 48.3% | 46.9% | 17.0% |

注：one-shot 的 `one_shot_episode` 不接收 eps 参数，因此 one-shot 三行相同；噪声敏感性只对自适应规则解释。

## 8. Prior 与探索性全库规则
| prior | n cases | top-1 | top-10 | cost USD |
|---|---:|---:|---:|---:|
| category-conditioned (87) | 87 | 64.4% | 98.9% | 0.0272 |
| category-conditioned (original 90) | 90 | 65.6% | 98.9% | 0.0272 |
| full-library prompt (87) | 87 | 58.6% | 98.9% | 0.2548 |
| full-library prompt (original 90) | 90 | 64.4% | 98.9% | 0.2548 |
| category-free full prompt (87) | 87 | 58.6% | 97.7% | 0.2450 |

| experiment | rule | stable correct | stable abstain | slip error | slip none | slip abstain |
|---|---|---:|---:|---:|---:|---:|
| domain-free prior, category candidates | one_shot_typed | 31.0% | 32.2% | 67.8% | 0.0% | 32.2% |
| domain-free prior, category candidates | fixed3 | 96.3% | 0.0% | 47.4% | 52.6% | 0.0% |
| domain-free prior, category candidates | maxent_k3 | 96.3% | 0.0% | 47.4% | 52.6% | 0.0% |
| domain-free prior, category candidates | stability_maxent | 97.7% | 1.4% | 5.5% | 32.6% | 61.8% |
| domain-free prior, category candidates | stability_mixed_maxent | 95.6% | 1.4% | 9.2% | 65.1% | 25.7% |
| domain-free prior, all 102 candidates | one_shot_typed | 31.0% | 32.2% | 67.8% | 0.0% | 32.2% |
| domain-free prior, all 102 candidates | fixed3 | 96.1% | 0.0% | 100.0% | 0.0% | 0.0% |
| domain-free prior, all 102 candidates | maxent_k3 | 96.1% | 0.0% | 100.0% | 0.0% | 0.0% |
| domain-free prior, all 102 candidates | stability_maxent | 97.2% | 1.4% | 3.7% | 0.0% | 96.3% |
| full prior, category candidates | one_shot_typed | 43.7% | 10.3% | 88.5% | 1.1% | 10.3% |
| full prior, category candidates | fixed3 | 95.9% | 0.0% | 50.8% | 49.2% | 0.0% |
| full prior, category candidates | maxent_k3 | 95.9% | 0.0% | 50.8% | 49.2% | 0.0% |
| full prior, category candidates | stability_maxent | 97.5% | 1.6% | 4.6% | 28.5% | 66.9% |
| full prior, category candidates | stability_mixed_maxent | 94.9% | 1.1% | 10.1% | 64.8% | 25.1% |
| full prior, all 102 candidates | one_shot_typed | 43.7% | 10.3% | 88.5% | 1.1% | 10.3% |
| full prior, all 102 candidates | fixed3 | 96.1% | 0.0% | 96.6% | 3.4% | 0.0% |
| full prior, all 102 candidates | maxent_k3 | 96.1% | 0.0% | 96.6% | 3.4% | 0.0% |
| full prior, all 102 candidates | stability_maxent | 97.2% | 1.6% | 3.2% | 0.0% | 96.8% |

## 9. Feedback pointwise（加权，权重和=174）

### DeepSeek full (116 episodes)
| condition | n | target hit | misleading | answer leak | math | actionability | overclaim | overall |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| oracle | 116 | 79.5% | 18.1% | 6.2% | 4.90 | 4.44 | 26.3% | 4.16 |
| pipeline | 116 | 67.5% | 30.5% | 5.4% | 4.83 | 4.32 | 32.6% | 3.88 |
| one_shot | 116 | 43.2% | 53.0% | 7.2% | 4.56 | 4.11 | 61.0% | 3.18 |
| no_diagnosis | 116 | 31.3% | 67.7% | 6.8% | 4.53 | 4.03 | 67.0% | 2.92 |

### GLM subset (60 episodes; per-condition parsed n below)
| condition | n | target hit | misleading | answer leak | math | actionability | overclaim | overall |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| oracle | 60 | 85.6% | 8.6% | 1.7% | 4.90 | 4.55 | 19.7% | 4.56 |
| pipeline | 58 | 75.6% | 21.4% | 0.0% | 4.93 | 4.53 | 20.8% | 4.34 |
| one_shot | 57 | 49.0% | 30.3% | 6.2% | 4.75 | 4.33 | 39.7% | 3.64 |
| no_diagnosis | 60 | 36.1% | 51.8% | 2.0% | 4.62 | 4.09 | 53.6% | 3.23 |

## 10. Feedback 配对差：family-cluster vs episode bootstrap
| scope | comparison | n pairs | target hit (cluster) | target hit (episode) | overall (cluster) | misleading (cluster) |
|---|---|---:|---:|---:|---:|---:|
| DeepSeek full | pipeline − one_shot | 116 | +0.242 [+0.126, +0.357] | +0.242 [+0.146, +0.337] | +0.705 [+0.415, +0.979] | -0.225 [-0.337, -0.109] |
| DeepSeek full | pipeline − no_diagnosis | 116 | +0.362 [+0.217, +0.494] | +0.362 [+0.261, +0.461] | +0.959 [+0.630, +1.270] | -0.372 [-0.495, -0.238] |
| DeepSeek full | pipeline − oracle | 116 | -0.121 [-0.211, -0.028] | -0.121 [-0.210, -0.032] | -0.272 [-0.462, -0.080] | +0.124 [+0.045, +0.200] |
| GLM subset | pipeline − one_shot | 55 | +0.288 [+0.153, +0.432] | +0.288 [+0.143, +0.433] | +0.714 [+0.352, +1.051] | -0.122 [-0.266, +0.008] |
| GLM subset | pipeline − no_diagnosis | 58 | +0.400 [+0.258, +0.533] | +0.400 [+0.254, +0.536] | +1.123 [+0.798, +1.425] | -0.328 [-0.448, -0.202] |
| GLM subset | pipeline − oracle | 58 | -0.093 [-0.229, +0.038] | -0.093 [-0.221, +0.029] | -0.239 [-0.563, +0.055] | +0.123 [+0.014, +0.242] |

共同 60-episode 子集上的 judge 直接比较：
| judge | comparison | n pairs | target hit | overall | misleading |
|---|---|---:|---:|---:|---:|
| DeepSeek | pipeline − one_shot | 60 | +0.217 [+0.066, +0.368] | +0.603 [+0.295, +0.904] | -0.150 [-0.279, -0.029] |
| DeepSeek | pipeline − no_diagnosis | 60 | +0.377 [+0.214, +0.536] | +1.037 [+0.681, +1.371] | -0.381 [-0.516, -0.241] |
| DeepSeek | pipeline − oracle | 60 | -0.103 [-0.233, +0.024] | -0.171 [-0.473, +0.145] | +0.171 [+0.061, +0.276] |
| GLM | pipeline − one_shot | 55 | +0.288 [+0.153, +0.432] | +0.714 [+0.352, +1.051] | -0.122 [-0.266, +0.008] |
| GLM | pipeline − no_diagnosis | 58 | +0.400 [+0.258, +0.533] | +1.123 [+0.798, +1.425] | -0.328 [-0.448, -0.202] |
| GLM | pipeline − oracle | 58 | -0.093 [-0.229, +0.038] | -0.239 [-0.563, +0.055] | +0.123 [+0.014, +0.242] |

### 10.1 设计权重敏感性（success strata 合并抽样）
| scope | comparison | target hit [cluster CI] |
|---|---|---:|
| DeepSeek full | pipeline − one_shot | +0.245 [+0.128, +0.357] |
| DeepSeek full | pipeline − no_diagnosis | +0.361 [+0.217, +0.492] |
| DeepSeek full | pipeline − oracle | -0.121 [-0.213, -0.026] |
| GLM subset | pipeline − one_shot | +0.286 [+0.151, +0.425] |
| GLM subset | pipeline − no_diagnosis | +0.392 [+0.254, +0.522] |
| GLM subset | pipeline − oracle | -0.088 [-0.234, +0.049] |

## 11. Pairwise A/B（双序；每比较计一次；下表为未加权计数）
| judge | student type | comparison | pipeline | comparator | tie | inconsistent | n |
|---|---|---|---:|---:|---:|---:|---:|
| DeepSeek | slip | oracle_vs_pipeline | 12 | 29 | 4 | 15 | 60 |
| DeepSeek | slip | pipeline_vs_none | 36 | 7 | 9 | 8 | 60 |
| DeepSeek | slip | pipeline_vs_one_shot | 40 | 5 | 7 | 8 | 60 |
| DeepSeek | stable | oracle_vs_pipeline | 11 | 17 | 7 | 21 | 56 |
| DeepSeek | stable | pipeline_vs_none | 41 | 4 | 5 | 6 | 56 |
| DeepSeek | stable | pipeline_vs_one_shot | 22 | 7 | 8 | 19 | 56 |
| GLM | slip | oracle_vs_pipeline | 6 | 18 | 1 | 8 | 33 |
| GLM | slip | pipeline_vs_none | 19 | 4 | 2 | 6 | 31 |
| GLM | slip | pipeline_vs_one_shot | 16 | 4 | 4 | 6 | 30 |
| GLM | stable | oracle_vs_pipeline | 3 | 10 | 7 | 5 | 25 |
| GLM | stable | pipeline_vs_none | 16 | 1 | 5 | 0 | 22 |
| GLM | stable | pipeline_vs_one_shot | 12 | 4 | 3 | 6 | 25 |

## 12. 跨 judge（共同子集）
- pointwise 共同可解析记录：n=235（请求为 60×4=240；GLM 缺 5 条解析）。
- overall MAE=0.557，Pearson r=0.820，exact agreement=51.9%。
- target-hit exact agreement=92.3%；actionability exact agreement=60.0%。
- pairwise：完整双序比较 n=166（请求 180；GLM 缺 14 个完整比较，即 15 条记录）；outcome agreement=65.1%，Cohen's κ=0.520；per-order agreement=72.6%（n=332）；tie=20.5%，inconsistent=32.5%。

## 13. Validator retry 与分母（flag 计数仅针对重试记录）
| scope | n records | retried | initial math incorrect | final math incorrect | initial leak suspected | final leak suspected | initial unverifiable | final unverifiable |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| full 480 | 480 | 96 | 49 | 30 | 57 | 30 | 36 | 54 |
| protocol-valid 464 | 464 | 88 | 41 | 27 | 57 | 30 | 36 | 49 |
| GLM episode subset 240 | 240 | 54 | 26 | 16 | 35 | 20 | 27 | 34 |

| judge subset | n | raw overall | final overall | raw target hit | final target hit | raw leak | final leak |
|---|---:|---:|---:|---:|---:|---:|---:|
| DeepSeek retry full 96 | 96 | 3.68 | 3.50 | 59.4% | 53.1% | 9.4% | 4.2% |
| DeepSeek retry valid 88 | 88 | 3.61 | 3.47 | 56.8% | 51.1% | 10.2% | 4.5% |
| GLM retry subset 54 | 54 | 3.83 | 3.74 | 59.3% | 53.7% | 5.6% | 0.0% |

## 14. 成本（按 token usage 与既有单价估算）
| 阶段 | USD |
|---|---:|
| feedback generation 480 | 0.0678 |
| DeepSeek judge 1296 calls | 0.2021 |
| GLM judge 681 calls | 0.1964 |
| dev category prior | 0.0050 |
| test category prior | 0.0272 |
| test full-library prior | 0.2548 |
| category-free full prior | 0.2450 |
| **合计** | **0.9983** |
