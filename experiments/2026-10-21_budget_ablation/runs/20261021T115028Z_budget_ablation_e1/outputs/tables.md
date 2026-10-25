# Question budget curve for stability-aware diagnosis

Same frozen v5 cases, LLM prior, pair-augmented hypothesis space, MaxEnt selection, eps=0.05, and 5 seeds. Only the cap on additional inquiries changes (cap=1/2/3/6 means max_obs=2/3/4/7 including the initial item).

## SM budget curve

| cap | stable inquiries | slip inquiries | stopped before cap | budget exhausted | slip false | slip none | slip abstain | stable correct | stable correct stop | stable abstain |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1.00 | 1.00 | 0.0 | 100.0 | 2.5 [1.1, 4.2] | 0.0 | 97.5 | 72.6 [58.9, 84.4] | 0.0 | 26.9 |
| 2 | 1.27 | 1.97 | 38.5 | 61.5 | 6.7 [4.3, 8.8] | 28.7 | 64.6 | 91.5 [86.7, 95.2] | 72.6 | 6.4 |
| 3 | 1.33 | 2.62 | 65.7 | 34.3 | 7.6 [5.2, 9.8] | 54.0 | 38.4 | 94.3 [91.9, 96.3] | 91.5 | 2.3 |
| 6 | 1.37 | 3.70 | 86.0 | 14.0 | 9.9 [6.9, 12.9] | 57.5 | 32.6 | 95.6 [93.5, 97.7] | 95.4 | 0.5 |

Inquiries are additional questions after the initial item. `stopped`/`exhausted` are pooled equally across stable/slip/mixed. Cap=1 has no pre-budget stop by construction (the stop check occurs after the budget check); its terminal diagnosis is still scored by `stable correct` / `slip false`, but `stable correct stop` is zero. At higher caps, `stable correct stop` counts only episodes that stop before the cap; budget-final correct diagnoses are in `stable correct`.

## Same-cap comparison (point estimates)

| cap | method | slip false | slip abstain | stable correct | stable abstain | stable inquiries | slip inquiries |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | fixed-k | 94.5 [88.0, 99.1] | 0.0 | 91.3 [85.8, 95.3] | 0.0 | 1.00 | 1.00 |
| 1 | SM | 2.5 [1.1, 4.2] | 97.5 | 72.6 [58.9, 84.4] | 26.9 | 1.00 | 1.00 |
| 1 | E-only | 2.5 [1.1, 4.2] | 97.5 | 72.6 [58.9, 84.4] | 26.9 | 1.00 | 1.00 |
| 1 | posterior-only | 29.0 [20.7, 38.2] | 71.0 | 76.1 [63.3, 87.1] | 20.7 | 0.95 | 0.95 |
| 2 | fixed-k | 72.6 [60.0, 83.8] | 0.0 | 96.8 [94.8, 98.4] | 0.0 | 2.00 | 2.00 |
| 2 | SM | 6.7 [4.3, 8.8] | 64.6 | 91.5 [86.7, 95.2] | 6.4 | 1.27 | 1.97 |
| 2 | E-only | 3.9 [1.9, 6.0] | 96.1 | 91.5 [86.7, 95.2] | 7.6 | 1.27 | 1.97 |
| 2 | posterior-only | 41.4 [30.6, 53.1] | 58.6 | 92.9 [88.8, 96.2] | 2.5 | 1.16 | 1.66 |
| 3 | fixed-k | 47.8 [35.1, 61.0] | 0.0 | 97.0 [95.0, 98.7] | 0.0 | 3.00 | 3.00 |
| 3 | SM | 7.6 [5.2, 9.8] | 38.4 | 94.3 [91.9, 96.3] | 2.3 | 1.33 | 2.62 |
| 3 | E-only | 3.9 [1.9, 6.0] | 96.1 | 94.7 [92.3, 96.7] | 4.4 | 1.34 | 2.94 |
| 3 | posterior-only | 49.7 [37.6, 63.3] | 50.3 | 94.9 [92.7, 97.0] | 0.5 | 1.19 | 2.25 |
| 6 | fixed-k | 45.7 [33.9, 58.6] | 0.0 | 98.9 [97.6, 99.8] | 0.0 | 6.00 | 6.00 |
| 6 | SM | 9.9 [6.9, 12.9] | 32.6 | 95.6 [93.5, 97.7] | 0.5 | 1.37 | 3.70 |
| 6 | E-only | 4.6 [2.4, 7.0] | 74.7 | 97.2 [95.2, 99.0] | 1.6 | 1.43 | 5.76 |
| 6 | posterior-only | 53.6 [40.5, 67.9] | 32.6 | 95.2 [92.9, 97.2] | 0.2 | 1.20 | 3.65 |

Fixed-k uses exactly k additional MaxEnt questions and then commits from the posterior (single/none, never abstain). SM uses the same selection but may stop earlier, return none, or abstain; its actual inquiries can be below the cap.

## Same-cap paired contrasts

| cap | contrast | slip false | stable correct | stable abstain | inquiries |
|---:|---|---:|---:|---:|---:|
| 1 | sm_b1 - fixed_k1 | -92.0 [-96.9, -85.5] | -18.6 [-30.8, -8.0] | +26.9 [+15.2, +40.3] | +0.0 [+0.0, +0.0] |
| 1 | e_b1 - sm_b1 | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] |
| 1 | posterior_b1 - e_b1 | +26.4 [+18.8, +35.1] | +3.4 [+0.3, +7.1] | -6.2 [-10.0, -3.0] | -0.0 [-0.1, -0.0] |
| 1 | sm_b1 - posterior_b1 | -26.4 [-35.1, -18.8] | -3.4 [-7.1, -0.3] | +6.2 [+3.0, +10.0] | +0.0 [+0.0, +0.1] |
| 2 | sm_b2 - fixed_k2 | -66.0 [-76.7, -54.0] | -5.3 [-9.2, -2.1] | +6.4 [+3.1, +10.9] | -0.0 [-0.0, -0.0] |
| 2 | e_b2 - sm_b2 | -2.8 [-4.4, -1.2] | +0.0 [+0.0, +0.0] | +1.1 [+0.3, +2.1] | +0.0 [+0.0, +0.0] |
| 2 | posterior_b2 - e_b2 | +37.5 [+27.7, +48.3] | +1.4 [+0.0, +4.0] | -5.1 [-8.1, -2.9] | -0.3 [-0.4, -0.2] |
| 2 | sm_b2 - posterior_b2 | -34.7 [-45.9, -24.8] | -1.4 [-4.0, +0.0] | +3.9 [+1.6, +6.9] | +0.3 [+0.2, +0.4] |
| 3 | sm_b3 - fixed_k3 | -40.2 [-52.1, -28.3] | -2.8 [-4.6, -0.9] | +2.3 [+1.0, +3.9] | -0.4 [-0.5, -0.3] |
| 3 | e_b3 - sm_b3 | -3.7 [-5.6, -1.9] | +0.5 [+0.0, +1.5] | +2.1 [+0.2, +3.9] | +0.3 [+0.2, +0.5] |
| 3 | posterior_b3 - e_b3 | +45.7 [+34.9, +58.4] | +0.2 [-0.5, +1.1] | -3.9 [-5.7, -2.4] | -0.7 [-0.9, -0.5] |
| 3 | sm_b3 - posterior_b3 | -42.1 [-54.6, -31.3] | -0.7 [-1.6, +0.0] | +1.8 [+0.5, +3.6] | +0.4 [+0.1, +0.6] |
| 6 | sm_b6 - fixed_k6 | -35.9 [-47.4, -25.1] | -3.2 [-5.3, -1.3] | +0.5 [+0.0, +1.2] | -2.3 [-2.7, -1.9] |
| 6 | e_b6 - sm_b6 | -5.3 [-7.9, -2.9] | +1.6 [+0.4, +3.0] | +1.1 [-0.2, +2.6] | +2.1 [+1.6, +2.5] |
| 6 | posterior_b6 - e_b6 | +49.0 [+37.3, +62.2] | -2.1 [-3.5, -0.7] | -1.4 [-2.7, -0.4] | -2.1 [-2.7, -1.6] |
| 6 | sm_b6 - posterior_b6 | -43.7 [-56.9, -32.3] | +0.5 [-0.4, +1.4] | +0.2 [-0.5, +1.1] | +0.1 [-0.7, +0.9] |

## Marginal change with more budget

| family | comparison | slip false | stable correct | slip inquiries |
|---|---|---:|---:|---:|
| sm | b1 -> b2 | -4.1 [-6.1, -2.2] | -18.9 [-31.4, -8.4] | -1.0 [-1.0, -1.0] |
| sm | b2 -> b3 | -0.9 [-1.8, -0.2] | -2.8 [-6.1, +0.0] | -0.6 [-0.8, -0.5] |
| sm | b3 -> b6 | -2.3 [-3.7, -1.0] | -1.4 [-2.7, -0.4] | -1.1 [-1.5, -0.7] |
| sm | b1 -> b6 | -7.4 [-10.0, -4.8] | -23.0 [-36.0, -11.9] | -2.7 [-3.1, -2.3] |
| e | b1 -> b2 | -1.4 [-2.8, -0.2] | -18.9 [-31.4, -8.4] | -1.0 [-1.0, -1.0] |
| e | b2 -> b3 | +0.0 [+0.0, +0.0] | -3.2 [-6.7, -0.5] | -1.0 [-1.0, -0.9] |
| e | b3 -> b6 | -0.7 [-1.5, +0.0] | -2.5 [-4.2, -1.1] | -2.8 [-2.9, -2.7] |
| e | b1 -> b6 | -2.1 [-3.7, -0.7] | -24.6 [-37.9, -13.1] | -4.8 [-4.9, -4.6] |
| posterior | b1 -> b2 | -12.4 [-20.3, -6.3] | -16.8 [-29.1, -7.0] | -0.7 [-0.8, -0.6] |
| posterior | b2 -> b3 | -8.3 [-15.0, -2.6] | -2.1 [-4.9, +0.0] | -0.6 [-0.7, -0.5] |
| posterior | b3 -> b6 | -3.9 [-8.2, -0.8] | -0.2 [-0.8, +0.0] | -1.4 [-1.8, -1.0] |
| posterior | b1 -> b6 | -24.6 [-35.3, -15.3] | -19.1 [-31.1, -8.6] | -2.7 [-3.2, -2.1] |

The comparison is earlier/smaller-budget minus later/larger-budget. For slip false, negative means the larger budget has higher error; positive means more budget reduces error. For stable correct, negative means the larger budget improves coverage.

## Selected cross-budget comparisons

| contrast | slip false | stable correct | stable abstain | stable inquiries | slip inquiries |
|---|---:|---:|---:|---:|---:|
| e_b2 - sm_b6 | -6.0 [-8.3, -3.9] | -4.1 [-7.8, -1.2] | +7.1 [+3.6, +11.6] | -0.1 [-0.2, -0.1] | -1.7 [-2.2, -1.3] |
| e_b3 - sm_b6 | -6.0 [-8.3, -3.9] | -0.9 [-1.9, -0.2] | +3.9 [+2.2, +5.8] | -0.0 [-0.1, -0.0] | -0.8 [-1.2, -0.3] |
| sm_b6 - fixed_k3 | -37.9 [-49.5, -26.2] | -1.4 [-3.1, +0.4] | +0.5 [+0.0, +1.2] | -1.6 [-1.8, -1.5] | +0.7 [+0.3, +1.1] |

`e_b3 - sm_b6` asks whether a 3-question E-gated single-diagnosis policy can match or beat the full 6-question SM; `sm_b6 - fixed_k3` reproduces the original v5 SM-vs-fixed3 comparison (fixed3 uses MaxEnt and 3 additional questions).

## E1: strict 2x2 decomposition of SM vs fixed3

MaxEnt selection, prior, hypothesis space, eps and seeds are held fixed. A = `fixed_k3`: 3 inquiries, then commit from the posterior (single/none, never abstain). B = `fixed_k3_gate`: the same 3 inquiries, then the full SM stability gate applied once; gate failure abstains, gate none-rules still return none. C = `sm_b6`: full SM, same gate with adaptive stopping under a cap of 6. B-A isolates the decision rule at a fixed budget; C-B isolates adaptive stopping on top of the gate (note C's cap is 6, not 3); C-A reproduces the mainline contrast. `sm_b3 - fixed_k3_gate` is the same-cap adaptive-stopping contrast.

| arm | slip false | slip none | slip abstain | stable correct | stable abstain | stable inq | slip inq |
|---|---:|---:|---:|---:|---:|---:|---:|
| A fixed_k3 | 47.8 [35.1, 61.0] | 52.2 | 0.0 | 97.0 [95.0, 98.7] | 0.0 | 3.00 | 3.00 |
| B fixed_k3_gate | 4.1 [2.4, 5.8] | 52.4 | 43.4 | 87.6 [84.8, 90.2] | 6.4 | 3.00 | 3.00 |
| C' sm_b3 (adaptive, cap 3) | 7.6 [5.2, 9.8] | 54.0 | 38.4 | 94.3 [91.9, 96.3] | 2.3 | 1.33 | 2.62 |
| C sm_b6 (adaptive, cap 6) | 9.9 [6.9, 12.9] | 57.5 | 32.6 | 95.6 [93.5, 97.7] | 0.5 | 1.37 | 3.70 |

### E1 paired contrasts

| contrast | slip false | stable correct | stable abstain | stable inq | slip inq |
|---|---:|---:|---:|---:|---:|
| fixed_k3_gate - fixed_k3 | -43.7 [-56.2, -31.3] | -9.4 [-12.0, -6.8] | +6.4 [+4.4, +8.8] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] |
| sm_b6 - fixed_k3_gate | +5.7 [+3.3, +8.6] | +8.0 [+5.8, +10.2] | -6.0 [-8.3, -3.9] | -1.6 [-1.8, -1.5] | +0.7 [+0.3, +1.1] |
| sm_b6 - fixed_k3 | -37.9 [-49.5, -26.2] | -1.4 [-3.1, +0.4] | +0.5 [+0.0, +1.2] | -1.6 [-1.8, -1.5] | +0.7 [+0.3, +1.1] |
| sm_b3 - fixed_k3_gate | +3.4 [+1.9, +5.3] | +6.7 [+4.6, +8.8] | -4.1 [-6.5, -2.0] | -1.7 [-1.8, -1.5] | -0.4 [-0.5, -0.3] |

## SM slip false remediation by category (point estimates)

| category | cap 1 | cap 3 | cap 6 |
|---|---:|---:|---:|
| subtraction | 0.0 | 6.7 | 7.8 |
| fractions | 2.2 | 5.6 | 5.6 |
| decimals | 5.0 | 10.0 | 15.0 |
| negative_numbers | 2.7 | 8.0 | 9.3 |
| order_of_operations | 5.0 | 13.3 | 18.3 |
| percentages | 1.7 | 3.3 | 6.7 |

## Reproduction check

| check | result |
|---|---|
| SM at cap=6 vs frozen v5 `stability_mixed/maxent` | 0 mismatches / 1305 episodes |
| max absolute aggregate difference | 0.000e+00 |

## Scope

- Post-hoc budget curve on the frozen v5 protocol-valid 87-case test set; no thresholds were tuned on these results.
- All arms use the LLM category prior and the same MaxEnt selection; this is not a prior ablation.
- `stable correct stop` is not comparable across caps: cap=1 cannot stop before budget, and budget-final correct diagnoses are counted in `stable correct` but not in `stable correct stop`.
- Fixed-k is a budget-matched reference that always commits after k questions; SM may stop earlier or abstain. `fixed_k3_gate` (E1 arm B) resolves this confound by applying the SM gate once after exactly 3 questions.
