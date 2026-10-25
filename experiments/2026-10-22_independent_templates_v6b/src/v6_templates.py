"""Authored independent structural templates (v6) for all six categories.

Second authored template set, built after the v5 analysis. It targets the same
30 reliable true labels as v5 but uses new structural families; no item text or
family name is shared with the v5 test/dev sets. Misconception predictions are
computed by small independent functions below and are audited in
audit_v6_data.py against MalRuleLib where the library supports the structure.

Schema matches v5_templates: text, category, family, split, operation, correct,
predictions, applicable, triggers, answers, meta, audit_expr.
"""
from __future__ import annotations

import json
import re
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
CATEGORIES = ["subtraction", "fractions", "decimals", "negative_numbers", "order_of_operations", "percentages"]
CATEGORY_HIDS: dict[str, list[str]] = json.loads((DATA / "hypotheses_v4.json").read_text(encoding="utf-8"))


def canon(value) -> str:
    if isinstance(value, Fraction):
        return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    s = str(value).strip().replace("$", "").replace(",", "")
    if re.fullmatch(r"-?\d+/\d+", s):
        f = Fraction(s)
        return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"
    if re.fullmatch(r"-?\d+(?:\.\d+)?", s):
        d = Decimal(s)
        if d == d.to_integral():
            return str(int(d))
        return format(d.normalize(), "f")
    return s


def _item(category: str, family: str, text: str, correct, bugs: dict[str, object],
          operation: str, meta: dict, audit_expr: str) -> dict:
    preds, applicable = {}, {}
    for hid in CATEGORY_HIDS[category]:
        local = hid.split(".", 1)[1]
        if local in bugs:
            preds[hid] = canon(bugs[local])
            applicable[hid] = True
        else:
            preds[hid] = canon(correct)
            applicable[hid] = False
    correct_c = canon(correct)
    return {
        "text": text,
        "category": category,
        "family": family,
        "split": "test",
        "operation": operation,
        "correct": correct_c,
        "predictions": preds,
        "applicable": applicable,
        "triggers": {hid: applicable[hid] and preds[hid] != correct_c for hid in applicable},
        "answers": sorted(set([correct_c] + list(preds.values()))),
        "meta": {**meta, "audit_kind": family},
        "audit_expr": audit_expr,
    }


# ------------------------------------------------------------------ subtraction
def _digits(n: int, width: int | None = None) -> list[int]:
    s = str(n) if width is None else str(n).zfill(width)
    return [int(c) for c in s]


def _from_digits(ds: list[int]) -> str:
    return str(int("".join(str(d) for d in ds)))


def bad_always_borrow_left(a: int, b: int) -> str:
    m = _digits(a)
    s = _digits(b, len(m))
    out = [0] * len(m)
    for i in range(len(m) - 1, 0, -1):
        top = m[i] + 10
        m[i - 1] -= 1
        out[i] = (top - s[i]) % 10
    out[0] = max(0, m[0] - s[0])
    return _from_digits(out)


def bad_borrow_from_bottom(a: int, b: int) -> str:
    m = _digits(a)
    s = _digits(b, len(m))
    out = [0] * len(m)
    for i in range(len(m) - 1, -1, -1):
        top, bot = m[i], s[i]
        if top < bot:
            j = i - 1
            zeros = []
            while j >= 0 and s[j] == 0:
                zeros.append(j)
                j -= 1
            if j >= 0:
                for k in zeros:
                    s[k] = 9
                s[j] -= 1
                top += 10
                out[i] = top - bot
            else:
                out[i] = bot - top
        else:
            out[i] = top - bot
    return _from_digits(out)


def bad_borrow_no_decrement(a: int, b: int) -> str:
    m = _digits(a)
    s = _digits(b, len(m))
    out = [0] * len(m)
    for i in range(len(m) - 1, -1, -1):
        out[i] = m[i] + 10 - s[i] if m[i] < s[i] else m[i] - s[i]
    return _from_digits(out)


def bad_diff_0_n_equals_n(a: int, b: int) -> str:
    original = _digits(a)
    work = original[:]
    s = _digits(b, len(work))
    out = [0] * len(work)
    for i in range(len(work) - 1, -1, -1):
        if original[i] == 0 and s[i] > 0:
            out[i] = s[i]
            continue
        if work[i] < s[i]:
            j = i - 1
            while j >= 0 and work[j] == 0:
                work[j] = 9
                j -= 1
            if j >= 0:
                work[j] -= 1
                work[i] += 10
                out[i] = work[i] - s[i]
            else:
                out[i] = abs(work[i] - s[i])
        else:
            out[i] = work[i] - s[i]
    return _from_digits(out)


def bad_smaller_from_larger(a: int, b: int) -> str:
    m = _digits(a)
    s = _digits(b, len(m))
    return _from_digits([abs(x - y) for x, y in zip(m, s)])


def bad_stops_borrow_at_zero(a: int, b: int) -> str:
    m = _digits(a)
    s = _digits(b, len(m))
    work = m[:]
    out = [0] * len(work)
    for i in range(len(work) - 1, -1, -1):
        top, bot = work[i], s[i]
        if top < bot:
            if i > 0 and work[i - 1] == 0:
                out[i] = abs(top - bot)
            elif i > 0:
                work[i - 1] -= 1
                out[i] = top + 10 - bot
            else:
                out[i] = abs(top - bot)
        else:
            out[i] = top - bot
    return _from_digits(out)


def sub_item(a: int, b: int, family: str) -> dict:
    correct = a - b
    bugs = {
        "always_borrow_left": bad_always_borrow_left(a, b),
        "borrow_from_bottom": bad_borrow_from_bottom(a, b),
        "borrow_no_decrement": bad_borrow_no_decrement(a, b),
        "diff_0_n_equals_n": bad_diff_0_n_equals_n(a, b),
        "smaller_from_larger": bad_smaller_from_larger(a, b),
        "stops_borrow_at_zero": bad_stops_borrow_at_zero(a, b),
    }
    bugs = {k: v for k, v in bugs.items() if canon(v) != canon(correct)}
    return _item("subtraction", family, f"Calculate: {a} - {b}", correct, bugs, "subtraction",
                 {"template": family, "a": a, "b": b}, f"{a}-{b}")


SUB_SPECS = [
    (4006, 1378, "sub4_zero_bridge"),
    (7004, 3526, "sub4_zero_bridge"),
    (5060, 2749, "sub4_zero_bridge"),
    (6312, 2547, "sub4_chain"),
    (7241, 3856, "sub4_chain"),
    (8453, 2674, "sub4_chain"),
    (30450, 12763, "sub5_zero_ones"),
    (52180, 26394, "sub5_zero_ones"),
    (74020, 38571, "sub5_zero_ones"),
    (800, 476, "sub3_zero_tail"),
    (600, 283, "sub3_zero_tail"),
    (900, 547, "sub3_zero_tail"),
    (9876, 5432, "sub4_no_borrow"),
    (8642, 5311, "sub4_no_borrow"),
    (7695, 2471, "sub4_no_borrow"),
    (4527, 1384, "sub4_ones_borrow"),
    (7632, 2478, "sub4_ones_borrow"),
    (5824, 3671, "sub4_ones_borrow"),
]


# ------------------------------------------------------------------ fractions
def frac(n, d) -> Fraction:
    return Fraction(n, d)


def frac_add3_item(pairs, family: str) -> dict:
    (a, b), (c, d), (e, f) = pairs
    correct = frac(a, b) + frac(c, d) + frac(e, f)
    bugs = {
        "add_numerators_denominators": Fraction(a + c + e, b + d + f),
        "ignore_denominators": Fraction(a + c + e, 1),
    }
    bugs = {k: v for k, v in bugs.items() if canon(v) != canon(correct)}
    text = f"Calculate: {a}/{b} + {c}/{d} + {e}/{f}"
    return _item("fractions", family, text, correct, bugs, "fraction_addition",
                 {"template": family, "operands": pairs, "operation": "addition"}, text.replace("Calculate: ", ""))


def frac_sub_improper_item(a, b, c, d, family: str) -> dict:
    correct = frac(a, b) - frac(c, d)
    bugs = {
        "subtract_across": Fraction(a - c, b - d) if b != d else None,
        "ignore_denominators": Fraction(a - c, 1),
    }
    bugs = {k: v for k, v in bugs.items() if v is not None and canon(v) != canon(correct)}
    text = f"Calculate: {a}/{b} - {c}/{d}"
    return _item("fractions", family, text, correct, bugs, "fraction_subtraction",
                 {"template": family, "operands": [(a, b), (c, d)], "operation": "subtraction"},
                 text.replace("Calculate: ", ""))


def frac_mul3_item(pairs, family: str) -> dict:
    (a, b), (c, d), (e, f) = pairs
    if not (b == d == f):
        raise ValueError("keep_common_denominator_for_multiplication requires like denominators")
    correct = frac(a, b) * frac(c, d) * frac(e, f)
    malrule = Fraction(a * c * e, b)
    bugs = {
        "keep_common_denominator_for_multiplication": malrule,
        "ignore_denominators": Fraction(a * c * e, 1),
    }
    bugs = {k: v for k, v in bugs.items() if canon(v) != canon(correct)}
    text = f"Calculate: {a}/{b} * {c}/{b} * {e}/{b}"
    return _item("fractions", family, text, correct, bugs, "fraction_multiplication",
                 {"template": "three_fractions", "v6_template_family": family,
                  "operands": pairs, "operation": "multiplication",
                  "numerator1": a, "numerator2": c, "numerator3": e,
                  "denominator": b,
                  "correct_numerator": correct.numerator,
                  "correct_denominator": correct.denominator,
                  "correct_answer": canon(correct),
                  "malrule_numerator": malrule.numerator,
                  "malrule_denominator": malrule.denominator,
                  "malrule_answer": canon(malrule)},
                 text.replace("Calculate: ", ""))


def frac_div_whole_item(a, b, c, family: str) -> dict:
    correct = frac(a, b) / c
    bugs = {
        "multiply_across_for_division": Fraction(a * c, b),
        "ignore_denominators": Fraction(a // c, 1),
    }
    bugs = {k: v for k, v in bugs.items() if canon(v) != canon(correct)}
    text = f"Calculate: {a}/{b} / {c}"
    return _item("fractions", family, text, correct, bugs, "fraction_division",
                 {"template": family, "operands": [(a, b), (c, 1)], "whole": c, "operation": "division",
                  "a": a, "b": b, "c": c, "d": 1},
                 text.replace("Calculate: ", ""))


def frac_whole_div_item(c, a, b, family: str) -> dict:
    correct = Fraction(c, 1) / frac(a, b)
    bugs = {
        "multiply_across_for_division": Fraction(c * a, b),
        "ignore_denominators": Fraction(c // a, 1),
    }
    bugs = {k: v for k, v in bugs.items() if canon(v) != canon(correct)}
    text = f"Calculate: {c} / ({a}/{b})"
    return _item("fractions", family, text, correct, bugs, "fraction_division",
                 {"template": family, "operands": [(c, 1), (a, b)], "whole": c, "operation": "division",
                  "a": c, "b": 1, "c": a, "d": b},
                 text.replace("Calculate: ", ""))


def frac_compare4_item(pairs, family: str) -> dict:
    values = [frac(n, d) for n, d in pairs]
    best = pairs[max(range(len(values)), key=lambda i: values[i])]
    correct = f"{best[0]}/{best[1]}"
    den_bug = max(pairs, key=lambda p: p[1])
    num_bug = max(pairs, key=lambda p: p[0])
    bugs = {
        "denominator_comparison_error": f"{den_bug[0]}/{den_bug[1]}",
        "natural_number_bias_numerator_only": f"{num_bug[0]}/{num_bug[1]}",
    }
    bugs = {k: v for k, v in bugs.items() if canon(v) != canon(correct)}
    text = "Which fraction is largest: " + ", ".join(f"{n}/{d}" for n, d in pairs) + "?"
    return _item("fractions", family, text, correct, bugs, "fraction_comparison",
                 {"template": family, "operands": pairs}, text.replace("Which fraction is largest: ", "").rstrip("?"))


FRAC3_ADD = [
    (1, 2, 1, 3, 1, 4),
    (2, 3, 1, 4, 1, 6),
    (3, 5, 1, 2, 2, 3),
]
FRAC_SUB = [(7, 4, 5, 6), (9, 5, 2, 3), (8, 3, 5, 4)]
FRAC3_MUL = [
    (2, 5, 3, 5, 4, 5),
    (3, 7, 5, 7, 2, 7),
    (1, 3, 2, 3, 2, 3),
]
FRAC_DIV_WHOLE = [(3, 4, 3), (2, 5, 4), (5, 6, 2)]
FRAC_WHOLE_DIV = [(3, 2, 5), (4, 3, 7), (2, 5, 6)]
FRAC_COMPARE4 = [
    [(7, 10), (2, 15), (3, 4), (5, 9)],
    [(9, 11), (3, 13), (4, 5), (6, 7)],
    [(5, 6), (9, 11), (8, 13), (3, 4)],
]


# ------------------------------------------------------------------ decimals
def _dec_places(s: str) -> int:
    return len(s.split(".")[1]) if "." in s else 0


def bad_ignore_decimal_point(x: str, y: str, op: str) -> str:
    xi = int(str(x).replace(".", ""))
    yi = int(str(y).replace(".", ""))
    if op == "multiplication":
        return str(xi * yi)
    if op == "division":
        return str(xi // yi) if yi else str(xi)
    if op == "addition":
        return str(xi + yi)
    return str(xi - yi)


def bad_right_align(x: str, y: str, op: str) -> str:
    xi = str(x).replace(".", "")
    yi = str(y).replace(".", "")
    width = max(len(xi), len(yi))
    xi, yi = xi.zfill(width), yi.zfill(width)
    val = int(xi) + int(yi) if op == "addition" else abs(int(xi) - int(yi))
    places = min(_dec_places(x), _dec_places(y))
    s = str(val)
    if places > 0 and len(s) > places:
        s = s[:-places] + "." + s[-places:]
    return s


def dec_mul_item(x: str, y: str, family: str) -> dict:
    correct = Decimal(x) * Decimal(y)
    bugs = {"ignore_decimal_point": bad_ignore_decimal_point(x, y, "multiplication")}
    bugs = {k: v for k, v in bugs.items() if canon(v) != canon(correct)}
    return _item("decimals", family, f"Calculate: {x} * {y}", correct, bugs, "multiplication",
                 {"template": "basic_multiplication", "v6_template_family": family,
                  "operands": [x, y], "num1": x, "num2": y, "operation": "multiplication",
                  "operation_symbol": "*"}, f"{x}*{y}")


def dec_div_item(x: str, y: str, family: str) -> dict:
    correct = Decimal(x) / Decimal(y)
    bugs = {"ignore_decimal_point": bad_ignore_decimal_point(x, y, "division")}
    bugs = {k: v for k, v in bugs.items() if canon(v) != canon(correct)}
    return _item("decimals", family, f"Calculate: {x} / {y}", correct, bugs, "division",
                 {"template": "division", "v6_template_family": family,
                  "operands": [x, y], "num1": x, "num2": y, "operation": "division",
                  "operation_symbol": "/", "num1_decimal_places": _dec_places(x),
                  "num2_decimal_places": _dec_places(y)}, f"{x}/{y}")


def dec_add_item(x: str, y: str, op: str, family: str) -> dict:
    correct = Decimal(x) + Decimal(y) if op == "addition" else Decimal(x) - Decimal(y)
    bugs = {"right_align_decimals": bad_right_align(x, y, op)}
    bugs = {k: v for k, v in bugs.items() if canon(v) != canon(correct)}
    return _item("decimals", family, f"Calculate: {x} {'+' if op == 'addition' else '-'} {y}",
                 correct, bugs, op,
                 {"template": "basic_addition" if op == "addition" else "basic_subtraction",
                  "v6_template_family": family, "operands": [x, y], "num1": x, "num2": y,
                  "operation": op, "operation_symbol": "+" if op == "addition" else "-",
                  "num1_decimal_places": _dec_places(x), "num2_decimal_places": _dec_places(y)},
                 f"{x}{'+' if op == 'addition' else '-'}{y}")


def dec_compare3_item(items, family: str) -> dict:
    vals = [Decimal(x) for x in items]
    correct = items[max(range(len(vals)), key=lambda i: vals[i])]
    longer = max(items, key=lambda s: _dec_places(s))
    shorter = min(items, key=lambda s: _dec_places(s))
    bugs = {"longer_is_larger": longer, "shorter_is_larger": shorter}
    bugs = {k: v for k, v in bugs.items() if canon(v) != canon(correct)}
    text = "Which is largest: " + ", ".join(items[:-1]) + f", or {items[-1]}?"
    return _item("decimals", family, text, correct, bugs, "decimal_comparison",
                 {"template": "basic_comparison", "v6_template_family": family,
                  "operands": items, "decimals": items}, "max(" + ",".join(items) + ")")


DEC_MUL = [("0.35", "0.4"), ("0.28", "1.5"), ("1.75", "0.6")]
DEC_DIV = [("0.36", "0.4"), ("0.72", "0.9"), ("0.144", "0.12")]
DEC_ADD = [("0.125", "2.4"), ("3.06", "1.875"), ("0.75", "12.125")]
DEC_SUB = [("5", "0.75"), ("12", "4.6"), ("8", "2.125")]
DEC_CMP3 = [
    ("0.46", "0.4", "0.375"),
    ("0.72", "0.7", "0.685"),
    ("0.34", "0.3", "0.285"),
]


# ------------------------------------------------------------------ negative numbers
def neg_item(expr: str, operands: list, correct, bugs: dict, meta: dict, family: str) -> dict:
    bugs = {k: v for k, v in bugs.items() if canon(v) != canon(correct)}
    meta = {**meta, "expression": expr, "operands": operands, "v6_template_family": family}
    return _item("negative_numbers", family, f"Calculate: {expr}", correct, bugs,
                 meta.get("operation", "arithmetic"), meta, expr)


def neg_add_two_item(a: int, b: int, family: str) -> dict:
    correct = -a - b
    bugs = {
        "multiplication_rule_for_addition": a + b,
        "two_negatives_always_positive": a + b,
    }
    return neg_item(f"-{a} + (-{b})", [-a, -b], correct, bugs,
                    {"operation": "negative_addition", "problem_type": "neg_plus_neg", "operator": "+",
                     "operation_type": "add_negative", "template": family, "a": -a, "b": -b}, family)


def neg_sub_pos_item(a: int, b: int, family: str) -> dict:
    correct = -a - b
    bugs = {"larger_absolute_value_always_wins": abs(b - a)}
    return neg_item(f"-{a} - {b}", [-a, b], correct, bugs,
                    {"operation": "negative_subtraction", "problem_type": "neg_minus_pos", "operator": "-",
                     "operation_type": "subtract_positive", "template": family, "a": -a, "b": b}, family)


def neg_neg_minus_neg_item(a: int, b: int, family: str) -> dict:
    correct = b - a
    bugs = {
        "two_negatives_always_positive": a + b,
        "negative_swaps_operation": -a - b,
        "larger_absolute_value_always_wins": -(b - a),
    }
    return neg_item(f"-{a} - (-{b})", [-a, -b], correct, bugs,
                    {"operation": "negative_subtraction", "problem_type": "neg_minus_neg", "operator": "-",
                     "operation_type": "subtract_negative", "pattern": "negative_minus_negative",
                     "template": family, "a": -a, "b": -b}, family)


def neg_multi_step_item(a: int, b: int, c: int, family: str) -> dict:
    correct = a * b * c
    bugs = {"negative_times_negative_negative": -a * b * c}
    return neg_item(f"(-{a}) * (-{b}) * {c}", [-a, -b, c], correct, bugs,
                    {"operation": "multiplication", "template": "multi_step_multiplication",
                     "a": -a, "b": -b, "c": c, "pattern": "both_negative"}, family)


def neg_mixed_item(a: int, b: int, c: int, family: str) -> dict:
    correct = a * b + c
    bugs = {"negative_times_negative_negative": -a * b + c}
    return neg_item(f"(-{a}) * (-{b}) + {c}", [-a, -b, c], correct, bugs,
                    {"operation": "mixed", "template": "mixed_operations",
                     "a": -a, "b": -b, "c": c, "pattern": "both_negative"}, family)


NEG_ADD = [(6, 4), (8, 5), (7, 3)]
NEG_SUB_POS = [(4, 6), (3, 7), (5, 9)]
NEG_NEG_SUB_NEG = [(6, 9), (4, 11), (8, 13)]
NEG_MULTI = [(2, 3, 4), (3, 5, 2), (4, 2, 3)]
NEG_MIXED = [(2, 3, 5), (4, 2, 7), (3, 5, 4)]


# ------------------------------------------------------------------ order of operations
def oo_item(text: str, values: list[int], ops: list[str], correct: int, bugs: dict,
            family: str, lib_template: str) -> dict:
    bugs = {k: v for k, v in bugs.items() if canon(v) != canon(correct)}
    expr = text.replace("Calculate: ", "")
    symbol_ops = {"*": "×", "/": "÷"}
    meta = {
        "template": lib_template,
        "v6_template_family": family,
        "values": values,
        "operations": ops,
        "operations_symbols": [symbol_ops.get(op, op) for op in ops],
        "expression": expr,
        "operands": values,
    }
    if len(values) == 3:
        meta.update({"a": values[0], "b": values[1], "c": values[2], "op1": ops[0], "op2": ops[1]})
    return _item("order_of_operations", family, text, correct, bugs, "order_of_operations", meta, expr)


def left_to_right(values: list[int], ops: list[str]) -> int:
    v = values[0]
    for i, op in enumerate(ops):
        x = values[i + 1]
        v = v + x if op == "+" else v - x if op == "-" else v * x if op == "*" else v // x
    return v


def addition_first(values: list[int], ops: list[str]) -> int:
    """Mirror MalRuleLib: merge the number before a '+' with the number after
    it, keeping the left number's operator; then subtract left-to-right."""
    arr = [(values[0], None)] + [(values[i + 1], ops[i]) for i in range(len(ops))]
    while True:
        idx = next((i for i, (_, op) in enumerate(arr) if op == "+"), None)
        if idx is None:
            break
        prev_num, prev_op = arr[idx - 1]
        cur_num, _ = arr[idx]
        arr[idx - 1] = (prev_num + cur_num, prev_op)
        arr.pop(idx)
    result = arr[0][0]
    for num, op in arr[1:]:
        result = result - num if op == "-" else result + num
    return result


OO = [
    ("Calculate: 84 / 7 * 3", [84, 7, 3], ["/", "*"], 36, {"multiplication_before_division_always": 84 // (7 * 3)}, "oo_muldiv_chain", "basic_mult_div"),
    ("Calculate: 72 / 6 * 4", [72, 6, 4], ["/", "*"], 48, {"multiplication_before_division_always": 72 // (6 * 4)}, "oo_muldiv_chain", "basic_mult_div"),
    ("Calculate: 96 / 8 * 2", [96, 8, 2], ["/", "*"], 24, {"multiplication_before_division_always": 96 // (8 * 2)}, "oo_muldiv_chain", "basic_mult_div"),
    ("Calculate: 48 / (2 * 4)", [48, 2, 4], ["/", "*"], 6, {"ignore_parentheses": left_to_right([48, 2, 4], ["/", "*"])}, "oo_div_paren_product", "basic_single_parentheses"),
    ("Calculate: 60 / (3 * 4)", [60, 3, 4], ["/", "*"], 5, {"ignore_parentheses": left_to_right([60, 3, 4], ["/", "*"])}, "oo_div_paren_product", "basic_single_parentheses"),
    ("Calculate: 96 / (4 * 6)", [96, 4, 6], ["/", "*"], 4, {"ignore_parentheses": left_to_right([96, 4, 6], ["/", "*"])}, "oo_div_paren_product", "basic_single_parentheses"),
    ("Calculate: 15 - 2 * (3 + 1)", [15, 2, 3, 1], ["-", "*", "+"], 7, {"ignore_parentheses": left_to_right([15, 2, 3, 1], ["-", "*", "+"])}, "oo_paren_sub_mul", "nested_parentheses"),
    ("Calculate: 20 - 3 * (2 + 3)", [20, 3, 2, 3], ["-", "*", "+"], 5, {"ignore_parentheses": left_to_right([20, 3, 2, 3], ["-", "*", "+"])}, "oo_paren_sub_mul", "nested_parentheses"),
    ("Calculate: 18 - 4 * (1 + 2)", [18, 4, 1, 2], ["-", "*", "+"], 6, {"ignore_parentheses": left_to_right([18, 4, 1, 2], ["-", "*", "+"])}, "oo_paren_sub_mul", "nested_parentheses"),
    ("Calculate: 40 - 12 + 7 - 5", [40, 12, 7, 5], ["-", "+", "-"], 30, {"addition_before_subtraction_always": addition_first([40, 12, 7, 5], ["-", "+", "-"])}, "oo_add_sub_four", "mixed_operations"),
    ("Calculate: 35 - 9 + 6 - 4", [35, 9, 6, 4], ["-", "+", "-"], 28, {"addition_before_subtraction_always": addition_first([35, 9, 6, 4], ["-", "+", "-"])}, "oo_add_sub_four", "mixed_operations"),
    ("Calculate: 50 - 18 + 9 - 7", [50, 18, 9, 7], ["-", "+", "-"], 34, {"addition_before_subtraction_always": addition_first([50, 18, 9, 7], ["-", "+", "-"])}, "oo_add_sub_four", "mixed_operations"),
    ("Calculate: 5 + 2 * 3 + 4", [5, 2, 3, 4], ["+", "*", "+"], 15, {"strict_left_to_right": left_to_right([5, 2, 3, 4], ["+", "*", "+"])}, "oo_mixed_four", "mixed_operations"),
    ("Calculate: 7 + 3 * 2 - 5", [7, 3, 2, 5], ["+", "*", "-"], 8, {"strict_left_to_right": left_to_right([7, 3, 2, 5], ["+", "*", "-"])}, "oo_mixed_four", "mixed_operations"),
    ("Calculate: 6 + 4 * 2 + 3", [6, 4, 2, 3], ["+", "*", "+"], 17, {"strict_left_to_right": left_to_right([6, 4, 2, 3], ["+", "*", "+"])}, "oo_mixed_four", "mixed_operations"),
]


# ------------------------------------------------------------------ percentages
def pct_over_hundred_item(p: int, total: int, family: str) -> dict:
    correct = Fraction(p, 100) * total
    bugs = {"percent_equals_decimal": p * total, "percentage_as_index": p}
    return _item("percentages", family, f"What is {p}% of {total}?", correct, bugs, "percentage",
                 {"template": family, "percent": p, "value": total, "percentage": p, "total": total,
                  "conversion_type": "percent_in_calculation"}, f"{p}/100*{total}")


def pct_find_whole_item(part: int, p: int, family: str) -> dict:
    correct = Fraction(part * 100, p)
    bugs = {"percent_equals_decimal": part * p, "percentage_as_index": p}
    return _item("percentages", family, f"{part} is {p}% of what number?", correct, bugs, "percentage_relationship",
                 {"template": family, "part": part, "percentage": p, "percent": p,
                  "formula_type": "find_total_from_percentage",
                  "conversion_type": "percent_in_calculation"}, f"{part}/({p}/100)")


def pct_two_increases_item(initial: int, p1: int, p2: int, family: str) -> dict:
    correct = Fraction(initial) * Fraction(100 + p1, 100) * Fraction(100 + p2, 100)
    bugs = {"add_percentages_directly": Fraction(initial) * Fraction(100 + p1 + p2, 100)}
    return _item("percentages", family,
                 f"{initial} is increased by {p1}% and then increased by {p2}%. What is the final value?",
                 correct, bugs, "percentage_sequential",
                 {"template": "sequential_percentage", "v6_template_family": family,
                  "initial_value": initial, "percentage1": p1, "percentage2": p2,
                  "problem_type": "two_increases"}, f"{initial}*(1+{p1}/100)*(1+{p2}/100)")


def pct_dec_then_inc_item(initial: int, p1: int, p2: int, family: str) -> dict:
    correct = Fraction(initial) * Fraction(100 - p1, 100) * Fraction(100 + p2, 100)
    bugs = {"add_percentages_directly": Fraction(initial) * Fraction(100 - p1 + p2, 100)}
    return _item("percentages", family,
                 f"{initial} is decreased by {p1}% and then increased by {p2}%. What is the final value?",
                 correct, bugs, "percentage_sequential",
                 {"template": "sequential_percentage", "v6_template_family": family,
                  "initial_value": initial, "percentage1": p1, "percentage2": p2,
                  "problem_type": "decrease_then_increase"}, f"{initial}*(1-{p1}/100)*(1+{p2}/100)")


def pct_compare_change_item(given: int, direction: str, correct, family: str) -> dict:
    bugs = {"reverse_percentage_error": given}
    if direction == "larger":
        text = f"A is {given}% larger than B. B is what percent smaller than A?"
    else:
        text = f"A is {given}% smaller than B. B is what percent larger than A?"
    return _item("percentages", family, text, correct, bugs, "percentage_relationship",
                 {"template": "comparison_statements", "v6_template_family": family,
                  "given_percent": given, "direction": direction,
                  "formula_type": "comparison_asymmetry"}, text)


PCT = [
    ("over", 120, 45), ("over", 150, 30), ("over", 125, 80),
    ("whole", 30, 20), ("whole", 45, 25), ("whole", 36, 40),
    ("two_inc", 80, 10, 25), ("two_inc", 100, 20, 25), ("two_inc", 60, 50, 20),
    ("dec_inc", 200, 20, 10), ("dec_inc", 150, 10, 20), ("dec_inc", 240, 25, 20),
]


def build_items() -> list[dict]:
    items = []
    for a, b, family in SUB_SPECS:
        items.append(sub_item(a, b, family))
    for spec in FRAC3_ADD:
        pairs = [(spec[0], spec[1]), (spec[2], spec[3]), (spec[4], spec[5])]
        items.append(frac_add3_item(pairs, "frac_add_three"))
    for a, b, c, d in FRAC_SUB:
        items.append(frac_sub_improper_item(a, b, c, d, "frac_sub_improper"))
    for spec in FRAC3_MUL:
        pairs = [(spec[0], spec[1]), (spec[2], spec[3]), (spec[4], spec[5])]
        items.append(frac_mul3_item(pairs, "frac_mul_three"))
    for a, b, c in FRAC_DIV_WHOLE:
        items.append(frac_div_whole_item(a, b, c, "frac_div_whole"))
    for c, a, b in FRAC_WHOLE_DIV:
        items.append(frac_whole_div_item(c, a, b, "frac_whole_div"))
    for pairs in FRAC_COMPARE4:
        items.append(frac_compare4_item(pairs, "frac_compare_four"))
    for x, y in DEC_MUL:
        items.append(dec_mul_item(x, y, "dec_mul_two_by_one"))
    for x, y in DEC_DIV:
        items.append(dec_div_item(x, y, "dec_div_dec"))
    for x, y in DEC_ADD:
        items.append(dec_add_item(x, y, "addition", "dec_add_3places"))
    for x, y in DEC_SUB:
        items.append(dec_add_item(x, y, "subtraction", "dec_sub_integer"))
    for triple in DEC_CMP3:
        items.append(dec_compare3_item(list(triple), "dec_compare_three"))
    for a, b in NEG_ADD:
        items.append(neg_add_two_item(a, b, "neg_add_two_new"))
    for a, b in NEG_SUB_POS:
        items.append(neg_sub_pos_item(a, b, "neg_sub_pos_new"))
    for a, b in NEG_NEG_SUB_NEG:
        items.append(neg_neg_minus_neg_item(a, b, "neg_minus_neg_new"))
    for a, b, c in NEG_MULTI:
        items.append(neg_multi_step_item(a, b, c, "neg_multi_step"))
    for a, b, c in NEG_MIXED:
        items.append(neg_mixed_item(a, b, c, "neg_mixed_ops"))
    for text, values, ops, correct, bugs, family, lib_template in OO:
        items.append(oo_item(text, values, ops, correct, bugs, family, lib_template))
    for spec in PCT:
        if spec[0] == "over":
            items.append(pct_over_hundred_item(spec[1], spec[2], "pct_over_hundred"))
        elif spec[0] == "whole":
            items.append(pct_find_whole_item(spec[1], spec[2], "pct_find_whole"))
        elif spec[0] == "two_inc":
            items.append(pct_two_increases_item(spec[1], spec[2], spec[3], "pct_two_increases"))
        elif spec[0] == "dec_inc":
            items.append(pct_dec_then_inc_item(spec[1], spec[2], spec[3], "pct_dec_then_inc"))
    # comparison-asymmetry family (reverse-percentage label), integers only
    items.append(pct_compare_change_item(25, "larger", 20, "pct_compare_change"))
    items.append(pct_compare_change_item(100, "larger", 50, "pct_compare_change"))
    items.append(pct_compare_change_item(20, "smaller", 25, "pct_compare_change"))
    return items


if __name__ == "__main__":
    from collections import Counter
    its = build_items()
    print("items", len(its))
    print(Counter(i["category"] for i in its))
    print(Counter(i["family"] for i in its))
