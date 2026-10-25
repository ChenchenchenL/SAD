"""
Absolute-Value-Distributes malrule implementation.

Students think: |x+2| = |x| + 2 instead of evaluating the expression inside first
"""

from .problem_generator import AbsoluteValueDistributesProblemGenerator
from .malrule_algorithm import AbsoluteValueDistributesMalrule
from .correct_algorithm import AbsoluteValueCorrectAlgorithm

__all__ = [
    'AbsoluteValueDistributesProblemGenerator',
    'AbsoluteValueDistributesMalrule',
    'AbsoluteValueCorrectAlgorithm'
]
