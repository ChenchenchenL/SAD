"""
Division-Makes-Smaller malrule.

Students incorrectly believe that division always makes numbers smaller.
For example: 4 ÷ 0.5 must be less than 4 (but it's actually 8).
"""

from .problem_generator import DivisionWithDecimalsProblemGenerator
from .malrule_algorithm import DivisionMakesSmallerMalrule
from .correct_algorithm import DivisionCorrectAlgorithm

# Alias for generate_step_samples.py compatibility
DivisionMakesSmallerProblemGenerator = DivisionWithDecimalsProblemGenerator
DivisionMakesSmallerCorrectAlgorithm = DivisionCorrectAlgorithm

__all__ = [
    'DivisionWithDecimalsProblemGenerator',
    'DivisionMakesSmallerMalrule',
    'DivisionCorrectAlgorithm',
    'DivisionMakesSmallerProblemGenerator',  # Alias
    'DivisionMakesSmallerCorrectAlgorithm',  # Alias
]
