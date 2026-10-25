"""
Multiplication-Makes-Bigger malrule.

Students incorrectly believe that multiplication always produces a result
larger than both factors. For example: 0.5 × 0.2 = 0.1, but students expect
a result larger than 0.5.
"""

from .problem_generator import MultiplicationProblemGenerator
from .malrule_algorithm import MultiplicationMakesBiggerMalrule
from .correct_algorithm import MultiplicationCorrectAlgorithm

# Alias for generate_step_samples.py compatibility
MultiplicationMakesBiggerProblemGenerator = MultiplicationProblemGenerator
MultiplicationMakesBiggerCorrectAlgorithm = MultiplicationCorrectAlgorithm

__all__ = [
    'MultiplicationProblemGenerator',
    'MultiplicationMakesBiggerMalrule',
    'MultiplicationCorrectAlgorithm',
    'MultiplicationMakesBiggerProblemGenerator',  # Alias
    'MultiplicationMakesBiggerCorrectAlgorithm',  # Alias
]
