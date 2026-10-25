"""
Carry-Not-Reset Malrule

After determining the carry, the student forgets to reset the "carry register"
to zero and hence the amount carried is accumulated across the columns.

Example: 328 + 917 = 1345 (correct: 1245)
  - 8+7=15, write 5, carry 1
  - 2+1=3, plus carry 1 = 4, but carry NOT reset (still 1)
  - 3+9=12, plus carry 1 (still there!) = 13

"""

from .problem_generator import CarryNotResetProblemGenerator
from .malrule_algorithm import CarryNotResetMalrule
from .correct_algorithm import AdditionCorrectAlgorithm

__all__ = [
    'CarryNotResetProblemGenerator',
    'CarryNotResetMalrule',
    'AdditionCorrectAlgorithm',
]
