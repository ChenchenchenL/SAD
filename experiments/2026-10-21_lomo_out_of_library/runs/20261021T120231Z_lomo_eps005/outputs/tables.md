# LOMO out-of-library student experiment

eps=0.05; removed-rule students (stable_ool: deterministic; slip_ool: eps random errors on top of the removed rule); MaxEnt selection; max_obs=7; 5 seeds; frozen category-conditioned cached prior with the removed rule dropped from the weights. Every single/pair/mixed terminal is a false commitment because the true rule is not in the hypothesis space.

## Main table

| arm | student | false commit (any) | single commit | pair/mixed commit | none | abstain | inquiries | J5 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| posterior_only | stable_ool | 44.8 [30.1, 62.7] | 44.8 | 0.0 | 48.3 | 6.9 | 2.20 | 5.44 |
| posterior_only | slip_ool | 47.6 [33.1, 65.1] | 47.6 | 0.0 | 45.3 | 7.1 | 2.18 | 5.56 |
| posterior_plus_E | stable_ool | 6.9 [1.1, 15.6] | 6.9 | 0.0 | 59.8 | 33.3 | 3.85 | 5.20 |
| posterior_plus_E | slip_ool | 7.1 [1.2, 15.9] | 7.1 | 0.0 | 56.1 | 36.8 | 3.96 | 5.32 |
| stability_mixed_reference | stable_ool | 6.9 [1.1, 15.6] | 6.9 | 0.0 | 66.7 | 26.4 | 3.39 | 4.74 |
| stability_mixed_reference | slip_ool | 9.7 [3.4, 18.5] | 7.1 | 2.5 | 63.9 | 26.4 | 3.43 | 4.91 |

Rates are percentages of episodes; bracketed intervals are 95% template-family cluster bootstrap intervals (2000 draws, with replacement and multiplicity). false commit = any library commitment (single, pair, or mixed terminal). none = explicit no-in-library-stable-misconception output; abstain = insufficient evidence.

## Paired contrasts (same case and seed)

| contrast | student | false commit | none | abstain | inquiries | J5 |
|---|---|---:|---:|---:|---:|---:|
| posterior_plus_E - posterior_only | stable_ool | -37.9 [-54.9, -23.5] | +11.5 [+2.4, +23.3] | +26.4 [+14.3, +42.1] | +1.7 [+1.0, +2.4] | -0.2 [-0.5, +0.0] |
| posterior_plus_E - posterior_only | slip_ool | -40.5 [-56.9, -26.5] | +10.8 [+3.9, +19.2] | +29.7 [+17.3, +45.4] | +1.8 [+1.1, +2.6] | -0.2 [-0.5, +0.0] |
| stability_mixed_reference - posterior_only | stable_ool | -37.9 [-54.9, -23.5] | +18.4 [+7.2, +31.3] | +19.5 [+4.6, +37.0] | +1.2 [+0.4, +2.1] | -0.7 [-1.1, -0.3] |
| stability_mixed_reference - posterior_only | slip_ool | -37.9 [-53.8, -24.4] | +18.6 [+9.0, +29.3] | +19.3 [+5.2, +35.9] | +1.2 [+0.5, +2.1] | -0.7 [-1.0, -0.3] |
| stability_mixed_reference - posterior_plus_E | stable_ool | +0.0 [+0.0, +0.0] | +6.9 [+1.1, +15.1] | -6.9 [-15.1, -1.1] | -0.5 [-0.8, -0.2] | -0.5 [-0.8, -0.2] |
| stability_mixed_reference - posterior_plus_E | slip_ool | +2.5 [+0.8, +4.6] | +7.8 [+1.9, +15.2] | -10.3 [-17.7, -4.4] | -0.5 [-0.8, -0.3] | -0.4 [-0.7, -0.2] |

Negative false-commit differences mean the first arm is safer on out-of-library students.

## Gate counterfactual at single stops

Gate states at the terminal step of episodes whose terminal is a single commitment. `E pass` = at least two observed consistent wrong answers matching the committed rule; `LR pass` = slip likelihood ratio >= 10; `pair guard pass` = committed single beats the top pair.

| student | arm | n single stops | E pass | LR pass | pair guard pass | any gate fail |
|---|---|---:|---:|---:|---:|---:|
| stable_ool | posterior_only | 195 | 12.8 | 12.8 | 100.0 | 87.2 |
| slip_ool | posterior_only | 207 | 11.6 | 23.2 | 99.0 | 88.4 |

Minimum log slip-LR at a posterior_only single stop: 0.0

## Misdiagnosis targets (stable_ool, single terminals)

Which library rule receives the false single diagnosis.

| arm | top blamed rules (count) |
|---|---|
| posterior_only | decimals.whole_number_thinking (60), order_of_operations.pemdas_strictly_sequential (35), order_of_operations.strict_left_to_right (15), percentages.reverse_percentage_error (15), percentages.add_percentages_directly (15), fractions.denominator_comparison_error (10) |
| posterior_plus_E | order_of_operations.strict_left_to_right (15), order_of_operations.ignore_parentheses (15) |
| stability_mixed_reference | order_of_operations.strict_left_to_right (15), order_of_operations.ignore_parentheses (15) |

## Removed-rule overlap vs false commitment (stable_ool)

Labels bucketed by the maximum number of triggering items shared with any remaining rule in the category bank.

| arm | max-overlap bucket | n labels | n episodes | false commit | none | abstain |
|---|---|---:|---:|---:|---:|---:|
| posterior_only | stable_ool | 0 | 18 | 270 | 55.6 | 35.2 | 9.3 |
| posterior_only | stable_ool | 1 | 4 | 60 | 25.0 | 66.7 | 8.3 |
| posterior_only | stable_ool | >=2 | 7 | 105 | 28.6 | 71.4 | 0.0 |
| posterior_only | slip_ool | 0 | 18 | 270 | 57.8 | 32.2 | 10.0 |
| posterior_only | slip_ool | 1 | 4 | 60 | 30.0 | 63.3 | 6.7 |
| posterior_only | slip_ool | >=2 | 7 | 105 | 31.4 | 68.6 | 0.0 |
| posterior_plus_E | stable_ool | 0 | 18 | 270 | 0.0 | 53.7 | 46.3 |
| posterior_plus_E | stable_ool | 1 | 4 | 60 | 0.0 | 66.7 | 33.3 |
| posterior_plus_E | stable_ool | >=2 | 7 | 105 | 28.6 | 71.4 | 0.0 |
| posterior_plus_E | slip_ool | 0 | 18 | 270 | 0.4 | 48.9 | 50.7 |
| posterior_plus_E | slip_ool | 1 | 4 | 60 | 0.0 | 63.3 | 36.7 |
| posterior_plus_E | slip_ool | >=2 | 7 | 105 | 28.6 | 70.5 | 1.0 |
| stability_mixed_reference | stable_ool | 0 | 18 | 270 | 0.0 | 63.0 | 37.0 |
| stability_mixed_reference | stable_ool | 1 | 4 | 60 | 0.0 | 75.0 | 25.0 |
| stability_mixed_reference | stable_ool | >=2 | 7 | 105 | 28.6 | 71.4 | 0.0 |
| stability_mixed_reference | slip_ool | 0 | 18 | 270 | 4.1 | 58.9 | 37.0 |
| stability_mixed_reference | slip_ool | 1 | 4 | 60 | 0.0 | 75.0 | 25.0 |
| stability_mixed_reference | slip_ool | >=2 | 7 | 105 | 29.5 | 70.5 | 0.0 |

## False commitment by category (point estimates, stable_ool)

| category | posterior_only | posterior_plus_E | stability_mixed_reference |
|---|---:|---:|---:|
| subtraction | 0.0 | 0.0 | 0.0 |
| fractions | 27.8 | 0.0 | 0.0 |
| decimals | 100.0 | 0.0 | 0.0 |
| negative_numbers | 13.3 | 0.0 | 0.0 |
| order_of_operations | 100.0 | 50.0 | 50.0 |
| percentages | 66.7 | 0.0 | 0.0 |

Category cells are exploratory (12-18 cases per category).

## Scope

- Post-hoc experiment on the frozen v5 protocol-valid 87-case test set; no thresholds were tuned on these results.
- The LLM prior cache was computed while the removed rule was still in the prompt library; the rule is dropped from the weights and the remaining ranks are kept, which slightly flattens the prior relative to a true out-of-library call.
- Every commitment is false by construction, so correct-diagnosis rates are undefined here; the question is how the system fails.
