"""Per-malrule applicability for the six controlled categories.

The rule is deliberately conservative: a malrule is applicable only on the
operations/templates authored by its own generator, with manual overrides for
known cross-operation mistakes (e.g. decimal comparison bugs on subtraction).
"""
from __future__ import annotations

import re

BLACKLIST_TEMPLATES = {
    "multi_step_problem",
    "multi_step_expression",
    "multi_step",
}

# Templates whose correct answer is not a single numeric value in this repo
# (the correct algorithm returns the first operand or the RHS instead).
CATEGORY_BLACKLIST = {
    "subtraction": {
        "comparison_problem",
        "missing_number",
        "multi_step_problem",
        "word_problem_missing_minuend",
        "word_problem_missing_subtrahend",
    },
    "negative_numbers": {"comparison_problem", "multi_step_expression", "pattern_completion"},
}

FRACTION_ARITHMETIC = {
    "add_numerators_denominators",
    "common_denominator_numerator",
    "subtract_across",
    "keep_common_denominator_for_multiplication",
    "multiply_across_for_division",
    "ignore_denominators",
}
FRACTION_COMPARISON_TEMPLATES = {
    "comparison_problem",
    "fraction_comparison",
    "fraction_ordering",
    "basic_comparison",
    "ordering",
    "three_fractions_ordering",
    "benchmark_comparison",
    "word_problem_ordering",
    "mixed_comparisons",
}


def is_blacklisted(category: str, template: str | None) -> bool:
    return template in BLACKLIST_TEMPLATES or template in CATEGORY_BLACKLIST.get(category, set())


def is_text_blacklisted(text: str) -> bool:
    # "Who was faster?" answers with a person, not with a numeric value;
    # the executable malrule predictions cannot be scored against it.
    return bool(re.search(r"\bwho\b", text, re.I))

OVERRIDES: dict[str, dict[str, set[str]]] = {
    "subtraction": {
        "decompose_by_place_value_label": {"place_value_decomposition"},
        "no_column_limit": {"subtraction"},
        "diff_0_n_equals_n": {"subtraction"},
        "stops_borrow_at_zero": {"subtraction"},
    },
    "fractions": {
        "add_numerators_denominators": {"fraction_addition"},
        "common_denominator_numerator": {"fraction_addition"},
        "denominator_comparison_error": {"fraction_comparison", "fraction_ordering"},
        "keep_common_denominator_for_multiplication": {"fraction_multiplication"},
        "multiply_across_for_division": {"fraction_division"},
        "natural_number_bias_numerator_only": {"fraction_comparison", "fraction_ordering"},
        "subtract_across": {"fraction_subtraction"},
    },
    "decimals": {
        "longer_is_larger": {"comparison", "decimal_comparison"},
        "shorter_is_larger": {"comparison", "decimal_comparison"},
        "ignore_decimal_point": {"multiplication", "division"},
        "right_align_decimals": {"addition", "subtraction", "mixed"},
    },
    "negative_numbers": {
        "multiplication_rule_for_addition": {"negative_addition", "negative_subtraction", "sequential_operations"},
        "two_negatives_always_positive": {"negative_addition", "negative_subtraction", "multi_step"},
        "negative_times_negative_negative": {"multiplication", "mixed", "distributive", "equation"},
        "negative_swaps_operation": {"arithmetic", "negative_subtraction"},
    },
    "order_of_operations": {},
    "percentages": {
        "percent_equals_decimal": {"percentage_conversion", "percentage_calculation"},
        "percentage_as_index": {"percentage", "percentage_calculation"},
        "reverse_percentage_error": {"percentage_relationship"},
        "add_percentages_directly": {"percentage_sequential"},
    },
}


def normalize(text: str) -> str:
    return (
        text.replace("\u2212", "-")
        .replace("\u00d7", "*")
        .replace("\u00f7", "/")
        .replace("\u2013", "-")
        .replace("\u2014", "-")
    )


def _count_binary_ops(text: str) -> int:
    # Operators between numeric/right-parenthesis tokens; leading signs do not count.
    cleaned = normalize(text)
    return len(re.findall(r"(?<=[0-9)])\s*[+\-*/]\s*(?=[0-9(])", cleaned))


def is_applicable(category: str, local: str, item: dict, authored_ops: dict[str, set[str]]) -> bool:
    template = item.get("template")
    if is_blacklisted(category, template):
        return False
    if is_text_blacklisted(item.get("text", "")):
        return False

    operation = item.get("operation")
    allowed = OVERRIDES.get(category, {}).get(local, authored_ops.get(local, set()))
    if allowed and operation not in allowed:
        return False
    if not allowed:
        # A malrule with no authored items and no override cannot be validated.
        return False

    text = normalize(item.get("text", ""))
    operands = item.get("operands") or []

    if category == "fractions" and local in FRACTION_ARITHMETIC:
        if template in FRACTION_COMPARISON_TEMPLATES:
            return False

    if category == "subtraction":
        if local == "diff_0_n_equals_n":
            if not any("0" in str(x) for x in operands):
                return False
        if local == "stops_borrow_at_zero":
            if not operands or "0" not in str(operands[0]):
                return False

    if category == "order_of_operations":
        if local == "ignore_parentheses" and "(" not in text and "[" not in text:
            return False
        if local == "addition_before_subtraction_always" and not ("+" in text and "-" in text):
            return False
        if local == "multiplication_before_division_always" and not ("*" in text and "/" in text):
            return False
        if local in ("pemdas_strictly_sequential", "strict_left_to_right"):
            if _count_binary_ops(text) < 2:
                return False
        if local == "pemdas_strictly_sequential":
            # On a same-precedence chain, sequential evaluation is correct;
            # require both an additive and a multiplicative operator.
            if not (("*" in text or "/" in text) and ("+" in text or "-" in text)):
                return False

    if category == "percentages":
        if local == "reverse_percentage_error" and operation != "percentage_relationship":
            return False
        if local == "percentage_as_index" and operation not in ("percentage", "percentage_calculation"):
            return False

    return True
