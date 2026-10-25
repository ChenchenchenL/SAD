"""
Forget-Exponent-On-Coefficient Malrule

Student forgets to raise coefficient to the outer power: (cx^m)^n = c·x^(mn)
Example: (2x³)⁵ = 2x¹⁵ (instead of 32x¹⁵)
"""

from .problem_generator import ForgetExponentOnCoefficientProblemGenerator
from .malrule_algorithm import ForgetExponentOnCoefficientMalrule
from .correct_algorithm import PowerOfPowerCorrectAlgorithm

__all__ = [
    'ForgetExponentOnCoefficientProblemGenerator',
    'ForgetExponentOnCoefficientMalrule',
    'PowerOfPowerCorrectAlgorithm'
]
