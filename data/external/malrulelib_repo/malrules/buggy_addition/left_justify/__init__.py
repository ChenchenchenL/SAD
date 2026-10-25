"""
Left-Justify Malrule

When adding numbers of different digit lengths, the student aligns them
on the left side instead of the right side (place value alignment).
This causes digits to be added in the wrong columns.

Example: 23 + 456
- Correct (right-justified): 23 + 456 = 479
- Malrule (left-justified): 230 + 456 = 686 (23 treated as 230)

"""

from .problem_generator import LeftJustifyProblemGenerator
from .malrule_algorithm import LeftJustifyMalrule
from .correct_algorithm import AdditionCorrectAlgorithm

__all__ = [
    'LeftJustifyProblemGenerator',
    'LeftJustifyMalrule',
    'AdditionCorrectAlgorithm',
]
