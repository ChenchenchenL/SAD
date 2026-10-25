"""Local regression checks for the v5 information boundary."""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUN_DIR = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(RUN_DIR))

from feedback_v5 import desc_text, diagnosis_for, feedback_prompt, pipeline_diagnosis, visible_diagnosis  # noqa: E402
from g0_lib import DESCRIPTIONS_PATH, load_descriptions  # noqa: E402
from v5_engine import one_shot_episode, build_model, run_episode  # noqa: E402
from v5_templates import CATEGORY_HIDS, build_items  # noqa: E402

items = build_items()
banks = {cat: [it for it in items if it["category"] == cat] for cat in CATEGORY_HIDS}
models = {cat: build_model(cat, banks[cat], CATEGORY_HIDS[cat], with_pairs=True, eps=0.05) for cat in CATEGORY_HIDS}
prior = {cat: models[cat].prior({h: 1.0 for h in CATEGORY_HIDS[cat]}) for cat in CATEGORY_HIDS}
case = next(c for c in json.loads((HERE / "data" / "cases_test_v5.json").read_text(encoding="utf-8"))
            if c["category"] == "decimals")
ep = run_episode(models[case["category"]], prior[case["category"]], case, "stable", "stability_mixed",
                  selection="maxent", partner="decimals.longer_is_larger", seed=0)
desc = {d["module"]: d for d in load_descriptions(DESCRIPTIONS_PATH)}

# 1. pipeline prompt is invariant to hidden labels while visible episode remains fixed
visible = visible_diagnosis(ep.__dict__)
p_base = feedback_prompt(case["problem"], case["correct"], case["answer"], pipeline_diagnosis(desc, visible))
alt = dict(visible)
alt["terminal_kind"] = "abstain"
p_abstain = feedback_prompt(case["problem"], case["correct"], case["answer"], pipeline_diagnosis(desc, alt))
labelled = dict(ep.__dict__)
labelled["true_id"] = "decimals.longer_is_larger"
labelled["student_type"] = "slip"
labelled["true_pair"] = "MIXED|decimals.a|decimals.b"
p2 = feedback_prompt(case["problem"], case["correct"], case["answer"],
                     diagnosis_for(desc, "pipeline", case, labelled, labelled))

assert p_base == p2, "pipeline prompt changed when only hidden true_id changed"
assert p_base != p_abstain, "terminal kind did not affect pipeline prompt"

# 2. abstention must not be automatically verbalised as a slip
slip_abstain = dict(visible, student_type="slip", terminal_kind="abstain", terminal_id=None)
assert "slip" not in pipeline_diagnosis(desc, slip_abstain).lower()
assert "insufficient" in pipeline_diagnosis(desc, slip_abstain).lower()

# 3. explicit none is distinguishable from abstain
none_ep = dict(visible, terminal_kind="none", terminal_id=None)
assert none_ep["terminal_kind"] != "abstain"
assert "does not support" in pipeline_diagnosis(desc, none_ep)

# 4. typed one-shot can emit all four terminal kinds
metas = {
    "stable": {"stable_or_mixed": "stable", "top10": [CATEGORY_HIDS[case["category"]][0]]},
    "slip": {"stable_or_mixed": "slip", "top10": [CATEGORY_HIDS[case["category"]][0]]},
    "mixed": {"stable_or_mixed": "mixed", "top10": CATEGORY_HIDS[case["category"]][:2]},
    "unsure": {"stable_or_mixed": "unsure", "top10": [CATEGORY_HIDS[case["category"]][0]]},
}
kinds = {one_shot_episode(models[case["category"]], prior[case["category"]], case, "slip",
                         partner=CATEGORY_HIDS[case["category"]][1], seed=0, typed=True,
                         prior_meta=m).terminal_kind for m in metas.values()}
assert kinds == {"single", "none", "pair", "abstain"}, kinds

# 5. forced one-shot is retained as a historical diagnostic control
forced = one_shot_episode(models[case["category"]], prior[case["category"]], case, "slip", seed=0, typed=False)
assert forced.terminal_kind == "single"

# 6. selection and stopping are separate returned dimensions
r = run_episode(models[case["category"]], prior[case["category"]], case, "stable", "stability_mixed",
                 selection="targeted", partner=CATEGORY_HIDS[case["category"]][1], seed=0)
assert r.rule == "stability_mixed" and r.selection == "targeted"

print("PASS: v5 information-boundary and typed one-shot regression checks")
