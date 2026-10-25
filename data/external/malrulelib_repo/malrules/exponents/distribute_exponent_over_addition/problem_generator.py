"""
Problem generator for Distribute-Exponent-Over-Addition malrule.
"""

import random
import sys
sys.path.append('/home/user/malrule-coding')

from utils import Problem, ProblemGenerator


class DistributeExponentOverAdditionProblemGenerator(ProblemGenerator):
    """Generates problems with exponents over sums."""

    def get_value_ranges(self):
        """Return the value ranges for problem generation."""
        return {
            'a': (1, 10),
            'b': (1, 10),
            'exponent': (2, 3)
        }

    def get_available_templates(self):
        """Return list of available problem templates."""
        templates = ['simple_two_term']
        if self.level >= 8:
            templates.extend([
                'three_term_square',
                'higher_power',
                'word_problem_pythagorean',
                'word_problem_area',
                'word_problem_context'  # NEW: Comprehensive word problems
            ])
        return templates

    def generate(self, seed=None, template=None):
        """
        Generate an exponent over sum problem.

        Args:
            seed: Optional random seed for reproducibility
            template: Optional template name. If None, random template is chosen.

        Returns:
            Problem with (a+b)^n expression
        """
        if seed is not None:
            random.seed(seed)

        # Choose problem type from available templates
        problem_types = self.get_available_templates()

        if template is None:
            problem_type = random.choice(problem_types)
        else:
            if template in problem_types:
                problem_type = template
            else:
                raise ValueError(f"Template '{template}' not in available templates: {problem_types}")

        if problem_type == 'simple_two_term':
            # Generate values
            a = random.randint(1, 10)
            b = random.randint(1, 10)
            exponent = random.randint(2, 3)  # Keep it 2 or 3 for reasonable numbers

            # Calculate correct answer: (a+b)^n
            sum_value = a + b
            correct_answer = sum_value ** exponent

            # Calculate malrule answer: a^n + b^n (incorrect distribution)
            malrule_answer = (a ** exponent) + (b ** exponent)

            # Create problem statement
            problem_statement = f"Evaluate: ({a} + {b})^{exponent}"

        elif problem_type == 'three_term_square':
            # Three terms with exponent 2: (a+b+c)^2
            a = random.randint(1, 5)
            b = random.randint(1, 5)
            c = random.randint(1, 5)
            exponent = 2

            # Calculate correct answer: (a+b+c)^2
            sum_value = a + b + c
            correct_answer = sum_value ** exponent

            # Calculate malrule answer: a^2 + b^2 + c^2 (incorrect distribution)
            malrule_answer = (a ** exponent) + (b ** exponent) + (c ** exponent)

            problem_statement = f"Evaluate: ({a} + {b} + {c})^{exponent}"

        elif problem_type == 'higher_power':
            # Use smaller numbers with higher powers
            a = random.randint(1, 4)
            b = random.randint(1, 4)
            exponent = random.choice([4, 5])

            # Calculate correct answer: (a+b)^n
            sum_value = a + b
            correct_answer = sum_value ** exponent

            # Calculate malrule answer: a^n + b^n
            malrule_answer = (a ** exponent) + (b ** exponent)

            problem_statement = f"Evaluate: ({a} + {b})^{exponent}"

        elif problem_type == 'word_problem_pythagorean':
            # Context that might confuse with Pythagorean theorem
            a = random.choice([3, 5, 6, 8])
            b = random.choice([4, 5, 7, 9])
            exponent = 2

            sum_value = a + b
            correct_answer = sum_value ** exponent
            malrule_answer = (a ** exponent) + (b ** exponent)

            contexts = [
                f"Calculate (length₁ + length₂)² where length₁ = {a} and length₂ = {b}. What is ({a} + {b})²?",
                f"If side A = {a} and side B = {b}, what is (A + B)²? Evaluate: ({a} + {b})²",
                f"Sum of two measurements: {a} and {b}. Square the sum: ({a} + {b})² = ?",
            ]
            problem_statement = random.choice(contexts)

        elif problem_type == 'word_problem_area':
            # Area/geometry context with sums
            a = random.randint(2, 8)
            b = random.randint(2, 8)
            exponent = 2

            sum_value = a + b
            correct_answer = sum_value ** exponent
            malrule_answer = (a ** exponent) + (b ** exponent)

            contexts = [
                f"A square has side length ({a} + {b}) cm. What is its area? Evaluate: ({a} + {b})²",
                f"Area of square with side = {a} + {b}. Calculate: ({a} + {b})² = ?",
                f"If the side length is ({a} + {b}), find the area: ({a} + {b})²",
            ]
            problem_statement = random.choice(contexts)

        elif problem_type == 'word_problem_context':
            # NEW: Comprehensive word problems covering all formula types
            return self._generate_word_problem_context(seed)

        else:  # Default fallback
            a = random.randint(1, 10)
            b = random.randint(1, 10)
            exponent = random.randint(2, 3)
            sum_value = a + b
            correct_answer = sum_value ** exponent
            malrule_answer = (a ** exponent) + (b ** exponent)
            problem_statement = f"Evaluate: ({a} + {b})^{exponent}"

        # Create metadata
        metadata = {
            'a': a,
            'b': b,
            'exponent': exponent,
            'sum_value': sum_value if 'sum_value' in locals() else a + b,
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer,
            'problem_type': problem_type
        }

        # Add 'c' if it exists (three-term problems)
        if 'c' in locals():
            metadata['c'] = c

        return Problem(
            text=problem_statement,
            operands=[a, b, exponent],
            operation='exponent_over_sum',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_word_problem_context(self, seed=None):
        """Generate word problem covering ALL formula types with 3 variants each."""
        if seed is not None:
            random.seed(seed)

        # Select which formula type to embed
        formula_types = ['simple_two_term', 'three_term_square', 'higher_power']
        formula_type = random.choice(formula_types)
        variant = random.randint(0, 2)  # 3 variants per formula type

        if formula_type == 'simple_two_term':
            # Formula: (a+b)^n
            a = random.randint(2, 8)
            b = random.randint(2, 8)
            exponent = random.randint(2, 3)

            sum_value = a + b
            correct_answer = sum_value ** exponent
            malrule_answer = (a ** exponent) + (b ** exponent)

            # 3 diverse real-world contexts
            templates = [
                # Variant 0: Finance/Investment
                f"An investment grows by ${a} thousand in year 1 and ${b} thousand in year 2, totaling ${a}+{b}=${sum_value} thousand growth. If this growth pattern compounds {exponent} times, the total effect is ({a}+{b})^{exponent}. Calculate this value.",
                # Variant 1: Physics/Engineering
                f"Two force vectors of {a} N and {b} N combine additively. The combined force of {sum_value} N is then amplified by a factor of {exponent} through mechanical advantage. Calculate ({a}+{b})^{exponent}.",
                # Variant 2: Computer Science/Data
                f"A server processes {a} GB in phase 1 and {b} GB in phase 2 (total: {sum_value} GB). This data volume is replicated across {exponent} redundant systems with exponential scaling. Calculate ({a}+{b})^{exponent}."
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[a, b, exponent],
                operation='exponent_over_sum',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'a': a,
                    'b': b,
                    'exponent': exponent,
                    'sum_value': sum_value,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'problem_type': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        elif formula_type == 'three_term_square':
            # Formula: (a+b+c)^2
            a = random.randint(1, 5)
            b = random.randint(1, 5)
            c = random.randint(1, 5)
            exponent = 2

            sum_value = a + b + c
            correct_answer = sum_value ** exponent
            malrule_answer = (a ** exponent) + (b ** exponent) + (c ** exponent)

            # 3 diverse real-world contexts
            templates = [
                # Variant 0: Economics/Business
                f"A company has three revenue streams: ${a}M, ${b}M, and ${c}M (total: ${sum_value}M). A market analysis projects the square of total revenue for risk assessment. Calculate ({a}+{b}+{c})^{exponent}.",
                # Variant 1: Chemistry/Science
                f"Three chemical components have concentrations of {a} mol/L, {b} mol/L, and {c} mol/L. The reaction rate is proportional to the square of the total concentration ({sum_value} mol/L). Calculate ({a}+{b}+{c})^{exponent}.",
                # Variant 2: Urban Planning/Architecture
                f"Three city zones have population densities of {a}, {b}, and {c} thousand per square mile (total: {sum_value} thousand). Infrastructure needs scale with the square of total density. Calculate ({a}+{b}+{c})^{exponent}."
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[a, b, exponent],
                operation='exponent_over_sum',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'a': a,
                    'b': b,
                    'c': c,
                    'exponent': exponent,
                    'sum_value': sum_value,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'problem_type': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        else:  # higher_power
            # Formula: (a+b)^n where n > 3
            a = random.randint(1, 4)
            b = random.randint(1, 4)
            exponent = random.choice([4, 5])

            sum_value = a + b
            correct_answer = sum_value ** exponent
            malrule_answer = (a ** exponent) + (b ** exponent)

            # 3 diverse real-world contexts
            templates = [
                # Variant 0: Astronomy/Space
                f"Two stellar mass measurements are {a} and {b} solar masses (total: {sum_value}). The gravitational field strength varies with the {exponent}th power of total mass. Calculate ({a}+{b})^{exponent}.",
                # Variant 1: Electrical Engineering
                f"Two resistances of {a} ohms and {b} ohms combine in series (total: {sum_value} ohms). A power calculation requires the {exponent}th power of total resistance. Calculate ({a}+{b})^{exponent}.",
                # Variant 2: Cryptography/Security
                f"A security key combines {a} and {b} entropy bits (total: {sum_value} bits). The encryption strength is ({sum_value})^{exponent}. Calculate ({a}+{b})^{exponent}."
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[a, b, exponent],
                operation='exponent_over_sum',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'a': a,
                    'b': b,
                    'exponent': exponent,
                    'sum_value': sum_value,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'problem_type': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )
