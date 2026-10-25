"""
Mode-Must-Exist malrule.

Students believe every data set must have a mode. When no value repeats,
they incorrectly pick the largest value, the smallest value, or the middle
value as the "mode" instead of recognizing that no mode exists.
"""

from .problem_generator import ModeMustExistProblemGenerator
from .malrule_algorithm import ModeMustExistMalrule
from .correct_algorithm import ModeMustExistCorrectAlgorithm

__all__ = [
    'ModeMustExistProblemGenerator',
    'ModeMustExistMalrule',
    'ModeMustExistCorrectAlgorithm',
]
