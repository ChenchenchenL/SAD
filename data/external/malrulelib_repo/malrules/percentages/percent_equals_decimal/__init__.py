"""
Percent-Equals-Decimal Malrule

Students confuse percent, decimal, and whole number notations, treating them as interchangeable.

Example: What is 25% as a decimal? → Student: 25 ❌
Correct: 0.25 ✓

Common confusions:
- 25% = 0.25 = 25 (treats all as same)
- 30% of 50: Student uses 30 instead of 0.30
- Converting 0.5 to %: Student thinks 0.5%

"""

from .problem_generator import PercentEqualsDecimalProblemGenerator
from .malrule_algorithm import PercentEqualsDecimalMalrule
from .correct_algorithm import PercentageConversionCorrectAlgorithm

__all__ = [
    'PercentEqualsDecimalProblemGenerator',
    'PercentEqualsDecimalMalrule',
    'PercentageConversionCorrectAlgorithm'
]
