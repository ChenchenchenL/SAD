# Scope and provenance

This package was curated on 2026-10-25 from the saved records supporting the current Full SM / Simplified SM manuscript. The manifest records SHA-256 checksums of the published bytes, their original source bytes, compression and machine-path normalization. It is a new publication snapshot, not a claim that every historical freeze hash matches.

The original freeze record predates a change to the main v5 engine: the engine file hash differs from the historical `v5_freeze.json` value. The original relocated provenance manifest is retained and records this conflict. The selection experiment at noise 0.05 also has a documented mismatch between the saved run manifest and the current run driver; the exact historical driver was not recovered. Input data and saved numerical results remain available, and the source audit explicitly marks this known conflict rather than changing the old hash.

The supported reproduction claim is reconstruction and verification of the paper statistics from the archived episode, feedback and judge records, together with the current implementation and regression checks. It does not certify bitwise regeneration of every historical trajectory by the current engine, or identical new LLM responses.

The corrected main analysis uses 87 of the original 90 cases under the recorded exclusion rule (`v5test:0013`–`0015`); both case sets and the sensitivity data are retained. Diagnosis uncertainty uses template-family cluster bootstrapping with 2,000 resamples. Feedback analyses retain the separately weighted full DeepSeek evaluation (116 scenarios), GLM common subset (60 scenarios), and DeepSeek common subset (the same 60 scenarios); these are not pooled.

The second bank is a corrected bank of new instances and partially extended structures. It is not a strict unseen-structure holdout. Selection source data retain the legacy reseeded-random diagnostic control; the main selection figure displays the advanced-stream Random strategy. Noise figure curves use the four iid conditions; saved burst-condition records are retained and are not silently discarded.

Machine-specific absolute paths and the private endpoint, where present in metadata or usage examples, are normalized for portability. The second-bank plotting command also uses the bundled QA scripts and permits a sans-serif font fallback. Numerical values, case identifiers, model outputs, prompts, exclusion rules and archived confidence intervals are not edited. Portability changes are individually marked in `reproduction_data/manifest.json`.

The public package omits unrelated datasets, local credentials, temporary runtime binaries, chat history, and manuscript drafts. MalruleLib runtime sources and its original license are retained with attribution. User-generated synthetic data and code are licensed only for non-commercial scientific research; third-party terms also apply.
