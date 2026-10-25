"""
Function-Notation-Is-Multiplication Malrule

Students think f(x) means f × x (multiplication).

Example: If f(x) = x + 3, then f(5) → Student: f × 5 instead of 5 + 3 ✗

Students misinterpret function notation as indicating multiplication.

"""

from .problem_generator import FunctionNotationIsMultiplicationProblemGenerator
from .malrule_algorithm import FunctionNotationIsMultiplicationMalrule
from .correct_algorithm import FunctionEvaluationCorrectAlgorithm

__all__ = [
    'FunctionNotationIsMultiplicationProblemGenerator',
    'FunctionNotationIsMultiplicationMalrule',
    'FunctionEvaluationCorrectAlgorithm'
]
