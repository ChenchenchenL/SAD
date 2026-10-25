"""
Multiplication-Before-Division-Always malrule.

Students incorrectly believe that multiplication must always be performed
before division, even when they appear left-to-right.
For example: 6 ÷ 2 × 3 = 6 ÷ 6 = 1 (WRONG! should be 3 × 3 = 9)
"""

from .problem_generator import MultiplicationDivisionOrderProblemGenerator
from .malrule_algorithm import MultiplicationBeforeDivisionAlwaysMalrule
from .correct_algorithm import OrderOfOperationsCorrectAlgorithm

# Alias for generate_step_samples.py compatibility
MultiplicationBeforeDivisionAlwaysProblemGenerator = MultiplicationDivisionOrderProblemGenerator
MultiplicationBeforeDivisionAlwaysCorrectAlgorithm = OrderOfOperationsCorrectAlgorithm

__all__ = [
    'MultiplicationDivisionOrderProblemGenerator',
    'MultiplicationBeforeDivisionAlwaysMalrule',
    'OrderOfOperationsCorrectAlgorithm',
    'MultiplicationBeforeDivisionAlwaysProblemGenerator',  # Alias
    'MultiplicationBeforeDivisionAlwaysCorrectAlgorithm',  # Alias
]
