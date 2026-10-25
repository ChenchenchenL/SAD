"""
Problem generator for Column-Mimics-Addition malrule.

Generates multi-digit multiplication problems where the malrule will produce
different answers than the correct algorithm. The malrule combines two bugs:
1. Column-by-column multiplication (mimicking addition structure)
2. Write-carry-forget-units (writing carry instead of units digit)
"""

import random
from typing import Dict, Tuple, Optional, List
import sys
sys.path.append('/Users/kitetsu/nlp_mac/malrule-coding')

from utils import Problem, ProblemGenerator, DifficultyLevel


class ColumnMimicsAdditionProblemGenerator(ProblemGenerator):
    """
    Generates multiplication problems where the Column-Mimics-Addition malrule
    will produce incorrect answers.

    The malrule treats multiplication like addition: multiplying corresponding
    digits column by column, and applying write-carry-forget-units to each
    column result.
    """

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level and difficulty."""
        ranges = {
            3: {
                DifficultyLevel.EASY: (10, 50),
                DifficultyLevel.MEDIUM: (20, 99),
                DifficultyLevel.HARD: (50, 999),
            },
            4: {
                DifficultyLevel.EASY: (10, 99),
                DifficultyLevel.MEDIUM: (100, 999),
                DifficultyLevel.HARD: (100, 9999),
            },
            5: {
                DifficultyLevel.EASY: (100, 999),
                DifficultyLevel.MEDIUM: (100, 9999),
                DifficultyLevel.HARD: (1000, 9999),
            }
        }

        # Default to level 4 if not in ranges
        lvl = self.level if self.level in ranges else 4
        return {'multiplicand': ranges[lvl][self.difficulty],
                'multiplier': ranges[lvl][self.difficulty]}

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_multiplication',
            'two_by_two',
            'three_by_two',
            'three_by_three',
            'word_problem_total',
            'word_problem_area',
        ]

    def _calculate_malrule_answer(self, multiplicand: int, multiplier: int) -> int:
        """
        Calculate the malrule answer for a multiplication problem.

        The malrule:
        1. Multiplies corresponding digits column by column (like addition)
        2. For each column product, if >= 10, writes the carry (tens digit)
           instead of the units digit (WRITE/CARRY/FORGET/UNITS)
        3. If product < 10, writes it normally
        4. When operands have different lengths, missing digits are treated as 1
           (multiplicative identity) - this matches Brown & Burton (1978) examples

        Args:
            multiplicand: First number
            multiplier: Second number

        Returns:
            The malrule answer
        """
        # Convert to digit lists (rightmost first for easier processing)
        m1_digits = [int(d) for d in str(multiplicand)][::-1]
        m2_digits = [int(d) for d in str(multiplier)][::-1]

        # Pad to same length using 1 (multiplicative identity) for missing digits
        # This matches Brown & Burton (1978) examples:
        # 734 x 37 = 792 (not 92), 2764 x 53 = 2731 (not 31)
        max_len = max(len(m1_digits), len(m2_digits))
        while len(m1_digits) < max_len:
            m1_digits.append(1)
        while len(m2_digits) < max_len:
            m2_digits.append(1)

        result_digits = []

        # Multiply column by column, applying write-carry-forget-units
        for i in range(max_len):
            product = m1_digits[i] * m2_digits[i]

            if product >= 10:
                # WRITE/CARRY/FORGET/UNITS: write the carry (tens digit)
                result_digits.append(product // 10)
            else:
                # Product < 10, write it normally
                result_digits.append(product)

        # Remove leading zeros
        while len(result_digits) > 1 and result_digits[-1] == 0:
            result_digits.pop()

        return int(''.join(str(d) for d in result_digits[::-1]))

    def _will_produce_different_answer(self, multiplicand: int, multiplier: int) -> bool:
        """
        Check if the malrule will produce a different answer than correct multiplication.

        Args:
            multiplicand: First number
            multiplier: Second number

        Returns:
            True if malrule answer differs from correct answer
        """
        correct = multiplicand * multiplier
        malrule = self._calculate_malrule_answer(multiplicand, multiplier)
        return correct != malrule

    def _generate_problem_text(self, multiplicand: int, multiplier: int,
                                problem_type: str) -> str:
        """
        Generate problem text based on problem type.

        Args:
            multiplicand: First number
            multiplier: Second number
            problem_type: Type of problem context

        Returns:
            Formatted problem text
        """
        if problem_type in ['basic', 'basic_multiplication', 'two_by_two',
                            'three_by_two', 'three_by_three']:
            templates = [
                f"What is {multiplicand} x {multiplier}?",
                f"Calculate: {multiplicand} x {multiplier}",
                f"Multiply {multiplicand} by {multiplier}.",
                f"Find the product of {multiplicand} and {multiplier}.",
            ]
            return random.choice(templates)

        elif problem_type == 'word_problem_total':
            contexts = [
                f"A store has {multiplicand} boxes, with {multiplier} items in each box. How many items are there in total?",
                f"There are {multiplicand} rows of chairs, with {multiplier} chairs in each row. How many chairs are there altogether?",
                f"A farmer has {multiplicand} trees, and each tree has {multiplier} apples. How many apples are there in total?",
                f"A school has {multiplicand} classrooms, with {multiplier} students in each. How many students are there?",
            ]
            return random.choice(contexts)

        elif problem_type == 'word_problem_area':
            contexts = [
                f"A rectangle has a length of {multiplicand} meters and a width of {multiplier} meters. What is its area?",
                f"A garden measures {multiplicand} feet by {multiplier} feet. What is the area of the garden?",
                f"A floor is {multiplicand} tiles long and {multiplier} tiles wide. How many tiles cover the floor?",
            ]
            return random.choice(contexts)

        else:
            return f"What is {multiplicand} x {multiplier}?"

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate a multiplication problem where Column-Mimics-Addition will fail.

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
        if template == 'basic_multiplication':
            return self._generate_basic_multiplication(seed)
        elif template == 'two_by_two':
            return self._generate_two_by_two(seed)
        elif template == 'three_by_two':
            return self._generate_three_by_two(seed)
        elif template == 'three_by_three':
            return self._generate_three_by_three(seed)
        elif template == 'word_problem_total':
            return self._generate_word_problem_total(seed)
        elif template == 'word_problem_area':
            return self._generate_word_problem_area(seed)
        else:
            return self._generate_basic_multiplication(seed)

    def _generate_basic_multiplication(self, seed: Optional[int] = None) -> Problem:
        """Template 1: Basic multiplication problems."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['multiplicand']

        # Try to generate a problem where malrule produces different answer
        for _ in range(100):
            multiplicand = random.randint(min_val, max_val)
            multiplier = random.randint(min_val, max_val)

            if self._will_produce_different_answer(multiplicand, multiplier):
                correct_answer = multiplicand * multiplier
                malrule_answer = self._calculate_malrule_answer(multiplicand, multiplier)
                problem_text = self._generate_problem_text(multiplicand, multiplier, 'basic')

                return Problem(
                    text=problem_text,
                    operands=[multiplicand, multiplier],
                    operation='multiplication',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'correct_answer': str(correct_answer),
                        'malrule_answer': str(malrule_answer),
                        'problem_type': 'basic',
                        'template': 'basic_multiplication'
                    }
                )

        # Fallback - use example from Brown & Burton
        multiplicand, multiplier = 68, 46
        correct_answer = multiplicand * multiplier
        malrule_answer = self._calculate_malrule_answer(multiplicand, multiplier)
        problem_text = self._generate_problem_text(multiplicand, multiplier, 'basic')

        return Problem(
            text=problem_text,
            operands=[multiplicand, multiplier],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'problem_type': 'basic',
                'template': 'basic_multiplication'
            }
        )

    def _generate_two_by_two(self, seed: Optional[int] = None) -> Problem:
        """Template 2: Two-digit by two-digit multiplication."""
        if seed is not None:
            random.seed(seed)

        # Force 2-digit numbers
        min_val, max_val = 10, 99

        for _ in range(100):
            multiplicand = random.randint(min_val, max_val)
            multiplier = random.randint(min_val, max_val)

            if self._will_produce_different_answer(multiplicand, multiplier):
                correct_answer = multiplicand * multiplier
                malrule_answer = self._calculate_malrule_answer(multiplicand, multiplier)
                problem_text = self._generate_problem_text(multiplicand, multiplier, 'two_by_two')

                return Problem(
                    text=problem_text,
                    operands=[multiplicand, multiplier],
                    operation='multiplication',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'correct_answer': str(correct_answer),
                        'malrule_answer': str(malrule_answer),
                        'problem_type': 'two_by_two',
                        'template': 'two_by_two'
                    }
                )

        # Fallback
        multiplicand, multiplier = 68, 46
        correct_answer = multiplicand * multiplier
        malrule_answer = self._calculate_malrule_answer(multiplicand, multiplier)
        problem_text = self._generate_problem_text(multiplicand, multiplier, 'two_by_two')

        return Problem(
            text=problem_text,
            operands=[multiplicand, multiplier],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'problem_type': 'two_by_two',
                'template': 'two_by_two'
            }
        )

    def _generate_three_by_two(self, seed: Optional[int] = None) -> Problem:
        """Template 3: Three-digit by two-digit multiplication."""
        if seed is not None:
            random.seed(seed)

        for _ in range(100):
            multiplicand = random.randint(100, 999)
            multiplier = random.randint(10, 99)

            if self._will_produce_different_answer(multiplicand, multiplier):
                correct_answer = multiplicand * multiplier
                malrule_answer = self._calculate_malrule_answer(multiplicand, multiplier)
                problem_text = self._generate_problem_text(multiplicand, multiplier, 'three_by_two')

                return Problem(
                    text=problem_text,
                    operands=[multiplicand, multiplier],
                    operation='multiplication',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'correct_answer': str(correct_answer),
                        'malrule_answer': str(malrule_answer),
                        'problem_type': 'three_by_two',
                        'template': 'three_by_two'
                    }
                )

        # Fallback - use example from Brown & Burton
        multiplicand, multiplier = 734, 37
        correct_answer = multiplicand * multiplier
        malrule_answer = self._calculate_malrule_answer(multiplicand, multiplier)
        problem_text = self._generate_problem_text(multiplicand, multiplier, 'three_by_two')

        return Problem(
            text=problem_text,
            operands=[multiplicand, multiplier],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'problem_type': 'three_by_two',
                'template': 'three_by_two'
            }
        )

    def _generate_three_by_three(self, seed: Optional[int] = None) -> Problem:
        """Template 4: Three-digit by three-digit multiplication."""
        if seed is not None:
            random.seed(seed)

        for _ in range(100):
            multiplicand = random.randint(100, 999)
            multiplier = random.randint(100, 999)

            if self._will_produce_different_answer(multiplicand, multiplier):
                correct_answer = multiplicand * multiplier
                malrule_answer = self._calculate_malrule_answer(multiplicand, multiplier)
                problem_text = self._generate_problem_text(multiplicand, multiplier, 'three_by_three')

                return Problem(
                    text=problem_text,
                    operands=[multiplicand, multiplier],
                    operation='multiplication',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'correct_answer': str(correct_answer),
                        'malrule_answer': str(malrule_answer),
                        'problem_type': 'three_by_three',
                        'template': 'three_by_three'
                    }
                )

        # Fallback - use example from Brown & Burton
        multiplicand, multiplier = 543, 206
        correct_answer = multiplicand * multiplier
        malrule_answer = self._calculate_malrule_answer(multiplicand, multiplier)
        problem_text = self._generate_problem_text(multiplicand, multiplier, 'three_by_three')

        return Problem(
            text=problem_text,
            operands=[multiplicand, multiplier],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'problem_type': 'three_by_three',
                'template': 'three_by_three'
            }
        )

    def _generate_word_problem_total(self, seed: Optional[int] = None) -> Problem:
        """Template 5: Word problems involving totals."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['multiplicand']

        for _ in range(100):
            multiplicand = random.randint(min_val, max_val)
            multiplier = random.randint(min_val, max_val)

            if self._will_produce_different_answer(multiplicand, multiplier):
                correct_answer = multiplicand * multiplier
                malrule_answer = self._calculate_malrule_answer(multiplicand, multiplier)
                problem_text = self._generate_problem_text(multiplicand, multiplier, 'word_problem_total')

                return Problem(
                    text=problem_text,
                    operands=[multiplicand, multiplier],
                    operation='multiplication',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'correct_answer': str(correct_answer),
                        'malrule_answer': str(malrule_answer),
                        'problem_type': 'word_problem_total',
                        'template': 'word_problem_total'
                    }
                )

        # Fallback
        multiplicand, multiplier = 68, 46
        correct_answer = multiplicand * multiplier
        malrule_answer = self._calculate_malrule_answer(multiplicand, multiplier)
        problem_text = self._generate_problem_text(multiplicand, multiplier, 'word_problem_total')

        return Problem(
            text=problem_text,
            operands=[multiplicand, multiplier],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'problem_type': 'word_problem_total',
                'template': 'word_problem_total'
            }
        )

    def _generate_word_problem_area(self, seed: Optional[int] = None) -> Problem:
        """Template 6: Word problems involving area calculations."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['multiplicand']

        for _ in range(100):
            multiplicand = random.randint(min_val, max_val)
            multiplier = random.randint(min_val, max_val)

            if self._will_produce_different_answer(multiplicand, multiplier):
                correct_answer = multiplicand * multiplier
                malrule_answer = self._calculate_malrule_answer(multiplicand, multiplier)
                problem_text = self._generate_problem_text(multiplicand, multiplier, 'word_problem_area')

                return Problem(
                    text=problem_text,
                    operands=[multiplicand, multiplier],
                    operation='multiplication',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'correct_answer': str(correct_answer),
                        'malrule_answer': str(malrule_answer),
                        'problem_type': 'word_problem_area',
                        'template': 'word_problem_area'
                    }
                )

        # Fallback
        multiplicand, multiplier = 68, 46
        correct_answer = multiplicand * multiplier
        malrule_answer = self._calculate_malrule_answer(multiplicand, multiplier)
        problem_text = self._generate_problem_text(multiplicand, multiplier, 'word_problem_area')

        return Problem(
            text=problem_text,
            operands=[multiplicand, multiplier],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'problem_type': 'word_problem_area',
                'template': 'word_problem_area'
            }
        )
