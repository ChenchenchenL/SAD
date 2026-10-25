"""
Borrow-Into-1-Equals-10 malrule (BORROW/INTO/1=10).

When borrowing into a column whose top digit is 1, the student gets 10
instead of 11. The student fails to add 10 to the existing digit, treating
the borrowed 10 as a replacement rather than an addition.

Example: 321 - 89 = 231 (Correct: 232)
  - Ones: 1 - 9 needs borrow, 11 - 9 = 2 (correct)
  - Tens: 2 becomes 1 after decrement, needs borrow, should be 11 - 8 = 3
         but student gets 10 - 8 = 2 (MALRULE: treats 1 + 10 as just 10)
  - Hundreds: 3 becomes 2 after decrement
  - Result: 231 instead of 232

Network location: ADD TEN procedure
"""

from .problem_generator import BorrowInto1Equals10ProblemGenerator
from .malrule_algorithm import BorrowInto1Equals10Malrule
from .correct_algorithm import SubtractionCorrectAlgorithm

__all__ = [
    'BorrowInto1Equals10ProblemGenerator',
    'BorrowInto1Equals10Malrule',
    'SubtractionCorrectAlgorithm',
]
