"""
Borrow-No-Decrement Malrule

One of the most common subtraction bugs where students borrow
correctly but forget to decrement the digit they borrowed from.
"""

from .problem_generator import BorrowNoDecrementProblemGenerator
from .malrule_algorithm import BorrowNoDecrementMalrule
from .correct_algorithm import SubtractionCorrectAlgorithm

__all__ = [
    'BorrowNoDecrementProblemGenerator',
    'BorrowNoDecrementMalrule',
    'SubtractionCorrectAlgorithm',
]
