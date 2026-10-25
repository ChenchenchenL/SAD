"""
Problem generator for Add-Under-Common-Root malrule.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, List
from utils import ProblemGenerator, Problem, DifficultyLevel


class AddUnderCommonRootProblemGenerator(ProblemGenerator):
    """Generates radical addition problems."""

    def get_available_templates(self) -> List[str]:
        """Return list of available template names."""
        return [
            'basic_addition',
            'basic_subtraction',
            'three_radicals',
            'word_problem_distance',
            'mixed_operations',
            'word_problem_addition',
            'word_problem_subtraction',
            'word_problem_three_radicals',
            'word_problem_mixed'
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        ranges = {
            8: {
                DifficultyLevel.EASY: {'perfect_square': (1, 9)},
                DifficultyLevel.MEDIUM: {'perfect_square': (1, 16)},
                DifficultyLevel.HARD: {'perfect_square': (1, 25)}
            },
            9: {
                DifficultyLevel.EASY: {'perfect_square': (1, 16)},
                DifficultyLevel.MEDIUM: {'perfect_square': (1, 25)},
                DifficultyLevel.HARD: {'perfect_square': (4, 36)}
            },
            10: {
                DifficultyLevel.EASY: {'perfect_square': (1, 25)},
                DifficultyLevel.MEDIUM: {'perfect_square': (4, 36)},
                DifficultyLevel.HARD: {'perfect_square': (4, 49)}
            }
        }
        lvl = self.level if self.level in ranges else 9
        return ranges[lvl][self.difficulty]

    def generate(self, seed=None, template=None) -> Problem:
        """Generate a problem, optionally using a specific template."""
        if seed is not None:
            random.seed(seed)

        # If no template specified, choose randomly
        if template is None:
            template = random.choice(self.get_available_templates())

        # Call the appropriate template generator
        if template == 'basic_addition':
            return self._generate_basic_addition()
        elif template == 'basic_subtraction':
            return self._generate_basic_subtraction()
        elif template == 'three_radicals':
            return self._generate_three_radicals()
        elif template == 'word_problem_distance':
            return self._generate_word_problem_distance()
        elif template == 'mixed_operations':
            return self._generate_mixed_operations()
        elif template == 'word_problem_addition':
            return self._generate_word_problem_addition()
        elif template == 'word_problem_subtraction':
            return self._generate_word_problem_subtraction()
        elif template == 'word_problem_three_radicals':
            return self._generate_word_problem_three_radicals()
        elif template == 'word_problem_mixed':
            return self._generate_word_problem_mixed()
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_addition(self) -> Problem:
        """Template 1: Basic addition √a² + √b²"""
        ranges = self.get_value_ranges()
        min_val, max_val = ranges['perfect_square']

        base1 = int((min_val ** 0.5))
        if base1 < 1:
            base1 = 1
        base2 = int((max_val ** 0.5))

        a = random.randint(base1, base2)
        b = random.randint(base1, base2)

        # Ensure a ≠ b
        attempts = 0
        while a == b and attempts < 20:
            b = random.randint(base1, base2)
            attempts += 1

        square_a = a ** 2
        square_b = b ** 2

        # Correct answer: √a² + √b² = a + b
        correct_answer = str(a + b)

        # Malrule answer: √(a² + b²)
        sum_of_squares = square_a + square_b
        malrule_answer = str(round(sum_of_squares ** 0.5, 2))

        text = f"Simplify √{square_a} + √{square_b}"

        return Problem(
            text=text,
            operands=[square_a, square_b],
            operation='radical_addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'basic_addition',
                'square_a': square_a,
                'square_b': square_b,
                'base_a': a,
                'base_b': b,
                'sum_of_squares': sum_of_squares,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_basic_subtraction(self) -> Problem:
        """Template 2: Basic subtraction √a² - √b²"""
        ranges = self.get_value_ranges()
        min_val, max_val = ranges['perfect_square']

        base1 = int((min_val ** 0.5))
        if base1 < 1:
            base1 = 1
        base2 = int((max_val ** 0.5))

        a = random.randint(base1, base2)
        b = random.randint(base1, base2)

        # Ensure a > b for positive result
        attempts = 0
        while a <= b and attempts < 20:
            a = random.randint(base1, base2)
            b = random.randint(base1, base2)
            attempts += 1

        square_a = a ** 2
        square_b = b ** 2

        # Correct answer: √a² - √b² = a - b
        correct_answer = str(a - b)

        # Malrule answer: √(a² - b²)
        diff_of_squares = square_a - square_b
        malrule_answer = str(round(diff_of_squares ** 0.5, 2))

        text = f"Simplify √{square_a} - √{square_b}"

        return Problem(
            text=text,
            operands=[square_a, square_b],
            operation='radical_subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'basic_subtraction',
                'square_a': square_a,
                'square_b': square_b,
                'base_a': a,
                'base_b': b,
                'diff_of_squares': diff_of_squares,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_three_radicals(self) -> Problem:
        """Template 3: Three radicals √a² + √b² + √c²"""
        ranges = self.get_value_ranges()
        min_val, max_val = ranges['perfect_square']

        base1 = int((min_val ** 0.5))
        if base1 < 1:
            base1 = 1
        base2 = int((max_val ** 0.5))

        a = random.randint(base1, base2)
        b = random.randint(base1, base2)
        c = random.randint(base1, base2)

        # Ensure all different
        attempts = 0
        while (a == b or b == c or a == c) and attempts < 20:
            b = random.randint(base1, base2)
            c = random.randint(base1, base2)
            attempts += 1

        square_a = a ** 2
        square_b = b ** 2
        square_c = c ** 2

        # Correct answer: √a² + √b² + √c² = a + b + c
        correct_answer = str(a + b + c)

        # Malrule answer: √(a² + b² + c²)
        sum_of_squares = square_a + square_b + square_c
        malrule_answer = str(round(sum_of_squares ** 0.5, 2))

        text = f"Simplify √{square_a} + √{square_b} + √{square_c}"

        return Problem(
            text=text,
            operands=[square_a, square_b, square_c],
            operation='radical_addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'three_radicals',
                'square_a': square_a,
                'square_b': square_b,
                'square_c': square_c,
                'base_a': a,
                'base_b': b,
                'base_c': c,
                'sum_of_squares': sum_of_squares,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_word_problem_distance(self) -> Problem:
        """Template 4: Word problem involving distances"""
        ranges = self.get_value_ranges()
        min_val, max_val = ranges['perfect_square']

        base1 = int((min_val ** 0.5))
        if base1 < 1:
            base1 = 1
        base2 = int((max_val ** 0.5))

        a = random.randint(base1, base2)
        b = random.randint(base1, base2)

        # Ensure a ≠ b
        attempts = 0
        while a == b and attempts < 20:
            b = random.randint(base1, base2)
            attempts += 1

        square_a = a ** 2
        square_b = b ** 2

        # Correct answer: a + b meters
        correct_answer = f"{a + b} meters"

        # Malrule answer: √(a² + b²) meters
        sum_of_squares = square_a + square_b
        malrule_value = round(sum_of_squares ** 0.5, 2)
        malrule_answer = f"{malrule_value} meters"

        text = (f"A hiker walks √{square_a} meters north and then √{square_b} meters north. "
                f"How far has the hiker walked in total?")

        return Problem(
            text=text,
            operands=[square_a, square_b],
            operation='radical_addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_distance',
                'square_a': square_a,
                'square_b': square_b,
                'base_a': a,
                'base_b': b,
                'sum_of_squares': sum_of_squares,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_mixed_operations(self) -> Problem:
        """Template 5: Mixed operations √a² + √b² - √c²"""
        ranges = self.get_value_ranges()
        min_val, max_val = ranges['perfect_square']

        base1 = int((min_val ** 0.5))
        if base1 < 1:
            base1 = 1
        base2 = int((max_val ** 0.5))

        a = random.randint(base1, base2)
        b = random.randint(base1, base2)
        c = random.randint(base1, base2)

        # Ensure a + b > c for positive result
        attempts = 0
        while (a == b or b == c or a == c or a + b <= c) and attempts < 20:
            b = random.randint(base1, base2)
            c = random.randint(base1, base2)
            attempts += 1

        square_a = a ** 2
        square_b = b ** 2
        square_c = c ** 2

        # Correct answer: √a² + √b² - √c² = a + b - c
        correct_answer = str(a + b - c)

        # Malrule answer: √(a² + b² - c²)
        mixed_squares = square_a + square_b - square_c
        malrule_answer = str(round(abs(mixed_squares) ** 0.5, 2))

        text = f"Simplify √{square_a} + √{square_b} - √{square_c}"

        return Problem(
            text=text,
            operands=[square_a, square_b, square_c],
            operation='radical_mixed',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'mixed_operations',
                'square_a': square_a,
                'square_b': square_b,
                'square_c': square_c,
                'base_a': a,
                'base_b': b,
                'base_c': c,
                'mixed_squares': mixed_squares,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_word_problem_addition(self) -> Problem:
        """Template 6: Word problem for addition √a² + √b² (3 variants)"""
        ranges = self.get_value_ranges()
        min_val, max_val = ranges['perfect_square']

        base1 = int((min_val ** 0.5))
        if base1 < 1:
            base1 = 1
        base2 = int((max_val ** 0.5))

        a = random.randint(base1, base2)
        b = random.randint(base1, base2)

        # Ensure a ≠ b
        attempts = 0
        while a == b and attempts < 20:
            b = random.randint(base1, base2)
            attempts += 1

        square_a = a ** 2
        square_b = b ** 2

        # Three context variants
        contexts = [
            {
                'type': 'rope_length',
                'text': f"Two ropes have lengths of √{square_a} meters and √{square_b} meters. If you connect them end-to-end, what is the total length?",
                'answer_unit': 'meters'
            },
            {
                'type': 'garden_perimeter',
                'text': f"A rectangular garden has two sides with lengths √{square_a} feet and √{square_b} feet. What is the sum of these two side lengths?",
                'answer_unit': 'feet'
            },
            {
                'type': 'distance_travel',
                'text': f"A car travels √{square_a} km on Monday and √{square_b} km on Tuesday. What is the total distance traveled?",
                'answer_unit': 'km'
            }
        ]

        context = random.choice(contexts)

        # Correct answer: √a² + √b² = a + b
        correct_answer = f"{a + b} {context['answer_unit']}"

        # Malrule answer: √(a² + b²)
        sum_of_squares = square_a + square_b
        malrule_value = round(sum_of_squares ** 0.5, 2)
        malrule_answer = f"{malrule_value} {context['answer_unit']}"

        return Problem(
            text=context['text'],
            operands=[square_a, square_b],
            operation='radical_addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_addition',
                'context_type': context['type'],
                'problem_type': 'addition',
                'square_a': square_a,
                'square_b': square_b,
                'base_a': a,
                'base_b': b,
                'sum_of_squares': sum_of_squares,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_word_problem_subtraction(self) -> Problem:
        """Template 7: Word problem for subtraction √a² - √b² (3 variants)"""
        ranges = self.get_value_ranges()
        min_val, max_val = ranges['perfect_square']

        base1 = int((min_val ** 0.5))
        if base1 < 1:
            base1 = 1
        base2 = int((max_val ** 0.5))

        a = random.randint(base1, base2)
        b = random.randint(base1, base2)

        # Ensure a > b for positive result
        attempts = 0
        while a <= b and attempts < 20:
            a = random.randint(base1, base2)
            b = random.randint(base1, base2)
            attempts += 1

        square_a = a ** 2
        square_b = b ** 2

        # Three context variants
        contexts = [
            {
                'type': 'rope_cutting',
                'text': f"You have a rope of length √{square_a} meters. If you cut off a piece of length √{square_b} meters, how much rope remains?",
                'answer_unit': 'meters'
            },
            {
                'type': 'distance_difference',
                'text': f"Town A is √{square_a} km from the city center, and Town B is √{square_b} km from the city center in the same direction. What is the distance between Town A and Town B?",
                'answer_unit': 'km'
            },
            {
                'type': 'height_difference',
                'text': f"A building has a height of √{square_a} meters, and a tree next to it has a height of √{square_b} meters. What is the difference in their heights?",
                'answer_unit': 'meters'
            }
        ]

        context = random.choice(contexts)

        # Correct answer: √a² - √b² = a - b
        correct_answer = f"{a - b} {context['answer_unit']}"

        # Malrule answer: √(a² - b²)
        diff_of_squares = square_a - square_b
        malrule_value = round(diff_of_squares ** 0.5, 2)
        malrule_answer = f"{malrule_value} {context['answer_unit']}"

        return Problem(
            text=context['text'],
            operands=[square_a, square_b],
            operation='radical_subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_subtraction',
                'context_type': context['type'],
                'problem_type': 'subtraction',
                'square_a': square_a,
                'square_b': square_b,
                'base_a': a,
                'base_b': b,
                'diff_of_squares': diff_of_squares,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_word_problem_three_radicals(self) -> Problem:
        """Template 8: Word problem for three radicals √a² + √b² + √c² (3 variants)"""
        ranges = self.get_value_ranges()
        min_val, max_val = ranges['perfect_square']

        base1 = int((min_val ** 0.5))
        if base1 < 1:
            base1 = 1
        base2 = int((max_val ** 0.5))

        a = random.randint(base1, base2)
        b = random.randint(base1, base2)
        c = random.randint(base1, base2)

        # Ensure all different
        attempts = 0
        while (a == b or b == c or a == c) and attempts < 20:
            b = random.randint(base1, base2)
            c = random.randint(base1, base2)
            attempts += 1

        square_a = a ** 2
        square_b = b ** 2
        square_c = c ** 2

        # Three context variants
        contexts = [
            {
                'type': 'three_segments',
                'text': f"Three segments of pipe have lengths √{square_a} meters, √{square_b} meters, and √{square_c} meters. What is the total length when they are connected end-to-end?",
                'answer_unit': 'meters'
            },
            {
                'type': 'perimeter',
                'text': f"A triangle has three sides with lengths √{square_a} cm, √{square_b} cm, and √{square_c} cm. What is the perimeter of the triangle?",
                'answer_unit': 'cm'
            },
            {
                'type': 'three_distances',
                'text': f"A delivery truck travels √{square_a} km on the first route, √{square_b} km on the second route, and √{square_c} km on the third route. What is the total distance traveled?",
                'answer_unit': 'km'
            }
        ]

        context = random.choice(contexts)

        # Correct answer: √a² + √b² + √c² = a + b + c
        correct_answer = f"{a + b + c} {context['answer_unit']}"

        # Malrule answer: √(a² + b² + c²)
        sum_of_squares = square_a + square_b + square_c
        malrule_value = round(sum_of_squares ** 0.5, 2)
        malrule_answer = f"{malrule_value} {context['answer_unit']}"

        return Problem(
            text=context['text'],
            operands=[square_a, square_b, square_c],
            operation='radical_addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_three_radicals',
                'context_type': context['type'],
                'problem_type': 'three_radicals',
                'square_a': square_a,
                'square_b': square_b,
                'square_c': square_c,
                'base_a': a,
                'base_b': b,
                'base_c': c,
                'sum_of_squares': sum_of_squares,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_word_problem_mixed(self) -> Problem:
        """Template 9: Word problem for mixed operations √a² + √b² - √c² (3 variants)"""
        ranges = self.get_value_ranges()
        min_val, max_val = ranges['perfect_square']

        base1 = int((min_val ** 0.5))
        if base1 < 1:
            base1 = 1
        base2 = int((max_val ** 0.5))

        a = random.randint(base1, base2)
        b = random.randint(base1, base2)
        c = random.randint(base1, base2)

        # Ensure a + b > c for positive result
        attempts = 0
        while (a == b or b == c or a == c or a + b <= c) and attempts < 20:
            b = random.randint(base1, base2)
            c = random.randint(base1, base2)
            attempts += 1

        square_a = a ** 2
        square_b = b ** 2
        square_c = c ** 2

        # Three context variants
        contexts = [
            {
                'type': 'budget',
                'text': f"A company receives funding of √{square_a} thousand dollars and √{square_b} thousand dollars from two sources, but spends √{square_c} thousand dollars on equipment. What is the net change in their budget (in thousands of dollars)?",
                'answer_unit': 'thousand dollars'
            },
            {
                'type': 'elevation',
                'text': f"A hiker climbs √{square_a} meters up a hill, then another √{square_b} meters up a second hill, and finally descends √{square_c} meters down a slope. What is the net change in elevation?",
                'answer_unit': 'meters'
            },
            {
                'type': 'material',
                'text': f"A construction project needs √{square_a} meters of wire for the first phase and √{square_b} meters for the second phase. However, √{square_c} meters of wire are defective and must be removed. How much usable wire remains?",
                'answer_unit': 'meters'
            }
        ]

        context = random.choice(contexts)

        # Correct answer: √a² + √b² - √c² = a + b - c
        correct_answer = f"{a + b - c} {context['answer_unit']}"

        # Malrule answer: √(a² + b² - c²)
        mixed_squares = square_a + square_b - square_c
        malrule_value = round(abs(mixed_squares) ** 0.5, 2)
        malrule_answer = f"{malrule_value} {context['answer_unit']}"

        return Problem(
            text=context['text'],
            operands=[square_a, square_b, square_c],
            operation='radical_mixed',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_mixed',
                'context_type': context['type'],
                'problem_type': 'mixed_operations',
                'square_a': square_a,
                'square_b': square_b,
                'square_c': square_c,
                'base_a': a,
                'base_b': b,
                'base_c': c,
                'mixed_squares': mixed_squares,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )
