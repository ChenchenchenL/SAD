"""
Swap-Ratios-Or-Units Malrule

Students set up proportions with swapped or inverted ratios/units.

Example: If 3 apples cost $6, how much do 5 apples cost?
Student: 3/5 = 6/x → x = 10 ✗
Correct: 3/6 = 5/x → x = 10 ✓ (but correct setup is 3/6 = 5/x → x = 10)

Actually student gets LUCKY sometimes, or sets up incorrectly and gets wrong answer.

Better example: 2 pounds for $3, how much for 5 pounds?
Student: 2/5 = 3/x → x = 7.5 ✗
Correct: 2/3 = 5/x → x = 7.5 ✓

Proportion setup error - wrong positions in ratio equation.

"""

from .problem_generator import SwapRatiosOrUnitsProblemGenerator
from .malrule_algorithm import SwapRatiosOrUnitsMalrule
from .correct_algorithm import ProportionSetupCorrectAlgorithm

__all__ = [
    'SwapRatiosOrUnitsProblemGenerator',
    'SwapRatiosOrUnitsMalrule',
    'ProportionSetupCorrectAlgorithm'
]
