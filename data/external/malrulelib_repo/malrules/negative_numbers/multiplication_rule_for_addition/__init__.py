"""
Multiplication-Rule-For-Addition malrule.

Students incorrectly apply multiplication rules (like "two negatives make
a positive") to addition and subtraction operations with negative numbers.
For example: -3 + (-5) = +8 because "negative plus negative = positive"
"""

from .problem_generator import NegativeAdditionProblemGenerator
from .malrule_algorithm import MultiplicationRuleForAdditionMalrule
from .correct_algorithm import NegativeAdditionCorrectAlgorithm

# Alias for generate_step_samples.py compatibility
MultiplicationRuleForAdditionProblemGenerator = NegativeAdditionProblemGenerator
MultiplicationRuleForAdditionCorrectAlgorithm = NegativeAdditionCorrectAlgorithm

__all__ = [
    'NegativeAdditionProblemGenerator',
    'MultiplicationRuleForAdditionMalrule',
    'NegativeAdditionCorrectAlgorithm',
    'MultiplicationRuleForAdditionProblemGenerator',  # Alias
    'MultiplicationRuleForAdditionCorrectAlgorithm',  # Alias
]
