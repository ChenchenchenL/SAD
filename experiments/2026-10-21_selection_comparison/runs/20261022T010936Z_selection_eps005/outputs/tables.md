# Selection-strategy comparison

Unified per block: frozen v5 category prior, same hypothesis space, same outcomes (common random numbers), eps=0.05, 5 seeds. Adaptive block = full SM stopping with max_obs=7 and pair-augmented space; fixed block = frozen Fixed-3 convention (no pairs, exactly 3 inquiries, posterior commit, never abstain).

## Adaptive full SM (max_obs=7)

| strategy | stable correct | stable correct stop | stable false single | stable pair/mixed | slip false remediation | slip none | slip abstain | stable inquiries | slip inquiries | stable J5 | slip J5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| sm_maxent | 95.6 [93.5, 97.7] | 95.4 | 0.9 | 1.6 | 9.9 [6.9, 12.9] | 57.5 | 32.6 | 1.37 | 3.70 | 2.42 | 5.20 |
| sm_ig | 95.9 [93.6, 97.8] | 95.6 | 0.5 | 1.6 | 11.0 [8.2, 13.9] | 57.9 | 31.0 | 1.35 | 3.66 | 2.37 | 5.22 |
| sm_random | 77.2 [72.5, 81.8] | 71.3 | 0.5 | 2.3 | 10.6 [7.4, 13.8] | 37.7 | 51.7 | 3.24 | 4.87 | 4.26 | 6.40 |
| sm_fixed_order | 57.7 [42.1, 72.0] | 54.3 | 0.2 | 2.8 | 9.2 [5.7, 13.2] | 22.8 | 68.0 | 3.89 | 5.02 | 4.90 | 6.48 |

## Fixed budget k=3 (Fixed-3 convention)

| strategy | stable correct | stable false single | stable pair/mixed | slip false remediation | slip none | stable J5 | slip J5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| k3_maxent | 97.0 [94.9, 98.7] | 1.6 [0.4, 3.5] | 0.0 | 47.8 [34.9, 61.0] | 52.2 | 4.08 | 6.39 |
| k3_ig | 97.2 [95.2, 98.9] | 1.6 [0.4, 3.5] | 0.0 | 47.6 [34.7, 60.9] | 52.4 | 4.08 | 6.38 |
| k3_random | 89.7 [85.1, 93.6] | 9.7 [5.6, 14.3] | 0.0 | 85.7 [80.3, 90.5] | 14.3 | 4.48 | 8.29 |
| k3_fixed_order | 82.5 [72.1, 91.1] | 17.0 [8.3, 27.5] | 0.0 | 89.4 [81.5, 95.8] | 10.6 | 4.85 | 8.47 |
| k3_random_legacy | 86.0 [79.2, 91.6] | 12.6 [7.2, 19.3] | 0.0 | 88.7 [83.7, 93.0] | 11.3 | 4.63 | 8.44 |

Rates are percentages; bracketed intervals are 95% template-family cluster bootstrap intervals (2000 draws, with replacement and multiplicity). `k3_random_legacy` is the historical reseeded-random implementation, kept only to reproduce the frozen numbers and measure the correction; it is not a standard random baseline.

## Paired contrasts (same case and seed)

| contrast | stable correct | slip false | slip none | slip abstain | stable inquiries | slip inquiries | slip J5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| sm_ig − sm_maxent | +0.2 [-0.5, +1.0] | +1.1 [-0.5, +2.8] | +0.5 [-0.9, +1.6] | -1.6 [-3.1, -0.2] | -0.0 [-0.1, +0.0] | -0.0 [-0.1, +0.0] | +0.0 [-0.1, +0.1] |
| sm_random − sm_maxent | -18.4 [-23.8, -13.3] | +0.7 [-3.6, +4.9] | -19.8 [-30.9, -9.2] | +19.1 [+10.1, +28.5] | +1.9 [+1.5, +2.2] | +1.2 [+0.8, +1.6] | +1.2 [+0.7, +1.7] |
| sm_fixed_order − sm_maxent | -37.9 [-53.7, -23.3] | -0.7 [-5.5, +3.8] | -34.7 [-54.2, -14.9] | +35.4 [+17.3, +53.3] | +2.5 [+1.9, +3.1] | +1.3 [+0.7, +1.9] | +1.3 [+0.6, +2.0] |
| sm_ig − sm_random | +18.6 [+13.6, +23.7] | +0.5 [-3.8, +4.4] | +20.2 [+10.0, +31.0] | -20.7 [-30.1, -11.8] | -1.9 [-2.2, -1.6] | -1.2 [-1.6, -0.8] | -1.2 [-1.7, -0.7] |
| k3_ig − k3_maxent | +0.2 [+0.0, +0.8] | -0.2 [-0.8, +0.0] | +0.2 [+0.0, +0.8] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] | -0.0 [-0.0, +0.0] |
| k3_random − k3_maxent | -7.4 [-11.7, -3.4] | +37.9 [+27.3, +48.2] | -37.9 [-48.2, -27.3] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] | +1.9 [+1.4, +2.4] |
| k3_fixed_order − k3_maxent | -14.5 [-24.4, -6.2] | +41.6 [+27.3, +55.7] | -41.6 [-55.7, -27.3] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] | +2.1 [+1.4, +2.8] |
| k3_random_legacy − k3_maxent | -11.0 [-17.6, -5.5] | +40.9 [+28.8, +52.6] | -40.9 [-52.6, -28.8] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] | +2.0 [+1.4, +2.6] |
| k3_ig − k3_random | +7.6 [+3.8, +11.7] | -38.2 [-48.4, -27.5] | +38.2 [+27.5, +48.4] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] | -1.9 [-2.4, -1.4] |

Positive stable-correct and negative slip-false differences favor the first strategy.

## Selection agreement

### First selected item (adaptive block; all strategies share the same initial state)

| pair | student | n | agreement |
|---|---|---:|---:|
| sm_maxent vs sm_ig | stable | 435 | 89.7% |
| sm_maxent vs sm_random | stable | 435 | 7.8% |
| sm_maxent vs sm_fixed_order | stable | 435 | 20.7% |
| sm_ig vs sm_random | stable | 435 | 7.1% |
| sm_ig vs sm_fixed_order | stable | 435 | 23.0% |
| sm_random vs sm_fixed_order | stable | 435 | 6.0% |
| sm_maxent vs sm_ig | slip | 435 | 89.7% |
| sm_maxent vs sm_random | slip | 435 | 7.8% |
| sm_maxent vs sm_fixed_order | slip | 435 | 20.7% |
| sm_ig vs sm_random | slip | 435 | 7.8% |
| sm_ig vs sm_fixed_order | slip | 435 | 23.0% |
| sm_random vs sm_fixed_order | slip | 435 | 5.7% |

### Full 3-item sequence identity (fixed k=3)

| pair | student | n | identical sequences |
|---|---|---:|---:|
| k3_maxent vs k3_ig | stable | 435 | 76.1% |
| k3_maxent vs k3_random | stable | 435 | 0.2% |
| k3_maxent vs k3_fixed_order | stable | 435 | 8.5% |
| k3_maxent vs k3_random_legacy | stable | 435 | 0.9% |
| k3_ig vs k3_random | stable | 435 | 0.0% |
| k3_ig vs k3_fixed_order | stable | 435 | 5.7% |
| k3_ig vs k3_random_legacy | stable | 435 | 0.5% |
| k3_random vs k3_fixed_order | stable | 435 | 0.0% |
| k3_random vs k3_random_legacy | stable | 435 | 0.0% |
| k3_fixed_order vs k3_random_legacy | stable | 435 | 7.4% |
| k3_maxent vs k3_ig | slip | 435 | 85.1% |
| k3_maxent vs k3_random | slip | 435 | 0.0% |
| k3_maxent vs k3_fixed_order | slip | 435 | 0.7% |
| k3_maxent vs k3_random_legacy | slip | 435 | 0.2% |
| k3_ig vs k3_random | slip | 435 | 0.0% |
| k3_ig vs k3_fixed_order | slip | 435 | 0.5% |
| k3_ig vs k3_random_legacy | slip | 435 | 0.2% |
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
| subtraction | 7.8 | 8.9 | 5.6 | 6.7 | 62.2 | 62.2 | 86.7 | 72.2 |
| fractions | 5.6 | 7.8 | 13.3 | 13.3 | 27.8 | 26.7 | 83.3 | 93.3 |
| decimals | 15.0 | 15.0 | 3.3 | 3.3 | 100.0 | 100.0 | 100.0 | 100.0 |
| negative_numbers | 9.3 | 13.3 | 16.0 | 16.0 | 14.7 | 14.7 | 84.0 | 100.0 |
| order_of_operations | 18.3 | 16.7 | 11.7 | 5.0 | 83.3 | 83.3 | 93.3 | 91.7 |
| percentages | 6.7 | 6.7 | 13.3 | 8.3 | 10.0 | 10.0 | 68.3 | 83.3 |

Category cells are exploratory (12-18 cases per category).
