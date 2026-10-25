"""
Problem template utilities for generating natural language problem statements.

Provides tools for creating varied, natural-sounding math problems with
randomized values within level-appropriate ranges.
"""

import random
from typing import Dict, List, Any, Optional
from string import Template


class ProblemTemplate:
    """
    A template for generating natural language problem statements.

    Supports variable substitution and multiple template variations.
    """

    def __init__(self, templates: List[str], parameter_names: List[str]):
        """
        Initialize problem template.

        Args:
            templates: List of template strings using $variable syntax
            parameter_names: Names of parameters to substitute
        """
        self.templates = [Template(t) for t in templates]
        self.parameter_names = parameter_names

    def generate(self, parameters: Dict[str, Any]) -> str:
        """
        Generate problem text by substituting parameters into a template.

        Args:
            parameters: Dictionary mapping parameter names to values

        Returns:
            Formatted problem text
        """
        # Verify all required parameters are provided
        missing = set(self.parameter_names) - set(parameters.keys())
        if missing:
            raise ValueError(f"Missing required parameters: {missing}")

        # Randomly select one template
        template = random.choice(self.templates)

        # Substitute parameters
        return template.safe_substitute(parameters)


class ContextualProblemTemplate(ProblemTemplate):
    """
    Extended problem template that includes real-world context.

    Generates problems with contextual scenarios (e.g., shopping, sharing).
    """

    def __init__(self, templates: List[str], parameter_names: List[str],
                 contexts: Optional[List[Dict[str, str]]] = None):
        """
        Initialize contextual problem template.

        Args:
            templates: List of template strings
            parameter_names: Names of numerical parameters
            contexts: List of context dictionaries with items, actors, actions, etc.
        """
        super().__init__(templates, parameter_names)
        self.contexts = contexts or []

    def generate_with_context(self, parameters: Dict[str, Any]) -> str:
        """
        Generate problem with random real-world context.

        Args:
            parameters: Numerical parameters for the problem

        Returns:
            Contextual problem text
        """
        if self.contexts:
            context = random.choice(self.contexts)
            parameters = {**parameters, **context}

        return self.generate(parameters)


# Common context collections for different problem types

SHARING_CONTEXTS = [
    {
        'actor': 'Sarah',
        'item': 'cookies',
        'action': 'sharing with her friends'
    },
    {
        'actor': 'John',
        'item': 'marbles',
        'action': 'dividing among his classmates'
    },
    {
        'actor': 'Maria',
        'item': 'stickers',
        'action': 'giving to her siblings'
    },
    {
        'actor': 'Alex',
        'item': 'pencils',
        'action': 'distributing to group members'
    }
]

SHOPPING_CONTEXTS = [
    {
        'actor': 'Mom',
        'item': 'apples',
        'location': 'grocery store'
    },
    {
        'actor': 'Dad',
        'item': 'notebooks',
        'location': 'office supply store'
    },
    {
        'actor': 'Emma',
        'item': 'books',
        'location': 'bookstore'
    },
    {
        'actor': 'Mike',
        'item': 'toys',
        'location': 'toy store'
    }
]

COLLECTION_CONTEXTS = [
    {
        'actor': 'the teacher',
        'item': 'homework assignments',
        'container': 'folder'
    },
    {
        'actor': 'the librarian',
        'item': 'books',
        'container': 'cart'
    },
    {
        'actor': 'the coach',
        'item': 'basketballs',
        'container': 'bag'
    }
]

MEASUREMENT_CONTEXTS = [
    {
        'actor': 'Jake',
        'item': 'rope',
        'unit': 'meters',
        'action': 'measuring'
    },
    {
        'actor': 'Lisa',
        'item': 'ribbon',
        'unit': 'inches',
        'action': 'cutting'
    },
    {
        'actor': 'Tom',
        'item': 'wood',
        'unit': 'feet',
        'action': 'sawing'
    }
]


def create_basic_arithmetic_template(operation: str) -> ProblemTemplate:
    """
    Create a basic arithmetic problem template.

    Args:
        operation: One of 'addition', 'subtraction', 'multiplication', 'division'

    Returns:
        ProblemTemplate instance
    """
    templates = {
        'addition': [
            "What is $a + $b?",
            "Add $a and $b.",
            "Calculate: $a + $b",
            "Find the sum of $a and $b.",
        ],
        'subtraction': [
            "What is $a - $b?",
            "Subtract $b from $a.",
            "Calculate: $a - $b",
            "Find the difference between $a and $b.",
        ],
        'multiplication': [
            "What is $a × $b?",
            "Multiply $a by $b.",
            "Calculate: $a × $b",
            "Find the product of $a and $b.",
        ],
        'division': [
            "What is $a ÷ $b?",
            "Divide $a by $b.",
            "Calculate: $a ÷ $b",
            "Find the quotient of $a and $b.",
        ]
    }

    return ProblemTemplate(
        templates=templates[operation],
        parameter_names=['a', 'b']
    )


def create_fraction_template(operation: str) -> ProblemTemplate:
    """
    Create a fraction operation problem template.

    Args:
        operation: One of 'addition', 'subtraction', 'multiplication', 'division'

    Returns:
        ProblemTemplate instance
    """
    templates = {
        'addition': [
            "What is $num1/$den1 + $num2/$den2?",
            "Add $num1/$den1 and $num2/$den2.",
            "Calculate: $num1/$den1 + $num2/$den2",
            "Find the sum: $num1/$den1 + $num2/$den2",
        ],
        'subtraction': [
            "What is $num1/$den1 - $num2/$den2?",
            "Subtract $num2/$den2 from $num1/$den1.",
            "Calculate: $num1/$den1 - $num2/$den2",
            "Find the difference: $num1/$den1 - $num2/$den2",
        ],
        'multiplication': [
            "What is $num1/$den1 × $num2/$den2?",
            "Multiply $num1/$den1 by $num2/$den2.",
            "Calculate: $num1/$den1 × $num2/$den2",
            "Find the product: $num1/$den1 × $num2/$den2",
        ],
        'division': [
            "What is $num1/$den1 ÷ $num2/$den2?",
            "Divide $num1/$den1 by $num2/$den2.",
            "Calculate: $num1/$den1 ÷ $num2/$den2",
            "Find the quotient: $num1/$den1 ÷ $num2/$den2",
        ]
    }

    return ProblemTemplate(
        templates=templates[operation],
        parameter_names=['num1', 'den1', 'num2', 'den2']
    )


def create_decimal_comparison_template() -> ProblemTemplate:
    """Create template for decimal comparison problems."""
    templates = [
        "Which is greater: $a or $b?",
        "Compare $a and $b. Which is larger?",
        "Is $a greater than, less than, or equal to $b?",
        "Order these numbers from least to greatest: $a, $b",
    ]

    return ProblemTemplate(
        templates=templates,
        parameter_names=['a', 'b']
    )


def create_negative_number_template(operation: str) -> ProblemTemplate:
    """
    Create template for negative number operations.

    Args:
        operation: One of 'addition', 'subtraction', 'multiplication', 'division'
    """
    templates = {
        'addition': [
            "What is $a + ($b)?",
            "Calculate: $a + ($b)",
            "Add $a and $b.",
        ],
        'subtraction': [
            "What is $a - ($b)?",
            "Calculate: $a - ($b)",
            "Subtract $b from $a.",
        ],
        'multiplication': [
            "What is $a × ($b)?",
            "Calculate: $a × ($b)",
            "Multiply $a by $b.",
        ],
        'division': [
            "What is $a ÷ ($b)?",
            "Calculate: $a ÷ ($b)",
            "Divide $a by $b.",
        ]
    }

    return ProblemTemplate(
        templates=templates[operation],
        parameter_names=['a', 'b']
    )


def create_order_of_operations_template() -> ProblemTemplate:
    """Create template for order of operations problems."""
    templates = [
        "Calculate: $expression",
        "What is the value of $expression?",
        "Evaluate: $expression",
        "Solve: $expression",
    ]

    return ProblemTemplate(
        templates=templates,
        parameter_names=['expression']
    )


def create_algebra_equation_template() -> ProblemTemplate:
    """Create template for algebra equation solving."""
    templates = [
        "Solve for $variable: $equation",
        "What is $variable in the equation $equation?",
        "Find the value of $variable: $equation",
        "Solve: $equation",
    ]

    return ProblemTemplate(
        templates=templates,
        parameter_names=['variable', 'equation']
    )
