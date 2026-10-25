"""
Problem generator for Left-Justify malrule.

Generates addition problems where operands have different digit lengths,
allowing the malrule (left-alignment instead of right-alignment) to manifest.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, List, Optional
from utils import ProblemGenerator, Problem, DifficultyLevel


class LeftJustifyProblemGenerator(ProblemGenerator):
    """
    Generates addition problems where operands have different digit lengths.

    The Left-Justify malrule manifests when numbers have different lengths:
    - Correct: Right-align numbers (place value alignment)
    - Malrule: Left-align numbers (first digits aligned)

    Example: 23 + 456
    - Correct:    23 + 456 = 479  (right-aligned)
    - Malrule:   230 + 456 = 686  (left-aligned, 23 becomes 230)
    """

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level and difficulty."""
        # Ranges designed to create different-length operands
        ranges = {
            2: {
                DifficultyLevel.EASY: {'shorter': (1, 9), 'longer': (10, 99)},
                DifficultyLevel.MEDIUM: {'shorter': (10, 99), 'longer': (100, 999)},
                DifficultyLevel.HARD: {'shorter': (1, 9), 'longer': (100, 999)},
            },
            3: {
                DifficultyLevel.EASY: {'shorter': (10, 99), 'longer': (100, 999)},
                DifficultyLevel.MEDIUM: {'shorter': (10, 99), 'longer': (100, 999)},
                DifficultyLevel.HARD: {'shorter': (1, 99), 'longer': (1000, 9999)},
            },
            4: {
                DifficultyLevel.EASY: {'shorter': (10, 99), 'longer': (100, 999)},
                DifficultyLevel.MEDIUM: {'shorter': (10, 999), 'longer': (1000, 9999)},
                DifficultyLevel.HARD: {'shorter': (1, 999), 'longer': (1000, 9999)},
            },
            5: {
                DifficultyLevel.EASY: {'shorter': (100, 999), 'longer': (1000, 9999)},
                DifficultyLevel.MEDIUM: {'shorter': (10, 999), 'longer': (1000, 99999)},
                DifficultyLevel.HARD: {'shorter': (1, 9999), 'longer': (10000, 99999)},
            }
        }

        lvl = self.level if self.level in ranges else 3
        return ranges[lvl][self.difficulty]

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_addition',
            'two_digit_plus_three_digit',
            'one_digit_plus_multi_digit',
            'word_problem_shopping',
            'word_problem_distance',
            'word_problem_collection'
        ]

    def _calculate_correct_answer(self, num1: int, num2: int) -> int:
        """Calculate the correct answer (standard addition)."""
        return num1 + num2

    def _calculate_malrule_answer(self, num1: int, num2: int) -> int:
        """
        Calculate the malrule answer using left-justification.

        The shorter number is padded with zeros on the right to match
        the length of the longer number, then added.

        Example: 23 + 456
        - 23 becomes 230 (padded to match 3 digits)
        - 230 + 456 = 686
        """
        str1 = str(num1)
        str2 = str(num2)

        len1 = len(str1)
        len2 = len(str2)

        if len1 == len2:
            # Same length - no difference in alignment
            return num1 + num2

        if len1 < len2:
            # num1 is shorter - pad with zeros on right
            diff = len2 - len1
            adjusted_num1 = num1 * (10 ** diff)
            return adjusted_num1 + num2
        else:
            # num2 is shorter - pad with zeros on right
            diff = len1 - len2
            adjusted_num2 = num2 * (10 ** diff)
            return num1 + adjusted_num2

    def _has_different_lengths(self, num1: int, num2: int) -> bool:
        """Check if two numbers have different digit lengths."""
        return len(str(num1)) != len(str(num2))

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate an addition problem where operands have different digit lengths.

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

        if template == 'basic_addition':
            return self._generate_basic_addition(seed)
        elif template == 'two_digit_plus_three_digit':
            return self._generate_two_digit_plus_three_digit(seed)
        elif template == 'one_digit_plus_multi_digit':
            return self._generate_one_digit_plus_multi_digit(seed)
        elif template == 'word_problem_shopping':
            return self._generate_word_problem_shopping(seed)
        elif template == 'word_problem_distance':
            return self._generate_word_problem_distance(seed)
        elif template == 'word_problem_collection':
            return self._generate_word_problem_collection(seed)
        else:
            return self._generate_basic_addition(seed)

    def _generate_basic_addition(self, seed: Optional[int] = None) -> Problem:
        """Template 1: Basic addition with different digit lengths."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()

        # Generate numbers with different lengths
        shorter_min, shorter_max = ranges['shorter']
        longer_min, longer_max = ranges['longer']

        shorter_num = random.randint(shorter_min, shorter_max)
        longer_num = random.randint(longer_min, longer_max)

        # Randomize order
        if random.random() < 0.5:
            num1, num2 = shorter_num, longer_num
        else:
            num1, num2 = longer_num, shorter_num

        correct_answer = self._calculate_correct_answer(num1, num2)
        malrule_answer = self._calculate_malrule_answer(num1, num2)

        problem_texts = [
            f"Calculate: {num1} + {num2}",
            f"What is {num1} + {num2}?",
            f"Add: {num1} + {num2}",
            f"Find the sum: {num1} + {num2}"
        ]
        problem_text = random.choice(problem_texts)

        return Problem(
            text=problem_text,
            operands=[num1, num2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': num1,
                'num2': num2,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'basic_addition',
                'has_different_lengths': self._has_different_lengths(num1, num2)
            }
        )

    def _generate_two_digit_plus_three_digit(self, seed: Optional[int] = None) -> Problem:
        """Template 2: Specifically 2-digit + 3-digit problems."""
        if seed is not None:
            random.seed(seed)

        # Force 2-digit and 3-digit numbers
        two_digit = random.randint(10, 99)
        three_digit = random.randint(100, 999)

        # Randomize order
        if random.random() < 0.5:
            num1, num2 = two_digit, three_digit
        else:
            num1, num2 = three_digit, two_digit

        correct_answer = self._calculate_correct_answer(num1, num2)
        malrule_answer = self._calculate_malrule_answer(num1, num2)

        problem_texts = [
            f"Calculate: {num1} + {num2}",
            f"What is {num1} + {num2}?",
            f"Add {num1} and {num2}.",
        ]
        problem_text = random.choice(problem_texts)

        return Problem(
            text=problem_text,
            operands=[num1, num2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': num1,
                'num2': num2,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'two_digit_plus_three_digit',
                'has_different_lengths': True
            }
        )

    def _generate_one_digit_plus_multi_digit(self, seed: Optional[int] = None) -> Problem:
        """Template 3: Single digit + multi-digit problems."""
        if seed is not None:
            random.seed(seed)

        single_digit = random.randint(1, 9)

        # Choose multi-digit length based on difficulty
        if self.difficulty == DifficultyLevel.EASY:
            multi_digit = random.randint(10, 99)
        elif self.difficulty == DifficultyLevel.MEDIUM:
            multi_digit = random.randint(100, 999)
        else:
            multi_digit = random.randint(100, 9999)

        # Randomize order
        if random.random() < 0.5:
            num1, num2 = single_digit, multi_digit
        else:
            num1, num2 = multi_digit, single_digit

        correct_answer = self._calculate_correct_answer(num1, num2)
        malrule_answer = self._calculate_malrule_answer(num1, num2)

        problem_texts = [
            f"What is {num1} + {num2}?",
            f"Calculate: {num1} + {num2}",
            f"Find: {num1} + {num2}",
        ]
        problem_text = random.choice(problem_texts)

        return Problem(
            text=problem_text,
            operands=[num1, num2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': num1,
                'num2': num2,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'one_digit_plus_multi_digit',
                'has_different_lengths': True
            }
        )

    def _generate_word_problem_shopping(self, seed: Optional[int] = None) -> Problem:
        """Template 4: Shopping context word problem."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        shorter_min, shorter_max = ranges['shorter']
        longer_min, longer_max = ranges['longer']

        price1 = random.randint(shorter_min, shorter_max)
        price2 = random.randint(longer_min, longer_max)

        correct_answer = self._calculate_correct_answer(price1, price2)
        malrule_answer = self._calculate_malrule_answer(price1, price2)

        items = [
            ('book', 'pencil case'),
            ('toy', 'game'),
            ('shirt', 'jacket'),
            ('snack', 'backpack'),
            ('pen', 'notebook'),
        ]
        item1, item2 = random.choice(items)

        problem_texts = [
            f"Emma bought a {item1} for ${price1} and a {item2} for ${price2}. How much did she spend in total?",
            f"A {item1} costs ${price1} and a {item2} costs ${price2}. What is the total cost?",
            f"Jake spent ${price1} on a {item1} and ${price2} on a {item2}. How much money did he spend altogether?",
        ]
        problem_text = random.choice(problem_texts)

        return Problem(
            text=problem_text,
            operands=[price1, price2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': price1,
                'num2': price2,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'word_problem_shopping',
                'has_different_lengths': self._has_different_lengths(price1, price2)
            }
        )

    def _generate_word_problem_distance(self, seed: Optional[int] = None) -> Problem:
        """Template 5: Distance/travel context word problem."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        shorter_min, shorter_max = ranges['shorter']
        longer_min, longer_max = ranges['longer']

        dist1 = random.randint(shorter_min, shorter_max)
        dist2 = random.randint(longer_min, longer_max)

        correct_answer = self._calculate_correct_answer(dist1, dist2)
        malrule_answer = self._calculate_malrule_answer(dist1, dist2)

        units = ['miles', 'kilometers', 'meters']
        unit = random.choice(units)

        problem_texts = [
            f"A hiker walked {dist1} {unit} in the morning and {dist2} {unit} in the afternoon. How far did they walk in total?",
            f"The first part of a trip is {dist1} {unit} and the second part is {dist2} {unit}. What is the total distance?",
            f"Sarah drove {dist1} {unit} on Monday and {dist2} {unit} on Tuesday. How many {unit} did she drive altogether?",
        ]
        problem_text = random.choice(problem_texts)

        return Problem(
            text=problem_text,
            operands=[dist1, dist2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': dist1,
                'num2': dist2,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'word_problem_distance',
                'has_different_lengths': self._has_different_lengths(dist1, dist2)
            }
        )

    def _generate_word_problem_collection(self, seed: Optional[int] = None) -> Problem:
        """Template 6: Collection/counting context word problem."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        shorter_min, shorter_max = ranges['shorter']
        longer_min, longer_max = ranges['longer']

        count1 = random.randint(shorter_min, shorter_max)
        count2 = random.randint(longer_min, longer_max)

        correct_answer = self._calculate_correct_answer(count1, count2)
        malrule_answer = self._calculate_malrule_answer(count1, count2)

        items = ['stickers', 'cards', 'stamps', 'coins', 'marbles', 'books']
        item = random.choice(items)

        problem_texts = [
            f"Tom has {count1} {item} and his friend has {count2} {item}. How many {item} do they have together?",
            f"A box contains {count1} {item} and another box contains {count2} {item}. What is the total number of {item}?",
            f"Maria collected {count1} {item} on Saturday and {count2} {item} on Sunday. How many {item} did she collect in all?",
        ]
        problem_text = random.choice(problem_texts)

        return Problem(
            text=problem_text,
            operands=[count1, count2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': count1,
                'num2': count2,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'word_problem_collection',
                'has_different_lengths': self._has_different_lengths(count1, count2)
            }
        )
