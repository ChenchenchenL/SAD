"""
Same-Area-Same-Perimeter Malrule

Students think same area means same perimeter.

Example: Compare 4×2 rectangle (area 8) with 8×1 rectangle (area 8)
Student: "Same area = same perimeter" ✗
Correct: 4×2 has perimeter 12, 8×1 has perimeter 18 ✓

Fundamental geometry misconception - confuses area with perimeter (inverse error).

"""

from .problem_generator import SameAreaSamePerimeterProblemGenerator
from .malrule_algorithm import SameAreaSamePerimeterMalrule
from .correct_algorithm import PerimeterCalculationCorrectAlgorithm

__all__ = [
    'SameAreaSamePerimeterProblemGenerator',
    'SameAreaSamePerimeterMalrule',
    'PerimeterCalculationCorrectAlgorithm'
]
