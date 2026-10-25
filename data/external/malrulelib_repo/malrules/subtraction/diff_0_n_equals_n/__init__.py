"""
Diff-0-N=N malrule.

Students treat 0 - N as simply N, not recognizing that subtraction
from zero requires borrowing from the next column to the left.
"""

from .problem_generator import Diff0NEqualsNProblemGenerator
from .malrule_algorithm import Diff0NEqualsNMalrule
from .correct_algorithm import SubtractionCorrectAlgorithm

__all__ = [
    'Diff0NEqualsNProblemGenerator',
    'Diff0NEqualsNMalrule',
    'SubtractionCorrectAlgorithm',
]
