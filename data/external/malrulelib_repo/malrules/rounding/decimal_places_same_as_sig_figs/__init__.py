"""
Decimal-Places-Same-As-Sig-Figs Malrule

Students confuse decimal places with significant figures.
They think "3 decimal places" means "3 significant figures".
"""

from .problem_generator import DecimalPlacesSameAsSigFigsProblemGenerator
from .malrule_algorithm import DecimalPlacesSameAsSigFigsMalrule
from .correct_algorithm import SignificantFiguresCorrectAlgorithm

__all__ = [
    'DecimalPlacesSameAsSigFigsProblemGenerator',
    'DecimalPlacesSameAsSigFigsMalrule',
    'SignificantFiguresCorrectAlgorithm',
]
