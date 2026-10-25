"""
Subtract-Across malrule for fraction subtraction.

Students incorrectly subtract numerators and subtract denominators.
For example: 3/4 - 1/2 = 2/2 = 1 (incorrect, should be 1/4).
"""

from .problem_generator import FractionSubtractionProblemGenerator
from .malrule_algorithm import SubtractAcrossMalrule
from .correct_algorithm import FractionSubtractionCorrectAlgorithm

# Alias for generate_step_samples.py compatibility
SubtractAcrossProblemGenerator = FractionSubtractionProblemGenerator
SubtractAcrossCorrectAlgorithm = FractionSubtractionCorrectAlgorithm

__all__ = [
    'FractionSubtractionProblemGenerator',
    'SubtractAcrossMalrule',
    'FractionSubtractionCorrectAlgorithm',
    'SubtractAcrossProblemGenerator',  # Alias
    'SubtractAcrossCorrectAlgorithm',  # Alias
]
