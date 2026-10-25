"""
Percentage-As-Index Malrule

Students treat percentage as a position marker or index rather than a proportion.

Example: "30% of 50" → Student thinks "30th position of 50" = 30 ✗ (should be 15)

Students confuse ordinal position with multiplicative percentage calculation.

"""

from .problem_generator import PercentageAsIndexProblemGenerator
from .malrule_algorithm import PercentageAsIndexMalrule
from .correct_algorithm import PercentageCorrectAlgorithm

__all__ = [
    'PercentageAsIndexProblemGenerator',
    'PercentageAsIndexMalrule',
    'PercentageCorrectAlgorithm'
]
