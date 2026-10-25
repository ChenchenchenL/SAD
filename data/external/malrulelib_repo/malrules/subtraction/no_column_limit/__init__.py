"""
No-Column-Limit Malrule

Students don't understand that a column can't hold values > 9.
When adding, they write multi-digit sums directly in one column without regrouping.
"""

from .problem_generator import NoColumnLimitProblemGenerator
from .malrule_algorithm import NoColumnLimitMalrule
from .correct_algorithm import TwoDigitAdditionCorrectAlgorithm

__all__ = [
    'NoColumnLimitProblemGenerator',
    'NoColumnLimitMalrule',
    'TwoDigitAdditionCorrectAlgorithm',
]
