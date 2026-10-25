"""Stopping-criterion ablation on the frozen v5 test set.

All arms use the same pair-augmented hypothesis space, category-conditioned
prior, MaxEnt item selection, noise level, seeds, and observation budget.
Only the single-misconception stopping gates differ.

The full-SM arm dispatches to the frozen v5 engine's original stop check, so
it can be compared episode-by-episode against the published v5 episodes.
"""
from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable

import numpy as np

import v5_engine as eng


STUDENT_TYPES = ("stable", "slip", "mixed")

ARM_SPECS = {
    # Posterior concentration only: same posterior thresholds and hypothesis
    # mass constraints as SM, but no consistent-error, slip-LR, or pair guard.
    "posterior_only": {
        "use_E": False,
        "use_LR": False,
        "use_pair_guard": False,
        "full_sm": False,
    },
    "posterior_plus_E": {
        "use_E": True,
        "use_LR": False,
        "use_pair_guard": False,
        "full_sm": False,
    },
    "posterior_plus_LR": {
        "use_E": False,
        "use_LR": True,
        "use_pair_guard": False,
        "full_sm": False,
    },
    "posterior_plus_E_LR": {
        "use_E": True,
        "use_LR": True,
        "use_pair_guard": False,
        "full_sm": False,
    },
    "posterior_plus_E_LR_pairguard": {
        "use_E": True,
        "use_LR": True,
        "use_pair_guard": True,
        "full_sm": False,
    },
    "stability_mixed_reference": {
        "use_E": True,
        "use_LR": True,
        "use_pair_guard": True,
        "full_sm": True,
    },
}

DEFAULT_ARM_ORDER = list(ARM_SPECS)

POSTERIOR = {
    "top1_cond": 0.80,
    "margin_cond": 0.20,
    "single_mass": 0.40,
    "pair_ceiling": 0.20,
    "none_ceiling": 0.15,
}
MIN_CONSISTENT_WRONG = 2
LR_SLIP_THRESHOLD = 10.0
PAIR_GUARD_MARGIN = -math.log(1.5)

METRICS = (
    "correct",
    "correct_stop",
    "false",
    "diagnosed",
    "abstain",
    "none",
    "single",
    "wrong_single",
    "n_inquiries",
    "J5",
    "J10",
)


def episode_metric(e: dict, metric: str) -> float:
    if metric == "correct":
        return float(bool(e["correct"]))
    if metric == "correct_stop":
        return float(bool(e["stopped"] and e["correct"]))
    if metric == "false":
        return float(bool(e["false_remediation"]))
    if metric == "diagnosed":
        return float(e["terminal_kind"] in ("single", "pair", "mixed"))
    if metric == "abstain":
        return float(e["terminal_kind"] == "abstain")
    if metric == "none":
        return float(e["terminal_kind"] == "none")
    if metric == "single":
        return float(e["terminal_kind"] == "single")
    if metric == "wrong_single":
        return float(e["terminal_kind"] == "single" and not e["correct"])
    if metric == "n_inquiries":
        return float(e["n_inquiries"])
    if metric == "n_obs":
        return float(e["n_obs"])
    if metric == "J5":
        return float(e["J5"])
    if metric == "J10":
        return float(e["J10"])
    raise KeyError(metric)


def gate_state(model, post: np.ndarray, history: list[tuple[int, str]]) -> dict:
    single, p1 = model.top_single(post)
    probs = post[model.single_idx]
    order = np.argsort(-probs)
    p2 = float(probs[order[1]]) if len(order) > 1 else 0.0
    single_mass = float(probs.sum())
    p1_cond = p1 / single_mass if single_mass > 1e-9 else 0.0
    p2_cond = p2 / single_mass if single_mass > 1e-9 else 0.0
    pair_mass = float(model.mass_on_pairs(post))
    none_mass = float(model.none_mass(post))

    posterior_ok = (
        p1_cond >= POSTERIOR["top1_cond"]
        and (p1_cond - p2_cond) >= POSTERIOR["margin_cond"]
        and single_mass >= POSTERIOR["single_mass"]
        and pair_mass <= POSTERIOR["pair_ceiling"]
        and none_mass <= POSTERIOR["none_ceiling"]
    )

    consistent = sum(
        1 for item_idx, outcome in history
        if model.consistent_wrong(item_idx, single, outcome)
    )
    ll_m = sum(model.malrule_loglik(i, single, o) for i, o in history)
    ll_slip = sum(model.slip_loglik(i, o) for i, o in history)
    log_lr_slip = ll_m - ll_slip

    pair, pair_p = model.top_pair(post)
    pair_guard_ok = True
    ll_pair = None
    if pair is not None and pair_p >= 0.05:
        ll_pair = sum(model.malrule_loglik(i, pair, o) for i, o in history)
        pair_guard_ok = (ll_m - ll_pair) >= PAIR_GUARD_MARGIN

    e_pass = consistent >= MIN_CONSISTENT_WRONG
    lr_pass = log_lr_slip >= math.log(LR_SLIP_THRESHOLD)

    return {
        "single": single,
        "p1": float(p1),
        "p1_cond": float(p1_cond),
        "p2_cond": float(p2_cond),
        "single_mass": single_mass,
        "pair_mass": pair_mass,
        "none_mass": none_mass,
        "posterior_ok": bool(posterior_ok),
        "consistent_wrong": int(consistent),
        "E_pass": bool(e_pass),
        "log_lr_slip": float(log_lr_slip),
        "lr_slip": float(math.exp(min(50.0, log_lr_slip))),
        "LR_pass": bool(lr_pass),
        "top_pair": pair,
        "top_pair_p": float(pair_p),
        "pair_guard_ok": bool(pair_guard_ok),
    }


def stop_check(
    model,
    post: np.ndarray,
    history: list[tuple[int, str]],
    arm: str,
    trace: list[dict] | None = None,
) -> tuple[str, str | None, float] | None:
    spec = ARM_SPECS[arm]
    if spec["full_sm"]:
        return eng._stop_check(model, post, history, "stability_mixed")

    g = gate_state(model, post, history)
    if g["posterior_ok"]:
        if trace is not None:
            trace.append({"step": len(history), **g})
        gates = []
        if spec["use_E"] and not g["E_pass"]:
            gates.append("E")
        if spec["use_LR"] and not g["LR_pass"]:
            gates.append("LR")
        if spec["use_pair_guard"] and not g["pair_guard_ok"]:
            gates.append("pair_guard")
        if not gates:
            return ("single", g["single"], g["p1"])

    if model.no_misconception_candidate(post, history, threshold=0.8):
        return ("none", None, model.none_mass(post))
    return None


def run_episode_ablation(
    model,
    prior: np.ndarray,
    case: dict,
    student_type: str,
    arm: str,
    partner: str | None = None,
    seed: int = 0,
    eps: float = 0.05,
    max_obs: int = 7,
    trace: list[dict] | None = None,
    process=None,
):
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
            partner = eng._choose_partner(model, case, seed)
        if partner is None:
            return None
        true_pair = eng.pair_id(true_id, partner)

    post = prior.copy()
    history = [(item_idx, answer)]
    used = {item_idx}
    stopped = False
    budget_exhausted = False
    terminal = None

    while True:
        if len(history) >= max_obs:
            budget_exhausted = True
            break

        cand = stop_check(model, post, history, arm, trace)
        if cand:
            terminal = cand
            stopped = True
            break

        available = [i for i in range(len(model.items)) if i not in used]
        if not available:
            budget_exhausted = True
            break

        nidx = model.select_maxent(post, available)
        outcome = eng.observe(
            model, student_type, nidx, true_id, true_pair,
            case["case_id"], seed, eps, process,
        )
        used.add(nidx)
        history.append((nidx, outcome))
        post = model.update(post, nidx, outcome)

    if terminal is None:
        cand = stop_check(model, post, history, arm, trace)
        terminal = cand if cand else ("abstain", None, float(post.max()))

    kind, tid, tp = terminal
    return eng.V5Result(
        rule=arm,
        selection="maxent",
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
        verifications=0,
        history=[(model.items[i]["text"], o) for i, o in history],
        meta={"arm": arm},
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
        "true_pair": res.true_pair,
        "terminal_kind": res.terminal_kind,
        "terminal_id": res.terminal_id,
        "terminal_p": float(res.terminal_p),
        "n_obs": int(res.n_obs),
        "n_inquiries": int(res.n_inquiries),
        "stopped": bool(res.stopped),
        "budget_exhausted": bool(res.budget_exhausted),
        "correct": bool(res.correct),
        "false_remediation": bool(res.false_remediation),
        "seed": int(seed),
        "J5": float(res.n_obs + 5.0 * float(res.false_remediation)),
        "J10": float(res.n_obs + 10.0 * float(res.false_remediation)),
    }


def case_means(episodes: Iterable[dict], metric: str) -> dict[str, float]:
    by_case = defaultdict(list)
    for e in episodes:
        by_case[e["case_id"]].append(episode_metric(e, metric))
    return {cid: float(np.mean(vals)) for cid, vals in by_case.items()}


class ClusterBoot:
    """Template-family bootstrap with replacement and multiplicity."""

    def __init__(self, family_of_case: dict[str, str], n_boot: int = 2000, seed: int = 20261026):
        self.family_of_case = family_of_case
        self.n_boot = n_boot
        self.seed = seed

    def _draw_counts(self, families: list[str]) -> np.ndarray:
        rng = np.random.default_rng(self.seed)
        idx = rng.integers(0, len(families), size=(self.n_boot, len(families)))
        counts = np.zeros((self.n_boot, len(families)), dtype=float)
        for b in range(self.n_boot):
            counts[b] = np.bincount(idx[b], minlength=len(families))
        return counts

    def _sums(self, vals: dict[str, float], fam_index: dict[str, int]):
        s = np.zeros(len(fam_index), dtype=float)
        n = np.zeros(len(fam_index), dtype=float)
        for cid, v in vals.items():
            f = fam_index.get(self.family_of_case.get(cid))
            if f is None:
                continue
            s[f] += v
            n[f] += 1.0
        return s, n

    def mean_ci(self, vals: dict[str, float], families: list[str] | None = None):
        families = sorted(families or {self.family_of_case[c] for c in vals})
        fam_index = {f: i for i, f in enumerate(families)}
        s, n = self._sums(vals, fam_index)
        point = float(s.sum() / n.sum())
        counts = self._draw_counts(families)
        reps = (counts @ s) / (counts @ n)
        lo, hi = np.percentile(reps, [2.5, 97.5])
        return {"mean": point, "ci_low": float(lo), "ci_high": float(hi), "n_cases": len(vals)}

    def diff_ci(self, a: dict[str, float], b: dict[str, float], families: list[str] | None = None):
        common = sorted(set(a) & set(b))
        d = {c: a[c] - b[c] for c in common}
        return self.mean_ci(d, families=families)


def summarize_arm(episodes: list[dict], cb: ClusterBoot) -> dict:
    out = {}
    for metric in METRICS:
        vals = case_means(episodes, metric)
        out[metric] = cb.mean_ci(vals)
    out["n_cases"] = len({e["case_id"] for e in episodes})
    out["n_episodes"] = len(episodes)
    return out


def arm_contrasts(
    episodes_by_arm_type: dict[tuple[str, str], list[dict]],
    pairs: list[tuple[str, str]],
    metrics: list[str],
    cb: ClusterBoot,
) -> dict:
    out = {}
    for arm_a, arm_b in pairs:
        for st in STUDENT_TYPES:
            a = episodes_by_arm_type.get((arm_a, st))
            b = episodes_by_arm_type.get((arm_b, st))
            if not a or not b:
                continue
            key = f"{arm_a} - {arm_b}/{st}"
            out[key] = {}
            for metric in metrics:
                out[key][metric] = cb.diff_ci(case_means(a, metric), case_means(b, metric))
    return out


def gate_counterfactual(episodes_by_arm_type: dict[tuple[str, str], list[dict]],
                        traces: dict[tuple[str, str, str, int], list[dict]]) -> dict:
    """Gate states at posterior-only single-stop steps, split by student type."""
    out = {}
    for st in STUDENT_TYPES:
        rows = episodes_by_arm_type.get(("posterior_only", st), [])
        n_single = 0
        n_eligible = 0
        stats = {
            "single_stops": 0,
            "E_fail": 0,
            "LR_fail": 0,
            "pair_guard_fail": 0,
            "any_gate_fail": 0,
            "all_gates_pass": 0,
            "single_stops_correct": 0,
            "single_stops_wrong": 0,
            "E_fail_correct": 0,
            "E_fail_wrong": 0,
            "LR_fail_correct": 0,
            "LR_fail_wrong": 0,
            "any_fail_correct": 0,
            "any_fail_wrong": 0,
        }
        for e in rows:
            key = (e["arm"], e["case_id"], e["student_type"], e["seed"])
            tr = traces.get(key) or []
            if tr:
                n_eligible += 1
            if e["terminal_kind"] == "single":
                n_single += 1
                if not tr:
                    continue
                g = tr[0]
                stats["single_stops"] += 1
                is_correct = bool(e["correct"])
                stats["single_stops_correct" if is_correct else "single_stops_wrong"] += 1
                e_fail = not g["E_pass"]
                lr_fail = not g["LR_pass"]
                pair_fail = not g["pair_guard_ok"]
                if e_fail:
                    stats["E_fail"] += 1
                    stats["E_fail_correct" if is_correct else "E_fail_wrong"] += 1
                if lr_fail:
                    stats["LR_fail"] += 1
                    stats["LR_fail_correct" if is_correct else "LR_fail_wrong"] += 1
                if pair_fail:
                    stats["pair_guard_fail"] += 1
                if e_fail or lr_fail or pair_fail:
                    stats["any_gate_fail"] += 1
                    stats["any_fail_correct" if is_correct else "any_fail_wrong"] += 1
                if not (e_fail or lr_fail or pair_fail):
                    stats["all_gates_pass"] += 1
        stats["all_gates_pass_correct"] = max(
            0, stats["single_stops_correct"] - stats["any_fail_correct"]
        )
        stats["all_gates_pass_wrong"] = max(
            0, stats["single_stops_wrong"] - stats["any_fail_wrong"]
        )
        out[st] = {
            "n_episodes": len(rows),
            "n_posterior_eligible_episodes": n_eligible,
            "n_single_stops": n_single,
            **stats,
            "pct_E_fail": stats["E_fail"] / stats["single_stops"] if stats["single_stops"] else None,
            "pct_LR_fail": stats["LR_fail"] / stats["single_stops"] if stats["single_stops"] else None,
            "pct_pair_guard_fail": stats["pair_guard_fail"] / stats["single_stops"] if stats["single_stops"] else None,
            "pct_any_gate_fail": stats["any_gate_fail"] / stats["single_stops"] if stats["single_stops"] else None,
            "pct_all_gates_pass": stats["all_gates_pass"] / stats["single_stops"] if stats["single_stops"] else None,
            "pct_all_gates_pass_correct": stats["all_gates_pass_correct"] / stats["single_stops_correct"] if stats["single_stops_correct"] else None,
            "pct_all_gates_pass_wrong": stats["all_gates_pass_wrong"] / stats["single_stops_wrong"] if stats["single_stops_wrong"] else None,
        }
    return out
