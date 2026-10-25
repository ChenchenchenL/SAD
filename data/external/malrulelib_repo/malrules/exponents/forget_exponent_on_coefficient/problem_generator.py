"""
Problem generator for Forget-Exponent-On-Coefficient malrule.
"""

import random
import sys
sys.path.append('/home/user/malrule-coding')

from typing import Optional, List
from utils import Problem, ProblemGenerator


class ForgetExponentOnCoefficientProblemGenerator(ProblemGenerator):
    """
    Generates (cx^m)^n problems where students forget to raise coefficient.

    Templates:
    1. basic_power_of_power - Simple (cx^m)^n with small coefficients
    2. larger_coefficients - Problems with larger coefficients (6-10)
    3. negative_coefficient - Problems with negative coefficients
    4. multiple_variables - Problems with multiple variables (xy terms)
    5. word_problem - Real-world contexts (area, volume, growth)
    """

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_power_of_power',
            'larger_coefficients',
            'negative_coefficient',
            'multiple_variables',
            'word_problem',  # Old word problem (kept for backwards compatibility)
            'word_problem_context'  # NEW: Covers all formula types with 3 variants each
        ]

    def get_value_ranges(self):
        """Return the value ranges for problem generation."""
        return {
            'coefficient': (2, 5),
            'base_exponent': (2, 4),
            'outer_exponent': (2, 4)
        }

    def generate(self, seed=None, template: Optional[str] = None):
        """Generate a power of power problem with coefficient."""
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            template = random.choice(self.get_available_templates())

        # Generate based on template
        if template == 'basic_power_of_power':
            return self._generate_basic_power_of_power(seed)
        elif template == 'larger_coefficients':
            return self._generate_larger_coefficients(seed)
        elif template == 'negative_coefficient':
            return self._generate_negative_coefficient(seed)
        elif template == 'multiple_variables':
            return self._generate_multiple_variables(seed)
        elif template == 'word_problem':
            return self._generate_word_problem(seed)
        elif template == 'word_problem_context':
            return self._generate_word_problem_context(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_power_of_power(self, seed=None) -> Problem:
        """Generate basic (cx^m)^n with small coefficients."""
        if seed is not None:
            random.seed(seed)

        coefficient = random.randint(2, 5)
        base_exponent = random.randint(2, 4)
        outer_exponent = random.randint(2, 4)

        # Calculate correct answer: (cx^m)^n = c^n · x^(m·n)
        new_coefficient = coefficient ** outer_exponent
        new_exponent = base_exponent * outer_exponent
        correct_answer = f"{new_coefficient}x^{new_exponent}"

        # Calculate malrule answer: c · x^(m·n) (forgot to raise coefficient)
        malrule_answer = f"{coefficient}x^{new_exponent}"

        problem_statement = f"Simplify: ({coefficient}x^{base_exponent})^{outer_exponent}"

        return Problem(
            text=problem_statement,
            operands=[coefficient, base_exponent, outer_exponent],
            operation='power_of_power',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'coefficient': coefficient,
                'base_exponent': base_exponent,
                'outer_exponent': outer_exponent,
                'new_coefficient': new_coefficient,
                'new_exponent': new_exponent,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'basic_power_of_power'
            }
        )

    def _generate_larger_coefficients(self, seed=None) -> Problem:
        """Generate problems with larger coefficients (6-10)."""
        if seed is not None:
            random.seed(seed)

        coefficient = random.randint(6, 10)
        base_exponent = random.randint(2, 3)
        outer_exponent = random.randint(2, 3)

        new_coefficient = coefficient ** outer_exponent
        new_exponent = base_exponent * outer_exponent
        correct_answer = f"{new_coefficient}x^{new_exponent}"
        malrule_answer = f"{coefficient}x^{new_exponent}"

        problem_statement = f"Simplify: ({coefficient}x^{base_exponent})^{outer_exponent}"

        return Problem(
            text=problem_statement,
            operands=[coefficient, base_exponent, outer_exponent],
            operation='power_of_power',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'coefficient': coefficient,
                'base_exponent': base_exponent,
                'outer_exponent': outer_exponent,
                'new_coefficient': new_coefficient,
                'new_exponent': new_exponent,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'larger_coefficients'
            }
        )

    def _generate_negative_coefficient(self, seed=None) -> Problem:
        """Generate problems with negative coefficients."""
        if seed is not None:
            random.seed(seed)

        coefficient = -random.randint(2, 5)
        base_exponent = random.randint(2, 4)
        outer_exponent = random.randint(2, 4)

        new_coefficient = coefficient ** outer_exponent
        new_exponent = base_exponent * outer_exponent

        # Format with proper signs
        if new_coefficient >= 0:
            correct_answer = f"{new_coefficient}x^{new_exponent}"
        else:
            correct_answer = f"{new_coefficient}x^{new_exponent}"

        if coefficient >= 0:
            malrule_answer = f"{coefficient}x^{new_exponent}"
        else:
            malrule_answer = f"{coefficient}x^{new_exponent}"

        problem_statement = f"Simplify: ({coefficient}x^{base_exponent})^{outer_exponent}"

        return Problem(
            text=problem_statement,
            operands=[coefficient, base_exponent, outer_exponent],
            operation='power_of_power',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'coefficient': coefficient,
                'base_exponent': base_exponent,
                'outer_exponent': outer_exponent,
                'new_coefficient': new_coefficient,
                'new_exponent': new_exponent,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'negative_coefficient'
            }
        )

    def _generate_multiple_variables(self, seed=None) -> Problem:
        """Generate problems with multiple variables like (2xy^2)^3."""
        if seed is not None:
            random.seed(seed)

        coefficient = random.randint(2, 5)
        x_exponent = random.randint(1, 3)
        y_exponent = random.randint(1, 3)
        outer_exponent = random.randint(2, 3)

        new_coefficient = coefficient ** outer_exponent
        new_x_exponent = x_exponent * outer_exponent
        new_y_exponent = y_exponent * outer_exponent

        # Format x part
        if x_exponent == 1:
            x_part = "x"
            new_x_part = f"x^{new_x_exponent}"
        else:
            x_part = f"x^{x_exponent}"
            new_x_part = f"x^{new_x_exponent}"

        # Format y part
        if y_exponent == 1:
            y_part = "y"
            new_y_part = f"y^{new_y_exponent}"
        else:
            y_part = f"y^{y_exponent}"
            new_y_part = f"y^{new_y_exponent}"

        correct_answer = f"{new_coefficient}{new_x_part}{new_y_part}"
        malrule_answer = f"{coefficient}{new_x_part}{new_y_part}"

        problem_statement = f"Simplify: ({coefficient}{x_part}{y_part})^{outer_exponent}"

        return Problem(
            text=problem_statement,
            operands=[coefficient, x_exponent, y_exponent, outer_exponent],
            operation='power_of_power',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'coefficient': coefficient,
                'x_exponent': x_exponent,
                'y_exponent': y_exponent,
                'outer_exponent': outer_exponent,
                'new_coefficient': new_coefficient,
                'new_x_exponent': new_x_exponent,
                'new_y_exponent': new_y_exponent,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'multiple_variables'
            }
        )

    def _generate_word_problem(self, seed=None) -> Problem:
        """Generate real-world word problem contexts."""
        if seed is not None:
            random.seed(seed)

        contexts = [
            {
                'text': 'The area of a square is {c}x^{m}. If you scale each side by x^{n}, what is the new area?',
                'context_type': 'area_scaling'
            },
            {
                'text': 'A cube has side length {c}x^{m}. If each dimension is raised to the {n} power, what is the expression for volume?',
                'context_type': 'volume'
            },
            {
                'text': 'A bacteria population grows by a factor of {c}x^{m} per hour. After {n} compounding periods, what is the growth factor?',
                'context_type': 'growth'
            }
        ]

        context = random.choice(contexts)
        coefficient = random.randint(2, 5)
        base_exponent = random.randint(2, 3)
        outer_exponent = random.randint(2, 3)

        new_coefficient = coefficient ** outer_exponent
        new_exponent = base_exponent * outer_exponent

        correct_answer = f"{new_coefficient}x^{new_exponent}"
        malrule_answer = f"{coefficient}x^{new_exponent}"

        problem_text = context['text'].format(c=coefficient, m=base_exponent, n=outer_exponent)

        return Problem(
            text=problem_text,
            operands=[coefficient, base_exponent, outer_exponent],
            operation='power_of_power',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'coefficient': coefficient,
                'base_exponent': base_exponent,
                'outer_exponent': outer_exponent,
                'new_coefficient': new_coefficient,
                'new_exponent': new_exponent,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'context_type': context['context_type'],
                'template': 'word_problem'
            }
        )

    def _generate_word_problem_context(self, seed=None) -> Problem:
        """Generate word problem covering ALL formula types with 3 variants each."""
        if seed is not None:
            random.seed(seed)

        # Select which formula type to embed
        formula_types = ['basic_power_of_power', 'larger_coefficients', 'negative_coefficient', 'multiple_variables']
        formula_type = random.choice(formula_types)
        variant = random.randint(0, 2)  # 3 variants per formula type

        if formula_type == 'basic_power_of_power':
            # Formula: (cx^m)^n with small coefficients (2-5)
            coefficient = random.randint(2, 5)
            base_exponent = random.randint(2, 4)
            outer_exponent = random.randint(2, 4)

            new_coefficient = coefficient ** outer_exponent
            new_exponent = base_exponent * outer_exponent
            correct_answer = f"{new_coefficient}x^{new_exponent}"
            malrule_answer = f"{coefficient}x^{new_exponent}"

            templates = [
                f"A sound wave has amplitude {coefficient}A^{base_exponent}. After passing through {outer_exponent} amplification stages (each raising to power {outer_exponent}), what is the final amplitude expression?",
                f"The surface area of a shape scales by ({coefficient}x^{base_exponent})^{outer_exponent}. Simplify this scaling factor.",
                f"In a physics experiment, energy increases by a factor of ({coefficient}E^{base_exponent})^{outer_exponent}. Express the total energy factor in simplified form."
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[coefficient, base_exponent, outer_exponent],
                operation='power_of_power',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'coefficient': coefficient,
                    'base_exponent': base_exponent,
                    'outer_exponent': outer_exponent,
                    'new_coefficient': new_coefficient,
                    'new_exponent': new_exponent,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        elif formula_type == 'larger_coefficients':
            # Formula: (cx^m)^n with larger coefficients (6-10)
            coefficient = random.randint(6, 10)
            base_exponent = random.randint(2, 3)
            outer_exponent = random.randint(2, 3)

            new_coefficient = coefficient ** outer_exponent
            new_exponent = base_exponent * outer_exponent
            correct_answer = f"{new_coefficient}x^{new_exponent}"
            malrule_answer = f"{coefficient}x^{new_exponent}"

            templates = [
                f"A bacteria colony multiplies by {coefficient}N^{base_exponent} each generation. After {outer_exponent} consecutive generations (raising the entire expression to power {outer_exponent}), what is the total multiplication factor?",
                f"The volume of a gas expands by ({coefficient}V^{base_exponent})^{outer_exponent} under certain conditions. Simplify this expansion factor.",
                f"A computer algorithm's complexity scales as ({coefficient}n^{base_exponent})^{outer_exponent}. Express this in simplified form."
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[coefficient, base_exponent, outer_exponent],
                operation='power_of_power',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'coefficient': coefficient,
                    'base_exponent': base_exponent,
                    'outer_exponent': outer_exponent,
                    'new_coefficient': new_coefficient,
                    'new_exponent': new_exponent,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        elif formula_type == 'negative_coefficient':
            # Formula: (-cx^m)^n with negative coefficients
            coefficient = -random.randint(2, 5)
            base_exponent = random.randint(2, 4)
            outer_exponent = random.randint(2, 4)

            new_coefficient = coefficient ** outer_exponent
            new_exponent = base_exponent * outer_exponent

            # Format with proper signs
            if new_coefficient >= 0:
                correct_answer = f"{new_coefficient}x^{new_exponent}"
            else:
                correct_answer = f"{new_coefficient}x^{new_exponent}"

            if coefficient >= 0:
                malrule_answer = f"{coefficient}x^{new_exponent}"
            else:
                malrule_answer = f"{coefficient}x^{new_exponent}"

            templates = [
                f"A wave has amplitude ({coefficient}A^{base_exponent})^{outer_exponent} (negative indicating direction). Simplify this expression.",
                f"In quantum mechanics, a phase factor is ({coefficient}ψ^{base_exponent})^{outer_exponent}. Express this in simplified form.",
                f"A financial model uses the expression ({coefficient}x^{base_exponent})^{outer_exponent} to represent loss. Simplify this expression."
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[coefficient, base_exponent, outer_exponent],
                operation='power_of_power',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'coefficient': coefficient,
                    'base_exponent': base_exponent,
                    'outer_exponent': outer_exponent,
                    'new_coefficient': new_coefficient,
                    'new_exponent': new_exponent,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        else:  # multiple_variables
            # Formula: (cxy^m)^n with multiple variables
            coefficient = random.randint(2, 5)
            x_exponent = random.randint(1, 3)
            y_exponent = random.randint(1, 3)
            outer_exponent = random.randint(2, 3)

            new_coefficient = coefficient ** outer_exponent
            new_x_exponent = x_exponent * outer_exponent
            new_y_exponent = y_exponent * outer_exponent

            # Format x part
            if x_exponent == 1:
                x_part = "x"
                new_x_part = f"x^{new_x_exponent}"
            else:
                x_part = f"x^{x_exponent}"
                new_x_part = f"x^{new_x_exponent}"

            # Format y part
            if y_exponent == 1:
                y_part = "y"
                new_y_part = f"y^{new_y_exponent}"
            else:
                y_part = f"y^{y_exponent}"
                new_y_part = f"y^{new_y_exponent}"

            correct_answer = f"{new_coefficient}{new_x_part}{new_y_part}"
            malrule_answer = f"{coefficient}{new_x_part}{new_y_part}"

            templates = [
                f"The area of a rectangle is {coefficient}{x_part}{y_part}. When both dimensions are raised to the {outer_exponent} power, express the new area.",
                f"A gravitational field strength is ({coefficient}{x_part}{y_part})^{outer_exponent}. Simplify this expression.",
                f"The resistance in a circuit follows ({coefficient}{x_part}{y_part})^{outer_exponent}. Express this in simplified form."
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[coefficient, x_exponent, y_exponent, outer_exponent],
                operation='power_of_power',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'coefficient': coefficient,
                    'x_exponent': x_exponent,
                    'y_exponent': y_exponent,
                    'outer_exponent': outer_exponent,
                    'new_coefficient': new_coefficient,
                    'new_x_exponent': new_x_exponent,
                    'new_y_exponent': new_y_exponent,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )
