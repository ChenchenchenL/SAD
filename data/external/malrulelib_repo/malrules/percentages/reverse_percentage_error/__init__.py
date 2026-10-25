"""
Reverse-Percentage-Error Malrule

Students incorrectly believe percentage relationships are symmetric/reversible.

Example: "20 is 50% of 40" → Student thinks "40 is 50% of 20" ❌
Correct: 40 is 200% of 20 ✓

Common cases:
- If A is 50% of B, student thinks B is 50% of A
- If A is 25% of B, student thinks B is 25% of A
- Reversibility confusion in percentage relationships

"""

from .problem_generator import ReversePercentageErrorProblemGenerator
from .malrule_algorithm import ReversePercentageErrorMalrule
from .correct_algorithm import PercentageRelationshipCorrectAlgorithm

__all__ = [
    'ReversePercentageErrorProblemGenerator',
    'ReversePercentageErrorMalrule',
    'PercentageRelationshipCorrectAlgorithm'
]
