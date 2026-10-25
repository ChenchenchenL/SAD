"""
Ignore-Parentheses malrule.

Students process expressions without respecting parentheses,
either using left-to-right or applying PEMDAS without parentheses first.
"""

from .problem_generator import IgnoreParenthesesProblemGenerator
from .malrule_algorithm import IgnoreParenthesesMalrule
from .correct_algorithm import OrderOfOperationsCorrectAlgorithm

__all__ = [
    'IgnoreParenthesesProblemGenerator',
    'IgnoreParenthesesMalrule',
    'OrderOfOperationsCorrectAlgorithm',
]
