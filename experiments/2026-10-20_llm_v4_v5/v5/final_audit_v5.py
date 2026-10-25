"""Final audit for v5: all numbers regenerate from raw episodes/judge files.

Reads only frozen raw outputs. Writes new files under out/final_audit/.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
AUD = OUT / "final_audit"
AUD.mkdir(exist_ok=True)

EXCLUDED_CASES = {"v5test:0013", "v5test:0014", "v5test:0015"}
TYPES = ("stable", "slip", "mixed")
N_BOOT = 2000
SEED = 20261026


def load_json(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def load_jsonl(p):
    return [json.loads(l) for l in Path(p).read_text(encoding="utf-8").splitlines() if l.strip()]


def episode_metric(e, metric):
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
    if metric == "detected":
        return float(e["student_type"] == "mixed" and (
            (e["terminal_kind"] == "pair" and e["correct"]) or e["terminal_kind"] == "mixed"))
    if metric == "pair":
        return float(e["student_type"] == "mixed" and e["terminal_kind"] == "pair" and e["correct"])
    if metric == "n_inquiries":
        return float(e["n_inquiries"])
    if metric == "n_obs":
        return float(e["n_obs"])
    if metric == "J5":
        return float(e["n_obs"] + 5.0 * float(e["false_remediation"]))
    if metric == "J10":
        return float(e["n_obs"] + 10.0 * float(e["false_remediation"]))
    if metric == "miss_pen":
        return float(e["student_type"] in ("stable", "mixed") and e["terminal_kind"] in ("none", "abstain"))
    raise KeyError(metric)


RULE_SELECTION = {
    "one_shot_forced": ("one_shot_forced", "none"),
    "one_shot_typed": ("one_shot_typed", "none"),
    "random_k3": ("random_k3", "random"),
    "fixed_k3": ("fixed_k3", "fixed"),
    "maxent_k3": ("maxent_k3", "maxent"),
    "fixed3": ("fixed3", "maxent"),
    "stability_maxent": ("stability", "maxent"),
    "stability_targeted": ("stability", "targeted"),
    "stability_mixed_maxent": ("stability_mixed", "maxent"),
    "stability_mixed_targeted": ("stability_mixed", "targeted"),
    "stability_mixed_heldout_maxent": ("stability_mixed_heldout", "maxent"),
}
SUMMARY_ONLY = {"posterior_abstain", "entropy_abstain"}


def index_episodes(episodes):
    by = defaultdict(list)
    for e in episodes:
        by[(e["rule"], e["selection"], e["student_type"])].append(e)
    return by


def rows_for(by, rid, st):
    rule, sel = RULE_SELECTION[rid]
    return by[(rule, sel, st)]


def case_means(rows, metric):
    by = defaultdict(list)
    for e in rows:
        by[e["case_id"]].append(episode_metric(e, metric))
    return {cid: float(np.mean(v)) for cid, v in by.items()}


class ClusterBoot:
    def __init__(self, family_of_case, n_boot=N_BOOT, seed=SEED):
        self.family_of_case = family_of_case
        self.n_boot = n_boot
        self.seed = seed

    def _draw_counts(self, families, with_replacement=True):
        rng = np.random.default_rng(self.seed)
        idx = rng.integers(0, len(families), size=(self.n_boot, len(families)))
        counts = np.zeros((self.n_boot, len(families)), dtype=float)
        for b in range(self.n_boot):
            row = idx[b]
            if with_replacement:
                counts[b] = np.bincount(row, minlength=len(families))
            else:
                counts[b, np.unique(row)] = 1.0
        return counts

    def _sums(self, vals, fam_index):
        s = np.zeros(len(fam_index), dtype=float)
        n = np.zeros(len(fam_index), dtype=float)
        for cid, v in vals.items():
            f = fam_index.get(self.family_of_case.get(cid))
            if f is None:
                continue
            s[f] += v
            n[f] += 1.0
        return s, n

    def mean_ci(self, vals, families=None, with_replacement=True, one_sided=False):
        families = sorted(families or {self.family_of_case[c] for c in vals})
        fam_index = {f: i for i, f in enumerate(families)}
        s, n = self._sums(vals, fam_index)
        point = float(s.sum() / n.sum())
        counts = self._draw_counts(families, with_replacement=with_replacement)
        reps = (counts @ s) / (counts @ n)
        lo, hi = np.percentile(reps, [2.5, 97.5])
        out = {"mean": point, "ci_low": float(lo), "ci_high": float(hi), "reps": reps}
        if one_sided:
            out["upper_95"] = float(np.percentile(reps, 95))
            out["p_ge_threshold"] = float(np.mean(reps >= 0.10))
        return out

    def diff_ci(self, a, b, families=None, with_replacement=True):
        common = sorted(set(a) & set(b))
        d = {c: a[c] - b[c] for c in common}
        return self.mean_ci(d, families=families, with_replacement=with_replacement)


def summarize_metric(by, cb, rule, st, metric):
    rows = rows_for(by, rule, st)
    vals = case_means(rows, metric)
    fams = {cb.family_of_case[c] for c in vals}
    c = cb.mean_ci(vals, families=fams)
    n_cases = len(vals)
    n_episodes = len(rows)
    return {
        "mean": c["mean"], "ci_low": c["ci_low"], "ci_high": c["ci_high"],
        "n_cases": n_cases, "n_episodes": n_episodes,
    }


def point_mean(rows, metric):
    return float(np.mean([episode_metric(e, metric) for e in rows]))


def main_diagnosis():
    cases = load_json(HERE / "data" / "cases_test_v5_exclusion_corrected.json")
    episodes = load_json(OUT / "test_category_eps05_corrected_episodes.json")
    family_of_case = {c["case_id"]: c["template_family"] for c in cases}
    cb = ClusterBoot(family_of_case)

    rules = [
        ("one_shot_forced", "one-shot forced (historical)"),
        ("one_shot_typed", "one-shot typed (fair)"),
        ("random_k3", "random+k3"),
        ("fixed_k3", "fixed-order+k3"),
        ("maxent_k3", "maxent+k3"),
        ("fixed3", "maxent+fixed3"),
        ("posterior_abstain", "maxent+posterior+budget abstain"),
        ("entropy_abstain", "maxent+entropy+budget abstain"),
        ("stability_maxent", "maxent+stability"),
        ("stability_targeted", "targeted+stability"),
        ("stability_mixed_maxent", "maxent+stability_mixed"),
        ("stability_mixed_targeted", "targeted+stability_mixed"),
        ("stability_mixed_heldout_maxent", "maxent+held-out safety"),
    ]
    by = index_episodes(episodes)

    metrics = {
        "stable": ["correct", "correct_stop", "diagnosed", "abstain", "none", "wrong_single",
                   "n_inquiries", "n_obs", "J5", "J10"],
        "slip": ["false", "none", "abstain", "diagnosed", "n_inquiries", "n_obs", "J5", "J10"],
        "mixed": ["false", "detected", "pair", "single", "none", "abstain",
                  "n_inquiries", "n_obs", "J5", "J10"],
    }
    table = {}
    for rid, label in rules:
        if rid in SUMMARY_ONLY:
            continue
        table[rid] = {"label": label}
        for st in TYPES:
            table[rid][st] = {
                m: summarize_metric(by, cb, rid, st, m) for m in metrics[st]
            }
            rows = rows_for(by, rid, st)
            table[rid][st]["n_cases"] = len({e["case_id"] for e in rows})
            table[rid][st]["n_episodes"] = len(rows)

    # Posterior/entropy force vs abstain variants are not distinguishable in the
    # episode dump (rule field omits on_budget); use the frozen summary for these
    # secondary controls and label their CIs as legacy.
    summary = load_json(OUT / "test_category_eps05_corrected_summary.json")
    for rid in SUMMARY_ONLY:
        agg = summary["aggregates"]
        cis = summary["case_clustered_CIs"]
        table[rid] = {"label": rid, "ci_source": "legacy_summary"}
        for st in TYPES:
            a = agg[f"{rid}/{st}"]
            table[rid][st] = {"n_cases": 87, "n_episodes": a["n"], "ci_source": "legacy_summary"}
            if st == "stable":
                vals = {
                    "correct": ("stable_correct_diagnosed", "correct"),
                    "correct_stop": ("stable_correct_stop", None),
                    "diagnosed": ("coverage", None),
                    "abstain": ("abstain_rate", None),
                    "none": ("none_rate", None),
                    "wrong_single": ("stable_wrong_single_rate", None),
                    "n_inquiries": ("avg_inquiries", "n_inquiries"),
                    "n_obs": ("avg_obs", "n_obs"),
                    "J5": ("J_lambda5", "J5"),
                    "J10": ("J_lambda10", "J10"),
                }
            elif st == "slip":
                vals = {
                    "false": ("slip_error_rate", "false"),
                    "none": ("slip_explicit_none_rate", None),
                    "abstain": ("slip_abstain_rate", None),
                    "diagnosed": ("coverage", None),
                    "n_inquiries": ("avg_inquiries", "n_inquiries"),
                    "n_obs": ("avg_obs", "n_obs"),
                    "J5": ("J_lambda5", "J5"),
                    "J10": ("J_lambda10", "J10"),
                }
            else:
                vals = {
                    "false": ("mixed_error_rate", "false"),
                    "detected": ("mixed_detected_rate", None),
                    "pair": ("pair_identified_rate", None),
                    "single": ("single_commit_rate", None),
                    "none": ("mixed_none_rate", None),
                    "abstain": ("mixed_abstain_rate", None),
                    "n_inquiries": ("avg_inquiries", "n_inquiries"),
                    "n_obs": ("avg_obs", "n_obs"),
                    "J5": ("J_lambda5", "J5"),
                    "J10": ("J_lambda10", "J10"),
                }
            for m, (akey, cikey) in vals.items():
                d = {"mean": a[akey], "ci_low": None, "ci_high": None}
                if cikey and cikey in cis.get(f"{rid}/{st}", {}):
                    c = cis[f"{rid}/{st}"][cikey]
                    d["ci_low"] = c["ci_low"]
                    d["ci_high"] = c["ci_high"]
                table[rid][st][m] = d

    # Legacy (unique-family set) CIs, to quantify the correction.
    legacy = {}
    for rid in ("stability_mixed_maxent", "fixed3"):
        legacy[rid] = {}
        for st, m in (("stable", "correct"), ("slip", "false"), ("slip", "J5"),
                      ("mixed", "false")):
            vals = case_means(rows_for(by, rid, st), m)
            c = cb.mean_ci(vals, with_replacement=False)
            legacy[rid][f"{st}/{m}"] = {k: c[k] for k in ("mean", "ci_low", "ci_high")}

    # Key paired contrasts.
    contrasts = {}
    pairs = [
        ("one_shot_typed", "one_shot_forced"),
        ("maxent_k3", "random_k3"),
        ("maxent_k3", "fixed_k3"),
        ("stability_mixed_maxent", "fixed3"),
        ("stability_mixed_targeted", "stability_mixed_maxent"),
        ("stability_targeted", "stability_maxent"),
        ("stability_mixed_heldout_maxent", "stability_mixed_maxent"),
        ("stability_maxent", "stability_mixed_maxent"),
    ]
    for a, b in pairs:
        for st in TYPES:
            key = f"{a}_minus_{b}/{st}"
            contrasts[key] = {}
            for m in ("correct", "correct_stop", "diagnosed", "abstain", "none",
                      "wrong_single", "false", "detected", "pair", "single",
                      "n_inquiries", "J5", "J10"):
                va = case_means(rows_for(by, a, st), m)
                vb = case_means(rows_for(by, b, st), m)
                if not va or not vb:
                    continue
                c = cb.diff_ci(va, vb)
                contrasts[key][m] = {k: c[k] for k in ("mean", "ci_low", "ci_high")}

    # J sensitivity and always-abstain reference.
    j_sens = {}
    always = {
        "stable": {"J5": 1.0, "J10": 1.0, "correct": 0.0, "correct_stop": 0.0,
                   "abstain": 1.0, "n_inquiries": 0.0},
        "slip": {"J5": 1.0, "J10": 1.0, "false": 0.0, "abstain": 1.0, "n_inquiries": 0.0},
        "mixed": {"J5": 1.0, "J10": 1.0, "false": 0.0, "abstain": 1.0, "n_inquiries": 0.0},
    }
    for rid, _ in rules:
        if rid in SUMMARY_ONLY:
            continue
        per = {}
        for st in TYPES:
            per[st] = {
                "J5": point_mean(rows_for(by, rid, st), "J5"),
                "J10": point_mean(rows_for(by, rid, st), "J10"),
            }
        mixes = {
            "stable_slip_50_50": {"stable": .5, "slip": .5},
            "stable_slip_70_30": {"stable": .7, "slip": .3},
            "stable_slip_30_70": {"stable": .3, "slip": .7},
            "all_50_25_25": {"stable": .5, "slip": .25, "mixed": .25},
        }
        out = {}
        for name, w in mixes.items():
            out[name] = {}
            for lam in ("J5", "J10"):
                out[name][lam] = sum(w[s] * per[s][lam] for s in w) / sum(w.values())
        out["per_type"] = per
        j_sens[rid] = out
    always_mix = {}
    for name, w in {
        "stable_slip_50_50": {"stable": .5, "slip": .5},
        "stable_slip_70_30": {"stable": .7, "slip": .3},
        "stable_slip_30_70": {"stable": .3, "slip": .7},
        "all_50_25_25": {"stable": .5, "slip": .25, "mixed": .25},
    }.items():
        always_mix[name] = {
            lam: sum(w[s] * always[s][lam] for s in w) / sum(w.values())
            for lam in ("J5", "J10")
        }
    j_sens["always_abstain"] = {"per_type": always, **always_mix}
    for rid in SUMMARY_ONLY:
        j_sens[rid] = summary["j_sensitivity"][rid]

    # Exploratory abstention penalty: c per stable/mixed none/abstain episode.
    pen_rules = ("one_shot_typed", "fixed3", "stability_maxent",
                 "stability_mixed_maxent", "stability_mixed_heldout_maxent")
    j_pen = {}
    for rid in pen_rules:
        j_pen[rid] = {}
        for lam in (5.0, 10.0):
            for c_pen in (1.0, 2.0, 5.0):
                per = {}
                for st in TYPES:
                    vals = [e["n_obs"] + lam * float(e["false_remediation"]) +
                            c_pen * episode_metric(e, "miss_pen") for e in rows_for(by, rid, st)]
                    per[st] = float(np.mean(vals))
                j_pen[rid][f"lambda{int(lam)}_c{int(c_pen)}"] = {
                    "per_type": per,
                    "stable_slip_50_50": .5 * per["stable"] + .5 * per["slip"],
                    "all_50_25_25": .5 * per["stable"] + .25 * per["slip"] + .25 * per["mixed"],
                }
    for lam in (5.0, 10.0):
        for c_pen in (1.0, 2.0, 5.0):
            j_pen.setdefault("always_abstain", {})[f"lambda{int(lam)}_c{int(c_pen)}"] = {
                "per_type": {
                    "stable": 1.0 + c_pen,
                    "slip": 1.0,
                    "mixed": 1.0 + c_pen,
                },
                "stable_slip_50_50": 1.0 + 0.5 * c_pen,
                "all_50_25_25": 1.0 + 0.5 * c_pen,
            }

    # Category and true-label breakdown for the primary rule.
    per_category = {}
    cats = sorted({e["category"] for e in rows_for(by, "stability_mixed_maxent", "stable")})
    for cat in cats:
        per_category[cat] = {}
        for st in TYPES:
            rows = [e for e in rows_for(by, "stability_mixed_maxent", st) if e["category"] == cat]
            fams = {family_of_case[e["case_id"]] for e in rows}
            mlist = ["correct", "correct_stop", "diagnosed", "abstain", "n_inquiries"] if st == "stable" else (
                ["false", "none", "abstain", "n_inquiries"] if st == "slip" else
                ["false", "detected", "pair", "none", "abstain", "n_inquiries"])
            per_category[cat][st] = {"n_cases": len({e["case_id"] for e in rows}),
                                     "n_episodes": len(rows)}
            for m in mlist:
                vals = case_means(rows, m)
                c = cb.mean_ci(vals, families=fams)
                per_category[cat][st][m] = {k: c[k] for k in ("mean", "ci_low", "ci_high")}

    case_map = {c["case_id"]: c for c in cases}
    per_label = {}
    def label_row(hid):
        return per_label.setdefault(hid, {"stable_n": 0, "stable_correct": 0,
                                          "slip_n": 0, "slip_error": 0,
                                          "mixed_n": 0, "mixed_detected": 0, "mixed_error": 0})
    for e in rows_for(by, "stability_mixed_maxent", "stable"):
        d = label_row(case_map[e["case_id"]]["true_id"])
        d["stable_n"] += 1
        d["stable_correct"] += int(bool(e["correct"]))
    for e in rows_for(by, "stability_mixed_maxent", "slip"):
        d = label_row(case_map[e["case_id"]]["true_id"])
        d["slip_n"] += 1
        d["slip_error"] += int(bool(e["false_remediation"]))
    for e in rows_for(by, "stability_mixed_maxent", "mixed"):
        d = label_row(case_map[e["case_id"]]["true_id"])
        d["mixed_n"] += 1
        d["mixed_detected"] += int(bool(episode_metric(e, "detected")))
        d["mixed_error"] += int(bool(e["false_remediation"]))
    for hid, d in per_label.items():
        for pre, nkey, vkey in (("stable", "stable_n", "stable_correct"),
                                ("slip", "slip_n", "slip_error"),
                                ("mixed", "mixed_n", "mixed_detected")):
            d[f"{pre}_rate"] = d[vkey] / d[nkey] if d[nkey] else None
        d["mixed_error_rate"] = d["mixed_error"] / d["mixed_n"] if d["mixed_n"] else None

    # Original 90-case vs protocol-valid 87-case key results.
    orig_cases = load_json(HERE / "data" / "cases_test_v5.json")
    orig_eps = load_json(OUT / "test_category_eps05_episodes.json")
    orig_fam = {c["case_id"]: c["template_family"] for c in orig_cases}
    orig_by = index_episodes(orig_eps)
    orig_cb = ClusterBoot(orig_fam)
    side_rules = ("one_shot_forced", "one_shot_typed", "maxent_k3", "fixed3",
                  "stability_mixed_maxent", "stability_mixed_heldout_maxent")
    side = {}
    for rid in side_rules:
        side[rid] = {"original_90": {}, "protocol_valid_87": {}}
        for st, ms in (("stable", ["correct", "correct_stop"]),
                       ("slip", ["false", "J5"]),
                       ("mixed", ["false"])):
            for m in ms:
                vo = case_means(rows_for(orig_by, rid, st), m)
                co = orig_cb.mean_ci(vo)
                vc = case_means(rows_for(by, rid, st), m)
                cc = cb.mean_ci(vc)
                side[rid]["original_90"][f"{st}/{m}"] = {
                    "mean": co["mean"], "ci_low": co["ci_low"], "ci_high": co["ci_high"]}
                side[rid]["protocol_valid_87"][f"{st}/{m}"] = {
                    "mean": cc["mean"], "ci_low": cc["ci_low"], "ci_high": cc["ci_high"]}

    # Noise sensitivity, recomputed from corrected episodes.
    noise = {}
    for eps, fname in (("0.0", "test_category_eps0.0_corrected_episodes.json"),
                       ("0.05", "test_category_eps05_corrected_episodes.json"),
                       ("0.10", "test_category_eps0.10_corrected_episodes.json")):
        ne = load_json(OUT / fname)
        nb = index_episodes(ne)
        noise[eps] = {}
        for rid in ("one_shot_typed", "fixed3", "stability_mixed_maxent",
                    "stability_mixed_heldout_maxent"):
            noise[eps][rid] = {
                "stable_correct": point_mean(rows_for(nb, rid, "stable"), "correct"),
                "stable_correct_stop": point_mean(rows_for(nb, rid, "stable"), "correct_stop"),
                "slip_error": point_mean(rows_for(nb, rid, "slip"), "false"),
                "slip_none": point_mean(rows_for(nb, rid, "slip"), "none"),
                "slip_abstain": point_mean(rows_for(nb, rid, "slip"), "abstain"),
                "mixed_error": point_mean(rows_for(nb, rid, "mixed"), "false"),
            }

    # Prior summaries (read, not recomputed; all derive from frozen prior JSONL).
    priors = {}
    for key, fname in (
        ("category_corrected", "priors_test_category_corrected_summary.json"),
        ("full_corrected", "priors_test_full_corrected_summary.json"),
        ("category_original", "priors_test_category_summary.json"),
        ("full_original", "priors_test_full_summary.json"),
        ("nodomain_corrected", "priors_test_full_nodomain_summary.json"),
    ):
        priors[key] = load_json(OUT / fname)

    # Exploratory prior / global-candidate rule results (frozen summaries).
    exploratory = {}
    for key, fname in (
        ("nodomain_category", "test_nodomainprior_category_summary.json"),
        ("nodomain_global", "test_nodomainprior_global_summary.json"),
        ("globalprior_category", "test_globalprior_category_corrected_summary.json"),
        ("globalprior_global", "test_globalprior_globalmodel_corrected_summary.json"),
    ):
        d = load_json(OUT / fname)
        exploratory[key] = {}
        for rid in ("one_shot_typed", "fixed3", "maxent_k3", "stability_maxent", "stability_mixed_maxent"):
            if f"{rid}/stable" not in d.get("aggregates", {}):
                continue
            exploratory[key][rid] = {
                "stable_correct": d["aggregates"][f"{rid}/stable"]["stable_correct_diagnosed"],
                "slip_error": d["aggregates"][f"{rid}/slip"]["slip_error_rate"],
                "slip_none": d["aggregates"][f"{rid}/slip"]["slip_explicit_none_rate"],
                "slip_abstain": d["aggregates"][f"{rid}/slip"]["slip_abstain_rate"],
                "stable_abstain": d["aggregates"][f"{rid}/stable"]["abstain_rate"],
                "stable_inquiries": d["aggregates"][f"{rid}/stable"]["avg_inquiries"],
            }

    result = {
        "meta": {
            "n_cases_protocol_valid": len(cases),
            "n_cases_original": len(orig_cases),
            "n_true_labels_protocol_valid": len({c["true_id"] for c in cases}),
            "n_true_labels_original": len({c["true_id"] for c in orig_cases}),
            "n_families_protocol_valid": len(set(family_of_case.values())),
            "n_families_original": len(set(orig_fam.values())),
            "n_episodes_protocol_valid": len(episodes),
            "n_episodes_original": len(orig_eps),
            "seeds": 5,
            "eps": 0.05,
            "bootstrap": N_BOOT,
            "bootstrap_unit": "template_family (36), with replacement and multiplicity",
        },
        "rules": [{"id": r, "label": l} for r, l in rules],
        "table": table,
        "legacy_ci": legacy,
        "contrasts": contrasts,
        "j_sensitivity": j_sens,
        "j_penalty_exploratory": j_pen,
        "per_category": per_category,
        "per_label": per_label,
        "original_vs_corrected": side,
        "noise": noise,
        "priors": priors,
        "exploratory_prior_rules": exploratory,
    }
    (AUD / "diagnosis_audit.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    return result


if __name__ == "__main__":
    r = main_diagnosis()
    print(json.dumps(r["meta"], indent=2))
    for rid in ("fixed3", "stability_mixed_maxent"):
        print(rid, json.dumps({k: r["table"][rid][k] for k in ("stable", "slip", "mixed")}, indent=1)[:1200])
    print("key contrast", json.dumps(r["contrasts"]["stability_mixed_maxent_minus_fixed3/slip"], indent=1))
