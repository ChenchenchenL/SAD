"""
Divide-Larger-By-Smaller-Always malrule.

Students believe division must always be larger ÷ smaller, thinking
problems like 4 ÷ 6 are impossible or should be reversed to 6 ÷ 4.
"""

from .problem_generator import DivideLargerBySmallerAlwaysProblemGenerator
from .malrule_algorithm import DivideLargerBySmallerAlwaysMalrule
from .correct_algorithm import DivisionCorrectAlgorithm

__all__ = [
    'DivideLargerBySmallerAlwaysProblemGenerator',
    'DivideLargerBySmallerAlwaysMalrule',
    'DivisionCorrectAlgorithm',
]
