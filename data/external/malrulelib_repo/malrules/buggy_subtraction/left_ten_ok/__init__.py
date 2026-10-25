"""
Left-Ten-OK malrule (variant of BORROW/FROM/ZERO).

The student changes 0 to 9 without further borrowing UNLESS the 0 is part
of a 10 in the left part of the top number.

Example: 803 - 508 = 395 (correct: 295)
  - Ones: 3 < 8, need to borrow from tens (0)
  - The 0 is NOT part of "10" at leftmost position
  - Bug: Change 0 to 9 without borrowing from 8
  - Tens: 9 - 0 = 9
  - Hundreds: 8 - 5 = 3
  - Result: 395 (WRONG)

But for 1003 - 508 = 495 (correct: 495)
  - The "10" is at the leftmost position, so student handles it correctly

Frequency: 50 students (combined with BORROW/FROM/ZERO)
Network location: ZERO procedure (special case)
"""

from .problem_generator import LeftTenOkProblemGenerator
from .malrule_algorithm import LeftTenOkMalrule
from .correct_algorithm import SubtractionCorrectAlgorithm

__all__ = [
    'LeftTenOkProblemGenerator',
    'LeftTenOkMalrule',
    'SubtractionCorrectAlgorithm',
]
