"""
Problem generator for Carry-Not-Reset malrule.

Generates multi-digit addition problems where the malrule will produce
different answers than the correct algorithm. Problems must have multiple
carries to demonstrate the cumulative carry error.
"""

import random
from typing import Dict, Tuple, Optional, List
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import Problem, ProblemGenerator, DifficultyLevel


class CarryNotResetProblemGenerator(ProblemGenerator):
    """
    Generates addition problems where the Carry-Not-Reset malrule will
    produce incorrect answers.

    For the malrule to manifest differently from correct addition, the problem
    must have at least two carries in succession (or with a non-carry column
    between them where the accumulated carry would still affect the result).

    Critical Constraint: Multiple carry-producing columns required
    ---------------------------------------------------------------
    The malrule only produces a different answer when:
    1. A carry is generated in one column
    2. The next column's sum is < 10 (so carry SHOULD reset to 0)
    3. But the malrule keeps the carry, making the result too large

    Single-carry problems (e.g., 18 + 21 = 39) produce identical results
    because the carry is never "not reset" - it's just used once.

    Fallback constructs numbers with pattern X28 + Y17 which guarantees:
    - Col 0: 8+7=15 (carry=1)
    - Col 1: 2+1+1=4 (carry should reset to 0, but malrule keeps it)
    - Col 2: X+Y+1 (extra 1 from unreset carry causes error)
    The hundreds digits (X, Y) are randomized for variety.
    """

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level and difficulty."""
        ranges = {
            2: {
                DifficultyLevel.EASY: (10, 99),
                DifficultyLevel.MEDIUM: (50, 99),
                DifficultyLevel.HARD: (100, 500),
            },
            3: {
                DifficultyLevel.EASY: (100, 500),
                DifficultyLevel.MEDIUM: (200, 999),
                DifficultyLevel.HARD: (500, 999),
            },
            4: {
                DifficultyLevel.EASY: (100, 999),
                DifficultyLevel.MEDIUM: (500, 9999),
                DifficultyLevel.HARD: (1000, 9999),
            }
        }

        # Default to level 3 if not in ranges
        lvl = self.level if self.level in ranges else 3
        return {'addend': ranges[lvl][self.difficulty]}

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_addition',
            'three_digit',
            'word_problem_total',
            'word_problem_combine',
        ]

    def _count_carries(self, num1: int, num2: int) -> int:
        """
        Count the number of carries that would occur in correct addition.

        Args:
            num1: First addend
            num2: Second addend

        Returns:
            Number of carries
        """
        num1_digits = [int(d) for d in str(num1)][::-1]
        num2_digits = [int(d) for d in str(num2)][::-1]

        # Pad to same length
        max_len = max(len(num1_digits), len(num2_digits))
        while len(num1_digits) < max_len:
            num1_digits.append(0)
        while len(num2_digits) < max_len:
            num2_digits.append(0)

        carry = 0
        carry_count = 0

        for i in range(max_len):
            column_sum = num1_digits[i] + num2_digits[i] + carry
            if column_sum >= 10:
                carry = column_sum // 10
                carry_count += 1
            else:
                carry = 0

        return carry_count

    def _has_carry_not_reset_opportunity(self, num1: int, num2: int) -> bool:
        """
        Check if problem will produce different answers with malrule vs correct.

        The malrule produces different results when there are at least 2 carries
        and subsequent columns would be affected by the accumulated carry.

        Args:
            num1: First addend
            num2: Second addend

        Returns:
            True if malrule will produce different answer from correct algorithm
        """
        # Calculate correct answer
        correct = num1 + num2

        # Calculate malrule answer
        malrule = self._calculate_malrule_answer(num1, num2)

        return correct != malrule

    def _calculate_malrule_answer(self, num1: int, num2: int) -> int:
        """
        Calculate the answer using the Carry-Not-Reset malrule.

        The bug: After a carry is generated, the student forgets to reset it to 0.
        The carry persists across columns even when the column sum < 10.
        However, the carry doesn't accumulate - it just never gets cleared.

        Example: 328 + 917 = 1345 (correct: 1245)
          - Col 0: 8+7=15, write 5, carry=1
          - Col 1: 2+1+1=4, write 4, carry should be 0 but stays 1 (BUG!)
          - Col 2: 3+9+1=13, write 3, carry=1 (new carry replaces old)
          - Final: write 1
          - Result: 1345

        Args:
            num1: First addend
            num2: Second addend

        Returns:
            Malrule answer (with persistent, non-resetting carry)
        """
        num1_digits = [int(d) for d in str(num1)][::-1]
        num2_digits = [int(d) for d in str(num2)][::-1]

        # Pad to same length
        max_len = max(len(num1_digits), len(num2_digits))
        while len(num1_digits) < max_len:
            num1_digits.append(0)
        while len(num2_digits) < max_len:
            num2_digits.append(0)

        result_digits = []
        carry = 0  # MALRULE: This never gets reset to 0!

        for i in range(max_len):
            column_sum = num1_digits[i] + num2_digits[i] + carry

            if column_sum >= 10:
                result_digits.append(column_sum % 10)
                # New carry generated - update carry value
                carry = column_sum // 10
            else:
                result_digits.append(column_sum)
                # MALRULE: No new carry, but old carry persists (NOT reset to 0!)
                # carry stays at its current value

        # Add any remaining carry
        if carry > 0:
            for digit in str(carry)[::-1]:
                result_digits.append(int(digit))

        # Convert back to integer
        result_digits = result_digits[::-1]
        return int(''.join(str(d) for d in result_digits))

    def _generate_problem_text(self, num1: int, num2: int, problem_type: str) -> str:
        """
        Generate problem text based on problem type.

        Args:
            num1: First addend
            num2: Second addend
            problem_type: Type of problem context

        Returns:
            Formatted problem text
        """
        if problem_type == 'basic':
            templates = [
                f"What is {num1} + {num2}?",
                f"Calculate: {num1} + {num2}",
                f"Add {num1} and {num2}.",
                f"Find the sum of {num1} and {num2}.",
            ]
            return random.choice(templates)

        elif problem_type == 'word_problem_total':
            contexts = [
                f"A store sold {num1} items on Monday and {num2} items on Tuesday. How many items were sold in total?",
                f"Maria collected {num1} stickers and then found {num2} more. How many stickers does she have now?",
                f"A farm has {num1} chickens and {num2} ducks. How many birds are there in total?",
                f"Tom read {num1} pages on Saturday and {num2} pages on Sunday. How many pages did he read in total?",
            ]
            return random.choice(contexts)

        elif problem_type == 'word_problem_combine':
            contexts = [
                f"School A has {num1} students and School B has {num2} students. How many students are there altogether?",
                f"A red box contains {num1} marbles and a blue box contains {num2} marbles. What is the total number of marbles?",
                f"Jake has ${num1} and Emma has ${num2}. How much money do they have together?",
                f"There are {num1} boys and {num2} girls in the school. How many students are there in all?",
            ]
            return random.choice(contexts)

        elif problem_type == 'three_digit':
            templates = [
                f"What is {num1} + {num2}?",
                f"Calculate: {num1} + {num2}",
                f"Add: {num1} + {num2}",
                f"A library has {num1} fiction books and {num2} non-fiction books. How many books are there?",
            ]
            return random.choice(templates)

        else:
            return f"What is {num1} + {num2}?"

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate an addition problem where Carry-Not-Reset will fail.

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
        if template == 'basic_addition':
            return self._generate_basic_addition(seed)
        elif template == 'three_digit':
            return self._generate_three_digit(seed)
        elif template == 'word_problem_total':
            return self._generate_word_problem_total(seed)
        elif template == 'word_problem_combine':
            return self._generate_word_problem_combine(seed)
        else:
            return self._generate_basic_addition(seed)

    def _generate_basic_addition(self, seed: Optional[int] = None) -> Problem:
        """Template 1: Basic addition problems."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['addend']

        # Try to generate a problem with carry-not-reset opportunity
        for _ in range(100):
            num1 = random.randint(min_val, max_val)
            num2 = random.randint(min_val, max_val)

            if self._has_carry_not_reset_opportunity(num1, num2):
                correct_answer = num1 + num2
                malrule_answer = self._calculate_malrule_answer(num1, num2)
                problem_text = self._generate_problem_text(num1, num2, 'basic')

                return Problem(
                    text=problem_text,
                    operands=[num1, num2],
                    operation='addition',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'has_carry_not_reset': True,
                        'problem_type': 'basic',
                        'template': 'basic_addition',
                        'num_carries': self._count_carries(num1, num2),
                        'correct_answer': str(correct_answer),
                        'malrule_answer': str(malrule_answer),
                    }
                )

        # Fallback: construct numbers that guarantee carry interaction
        # ones: 8+7=15 (carry=1), tens: 2+1=3 (carry should reset but doesn't)
        hund_1, hund_2 = random.randint(1, 9), random.randint(1, 9)
        num1 = hund_1 * 100 + 28  # X28
        num2 = hund_2 * 100 + 17  # Y17
        correct_answer = num1 + num2
        malrule_answer = self._calculate_malrule_answer(num1, num2)
        problem_text = self._generate_problem_text(num1, num2, 'basic')

        return Problem(
            text=problem_text,
            operands=[num1, num2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'has_carry_not_reset': True,
                'problem_type': 'basic',
                'template': 'basic_addition',
                'num_carries': self._count_carries(num1, num2),
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
            }
        )

    def _generate_three_digit(self, seed: Optional[int] = None) -> Problem:
        """Template 2: Three-digit addition problems."""
        if seed is not None:
            random.seed(seed)

        # Force 3-digit range for good carry demonstration
        min_val, max_val = 100, 999

        for _ in range(100):
            num1 = random.randint(min_val, max_val)
            num2 = random.randint(min_val, max_val)

            if self._has_carry_not_reset_opportunity(num1, num2):
                correct_answer = num1 + num2
                malrule_answer = self._calculate_malrule_answer(num1, num2)
                problem_text = self._generate_problem_text(num1, num2, 'three_digit')

                return Problem(
                    text=problem_text,
                    operands=[num1, num2],
                    operation='addition',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'has_carry_not_reset': True,
                        'problem_type': 'three_digit',
                        'template': 'three_digit',
                        'num_carries': self._count_carries(num1, num2),
                        'correct_answer': str(correct_answer),
                        'malrule_answer': str(malrule_answer),
                    }
                )

        # Fallback: construct numbers that guarantee carry interaction
        # ones: 8+7=15 (carry=1), tens: 2+1=3 (carry should reset but doesn't)
        hund_1, hund_2 = random.randint(1, 9), random.randint(1, 9)
        num1 = hund_1 * 100 + 28  # X28
        num2 = hund_2 * 100 + 17  # Y17
        correct_answer = num1 + num2
        malrule_answer = self._calculate_malrule_answer(num1, num2)
        problem_text = self._generate_problem_text(num1, num2, 'three_digit')

        return Problem(
            text=problem_text,
            operands=[num1, num2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'has_carry_not_reset': True,
                'problem_type': 'three_digit',
                'template': 'three_digit',
                'num_carries': self._count_carries(num1, num2),
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
            }
        )

    def _generate_word_problem_total(self, seed: Optional[int] = None) -> Problem:
        """Template 3: Word problems about finding totals."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['addend']

        for _ in range(100):
            num1 = random.randint(min_val, max_val)
            num2 = random.randint(min_val, max_val)

            if self._has_carry_not_reset_opportunity(num1, num2):
                correct_answer = num1 + num2
                malrule_answer = self._calculate_malrule_answer(num1, num2)
                problem_text = self._generate_problem_text(num1, num2, 'word_problem_total')

                return Problem(
                    text=problem_text,
                    operands=[num1, num2],
                    operation='addition',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'has_carry_not_reset': True,
                        'problem_type': 'word_problem_total',
                        'template': 'word_problem_total',
                        'num_carries': self._count_carries(num1, num2),
                        'correct_answer': str(correct_answer),
                        'malrule_answer': str(malrule_answer),
                    }
                )

        # Fallback: construct numbers that guarantee carry interaction
        # ones: 8+7=15 (carry=1), tens: 2+1=3 (carry should reset but doesn't)
        hund_1, hund_2 = random.randint(1, 9), random.randint(1, 9)
        num1 = hund_1 * 100 + 28  # X28
        num2 = hund_2 * 100 + 17  # Y17
        correct_answer = num1 + num2
        malrule_answer = self._calculate_malrule_answer(num1, num2)
        problem_text = self._generate_problem_text(num1, num2, 'word_problem_total')

        return Problem(
            text=problem_text,
            operands=[num1, num2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'has_carry_not_reset': True,
                'problem_type': 'word_problem_total',
                'template': 'word_problem_total',
                'num_carries': self._count_carries(num1, num2),
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
            }
        )

    def _generate_word_problem_combine(self, seed: Optional[int] = None) -> Problem:
        """Template 4: Word problems about combining quantities."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['addend']

        for _ in range(100):
            num1 = random.randint(min_val, max_val)
            num2 = random.randint(min_val, max_val)

            if self._has_carry_not_reset_opportunity(num1, num2):
                correct_answer = num1 + num2
                malrule_answer = self._calculate_malrule_answer(num1, num2)
                problem_text = self._generate_problem_text(num1, num2, 'word_problem_combine')

                return Problem(
                    text=problem_text,
                    operands=[num1, num2],
                    operation='addition',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'has_carry_not_reset': True,
                        'problem_type': 'word_problem_combine',
                        'template': 'word_problem_combine',
                        'num_carries': self._count_carries(num1, num2),
                        'correct_answer': str(correct_answer),
                        'malrule_answer': str(malrule_answer),
                    }
                )

        # Fallback: construct numbers that guarantee carry interaction
        # ones: 8+7=15 (carry=1), tens: 2+1=3 (carry should reset but doesn't)
        hund_1, hund_2 = random.randint(1, 9), random.randint(1, 9)
        num1 = hund_1 * 100 + 28  # X28
        num2 = hund_2 * 100 + 17  # Y17
        correct_answer = num1 + num2
        malrule_answer = self._calculate_malrule_answer(num1, num2)
        problem_text = self._generate_problem_text(num1, num2, 'word_problem_combine')

        return Problem(
            text=problem_text,
            operands=[num1, num2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'has_carry_not_reset': True,
                'problem_type': 'word_problem_combine',
                'template': 'word_problem_combine',
                'num_carries': self._count_carries(num1, num2),
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
            }
        )
