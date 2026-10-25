"""
Sum-Of-Squares-Factors Malrule

Student incorrectly factors sum of squares: a² + b² = (a+b)²
Example: x² + 4 → Student: (x+2)² instead of "cannot be factored over reals"
"""

from .problem_generator import SumOfSquaresFactorsProblemGenerator
from .malrule_algorithm import SumOfSquaresFactorsMalrule
from .correct_algorithm import SumOfSquaresCorrectAlgorithm

__all__ = [
    'SumOfSquaresFactorsProblemGenerator',
    'SumOfSquaresFactorsMalrule',
    'SumOfSquaresCorrectAlgorithm'
]
