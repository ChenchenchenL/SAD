"""
Problem generator for Longer-Is-Larger malrule.

Generates decimal comparison problems designed to elicit the misconception
that more decimal digits means a larger number.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional, List
from utils import ProblemGenerator, Problem, DifficultyLevel


class LongerIsLargerProblemGenerator(ProblemGenerator):
    """
    Generates decimal comparison problems that elicit the Longer-Is-Larger malrule.

    The key is to generate pairs where one number has more decimal places but is
    actually smaller in value. For example: 0.5 vs 0.36, where 0.5 > 0.36 but
    students with this malrule will incorrectly say 0.36 > 0.5.

    Templates:
    1. basic_comparison - Simple which is larger comparison
    2. ordering - Order from smallest to largest
    3. money_context - Money comparison
    4. measurement_context - Measurement comparison
    5. number_line - Number line positioning
    """

    def get_name(self) -> str:
        return "Longer-Is-Larger Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates decimal comparison problems where one number has more "
            "decimal digits but is actually smaller. This elicits the misconception "
            "that more digits means a larger number."
        )

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_comparison',
            'ordering',
            'money_context',
            'measurement_context',
            'number_line',
            'word_problem_context'  # NEW: Covers all formula types with variants
        ]

    def get_value_ranges(self):
        """Get appropriate decimal ranges for the level."""
        # For decimal comparison, we don't use value ranges in the same way
        # as integer arithmetic, so we return a dummy range
        return {'decimal': (0, 1)}

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate a decimal comparison problem based on selected template.

        Args:
            seed: Optional random seed for reproducibility
            template: Specific template to use, or None for random selection

        Returns:
            Problem instance
        """
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            template = random.choice(self.get_available_templates())

        # Generate based on template
        if template == 'basic_comparison':
            return self._generate_basic_comparison(seed)
        elif template == 'ordering':
            return self._generate_ordering(seed)
        elif template == 'money_context':
            return self._generate_money_context(seed)
        elif template == 'measurement_context':
            return self._generate_measurement_context(seed)
        elif template == 'number_line':
            return self._generate_number_line(seed)
        elif template == 'word_problem_context':
            return self._generate_word_problem_context(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _get_decimal_places(self):
        """Get number of decimal places based on difficulty."""
        if self.difficulty == DifficultyLevel.EASY:
            shorter_places = 1
            longer_places = 2
        elif self.difficulty == DifficultyLevel.MEDIUM:
            shorter_places = random.choice([1, 2])
            longer_places = 3
        else:  # HARD
            shorter_places = random.choice([1, 2])
            longer_places = random.choice([3, 4])
        return shorter_places, longer_places

    def _generate_decimals(self, shorter_places: int, longer_places: int):
        """Generate a shorter (larger) and longer (smaller) decimal."""
        # Generate the shorter decimal (this will be the LARGER number)
        if shorter_places == 1:
            shorter_numerator = random.randint(5, 9)
            shorter_decimal = shorter_numerator / 10
        else:  # 2 places
            shorter_numerator = random.randint(30, 95)
            shorter_decimal = shorter_numerator / 100

        # Generate the longer decimal (this will be the SMALLER number)
        if longer_places == 2:
            max_numerator = int(shorter_decimal * 100) - 1
            if max_numerator < 10:
                max_numerator = int(shorter_decimal * 100) - 5
            longer_numerator = random.randint(10, max(10, max_numerator))
            longer_decimal = longer_numerator / 100
        elif longer_places == 3:
            max_numerator = int(shorter_decimal * 1000) - 1
            if max_numerator < 100:
                max_numerator = int(shorter_decimal * 1000) - 50
            longer_numerator = random.randint(100, max(100, max_numerator))
            longer_decimal = longer_numerator / 1000
        else:  # 4 places
            max_numerator = int(shorter_decimal * 10000) - 1
            if max_numerator < 1000:
                max_numerator = int(shorter_decimal * 10000) - 500
            longer_numerator = random.randint(1000, max(1000, max_numerator))
            longer_decimal = longer_numerator / 10000

        return shorter_decimal, longer_decimal

    def _generate_basic_comparison(self, seed=None) -> Problem:
        """Generate basic 'which is larger' comparison."""
        if seed is not None:
            random.seed(seed)

        shorter_places, longer_places = self._get_decimal_places()
        shorter_decimal, longer_decimal = self._generate_decimals(shorter_places, longer_places)

        # Randomly order
        if random.random() < 0.5:
            decimal1, decimal2 = shorter_decimal, longer_decimal
        else:
            decimal1, decimal2 = longer_decimal, shorter_decimal

        problem_texts = [
            f"Which is larger: {decimal1} or {decimal2}?",
            f"Which is greater: {decimal1} or {decimal2}?",
            f"Compare {decimal1} and {decimal2}. Which is larger?",
        ]
        problem_text = random.choice(problem_texts)

        return Problem(
            text=problem_text,
            operands=[decimal1, decimal2],
            operation='decimal_comparison',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'decimal1': decimal1,
                'decimal2': decimal2,
                'shorter_decimal': shorter_decimal,
                'longer_decimal': longer_decimal,
                'correct_answer': f'{shorter_decimal}',
                'malrule_answer': f'{longer_decimal}',
                'template': 'basic_comparison'
            }
        )

    def _generate_ordering(self, seed=None) -> Problem:
        """Generate ordering problem with 3 decimals."""
        if seed is not None:
            random.seed(seed)

        shorter_places, longer_places = self._get_decimal_places()
        shorter_decimal, longer_decimal = self._generate_decimals(shorter_places, longer_places)

        # Generate a middle decimal
        middle_places = 2 if longer_places >= 3 else longer_places
        if middle_places == 2:
            middle_numerator = random.randint(20, int(shorter_decimal * 100) - 10)
            middle_decimal = middle_numerator / 100
        else:
            middle_numerator = random.randint(200, int(shorter_decimal * 1000) - 50)
            middle_decimal = middle_numerator / 1000

        # Shuffle for presentation
        decimals = [shorter_decimal, longer_decimal, middle_decimal]
        random.shuffle(decimals)

        problem_texts = [
            f"Order from smallest to largest: {decimals[0]}, {decimals[1]}, {decimals[2]}",
            f"Which is the largest: {decimals[0]}, {decimals[1]}, or {decimals[2]}?",
            f"Arrange in ascending order: {decimals[0]}, {decimals[1]}, {decimals[2]}",
        ]
        problem_text = random.choice(problem_texts)

        # Correct order: longer_decimal < middle_decimal < shorter_decimal
        correct_order = sorted([shorter_decimal, longer_decimal, middle_decimal])

        # Malrule: orders by number of digits (more digits = larger)
        malrule_order = sorted(decimals, key=lambda x: len(str(x).split('.')[1]) if '.' in str(x) else 0, reverse=True)

        return Problem(
            text=problem_text,
            operands=decimals,
            operation='decimal_comparison',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'decimals': decimals,
                'shorter_decimal': shorter_decimal,
                'longer_decimal': longer_decimal,
                'middle_decimal': middle_decimal,
                'correct_answer': f'{shorter_decimal}',  # The largest
                'malrule_answer': f'{longer_decimal}',  # Incorrectly chosen as largest
                'correct_order': ', '.join(str(d) for d in correct_order),
                'malrule_order': ', '.join(str(d) for d in malrule_order),
                'template': 'ordering'
            }
        )

    def _generate_money_context(self, seed=None) -> Problem:
        """Generate money comparison problem."""
        if seed is not None:
            random.seed(seed)

        shorter_places, longer_places = self._get_decimal_places()
        shorter_decimal, longer_decimal = self._generate_decimals(shorter_places, longer_places)

        # Randomly order
        if random.random() < 0.5:
            decimal1, decimal2 = shorter_decimal, longer_decimal
        else:
            decimal1, decimal2 = longer_decimal, shorter_decimal

        contexts = [
            f"Sarah has ${decimal1} and Tom has ${decimal2}. Who has more money?",
            f"Which costs more: an item for ${decimal1} or one for ${decimal2}?",
            f"A book costs ${decimal1} and a pen costs ${decimal2}. Which is more expensive?",
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[decimal1, decimal2],
            operation='decimal_comparison',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'decimal1': decimal1,
                'decimal2': decimal2,
                'shorter_decimal': shorter_decimal,
                'longer_decimal': longer_decimal,
                'correct_answer': f'${shorter_decimal}',
                'malrule_answer': f'${longer_decimal}',
                'template': 'money_context'
            }
        )

    def _generate_measurement_context(self, seed=None) -> Problem:
        """Generate measurement comparison problem."""
        if seed is not None:
            random.seed(seed)

        shorter_places, longer_places = self._get_decimal_places()
        shorter_decimal, longer_decimal = self._generate_decimals(shorter_places, longer_places)

        # Randomly order
        if random.random() < 0.5:
            decimal1, decimal2 = shorter_decimal, longer_decimal
        else:
            decimal1, decimal2 = longer_decimal, shorter_decimal

        unit = random.choice(['meters', 'kilometers', 'liters', 'kilograms'])
        contexts = [
            f"Which is longer: {decimal1} {unit} or {decimal2} {unit}?",
            f"A rope is {decimal1} {unit} and another is {decimal2} {unit}. Which is longer?",
            f"Compare the measurements: {decimal1} {unit} and {decimal2} {unit}. Which is greater?",
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[decimal1, decimal2],
            operation='decimal_comparison',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'decimal1': decimal1,
                'decimal2': decimal2,
                'shorter_decimal': shorter_decimal,
                'longer_decimal': longer_decimal,
                'unit': unit,
                'correct_answer': f'{shorter_decimal} {unit}',
                'malrule_answer': f'{longer_decimal} {unit}',
                'template': 'measurement_context'
            }
        )

    def _generate_number_line(self, seed=None) -> Problem:
        """Generate number line positioning problem."""
        if seed is not None:
            random.seed(seed)

        shorter_places, longer_places = self._get_decimal_places()
        shorter_decimal, longer_decimal = self._generate_decimals(shorter_places, longer_places)

        # Randomly order
        if random.random() < 0.5:
            decimal1, decimal2 = shorter_decimal, longer_decimal
        else:
            decimal1, decimal2 = longer_decimal, shorter_decimal

        contexts = [
            f"Which number is closer to 1 on a number line: {decimal1} or {decimal2}?",
            f"On a number line from 0 to 1, which is further from 0: {decimal1} or {decimal2}?",
            f"Which decimal is positioned higher on a vertical number line: {decimal1} or {decimal2}?",
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[decimal1, decimal2],
            operation='decimal_comparison',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'decimal1': decimal1,
                'decimal2': decimal2,
                'shorter_decimal': shorter_decimal,
                'longer_decimal': longer_decimal,
                'correct_answer': f'{shorter_decimal}',
                'malrule_answer': f'{longer_decimal}',
                'template': 'number_line'
            }
        )

    def _generate_word_problem_context(self, seed=None):
        """Generate word problem covering ALL formula types with 3 variants each."""
        if seed is not None:
            random.seed(seed)

        # Select which formula type to embed
        formula_types = ['two_number_comparison', 'three_number_ordering']
        formula_type = random.choice(formula_types)
        variant = random.randint(0, 2)  # 3 variants per formula type

        if formula_type == 'two_number_comparison':
            shorter_places, longer_places = self._get_decimal_places()
            shorter_decimal, longer_decimal = self._generate_decimals(shorter_places, longer_places)

            # Randomly order
            if random.random() < 0.5:
                decimal1, decimal2 = shorter_decimal, longer_decimal
            else:
                decimal1, decimal2 = longer_decimal, shorter_decimal

            templates = [
                f"Maria has ${decimal1} and Tom has ${decimal2}. Who has more money?",
                f"A rope is {decimal1} meters long and another is {decimal2} meters long. Which rope is longer?",
                f"Which is heavier: a package weighing {decimal1} kg or one weighing {decimal2} kg?"
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[decimal1, decimal2],
                operation='decimal_comparison',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'decimal1': decimal1,
                    'decimal2': decimal2,
                    'shorter_decimal': shorter_decimal,
                    'longer_decimal': longer_decimal,
                    'correct_answer': f'{shorter_decimal}',
                    'malrule_answer': f'{longer_decimal}',
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        else:  # three_number_ordering
            shorter_places, longer_places = self._get_decimal_places()
            shorter_decimal, longer_decimal = self._generate_decimals(shorter_places, longer_places)

            # Generate a middle decimal
            middle_places = 2 if longer_places >= 3 else longer_places
            if middle_places == 2:
                middle_numerator = random.randint(20, int(shorter_decimal * 100) - 10)
                middle_decimal = middle_numerator / 100
            else:
                middle_numerator = random.randint(200, int(shorter_decimal * 1000) - 50)
                middle_decimal = middle_numerator / 1000

            # Shuffle for presentation
            decimals = [shorter_decimal, longer_decimal, middle_decimal]
            random.shuffle(decimals)

            # Correct order: longer_decimal < middle_decimal < shorter_decimal
            correct_order = sorted([shorter_decimal, longer_decimal, middle_decimal])

            # Malrule: orders by number of digits (more digits = larger)
            malrule_order = sorted(decimals, key=lambda x: len(str(x).split('.')[1]) if '.' in str(x) else 0, reverse=True)

            templates = [
                f"Three runners finished in times {decimals[0]} seconds, {decimals[1]} seconds, and {decimals[2]} seconds. Order them from fastest to slowest.",
                f"Three bags weigh {decimals[0]} kg, {decimals[1]} kg, and {decimals[2]} kg. Order them from lightest to heaviest.",
                f"Sarah scored {decimals[0]}, Tom scored {decimals[1]}, and Lisa scored {decimals[2]}. Order them from highest to lowest score."
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=decimals,
                operation='decimal_comparison',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'decimals': decimals,
                    'shorter_decimal': shorter_decimal,
                    'longer_decimal': longer_decimal,
                    'middle_decimal': middle_decimal,
                    'correct_answer': f'{shorter_decimal}',  # The largest
                    'malrule_answer': f'{longer_decimal}',  # Incorrectly chosen as largest
                    'correct_order': ', '.join(str(d) for d in correct_order),
                    'malrule_order': ', '.join(str(d) for d in malrule_order),
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )
