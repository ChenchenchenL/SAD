"""
Longer-Is-Larger malrule for decimal comparison.

Students incorrectly believe that more decimal digits means a larger number.
For example, they think 0.36 > 0.5 because 36 > 5.
"""

from .problem_generator import LongerIsLargerProblemGenerator
from .malrule_algorithm import LongerIsLargerMalrule
from .correct_algorithm import DecimalComparisonCorrectAlgorithm

__all__ = [
    'LongerIsLargerProblemGenerator',
    'LongerIsLargerMalrule',
    'DecimalComparisonCorrectAlgorithm',
]
