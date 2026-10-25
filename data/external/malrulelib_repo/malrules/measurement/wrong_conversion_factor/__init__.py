"""
Wrong-Conversion-Factor malrule.

Students use incorrect (often round number) conversion factors.
For example: 1 foot = 10 inches, 1 km = 100 meters, 1 hour = 100 minutes.
"""

from .problem_generator import WrongConversionFactorProblemGenerator
from .malrule_algorithm import WrongConversionFactorMalrule
from .correct_algorithm import UnitConversionCorrectAlgorithm

__all__ = [
    'WrongConversionFactorProblemGenerator',
    'WrongConversionFactorMalrule',
    'UnitConversionCorrectAlgorithm',
]
