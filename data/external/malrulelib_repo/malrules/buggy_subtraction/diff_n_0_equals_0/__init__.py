"""
DIFF/N-0=0 Malrule

Whenever the bottom digit (subtrahend) in a column is 0, the student writes 0
in the answer instead of the top digit. The student incorrectly believes N-0=0.

Example: 403 - 208 = 105 (Correct: 195)
  - Ones: 3-8 requires borrow... 13-8=5 (student does correctly)
  - Tens: 9-0, student writes 0 (BUG!) instead of 9
  - Hundreds: 3-2=1

"""

from .problem_generator import DiffN0Equals0ProblemGenerator
from .malrule_algorithm import DiffN0Equals0Malrule
from .correct_algorithm import SubtractionCorrectAlgorithm

__all__ = [
    'DiffN0Equals0ProblemGenerator',
    'DiffN0Equals0Malrule',
    'SubtractionCorrectAlgorithm',
]
