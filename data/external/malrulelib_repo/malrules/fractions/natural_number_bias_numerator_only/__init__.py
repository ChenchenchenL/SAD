"""
Natural-Number-Bias-Numerator-Only malrule.

Students compare fractions by looking at numerators only, ignoring denominators.
For example: 3/4 < 5/8 because 3 < 5.
"""

from .problem_generator import NaturalNumberBiasNumeratorOnlyProblemGenerator
from .malrule_algorithm import NaturalNumberBiasNumeratorOnlyMalrule
from .correct_algorithm import FractionComparisonCorrectAlgorithm

__all__ = [
    'NaturalNumberBiasNumeratorOnlyProblemGenerator',
    'NaturalNumberBiasNumeratorOnlyMalrule',
    'FractionComparisonCorrectAlgorithm',
]
