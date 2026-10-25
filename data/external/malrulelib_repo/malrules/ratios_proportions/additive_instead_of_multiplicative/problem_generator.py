"""
Problem generator for Additive-Instead-Of-Multiplicative malrule.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, List
from utils import ProblemGenerator, Problem, DifficultyLevel


class AdditiveInsteadOfMultiplicativeProblemGenerator(ProblemGenerator):
    """Generates ratio scaling problems with template-based approach."""

    def get_available_templates(self) -> List[str]:
        """Return list of available template names."""
        return [
            'basic_scaling',
            'recipe_scaling',
            'speed_problems',
            'similar_figures',
            'mixture_problems',
            'word_problem_context'  # NEW: Covers all formula types with variants
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        ranges = {
            6: {
                DifficultyLevel.EASY: {'ratio': (2, 5), 'scale': (2, 4)},
                DifficultyLevel.MEDIUM: {'ratio': (2, 8), 'scale': (2, 6)},
                DifficultyLevel.HARD: {'ratio': (2, 10), 'scale': (2, 8)}
            },
            7: {
                DifficultyLevel.EASY: {'ratio': (2, 8), 'scale': (2, 6)},
                DifficultyLevel.MEDIUM: {'ratio': (2, 10), 'scale': (2, 8)},
                DifficultyLevel.HARD: {'ratio': (2, 12), 'scale': (2, 10)}
            },
            8: {
                DifficultyLevel.EASY: {'ratio': (2, 10), 'scale': (2, 8)},
                DifficultyLevel.MEDIUM: {'ratio': (2, 12), 'scale': (2, 10)},
                DifficultyLevel.HARD: {'ratio': (2, 15), 'scale': (3, 12)}
            },
            9: {
                DifficultyLevel.EASY: {'ratio': (2, 12), 'scale': (2, 10)},
                DifficultyLevel.MEDIUM: {'ratio': (3, 15), 'scale': (3, 12)},
                DifficultyLevel.HARD: {'ratio': (3, 20), 'scale': (4, 15)}
            }
        }
        lvl = self.level if self.level in ranges else 7
        return ranges[lvl][self.difficulty]

    def generate(self, seed=None, template=None) -> Problem:
        """
        Generate a problem, optionally using a specific template.

        Args:
            seed: Random seed for reproducibility
            template: Specific template name to use (or None for random)
        """
        if seed is not None:
            random.seed(seed)

        # Choose template
        available_templates = self.get_available_templates()
        if template is None:
            template = random.choice(available_templates)
        elif template not in available_templates:
            raise ValueError(f"Template '{template}' not available. Choose from: {available_templates}")

        # Generate based on template
        if template == 'basic_scaling':
            return self._generate_basic_scaling()
        elif template == 'recipe_scaling':
            return self._generate_recipe_scaling()
        elif template == 'speed_problems':
            return self._generate_speed_problems()
        elif template == 'similar_figures':
            return self._generate_similar_figures()
        elif template == 'mixture_problems':
            return self._generate_mixture_problems()
        elif template == 'word_problem_context':
            return self._generate_word_problem_context()
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_scaling(self) -> Problem:
        """Generate basic ratio scaling problem."""
        ranges = self.get_value_ranges()
        ratio_range = ranges['ratio']
        scale_range = ranges['scale']

        # Generate initial ratio a:b
        a = random.randint(ratio_range[0], ratio_range[1])
        b = random.randint(ratio_range[0], ratio_range[1])

        # Ensure a ≠ b for clarity
        attempts = 0
        while a == b and attempts < 20:
            b = random.randint(ratio_range[0], ratio_range[1])
            attempts += 1

        # Generate scale factor
        scale_factor = random.randint(scale_range[0], scale_range[1])

        # Correct answer: multiply both parts by scale factor
        correct_a = a * scale_factor
        correct_b = b * scale_factor
        correct_answer = f"{correct_a}:{correct_b}"

        # Malrule answer: add scale factor to both parts (additive scaling)
        malrule_a = a + scale_factor
        malrule_b = b + scale_factor
        malrule_answer = f"{malrule_a}:{malrule_b}"

        text = f"Scale the ratio {a}:{b} by a factor of {scale_factor}. What is the new ratio?"

        return Problem(
            text=text,
            operands=[a, b, scale_factor],
            operation='ratio_scaling',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'basic_scaling',
                'initial_a': a,
                'initial_b': b,
                'scale_factor': scale_factor,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_recipe_scaling(self) -> Problem:
        """Generate recipe scaling problem."""
        # Recipe ingredient ratios - scale by factor
        recipes = [
            (2, 3, 'cups of flour', 'cups of sugar'),
            (3, 4, 'eggs', 'cups of milk'),
            (1, 2, 'teaspoons of salt', 'tablespoons of butter'),
            (4, 5, 'ounces of chocolate', 'ounces of cream'),
            (2, 5, 'cups of water', 'cups of rice'),
            (3, 2, 'tablespoons of oil', 'cups of flour')
        ]
        amount1, amount2, ingredient1, ingredient2 = random.choice(recipes)

        ranges = self.get_value_ranges()
        scale_factor = random.randint(ranges['scale'][0], ranges['scale'][1])

        # Correct: multiply both amounts
        correct_amount1 = amount1 * scale_factor
        correct_amount2 = amount2 * scale_factor
        correct_answer = f"{correct_amount1} {ingredient1} and {correct_amount2} {ingredient2}"

        # Malrule: add to both amounts
        malrule_amount1 = amount1 + scale_factor
        malrule_amount2 = amount2 + scale_factor
        malrule_answer = f"{malrule_amount1} {ingredient1} and {malrule_amount2} {ingredient2}"

        text = f"A recipe uses {amount1} {ingredient1} and {amount2} {ingredient2}. If you scale the recipe by a factor of {scale_factor}, how much of each ingredient do you need?"

        return Problem(
            text=text,
            operands=[amount1, amount2, scale_factor],
            operation='recipe_scaling',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'recipe_scaling',
                'initial_a': amount1,
                'initial_b': amount2,
                'scale_factor': scale_factor,
                'ingredient1': ingredient1,
                'ingredient2': ingredient2,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_speed_problems(self) -> Problem:
        """Generate speed/rate problem with proportional reasoning."""
        # Speed problems: if car travels X miles in Y hours, how far in Z hours?
        speeds = [
            (60, 2, 'miles', 'hours'),
            (80, 3, 'miles', 'hours'),
            (45, 2, 'miles', 'hours'),
            (120, 4, 'kilometers', 'hours'),
            (90, 3, 'kilometers', 'hours'),
            (50, 2, 'feet', 'seconds')
        ]
        distance, time1, distance_unit, time_unit = random.choice(speeds)

        ranges = self.get_value_ranges()
        time2 = random.randint(ranges['scale'][0], min(ranges['scale'][1], 10))

        # Ensure time2 ≠ time1
        while time2 == time1:
            time2 = random.randint(ranges['scale'][0], min(ranges['scale'][1], 10))

        # Speed = distance / time
        speed = distance / time1

        # Correct: use multiplicative reasoning
        # distance2 = speed * time2 = (distance/time1) * time2
        correct_distance = int(speed * time2)
        correct_answer = f"{correct_distance} {distance_unit}"

        # Malrule: add the difference in times to distance
        # Student thinks: time increased by (time2-time1), so add that to distance
        time_diff = time2 - time1
        malrule_distance = distance + time_diff
        malrule_answer = f"{malrule_distance} {distance_unit}"

        text = f"A car travels {distance} {distance_unit} in {time1} {time_unit}. At the same speed, how far will it travel in {time2} {time_unit}?"

        return Problem(
            text=text,
            operands=[distance, time1, time2],
            operation='speed_scaling',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'speed_problems',
                'distance': distance,
                'time1': time1,
                'time2': time2,
                'speed': speed,
                'distance_unit': distance_unit,
                'time_unit': time_unit,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_similar_figures(self) -> Problem:
        """Generate similar figures/shapes scaling problem."""
        # Rectangle dimensions - scale by factor
        dimensions = [(3, 5), (4, 6), (2, 7), (5, 8), (3, 4), (6, 9)]
        width, height = random.choice(dimensions)

        ranges = self.get_value_ranges()
        scale_factor = random.randint(ranges['scale'][0], ranges['scale'][1])

        # Correct: multiply both dimensions
        correct_width = width * scale_factor
        correct_height = height * scale_factor
        correct_answer = f"{correct_width} cm by {correct_height} cm"

        # Malrule: add to both dimensions
        malrule_width = width + scale_factor
        malrule_height = height + scale_factor
        malrule_answer = f"{malrule_width} cm by {malrule_height} cm"

        text = f"A rectangle has dimensions {width} cm by {height} cm. If you scale it by a factor of {scale_factor}, what are the new dimensions?"

        return Problem(
            text=text,
            operands=[width, height, scale_factor],
            operation='shape_scaling',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'similar_figures',
                'initial_a': width,
                'initial_b': height,
                'scale_factor': scale_factor,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_mixture_problems(self) -> Problem:
        """Generate mixture concentration/ratio problem."""
        # Mixture ratios - scale by factor
        mixtures = [
            (1, 3, 'part juice', 'parts water'),
            (2, 5, 'parts concentrate', 'parts water'),
            (3, 7, 'parts syrup', 'parts soda'),
            (1, 4, 'part detergent', 'parts water'),
            (2, 3, 'parts paint', 'parts thinner'),
            (1, 2, 'part acid', 'parts water')
        ]
        parts1, parts2, component1, component2 = random.choice(mixtures)

        ranges = self.get_value_ranges()
        scale_factor = random.randint(ranges['scale'][0], ranges['scale'][1])

        # Correct: multiply both parts
        correct_parts1 = parts1 * scale_factor
        correct_parts2 = parts2 * scale_factor
        correct_answer = f"{correct_parts1}:{correct_parts2}"

        # Malrule: add to both parts
        malrule_parts1 = parts1 + scale_factor
        malrule_parts2 = parts2 + scale_factor
        malrule_answer = f"{malrule_parts1}:{malrule_parts2}"

        text = f"A mixture has a ratio of {parts1} {component1} to {parts2} {component2}. If you need to make {scale_factor} times as much mixture, what is the new ratio?"

        return Problem(
            text=text,
            operands=[parts1, parts2, scale_factor],
            operation='mixture_scaling',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'mixture_problems',
                'initial_a': parts1,
                'initial_b': parts2,
                'scale_factor': scale_factor,
                'component1': component1,
                'component2': component2,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_word_problem_context(self) -> Problem:
        """Generate word problem covering ALL formula types with 3 variants each."""
        # Select which formula type to embed
        formula_types = [
            'direct_proportion_unknown',  # a:b = c:?, find ?
            'part_to_whole_ratio',        # Given ratio a:b and total T, find parts
            'three_part_ratio_scaling',    # a:b:c scaled by k
            'finding_multiplier',          # a:b, given b*k, find k
            'compound_scaling'             # Scale ratio then scale again
        ]
        formula_type = random.choice(formula_types)

        if formula_type == 'direct_proportion_unknown':
            return self._word_problem_proportion_unknown()
        elif formula_type == 'part_to_whole_ratio':
            return self._word_problem_part_to_whole()
        elif formula_type == 'three_part_ratio_scaling':
            return self._word_problem_three_part_ratio()
        elif formula_type == 'finding_multiplier':
            return self._word_problem_finding_multiplier()
        elif formula_type == 'compound_scaling':
            return self._word_problem_compound_scaling()
        else:
            raise ValueError(f"Unknown formula type: {formula_type}")

    def _word_problem_proportion_unknown(self) -> Problem:
        """Formula: a:b = c:x, find x. Student uses addition instead of multiplication."""
        ranges = self.get_value_ranges()
        ratio_range = ranges['ratio']

        # Generate ratio a:b
        a = random.randint(ratio_range[0], ratio_range[1])
        b = random.randint(ratio_range[0], ratio_range[1])
        while a == b:
            b = random.randint(ratio_range[0], ratio_range[1])

        # Generate first quantity c
        k = random.randint(2, 5)
        c = a * k

        # Correct: x = b * k (multiplicative)
        correct_x = b * k
        correct_answer = str(correct_x)

        # Malrule: Student thinks "c is a + something, so x is b + same something"
        # difference = c - a, so x = b + difference (additive)
        difference = c - a
        malrule_x = b + difference
        malrule_answer = str(malrule_x)

        # 3 context variants
        variant = random.randint(0, 2)
        contexts = [
            f"If {a} apples cost ${b}, how much do {c} apples cost?",
            f"A car uses {b} gallons to travel {a} miles. How many gallons are needed for {c} miles?",
            f"If {a} workers complete a job in {b} hours, how long would {c} workers take (assuming same rate per worker)?"
        ]

        text = contexts[variant]

        return Problem(
            text=text,
            operands=[a, b, c],
            operation='proportion',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_context',
                'problem_type': 'direct_proportion_unknown',
                'formula': 'a:b = c:x',
                'variant': variant,
                'ratio_a': a,
                'ratio_b': b,
                'given_c': c,
                'multiplier': k,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'is_word_problem': True
            }
        )

    def _word_problem_part_to_whole(self) -> Problem:
        """Formula: Given ratio a:b and total T, find parts. Student uses addition."""
        ranges = self.get_value_ranges()
        ratio_range = ranges['ratio']

        # Generate ratio a:b
        a = random.randint(ratio_range[0], min(ratio_range[1], 8))
        b = random.randint(ratio_range[0], min(ratio_range[1], 8))
        while a == b:
            b = random.randint(ratio_range[0], min(ratio_range[1], 8))

        # Generate total T (must be multiple of a+b)
        k = random.randint(2, 5)
        total = (a + b) * k

        # Correct: part1 = a*k, part2 = b*k (multiplicative)
        correct_part1 = a * k
        correct_part2 = b * k
        correct_answer = f"{correct_part1} and {correct_part2}"

        # Malrule: Student adds instead
        # They might think: total = T, ratio difference = b-a, so split as a+something and b+something
        # Or: simply add scale factor to each part
        malrule_part1 = a + k
        malrule_part2 = b + k
        malrule_answer = f"{malrule_part1} and {malrule_part2}"

        # 3 context variants
        variant = random.randint(0, 2)
        contexts = [
            f"{total} students are divided into two groups in the ratio {a}:{b}. How many students are in each group?",
            f"A prize of ${total} is split between two winners in the ratio {a}:{b}. How much does each person get?",
            f"{total} marbles are shared between two children in the ratio {a}:{b}. How many marbles does each child receive?"
        ]

        text = contexts[variant]

        return Problem(
            text=text,
            operands=[a, b, total],
            operation='part_to_whole',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_context',
                'problem_type': 'part_to_whole_ratio',
                'formula': 'a:b with total T',
                'variant': variant,
                'ratio_a': a,
                'ratio_b': b,
                'total': total,
                'multiplier': k,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'is_word_problem': True
            }
        )

    def _word_problem_three_part_ratio(self) -> Problem:
        """Formula: a:b:c scaled by k. Student uses addition."""
        ranges = self.get_value_ranges()
        ratio_range = ranges['ratio']
        scale_range = ranges['scale']

        # Generate three-part ratio a:b:c
        a = random.randint(ratio_range[0], min(ratio_range[1], 6))
        b = random.randint(ratio_range[0], min(ratio_range[1], 6))
        c = random.randint(ratio_range[0], min(ratio_range[1], 6))

        # Ensure they're not all equal
        attempts = 0
        while (a == b == c) and attempts < 20:
            c = random.randint(ratio_range[0], min(ratio_range[1], 6))
            attempts += 1

        # Generate scale factor
        k = random.randint(scale_range[0], min(scale_range[1], 5))

        # Correct: (a*k):(b*k):(c*k)
        correct_a = a * k
        correct_b = b * k
        correct_c = c * k
        correct_answer = f"{correct_a}:{correct_b}:{correct_c}"

        # Malrule: (a+k):(b+k):(c+k)
        malrule_a = a + k
        malrule_b = b + k
        malrule_c = c + k
        malrule_answer = f"{malrule_a}:{malrule_b}:{malrule_c}"

        # 3 context variants
        variant = random.randint(0, 2)
        contexts = [
            f"A recipe for a cocktail uses juice, soda, and syrup in the ratio {a}:{b}:{c}. If you scale the recipe by a factor of {k}, what is the new ratio?",
            f"Three partners invest money in the ratio {a}:{b}:{c}. If they each scale up their investment by a factor of {k}, what is the new investment ratio?",
            f"A paint mixture combines red, blue, and yellow in the ratio {a}:{b}:{c}. To make {k} times as much paint, what should the new ratio be?"
        ]

        text = contexts[variant]

        return Problem(
            text=text,
            operands=[a, b, c, k],
            operation='three_part_ratio_scaling',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_context',
                'problem_type': 'three_part_ratio_scaling',
                'formula': 'a:b:c scaled by k',
                'variant': variant,
                'initial_a': a,
                'initial_b': b,
                'initial_c': c,
                'scale_factor': k,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'is_word_problem': True
            }
        )

    def _word_problem_finding_multiplier(self) -> Problem:
        """Formula: Given a:b and scaled value b*k, find k. Student uses addition."""
        ranges = self.get_value_ranges()
        ratio_range = ranges['ratio']

        # Generate ratio a:b
        a = random.randint(ratio_range[0], ratio_range[1])
        b = random.randint(ratio_range[0], ratio_range[1])
        while a == b:
            b = random.randint(ratio_range[0], ratio_range[1])

        # Generate multiplier k
        k = random.randint(2, 6)

        # Correct: k = (b*k) / b
        scaled_value = b * k
        correct_answer = str(k)

        # Malrule: Student thinks additively
        # They see scaled_value - b and think that's the answer
        malrule_k = scaled_value - b
        malrule_answer = str(malrule_k)

        # 3 context variants
        variant = random.randint(0, 2)
        contexts = [
            f"A map has a scale where {a} cm represents {b} km. If a road measures {scaled_value} km in reality, what is the scale factor being used?",
            f"A model car is built at a ratio of {a}:{b}. If the real car part is {scaled_value} inches, what scaling factor was applied?",
            f"A recipe ratio of flour to sugar is {a}:{b}. If you use {scaled_value} cups of sugar, by what factor did you scale the recipe?"
        ]

        text = contexts[variant]

        return Problem(
            text=text,
            operands=[a, b, scaled_value],
            operation='finding_scale_factor',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_context',
                'problem_type': 'finding_multiplier',
                'formula': 'find k given a:b and b*k',
                'variant': variant,
                'ratio_a': a,
                'ratio_b': b,
                'scaled_value': scaled_value,
                'multiplier': k,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'is_word_problem': True
            }
        )

    def _word_problem_compound_scaling(self) -> Problem:
        """Formula: Scale ratio a:b by k1, then by k2. Student uses addition."""
        ranges = self.get_value_ranges()
        ratio_range = ranges['ratio']

        # Generate ratio a:b
        a = random.randint(ratio_range[0], min(ratio_range[1], 5))
        b = random.randint(ratio_range[0], min(ratio_range[1], 5))
        while a == b:
            b = random.randint(ratio_range[0], min(ratio_range[1], 5))

        # Two scale factors
        k1 = random.randint(2, 4)
        k2 = random.randint(2, 3)

        # Correct: multiply both factors: (a*k1*k2):(b*k1*k2)
        correct_a = a * k1 * k2
        correct_b = b * k1 * k2
        correct_answer = f"{correct_a}:{correct_b}"

        # Malrule: add both factors: (a+k1+k2):(b+k1+k2)
        malrule_a = a + k1 + k2
        malrule_b = b + k1 + k2
        malrule_answer = f"{malrule_a}:{malrule_b}"

        # 3 context variants
        variant = random.randint(0, 2)
        contexts = [
            f"A photo with dimensions in ratio {a}:{b} is enlarged by a factor of {k1}, then enlarged again by a factor of {k2}. What is the final ratio?",
            f"A recipe with ratio {a}:{b} is scaled by {k1} for a party, then scaled by {k2} for a larger event. What is the final ratio?",
            f"An investment split {a}:{b} grows by a factor of {k1} in year 1, then by {k2} in year 2. What is the final investment ratio?"
        ]

        text = contexts[variant]

        return Problem(
            text=text,
            operands=[a, b, k1, k2],
            operation='compound_scaling',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_context',
                'problem_type': 'compound_scaling',
                'formula': 'a:b scaled by k1 then k2',
                'variant': variant,
                'initial_a': a,
                'initial_b': b,
                'scale_factor_1': k1,
                'scale_factor_2': k2,
                'combined_factor': k1 * k2,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'is_word_problem': True
            }
        )
