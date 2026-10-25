"""
Column-Mimics-Addition Malrule

The student's multiplication algorithm mimics the column behavior of addition,
multiplying column by column instead of digit by digit. Additionally, the student
applies the WRITE/CARRY/FORGET/UNITS bug: when a column product exceeds 9, they
write the carry digit (tens place) instead of the units digit.

Example: 68 x 46 = 24 (Correct: 3128)
    - Column 1: 8 x 6 = 48, writes 4 (carry), forgets 8 (units)
    - Column 2: 6 x 4 = 24, writes 2 (carry), forgets 4 (units)
    - Result: 24

More examples from Brown & Burton (1978):
    - 734 x 37 = 792 (Correct: 27,158)
    - 543 x 206 = 141 (Correct: 111,858)
    - 758 x 296 = 144 (Correct: 224,368)
    - 2764 x 53 = 2731 (Correct: 146,492)

"""

from .problem_generator import ColumnMimicsAdditionProblemGenerator
from .malrule_algorithm import ColumnMimicsAdditionMalrule
from .correct_algorithm import MultiplicationCorrectAlgorithm

__all__ = [
    'ColumnMimicsAdditionProblemGenerator',
    'ColumnMimicsAdditionMalrule',
    'MultiplicationCorrectAlgorithm',
]
