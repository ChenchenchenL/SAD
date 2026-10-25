"""
Decompose-By-Place-Value-Label Malrule

Students incorrectly write numbers from place value decompositions by
concatenating the labels instead of adding values.
"""

from .problem_generator import DecomposeByPlaceValueLabelProblemGenerator
from .malrule_algorithm import DecomposeByPlaceValueLabelMalrule
from .correct_algorithm import PlaceValueDecompositionCorrectAlgorithm

__all__ = [
    'DecomposeByPlaceValueLabelProblemGenerator',
    'DecomposeByPlaceValueLabelMalrule',
    'PlaceValueDecompositionCorrectAlgorithm',
]
