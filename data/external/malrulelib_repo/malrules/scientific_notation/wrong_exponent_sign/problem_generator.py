"""
Problem generator for Wrong-Exponent-Sign malrule.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional, List
from utils import ProblemGenerator, Problem, DifficultyLevel


class WrongExponentSignProblemGenerator(ProblemGenerator):
    """Generates scientific notation conversion problems."""

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        ranges = {
            6: {
                DifficultyLevel.EASY: {'exponent': (1, 3)},
                DifficultyLevel.MEDIUM: {'exponent': (2, 4)},
                DifficultyLevel.HARD: {'exponent': (3, 5)}
            },
            7: {
                DifficultyLevel.EASY: {'exponent': (2, 4)},
                DifficultyLevel.MEDIUM: {'exponent': (3, 5)},
                DifficultyLevel.HARD: {'exponent': (4, 6)}
            },
            8: {
                DifficultyLevel.EASY: {'exponent': (3, 5)},
                DifficultyLevel.MEDIUM: {'exponent': (4, 6)},
                DifficultyLevel.HARD: {'exponent': (5, 8)}
            },
            9: {
                DifficultyLevel.EASY: {'exponent': (4, 6)},
                DifficultyLevel.MEDIUM: {'exponent': (5, 8)},
                DifficultyLevel.HARD: {'exponent': (6, 10)}
            }
        }
        lvl = self.level if self.level in ranges else 7
        return ranges[lvl][self.difficulty]

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        templates = ['basic_conversion']
        if self.level >= 7:
            templates.extend([
                'real_world_small',
                'real_world_large',
                'unit_conversion_context',
                'comparison_context',
            ])
        return templates

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate a scientific notation conversion problem.

        Args:
            seed: Optional random seed for reproducibility
            template: Optional template name. If None, random template is chosen.

        Returns:
            Problem instance
        """
        if seed is not None:
            random.seed(seed)

        # Get available templates
        problem_types = self.get_available_templates()

        # Choose problem type from available templates
        if template is None:
            problem_type = random.choice(problem_types)
        else:
            if template in problem_types:
                problem_type = template
            else:
                raise ValueError(f"Template '{template}' not in available templates: {problem_types}")

        ranges = self.get_value_ranges()
        min_exp, max_exp = ranges['exponent']

        # Handle enhanced problem types first
        if problem_type == 'real_world_small':
            # Very small numbers in real-world contexts
            contexts = [
                ('The diameter of a bacterium is approximately', 'meters'),
                ('The wavelength of red light is about', 'meters'),
                ('The mass of a dust particle is roughly', 'grams'),
                ('The thickness of a cell membrane is around', 'meters')
            ]
            context, unit = random.choice(contexts)

            mantissa = random.randint(10, 99) / 10.0
            exponent_magnitude = random.randint(min_exp, max_exp)
            correct_exponent = -exponent_magnitude
            decimal_number = mantissa * (10 ** correct_exponent)
            malrule_exponent = exponent_magnitude

            number_str = f"{decimal_number:.10f}".rstrip('0').rstrip('.')
            text = f"{context} {number_str} {unit}. Express this in scientific notation."

            return Problem(
                text=text,
                operands=[mantissa, correct_exponent],
                operation='scientific_notation_conversion',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'problem_type': problem_type,
                    'decimal_number': decimal_number,
                    'number_str': number_str,
                    'mantissa': mantissa,
                    'correct_exponent': correct_exponent,
                    'malrule_exponent': malrule_exponent,
                    'is_small': True,
                    'context': context,
                    'unit': unit
                }
            )

        elif problem_type == 'real_world_large':
            # Very large numbers in real-world contexts
            contexts = [
                ('The distance from Earth to the Sun is about', 'meters'),
                ('The world population is approximately', 'people'),
                ('The national debt is roughly', 'dollars'),
                ('The number of stars in our galaxy is about', 'stars')
            ]
            context, unit = random.choice(contexts)

            mantissa = random.randint(10, 99) / 10.0
            exponent_magnitude = random.randint(min_exp, max_exp)
            correct_exponent = exponent_magnitude
            decimal_number = mantissa * (10 ** correct_exponent)
            malrule_exponent = -exponent_magnitude

            number_str = f"{int(decimal_number)}"
            text = f"{context} {number_str} {unit}. Express this in scientific notation."

            return Problem(
                text=text,
                operands=[mantissa, correct_exponent],
                operation='scientific_notation_conversion',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'problem_type': problem_type,
                    'decimal_number': decimal_number,
                    'number_str': number_str,
                    'mantissa': mantissa,
                    'correct_exponent': correct_exponent,
                    'malrule_exponent': malrule_exponent,
                    'is_small': False,
                    'context': context,
                    'unit': unit
                }
            )

        elif problem_type == 'unit_conversion_context':
            # Unit conversion contexts
            is_small = random.choice([True, False])

            if is_small:
                conversions = [
                    ('Convert 0.{} meters to nanometers (1 nm = 1 × 10⁻⁹ m). The value is', 'meters'),
                    ('A measurement of 0.{} grams needs to be expressed in scientific notation. The value is', 'grams'),
                    ('Express the length 0.{} millimeters in scientific notation', 'mm')
                ]
                conversion_template, unit = random.choice(conversions)

                mantissa = random.randint(10, 99) / 10.0
                exponent_magnitude = random.randint(min_exp, max_exp)
                correct_exponent = -exponent_magnitude
                decimal_number = mantissa * (10 ** correct_exponent)
                malrule_exponent = exponent_magnitude

                number_str = f"{decimal_number:.10f}".rstrip('0').rstrip('.')
                # Fill in the template with the number
                if '{}' in conversion_template:
                    text = conversion_template.replace('0.{}', number_str)
                else:
                    text = f"{conversion_template} {number_str}. Express in scientific notation."
            else:
                conversions = [
                    ('The distance {} kilometers needs to be expressed in scientific notation', 'km'),
                    ('A large mass of {} kilograms should be written in scientific notation', 'kg'),
                    ('Express the value {} bytes in scientific notation', 'bytes')
                ]
                conversion_template, unit = random.choice(conversions)

                mantissa = random.randint(10, 99) / 10.0
                exponent_magnitude = random.randint(min_exp, max_exp)
                correct_exponent = exponent_magnitude
                decimal_number = mantissa * (10 ** correct_exponent)
                malrule_exponent = -exponent_magnitude

                number_str = f"{int(decimal_number)}"
                text = conversion_template.replace('{}', number_str) + "."

            return Problem(
                text=text,
                operands=[mantissa, correct_exponent],
                operation='scientific_notation_conversion',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'problem_type': problem_type,
                    'decimal_number': decimal_number,
                    'number_str': number_str,
                    'mantissa': mantissa,
                    'correct_exponent': correct_exponent,
                    'malrule_exponent': malrule_exponent,
                    'is_small': is_small,
                    'unit': unit
                }
            )

        elif problem_type == 'comparison_context':
            # Comparison context
            is_small = random.choice([True, False])

            mantissa = random.randint(10, 99) / 10.0
            exponent_magnitude = random.randint(min_exp, max_exp)

            if is_small:
                correct_exponent = -exponent_magnitude
                decimal_number = mantissa * (10 ** correct_exponent)
                malrule_exponent = exponent_magnitude
                number_str = f"{decimal_number:.10f}".rstrip('0').rstrip('.')
                text = f"Which is larger: {number_str} or 1? First, express {number_str} in scientific notation."
            else:
                correct_exponent = exponent_magnitude
                decimal_number = mantissa * (10 ** correct_exponent)
                malrule_exponent = -exponent_magnitude
                number_str = f"{int(decimal_number)}"
                text = f"To compare {number_str} with other values, express it in scientific notation."

            return Problem(
                text=text,
                operands=[mantissa, correct_exponent],
                operation='scientific_notation_conversion',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'problem_type': problem_type,
                    'decimal_number': decimal_number,
                    'number_str': number_str,
                    'mantissa': mantissa,
                    'correct_exponent': correct_exponent,
                    'malrule_exponent': malrule_exponent,
                    'is_small': is_small
                }
            )

        # Original basic problem type
        # Decide whether to generate small number (0.00...) or large number (1000...)
        is_small = random.choice([True, False])

        # Generate mantissa (coefficient) between 1.0 and 9.9
        mantissa = random.randint(10, 99) / 10.0

        # Generate exponent magnitude
        exponent_magnitude = random.randint(min_exp, max_exp)

        if is_small:
            # Small number: 0.00...X
            # Correct: negative exponent
            correct_exponent = -exponent_magnitude
            # Generate the actual decimal number
            decimal_number = mantissa * (10 ** correct_exponent)

            # Malrule: student uses positive exponent
            malrule_exponent = exponent_magnitude
        else:
            # Large number: X000...
            # Correct: positive exponent
            correct_exponent = exponent_magnitude
            # Generate the actual decimal number
            decimal_number = mantissa * (10 ** correct_exponent)

            # Malrule: student uses negative exponent
            malrule_exponent = -exponent_magnitude

        # Format number appropriately
        if is_small:
            if decimal_number >= 0.01:
                number_str = f"{decimal_number:.4f}".rstrip('0').rstrip('.')
            else:
                number_str = f"{decimal_number:.10f}".rstrip('0').rstrip('.')
        else:
            number_str = f"{int(decimal_number)}"

        text = f"Write {number_str} in scientific notation"

        return Problem(
            text=text,
            operands=[mantissa, correct_exponent],
            operation='scientific_notation_conversion',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'problem_type': 'basic_conversion',
                'decimal_number': decimal_number,
                'number_str': number_str,
                'mantissa': mantissa,
                'correct_exponent': correct_exponent,
                'malrule_exponent': malrule_exponent,
                'is_small': is_small
            }
        )
