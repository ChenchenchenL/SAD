"""
Square-Root-Equals-Plus-Minus Malrule

Students believe √16 = ±4 instead of √16 = 4 (always positive).

Example: √16 = ±4 ✗ (should be √16 = 4 only)

Students confuse the square root function with solving x² = 16.

"""

from .problem_generator import SquareRootEqualsPlusMinusProblemGenerator
from .malrule_algorithm import SquareRootEqualsPlusMinusMalrule
from .correct_algorithm import SquareRootCorrectAlgorithm

__all__ = [
    'SquareRootEqualsPlusMinusProblemGenerator',
    'SquareRootEqualsPlusMinusMalrule',
    'SquareRootCorrectAlgorithm'
]
