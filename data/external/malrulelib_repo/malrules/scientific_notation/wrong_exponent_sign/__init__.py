"""
Wrong-Exponent-Sign Malrule

Students use positive exponent when should be negative or vice versa.

Example: Write 0.0045 in scientific notation
Student: 4.5 × 10³ ✗
Correct: 4.5 × 10⁻³ ✓

Direction confusion - doesn't connect decimal movement to exponent sign.

"""

from .problem_generator import WrongExponentSignProblemGenerator
from .malrule_algorithm import WrongExponentSignMalrule
from .correct_algorithm import ScientificNotationCorrectAlgorithm

__all__ = [
    'WrongExponentSignProblemGenerator',
    'WrongExponentSignMalrule',
    'ScientificNotationCorrectAlgorithm'
]
