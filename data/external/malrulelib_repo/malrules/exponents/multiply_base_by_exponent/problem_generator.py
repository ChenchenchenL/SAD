"""
Problem generator for Multiply-Base-By-Exponent malrule.
"""

import random
import sys
sys.path.append('/home/user/malrule-coding')

from typing import List, Optional
from utils import Problem, ProblemGenerator


class MultiplyBaseByExponentProblemGenerator(ProblemGenerator):
    """Generates exponentiation problems."""

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'simple_numeric',
            'larger_exponent',
            'word_problem_context'  # NEW: Covers all formula types with 3 variants each
        ]

    def get_value_ranges(self):
        """Return the value ranges for problem generation."""
        return {
            'base': (2, 10),
            'exponent': (2, 5)
        }

    def generate(self, seed=None, template: Optional[str] = None):
        """
        Generate an exponentiation problem.

        Args:
            seed: Optional random seed for reproducibility
            template: Optional template type to use

        Returns:
            Problem with exponentiation question
        """
        if seed is not None:
            random.seed(seed)

        # If template is specified, use it
        if template is not None:
            if template == 'word_problem_context':
                return self._generate_word_problem_context(seed)
            elif template in ['simple_numeric', 'larger_exponent']:
                problem_type = template
            else:
                # Handle old word problem types for backwards compatibility
                problem_type = template
        else:
            # Choose problem type
            problem_types = ['simple_numeric']

            # Add enhanced problem types for higher levels
            if self.level >= 7:
                problem_types.extend([
                    'larger_exponent',         # Larger exponents (6-8)
                    'word_problem_area',       # Area/geometry contexts
                    'word_problem_volume',     # Volume contexts
                    'word_problem_growth',     # Population/bacteria growth
                ])

            problem_type = random.choice(problem_types)

        if problem_type == 'simple_numeric':
            # Generate base and exponent
            base = random.randint(2, 10)
            exponent = random.randint(2, 5)

            # Calculate correct answer
            correct_answer = base ** exponent

            # Calculate malrule answer (multiply instead of exponentiate)
            malrule_answer = base * exponent

            # Create problem statement
            problem_statement = f"Evaluate: {base}^{exponent}"

        elif problem_type == 'larger_exponent':
            # Use smaller bases with larger exponents
            base = random.randint(2, 5)
            exponent = random.randint(6, 8)

            correct_answer = base ** exponent
            malrule_answer = base * exponent

            problem_statement = f"Evaluate: {base}^{exponent}"

        elif problem_type == 'word_problem_area':
            # Area context: square or cube
            side = random.randint(3, 12)
            exponent = random.choice([2, 3])

            if exponent == 2:
                contexts = [
                    f"A square has side length {side} cm. What is the area? (Area = side^2)",
                    f"Calculate the area of a square with side {side} meters: {side}^2",
                    f"Square area: side = {side}, area = {side}^{exponent}. Calculate.",
                ]
            else:  # exponent == 3
                contexts = [
                    f"A cube has side length {side} cm. What is the volume? (Volume = side^3)",
                    f"Calculate the volume of a cube with side {side} meters: {side}^3",
                    f"Cube volume: side = {side}, volume = {side}^{exponent}. Calculate.",
                ]

            problem_statement = random.choice(contexts)
            base = side
            correct_answer = base ** exponent
            malrule_answer = base * exponent

        elif problem_type == 'word_problem_volume':
            # Volume of a cube
            side = random.randint(4, 10)
            exponent = 3

            contexts = [
                f"A cubic box has sides of {side} inches. What is its volume? (V = s^3)",
                f"Volume of cube with side {side} cm: {side}^3 = ?",
                f"Calculate the volume: cube side = {side}, V = {side}^3",
            ]

            problem_statement = random.choice(contexts)
            base = side
            correct_answer = base ** exponent
            malrule_answer = base * exponent

        elif problem_type == 'word_problem_growth':
            # Population/bacteria growth
            initial = random.choice([2, 3, 4, 5])
            time = random.randint(3, 6)

            contexts = [
                f"A bacteria colony doubles every hour. Starting with {initial}, after {time} hours: {initial}^{time}. How many?",
                f"Population grows by factor of {initial} each generation. After {time} generations: {initial}^{time} = ?",
                f"Exponential growth: {initial}^{time}. Calculate the result.",
            ]

            problem_statement = random.choice(contexts)
            base = initial
            exponent = time
            correct_answer = base ** exponent
            malrule_answer = base * exponent

        else:  # Default fallback
            base = random.randint(2, 10)
            exponent = random.randint(2, 5)
            correct_answer = base ** exponent
            malrule_answer = base * exponent
            problem_statement = f"Evaluate: {base}^{exponent}"

        # Create metadata
        metadata = {
            'base': base,
            'exponent': exponent,
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer,
            'problem_type': problem_type
        }

        return Problem(
            text=problem_statement,
            operands=[base, exponent],
            operation='exponentiation',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_word_problem_context(self, seed=None) -> Problem:
        """Generate word problem covering ALL formula types with 3 variants each."""
        if seed is not None:
            random.seed(seed)

        # Select which formula type to embed
        formula_types = ['simple_numeric', 'larger_exponent']
        formula_type = random.choice(formula_types)
        variant = random.randint(0, 2)  # 3 variants per formula type

        if formula_type == 'simple_numeric':
            # Formula: base^exponent with typical values
            base = random.randint(2, 10)
            exponent = random.randint(2, 5)

            correct_answer = base ** exponent
            malrule_answer = base * exponent

            templates = [
                # Variant 0: Area/Volume contexts
                f"A square garden has sides of length {base} meters. What is the area in square meters? (Area = side^2)" if exponent == 2
                else f"A cube-shaped storage container has edges of length {base} feet. What is the volume in cubic feet? (Volume = side^3)" if exponent == 3
                else f"A pizza chain expands to {base} cities, and each city gets {exponent} stores. If growth follows the pattern {base}^{exponent}, how many total expansion points are there?",

                # Variant 1: Growth/Multiplication contexts
                f"A bacteria colony has {base} cells. Each cell divides into {base} new cells over {exponent} generations following the pattern {base}^{exponent}. How many cells are there after {exponent} generations?" if exponent <= 4
                else f"An investment grows by a factor of {base} each year. After {exponent} years, the growth factor is {base}^{exponent}. What is the total growth factor?",

                # Variant 2: Technology/Computing contexts
                f"A computer network has {base} nodes. Each node can connect to {base} others, forming {base}^{exponent} total possible connection patterns over {exponent} layers. How many connection patterns exist?" if exponent <= 4
                else f"A data storage system uses blocks of size {base}^{exponent} bytes. Calculate the block size in bytes."
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[base, exponent],
                operation='exponentiation',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'base': base,
                    'exponent': exponent,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'problem_type': 'word_problem_context',
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        else:  # larger_exponent
            # Formula: base^exponent with smaller bases and larger exponents
            base = random.randint(2, 5)
            exponent = random.randint(6, 8)

            correct_answer = base ** exponent
            malrule_answer = base * exponent

            templates = [
                # Variant 0: Population growth
                f"A rare species population multiplies by {base} every decade. Over {exponent} decades, the population growth factor is {base}^{exponent}. Calculate the growth factor.",

                # Variant 1: Compound interest
                f"An investment compounds at a rate where the multiplier is {base}^{exponent} over {exponent} compounding periods. What is the total multiplier?",

                # Variant 2: Scientific notation/large numbers
                f"A particle accelerator generates {base}^{exponent} particle collisions. How many collisions occur?"
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[base, exponent],
                operation='exponentiation',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'base': base,
                    'exponent': exponent,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'problem_type': 'word_problem_context',
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )
