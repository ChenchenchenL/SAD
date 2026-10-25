"""
Right-Align-Decimals malrule.

Students align decimal numbers by the rightmost digit instead of
by the decimal point when performing addition or subtraction.
"""

from .problem_generator import RightAlignDecimalsProblemGenerator
from .malrule_algorithm import RightAlignDecimalsMalrule
from .correct_algorithm import DecimalAdditionCorrectAlgorithm

__all__ = [
    'RightAlignDecimalsProblemGenerator',
    'RightAlignDecimalsMalrule',
    'DecimalAdditionCorrectAlgorithm',
]
