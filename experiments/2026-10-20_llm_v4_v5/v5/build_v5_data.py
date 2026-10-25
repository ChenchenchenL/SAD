"""Build v5 authored banks, dev cases, and a frozen test set."""
from __future__ import annotations

import hashlib
import json
import random
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
import sys
sys.path.insert(0, str(HERE))

from v5_templates import CATEGORIES, CATEGORY_HIDS, build_items, canon

OUT = HERE / "data"
CFG = HERE / "config"
OUT.mkdir(exist_ok=True)
CFG.mkdir(exist_ok=True)

# True labels are those whose prediction vector differs from every other
# candidate in the category. Identical rules are kept as diagnosis candidates
# but cannot be assigned a reliable ground-truth label.
EXCLUDED_TRUE_LABELS = {
    "fractions.common_denominator_numerator",
    "subtraction.no_column_limit",
    "subtraction.decompose_by_place_value_label",
    "decimals.whole_number_thinking",
    "order_of_operations.pemdas_strictly_sequential",
}
TARGET_PER_TRUE = 3
DEV_TARGET = 1


def sha(obj) -> str:
    if isinstance(obj, Path):
        return hashlib.sha256(obj.read_bytes()).hexdigest()
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def stable_key(problem: str, answer: str, correct: str) -> str:
    return hashlib.sha256(f"{problem}\n{answer}\n{correct}".encode()).hexdigest()[:20]


def duplicate_hypotheses(bank_by_cat: dict[str, list[dict]]) -> dict[str, list[str]]:
    out = {}
    for cat, items in bank_by_cat.items():
        vectors = {}
        for hid in CATEGORY_HIDS[cat]:
            vectors[hid] = tuple(item["predictions"][hid] for item in items)
        dupes = defaultdict(list)
        for hid, vec in vectors.items():
            dupes[vec].append(hid)
        out[cat] = sorted([h for group in dupes.values() if len(group) > 1 for h in group])
    return out


def select_cases(bank_by_cat: dict[str, list[dict]], split: str, target: int, seed: int = 20261023) -> list[dict]:
    rng = random.Random(seed)
    cases = []
    for cat, items in bank_by_cat.items():
        for hid in CATEGORY_HIDS[cat]:
            if hid in EXCLUDED_TRUE_LABELS:
                continue
            rows = []
            by_family: dict[str, list[tuple[int, dict]]] = defaultdict(list)
            for idx, item in enumerate(items):
                if item["split"] != split:
                    continue
                if item["predictions"][hid] == item["correct"] or not item["applicable"][hid]:
                    continue
                by_family[item["family"]].append((idx, item))
            # interleave families to maximise structural diversity
            while any(by_family.values()) and len(rows) < target:
                for family in sorted(by_family):
                    if by_family[family]:
                        idx, item = by_family[family].pop(0)
                        rows.append((idx, item))
                        if len(rows) >= target:
                            break
            rng.shuffle(rows)
            for idx, item in rows[:target]:
                answer = item["predictions"][hid]
                ambiguity = sum(
                    1 for h in CATEGORY_HIDS[cat]
                    if item["applicable"][h] and item["predictions"][h] == answer
                )
                vector = tuple(x["predictions"][hid] for x in items)
                unique = sum(1 for x in items if x["predictions"][hid] != x["correct"]) >= 2
                cases.append(
                    {
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
                        "split": split,
                        "operation": item["operation"],
                        "v5_unique_error_vector": unique,
                        "key": stable_key(item["text"], answer, item["correct"]),
                    }
                )
    # stable ordering: category then malrule then family then text
    cases.sort(key=lambda c: (c["category"], c["true_id"], c["template_family"], c["problem"]))
    for i, case in enumerate(cases, 1):
        case["case_id"] = f"v5{split}:{i:04d}"
        case["test_version"] = f"v5_authored_{split}_2026-10-20"
    return cases


def main() -> None:
    items = build_items()
    # attach global item index for provenance
    for i, item in enumerate(items):
        item["item_id"] = f"v5i:{i:04d}"
    bank_by_cat: dict[str, list[dict]] = defaultdict(list)
    for item in items:
        bank_by_cat[item["category"]].append(item)

    dupes = duplicate_hypotheses(bank_by_cat)
    test_cases = select_cases(bank_by_cat, "test", TARGET_PER_TRUE)
    dev_cases = select_cases(bank_by_cat, "dev", DEV_TARGET)

    for cat in CATEGORIES:
        (OUT / f"bank_v5_{cat}.json").write_text(
            json.dumps({
                "category": cat,
                "settings": {
                    "builder": "v5_authored_structural_templates",
                    "level": 5,
                    "source": "human-authored templates, not MalruleLib generators",
                },
                "hypotheses": [{"id": h} for h in CATEGORY_HIDS[cat]],
                "items": bank_by_cat[cat],
            }, indent=1, ensure_ascii=False),
            encoding="utf-8",
        )
    (OUT / "cases_test_v5.json").write_text(json.dumps(test_cases, indent=1, ensure_ascii=False), encoding="utf-8")
    (OUT / "cases_dev_v5.json").write_text(json.dumps(dev_cases, indent=1, ensure_ascii=False), encoding="utf-8")

    families = sorted({c["template_family"] for c in test_cases})
    dev_families = sorted({c["template_family"] for c in dev_cases})
    overlap = set(families) & set(dev_families)
    freeze = {
        "version": "v5_authored_template_holdout_2026-10-20",
        "frozen_at": datetime.now(timezone.utc).isoformat(),
        "n_test_cases": len(test_cases),
        "n_dev_cases": len(dev_cases),
        "n_bank_items": len(items),
        "test_template_families": families,
        "dev_template_families": dev_families,
        "dev_test_family_overlap": sorted(overlap),
        "target_per_true_id": TARGET_PER_TRUE,
        "excluded_true_labels": sorted(EXCLUDED_TRUE_LABELS),
        "globally_indistinguishable_hypotheses": dupes,
        "n_true_labels": len({c["true_id"] for c in test_cases}),
        "n_per_category": dict(Counter(c["category"] for c in test_cases)),
        "n_per_true_id": dict(Counter(c["true_id"] for c in test_cases)),
        "sha256": {
            "cases_test_v5": sha(OUT / "cases_test_v5.json"),
            "cases_dev_v5": sha(OUT / "cases_dev_v5.json"),
            "v5_templates": sha(HERE / "v5_templates.py"),
            "v5_engine": sha(HERE / "v5_engine.py"),
            "build_script": sha(HERE / "build_v5_data.py"),
        },
    }
    (CFG / "v5_freeze.json").write_text(json.dumps(freeze, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: freeze[k] for k in ("n_test_cases", "n_dev_cases", "n_true_labels", "n_per_category", "dev_test_family_overlap")}, ensure_ascii=False, indent=2))
    print("duplicates", dupes)


if __name__ == "__main__":
    main()
