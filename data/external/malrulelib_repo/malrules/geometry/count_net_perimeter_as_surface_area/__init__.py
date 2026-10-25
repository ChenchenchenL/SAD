"""
Count-Net-Perimeter-As-Surface-Area Malrule

Students confuse perimeter with area when working with 3D nets.
When given a net (unfolded 3D shape), they calculate the perimeter around
the outside of the net instead of calculating the surface area by finding
the area of each face and adding them.

Example: Cube with side 3
Student: Measures net perimeter → 12×3 = 36 (if cross-shaped net) ✗
Correct: Calculates surface area → 6×(3²) = 54 ✓

Common 2D/3D confusion in geometry.

"""

from .problem_generator import CountNetPerimeterAsSurfaceAreaProblemGenerator
from .malrule_algorithm import CountNetPerimeterAsSurfaceAreaMalrule
from .correct_algorithm import NetSurfaceAreaCorrectAlgorithm

__all__ = [
    'CountNetPerimeterAsSurfaceAreaProblemGenerator',
    'CountNetPerimeterAsSurfaceAreaMalrule',
    'NetSurfaceAreaCorrectAlgorithm'
]
