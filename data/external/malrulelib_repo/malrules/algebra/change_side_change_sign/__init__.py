"""
Change-Side-Change-Sign malrule.

Students incorrectly believe that when moving a term from one side
of an equation to the other, you simply change its sign.
For example: x + 3 = 7 becomes x = 7 + 3 (WRONG!)
"""

from .problem_generator import LinearEquationProblemGenerator
from .malrule_algorithm import ChangeSideChangeSignMalrule
from .correct_algorithm import LinearEquationCorrectAlgorithm

# Alias for generate_step_samples.py compatibility
ChangeSideChangeSignProblemGenerator = LinearEquationProblemGenerator
ChangeSideChangeSignCorrectAlgorithm = LinearEquationCorrectAlgorithm

__all__ = [
    'LinearEquationProblemGenerator',
    'ChangeSideChangeSignMalrule',
    'LinearEquationCorrectAlgorithm',
    'ChangeSideChangeSignProblemGenerator',  # Alias
    'ChangeSideChangeSignCorrectAlgorithm',  # Alias
]
