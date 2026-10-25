"""
Ignore-Denominators malrule.

Students operate only on numerators, ignoring denominators entirely.
For example: 2/3 + 1/5 → Student computes 2+1=3, treats result as 3 or 3/3.
"""

from .problem_generator import IgnoreDenominatorsProblemGenerator
from .malrule_algorithm import IgnoreDenominatorsMalrule
from .correct_algorithm import FractionCorrectAlgorithm

__all__ = [
    'IgnoreDenominatorsProblemGenerator',
    'IgnoreDenominatorsMalrule',
    'FractionCorrectAlgorithm',
]
