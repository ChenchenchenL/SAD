# Selection-strategy comparison

Unified per block: frozen v5 category prior, same hypothesis space, same outcomes (common random numbers), eps=0.05, 5 seeds. Adaptive block = full SM stopping with max_obs=7 and pair-augmented space; fixed block = frozen Fixed-3 convention (no pairs, exactly 3 inquiries, posterior commit, never abstain).

## Adaptive full SM (max_obs=7)

| strategy | stable correct | stable correct stop | stable false single | stable pair/mixed | slip false remediation | slip none | slip abstain | stable inquiries | slip inquiries | stable J5 | slip J5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| sm_maxent | 92.4 [89.4, 95.0] | 92.4 | 0.9 | 0.9 | 10.8 [8.1, 13.6] | 51.7 | 37.5 | 1.75 | 4.18 | 2.80 | 5.72 |
| sm_ig | 93.3 [90.3, 95.7] | 93.1 | 0.9 | 0.9 | 9.2 [6.7, 11.9] | 58.4 | 32.4 | 1.67 | 3.89 | 2.72 | 5.35 |
| sm_random | 72.2 [66.7, 77.8] | 65.3 | 0.5 | 1.4 | 10.6 [7.2, 14.3] | 32.4 | 57.0 | 3.54 | 4.97 | 4.56 | 6.49 |
| sm_fixed_order | 53.3 [38.7, 67.0] | 49.4 | 0.2 | 2.5 | 6.9 [3.6, 10.5] | 27.4 | 65.7 | 4.04 | 4.95 | 5.05 | 6.30 |

## Fixed budget k=3 (Fixed-3 convention)

| strategy | stable correct | stable false single | stable pair/mixed | slip false remediation | slip none | stable J5 | slip J5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| k3_maxent | 94.7 [91.9, 96.9] | 4.4 [2.2, 7.2] | 0.0 | 71.5 [61.8, 81.0] | 28.5 | 4.22 | 7.57 |
| k3_ig | 94.3 [91.2, 96.7] | 4.1 [1.9, 6.9] | 0.0 | 69.7 [59.3, 79.8] | 30.3 | 4.21 | 7.48 |
| k3_random | 86.4 [81.6, 91.0] | 13.3 [9.0, 18.1] | 0.0 | 93.8 [90.4, 96.8] | 6.2 | 4.67 | 8.69 |
| k3_fixed_order | 80.7 [70.4, 89.5] | 18.4 [9.7, 28.6] | 0.0 | 89.9 [82.2, 96.1] | 10.1 | 4.92 | 8.49 |
| k3_random_legacy | 83.7 [77.3, 89.2] | 14.9 [9.3, 21.3] | 0.0 | 91.5 [87.2, 95.3] | 8.5 | 4.75 | 8.57 |

Rates are percentages; bracketed intervals are 95% template-family cluster bootstrap intervals (2000 draws, with replacement and multiplicity). `k3_random_legacy` is the historical reseeded-random implementation, kept only to reproduce the frozen numbers and measure the correction; it is not a standard random baseline.

## Paired contrasts (same case and seed)

| contrast | stable correct | slip false | slip none | slip abstain | stable inquiries | slip inquiries | slip J5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| sm_ig − sm_maxent | +0.9 [+0.0, +2.1] | -1.6 [-3.7, +0.3] | +6.7 [+2.1, +11.6] | -5.1 [-9.8, -0.5] | -0.1 [-0.2, -0.0] | -0.3 [-0.5, -0.1] | -0.4 [-0.6, -0.2] |
| sm_random − sm_maxent | -20.2 [-25.4, -14.9] | -0.2 [-3.7, +3.6] | -19.3 [-31.6, -8.6] | +19.5 [+8.5, +31.7] | +1.8 [+1.5, +2.1] | +0.8 [+0.3, +1.3] | +0.8 [+0.3, +1.3] |
| sm_fixed_order − sm_maxent | -39.1 [-53.0, -25.8] | -3.9 [-7.6, -0.2] | -24.4 [-40.9, -7.7] | +28.3 [+11.3, +45.2] | +2.3 [+1.7, +2.9] | +0.8 [+0.2, +1.4] | +0.6 [-0.0, +1.2] |
| sm_ig − sm_random | +21.1 [+16.0, +26.3] | -1.4 [-5.0, +2.2] | +26.0 [+15.5, +37.4] | -24.6 [-35.8, -14.7] | -1.9 [-2.2, -1.6] | -1.1 [-1.5, -0.7] | -1.1 [-1.6, -0.8] |
| k3_ig − k3_maxent | -0.5 [-1.6, +0.5] | -1.8 [-6.6, +0.6] | +1.8 [-0.6, +6.6] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] | -0.1 [-0.3, +0.0] |
| k3_random − k3_maxent | -8.3 [-12.9, -3.9] | +22.3 [+14.4, +30.7] | -22.3 [-30.7, -14.4] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] | +1.1 [+0.7, +1.5] |
| k3_fixed_order − k3_maxent | -14.0 [-24.0, -5.5] | +18.4 [+10.4, +27.4] | -18.4 [-27.4, -10.4] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] | +0.9 [+0.5, +1.4] |
| k3_random_legacy − k3_maxent | -11.0 [-17.1, -5.5] | +20.0 [+12.3, +28.0] | -20.0 [-28.0, -12.3] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] | +1.0 [+0.6, +1.4] |
| k3_ig − k3_random | +7.8 [+3.4, +12.5] | -24.1 [-33.6, -15.6] | +24.1 [+15.6, +33.6] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] | -1.2 [-1.7, -0.8] |

Positive stable-correct and negative slip-false differences favor the first strategy.

## Selection agreement

### First selected item (adaptive block; all strategies share the same initial state)

| pair | student | n | agreement |
|---|---|---:|---:|
| sm_maxent vs sm_ig | stable | 435 | 93.1% |
| sm_maxent vs sm_random | stable | 435 | 7.1% |
| sm_maxent vs sm_fixed_order | stable | 435 | 20.7% |
| sm_ig vs sm_random | stable | 435 | 7.1% |
| sm_ig vs sm_fixed_order | stable | 435 | 19.5% |
| sm_random vs sm_fixed_order | stable | 435 | 6.0% |
| sm_maxent vs sm_ig | slip | 435 | 93.1% |
| sm_maxent vs sm_random | slip | 435 | 8.0% |
| sm_maxent vs sm_fixed_order | slip | 435 | 20.7% |
| sm_ig vs sm_random | slip | 435 | 8.3% |
| sm_ig vs sm_fixed_order | slip | 435 | 19.5% |
| sm_random vs sm_fixed_order | slip | 435 | 5.7% |

### Full 3-item sequence identity (fixed k=3)

| pair | student | n | identical sequences |
|---|---|---:|---:|
| k3_maxent vs k3_ig | stable | 435 | 72.4% |
| k3_maxent vs k3_random | stable | 435 | 0.0% |
| k3_maxent vs k3_fixed_order | stable | 435 | 8.0% |
| k3_maxent vs k3_random_legacy | stable | 435 | 1.1% |
| k3_ig vs k3_random | stable | 435 | 0.2% |
| k3_ig vs k3_fixed_order | stable | 435 | 7.1% |
| k3_ig vs k3_random_legacy | stable | 435 | 1.4% |
| k3_random vs k3_fixed_order | stable | 435 | 0.0% |
| k3_random vs k3_random_legacy | stable | 435 | 0.0% |
| k3_fixed_order vs k3_random_legacy | stable | 435 | 7.4% |
| k3_maxent vs k3_ig | slip | 435 | 73.8% |
| k3_maxent vs k3_random | slip | 435 | 0.0% |
| k3_maxent vs k3_fixed_order | slip | 435 | 4.1% |
| k3_maxent vs k3_random_legacy | slip | 435 | 0.7% |
| k3_ig vs k3_random | slip | 435 | 0.0% |
| k3_ig vs k3_fixed_order | slip | 435 | 3.0% |
| k3_ig vs k3_random_legacy | slip | 435 | 0.5% |
| k3_random vs k3_fixed_order | slip | 435 | 0.5% |
| k3_random vs k3_random_legacy | slip | 435 | 0.2% |
| k3_fixed_order vs k3_random_legacy | slip | 435 | 6.0% |

## Reproduction checks against frozen v5 episodes

| check | mismatches |
|---|---|
| sm_maxent vs frozen stability_mixed/maxent | 0 / 870 |
| k3_maxent vs frozen maxent_k3 | 0 / 870 |
| k3_fixed_order vs frozen fixed_k3 | 0 / 870 |
| k3_random_legacy vs frozen random_k3 | 0 / 870 |

The reference arms use the same engine code and frozen inputs as the v5 pipeline; identical episodes prove the harness before any new strategy is compared.

## Slip false remediation by category (point estimates)

| category | sm_maxent | sm_ig | sm_random | sm_fixed_order | k3_maxent | k3_ig | k3_random | k3_fixed_order |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| subtraction | 5.6 | 4.4 | 7.8 | 4.4 | 62.2 | 62.2 | 86.7 | 73.3 |
| fractions | 10.0 | 10.0 | 10.0 | 10.0 | 42.2 | 42.2 | 96.7 | 93.3 |
| decimals | 11.7 | 10.0 | 6.7 | 1.7 | 100.0 | 100.0 | 100.0 | 100.0 |
| negative_numbers | 13.3 | 13.3 | 16.0 | 10.7 | 78.7 | 66.7 | 92.0 | 100.0 |
| order_of_operations | 15.0 | 15.0 | 11.7 | 10.0 | 85.0 | 85.0 | 96.7 | 93.3 |
| percentages | 11.7 | 3.3 | 11.7 | 3.3 | 78.3 | 80.0 | 93.3 | 83.3 |

Category cells are exploratory (12-18 cases per category).
