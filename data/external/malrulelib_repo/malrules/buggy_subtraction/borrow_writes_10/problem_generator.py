"""
Problem generator for Borrow-Writes-10 malrule.

Generates subtraction problems where borrowing encounters a zero
and the malrule produces a different answer by writing 10 instead of 9.

Reference: Brown & Burton (1978). Diagnostic models for procedural bugs
in basic mathematical skills. Cognitive Science, 2(2), 155-192.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import random
from typing import Dict, Tuple, List
from utils import ProblemGenerator, Problem, DifficultyLevel


class BorrowWrites10ProblemGenerator(ProblemGenerator):
    """
    Generates subtraction problems that elicit the Borrow-Writes-10 error.

    The bug occurs when:
    1. Student needs to borrow from a column with 0 on top
    2. Student correctly borrows from the next column to the left
    3. BUT student writes 10 instead of 9 in the zero column

    Example from Brown & Burton (1978): 1300 - 522 = 788 (correct: 778)

    Critical Constraint: sub_ones > minuend_ones (last digit)
    ----------------------------------------------------------
    For the malrule to fire, borrowing must cascade through the zero column(s).
    This only happens when the subtrahend's ones digit exceeds the minuend's
    ones digit, forcing a borrow from tens. If the tens column is 0, the
    borrow cascades through it, triggering the "write 10 instead of 9" error.

    Without this constraint (e.g., 1300 - 650 where ones are 0-0), no borrowing
    occurs in the ones column and the malrule produces the same answer as correct.
    """

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'single_zero',           # X0Y - Z (e.g., 503 - 267)
            'double_zero',           # X00Y - Z (e.g., 1300 - 522)
            'multiple_zeros',        # X0Y0Z - W (e.g., 50205 - 12867)
            'zero_near_beginning',   # 0XY format in hundreds (e.g., 1023 - 567)
            'word_problem'           # Word problem context
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level and difficulty."""
        ranges = {
            3: {
                DifficultyLevel.EASY: (100, 500),
                DifficultyLevel.MEDIUM: (200, 999),
                DifficultyLevel.HARD: (500, 2000),
            },
            4: {
                DifficultyLevel.EASY: (200, 1000),
                DifficultyLevel.MEDIUM: (500, 3000),
                DifficultyLevel.HARD: (1000, 5000),
            },
            5: {
                DifficultyLevel.EASY: (500, 2000),
                DifficultyLevel.MEDIUM: (1000, 5000),
                DifficultyLevel.HARD: (2000, 10000),
            }
        }

        lvl = self.level if self.level in ranges else 4
        return {'minuend': ranges[lvl][self.difficulty]}

    def _calculate_malrule_answer(self, minuend: int, subtrahend: int) -> int:
        """
        Calculate the malrule answer for Borrow-Writes-10.

        When encountering a 0 that needs to be borrowed through,
        the student writes 10 instead of 9.
        """
        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend).zfill(len(minuend_str))

        minuend_digits = [int(d) for d in minuend_str]
        subtrahend_digits = [int(d) for d in subtrahend_str]

        working_minuend = minuend_digits.copy()
        result_digits = []

        # Process each column right to left
        for i in range(len(working_minuend) - 1, -1, -1):
            top_digit = working_minuend[i]
            bottom_digit = subtrahend_digits[i]

            if top_digit < bottom_digit:
                # Need to borrow
                borrow_from = i - 1
                cascade_positions = []

                # Find zeros to cascade through
                while borrow_from >= 0 and working_minuend[borrow_from] == 0:
                    cascade_positions.append(borrow_from)
                    borrow_from -= 1

                if borrow_from >= 0:
                    # Decrement the source
                    working_minuend[borrow_from] -= 1

                    # MALRULE: Write 10 instead of 9 for zeros in cascade
                    for pos in cascade_positions:
                        working_minuend[pos] = 10  # Bug: should be 9

                    # Add 10 to current position
                    top_digit += 10
                    working_minuend[i] = top_digit

            digit_result = working_minuend[i] - bottom_digit
            result_digits.insert(0, digit_result)

        # Handle digits > 9 in result (from the 10 vs 9 error)
        final_result = []
        carry = 0
        for d in reversed(result_digits):
            d += carry
            carry = d // 10
            final_result.insert(0, d % 10)
        if carry > 0:
            final_result.insert(0, carry)

        result_str = ''.join(str(d) for d in final_result).lstrip('0') or '0'
        return int(result_str)

    def _has_borrow_through_zero(self, minuend: int, subtrahend: int) -> bool:
        """Check if this problem requires borrowing through a zero."""
        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend).zfill(len(minuend_str))

        minuend_digits = [int(d) for d in minuend_str]
        subtrahend_digits = [int(d) for d in subtrahend_str]

        working_minuend = minuend_digits.copy()

        for i in range(len(working_minuend) - 1, -1, -1):
            top_digit = working_minuend[i]
            bottom_digit = subtrahend_digits[i]

            if top_digit < bottom_digit:
                # Check if next column is zero
                if i > 0 and working_minuend[i - 1] == 0:
                    return True

                # Process borrow for next iteration
                borrow_from = i - 1
                while borrow_from >= 0 and working_minuend[borrow_from] == 0:
                    working_minuend[borrow_from] = 9
                    borrow_from -= 1
                if borrow_from >= 0:
                    working_minuend[borrow_from] -= 1

        return False

    def generate(self, seed=None) -> Problem:
        """
        Generate a subtraction problem with zero that needs borrowing through.

        Returns:
            Problem instance requiring borrowing through zero
        """
        if seed is not None:
            random.seed(seed)

        templates = self.get_available_templates()
        template = random.choice(templates)

        if template == 'single_zero':
            return self._generate_single_zero()
        elif template == 'double_zero':
            return self._generate_double_zero()
        elif template == 'multiple_zeros':
            return self._generate_multiple_zeros()
        elif template == 'zero_near_beginning':
            return self._generate_zero_near_beginning()
        elif template == 'word_problem':
            return self._generate_word_problem()
        else:
            return self._generate_single_zero()

    def _generate_single_zero(self) -> Problem:
        """Generate a problem with single zero: X0Y - Z pattern."""
        # Pattern: hundreds digit, 0, units digit (e.g., 503)
        first_digit = random.randint(2, 9)
        last_digit = random.randint(0, 5)  # Small to force borrowing
        minuend = first_digit * 100 + last_digit

        # Subtrahend must have ones digit > last_digit to force borrow through zero
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
                'template': 'single_zero',
                'requires_borrow_through_zero': True
            }
        )

    def _generate_double_zero(self) -> Problem:
        """
        Generate a problem with double zero: X00Y - Z pattern.
        This is the pattern from Brown & Burton (1978): 1300 - 522 = 788
        """
        # Pattern: X00Y (e.g., 1300, 2005, 5001)
        first_digit = random.randint(1, 9)
        last_digit = random.randint(0, 5)
        minuend = first_digit * 1000 + last_digit

        # Subtrahend must force borrowing through both zeros
        # ones digit > last_digit
        sub_thousands = 0  # No thousands
        sub_hundreds = random.randint(1, 9)
        sub_tens = random.randint(1, 9)
        sub_ones = random.randint(last_digit + 1, 9)
        subtrahend = sub_hundreds * 100 + sub_tens * 10 + sub_ones

        # Ensure subtrahend < minuend while preserving borrow constraint
        if subtrahend >= minuend:
            # Minuend is X00Y, need sub_ones > last_digit to force borrow through zeros
            subtrahend = sub_tens * 10 + sub_ones

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
                'template': 'double_zero',
                'requires_borrow_through_zero': True
            }
        )

    def _generate_multiple_zeros(self) -> Problem:
        """Generate a problem with multiple zeros in different positions."""
        # Pattern: X0Y0Z (e.g., 50203)
        first = random.randint(1, 9)
        middle = random.randint(1, 9)
        last = random.randint(0, 5)
        minuend = first * 10000 + middle * 100 + last

        # Subtrahend forces borrowing
        subtrahend = random.randint(minuend // 3, minuend - 1000)

        # Ensure borrowing through zero is needed
        if not self._has_borrow_through_zero(minuend, subtrahend):
            # Adjust subtrahend to force borrow through zero
            minuend_str = str(minuend)
            sub_str = str(subtrahend).zfill(len(minuend_str))
            sub_digits = list(sub_str)
            # Make ones digit larger than minuend's ones digit
            sub_digits[-1] = str(min(9, int(minuend_str[-1]) + random.randint(1, 4)))
            subtrahend = int(''.join(sub_digits))

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
                'template': 'multiple_zeros',
                'requires_borrow_through_zero': True
            }
        )

    def _generate_zero_near_beginning(self) -> Problem:
        """Generate a problem with zero near the beginning (second position)."""
        # Pattern: X0YZ (e.g., 1023, 2045)
        first = random.randint(1, 9)
        third = random.randint(1, 9)
        fourth = random.randint(0, 5)
        minuend = first * 1000 + third * 10 + fourth

        # Force borrow through zero
        sub_hundreds = random.randint(1, 9)
        sub_tens = random.randint(third + 1, 9) if third < 9 else 9
        sub_ones = random.randint(fourth + 1, 9) if fourth < 9 else 9
        subtrahend = sub_hundreds * 100 + sub_tens * 10 + sub_ones

        if subtrahend >= minuend:
            # Minuend is X0YZ, need sub_ones > fourth to force borrow through zero
            subtrahend = sub_tens * 10 + sub_ones

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
                'template': 'zero_near_beginning',
                'requires_borrow_through_zero': True
            }
        )

    def _generate_word_problem(self) -> Problem:
        """Generate a word problem that requires borrowing through zero."""
        contexts = [
            ('inventory', 'A warehouse had {minuend} items. After shipping {subtrahend} items, how many remain?'),
            ('attendance', 'A stadium held {minuend} people. After {subtrahend} people left, how many remained?'),
            ('money', 'A store had ${minuend} in sales. After ${subtrahend} in expenses, what is the profit?'),
            ('distance', 'A road is {minuend} meters long. After paving {subtrahend} meters, how much is left?')
        ]
        context, template = random.choice(contexts)

        # Use double zero pattern for word problems (like the paper example)
        first_digit = random.randint(1, 9)
        last_digit = random.randint(0, 5)
        minuend = first_digit * 1000 + last_digit

        sub_hundreds = random.randint(1, 9)
        sub_tens = random.randint(1, 9)
        sub_ones = random.randint(last_digit + 1, 9)
        subtrahend = sub_hundreds * 100 + sub_tens * 10 + sub_ones

        if subtrahend >= minuend:
            # Minuend is X00Y, need sub_ones > last_digit to force borrow through zeros
            subtrahend = sub_tens * 10 + sub_ones

        correct_answer = minuend - subtrahend
        malrule_answer = self._calculate_malrule_answer(minuend, subtrahend)

        return Problem(
            text=template.format(minuend=minuend, subtrahend=subtrahend),
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
                'requires_borrow_through_zero': True
            }
        )
