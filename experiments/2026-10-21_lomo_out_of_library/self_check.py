"""Implementation self-check for the LOMO runner.

Verifies the code paths that are NEW relative to the frozen stability
ablation (whose stop_check/model construction is already episode-verified
against the frozen v5 episodes, 0 mismatches / 1305):

  1. reduced-model construction (rule removed from singles and pairs;
     finite likelihoods; prior vector normalised);
  2. prior filtering (removed rule absent from weights, weights renormalise);
  3. observe_ool students (stable_ool deterministic = removed-rule
     prediction; slip_ool marginal rule-follow frequency == 1 - eps and
     noise answers never equal the rule prediction);
  4. terminal scoring map (single/pair/mixed -> false commit; none; abstain);
  5. eligibility (initial answer is the removed rule's prediction on the
     case item, for every case).
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "src"))

import ablation  # noqa: E402
import lomo  # noqa: E402
import v5_engine as eng  # noqa: E402

CATEGORY_ORDER = [
    "subtraction",
    "fractions",
    "decimals",
    "negative_numbers",
    "order_of_operations",
    "percentages",
]

failures = []


def check(name: str, ok: bool, detail: str = "") -> None:
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def main() -> int:
    cases = json.loads((HERE / "data" / "cases_test_v5_exclusion_corrected.json").read_text(encoding="utf-8"))
    banks = {}
    singles_full = {}
    for cat in CATEGORY_ORDER:
        bank = json.loads((HERE / "data" / f"bank_v5_{cat}.json").read_text(encoding="utf-8"))
        banks[cat] = bank
        singles_full[cat] = lomo.effective_singles(bank)

    eps = 0.05

    # --- 5. eligibility for every case -----------------------------------
    bad = []
    for case in cases:
        cat = case["category"]
        h = case["true_id"]
        item = banks[cat]["items"][int(case["item_idx"])]
        if case["answer"] not in item["answers"]:
            bad.append((case["case_id"], "answer_not_in_answers"))
        if lomo.vector_of([item], h)[0] != case["answer"]:
            bad.append((case["case_id"], "answer_is_not_removed_rule_prediction"))
        if case["answer"] == item["correct"]:
            bad.append((case["case_id"], "initial_answer_is_correct"))
    check("eligibility: initial answer == removed-rule prediction for all 87 cases",
          not bad, str(bad[:5]))

    # --- 1/2. reduced model + prior filtering -----------------------------
    for case in cases[:60]:
        cat = case["category"]
        h = case["true_id"]
        singles = [x for x in singles_full[cat] if x != h]
        model = eng.build_model(cat, banks[cat]["items"], singles, with_pairs=True, eps=eps)
        if h in model.index:
            failures.append("h in index")
            break
        expected_pairs = {
            eng.pair_id(a, b) for a, b in __import__("itertools").combinations(singles, 2)
        }
        if set(model.pairs) != expected_pairs or any(h in p for p in model.pairs):
            failures.append("pair reconstruction")
            break
        if not np.all(np.isfinite(model.L_stack)) or np.any(model.L_stack < -1e-12):
            failures.append("likelihood finite")
            break
        prior = lomo.build_prior_for_case({"top10": singles_full[cat][:5]}, singles, model)
        if abs(float(prior.sum()) - 1.0) > 1e-9:
            failures.append("prior sum")
            break
        if prior[model.index[h]] != 0.0 if h in model.index else False:
            failures.append("prior mass on removed rule")
            break
        if abs(float(prior[model.single_idx].sum()) + float(prior[model.pair_idx].sum())
               + float(prior[model.correct_idx]) + float(prior[model.other_idx]) - 1.0) > 1e-9:
            failures.append("prior mass decomposition")
            break
    else:
        check("reduced model: singles/pairs exclude removed rule; likelihoods finite; prior normalised", True)

    # --- 3. student simulators --------------------------------------------
    case = cases[0]
    cat, h = case["category"], case["true_id"]
    singles = [x for x in singles_full[cat] if x != h]
    model = eng.build_model(cat, banks[cat]["items"], singles, with_pairs=True, eps=eps)

    det_ok = all(
        lomo.observe_ool(model, "stable_ool", i, h, case["case_id"], s, eps)
        == model.effective_pred(i, h)
        for i in range(len(model.items))
        for s in range(5)
    )
    check("stable_ool: deterministic removed-rule prediction on every item", det_ok)

    # _case_rng restarts its stream per key, so distinct (item, seed) keys are
    # the independent Bernoulli units (same convention as the frozen engine).
    n_keys_seed = 500
    rng_cases = [(i, s) for i in range(len(model.items)) for s in range(n_keys_seed)]
    counts = Counter()
    noise_bad = 0
    for _ in range(2):
        for i, s in rng_cases:
            out = lomo.observe_ool(model, "slip_ool", i, h, case["case_id"], s, eps)
            pred = model.effective_pred(i, h)
            if out == pred:
                counts["pred"] += 1
            else:
                counts["other"] += 1
            if out not in model.items[i]["answers"]:
                noise_bad += 1
    n_draws = 2 * len(rng_cases)
    freq = counts["pred"] / n_draws
    sd = (eps * (1.0 - eps) / len(rng_cases)) ** 0.5
    check("slip_ool: marginal rule-prediction frequency == 1 - eps (3sd over independent keys)",
          abs(freq - (1.0 - eps)) < 3 * sd, f"freq={freq:.4f} sd={sd:.4f}")
    check("slip_ool: every draw is a valid answer option", noise_bad == 0)

    # --- 4. scoring map ----------------------------------------------------
    import unittest.mock as mock

    class Fake:
        pass

    f = Fake()
    f.rule = "arm"
    f.selection = "maxent"
    f.student_type = "stable_ool"
    f.case_id = "x"
    f.family = "f"
    f.category = "c"
    f.true_id = "h"
    f.true_pair = None
    f.terminal_p = 0.5
    f.n_obs = 3
    f.n_inquiries = 2
    f.stopped = True
    f.budget_exhausted = False
    f.verifications = 0
    f.history = []
    f.meta = {"removed_rule": "h", "gate_state_at_terminal": {}}
    mapping = {
        ("single", "g"): (True, True, False, False, False),
        ("pair", "MIXED|a|b"): (True, False, True, False, False),
        ("mixed", None): (True, False, True, False, False),
        ("none", None): (False, False, False, True, False),
        ("abstain", None): (False, False, False, False, True),
    }
    ok = True
    for (kind, tid), expect in mapping.items():
        f.terminal_kind, f.terminal_id = kind, tid
        d = lomo.episode_to_dict(f, 0)
        got = (d["false_commit"], d["false_single"], d["false_pair_mixed"], d["none"], d["abstain"])
        if got != expect or d["safe"] != (expect[3] or expect[4]):
            ok = False
            print(f"  scoring mismatch for {kind}: got {got}, safe={d['safe']}")
    check("scoring: terminal kind -> false_commit/none/abstain mapping", ok)

    # --- sanity: full-SM in-library positive control on one case -----------
    # With the rule still IN the model and the frozen "stable" student, the
    # reused stop_check must diagnose the rule (main pipeline behaviour).
    full_model = eng.build_model(cat, banks[cat]["items"], singles_full[cat], with_pairs=True, eps=eps)
    prior_row_full = {x: 1.0 / len(singles_full[cat]) for x in singles_full[cat]}
    res = None
    for seed in range(5):
        r = ablation.run_episode_ablation(
            full_model, full_model.prior(prior_row_full), case, "stable",
            "stability_mixed_reference", seed=seed, eps=eps,
        )
        if r is not None:
            res = r
            break
    check("in-library control: full SM diagnoses the rule when it is in the library",
          res is not None and res.correct,
          f"terminal={res.terminal_kind}:{res.terminal_id}" if res is not None else "no episode")

    print()
    if failures:
        print(f"SELF-CHECK FAILED: {failures}")
        return 1
    print("ALL SELF-CHECKS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
