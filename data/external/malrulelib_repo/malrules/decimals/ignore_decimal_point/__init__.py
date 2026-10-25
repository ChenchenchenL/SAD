"""
Ignore-Decimal-Point Malrule

Students ignore the decimal point and treat numbers as whole numbers.

Example: 3.5 + 2.3 → Student sees 35 + 23 = 58 ❌
Correct: 3.5 + 2.3 = 5.8 ✓

Common cases:
- Addition: 1.2 + 3.4 → 12 + 34 = 46
- Multiplication: 2.5 × 3 → 25 × 3 = 75
- Subtraction: 4.8 - 1.2 → 48 - 12 = 36

"""

from .problem_generator import IgnoreDecimalPointProblemGenerator
from .malrule_algorithm import IgnoreDecimalPointMalrule
from .correct_algorithm import DecimalArithmeticCorrectAlgorithm

__all__ = [
    'IgnoreDecimalPointProblemGenerator',
    'IgnoreDecimalPointMalrule',
    'DecimalArithmeticCorrectAlgorithm'
]
