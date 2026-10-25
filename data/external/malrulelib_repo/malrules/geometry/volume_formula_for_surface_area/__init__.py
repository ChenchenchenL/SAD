"""
Volume-Formula-For-Surface-Area Malrule

Students use volume formula (V = lwh) when asked for surface area.

Example: Rectangular prism 3×4×5
Student: Uses V = lwh → 3×4×5 = 60 ✗
Correct: Uses SA = 2(lw + lh + wh) → 2(12 + 15 + 20) = 94 ✓

Common formula confusion in 3D geometry.

"""

from .problem_generator import VolumeFormulaForSurfaceAreaProblemGenerator
from .malrule_algorithm import VolumeFormulaForSurfaceAreaMalrule
from .correct_algorithm import SurfaceAreaCalculationCorrectAlgorithm

__all__ = [
    'VolumeFormulaForSurfaceAreaProblemGenerator',
    'VolumeFormulaForSurfaceAreaMalrule',
    'SurfaceAreaCalculationCorrectAlgorithm'
]
