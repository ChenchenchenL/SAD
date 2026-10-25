"""
Strict-Left-To-Right malrule for order of operations.

Students evaluate expressions strictly from left to right, ignoring
operator precedence rules (PEMDAS/BODMAS).
For example: 3 + 4 × 2 = 14 (wrong, should be 11).
"""

from .problem_generator import OrderOfOperationsProblemGenerator
from .malrule_algorithm import StrictLeftToRightMalrule
from .correct_algorithm import OrderOfOperationsCorrectAlgorithm

# Alias for generate_step_samples.py compatibility
StrictLeftToRightProblemGenerator = OrderOfOperationsProblemGenerator
StrictLeftToRightCorrectAlgorithm = OrderOfOperationsCorrectAlgorithm

__all__ = [
    'OrderOfOperationsProblemGenerator',
    'StrictLeftToRightMalrule',
    'OrderOfOperationsCorrectAlgorithm',
    'StrictLeftToRightProblemGenerator',  # Alias
    'StrictLeftToRightCorrectAlgorithm',  # Alias
]
