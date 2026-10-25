"""
Add-All-Digits Malrule

The student always sums up all the digits with no regard to columns.
Instead of aligning digits by place value and adding column by column,
the student simply adds every individual digit together.

Example: 17 + 5 = 13 (correct: 22) -> 1+7+5=13
Example: 51 + 1707 = 21 (correct: 1758) -> 5+1+1+7+0+7=21

"""

from .problem_generator import AddAllDigitsProblemGenerator
from .malrule_algorithm import AddAllDigitsMalrule
from .correct_algorithm import AdditionCorrectAlgorithm

__all__ = [
    'AddAllDigitsProblemGenerator',
    'AddAllDigitsMalrule',
    'AdditionCorrectAlgorithm',
]
