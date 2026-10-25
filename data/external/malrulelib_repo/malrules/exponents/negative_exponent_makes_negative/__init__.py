"""
Negative-Exponent-Makes-Negative Malrule

Student thinks negative exponent makes the result negative: x^-n = -x^n
Example: 2^-2 = -4 (instead of 1/4)
"""

from .problem_generator import NegativeExponentMakesNegativeProblemGenerator
from .malrule_algorithm import NegativeExponentMakesNegativeMalrule
from .correct_algorithm import NegativeExponentCorrectAlgorithm

__all__ = [
    'NegativeExponentMakesNegativeProblemGenerator',
    'NegativeExponentMakesNegativeMalrule',
    'NegativeExponentCorrectAlgorithm'
]
