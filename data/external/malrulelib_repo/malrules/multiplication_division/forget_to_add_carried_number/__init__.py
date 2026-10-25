"""
Forget-To-Add-Carried-Number Malrule

Student forgets to add the carried value when doing multi-digit multiplication.
Example: 23 × 4 → Student gets 82 instead of 92 (forgets to add carry)
"""

from .problem_generator import ForgetToAddCarriedNumberProblemGenerator
from .malrule_algorithm import ForgetToAddCarriedNumberMalrule
from .correct_algorithm import MultiDigitMultiplicationCorrectAlgorithm

__all__ = [
    'ForgetToAddCarriedNumberProblemGenerator',
    'ForgetToAddCarriedNumberMalrule',
    'MultiDigitMultiplicationCorrectAlgorithm'
]
