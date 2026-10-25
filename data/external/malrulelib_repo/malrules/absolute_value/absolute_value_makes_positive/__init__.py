"""
Absolute-Value-Makes-Positive Malrule

Student thinks absolute value "makes negatives positive": |x| = -3 has solution x = 3
Example: |x| = -5 → x = 5 (instead of recognizing no solution exists)
"""

from .problem_generator import AbsoluteValueMakesPositiveProblemGenerator
from .malrule_algorithm import AbsoluteValueMakesPositiveMalrule
from .correct_algorithm import AbsoluteValueEquationCorrectAlgorithm

__all__ = [
    'AbsoluteValueMakesPositiveProblemGenerator',
    'AbsoluteValueMakesPositiveMalrule',
    'AbsoluteValueEquationCorrectAlgorithm'
]
