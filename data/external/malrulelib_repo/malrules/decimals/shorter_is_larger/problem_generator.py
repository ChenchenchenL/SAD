"""
Problem generator for Shorter-Is-Larger malrule.

Students incorrectly think decimals with fewer decimal places are larger.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional, List
from utils import ProblemGenerator, Problem, DifficultyLevel


class ShorterIsLargerProblemGenerator(ProblemGenerator):
    """Generates decimal comparison problems to elicit Shorter-Is-Larger malrule."""

    def get_available_templates(self) -> List[str]:
        """Return list of exactly 5 templates for this malrule."""
        return [
            'basic_comparison',        # 1 vs 2 decimal places
            'ordering',                # 3+ decimals with different lengths
            'money_context',           # Money comparison
            'measurement_context',     # Measurement comparison
            'number_line',             # Number line placement
            'word_problem_context'     # NEW: Covers all formula types with variants
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        ranges = {
            4: {DifficultyLevel.EASY: (0, 10), DifficultyLevel.MEDIUM: (0, 50), DifficultyLevel.HARD: (0, 100)},
            5: {DifficultyLevel.EASY: (0, 50), DifficultyLevel.MEDIUM: (0, 100), DifficultyLevel.HARD: (0, 500)},
            6: {DifficultyLevel.EASY: (0, 100), DifficultyLevel.MEDIUM: (0, 500), DifficultyLevel.HARD: (0, 1000)},
        }
        lvl = self.level if self.level in ranges else 5
        return {'values': ranges[lvl][self.difficulty]}

    def _generate_basic_comparison(self, seed=None) -> Problem:
        """Generate basic comparison: 1 vs 2 decimal places"""
        if seed is not None:
            random.seed(seed)

        value_range = self.get_value_ranges()['values']
        min_val, max_val = value_range

        # Generate shorter decimal (1 place) and longer decimal (2 places)
        # Make shorter decimal SMALLER in value but student thinks it's larger
        whole1 = random.randint(min_val, min(max_val, 20))
        decimal1 = random.randint(1, 9)
        shorter_decimal = float(f"{whole1}.{decimal1}")  # e.g., 3.5

        # Longer decimal should be LARGER in value
        whole2 = whole1  # Same whole part
        decimal2 = decimal1 * 10 + random.randint(1, 9)  # e.g., 3.56 (larger than 3.5)
        longer_decimal = float(f"{whole2}.{decimal2}")

        # Correct answer: longer decimal is larger
        correct_answer = longer_decimal
        # Malrule: student thinks shorter decimal is larger
        malrule_answer = shorter_decimal

        problem_text = f"Which is larger: {shorter_decimal} or {longer_decimal}?"

        return Problem(
            text=problem_text,
            operands=[shorter_decimal, longer_decimal],
            operation='comparison',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'basic_comparison',
                'shorter_decimal': shorter_decimal,
                'longer_decimal': longer_decimal,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'shorter_places': 1,
                'longer_places': 2
            }
        )

    def _generate_ordering(self, seed=None) -> Problem:
        """Generate ordering of 3-4 decimals with different lengths"""
        if seed is not None:
            random.seed(seed)

        value_range = self.get_value_ranges()['values']
        min_val, max_val = value_range

        # Generate 3 decimals: 1, 2, and 3 decimal places
        # Make the shortest one (1 place) the SMALLEST value
        whole = random.randint(min_val, min(max_val, 20))

        decimal1 = random.randint(1, 4)  # e.g., 5.2 (smallest value)
        num1 = float(f"{whole}.{decimal1}")

        decimal2 = decimal1 * 10 + random.randint(1, 9)  # e.g., 5.25
        num2 = float(f"{whole}.{decimal2}")

        decimal3 = decimal2 * 10 + random.randint(1, 9)  # e.g., 5.257 (largest value)
        num3 = float(f"{whole}.{decimal3}")

        decimals = [num1, num2, num3]

        # Correct answer: largest by value (num3)
        correct_answer = max(decimals)
        # Malrule: student thinks shortest is largest (num1)
        malrule_answer = num1

        problem_text = f"Which is the largest: {num1}, {num2}, or {num3}?"

        return Problem(
            text=problem_text,
            operands=decimals,
            operation='comparison',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'ordering',
                'decimals': decimals,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'num_count': 3
            }
        )

    def _generate_money_context(self, seed=None) -> Problem:
        """Generate money comparison"""
        if seed is not None:
            random.seed(seed)

        # Money: 1 vs 2 decimal places
        whole1 = random.randint(1, 50)
        decimal1 = random.randint(1, 9)
        shorter_amount = float(f"{whole1}.{decimal1}")

        # Longer decimal should be larger
        whole2 = whole1
        decimal2 = decimal1 * 10 + random.randint(1, 9)
        longer_amount = float(f"{whole2}.{decimal2}")

        correct_answer = longer_amount
        malrule_answer = shorter_amount

        problem_text = f"Which is more money: ${shorter_amount} or ${longer_amount}?"

        return Problem(
            text=problem_text,
            operands=[shorter_amount, longer_amount],
            operation='comparison',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'money_context',
                'shorter_amount': shorter_amount,
                'longer_amount': longer_amount,
                'correct_answer': f'${correct_answer}',
                'malrule_answer': f'${malrule_answer}',
                'context': 'money'
            }
        )

    def _generate_measurement_context(self, seed=None) -> Problem:
        """Generate measurement comparison"""
        if seed is not None:
            random.seed(seed)

        units = ['meters', 'seconds', 'kilograms', 'liters']
        unit = random.choice(units)

        value_range = self.get_value_ranges()['values']
        min_val, max_val = value_range

        # Generate shorter (1 place) vs longer (3 places)
        whole1 = random.randint(min_val, min(50, max_val))
        decimal1 = random.randint(1, 9)
        shorter_measure = float(f"{whole1}.{decimal1}")

        # Longer should be larger
        whole2 = whole1
        decimal2 = decimal1 * 100 + random.randint(10, 99)
        longer_measure = float(f"{whole2}.{decimal2}")

        correct_answer = longer_measure
        malrule_answer = shorter_measure

        problem_text = f"Which measurement is greater: {shorter_measure} {unit} or {longer_measure} {unit}?"

        return Problem(
            text=problem_text,
            operands=[shorter_measure, longer_measure],
            operation='comparison',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'measurement_context',
                'shorter_measure': shorter_measure,
                'longer_measure': longer_measure,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'context': 'measurement',
                'unit': unit
            }
        )

    def _generate_number_line(self, seed=None) -> Problem:
        """Generate number line placement"""
        if seed is not None:
            random.seed(seed)

        # Generate two decimals for number line
        whole = random.randint(0, 20)
        decimal1 = random.randint(1, 5)
        shorter_decimal = float(f"{whole}.{decimal1}")

        decimal2 = decimal1 * 10 + random.randint(1, 9)
        longer_decimal = float(f"{whole}.{decimal2}")

        correct_answer = longer_decimal
        malrule_answer = shorter_decimal

        contexts = [
            f"On a number line, which number is further to the right: {shorter_decimal} or {longer_decimal}?",
            f"Which number is closer to {whole + 1} on a number line: {shorter_decimal} or {longer_decimal}?",
            f"Between {shorter_decimal} and {longer_decimal}, which is greater?",
            f"Place these numbers on a number line. Which comes last: {shorter_decimal} or {longer_decimal}?"
        ]

        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[shorter_decimal, longer_decimal],
            operation='comparison',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'number_line',
                'shorter_decimal': shorter_decimal,
                'longer_decimal': longer_decimal,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer)
            }
        )

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate a decimal comparison problem.

        Args:
            seed: Optional random seed for reproducibility
            template: Optional template name. If None, random template is chosen.

        Returns:
            Problem instance
        """
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            template = random.choice(self.get_available_templates())

        # Validate template
        if template not in self.get_available_templates():
            raise ValueError(f"Invalid template: {template}")

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
            # Fallback
            return self._generate_basic_comparison(seed)

    def _generate_word_problem_context(self, seed=None):
        """Generate word problem covering ALL formula types with 3 variants each."""
        if seed is not None:
            random.seed(seed)

        # Select which formula type to embed
        formula_types = ['two_number_comparison', 'three_number_ordering']
        formula_type = random.choice(formula_types)
        variant = random.randint(0, 2)  # 3 variants per formula type

        if formula_type == 'two_number_comparison':
            value_range = self.get_value_ranges()['values']
            min_val, max_val = value_range

            # Generate shorter decimal (1 place) and longer decimal (2 places)
            # Make shorter decimal SMALLER in value but student thinks it's larger
            whole1 = random.randint(min_val, min(max_val, 20))
            decimal1 = random.randint(1, 9)
            shorter_decimal = float(f"{whole1}.{decimal1}")

            # Longer decimal should be LARGER in value
            whole2 = whole1  # Same whole part
            decimal2 = decimal1 * 10 + random.randint(1, 9)
            longer_decimal = float(f"{whole2}.{decimal2}")

            # Correct answer: longer decimal is larger
            correct_answer = longer_decimal
            # Malrule: student thinks shorter decimal is larger
            malrule_answer = shorter_decimal

            templates = [
                f"Maria has ${shorter_decimal} and Tom has ${longer_decimal}. Who has more money?",
                f"A rope is {shorter_decimal} meters long and another is {longer_decimal} meters long. Which rope is longer?",
                f"Which is heavier: a package weighing {shorter_decimal} kg or one weighing {longer_decimal} kg?"
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[shorter_decimal, longer_decimal],
                operation='comparison',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'template': 'word_problem_context',
                    'shorter_decimal': shorter_decimal,
                    'longer_decimal': longer_decimal,
                    'correct_answer': str(correct_answer),
                    'malrule_answer': str(malrule_answer),
                    'shorter_places': 1,
                    'longer_places': 2,
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        else:  # three_number_ordering
            value_range = self.get_value_ranges()['values']
            min_val, max_val = value_range

            # Generate 3 decimals: 1, 2, and 3 decimal places
            # Make the shortest one (1 place) the SMALLEST value
            whole = random.randint(min_val, min(max_val, 20))

            decimal1 = random.randint(1, 4)  # e.g., 5.2 (smallest value)
            num1 = float(f"{whole}.{decimal1}")

            decimal2 = decimal1 * 10 + random.randint(1, 9)  # e.g., 5.25
            num2 = float(f"{whole}.{decimal2}")

            decimal3 = decimal2 * 10 + random.randint(1, 9)  # e.g., 5.257 (largest value)
            num3 = float(f"{whole}.{decimal3}")

            decimals = [num1, num2, num3]
            random.shuffle(decimals)

            # Correct order: num1 < num2 < num3
            correct_order = [num1, num2, num3]
            # Malrule: shortest (1 place) is largest
            malrule_order = [num3, num2, num1]

            templates = [
                f"Three runners finished in times {decimals[0]} seconds, {decimals[1]} seconds, and {decimals[2]} seconds. Order them from fastest to slowest.",
                f"Three bags weigh {decimals[0]} kg, {decimals[1]} kg, and {decimals[2]} kg. Order them from lightest to heaviest.",
                f"Sarah scored {decimals[0]}, Tom scored {decimals[1]}, and Lisa scored {decimals[2]}. Order them from highest to lowest score."
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=decimals,
                operation='comparison',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'template': 'word_problem_context',
                    'decimals': decimals,
                    'shortest_decimal': num1,
                    'middle_decimal': num2,
                    'longest_decimal': num3,
                    'correct_answer': str(num3),  # The largest
                    'malrule_answer': str(num1),  # Incorrectly chosen as largest
                    'correct_order': ', '.join(str(d) for d in correct_order),
                    'malrule_order': ', '.join(str(d) for d in malrule_order),
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )
