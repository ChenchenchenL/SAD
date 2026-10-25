"""
Write-Carry-Forget-Units Malrule

When adding columns that require a carry, the student writes the carry digit
and forgets to write the units digit in the answer.

Example: 87 + 93 = 11 (Correct: 180)
    - 7+3=10, writes 1 (the carry), forgets the 0
    - 8+9=17, writes 1 (the carry), forgets the 7
    - Result: 11

"""

from .problem_generator import WriteCarryForgetUnitsProblemGenerator
from .malrule_algorithm import WriteCarryForgetUnitsMalrule
from .correct_algorithm import AdditionCorrectAlgorithm

__all__ = [
    'WriteCarryForgetUnitsProblemGenerator',
    'WriteCarryForgetUnitsMalrule',
    'AdditionCorrectAlgorithm',
]
