"""
Same-Perimeter-Same-Area Malrule

Students think same perimeter means same area.

Example: Compare 4×1 rectangle (perimeter 10) with 3×2 rectangle (perimeter 10)
Student: "Same perimeter = same area, so both have area 4" ✗
Correct: 4×1 has area 4, 3×2 has area 6 ✓

Fundamental geometry misconception - confuses perimeter with area.

"""

from .problem_generator import SamePerimeterSameAreaProblemGenerator
from .malrule_algorithm import SamePerimeterSameAreaMalrule
from .correct_algorithm import AreaCalculationCorrectAlgorithm

__all__ = [
    'SamePerimeterSameAreaProblemGenerator',
    'SamePerimeterSameAreaMalrule',
    'AreaCalculationCorrectAlgorithm'
]
