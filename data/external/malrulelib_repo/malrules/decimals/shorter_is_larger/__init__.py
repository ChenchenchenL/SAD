"""
Shorter-Is-Larger malrule.

Students incorrectly believe that decimals with fewer decimal places
are larger (opposite of Longer-Is-Larger).
"""

from .problem_generator import ShorterIsLargerProblemGenerator
from .malrule_algorithm import ShorterIsLargerMalrule
from .correct_algorithm import DecimalComparisonCorrectAlgorithm

__all__ = [
    'ShorterIsLargerProblemGenerator',
    'ShorterIsLargerMalrule',
    'DecimalComparisonCorrectAlgorithm',
]
