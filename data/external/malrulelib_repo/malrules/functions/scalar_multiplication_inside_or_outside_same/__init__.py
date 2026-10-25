"""
Scalar-Multiplication-Inside-Or-Outside-Same Malrule

Student confuses input multiplication with output multiplication: f(cx) = c·f(x)
Example: If f(x)=x², then f(2x) = 2f(x) = 2x² (instead of 4x²)
"""

from .problem_generator import ScalarMultiplicationInsideOrOutsideSameProblemGenerator
from .malrule_algorithm import ScalarMultiplicationInsideOrOutsideSameMalrule
from .correct_algorithm import FunctionEvaluationCorrectAlgorithm

__all__ = [
    'ScalarMultiplicationInsideOrOutsideSameProblemGenerator',
    'ScalarMultiplicationInsideOrOutsideSameMalrule',
    'FunctionEvaluationCorrectAlgorithm'
]
