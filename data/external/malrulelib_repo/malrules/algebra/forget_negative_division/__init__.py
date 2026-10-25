"""
Forget-Negative-Division Malrule

Students forget to flip inequality sign when dividing/multiplying by negative.

Example: -2x < 6 → Student: x < -3 ❌
Correct: x > -3 ✓ (flip sign when dividing by -2)

Common cases:
- -3x > 9 → Student thinks x > -3 (should be x < -3)
- -x ≤ 5 → Student thinks x ≤ -5 (should be x ≥ -5)
- Dividing: x/-2 > 4 → Student thinks x > -8 (should be x < -8)

"""

from .problem_generator import ForgetNegativeDivisionProblemGenerator
from .malrule_algorithm import ForgetNegativeDivisionMalrule
from .correct_algorithm import InequalitySolvingCorrectAlgorithm

__all__ = [
    'ForgetNegativeDivisionProblemGenerator',
    'ForgetNegativeDivisionMalrule',
    'InequalitySolvingCorrectAlgorithm'
]
