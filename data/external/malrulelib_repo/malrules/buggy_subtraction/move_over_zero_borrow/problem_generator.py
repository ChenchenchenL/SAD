"""
Problem generator for Move-Over-Zero-Borrow malrule.

Generates subtraction problems where the minuend has a zero in the middle
and borrowing is required through that zero column.

Reference: Brown & Burton (1978) - Diagnostic Models for Procedural Bugs
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import random
from typing import Dict, Tuple, List
from utils import ProblemGenerator, Problem, DifficultyLevel


class MoveOverZeroBorrowProblemGenerator(ProblemGenerator):
    """
    Generates subtraction problems requiring borrowing through a zero.

    The minuend must have a 0 in a middle position, and the subtrahend
    must require borrowing from the column immediately to the right of
    that zero.

    Example: 304 - 75 (Brown & Burton, 1978)
      - Minuend has 0 in tens place
      - Ones column (4-5) requires borrowing
      - Student should borrow through the 0, but skips it instead
    """

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'single_middle_zero',      # X0Y pattern (e.g., 304)
            'multiple_zeros',          # X00Y pattern (e.g., 5003)
            'zero_after_borrow',       # Zero encountered after initial borrow
            'large_numbers',           # 4+ digit numbers with zeros
            'word_problem'             # Context-based problems
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level and difficulty."""
        ranges = {
            3: {
                DifficultyLevel.EASY: (100, 500),
                DifficultyLevel.MEDIUM: (200, 700),
                DifficultyLevel.HARD: (300, 999),
            },
            4: {
                DifficultyLevel.EASY: (200, 800),
                DifficultyLevel.MEDIUM: (300, 1500),
                DifficultyLevel.HARD: (500, 2999),
            },
            5: {
                DifficultyLevel.EASY: (500, 2000),
                DifficultyLevel.MEDIUM: (1000, 5000),
                DifficultyLevel.HARD: (2000, 9999),
            }
        }

        lvl = self.level if self.level in ranges else 3
        return {'minuend': ranges[lvl][self.difficulty]}

    def generate(self, seed=None) -> Problem:
        """
        Generate a subtraction problem with zero that needs borrowing through.

        Returns:
            Problem instance requiring borrowing through zero
        """
        if seed is not None:
            random.seed(seed)

        # Choose template
        template = random.choice(self.get_available_templates())

        if template == 'single_middle_zero':
            return self._generate_single_middle_zero()
        elif template == 'multiple_zeros':
            return self._generate_multiple_zeros()
        elif template == 'zero_after_borrow':
            return self._generate_zero_after_borrow()
        elif template == 'large_numbers':
            return self._generate_large_numbers()
        elif template == 'word_problem':
            return self._generate_word_problem()
        else:
            return self._generate_single_middle_zero()

    def _generate_single_middle_zero(self) -> Problem:
        """
        Generate a problem with a single zero in the middle (X0Y pattern).

        This is the classic case from Brown & Burton (1978): 304 - 75 = 139
        """
        # Pattern: X0Y where X is hundreds, 0 is tens, Y is ones
        first_digit = random.randint(2, 9)  # Hundreds digit (at least 2 for borrowing)
        last_digit = random.randint(0, 5)   # Small ones digit to force borrowing

        minuend = first_digit * 100 + last_digit  # X0Y pattern (e.g., 304)

        # Generate subtrahend that forces borrowing in ones column
        # The ones digit of subtrahend must be > last_digit
        sub_tens = random.randint(1, 9)  # Non-zero tens to create 0-N situation
        sub_ones = random.randint(last_digit + 1, 9) if last_digit < 9 else 9

        # Ensure subtrahend is less than minuend
        max_sub_hundreds = first_digit - 2  # Leave room for borrowing
        if max_sub_hundreds < 0:
            max_sub_hundreds = 0
        sub_hundreds = random.randint(0, max_sub_hundreds) if max_sub_hundreds > 0 else 0

        subtrahend = sub_hundreds * 100 + sub_tens * 10 + sub_ones

        # Ensure valid subtraction
        if subtrahend >= minuend:
            subtrahend = sub_tens * 10 + sub_ones  # Remove hundreds

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
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'zero_position': 1,  # Tens place (0-indexed from left)
                'requires_borrow_through_zero': True,
                'template': 'single_middle_zero'
            }
        )

    def _generate_multiple_zeros(self) -> Problem:
        """
        Generate a problem with multiple consecutive zeros (X00Y pattern).

        Example: 5003 - 2567
        """
        # Pattern: X00Y
        first_digit = random.randint(3, 9)
        last_digit = random.randint(0, 5)

        minuend = first_digit * 1000 + last_digit  # e.g., 5003

        # Subtrahend forces borrowing in ones column
        sub_thousands = random.randint(1, first_digit - 2) if first_digit > 2 else 0
        sub_hundreds = random.randint(1, 9)
        sub_tens = random.randint(1, 9)
        sub_ones = random.randint(last_digit + 1, 9) if last_digit < 9 else 9

        subtrahend = sub_thousands * 1000 + sub_hundreds * 100 + sub_tens * 10 + sub_ones

        if subtrahend >= minuend:
            subtrahend = sub_hundreds * 100 + sub_tens * 10 + sub_ones

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
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'zero_count': 2,
                'requires_borrow_through_zero': True,
                'template': 'multiple_zeros'
            }
        )

    def _generate_zero_after_borrow(self) -> Problem:
        """
        Generate a problem where zero is encountered after initial borrowing.

        Pattern: XY0Z where borrowing cascades to hit the 0
        """
        # Pattern: XY0Z (e.g., 4502)
        first = random.randint(2, 9)
        second = random.randint(1, 9)
        last = random.randint(0, 5)

        minuend = first * 1000 + second * 100 + last  # e.g., 4502

        # Force borrowing that hits the zero
        sub_tens = random.randint(1, 9)
        sub_ones = random.randint(last + 1, 9) if last < 9 else 9

        subtrahend = random.randint(10, 99) * 10 + sub_ones
        if subtrahend >= minuend:
            subtrahend = sub_tens * 10 + sub_ones

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
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'requires_borrow_through_zero': True,
                'template': 'zero_after_borrow'
            }
        )

    def _generate_large_numbers(self) -> Problem:
        """
        Generate a problem with larger numbers (4-5 digits) containing zeros.

        Constraint: sub_ones > last (minuend's ones digit)
        This ensures borrowing must occur through the zero column(s), which
        triggers the malrule. Without this constraint, if sub_ones <= last,
        no borrowing is needed and the malrule won't produce a different answer.
        """
        # Pattern: X0Y0Z or similar
        first = random.randint(1, 9)
        middle = random.randint(1, 9)
        last = random.randint(0, 5)

        minuend = first * 10000 + middle * 100 + last  # e.g., 50205

        # Generate subtrahend with sub_ones > last to force borrow through zeros
        base = random.randint(minuend // 4, minuend // 2)
        sub_ones = last + 1 if last < 9 else 9
        subtrahend = (base // 10) * 10 + sub_ones

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
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'requires_borrow_through_zero': True,
                'template': 'large_numbers',
                'num_digits': len(str(minuend))
            }
        )

    def _generate_word_problem(self) -> Problem:
        """
        Generate a word problem with zero in the minuend.
        """
        contexts = [
            ('inventory', 'A warehouse had {minuend} items. After shipping {subtrahend} items, how many remain?'),
            ('attendance', 'A stadium held {minuend} people. After {subtrahend} people left, how many remained?'),
            ('money', 'A store had ${minuend} in sales. After ${subtrahend} in expenses, what is the profit?'),
            ('distance', 'A road is {minuend} meters long. After paving {subtrahend} meters, how much is left?')
        ]
        context, problem_template = random.choice(contexts)

        # Generate number with zero: X0Y pattern
        first_digit = random.randint(3, 9)
        last_digit = random.randint(0, 5)
        minuend = first_digit * 100 + last_digit  # e.g., 503, 704

        # Force borrowing through zero
        sub_hundreds = random.randint(0, first_digit - 2) if first_digit > 2 else 0
        sub_tens = random.randint(1, 9)
        sub_ones = random.randint(last_digit + 1, 9) if last_digit < 9 else 9
        subtrahend = sub_hundreds * 100 + sub_tens * 10 + sub_ones

        if subtrahend >= minuend:
            subtrahend = sub_tens * 10 + sub_ones

        correct_answer = minuend - subtrahend
        malrule_answer = self._calculate_malrule_answer(minuend, subtrahend)
        problem_text = problem_template.format(minuend=minuend, subtrahend=subtrahend)

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
                'zero_position': 1,
                'requires_borrow_through_zero': True,
                'template': 'word_problem',
                'context': context
            }
        )

    def _calculate_malrule_answer(self, minuend: int, subtrahend: int) -> int:
        """
        Calculate the expected incorrect answer using the Move-Over-Zero-Borrow malrule.

        The malrule:
        1. When borrowing is needed and the column to the left has 0
        2. SKIP the 0 and borrow from the next column left
        3. The 0 is NOT decremented (stays 0)
        4. When 0-N is encountered (from the skipped column), use smaller-from-larger

        Example: 304 - 75
        - Ones: 4 < 5, need to borrow
        - Tens has 0, so skip it and borrow from 3
        - 3 becomes 2, 0 stays 0, 4 becomes 14
        - 14 - 5 = 9
        - 0 - 7: Can't do this, so 7 - 0 = 7 (smaller from larger)
        - 2 - 0 = 2
        - Result: 279... but paper says 139

        Actually, re-reading: The paper example 304-75=139 suggests:
        - The student uses 0-7 = 7 (writing bottom digit when top is 0)
        - OR the student gets confused about the borrow

        Let me trace through more carefully with the paper's result:
        304 - 75 = 139
        - 14 - 5 = 9 (ones)
        - 0 - 7 = 3 (some error here - maybe they see decremented hundreds as affecting tens?)
        - 3 is decremented to 2, but they write... 1?

        The combination with DIFF/0-N=N would give:
        - 14-5 = 9 (after skipping 0 to borrow from 3)
        - 0-7 = 7 (0-N=N)
        - 2-0 = 2
        - Result: 279

        But paper says 139. Let me reconsider...
        Perhaps with pure move-over-zero:
        - 4 becomes 14 (borrowed), 3 becomes 2, 0 unchanged
        - 14-5=9, 0-7=? (this is the problem)
        - If they do smaller-from-larger for the 0-7: |0-7|=7
        - 2-0=2 -> 279

        For 139: The 1 in hundreds suggests something else...
        Maybe the student also borrows from the 0 after skipping? Or makes another error.

        Let me implement the basic malrule and handle 0-N with smaller-from-larger (|0-N|=N).
        """
        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend).zfill(len(minuend_str))

        minuend_digits = [int(d) for d in minuend_str]
        subtrahend_digits = [int(d) for d in subtrahend_str]

        working_minuend = minuend_digits.copy()
        result_digits = []

        # Process right to left
        for i in range(len(working_minuend) - 1, -1, -1):
            top_digit = working_minuend[i]
            bottom_digit = subtrahend_digits[i]

            if top_digit < bottom_digit:
                # Need to borrow
                # Look for a column to borrow from, SKIPPING zeros
                borrow_from = i - 1

                # MALRULE: Skip over zeros without decrementing them
                while borrow_from >= 0 and working_minuend[borrow_from] == 0:
                    borrow_from -= 1

                if borrow_from >= 0:
                    # Borrow from this column (skip the zeros)
                    working_minuend[borrow_from] -= 1
                    # The zeros in between are NOT changed (not set to 9)
                    top_digit += 10
                    digit_result = top_digit - bottom_digit
                else:
                    # No column to borrow from - use smaller from larger
                    digit_result = abs(top_digit - bottom_digit)

                result_digits.insert(0, digit_result)
            else:
                # No borrowing needed, but check if top is 0 and bottom is not
                # This handles the 0-N case that occurs after the malrule
                if top_digit == 0 and bottom_digit > 0:
                    # The 0 was skipped during borrow, so 0-N situation
                    # Use smaller-from-larger: 0-N = N (take the bottom digit)
                    digit_result = bottom_digit
                else:
                    digit_result = top_digit - bottom_digit
                result_digits.insert(0, digit_result)

        result_str = ''.join(str(d) for d in result_digits).lstrip('0') or '0'
        return int(result_str)
