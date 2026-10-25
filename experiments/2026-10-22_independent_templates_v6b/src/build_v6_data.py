"""Build the v6 independent banks/cases and freeze them before any LLM call.

Selection is deterministic and outcome-blind: for each of the 30 true labels,
eligible items (label triggers, applicable) are grouped by family and taken
round-robin in sorted order until 3 cases are chosen.
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from v6_templates import CATEGORIES, CATEGORY_HIDS, build_items  # noqa: E402

DATA = HERE.parent / "data"
DATA.mkdir(exist_ok=True)

V5_DIR = HERE.parents[1] / "2026-10-20_llm_v4_v5"
V5_DATA = V5_DIR / "v5" / "data"
V5_OUT = V5_DIR / "v5" / "out"
TARGET_PER_LABEL = 3

# Same five labels v5 excludes as unreliable/indistinguishable true labels.
EXCLUDED_TRUE_LABELS = {
    "fractions.common_denominator_numerator",
    "subtraction.no_column_limit",
    "subtraction.decompose_by_place_value_label",
    "decimals.whole_number_thinking",
    "order_of_operations.pemdas_strictly_sequential",
}


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: Path) -> str:
    return sha_bytes(p.read_bytes())


def stable_key(problem: str, answer: str, correct: str) -> str:
    return hashlib.sha256(f"{problem}\n{answer}\n{correct}".encode()).hexdigest()[:20]


def duplicate_vectors(bank_by_cat: dict[str, list[dict]]) -> dict[str, list[str]]:
    out = {}
    for cat, items in bank_by_cat.items():
        vectors = {hid: tuple(it["predictions"][hid] for it in items) for hid in CATEGORY_HIDS[cat]}
        groups = defaultdict(list)
        for hid, vec in vectors.items():
            groups[vec].append(hid)
        out[cat] = sorted(h for group in groups.values() if len(group) > 1 for h in group)
    return out


def select_cases(bank_by_cat: dict[str, list[dict]]) -> tuple[list[dict], dict]:
    cases, report = [], {}
    for cat, items in bank_by_cat.items():
        for hid in CATEGORY_HIDS[cat]:
            if hid in EXCLUDED_TRUE_LABELS:
                continue
            by_family: dict[str, list[tuple[int, dict]]] = defaultdict(list)
            for idx, item in enumerate(items):
                if not item["applicable"].get(hid):
                    continue
                if item["predictions"][hid] == item["correct"]:
                    continue
                by_family[item["family"]].append((idx, item))
            picked = []
            while len(picked) < TARGET_PER_LABEL and any(by_family.values()):
                for fam in sorted(by_family):
                    if by_family[fam] and len(picked) < TARGET_PER_LABEL:
                        picked.append(by_family[fam].pop(0))
            report[hid] = {"n_eligible": sum(len(v) for v in by_family.values()) + len(picked),
                           "n_families": len({it["family"] for _, it in picked}),
                           "n_picked": len(picked)}
            for idx, item in picked:
                answer = item["predictions"][hid]
                ambiguity = sum(1 for h in CATEGORY_HIDS[cat]
                                if item["applicable"].get(h) and item["predictions"][h] == answer)
                unique = sum(1 for x in items if x["predictions"][hid] != x["correct"]) >= 2
                cases.append({
                    "case_id": "",
                    "category": cat,
                    "true_id": hid,
                    "item_idx": idx,
                    "problem": item["text"],
                    "base_problem": item["text"],
                    "correct": item["correct"],
                    "answer": answer,
                    "ambiguity": ambiguity,
                    "template_family": item["family"],
                    "split": "test",
                    "operation": item["operation"],
                    "v6_unique_error_vector": unique,
                    "key": stable_key(item["text"], answer, item["correct"]),
                })
    cases.sort(key=lambda c: (c["category"], c["true_id"], c["template_family"], c["problem"]))
    for i, case in enumerate(cases, 1):
        case["case_id"] = f"v6test:{i:04d}"
        case["test_version"] = "v6b_independent_2026-10-22"
    return cases, report


def main() -> None:
    items = build_items()
    for i, item in enumerate(items):
        item["item_id"] = f"v6i:{i:04d}"
    bank_by_cat: dict[str, list[dict]] = defaultdict(list)
    for item in items:
        bank_by_cat[item["category"]].append(item)

    dupes = duplicate_vectors(bank_by_cat)
    cases, label_report = select_cases(bank_by_cat)

    missing = [hid for hid, r in label_report.items() if r["n_picked"] < TARGET_PER_LABEL]
    if missing:
        print("FATAL: labels with <3 eligible/picked items:", missing)
        sys.exit(1)

    # ---- integrity checks (outcome-blind) ----
    problems = []
    for case in cases:
        item = bank_by_cat[case["category"]][case["item_idx"]]
        if case["answer"] != item["predictions"][case["true_id"]]:
            problems.append(("answer!=pred", case["case_id"]))
        if case["answer"] == case["correct"]:
            problems.append(("answer==correct", case["case_id"]))
        if not item["applicable"].get(case["true_id"]):
            problems.append(("not_applicable", case["case_id"]))
    fams = sorted({c["template_family"] for c in cases})
    n_unique_keys = len({c["key"] for c in cases})
    if problems:
        print("FATAL integrity problems:", problems[:10])
        sys.exit(1)

    # ---- overlap checks against v4/v5 ----
    v5_cases = json.loads((V5_DATA / "cases_test_v5_exclusion_corrected.json").read_text(encoding="utf-8"))
    v5_dev = json.loads((V5_DATA / "cases_dev_v5.json").read_text(encoding="utf-8"))
    v4_cases = json.loads((V5_DIR / "cases_test_v4.json").read_text(encoding="utf-8"))
    v5_texts = set()
    v5_fams = set()
    for cat in CATEGORIES:
        bank = json.loads((V5_DATA / f"bank_v5_{cat}.json").read_text(encoding="utf-8"))
        v5_texts |= {it["text"] for it in bank["items"]}
        v5_fams |= {it["family"] for it in bank["items"]}
    v5_fams |= {c["template_family"] for c in v5_cases} | {c["template_family"] for c in v5_dev}
    v4_texts = {c["problem"] for c in v4_cases}
    text_overlap = sorted({c["problem"] for c in cases} & (v5_texts | v4_texts))
    family_overlap = sorted(set(fams) & v5_fams)

    for cat in CATEGORIES:
        (DATA / f"bank_v6b_{cat}.json").write_text(json.dumps({
            "category": cat,
            "settings": {"builder": "v6b_corrected_independent_authored_templates",
                         "source": "v6 corrected for F1/F2; text/family disjoint from v5/v4, partial structural overlap"},
            "hypotheses": [{"id": h} for h in CATEGORY_HIDS[cat]],
            "items": bank_by_cat[cat],
        }, indent=1, ensure_ascii=False), encoding="utf-8")
    (DATA / "cases_test_v6b.json").write_text(json.dumps(cases, indent=1, ensure_ascii=False), encoding="utf-8")

    freeze = {
        "version": "v6b_independent_templates_2026-10-22",
        "frozen_at": datetime.now(timezone.utc).isoformat(),
        "n_items": len(items),
        "n_cases": len(cases),
        "n_unique_case_keys": n_unique_keys,
        "n_true_labels": len({c["true_id"] for c in cases}),
        "n_families": len(fams),
        "families": fams,
        "n_per_category": dict(Counter(c["category"] for c in cases)),
        "n_per_true_id": dict(Counter(c["true_id"] for c in cases)),
        "label_selection_report": label_report,
        "globally_indistinguishable_hypotheses": dupes,
        "text_overlap_with_v4_or_v5": text_overlap,
        "family_overlap_with_v5": family_overlap,
        "ambiguity_distribution": dict(Counter(c["ambiguity"] for c in cases)),
        "sha256": {
            "cases_test_v6b": sha_file(DATA / "cases_test_v6b.json"),
            "templates": sha_file(HERE / "v6_templates.py"),
            "build_script": sha_file(Path(__file__)),
            **{f"bank_v6b_{cat}": sha_file(DATA / f"bank_v6b_{cat}.json") for cat in CATEGORIES},
        },
    }
    (DATA / "v6b_freeze.json").write_text(json.dumps(freeze, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: freeze[k] for k in ("n_items", "n_cases", "n_true_labels", "n_families",
                                             "n_per_category", "text_overlap_with_v4_or_v5",
                                             "family_overlap_with_v5", "ambiguity_distribution")},
                     ensure_ascii=False, indent=1))
    print("indistinguishable hypotheses:", dupes)
    print("NOTE: text/family-name overlap only. Structural overlap is audited separately in v6b_data_audit.json.")
    weak = {h: r for h, r in label_report.items() if r["n_eligible"] < 3 or r["n_families"] < 2}
    print("labels with <3 eligible or single-family cases:", weak)


if __name__ == "__main__":
    main()
