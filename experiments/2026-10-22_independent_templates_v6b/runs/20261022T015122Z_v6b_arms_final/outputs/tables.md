# 四臂对比：v6b 第二套题库 vs v5 参照

## v6b 第二套题库（90 cases / 32 families；与 v5 部分结构重叠）

| arm | stable correct | stable correct-stop | stable inquiries | slip false | slip none | slip abstain | slip inquiries | mixed false | slip J5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| full_sm | 0.929 [0.903, 0.951] | 0.924 | 1.45 | 0.084 [0.054, 0.120] | 0.504 | 0.411 | 4.05 | 0.602 | 5.47 |
| e_only | 0.964 [0.943, 0.982] | 0.951 | 1.58 | 0.033 [0.015, 0.057] | 0.158 | 0.809 | 5.81 | 0.667 | 6.98 |
| simplified_sm | 0.949 [0.922, 0.970] | 0.936 | 1.54 | 0.031 [0.013, 0.055] | 0.513 | 0.456 | 4.17 | 0.624 | 5.33 |
| fixed3 | 0.962 [0.941, 0.978] | N/A | 3.00 | 0.591 [0.444, 0.731] | 0.409 | 0.000 | 3.00 | 0.880 | 6.96 |

Note: fixed3 has no adaptive correct-stop (budget exhausted); use stable correct for the substantive comparison.


## v5 参照（87 protocol-valid cases / 36 families）

| arm | stable correct | stable correct-stop | stable inquiries | slip false | slip none | slip abstain | slip inquiries | mixed false | slip J5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| full_sm | 0.956 [0.934, 0.978] | 0.954 | 1.37 | 0.099 [0.070, 0.128] | 0.575 | 0.326 | 3.70 | 0.623 | 5.20 |
| e_only | 0.972 [0.951, 0.991] | 0.970 | 1.43 | 0.046 [0.023, 0.070] | 0.207 | 0.747 | 5.76 | 0.669 | 6.99 |
| simplified_sm | 0.961 [0.939, 0.981] | 0.959 | 1.42 | 0.039 [0.019, 0.061] | 0.589 | 0.372 | 3.84 | 0.634 | 5.03 |
| fixed3 | 0.970 [0.949, 0.987] | N/A | 3.00 | 0.478 [0.351, 0.607] | 0.522 | 0.000 | 3.00 | 0.876 | 6.39 |

Note: fixed3 has no adaptive correct-stop (budget exhausted); use stable correct for the substantive comparison.


## 配对差（family-cluster bootstrap 95% CI）

| contrast | type | metric | v6 | v5 |
|---|---|---|---:|---:|
| full_sm − fixed3 | stable | false | -0.022 [-0.040, -0.009] | -0.007 [-0.020, +0.005] |
| full_sm − fixed3 | stable | correct_stop | +0.924 [+0.900, +0.945] | +0.954 [+0.932, +0.975] |
| full_sm − fixed3 | stable | n_inquiries | -1.549 [-1.691, -1.379] | -1.628 [-1.769, -1.459] |
| full_sm − fixed3 | slip | false | -0.507 [-0.649, -0.359] | -0.379 [-0.497, -0.264] |
| full_sm − fixed3 | slip | correct_stop | +0.502 [+0.356, +0.650] | +0.566 [+0.434, +0.693] |
| full_sm − fixed3 | slip | n_inquiries | +1.049 [+0.561, +1.531] | +0.703 [+0.314, +1.105] |
| full_sm − fixed3 | mixed | false | -0.278 [-0.338, -0.224] | -0.253 [-0.297, -0.211] |
| full_sm − fixed3 | mixed | correct_stop | +0.009 [+0.002, +0.018] | +0.018 [+0.002, +0.040] |
| full_sm − fixed3 | mixed | n_inquiries | -0.549 [-0.753, -0.309] | -0.715 [-0.884, -0.530] |
| e_only − fixed3 | stable | false | -0.022 [-0.040, -0.009] | -0.007 [-0.020, +0.005] |
| e_only − fixed3 | stable | correct_stop | +0.951 [+0.929, +0.968] | +0.970 [+0.949, +0.989] |
| e_only − fixed3 | stable | n_inquiries | -1.424 [-1.574, -1.248] | -1.568 [-1.730, -1.382] |
| e_only − fixed3 | slip | false | -0.558 [-0.701, -0.402] | -0.432 [-0.561, -0.305] |
| e_only − fixed3 | slip | correct_stop | +0.042 [+0.010, +0.084] | +0.039 [+0.000, +0.096] |
| e_only − fixed3 | slip | n_inquiries | +2.809 [+2.687, +2.908] | +2.756 [+2.602, +2.875] |
| e_only − fixed3 | mixed | false | -0.213 [-0.278, -0.152] | -0.207 [-0.263, -0.155] |
| e_only − fixed3 | mixed | correct_stop | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| e_only − fixed3 | mixed | n_inquiries | +0.327 [+0.109, +0.611] | +0.168 [-0.081, +0.421] |
| simplified_sm − fixed3 | stable | false | -0.022 [-0.040, -0.009] | -0.007 [-0.020, +0.005] |
| simplified_sm − fixed3 | stable | correct_stop | +0.936 [+0.911, +0.956] | +0.959 [+0.936, +0.979] |
| simplified_sm − fixed3 | stable | n_inquiries | -1.458 [-1.602, -1.289] | -1.584 [-1.728, -1.414] |
| simplified_sm − fixed3 | slip | false | -0.560 [-0.703, -0.405] | -0.439 [-0.565, -0.316] |
| simplified_sm − fixed3 | slip | correct_stop | +0.509 [+0.366, +0.653] | +0.575 [+0.444, +0.701] |
| simplified_sm − fixed3 | slip | n_inquiries | +1.173 [+0.665, +1.669] | +0.839 [+0.428, +1.273] |
| simplified_sm − fixed3 | mixed | false | -0.256 [-0.312, -0.205] | -0.241 [-0.289, -0.197] |
| simplified_sm − fixed3 | mixed | correct_stop | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| simplified_sm − fixed3 | mixed | n_inquiries | -0.024 [-0.239, +0.230] | -0.211 [-0.426, +0.014] |
| full_sm − e_only | stable | false | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| full_sm − e_only | stable | correct_stop | -0.027 [-0.041, -0.014] | -0.016 [-0.031, -0.005] |
| full_sm − e_only | stable | n_inquiries | -0.124 [-0.177, -0.071] | -0.060 [-0.105, -0.010] |
| full_sm − e_only | slip | false | +0.051 [+0.027, +0.080] | +0.053 [+0.029, +0.080] |
| full_sm − e_only | slip | correct_stop | +0.460 [+0.328, +0.598] | +0.526 [+0.402, +0.654] |
| full_sm − e_only | slip | n_inquiries | -1.760 [-2.236, -1.320] | -2.053 [-2.466, -1.608] |
| full_sm − e_only | mixed | false | -0.064 [-0.094, -0.040] | -0.046 [-0.064, -0.028] |
| full_sm − e_only | mixed | correct_stop | +0.009 [+0.002, +0.018] | +0.018 [+0.002, +0.040] |
| full_sm − e_only | mixed | n_inquiries | -0.876 [-1.077, -0.715] | -0.883 [-1.069, -0.709] |
| simplified_sm − full_sm | stable | false | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| simplified_sm − full_sm | stable | correct_stop | +0.011 [+0.003, +0.021] | +0.005 [+0.000, +0.011] |
| simplified_sm − full_sm | stable | n_inquiries | +0.091 [+0.056, +0.126] | +0.044 [+0.011, +0.081] |
| simplified_sm − full_sm | slip | false | -0.053 [-0.082, -0.030] | -0.060 [-0.083, -0.038] |
| simplified_sm − full_sm | slip | correct_stop | +0.007 [+0.000, +0.017] | +0.009 [+0.000, +0.023] |
| simplified_sm − full_sm | slip | n_inquiries | +0.124 [+0.068, +0.186] | +0.136 [+0.078, +0.198] |
| simplified_sm − full_sm | mixed | false | +0.022 [+0.008, +0.041] | +0.011 [+0.002, +0.024] |
| simplified_sm − full_sm | mixed | correct_stop | -0.009 [-0.018, -0.002] | -0.018 [-0.040, -0.002] |
| simplified_sm − full_sm | mixed | n_inquiries | +0.524 [+0.393, +0.675] | +0.503 [+0.393, +0.629] |

## 预注册复现判据（v6b）

- **R1_full_sm_vs_fixed3**: PASS; substantive=PASS — slip_false: -0.507 [-0.649, -0.359]; stable_correct_stop: +0.924 [+0.900, +0.945]; stable_correct: -0.033 [-0.052, -0.016]
- **R2_e_only_vs_fixed3**: PASS; substantive=PASS — slip_false: -0.558 [-0.701, -0.402]; stable_correct_stop: +0.951 [+0.929, +0.968]; stable_correct: +0.002 [-0.012, +0.016]
- **R3_full_sm_vs_e_only**: PASS — slip_inquiries: -1.760 [-2.236, -1.320]; stable_correct_stop: -0.027 [-0.041, -0.014]
- **R4_simplified_sm_vs_full_sm**: PASS — slip_false: -0.053 [-0.082, -0.030]; slip_inquiries: +0.124 [+0.068, +0.186]

**ALL PASS (original criteria): True**
**ALL PASS (substantive stable-correct criteria): True**

## 先验质量

| dataset | n with prior | top-1 (category) | top-10 (category) |
|---|---:|---:|---:|
| v6b | 90 | 0.633 | 0.978 |
| v5 | 87 | 0.632 | 0.989 |

## 结构重叠审计（v5）

- text-parsed correct-answer issues: 0
- v6b items with a matching v5 structural signature: 18 / 96
- v6b cases with a matching v5 structural signature: 23 / 90
- v6b families with a matching v5 signature: 6
- matching families: neg_add_two_new, neg_minus_neg_new, neg_sub_pos_new, oo_add_sub_four, oo_muldiv_chain, sub3_zero_tail
- v6b is a second item bank / partial structural extension, not a strict unseen-structure holdout.