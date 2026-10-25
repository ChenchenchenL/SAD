"""
Ratio-As-Division-Only Malrule

Students understand ratio only as division (quotient), not as multiplicative relationship.

Example 1 - Interpretation:
Question: "What does 3:5 mean?"
Student: "3 divided by 5 equals 0.6" ✗
Correct: "For every 3 of the first, there are 5 of the second" ✓

Example 2 - Application:
Question: "Ratio is 3:5, there are 9 of first, how many of second?"
Student: 9 × (3/5) = 5.4 (uses ratio as decimal conversion incorrectly) ✗
Correct: 9 = 3×3, so second = 5×3 = 15 (uses multiplicative relationship) ✓

The malrule: Students see ratio as a single quotient value rather than
as a relationship describing how quantities scale together.

"""

from .problem_generator import RatioAsDivisionOnlyProblemGenerator
from .malrule_algorithm import RatioAsDivisionOnlyMalrule
from .correct_algorithm import RatioMultiplicativeRelationshipCorrectAlgorithm

__all__ = [
    'RatioAsDivisionOnlyProblemGenerator',
    'RatioAsDivisionOnlyMalrule',
    'RatioMultiplicativeRelationshipCorrectAlgorithm'
]
