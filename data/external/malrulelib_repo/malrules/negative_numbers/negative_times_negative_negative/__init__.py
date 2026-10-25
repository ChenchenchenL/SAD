"""
Negative-Times-Negative-Negative malrule.

Students incorrectly apply reversed sign rules for multiplication,
believing that negative × negative = negative (instead of positive).
"""

from .problem_generator import NegativeTimesNegativeNegativeProblemGenerator
from .malrule_algorithm import NegativeTimesNegativeNegativeMalrule
from .correct_algorithm import NegativeMultiplicationCorrectAlgorithm

__all__ = [
    'NegativeTimesNegativeNegativeProblemGenerator',
    'NegativeTimesNegativeNegativeMalrule',
    'NegativeMultiplicationCorrectAlgorithm',
]
