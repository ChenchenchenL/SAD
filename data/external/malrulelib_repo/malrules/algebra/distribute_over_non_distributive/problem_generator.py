"""
Problem generator for Distribute-Over-Non-Distributive malrule.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List, Dict, Any, Optional
from utils import ProblemGenerator, Problem, DifficultyLevel
import random


class DistributeOverNonDistributiveProblemGenerator(ProblemGenerator):
    """
    Generates problems involving non-distributive operations.

    Templates:
    1. basic_square_binomial - (x+a)²
    2. basic_sqrt_sum - √(a+b)
    3. square_binomial_subtraction - (x-a)²
    4. sqrt_difference - √(a-b) and √(a²+b²)
    5. word_problem - Real-world contexts
    """

    def get_name(self) -> str:
        return "Distribute-Over-Non-Distributive Problem Generator"

    def get_description(self) -> str:
        return "Generates algebra problems with non-distributive operations (squaring binomials, square roots of sums)."

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_square_binomial',
            'basic_sqrt_sum',
            'square_binomial_subtraction',
            'sqrt_difference',
            'word_problem'
        ]

    def get_value_ranges(self) -> Dict[str, Any]:
        """Returns the value ranges for problem generation."""
        return {
            'constant_min': 1,
            'constant_max': 10,
            'operation_types': ['square_binomial', 'sqrt_sum'],
            'variables': ['x', 'y', 'a', 'b']
        }

    def generate(self, seed=None, template: Optional[str] = None) -> Problem:
        """Generate a problem involving non-distributive operations."""
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            template = random.choice(self.get_available_templates())

        # Generate based on template
        if template == 'basic_square_binomial':
            return self._generate_basic_square_binomial(seed)
        elif template == 'basic_sqrt_sum':
            return self._generate_basic_sqrt_sum(seed)
        elif template == 'square_binomial_subtraction':
            return self._generate_square_binomial_subtraction(seed)
        elif template == 'sqrt_difference':
            return self._generate_sqrt_difference(seed)
        elif template == 'word_problem':
            return self._generate_word_problem(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_square_binomial(self, seed=None) -> Problem:
        """
        Generate basic square binomial problem (original template).

        Example: (x+3)²
        Correct: x² + 6x + 9
        Malrule: x² + 9 (missing middle term)
        """
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        variable = random.choice(ranges['variables'])
        constant = random.randint(ranges['constant_min'], ranges['constant_max'])

        # Correct expansion: (x + a)² = x² + 2ax + a²
        # Malrule answer: x² + a²
        correct_coeffs = {
            'x²': 1,
            'x': 2 * constant,
            'constant': constant ** 2
        }
        malrule_coeffs = {
            'x²': 1,
            'x': 0,  # Missing middle term!
            'constant': constant ** 2
        }

        text = f"Expand: ({variable}+{constant})²"

        metadata = {
            'variable': variable,
            'constant': constant,
            'operation': 'square_binomial',
            'correct_coeffs': correct_coeffs,
            'malrule_coeffs': malrule_coeffs,
            'expression': f"({variable}+{constant})²",
            'template': 'basic_square_binomial'
        }

        return Problem(
            text=text,
            operands=[constant],
            operation='algebra_expansion',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_basic_sqrt_sum(self, seed=None) -> Problem:
        """
        Generate basic square root sum problem (original template).

        Example: √(9+16)
        Correct: √25 = 5
        Malrule: √9 + √16 = 3 + 4 = 7
        """
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        num1 = random.randint(ranges['constant_min'], ranges['constant_max'])
        num2 = random.randint(ranges['constant_min'], ranges['constant_max'])

        # Correct: √(a + b) = √(a+b) [cannot simplify]
        # Malrule: √(a + b) = √a + √b
        correct_value = (num1 + num2) ** 0.5
        malrule_value = num1 ** 0.5 + num2 ** 0.5

        text = f"Simplify: √({num1}+{num2})"

        metadata = {
            'num1': num1,
            'num2': num2,
            'operation': 'sqrt_sum',
            'correct_answer': round(correct_value, 2),
            'malrule_answer': round(malrule_value, 2),
            'expression': f"√({num1}+{num2})",
            'template': 'basic_sqrt_sum'
        }

        return Problem(
            text=text,
            operands=[num1, num2],
            operation='algebra_expansion',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_square_binomial_subtraction(self, seed=None) -> Problem:
        """
        Generate square binomial with subtraction.

        Example: (x-5)²
        Correct: x² - 10x + 25
        Malrule: x² + 25 (missing middle term)
        """
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        variable = random.choice(ranges['variables'])
        constant = random.randint(ranges['constant_min'], ranges['constant_max'])

        # Correct expansion: (x - a)² = x² - 2ax + a²
        # Malrule answer: x² + a²
        correct_coeffs = {
            'x²': 1,
            'x': -2 * constant,
            'constant': constant ** 2
        }
        malrule_coeffs = {
            'x²': 1,
            'x': 0,  # Missing middle term!
            'constant': constant ** 2
        }

        text = f"Expand: ({variable}-{constant})²"

        metadata = {
            'variable': variable,
            'constant': constant,
            'operation': 'square_binomial',
            'correct_coeffs': correct_coeffs,
            'malrule_coeffs': malrule_coeffs,
            'expression': f"({variable}-{constant})²",
            'template': 'square_binomial_subtraction',
            'is_subtraction': True
        }

        return Problem(
            text=text,
            operands=[constant],
            operation='algebra_expansion',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_sqrt_difference(self, seed=None) -> Problem:
        """
        Generate square root of Pythagorean-like sum.

        Example: √(9²+12²) = √(81+144) = √225 = 15
        Malrule: √(9²+12²) = √9² + √12² = 9 + 12 = 21
        """
        if seed is not None:
            random.seed(seed)

        # Use perfect square pairs for interesting problems
        num1 = random.randint(3, 12)
        num2 = random.randint(3, 12)

        # Calculate a² + b²
        sum_of_squares = num1**2 + num2**2

        # Correct: √(a² + b²)
        correct_value = sum_of_squares ** 0.5

        # Malrule: √(a²) + √(b²) = a + b
        malrule_value = num1 + num2

        text = f"Simplify: √({num1}²+{num2}²)"

        metadata = {
            'num1': num1,
            'num2': num2,
            'sum_of_squares': sum_of_squares,
            'operation': 'sqrt_sum',
            'correct_answer': round(correct_value, 2),
            'malrule_answer': malrule_value,
            'expression': f"√({num1}²+{num2}²)",
            'template': 'sqrt_difference',
            'is_pythagorean': True
        }

        return Problem(
            text=text,
            operands=[num1, num2],
            operation='algebra_expansion',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_word_problem(self, seed=None) -> Problem:
        """
        Generate word problem with non-distributive operations.

        Real-world contexts where distribution doesn't apply.
        Covers ALL formula types with 3 variants each.
        """
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()

        # Select which formula type to embed
        formula_types = ['square_binomial_addition', 'square_binomial_subtraction', 'sqrt_sum']
        formula_type = random.choice(formula_types)
        variant = random.randint(0, 2)

        if formula_type == 'square_binomial_addition':
            # Formula: (x+a)²
            variable = 'x'
            constant = random.randint(ranges['constant_min'], ranges['constant_max'])

            templates = [
                f"A square garden has side length ({variable}+{constant}) meters. What is its area in expanded form?",
                f"If the edge of a square is ({variable}+{constant}) units, express the area as a polynomial.",
                f"The side of a square picture frame is ({variable}+{constant}) inches. Write the area in standard form."
            ]

            text = templates[variant]

            # Correct expansion: (x + a)² = x² + 2ax + a²
            # Malrule answer: x² + a²
            correct_coeffs = {
                'x²': 1,
                'x': 2 * constant,
                'constant': constant ** 2
            }
            malrule_coeffs = {
                'x²': 1,
                'x': 0,  # Missing middle term!
                'constant': constant ** 2
            }

            metadata = {
                'variable': variable,
                'constant': constant,
                'operation': 'square_binomial',
                'correct_coeffs': correct_coeffs,
                'malrule_coeffs': malrule_coeffs,
                'expression': f"({variable}+{constant})²",
                'template': 'word_problem',
                'context': 'square_area',
                'word_problem_type': formula_type,
                'word_problem_variant': variant
            }

            operands = [constant]

        elif formula_type == 'square_binomial_subtraction':
            # Formula: (x-a)²
            variable = 'x'
            constant = random.randint(ranges['constant_min'], ranges['constant_max'])

            templates = [
                f"A square field has side length ({variable}-{constant}) meters after a reduction. What is its area in expanded form?",
                f"The side of a square is reduced to ({variable}-{constant}) units. Express the area as a polynomial.",
                f"A square tile has side ({variable}-{constant}) cm after trimming. What is the area in standard form?"
            ]

            text = templates[variant]

            # Correct expansion: (x - a)² = x² - 2ax + a²
            # Malrule answer: x² + a² (missing middle term and wrong sign)
            correct_coeffs = {
                'x²': 1,
                'x': -2 * constant,
                'constant': constant ** 2
            }
            malrule_coeffs = {
                'x²': 1,
                'x': 0,  # Missing middle term!
                'constant': constant ** 2
            }

            metadata = {
                'variable': variable,
                'constant': constant,
                'operation': 'square_binomial',
                'correct_coeffs': correct_coeffs,
                'malrule_coeffs': malrule_coeffs,
                'expression': f"({variable}-{constant})²",
                'template': 'word_problem',
                'context': 'square_area_subtraction',
                'is_subtraction': True,
                'word_problem_type': formula_type,
                'word_problem_variant': variant
            }

            operands = [constant]

        else:  # sqrt_sum
            num1 = random.randint(ranges['constant_min'], ranges['constant_max'])
            num2 = random.randint(ranges['constant_min'], ranges['constant_max'])

            templates = [
                f"If you add {num1} units and {num2} units, then take the square root, what is √({num1}+{num2})?",
                f"A formula requires computing √({num1}+{num2}). What is the simplified value?",
                f"The area formula gives √({num1}+{num2}). Simplify this expression."
            ]

            text = templates[variant]

            # Correct: √(a + b) = √(a+b) [cannot simplify]
            # Malrule: √(a + b) = √a + √b
            correct_value = (num1 + num2) ** 0.5
            malrule_value = num1 ** 0.5 + num2 ** 0.5

            metadata = {
                'num1': num1,
                'num2': num2,
                'operation': 'sqrt_sum',
                'correct_answer': round(correct_value, 2),
                'malrule_answer': round(malrule_value, 2),
                'expression': f"√({num1}+{num2})",
                'template': 'word_problem',
                'context': 'sqrt_calculation',
                'word_problem_type': formula_type,
                'word_problem_variant': variant
            }

            operands = [num1, num2]

        return Problem(
            text=text,
            operands=operands,
            operation='algebra_expansion',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )
