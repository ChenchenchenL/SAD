"""Recompute protocol-valid feedback metrics, excluding implementation-bug cases."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
EXCLUDED_CASES = {"v5test:0013", "v5test:0014", "v5test:0015"}
FIELDS = ("true_target_hit", "misleading", "answer_leak", "math_correct", "new_example",
          "practice_without_answer", "overclaims_misconception", "actionable_next_step", "overall")

def load_jsonl(p):
    p = Path(p)
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]

feedback = {r["cache_key"]: r for r in load_jsonl(OUT / "feedback_v5.jsonl")}

import sys
sys.path.insert(0, str(HERE))
from feedback_v5 import strata

episodes = json.loads((OUT / "test_category_eps05_corrected_episodes.json").read_text(encoding="utf-8"))
primary = {}
for ep in episodes:
    if ep["seed"] == 0 and ep["rule"] == "stability_mixed" and ep.get("selection") == "maxent":
        primary[(ep["student_type"], ep["case_id"])] = ep
pop_counts = Counter(k for k, v in strata(primary).items() for _ in v)
population = {k: sum(len(v) for kk, v in strata(primary).items() if kk == k) for k in pop_counts}
# Correct population from strata keys and list lengths
population = {k: len(v) for k, v in strata(primary).items()}
sample = Counter(r["stratum"] for r in feedback.values() if r["condition"] == "pipeline" and r["case_id"] not in EXCLUDED_CASES)
weights = {s: population[s] / sample[s] for s in sample if sample[s]}
# Update cache-side weights for later aggregation.
rows = []
for r in feedback.values():
    if r["case_id"] in EXCLUDED_CASES:
        continue
    rr = dict(r)
    rr["weight"] = weights[r["stratum"]]
    rr["population_n"] = population[r["stratum"]]
    rr["sample_n"] = sample[r["stratum"]]
    rows.append(rr)

def model_slug(model):
    import re
    return re.sub(r"[^A-Za-z0-9]+", "_", model)

def judge_rows(model):
    rows = {}
    for path in sorted(OUT.glob(f"judge_v5_{model_slug(model)}*.jsonl")):
        for r in load_jsonl(path):
            if r.get("model") == model:
                rows.setdefault((r.get("task"), r["record_key"]), r)
    return list(rows.values())

def pointwise(model, variant="final"):
    judge = judge_rows(model)
    rows_by = {(r["case_id"], r["student_type"], r["condition"]): r for r in rows}
    out = {}
    for cond in ("oracle", "pipeline", "one_shot", "no_diagnosis"):
        sub = [r for r in judge if r.get("task") == "judge" and r.get("variant") == variant and r["condition"] == cond
               and r.get("http_status") == 200 and r.get("parsed") and r["case_id"] not in EXCLUDED_CASES]
        vals = {"n": len(sub)}
        for f in FIELDS:
            vals[f] = sum(r["parsed"].get(f, 0) for r in sub if isinstance(r["parsed"].get(f), (int, float))) / max(1, len(sub))
            wsum = den = 0.0
            for r in sub:
                source = rows_by.get((r["case_id"], r["student_type"], r["condition"]))
                if source and isinstance(r["parsed"].get(f), (int, float)):
                    wsum += source["weight"] * r["parsed"][f]
                    den += source["weight"]
            vals["weighted_" + f] = wsum / den if den else None
        out[cond] = vals
    return out

def pairwise(model):
    judge = [r for r in judge_rows(model) if r.get("task") == "pairwise" and r.get("http_status") == 200
             and r.get("parsed") and r["case_id"] not in EXCLUDED_CASES]
    by = defaultdict(dict)
    for r in judge:
        by[(r["case_id"], r["student_type"], r["condition"])][r["order"]] = r
    counts = Counter(); weighted = Counter(); inconsistent = 0
    for key, orders in by.items():
        if len(orders) != 2:
            continue
        first, second = key[2].split("_vs_")
        x, y = orders["ab"]["parsed"].get("winner"), orders["ba"]["parsed"].get("winner")
        if x is None or y is None:
            continue
        if x == "tie" or y == "tie":
            result = "tie"
        elif x == "A" and y == "B":
            result = first
        elif x == "B" and y == "A":
            result = second
        else:
            result = "inconsistent"; inconsistent += 1
        counts[(key[1], key[2], result)] += 1
        weighted[(key[1], key[2], result)] += orders["ab"]["weight"]
    return {"counts": {f"{a}/{b}/{c}": n for (a,b,c),n in sorted(counts.items())},
            "weighted": {f"{a}/{b}/{c}": v for (a,b,c),v in sorted(weighted.items())},
            "inconsistent": inconsistent, "n": len(by)}

def cross():
    def j(model):
        return {(r["case_id"], r["student_type"], r["condition"], r["variant"]): r["parsed"]
                for r in judge_rows(model) if r.get("task") == "judge" and r.get("http_status") == 200
                and r["case_id"] not in EXCLUDED_CASES}
    a, b = j("deepseek-v4.1-flash"), j("glm-5.3-flash")
    common = set(a) & set(b)
    out = {"n": len(common)}
    for f in ("true_target_hit", "misleading", "answer_leak", "overclaims_misconception", "new_example",
              "practice_without_answer", "actionable_next_step"):
        vals = [(a[k].get(f), b[k].get(f)) for k in common if isinstance(a[k].get(f), int) and isinstance(b[k].get(f), int)]
        out[f] = sum(x == y for x, y in vals) / len(vals) if vals else None
    overall = [(a[k].get("overall"), b[k].get("overall")) for k in common if isinstance(a[k].get("overall"), (int, float)) and isinstance(b[k].get("overall"), (int, float))]
    out["overall_mae"] = sum(abs(x-y) for x,y in overall)/len(overall) if overall else None
    def pw(model):
        return {(r["case_id"], r["student_type"], r["condition"], r["order"]): r["parsed"].get("winner")
                for r in judge_rows(model) if r.get("task") == "pairwise" and r.get("http_status") == 200
                and r["case_id"] not in EXCLUDED_CASES}
    p1, p2 = pw("deepseek-v4.1-flash"), pw("glm-5.3-flash")
    commonp = set(p1) & set(p2)
    out["pairwise"] = {
        "n": len(commonp),
        "winner_agreement": sum(p1[k] == p2[k] for k in commonp)/len(commonp) if commonp else None,
        "ties": sum(p1[k] == "tie" or p2[k] == "tie" for k in commonp)/len(commonp) if commonp else None,
    }
    return out

models = ["deepseek-v4.1-flash", "glm-5.3-flash"]
def retry_ablation(models):
    combined = {}
    for model in models:
        rows = [r for r in judge_rows(model) if r.get("task") == "judge" and r.get("variant") in ("raw", "final") and r.get("http_status") == 200]
        raw = {(r["case_id"], r["student_type"], r["condition"]): r for r in rows if r.get("variant") == "raw"}
        final = {(r["case_id"], r["student_type"], r["condition"]): r for r in rows if r.get("variant") == "final"}
        common = set(raw) & set(final)
        d = {"n": len(common)}
        for label, source in (("raw", raw), ("final", final)):
            vals = [source[k]["parsed"] for k in common]
            for f in ("overall", "math_correct", "true_target_hit", "misleading", "answer_leak", "actionable_next_step"):
                xs = [v[f] for v in vals if isinstance(v.get(f), (int, float))]
                d[f"{label}_{f}"] = sum(xs) / len(xs) if xs else None
        combined[model] = d
    return combined

result = {
    "protocol_valid_population": dict(population),
    "protocol_valid_sample": dict(sample),
    "protocol_valid_weights": weights,
    "pointwise": {m: pointwise(m) for m in models},
    "pairwise": {m: pairwise(m) for m in models},
    "retry_ablation": retry_ablation(models),
    "cross": cross(),
}
(OUT / "feedback_v5_protocol_valid_summary.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(result, indent=2, ensure_ascii=False)[:8000])
