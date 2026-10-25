"""
Sign-Errors-In-Factoring Malrule

Student makes sign errors when factoring quadratics, especially in decomposition method.
Example: x² + 5x + 6 → Student factors as (x - 2)(x - 3) instead of (x + 2)(x + 3)
"""

from .problem_generator import SignErrorsInFactoringProblemGenerator
from .malrule_algorithm import SignErrorsInFactoringMalrule
from .correct_algorithm import QuadraticFactoringCorrectAlgorithm

__all__ = [
    'SignErrorsInFactoringProblemGenerator',
    'SignErrorsInFactoringMalrule',
    'QuadraticFactoringCorrectAlgorithm'
]
