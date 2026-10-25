"""
Slope-Is-Delta-X-Over-Delta-Y Malrule

Students invert the slope formula, calculating Δx/Δy instead of Δy/Δx.

Example: Points (2,3) and (5,11)
Student: slope = (5-2)/(11-3) = 3/8 ✗
Correct: slope = (11-3)/(5-2) = 8/3 ✓

Common slope formula inversion error.

"""

from .problem_generator import SlopeIsDeltaXOverDeltaYProblemGenerator
from .malrule_algorithm import SlopeIsDeltaXOverDeltaYMalrule
from .correct_algorithm import SlopeCalculationCorrectAlgorithm

__all__ = [
    'SlopeIsDeltaXOverDeltaYProblemGenerator',
    'SlopeIsDeltaXOverDeltaYMalrule',
    'SlopeCalculationCorrectAlgorithm'
]
