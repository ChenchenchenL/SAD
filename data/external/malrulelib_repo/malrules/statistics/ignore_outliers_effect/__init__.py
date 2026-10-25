"""
Ignore-Outliers-Effect malrule.

Students don't recognize how outliers affect the mean. When asked if the mean
represents a data set with outliers, they say "yes" without understanding
outliers pull the mean away from typical values. They may also fail to identify
that median is more appropriate for skewed data.
"""

from .problem_generator import IgnoreOutliersEffectProblemGenerator
from .malrule_algorithm import IgnoreOutliersEffectMalrule
from .correct_algorithm import IgnoreOutliersEffectCorrectAlgorithm

__all__ = [
    'IgnoreOutliersEffectProblemGenerator',
    'IgnoreOutliersEffectMalrule',
    'IgnoreOutliersEffectCorrectAlgorithm',
]
