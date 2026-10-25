"""
Common-Denominator-Numerator Malrule

Students add numerators correctly but make denominators same by adding them.

Example: 1/4 + 1/6 → Student: (1+1)/(4+6) = 2/10 = 1/5 ❌
Correct: Find LCD (12): 3/12 + 2/12 = 5/12 ✓

This is a variant where they partially understand common denominators
but incorrectly create them by adding.

"""

from .problem_generator import CommonDenominatorNumeratorProblemGenerator
from .malrule_algorithm import CommonDenominatorNumeratorMalrule
from .correct_algorithm import FractionAdditionCorrectAlgorithm

__all__ = [
    'CommonDenominatorNumeratorProblemGenerator',
    'CommonDenominatorNumeratorMalrule',
    'FractionAdditionCorrectAlgorithm'
]
