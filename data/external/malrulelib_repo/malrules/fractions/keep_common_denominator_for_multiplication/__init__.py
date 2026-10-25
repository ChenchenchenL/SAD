"""
Keep-Common-Denominator-For-Multiplication Malrule

Student keeps common denominator when multiplying fractions: (a/b)×(c/b) = (a×c)/b
Example: (2/5)×(3/5) = 6/5 (instead of 6/25)
"""

from .problem_generator import KeepCommonDenominatorForMultiplicationProblemGenerator
from .malrule_algorithm import KeepCommonDenominatorForMultiplicationMalrule
from .correct_algorithm import FractionMultiplicationCorrectAlgorithm

__all__ = [
    'KeepCommonDenominatorForMultiplicationProblemGenerator',
    'KeepCommonDenominatorForMultiplicationMalrule',
    'FractionMultiplicationCorrectAlgorithm'
]
