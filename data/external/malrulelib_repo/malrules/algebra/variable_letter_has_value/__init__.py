"""
Variable-Letter-Has-Value Malrule

Students believe variable letters have inherent fixed values.

Example: x + 5 = 12 → Student thinks: "x is 10, so 10 + 5 = 15" ❌
Correct: x = 7 ✓

Common beliefs:
- x always equals 10 (x is tenth letter)
- n always equals 1 (n for "number one")
- a always equals 1 (first letter)
- z always equals 26 (26th letter)

"""

from .problem_generator import VariableLetterHasValueProblemGenerator
from .malrule_algorithm import VariableLetterHasValueMalrule
from .correct_algorithm import AlgebraicEquationCorrectAlgorithm

__all__ = [
    'VariableLetterHasValueProblemGenerator',
    'VariableLetterHasValueMalrule',
    'AlgebraicEquationCorrectAlgorithm'
]
