"""
Distribute-Exponent-Over-Addition Malrule

Student incorrectly distributes exponents over addition: (a+b)^n = a^n + b^n
Example: (2+3)² = 2² + 3² = 4 + 9 = 13 (instead of 5² = 25)
"""

from .problem_generator import DistributeExponentOverAdditionProblemGenerator
from .malrule_algorithm import DistributeExponentOverAdditionMalrule
from .correct_algorithm import ExponentOverSumCorrectAlgorithm

__all__ = [
    'DistributeExponentOverAdditionProblemGenerator',
    'DistributeExponentOverAdditionMalrule',
    'ExponentOverSumCorrectAlgorithm'
]
