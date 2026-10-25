"""Implementation self-check for the selection comparison.

  1. `BankModel.select_ig` vs an independent brute-force expected-information-
     gain computation on real posterior states;
  2. corrected random stream: one stream per episode, without replacement,
     distinct picks, non-degenerate across seeds;
  3. legacy random defect: per-step reseeding reuses the same raw draw, so the
     chosen position repeats over the shrinking list (it behaves like a fixed
     positional order rather than a random permutation);
  4. reproduction of the four frozen reference arms is asserted by run.py
     (0 mismatches); this script does not repeat it.
"""
from __future__ import annotations

import json
import math
import sys
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "src"))

import ablation  # noqa: E402
import selection as sel  # noqa: E402
import v5_engine as eng  # noqa: E402
from g0_lib import prior_weights  # noqa: E402

CATEGORY_ORDER = [
    "subtraction", "fractions", "decimals", "negative_numbers",
    "order_of_operations", "percentages",
]

failures = []


def check(name: str, ok: bool, detail: str = "") -> None:
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def brute_ig(model, post, idx):
    base = model.entropy(post)
    dist = model.predictive(post, idx)
    exp = 0.0
    for o, p in enumerate(dist):
        if p <= 1e-9:
            continue
        new = post * model.L[idx][:, o]
        total = new.sum()
        if total <= 0:
            continue
        exp += p * model.entropy(new / total)
    return base - exp


def main() -> int:
    cases = json.loads((HERE / "data" / "cases_test_v5_exclusion_corrected.json").read_text(encoding="utf-8"))
    priors = {}
    for line in (HERE / "data" / "priors_test_category.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            if row.get("http_status") == 200 and row.get("top10"):
                priors[row["key"]] = row

    # --- 1. IG equivalence on real states ---------------------------------
    n_states = 0
    mismatches = 0
    for case in cases[:12]:
        cat = case["category"]
        bank = json.loads((HERE / "data" / f"bank_v5_{cat}.json").read_text(encoding="utf-8"))
        singles = [h["id"] for h in bank["hypotheses"]]
        model = eng.build_model(cat, bank["items"], singles, with_pairs=True, eps=0.05)
        prior_row = priors.get(case["key"]) or {}
        top10 = prior_row.get("top10") or []
        weights = prior_weights(top10, singles) if top10 else {h: 1.0 / len(singles) for h in singles}
        post = model.prior(weights)
        item_idx = int(case["item_idx"])
        states = [post, model.update(post, item_idx, case["answer"])]
        states.append(model.update(states[-1], (item_idx + 1) % len(model.items), case["answer"]))
        for state in states:
            available = list(range(len(model.items)))
            chosen = model.select_ig(state, available)
            scores = [brute_ig(model, state, i) for i in available]
            best = max(scores)
            close = [i for i, s in zip(available, scores) if best - s < 1e-9]
            n_states += 1
            if chosen not in close:
                mismatches += 1
    check("IG: select_ig argmax matches independent brute-force IG",
          mismatches == 0, f"{mismatches}/{n_states} states")

    # --- 2. corrected random stream properties ----------------------------
    case = cases[0]
    cat = case["category"]
    bank = json.loads((HERE / "data" / f"bank_v5_{cat}.json").read_text(encoding="utf-8"))
    singles = [h["id"] for h in bank["hypotheses"]]
    pairs_model = eng.build_model(cat, bank["items"], singles, with_pairs=True, eps=0.05)
    seqs = []
    ok_distinct = True
    for seed in range(5):
        st = "stable"
        rng = sel.episode_rng(case["case_id"], seed, st)
        available = list(range(len(pairs_model.items)))
        picks = []
        for _ in range(3):
            pick = sel.select_item(pairs_model, pairs_model.prior({h: 1.0 for h in singles}),
                                   available, "random", rng, case["case_id"], seed, st)
            picks.append(pick)
            available.remove(pick)
        seqs.append(tuple(picks))
        if len(set(picks)) != 3:
            ok_distinct = False
    check("random: per-episode without-replacement picks, distinct across 3 steps", ok_distinct)
    check("random: sequence varies across seeds", len(set(seqs)) > 1, str(seqs[:3]))

    # --- 3. legacy defect demonstration -----------------------------------
    # The legacy implementation re-seeds the same stream every step. Both
    # steps therefore consume the same first raw draw and (for a 15-item list)
    # usually accept at the same position: the picked list position repeats,
    # so the "random" order is a sequential walk from one random start,
    # essentially fixed order with a random offset. The corrected stream has
    # independent per-step positions.
    n_items = 15
    same_pos_corrected = 0
    same_pos_legacy = 0
    n_trials = 4000
    for case_i in range(n_trials):
        cid = f"synthetic:{case_i}"
        available = list(range(n_items))
        rng = sel.episode_rng(cid, 0, "stable")
        pos1 = rng.randrange(len(available))
        available.pop(pos1)
        pos2 = rng.randrange(len(available))
        if pos2 == pos1:
            same_pos_corrected += 1

        avail_l = list(range(n_items))
        l1 = eng._case_rng(cid, 0, -1, "stable", "selection").choice(avail_l)
        avail_l.remove(l1)
        l2 = eng._case_rng(cid, 0, -1, "stable", "selection").choice(avail_l)
        if avail_l.index(l2) == l1:
            same_pos_legacy += 1
    corr_rate = same_pos_corrected / n_trials
    leg_rate = same_pos_legacy / n_trials
    check("random: corrected step-2 position repeats at chance level (~1/14)",
          abs(corr_rate - 1.0 / (n_items - 1)) < 0.03, f"{corr_rate:.3f}")
    check("random: legacy repeats the same list position (defect reproduced)",
          leg_rate > 0.5,
          f"{leg_rate:.3f} vs chance {1.0/(n_items-1):.3f} "
          f"(= sequential walk from a random start, i.e. near fixed order)")

    print()
    if failures:
        print("SELF-CHECK FAILED:", failures)
        return 1
    print("ALL SELF-CHECKS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
