"""
Multiply-Exponents-When-Multiplying-Powers Malrule

Student multiplies exponents when multiplying powers: x^m × x^n = x^(m×n)
Example: x³ × x⁵ = x¹⁵ (instead of x⁸)
"""

from .problem_generator import MultiplyExponentsWhenMultiplyingPowersProblemGenerator
from .malrule_algorithm import MultiplyExponentsWhenMultiplyingPowersMalrule
from .correct_algorithm import ProductRuleCorrectAlgorithm

__all__ = [
    'MultiplyExponentsWhenMultiplyingPowersProblemGenerator',
    'MultiplyExponentsWhenMultiplyingPowersMalrule',
    'ProductRuleCorrectAlgorithm'
]
