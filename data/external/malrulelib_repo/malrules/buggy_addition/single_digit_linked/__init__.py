"""
Single-Digit-Linked Malrule

A procedural bug where students link (append) single-digit operands to the end
of multi-digit operands instead of adding them. The single-digit number is
always appended to the multi-digit number, regardless of which operand it is.

Example: 19 + 9 = 199 (Correct: 28) - single digit 9 appended to 19
Example: 8 + 12 = 128 (Correct: 20) - single digit 8 appended to 12 (NOT 812!)

"""

from .problem_generator import SingleDigitLinkedProblemGenerator
from .malrule_algorithm import SingleDigitLinkedMalrule
from .correct_algorithm import AdditionCorrectAlgorithm

__all__ = [
    'SingleDigitLinkedProblemGenerator',
    'SingleDigitLinkedMalrule',
    'AdditionCorrectAlgorithm',
]
