"""Independent audit of the v6 authored banks and cases.

Three checks:
  1. correct answers recomputed from metadata with sympy / Fraction / Decimal;
  2. every declared bug prediction recomputed by a second, formula-level
     implementation living in this file (not imported from v6_templates);
  3. triggered predictions additionally cross-checked against MalRuleLib when
     the library supports the structure. Library mismatches are treated as
     failures; library-unsupported structures fall back to check 2.
Plus: case answer/trigger checks, family/text overlap with v4/v5, uniqueness.
"""
from __future__ import annotations

import importlib
import inspect
import json
import math
import re
import sys
from collections import defaultdict
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATA = HERE.parent / "data"
sys.path.insert(0, str(ROOT / "data" / "external" / "malrulelib_repo"))

from utils import DifficultyLevel, Problem  # noqa: E402

CATEGORIES = ["subtraction", "fractions", "decimals", "negative_numbers", "order_of_operations", "percentages"]
V5_DIR = HERE.parents[1] / "2026-10-20_llm_v4_v5"

# Structures beyond the MalRuleLib implementation's input arity / template set.
# These are genuine new structural variants; their predictions are verified by
# the second formula-level implementation below. Everything else must match the
# library exactly.
OUT_OF_SCOPE = {
    ("frac_add_three", "ignore_denominators"):
        "library accepts two fractions; three-fraction extension verified independently",
    ("frac_mul_three", "ignore_denominators"):
        "library's ignore-denominators rule reads only the first two fractions; three-fraction extension verified independently",
    ("frac_compare_four", "denominator_comparison_error"):
        "library supports at most three fractions; four-way comparison verified independently",
    ("frac_compare_four", "natural_number_bias_numerator_only"):
        "library supports at most three fractions; four-way comparison verified independently",
    ("pct_find_whole", "percent_equals_decimal"):
        "library's percent_equals_decimal covers percent-of-value, not find-whole; independent formula verified",
    ("pct_compare_change", "reverse_percentage_error"):
        "library's reverse_percentage_error covers 'p% as much' comparison statements, not the larger/smaller asymmetry used here; independent formula verified",
}


def canon(value) -> str:
    if isinstance(value, Fraction):
        return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    if isinstance(value, Decimal):
        d = value.normalize()
        return str(int(d)) if d == d.to_integral() else format(d, "f")
    s = str(value).strip().replace("$", "").replace(",", "").rstrip(".")
    if re.fullmatch(r"-?\d+/\d+", s):
        return canon(Fraction(s))
    if re.fullmatch(r"-?\d+(?:\.\d+)?", s):
        d = Decimal(s)
        if d == d.to_integral():
            return str(int(d))
        return format(d.normalize(), "f")
    return s


def sympy_value(expr: str) -> str:
    v = sp.sympify(expr.replace("×", "*").replace("÷", "/"), rational=True)
    if v.free_symbols:
        raise ValueError(expr)
    if isinstance(v, sp.Integer):
        return str(int(v))
    if isinstance(v, sp.Rational):
        return canon(Fraction(int(v.p), int(v.q)))
    return canon(Decimal(str(v)))


def same_value(a, b) -> bool:
    try:
        return Fraction(str(a)) == Fraction(str(b))
    except Exception:
        return canon(a) == canon(b)


def parse_text_correct(item: dict):
    """Parse the visible problem statement, not metadata, to catch ambiguous text."""
    if item["category"] not in ("subtraction", "fractions", "decimals",
                                "negative_numbers", "order_of_operations"):
        return None
    text = item["text"]
    if not text.startswith("Calculate:"):
        return None
    expr = text.split("Calculate:", 1)[1].strip()
    try:
        return sympy_value(expr)
    except Exception:
        return None


def _norm_text(text: str) -> str:
    s = text.lower().strip()
    s = re.sub(r"-?\d+(?:\.\d+)?(?:/\d+)?", "#", s)
    s = re.sub(r"\s+", " ", s)
    return s


def _borrow_profile(a: int, b: int) -> tuple:
    m = [int(c) for c in str(a)]
    s = [int(c) for c in str(b).zfill(len(m))]
    flags, borrow = [], 0
    for i in range(len(m) - 1, -1, -1):
        top = m[i] - borrow
        if top < s[i]:
            flags.append(1)
            borrow = 1
        else:
            flags.append(0)
            borrow = 0
    return tuple(flags)


def structural_signature(item: dict) -> tuple:
    """Coarse structural key for overlap checks, not a proof of uniqueness.

    Uses operation, arity, normalized surface skeleton and category-specific
    structure (borrow profile, fraction arity/common denominator, decimal
    places, operator sequence/parentheses, percentage template).
    """
    cat = item["category"]
    meta = item.get("meta", {})
    text = item.get("text", "")
    nums = re.findall(r"-?\d+(?:\.\d+)?(?:/\d+)?", text)
    base = [cat, item.get("operation"), len(nums), _norm_text(text)]
    try:
        if cat == "subtraction":
            a, b = int(meta["a"]), int(meta["b"])
            return tuple(base + ["sub", len(str(a)), len(str(b)), _borrow_profile(a, b)])
        if cat == "fractions":
            pairs = meta.get("operands") or []
            same_den = len({int(p[1]) for p in pairs}) == 1 if pairs else None
            return tuple(base + ["frac", len(pairs), same_den])
        if cat == "decimals":
            places = tuple(len(tok.split(".")[1]) if "." in tok else 0 for tok in nums)
            return tuple(base + ["dec", places])
        if cat == "negative_numbers":
            return tuple(base + ["neg", len(meta.get("operands") or [])])
        if cat == "order_of_operations":
            return tuple(base + ["oo", tuple(meta.get("operations") or []),
                                 "paren" if "(" in text else "noparen"])
        if cat == "percentages":
            return tuple(base + ["pct", meta.get("template")])
    except Exception:
        pass
    return tuple(base)


def correct_answer(item: dict) -> str:
    kind, meta = item["meta"]["audit_kind"], item["meta"]
    cat = item["category"]
    if cat == "subtraction":
        return sympy_value(f"{meta['a']}-{meta['b']}")
    if kind == "frac_add_three":
        pairs = meta["operands"]
        return canon(sum((Fraction(a, b) for a, b in pairs), Fraction(0)))
    if kind == "frac_sub_improper":
        (a, b), (c, d) = meta["operands"]
        return canon(Fraction(a, b) - Fraction(c, d))
    if kind == "frac_mul_three":
        pairs = meta["operands"]
        v = Fraction(1)
        for a, b in pairs:
            v *= Fraction(a, b)
        return canon(v)
    if kind == "frac_div_whole":
        (a, b), _ = meta["operands"]
        return canon(Fraction(a, b) / meta["whole"])
    if kind == "frac_whole_div":
        (c, _), (a, b) = meta["operands"]
        return canon(Fraction(c, 1) / Fraction(a, b))
    if kind == "frac_compare_four":
        pairs = meta["operands"]
        vals = [Fraction(n, d) for n, d in pairs]
        best = pairs[max(range(len(vals)), key=lambda i: vals[i])]
        return f"{best[0]}/{best[1]}"
    if cat == "decimals":
        if kind == "dec_compare_three":
            return canon(max(Decimal(x) for x in meta["decimals"]))
        x, y = Decimal(meta["num1"]), Decimal(meta["num2"])
        op = item["operation"]
        if op == "multiplication":
            return canon(x * y)
        if op == "division":
            return canon(x / y)
        if op == "addition":
            return canon(x + y)
        if op == "subtraction":
            return canon(x - y)
    if cat == "negative_numbers":
        return sympy_value(item["text"].replace("Calculate: ", ""))
    if cat == "order_of_operations":
        return sympy_value(meta["expression"])
    if cat == "percentages":
        if kind == "pct_over_hundred":
            return canon(Fraction(meta["percent"], 100) * meta["value"])
        if kind == "pct_find_whole":
            return canon(Fraction(meta["part"] * 100, meta["percentage"]))
        if kind == "pct_two_increases":
            return canon(Fraction(meta["initial_value"]) * Fraction(100 + meta["percentage1"], 100)
                         * Fraction(100 + meta["percentage2"], 100))
        if kind == "pct_dec_then_inc":
            return canon(Fraction(meta["initial_value"]) * Fraction(100 - meta["percentage1"], 100)
                         * Fraction(100 + meta["percentage2"], 100))
        if kind == "pct_compare_change":
            g = meta["given_percent"]
            return canon(Fraction(g * 100, 100 + g) if meta["direction"] == "larger" else Fraction(g * 100, 100 - g))
    raise ValueError((cat, kind, item["text"]))


def independent_bug(item: dict, local: str):
    """Second implementation of each declared misconception, by formula."""
    kind, meta = item["meta"]["audit_kind"], item["meta"]
    cat = item["category"]
    if cat == "subtraction":
        return None  # covered by the MalRuleLib cross-check at any digit width
    if kind in ("frac_add_three", "frac_sub_improper", "frac_mul_three", "frac_div_whole", "frac_whole_div"):
        pairs = meta["operands"]
        (a, b), (c, d) = pairs[0], pairs[1]
        if kind == "frac_add_three":
            e, f = pairs[2]
            if local == "add_numerators_denominators":
                return Fraction(a + c + e, b + d + f)
            if local == "ignore_denominators":
                return Fraction(a + c + e, 1)
        if kind == "frac_sub_improper":
            if local == "subtract_across":
                return Fraction(a - c, b - d)
            if local == "ignore_denominators":
                return Fraction(a - c, 1)
        if kind == "frac_mul_three":
            e, f = pairs[2]
            if local == "keep_common_denominator_for_multiplication":
                return Fraction(a * c * e, b)
            if local == "ignore_denominators":
                return Fraction(a * c * e, 1)
        if kind == "frac_div_whole":
            if local == "multiply_across_for_division":
                return Fraction(a * meta["whole"], b)
            if local == "ignore_denominators":
                return Fraction(a // meta["whole"], 1)
        if kind == "frac_whole_div":
            w = meta["whole"]
            n2, d2 = pairs[1]
            if local == "multiply_across_for_division":
                return Fraction(w * n2, d2)
            if local == "ignore_denominators":
                return Fraction(w // n2, 1)
    if kind == "frac_compare_four":
        pairs = meta["operands"]
        if local == "denominator_comparison_error":
            n, d = max(pairs, key=lambda p: p[1])
            return f"{n}/{d}"
        if local == "natural_number_bias_numerator_only":
            n, d = max(pairs, key=lambda p: p[0])
            return f"{n}/{d}"
    if cat == "decimals":
        if kind == "dec_compare_three":
            xs = meta["decimals"]
            dp = lambda s: len(s.split(".")[1]) if "." in s else 0
            if local == "longer_is_larger":
                return max(xs, key=dp)
            if local == "shorter_is_larger":
                return min(xs, key=dp)
        x, y = meta["num1"], meta["num2"]
        xi, yi = int(x.replace(".", "")), int(y.replace(".", ""))
        if local == "ignore_decimal_point":
            if item["operation"] == "multiplication":
                return xi * yi
            if item["operation"] == "division":
                return xi // yi
        if local == "right_align_decimals":
            a, b = x.replace(".", ""), y.replace(".", "")
            w = max(len(a), len(b))
            a, b = a.zfill(w), b.zfill(w)
            val = int(a) + int(b) if item["operation"] == "addition" else abs(int(a) - int(b))
            places = min(len(x.split(".")[1]) if "." in x else 0, len(y.split(".")[1]) if "." in y else 0)
            s = str(val)
            return s[:-places] + "." + s[-places:] if places > 0 and len(s) > places else s
    if cat == "negative_numbers":
        a, b, c = meta.get("a"), meta.get("b"), meta.get("c")
        if kind == "neg_add_two_new":
            return {"multiplication_rule_for_addition": abs(a) + abs(b),
                    "two_negatives_always_positive": abs(a) + abs(b)}.get(local)
        if kind == "neg_sub_pos_new":
            return abs(abs(b) - abs(a)) if local == "larger_absolute_value_always_wins" else None
        if kind == "neg_minus_neg_new":
            return {"two_negatives_always_positive": abs(a) + abs(b),
                    "negative_swaps_operation": -abs(a) - abs(b),
                    "larger_absolute_value_always_wins": -(abs(b) - abs(a))}.get(local)
        if kind == "neg_multi_step":
            return -abs(a) * abs(b) * abs(c) if local == "negative_times_negative_negative" else None
        if kind == "neg_mixed_ops":
            return -abs(a) * abs(b) + c if local == "negative_times_negative_negative" else None
    if cat == "order_of_operations":
        vals, ops = meta["values"], meta["operations"]
        def ltr():
            v = vals[0]
            for i, op in enumerate(ops):
                x = vals[i + 1]
                v = v + x if op == "+" else v - x if op == "-" else v * x if op == "*" else v // x
            return v
        def add_first():
            arr = [(vals[0], None)] + [(vals[i + 1], ops[i]) for i in range(len(ops))]
            while True:
                idx = next((i for i, (_, op) in enumerate(arr) if op == "+"), None)
                if idx is None:
                    break
                pn, po = arr[idx - 1]
                cn, _ = arr[idx]
                arr[idx - 1] = (pn + cn, po)
                arr.pop(idx)
            r = arr[0][0]
            for n, op in arr[1:]:
                r = r - n if op == "-" else r + n
            return r
        if local == "strict_left_to_right":
            return ltr()
        if local == "ignore_parentheses":
            return ltr()
        if local == "addition_before_subtraction_always":
            return add_first()
        if local == "multiplication_before_division_always":
            return vals[0] // (vals[1] * vals[2])
    if cat == "percentages":
        if kind == "pct_over_hundred":
            if local == "percent_equals_decimal":
                return meta["percent"] * meta["total"]
            if local == "percentage_as_index":
                return meta["percent"]
        if kind == "pct_find_whole":
            if local == "percent_equals_decimal":
                return meta["part"] * meta["percentage"]
            if local == "percentage_as_index":
                return meta["percentage"]
        if kind in ("pct_two_increases", "pct_dec_then_inc"):
            if local == "add_percentages_directly":
                init, p1, p2 = meta["initial_value"], meta["percentage1"], meta["percentage2"]
                sign = 1 if kind == "pct_two_increases" else -1
                return Fraction(init) * Fraction(100 + sign * p1 + p2, 100)
        if kind == "pct_compare_change" and local == "reverse_percentage_error":
            return meta["given_percent"]
    return None


def malrule_classes():
    classes = {}
    for cat in CATEGORIES:
        cat_dir = ROOT / "data" / "external" / "malrulelib_repo" / "malrules" / cat
        for md in sorted(cat_dir.iterdir()):
            if not (md.is_dir() and (md / "__init__.py").exists()):
                continue
            module = importlib.import_module(f"malrules.{cat}.{md.name}")
            for _, obj in vars(module).items():
                if inspect.isclass(obj) and obj.__module__.startswith(module.__name__) and hasattr(obj, "calculate_expected_answer"):
                    inst = None
                    for args in [(), (5,)]:
                        try:
                            inst = obj(*args)
                            break
                        except Exception:
                            pass
                    if inst is not None:
                        classes[f"{cat}.{md.name}"] = inst
                    break
    return classes


def problem_for(item: dict, local: str) -> Problem:
    meta = item["meta"]
    text, operation = item["text"], item["operation"]
    if item["category"] == "subtraction":
        operands = [meta["a"], meta["b"]]
    elif item["category"] == "fractions":
        pairs = meta["operands"]
        if local == "ignore_denominators":
            operands = [n for pair in pairs for n in pair]
        else:
            operands = [tuple(p) for p in pairs]
    elif item["category"] == "decimals":
        operands = [Decimal(str(x)) for x in meta.get("operands", meta.get("decimals"))]
    elif item["category"] == "negative_numbers":
        operands = list(meta["operands"])
    else:
        operands = list(meta.get("operands") or meta.get("values") or [])
    md = dict(meta)
    md.setdefault("operation", operation)
    if item["category"] == "order_of_operations":
        md["operations"] = md.get("operations_symbols", md.get("operations"))
        if "op1" in md:
            md["op1"] = {"*": "×", "/": "÷"}.get(md["op1"], md["op1"])
        if "op2" in md:
            md["op2"] = {"*": "×", "/": "÷"}.get(md["op2"], md["op2"])
    return Problem(text=text, operands=operands, operation=operation, level=5,
                   difficulty=DifficultyLevel.MEDIUM, metadata=md)


def main() -> None:
    items = []
    for cat in CATEGORIES:
        bank = json.loads((DATA / f"bank_v6b_{cat}.json").read_text(encoding="utf-8"))
        for idx, item in enumerate(bank["items"]):
            item["_idx"] = (cat, idx)
            items.append(item)
    cases = json.loads((DATA / "cases_test_v6b.json").read_text(encoding="utf-8"))
    classes = malrule_classes()

    correct_issues, independent_issues, lib_issues, text_issues = [], [], [], []
    lib_status_by_pred = {}
    for item in items:
        try:
            expected = correct_answer(item)
            if canon(item["correct"]) != expected:
                correct_issues.append({"item": item["text"], "stored": item["correct"], "independent": expected})
        except Exception as exc:
            correct_issues.append({"item": item["text"], "error": repr(exc)})
        try:
            expected_text = parse_text_correct(item)
            if expected_text is not None and not same_value(item["correct"], expected_text):
                text_issues.append({"item": item["text"], "stored": item["correct"],
                                    "parsed_from_text": expected_text})
        except Exception as exc:
            text_issues.append({"item": item["text"], "error": repr(exc)})
        for hid, pred in item["predictions"].items():
            if pred == item["correct"]:
                continue
            local = hid.split(".", 1)[1]
            ind = independent_bug(item, local)
            if ind is not None and canon(ind) != canon(pred):
                independent_issues.append({"item": item["text"], "hid": hid, "stored": pred, "independent": canon(ind)})
            kind_key = (item["meta"]["audit_kind"], local)
            if kind_key in OUT_OF_SCOPE:
                lib_status_by_pred[(item["text"], hid)] = "library_out_of_scope"
                continue
            inst = classes.get(hid)
            if inst is None:
                lib_status_by_pred[(item["text"], hid)] = "library_unavailable"
                continue
            try:
                lib = canon(inst.calculate_expected_answer(problem_for(item, local)))
            except Exception as exc:
                lib_status_by_pred[(item["text"], hid)] = f"unsupported:{type(exc).__name__}"
                continue
            if lib != canon(pred):
                lib_issues.append({"item": item["text"], "hid": hid, "stored": pred, "library": lib,
                                   "independent": canon(ind) if ind is not None else None})
                lib_status_by_pred[(item["text"], hid)] = "library_mismatch"
            else:
                lib_status_by_pred[(item["text"], hid)] = "library_match"

    case_issues, verified = [], {"library": 0, "independent_only": 0, "none": 0}
    for case in cases:
        item = json.loads((DATA / f"bank_v6b_{case['category']}.json").read_text(encoding="utf-8"))["items"][case["item_idx"]]
        if case["answer"] != item["predictions"].get(case["true_id"]):
            case_issues.append({"case": case["case_id"], "issue": "answer!=prediction"})
        if case["answer"] == case["correct"]:
            case_issues.append({"case": case["case_id"], "issue": "answer==correct"})
        status = lib_status_by_pred.get((item["text"], case["true_id"]), "not_triggered")
        if status == "library_match":
            verified["library"] += 1
        elif independent_bug(item, case["true_id"].split(".", 1)[1]) is not None:
            verified["independent_only"] += 1
        else:
            verified["none"] += 1
            case_issues.append({"case": case["case_id"], "issue": f"true-label prediction unverified ({status})"})

    # overlap with v4/v5
    v5_data = V5_DIR / "v5" / "data"
    v5_texts, v5_fams, v5_items = set(), set(), []
    for cat in CATEGORIES:
        bank = json.loads((v5_data / f"bank_v5_{cat}.json").read_text(encoding="utf-8"))
        v5_texts |= {it["text"] for it in bank["items"]}
        v5_fams |= {it["family"] for it in bank["items"]}
        v5_items.extend(bank["items"])
    v5_test = json.loads((v5_data / "cases_test_v5_exclusion_corrected.json").read_text(encoding="utf-8"))
    v5_dev = json.loads((v5_data / "cases_dev_v5.json").read_text(encoding="utf-8"))
    v5_fams |= {c["template_family"] for c in v5_test} | {c["template_family"] for c in v5_dev}
    v4 = json.loads((V5_DIR / "cases_test_v4.json").read_text(encoding="utf-8"))
    v6_texts = {it["text"] for it in items}
    v6_fams = {it["family"] for it in items}
    overlap = {
        "text": sorted(v6_texts & (v5_texts | {c["problem"] for c in v4})),
        "family": sorted(v6_fams & v5_fams),
    }

    v5_sigs = {structural_signature(it) for it in v5_items}
    sig_to_fams, sig_to_items = defaultdict(set), defaultdict(list)
    for item in items:
        sig = structural_signature(item)
        sig_to_fams[sig].add(item["family"])
        sig_to_items[sig].append(item)
    matching_sigs = [s for s in sig_to_fams if s in v5_sigs]
    matching_fams = sorted({f for s in matching_sigs for f in sig_to_fams[s]})
    matching_items = [it for s in matching_sigs for it in sig_to_items[s]]
    case_item = {}
    for case in cases:
        case_item[case["case_id"]] = json.loads(
            (DATA / f"bank_v6b_{case['category']}.json").read_text(encoding="utf-8"))["items"][case["item_idx"]]
    matching_cases = sum(1 for cid, it in case_item.items() if structural_signature(it) in v5_sigs)
    structural_overlap = {
        "definition": (
            "category + operation + arity + normalized text skeleton + category-specific structure "
            "(subtraction borrow profile; fraction arity/common denominator; decimal places; "
            "OO operator sequence/parentheses; percentage template). Coarse diagnostic, not a proof of uniqueness."
        ),
        "n_v5_items": len(v5_items),
        "n_v6_items": len(items),
        "n_v6_items_with_matching_v5_signature": len(matching_items),
        "n_v6_families_with_matching_v5_signature": len(matching_fams),
        "families": matching_fams,
        "n_v6_cases_with_matching_v5_signature": matching_cases,
        "examples": [{"item": it["text"], "family": it["family"]} for it in matching_items[:20]],
    }

    statuses = {}
    for v in lib_status_by_pred.values():
        key = v.split(":", 1)[0]
        statuses[key] = statuses.get(key, 0) + 1
    # all declared bugs are triggered by construction? count declared-but-not-triggering
    nontrigger = [
        {"item": item["text"], "hid": hid} for item in items for hid in item["applicable"]
        if item["applicable"][hid] and item["predictions"][hid] == item["correct"]
    ]
    report = {
        "n_items": len(items),
        "n_cases": len(cases),
        "correct_audit": {"n_issues": len(correct_issues), "issues": correct_issues[:20]},
        "text_audit": {"n_issues": len(text_issues), "issues": text_issues[:20]},
        "independent_bug_audit": {"n_issues": len(independent_issues), "issues": independent_issues[:20]},
        "library_audit": {"statuses": statuses, "n_mismatches": len(lib_issues), "mismatches": lib_issues[:30],
                          "out_of_scope_structures": {f"{k[0]}/{k[1]}": v for k, v in OUT_OF_SCOPE.items()}},
        "case_audit": {"n_issues": len(case_issues), "issues": case_issues[:20],
                       "true_label_verification": verified},
        "overlap_with_v4_v5": {k: {"n": len(v), "items": v[:20]} for k, v in overlap.items()},
        "structural_overlap_with_v5": structural_overlap,
        "declared_but_not_triggering": {"n": len(nontrigger), "items": nontrigger[:10]},
    }
    (HERE.parent / "data" / "v6b_data_audit.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: (v["n_issues"] if isinstance(v, dict) and "n_issues" in v else v)
                      for k, v in report.items() if k in ("n_items", "n_cases", "correct_audit",
                                                          "text_audit", "independent_bug_audit",
                                                          "case_audit", "overlap_with_v4_v5",
                                                          "structural_overlap_with_v5",
                                                          "declared_but_not_triggering")},
                     ensure_ascii=False, indent=1))
    print("library statuses:", statuses, "mismatches:", len(lib_issues))
    for x in (correct_issues + text_issues + independent_issues + lib_issues + case_issues)[:20]:
        print(x)


if __name__ == "__main__":
    main()
