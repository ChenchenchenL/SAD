"""
Mean-Without-Understanding malrule.

Students calculate mean procedurally (add all, divide by count) without
understanding what it represents. They apply the procedure even when it
doesn't make sense or fail to recognize when the mean is not representative.
"""

from .problem_generator import MeanUnderstandingProblemGenerator
from .malrule_algorithm import MeanWithoutUnderstandingMalrule
from .correct_algorithm import MeanWithUnderstandingCorrectAlgorithm

# Alias for generate_step_samples.py compatibility
MeanWithoutUnderstandingProblemGenerator = MeanUnderstandingProblemGenerator
MeanWithoutUnderstandingCorrectAlgorithm = MeanWithUnderstandingCorrectAlgorithm

__all__ = [
    'MeanUnderstandingProblemGenerator',
    'MeanWithoutUnderstandingMalrule',
    'MeanWithUnderstandingCorrectAlgorithm',
    'MeanWithoutUnderstandingProblemGenerator',  # Alias
    'MeanWithoutUnderstandingCorrectAlgorithm',  # Alias
]
