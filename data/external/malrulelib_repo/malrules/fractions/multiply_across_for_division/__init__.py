"""
Multiply-Across-For-Division malrule implementation.

Students think: (a/b)÷(c/d) = (a÷c)/(b÷d) instead of (a/b)×(d/c)
"""

from .problem_generator import MultiplyAcrossForDivisionProblemGenerator
from .malrule_algorithm import MultiplyAcrossForDivisionMalrule
from .correct_algorithm import FractionDivisionCorrectAlgorithm

__all__ = [
    'MultiplyAcrossForDivisionProblemGenerator',
    'MultiplyAcrossForDivisionMalrule',
    'FractionDivisionCorrectAlgorithm'
]
