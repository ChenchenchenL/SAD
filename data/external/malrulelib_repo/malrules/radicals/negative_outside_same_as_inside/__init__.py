"""
Negative-Outside-Same-As-Inside Malrule

Students confuse -√4 with √-4. They think -√4 has no real solution
(confusing it with √-4, which is undefined in real numbers).
"""

from .problem_generator import NegativeOutsideSameAsInsideProblemGenerator
from .malrule_algorithm import NegativeOutsideSameAsInsideMalrule
from .correct_algorithm import NegativeSquareRootCorrectAlgorithm

__all__ = [
    'NegativeOutsideSameAsInsideProblemGenerator',
    'NegativeOutsideSameAsInsideMalrule',
    'NegativeSquareRootCorrectAlgorithm',
]
