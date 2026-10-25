"""Audit feedback v5 judge results from raw records.

Fixes:
  * template-family cluster bootstrap with replacement (not unique-set resampling);
  * GLM subset reweighted by its own stratum sample counts;
  * DeepSeek full vs GLM subset vs common subset reported separately;
  * cross-judge comparisons restricted to the common 60-episode set;
  * validator-retry denominators separated (480/464/240/60).
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
FIELDS = ("true_target_hit", "misleading", "answer_leak", "math_correct", "new_example",
          "practice_without_answer", "overclaims_misconception", "actionable_next_step", "overall")
N_BOOT = 2000
SEED = 20261027
JUDGES = ("deepseek-v4.1-flash", "glm-5.3-flash")


def load_json(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def load_jsonl(p):
    return [json.loads(l) for l in Path(p).read_text(encoding="utf-8").splitlines() if l.strip()]


def dedupe(rows, keep="first"):
    out = {}
    for r in rows:
        k = r["record_key"]
        if keep == "first":
            out.setdefault(k, r)
        else:
            out[k] = r
    return list(out.values())


class WClusterBoot:
    """Weighted cluster bootstrap over template families."""

    def __init__(self, n_boot=N_BOOT, seed=SEED):
        self.n_boot = n_boot
        self.seed = seed

    def _counts(self, families):
        rng = np.random.default_rng(self.seed)
        idx = rng.integers(0, len(families), size=(self.n_boot, len(families)))
        counts = np.zeros((self.n_boot, len(families)), dtype=float)
        for b in range(self.n_boot):
            counts[b] = np.bincount(idx[b], minlength=len(families))
        return counts

    def mean(self, values, weights, family_of_key, families=None):
        families = sorted(families or {family_of_key[k] for k in values})
        fi = {f: i for i, f in enumerate(families)}
        S = np.zeros(len(families)); W = np.zeros(len(families))
        for k, y in values.items():
            f = fi[family_of_key[k]]
            S[f] += weights[k] * y
            W[f] += weights[k]
        point = float(S.sum() / W.sum())
        counts = self._counts(families)
        reps = (counts @ S) / (counts @ W)
        lo, hi = np.percentile(reps, [2.5, 97.5])
        return {"mean": point, "ci_low": float(lo), "ci_high": float(hi), "reps": reps}

    def diff(self, a, b, weights, family_of_key, families=None):
        keys = sorted(set(a) & set(b))
        d = {k: a[k] - b[k] for k in keys}
        w = {k: weights[k] for k in keys}
        return self.mean(d, w, family_of_key, families=families)


def episode_boot_diff(a, b, weights, n_boot=N_BOOT, seed=SEED):
    keys = sorted(set(a) & set(b))
    d = np.array([a[k] - b[k] for k in keys])
    w = np.array([weights[k] for k in keys])
    rng = np.random.default_rng(seed)
    reps = []
    n = len(keys)
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        reps.append(float(np.sum(w[idx] * d[idx]) / np.sum(w[idx])))
    reps = np.array(reps)
    point = float(np.sum(w * d) / np.sum(w))
    lo, hi = np.percentile(reps, [2.5, 97.5])
    return {"mean": point, "ci_low": float(lo), "ci_high": float(hi)}


def main():
    cases = load_json(HERE / "data" / "cases_test_v5_exclusion_corrected.json")
    family_of_case = {c["case_id"]: c["template_family"] for c in cases}
    family_of_key = {}
    for cid, fam in family_of_case.items():
        family_of_key[(cid, "stable")] = fam
        family_of_key[(cid, "slip")] = fam

    episodes = load_json(OUT / "test_category_eps05_corrected_episodes.json")
    primary = {}
    for e in episodes:
        if e["seed"] == 0 and e["rule"] == "stability_mixed" and e["selection"] == "maxent":
            primary[(e["student_type"], e["case_id"])] = e

    def stratum(ep):
        if ep["student_type"] == "stable":
            if ep["terminal_kind"] == "single":
                return "stable_correct" if ep["correct"] else "stable_wrong"
            if ep["terminal_kind"] == "none":
                return "stable_explicit_none"
            if ep["terminal_kind"] == "abstain":
                return "stable_abstain"
            return "stable_other"
        if ep["student_type"] == "slip":
            if ep["terminal_kind"] == "none":
                return "slip_explicit_none"
            if ep["terminal_kind"] == "abstain":
                return "slip_abstain"
            return "slip_error"
        return "mixed"

    population = Counter()
    for key, ep in primary.items():
        if ep["student_type"] in ("stable", "slip"):
            population[stratum(ep)] += 1

    feedback = {r["cache_key"]: r for r in load_jsonl(OUT / "feedback_v5.jsonl")}
    feedback_rows = list(feedback.values())
    valid_feedback = [r for r in feedback_rows if r["case_id"] not in EXCLUDED_CASES]
    fb_by_key = {(r["case_id"], r["student_type"], r["condition"]): r for r in valid_feedback}

    # judge records
    def judge_rows(model):
        slug = model.replace("-", "_").replace(".", "_")
        paths = sorted(OUT.glob(f"judge_v5_{slug}*.jsonl"))
        rows = []
        for p in paths:
            rows.extend(load_jsonl(p))
        return rows

    def final_pointwise(rows, keep="first"):
        rows = [r for r in rows if r.get("task") == "judge" and r.get("variant") == "final"
                and r.get("http_status") == 200
                and r.get("model") in JUDGES]
        return dedupe(rows, keep=keep)

    raw_rows = {m: judge_rows(m) for m in JUDGES}
    ds_final = final_pointwise(raw_rows["deepseek-v4.1-flash"])
    glm_final_all = final_pointwise(raw_rows["glm-5.3-flash"])
    ds_final_valid = [r for r in ds_final if r["case_id"] not in EXCLUDED_CASES and r.get("parsed")]
    glm_final_all_valid = [r for r in glm_final_all if r["case_id"] not in EXCLUDED_CASES]
    glm_final_valid = [r for r in glm_final_all_valid if r.get("parsed")]
    glm_final_last_all = [r for r in final_pointwise(raw_rows["glm-5.3-flash"], keep="last")
                          if r["case_id"] not in EXCLUDED_CASES]
    glm_final_last = [r for r in glm_final_last_all if r.get("parsed")]

    def key(r):
        return (r["case_id"], r["student_type"], r["condition"])

    def epkey(r):
        return (r["case_id"], r["student_type"])

    ds_map = {key(r): r for r in ds_final_valid}
    glm_map = {key(r): r for r in glm_final_valid}
    glm_last_map = {key(r): r for r in glm_final_last}
    common_keys = sorted(set(ds_map) & set(glm_map))
    common_episodes = sorted({(k[0], k[1]) for k in common_keys})

    # sample counts / weights
    def sample_counts(rows):
        c = Counter(r["stratum"] for r in rows if r["condition"] == "pipeline")
        return c

    ds_sample = sample_counts(ds_final_valid)
    glm_sample = sample_counts(glm_final_all_valid)
    strata = sorted(population)
    ds_weights = {s: population[s] / ds_sample[s] for s in strata if ds_sample.get(s)}
    glm_weights = {s: population[s] / glm_sample[s] for s in strata if glm_sample.get(s)}
    # design-weight sensitivity: success strata were pooled then sampled.
    success = {"stable_correct", "slip_explicit_none", "slip_abstain"}
    fail = {"stable_other", "slip_error"}
    design = {}
    for name, sample in (("ds", ds_sample), ("glm", glm_sample)):
        w = {}
        succ_pop = sum(population[s] for s in success)
        succ_n = sum(sample[s] for s in success)
        for s in strata:
            if s in success:
                w[s] = succ_pop / succ_n
            elif s in fail:
                w[s] = population[s] / sample[s]
        design[name] = w

    def weights_for(rows, wmap):
        return {(r["case_id"], r["student_type"], r["condition"]): wmap[r["stratum"]] for r in rows}

    ds_w = weights_for(ds_final_valid, ds_weights)
    glm_w = weights_for(glm_final_valid, glm_weights)

    cb = WClusterBoot()

    def pointwise(rows, wmap):
        out = {}
        for cond in ("oracle", "pipeline", "one_shot", "no_diagnosis"):
            sub = [r for r in rows if r["condition"] == cond]
            w = {epkey(r): wmap[r["stratum"]] for r in sub}
            out[cond] = {"n": len(sub)}
            for field in FIELDS:
                v = {epkey(r): float(r["parsed"][field]) for r in sub
                     if isinstance(r["parsed"].get(field), (int, float))}
                ww = {k: w[k] for k in v}
                c = cb.mean(v, ww, family_of_key)
                out[cond][field] = {
                    "weighted": c["mean"], "ci_low": c["ci_low"], "ci_high": c["ci_high"],
                    "unweighted": float(np.mean(list(v.values()))),
                }
        return out

    ds_point = pointwise(ds_final_valid, ds_weights)
    glm_point = pointwise(glm_final_valid, glm_weights)

    # common-subset pointwise: same episodes and GLM post-stratification weights for both judges.
    common_set = set(common_episodes)
    ds_common_rows = [r for r in ds_final_valid if (r["case_id"], r["student_type"]) in common_set]
    glm_common_rows = [r for r in glm_final_valid if (r["case_id"], r["student_type"]) in common_set]
    ds_common_point = pointwise(ds_common_rows, glm_weights)
    glm_common_point = pointwise(glm_common_rows, glm_weights)

    def values(rows, field, cond):
        return {epkey(r): float(r["parsed"][field]) for r in rows if r["condition"] == cond}

    def weights_ep(rows, wmap, conds):
        return {epkey(r): wmap[r["stratum"]] for r in rows if r["condition"] in conds}

    def compare(rows, wmap, other):
        out = {}
        for field in ("true_target_hit", "overall", "misleading"):
            a = values(rows, field, "pipeline")
            b = values(rows, field, other)
            w = weights_ep(rows, wmap, ("pipeline", other))
            c = cb.diff(a, b, w, family_of_key)
            e = episode_boot_diff(a, b, w)
            out[field] = {"cluster": {k: c[k] for k in ("mean", "ci_low", "ci_high")},
                          "episode": e, "n_pairs": len(set(a) & set(b))}
        return out

    paired = {
        "deepseek_full": {other: compare(ds_final_valid, ds_weights, other)
                          for other in ("one_shot", "no_diagnosis", "oracle")},
        "glm_subset": {other: compare(glm_final_valid, glm_weights, other)
                       for other in ("one_shot", "no_diagnosis", "oracle")},
        "common": {
            "deepseek": {other: compare(ds_common_rows, glm_weights, other)
                         for other in ("one_shot", "no_diagnosis", "oracle")},
            "glm": {other: compare(glm_common_rows, glm_weights, other)
                    for other in ("one_shot", "no_diagnosis", "oracle")},
        },
    }

    # Design-weight sensitivity for the headline target-hit comparisons.
    design_sens = {}
    for name, rows, wmap, label in (
        ("deepseek_full", ds_final_valid, design["ds"], "deepseek"),
        ("glm_subset", glm_final_valid, design["glm"], "glm"),
    ):
        w = weights_for(rows, wmap)
        design_sens[name] = {}
        for other in ("one_shot", "no_diagnosis", "oracle"):
            a = values(rows, "true_target_hit", "pipeline")
            b = values(rows, "true_target_hit", other)
            ww = weights_ep(rows, wmap, ("pipeline", other))
            c = cb.diff(a, b, ww, family_of_key)
            design_sens[name][other] = {k: c[k] for k in ("mean", "ci_low", "ci_high")}

    # Judge difference on common subset (same weights, same episodes).
    judge_diff = {}
    for field in ("true_target_hit", "overall", "misleading"):
        judge_diff[field] = {}
        for cond in ("oracle", "pipeline", "one_shot", "no_diagnosis"):
            a = values(ds_common_rows, field, cond)
            b = values(glm_common_rows, field, cond)
            w = weights_ep(glm_common_rows, glm_weights, (cond,))
            c = cb.diff(a, b, w, family_of_key)
            judge_diff[field][cond] = {k: c[k] for k in ("mean", "ci_low", "ci_high")}
            judge_diff[field][cond]["n_pairs"] = len(set(a) & set(b))
    moderation = {}
    for other in ("one_shot", "no_diagnosis", "oracle"):
        da = values(ds_common_rows, "true_target_hit", "pipeline")
        db = values(ds_common_rows, "true_target_hit", other)
        ga = values(glm_common_rows, "true_target_hit", "pipeline")
        gb = values(glm_common_rows, "true_target_hit", other)
        ds_eff = {k: da[k] - db[k] for k in da if k in db}
        glm_eff = {k: ga[k] - gb[k] for k in ga if k in gb}
        w = weights_ep(glm_common_rows, glm_weights, ("pipeline", other))
        c = cb.diff(ds_eff, glm_eff, w, family_of_key)
        moderation[other] = {k: c[k] for k in ("mean", "ci_low", "ci_high")}
        moderation[other]["n_pairs"] = len(set(ds_eff) & set(glm_eff))

    # Pairwise: outcome per comparison.
    def pairwise(rows, wmap):
        rows = [r for r in rows if r.get("task") == "pairwise" and r.get("http_status") == 200
                and r.get("parsed")]
        by = defaultdict(dict)
        for r in rows:
            if r["case_id"] in EXCLUDED_CASES:
                continue
            by[(r["case_id"], r["student_type"], r["condition"])][r["order"]] = r
        counts = Counter(); weighted = Counter(); n_complete = 0
        for k, orders in by.items():
            if "ab" not in orders or "ba" not in orders:
                continue
            x = orders["ab"]["parsed"].get("winner")
            y = orders["ba"]["parsed"].get("winner")
            if x is None or y is None:
                continue
            first, second = k[2].split("_vs_")
            if x == "tie" or y == "tie":
                res = "tie"
            elif x == "A" and y == "B":
                res = first
            elif x == "B" and y == "A":
                res = second
            else:
                res = "inconsistent"
            n_complete += 1
            counts[(k[1], k[2], res)] += 1
            weighted[(k[1], k[2], res)] += wmap[orders["ab"]["stratum"]]
        return {
            "counts": [{"student_type": k[0], "comparison": k[1], "outcome": k[2], "n": v}
                       for k, v in sorted(counts.items())],
            "weighted": [{"student_type": k[0], "comparison": k[1], "outcome": k[2], "weight": v}
                         for k, v in sorted(weighted.items())],
            "n_comparisons": n_complete,
        }

    pw = {
        "deepseek_full": pairwise(raw_rows["deepseek-v4.1-flash"], ds_weights),
        "glm_subset": pairwise(raw_rows["glm-5.3-flash"], glm_weights),
    }

    def pair_outcomes(rows, wmap):
        rows = [r for r in rows if r.get("task") == "pairwise" and r.get("http_status") == 200
                and r.get("parsed") and r["case_id"] not in EXCLUDED_CASES]
        by = defaultdict(dict)
        for r in rows:
            by[(r["case_id"], r["student_type"], r["condition"])][r["order"]] = r
        out = {}
        for k, orders in by.items():
            if "ab" not in orders or "ba" not in orders:
                continue
            x = orders["ab"]["parsed"].get("winner"); y = orders["ba"]["parsed"].get("winner")
            first, second = k[2].split("_vs_")
            if x == "tie" or y == "tie":
                res = "tie"
            elif x == "A" and y == "B":
                res = first
            elif x == "B" and y == "A":
                res = second
            else:
                res = "inconsistent"
            out[k] = res
        return out

    ds_pw = pair_outcomes(raw_rows["deepseek-v4.1-flash"], ds_weights)
    glm_pw = pair_outcomes(raw_rows["glm-5.3-flash"], glm_weights)
    common_pw = sorted(set(ds_pw) & set(glm_pw))
    cats = sorted(set(ds_pw.values()) | set(glm_pw.values()))
    po = sum(ds_pw[k] == glm_pw[k] for k in common_pw) / len(common_pw)
    pc = Counter(glm_pw[k] for k in common_pw)
    pe = sum((v / len(common_pw)) ** 2 for v in pc.values())
    kappa = (po - pe) / (1 - pe) if pe < 1 else None
    # per-order winner agreement on common comparisons
    order_common = []
    for k in common_pw:
        for order in ("ab", "ba"):
            a = next((r for r in raw_rows["deepseek-v4.1-flash"]
                      if r.get("task") == "pairwise" and key_pair(r) == k and r.get("order") == order), None)
            b = next((r for r in raw_rows["glm-5.3-flash"]
                      if r.get("task") == "pairwise" and key_pair(r) == k and r.get("order") == order), None)
            if a and b:
                order_common.append(a["parsed"].get("winner") == b["parsed"].get("winner"))
    cross_pw = {
        "n_comparisons": len(common_pw),
        "outcome_agreement": po,
        "cohen_kappa": kappa,
        "outcome_counts_glm": dict(pc),
        "per_order_n": len(order_common),
        "per_order_agreement": float(np.mean(order_common)) if order_common else None,
        "ties": float(np.mean([ds_pw[k] == "tie" or glm_pw[k] == "tie" for k in common_pw])),
        "inconsistent": float(np.mean([ds_pw[k] == "inconsistent" or glm_pw[k] == "inconsistent"
                                       for k in common_pw])),
    }

    # Cross-judge pointwise on common 240 final records.
    common_point_keys = sorted(set(ds_map) & set(glm_map))
    cross_point = {"n": len(common_point_keys), "fields": {}}
    for field in FIELDS:
        pairs = [(float(ds_map[k]["parsed"][field]), float(glm_map[k]["parsed"][field]))
                 for k in common_point_keys if isinstance(ds_map[k]["parsed"].get(field), (int, float))
                 and isinstance(glm_map[k]["parsed"].get(field), (int, float))]
        a = np.array([x for x, _ in pairs]); b = np.array([y for _, y in pairs])
        cross_point["fields"][field] = {
            "exact_agreement": float(np.mean(a == b)),
            "mae": float(np.mean(np.abs(a - b))),
            "pearson": float(np.corrcoef(a, b)[0, 1]) if len(a) > 1 and a.std() > 0 and b.std() > 0 else None,
        }
    cross_point["weighted_mae_overall"] = None
    if "overall" in cross_point["fields"]:
        wsum = den = 0.0
        for k in common_point_keys:
            if k[2] != "pipeline":
                continue
            a = ds_map[k]["parsed"].get("overall"); b = glm_map[k]["parsed"].get("overall")
            if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                w = glm_weights[glm_map[k]["stratum"]]
                wsum += w * abs(a - b); den += w
        cross_point["weighted_mae_overall"] = wsum / den if den else None

    # GLM duplicate sensitivity.
    glm_dup_keys = [k for k, v in Counter(r["record_key"] for r in raw_rows["glm-5.3-flash"]).items() if v > 1]
    dup_diff = {}
    for cond in ("oracle", "pipeline", "one_shot", "no_diagnosis"):
        a = [r for r in glm_final_valid if r["condition"] == cond]
        b = [r for r in glm_final_last if r["condition"] == cond]
        amap = {key(r): r for r in a}; bmap = {key(r): r for r in b}
        ks = sorted(set(amap) & set(bmap))
        dup_diff[cond] = {
            "n": len(ks),
            "overall_mean_first": float(np.mean([amap[k]["parsed"]["overall"] for k in ks])),
            "overall_mean_last": float(np.mean([bmap[k]["parsed"]["overall"] for k in ks])),
            "target_hit_first": float(np.mean([amap[k]["parsed"]["true_target_hit"] for k in ks])),
            "target_hit_last": float(np.mean([bmap[k]["parsed"]["true_target_hit"] for k in ks])),
        }

    # Validator retry denominators and flags.
    def retry_stats(rows):
        rr = [r for r in rows if r["retried"]]
        out = {"n_records": len(rows), "n_retried": len(rr)}
        for label, val in (("init", "initial_validation"), ("final", "final_validation")):
            vals = [r[val] for r in rr]
            out[f"{label}_math_incorrect"] = sum(1 for v in vals if v.get("math", {}).get("status") == "incorrect")
            out[f"{label}_math_unverifiable"] = sum(1 for v in vals if v.get("math", {}).get("status") == "unverifiable")
            out[f"{label}_leak_suspected"] = sum(1 for v in vals if v.get("leak", {}).get("suspected"))
        return out

    glm_keys = {(r["case_id"], r["student_type"]) for r in glm_final_valid}
    glm_feedback = [r for r in valid_feedback if (r["case_id"], r["student_type"]) in glm_keys]
    retry = {
        "full_480": retry_stats(feedback_rows),
        "protocol_valid_464": retry_stats(valid_feedback),
        "glm_episode_subset_240": retry_stats(glm_feedback),
    }

    # Judge raw/final retry quality.
    def retry_quality(rows, valid_only=False):
        rows = [r for r in rows if r.get("task") == "judge" and r.get("variant") in ("raw", "final")
                and r.get("http_status") == 200 and r.get("parsed")]
        if valid_only:
            rows = [r for r in rows if r["case_id"] not in EXCLUDED_CASES]
        raw = {key(r): r for r in rows if r["variant"] == "raw"}
        final = {key(r): r for r in rows if r["variant"] == "final"}
        ks = sorted(set(raw) & set(final))
        out = {"n": len(ks)}
        for label, src in (("raw", raw), ("final", final)):
            for field in ("overall", "true_target_hit", "misleading", "answer_leak",
                          "math_correct", "actionable_next_step"):
                vals = [src[k]["parsed"][field] for k in ks
                        if isinstance(src[k]["parsed"].get(field), (int, float))]
                out[f"{label}_{field}"] = float(np.mean(vals)) if vals else None
        return out

    retry_quality_out = {
        "deepseek_full_96": retry_quality(raw_rows["deepseek-v4.1-flash"], valid_only=False),
        "deepseek_valid_88": retry_quality(raw_rows["deepseek-v4.1-flash"], valid_only=True),
        "glm_subset_54": retry_quality(raw_rows["glm-5.3-flash"], valid_only=True),
    }

    # Cost audit from usage (all actual calls, including duplicate judge re-runs).
    def usage_cost(rows, input_rate=0.28, output_rate=0.42):
        it = sum((r.get("usage", {}) or {}).get("input_tokens") or 0 for r in rows)
        ot = sum((r.get("usage", {}) or {}).get("output_tokens") or 0 for r in rows)
        return {"input_tokens": it, "output_tokens": ot,
                "usd": it / 1e6 * input_rate + ot / 1e6 * output_rate}

    cost = {
        "feedback_generation_480": usage_cost(feedback_rows),
        "deepseek_judge_1296": usage_cost(raw_rows["deepseek-v4.1-flash"]),
        "glm_judge_681": usage_cost(raw_rows["glm-5.3-flash"]),
    }

    meta = {
        "n_feedback_records_full": len(feedback_rows),
        "n_feedback_records_valid": len(valid_feedback),
        "n_feedback_episodes_full": len({(r["case_id"], r["student_type"]) for r in feedback_rows if r["condition"] == "pipeline"}),
        "n_feedback_episodes_valid": len({(r["case_id"], r["student_type"]) for r in valid_feedback if r["condition"] == "pipeline"}),
        "n_deepseek_final": len(ds_final),
        "n_deepseek_final_valid": len(ds_final_valid),
        "n_glm_final_unique": len(glm_final_all),
        "n_glm_final_valid": len(glm_final_all_valid),
        "n_glm_final_parsed": len(glm_final_valid),
        "n_glm_final_missing_parsed": len(glm_final_all_valid) - len(glm_final_valid),
        "n_glm_pairwise_requested_comparisons": 180,
        "n_glm_pairwise_complete_comparisons": pw["glm_subset"]["n_comparisons"],
        "n_glm_duplicate_record_keys": len(glm_dup_keys),
        "n_common_episodes": len(common_episodes),
        "n_common_pointwise": len(common_keys),
        "n_common_pairwise_comparisons": len(common_pw),
        "population_strata": dict(population),
        "deepseek_sample_strata": dict(ds_sample),
        "glm_sample_strata": dict(glm_sample),
        "deepseek_weights": ds_weights,
        "glm_weights": glm_weights,
        "deepseek_design_weights": design["ds"],
        "glm_design_weights": design["glm"],
        "bootstrap": N_BOOT,
        "bootstrap_unit": "template_family with replacement; 36 DS families, 31 GLM/common families",
    }

    meta["glm_parsed_by_condition"] = dict(Counter(
        r["condition"] for r in glm_final_valid))
    meta["glm_missing_parsed_by_condition"] = dict(Counter(
        r["condition"] for r in glm_final_all_valid if not r.get("parsed")))
    meta["glm_missing_pairwise_by_condition"] = dict(Counter(
        r["condition"] for r in raw_rows["glm-5.3-flash"]
        if r.get("task") == "pairwise" and not r.get("parsed")))

    result = {
        "meta": meta,
        "pointwise": {"deepseek_full": ds_point, "glm_subset": glm_point,
                      "deepseek_common": ds_common_point, "glm_common": glm_common_point},
        "paired": paired,
        "design_weight_sensitivity": design_sens,
        "judge_difference_common": judge_diff,
        "judge_moderation_target_hit": moderation,
        "pairwise": pw,
        "cross_pairwise": cross_pw,
        "cross_pointwise": cross_point,
        "glm_duplicate_sensitivity": {
            "n_duplicate_keys": len(glm_dup_keys),
        "n_final_duplicate_keys": len([k for k, v in Counter(
            r["record_key"] for r in raw_rows["glm-5.3-flash"]
            if r.get("task") == "judge" and r.get("variant") == "final").items() if v > 1]),
            "by_condition": dup_diff,
        },
        "retry": retry,
        "retry_quality": retry_quality_out,
        "cost": cost,
    }
    (AUD / "feedback_audit.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    return result


def key_pair(r):
    return (r["case_id"], r["student_type"], r["condition"])


if __name__ == "__main__":
    r = main()
    print(json.dumps(r["meta"], indent=1))
    print("paired DS one_shot", json.dumps(r["paired"]["deepseek_full"]["one_shot"], indent=1))
    print("paired GLM one_shot", json.dumps(r["paired"]["glm_subset"]["one_shot"], indent=1))
