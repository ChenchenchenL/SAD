"""
Problem generator for Inverted-Conversion-Factor malrule.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple
from utils import ProblemGenerator, Problem, DifficultyLevel


class InvertedConversionFactorProblemGenerator(ProblemGenerator):
    """Generates unit conversion problems."""

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        ranges = {
            6: {
                DifficultyLevel.EASY: {'value': (12, 48)},  # inches to feet
                DifficultyLevel.MEDIUM: {'value': (24, 96)},
                DifficultyLevel.HARD: {'value': (36, 120)}
            },
            7: {
                DifficultyLevel.EASY: {'value': (24, 96)},
                DifficultyLevel.MEDIUM: {'value': (36, 120)},
                DifficultyLevel.HARD: {'value': (60, 180)}
            },
            8: {
                DifficultyLevel.EASY: {'value': (36, 120)},
                DifficultyLevel.MEDIUM: {'value': (60, 180)},
                DifficultyLevel.HARD: {'value': (100, 300)}
            },
            9: {
                DifficultyLevel.EASY: {'value': (60, 180)},
                DifficultyLevel.MEDIUM: {'value': (100, 300)},
                DifficultyLevel.HARD: {'value': (200, 500)}
            },
            10: {
                DifficultyLevel.EASY: {'value': (100, 300)},
                DifficultyLevel.MEDIUM: {'value': (200, 500)},
                DifficultyLevel.HARD: {'value': (500, 1000)}
            }
        }
        lvl = self.level if self.level in ranges else 7
        return ranges[lvl][self.difficulty]

    def generate(self, seed=None) -> Problem:
        if seed is not None:
            random.seed(seed)

        # Choose problem type
        problem_types = ['basic_conversion']

        # Add enhanced problem types for higher levels
        if self.level >= 7:
            problem_types.extend([
                'multi_step_conversion',    # Multi-step conversions where student inverts at one step
                'imperial_to_metric',       # Cross-system conversions where inversion creates huge errors
                'word_problem_context',     # Real-world word problems
                'compound_units',           # Speed, density with compound units
            ])

        problem_type = random.choice(problem_types)

        # Handle enhanced problem types first
        if problem_type == 'multi_step_conversion':
            # Multi-step conversion where student inverts at one step
            # Each conversion has 3 different question phrasings
            conversions = [
                ('inches', 'feet', 'yards', 12, 3, [
                    "Convert {value} {start_unit} to {end_unit}",
                    "Express {value} {start_unit} in terms of {end_unit}",
                    "A measurement of {value} {start_unit} equals how many {end_unit}?"
                ]),
                ('seconds', 'minutes', 'hours', 60, 60, [
                    "Convert {value} {start_unit} to {end_unit}",
                    "How many {end_unit} are in {value} {start_unit}?",
                    "Express a duration of {value} {start_unit} in {end_unit}"
                ]),
                ('centimeters', 'meters', 'kilometers', 100, 1000, [
                    "Convert {value} {start_unit} to {end_unit}",
                    "A distance of {value} {start_unit} is equal to how many {end_unit}?",
                    "Express {value} {start_unit} in {end_unit}"
                ]),
            ]

            start_unit, mid_unit, end_unit, factor1, factor2, text_templates = random.choice(conversions)

            ranges = self.get_value_ranges()
            min_val, max_val = ranges['value']

            # Generate value divisible by both factors for clean answer
            result = random.randint(max(1, min_val // (factor1 * factor2)), max(2, max_val // (factor1 * factor2)))
            value = result * factor1 * factor2

            # Correct: value / factor1 / factor2
            correct_answer = value / factor1 / factor2

            # Malrule: Invert at first step (multiply instead of divide)
            malrule_answer = value * factor1 / factor2

            # Select one of the 3 question variants
            question_variant = random.randint(0, 2)
            text = text_templates[question_variant].format(value=value, start_unit=start_unit, end_unit=end_unit)

            return Problem(
                text=text,
                operands=[value, factor1, factor2],
                operation='multi_step_conversion',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'value': value,
                    'problem_type': problem_type,
                    'start_unit': start_unit,
                    'mid_unit': mid_unit,
                    'end_unit': end_unit,
                    'factor1': factor1,
                    'factor2': factor2,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'question_variant': question_variant
                }
            )

        elif problem_type == 'imperial_to_metric':
            # Cross-system conversions where inversion creates huge errors
            # Each conversion has 3 different question phrasings
            conversions = [
                ('feet', 'meters', 3.281, 0.305, [
                    "Convert {value} {from_unit} to {to_unit} (use 1 {from_unit} = {correct_factor} {to_unit})",
                    "A room is {value} {from_unit} wide. Express this in {to_unit} (1 {from_unit} = {correct_factor} {to_unit})",
                    "What is {value} {from_unit} in {to_unit}? (Use: 1 {from_unit} = {correct_factor} {to_unit})"
                ]),
                ('pounds', 'kilograms', 2.205, 0.454, [
                    "Convert {value} {from_unit} to {to_unit} (use 1 {from_unit} = {correct_factor} {to_unit})",
                    "A package weighs {value} {from_unit}. What is this in {to_unit}? (1 {from_unit} = {correct_factor} {to_unit})",
                    "Express {value} {from_unit} in {to_unit} using 1 {from_unit} = {correct_factor} {to_unit}"
                ]),
                ('gallons', 'liters', 0.264, 3.785, [
                    "Convert {value} {from_unit} to {to_unit} (use 1 {from_unit} = {correct_factor} {to_unit})",
                    "A tank holds {value} {from_unit}. Convert to {to_unit} (1 {from_unit} = {correct_factor} {to_unit})",
                    "How many {to_unit} equal {value} {from_unit}? (Given: 1 {from_unit} = {correct_factor} {to_unit})"
                ]),
            ]

            from_unit, to_unit, inv_factor, correct_factor, text_templates = random.choice(conversions)

            ranges = self.get_value_ranges()
            min_val, max_val = ranges['value']
            value = random.randint(max(2, min_val // 10), max(20, max_val // 10))

            # Correct: multiply by correct_factor
            correct_answer = round(value * correct_factor, 2)

            # Malrule: Invert - multiply by inverse factor instead
            malrule_answer = round(value * inv_factor, 2)

            # Select one of the 3 question variants
            question_variant = random.randint(0, 2)
            text = text_templates[question_variant].format(
                value=value, from_unit=from_unit, to_unit=to_unit, correct_factor=correct_factor
            )

            return Problem(
                text=text,
                operands=[value, correct_factor],
                operation='imperial_metric_conversion',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'value': value,
                    'problem_type': problem_type,
                    'from_unit': from_unit,
                    'to_unit': to_unit,
                    'correct_factor': correct_factor,
                    'inv_factor': inv_factor,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'question_variant': question_variant
                }
            )

        elif problem_type == 'word_problem_context':
            # Real-world word problems requiring unit conversion
            # Each scenario has 3 different question variants for variety
            scenarios = [
                ('inches', 'feet', 12, [
                    "A ribbon is {value} inches long. How many feet is that?",
                    "Sarah's pencil measures {value} inches. Convert this to feet.",
                    "The width of a picture frame is {value} inches. What is this in feet?"
                ]),
                ('minutes', 'hours', 60, [
                    "A meeting lasted {value} minutes. How many hours is that?",
                    "Tom worked for {value} minutes. Express this time in hours.",
                    "The movie runtime is {value} minutes. Convert to hours."
                ]),
                ('ounces', 'pounds', 16, [
                    "A package weighs {value} ounces. How many pounds is that?",
                    "The baby weighs {value} ounces at birth. What is this in pounds?",
                    "A bag contains {value} ounces of flour. Convert this to pounds."
                ]),
                ('feet', 'yards', 3, [
                    "A rope is {value} feet long. How many yards is that?",
                    "The garden fence measures {value} feet. Express this in yards.",
                    "Maria ran {value} feet. How many yards did she run?"
                ]),
                ('seconds', 'minutes', 60, [
                    "A video is {value} seconds long. How many minutes is that?",
                    "The timer was set for {value} seconds. Convert this to minutes.",
                    "An experiment lasted {value} seconds. What is this in minutes?"
                ]),
            ]

            from_unit, to_unit, factor, text_templates = random.choice(scenarios)

            # Select one of the 3 question variants
            question_variant = random.randint(0, 2)
            text_template = text_templates[question_variant]

            ranges = self.get_value_ranges()
            min_val, max_val = ranges['value']

            # Generate value divisible by factor for clean answer
            result = random.randint(max(1, min_val // factor), max(3, max_val // factor))
            value = result * factor

            # Correct: value / factor
            correct_answer = value / factor

            # Malrule: Invert - multiply instead of divide
            malrule_answer = value * factor

            text = text_template.format(value=value)

            return Problem(
                text=text,
                operands=[value, factor],
                operation='word_problem_conversion',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'value': value,
                    'problem_type': problem_type,
                    'from_unit': from_unit,
                    'to_unit': to_unit,
                    'factor': factor,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'question_variant': question_variant
                }
            )

        elif problem_type == 'compound_units':
            # Compound units like speed (feet/second → miles/hour)
            # Each scenario has 3 different question phrasings
            scenarios = [
                ('feet per second', 'miles per hour', 0.682, 1.467, 'ft/s', 'mph', [
                    "Convert {value} {from_unit_long} to {to_unit_long}",
                    "A car travels at {value} {from_unit_long}. Express this speed in {to_unit_long}",
                    "What is {value} {from_abbr} in {to_abbr}?"
                ]),
                ('meters per second', 'kilometers per hour', 3.6, 0.278, 'm/s', 'km/h', [
                    "Convert {value} {from_unit_long} to {to_unit_long}",
                    "An object moves at {value} {from_unit_long}. What is this in {to_unit_long}?",
                    "Express {value} {from_abbr} as {to_abbr}"
                ]),
            ]

            from_unit_long, to_unit_long, correct_factor, inv_factor, from_abbr, to_abbr, text_templates = random.choice(scenarios)

            ranges = self.get_value_ranges()
            min_val, max_val = ranges['value']
            value = random.randint(max(5, min_val // 10), max(30, max_val // 10))

            # Correct: multiply by correct_factor
            correct_answer = round(value * correct_factor, 2)

            # Malrule: Invert - use inverse factor instead
            malrule_answer = round(value * inv_factor, 2)

            # Select one of the 3 question variants
            question_variant = random.randint(0, 2)
            text = text_templates[question_variant].format(
                value=value, from_unit_long=from_unit_long, to_unit_long=to_unit_long,
                from_abbr=from_abbr, to_abbr=to_abbr
            )

            return Problem(
                text=text,
                operands=[value, correct_factor],
                operation='compound_unit_conversion',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'value': value,
                    'problem_type': problem_type,
                    'from_unit': from_unit_long,
                    'to_unit': to_unit_long,
                    'from_abbr': from_abbr,
                    'to_abbr': to_abbr,
                    'correct_factor': correct_factor,
                    'inv_factor': inv_factor,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'question_variant': question_variant
                }
            )

        # Original basic problem type with 3 question variants
        conversion_types = [
            ('inches', 'feet', 12),      # 12 inches = 1 foot
            ('feet', 'yards', 3),        # 3 feet = 1 yard
            ('ounces', 'pounds', 16),    # 16 ounces = 1 pound
            ('minutes', 'hours', 60),    # 60 minutes = 1 hour
        ]

        from_unit, to_unit, factor = random.choice(conversion_types)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['value']

        # Generate value that's divisible by factor for clean answer
        # Pick a nice result first, then multiply by factor
        result = random.randint(min_val // factor, max_val // factor)
        value = result * factor

        # Correct answer: value / factor
        correct_answer = value / factor

        # Malrule answer: value * factor (inverted!)
        malrule_answer = value * factor

        # Create problem text with 3 variants
        text_templates = [
            f"Convert {value} {from_unit} to {to_unit}",
            f"Express {value} {from_unit} in {to_unit}",
            f"How many {to_unit} are in {value} {from_unit}?"
        ]
        question_variant = random.randint(0, 2)
        text = text_templates[question_variant]

        return Problem(
            text=text,
            operands=[value, factor],
            operation='unit_conversion',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'value': value,
                'problem_type': 'basic_conversion',
                'from_unit': from_unit,
                'to_unit': to_unit,
                'factor': factor,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'question_variant': question_variant
            }
        )
