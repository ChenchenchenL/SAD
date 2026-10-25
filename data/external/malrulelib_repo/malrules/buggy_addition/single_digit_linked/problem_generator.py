"""
Problem generator for Single-Digit-Linked malrule.

Generates addition problems where one operand is single-digit and one is
multi-digit, which elicits the linking (appending) error behavior.
"""

import random
from typing import Dict, Tuple, Optional, List
import sys
sys.path.append('/Users/kitetsu/nlp_mac/malrule-coding')

from utils import Problem, ProblemGenerator, DifficultyLevel


class SingleDigitLinkedProblemGenerator(ProblemGenerator):
    """
    Generates addition problems where one operand is single-digit and the
    other is multi-digit, creating conditions for the Single-Digit-Linked
    malrule to produce incorrect answers.
    """

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level and difficulty."""
        # Single digit is always 1-9
        # Multi-digit varies by level and difficulty
        ranges = {
            2: {
                DifficultyLevel.EASY: (10, 50),
                DifficultyLevel.MEDIUM: (20, 80),
                DifficultyLevel.HARD: (40, 99),
            },
            3: {
                DifficultyLevel.EASY: (10, 99),
                DifficultyLevel.MEDIUM: (50, 200),
                DifficultyLevel.HARD: (100, 500),
            },
            4: {
                DifficultyLevel.EASY: (10, 100),
                DifficultyLevel.MEDIUM: (100, 500),
                DifficultyLevel.HARD: (500, 1000),
            }
        }

        # Default to level 3 if not in ranges
        lvl = self.level if self.level in ranges else 3
        return {
            'single_digit': (1, 9),
            'multi_digit': ranges[lvl][self.difficulty]
        }

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_addition',
            'single_digit_first',
            'single_digit_second',
            'word_problem_combining',
            'word_problem_increase',
            'word_problem_collection',
        ]

    def _calculate_correct(self, num1: int, num2: int) -> int:
        """Calculate the correct sum."""
        return num1 + num2

    def _calculate_malrule(self, num1: int, num2: int) -> int:
        """
        Calculate the malrule answer for Single-Digit-Linked.

        The single-digit operand is always appended to the multi-digit operand.

        Args:
            num1: First operand
            num2: Second operand

        Returns:
            Malrule result (concatenation with single digit appended to multi-digit)
        """
        # Determine which is single-digit and which is multi-digit
        if num1 < 10 and num2 >= 10:
            # num1 is single-digit, append it to num2
            return int(str(num2) + str(num1))
        elif num2 < 10 and num1 >= 10:
            # num2 is single-digit, append it to num1
            return int(str(num1) + str(num2))
        else:
            # Both are single-digit or both are multi-digit
            # Just concatenate in order (edge case)
            return int(str(num1) + str(num2))

    def _generate_problem_text(self, num1: int, num2: int, problem_type: str) -> str:
        """
        Generate problem text based on problem type.

        Args:
            num1: First operand
            num2: Second operand
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

        elif problem_type == 'combining':
            contexts = [
                f"Emma has {num1} stickers and her friend has {num2} stickers. How many stickers do they have together?",
                f"A bakery made {num1} cookies in the morning and {num2} cookies in the afternoon. How many cookies did they make in total?",
                f"Tom collected {num1} stamps and then found {num2} more. How many stamps does he have now?",
            ]
            return random.choice(contexts)

        elif problem_type == 'increase':
            contexts = [
                f"A store had {num1} customers on Monday. On Tuesday, {num2} more customers came. How many customers came in total?",
                f"Sarah read {num1} pages yesterday and {num2} pages today. How many pages has she read altogether?",
                f"The temperature was {num1} degrees. It went up by {num2} degrees. What is the new temperature?",
            ]
            return random.choice(contexts)

        elif problem_type == 'collection':
            contexts = [
                f"A basket contains {num1} apples and {num2} oranges. How many pieces of fruit are there?",
                f"Jake has {num1} red marbles and {num2} blue marbles. How many marbles does he have in total?",
                f"A garden has {num1} roses and {num2} tulips. How many flowers are there altogether?",
            ]
            return random.choice(contexts)

        else:
            return f"What is {num1} + {num2}?"

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate an addition problem where Single-Digit-Linked malrule applies.

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
        elif template == 'single_digit_first':
            return self._generate_single_digit_first(seed)
        elif template == 'single_digit_second':
            return self._generate_single_digit_second(seed)
        elif template == 'word_problem_combining':
            return self._generate_word_problem_combining(seed)
        elif template == 'word_problem_increase':
            return self._generate_word_problem_increase(seed)
        elif template == 'word_problem_collection':
            return self._generate_word_problem_collection(seed)
        else:
            return self._generate_basic_addition(seed)

    def _generate_basic_addition(self, seed: Optional[int] = None) -> Problem:
        """Template 1: Basic addition problems (randomly ordered)."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        single_digit = random.randint(*ranges['single_digit'])
        multi_digit = random.randint(*ranges['multi_digit'])

        # Randomly decide order
        if random.choice([True, False]):
            num1, num2 = multi_digit, single_digit
        else:
            num1, num2 = single_digit, multi_digit

        correct_answer = self._calculate_correct(num1, num2)
        malrule_answer = self._calculate_malrule(num1, num2)

        problem_text = self._generate_problem_text(num1, num2, 'basic')

        return Problem(
            text=problem_text,
            operands=[num1, num2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': num1,
                'num2': num2,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'problem_type': 'basic',
                'template': 'basic_addition',
                'single_digit_position': 'second' if num1 >= 10 else 'first'
            }
        )

    def _generate_single_digit_first(self, seed: Optional[int] = None) -> Problem:
        """Template 2: Single digit as first operand (e.g., 8 + 12 = 128)."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        single_digit = random.randint(*ranges['single_digit'])
        multi_digit = random.randint(*ranges['multi_digit'])

        num1, num2 = single_digit, multi_digit

        correct_answer = self._calculate_correct(num1, num2)
        malrule_answer = self._calculate_malrule(num1, num2)

        problem_text = self._generate_problem_text(num1, num2, 'basic')

        return Problem(
            text=problem_text,
            operands=[num1, num2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': num1,
                'num2': num2,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'problem_type': 'basic',
                'template': 'single_digit_first',
                'single_digit_position': 'first'
            }
        )

    def _generate_single_digit_second(self, seed: Optional[int] = None) -> Problem:
        """Template 3: Single digit as second operand (e.g., 19 + 9 = 199)."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        single_digit = random.randint(*ranges['single_digit'])
        multi_digit = random.randint(*ranges['multi_digit'])

        num1, num2 = multi_digit, single_digit

        correct_answer = self._calculate_correct(num1, num2)
        malrule_answer = self._calculate_malrule(num1, num2)

        problem_text = self._generate_problem_text(num1, num2, 'basic')

        return Problem(
            text=problem_text,
            operands=[num1, num2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': num1,
                'num2': num2,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'problem_type': 'basic',
                'template': 'single_digit_second',
                'single_digit_position': 'second'
            }
        )

    def _generate_word_problem_combining(self, seed: Optional[int] = None) -> Problem:
        """Template 4: Word problems about combining quantities."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        single_digit = random.randint(*ranges['single_digit'])
        multi_digit = random.randint(*ranges['multi_digit'])

        # Randomly decide order
        if random.choice([True, False]):
            num1, num2 = multi_digit, single_digit
        else:
            num1, num2 = single_digit, multi_digit

        correct_answer = self._calculate_correct(num1, num2)
        malrule_answer = self._calculate_malrule(num1, num2)

        problem_text = self._generate_problem_text(num1, num2, 'combining')

        return Problem(
            text=problem_text,
            operands=[num1, num2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': num1,
                'num2': num2,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'problem_type': 'combining',
                'template': 'word_problem_combining',
                'single_digit_position': 'second' if num1 >= 10 else 'first'
            }
        )

    def _generate_word_problem_increase(self, seed: Optional[int] = None) -> Problem:
        """Template 5: Word problems about increases/additions."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        single_digit = random.randint(*ranges['single_digit'])
        multi_digit = random.randint(*ranges['multi_digit'])

        # Randomly decide order
        if random.choice([True, False]):
            num1, num2 = multi_digit, single_digit
        else:
            num1, num2 = single_digit, multi_digit

        correct_answer = self._calculate_correct(num1, num2)
        malrule_answer = self._calculate_malrule(num1, num2)

        problem_text = self._generate_problem_text(num1, num2, 'increase')

        return Problem(
            text=problem_text,
            operands=[num1, num2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': num1,
                'num2': num2,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'problem_type': 'increase',
                'template': 'word_problem_increase',
                'single_digit_position': 'second' if num1 >= 10 else 'first'
            }
        )

    def _generate_word_problem_collection(self, seed: Optional[int] = None) -> Problem:
        """Template 6: Word problems about collections of items."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        single_digit = random.randint(*ranges['single_digit'])
        multi_digit = random.randint(*ranges['multi_digit'])

        # Randomly decide order
        if random.choice([True, False]):
            num1, num2 = multi_digit, single_digit
        else:
            num1, num2 = single_digit, multi_digit

        correct_answer = self._calculate_correct(num1, num2)
        malrule_answer = self._calculate_malrule(num1, num2)

        problem_text = self._generate_problem_text(num1, num2, 'collection')

        return Problem(
            text=problem_text,
            operands=[num1, num2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': num1,
                'num2': num2,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'problem_type': 'collection',
                'template': 'word_problem_collection',
                'single_digit_position': 'second' if num1 >= 10 else 'first'
            }
        )
