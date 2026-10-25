"""
PEMDAS-Strictly-Sequential Malrule

Students treat PEMDAS as 6 separate sequential steps instead of understanding
that M/D are equal priority (left-to-right) and A/S are equal priority.

Example: 10 - 3 + 2 → Student does Addition first (PEMDAS says A before S): 10 - 5 = 5 ❌
Correct: Left to right: 10 - 3 = 7, then 7 + 2 = 9 ✓

Common cases:
- 6 ÷ 2 × 3 → Does M first: 6 ÷ 6 = 1 (wrong, should be 9)
- 10 - 3 + 2 → Does A first: 10 - 5 = 5 (wrong, should be 9)
- 8 ÷ 4 × 2 → Does M first: 8 ÷ 8 = 1 (wrong, should be 4)

"""

from .problem_generator import PEMDASStrictlySequentialProblemGenerator
from .malrule_algorithm import PEMDASStrictlySequentialMalrule
from .correct_algorithm import OrderOfOperationsCorrectAlgorithm

# Alias for generate_step_samples.py compatibility
PemdasStrictlySequentialProblemGenerator = PEMDASStrictlySequentialProblemGenerator
PemdasStrictlySequentialMalrule = PEMDASStrictlySequentialMalrule
PemdasStrictlySequentialCorrectAlgorithm = OrderOfOperationsCorrectAlgorithm

__all__ = [
    'PEMDASStrictlySequentialProblemGenerator',
    'PEMDASStrictlySequentialMalrule',
    'OrderOfOperationsCorrectAlgorithm',
    'PemdasStrictlySequentialProblemGenerator',  # Alias
    'PemdasStrictlySequentialMalrule',  # Alias
    'PemdasStrictlySequentialCorrectAlgorithm',  # Alias
]
