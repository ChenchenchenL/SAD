"""
Incomplete-Factoring malrule implementation.

Students stop factoring before the expression is completely factored.
Example: 2x² - 8 = 2(x² - 4) instead of 2(x+2)(x-2)
"""

from .problem_generator import IncompleteFactoringProblemGenerator
from .malrule_algorithm import IncompleteFactoringMalrule
from .correct_algorithm import CompleteFactoringCorrectAlgorithm

__all__ = [
    'IncompleteFactoringProblemGenerator',
    'IncompleteFactoringMalrule',
    'CompleteFactoringCorrectAlgorithm'
]
