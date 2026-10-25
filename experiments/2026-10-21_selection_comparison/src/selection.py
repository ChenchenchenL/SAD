"""Selection-strategy comparison under unified hypothesis space, prior,
stopping rule and budget.

Two budget blocks, each internally uniform:

  * adaptive block: full SM stopping (`stability_mixed`, frozen), pair-augmented
    hypothesis space, max_obs=7, MaxEnt/IG/random/fixed selection;
  * fixed block: frozen Fixed-3 convention (no pair hypotheses, exactly 3
    inquiries, posterior commit to single/none, never abstain),
    MaxEnt/IG/random/fixed selection.

Random is corrected: one RNG stream per episode, advanced per step (the frozen
v5 pipeline re-seeded the same stream at every step, which makes the order a
single-draw function of the remaining-list length). The legacy reseeded random
is kept as one diagnostic fixed-k arm so the historical numbers can be
reproduced and the size of the correction measured.

Student outcomes are keyed by (case, seed, item, student type) exactly as in
the frozen engine, so every strategy sees the same answer for the same item
(common random numbers); strategies differ only in which items they observe.
"""
from __future__ import annotations

import hashlib
import random

import ablation
import v5_engine as eng

STUDENT_TYPES = ("stable", "slip")

ADAPTIVE_ARMS = {
    "sm_maxent": "maxent",
    "sm_ig": "ig",
    "sm_random": "random",
    "sm_fixed_order": "fixed",
}

K3_ARMS = {
    "k3_maxent": "maxent",
    "k3_ig": "ig",
    "k3_random": "random",
    "k3_fixed_order": "fixed",
    "k3_random_legacy": "random_legacy",
}

ALL_ARMS = {**ADAPTIVE_ARMS, **K3_ARMS}


def episode_rng(case_id: str, seed: int, student_type: str) -> random.Random:
    raw = f"{case_id}|{seed}|{student_type}|selection|random_stream_corrected"
    return random.Random(int(hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16], 16))


def select_item(model, post, available, strategy: str, rng,
                case_id: str, seed: int, student_type: str) -> int:
    if strategy == "maxent":
        return model.select_maxent(post, available)
    if strategy == "ig":
        return model.select_ig(post, available)
    if strategy == "fixed":
        return available[0]
    if strategy == "random":
        return rng.choice(available)
    if strategy == "random_legacy":
        # Frozen v5 implementation: a fresh RNG with the same seed per step.
        legacy = eng._case_rng(case_id, seed, -1, student_type, "selection")
        return legacy.choice(available)
    raise KeyError(strategy)


def _eligible(model, case, student_type: str) -> bool:
    item = model.items[int(case["item_idx"])]
    answer = case["answer"]
    true_id = case["true_id"]
    if answer not in item["answers"]:
        return False
    if student_type == "slip" and answer == item["correct"]:
        return False
    if student_type in ("stable", "mixed"):
        if model.effective_pred(int(case["item_idx"]), true_id) != answer:
            return False
        if true_id not in model.index:
            return False
    return True


def run_adaptive(model, prior, case: dict, student_type: str, arm: str,
                 strategy: str, seed: int, eps: float = 0.05, max_obs: int = 7):
    """Mirror of ablation.run_episode_ablation with an injected selector."""
    if not _eligible(model, case, student_type):
        return None
    true_id = case["true_id"]
    item_idx = int(case["item_idx"])
    answer = case["answer"]

    post = prior.copy()
    history = [(item_idx, answer)]
    used = {item_idx}
    stopped = False
    budget_exhausted = False
    terminal = None
    selected: list[int] = []
    rng = episode_rng(case["case_id"], seed, student_type)

    while True:
        if len(history) >= max_obs:
            budget_exhausted = True
            break
        cand = ablation.stop_check(model, post, history, "stability_mixed_reference")
        if cand:
            terminal = cand
            stopped = True
            break
        available = [i for i in range(len(model.items)) if i not in used]
        if not available:
            budget_exhausted = True
            break
        nidx = select_item(model, post, available, strategy, rng,
                           case["case_id"], seed, student_type)
        outcome = eng.observe(model, student_type, nidx, true_id, None,
                              case["case_id"], seed, eps)
        used.add(nidx)
        history.append((nidx, outcome))
        selected.append(nidx)
        post = model.update(post, nidx, outcome)

    if terminal is None:
        cand = ablation.stop_check(model, post, history, "stability_mixed_reference")
        terminal = cand if cand else ("abstain", None, float(post.max()))

    kind, tid, tp = terminal
    return eng.V5Result(
        rule=arm,
        selection=strategy,
        student_type=student_type,
        case_id=case["case_id"],
        family=case.get("family") or case.get("template_family") or str(case.get("library_template")),
        category=case["category"],
        true_id=true_id,
        true_pair=None,
        terminal_kind=kind,
        terminal_id=tid,
        terminal_p=tp,
        n_obs=len(history),
        stopped=stopped,
        budget_exhausted=budget_exhausted,
        verifications=0,
        history=[(model.items[i]["text"], o) for i, o in history],
        meta={"selected_items": selected},
    )


def run_fixed_k(model, prior, case: dict, student_type: str, arm: str,
                strategy: str, seed: int, eps: float = 0.05, k: int = 3):
    """Mirror of eng.run_budget_episode with an injected selector."""
    if not _eligible(model, case, student_type):
        return None
    true_id = case["true_id"]
    item_idx = int(case["item_idx"])
    answer = case["answer"]

    post = prior.copy()
    history = [(item_idx, answer)]
    used = {item_idx}
    selected: list[int] = []
    rng = episode_rng(case["case_id"], seed, student_type)

    for _ in range(k):
        available = [i for i in range(len(model.items)) if i not in used]
        if not available:
            break
        nidx = select_item(model, post, available, strategy, rng,
                           case["case_id"], seed, student_type)
        outcome = eng.observe(model, student_type, nidx, true_id, None,
                              case["case_id"], seed, eps)
        used.add(nidx)
        history.append((nidx, outcome))
        selected.append(nidx)
        post = model.update(post, nidx, outcome)

    kind, tid, tp = eng._terminal_from_posterior(model, post, allow_pairs=False)
    return eng.V5Result(
        rule=arm,
        selection=strategy,
        student_type=student_type,
        case_id=case["case_id"],
        family=case.get("family") or case.get("template_family") or str(case.get("library_template")),
        category=case["category"],
        true_id=true_id,
        true_pair=None,
        terminal_kind=kind,
        terminal_id=tid,
        terminal_p=tp,
        n_obs=len(history),
        stopped=False,
        budget_exhausted=True,
        verifications=0,
        history=[(model.items[i]["text"], o) for i, o in history],
        meta={"selected_items": selected},
    )


def episode_to_dict(res, seed: int) -> dict:
    return {
        "arm": res.rule,
        "selection": res.selection,
        "student_type": res.student_type,
        "case_id": res.case_id,
        "family": res.family,
        "category": res.category,
        "true_id": res.true_id,
        "terminal_kind": res.terminal_kind,
        "terminal_id": res.terminal_id,
        "terminal_p": float(res.terminal_p),
        "n_obs": int(res.n_obs),
        "n_inquiries": int(res.n_inquiries),
        "stopped": bool(res.stopped),
        "budget_exhausted": bool(res.budget_exhausted),
        "correct": bool(res.correct),
        "false_remediation": bool(res.false_remediation),
        "selected_items": list(res.meta["selected_items"]),
        "seed": int(seed),
        "J5": float(res.n_obs + 5.0 * float(res.false_remediation)),
        "J10": float(res.n_obs + 10.0 * float(res.false_remediation)),
    }


def episode_metric(e: dict, metric: str) -> float:
    if metric == "correct":
        return float(bool(e["correct"]))
    if metric == "correct_stop":
        return float(bool(e["stopped"] and e["correct"]))
    if metric == "false":
        return float(bool(e["false_remediation"]))
    if metric == "none":
        return float(e["terminal_kind"] == "none")
    if metric == "abstain":
        return float(e["terminal_kind"] == "abstain")
    if metric == "pair_mixed":
        return float(e["terminal_kind"] in ("pair", "mixed"))
    if metric == "n_inquiries":
        return float(e["n_inquiries"])
    if metric == "n_obs":
        return float(e["n_obs"])
    if metric == "J5":
        return float(e["J5"])
    if metric == "J10":
        return float(e["J10"])
    raise KeyError(metric)


METRICS = (
    "correct",
    "correct_stop",
    "false",
    "pair_mixed",
    "none",
    "abstain",
    "n_inquiries",
    "n_obs",
    "J5",
    "J10",
)


def step1_agreement(episodes_by_arm_type: dict, arms: list[str], student_type: str) -> dict:
    """Fraction of paired episodes whose first selected item is identical."""
    by_arm = {
        arm: {(e["case_id"], e["seed"]): e["selected_items"] for e in episodes_by_arm_type.get((arm, student_type), [])}
        for arm in arms
    }
    out = {}
    for i, a in enumerate(arms):
        for b in arms[i + 1:]:
            common = sorted(set(by_arm[a]) & set(by_arm[b]))
            if not common:
                continue
            same = sum(
                1 for key in common
                if by_arm[a][key] and by_arm[b][key] and by_arm[a][key][0] == by_arm[b][key][0]
            )
            out[f"{a} vs {b}"] = {"n": len(common), "agreement": same / len(common)}
    return out


def sequence_identity(episodes_by_arm_type: dict, arms: list[str], student_type: str) -> dict:
    """Fraction of paired episodes with identical full item sequences (fixed-k)."""
    by_arm = {
        arm: {(e["case_id"], e["seed"]): e["selected_items"] for e in episodes_by_arm_type.get((arm, student_type), [])}
        for arm in arms
    }
    out = {}
    for i, a in enumerate(arms):
        for b in arms[i + 1:]:
            common = sorted(set(by_arm[a]) & set(by_arm[b]))
            if not common:
                continue
            same = sum(1 for key in common if by_arm[a][key] == by_arm[b][key])
            out[f"{a} vs {b}"] = {"n": len(common), "identity": same / len(common)}
    return out
