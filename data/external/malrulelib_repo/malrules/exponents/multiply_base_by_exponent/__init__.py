"""
Multiply-Base-By-Exponent Malrule

Student treats exponentiation as multiplication: a^b = a × b
Example: 2³ = 2 × 3 = 6 (instead of 2 × 2 × 2 = 8)
"""

from .problem_generator import MultiplyBaseByExponentProblemGenerator
from .malrule_algorithm import MultiplyBaseByExponentMalrule
from .correct_algorithm import ExponentiationCorrectAlgorithm

__all__ = [
    'MultiplyBaseByExponentProblemGenerator',
    'MultiplyBaseByExponentMalrule',
    'ExponentiationCorrectAlgorithm'
]
