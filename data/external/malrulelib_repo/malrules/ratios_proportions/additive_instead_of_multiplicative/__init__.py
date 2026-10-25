"""
Additive-Instead-Of-Multiplicative Malrule

Students use addition to scale ratios instead of multiplication.

Example: Scale ratio 2:3 by factor 4
Student: 2+4=6, 3+4=7 → 6:7 ✗
Correct: 2×4=8, 3×4=12 → 8:12 ✓

Core additive vs multiplicative reasoning gap.

"""

from .problem_generator import AdditiveInsteadOfMultiplicativeProblemGenerator
from .malrule_algorithm import AdditiveInsteadOfMultiplicativeMalrule
from .correct_algorithm import RatioScalingCorrectAlgorithm

__all__ = [
    'AdditiveInsteadOfMultiplicativeProblemGenerator',
    'AdditiveInsteadOfMultiplicativeMalrule',
    'RatioScalingCorrectAlgorithm'
]
