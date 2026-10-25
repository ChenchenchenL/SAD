"""
Distribute-Over-Non-Distributive Malrule

Students incorrectly apply distributive property to non-distributive operations.

Example: (x+3)² → Student thinks: x² + 3² = x² + 9 ❌
Correct: (x+3)² = x² + 6x + 9 ✓

Common cases:
- Squaring binomials: (a+b)² ≠ a² + b²
- Square roots: √(a+b) ≠ √a + √b
- Exponentiation: (ab)ⁿ ≠ aⁿbⁿ (wrong direction)

"""

from .problem_generator import DistributeOverNonDistributiveProblemGenerator
from .malrule_algorithm import DistributeOverNonDistributiveMalrule
from .correct_algorithm import AlgebraExpansionCorrectAlgorithm

__all__ = [
    'DistributeOverNonDistributiveProblemGenerator',
    'DistributeOverNonDistributiveMalrule',
    'AlgebraExpansionCorrectAlgorithm'
]
