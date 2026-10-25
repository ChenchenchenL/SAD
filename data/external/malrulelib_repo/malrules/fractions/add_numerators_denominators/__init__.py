"""
Add-Numerators-Add-Denominators Malrule

Common fraction addition error where students add numerators and denominators
separately: a/b + c/d = (a+c)/(b+d)
"""

from .problem_generator import FractionAdditionProblemGenerator
from .malrule_algorithm import AddNumeratorsAddDenominatorsMalrule
from .correct_algorithm import FractionAdditionCorrectAlgorithm

# Alias for generate_step_samples.py compatibility
AddNumeratorsDenominatorsProblemGenerator = FractionAdditionProblemGenerator
AddNumeratorsDenominatorsMalrule = AddNumeratorsAddDenominatorsMalrule
AddNumeratorsDenominatorsCorrectAlgorithm = FractionAdditionCorrectAlgorithm

__all__ = [
    'FractionAdditionProblemGenerator',
    'AddNumeratorsAddDenominatorsMalrule',
    'FractionAdditionCorrectAlgorithm',
    'AddNumeratorsDenominatorsProblemGenerator',  # Alias
    'AddNumeratorsDenominatorsMalrule',  # Alias
    'AddNumeratorsDenominatorsCorrectAlgorithm',  # Alias
]
