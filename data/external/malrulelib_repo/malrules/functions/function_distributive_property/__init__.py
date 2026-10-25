"""
Function-Distributive-Property Malrule

Students think functions distribute over addition: f(x+a) = f(x) + f(a)

Example: f(x) = x², f(5+2)
Student: f(5+2) = f(5) + f(2) = 25 + 4 = 29 ✗
Correct: f(5+2) = f(7) = 49 ✓

Incorrect generalization from distributive property.

"""

from .problem_generator import FunctionDistributivePropertyProblemGenerator
from .malrule_algorithm import FunctionDistributivePropertyMalrule
from .correct_algorithm import FunctionCompositionCorrectAlgorithm

__all__ = [
    'FunctionDistributivePropertyProblemGenerator',
    'FunctionDistributivePropertyMalrule',
    'FunctionCompositionCorrectAlgorithm'
]
