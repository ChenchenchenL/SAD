"""
Negative-Swaps-Operation Malrule

Students think negative sign changes the operation (addition ↔ subtraction).

Example: 5 + (-3) → Student thinks: "negative changes + to -" so 5 - 3 = 2 ✓ (accidentally correct!)
But: 5 - (-3) → Student thinks: "negative changes - to +" so 5 + 3 = 8 ✗ (should be 8, but for wrong reason!)

Common cases:
- Student treats negative as operation swap, not value
- Gets some answers right by accident
- Fundamental conceptual confusion

"""

from .problem_generator import NegativeSwapsOperationProblemGenerator
from .malrule_algorithm import NegativeSwapsOperationMalrule
from .correct_algorithm import NegativeArithmeticCorrectAlgorithm

__all__ = [
    'NegativeSwapsOperationProblemGenerator',
    'NegativeSwapsOperationMalrule',
    'NegativeArithmeticCorrectAlgorithm'
]
