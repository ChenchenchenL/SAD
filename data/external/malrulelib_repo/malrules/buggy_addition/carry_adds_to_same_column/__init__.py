"""
Carry-Adds-To-Same-Column Malrule

If a column adds to more than 9, the units digit and the carry digit are added
together and the result is written as the answer for that column. The carry is
added back into the same column rather than carried to the next column.

Example: 17 + 5 = 13 (correct: 22)
  - 7+5=12, student adds 1+2=3, writes 3 in ones column
  - 1+0=1, writes 1 in tens column
  - Result: 13 (instead of 22)

Example: 45 + 38 = 74 (correct: 83)
  - 5+8=13, student adds 1+3=4, writes 4 in ones column
  - 4+3=7, writes 7 in tens column
  - Result: 74 (instead of 83)

Note: Could arise from Method 2 (left-to-right) with carry written under same column
"""

from .problem_generator import CarryAddsToSameColumnProblemGenerator
from .malrule_algorithm import CarryAddsToSameColumnMalrule
from .correct_algorithm import AdditionCorrectAlgorithm

__all__ = [
    'CarryAddsToSameColumnProblemGenerator',
    'CarryAddsToSameColumnMalrule',
    'AdditionCorrectAlgorithm',
]
