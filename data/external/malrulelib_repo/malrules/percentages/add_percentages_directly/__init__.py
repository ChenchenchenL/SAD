"""
Add-Percentages-Directly malrule.

Students incorrectly add percentages directly without considering that
they may apply to different base values or compound with each other.
For example: "A shirt is marked up 20% then discounted 20%, so it's
back to the original price" or "20% + 30% = 50%" when they compound.
"""

from .problem_generator import AddPercentagesProblemGenerator
from .malrule_algorithm import AddPercentagesDirectlyMalrule
from .correct_algorithm import PercentageCorrectAlgorithm

# Alias for generate_step_samples.py compatibility
AddPercentagesDirectlyProblemGenerator = AddPercentagesProblemGenerator
AddPercentagesDirectlyCorrectAlgorithm = PercentageCorrectAlgorithm

__all__ = [
    'AddPercentagesProblemGenerator',
    'AddPercentagesDirectlyMalrule',
    'PercentageCorrectAlgorithm',
    'AddPercentagesDirectlyProblemGenerator',  # Alias
    'AddPercentagesDirectlyCorrectAlgorithm',  # Alias
]
