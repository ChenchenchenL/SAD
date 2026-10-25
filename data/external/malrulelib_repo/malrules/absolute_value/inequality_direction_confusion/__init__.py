"""
Inequality-Direction-Confusion Malrule

Student doesn't distinguish between less than and greater than cases in absolute value inequalities.
Example: |x| > 3 → Student incorrectly writes -3 < x < 3 (should be x < -3 OR x > 3)
"""

from .problem_generator import InequalityDirectionConfusionProblemGenerator
from .malrule_algorithm import InequalityDirectionConfusionMalrule
from .correct_algorithm import AbsoluteValueInequalityCorrectAlgorithm

__all__ = [
    'InequalityDirectionConfusionProblemGenerator',
    'InequalityDirectionConfusionMalrule',
    'AbsoluteValueInequalityCorrectAlgorithm'
]
