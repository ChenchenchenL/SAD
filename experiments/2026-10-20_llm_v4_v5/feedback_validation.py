"""Frozen validators for formal feedback evaluation (protocol v4)."""
from __future__ import annotations

import re
from fractions import Fraction

import sympy as sp

NUMBER = r"-?\d+(?:\.\d+)?"
FRACTION = r"-?\d+/\d+"
EQ_RE = re.compile(
    rf"({NUMBER}|{FRACTION})\s*([+\-*/])\s*({NUMBER}|{FRACTION})\s*=\s*({NUMBER}|{FRACTION})"
)


def _number(value: str) -> Fraction | float | None:
    value = value.strip().replace(",", "").replace("$", "").replace("%", "")
    value = re.sub(r"(cm|mm|meters?|m|items?|dollars?|people|students?|books?|liters?|gallons?)\b", "", value).strip()
    if "/" in value:
        try:
            return Fraction(value)
        except Exception:
            return None
    try:
        return float(value)
    except Exception:
        return None


def leak_suspected(feedback: str, correct: str) -> dict:
    """Deterministic string/number match. This only marks suspicion."""
    answer = correct.strip().lstrip("$").rstrip("%").strip()
    if not answer:
        return {"suspected": False, "match": None}
    if "/" in answer:
        hit = re.search(rf"(?<![\d/]){re.escape(answer)}(?![\d/])", feedback)
        return {"suspected": bool(hit), "match": answer if hit else None}
    num = _number(correct)
    if num is None:
        hit = answer.lower() in feedback.lower()
        return {"suspected": bool(hit), "match": answer if hit else None}
    body = str(num).rstrip("0").rstrip(".") if isinstance(num, float) else str(num)
    hit = re.search(rf"(?<![\d.]){re.escape(body)}(?![\d.])", feedback)
    return {"suspected": bool(hit), "match": body if hit else None}


def verify_math(feedback: str) -> dict:
    """Tri-state check of explicit arithmetic equations in the feedback."""
    checked = correct = incorrect = 0
    for m in EQ_RE.finditer(feedback):
        a, op, b, c = m.groups()
        va, vb, vc = _number(a), _number(b), _number(c)
        if va is None or vb is None or vc is None:
            continue
        try:
            expected = {"+": va + vb, "-": va - vb, "*": va * vb, "/": va / vb}[op]
        except Exception:
            continue
        checked += 1
        if abs(float(expected) - float(vc)) <= 1e-6:
            correct += 1
        else:
            incorrect += 1
    if checked == 0:
        status = "unverifiable"
    elif incorrect:
        status = "incorrect"
    else:
        status = "correct"
    return {"status": status, "checked": checked, "correct": correct, "incorrect": incorrect}


def validate(feedback: str, correct: str) -> dict:
    return {"leak": leak_suspected(feedback, correct), "math": verify_math(feedback)}
