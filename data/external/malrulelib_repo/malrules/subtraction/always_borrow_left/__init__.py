"""
Always-Borrow-Left Malrule

Students always borrow from the immediate left column, even when not needed.

Example: 75 - 32 → Student borrows unnecessarily: 6(15) - 32 = 43 ✓ (accidentally correct!)
But: 85 - 23 → Student borrows: 7(15) - 23 = 52 ❌ (should be 62)

Students overgeneralize the borrowing procedure and apply it to every column,
regardless of whether top digit is larger than bottom digit.

"""

from .problem_generator import AlwaysBorrowLeftProblemGenerator
from .malrule_algorithm import AlwaysBorrowLeftMalrule
from .correct_algorithm import SubtractionCorrectAlgorithm

__all__ = [
    'AlwaysBorrowLeftProblemGenerator',
    'AlwaysBorrowLeftMalrule',
    'SubtractionCorrectAlgorithm'
]
