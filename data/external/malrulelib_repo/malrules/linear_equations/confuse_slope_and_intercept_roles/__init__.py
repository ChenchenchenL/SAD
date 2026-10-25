"""
Confuse-Slope-And-Intercept-Roles Malrule

Students swap the roles of slope (m) and y-intercept (b) in the equation y = mx + b.
When given slope = 3 and y-intercept = 5, they write y = 5x + 3 instead of y = 3x + 5.
Or when asked to identify the slope from y = 2x + 7, they incorrectly say slope = 7.

This is a parameter confusion error - students don't understand the distinct roles
of slope and y-intercept in linear equations.

Example 1: Write equation with slope = 3, y-intercept = 5
Student: y = 5x + 3 ✗
Correct: y = 3x + 5 ✓

Example 2: What is the slope of y = 2x + 7?
Student: slope = 7 ✗
Correct: slope = 2 ✓

"""

from .problem_generator import ConfuseSlopeAndInterceptRolesProblemGenerator
from .malrule_algorithm import ConfuseSlopeAndInterceptRolesMalrule
from .correct_algorithm import SlopeInterceptCorrectAlgorithm

__all__ = [
    'ConfuseSlopeAndInterceptRolesProblemGenerator',
    'ConfuseSlopeAndInterceptRolesMalrule',
    'SlopeInterceptCorrectAlgorithm'
]
