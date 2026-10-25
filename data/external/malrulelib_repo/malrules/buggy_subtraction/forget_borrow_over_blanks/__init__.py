"""
FORGET/BORROW/OVER/BLANKS Malrule

When the top number (minuend) has fewer digits than the bottom number (subtrahend),
the student forgets to borrow over blank columns. The student treats missing digits
in the minuend as if they were 0s that don't participate in borrowing.

Example: 85 - 127
  - Correct approach: Treat 85 as 085, recognize that 0-1 in hundreds requires
    borrowing which is impossible (result would be negative)
  - Malrule: Student subtracts column by column:
    - Ones: 5-7 requires borrow, so 15-7=8 (with borrow from tens)
    - Tens: 7-2=5 (after decrement: 8-1=7, then 7-2=5)
    - Hundreds: blank-1 = treats as nothing or 0-1=1 (smaller from larger)
    - Result: 158 or similar incorrect answer

Example: 42 - 156
  - Student may get 42-156 = 126 or another wrong answer
  - Correct: This would be -114 (negative), or in unsigned context, invalid

The key error is in the COLUMN SEQUENCE procedure where the student fails to
recognize that borrowing must continue leftward even when the minuend has no
digits in that position.

Network location: COLUMN SEQUENCE procedure
"""

from .problem_generator import ForgetBorrowOverBlanksProblemGenerator
from .malrule_algorithm import ForgetBorrowOverBlanksMalrule
from .correct_algorithm import SubtractionCorrectAlgorithm

__all__ = [
    'ForgetBorrowOverBlanksProblemGenerator',
    'ForgetBorrowOverBlanksMalrule',
    'SubtractionCorrectAlgorithm',
]
