"""
Borrow-Writes-10 malrule.

When borrowing from a column where the top digit is 0, the student
borrows from the next column to the left correctly but writes 10
instead of 9 in this column.

Example: 1300 - 522 = 788 (Correct: 778)
  - Student correctly borrows through the zeros
  - But writes 10 instead of 9 in the tens place
  - So tens: 10-2=8 instead of 9-2=7

Network location: ZERO procedure (writes 10 instead of 9)
"""

from .problem_generator import BorrowWrites10ProblemGenerator
from .malrule_algorithm import BorrowWrites10Malrule
from .correct_algorithm import SubtractionCorrectAlgorithm

__all__ = [
    'BorrowWrites10ProblemGenerator',
    'BorrowWrites10Malrule',
    'SubtractionCorrectAlgorithm',
]
