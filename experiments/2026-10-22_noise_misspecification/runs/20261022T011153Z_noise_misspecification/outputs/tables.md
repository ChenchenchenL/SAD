# Noise misspecification and bursty slips

Diagnostician likelihood/gates always assume eps=0.05. The simulated student's true noise changes across conditions. `burst_0.20_r3/r6` use a two-state inattention chain with marginal lapse rate 0.20 and mean lapse run length 3/6, so they are comparable to `iid_0.20`: only the temporal correlation of wrong answers changes. All arms share the category prior, pair-augmented hypothesis space, MaxEnt selection, 5 seeds and caps (SM/E-only: 6; fixed-k/gate: 3).

## SM across student-noise conditions

| condition | slip false | slip abstain | slip none | stable correct | stable abstain | stable inq | slip inq |
|---|---:|---:|---:|---:|---:|---:|---:|
| iid_0.01 | 1.6 [0.6, 2.9] | 36.1 | 62.3 | 99.3 [98.2, 100.0] | 0.0 | 1.30 | 3.81 |
| iid_0.05 | 9.9 [6.9, 12.9] | 32.6 | 57.5 | 95.6 [93.5, 97.7] | 0.5 | 1.37 | 3.70 |
| iid_0.10 | 19.1 [14.9, 23.7] | 27.8 | 53.1 | 90.1 [87.1, 92.6] | 0.7 | 1.45 | 3.55 |
| iid_0.20 | 34.9 [29.9, 40.2] | 22.1 | 43.0 | 78.4 [73.9, 82.2] | 1.4 | 1.73 | 3.31 |
| burst_0.20_r3 | 28.5 [24.3, 32.9] | 23.2 | 48.3 | 77.2 [73.8, 80.4] | 1.8 | 1.78 | 3.39 |
| burst_0.20_r6 | 23.4 [19.5, 27.9] | 26.0 | 50.6 | 82.8 [79.8, 86.0] | 2.1 | 1.72 | 3.51 |

## Arm comparison within each condition (point estimates)

| condition | method | slip false | stable correct | stable abstain | stable inq | slip inq |
|---|---|---:|---:|---:|---:|---:|
| iid_0.01 | SM | 1.6 [0.6, 2.9] | 99.3 [98.2, 100.0] | 0.0 | 1.30 | 3.81 |
| iid_0.01 | fixed3 | 42.1 [27.9, 56.7] | 100.0 [100.0, 100.0] | 0.0 | 3.00 | 3.00 |
| iid_0.01 | fixed3+gate | 0.5 [0.0, 1.2] | 97.7 [96.0, 99.1] | 0.9 | 3.00 | 3.00 |
| iid_0.01 | E-only | 0.9 [0.2, 1.9] | 99.8 [99.3, 100.0] | 0.0 | 1.30 | 5.89 |
| iid_0.05 | SM | 9.9 [6.9, 12.9] | 95.6 [93.5, 97.7] | 0.5 | 1.37 | 3.70 |
| iid_0.05 | fixed3 | 47.8 [35.1, 61.0] | 97.0 [95.0, 98.7] | 0.0 | 3.00 | 3.00 |
| iid_0.05 | fixed3+gate | 4.1 [2.4, 5.8] | 87.6 [84.8, 90.2] | 6.4 | 3.00 | 3.00 |
| iid_0.05 | E-only | 4.6 [2.4, 7.0] | 97.2 [95.2, 99.0] | 1.6 | 1.43 | 5.76 |
| iid_0.10 | SM | 19.1 [14.9, 23.7] | 90.1 [87.1, 92.6] | 0.7 | 1.45 | 3.55 |
| iid_0.10 | fixed3 | 53.1 [41.4, 65.1] | 93.3 [90.0, 95.9] | 0.0 | 3.00 | 3.00 |
| iid_0.10 | fixed3+gate | 9.7 [6.7, 12.9] | 76.1 [72.4, 79.5] | 11.0 | 3.00 | 3.00 |
| iid_0.10 | E-only | 9.9 [6.3, 14.1] | 92.9 [89.8, 95.4] | 5.3 | 1.66 | 5.54 |
| iid_0.20 | SM | 34.9 [29.9, 40.2] | 78.4 [73.9, 82.2] | 1.4 | 1.73 | 3.31 |
| iid_0.20 | fixed3 | 61.6 [52.8, 70.5] | 83.7 [79.7, 87.1] | 0.0 | 3.00 | 3.00 |
| iid_0.20 | fixed3+gate | 18.2 [14.3, 22.1] | 52.0 [47.2, 56.8] | 27.6 | 3.00 | 3.00 |
| iid_0.20 | E-only | 22.8 [17.0, 29.1] | 83.7 [79.1, 87.6] | 12.2 | 2.18 | 5.07 |
| burst_0.20_r3 | SM | 28.5 [24.3, 32.9] | 77.2 [73.8, 80.4] | 1.8 | 1.78 | 3.39 |
| burst_0.20_r3 | fixed3 | 56.6 [45.6, 67.7] | 77.5 [73.2, 81.7] | 0.0 | 3.00 | 3.00 |
| burst_0.20_r3 | fixed3+gate | 15.4 [12.0, 19.3] | 65.5 [62.1, 68.5] | 20.0 | 3.00 | 3.00 |
| burst_0.20_r3 | E-only | 20.7 [15.7, 26.9] | 78.9 [75.2, 82.1] | 10.8 | 2.09 | 5.15 |
| burst_0.20_r6 | SM | 23.4 [19.5, 27.9] | 82.8 [79.8, 86.0] | 2.1 | 1.72 | 3.51 |
| burst_0.20_r6 | fixed3 | 53.1 [41.9, 65.1] | 80.5 [77.5, 83.6] | 0.0 | 3.00 | 3.00 |
| burst_0.20_r6 | fixed3+gate | 14.5 [10.9, 18.3] | 74.9 [71.3, 78.9] | 15.2 | 3.00 | 3.00 |
| burst_0.20_r6 | E-only | 17.7 [13.9, 22.0] | 83.7 [80.9, 86.7] | 6.4 | 1.88 | 5.26 |

## SM - fixed3 within each condition

| condition | slip false | stable correct | stable inq | slip inq |
|---|---:|---:|---:|---:|
| iid_0.01 | -40.5 [-54.5, -26.7] | -0.7 [-1.8, +0.0] | -1.7 [-1.8, -1.5] | +0.8 [+0.3, +1.3] |
| iid_0.05 | -37.9 [-49.5, -26.2] | -1.4 [-3.1, +0.4] | -1.6 [-1.8, -1.5] | +0.7 [+0.3, +1.1] |
| iid_0.10 | -34.0 [-44.7, -23.8] | -3.2 [-5.0, -1.4] | -1.5 [-1.7, -1.4] | +0.6 [+0.2, +1.0] |
| iid_0.20 | -26.7 [-34.4, -18.5] | -5.3 [-8.6, -1.9] | -1.3 [-1.4, -1.1] | +0.3 [+0.0, +0.6] |
| burst_0.20_r3 | -28.0 [-38.2, -18.0] | -0.2 [-3.8, +2.9] | -1.2 [-1.4, -1.0] | +0.4 [+0.0, +0.7] |
| burst_0.20_r6 | -29.7 [-39.8, -19.7] | +2.3 [+0.5, +3.9] | -1.3 [-1.4, -1.1] | +0.5 [+0.1, +0.9] |

## Mismatch penalty and burst effect (paired, condition - reference)

| arm | contrast | slip false | stable correct | stable inq | slip inq |
|---|---|---:|---:|---:|---:|
| SM | iid_0.01 - iid_0.05 | -8.3 [-11.0, -5.6] | +3.7 [+1.8, +5.8] | -0.1 [-0.1, -0.0] | +0.1 [+0.0, +0.2] |
| SM | iid_0.10 - iid_0.05 | +9.2 [+6.5, +11.9] | -5.5 [-7.9, -3.4] | +0.1 [+0.0, +0.1] | -0.2 [-0.3, -0.0] |
| SM | iid_0.20 - iid_0.05 | +25.1 [+21.6, +28.9] | -17.2 [-21.1, -13.5] | +0.4 [+0.2, +0.5] | -0.4 [-0.6, -0.2] |
| SM | burst_0.20_r3 - iid_0.20 | -6.4 [-12.2, -0.5] | -1.1 [-6.9, +4.6] | +0.1 [-0.1, +0.2] | +0.1 [-0.1, +0.3] |
| SM | burst_0.20_r6 - iid_0.20 | -11.5 [-17.0, -6.0] | +4.4 [-0.9, +10.1] | -0.0 [-0.2, +0.1] | +0.2 [-0.0, +0.4] |
| fixed3 | iid_0.01 - iid_0.05 | -5.7 [-8.5, -3.1] | +3.0 [+1.3, +5.0] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] |
| fixed3 | iid_0.10 - iid_0.05 | +5.3 [+2.2, +8.7] | -3.7 [-5.8, -1.9] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] |
| fixed3 | iid_0.20 - iid_0.05 | +13.8 [+7.9, +19.8] | -13.3 [-16.1, -10.6] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] |
| fixed3 | burst_0.20_r3 - iid_0.20 | -5.1 [-10.2, -0.3] | -6.2 [-12.3, +0.2] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] |
| fixed3 | burst_0.20_r6 - iid_0.20 | -8.5 [-15.1, -2.0] | -3.2 [-8.0, +1.7] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] |
| fixed3+gate | iid_0.01 - iid_0.05 | -3.7 [-5.2, -2.1] | +10.1 [+7.7, +12.6] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] |
| fixed3+gate | iid_0.10 - iid_0.05 | +5.5 [+3.3, +7.9] | -11.5 [-14.8, -8.5] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] |
| fixed3+gate | iid_0.20 - iid_0.05 | +14.0 [+10.7, +17.4] | -35.6 [-40.6, -30.9] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] |
| fixed3+gate | burst_0.20_r3 - iid_0.20 | -2.8 [-8.3, +2.9] | +13.6 [+7.6, +18.9] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] |
| fixed3+gate | burst_0.20_r6 - iid_0.20 | -3.7 [-8.9, +1.8] | +23.0 [+16.9, +29.7] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] |
| E-only | iid_0.01 - iid_0.05 | -3.7 [-5.8, -1.7] | +2.5 [+0.8, +4.6] | -0.1 [-0.2, -0.1] | +0.1 [+0.1, +0.2] |
| E-only | iid_0.10 - iid_0.05 | +5.3 [+3.0, +8.0] | -4.4 [-6.5, -2.5] | +0.2 [+0.1, +0.3] | -0.2 [-0.3, -0.1] |
| E-only | iid_0.20 - iid_0.05 | +18.2 [+14.1, +22.6] | -13.6 [-17.3, -10.2] | +0.7 [+0.6, +0.9] | -0.7 [-0.9, -0.5] |
| E-only | burst_0.20_r3 - iid_0.20 | -2.1 [-9.3, +5.1] | -4.8 [-10.5, +1.1] | -0.1 [-0.3, +0.2] | +0.1 [-0.2, +0.4] |
| E-only | burst_0.20_r6 - iid_0.20 | -5.1 [-12.2, +1.4] | -0.0 [-5.2, +5.8] | -0.3 [-0.6, -0.1] | +0.2 [-0.1, +0.5] |

`iid_* - iid_0.05` rows are mismatch penalties relative to the matched condition; `burst_* - iid_0.20` rows isolate temporal correlation at the same marginal error rate. Positive slip-false differences mean more false remediation; negative stable-correct differences mean lower coverage.

## Burst vs iid at the same marginal rate: all arms

| condition - iid_0.20 | arm | slip false | stable correct | stable abstain | slip none |
|---|---:|---:|---:|---:|---:|
| burst_0.20_r3 | SM | -6.4 [-12.2, -0.5] | -1.1 [-6.9, +4.6] | +0.5 [-1.2, +2.2] | +5.3 [-1.5, +12.2] |
| burst_0.20_r3 | fixed3 | -5.1 [-10.2, -0.3] | -6.2 [-12.3, +0.2] | +0.0 [+0.0, +0.0] | +5.1 [+0.3, +10.2] |
| burst_0.20_r3 | fixed3+gate | -2.8 [-8.3, +2.9] | +13.6 [+7.6, +18.9] | -7.6 [-12.6, -2.5] | +4.4 [-1.3, +10.2] |
| burst_0.20_r3 | E-only | -2.1 [-9.3, +5.1] | -4.8 [-10.5, +1.1] | -1.4 [-5.9, +2.9] | +9.2 [+3.9, +14.9] |
| burst_0.20_r6 | SM | -11.5 [-17.0, -6.0] | +4.4 [-0.9, +10.1] | +0.7 [-1.2, +2.6] | +7.6 [-0.5, +16.1] |
| burst_0.20_r6 | fixed3 | -8.5 [-15.1, -2.0] | -3.2 [-8.0, +1.7] | +0.0 [+0.0, +0.0] | +8.5 [+2.0, +15.1] |
| burst_0.20_r6 | fixed3+gate | -3.7 [-8.9, +1.8] | +23.0 [+16.9, +29.7] | -12.4 [-17.9, -7.4] | +7.1 [-0.7, +14.9] |
| burst_0.20_r6 | E-only | -5.1 [-12.2, +1.4] | -0.0 [-5.2, +5.8] | -5.7 [-11.0, -1.5] | +13.6 [+6.2, +22.0] |

## Reproduction and process checks

| check | result |
|---|---|
| SM iid_0.05 vs frozen v5 `stability_mixed/maxent` | 0 mismatches / 1305 episodes |
| fixed_k3 iid_0.05 vs budget-ablation E1 run | 0 mismatches / 1305 episodes |
| fixed_k3_gate iid_0.05 vs budget-ablation E1 run | 0 mismatches / 1305 episodes |
| e_b6 iid_0.05 vs budget-ablation E1 run | 0 mismatches / 1305 episodes |
| burst marginal wrong rate (6 draws, slip) | 0.221 vs nominal 0.200 |

## Scope

- Post-hoc robustness run on the frozen v5 protocol-valid 87-case test set; no thresholds tuned on these results.
- The diagnostician uses eps=0.05 everywhere; only the student-side process changes. The burst chain is an inattention model, not estimated from real students.
- In burst conditions stable/mixed students also lapse (emit a random wrong answer instead of their misconception prediction), so the condition tests the iid assumption rather than slip students alone.
- Mixed students remain a pressure test with near-zero pair identification; no mixed claim is made here.
