"""
Distribute-Square-Root-Over-Addition Malrule

Students think √(a²+b²) = a + b (distributing square root over addition)

Example: √(3²+4²)
Student: √(3²+4²) = 3 + 4 = 7 ✗
Correct: √(9+16) = √25 = 5 ✓

Overgeneralization from √(a²) = a, Pythagorean confusion.

"""

from .problem_generator import DistributeSquareRootOverAdditionProblemGenerator
from .malrule_algorithm import DistributeSquareRootOverAdditionMalrule
from .correct_algorithm import SquareRootSimplificationCorrectAlgorithm

__all__ = [
    'DistributeSquareRootOverAdditionProblemGenerator',
    'DistributeSquareRootOverAdditionMalrule',
    'SquareRootSimplificationCorrectAlgorithm'
]
