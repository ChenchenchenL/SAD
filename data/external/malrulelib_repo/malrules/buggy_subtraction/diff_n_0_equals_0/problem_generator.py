"""
Problem generator for DIFF/N-0=0 malrule.

Generates multi-digit subtraction problems where the subtrahend (bottom number)
contains at least one 0 digit, which will trigger the N-0=0 bug.
"""

import random
from typing import Dict, Tuple, Optional, List
import sys
sys.path.append('/home/user/malrule-coding')

from utils import Problem, ProblemGenerator, DifficultyLevel, create_basic_arithmetic_template


class DiffN0Equals0ProblemGenerator(ProblemGenerator):
    """
    Generates subtraction problems where the subtrahend contains 0 digits.

    The DIFF/N-0=0 bug occurs when a student sees 0 in the bottom (subtrahend)
    and writes 0 in the answer instead of the top digit. Problems must have
    at least one column where: top digit is non-zero AND bottom digit is 0.
    """

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level and difficulty."""
        ranges = {
            2: {
                DifficultyLevel.EASY: (10, 50),
                DifficultyLevel.MEDIUM: (20, 80),
                DifficultyLevel.HARD: (40, 99),
            },
            3: {
                DifficultyLevel.EASY: (100, 300),
                DifficultyLevel.MEDIUM: (200, 600),
                DifficultyLevel.HARD: (400, 999),
            },
            4: {
                DifficultyLevel.EASY: (100, 500),
                DifficultyLevel.MEDIUM: (500, 2000),
                DifficultyLevel.HARD: (1000, 9999),
            }
        }

        # Default to level 3 if not in ranges
        lvl = self.level if self.level in ranges else 3
        return {'minuend': ranges[lvl][self.difficulty],
                'subtrahend': ranges[lvl][self.difficulty]}

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_subtraction',
            'money_context',
            'measurement_context',
            'three_digit',
            'four_digit',
            'word_problem_result_unknown',
            'word_problem_comparison'
        ]

    def _has_n_minus_0_opportunity(self, minuend: int, subtrahend: int) -> bool:
        """
        Check if problem has at least one column where:
        - Top digit (minuend) is non-zero
        - Bottom digit (subtrahend) is 0

        This is where the DIFF/N-0=0 malrule will produce wrong answer.

        Args:
            minuend: Top number
            subtrahend: Bottom number

        Returns:
            True if at least one column has non-zero top and zero bottom
        """
        if minuend <= subtrahend:
            return False

        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend).zfill(len(minuend_str))

        # Check if any column has non-zero top and zero bottom
        for m_digit, s_digit in zip(minuend_str, subtrahend_str):
            if int(m_digit) > 0 and int(s_digit) == 0:
                return True

        return False

    def _calculate_correct_answer(self, minuend: int, subtrahend: int) -> int:
        """Calculate the correct answer for subtraction."""
        return minuend - subtrahend

    def _calculate_malrule_answer(self, minuend: int, subtrahend: int) -> int:
        """
        Calculate the malrule answer using DIFF/N-0=0 bug.

        The student correctly handles borrowing (including borrow-across-zero),
        but when they see 0 in the subtrahend (bottom), they write 0 instead
        of the actual difference (which would be the top digit minus zero = top digit).
        """
        # Convert to digit lists (rightmost digit first)
        minuend_digits = [int(d) for d in str(minuend)][::-1]
        subtrahend_digits = [int(d) for d in str(subtrahend)][::-1]

        # Pad subtrahend with zeros if needed
        while len(subtrahend_digits) < len(minuend_digits):
            subtrahend_digits.append(0)

        # Make a copy of minuend digits that we'll modify with borrows
        working_minuend = minuend_digits.copy()

        result_digits = []

        # Process each column
        for i in range(len(working_minuend)):
            top_digit = working_minuend[i]
            bottom_digit = subtrahend_digits[i]

            # MALRULE: If bottom digit is 0, write 0 (not top digit)
            # The student ignores the actual top digit value
            if bottom_digit == 0:
                result_digits.append(0)  # BUG! Should be top_digit
                # No borrowing needed when bottom is 0
            else:
                # Normal subtraction with borrowing
                if top_digit < bottom_digit:
                    # Need to borrow - find a column to borrow from
                    # This handles borrow-across-zero correctly
                    borrow_col = i + 1
                    while borrow_col < len(working_minuend) and working_minuend[borrow_col] == 0:
                        working_minuend[borrow_col] = 9  # Borrowed through
                        borrow_col += 1
                    if borrow_col < len(working_minuend):
                        working_minuend[borrow_col] -= 1
                    top_digit += 10

                result_digits.append(top_digit - bottom_digit)

        # Remove leading zeros
        while len(result_digits) > 1 and result_digits[-1] == 0:
            result_digits.pop()

        return int(''.join(str(d) for d in result_digits[::-1]))

    def _generate_problem_text(self, minuend: int, subtrahend: int, problem_type: str) -> str:
        """
        Generate problem text based on problem type.

        Args:
            minuend: Top number
            subtrahend: Bottom number (contains 0s)
            problem_type: Type of problem context

        Returns:
            Formatted problem text
        """
        if problem_type == 'basic':
            template = create_basic_arithmetic_template('subtraction')
            return template.generate({'a': minuend, 'b': subtrahend})

        elif problem_type == 'money':
            contexts = [
                f"Sarah had ${minuend}. She spent ${subtrahend} on books. How much money does she have left?",
                f"A store had ${minuend} in the cash register. After a purchase of ${subtrahend}, how much is left?",
                f"Tom saved ${minuend} and then spent ${subtrahend} on a new game. How much money does he have now?",
            ]
            return random.choice(contexts)

        elif problem_type == 'measurement':
            contexts = [
                f"A rope was {minuend} meters long. After cutting off {subtrahend} meters, how much remains?",
                f"The total distance is {minuend} kilometers. After traveling {subtrahend} kilometers, how far is left?",
                f"A builder had {minuend} feet of wood. After using {subtrahend} feet, how much is left?",
            ]
            return random.choice(contexts)

        elif problem_type == 'three_digit':
            contexts = [
                f"What is {minuend} - {subtrahend}?",
                f"Calculate: {minuend} - {subtrahend}",
                f"Subtract {subtrahend} from {minuend}.",
            ]
            return random.choice(contexts)

        else:
            # Default to basic
            template = create_basic_arithmetic_template('subtraction')
            return template.generate({'a': minuend, 'b': subtrahend})

    def _generate_subtrahend_with_zero(self, min_val: int, max_val: int) -> int:
        """
        Generate a subtrahend that contains at least one 0 digit.

        Args:
            min_val: Minimum value
            max_val: Maximum value

        Returns:
            A number containing at least one 0 digit
        """
        for _ in range(100):
            num = random.randint(min_val, max_val)
            if '0' in str(num):
                return num

        # Fallback: construct a number with 0
        # For 3-digit numbers: X0Y format
        if max_val >= 100:
            first = random.randint(1, 9)
            last = random.randint(1, 9)
            return first * 100 + last  # e.g., 101, 203, 508
        else:
            # For 2-digit numbers: X0 format
            return random.randint(1, 9) * 10  # e.g., 10, 20, 30

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate a subtraction problem where DIFF/N-0=0 will produce incorrect answer.

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
        if template == 'basic_subtraction':
            return self._generate_basic_subtraction(seed)
        elif template == 'money_context':
            return self._generate_money_context(seed)
        elif template == 'measurement_context':
            return self._generate_measurement_context(seed)
        elif template == 'three_digit':
            return self._generate_three_digit(seed)
        elif template == 'four_digit':
            return self._generate_four_digit(seed)
        elif template == 'word_problem_result_unknown':
            return self._generate_word_problem_result_unknown(seed)
        elif template == 'word_problem_comparison':
            return self._generate_word_problem_comparison(seed)
        else:
            return self._generate_basic_subtraction(seed)

    def _generate_basic_subtraction(self, seed: Optional[int] = None) -> Problem:
        """Template 1: Basic subtraction problems."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['minuend']

        for _ in range(100):
            # Generate subtrahend with a 0 digit
            subtrahend = self._generate_subtrahend_with_zero(min_val // 2, max_val // 2)
            # Minuend must be larger and have non-zero in 0-columns
            minuend = random.randint(subtrahend + 10, max_val)

            if self._has_n_minus_0_opportunity(minuend, subtrahend):
                problem_text = self._generate_problem_text(minuend, subtrahend, 'basic')
                correct_answer = self._calculate_correct_answer(minuend, subtrahend)
                malrule_answer = self._calculate_malrule_answer(minuend, subtrahend)

                return Problem(
                    text=problem_text,
                    operands=[minuend, subtrahend],
                    operation='subtraction',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'has_n_minus_0': True,
                        'problem_type': 'basic',
                        'template': 'basic_subtraction',
                        'correct_answer': str(correct_answer),
                        'malrule_answer': str(malrule_answer)
                    }
                )

        # Fallback with known good example
        minuend, subtrahend = 403, 208
        problem_text = self._generate_problem_text(minuend, subtrahend, 'basic')
        return Problem(
            text=problem_text,
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'has_n_minus_0': True,
                'problem_type': 'basic',
                'template': 'basic_subtraction',
                'correct_answer': '195',
                'malrule_answer': '105'
            }
        )

    def _generate_money_context(self, seed: Optional[int] = None) -> Problem:
        """Template 2: Money word problems."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['minuend']

        for _ in range(100):
            subtrahend = self._generate_subtrahend_with_zero(min_val // 2, max_val // 2)
            minuend = random.randint(subtrahend + 10, max_val)

            if self._has_n_minus_0_opportunity(minuend, subtrahend):
                problem_text = self._generate_problem_text(minuend, subtrahend, 'money')
                correct_answer = self._calculate_correct_answer(minuend, subtrahend)
                malrule_answer = self._calculate_malrule_answer(minuend, subtrahend)

                return Problem(
                    text=problem_text,
                    operands=[minuend, subtrahend],
                    operation='subtraction',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'has_n_minus_0': True,
                        'problem_type': 'money',
                        'template': 'money_context',
                        'correct_answer': str(correct_answer),
                        'malrule_answer': str(malrule_answer)
                    }
                )

        # Fallback
        minuend, subtrahend = 450, 203
        problem_text = self._generate_problem_text(minuend, subtrahend, 'money')
        return Problem(
            text=problem_text,
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'has_n_minus_0': True,
                'problem_type': 'money',
                'template': 'money_context',
                'correct_answer': '247',
                'malrule_answer': '207'
            }
        )

    def _generate_measurement_context(self, seed: Optional[int] = None) -> Problem:
        """Template 3: Measurement word problems."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['minuend']

        for _ in range(100):
            subtrahend = self._generate_subtrahend_with_zero(min_val // 2, max_val // 2)
            minuend = random.randint(subtrahend + 10, max_val)

            if self._has_n_minus_0_opportunity(minuend, subtrahend):
                problem_text = self._generate_problem_text(minuend, subtrahend, 'measurement')
                correct_answer = self._calculate_correct_answer(minuend, subtrahend)
                malrule_answer = self._calculate_malrule_answer(minuend, subtrahend)

                return Problem(
                    text=problem_text,
                    operands=[minuend, subtrahend],
                    operation='subtraction',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'has_n_minus_0': True,
                        'problem_type': 'measurement',
                        'template': 'measurement_context',
                        'correct_answer': str(correct_answer),
                        'malrule_answer': str(malrule_answer)
                    }
                )

        # Fallback
        minuend, subtrahend = 543, 201
        problem_text = self._generate_problem_text(minuend, subtrahend, 'measurement')
        return Problem(
            text=problem_text,
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'has_n_minus_0': True,
                'problem_type': 'measurement',
                'template': 'measurement_context',
                'correct_answer': '342',
                'malrule_answer': '302'
            }
        )

    def _generate_three_digit(self, seed: Optional[int] = None) -> Problem:
        """Template 4: Three-digit subtraction problems."""
        if seed is not None:
            random.seed(seed)

        # Force 3-digit range
        min_val, max_val = 100, 999

        for _ in range(100):
            subtrahend = self._generate_subtrahend_with_zero(100, 500)
            minuend = random.randint(subtrahend + 10, max_val)

            if self._has_n_minus_0_opportunity(minuend, subtrahend):
                problem_text = self._generate_problem_text(minuend, subtrahend, 'three_digit')
                correct_answer = self._calculate_correct_answer(minuend, subtrahend)
                malrule_answer = self._calculate_malrule_answer(minuend, subtrahend)

                return Problem(
                    text=problem_text,
                    operands=[minuend, subtrahend],
                    operation='subtraction',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'has_n_minus_0': True,
                        'problem_type': 'three_digit',
                        'template': 'three_digit',
                        'correct_answer': str(correct_answer),
                        'malrule_answer': str(malrule_answer)
                    }
                )

        # Fallback with paper example
        minuend, subtrahend = 403, 208
        problem_text = self._generate_problem_text(minuend, subtrahend, 'three_digit')
        return Problem(
            text=problem_text,
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'has_n_minus_0': True,
                'problem_type': 'three_digit',
                'template': 'three_digit',
                'correct_answer': '195',
                'malrule_answer': '105'
            }
        )

    def _generate_four_digit(self, seed: Optional[int] = None) -> Problem:
        """Template 5: Four-digit subtraction problems."""
        if seed is not None:
            random.seed(seed)

        # Force 4-digit range
        min_val, max_val = 1000, 9999

        for _ in range(100):
            subtrahend = self._generate_subtrahend_with_zero(1000, 5000)
            minuend = random.randint(subtrahend + 100, max_val)

            if self._has_n_minus_0_opportunity(minuend, subtrahend):
                contexts = [
                    f"What is {minuend} - {subtrahend}?",
                    f"Calculate: {minuend} - {subtrahend}",
                    f"Subtract {subtrahend} from {minuend}.",
                ]
                problem_text = random.choice(contexts)
                correct_answer = self._calculate_correct_answer(minuend, subtrahend)
                malrule_answer = self._calculate_malrule_answer(minuend, subtrahend)

                return Problem(
                    text=problem_text,
                    operands=[minuend, subtrahend],
                    operation='subtraction',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'has_n_minus_0': True,
                        'problem_type': 'four_digit',
                        'template': 'four_digit',
                        'correct_answer': str(correct_answer),
                        'malrule_answer': str(malrule_answer)
                    }
                )

        # Fallback
        minuend, subtrahend = 5432, 2301
        problem_text = f"What is {minuend} - {subtrahend}?"
        return Problem(
            text=problem_text,
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'has_n_minus_0': True,
                'problem_type': 'four_digit',
                'template': 'four_digit',
                'correct_answer': '3131',
                'malrule_answer': '3001'
            }
        )

    def _generate_word_problem_result_unknown(self, seed: Optional[int] = None) -> Problem:
        """Template 6: Word problems with result unknown."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['minuend']

        for _ in range(100):
            subtrahend = self._generate_subtrahend_with_zero(min_val // 2, max_val // 2)
            minuend = random.randint(subtrahend + 10, max_val)

            if self._has_n_minus_0_opportunity(minuend, subtrahend):
                context_sets = [
                    f"Emma collected {minuend} trading cards. She traded away {subtrahend} cards. How many cards does she have now?",
                    f"A movie theater had {minuend} seats. {subtrahend} seats were occupied. How many seats are empty?",
                    f"There were {minuend} students in the cafeteria. {subtrahend} students left to go outside. How many students remain?",
                ]
                problem_text = random.choice(context_sets)
                correct_answer = self._calculate_correct_answer(minuend, subtrahend)
                malrule_answer = self._calculate_malrule_answer(minuend, subtrahend)

                return Problem(
                    text=problem_text,
                    operands=[minuend, subtrahend],
                    operation='subtraction',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'has_n_minus_0': True,
                        'problem_type': 'word_problem_result_unknown',
                        'template': 'word_problem_result_unknown',
                        'formula_type': 'result_unknown',
                        'correct_answer': str(correct_answer),
                        'malrule_answer': str(malrule_answer)
                    }
                )

        # Fallback
        minuend, subtrahend = 456, 203
        problem_text = f"There were {minuend} items. {subtrahend} were taken. How many remain?"
        return Problem(
            text=problem_text,
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'has_n_minus_0': True,
                'problem_type': 'word_problem_result_unknown',
                'template': 'word_problem_result_unknown',
                'formula_type': 'result_unknown',
                'correct_answer': '253',
                'malrule_answer': '203'
            }
        )

    def _generate_word_problem_comparison(self, seed: Optional[int] = None) -> Problem:
        """Template 7: Word problems with comparison."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['minuend']

        for _ in range(100):
            subtrahend = self._generate_subtrahend_with_zero(min_val // 2, max_val // 2)
            minuend = random.randint(subtrahend + 10, max_val)

            if self._has_n_minus_0_opportunity(minuend, subtrahend):
                contexts = [
                    f"Anna scored {minuend} points and Ben scored {subtrahend} points. How many more points did Anna score?",
                    f"Building A is {minuend} feet tall and Building B is {subtrahend} feet tall. What is the difference in height?",
                    f"Team Red has {minuend} members and Team Blue has {subtrahend} members. How many more members does Team Red have?",
                ]
                problem_text = random.choice(contexts)
                correct_answer = self._calculate_correct_answer(minuend, subtrahend)
                malrule_answer = self._calculate_malrule_answer(minuend, subtrahend)

                return Problem(
                    text=problem_text,
                    operands=[minuend, subtrahend],
                    operation='subtraction',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'has_n_minus_0': True,
                        'problem_type': 'word_problem_comparison',
                        'template': 'word_problem_comparison',
                        'formula_type': 'comparison',
                        'correct_answer': str(correct_answer),
                        'malrule_answer': str(malrule_answer)
                    }
                )

        # Fallback
        minuend, subtrahend = 589, 304
        problem_text = f"Group A has {minuend} and Group B has {subtrahend}. What is the difference?"
        return Problem(
            text=problem_text,
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'has_n_minus_0': True,
                'problem_type': 'word_problem_comparison',
                'template': 'word_problem_comparison',
                'formula_type': 'comparison',
                'correct_answer': '285',
                'malrule_answer': '205'
            }
        )
