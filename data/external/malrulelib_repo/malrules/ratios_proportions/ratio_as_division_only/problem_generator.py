"""
Problem generator for Ratio-As-Division-Only malrule.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple
from utils import ProblemGenerator, Problem, DifficultyLevel


class RatioAsDivisionOnlyProblemGenerator(ProblemGenerator):
    """Generates ratio interpretation and application problems."""

    def get_available_templates(self):
        """Return list of available template names."""
        return [
            'part_to_part_ratio',
            'recipe_scaling',
            'paint_mixing',
            'distance_rate',
            'map_scale',
            'word_problem_context'  # NEW: Covers all formula types with variants
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        ranges = {
            6: {
                DifficultyLevel.EASY: {'ratio': (2, 5), 'multiplier': (2, 4)},
                DifficultyLevel.MEDIUM: {'ratio': (2, 8), 'multiplier': (2, 5)},
                DifficultyLevel.HARD: {'ratio': (2, 10), 'multiplier': (3, 6)}
            },
            7: {
                DifficultyLevel.EASY: {'ratio': (2, 8), 'multiplier': (2, 5)},
                DifficultyLevel.MEDIUM: {'ratio': (2, 10), 'multiplier': (3, 6)},
                DifficultyLevel.HARD: {'ratio': (2, 12), 'multiplier': (3, 8)}
            },
            8: {
                DifficultyLevel.EASY: {'ratio': (2, 10), 'multiplier': (3, 6)},
                DifficultyLevel.MEDIUM: {'ratio': (2, 12), 'multiplier': (3, 8)},
                DifficultyLevel.HARD: {'ratio': (3, 15), 'multiplier': (4, 10)}
            }
        }
        lvl = self.level if self.level in ranges else 7
        return ranges[lvl][self.difficulty]

    def generate(self, seed=None, template=None) -> Problem:
        if seed is not None:
            random.seed(seed)

        # If no template specified, choose randomly
        if template is None:
            template = random.choice(self.get_available_templates())

        # Call appropriate template method
        if template == 'part_to_part_ratio':
            return self._generate_part_to_part_ratio()
        elif template == 'recipe_scaling':
            return self._generate_recipe_scaling()
        elif template == 'paint_mixing':
            return self._generate_paint_mixing()
        elif template == 'distance_rate':
            return self._generate_distance_rate()
        elif template == 'map_scale':
            return self._generate_map_scale()
        elif template == 'word_problem_context':
            return self._generate_word_problem_context()
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_part_to_part_ratio(self) -> Problem:
        """Template 1: Basic part-to-part ratio with marbles/students."""
        ranges = self.get_value_ranges()
        ratio_range = ranges['ratio']
        multiplier_range = ranges['multiplier']

        # Generate ratio a:b
        a = random.randint(ratio_range[0], ratio_range[1])
        b = random.randint(ratio_range[0], ratio_range[1])

        # Ensure a ≠ b and a < b for clearer problems
        attempts = 0
        while (a == b or a >= b) and attempts < 20:
            a = random.randint(ratio_range[0], ratio_range[1])
            b = random.randint(ratio_range[0], ratio_range[1])
            attempts += 1

        k = random.randint(multiplier_range[0], multiplier_range[1])
        first_quantity = a * k

        # Correct: Use multiplicative relationship (b * k)
        correct_answer = str(b * k)

        # Malrule: Student uses division - computes first_quantity * (a/b) instead of * (b/a)
        malrule_answer = str(round(first_quantity * (a / b), 2))

        text = f"If the ratio of red marbles to blue marbles is {a}:{b}, and there are {first_quantity} red marbles, how many blue marbles are there?"

        return Problem(
            text=text,
            operands=[a, b, first_quantity],
            operation='ratio_application',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'part_to_part_ratio',
                'ratio_a': a,
                'ratio_b': b,
                'first_quantity': first_quantity,
                'multiplier': k,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_recipe_scaling(self) -> Problem:
        """Template 2: Recipe scaling with ingredients in given ratio."""
        ranges = self.get_value_ranges()
        ratio_range = ranges['ratio']
        multiplier_range = ranges['multiplier']

        # Generate ratio a:b for flour:sugar
        a = random.randint(ratio_range[0], ratio_range[1])
        b = random.randint(ratio_range[0], ratio_range[1])

        attempts = 0
        while (a == b or a >= b) and attempts < 20:
            a = random.randint(ratio_range[0], ratio_range[1])
            b = random.randint(ratio_range[0], ratio_range[1])
            attempts += 1

        k = random.randint(multiplier_range[0], multiplier_range[1])
        flour_cups = a * k

        # Correct: sugar = b * k cups
        correct_answer = str(b * k)

        # Malrule: flour_cups * (a/b) - uses division incorrectly
        malrule_answer = str(round(flour_cups * (a / b), 2))

        text = f"A recipe calls for flour and sugar in the ratio {a}:{b}. If you use {flour_cups} cups of flour, how many cups of sugar do you need?"

        return Problem(
            text=text,
            operands=[a, b, flour_cups],
            operation='ratio_application',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'recipe_scaling',
                'ratio_a': a,
                'ratio_b': b,
                'flour_cups': flour_cups,
                'multiplier': k,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_paint_mixing(self) -> Problem:
        """Template 3: Mixing paint colors in given ratio."""
        ranges = self.get_value_ranges()
        ratio_range = ranges['ratio']
        multiplier_range = ranges['multiplier']

        # Generate ratio a:b for red:yellow paint
        a = random.randint(ratio_range[0], ratio_range[1])
        b = random.randint(ratio_range[0], ratio_range[1])

        attempts = 0
        while (a == b or a >= b) and attempts < 20:
            a = random.randint(ratio_range[0], ratio_range[1])
            b = random.randint(ratio_range[0], ratio_range[1])
            attempts += 1

        k = random.randint(multiplier_range[0], multiplier_range[1])
        red_drops = a * k

        # Correct: yellow = b * k drops
        correct_answer = str(b * k)

        # Malrule: red_drops * (a/b) - inverted ratio
        malrule_answer = str(round(red_drops * (a / b), 2))

        text = f"To make orange paint, you mix red and yellow paint in the ratio {a}:{b}. If you use {red_drops} drops of red paint, how many drops of yellow paint should you use?"

        return Problem(
            text=text,
            operands=[a, b, red_drops],
            operation='ratio_application',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'paint_mixing',
                'ratio_a': a,
                'ratio_b': b,
                'red_drops': red_drops,
                'multiplier': k,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_distance_rate(self) -> Problem:
        """Template 4: Distance/rate problems (miles per hour)."""
        ranges = self.get_value_ranges()
        ratio_range = ranges['ratio']

        # Generate ratio a:b for miles:hours (e.g., 60:1 means 60 mph)
        miles_per_unit = random.randint(ratio_range[0] * 5, ratio_range[1] * 5)  # Scale up for realistic speeds
        hours = random.randint(2, 6)

        # Correct: total_miles = miles_per_unit * hours
        total_miles = miles_per_unit * hours
        correct_answer = str(total_miles)

        # Malrule: Student thinks "ratio means division" so divides instead: miles_per_unit / hours
        malrule_answer = str(round(miles_per_unit / hours, 2))

        text = f"A car travels at a constant rate of {miles_per_unit} miles per hour. How many miles will it travel in {hours} hours?"

        return Problem(
            text=text,
            operands=[miles_per_unit, hours],
            operation='ratio_application',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'distance_rate',
                'rate': miles_per_unit,
                'time': hours,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_map_scale(self) -> Problem:
        """Template 5: Map scale interpretation and application."""
        ranges = self.get_value_ranges()
        ratio_range = ranges['ratio']
        multiplier_range = ranges['multiplier']

        # Generate ratio a:b for map (e.g., 1 inch : 5 miles)
        map_inches = 1  # Keep simple for level level
        real_miles = random.randint(ratio_range[0], ratio_range[1] * 2)

        # Now given some map measurement, find real distance
        k = random.randint(multiplier_range[0], multiplier_range[1])
        map_distance = map_inches * k

        # Correct: real_distance = real_miles * k
        correct_answer = str(real_miles * k)

        # Malrule: Student thinks ratio means division, computes map_distance / real_miles
        malrule_answer = str(round(map_distance / real_miles, 2))

        text = f"On a map, the scale is 1 inch : {real_miles} miles. If two cities are {map_distance} inches apart on the map, how many miles apart are they in real life?"

        return Problem(
            text=text,
            operands=[map_inches, real_miles, map_distance],
            operation='ratio_application',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'map_scale',
                'map_unit': map_inches,
                'real_unit': real_miles,
                'map_distance': map_distance,
                'multiplier': k,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_word_problem_context(self) -> Problem:
        """Generate word problem covering ALL formula types with 3 variants each."""
        formula_types = [
            'inverse_proportion',      # Given a:b and b*k, find a*k
            'part_to_whole_fraction',  # Given a:b, find a/(a+b)
            'finding_whole_from_part', # Given a:b and a*k, find total (a+b)*k
        ]
        formula_type = random.choice(formula_types)

        if formula_type == 'inverse_proportion':
            return self._word_problem_inverse_proportion()
        elif formula_type == 'part_to_whole_fraction':
            return self._word_problem_part_to_whole_fraction()
        elif formula_type == 'finding_whole_from_part':
            return self._word_problem_finding_whole()
        else:
            raise ValueError(f"Unknown formula type: {formula_type}")

    def _word_problem_inverse_proportion(self) -> Problem:
        """Formula: Given a:b and second quantity (b*k), find first quantity (a*k)."""
        ranges = self.get_value_ranges()
        ratio_range = ranges['ratio']
        multiplier_range = ranges['multiplier']

        a = random.randint(ratio_range[0], ratio_range[1])
        b = random.randint(ratio_range[0], ratio_range[1])
        while a == b or a >= b:
            a = random.randint(ratio_range[0], ratio_range[1])
            b = random.randint(ratio_range[0], ratio_range[1])

        k = random.randint(multiplier_range[0], multiplier_range[1])
        second_quantity = b * k

        # Correct: first = a * k (multiplicative)
        correct_answer = str(a * k)

        # Malrule: Student uses division incorrectly
        # They think: ratio = a/b, so first = second * (a/b)
        # But they reverse it: first = second * (b/a)
        malrule_answer = str(round(second_quantity * (b / a), 2))

        variant = random.randint(0, 2)
        contexts = [
            f"The ratio of cats to dogs is {a}:{b}. If there are {second_quantity} dogs, how many cats are there?",
            f"In a class, the ratio of boys to girls is {a}:{b}. If there are {second_quantity} girls, how many boys are there?",
            f"A recipe uses ingredients A and B in ratio {a}:{b}. If you use {second_quantity} units of B, how much of A do you need?"
        ]

        text = contexts[variant]

        return Problem(
            text=text,
            operands=[a, b, second_quantity],
            operation='inverse_ratio_application',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_context',
                'problem_type': 'inverse_proportion',
                'formula': 'a:b, given b*k, find a*k',
                'variant': variant,
                'ratio_a': a,
                'ratio_b': b,
                'second_quantity': second_quantity,
                'multiplier': k,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'is_word_problem': True
            }
        )

    def _word_problem_part_to_whole_fraction(self) -> Problem:
        """Formula: Given ratio a:b, find fraction a/(a+b). Student just uses a/b."""
        ranges = self.get_value_ranges()
        ratio_range = ranges['ratio']

        a = random.randint(ratio_range[0], min(ratio_range[1], 8))
        b = random.randint(ratio_range[0], min(ratio_range[1], 8))
        while a == b:
            b = random.randint(ratio_range[0], min(ratio_range[1], 8))

        # Correct: a/(a+b)
        correct_fraction = a / (a + b)
        correct_answer = f"{a}/{a+b}"

        # Malrule: Student thinks ratio means division, so just a/b
        malrule_fraction = a / b
        malrule_answer = f"{a}/{b}"

        variant = random.randint(0, 2)
        contexts = [
            f"In a class, the ratio of students who like math to those who like science is {a}:{b}. What fraction of the class likes math?",
            f"A mixture has ingredients in ratio {a}:{b}. What fraction of the mixture is the first ingredient?",
            f"Prize money is divided in ratio {a}:{b}. What fraction does the first person receive?"
        ]

        text = contexts[variant]

        return Problem(
            text=text,
            operands=[a, b],
            operation='part_to_whole_fraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_context',
                'problem_type': 'part_to_whole_fraction',
                'formula': 'a:b, find a/(a+b)',
                'variant': variant,
                'ratio_a': a,
                'ratio_b': b,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'correct_fraction': correct_fraction,
                'malrule_fraction': malrule_fraction,
                'is_word_problem': True
            }
        )

    def _word_problem_finding_whole(self) -> Problem:
        """Formula: Given a:b and first part (a*k), find total (a+b)*k."""
        ranges = self.get_value_ranges()
        ratio_range = ranges['ratio']
        multiplier_range = ranges['multiplier']

        a = random.randint(ratio_range[0], min(ratio_range[1], 8))
        b = random.randint(ratio_range[0], min(ratio_range[1], 8))
        while a == b:
            b = random.randint(ratio_range[0], min(ratio_range[1], 8))

        k = random.randint(multiplier_range[0], multiplier_range[1])
        first_part = a * k

        # Correct: total = (a+b) * k
        correct_total = (a + b) * k
        correct_answer = str(correct_total)

        # Malrule: Student uses division incorrectly
        # They think: first_part / a gives something, multiply by b?
        # Or: first_part * (b/a) - confused division
        malrule_total = round(first_part * (b / a))
        malrule_answer = str(malrule_total)

        variant = random.randint(0, 2)
        contexts = [
            f"A class has students in ratio {a}:{b} for group A to group B. If group A has {first_part} students, how many students are in the class total?",
            f"Prize money is split in ratio {a}:{b}. If the first person gets ${first_part}, what was the total prize?",
            f"A recipe divides ingredients in ratio {a}:{b}. If you use {first_part} cups of the first ingredient, how many cups total do you need?"
        ]

        text = contexts[variant]

        return Problem(
            text=text,
            operands=[a, b, first_part],
            operation='finding_total_from_part',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_context',
                'problem_type': 'finding_whole_from_part',
                'formula': 'a:b, given a*k, find (a+b)*k',
                'variant': variant,
                'ratio_a': a,
                'ratio_b': b,
                'first_part': first_part,
                'multiplier': k,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'is_word_problem': True
            }
        )
