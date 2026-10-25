"""
Utilities package for malrule implementations.

Provides base classes, templates, and testing framework.
"""

from .malrule_base import (
    DifficultyLevel,
    Problem,
    Solution,
    ProblemGenerator,
    Algorithm,
    Malrule,
    CorrectAlgorithm,
    MalruleComparison
)

from .problem_template import (
    ProblemTemplate,
    ContextualProblemTemplate,
    SHARING_CONTEXTS,
    SHOPPING_CONTEXTS,
    COLLECTION_CONTEXTS,
    MEASUREMENT_CONTEXTS,
    create_basic_arithmetic_template,
    create_fraction_template,
    create_decimal_comparison_template,
    create_negative_number_template,
    create_order_of_operations_template,
    create_algebra_equation_template
)

from .test_framework import (
    TestResult,
    MalruleTest,
    InteractiveDemo
)

__all__ = [
    # Base classes
    'DifficultyLevel',
    'Problem',
    'Solution',
    'ProblemGenerator',
    'Algorithm',
    'Malrule',
    'CorrectAlgorithm',
    'MalruleComparison',

    # Template utilities
    'ProblemTemplate',
    'ContextualProblemTemplate',
    'SHARING_CONTEXTS',
    'SHOPPING_CONTEXTS',
    'COLLECTION_CONTEXTS',
    'MEASUREMENT_CONTEXTS',
    'create_basic_arithmetic_template',
    'create_fraction_template',
    'create_decimal_comparison_template',
    'create_negative_number_template',
    'create_order_of_operations_template',
    'create_algebra_equation_template',

    # Testing
    'TestResult',
    'MalruleTest',
    'InteractiveDemo',
]
