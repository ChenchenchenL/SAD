"""
Alignment-Error-In-Multi-Digit malrule.

Students misalign partial products during multi-digit multiplication.
When multiplying by the tens digit, they don't shift the partial product
one place to the left.
"""

from .problem_generator import AlignmentErrorProblemGenerator
from .malrule_algorithm import AlignmentErrorMalrule
from .correct_algorithm import MultiDigitMultiplicationCorrectAlgorithm

# Alias for generate_step_samples.py compatibility
AlignmentErrorInMultiDigitProblemGenerator = AlignmentErrorProblemGenerator
AlignmentErrorInMultiDigitMalrule = AlignmentErrorMalrule
AlignmentErrorInMultiDigitCorrectAlgorithm = MultiDigitMultiplicationCorrectAlgorithm

__all__ = [
    'AlignmentErrorProblemGenerator',
    'AlignmentErrorMalrule',
    'MultiDigitMultiplicationCorrectAlgorithm',
    'AlignmentErrorInMultiDigitProblemGenerator',  # Alias
    'AlignmentErrorInMultiDigitMalrule',  # Alias
    'AlignmentErrorInMultiDigitCorrectAlgorithm',  # Alias
]
