"""Authored structural templates for the v5 test.

These are deliberately NOT MalruleLib generators.  Each item is written as a
problem statement with explicit operands and an independent expected answer;
the malrule predictions are computed by small, independent functions below.
The audit script cross-checks the predictions against the MalruleLib malrule
implementations and the correct answers against a separate symbolic/rational
evaluator.

Split policy:
  * "test" families are frozen before looking at v5 outcomes;
  * "dev" families are structurally different and are used only for
    implementation sanity / threshold confirmation.
"""
from __future__ import annotations

import json
import re
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

RUN_DIR = Path(__file__).resolve().parents[1]
CATEGORIES = ["subtraction", "fractions", "decimals", "negative_numbers", "order_of_operations", "percentages"]
CATEGORY_HIDS: dict[str, list[str]] = {}


def _load_hids() -> None:
    for cat in CATEGORIES:
        path = RUN_DIR / f"bank_v4_{cat}.json"
        bank = json.loads(path.read_text(encoding="utf-8"))
        CATEGORY_HIDS[cat] = [h["id"] for h in bank["hypotheses"]]


_load_hids()


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


def _item(category: str, split: str, family: str, text: str, correct, bugs: dict[str, object],
          operation: str, meta: dict, audit_expr: str | None = None) -> dict:
    preds = {}
    applicable = {}
    for hid in CATEGORY_HIDS[category]:
        local = hid.split(".", 1)[1]
        if local in bugs:
            preds[hid] = canon(bugs[local])
            applicable[hid] = True
        else:
            preds[hid] = canon(correct)
            applicable[hid] = False
    answers = sorted(set([canon(correct)] + list(preds.values())))
    correct_c = canon(correct)
    return {
        "text": text,
        "category": category,
        "family": family,
        "split": split,
        "operation": operation,
        "correct": correct_c,
        "predictions": preds,
        "applicable": applicable,
        "triggers": {hid: applicable[hid] and preds[hid] != correct_c for hid in applicable},
        "answers": answers,
        "meta": meta,
        "audit_expr": audit_expr,
    }


# ------------------------------------------------------------------ subtraction
# Digit helpers use ordinary left-to-right digit order.
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
    """0 - N is written as N; all other columns use ordinary borrowing."""
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


def sub_item(a: int, b: int, split: str, family: str) -> dict:
    bugs = {
        "always_borrow_left": bad_always_borrow_left(a, b),
        "borrow_from_bottom": bad_borrow_from_bottom(a, b),
        "borrow_no_decrement": bad_borrow_no_decrement(a, b),
        "diff_0_n_equals_n": bad_diff_0_n_equals_n(a, b),
        "smaller_from_larger": bad_smaller_from_larger(a, b),
        "stops_borrow_at_zero": bad_stops_borrow_at_zero(a, b),
    }
    # keep only genuine triggers; the audit checks the rest
    bugs = {k: v for k, v in bugs.items() if canon(v) != canon(a - b)}
    return _item("subtraction", split, family, f"Calculate: {a} - {b}", a - b, bugs,
                 "subtraction", {"template": family, "a": a, "b": b}, f"{a}-{b}")


SUB_SPECS = [
    (532, 178, "test", "sub_chain_borrow"),
    (864, 321, "test", "sub_no_borrow"),
    (506, 278, "test", "sub_zero_cascade"),
    (452, 137, "test", "sub_borrow_from_bottom"),
    (730, 245, "test", "sub_zero_ones"),
    (703, 258, "test", "sub_zero_tens_stop"),
    (915, 267, "test", "sub_chain_borrow"),
    (947, 513, "test", "sub_no_borrow"),
    (604, 189, "test", "sub_zero_cascade"),
    (623, 148, "test", "sub_borrow_from_bottom"),
    (850, 376, "test", "sub_zero_ones"),
    (802, 367, "test", "sub_zero_tens_stop"),
    (74, 28, "dev", "sub_dev_two_digit"),
    (91, 47, "dev", "sub_dev_two_digit"),
    (305, 167, "dev", "sub_dev_zero"),
]


# ------------------------------------------------------------------ fractions
def frac(n: int, d: int) -> Fraction:
    return Fraction(n, d)


def bad_add_num_den(pairs):
    return Fraction(sum(n for n, _ in pairs), sum(d for _, d in pairs))


def bad_ignore_den(pairs, operation: str):
    nums = [n for n, _ in pairs]
    if operation == "addition":
        v = sum(nums)
    elif operation == "subtraction":
        v = nums[0] - nums[1]
    elif operation == "multiplication":
        v = nums[0] * nums[1]
    elif operation == "division":
        v = nums[0] // nums[1] if nums[1] else nums[0]
    else:
        v = sum(nums)
    return Fraction(v, 1)


def bad_keep_common_den_mult(pairs):
    (a, b), (c, _d) = pairs
    return Fraction(a * c, b)


def bad_mult_across_div(pairs):
    (a, b), (c, d) = pairs
    return Fraction(a * c, b * d)


def bad_subtract_across(pairs):
    (a, b), (c, d) = pairs
    if b - d == 0:
        return "undefined"
    return Fraction(a - c, b - d)


def _frac_item(split, family, text, pairs, correct: Fraction, bugs: dict, operation: str) -> dict:
    meta = {"template": family, "operation": operation, "operands": pairs}
    if len(pairs) >= 2:
        meta.update({
            "numer1": pairs[0][0], "denom1": pairs[0][1],
            "numer2": pairs[1][0], "denom2": pairs[1][1],
            "num1": pairs[0][0], "den1": pairs[0][1],
            "num2": pairs[1][0], "den2": pairs[1][1],
            "a": pairs[0][0], "b": pairs[0][1], "c": pairs[1][0], "d": pairs[1][1],
        })
    return _item("fractions", split, family, text, correct, bugs, operation, meta,
                 " ; ".join(f"{n}/{d}" for n, d in pairs))


def frac_add_item(a, b, c, d, split, family, op="addition") -> dict:
    pairs = [(a, b), (c, d)]
    correct = frac(a, b) + frac(c, d) if op == "addition" else frac(a, b) - frac(c, d)
    bugs = {"ignore_denominators": bad_ignore_den(pairs, op)}
    if op == "addition":
        bugs["add_numerators_denominators"] = bad_add_num_den(pairs)
        bugs["common_denominator_numerator"] = bad_add_num_den(pairs)
    if op == "subtraction" and b != d:
        bugs["subtract_across"] = bad_subtract_across(pairs)
    bugs = {k: v for k, v in bugs.items() if canon(v) != canon(correct)}
    return _frac_item(split, family, f"Calculate: {a}/{b} {'+' if op == 'addition' else '-'} {c}/{d}",
                      pairs, correct, bugs, op)


def frac_mul_item(a, b, c, d, split, family) -> dict:
    pairs = [(a, b), (c, d)]
    correct = frac(a, b) * frac(c, d)
    bugs = {
        "keep_common_denominator_for_multiplication": bad_keep_common_den_mult(pairs),
        "ignore_denominators": bad_ignore_den(pairs, "multiplication"),
    }
    bugs = {k: v for k, v in bugs.items() if canon(v) != canon(correct)}
    return _frac_item(split, family, f"Calculate: {a}/{b} * {c}/{d}", pairs, correct, bugs, "multiplication")


def frac_div_item(a, b, c, d, split, family) -> dict:
    pairs = [(a, b), (c, d)]
    correct = frac(a, b) / frac(c, d)
    bugs = {
        "multiply_across_for_division": bad_mult_across_div(pairs),
        "ignore_denominators": bad_ignore_den(pairs, "division"),
    }
    bugs = {k: v for k, v in bugs.items() if canon(v) != canon(correct)}
    return _frac_item(split, family, f"Calculate: {a}/{b} / {c}/{d}", pairs, correct, bugs, "division")


def frac_compare_item(fractions, split, family) -> dict:
    pairs = [(n, d) for n, d in fractions]
    values = [Fraction(n, d) for n, d in pairs]
    correct = pairs[values.index(max(values))]
    # denominator rule: largest denominator (three-fraction variant)
    den_bug = max(pairs, key=lambda p: p[1])
    num_bug = max(pairs, key=lambda p: p[0])
    bugs = {
        "denominator_comparison_error": f"{den_bug[0]}/{den_bug[1]}",
        "natural_number_bias_numerator_only": f"{num_bug[0]}/{num_bug[1]}",
    }
    bugs = {k: v for k, v in bugs.items() if canon(v) != canon(f"{correct[0]}/{correct[1]}")}
    return _item("fractions", split, family,
                 "Which fraction is largest: " + ", ".join(f"{n}/{d}" for n, d in pairs) + "?",
                 f"{correct[0]}/{correct[1]}", bugs, "fraction_comparison", {"template": family, "operands": pairs})


FRAC_SPECS = [
    ("add", 3, 4, 5, 6, "test", "frac_add_unlike"),
    ("add", 2, 3, 1, 5, "test", "frac_add_unlike"),
    ("add", 5, 8, 2, 3, "test", "frac_add_unlike"),
    ("sub", 5, 6, 3, 8, "test", "frac_sub_unlike"),
    ("sub", 7, 8, 2, 5, "test", "frac_sub_unlike"),
    ("sub", 9, 10, 3, 7, "test", "frac_sub_unlike"),
    ("mul", 2, 5, 3, 5, "test", "frac_mul_like"),
    ("mul", 3, 7, 4, 7, "test", "frac_mul_like"),
    ("mul", 4, 9, 5, 9, "test", "frac_mul_like"),
    ("div", 2, 3, 4, 5, "test", "frac_div_unlike"),
    ("div", 3, 4, 2, 5, "test", "frac_div_unlike"),
    ("div", 5, 7, 3, 8, "test", "frac_div_unlike"),
    ("add", 1, 2, 1, 6, "dev", "frac_dev_like_add"),
    ("sub", 3, 4, 1, 4, "dev", "frac_dev_like_sub"),
]


# ------------------------------------------------------------------ decimals

def dec(s: str) -> Decimal:
    return Decimal(s)


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


def _dec_places(s: str) -> int:
    return len(s.split(".")[1]) if "." in s else 0


def bad_right_align(x: str, y: str, op: str) -> str:
    xi = str(x).replace(".", "")
    yi = str(y).replace(".", "")
    width = max(len(xi), len(yi))
    xi = xi.zfill(width)
    yi = yi.zfill(width)
    val = int(xi) + int(yi) if op == "addition" else abs(int(xi) - int(yi))
    places = min(_dec_places(x), _dec_places(y))
    s = str(val)
    if places > 0 and len(s) > places:
        s = s[:-places] + "." + s[-places:]
    return s


def dec_mul_item(x: str, y: str, split: str, family: str) -> dict:
    correct = dec(x) * dec(y)
    bugs = {"ignore_decimal_point": bad_ignore_decimal_point(x, y, "multiplication")}
    bugs = {k: v for k, v in bugs.items() if canon(v) != canon(correct)}
    return _item("decimals", split, family, f"Calculate: {x} * {y}", correct, bugs, "multiplication",
                 {"template": "basic_multiplication", "v5_template_family": family, "operands": [x, y],
                  "num1": x, "num2": y, "operation": "multiplication", "operation_symbol": "*"}, f"{x}*{y}")


def dec_div_item(x: str, y: str, split: str, family: str) -> dict:
    correct = dec(x) / dec(y)
    bugs = {"ignore_decimal_point": bad_ignore_decimal_point(x, y, "division")}
    bugs = {k: v for k, v in bugs.items() if canon(v) != canon(correct)}
    return _item("decimals", split, family, f"Calculate: {x} / {y}", correct, bugs, "division",
                 {"template": "division", "v5_template_family": family, "operands": [x, y], "num1": x, "num2": y,
                  "operation": "division", "operation_symbol": "/", "num1_decimal_places": _dec_places(x),
                  "num2_decimal_places": _dec_places(y)}, f"{x}/{y}")


def dec_add_item(x: str, y: str, op: str, split: str, family: str) -> dict:
    correct = dec(x) + dec(y) if op == "addition" else dec(x) - dec(y)
    bugs = {"right_align_decimals": bad_right_align(x, y, op)}
    bugs = {k: v for k, v in bugs.items() if canon(v) != canon(correct)}
    return _item("decimals", split, family, f"Calculate: {x} {'+' if op == 'addition' else '-'} {y}", correct, bugs, op,
                 {"template": "basic_addition" if op == "addition" else "basic_subtraction", "v5_template_family": family,
                  "operands": [x, y], "num1": x, "num2": y, "operation": op,
                  "operation_symbol": "+" if op == "addition" else "-", "num1_decimal_places": _dec_places(x),
                  "num2_decimal_places": _dec_places(y)}, f"{x}{'+' if op == 'addition' else '-'}{y}")


def dec_compare_item(x: str, y: str, split: str, family: str) -> dict:
    correct = x if dec(x) > dec(y) else y
    longer = x if _dec_places(x) > _dec_places(y) else y
    shorter = x if _dec_places(x) < _dec_places(y) else y
    bugs = {"longer_is_larger": longer, "shorter_is_larger": shorter}
    bugs = {k: v for k, v in bugs.items() if canon(v) != canon(correct)}
    return _item("decimals", split, family, f"Which is larger: {x} or {y}?", correct, bugs, "decimal_comparison",
                 {"template": "basic_comparison", "v5_template_family": family, "operands": [x, y],
                  "decimal1": x, "decimal2": y, "num1": x, "num2": y}, f"max({x},{y})")


DEC_SPECS = [
    ("mul", "2.4", "1.5", "test", "dec_mul"),
    ("mul", "3.2", "1.25", "test", "dec_mul"),
    ("mul", "1.8", "0.75", "test", "dec_mul"),
    ("div", "7.2", "1.5", "test", "dec_div"),
    ("div", "8.4", "1.6", "test", "dec_div"),
    ("div", "9.6", "2.4", "test", "dec_div"),
    ("add", "12.3", "4.56", "test", "dec_add_misaligned"),
    ("add", "3.5", "2.75", "test", "dec_add_misaligned"),
    ("sub", "20.4", "3.75", "test", "dec_sub_misaligned"),
    ("sub", "15.2", "4.75", "test", "dec_sub_misaligned"),
    ("cmp", "0.45", "0.8", "test", "dec_compare_longer"),
    ("cmp", "0.125", "0.14", "test", "dec_compare_longer"),
    ("cmp", "0.09", "0.1", "test", "dec_compare_longer"),
    ("cmp", "0.25", "0.9", "test", "dec_compare_longer"),
    ("cmp", "0.3", "0.496", "test", "dec_compare_shorter"),
    ("cmp", "0.75", "0.812", "test", "dec_compare_shorter"),
    ("cmp", "0.6", "0.625", "test", "dec_compare_shorter"),
    ("mul", "1.6", "2.5", "dev", "dec_dev_mul"),
    ("add", "1.2", "3.45", "dev", "dec_dev_add"),
]


# ------------------------------------------------------------------ negative numbers

def neg_item(expr: str, operands: list[int], correct: int, bugs: dict, meta: dict,
             split: str, family: str) -> dict:
    bugs = {k: v for k, v in bugs.items() if canon(v) != canon(correct)}
    meta = {**meta, "expression": expr, "operands": operands, "num1": operands[0], "num2": operands[1],
            "v5_template_family": family}
    return _item("negative_numbers", split, family, f"Calculate: {expr}", correct, bugs, meta.get("operation", "arithmetic"), meta, expr)


def neg_add_two(a: int, b: int, split: str, family: str) -> dict:
    # -a + (-b)
    correct = -a - b
    bugs = {
        "multiplication_rule_for_addition": a + b,
        "two_negatives_always_positive": a + b,
        "larger_absolute_value_always_wins": -(a + b),
    }
    return neg_item(f"-{a} + (-{b})", [-a, -b], correct, bugs,
                    {"operation": "negative_addition", "problem_type": "neg_plus_neg", "operator": "+",
                     "operation_type": "add_negative", "template": family, "a": -a, "b": -b}, split, family)


def neg_sub_neg(a: int, b: int, split: str, family: str) -> dict:
    # -a - (-b), a < b => correct positive
    correct = b - a
    bugs = {
        "larger_absolute_value_always_wins": -(b - a),
        "two_negatives_always_positive": a + b,
        "negative_swaps_operation": -a - b,
        "multiplication_rule_for_addition": b - a,
    }
    return neg_item(f"-{a} - (-{b})", [-a, -b], correct, bugs,
                    {"operation": "negative_subtraction", "problem_type": "neg_minus_neg", "operator": "-",
                     "operation_type": "subtract_negative", "pattern": "negative_minus_negative",
                     "template": family, "a": -a, "b": -b}, split, family)


def neg_add_pos_neg(a: int, b: int, split: str, family: str) -> dict:
    # a + (-b), b > a => correct negative
    correct = a - b
    bugs = {
        "multiplication_rule_for_addition": a + b,
        "negative_swaps_operation": a + b,
        "two_negatives_always_positive": a + b,
        "larger_absolute_value_always_wins": a - b,
    }
    return neg_item(f"{a} + (-{b})", [a, -b], correct, bugs,
                    {"operation": "negative_addition", "problem_type": "pos_plus_neg", "operator": "+",
                     "operation_type": "add_negative", "template": family, "a": a, "b": -b}, split, family)


def neg_sub_pos(a: int, b: int, split: str, family: str) -> dict:
    # -a - b, correct negative
    correct = -a - b
    bugs = {
        "larger_absolute_value_always_wins": abs(b - a),
    }
    return neg_item(f"-{a} - {b}", [-a, b], correct, bugs,
                    {"operation": "negative_subtraction", "problem_type": "neg_minus_pos", "operator": "-",
                     "operation_type": "subtract_positive", "template": "negative_subtraction",
                     "v5_template_family": family, "a": -a, "b": b}, split, family)


def neg_mul_two(a: int, b: int, split: str, family: str) -> dict:
    correct = a * b
    bugs = {"negative_times_negative_negative": -a * b}
    return neg_item(f"(-{a}) * (-{b})", [-a, -b], correct, bugs,
                    {"operation": "multiplication", "template": family, "a": -a, "b": -b}, split, family)


def neg_div_two(a: int, b: int, split: str, family: str) -> dict:
    correct = a // b
    bugs = {"negative_times_negative_negative": -(a // b)}
    return neg_item(f"(-{a}) / (-{b})", [-a, -b], correct, bugs,
                    {"operation": "division", "template": family, "a": -a, "b": -b}, split, family)


NEG_SPECS = [
    ("add2", 3, 5, "test", "neg_add_two"),
    ("add2", 4, 7, "test", "neg_add_two"),
    ("add2", 2, 9, "test", "neg_add_two"),
    ("subneg", 5, 8, "test", "neg_sub_neg"),
    ("subneg", 3, 9, "test", "neg_sub_neg"),
    ("subneg", 7, 10, "test", "neg_sub_neg"),
    ("addpos", 2, 9, "test", "neg_add_pos_neg"),
    ("addpos", 4, 11, "test", "neg_add_pos_neg"),
    ("subpos", 3, 5, "test", "neg_sub_pos"),
    ("mul2", 3, 4, "test", "neg_mul_two"),
    ("mul2", 5, 6, "test", "neg_mul_two"),
    ("div2", 12, 4, "test", "neg_div_two"),
    ("div2", 18, 3, "test", "neg_div_two"),
    ("add2", 2, 3, "dev", "neg_dev_add"),
    ("subneg", 2, 6, "dev", "neg_dev_sub"),
]


# ------------------------------------------------------------------ order of operations

def _eval_left(values: list[int], ops: list[str]) -> int:
    v = values[0]
    for i, op in enumerate(ops):
        if op == "+":
            v += values[i + 1]
        elif op == "-":
            v -= values[i + 1]
        elif op == "*":
            v *= values[i + 1]
        elif op == "/":
            v //= values[i + 1]
    return v


def addition_first(values: list[int], ops: list[str]) -> int:
    """Group runs joined by '+', then subtract the groups left to right."""
    terms = [values[0]]
    for i, op in enumerate(ops):
        if op == "+":
            terms[-1] += values[i + 1]
        elif op == "-":
            terms.append(-values[i + 1])
        else:
            raise ValueError(op)
    return sum(terms)


def multiplication_first(values: list[int], ops: list[str]) -> int:
    """Evaluate '*' before '/' in a chain; division is integer division here."""
    # Only the a / b * c shape is used in the authored items.
    if len(values) == 3 and ops == ["/", "*"]:
        return values[0] // (values[1] * values[2])
    if len(values) == 3 and ops == ["*", "/"]:
        return (values[0] * values[1]) // values[2]
    return _eval_left(values, ops)


SYMBOL_OPS = {"*": "×", "/": "÷"}


def oo_item(text: str, values: list[int], ops: list[str], correct: int, bugs: dict,
            split: str, family: str, lib_template: str) -> dict:
    bugs = {k: v for k, v in bugs.items() if canon(v) != canon(correct)}
    expr = text.replace("Calculate: ", "")
    meta = {
        "template": lib_template,
        "v5_template_family": family,
        "values": values,
        "operations": ops,
        "operations_symbols": [SYMBOL_OPS.get(op, op) for op in ops],
        "expression": expr,
        "operands": values,
    }
    if len(values) == 3:
        meta.update({"a": values[0], "b": values[1], "c": values[2], "op1": ops[0], "op2": ops[1]})
    return _item("order_of_operations", split, family, text, correct, bugs, "order_of_operations", meta, expr)


OO_SPECS = [
    # text, values, ops, correct, add_first, mul_first, left_to_right, ignore_paren, split, family
    ("Calculate: 10 - 3 + 2", [10, 3, 2], ["-", "+"], 9, 5, None, 9, None, "test", "oo_add_sub", "simple_expression"),
    ("Calculate: 20 - 6 + 4", [20, 6, 4], ["-", "+"], 18, 10, None, 18, None, "test", "oo_add_sub", "simple_expression"),
    ("Calculate: 15 - 4 + 6 - 2", [15, 4, 6, 2], ["-", "+", "-"], 15, 3, None, 15, None, "test", "oo_add_sub_long", "mixed_operations"),
    ("Calculate: 8 / 4 * 2", [8, 4, 2], ["/", "*"], 4, None, 1, 4, None, "test", "oo_mul_div", "basic_mult_div"),
    ("Calculate: 12 / 3 * 2", [12, 3, 2], ["/", "*"], 8, None, 2, 8, None, "test", "oo_mul_div", "basic_mult_div"),
    ("Calculate: 18 / 3 * 2", [18, 3, 2], ["/", "*"], 12, None, 3, 12, None, "test", "oo_mul_div", "basic_mult_div"),
    ("Calculate: 2 * (3 + 4)", [2, 3, 4], ["*", "+"], 14, None, None, 10, 10, "test", "oo_paren_mul", "basic_single_parentheses"),
    ("Calculate: 20 - (3 + 5)", [20, 3, 5], ["-", "+"], 12, None, None, 22, 22, "test", "oo_paren_sub", "basic_single_parentheses"),
    ("Calculate: 2 * (3 + (4 - 1))", [2, 3, 4, 1], ["*", "+", "-"], 12, None, None, 9, 9, "test", "oo_nested", "nested_parentheses"),
    ("Calculate: 2 + 3 * 4", [2, 3, 4], ["+", "*"], 14, None, None, 20, None, "test", "oo_mixed_mul", "basic_expression"),
    ("Calculate: 10 - 2 * 3", [10, 2, 3], ["-", "*"], 4, None, None, 24, None, "test", "oo_sub_mul", "basic_expression"),
    ("Calculate: 24 / (2 + 4)", [24, 2, 4], ["/", "+"], 4, None, None, 16, 16, "test", "oo_paren_div", "basic_single_parentheses"),
    ("Calculate: 8 - 2 + 3", [8, 2, 3], ["-", "+"], 9, 3, None, 9, None, "dev", "oo_dev_add_sub", "simple_expression"),
    ("Calculate: 3 * (2 + 5)", [3, 2, 5], ["*", "+"], 21, None, None, 11, 11, "dev", "oo_dev_paren", "basic_single_parentheses"),
]


# ------------------------------------------------------------------ percentages

def pct_of_item(p: int, total: int, split: str, family: str) -> dict:
    correct = Fraction(p, 100) * total
    bugs = {
        "percent_equals_decimal": p * total,
        "percentage_as_index": p,
    }
    return _item("percentages", split, family, f"What is {p}% of {total}?", correct, bugs, "percentage",
                 {"template": family, "percent": p, "value": total, "conversion_type": "percent_in_calculation",
                  "percentage": p, "total": total}, f"{p}/100*{total}")


def pct_change_item(p: int, total: int, direction: str, split: str, family: str) -> dict:
    correct = total * (1 + p / 100) if direction == "increase" else total * (1 - p / 100)
    bugs = {
        "percent_equals_decimal": p * total,
        "percentage_as_index": total + p if direction == "increase" else total - p,
    }
    return _item("percentages", split, family,
                 f"{total} is {'increased' if direction == 'increase' else 'decreased'} by {p}%. What is the result?",
                 correct, bugs, "percentage",
                 {"template": "percentage_increase" if direction == "increase" else "percentage_decrease",
                  "v5_template_family": family, "formula_type": "percentage_increase" if direction == "increase" else "percentage_decrease",
                  "percent": p, "value": total, "conversion_type": "percent_in_calculation",
                  "percentage": p, "total": total}, f"{total}*(1{'+' if direction == 'increase' else '-'}{p}/100)")


def pct_reverse_item(part: int, total: int, split: str, family: str) -> dict:
    p = Fraction(part, total) * 100
    assert p.denominator == 1, "part/total must produce an integer percentage"
    p = int(p)
    correct = Fraction(10000, p)
    bugs = {"reverse_percentage_error": p}
    return _item("percentages", split, family,
                 f"If {part} is {p}% of {total}, what percent is {total} of {part}?",
                 correct, bugs, "percentage_relationship",
                 {"template": "basic_reverse_relationship", "v5_template_family": family,
                  "percentage": p, "part": part, "total": total,
                  "conversion_type": "percent_in_calculation"}, f"10000/{p}")


def pct_sequential_item(initial: int, p1: int, p2: int, split: str, family: str) -> dict:
    correct = Fraction(initial) * Fraction(100 + p1, 100) * Fraction(100 - p2, 100)
    bugs = {"add_percentages_directly": Fraction(initial) * Fraction(100 + p1 - p2, 100)}
    return _item("percentages", split, family,
                 f"{initial} is increased by {p1}% and then decreased by {p2}%. What is the final value?",
                 correct, bugs, "percentage_sequential",
                 {"template": "sequential_percentage", "v5_template_family": family,
                  "initial_value": initial, "percentage1": p1, "percentage2": p2,
                  "problem_type": "increase_then_decrease"}, f"{initial}*(1+{p1}/100)*(1-{p2}/100)")


PCT_SPECS = [
    ("of", 20, 70, "test", "pct_of"),
    ("of", 15, 80, "test", "pct_of"),
    ("of", 25, 64, "test", "pct_of"),
    ("change", 25, 80, "increase", "test", "pct_change"),
    ("change", 15, 60, "decrease", "test", "pct_change"),
    ("reverse", 40, 50, "test", "pct_reverse"),
    ("reverse", 20, 50, "test", "pct_reverse"),
    ("reverse", 25, 125, "test", "pct_reverse"),
    ("seq", 200, 20, 10, "test", "pct_sequential"),
    ("seq", 150, 10, 20, "test", "pct_sequential"),
    ("seq", 80, 25, 20, "test", "pct_sequential"),
    ("of", 10, 50, "dev", "pct_dev_of"),
    ("change", 20, 40, "increase", "dev", "pct_dev_change"),
]


def build_items() -> list[dict]:
    items = []
    for a, b, split, family in SUB_SPECS:
        items.append(sub_item(a, b, split, family))
    for spec in FRAC_SPECS:
        if spec[0] in ("add", "sub"):
            _, a, b, c, d, split, family = spec
            items.append(frac_add_item(a, b, c, d, split, family, "addition" if spec[0] == "add" else "subtraction"))
        elif spec[0] == "mul":
            _, a, b, c, d, split, family = spec
            items.append(frac_mul_item(a, b, c, d, split, family))
        elif spec[0] == "div":
            _, a, b, c, d, split, family = spec
            items.append(frac_div_item(a, b, c, d, split, family))
    for fam in [
        ("frac_compare_three_a", [(7, 10), (5, 12), (3, 4)], "test"),
        ("frac_compare_three_b", [(8, 11), (6, 13), (4, 5)], "test"),
        ("frac_compare_three_c", [(7, 11), (5, 13), (3, 4)], "test"),
        ("frac_dev_compare", [(2, 3), (3, 5), (4, 9)], "dev"),
    ]:
        items.append(frac_compare_item(fam[1], fam[2], fam[0]))
    for spec in DEC_SPECS:
        kind, x, y, split, family = spec
        if kind == "mul":
            items.append(dec_mul_item(x, y, split, family))
        elif kind == "div":
            items.append(dec_div_item(x, y, split, family))
        elif kind == "add":
            items.append(dec_add_item(x, y, "addition", split, family))
        elif kind == "sub":
            items.append(dec_add_item(x, y, "subtraction", split, family))
        elif kind == "cmp":
            items.append(dec_compare_item(x, y, split, family))
    for spec in NEG_SPECS:
        kind, a, b, split, family = spec
        fn = {"add2": neg_add_two, "subneg": neg_sub_neg, "addpos": neg_add_pos_neg,
              "subpos": neg_sub_pos, "mul2": neg_mul_two, "div2": neg_div_two}[kind]
        items.append(fn(a, b, split, family))
    for text, values, ops, correct, add_first, mul_first, left, ignore_paren, split, family, lib_template in OO_SPECS:
        bugs = {}
        if add_first is not None:
            bugs["addition_before_subtraction_always"] = add_first
        if mul_first is not None:
            bugs["multiplication_before_division_always"] = mul_first
        if left is not None:
            bugs["strict_left_to_right"] = left
        if ignore_paren is not None:
            bugs["ignore_parentheses"] = ignore_paren
        items.append(oo_item(text, values, ops, correct, bugs, split, family, lib_template))
    for spec in PCT_SPECS:
        kind = spec[0]
        if kind == "of":
            _, p, total, split, family = spec
            items.append(pct_of_item(p, total, split, family))
        elif kind == "change":
            _, p, total, direction, split, family = spec
            items.append(pct_change_item(p, total, direction, split, family))
        elif kind == "reverse":
            _, part, total, split, family = spec
            items.append(pct_reverse_item(part, total, split, family))
        elif kind == "seq":
            _, initial, p1, p2, split, family = spec
            items.append(pct_sequential_item(initial, p1, p2, split, family))
    return items


if __name__ == "__main__":
    items = build_items()
    from collections import Counter
    print("items", len(items), Counter((i["category"], i["split"]) for i in items))
    for i in items[:6]:
        print(i["category"], i["family"], i["text"], "correct", i["correct"],
              "n_bugs", sum(1 for k, v in i["predictions"].items() if v != i["correct"]))
