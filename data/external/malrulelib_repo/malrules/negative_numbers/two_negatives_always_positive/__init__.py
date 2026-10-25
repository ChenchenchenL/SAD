"""
Two-Negatives-Always-Positive malrule for negative number operations.

Students incorrectly apply the multiplication rule "negative times negative equals positive"
to subtraction operations. For example: -5 - 6 = 11 (incorrect, should be -11).
"""

from .problem_generator import NegativeSubtractionProblemGenerator
from .malrule_algorithm import TwoNegativesAlwaysPositiveMalrule
from .correct_algorithm import NegativeSubtractionCorrectAlgorithm

# Alias for generate_step_samples.py compatibility
TwoNegativesAlwaysPositiveProblemGenerator = NegativeSubtractionProblemGenerator
TwoNegativesAlwaysPositiveCorrectAlgorithm = NegativeSubtractionCorrectAlgorithm

__all__ = [
    'NegativeSubtractionProblemGenerator',
    'TwoNegativesAlwaysPositiveMalrule',
    'NegativeSubtractionCorrectAlgorithm',
    'TwoNegativesAlwaysPositiveProblemGenerator',  # Alias
    'TwoNegativesAlwaysPositiveCorrectAlgorithm',  # Alias
]
