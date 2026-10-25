"""
Stops-Borrow-At-Zero malrule.

Students stop the borrowing process when they encounter a zero,
rather than continuing to cascade left.
"""

from .problem_generator import StopsBorrowAtZeroProblemGenerator
from .malrule_algorithm import StopsBorrowAtZeroMalrule
from .correct_algorithm import SubtractionCorrectAlgorithm

__all__ = [
    'StopsBorrowAtZeroProblemGenerator',
    'StopsBorrowAtZeroMalrule',
    'SubtractionCorrectAlgorithm',
]
