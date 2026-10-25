"""
Larger-Absolute-Value-Always-Wins malrule.

Students incorrectly determine the sign of the result by always
using the sign of the number with the larger absolute value.
"""

from .problem_generator import LargerAbsoluteValueAlwaysWinsProblemGenerator
from .malrule_algorithm import LargerAbsoluteValueAlwaysWinsMalrule
from .correct_algorithm import NegativeNumbersCorrectAlgorithm

__all__ = [
    'LargerAbsoluteValueAlwaysWinsProblemGenerator',
    'LargerAbsoluteValueAlwaysWinsMalrule',
    'NegativeNumbersCorrectAlgorithm',
]
