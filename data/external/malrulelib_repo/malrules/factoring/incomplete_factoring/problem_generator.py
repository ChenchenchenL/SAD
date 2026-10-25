"""
Problem generator for Incomplete-Factoring malrule.

Generates multi-step factoring problems where students stop after first factoring step.
"""

import random
import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, Tuple, Optional, List
from utils import Problem, ProblemGenerator, DifficultyLevel


class IncompleteFactoringProblemGenerator(ProblemGenerator):
    """
    Generates factoring problems that require multiple steps.

    Templates:
    1. gcf_then_difference_of_squares - GCF(x² - b²)
    2. gcf_then_trinomial - GCF(x² + bx + c) where x² + bx + c factors
    3. gcf_then_perfect_square - GCF((x+a)²)
    4. nested_factoring - x(x² - b²) needs x(x+b)(x-b)
    5. word_problem - Geometry/area contexts
    """

    def get_name(self) -> str:
        return "Incomplete-Factoring Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates multi-step factoring problems to elicit the misconception "
            "of stopping before complete factorization."
        )

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'gcf_then_difference_of_squares',
            'gcf_then_trinomial',
            'gcf_then_perfect_square',
            'nested_factoring',
            'word_problem'
        ]

    def get_value_ranges(self):
        """Return the value ranges for problem generation."""
        if self.difficulty == DifficultyLevel.EASY:
            return {
                'gcf': (2, 3),
                'difference_base': (2, 4),  # For difference of squares: a² - b²
                'trinomial_factor': (1, 3)  # For trinomial: (x+p)(x+q)
            }
        elif self.difficulty == DifficultyLevel.MEDIUM:
            return {
                'gcf': (2, 5),
                'difference_base': (2, 6),
                'trinomial_factor': (1, 4)
            }
        else:  # HARD
            return {
                'gcf': (2, 6),
                'difference_base': (2, 8),
                'trinomial_factor': (1, 5)
            }

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate an incomplete factoring problem.

        Args:
            seed: Optional random seed for reproducibility
            template: Optional template name to use

        Returns:
            Problem with multi-step factoring
        """
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            template = random.choice(self.get_available_templates())

        # Generate based on template
        if template == 'gcf_then_difference_of_squares':
            return self._generate_gcf_then_difference_of_squares(seed)
        elif template == 'gcf_then_trinomial':
            return self._generate_gcf_then_trinomial(seed)
        elif template == 'gcf_then_perfect_square':
            return self._generate_gcf_then_perfect_square(seed)
        elif template == 'nested_factoring':
            return self._generate_nested_factoring(seed)
        elif template == 'word_problem':
            return self._generate_word_problem(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_gcf_then_difference_of_squares(self, seed=None) -> Problem:
        """Generate GCF(x² - b²) problem."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        gcf = random.randint(ranges['gcf'][0], ranges['gcf'][1])
        b = random.randint(ranges['difference_base'][0], ranges['difference_base'][1])

        # Create expression: gcf(x² - b²)
        # Expanded form: gcf*x² - gcf*b²
        coefficient = gcf
        constant_term = gcf * (b ** 2)

        expression = f"{coefficient}x² - {constant_term}"

        # Incomplete: just factor out GCF
        if gcf == 1:
            incomplete_answer = f"x² - {b**2}"
        else:
            incomplete_answer = f"{gcf}(x² - {b**2})"

        # Complete: GCF and difference of squares
        if gcf == 1:
            complete_answer = f"(x + {b})(x - {b})"
        else:
            complete_answer = f"{gcf}(x + {b})(x - {b})"

        metadata = {
            'template': 'gcf_then_difference_of_squares',
            'gcf': gcf,
            'b': b,
            'coefficient': coefficient,
            'constant': constant_term,
            'expression': expression,
            'incomplete_answer': incomplete_answer,
            'complete_answer': complete_answer
        }

        return Problem(
            text=f"Factor completely: {expression}",
            operands=[coefficient, constant_term],
            operation='factoring',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_gcf_then_trinomial(self, seed=None) -> Problem:
        """Generate GCF(x² + bx + c) where trinomial factors."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        gcf = random.randint(ranges['gcf'][0], ranges['gcf'][1])

        # Generate factors: (x+p)(x+q) = x² + (p+q)x + pq
        p = random.randint(ranges['trinomial_factor'][0], ranges['trinomial_factor'][1])
        q = random.randint(ranges['trinomial_factor'][0], ranges['trinomial_factor'][1])

        # Trinomial coefficients
        b_coeff = p + q  # coefficient of x
        c_coeff = p * q  # constant term

        # Build expression: gcf(x² + bx + c)
        # Expanded: gcf*x² + gcf*b*x + gcf*c
        expression = f"{gcf}x² + {gcf * b_coeff}x + {gcf * c_coeff}"

        # Incomplete: just factor out GCF
        incomplete_answer = f"{gcf}(x² + {b_coeff}x + {c_coeff})"

        # Complete: GCF and trinomial factoring
        complete_answer = f"{gcf}(x + {p})(x + {q})"

        metadata = {
            'template': 'gcf_then_trinomial',
            'gcf': gcf,
            'p': p,
            'q': q,
            'b_coeff': b_coeff,
            'c_coeff': c_coeff,
            'expression': expression,
            'incomplete_answer': incomplete_answer,
            'complete_answer': complete_answer
        }

        return Problem(
            text=f"Factor completely: {expression}",
            operands=[gcf, gcf * b_coeff, gcf * c_coeff],
            operation='factoring',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_gcf_then_perfect_square(self, seed=None) -> Problem:
        """Generate GCF((x+a)²) problem."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        gcf = random.randint(ranges['gcf'][0], ranges['gcf'][1])
        a = random.randint(ranges['trinomial_factor'][0], ranges['trinomial_factor'][1])

        # Perfect square: (x+a)² = x² + 2ax + a²
        middle_coeff = 2 * a
        constant = a ** 2

        # Build expression: gcf(x² + 2ax + a²)
        expression = f"{gcf}x² + {gcf * middle_coeff}x + {gcf * constant}"

        # Incomplete: just factor out GCF
        incomplete_answer = f"{gcf}(x² + {middle_coeff}x + {constant})"

        # Complete: GCF and perfect square
        complete_answer = f"{gcf}(x + {a})²"

        metadata = {
            'template': 'gcf_then_perfect_square',
            'gcf': gcf,
            'a': a,
            'middle_coeff': middle_coeff,
            'constant': constant,
            'expression': expression,
            'incomplete_answer': incomplete_answer,
            'complete_answer': complete_answer
        }

        return Problem(
            text=f"Factor completely: {expression}",
            operands=[gcf, gcf * middle_coeff, gcf * constant],
            operation='factoring',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_nested_factoring(self, seed=None) -> Problem:
        """Generate x(x² - b²) needing x(x+b)(x-b)."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        b = random.randint(ranges['difference_base'][0], ranges['difference_base'][1])

        # Expression: x³ - b²x = x(x² - b²)
        expression = f"x³ - {b**2}x"

        # Incomplete: just factor out x
        incomplete_answer = f"x(x² - {b**2})"

        # Complete: factor x and difference of squares
        complete_answer = f"x(x + {b})(x - {b})"

        metadata = {
            'template': 'nested_factoring',
            'b': b,
            'expression': expression,
            'incomplete_answer': incomplete_answer,
            'complete_answer': complete_answer
        }

        return Problem(
            text=f"Factor completely: {expression}",
            operands=[1, 0, 0, -(b**2)],  # x³ + 0x² + 0x - b²
            operation='factoring',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_word_problem(self, seed=None) -> Problem:
        """Generate word problem context covering ALL formula types."""
        if seed is not None:
            random.seed(seed)

        # Select which formula type to embed
        formula_types = ['gcf_then_difference_of_squares', 'gcf_then_trinomial',
                        'gcf_then_perfect_square', 'nested_factoring']
        formula_type = random.choice(formula_types)
        variant = random.randint(0, 2)  # 3 variants per formula type

        ranges = self.get_value_ranges()

        if formula_type == 'gcf_then_difference_of_squares':
            gcf = random.randint(ranges['gcf'][0], ranges['gcf'][1])
            b = random.randint(ranges['difference_base'][0], ranges['difference_base'][1])

            coefficient = gcf
            constant_term = gcf * (b ** 2)
            expression = f"{coefficient}x² - {constant_term}"

            contexts = [
                f"A rectangular garden has area {expression} square feet. Factor this expression completely to find possible dimensions.",
                f"The difference between the area of a large square and a small square is {expression} square units. Factor completely.",
                f"A farmer has {expression} square meters of land. Express this area in completely factored form."
            ]

            if gcf == 1:
                incomplete_answer = f"x² - {b**2}"
                complete_answer = f"(x + {b})(x - {b})"
            else:
                incomplete_answer = f"{gcf}(x² - {b**2})"
                complete_answer = f"{gcf}(x + {b})(x - {b})"

            metadata = {
                'template': 'word_problem',
                'gcf': gcf,
                'b': b,
                'coefficient': coefficient,
                'constant': constant_term,
                'expression': expression,
                'incomplete_answer': incomplete_answer,
                'complete_answer': complete_answer,
                'is_word_problem': True,
                'word_problem_type': formula_type,
                'word_problem_variant': variant
            }

            return Problem(
                text=contexts[variant],
                operands=[coefficient, constant_term],
                operation='factoring',
                level=self.level,
                difficulty=self.difficulty,
                metadata=metadata
            )

        elif formula_type == 'gcf_then_trinomial':
            gcf = random.randint(ranges['gcf'][0], ranges['gcf'][1])
            p = random.randint(ranges['trinomial_factor'][0], ranges['trinomial_factor'][1])
            q = random.randint(ranges['trinomial_factor'][0], ranges['trinomial_factor'][1])

            b_coeff = p + q
            c_coeff = p * q

            a = gcf
            b = gcf * b_coeff
            c = gcf * c_coeff
            expression = f"{a}x² + {b}x + {c}"

            contexts = [
                f"The total area of {gcf} identical rectangular plots is {expression} square meters. Factor completely to find the dimensions of each plot.",
                f"A rectangular swimming pool design has area expression {expression}. Factor this completely.",
                f"The area of a composite rectangle is {expression} square feet. Express in completely factored form."
            ]

            incomplete_answer = f"{gcf}(x² + {b_coeff}x + {c_coeff})"
            complete_answer = f"{gcf}(x + {p})(x + {q})"

            metadata = {
                'template': 'word_problem',
                'gcf': gcf,
                'p': p,
                'q': q,
                'b_coeff': b_coeff,
                'c_coeff': c_coeff,
                'expression': expression,
                'incomplete_answer': incomplete_answer,
                'complete_answer': complete_answer,
                'is_word_problem': True,
                'word_problem_type': formula_type,
                'word_problem_variant': variant
            }

            return Problem(
                text=contexts[variant],
                operands=[a, b, c],
                operation='factoring',
                level=self.level,
                difficulty=self.difficulty,
                metadata=metadata
            )

        elif formula_type == 'gcf_then_perfect_square':
            gcf = random.randint(ranges['gcf'][0], ranges['gcf'][1])
            a = random.randint(ranges['trinomial_factor'][0], ranges['trinomial_factor'][1])

            middle_coeff = 2 * a
            constant = a ** 2

            expression = f"{gcf}x² + {gcf * middle_coeff}x + {gcf * constant}"

            contexts = [
                f"A square patio design has {gcf} sections, each with area x² + {middle_coeff}x + {constant}. Factor the total area {expression} completely.",
                f"The expression {expression} represents the total area of a tiled floor. Factor completely.",
                f"A rectangular garden bed has area {expression} square meters. Express in completely factored form."
            ]

            incomplete_answer = f"{gcf}(x² + {middle_coeff}x + {constant})"
            complete_answer = f"{gcf}(x + {a})²"

            metadata = {
                'template': 'word_problem',
                'gcf': gcf,
                'a': a,
                'middle_coeff': middle_coeff,
                'constant': constant,
                'expression': expression,
                'incomplete_answer': incomplete_answer,
                'complete_answer': complete_answer,
                'is_word_problem': True,
                'word_problem_type': formula_type,
                'word_problem_variant': variant
            }

            return Problem(
                text=contexts[variant],
                operands=[gcf, gcf * middle_coeff, gcf * constant],
                operation='factoring',
                level=self.level,
                difficulty=self.difficulty,
                metadata=metadata
            )

        else:  # nested_factoring
            b = random.randint(ranges['difference_base'][0], ranges['difference_base'][1])
            expression = f"x³ - {b**2}x"

            contexts = [
                f"The volume of a geometric shape is {expression} cubic units. Factor this expression completely.",
                f"A polynomial expression {expression} models a physical quantity. Factor completely.",
                f"The expression {expression} represents a three-dimensional measurement. Express in completely factored form."
            ]

            incomplete_answer = f"x(x² - {b**2})"
            complete_answer = f"x(x + {b})(x - {b})"

            metadata = {
                'template': 'word_problem',
                'b': b,
                'expression': expression,
                'incomplete_answer': incomplete_answer,
                'complete_answer': complete_answer,
                'is_word_problem': True,
                'word_problem_type': formula_type,
                'word_problem_variant': variant
            }

            return Problem(
                text=contexts[variant],
                operands=[1, 0, 0, -(b**2)],
                operation='factoring',
                level=self.level,
                difficulty=self.difficulty,
                metadata=metadata
            )
