"""Independent audit of v5 authored bank and cases.

The audit deliberately does not import the buggy generators from
v5_templates.py.  Correct answers are recomputed from metadata with
sympy / Fraction / Decimal.  Error answers are cross-checked against the
MalruleLib malrule implementation when that implementation can be called
without feeding it the answer itself.  The remaining error outputs require an
explicit manually reviewed example in MANUAL_EXPECTED_BUGS below.
"""
from __future__ import annotations

import json
import re
import sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
RUN_DIR = HERE.parent
ROOT = RUN_DIR.parents[1]
sys.path.insert(0, str(RUN_DIR))
sys.path.insert(0, str(ROOT / "data" / "external" / "malrulelib_repo"))

from utils import DifficultyLevel, Problem  # noqa: E402

CATEGORIES = ["subtraction", "fractions", "decimals", "negative_numbers", "order_of_operations", "percentages"]

# Each tuple is (category, malrule local, problem text, manually reviewed expected answer)
MANUAL_EXPECTED_BUGS = [
    ("subtraction", "always_borrow_left", "Calculate: 864 - 321", "433"),
    ("subtraction", "borrow_from_bottom", "Calculate: 532 - 178", "574"),
    ("subtraction", "borrow_no_decrement", "Calculate: 532 - 178", "464"),
    ("subtraction", "diff_0_n_equals_n", "Calculate: 506 - 278", "278"),
    ("subtraction", "smaller_from_larger", "Calculate: 532 - 178", "446"),
    ("subtraction", "stops_borrow_at_zero", "Calculate: 703 - 258", "455"),
    ("fractions", "add_numerators_denominators", "Calculate: 3/4 + 5/6", "4/5"),
    ("fractions", "ignore_denominators", "Calculate: 3/4 + 5/6", "8"),
    ("fractions", "subtract_across", "Calculate: 7/8 - 2/5", "5/3"),
    ("fractions", "keep_common_denominator_for_multiplication", "Calculate: 2/5 * 3/5", "6/5"),
    ("fractions", "multiply_across_for_division", "Calculate: 2/3 / 4/5", "8/15"),
    ("fractions", "denominator_comparison_error", "Which fraction is largest: 7/10, 5/12, 3/4?", "5/12"),
    ("fractions", "natural_number_bias_numerator_only", "Which fraction is largest: 7/10, 5/12, 3/4?", "7/10"),
    ("decimals", "ignore_decimal_point", "Calculate: 2.4 * 1.5", "360"),
    ("decimals", "ignore_decimal_point", "Calculate: 7.2 / 1.5", "4"),
    ("decimals", "right_align_decimals", "Calculate: 12.3 + 4.56", "57.9"),
    ("decimals", "right_align_decimals", "Calculate: 20.4 - 3.75", "17.1"),
    ("decimals", "longer_is_larger", "Which is larger: 0.45 or 0.8?", "0.45"),
    ("decimals", "shorter_is_larger", "Which is larger: 0.3 or 0.496?", "0.3"),
    ("negative_numbers", "multiplication_rule_for_addition", "Calculate: -3 + (-5)", "8"),
    ("negative_numbers", "two_negatives_always_positive", "Calculate: -5 - (-8)", "13"),
    ("negative_numbers", "larger_absolute_value_always_wins", "Calculate: -5 - (-8)", "-3"),
    ("negative_numbers", "negative_swaps_operation", "Calculate: -5 - (-8)", "-13"),
    ("negative_numbers", "negative_times_negative_negative", "Calculate: (-3) * (-4)", "-12"),
    ("negative_numbers", "negative_times_negative_negative", "Calculate: (-12) / (-4)", "-3"),
    ("order_of_operations", "addition_before_subtraction_always", "Calculate: 10 - 3 + 2", "5"),
    ("order_of_operations", "multiplication_before_division_always", "Calculate: 8 / 4 * 2", "1"),
    ("order_of_operations", "ignore_parentheses", "Calculate: 2 * (3 + 4)", "10"),
    ("order_of_operations", "strict_left_to_right", "Calculate: 2 + 3 * 4", "20"),
    ("percentages", "percent_equals_decimal", "What is 20% of 70?", "1400"),
    ("percentages", "percentage_as_index", "What is 20% of 70?", "20"),
    ("percentages", "reverse_percentage_error", "If 40 is 80% of 50, what percent is 50 of 40?", "80"),
    ("percentages", "add_percentages_directly", "200 is increased by 20% and then decreased by 10%. What is the final value?", "220"),
]


def canon(value) -> str:
    if isinstance(value, Fraction):
        return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    if isinstance(value, Decimal):
        return format(value.normalize(), "f")
    s = str(value).strip().replace("$", "").replace(",", "").rstrip(".")
    if re.fullmatch(r"-?\d+/\d+", s):
        return canon(Fraction(s))
    if re.fullmatch(r"-?\d+(?:\.\d+)?", s):
        d = Decimal(s)
        if abs(d - d.to_integral()) <= Decimal("1e-9"):
            return str(int(d.to_integral_value()))
        return format(d.normalize(), "f")
    return s


def sympy_value(expr: str) -> str:
    v = sp.sympify(expr, rational=True)
    if v.free_symbols:
        raise ValueError(expr)
    f = sp.nsimplify(v)
    if isinstance(f, sp.Integer):
        return str(int(f))
    if isinstance(f, sp.Rational):
        return canon(Fraction(int(f.p), int(f.q)))
    return canon(Decimal(str(float(f))))


def correct_answer(item: dict) -> str:
    cat, meta, operation = item["category"], item["meta"], item["operation"]
    if cat == "subtraction":
        return sympy_value(f"{meta['a']}-{meta['b']}")
    if cat == "fractions":
        pairs = meta.get("operands") or []
        if operation in ("addition", "fraction_addition"):
            a, b = pairs[0]; c, d = pairs[1]
            return canon(Fraction(a, b) + Fraction(c, d))
        if operation in ("subtraction", "fraction_subtraction"):
            a, b = pairs[0]; c, d = pairs[1]
            return canon(Fraction(a, b) - Fraction(c, d))
        if operation in ("multiplication", "fraction_multiplication"):
            a, b = pairs[0]; c, d = pairs[1]
            return canon(Fraction(a, b) * Fraction(c, d))
        if operation in ("division", "fraction_division"):
            a, b = pairs[0]; c, d = pairs[1]
            return canon(Fraction(a, b) / Fraction(c, d))
        if operation == "fraction_comparison":
            vals = [Fraction(n, d) for n, d in pairs]
            best = pairs[max(range(len(vals)), key=lambda i: vals[i])]
            return canon(Fraction(best[0], best[1]))
    if cat == "decimals":
        x, y = Decimal(meta.get("num1", meta.get("decimal1"))), Decimal(meta.get("num2", meta.get("decimal2")))
        if operation == "multiplication":
            return canon(x * y)
        if operation == "division":
            return canon((x / y).normalize())
        if operation == "addition":
            return canon(x + y)
        if operation == "subtraction":
            return canon(x - y)
        if operation in ("decimal_comparison", "comparison"):
            return canon(max(x, y))
    if cat == "negative_numbers":
        return sympy_value(re.sub(r"\s+", "", item["text"].replace("Calculate: ", "").replace("(-", "(-")))
    if cat == "order_of_operations":
        expr = meta["expression"].replace("(", "(").replace(")", ")")
        return sympy_value(expr)
    if cat == "percentages":
        op = item["operation"]
        if op == "percentage":
            # distinguish "x% of y" from change problems by text
            m = re.search(r"What is (\d+)% of (\d+)", item["text"])
            if m:
                return canon(Fraction(int(m.group(1)), 100) * int(m.group(2)))
            p = int(meta["percent"]); total = int(meta["value"])
            direction = 1 if "increased" in item["text"] else -1
            return canon(Fraction(total) * (100 + direction * p) / 100)
        if op == "percentage_relationship":
            m = re.search(r"If (\d+) is (\d+)% of (\d+)", item["text"])
            part, p, total = map(int, m.groups())
            return canon(Fraction(100 * total, part))
        if op == "percentage_sequential":
            init = int(meta["initial_value"]); p1 = int(meta["percentage1"]); p2 = int(meta["percentage2"])
            return canon(Fraction(init) * (100 + p1) / 100 * (100 - p2) / 100)
    raise ValueError((cat, operation, item["text"]))


def malrule_classes():
    import importlib
    import inspect
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
    text = item["text"]
    operation = item["operation"]
    level = 5
    if item["category"] == "subtraction":
        operands = [meta["a"], meta["b"]]
    elif item["category"] == "fractions":
        pairs = meta["operands"]
        if local == "ignore_denominators":
            operands = [n for pair in pairs for n in pair]
        elif local in ("denominator_comparison_error", "natural_number_bias_numerator_only"):
            operands = pairs
        else:
            operands = pairs
    else:
        operands = meta.get("operands", [])
        if item["category"] == "decimals":
            operands = [Decimal(str(x)) for x in operands]
        if not operands and "a" in meta and "b" in meta:
            operands = [meta["a"], meta["b"]]
        if not operands and "values" in meta:
            operands = meta["values"]
    metadata = dict(meta)
    metadata.setdefault("template", meta.get("template"))
    metadata.setdefault("operation", operation)
    if item["category"] == "order_of_operations":
        # library implementations test for × and ÷, while our authored specs use ASCII
        metadata["operations"] = metadata.get("operations_symbols", metadata.get("operations", []))
        metadata["op1"] = {"*": "×", "/": "÷"}.get(metadata.get("op1"), metadata.get("op1"))
        metadata["op2"] = {"*": "×", "/": "÷"}.get(metadata.get("op2"), metadata.get("op2"))
    return Problem(text=text, operands=operands, operation=operation, level=level,
                   difficulty=DifficultyLevel.MEDIUM, metadata=metadata)


def main() -> None:
    items = []
    for cat in CATEGORIES:
        bank = json.loads((HERE / "data" / f"bank_v5_{cat}.json").read_text(encoding="utf-8"))
        for idx, item in enumerate(bank["items"]):
            item["_global_idx"] = (cat, idx)
            items.append(item)
    cases = json.loads((HERE / "data" / "cases_test_v5.json").read_text(encoding="utf-8"))

    correct_mismatches = []
    for item in items:
        try:
            expected = correct_answer(item)
        except Exception as exc:
            correct_mismatches.append({"type": "correct_unverifiable", "item": item["text"], "error": repr(exc)})
            continue
        if canon(item["correct"]) != expected:
            correct_mismatches.append({"type": "correct_mismatch", "item": item["text"],
                                      "stored": item["correct"], "independent": expected})

    classes = malrule_classes()
    lib_checks = []
    manual_map = {(cat, local, text): canon(ans) for cat, local, text, ans in MANUAL_EXPECTED_BUGS}

    def manual_expected(item, local):
        explicit = manual_map.get((item["category"], local, item["text"]))
        if explicit is not None:
            return canon(explicit)
        meta = item["meta"]
        if local == "keep_common_denominator_for_multiplication":
            (a, b), (c, _d) = meta["operands"]
            return canon(Fraction(a * c, b))
        if local == "denominator_comparison_error":
            pairs = meta.get("operands", [])
            return canon(Fraction(*(max(pairs, key=lambda x: x[1]))))
        if local == "natural_number_bias_numerator_only":
            pairs = meta.get("operands", [])
            return canon(Fraction(*(max(pairs, key=lambda x: x[0]))))
        return None

    audit_reimplemented = set()
    for item in items:
        for hid, pred in item["predictions"].items():
            if pred == item["correct"]:
                continue
            local = hid.split(".", 1)[1]
            manual = manual_expected(item, local)
            if manual is not None and manual != canon(pred):
                lib_checks.append({"type": "manual_mismatch", "item": item["text"], "hid": hid,
                                  "stored": pred, "manual": manual})
            inst = classes.get(hid)
            if manual is not None and (inst is None or local in {"keep_common_denominator_for_multiplication", "denominator_comparison_error", "natural_number_bias_numerator_only"}):
                audit_reimplemented.add(hid)
            if inst is None:
                lib_checks.append({"type": "library_unavailable", "item": item["text"], "hid": hid})
                continue
            try:
                lib = canon(inst.calculate_expected_answer(problem_for(item, local)))
            except Exception as exc:
                etype = "library_unsupported" if isinstance(exc, (KeyError, TypeError, ValueError)) else "library_error"
                lib_checks.append({"type": etype, "item": item["text"], "hid": hid, "error": repr(exc)})
                continue
            if lib != canon(pred):
                lib_checks.append({"type": "library_mismatch", "item": item["text"], "hid": hid,
                                  "stored": pred, "library": lib})

    # case answer must equal prediction for true label
    case_errors = []
    for case in cases:
        bank = json.loads((HERE / "data" / f"bank_v5_{case['category']}.json").read_text(encoding="utf-8"))
        item = bank["items"][case["item_idx"]]
        if item["predictions"].get(case["true_id"]) != case["answer"]:
            case_errors.append(case)
        if case["answer"] == case["correct"]:
            case_errors.append(case)

    manual_by_key = {(c, l, t): a for c, l, t, a in MANUAL_EXPECTED_BUGS}
    manual_hits = sum(1 for item in items for hid, pred in item["predictions"].items()
                      if pred != item["correct"] and manual_by_key.get((item["category"], hid.split('.', 1)[1], item["text"])) == canon(pred))

    true_failures = []
    for case in cases:
        bank = json.loads((HERE / "data" / f"bank_v5_{case['category']}.json").read_text(encoding="utf-8"))
        item = bank["items"][case["item_idx"]]
        local = case["true_id"].split(".", 1)[1]
        manual = manual_expected(item, local)
        lib_status = next((x for x in lib_checks if x.get("item") == item["text"] and x.get("hid") == case["true_id"]), None)
        library_ok = lib_status is None and item["predictions"][case["true_id"]] != item["correct"]
        audit_ok = manual == canon(item["predictions"][case["true_id"]])
        if not (library_ok or audit_ok):
            true_failures.append({"case": case["case_id"], "hid": case["true_id"], "text": item["text"],
                                  "stored": case["answer"], "manual": manual, "library_status": lib_status, "manual": manual})
    statuses = {}
    for x in lib_checks:
        statuses[x["type"]] = statuses.get(x["type"], 0) + 1
    report = {
        "n_items": len(items),
        "n_cases": len(cases),
        "correct_audit": {
            "n_mismatches_or_unverifiable": len(correct_mismatches),
            "items": correct_mismatches[:20],
        },
        "error_audit": {
            "n_manual_expected_reviewed": len(MANUAL_EXPECTED_BUGS),
            "n_manual_matches_among_trigger_predictions": manual_hits,
            "n_audit_reimplemented_rules": len(audit_reimplemented),
            "audit_reimplemented_rules": sorted(audit_reimplemented),
            "statuses": statuses,
            "issues": lib_checks[:40],
        },
        "case_audit": {"n_errors": len(case_errors), "examples": case_errors[:10]},
        "true_label_audit": {"n_failures": len(true_failures), "failures": true_failures[:30]},
    }
    (HERE / "out" / "v5_data_audit.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("n_items", "n_cases")}, indent=2))
    print("correct issues", len(correct_mismatches), "error issues", len(lib_checks), "case errors", len(case_errors), "true-label failures", len(true_failures))
    for x in (correct_mismatches + lib_checks + case_errors + true_failures)[:15]:
        print(x)


if __name__ == "__main__":
    main()
