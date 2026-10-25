"""
Divide-One-Term-Only malrule.

Students incorrectly apply division to only one term instead of the
entire side of an equation.
For example: 2x + 4 = 10, dividing by 2 gives x + 4 = 5 (WRONG!)
Should be: x + 2 = 5
"""

from .problem_generator import TwoStepEquationProblemGenerator
from .malrule_algorithm import DivideOneTermOnlyMalrule
from .correct_algorithm import TwoStepEquationCorrectAlgorithm

# Alias for generate_step_samples.py compatibility
DivideOneTermOnlyProblemGenerator = TwoStepEquationProblemGenerator
DivideOneTermOnlyCorrectAlgorithm = TwoStepEquationCorrectAlgorithm

__all__ = [
    'TwoStepEquationProblemGenerator',
    'DivideOneTermOnlyMalrule',
    'TwoStepEquationCorrectAlgorithm',
    'DivideOneTermOnlyProblemGenerator',  # Alias
    'DivideOneTermOnlyCorrectAlgorithm',  # Alias
]
