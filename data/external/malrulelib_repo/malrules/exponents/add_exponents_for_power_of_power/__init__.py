"""
Add-Exponents-For-Power-Of-Power malrule implementation.

Students think: (a³)⁵ = a⁸ instead of (a³)⁵ = a¹⁵
"""

from .problem_generator import AddExponentsForPowerOfPowerProblemGenerator
from .malrule_algorithm import AddExponentsForPowerOfPowerMalrule
from .correct_algorithm import PowerOfPowerCorrectAlgorithm

__all__ = [
    'AddExponentsForPowerOfPowerProblemGenerator',
    'AddExponentsForPowerOfPowerMalrule',
    'PowerOfPowerCorrectAlgorithm'
]
