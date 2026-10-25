"""
Problem generator for Sum-Of-Squares-Factors malrule.

Generates sum of squares problems where students incorrectly try to factor them.
"""

import random
import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, Tuple, Optional, List
from utils import Problem, ProblemGenerator, DifficultyLevel


class SumOfSquaresFactorsProblemGenerator(ProblemGenerator):
    """
    Generates sum of squares factoring problems.

    Templates:
    1. basic_sum_of_squares - x² + b²
    2. coefficient_on_x - ax² + c²
    3. both_variables - x² + y²
    4. larger_coefficients - x² + larger b² (b=6-10)
    5. word_problem - Real-world contexts (geometry, Pythagorean confusion)
    """

    def get_name(self) -> str:
        return "Sum-Of-Squares-Factors Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates sum of squares factoring problems to elicit the misconception "
            "that x² + b² can be factored like x² - b² = (x-b)(x+b)."
        )

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_sum_of_squares',
            'coefficient_on_x',
            'both_variables',
            'larger_coefficients',
            'word_problem'
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Return the value ranges for problem generation."""
        ranges = {
            8: {
                DifficultyLevel.EASY: (2, 4),
                DifficultyLevel.MEDIUM: (2, 5),
                DifficultyLevel.HARD: (3, 6),
            },
            9: {
                DifficultyLevel.EASY: (2, 5),
                DifficultyLevel.MEDIUM: (3, 6),
                DifficultyLevel.HARD: (4, 7),
            },
            10: {
                DifficultyLevel.EASY: (3, 6),
                DifficultyLevel.MEDIUM: (4, 7),
                DifficultyLevel.HARD: (5, 8),
            }
        }

        lvl = self.level if self.level in ranges else 9
        return {'b': ranges[lvl][self.difficulty]}

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """Generate a sum of squares problem."""
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            template = random.choice(self.get_available_templates())

        # Generate based on template
        if template == 'basic_sum_of_squares':
            return self._generate_basic_sum_of_squares(seed)
        elif template == 'coefficient_on_x':
            return self._generate_coefficient_on_x(seed)
        elif template == 'both_variables':
            return self._generate_both_variables(seed)
        elif template == 'larger_coefficients':
            return self._generate_larger_coefficients(seed)
        elif template == 'word_problem':
            return self._generate_word_problem(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_sum_of_squares(self, seed=None) -> Problem:
        """Generate basic x² + b²."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        b = random.randint(*ranges['b'])

        expression = f"x² + {b**2}"
        correct_answer = f"x² + {b**2} (prime/cannot be factored)"
        malrule_answer = f"(x + {b})²"

        metadata = {
            'template': 'basic_sum_of_squares',
            'b': b,
            'b_squared': b**2,
            'expression': expression,
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer
        }

        return Problem(
            text=f"Factor: {expression}",
            operands=[1, 0, b**2],
            operation='factoring',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_coefficient_on_x(self, seed=None) -> Problem:
        """Generate ax² + c²."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        a = random.choice([2, 3, 4, 5])
        c = random.randint(*ranges['b'])

        expression = f"{a}x² + {c**2}"
        correct_answer = f"{a}x² + {c**2} (cannot be factored over reals)"

        # Malrule: Student tries (√a·x + c)² or factors out incorrectly
        malrule_answer = f"({a}x + {c})²"  # Most common error

        metadata = {
            'template': 'coefficient_on_x',
            'a': a,
            'c': c,
            'c_squared': c**2,
            'expression': expression,
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer
        }

        return Problem(
            text=f"Factor: {expression}",
            operands=[a, 0, c**2],
            operation='factoring',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_both_variables(self, seed=None) -> Problem:
        """Generate x² + y²."""
        if seed is not None:
            random.seed(seed)

        # Could add coefficients
        has_coeff = random.choice([True, False])

        if has_coeff:
            ranges = self.get_value_ranges()
            a = random.randint(*ranges['b'])
            b = random.randint(*ranges['b'])
            expression = f"{a}²x² + {b}²y²"
            correct_answer = f"{a}²x² + {b}²y² (cannot be factored)"
            malrule_answer = f"({a}x + {b}y)²"
        else:
            expression = "x² + y²"
            correct_answer = "x² + y² (prime over reals)"
            malrule_answer = "(x + y)²"

        metadata = {
            'template': 'both_variables',
            'has_coeff': has_coeff,
            'expression': expression,
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer
        }

        return Problem(
            text=f"Factor: {expression}",
            operands=[1, 0, 1],
            operation='factoring',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_larger_coefficients(self, seed=None) -> Problem:
        """Generate x² + b² with larger b (6-10)."""
        if seed is not None:
            random.seed(seed)

        b = random.randint(6, 10)
        b_squared = b**2

        expression = f"x² + {b_squared}"
        correct_answer = f"x² + {b_squared} (cannot be factored)"
        malrule_answer = f"(x + {b})²"

        metadata = {
            'template': 'larger_coefficients',
            'b': b,
            'b_squared': b_squared,
            'expression': expression,
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer
        }

        return Problem(
            text=f"Factor: {expression}",
            operands=[1, 0, b_squared],
            operation='factoring',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_word_problem(self, seed=None) -> Problem:
        """Generate word problem context covering all formula types."""
        if seed is not None:
            random.seed(seed)

        # Select formula type and variant
        formula_types = ['basic_sum_of_squares', 'coefficient_on_x', 'both_variables', 'larger_coefficients']
        formula_type = random.choice(formula_types)
        variant = random.randint(0, 2)

        ranges = self.get_value_ranges()

        if formula_type == 'basic_sum_of_squares':
            b = random.randint(*ranges['b'])
            expression = f"x² + {b**2}"
            correct_answer = f"x² + {b**2} (cannot be factored)"
            malrule_answer = f"(x + {b})²"

            contexts = [
                f"A rectangle has sides of length x and {b}. Express x² + {b**2} in factored form if possible.",
                f"The sum of two squared terms is x² + {b**2}. Can this expression be factored?",
                f"A geometry problem yields x² + {b**2}. Factor if possible."
            ]

            metadata = {
                'template': 'word_problem',
                'b': b,
                'b_squared': b**2,
                'expression': expression,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'is_word_problem': True,
                'word_problem_type': formula_type,
                'word_problem_variant': variant
            }

            return Problem(
                text=contexts[variant],
                operands=[1, 0, b**2],
                operation='factoring',
                level=self.level,
                difficulty=self.difficulty,
                metadata=metadata
            )

        elif formula_type == 'coefficient_on_x':
            a = random.choice([2, 3, 4, 5])
            c = random.randint(*ranges['b'])
            expression = f"{a}x² + {c**2}"
            correct_answer = f"{a}x² + {c**2} (cannot be factored over reals)"
            malrule_answer = f"({a}x + {c})²"

            contexts = [
                f"The expression {a}x² + {c**2} appears in a physics formula. Can it be factored?",
                f"Factor {expression} if possible for a mathematical model.",
                f"A problem yields {expression}. Express in factored form if possible."
            ]

            metadata = {
                'template': 'word_problem',
                'a': a,
                'c': c,
                'c_squared': c**2,
                'expression': expression,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'is_word_problem': True,
                'word_problem_type': formula_type,
                'word_problem_variant': variant
            }

            return Problem(
                text=contexts[variant],
                operands=[a, 0, c**2],
                operation='factoring',
                level=self.level,
                difficulty=self.difficulty,
                metadata=metadata
            )

        elif formula_type == 'both_variables':
            expression = "x² + y²"
            correct_answer = "x² + y² (prime over reals)"
            malrule_answer = "(x + y)²"

            contexts = [
                f"Factor the expression x² + y² that represents the sum of two areas.",
                f"The Pythagorean-like expression x² + y² appears. Can it be factored?",
                f"Express x² + y² in factored form if possible for a geometry problem."
            ]

            metadata = {
                'template': 'word_problem',
                'has_coeff': False,
                'expression': expression,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'is_word_problem': True,
                'word_problem_type': formula_type,
                'word_problem_variant': variant
            }

            return Problem(
                text=contexts[variant],
                operands=[1, 0, 1],
                operation='factoring',
                level=self.level,
                difficulty=self.difficulty,
                metadata=metadata
            )

        else:  # larger_coefficients
            b = random.randint(6, 10)
            b_squared = b**2
            expression = f"x² + {b_squared}"
            correct_answer = f"x² + {b_squared} (cannot be factored)"
            malrule_answer = f"(x + {b})²"

            contexts = [
                f"A mathematical model has expression x² + {b_squared}. Factor if possible.",
                f"The expression x² + {b_squared} appears in an engineering problem. Can it be factored?",
                f"Factor x² + {b_squared} for a physics application if possible."
            ]

            metadata = {
                'template': 'word_problem',
                'b': b,
                'b_squared': b_squared,
                'expression': expression,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'is_word_problem': True,
                'word_problem_type': formula_type,
                'word_problem_variant': variant
            }

            return Problem(
                text=contexts[variant],
                operands=[1, 0, b_squared],
                operation='factoring',
                level=self.level,
                difficulty=self.difficulty,
                metadata=metadata
            )
