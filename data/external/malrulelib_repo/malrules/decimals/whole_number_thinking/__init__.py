"""
Whole-Number-Thinking malrule for decimals.

Students incorrectly treat decimals like whole numbers, comparing them
by the number of digits or the numerical value after the decimal point.
"""

from .problem_generator import DecimalWholeNumberProblemGenerator
from .malrule_algorithm import WholeNumberThinkingMalrule
from .correct_algorithm import DecimalCorrectAlgorithm

# Alias for generate_step_samples.py compatibility
WholeNumberThinkingProblemGenerator = DecimalWholeNumberProblemGenerator
WholeNumberThinkingCorrectAlgorithm = DecimalCorrectAlgorithm

__all__ = [
    'DecimalWholeNumberProblemGenerator',
    'WholeNumberThinkingMalrule',
    'DecimalCorrectAlgorithm',
    'WholeNumberThinkingProblemGenerator',  # Alias
    'WholeNumberThinkingCorrectAlgorithm',  # Alias
]
