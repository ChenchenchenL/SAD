"""
Same-Input-Different-Outputs-OK malrule.

Students don't understand that functions must map each input to exactly ONE output.
They think f(3)=5 and f(3)=7 can both be true.
"""

from .problem_generator import SameInputDifferentOutputsOKProblemGenerator
from .malrule_algorithm import SameInputDifferentOutputsOKMalrule
from .correct_algorithm import FunctionDefinitionCorrectAlgorithm

# Alias for generate_step_samples.py compatibility
SameInputDifferentOutputsOkProblemGenerator = SameInputDifferentOutputsOKProblemGenerator
SameInputDifferentOutputsOkMalrule = SameInputDifferentOutputsOKMalrule
SameInputDifferentOutputsOkCorrectAlgorithm = FunctionDefinitionCorrectAlgorithm

__all__ = [
    'SameInputDifferentOutputsOKProblemGenerator',
    'SameInputDifferentOutputsOKMalrule',
    'FunctionDefinitionCorrectAlgorithm',
    'SameInputDifferentOutputsOkProblemGenerator',  # Alias
    'SameInputDifferentOutputsOkMalrule',  # Alias
    'SameInputDifferentOutputsOkCorrectAlgorithm',  # Alias
]
