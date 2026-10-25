"""
Addition-Before-Subtraction-Always malrule.

Students incorrectly believe that addition must always be performed
before subtraction, even when they appear left-to-right.
For example: 10 - 3 + 2 = 10 - 5 = 5 (WRONG! should be 7 + 2 = 9)
"""

from .problem_generator import AdditionSubtractionOrderProblemGenerator
from .malrule_algorithm import AdditionBeforeSubtractionAlwaysMalrule
from .correct_algorithm import AddSubOrderCorrectAlgorithm

# Alias for generate_step_samples.py compatibility
AdditionBeforeSubtractionAlwaysProblemGenerator = AdditionSubtractionOrderProblemGenerator
AdditionBeforeSubtractionAlwaysCorrectAlgorithm = AddSubOrderCorrectAlgorithm

__all__ = [
    'AdditionSubtractionOrderProblemGenerator',
    'AdditionBeforeSubtractionAlwaysMalrule',
    'AddSubOrderCorrectAlgorithm',
    'AdditionBeforeSubtractionAlwaysProblemGenerator',  # Alias
    'AdditionBeforeSubtractionAlwaysCorrectAlgorithm',  # Alias
]
