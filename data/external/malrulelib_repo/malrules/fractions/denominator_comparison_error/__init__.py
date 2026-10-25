"""
Denominator-Comparison-Error malrule.

Students incorrectly believe that a larger denominator means a larger fraction.
For example: 1/4 > 1/3 because 4 > 3.
"""

from .problem_generator import FractionComparisonProblemGenerator
from .malrule_algorithm import DenominatorComparisonErrorMalrule
from .correct_algorithm import FractionComparisonCorrectAlgorithm

# Alias for generate_step_samples.py compatibility
DenominatorComparisonErrorProblemGenerator = FractionComparisonProblemGenerator
DenominatorComparisonErrorCorrectAlgorithm = FractionComparisonCorrectAlgorithm

__all__ = [
    'FractionComparisonProblemGenerator',
    'DenominatorComparisonErrorMalrule',
    'FractionComparisonCorrectAlgorithm',
    'DenominatorComparisonErrorProblemGenerator',  # Alias
    'DenominatorComparisonErrorCorrectAlgorithm',  # Alias
]
