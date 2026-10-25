"""
Problem generator for Add-Exponents-For-Power-Of-Power malrule.
"""

import random
import sys
sys.path.append('/home/user/malrule-coding')

from typing import Optional, List
from utils import Problem, ProblemGenerator, DifficultyLevel


class AddExponentsForPowerOfPowerProblemGenerator(ProblemGenerator):
    """
    Generates power of power problems.

    Templates:
    1. basic_power_of_power - Simple (x^m)^n expressions
    2. with_coefficient - Problems like (3x^2)^4
    3. numerical_evaluation - Evaluate with specific base values
    4. product_of_powers - Combining (x^m)^n with x^p
    5. word_problem - Real-world contexts
    """

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_power_of_power',
            'with_coefficient',
            'numerical_evaluation',
            'product_of_powers',
            'word_problem',  # Old word problem (kept for backwards compatibility)
            'word_problem_context'  # NEW: Covers all formula types with 3 variants each
        ]

    def get_value_ranges(self):
        """Return the value ranges for problem generation."""
        if self.difficulty == DifficultyLevel.EASY:
            return {
                'inner_exponent': (2, 3),
                'outer_exponent': (2, 3),
                'coefficient': (1, 1)  # No coefficient for easy
            }
        elif self.difficulty == DifficultyLevel.MEDIUM:
            return {
                'inner_exponent': (2, 5),
                'outer_exponent': (2, 4),
                'coefficient': (1, 3)  # Small coefficients
            }
        else:  # HARD
            return {
                'inner_exponent': (2, 6),
                'outer_exponent': (2, 5),
                'coefficient': (1, 5)  # Larger coefficients
            }

    def generate(self, seed=None, template: Optional[str] = None):
        """Generate a power of power problem."""
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            template = random.choice(self.get_available_templates())

        # Generate based on template
        if template == 'basic_power_of_power':
            return self._generate_basic_power_of_power(seed)
        elif template == 'with_coefficient':
            return self._generate_with_coefficient(seed)
        elif template == 'numerical_evaluation':
            return self._generate_numerical_evaluation(seed)
        elif template == 'product_of_powers':
            return self._generate_product_of_powers(seed)
        elif template == 'word_problem':
            return self._generate_word_problem(seed)
        elif template == 'word_problem_context':
            return self._generate_word_problem_context(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_power_of_power(self, seed=None) -> Problem:
        """Generate basic power of power (x^m)^n."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        inner_exp = random.randint(ranges['inner_exponent'][0], ranges['inner_exponent'][1])
        outer_exp = random.randint(ranges['outer_exponent'][0], ranges['outer_exponent'][1])

        # Ensure inner_exp != outer_exp to avoid cases where m*n = m+n
        while inner_exp == outer_exp:
            outer_exp = random.randint(ranges['outer_exponent'][0], ranges['outer_exponent'][1])

        correct_result_exp = inner_exp * outer_exp
        malrule_result_exp = inner_exp + outer_exp

        problem_statement = f"Simplify: (x^{inner_exp})^{outer_exp}"
        correct_answer = f"x^{correct_result_exp}"
        malrule_answer = f"x^{malrule_result_exp}"

        return Problem(
            text=problem_statement,
            operands=[inner_exp, outer_exp],
            operation='power_of_power',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'coefficient': 1,
                'inner_exponent': inner_exp,
                'outer_exponent': outer_exp,
                'correct_exponent': correct_result_exp,
                'correct_coefficient': 1,
                'malrule_exponent': malrule_result_exp,
                'malrule_coefficient': 1,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'basic_power_of_power'
            }
        )

    def _generate_with_coefficient(self, seed=None) -> Problem:
        """Generate power of power with coefficient (cx^m)^n."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        inner_exp = random.randint(ranges['inner_exponent'][0], ranges['inner_exponent'][1])
        outer_exp = random.randint(ranges['outer_exponent'][0], ranges['outer_exponent'][1])

        # Ensure inner_exp != outer_exp
        while inner_exp == outer_exp:
            outer_exp = random.randint(ranges['outer_exponent'][0], ranges['outer_exponent'][1])

        coeff = random.randint(2, ranges['coefficient'][1])

        correct_result_exp = inner_exp * outer_exp
        correct_result_coeff = coeff ** outer_exp
        malrule_result_exp = inner_exp + outer_exp
        malrule_result_coeff = coeff

        problem_statement = f"Simplify: ({coeff}x^{inner_exp})^{outer_exp}"
        correct_answer = f"{correct_result_coeff}x^{correct_result_exp}"
        malrule_answer = f"{malrule_result_coeff}x^{malrule_result_exp}"

        return Problem(
            text=problem_statement,
            operands=[inner_exp, outer_exp],
            operation='power_of_power',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'coefficient': coeff,
                'inner_exponent': inner_exp,
                'outer_exponent': outer_exp,
                'correct_exponent': correct_result_exp,
                'correct_coefficient': correct_result_coeff,
                'malrule_exponent': malrule_result_exp,
                'malrule_coefficient': malrule_result_coeff,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'with_coefficient'
            }
        )

    def _generate_numerical_evaluation(self, seed=None) -> Problem:
        """Generate numerical evaluation of power of power."""
        if seed is not None:
            random.seed(seed)

        base_values = [2, 3, 4, 5]
        base = random.choice(base_values)
        inner_exp = random.randint(2, 3)
        outer_exp = random.randint(2, 3)

        # Ensure inner_exp != outer_exp to avoid cases where m*n = m+n
        while inner_exp == outer_exp:
            outer_exp = random.randint(2, 3)

        correct_result = base ** (inner_exp * outer_exp)
        malrule_result = base ** (inner_exp + outer_exp)

        problem_statement = f"Evaluate: ({base}^{inner_exp})^{outer_exp}"

        return Problem(
            text=problem_statement,
            operands=[base, inner_exp, outer_exp],
            operation='power_of_power',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'base': base,
                'inner_exponent': inner_exp,
                'outer_exponent': outer_exp,
                'correct_answer': correct_result,
                'malrule_answer': malrule_result,
                'template': 'numerical_evaluation'
            }
        )

    def _generate_product_of_powers(self, seed=None) -> Problem:
        """Generate (x^m)^n × x^p."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        inner_exp = random.randint(ranges['inner_exponent'][0], ranges['inner_exponent'][1])
        outer_exp = random.randint(ranges['outer_exponent'][0], ranges['outer_exponent'][1])

        # Ensure inner_exp != outer_exp
        while inner_exp == outer_exp:
            outer_exp = random.randint(ranges['outer_exponent'][0], ranges['outer_exponent'][1])

        additional_exp = random.randint(2, 4)

        correct_result_exp = inner_exp * outer_exp + additional_exp
        malrule_result_exp = inner_exp + outer_exp + additional_exp

        problem_statement = f"Simplify: (x^{inner_exp})^{outer_exp} × x^{additional_exp}"
        correct_answer = f"x^{correct_result_exp}"
        malrule_answer = f"x^{malrule_result_exp}"

        return Problem(
            text=problem_statement,
            operands=[inner_exp, outer_exp, additional_exp],
            operation='power_of_power',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'inner_exponent': inner_exp,
                'outer_exponent': outer_exp,
                'additional_exponent': additional_exp,
                'correct_exponent': correct_result_exp,
                'malrule_exponent': malrule_result_exp,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'product_of_powers'
            }
        )

    def _generate_word_problem(self, seed=None) -> Problem:
        """Generate word problem with power of power."""
        if seed is not None:
            random.seed(seed)

        contexts = [
            "A bacteria population squares every hour. If it starts at 2^{inner} and this pattern continues for {outer} hours",
            "A number is raised to the {inner} power, then that result is raised to the {outer} power",
            "The area of a square is x^{inner}. What is the area when each side is raised to the {outer} power"
        ]

        context = random.choice(contexts)
        inner_exp = random.randint(2, 4)
        outer_exp = random.randint(2, 3)

        # Ensure inner_exp != outer_exp
        while inner_exp == outer_exp:
            outer_exp = random.randint(2, 3)

        correct_result_exp = inner_exp * outer_exp
        malrule_result_exp = inner_exp + outer_exp

        problem_statement = context.format(inner=inner_exp, outer=outer_exp) + f", what is the exponent in the final expression x^?"
        correct_answer = correct_result_exp
        malrule_answer = malrule_result_exp

        return Problem(
            text=problem_statement,
            operands=[inner_exp, outer_exp],
            operation='power_of_power',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'inner_exponent': inner_exp,
                'outer_exponent': outer_exp,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'word_problem'
            }
        )

    def _generate_word_problem_context(self, seed=None) -> Problem:
        """Generate word problem covering ALL formula types with 3 variants each."""
        if seed is not None:
            random.seed(seed)

        # Select which formula type to embed
        formula_types = ['basic_power_of_power', 'with_coefficient', 'numerical_evaluation', 'product_of_powers']
        formula_type = random.choice(formula_types)
        variant = random.randint(0, 2)  # 3 variants per formula type

        if formula_type == 'basic_power_of_power':
            # Formula: (x^m)^n
            inner_exp = random.randint(2, 4)
            outer_exp = random.randint(2, 3)

            # Ensure inner_exp != outer_exp
            while inner_exp == outer_exp:
                outer_exp = random.randint(2, 3)

            correct_result_exp = inner_exp * outer_exp
            malrule_result_exp = inner_exp + outer_exp

            templates = [
                f"A bacteria colony triples (multiplied by 3^{inner_exp}) each day. After {outer_exp} cycles of this growth pattern, express the total growth factor as a power of 3. What is the exponent?",
                f"A computer algorithm processes data in blocks of size 2^{inner_exp}. If this process repeats {outer_exp} times, express the total processing factor as a power of 2. What is the exponent?",
                f"In a fractal pattern, each iteration scales dimensions by x^{inner_exp}. After {outer_exp} iterations, express the total scaling as x^?. What is the exponent?"
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[inner_exp, outer_exp],
                operation='power_of_power',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'coefficient': 1,
                    'inner_exponent': inner_exp,
                    'outer_exponent': outer_exp,
                    'correct_exponent': correct_result_exp,
                    'correct_coefficient': 1,
                    'malrule_exponent': malrule_result_exp,
                    'malrule_coefficient': 1,
                    'correct_answer': correct_result_exp,
                    'malrule_answer': malrule_result_exp,
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        elif formula_type == 'with_coefficient':
            # Formula: (cx^m)^n
            inner_exp = random.randint(2, 4)
            outer_exp = random.randint(2, 3)

            # Ensure inner_exp != outer_exp
            while inner_exp == outer_exp:
                outer_exp = random.randint(2, 3)

            coeff = random.randint(2, 5)

            correct_result_exp = inner_exp * outer_exp
            correct_result_coeff = coeff ** outer_exp
            malrule_result_exp = inner_exp + outer_exp
            malrule_result_coeff = coeff

            templates = [
                f"A cube with side length {coeff}x^{inner_exp} is scaled by raising all dimensions to the power of {outer_exp}. Express the resulting side length as a simplified expression. What is the coefficient and exponent? (Format: coefficient,exponent)",
                f"A sound wave has amplitude {coeff}A^{inner_exp}. If the wave undergoes {outer_exp} amplification stages (raising to power {outer_exp}), express the final amplitude. What is the coefficient and exponent? (Format: coefficient,exponent)",
                f"The volume formula involves a term ({coeff}r^{inner_exp})^{outer_exp}. Simplify this expression. What is the coefficient and exponent? (Format: coefficient,exponent)"
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[inner_exp, outer_exp],
                operation='power_of_power',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'coefficient': coeff,
                    'inner_exponent': inner_exp,
                    'outer_exponent': outer_exp,
                    'correct_exponent': correct_result_exp,
                    'correct_coefficient': correct_result_coeff,
                    'malrule_exponent': malrule_result_exp,
                    'malrule_coefficient': malrule_result_coeff,
                    'correct_answer': f"{correct_result_coeff},{correct_result_exp}",
                    'malrule_answer': f"{malrule_result_coeff},{malrule_result_exp}",
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        elif formula_type == 'numerical_evaluation':
            # Formula: (base^m)^n = base^(m*n)
            base_values = [2, 3, 4, 5]
            base = random.choice(base_values)
            inner_exp = random.randint(2, 3)
            outer_exp = random.randint(2, 3)

            # Ensure inner_exp != outer_exp
            while inner_exp == outer_exp:
                outer_exp = random.randint(2, 3)

            correct_result = base ** (inner_exp * outer_exp)
            malrule_result = base ** (inner_exp + outer_exp)

            templates = [
                f"A city's population is ({base}^{inner_exp})^{outer_exp} thousand people. Calculate the actual population in thousands.",
                f"A server processes ({base}^{inner_exp})^{outer_exp} requests per second. Calculate the number of requests.",
                f"The energy output of a reactor is ({base}^{inner_exp})^{outer_exp} megawatts. Calculate the total energy output."
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[base, inner_exp, outer_exp],
                operation='power_of_power',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'base': base,
                    'inner_exponent': inner_exp,
                    'outer_exponent': outer_exp,
                    'correct_answer': correct_result,
                    'malrule_answer': malrule_result,
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        else:  # product_of_powers
            # Formula: (x^m)^n × x^p
            inner_exp = random.randint(2, 4)
            outer_exp = random.randint(2, 3)

            # Ensure inner_exp != outer_exp
            while inner_exp == outer_exp:
                outer_exp = random.randint(2, 3)

            additional_exp = random.randint(2, 4)

            correct_result_exp = inner_exp * outer_exp + additional_exp
            malrule_result_exp = inner_exp + outer_exp + additional_exp

            templates = [
                f"A bacteria colony grows by a factor of (x^{inner_exp})^{outer_exp} in the first phase and x^{additional_exp} in the second phase. Express the total growth factor as x^?. What is the exponent?",
                f"Two machines process data: Machine A processes (x^{inner_exp})^{outer_exp} units, Machine B processes x^{additional_exp} units. The combined processing is their product. Express as x^?. What is the exponent?",
                f"A rocket's velocity increases by (v^{inner_exp})^{outer_exp} in stage 1, then multiplied by v^{additional_exp} in stage 2. Express the total velocity factor as v^?. What is the exponent?"
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[inner_exp, outer_exp, additional_exp],
                operation='power_of_power',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'inner_exponent': inner_exp,
                    'outer_exponent': outer_exp,
                    'additional_exponent': additional_exp,
                    'correct_exponent': correct_result_exp,
                    'malrule_exponent': malrule_result_exp,
                    'correct_answer': correct_result_exp,
                    'malrule_answer': malrule_result_exp,
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )
