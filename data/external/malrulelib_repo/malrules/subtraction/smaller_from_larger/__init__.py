"""
Smaller-From-Larger Malrule

One of the most common subtraction bugs where students always subtract
the smaller digit from the larger digit, regardless of position.
"""

from .problem_generator import SmallerFromLargerProblemGenerator
from .malrule_algorithm import SmallerFromLargerMalrule
from .correct_algorithm import SubtractionCorrectAlgorithm

__all__ = [
    'SmallerFromLargerProblemGenerator',
    'SmallerFromLargerMalrule',
    'SubtractionCorrectAlgorithm',
]
