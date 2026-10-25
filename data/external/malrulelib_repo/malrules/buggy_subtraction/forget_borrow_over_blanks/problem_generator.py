"""
Problem generator for FORGET/BORROW/OVER/BLANKS malrule.

Generates subtraction problems where the minuend (top number) has fewer digits
than the subtrahend (bottom number), which would normally require borrowing
over blank/implicit-zero columns.

Research: Brown & Burton (1978) "Diagnostic Models for Procedural Bugs"
"""

import random
from typing import Dict, Tuple, Optional, List
import sys
sys.path.append('/home/user/malrule-coding')

from utils import Problem, ProblemGenerator, DifficultyLevel


class ForgetBorrowOverBlanksProblemGenerator(ProblemGenerator):
    """
    Generates subtraction problems where the minuend has fewer digits than
    the subtrahend, creating situations where borrowing over blanks is required.

    This malrule manifests when students don't properly handle the implicit
    zeros in the minuend's leading positions.
    """

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level and difficulty."""
        ranges = {
            2: {
                DifficultyLevel.EASY: {'minuend': (10, 99), 'subtrahend': (100, 199)},
                DifficultyLevel.MEDIUM: {'minuend': (10, 99), 'subtrahend': (100, 299)},
                DifficultyLevel.HARD: {'minuend': (10, 99), 'subtrahend': (100, 499)},
            },
            3: {
                DifficultyLevel.EASY: {'minuend': (10, 99), 'subtrahend': (100, 299)},
                DifficultyLevel.MEDIUM: {'minuend': (10, 999), 'subtrahend': (100, 999)},
                DifficultyLevel.HARD: {'minuend': (10, 999), 'subtrahend': (1000, 2999)},
            },
            4: {
                DifficultyLevel.EASY: {'minuend': (10, 999), 'subtrahend': (100, 999)},
                DifficultyLevel.MEDIUM: {'minuend': (10, 999), 'subtrahend': (1000, 4999)},
                DifficultyLevel.HARD: {'minuend': (10, 9999), 'subtrahend': (1000, 9999)},
            }
        }

        # Default to level 3 if not in ranges
        lvl = self.level if self.level in ranges else 3
        return ranges[lvl][self.difficulty]

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_subtraction',
            'two_digit_minus_three_digit',
            'three_digit_minus_four_digit',
            'word_problem_debt',
            'word_problem_temperature',
            'word_problem_elevation',
        ]

    def _requires_borrow_over_blank(self, minuend: int, subtrahend: int) -> bool:
        """
        Check if problem requires borrowing over a blank column.

        This occurs when:
        1. Minuend has fewer digits than subtrahend
        2. After standard borrowing, we need to borrow from a column that
           doesn't exist in the minuend

        Args:
            minuend: Top number (smaller number of digits)
            subtrahend: Bottom number (larger number of digits)

        Returns:
            True if borrowing over blanks would be required
        """
        # Check digit count
        minuend_digits = len(str(minuend))
        subtrahend_digits = len(str(subtrahend))

        if minuend_digits >= subtrahend_digits:
            return False

        # Pad minuend with zeros to same length
        minuend_str = str(minuend).zfill(subtrahend_digits)
        subtrahend_str = str(subtrahend)

        # Check if any leading zero position in minuend has a non-zero
        # digit in the subtrahend - this requires "borrowing over blank"
        for i in range(subtrahend_digits - minuend_digits):
            if int(subtrahend_str[i]) > 0:
                return True

        return False

    def _has_borrow_needed_in_shorter_columns(self, minuend: int, subtrahend: int) -> bool:
        """
        Check if borrowing is needed in columns where minuend has digits.

        We want problems where the malrule produces a different answer than
        the correct algorithm.
        """
        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend)

        # Align from right
        max_len = max(len(minuend_str), len(subtrahend_str))
        minuend_padded = minuend_str.zfill(max_len)
        subtrahend_padded = subtrahend_str.zfill(max_len)

        # Check columns from right to left
        for i in range(max_len - 1, -1, -1):
            m_digit = int(minuend_padded[i])
            s_digit = int(subtrahend_padded[i])
            if m_digit < s_digit:
                return True

        return False

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate a subtraction problem where borrowing over blanks is required.

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
        elif template == 'two_digit_minus_three_digit':
            return self._generate_two_minus_three(seed)
        elif template == 'three_digit_minus_four_digit':
            return self._generate_three_minus_four(seed)
        elif template == 'word_problem_debt':
            return self._generate_word_problem_debt(seed)
        elif template == 'word_problem_temperature':
            return self._generate_word_problem_temperature(seed)
        elif template == 'word_problem_elevation':
            return self._generate_word_problem_elevation(seed)
        else:
            return self._generate_basic_subtraction(seed)

    def _generate_valid_pair(self, min_minuend: int, max_minuend: int,
                              min_subtrahend: int, max_subtrahend: int) -> Tuple[int, int]:
        """
        Generate a valid (minuend, subtrahend) pair where:
        - minuend has fewer digits than subtrahend
        - borrowing over blanks is needed
        """
        for _ in range(100):
            minuend = random.randint(min_minuend, max_minuend)
            subtrahend = random.randint(min_subtrahend, max_subtrahend)

            # Ensure minuend has fewer digits
            if len(str(minuend)) >= len(str(subtrahend)):
                continue

            # Ensure this triggers the borrow-over-blank scenario
            if self._requires_borrow_over_blank(minuend, subtrahend):
                return minuend, subtrahend

        # Fallback: construct a guaranteed pair
        minuend = random.randint(10, 99)  # 2 digits
        subtrahend = 100 + random.randint(10, 99)  # 3 digits starting with 1
        return minuend, subtrahend

    def _calculate_malrule_answer(self, minuend: int, subtrahend: int) -> int:
        """
        Calculate the answer using the FORGET/BORROW/OVER/BLANKS malrule.

        The student forgets to borrow over blank columns. When minuend has fewer
        digits, the student treats the blank as not participating in borrowing
        and uses smaller-from-larger for the extra columns.
        """
        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend)
        max_len = max(len(minuend_str), len(subtrahend_str))

        # Pad minuend with zeros
        minuend_padded = minuend_str.zfill(max_len)

        result_digits = []
        borrow = 0

        # Process from right to left
        for i in range(max_len - 1, -1, -1):
            m_digit = int(minuend_padded[i])
            s_digit = int(subtrahend_str[i]) if i < len(subtrahend_str) else 0

            # Check if this is a "blank" column (where original minuend had no digit)
            original_minuend_pos = i - (max_len - len(minuend_str))
            is_blank_column = original_minuend_pos < 0

            m_digit_after_borrow = m_digit - borrow
            borrow = 0

            if is_blank_column:
                # MALRULE: In blank columns, don't properly handle borrowing
                # Just do smaller from larger (like smaller-from-larger bug)
                if m_digit_after_borrow < s_digit:
                    result_digits.append(s_digit - m_digit_after_borrow)
                else:
                    result_digits.append(m_digit_after_borrow - s_digit)
            else:
                # Normal borrowing within the original minuend's columns
                if m_digit_after_borrow < s_digit:
                    # Need to borrow
                    m_digit_after_borrow += 10
                    borrow = 1
                result_digits.append(m_digit_after_borrow - s_digit)

        # Reverse to get correct order and convert to number
        result_digits.reverse()

        # Remove leading zeros
        while len(result_digits) > 1 and result_digits[0] == 0:
            result_digits.pop(0)

        return int(''.join(str(d) for d in result_digits))

    def _generate_basic_subtraction(self, seed: Optional[int] = None) -> Problem:
        """Template 1: Basic subtraction with fewer digits in minuend."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_m, max_m = ranges['minuend']
        min_s, max_s = ranges['subtrahend']

        minuend, subtrahend = self._generate_valid_pair(min_m, max_m, min_s, max_s)

        # Calculate correct answer (negative or abs value)
        correct_answer = minuend - subtrahend
        malrule_answer = self._calculate_malrule_answer(minuend, subtrahend)

        problem_text = f"Calculate: {minuend} - {subtrahend}"

        return Problem(
            text=problem_text,
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'minuend': minuend,
                'subtrahend': subtrahend,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'requires_borrow_over_blank': True,
                'problem_type': 'basic_subtraction',
                'template': 'basic_subtraction'
            }
        )

    def _generate_two_minus_three(self, seed: Optional[int] = None) -> Problem:
        """Template 2: 2-digit minus 3-digit problems."""
        if seed is not None:
            random.seed(seed)

        # Force 2-digit minuend and 3-digit subtrahend
        minuend, subtrahend = self._generate_valid_pair(10, 99, 100, 999)

        correct_answer = minuend - subtrahend
        malrule_answer = self._calculate_malrule_answer(minuend, subtrahend)

        contexts = [
            f"What is {minuend} - {subtrahend}?",
            f"Subtract {subtrahend} from {minuend}.",
            f"Find: {minuend} - {subtrahend}",
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'minuend': minuend,
                'subtrahend': subtrahend,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'requires_borrow_over_blank': True,
                'problem_type': 'two_digit_minus_three_digit',
                'template': 'two_digit_minus_three_digit'
            }
        )

    def _generate_three_minus_four(self, seed: Optional[int] = None) -> Problem:
        """Template 3: 3-digit minus 4-digit problems."""
        if seed is not None:
            random.seed(seed)

        minuend, subtrahend = self._generate_valid_pair(100, 999, 1000, 9999)

        correct_answer = minuend - subtrahend
        malrule_answer = self._calculate_malrule_answer(minuend, subtrahend)

        contexts = [
            f"Calculate: {minuend} - {subtrahend}",
            f"What is {minuend} minus {subtrahend}?",
            f"Subtract: {minuend} - {subtrahend}",
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'minuend': minuend,
                'subtrahend': subtrahend,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'requires_borrow_over_blank': True,
                'problem_type': 'three_digit_minus_four_digit',
                'template': 'three_digit_minus_four_digit'
            }
        )

    def _generate_word_problem_debt(self, seed: Optional[int] = None) -> Problem:
        """Template 4: Word problem about debt/owing money."""
        if seed is not None:
            random.seed(seed)

        minuend, subtrahend = self._generate_valid_pair(10, 99, 100, 500)

        correct_answer = minuend - subtrahend
        malrule_answer = self._calculate_malrule_answer(minuend, subtrahend)

        contexts = [
            f"Alex has ${minuend} in savings. He owes ${subtrahend} on a purchase. "
            f"What is his account balance after paying? ({minuend} - {subtrahend})",
            f"A store has ${minuend} in the register but needs to pay a ${subtrahend} bill. "
            f"Calculate: {minuend} - {subtrahend}",
            f"Maria saved ${minuend} but her expenses are ${subtrahend}. "
            f"What is {minuend} - {subtrahend}?",
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'minuend': minuend,
                'subtrahend': subtrahend,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'requires_borrow_over_blank': True,
                'problem_type': 'word_problem_debt',
                'template': 'word_problem_debt'
            }
        )

    def _generate_word_problem_temperature(self, seed: Optional[int] = None) -> Problem:
        """Template 5: Word problem about temperature changes."""
        if seed is not None:
            random.seed(seed)

        minuend, subtrahend = self._generate_valid_pair(10, 50, 100, 200)

        correct_answer = minuend - subtrahend
        malrule_answer = self._calculate_malrule_answer(minuend, subtrahend)

        contexts = [
            f"The temperature is {minuend} degrees. If it drops by {subtrahend} degrees, "
            f"what is the new temperature? Calculate: {minuend} - {subtrahend}",
            f"A thermometer shows {minuend} degrees. After cooling by {subtrahend} degrees, "
            f"what does it show? ({minuend} - {subtrahend})",
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'minuend': minuend,
                'subtrahend': subtrahend,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'requires_borrow_over_blank': True,
                'problem_type': 'word_problem_temperature',
                'template': 'word_problem_temperature'
            }
        )

    def _generate_word_problem_elevation(self, seed: Optional[int] = None) -> Problem:
        """Template 6: Word problem about elevation/depth."""
        if seed is not None:
            random.seed(seed)

        minuend, subtrahend = self._generate_valid_pair(50, 200, 500, 1500)

        correct_answer = minuend - subtrahend
        malrule_answer = self._calculate_malrule_answer(minuend, subtrahend)

        contexts = [
            f"A hiker is at {minuend} meters elevation. The base camp is {subtrahend} meters "
            f"below their starting point. Calculate: {minuend} - {subtrahend}",
            f"A submarine is at {minuend} meters depth. It needs to descend another {subtrahend} "
            f"meters. What is {minuend} - {subtrahend}?",
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'minuend': minuend,
                'subtrahend': subtrahend,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'requires_borrow_over_blank': True,
                'problem_type': 'word_problem_elevation',
                'template': 'word_problem_elevation'
            }
        )
