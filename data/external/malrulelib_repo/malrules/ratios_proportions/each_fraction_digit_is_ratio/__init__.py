"""
Each-Fraction-Digit-Is-Ratio Malrule

Students treat multi-digit numerators/denominators as separate single-digit ratios.

Example: Simplify 12/34
Student: "1÷3 and 2÷4" → treats as separate ratios
Correct: 12/34 = 6/17 (divide both by GCD of 2)

Another example: 24:36
Student: "2:3 and 4:6" → processes digits independently
Correct: 24:36 = 2:3 (divide both by GCD of 12)

This reflects a fundamental misunderstanding of place value in rational numbers.

"""

from .problem_generator import EachFractionDigitIsRatioProblemGenerator
from .malrule_algorithm import EachFractionDigitIsRatioMalrule
from .correct_algorithm import RatioSimplificationCorrectAlgorithm

__all__ = [
    'EachFractionDigitIsRatioProblemGenerator',
    'EachFractionDigitIsRatioMalrule',
    'RatioSimplificationCorrectAlgorithm'
]
