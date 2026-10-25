"""
Slope-Direction-Confusion Malrule

Students confuse positive and negative slope directions. When asked to describe
the direction of a line with negative slope, they say it's "increasing" or "going up."
When asked about a positive slope, they may say it's "decreasing" or "going down."

This represents a fundamental misunderstanding of the relationship between slope sign
and line direction.

Example 1: Describe direction of line with slope = -2
Student: "increasing" or "going up" ✗
Correct: "decreasing" or "going down" ✓

Example 2: Describe direction of line with slope = 3
Student: "decreasing" or "going down" ✗
Correct: "increasing" or "going up" ✓

"""

from .problem_generator import SlopeDirectionConfusionProblemGenerator
from .malrule_algorithm import SlopeDirectionConfusionMalrule
from .correct_algorithm import SlopeDirectionCorrectAlgorithm

__all__ = [
    'SlopeDirectionConfusionProblemGenerator',
    'SlopeDirectionConfusionMalrule',
    'SlopeDirectionCorrectAlgorithm'
]
