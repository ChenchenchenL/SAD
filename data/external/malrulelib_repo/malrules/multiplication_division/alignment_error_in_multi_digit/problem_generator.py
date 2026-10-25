"""
Problem generator for Alignment-Error-In-Multi-Digit malrule.

Generates 2-digit by 2-digit multiplication problems to elicit the
misconception where students misalign partial products.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional, List
from utils import ProblemGenerator, Problem, DifficultyLevel


class AlignmentErrorProblemGenerator(ProblemGenerator):
    """
    Generates multi-digit multiplication problems to elicit Alignment-Error malrule.

    Focus on 2-digit × 2-digit multiplication where misalignment of partial
    products produces significantly different (incorrect) results.

    Templates:
    1. basic_2x2 - Standard 2-digit × 2-digit multiplication
    2. word_problem - Real-world contexts (arrays, groups, area)
    3. three_digit - 2-digit × 3-digit or 3-digit × 2-digit
    4. money_context - Dollar amounts and prices
    5. array_model - Describe rectangular arrays or area
    """

    def get_name(self) -> str:
        return "Alignment-Error-In-Multi-Digit Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates 2-digit by 2-digit multiplication problems where "
            "misaligning partial products leads to incorrect answers. "
            "Students fail to shift the second partial product one place left."
        )

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_2x2',
            'word_problem',
            'three_digit',
            'money_context',
            'array_model',
            'three_digit_times_three',
            'perimeter_then_area',
            'multi_item_purchase',
            'tiling_problem',
            'calendar_calculation'
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level and difficulty."""
        ranges = {
            3: {
                DifficultyLevel.EASY: (11, 19),      # 11-19 × 11-19
                DifficultyLevel.MEDIUM: (11, 29),     # 11-29 × 11-29
                DifficultyLevel.HARD: (11, 39),       # 11-39 × 11-39
            },
            4: {
                DifficultyLevel.EASY: (11, 29),
                DifficultyLevel.MEDIUM: (20, 49),     # 20-49 × 20-49
                DifficultyLevel.HARD: (30, 69),       # 30-69 × 30-69
            },
            5: {
                DifficultyLevel.EASY: (20, 49),
                DifficultyLevel.MEDIUM: (30, 69),
                DifficultyLevel.HARD: (40, 99),       # 40-99 × 40-99
            },
            6: {
                DifficultyLevel.EASY: (30, 69),
                DifficultyLevel.MEDIUM: (40, 99),
                DifficultyLevel.HARD: (50, 99),
            }
        }

        lvl = self.level if self.level in ranges else 4
        return {'numbers': ranges[lvl][self.difficulty]}

    def _generate_2digit_numbers(self, seed=None):
        """Generate two 2-digit numbers suitable for demonstrating the malrule."""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['numbers']

        # Generate two 2-digit numbers
        num1 = random.randint(min_val, max_val)
        num2 = random.randint(min_val, max_val)

        # Ensure both are truly 2-digit
        while num1 < 10 or num2 < 10:
            num1 = random.randint(min_val, max_val)
            num2 = random.randint(min_val, max_val)

        # Prefer cases where ones digits are not 0 or 1 (makes error more obvious)
        if random.random() < 0.7:
            while (num1 % 10 in [0, 1]) or (num2 % 10 in [0, 1]):
                num1 = random.randint(min_val, max_val)
                num2 = random.randint(min_val, max_val)

        return num1, num2

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate a multiplication problem based on selected template.

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
        if template == 'basic_2x2':
            return self._generate_basic_2x2(seed)
        elif template == 'word_problem':
            return self._generate_word_problem(seed)
        elif template == 'three_digit':
            return self._generate_three_digit(seed)
        elif template == 'money_context':
            return self._generate_money_context(seed)
        elif template == 'array_model':
            return self._generate_array_model(seed)
        elif template == 'three_digit_times_three':
            return self._generate_three_digit_times_three(seed)
        elif template == 'perimeter_then_area':
            return self._generate_perimeter_then_area(seed)
        elif template == 'multi_item_purchase':
            return self._generate_multi_item_purchase(seed)
        elif template == 'tiling_problem':
            return self._generate_tiling_problem(seed)
        elif template == 'calendar_calculation':
            return self._generate_calendar_calculation(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_2x2(self, seed=None) -> Problem:
        """Generate basic 2-digit × 2-digit multiplication."""
        if seed is not None:
            random.seed(seed)

        num1, num2 = self._generate_2digit_numbers(seed)

        # Calculate answers
        correct_answer = num1 * num2

        # Malrule answer: misalign partial products
        num2_ones = num2 % 10
        num2_tens = num2 // 10
        partial1 = num1 * num2_ones
        partial2_malrule = num1 * num2_tens  # Don't shift!
        malrule_answer = partial1 + partial2_malrule

        problem_texts = [
            f"Multiply {num1} × {num2}",
            f"What is {num1} × {num2}?",
            f"Calculate: {num1} × {num2}",
        ]
        problem_text = random.choice(problem_texts)

        return Problem(
            text=problem_text,
            operands=[num1, num2],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': num1,
                'num2': num2,
                'num1_tens': num1 // 10,
                'num1_ones': num1 % 10,
                'num2_tens': num2 // 10,
                'num2_ones': num2 % 10,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'template': 'basic_2x2',
                'problem_type': 'two_digit_multiplication'
            }
        )

    def _generate_word_problem(self, seed=None) -> Problem:
        """Generate word problem with real-world context."""
        if seed is not None:
            random.seed(seed)

        num1, num2 = self._generate_2digit_numbers(seed)

        # Calculate answers
        correct_answer = num1 * num2

        # Malrule answer
        num2_ones = num2 % 10
        num2_tens = num2 // 10
        partial1 = num1 * num2_ones
        partial2_malrule = num1 * num2_tens
        malrule_answer = partial1 + partial2_malrule

        contexts = [
            f"A school has {num1} classrooms with {num2} students in each classroom. How many students are there in total?",
            f"There are {num1} boxes, and each box contains {num2} toys. How many toys are there altogether?",
            f"A garden has {num1} rows of plants with {num2} plants in each row. How many plants are in the garden?",
            f"A theater has {num1} rows of seats with {num2} seats per row. What is the total seating capacity?",
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[num1, num2],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': num1,
                'num2': num2,
                'num1_tens': num1 // 10,
                'num1_ones': num1 % 10,
                'num2_tens': num2 // 10,
                'num2_ones': num2 % 10,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'template': 'word_problem',
                'problem_type': 'word_problem'
            }
        )

    def _generate_three_digit(self, seed=None) -> Problem:
        """Generate 2-digit × 3-digit multiplication (more partial products)."""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['numbers']

        # Generate a 2-digit number
        num1 = random.randint(min_val, max_val)
        while num1 < 10:
            num1 = random.randint(min_val, max_val)

        # Generate a 3-digit number
        num2 = random.randint(100, 199)

        # Calculate answers
        correct_answer = num1 * num2

        # Malrule: misalign all partial products after first
        num2_ones = num2 % 10
        num2_tens = (num2 // 10) % 10
        num2_hundreds = num2 // 100

        partial1 = num1 * num2_ones
        partial2_malrule = num1 * num2_tens  # Should be × 10
        partial3_malrule = num1 * num2_hundreds  # Should be × 100

        malrule_answer = partial1 + partial2_malrule + partial3_malrule

        problem_text = f"Calculate {num1} × {num2}"

        return Problem(
            text=problem_text,
            operands=[num1, num2],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': num1,
                'num2': num2,
                'num1_tens': num1 // 10,
                'num1_ones': num1 % 10,
                'num2_ones': num2_ones,
                'num2_tens': num2_tens,
                'num2_hundreds': num2_hundreds,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'template': 'three_digit',
                'is_3digit': True,
                'problem_type': 'three_digit_multiplication'
            }
        )

    def _generate_money_context(self, seed=None) -> Problem:
        """Generate money problem with prices."""
        if seed is not None:
            random.seed(seed)

        num1, num2 = self._generate_2digit_numbers(seed)

        # Calculate answers
        correct_answer = num1 * num2

        # Malrule answer
        num2_ones = num2 % 10
        num2_tens = num2 // 10
        partial1 = num1 * num2_ones
        partial2_malrule = num1 * num2_tens
        malrule_answer = partial1 + partial2_malrule

        contexts = [
            f"Each book costs ${num1}. If you buy {num2} books, how much do you pay in total?",
            f"A ticket costs ${num1}. What is the total cost for {num2} tickets?",
            f"You earn ${num1} per hour. How much do you earn in {num2} hours?",
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[num1, num2],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': num1,
                'num2': num2,
                'num1_tens': num1 // 10,
                'num1_ones': num1 % 10,
                'num2_tens': num2 // 10,
                'num2_ones': num2 % 10,
                'correct_answer': f'${correct_answer}',
                'malrule_answer': f'${malrule_answer}',
                'template': 'money_context',
                'problem_type': 'money_calculation'
            }
        )

    def _generate_array_model(self, seed=None) -> Problem:
        """Generate problem describing rectangular arrays or area."""
        if seed is not None:
            random.seed(seed)

        num1, num2 = self._generate_2digit_numbers(seed)

        # Calculate answers
        correct_answer = num1 * num2

        # Malrule answer
        num2_ones = num2 % 10
        num2_tens = num2 // 10
        partial1 = num1 * num2_ones
        partial2_malrule = num1 * num2_tens
        malrule_answer = partial1 + partial2_malrule

        contexts = [
            f"A rectangular room is {num1} feet long and {num2} feet wide. What is the area in square feet?",
            f"A parking lot has {num1} rows with {num2} parking spaces in each row. How many total parking spaces?",
            f"An array has {num1} rows and {num2} columns. How many elements are in the array?",
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[num1, num2],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': num1,
                'num2': num2,
                'num1_tens': num1 // 10,
                'num1_ones': num1 % 10,
                'num2_tens': num2 // 10,
                'num2_ones': num2 % 10,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'template': 'array_model',
                'problem_type': 'array_calculation'
            }
        )

    def _generate_three_digit_times_three(self, seed=None) -> Problem:
        """Generate 3-digit × 3-digit multiplication (e.g., 234 × 567)."""
        if seed is not None:
            random.seed(seed)

        # Generate two 3-digit numbers
        num1 = random.randint(100, 299)
        num2 = random.randint(100, 299)

        # Calculate correct answer
        correct_answer = num1 * num2

        # Malrule: misalign all partial products
        num2_ones = num2 % 10
        num2_tens = (num2 // 10) % 10
        num2_hundreds = num2 // 100

        partial1 = num1 * num2_ones
        partial2_malrule = num1 * num2_tens  # Should be × 10
        partial3_malrule = num1 * num2_hundreds  # Should be × 100

        malrule_answer = partial1 + partial2_malrule + partial3_malrule

        problem_texts = [
            f"Calculate {num1} × {num2}",
            f"What is {num1} × {num2}?",
            f"Multiply: {num1} × {num2}"
        ]
        problem_text = random.choice(problem_texts)

        return Problem(
            text=problem_text,
            operands=[num1, num2],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': num1,
                'num2': num2,
                'num1_hundreds': num1 // 100,
                'num1_tens': (num1 // 10) % 10,
                'num1_ones': num1 % 10,
                'num2_hundreds': num2_hundreds,
                'num2_tens': num2_tens,
                'num2_ones': num2_ones,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'template': 'three_digit_times_three',
                'problem_type': 'large_multiplication',
                'is_3digit': True,
            }
        )

    def _generate_perimeter_then_area(self, seed=None) -> Problem:
        """Generate multi-step geometry problem."""
        if seed is not None:
            random.seed(seed)

        num1, num2 = self._generate_2digit_numbers(seed)

        # Calculate area (the multiplication part)
        correct_answer = num1 * num2

        # Malrule answer for area calculation
        num2_ones = num2 % 10
        num2_tens = num2 // 10
        partial1 = num1 * num2_ones
        partial2_malrule = num1 * num2_tens
        malrule_answer = partial1 + partial2_malrule

        problem_texts = [
            f"A rectangle has length {num1} cm and width {num2} cm. Find its area in square centimeters.",
            f"Calculate the area of a rectangular field that is {num1} meters long and {num2} meters wide.",
            f"A garden plot measures {num1} feet by {num2} feet. What is the area?"
        ]
        problem_text = random.choice(problem_texts)

        return Problem(
            text=problem_text,
            operands=[num1, num2],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': num1,
                'num2': num2,
                'num1_tens': num1 // 10,
                'num1_ones': num1 % 10,
                'num2_tens': num2 // 10,
                'num2_ones': num2 % 10,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'template': 'perimeter_then_area',
                'problem_type': 'geometry_area'
            }
        )

    def _generate_multi_item_purchase(self, seed=None) -> Problem:
        """Generate problem with multiple items at different prices."""
        if seed is not None:
            random.seed(seed)

        num1, num2 = self._generate_2digit_numbers(seed)

        # Calculate correct total
        correct_answer = num1 * num2

        # Malrule answer
        num2_ones = num2 % 10
        num2_tens = num2 // 10
        partial1 = num1 * num2_ones
        partial2_malrule = num1 * num2_tens
        malrule_answer = partial1 + partial2_malrule

        items = ['notebooks', 'pens', 'pencils', 'markers', 'folders', 'binders']
        item = random.choice(items)

        problem_texts = [
            f"A store sells {item} for ${num1} each. If you buy {num2} {item}, how much do you spend?",
            f"You purchase {num2} {item} at ${num1} per item. What is the total cost?",
            f"Each {item[:-1]} costs ${num1}. Calculate the total for {num2} {item}."
        ]
        problem_text = random.choice(problem_texts)

        return Problem(
            text=problem_text,
            operands=[num1, num2],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': num1,
                'num2': num2,
                'num1_tens': num1 // 10,
                'num1_ones': num1 % 10,
                'num2_tens': num2 // 10,
                'num2_ones': num2 % 10,
                'item': item,
                'correct_answer': f'${correct_answer}',
                'malrule_answer': f'${malrule_answer}',
                'template': 'multi_item_purchase',
                'problem_type': 'shopping_calculation'
            }
        )

    def _generate_tiling_problem(self, seed=None) -> Problem:
        """Generate tiling/coverage problem (rows × columns)."""
        if seed is not None:
            random.seed(seed)

        num1, num2 = self._generate_2digit_numbers(seed)

        # Calculate correct total tiles
        correct_answer = num1 * num2

        # Malrule answer
        num2_ones = num2 % 10
        num2_tens = num2 // 10
        partial1 = num1 * num2_ones
        partial2_malrule = num1 * num2_tens
        malrule_answer = partial1 + partial2_malrule

        problem_texts = [
            f"A floor has {num1} rows of tiles with {num2} tiles per row. How many tiles cover the floor?",
            f"You need to tile a wall that is {num1} tiles wide and {num2} tiles tall. How many tiles do you need?",
            f"A checkerboard pattern has {num1} squares in one direction and {num2} in the other. How many squares total?"
        ]
        problem_text = random.choice(problem_texts)

        return Problem(
            text=problem_text,
            operands=[num1, num2],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': num1,
                'num2': num2,
                'num1_tens': num1 // 10,
                'num1_ones': num1 % 10,
                'num2_tens': num2 // 10,
                'num2_ones': num2 % 10,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'template': 'tiling_problem',
                'problem_type': 'tiling_coverage'
            }
        )

    def _generate_calendar_calculation(self, seed=None) -> Problem:
        """Generate calendar/time calculation (weeks × days, months × weeks, etc.)."""
        if seed is not None:
            random.seed(seed)

        num1, num2 = self._generate_2digit_numbers(seed)

        # Calculate correct total
        correct_answer = num1 * num2

        # Malrule answer
        num2_ones = num2 % 10
        num2_tens = num2 // 10
        partial1 = num1 * num2_ones
        partial2_malrule = num1 * num2_tens
        malrule_answer = partial1 + partial2_malrule

        contexts = [
            (f"If you work {num1} hours per week for {num2} weeks, how many total hours do you work?", "hours"),
            (f"A class meets {num1} minutes each day for {num2} days. How many total minutes?", "minutes"),
            (f"You read {num1} pages per day for {num2} days. How many pages total?", "pages")
        ]
        context, unit = random.choice(contexts)

        return Problem(
            text=context,
            operands=[num1, num2],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': num1,
                'num2': num2,
                'num1_tens': num1 // 10,
                'num1_ones': num1 % 10,
                'num2_tens': num2 // 10,
                'num2_ones': num2 % 10,
                'unit': unit,
                'correct_answer': f'{correct_answer} {unit}',
                'malrule_answer': f'{malrule_answer} {unit}',
                'template': 'calendar_calculation',
                'problem_type': 'time_calculation'
            }
        )
