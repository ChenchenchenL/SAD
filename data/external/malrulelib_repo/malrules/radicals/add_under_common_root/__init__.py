"""
Add-Under-Common-Root Malrule

Students combine separate radicals under one root: √4 + √9 = √(4+9) = √13

Example: Simplify √4 + √9
Student: √(4+9) = √13 ✗
Correct: √4 + √9 = 2 + 3 = 5 ✓

Inverse error of Distribute-Square-Root-Over-Addition.

"""

from .problem_generator import AddUnderCommonRootProblemGenerator
from .malrule_algorithm import AddUnderCommonRootMalrule
from .correct_algorithm import RadicalAdditionCorrectAlgorithm

__all__ = [
    'AddUnderCommonRootProblemGenerator',
    'AddUnderCommonRootMalrule',
    'RadicalAdditionCorrectAlgorithm'
]
