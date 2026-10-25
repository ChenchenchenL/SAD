"""
Problem generator for Left-Ten-OK malrule.

Generates subtraction problems where borrowing encounters a zero,
distinguishing between zeros that are part of "10" at the left vs. other zeros.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import random
from typing import Dict, Tuple, List
from utils import ProblemGenerator, Problem, DifficultyLevel


class LeftTenOkProblemGenerator(ProblemGenerator):
    """
    Generates subtraction problems for Left-Ten-OK malrule.

    This malrule is a variant of BORROW/FROM/ZERO where:
    - Student changes 0 to 9 without further borrowing
    - UNLESS the 0 is part of "10" at the leftmost position

    Example: 803 - 508 requires borrowing through 0, bug applies
    Example: 1003 - 508 has "10" at left, so student handles correctly
    """

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'zero_not_part_of_left_ten',  # Bug applies (e.g., 803 - 508)
            'multiple_zeros_not_left_ten', # Multiple zeros, bug applies
            'word_problem',                # Word problem context
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level and difficulty."""
        ranges = {
            3: {
                DifficultyLevel.EASY: (100, 500),
                DifficultyLevel.MEDIUM: (200, 900),
                DifficultyLevel.HARD: (300, 999),
            },
            4: {
                DifficultyLevel.EASY: (200, 800),
                DifficultyLevel.MEDIUM: (500, 2000),
                DifficultyLevel.HARD: (1000, 5000),
            },
            5: {
                DifficultyLevel.EASY: (500, 2000),
                DifficultyLevel.MEDIUM: (1000, 5000),
                DifficultyLevel.HARD: (2000, 9999),
            }
        }

        lvl = self.level if self.level in ranges else 4
        return {'minuend': ranges[lvl][self.difficulty]}

    def _is_left_ten_pattern(self, minuend_str: str, zero_position: int) -> bool:
        """
        Check if the zero at given position is part of "10" at the leftmost position.

        The bug does NOT apply when:
        - The number starts with "10..." (e.g., 1003, 103, 10234)
        - The zero being borrowed from is part of that left "10" prefix

        For example:
        - 1003: Starts with "10", zeros at positions 1 and 2 are part of this
        - 103: Starts with "10", zero at position 1 is part of this
        - 803: Does NOT start with "10", bug applies to zero at position 1

        Args:
            minuend_str: String representation of minuend
            zero_position: Index of the zero (0-based from left)

        Returns:
            True if this is a "left ten" pattern where bug doesn't apply
        """
        # Check if number starts with "10"
        if len(minuend_str) >= 2 and minuend_str[0] == '1' and minuend_str[1] == '0':
            # Find how far the leading zeros extend after the "1"
            first_nonzero_after_one = 1
            while first_nonzero_after_one < len(minuend_str) and minuend_str[first_nonzero_after_one] == '0':
                first_nonzero_after_one += 1

            # If the zero_position is within the "10..." prefix region, bug doesn't apply
            if zero_position >= 1 and zero_position < first_nonzero_after_one:
                return True

        return False

    def _calculate_malrule_answer(self, minuend: int, subtrahend: int) -> int:
        """
        Calculate what the student would get with the LEFT/TEN/OK bug.

        Bug behavior:
        - When borrowing from a zero, change 0 to 9 without further borrowing
        - UNLESS the zero is part of "10" at the leftmost position
        """
        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend).zfill(len(minuend_str))

        working_digits = [int(d) for d in minuend_str]
        subtrahend_digits = [int(d) for d in subtrahend_str]

        result_digits = []

        # Process right to left
        for i in range(len(working_digits) - 1, -1, -1):
            top = working_digits[i]
            bottom = subtrahend_digits[i]

            if top < bottom:
                # Need to borrow
                if i > 0:
                    # Check if next column is zero
                    if working_digits[i - 1] == 0:
                        # Check if this zero is part of "10" at left
                        if self._is_left_ten_pattern(minuend_str, i - 1):
                            # Left-ten pattern: borrow correctly through cascade
                            borrow_from = i - 1
                            cascade_positions = []

                            while borrow_from >= 0 and working_digits[borrow_from] == 0:
                                cascade_positions.append(borrow_from)
                                borrow_from -= 1

                            if borrow_from >= 0:
                                working_digits[borrow_from] -= 1
                                for pos in cascade_positions:
                                    working_digits[pos] = 9
                                top += 10
                        else:
                            # BUG: Change 0 to 9 without further borrowing
                            working_digits[i - 1] = 9
                            top += 10
                    else:
                        # Normal borrow from non-zero
                        working_digits[i - 1] -= 1
                        top += 10

            digit_result = top - bottom
            result_digits.insert(0, digit_result)

        result_str = ''.join(str(d) for d in result_digits).lstrip('0') or '0'
        return int(result_str)

    def generate(self, seed=None) -> Problem:
        """
        Generate a subtraction problem for Left-Ten-OK malrule testing.

        Returns:
            Problem instance
        """
        if seed is not None:
            random.seed(seed)

        templates = self.get_available_templates()
        template = random.choice(templates)

        if template == 'zero_not_part_of_left_ten':
            return self._generate_zero_not_left_ten()
        elif template == 'multiple_zeros_not_left_ten':
            return self._generate_multiple_zeros()
        elif template == 'word_problem':
            return self._generate_word_problem()
        else:
            return self._generate_zero_not_left_ten()

    def _generate_zero_not_left_ten(self) -> Problem:
        """
        Generate problem where zero is NOT part of "10" at left.
        Bug APPLIES here.

        Examples: 803 - 508, 504 - 267, 902 - 456
        Pattern: X0Y where X != 1
        """
        # First digit should NOT be 1 (to avoid left-ten pattern)
        first_digit = random.choice([2, 3, 4, 5, 6, 7, 8, 9])
        last_digit = random.randint(0, 5)  # Small to force borrowing
        minuend = first_digit * 100 + last_digit  # X0Y pattern

        # Subtrahend forces borrowing through the zero
        sub_hundreds = random.randint(1, first_digit - 1)
        sub_tens = random.randint(1, 9)
        sub_ones = random.randint(last_digit + 1, 9)
        subtrahend = sub_hundreds * 100 + sub_tens * 10 + sub_ones

        correct_answer = minuend - subtrahend
        malrule_answer = self._calculate_malrule_answer(minuend, subtrahend)

        return Problem(
            text=f"Calculate: {minuend} - {subtrahend}",
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'minuend': minuend,
                'subtrahend': subtrahend,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'zero_not_part_of_left_ten',
                'bug_applies': True,
                'zero_position': 1,  # Position of zero (0-indexed)
            }
        )

    def _generate_multiple_zeros(self) -> Problem:
        """
        Generate problem with multiple consecutive zeros.
        Bug applies because zeros are not part of "10" at left.

        Examples: 5003 - 2567, 8002 - 3456
        Pattern: X00Y where X != 1

        Constraint: sub_ones > last_digit (minuend's ones digit)
        This ensures borrowing must occur through the zeros, which triggers
        the malrule. Without this constraint, if sub_ones <= last_digit,
        no borrowing is needed in the ones column and the malrule won't fire.
        """
        first_digit = random.choice([2, 3, 4, 5, 6, 7, 8, 9])
        last_digit = random.randint(0, 5)  # Small to force borrowing
        minuend = first_digit * 1000 + last_digit  # X00Y pattern

        # Subtrahend must force borrowing through zeros: sub_ones > last_digit
        sub_thousands = random.randint(0, first_digit - 2) if first_digit > 2 else 0
        sub_hundreds = random.randint(1, 9)
        sub_tens = random.randint(1, 9)
        sub_ones = random.randint(last_digit + 1, 9)
        subtrahend = sub_thousands * 1000 + sub_hundreds * 100 + sub_tens * 10 + sub_ones

        # Ensure subtrahend < minuend while preserving borrow constraint
        if subtrahend >= minuend:
            # Minuend is X00Y, need sub_ones > last_digit to force borrow through zeros
            subtrahend = sub_hundreds * 100 + sub_tens * 10 + sub_ones

        correct_answer = minuend - subtrahend
        malrule_answer = self._calculate_malrule_answer(minuend, subtrahend)

        return Problem(
            text=f"Calculate: {minuend} - {subtrahend}",
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'minuend': minuend,
                'subtrahend': subtrahend,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'multiple_zeros_not_left_ten',
                'bug_applies': True,
                'zero_count': 2,
            }
        )

    def _generate_word_problem(self) -> Problem:
        """Generate a word problem that elicits the bug."""
        contexts = [
            ('inventory', 'A warehouse had {minuend} items. After shipping {subtrahend} items, how many remain?'),
            ('money', 'A store had ${minuend} in sales. After ${subtrahend} in expenses, what is the profit?'),
            ('distance', 'A road is {minuend} meters long. After paving {subtrahend} meters, how much is left?'),
            ('books', 'A library had {minuend} books. After lending {subtrahend} books, how many are left?')
        ]
        context, template_text = random.choice(contexts)

        # Generate X0Y pattern (bug applies)
        first_digit = random.choice([3, 4, 5, 6, 7, 8, 9])
        last_digit = random.randint(0, 5)
        minuend = first_digit * 100 + last_digit

        sub_hundreds = random.randint(1, first_digit - 2)
        sub_tens = random.randint(1, 9)
        sub_ones = random.randint(last_digit + 1, 9)
        subtrahend = sub_hundreds * 100 + sub_tens * 10 + sub_ones

        correct_answer = minuend - subtrahend
        malrule_answer = self._calculate_malrule_answer(minuend, subtrahend)

        problem_text = template_text.format(minuend=minuend, subtrahend=subtrahend)

        return Problem(
            text=problem_text,
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'minuend': minuend,
                'subtrahend': subtrahend,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'word_problem',
                'context': context,
                'bug_applies': True,
            }
        )
