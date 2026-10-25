"""
Borrow-From-Bottom Malrule

Students borrow from the bottom number instead of the top number.

Example: 53 - 28 → Student borrows from 28: 53 - 1(18) = 45 ✗ (should be 25)

Students misunderstand the borrowing direction - they decrement the wrong number.

"""

from .problem_generator import BorrowFromBottomProblemGenerator
from .malrule_algorithm import BorrowFromBottomMalrule
from .correct_algorithm import SubtractionCorrectAlgorithm

__all__ = [
    'BorrowFromBottomProblemGenerator',
    'BorrowFromBottomMalrule',
    'SubtractionCorrectAlgorithm'
]
