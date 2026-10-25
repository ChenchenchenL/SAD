"""
Problem generator for Wrong-Conversion-Factor malrule.

Generates unit conversion problems where students might use
incorrect (round number) conversion factors.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional
from utils import ProblemGenerator, Problem, DifficultyLevel


class WrongConversionFactorProblemGenerator(ProblemGenerator):
    """
    Generates unit conversion problems to elicit Wrong-Conversion-Factor malrule.

    Creates problems where students need to convert between units, and the
    malrule predicts they'll use round numbers (10, 100) instead of correct
    conversion factors.
    """

    def get_name(self) -> str:
        return "Wrong Conversion Factor Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates unit conversion problems where students might "
            "substitute round numbers for actual conversion factors."
        )

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level."""
        ranges = {
            5: {
                DifficultyLevel.EASY: (1, 10),
                DifficultyLevel.MEDIUM: (2, 20),
                DifficultyLevel.HARD: (5, 50),
            },
            6: {
                DifficultyLevel.EASY: (2, 15),
                DifficultyLevel.MEDIUM: (5, 30),
                DifficultyLevel.HARD: (10, 60),
            },
            7: {
                DifficultyLevel.EASY: (2, 20),
                DifficultyLevel.MEDIUM: (5, 40),
                DifficultyLevel.HARD: (10, 80),
            },
            8: {
                DifficultyLevel.EASY: (5, 25),
                DifficultyLevel.MEDIUM: (10, 50),
                DifficultyLevel.HARD: (20, 100),
            },
            9: {
                DifficultyLevel.EASY: (5, 30),
                DifficultyLevel.MEDIUM: (10, 60),
                DifficultyLevel.HARD: (25, 120),
            },
            10: {
                DifficultyLevel.EASY: (10, 40),
                DifficultyLevel.MEDIUM: (20, 80),
                DifficultyLevel.HARD: (50, 150),
            }
        }

        lvl = self.level if self.level in ranges else 6
        return {'value': ranges[lvl][self.difficulty]}

    def generate(self, seed: Optional[int] = None) -> Problem:
        """
        Generate a unit conversion problem.

        Args:
            seed: Optional random seed for reproducibility

        Returns:
            Problem instance
        """
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['value']

        # Choose problem type
        problem_types = ['basic_conversion']

        # Add enhanced problem types for higher levels
        if self.level >= 6:
            problem_types.extend([
                'multi_step_conversion',    # Multi-step conversions (yards → feet → inches)
                'imperial_to_metric',       # Cross-system conversions
                'word_problem_context',     # Real-world word problems
                'compound_units',           # Speed, density with compound units
            ])

        problem_type = random.choice(problem_types)

        # Handle enhanced problem types first
        if problem_type == 'multi_step_conversion':
            # Multi-step conversion where student might use wrong factor at any step
            # Each conversion has 3 different question phrasings
            conversions = [
                ('yards', 'feet', 'inches', 3, 12, 10, 10, [
                    "Convert {value} {start_unit} to {end_unit}",
                    "Express {value} {start_unit} in terms of {end_unit}",
                    "A length of {value} {start_unit} equals how many {end_unit}?"
                ]),
                ('hours', 'minutes', 'seconds', 60, 60, 100, 100, [
                    "Convert {value} {start_unit} to {end_unit}",
                    "How many {end_unit} are in {value} {start_unit}?",
                    "Express a time duration of {value} {start_unit} in {end_unit}"
                ]),
                ('kilometers', 'meters', 'centimeters', 1000, 100, 100, 10, [
                    "Convert {value} {start_unit} to {end_unit}",
                    "A distance of {value} {start_unit} is equal to how many {end_unit}?",
                    "Express {value} {start_unit} in {end_unit}"
                ]),
            ]

            start_unit, mid_unit, end_unit, factor1, factor2, wrong1, wrong2, text_templates = random.choice(conversions)
            value = random.randint(max(1, min_val // 10), max(5, max_val // 10))

            # Correct: value * factor1 * factor2
            correct_answer = value * factor1 * factor2

            # Malrule: Use wrong factor at first step (most common error point)
            malrule_answer = value * wrong1 * factor2

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
                    'wrong_factor1': wrong1,
                    'wrong_factor2': wrong2,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'question_variant': question_variant
                }
            )

        elif problem_type == 'imperial_to_metric':
            # Cross-system conversions where students might guess round numbers
            # Each conversion has 3 different question phrasings
            conversions = [
                ('miles', 'kilometers', 1.609, 1.0, [
                    "Convert {value} {from_unit} to {to_unit} (use 1 {from_unit} ≈ {correct_factor} {to_unit})",
                    "A car travels {value} {from_unit}. Express this distance in {to_unit} (1 {from_unit} ≈ {correct_factor} {to_unit})",
                    "How many {to_unit} are in {value} {from_unit}? (Use the conversion: 1 {from_unit} ≈ {correct_factor} {to_unit})"
                ]),
                ('pounds', 'kilograms', 0.454, 0.5, [
                    "Convert {value} {from_unit} to {to_unit} (use 1 {from_unit} ≈ {correct_factor} {to_unit})",
                    "A box weighs {value} {from_unit}. What is this weight in {to_unit}? (1 {from_unit} ≈ {correct_factor} {to_unit})",
                    "Express {value} {from_unit} in {to_unit} using the conversion factor 1 {from_unit} ≈ {correct_factor} {to_unit}"
                ]),
                ('feet', 'meters', 0.305, 0.3, [
                    "Convert {value} {from_unit} to {to_unit} (use 1 {from_unit} ≈ {correct_factor} {to_unit})",
                    "The ceiling height is {value} {from_unit}. Convert to {to_unit} (1 {from_unit} ≈ {correct_factor} {to_unit})",
                    "What is {value} {from_unit} in {to_unit}? (Use: 1 {from_unit} ≈ {correct_factor} {to_unit})"
                ]),
                ('inches', 'centimeters', 2.54, 2.5, [
                    "Convert {value} {from_unit} to {to_unit} (use 1 {from_unit} ≈ {correct_factor} {to_unit})",
                    "A pencil is {value} {from_unit} long. Express this in {to_unit} (1 {from_unit} ≈ {correct_factor} {to_unit})",
                    "How many {to_unit} equal {value} {from_unit}? (Given: 1 {from_unit} ≈ {correct_factor} {to_unit})"
                ]),
            ]

            from_unit, to_unit, correct_factor, wrong_factor, text_templates = random.choice(conversions)
            value = random.randint(max(1, min_val // 2), max(10, max_val // 2))

            correct_answer = round(value * correct_factor, 2)
            malrule_answer = round(value * wrong_factor, 2)

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
                    'wrong_factor': wrong_factor,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'question_variant': question_variant
                }
            )

        elif problem_type == 'word_problem_context':
            # Real-world word problems requiring unit conversion
            # Each scenario has 3 different question variants for variety
            scenarios = [
                ('feet', 'inches', 12, 10, [
                    "A board is {value} feet long. How many inches is that?",
                    "Sarah measures a rope that is {value} feet in length. Convert this measurement to inches.",
                    "The width of a room is {value} feet. What is this distance in inches?"
                ]),
                ('hours', 'minutes', 60, 100, [
                    "A movie runs for {value} hours. How many minutes is that?",
                    "Tom spent {value} hours studying. How many minutes did he study?",
                    "The concert lasted {value} hours. Convert this time to minutes."
                ]),
                ('yards', 'feet', 3, 10, [
                    "A football field section is {value} yards. How many feet is that?",
                    "The garden is {value} yards long. What is this length in feet?",
                    "Maria ran {value} yards during practice. How many feet did she run?"
                ]),
                ('kilometers', 'meters', 1000, 100, [
                    "You drive {value} kilometers. How many meters is that?",
                    "The race course is {value} kilometers long. Convert this distance to meters.",
                    "A bike path extends for {value} kilometers. What is this distance in meters?"
                ]),
                ('pounds', 'ounces', 16, 10, [
                    "A package weighs {value} pounds. How many ounces is that?",
                    "The baby weighs {value} pounds. Convert this weight to ounces.",
                    "A bag of flour is {value} pounds. What is this weight in ounces?"
                ]),
                ('gallons', 'quarts', 4, 10, [
                    "A tank holds {value} gallons of water. How many quarts is that?",
                    "The recipe calls for {value} gallons of milk. Convert this to quarts.",
                    "A container has {value} gallons of juice. What is this volume in quarts?"
                ]),
            ]

            from_unit, to_unit, correct_factor, wrong_factor, text_templates = random.choice(scenarios)
            # Select one of the 3 question variants
            question_variant = random.randint(0, 2)
            text_template = text_templates[question_variant]

            value = random.randint(max(2, min_val // 5), max(10, max_val // 5))

            correct_answer = value * correct_factor
            malrule_answer = value * wrong_factor

            text = text_template.format(value=value)

            return Problem(
                text=text,
                operands=[value, correct_factor],
                operation='word_problem_conversion',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'value': value,
                    'problem_type': problem_type,
                    'from_unit': from_unit,
                    'to_unit': to_unit,
                    'correct_factor': correct_factor,
                    'wrong_factor': wrong_factor,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'question_variant': question_variant
                }
            )

        elif problem_type == 'compound_units':
            # Compound units like speed (miles/hour → feet/second)
            # Each scenario has 3 different question phrasings
            scenarios = [
                ('miles per hour', 'feet per second', 1.467, 1.0, 'mph', 'ft/s', 'speed', [
                    "Convert {value} {from_unit_long} to {to_unit_long}",
                    "A car travels at {value} {from_unit_long}. Express this speed in {to_unit_long}",
                    "What is {value} {from_abbr} in {to_abbr}?"
                ]),
                ('feet per second', 'miles per hour', 0.682, 1.0, 'ft/s', 'mph', 'speed', [
                    "Convert {value} {from_unit_long} to {to_unit_long}",
                    "An object moves at {value} {from_unit_long}. What is this speed in {to_unit_long}?",
                    "Express {value} {from_abbr} as {to_abbr}"
                ]),
                ('kilometers per hour', 'meters per second', 0.278, 0.1, 'km/h', 'm/s', 'speed', [
                    "Convert {value} {from_unit_long} to {to_unit_long}",
                    "A train travels at {value} {from_unit_long}. What is this in {to_unit_long}?",
                    "How many {to_unit_long} equal {value} {from_unit_long}?"
                ]),
            ]

            from_unit_long, to_unit_long, correct_factor, wrong_factor, from_abbr, to_abbr, unit_type, text_templates = random.choice(scenarios)
            value = random.randint(max(10, min_val), max(60, max_val // 2))

            correct_answer = round(value * correct_factor, 2)
            malrule_answer = round(value * wrong_factor, 2)

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
                    'unit_type': unit_type,
                    'correct_factor': correct_factor,
                    'wrong_factor': wrong_factor,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'question_variant': question_variant
                }
            )

        # Original basic problem type with 3 question variants
        conversion_types = [
            ('feet', 'inches', 12, 10),           # Correct: 12, Wrong: 10
            ('yards', 'feet', 3, 10),             # Correct: 3, Wrong: 10
            ('meters', 'centimeters', 100, 10),   # Correct: 100, Wrong: 10
            ('kilometers', 'meters', 1000, 100),  # Correct: 1000, Wrong: 100
            ('hours', 'minutes', 60, 100),        # Correct: 60, Wrong: 100
            ('minutes', 'seconds', 60, 100),      # Correct: 60, Wrong: 100
            ('pounds', 'ounces', 16, 10),         # Correct: 16, Wrong: 10
            ('gallons', 'quarts', 4, 10),         # Correct: 4, Wrong: 10
        ]

        from_unit, to_unit, correct_factor, wrong_factor = random.choice(conversion_types)

        # Generate a value to convert
        value = random.randint(min_val, max_val)

        # Calculate answers
        correct_answer = value * correct_factor
        malrule_answer = value * wrong_factor

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
            operands=[value, correct_factor],
            operation='unit_conversion',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'value': value,
                'problem_type': problem_type,
                'from_unit': from_unit,
                'to_unit': to_unit,
                'correct_factor': correct_factor,
                'wrong_factor': wrong_factor,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'question_variant': question_variant
            }
        )
