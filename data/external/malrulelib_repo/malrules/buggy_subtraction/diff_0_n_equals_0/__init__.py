"""
Diff-0-N=0 malrule.

When the top digit in a column is 0, students write 0 in the answer instead
of borrowing from the next column to the left. This is the 0-N=0 error
documented in Brown & Burton (1978).

Example: 140 - 21 = 120 (correct: 119)
    - Ones: 0-1, student writes 0 (bug!)
    - Tens: 4-2=2
    - Hundreds: 1-0=1
    Result: 120 instead of 119

Network location: COMPLETE COLUMN procedure
"""

from .problem_generator import Diff0NEquals0ProblemGenerator
from .malrule_algorithm import Diff0NEquals0Malrule
from .correct_algorithm import SubtractionCorrectAlgorithm

__all__ = [
    'Diff0NEquals0ProblemGenerator',
    'Diff0NEquals0Malrule',
    'SubtractionCorrectAlgorithm',
]
