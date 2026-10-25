"""E6-lite: one-factor-at-a-time threshold sensitivity for the frozen v5
stability_mixed/maxent stopping rule.

Design notes
------------
* All eight swept thresholds (u1, margin, S, P, N, E, LR, pair_guard) live in
  the single-misconception admission gate of the frozen stop rule. Everything
  else (explicit-none 0.8, extra-none 2/0.30/0.30, mixed-branch 0.30/0.65/3,
  pair-branch 0.6/0.5/0.2/pair_lr 2.0/pair_slip 10) stays at frozen values.
* Item selection under MaxEnt and the simulated outcomes (common random
  numbers) do not depend on the stopping thresholds. Therefore the full
  (posterior, history) trajectory of every episode up to the budget is
  threshold-independent and is precomputed once per (case, student type,
  seed, eps). Each threshold configuration is then evaluated on the recorded
  prefixes with earliest-fire semantics, which is exactly equivalent to
  re-running the engine.
* No logic in this module selects, ranks, or recommends thresholds. The sweep
  is descriptive only.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, replace
from typing import Iterable

import numpy as np

import v5_engine as eng

STUDENT_TYPES = ("stable", "slip", "mixed")

# Frozen defaults (v5 pre-registered values).
DEFAULTS = {
    "u1": 0.80,          # top-1 conditional posterior floor
    "margin": 0.20,      # conditional u1 - u2 margin
    "S": 0.40,           # single-hypothesis mass floor
    "P": 0.20,           # pair-mass ceiling in the single gate
    "N": 0.15,           # CORRECT+OTHER mass ceiling in the single gate
    "E": 2,              # min consistent wrong observations
    "LR": 10.0,          # slip likelihood-ratio threshold
    "pair_guard": 1.5,   # max allowed pair/single log-lik ratio (None = off)
}
# Fixed internal constants of the frozen rule (not swept here).
FIXED = {
    "none_threshold": 0.8,        # explicit none mass
    "extra_none_correct": 2,      # extra none: correct observations
    "extra_none_p1": 0.30,        # extra none: raw top-1 posterior ceiling
    "extra_none_pm": 0.30,        # extra none: pair mass ceiling
    "mixed_pm": 0.30,             # mixed branch: pair mass floor
    "mixed_single_mass": 0.65,    # mixed branch: single mass ceiling
    "mixed_min_hist": 3,          # mixed branch: min history length
    "mixed_pair_margin": -math.log(1.5),   # mixed branch: pair-better margin
    "mixed_pair_slip": math.log(10.0),     # mixed branch: pair-vs-slip LR
    "pair_pp": 0.6,               # pair branch: top-pair posterior floor
    "pair_pm": 0.5,               # pair branch: pair mass floor
    "pair_gap": 0.2,              # pair branch: pp - top single gap
    "pair_lr_single": 2.0,        # pair branch: pair-vs-single LR
    "pair_slip_lr": 10.0,         # pair branch: pair-vs-slip LR
}

GRID_ORDER = ["u1", "margin", "S", "P", "N", "E", "LR", "pair_guard"]
GRIDS = {
    "u1": [0.70, 0.75, 0.80, 0.85, 0.90],
    "margin": [0.10, 0.15, 0.20, 0.25, 0.30],
    "S": [0.30, 0.35, 0.40, 0.45, 0.50],
    "P": [0.10, 0.15, 0.20, 0.25, 0.30],
    "N": [0.05, 0.10, 0.15, 0.20, 0.25],
    "E": [1, 2, 3],
    "LR": [3.0, 5.0, 10.0, 30.0, 100.0],
    "pair_guard": ["off", 1.25, 1.5, 2.0, 3.0],
}

METRICS = (
    "correct",
    "correct_stop",
    "false",
    "diagnosed",
    "abstain",
    "none",
    "single",
    "pair_mixed",
    "wrong_single",
    "n_inquiries",
    "J5",
    "J10",
)


@dataclass(frozen=True)
class Thresholds:
    u1: float = DEFAULTS["u1"]
    margin: float = DEFAULTS["margin"]
    S: float = DEFAULTS["S"]
    P: float = DEFAULTS["P"]
    N: float = DEFAULTS["N"]
    E: int = DEFAULTS["E"]
    LR: float = DEFAULTS["LR"]
    pair_guard: float | None = DEFAULTS["pair_guard"]

    @property
    def config_id(self) -> str:
        if self == Thresholds():
            return "default"
        parts = []
        for k in GRID_ORDER:
            v = getattr(self, k)
            if v != DEFAULTS[k]:
                parts.append(f"{k}={'off' if v is None else v}")
        return "+".join(parts) if parts else "default"


def parse_config_id(cid: str) -> Thresholds:
    th = Thresholds()
    if cid in ("", "default"):
        return th
    for part in cid.split("+"):
        k, v = part.split("=", 1)
        if k not in GRID_ORDER:
            raise KeyError(k)
        cur = DEFAULTS[k]
        if v == "off":
            val = None
        elif isinstance(cur, int) and not isinstance(cur, bool):
            val = int(v)
        else:
            val = float(v)
        th = replace(th, **{k: val})
    return th


def grid_configs() -> list[Thresholds]:
    """OFAT configurations: default + one perturbation per grid value."""
    out = [Thresholds()]
    for k in GRID_ORDER:
        for v in GRIDS[k]:
            if v == DEFAULTS[k]:
                continue
            val = None if v == "off" else v
            out.append(replace(Thresholds(), **{k: val}))
    return out


# ---------------------------------------------------------------- step states


def step_state(model, post: np.ndarray, history: list[tuple[int, str]]) -> dict:
    """All stopping-relevant quantities at one step (threshold-independent)."""
    single, p1 = model.top_single(post)
    probs = post[model.single_idx]
    order = np.argsort(-probs)
    p2 = float(probs[order[1]]) if len(order) > 1 else 0.0
    single_mass = float(probs.sum())
    p1_cond = p1 / single_mass if single_mass > 1e-9 else 0.0
    p2_cond = p2 / single_mass if single_mass > 1e-9 else 0.0
    pm = model.mass_on_pairs(post)
    nm = model.none_mass(post)

    consistent = sum(1 for i, o in history if model.consistent_wrong(i, single, o))
    ll_m = sum(model.malrule_loglik(i, single, o) for i, o in history)
    ll_s = sum(model.slip_loglik(i, o) for i, o in history)
    log_lr = ll_m - ll_s

    pair, pp = model.top_pair(post)
    ll_pair = None
    if pair is not None and pp >= 0.05:
        ll_pair = sum(model.malrule_loglik(i, pair, o) for i, o in history)
    ca, cb = model.pair_member_counts(history, pair) if pair is not None else (0, 0)
    wrong_obs = sum(1 for i, o in history if o != model.items[i]["correct"])
    correct_obs = sum(1 for i, o in history if o == model.items[i]["correct"])
    # single_pair_margin returns +inf when the top pair posterior < .05; the
    # mixed branch treats that as failing the pair-better check.
    spm = model.single_pair_margin(post, history)
    psm = model.pair_slip_margin(history, pair) if pair is not None else -math.inf
    return {
        "t": len(history),
        "single": single,
        "p1": float(p1),
        "p1_cond": float(p1_cond),
        "p2_cond": float(p2_cond),
        "single_mass": single_mass,
        "pm": float(pm),
        "nm": float(nm),
        "pair": pair,
        "pp": float(pp),
        "consistent": int(consistent),
        "log_lr": float(log_lr),
        "ll_pair": ll_pair,
        "ll_m": float(ll_m),
        "ll_s": float(ll_s),
        "min_ca_cb": int(min(ca, cb)),
        "wrong_obs": int(wrong_obs),
        "correct_obs": int(correct_obs),
        "spm": (float(spm) if math.isfinite(spm) else math.inf),
        "psm": (float(psm) if math.isfinite(psm) else -math.inf),
        "post_max": float(post.max()),
    }


def stop_from_state(s: dict, th: Thresholds) -> tuple[str, str | None, float] | None:
    """Parameterised copy of v5 `_stop_check("stability_mixed")`.

    Order matters and mirrors the frozen rule: single gate (incl. pair branch
    of stability_candidate) -> explicit none -> extra none -> mixed branch.
    """
    ll_m = s["ll_m"]
    # single gate of stability_candidate
    single_beats_pair = True
    if s["ll_pair"] is not None:
        if th.pair_guard is None:
            single_beats_pair = True
        else:
            single_beats_pair = (ll_m - s["ll_pair"]) >= -math.log(th.pair_guard)
    if (
        s["p1_cond"] >= th.u1
        and (s["p1_cond"] - s["p2_cond"]) >= th.margin
        and s["single_mass"] >= th.S
        and s["pm"] <= th.P
        and s["nm"] <= th.N
        and s["consistent"] >= th.E
        and s["log_lr"] >= math.log(th.LR)
        and single_beats_pair
    ):
        return ("single", s["single"], s["p1"])

    # pair branch of stability_candidate (fixed thresholds)
    if (
        s["pair"] is not None
        and s["ll_pair"] is not None
        and s["pp"] >= FIXED["pair_pp"]
        and s["pm"] >= FIXED["pair_pm"]
        and (s["pp"] - s["p1"]) >= FIXED["pair_gap"]
        and s["t"] >= 2
        and s["min_ca_cb"] >= 1
        and s["wrong_obs"] >= 2
        and (s["ll_pair"] - ll_m) >= math.log(FIXED["pair_lr_single"])
        and (s["ll_pair"] - s["ll_s"]) >= math.log(FIXED["pair_slip_lr"])
    ):
        return ("pair", s["pair"], s["pp"])

    # explicit none (fixed 0.8, min 2 observations)
    if s["nm"] >= FIXED["none_threshold"] and s["t"] >= 2:
        return ("none", None, s["nm"])

    # extra none rule (fixed 2 / .30 / .30)
    if s["correct_obs"] >= FIXED["extra_none_correct"] and s["p1"] < FIXED["extra_none_p1"] and s["pm"] < FIXED["extra_none_pm"]:
        return ("none", None, 1.0 - s["p1"])

    # mixed branch (fixed .30 / .65 / 3 + pair admission guards)
    if s["pm"] >= FIXED["mixed_pm"] and s["single_mass"] <= FIXED["mixed_single_mass"] and s["t"] >= FIXED["mixed_min_hist"]:
        if (
            s["pair"] is not None
            and s["min_ca_cb"] >= 1
            and s["wrong_obs"] >= 2
            and s["spm"] <= FIXED["mixed_pair_margin"]
            and s["psm"] >= FIXED["mixed_pair_slip"]
        ):
            return ("mixed", None, s["pm"])
    return None


# ---------------------------------------------------------------- trajectories


def _eligible(model, case: dict, student_type: str, seed: int) -> tuple[bool, str | None]:
    item_idx = int(case["item_idx"])
    item = model.items[item_idx]
    answer = case["answer"]
    true_id = case["true_id"]
    if answer not in item["answers"]:
        return False, "answer_not_in_answers"
    if student_type == "slip" and answer == item["correct"]:
        return False, "slip_correct_answer"
    if student_type in ("stable", "mixed"):
        if model.effective_pred(item_idx, true_id) != answer:
            return False, "pred_mismatch"
        if true_id not in model.index:
            return False, "true_id_not_in_index"
    return True, None


def precompute_trajectory(model, prior: np.ndarray, case: dict, student_type: str,
                          seed: int, eps: float, max_obs: int = 7) -> dict | None:
    """Threshold-independent episode trajectory under MaxEnt selection.

    Mirrors v5_engine.run_episode for stop_rule="stability_mixed",
    selection="maxent", on_budget="abstain" (no verification loop), but never
    stops: it records the stop-check state at every step t=1..max_obs.
    """
    ok, _ = _eligible(model, case, student_type, seed)
    if not ok:
        return None

    true_id = case["true_id"]
    true_pair = None
    if student_type == "mixed":
        partner = eng._choose_partner(model, case, seed)
        if partner is None:
            return None
        true_pair = eng.pair_id(true_id, partner)

    post = prior.copy()
    history = [(int(case["item_idx"]), case["answer"])]
    used = {int(case["item_idx"])}
    steps = [step_state(model, post, history)]
    while len(history) < max_obs:
        available = [i for i in range(len(model.items)) if i not in used]
        if not available:
            break
        nidx = model.select_maxent(post, available)
        outcome = eng.observe(model, student_type, nidx, true_id, true_pair,
                              case["case_id"], seed, eps)
        used.add(nidx)
        history.append((nidx, outcome))
        post = model.update(post, nidx, outcome)
        steps.append(step_state(model, post, history))
    return {
        "case_id": case["case_id"],
        "student_type": student_type,
        "seed": seed,
        "family": case.get("family") or case.get("template_family") or str(case.get("library_template")),
        "category": case["category"],
        "true_id": true_id if student_type == "stable" else None,
        "true_pair": true_pair,
        "steps": steps,
    }


def evaluate_trajectory(traj: dict, th: Thresholds, max_obs: int = 7) -> dict:
    """Earliest-fire evaluation of one threshold config on a recorded trajectory.

    Stopping fired during the loop (t <= max_obs-1) counts as `stopped=True`;
    a candidate only at the budget-time final check (t == max_obs) keeps
    stopped=False with budget_exhausted=True, matching the frozen engine.
    """
    for s in traj["steps"]:
        cand = stop_from_state(s, th)
        if cand:
            kind, tid, tp = cand
            return _episode_dict(traj, kind, tid, tp, n_obs=s["t"],
                                 stopped=s["t"] < max_obs,
                                 budget_exhausted=s["t"] == max_obs)
    last = traj["steps"][-1]
    return _episode_dict(traj, "abstain", None, last["post_max"],
                         n_obs=last["t"], stopped=False, budget_exhausted=True)


def _episode_dict(traj: dict, kind: str, tid: str | None, tp: float,
                  n_obs: int, stopped: bool, budget_exhausted: bool) -> dict:
    st = traj["student_type"]
    if st == "stable":
        correct = kind == "single" and tid == traj["true_id"]
        false = kind == "single" and tid != traj["true_id"]
    elif st == "slip":
        correct = kind in ("none", "abstain")
        false = kind in ("single", "pair", "mixed")
    else:
        correct = kind == "pair" and tid == traj["true_pair"]
        false = kind == "single" or (kind == "pair" and tid != traj["true_pair"])
    return {
        "case_id": traj["case_id"],
        "student_type": st,
        "seed": traj["seed"],
        "family": traj["family"],
        "category": traj["category"],
        "terminal_kind": kind,
        "terminal_id": tid,
        "terminal_p": float(tp),
        "n_obs": int(n_obs),
        "n_inquiries": int(n_obs - 1),
        "stopped": bool(stopped),
        "budget_exhausted": bool(budget_exhausted),
        "correct": bool(correct),
        "false_remediation": bool(false),
        "J5": float(n_obs + 5.0 * float(false)),
        "J10": float(n_obs + 10.0 * float(false)),
    }


def run_episode_th(model, prior: np.ndarray, case: dict, student_type: str,
                   th: Thresholds, seed: int = 0, eps: float = 0.05,
                   max_obs: int = 7) -> dict | None:
    """Reference slow path: actual engine loop with the parameterised check.

    Used only to validate the prefix/earliest-fire evaluation; not for sweeps.
    """
    ok, _ = _eligible(model, case, student_type, seed)
    if not ok:
        return None
    true_id = case["true_id"]
    true_pair = None
    if student_type == "mixed":
        partner = eng._choose_partner(model, case, seed)
        if partner is None:
            return None
        true_pair = eng.pair_id(true_id, partner)

    post = prior.copy()
    history = [(int(case["item_idx"]), case["answer"])]
    used = {int(case["item_idx"])}
    stopped = False
    budget_exhausted = False
    terminal = None
    while True:
        if len(history) >= max_obs:
            budget_exhausted = True
            break
        cand = stop_from_state(step_state(model, post, history), th)
        if cand:
            terminal = cand
            stopped = True
            break
        available = [i for i in range(len(model.items)) if i not in used]
        if not available:
            budget_exhausted = True
            break
        nidx = model.select_maxent(post, available)
        outcome = eng.observe(model, student_type, nidx, true_id, true_pair,
                              case["case_id"], seed, eps)
        used.add(nidx)
        history.append((nidx, outcome))
        post = model.update(post, nidx, outcome)
    if terminal is None:
        cand = stop_from_state(step_state(model, post, history), th)
        terminal = cand if cand else ("abstain", None, float(post.max()))
    kind, tid, tp = terminal
    return _episode_dict({"case_id": case["case_id"], "student_type": student_type,
                          "seed": seed, "family": case.get("family") or case.get("template_family"),
                          "category": case["category"], "true_id": true_id if student_type == "stable" else None,
                          "true_pair": true_pair},
                         kind, tid, tp, n_obs=len(history), stopped=stopped,
                         budget_exhausted=budget_exhausted)


# ---------------------------------------------------------------- statistics


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
    if metric == "pair_mixed":
        return float(e["terminal_kind"] in ("pair", "mixed"))
    if metric == "wrong_single":
        return float(e["terminal_kind"] == "single" and not e["correct"])
    if metric == "n_inquiries":
        return float(e["n_inquiries"])
    if metric == "J5":
        return float(e["J5"])
    if metric == "J10":
        return float(e["J10"])
    raise KeyError(metric)


def case_means(episodes: Iterable[dict], metric: str) -> dict[str, float]:
    by_case: dict[str, list[float]] = {}
    for e in episodes:
        by_case.setdefault(e["case_id"], []).append(episode_metric(e, metric))
    return {cid: float(np.mean(v)) for cid, v in by_case.items()}


class ClusterBoot:
    """Template-family bootstrap with replacement and multiplicity."""

    def __init__(self, family_of_case: dict[str, str], n_boot: int = 2000, seed: int = 20261027):
        self.family_of_case = family_of_case
        self.n_boot = n_boot
        self.seed = seed
        self._counts: dict[tuple, np.ndarray] = {}

    def _draw_counts(self, families: list[str]) -> np.ndarray:
        key = tuple(families)
        cached = self._counts.get(key)
        if cached is not None:
            return cached
        rng = np.random.default_rng(self.seed)
        idx = rng.integers(0, len(families), size=(self.n_boot, len(families)))
        counts = np.zeros((self.n_boot, len(families)), dtype=float)
        for b in range(self.n_boot):
            counts[b] = np.bincount(idx[b], minlength=len(families))
        self._counts[key] = counts
        return counts

    def mean_ci(self, vals: dict[str, float], families: list[str] | None = None) -> dict:
        families = sorted(families or {self.family_of_case[c] for c in vals})
        fam_index = {f: i for i, f in enumerate(families)}
        s = np.zeros(len(families))
        n = np.zeros(len(families))
        for cid, v in vals.items():
            f = fam_index.get(self.family_of_case.get(cid))
            if f is None:
                continue
            s[f] += v
            n[f] += 1.0
        point = float(s.sum() / n.sum())
        counts = self._draw_counts(families)
        reps = (counts @ s) / (counts @ n)
        lo, hi = np.percentile(reps, [2.5, 97.5])
        return {"mean": point, "ci_low": float(lo), "ci_high": float(hi), "n_cases": int(n.sum())}

    def lofo_fold_means(self, vals: dict[str, float]) -> dict[str, float]:
        """Leave-one-family-out fold means (descriptive robustness only)."""
        by_family: dict[str, list[float]] = {}
        for cid, v in vals.items():
            by_family.setdefault(self.family_of_case.get(cid), []).append(v)
        fams = sorted(by_family)
        out = {}
        for f in fams:
            others = [x for g in fams if g != f for x in by_family[g]]
            out[f] = float(np.mean(others)) if others else float("nan")
        return out


def summarize_config(episodes_by_type: dict[str, list[dict]], cb: ClusterBoot) -> dict:
    out = {"n_episodes": sum(len(v) for v in episodes_by_type.values())}
    for st, rows in episodes_by_type.items():
        block = {}
        for metric in METRICS:
            block[metric] = cb.mean_ci(case_means(rows, metric))
        block["n_episodes"] = len(rows)
        out[st] = block
    return out


def lofo_ranges(episodes_by_type: dict[str, list[dict]], cb: ClusterBoot) -> dict:
    """Per-type LOFO fold range for key metrics (family heterogeneity, not selection)."""
    out = {}
    for st, rows in episodes_by_type.items():
        block = {}
        for metric in ("correct", "correct_stop", "false", "n_inquiries"):
            folds = cb.lofo_fold_means(case_means(rows, metric))
            vals = [v for v in folds.values() if math.isfinite(v)]
            if vals:
                block[metric] = {"min": min(vals), "max": max(vals),
                                 "range": max(vals) - min(vals), "n_folds": len(vals)}
        out[st] = block
    return out
