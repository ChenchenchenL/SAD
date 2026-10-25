"""
Problem generator for Add-All-Digits malrule.

Generates multi-digit addition problems where the malrule will produce
different answers than the correct algorithm.
"""

import random
from typing import Dict, Tuple, Optional, List
import sys
sys.path.append('/Users/kitetsu/nlp_mac/malrule-coding')

from utils import Problem, ProblemGenerator, DifficultyLevel


class AddAllDigitsProblemGenerator(ProblemGenerator):
    """
    Generates addition problems where the Add-All-Digits malrule will
    produce incorrect answers by summing all individual digits.
    """

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level and difficulty."""
        ranges = {
            1: {
                DifficultyLevel.EASY: (10, 50),
                DifficultyLevel.MEDIUM: (10, 99),
                DifficultyLevel.HARD: (10, 99),
            },
            2: {
                DifficultyLevel.EASY: (10, 50),
                DifficultyLevel.MEDIUM: (20, 99),
                DifficultyLevel.HARD: (50, 999),
            },
            3: {
                DifficultyLevel.EASY: (10, 99),
                DifficultyLevel.MEDIUM: (100, 999),
                DifficultyLevel.HARD: (100, 9999),
            },
            4: {
                DifficultyLevel.EASY: (100, 999),
                DifficultyLevel.MEDIUM: (100, 9999),
                DifficultyLevel.HARD: (1000, 9999),
            }
        }

        # Default to level 2 if not in ranges
        lvl = self.level if self.level in ranges else 2
        return {'addend1': ranges[lvl][self.difficulty],
                'addend2': ranges[lvl][self.difficulty]}

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_addition',
            'two_digit_plus_one_digit',
            'three_digit',
            'four_digit',
            'money_context',
            'counting_context',
            'word_problem',
        ]

    def _sum_all_digits(self, *numbers) -> int:
        """
        Calculate the sum of all individual digits in all given numbers.

        Args:
            *numbers: Variable number of integers

        Returns:
            Sum of all individual digits
        """
        total = 0
        for num in numbers:
            for digit in str(num):
                total += int(digit)
        return total

    def _will_produce_different_answer(self, addend1: int, addend2: int) -> bool:
        """
        Check if the malrule will produce a different answer than correct addition.

        The malrule sums all digits, so it will almost always differ from
        correct column-by-column addition for multi-digit numbers.

        Args:
            addend1: First addend
            addend2: Second addend

        Returns:
            True if malrule answer differs from correct answer
        """
        correct_answer = addend1 + addend2
        malrule_answer = self._sum_all_digits(addend1, addend2)
        return correct_answer != malrule_answer

    def _generate_problem_text(self, addend1: int, addend2: int, problem_type: str) -> str:
        """
        Generate problem text based on problem type.

        Args:
            addend1: First addend
            addend2: Second addend
            problem_type: Type of problem context

        Returns:
            Formatted problem text
        """
        if problem_type == 'basic':
            templates = [
                f"What is {addend1} + {addend2}?",
                f"Calculate: {addend1} + {addend2}",
                f"Add {addend1} and {addend2}.",
                f"Find the sum of {addend1} and {addend2}.",
            ]
            return random.choice(templates)

        elif problem_type == 'money':
            contexts = [
                f"Sarah has ${addend1} and earns ${addend2} more. How much money does she have now?",
                f"A store sold ${addend1} worth of items in the morning and ${addend2} in the afternoon. What is the total?",
                f"Tom saved ${addend1} last month and ${addend2} this month. How much has he saved in total?",
            ]
            return random.choice(contexts)

        elif problem_type == 'counting':
            contexts = [
                f"A classroom has {addend1} red crayons and {addend2} blue crayons. How many crayons are there in total?",
                f"There are {addend1} apples in one basket and {addend2} in another. How many apples altogether?",
                f"Maria collected {addend1} stamps last year and {addend2} stamps this year. How many stamps does she have now?",
            ]
            return random.choice(contexts)

        elif problem_type == 'word_problem':
            contexts = [
                f"A library has {addend1} fiction books and {addend2} non-fiction books. How many books in total?",
                f"On Monday, {addend1} students came to school. On Tuesday, {addend2} students came. What is the total attendance?",
                f"A farmer has {addend1} chickens and buys {addend2} more. How many chickens does the farmer have now?",
            ]
            return random.choice(contexts)

        else:
            return f"What is {addend1} + {addend2}?"

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate an addition problem where Add-All-Digits will produce wrong answer.

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
        elif template == 'two_digit_plus_one_digit':
            return self._generate_two_digit_plus_one_digit(seed)
        elif template == 'three_digit':
            return self._generate_three_digit(seed)
        elif template == 'four_digit':
            return self._generate_four_digit(seed)
        elif template == 'money_context':
            return self._generate_money_context(seed)
        elif template == 'counting_context':
            return self._generate_counting_context(seed)
        elif template == 'word_problem':
            return self._generate_word_problem(seed)
        else:
            return self._generate_basic_addition(seed)

    def _generate_basic_addition(self, seed: Optional[int] = None) -> Problem:
        """Template 1: Basic two-digit addition problems."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['addend1']

        for _ in range(100):
            addend1 = random.randint(min_val, max_val)
            addend2 = random.randint(min_val, max_val)

            if self._will_produce_different_answer(addend1, addend2):
                correct_answer = addend1 + addend2
                malrule_answer = self._sum_all_digits(addend1, addend2)
                problem_text = self._generate_problem_text(addend1, addend2, 'basic')

                return Problem(
                    text=problem_text,
                    operands=[addend1, addend2],
                    operation='addition',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'correct_answer': str(correct_answer),
                        'malrule_answer': str(malrule_answer),
                        'problem_type': 'basic_addition',
                        'template': 'basic_addition'
                    }
                )

        # Fallback
        addend1 = random.randint(min_val, max_val)
        addend2 = random.randint(min_val, max_val)
        correct_answer = addend1 + addend2
        malrule_answer = self._sum_all_digits(addend1, addend2)
        problem_text = self._generate_problem_text(addend1, addend2, 'basic')

        return Problem(
            text=problem_text,
            operands=[addend1, addend2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'problem_type': 'basic_addition',
                'template': 'basic_addition'
            }
        )

    def _generate_two_digit_plus_one_digit(self, seed: Optional[int] = None) -> Problem:
        """Template 2: Two-digit plus one-digit (like 17 + 5 from paper)."""
        if seed is not None:
            random.seed(seed)

        for _ in range(100):
            addend1 = random.randint(10, 99)  # Two-digit
            addend2 = random.randint(1, 9)    # One-digit

            if self._will_produce_different_answer(addend1, addend2):
                correct_answer = addend1 + addend2
                malrule_answer = self._sum_all_digits(addend1, addend2)
                problem_text = self._generate_problem_text(addend1, addend2, 'basic')

                return Problem(
                    text=problem_text,
                    operands=[addend1, addend2],
                    operation='addition',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'correct_answer': str(correct_answer),
                        'malrule_answer': str(malrule_answer),
                        'problem_type': 'two_digit_plus_one_digit',
                        'template': 'two_digit_plus_one_digit'
                    }
                )

        # Fallback: use 17 + 5 from the paper
        addend1, addend2 = 17, 5
        correct_answer = addend1 + addend2
        malrule_answer = self._sum_all_digits(addend1, addend2)
        problem_text = self._generate_problem_text(addend1, addend2, 'basic')

        return Problem(
            text=problem_text,
            operands=[addend1, addend2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'problem_type': 'two_digit_plus_one_digit',
                'template': 'two_digit_plus_one_digit'
            }
        )

    def _generate_three_digit(self, seed: Optional[int] = None) -> Problem:
        """Template 3: Three-digit addition problems."""
        if seed is not None:
            random.seed(seed)

        for _ in range(100):
            addend1 = random.randint(100, 999)
            addend2 = random.randint(100, 999)

            if self._will_produce_different_answer(addend1, addend2):
                correct_answer = addend1 + addend2
                malrule_answer = self._sum_all_digits(addend1, addend2)
                problem_text = self._generate_problem_text(addend1, addend2, 'basic')

                return Problem(
                    text=problem_text,
                    operands=[addend1, addend2],
                    operation='addition',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'correct_answer': str(correct_answer),
                        'malrule_answer': str(malrule_answer),
                        'problem_type': 'three_digit',
                        'template': 'three_digit'
                    }
                )

        # Fallback
        addend1 = random.randint(100, 999)
        addend2 = random.randint(100, 999)
        correct_answer = addend1 + addend2
        malrule_answer = self._sum_all_digits(addend1, addend2)
        problem_text = self._generate_problem_text(addend1, addend2, 'basic')

        return Problem(
            text=problem_text,
            operands=[addend1, addend2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'problem_type': 'three_digit',
                'template': 'three_digit'
            }
        )

    def _generate_four_digit(self, seed: Optional[int] = None) -> Problem:
        """Template 4: Four-digit addition (like 51 + 1707 from paper)."""
        if seed is not None:
            random.seed(seed)

        for _ in range(100):
            # Mix of different digit lengths like in the paper
            if random.random() < 0.5:
                addend1 = random.randint(10, 99)
                addend2 = random.randint(1000, 9999)
            else:
                addend1 = random.randint(1000, 9999)
                addend2 = random.randint(10, 99)

            if self._will_produce_different_answer(addend1, addend2):
                correct_answer = addend1 + addend2
                malrule_answer = self._sum_all_digits(addend1, addend2)
                problem_text = self._generate_problem_text(addend1, addend2, 'basic')

                return Problem(
                    text=problem_text,
                    operands=[addend1, addend2],
                    operation='addition',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'correct_answer': str(correct_answer),
                        'malrule_answer': str(malrule_answer),
                        'problem_type': 'four_digit',
                        'template': 'four_digit'
                    }
                )

        # Fallback: use 51 + 1707 from the paper
        addend1, addend2 = 51, 1707
        correct_answer = addend1 + addend2
        malrule_answer = self._sum_all_digits(addend1, addend2)
        problem_text = self._generate_problem_text(addend1, addend2, 'basic')

        return Problem(
            text=problem_text,
            operands=[addend1, addend2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'problem_type': 'four_digit',
                'template': 'four_digit'
            }
        )

    def _generate_money_context(self, seed: Optional[int] = None) -> Problem:
        """Template 5: Money word problems."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['addend1']

        for _ in range(100):
            addend1 = random.randint(min_val, max_val)
            addend2 = random.randint(min_val, max_val)

            if self._will_produce_different_answer(addend1, addend2):
                correct_answer = addend1 + addend2
                malrule_answer = self._sum_all_digits(addend1, addend2)
                problem_text = self._generate_problem_text(addend1, addend2, 'money')

                return Problem(
                    text=problem_text,
                    operands=[addend1, addend2],
                    operation='addition',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'correct_answer': str(correct_answer),
                        'malrule_answer': str(malrule_answer),
                        'problem_type': 'money_context',
                        'template': 'money_context'
                    }
                )

        # Fallback
        addend1 = random.randint(min_val, max_val)
        addend2 = random.randint(min_val, max_val)
        correct_answer = addend1 + addend2
        malrule_answer = self._sum_all_digits(addend1, addend2)
        problem_text = self._generate_problem_text(addend1, addend2, 'money')

        return Problem(
            text=problem_text,
            operands=[addend1, addend2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'problem_type': 'money_context',
                'template': 'money_context'
            }
        )

    def _generate_counting_context(self, seed: Optional[int] = None) -> Problem:
        """Template 6: Counting word problems."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['addend1']

        for _ in range(100):
            addend1 = random.randint(min_val, max_val)
            addend2 = random.randint(min_val, max_val)

            if self._will_produce_different_answer(addend1, addend2):
                correct_answer = addend1 + addend2
                malrule_answer = self._sum_all_digits(addend1, addend2)
                problem_text = self._generate_problem_text(addend1, addend2, 'counting')

                return Problem(
                    text=problem_text,
                    operands=[addend1, addend2],
                    operation='addition',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'correct_answer': str(correct_answer),
                        'malrule_answer': str(malrule_answer),
                        'problem_type': 'counting_context',
                        'template': 'counting_context'
                    }
                )

        # Fallback
        addend1 = random.randint(min_val, max_val)
        addend2 = random.randint(min_val, max_val)
        correct_answer = addend1 + addend2
        malrule_answer = self._sum_all_digits(addend1, addend2)
        problem_text = self._generate_problem_text(addend1, addend2, 'counting')

        return Problem(
            text=problem_text,
            operands=[addend1, addend2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'problem_type': 'counting_context',
                'template': 'counting_context'
            }
        )

    def _generate_word_problem(self, seed: Optional[int] = None) -> Problem:
        """Template 7: General word problems."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['addend1']

        for _ in range(100):
            addend1 = random.randint(min_val, max_val)
            addend2 = random.randint(min_val, max_val)

            if self._will_produce_different_answer(addend1, addend2):
                correct_answer = addend1 + addend2
                malrule_answer = self._sum_all_digits(addend1, addend2)
                problem_text = self._generate_problem_text(addend1, addend2, 'word_problem')

                return Problem(
                    text=problem_text,
                    operands=[addend1, addend2],
                    operation='addition',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'correct_answer': str(correct_answer),
                        'malrule_answer': str(malrule_answer),
                        'problem_type': 'word_problem',
                        'template': 'word_problem'
                    }
                )

        # Fallback
        addend1 = random.randint(min_val, max_val)
        addend2 = random.randint(min_val, max_val)
        correct_answer = addend1 + addend2
        malrule_answer = self._sum_all_digits(addend1, addend2)
        problem_text = self._generate_problem_text(addend1, addend2, 'word_problem')

        return Problem(
            text=problem_text,
            operands=[addend1, addend2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'problem_type': 'word_problem',
                'template': 'word_problem'
            }
        )
