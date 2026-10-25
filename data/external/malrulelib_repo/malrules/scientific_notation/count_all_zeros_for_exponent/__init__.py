"""
Count-All-Zeros-For-Exponent malrule.

Students count ALL zeros in a number when determining the exponent for
scientific notation, without considering their placement (leading, trailing,
or between significant digits).
"""

from .problem_generator import CountZerosProblemGenerator
from .malrule_algorithm import CountAllZerosMalrule
from .correct_algorithm import ScientificNotationCorrectAlgorithm

# Alias for generate_step_samples.py compatibility
CountAllZerosForExponentProblemGenerator = CountZerosProblemGenerator
CountAllZerosForExponentMalrule = CountAllZerosMalrule
CountAllZerosForExponentCorrectAlgorithm = ScientificNotationCorrectAlgorithm

__all__ = [
    'CountZerosProblemGenerator',
    'CountAllZerosMalrule',
    'ScientificNotationCorrectAlgorithm',
    'CountAllZerosForExponentProblemGenerator',  # Alias
    'CountAllZerosForExponentMalrule',  # Alias
    'CountAllZerosForExponentCorrectAlgorithm',  # Alias
]
