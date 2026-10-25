"""
Inverted-Conversion-Factor Malrule

Students set up conversion fraction upside down.

Example: Convert 24 inches to feet
Student: 24 × (12 in / 1 ft) = 288 ✗
Correct: 24 × (1 ft / 12 in) = 2 ft ✓

Dimensional analysis error - inverts the conversion fraction.

"""

from .problem_generator import InvertedConversionFactorProblemGenerator
from .malrule_algorithm import InvertedConversionFactorMalrule
from .correct_algorithm import UnitConversionCorrectAlgorithm

__all__ = [
    'InvertedConversionFactorProblemGenerator',
    'InvertedConversionFactorMalrule',
    'UnitConversionCorrectAlgorithm'
]
