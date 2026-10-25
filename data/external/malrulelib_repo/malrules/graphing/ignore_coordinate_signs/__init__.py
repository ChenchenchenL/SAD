"""
Ignore-Coordinate-Signs Malrule

Students ignore negative signs in coordinates, treating all values as positive.

Example: Plot point (-3, 4)
Student: Plots (3, 4) instead - ignores the negative sign ✗
Correct: (-3, 4) means 3 left, 4 up ✓

Another example: Plot point (-5, -2)
Student: Plots (5, 2) - uses absolute values ✗
Correct: (-5, -2) means 5 left, 2 down ✓

Fundamental misconception about negative numbers on coordinate plane.

"""

from .problem_generator import IgnoreCoordinateSignsProblemGenerator
from .malrule_algorithm import IgnoreCoordinateSignsMalrule
from .correct_algorithm import CoordinatePlottingWithSignsCorrectAlgorithm

__all__ = [
    'IgnoreCoordinateSignsProblemGenerator',
    'IgnoreCoordinateSignsMalrule',
    'CoordinatePlottingWithSignsCorrectAlgorithm'
]
