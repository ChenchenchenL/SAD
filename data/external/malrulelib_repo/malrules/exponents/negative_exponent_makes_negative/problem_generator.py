"""
Problem generator for Negative-Exponent-Makes-Negative malrule.
"""

import random
import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import Problem, ProblemGenerator
from fractions import Fraction


class NegativeExponentMakesNegativeProblemGenerator(ProblemGenerator):
    """Generates negative exponent problems."""

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'simple_numeric',
            'larger_negative_exponent',
            'fractional_base',
            'word_problem_scientific',  # Old word problem (kept for backwards compatibility)
            'word_problem_finance',     # Old word problem (kept for backwards compatibility)
            'word_problem_context'      # NEW: Covers all formula types with 3 variants each
        ]

    def get_value_ranges(self):
        """Return the value ranges for problem generation."""
        return {
            'base': (2, 5),
            'exponent': (1, 3)
        }

    def generate(self, seed=None, template=None):
        """
        Generate a negative exponent problem.

        Args:
            seed: Optional random seed for reproducibility
            template: Optional specific template to use

        Returns:
            Problem with negative exponent
        """
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            # Choose problem type
            problem_types = ['simple_numeric']

            # Add enhanced problem types for higher levels
            if self.level >= 8:
                problem_types.extend([
                    'larger_negative_exponent',    # Larger negative exponents (-4 to -6)
                    'fractional_base',             # Fractional bases like (1/2)^-2
                    'word_problem_scientific',     # Scientific/bacteria growth contexts
                    'word_problem_finance',        # Investment/depreciation contexts
                    'word_problem_context'         # NEW: Contextual word problems for all formula types
                ])

            problem_type = random.choice(problem_types)
        else:
            problem_type = template

        # Handle word_problem_context template
        if problem_type == 'word_problem_context':
            return self._generate_word_problem_context(seed)

        if problem_type == 'simple_numeric':
            # Generate base and positive exponent, then negate
            base = random.randint(2, 5)
            positive_exp = random.randint(1, 3)
            negative_exp = -positive_exp

            # Calculate correct answer: base^(-n) = 1/(base^n)
            denominator = base ** positive_exp
            correct_answer_fraction = f"1/{denominator}"
            correct_answer_decimal = 1 / denominator

            # Calculate malrule answer: student thinks it makes negative
            # They compute base^n and negate it
            malrule_answer = -(base ** positive_exp)

            # Create problem statement
            problem_statement = f"Evaluate: {base}^{negative_exp}"

        elif problem_type == 'larger_negative_exponent':
            # Use smaller bases with larger negative exponents
            base = random.choice([2, 3])
            positive_exp = random.randint(4, 6)
            negative_exp = -positive_exp

            denominator = base ** positive_exp
            correct_answer_fraction = f"1/{denominator}"
            correct_answer_decimal = 1 / denominator
            malrule_answer = -(base ** positive_exp)

            problem_statement = f"Evaluate: {base}^{negative_exp}"

        elif problem_type == 'fractional_base':
            # Use fractional bases like (1/2), (1/3), (1/4)
            denominator_base = random.choice([2, 3, 4])
            positive_exp = random.randint(2, 3)
            negative_exp = -positive_exp

            # For (1/n)^(-k), the correct answer is n^k
            # Example: (1/2)^(-2) = 2^2 = 4
            correct_answer_value = denominator_base ** positive_exp
            correct_answer_fraction = str(correct_answer_value)
            correct_answer_decimal = float(correct_answer_value)

            # Malrule: student thinks negative exponent makes result negative
            # They might compute (1/n)^k and negate it
            malrule_answer = -(1 / (denominator_base ** positive_exp))

            # Store numeric base value for computation
            base_numeric = 1 / denominator_base
            base_display = f"(1/{denominator_base})"
            problem_statement = f"Evaluate: {base_display}^{negative_exp}"
            base = base_numeric  # Use numeric value for algorithm computation

        elif problem_type == 'word_problem_scientific':
            # Scientific notation / exponential decay contexts
            base = random.choice([2, 10])
            positive_exp = random.randint(2, 4)
            negative_exp = -positive_exp

            denominator = base ** positive_exp
            correct_answer_fraction = f"1/{denominator}"
            correct_answer_decimal = 1 / denominator
            malrule_answer = -(base ** positive_exp)

            contexts = [
                f"A microscopic organism shrinks by a factor of {base}^{negative_exp} each cycle. What is {base}^{negative_exp}?",
                f"In scientific notation, calculate: {base}^{negative_exp}",
                f"Half-life decay: concentration = {base}^{negative_exp}. Calculate the value.",
            ]
            problem_statement = random.choice(contexts)

        elif problem_type == 'word_problem_finance':
            # Investment/depreciation contexts
            base = random.choice([2, 3, 4, 5])
            positive_exp = random.randint(1, 3)
            negative_exp = -positive_exp

            denominator = base ** positive_exp
            correct_answer_fraction = f"1/{denominator}"
            correct_answer_decimal = 1 / denominator
            malrule_answer = -(base ** positive_exp)

            contexts = [
                f"An investment decreases by factor {base}^{negative_exp}. What is this factor as a decimal?",
                f"Depreciation factor: {base}^{negative_exp}. Calculate the value.",
                f"Value multiplier = {base}^{negative_exp}. What does this equal?",
            ]
            problem_statement = random.choice(contexts)

        else:  # Default fallback
            base = random.randint(2, 5)
            positive_exp = random.randint(1, 3)
            negative_exp = -positive_exp
            denominator = base ** positive_exp
            correct_answer_fraction = f"1/{denominator}"
            correct_answer_decimal = 1 / denominator
            malrule_answer = -(base ** positive_exp)
            problem_statement = f"Evaluate: {base}^{negative_exp}"

        # Create metadata
        metadata = {
            'base': base,  # Numeric base for computation
            'negative_exp': negative_exp,
            'positive_exp': positive_exp,
            'correct_answer_fraction': correct_answer_fraction,
            'correct_answer_decimal': correct_answer_decimal,
            'malrule_answer': malrule_answer,
            'problem_type': problem_type
        }

        # Determine operands - for fractional bases, use the denominator value
        if problem_type == 'fractional_base':
            operand_base = denominator_base if 'denominator_base' in locals() else 2
        else:
            operand_base = base if isinstance(base, int) else 2

        return Problem(
            text=problem_statement,
            operands=[operand_base, negative_exp],
            operation='negative_exponent',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_word_problem_context(self, seed=None) -> Problem:
        """Generate word problem covering ALL formula types with 3 variants each."""
        if seed is not None:
            random.seed(seed)

        # Select which formula type to embed
        formula_types = ['simple_numeric', 'larger_negative_exponent', 'fractional_base']
        formula_type = random.choice(formula_types)
        variant = random.randint(0, 2)  # 3 variants per formula type

        if formula_type == 'simple_numeric':
            # Formula: base^(-n) where base is 2-5, n is 1-3
            base = random.randint(2, 5)
            positive_exp = random.randint(1, 3)
            negative_exp = -positive_exp

            denominator = base ** positive_exp
            correct_answer_fraction = f"1/{denominator}"
            correct_answer_decimal = 1 / denominator
            malrule_answer = -(base ** positive_exp)

            templates = [
                f"A radioactive substance decays by a factor of {base}^{negative_exp} each hour. Express this decay factor as a fraction. What is the value?",
                f"The concentration of a chemical solution is diluted by {base}^{negative_exp}. Calculate the dilution factor as a decimal.",
                f"A computer's processing speed decreases by a factor of {base}^{negative_exp} when running in power-saving mode. What is this factor?"
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[base, negative_exp],
                operation='negative_exponent',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'base': base,
                    'negative_exp': negative_exp,
                    'positive_exp': positive_exp,
                    'correct_answer_fraction': correct_answer_fraction,
                    'correct_answer_decimal': correct_answer_decimal,
                    'malrule_answer': malrule_answer,
                    'problem_type': 'simple_numeric',
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        elif formula_type == 'larger_negative_exponent':
            # Formula: base^(-n) where base is 2-3, n is 4-6
            base = random.choice([2, 3])
            positive_exp = random.randint(4, 6)
            negative_exp = -positive_exp

            denominator = base ** positive_exp
            correct_answer_fraction = f"1/{denominator}"
            correct_answer_decimal = 1 / denominator
            malrule_answer = -(base ** positive_exp)

            templates = [
                f"In scientific notation, a particle's size is {base}^{negative_exp} meters. Calculate this value as a decimal.",
                f"The probability of a rare event is {base}^{negative_exp}. What is this probability as a fraction?",
                f"A sound wave's intensity decreases by {base}^{negative_exp} at a certain distance. Calculate the intensity factor."
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[base, negative_exp],
                operation='negative_exponent',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'base': base,
                    'negative_exp': negative_exp,
                    'positive_exp': positive_exp,
                    'correct_answer_fraction': correct_answer_fraction,
                    'correct_answer_decimal': correct_answer_decimal,
                    'malrule_answer': malrule_answer,
                    'problem_type': 'larger_negative_exponent',
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        else:  # fractional_base
            # Formula: (1/n)^(-k) where n is 2-4, k is 2-3
            denominator_base = random.choice([2, 3, 4])
            positive_exp = random.randint(2, 3)
            negative_exp = -positive_exp

            # For (1/n)^(-k), the correct answer is n^k
            correct_answer_value = denominator_base ** positive_exp
            correct_answer_fraction = str(correct_answer_value)
            correct_answer_decimal = float(correct_answer_value)

            # Malrule: student thinks negative exponent makes result negative
            malrule_answer = -(1 / (denominator_base ** positive_exp))

            base_numeric = 1 / denominator_base
            base_display = f"(1/{denominator_base})"

            templates = [
                f"An asset's value appreciates by a factor of {base_display}^{negative_exp} each year. Calculate this appreciation factor.",
                f"The resistance in a circuit changes by {base_display}^{negative_exp}. What is this change factor?",
                f"A lens magnifies by a power of {base_display}^{negative_exp}. Calculate the magnification factor."
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[denominator_base, negative_exp],
                operation='negative_exponent',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'base': base_numeric,
                    'negative_exp': negative_exp,
                    'positive_exp': positive_exp,
                    'correct_answer_fraction': correct_answer_fraction,
                    'correct_answer_decimal': correct_answer_decimal,
                    'malrule_answer': malrule_answer,
                    'problem_type': 'fractional_base',
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )
