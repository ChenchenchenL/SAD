"""Leave-one-misconception-out (LOMO) out-of-library student experiment.

For each protocol-valid v5 test case, the case's true misconception h is
removed from the diagnosis hypothesis space (singles and all pairs involving
h), and a simulated student is generated from h itself:

  * stable_ool: the student always applies h (deterministic; eps = 0);
  * slip_ool:   the student applies h and makes eps-probability random errors
                (noise model identical to the v5 stable student).

The initial observation is the frozen case answer, which by construction is
h's prediction on the case item. Three stopping arms from the frozen
stability ablation are compared on the same episodes:

  * posterior_only          (posterior concentration gates only)
  * posterior_plus_E        (+ consistent-error gate E >= 2)
  * stability_mixed_reference (full SM, frozen v5 stop logic)

Because h is not in the hypothesis space, every single/pair/mixed terminal is
by definition a false commitment to library misconception(s) the student does
not have. Terminals are therefore scored as false_commit (any library
commitment), none (explicit "no in-library stable misconception evidence"),
or abstain (insufficient evidence).

No API calls: the LLM prior is the frozen category-conditioned cache computed
with h still present in the prompt library; h is dropped from the weights and
the remaining ranks are kept. This is documented as an approximation.

Hidden labels (true_id = h) are used only to simulate the student and score
outcomes, never for diagnosis decisions.
"""
from __future__ import annotations

import math
from collections import defaultdict

import numpy as np

import ablation
import v5_engine as eng
from g0_lib import prior_weights

STUDENT_TYPES = ("stable_ool", "slip_ool")

ARMS = ("posterior_only", "posterior_plus_E", "stability_mixed_reference")

METRICS = (
    "false_commit",
    "false_single",
    "false_pair_mixed",
    "none",
    "abstain",
    "safe",
    "n_obs",
    "n_inquiries",
    "J5",
    "J10",
)


def effective_singles(bank: dict) -> list[str]:
    return [h["id"] for h in bank["hypotheses"]]


def vector_of(items: list[dict], hid: str) -> tuple:
    """Behaviour-level prediction vector: effective prediction on every item."""
    out = []
    for idx, item in enumerate(items):
        applicable = item.get("applicable", {}).get(hid, True)
        pred = item["predictions"].get(hid, item["correct"]) if applicable else item["correct"]
        out.append(pred)
    return tuple(out)


def triggering_indices(items: list[dict], hid: str) -> list[int]:
    return [
        i for i, item in enumerate(items)
        if item.get("applicable", {}).get(hid, True)
        and item["predictions"].get(hid, item["correct"]) != item["correct"]
    ]


def uniqueness_and_overlap(banks: dict[str, dict], cases: list[dict]) -> dict:
    """Verify behaviour-level vector uniqueness of each LOMO label and compute
    trigger-overlap statistics against the remaining hypotheses."""
    report = {"labels": {}, "violations": []}
    by_cat_items = {cat: bank["items"] for cat, bank in banks.items()}
    for cat, items in by_cat_items.items():
        hids = effective_singles(banks[cat])
        vecs = {h: vector_of(items, h) for h in hids}
        for h in hids:
            others = [g for g in hids if g != h]
            identical = [g for g in others if vecs[g] == vecs[h]]
            trig = triggering_indices(items, h)
            overlaps = {}
            for g in others:
                n = sum(1 for i in trig if vecs[g][i] == vecs[h][i])
                if n:
                    overlaps[g] = n
            max_g = max(overlaps, key=overlaps.get) if overlaps else None
            report["labels"][h] = {
                "category": cat,
                "n_triggering_items": len(trig),
                "identical_vectors": sorted(identical),
                "overlap_counts": dict(sorted(overlaps.items(), key=lambda kv: -kv[1])),
                "max_overlap_rule": max_g,
                "max_overlap_count": overlaps.get(max_g, 0) if max_g else 0,
                "n_overlap_rules_ge2": sum(1 for v in overlaps.values() if v >= 2),
            }
    for case in cases:
        h = case["true_id"]
        info = report["labels"].get(h)
        if info is None:
            report["violations"].append({"case_id": case["case_id"], "reason": "label_not_in_bank"})
        elif info["identical_vectors"]:
            report["violations"].append(
                {"case_id": case["case_id"], "reason": "identical_vector", "with": info["identical_vectors"]}
            )
    return report


def observe_ool(model, student_type: str, item_idx: int, h: str,
                case_id: str, seed: int, eps: float) -> str:
    if student_type == "stable_ool":
        return model.effective_pred(item_idx, h)
    if student_type == "slip_ool":
        return eng._single_outcome(model, item_idx, h, case_id, seed, student_type, eps)
    raise KeyError(student_type)


def run_episode_ool(model, prior: np.ndarray, case: dict, student_type: str,
                    arm: str, seed: int, eps: float, max_obs: int = 7):
    h = case["true_id"]
    item_idx = int(case["item_idx"])
    item = model.items[item_idx]
    answer = case["answer"]
    if answer not in item["answers"]:
        return None
    if model.effective_pred(item_idx, h) != answer:
        return None
    if h in model.index:
        return None

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
        cand = ablation.stop_check(model, post, history, arm)
        if cand:
            terminal = cand
            stopped = True
            break
        available = [i for i in range(len(model.items)) if i not in used]
        if not available:
            budget_exhausted = True
            break
        nidx = model.select_maxent(post, available)
        outcome = observe_ool(model, student_type, nidx, h, case["case_id"], seed, eps)
        used.add(nidx)
        history.append((nidx, outcome))
        post = model.update(post, nidx, outcome)

    if terminal is None:
        cand = ablation.stop_check(model, post, history, arm)
        terminal = cand if cand else ("abstain", None, float(post.max()))

    kind, tid, tp = terminal
    return eng.V5Result(
        rule=arm,
        selection="maxent",
        student_type=student_type,
        case_id=case["case_id"],
        family=case.get("family") or case.get("template_family") or str(case.get("library_template")),
        category=case["category"],
        true_id=h,
        true_pair=None,
        terminal_kind=kind,
        terminal_id=tid,
        terminal_p=tp,
        n_obs=len(history),
        stopped=stopped,
        budget_exhausted=budget_exhausted,
        verifications=0,
        history=[(model.items[i]["text"], o) for i, o in history],
        meta={"removed_rule": h, "gate_state_at_terminal": ablation.gate_state(model, post, history)},
    )


def episode_to_dict(res, seed: int) -> dict:
    kind = res.terminal_kind
    false_commit = kind in ("single", "pair", "mixed")
    return {
        "arm": res.rule,
        "student_type": res.student_type,
        "case_id": res.case_id,
        "family": res.family,
        "category": res.category,
        "removed_rule": res.meta["removed_rule"],
        "terminal_kind": kind,
        "terminal_id": res.terminal_id,
        "terminal_p": float(res.terminal_p),
        "n_obs": int(res.n_obs),
        "n_inquiries": int(res.n_inquiries),
        "stopped": bool(res.stopped),
        "budget_exhausted": bool(res.budget_exhausted),
        "false_commit": bool(false_commit),
        "false_single": bool(kind == "single"),
        "false_pair_mixed": bool(kind in ("pair", "mixed")),
        "none": bool(kind == "none"),
        "abstain": bool(kind == "abstain"),
        "safe": bool(kind in ("none", "abstain")),
        "gate": res.meta["gate_state_at_terminal"],
        "seed": int(seed),
        "J5": float(res.n_obs + 5.0 * float(false_commit)),
        "J10": float(res.n_obs + 10.0 * float(false_commit)),
    }


def episode_metric(e: dict, metric: str) -> float:
    if metric in ("false_commit", "false_single", "false_pair_mixed", "none", "abstain", "safe"):
        return float(bool(e[metric]))
    if metric == "n_obs":
        return float(e["n_obs"])
    if metric == "n_inquiries":
        return float(e["n_inquiries"])
    if metric == "J5":
        return float(e["J5"])
    if metric == "J10":
        return float(e["J10"])
    raise KeyError(metric)


def case_means(episodes: list[dict], metric: str) -> dict[str, float]:
    by_case = defaultdict(list)
    for e in episodes:
        by_case[e["case_id"]].append(episode_metric(e, metric))
    return {cid: float(np.mean(vals)) for cid, vals in by_case.items()}


def build_prior_for_case(prior_row: dict | None, singles: list[str], model) -> np.ndarray:
    top10 = (prior_row or {}).get("top10") or []
    if top10:
        weights = prior_weights(top10, singles)
    else:
        weights = {h: 1.0 / len(singles) for h in singles}
    return model.prior(weights)


def terminal_targets(episodes: list[dict]) -> dict:
    counts: dict[str, int] = defaultdict(int)
    pair_counts: dict[str, int] = defaultdict(int)
    for e in episodes:
        if e["terminal_kind"] == "single":
            counts[e["terminal_id"]] += 1
        elif e["terminal_kind"] == "pair":
            a, b = e["terminal_id"].split("|")[1:]
            pair_counts[a] += 1
            pair_counts[b] += 1
            counts[e["terminal_id"]] += 1
        elif e["terminal_kind"] == "mixed":
            counts["<unspecified-mixed>"] += 1
    return {
        "single_targets": dict(sorted(counts.items(), key=lambda kv: -kv[1])),
        "pair_member_counts": dict(sorted(pair_counts.items(), key=lambda kv: -kv[1])),
    }


def gate_counterfactual(episodes: list[dict], arms: tuple[str, ...] = ARMS) -> dict:
    """At each arm's single stops, would the E / LR / pair guards block?"""
    out = {}
    for arm in arms:
        stats = {
            "single_stops": 0,
            "E_pass": 0,
            "LR_pass": 0,
            "pair_guard_pass": 0,
            "any_gate_fail": 0,
            "min_log_lr": None,
            "n_overshoot": 0,
        }
        for e in episodes:
            if e["arm"] != arm or e["terminal_kind"] != "single":
                continue
            g = e.get("gate")
            if not g:
                continue
            stats["single_stops"] += 1
            e_pass = bool(g["E_pass"])
            lr_pass = bool(g["LR_pass"])
            pg = bool(g["pair_guard_ok"])
            stats["E_pass"] += int(e_pass)
            stats["LR_pass"] += int(lr_pass)
            stats["pair_guard_pass"] += int(pg)
            if not (e_pass and lr_pass and pg):
                stats["any_gate_fail"] += 1
            val = float(g["log_lr_slip"])
            stats["min_log_lr"] = val if stats["min_log_lr"] is None else min(stats["min_log_lr"], val)
            if e_pass and int(g["consistent_wrong"]) > 2:
                stats["n_overshoot"] += 1
        n = stats["single_stops"]
        out[arm] = {
            "n_single_stops": n,
            "pct_E_pass": stats["E_pass"] / n if n else None,
            "pct_LR_pass": stats["LR_pass"] / n if n else None,
            "pct_pair_guard_pass": stats["pair_guard_pass"] / n if n else None,
            "pct_any_gate_fail": stats["any_gate_fail"] / n if n else None,
            "min_log_lr_at_stop": stats["min_log_lr"],
            "log10_threshold": math.log(10.0),
        }
    return out


def fooled_by_label(episodes: list[dict], overlap_report: dict) -> dict:
    """Per removed-rule false-commit rate paired with its bank overlap stats."""
    by_rule = defaultdict(list)
    for e in episodes:
        by_rule[e["removed_rule"]].append(e)
    rows = []
    for h, eps_rows in sorted(by_rule.items()):
        info = overlap_report["labels"].get(h, {})
        rows.append({
            "removed_rule": h,
            "category": info.get("category"),
            "n_episodes": len(eps_rows),
            "false_commit_rate": float(np.mean([e["false_commit"] for e in eps_rows])),
            "none_rate": float(np.mean([e["none"] for e in eps_rows])),
            "abstain_rate": float(np.mean([e["abstain"] for e in eps_rows])),
            "max_overlap_count": info.get("max_overlap_count"),
            "max_overlap_rule": info.get("max_overlap_rule"),
            "n_triggering_items": info.get("n_triggering_items"),
        })
    return rows
