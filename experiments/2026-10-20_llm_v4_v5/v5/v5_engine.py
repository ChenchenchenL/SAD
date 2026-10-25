"""V5 diagnosis engine.

Compared with the v4 engine this module:
  * separates item-selection policy from stopping policy;
  * supports a typed one-shot output (single / slip / mixed / abstain);
  * reports explicit "no stable misconception" separately from abstention;
  * reports total observations (including the initial item) and additional inquiries;
  * uses common random numbers keyed by case/item/student so paired rules see the
    same simulated response for the same item;
  * never reads hidden labels for diagnosis decisions.
"""
from __future__ import annotations

import hashlib
import itertools
import math
import random
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

PARENT = Path(__file__).resolve().parents[1]
if str(PARENT) not in sys.path:
    sys.path.insert(0, str(PARENT))

from g0_lib import BankModel, pair_id  # noqa: E402

HIDDEN_FIELDS = ("student_type", "true_id", "true_pair")


@dataclass
class V5Result:
    rule: str
    selection: str
    student_type: str
    case_id: str
    family: str
    category: str
    true_id: str | None
    true_pair: str | None
    terminal_kind: str
    terminal_id: str | None
    terminal_p: float
    n_obs: int
    stopped: bool
    budget_exhausted: bool
    verifications: int
    history: list = field(default_factory=list)
    meta: dict = field(default_factory=dict)

    @property
    def n_inquiries(self) -> int:
        return max(0, self.n_obs - 1)

    @property
    def explicit_none(self) -> bool:
        return self.terminal_kind == "none"

    @property
    def abstain(self) -> bool:
        return self.terminal_kind == "abstain"

    @property
    def diagnosed(self) -> bool:
        return self.terminal_kind in ("single", "pair", "mixed")

    @property
    def correct(self) -> bool:
        if self.student_type == "stable":
            return self.terminal_kind == "single" and self.terminal_id == self.true_id
        if self.student_type == "slip":
            # both an explicit no-misconception judgement and an abstention
            # are acceptable for a student who has no stable misconception
            return self.terminal_kind in ("none", "abstain")
        return self.terminal_kind == "pair" and self.terminal_id == self.true_pair

    @property
    def false_remediation(self) -> bool:
        if self.student_type == "stable":
            return self.terminal_kind == "single" and self.terminal_id != self.true_id
        if self.student_type == "slip":
            return self.terminal_kind in ("single", "pair", "mixed")
        if self.terminal_kind == "single":
            return True
        if self.terminal_kind == "pair":
            return self.terminal_id != self.true_pair
        return False

    @property
    def mixed_detected(self) -> bool:
        return self.student_type == "mixed" and (
            (self.terminal_kind == "pair" and self.terminal_id == self.true_pair)
            or self.terminal_kind == "mixed"
        )

    @property
    def pair_identified(self) -> bool:
        return self.student_type == "mixed" and self.terminal_kind == "pair" and self.terminal_id == self.true_pair


def build_model(category: str, items: list[dict], singles: list[str], with_pairs: bool = False, eps: float = 0.05) -> BankModel:
    pairs = [pair_id(a, b) for a, b in itertools.combinations(singles, 2)] if with_pairs else []
    return BankModel(category=category, singles=singles, pairs=pairs, items=items, eps=eps)


def usable_singles(model: BankModel, min_triggers: int = 1) -> list[str]:
    return [
        h
        for h in model.singles
        if sum(1 for it in model.items if it.get("applicable", {}).get(h, False) and it["triggers"].get(h, False)) >= min_triggers
    ]


def _case_rng(case_id: str, seed: int, item_idx: int, student_type: str, extra: str = "") -> random.Random:
    raw = f"{case_id}|{seed}|{item_idx}|{student_type}|{extra}"
    return random.Random(int(hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16], 16))


def _choose_partner(model: BankModel, case: dict, seed: int) -> str | None:
    true_id = case["true_id"]
    item_idx = int(case["item_idx"])
    cands = [
        h for h in usable_singles(model)
        if h != true_id and h in model.index
    ]
    if not cands:
        return None
    # deterministic across all rules for a given case/seed
    raw = f"{case['case_id']}|{seed}|partner"
    idx = int(hashlib.sha256(raw.encode("utf-8")).hexdigest()[:8], 16) % len(cands)
    return cands[idx]


def _single_outcome(model: BankModel, item_idx: int, h: str, case_id: str, seed: int, student_type: str, eps: float) -> str:
    item = model.items[item_idx]
    pred = model.effective_pred(item_idx, h)
    rng = _case_rng(case_id, seed, item_idx, student_type, h)
    if rng.random() < eps:
        choices = [a for a in item["answers"] if a != pred]
        return rng.choice(choices) if choices else pred
    return pred


def _slip_outcome(model: BankModel, item_idx: int, case_id: str, seed: int, eps: float) -> str:
    item = model.items[item_idx]
    rng = _case_rng(case_id, seed, item_idx, "slip")
    if rng.random() >= eps:
        return item["correct"]
    choices = [a for a in item["answers"] if a != item["correct"]]
    return rng.choice(choices) if choices else item["correct"]


def _mixed_outcome(model: BankModel, item_idx: int, pair: str, case_id: str, seed: int, eps: float) -> str:
    a, b = pair.split("|")[1:]
    rng = _case_rng(case_id, seed, item_idx, "mixed", pair)
    chosen = a if rng.random() < 0.5 else b
    return _single_outcome(model, item_idx, chosen, case_id, seed, "mixed", eps)


def observe(model: BankModel, student_type: str, item_idx: int, true_id: str, true_pair: str | None,
            case_id: str, seed: int, eps: float) -> str:
    if student_type == "stable":
        return _single_outcome(model, item_idx, true_id, case_id, seed, student_type, eps)
    if student_type == "slip":
        return _slip_outcome(model, item_idx, case_id, seed, eps)
    assert true_pair is not None
    return _mixed_outcome(model, item_idx, true_pair, case_id, seed, eps)


def _terminal_from_posterior(model: BankModel, post: np.ndarray, allow_pairs: bool) -> tuple[str, str | None, float]:
    j = int(np.argmax(post))
    name = model.names[j]
    if name in ("CORRECT", "OTHER"):
        return ("none", None, float(post[j]))
    if name.startswith("MIXED|"):
        if allow_pairs:
            return ("pair", name, float(post[j]))
        h, p = model.top_single(post)
        return ("single", h, p)
    return ("single", name, float(post[j]))


def _stop_check(model: BankModel, post: np.ndarray, history: list[tuple[int, str]], rule: str) -> tuple[str, str | None, float] | None:
    if rule == "posterior":
        h, p = model.top_single(post)
        return ("single", h, p) if p >= 0.9 else None
    if rule == "entropy":
        idx = list(model.single_idx) + [model.correct_idx, model.other_idx]
        p = post[idx]
        total = p.sum()
        hval = model.entropy(p / total) if total > 0 else 0.0
        if hval <= 0.3:
            h, p1 = model.top_single(post)
            return ("single", h, p1)
        return None
    if rule.startswith("stability"):
        allow_pairs = rule != "stability"
        cand = model.stability_candidate(
            post,
            history,
            allow_pairs=allow_pairs,
            check_pairs=allow_pairs,
            pair_ceiling=0.20 if allow_pairs else 0.15,
        )
        if cand:
            return cand
        if model.no_misconception_candidate(post, history, threshold=0.8):
            return ("none", None, model.none_mass(post))
        if allow_pairs:
            pm = model.mass_on_pairs(post)
            single_mass = float(post[model.single_idx].sum())
            top_single_p = model.top_single(post)[1]
            correct_obs = sum(1 for i, o in history if o == model.items[i]["correct"])
            if correct_obs >= 2 and top_single_p < 0.30 and pm < 0.30:
                return ("none", None, 1.0 - top_single_p)
            if pm >= 0.30 and single_mass <= 0.65 and len(history) >= 3:
                pair, _ = model.top_pair(post)
                if pair is not None:
                    ca, cb = model.pair_member_counts(history, pair)
                    wrong_obs = sum(1 for i, o in history if o != model.items[i]["correct"])
                    pair_better = model.single_pair_margin(post, history) <= -math.log(1.5)
                    pair_beats_slip = model.pair_slip_margin(history, pair) >= math.log(10.0)
                    if min(ca, cb) >= 1 and wrong_obs >= 2 and pair_better and pair_beats_slip:
                        return ("mixed", None, pm)
    return None


def _verification_ok(model: BankModel, post: np.ndarray, cand: tuple[str, str | None, float],
                     item_idx: int, outcome: str) -> bool:
    kind, cid, _ = cand
    if kind == "single":
        return model.effective_pred(item_idx, cid) == outcome
    if kind == "pair":
        pair, pp = model.top_pair(post)
        if pair != cid or pp < 0.5:
            return False
        a, b = cid.split("|")[1:]
        preds = {model.effective_pred(item_idx, a), model.effective_pred(item_idx, b)}
        if outcome not in preds:
            return False
        # a single member matching the outcome must not explain it better than the pair
        single, _ = model.top_single(post)
        ll_pair = model.malrule_loglik(item_idx, cid, outcome)
        ll_single = model.malrule_loglik(item_idx, single, outcome)
        return ll_pair >= ll_single
    return model.none_mass(post) >= 0.8


def _select(model: BankModel, post: np.ndarray, available: list[int], selection: str,
            cand: tuple[str, str | None, float] | None = None) -> int:
    if selection == "targeted":
        if cand:
            return model.select_targeted(post, available, cand[0], cand[1])
        return model.select_targeted(post, available)
    if selection == "ig":
        return model.select_ig(post, available)
    return model.select_maxent(post, available)


def run_episode(model: BankModel, prior: np.ndarray, case: dict, student_type: str,
                stop_rule: str, selection: str = "maxent", on_budget: str = "abstain",
                partner: str | None = None, seed: int = 0, eps: float = 0.05,
                max_obs: int = 7) -> V5Result | None:
    true_id = case["true_id"]
    item_idx = int(case["item_idx"])
    item = model.items[item_idx]
    answer = case["answer"]
    if answer not in item["answers"]:
        return None
    if student_type == "slip" and answer == item["correct"]:
        return None
    if student_type in ("stable", "mixed") and model.effective_pred(item_idx, true_id) != answer:
        return None
    if student_type in ("stable", "mixed") and true_id not in model.index:
        return None

    true_pair = None
    if student_type == "mixed":
        if partner is None or partner == true_id or partner not in model.index:
            partner = _choose_partner(model, case, seed)
        if partner is None:
            return None
        true_pair = pair_id(true_id, partner)

    post = prior.copy()
    history = [(item_idx, answer)]
    used = {item_idx}
    verifications = 0
    stopped = False
    budget_exhausted = False
    terminal = None
    single_banned = False
    verify_streak: dict[str, int] = {}

    while True:
        if len(history) >= max_obs:
            budget_exhausted = True
            break
        if stop_rule == "fixed3" and len(history) >= 4:
            terminal = _terminal_from_posterior(model, post, allow_pairs=False)
            stopped = True
            break

        cand = _stop_check(model, post, history, stop_rule)
        if cand and single_banned and cand[0] == "single":
            cand = None
        if cand:
            heldout = stop_rule in ("stability_mixed_heldout", "stability_mixed_conditional")
            if heldout and cand[0] in ("single", "pair"):
                if (
                    stop_rule == "stability_mixed_conditional"
                    and cand[0] == "single"
                    and model.single_pair_margin(post, history) >= math.log(2.0)
                    and model.single_single_margin(post, history) >= math.log(2.0)
                    and model.mass_on_pairs(post) < 0.20
                ):
                    terminal = cand
                    stopped = True
                    break
                if verifications < 2:
                    available = [i for i in range(len(model.items)) if i not in used]
                    if not available:
                        break
                    vidx = model.select_targeted(post, available, cand[0], cand[1])
                    voutcome = observe(model, student_type, vidx, true_id, true_pair, case["case_id"], seed, eps)
                    used.add(vidx)
                    history.append((vidx, voutcome))
                    post = model.update(post, vidx, voutcome)
                    verifications += 1
                    key = f"{cand[0]}:{cand[1]}"
                    if _verification_ok(model, post, cand, vidx, voutcome):
                        verify_streak[key] = verify_streak.get(key, 0) + 1
                        required = 2 if cand[0] == "single" else 1
                        if verify_streak[key] >= required:
                            terminal = cand
                            stopped = True
                            break
                        continue
                    verify_streak[key] = 0
                    if cand[0] == "single":
                        single_banned = True
                    continue
                break
            terminal = cand
            stopped = True
            break

        available = [i for i in range(len(model.items)) if i not in used]
        if not available:
            budget_exhausted = True
            break
        nidx = _select(model, post, available, selection, cand)
        outcome = observe(model, student_type, nidx, true_id, true_pair, case["case_id"], seed, eps)
        used.add(nidx)
        history.append((nidx, outcome))
        post = model.update(post, nidx, outcome)

    if terminal is None:
        if stop_rule in ("fixed3", "posterior", "entropy") and on_budget == "force":
            terminal = _terminal_from_posterior(model, post, allow_pairs=False)
        elif stop_rule in ("stability", "stability_mixed"):
            cand = _stop_check(model, post, history, stop_rule)
            if cand and single_banned and cand[0] == "single":
                cand = None
            terminal = cand if cand else ("abstain", None, float(post.max()))
        else:
            terminal = ("abstain", None, float(post.max()))

    kind, tid, tp = terminal
    return V5Result(
        rule=stop_rule,
        selection=selection,
        student_type=student_type,
        case_id=case["case_id"],
        family=case.get("family") or case.get("template_family") or str(case.get("library_template")),
        category=case["category"],
        true_id=true_id if student_type == "stable" else None,
        true_pair=true_pair,
        terminal_kind=kind,
        terminal_id=tid,
        terminal_p=tp,
        n_obs=len(history),
        stopped=stopped,
        budget_exhausted=budget_exhausted,
        verifications=verifications,
        history=[(model.items[i]["text"], o) for i, o in history],
    )


def run_budget_episode(model: BankModel, prior: np.ndarray, case: dict, student_type: str,
                       policy: str, k: int, partner: str | None = None, seed: int = 0,
                       eps: float = 0.05) -> V5Result | None:
    true_id = case["true_id"]
    item_idx = int(case["item_idx"])
    item = model.items[item_idx]
    answer = case["answer"]
    if answer not in item["answers"]:
        return None
    if student_type == "slip" and answer == item["correct"]:
        return None
    if student_type in ("stable", "mixed") and model.effective_pred(item_idx, true_id) != answer:
        return None
    if student_type in ("stable", "mixed") and true_id not in model.index:
        return None
    true_pair = None
    if student_type == "mixed":
        if partner is None or partner == true_id or partner not in model.index:
            partner = _choose_partner(model, case, seed)
        if partner is None:
            return None
        true_pair = pair_id(true_id, partner)

    post = prior.copy()
    history = [(item_idx, answer)]
    used = {item_idx}
    for _ in range(k):
        available = [i for i in range(len(model.items)) if i not in used]
        if not available:
            break
        if policy == "random":
            rng = _case_rng(case["case_id"], seed, -1, student_type, "selection")
            nidx = rng.choice(available)
        elif policy == "fixed":
            nidx = available[0]
        elif policy == "ig":
            nidx = model.select_ig(post, available)
        else:
            nidx = model.select_maxent(post, available)
        outcome = observe(model, student_type, nidx, true_id, true_pair, case["case_id"], seed, eps)
        used.add(nidx)
        history.append((nidx, outcome))
        post = model.update(post, nidx, outcome)
    kind, tid, tp = _terminal_from_posterior(model, post, allow_pairs=False)
    return V5Result(
        rule=f"{policy}_k{k}",
        selection=policy,
        student_type=student_type,
        case_id=case["case_id"],
        family=case.get("family") or case.get("template_family") or str(case.get("library_template")),
        category=case["category"],
        true_id=true_id if student_type == "stable" else None,
        true_pair=true_pair,
        terminal_kind=kind,
        terminal_id=tid,
        terminal_p=tp,
        n_obs=len(history),
        stopped=False,
        budget_exhausted=True,
        verifications=0,
        history=[(model.items[i]["text"], o) for i, o in history],
    )


def one_shot_episode(model: BankModel, prior: np.ndarray, case: dict, student_type: str,
                     partner: str | None = None, seed: int = 0, typed: bool = False,
                     prior_meta: dict | None = None) -> V5Result | None:
    true_id = case["true_id"]
    item_idx = int(case["item_idx"])
    item = model.items[item_idx]
    answer = case["answer"]
    if answer not in item["answers"]:
        return None
    if student_type == "slip" and answer == item["correct"]:
        return None
    if student_type in ("stable", "mixed") and model.effective_pred(item_idx, true_id) != answer:
        return None
    true_pair = None
    if student_type == "mixed":
        if partner is None or partner == true_id or partner not in model.index:
            partner = _choose_partner(model, case, seed)
        if partner is None:
            return None
        true_pair = pair_id(true_id, partner)

    h, p = model.top_single(prior)
    kind, tid, tp = "single", h, p
    if typed:
        meta = prior_meta or {}
        declared = str(meta.get("stable_or_mixed") or "unsure").strip().lower()
        if declared in ("slip", "one_off", "one-off"):
            kind, tid, tp = "none", None, float(p)
        elif declared in ("mixed", "mixture"):
            top2 = [x for x in (meta.get("top10") or []) if x in model.index][:2]
            if len(top2) >= 2 and pair_id(top2[0], top2[1]) in model.index:
                kind, tid, tp = "pair", pair_id(top2[0], top2[1]), float(p)
            else:
                kind, tid, tp = "mixed", None, float(p)
        elif declared in ("stable", "single"):
            kind, tid, tp = "single", h, p
        else:
            kind, tid, tp = "abstain", None, float(p)
    return V5Result(
        rule="one_shot_typed" if typed else "one_shot_forced",
        selection="none",
        student_type=student_type,
        case_id=case["case_id"],
        family=case.get("family") or case.get("template_family") or str(case.get("library_template")),
        category=case["category"],
        true_id=true_id if student_type == "stable" else None,
        true_pair=true_pair,
        terminal_kind=kind,
        terminal_id=tid,
        terminal_p=tp,
        n_obs=1,
        stopped=False,
        budget_exhausted=False,
        verifications=0,
        history=[],
    )


def aggregate(results: list[V5Result]) -> dict:
    n = len(results)
    if not n:
        return {"n": 0}
    st = results[0].student_type
    false_rate = sum(r.false_remediation for r in results) / n
    out = {
        "n": n,
        "avg_obs": sum(r.n_obs for r in results) / n,
        "avg_inquiries": sum(r.n_inquiries for r in results) / n,
        "stop_rate": sum(r.stopped for r in results) / n,
        "budget_exhausted_rate": sum(r.budget_exhausted for r in results) / n,
        "abstain_rate": sum(r.abstain for r in results) / n,
        "none_rate": sum(r.explicit_none for r in results) / n,
        "single_rate": sum(r.terminal_kind == "single" for r in results) / n,
        "pair_rate": sum(r.terminal_kind == "pair" for r in results) / n,
        "mixed_unspecified_rate": sum(r.terminal_kind == "mixed" for r in results) / n,
        "diagnosed_rate": sum(r.diagnosed for r in results) / n,
        "coverage": sum(r.diagnosed for r in results) / n,
        "correct_rate": sum(r.correct for r in results) / n,
        "false_remediation_rate": false_rate,
        "J_lambda5": sum(r.n_obs for r in results) / n + 5.0 * false_rate,
        "J_lambda10": sum(r.n_obs for r in results) / n + 10.0 * false_rate,
        "avg_verifications": sum(r.verifications for r in results) / n,
    }
    if st == "stable":
        singles = [r for r in results if r.terminal_kind == "single"]
        out["stable_correct_stop"] = sum(r.stopped and r.correct for r in results) / n
        out["stable_correct_diagnosed"] = sum(r.correct for r in results) / n
        out["stable_diagnosed_error_rate"] = (
            sum(r.terminal_id != r.true_id for r in singles) / len(singles) if singles else None
        )
        out["stable_wrong_single_rate"] = sum(r.terminal_kind == "single" and not r.correct for r in results) / n
    if st == "slip":
        out["slip_error_rate"] = false_rate
        out["slip_explicit_none_rate"] = sum(r.explicit_none for r in results) / n
        out["slip_abstain_rate"] = sum(r.abstain for r in results) / n
        out["slip_remediation_error_rate"] = false_rate
    if st == "mixed":
        out["mixed_error_rate"] = false_rate
        out["mixed_detected_rate"] = sum(r.mixed_detected for r in results) / n
        out["pair_identified_rate"] = sum(r.pair_identified for r in results) / n
        out["single_commit_rate"] = sum(r.terminal_kind == "single" for r in results) / n
        out["wrong_pair_rate"] = sum(r.terminal_kind == "pair" and not r.pair_identified for r in results) / n
        out["mixed_none_rate"] = sum(r.explicit_none for r in results) / n
        out["mixed_abstain_rate"] = sum(r.abstain for r in results) / n
    return out


# ---------------------------------------------------------------- bootstrap
def _case_metric(results: list[V5Result], metric: str) -> dict[tuple[str, str], float]:
    """case_id -> mean over seeds for one metric."""
    by = {}
    for r in results:
        by.setdefault(r.case_id, []).append(r)
    out = {}
    for cid, rows in by.items():
        n = len(rows)
        if metric in ("correct", "false", "diagnosed"):
            key = {"correct": "correct", "false": "false_remediation", "diagnosed": "diagnosed"}[metric]
            out[cid] = sum(bool(getattr(r, key)) for r in rows) / n
        elif metric == "n_obs":
            out[cid] = sum(r.n_obs for r in rows) / n
        elif metric == "n_inquiries":
            out[cid] = sum(r.n_inquiries for r in rows) / n
        elif metric == "J5":
            out[cid] = sum(r.n_obs + 5.0 * float(r.false_remediation) for r in rows) / n
        elif metric == "J10":
            out[cid] = sum(r.n_obs + 10.0 * float(r.false_remediation) for r in rows) / n
        else:
            raise KeyError(metric)
    return out


def bootstrap_mean(results: list[V5Result], metric: str, n_boot: int = 2000, seed: int = 20261023):
    by_case = _case_metric(results, metric)
    family = {r.case_id: r.family for r in results}
    families = sorted({family[c] for c in by_case})
    if not families:
        return None, None, None
    def mean_for(fs):
        vals = [by_case[c] for c in by_case if family[c] in fs]
        return sum(vals) / len(vals) if vals else 0.0
    point = mean_for(set(families))
    rng = random.Random(seed)
    samples = []
    for _ in range(n_boot):
        chosen = {rng.choice(families) for _ in families}
        samples.append(mean_for(chosen))
    samples.sort()
    return point, samples[int(0.025 * len(samples))], samples[int(0.975 * len(samples)) - 1]


def bootstrap_diff(results_a: list[V5Result], results_b: list[V5Result], metric: str,
                   n_boot: int = 2000, seed: int = 20261023):
    a = _case_metric(results_a, metric)
    b = _case_metric(results_b, metric)
    family = {r.case_id: r.family for r in results_a}
    common = sorted(set(a) & set(b))
    families = sorted({family[c] for c in common})
    if not families:
        return None, None, None
    def mean_for(fs, vals):
        xs = [vals[c] for c in common if family[c] in fs]
        return sum(xs) / len(xs) if xs else 0.0
    point = mean_for(set(families), a) - mean_for(set(families), b)
    rng = random.Random(seed)
    samples = []
    for _ in range(n_boot):
        chosen = {rng.choice(families) for _ in families}
        samples.append(mean_for(chosen, a) - mean_for(chosen, b))
    samples.sort()
    return point, samples[int(0.025 * len(samples))], samples[int(0.975 * len(samples)) - 1]
