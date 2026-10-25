"""
Move-Over-Zero-Borrow malrule.

When the student needs to borrow from a column whose top digit is 0,
they SKIP that column and borrow from the next one to the left,
but do NOT decrement the 0. The 0 remains unchanged.

Example: 304 - 75 = 139 (Correct: 229)
  - Student skips the 0 and borrows from the 3
  - 3 becomes 2, 0 stays 0, 4 becomes 14
  - Column work: 14-5=9, 0-7=-7 (handled as smaller-from-larger: 7-0=7 or 0-7=7)
  - Hundreds: 2-0=2 -> Result varies based on secondary bug handling

Network location: FIND NEXT COLUMN procedure
"""

from .problem_generator import MoveOverZeroBorrowProblemGenerator
from .malrule_algorithm import MoveOverZeroBorrowMalrule
from .correct_algorithm import SubtractionCorrectAlgorithm

__all__ = [
    'MoveOverZeroBorrowProblemGenerator',
    'MoveOverZeroBorrowMalrule',
    'SubtractionCorrectAlgorithm',
]
