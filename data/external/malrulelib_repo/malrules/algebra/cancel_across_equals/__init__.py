"""
Cancel-Across-Equals Malrule

Students cancel matching terms from both sides without performing the operation.

Example: 2x = x + 5 → Student "cancels" x: 2 = 5 ✗ (should be x = 5)

Students treat equations like fractions, crossing out matching terms instead of
subtracting them properly from both sides.

"""

from .problem_generator import CancelAcrossEqualsProblemGenerator
from .malrule_algorithm import CancelAcrossEqualsMalrule
from .correct_algorithm import LinearEquationCorrectAlgorithm

__all__ = [
    'CancelAcrossEqualsProblemGenerator',
    'CancelAcrossEqualsMalrule',
    'LinearEquationCorrectAlgorithm'
]
