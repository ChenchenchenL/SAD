# SAD: Stability-Aware Active Diagnosis and Feedback

Reproduction materials for **Stability-Aware Active Diagnosis and Feedback for Mathematical Misconceptions**, by Lei Chen and Xinnian Wang. This snapshot supports the Applied Intelligence submission. All included participant records are synthetic or simulated; there are no human-participant data.

The package is publicly accessible **for non-commercial scientific research only**. See [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Public availability is not an unrestricted commercial-use license.

## Reproduce without an LLM account

Use CPython 3.12 and run from the repository root:

```sh
python -m venv .venv
# Activate .venv using the command appropriate for your operating system.
python -m pip install -r requirements.txt
python scripts/reproduce_offline.py
```

The script verifies and unpacks losslessly compressed raw records, tests the diagnosis/feedback information boundary, rebuilds the main diagnosis and feedback statistics, compares the results with the archived audit JSONs, and audits extension data and confidence intervals. It makes no network or paid LLM requests. Logs and a machine-readable result are written to `verification/`. The tested package versions are pinned in requirements.txt; Arial is used when installed, with sans-serif fallbacks for other systems.

## Data and code map

| Material | Location |
|---|---|
| Main synthetic question banks, test/development cases and frozen configuration | `experiments/2026-10-20_llm_v4_v5/v5/data/`, `v5/config/` |
| Main diagnosis engine, prior, feedback and judge implementations/prompts | Python files in `experiments/2026-10-20_llm_v4_v5/v5/` and its parent |
| Raw simulation trajectories and LLM feedback/judge records | `reproduction_data/`, restored to their original relative experiment paths by `scripts/unpack_data.py` |
| Main diagnosis and feedback statistics | `experiments/2026-10-20_llm_v4_v5/v5/out/final_audit/` |
| Selection, gate/budget, threshold, out-of-library, second-bank and noise experiments | Corresponding dated directories under `experiments/` (only the runs listed in the manifest are included) |
| Figure source CSVs and table data | `results/figures/data/`, `results/tables/` |
| Plotting scripts and vector quantitative figures | `results/figures/scripts/`, `results/figures/exports/` |
| File hashes, compression and path-normalization records | `reproduction_data/manifest.json` |
| Provenance boundaries and historical conflicts | [docs/PROVENANCE.md](docs/PROVENANCE.md) |

Main analysis: 87 protocol-valid initial cases across six domains and 36 template families, retaining the original 90-case analysis as a sensitivity check. Full SM and Simplified SM are different terminal policies: the main Full SM feedback effect is **24.2 percentage points** relative to one-shot diagnosis. Later exploratory variants are excluded from this package.

## Rebuild the quantitative figures

After offline reproduction:

```sh
python results/figures/scripts/fig1_fig5_selection_noise.py selection
python results/figures/scripts/fig_e1_gate_stopping_budget.py
python results/figures/scripts/fig_e6_threshold_sensitivity.py
python results/figures/scripts/fig4_second_bank_replication.py
python results/figures/scripts/fig1_fig5_selection_noise.py noise
python results/figures/scripts/fig3_feedback_forest.py
```

Submission figure numbers map to script stems as follows: Fig2 = `fig1_selection_comparison`; Fig3 = `fig_e1_gate_stopping_budget`; Fig4 = `fig_e6_threshold_sensitivity`; Fig5 = `fig4_second_bank_replication`; Fig6 = `fig5_noise_misspecification`; Fig7 = `fig3_feedback_forest`. Fig1 is a conceptual workflow and has no numerical source dataset.

The plotting scripts retain source estimates and family-cluster confidence intervals, export editable PDF/SVG and 600-ppi TIFF/PNG, and measure comparable-panel alignment. No experimental value was changed to revise display labels.

## Optional new LLM runs

The prior, feedback-generation and judging code is provided for inspection. Reproducing the archived statistical results does not require new model calls. New calls require the user's own endpoint and credentials in an untracked `.env` (see `.env.example`), may incur charges, and may not reproduce stochastic historical text. Observe all third-party license restrictions before any new use. No credentials or private service endpoint are included.

## Citation

Until publication metadata is assigned, cite the paper title and authors and use the commit permalink of the snapshot inspected. No DOI or acceptance status is claimed.
