"""
Malrule algorithm for Move-Over-Zero-Borrow error.

When borrowing is needed and the column to the left has 0, the student
SKIPS that column and borrows from the next non-zero column, but does
NOT decrement the 0 (doesn't turn it into 9).

Reference: Brown & Burton (1978) - Diagnostic Models for Procedural Bugs
Network location: FIND NEXT COLUMN procedure
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class MoveOverZeroBorrowMalrule(Malrule):
    """
    Implements the Move-Over-Zero-Borrow malrule from Brown & Burton (1978).

    When borrowing is needed and the column to the left has 0:
    1. Student SKIPS the 0 column
    2. Borrows from the next non-zero column to the left
    3. Does NOT decrement the 0 (doesn't cascade through it)
    4. The 0 column stays as 0

    Later, when processing the 0 column:
    - 0 - N requires borrowing again
    - Student borrows from the left (already decremented once!)
    - This results in double-decrementing the leftmost digit

    Example: 304 - 75 = 139 (correct: 229)
      - Ones: 4 < 5, need to borrow
      - Tens is 0, SKIP it, borrow from hundreds
      - 3 becomes 2, 0 stays 0, 4 becomes 14
      - 14 - 5 = 9
      - Tens: 0 < 7, need to borrow again
      - 2 becomes 1, 0 becomes 10
      - 10 - 7 = 3
      - Hundreds: 1 - 0 = 1
      - Result: 139

    Frequency: 10 students (alone) in Brown & Burton (1978) study
    Often combined with DIFF/0-N=N (34 students) or DIFF/0-N=0 (12 students)
    """

    def get_name(self) -> str:
        return "Move-Over-Zero-Borrow"

    def get_description(self) -> str:
        return (
            "A systematic procedural bug where the student skips over a zero "
            "when borrowing, rather than cascading through it properly. The student "
            "borrows from the next non-zero digit to the left but fails to decrement "
            "the zero to 9. This leaves the zero unchanged, creating a 0-N situation "
            "in that column which requires another borrow, effectively double-borrowing "
            "from the leftmost non-zero digit.\n\n"
            "Example: 304 - 75 = 139 (correct: 229)\n"
            "The student skips the 0 when borrowing for ones column, then has to "
            "borrow again when processing the tens column (0-7)."
        )

    def calculate_expected_answer(self, problem: Problem) -> int:
        """
        Calculate the expected incorrect answer for this malrule.

        For Move-Over-Zero-Borrow:
        1. When borrowing and next column is 0, skip the 0
        2. Borrow from the next non-zero column
        3. Don't change the 0 to 9
        4. When processing the 0 column, borrow again if needed

        Args:
            problem: Subtraction problem

        Returns:
            Expected incorrect answer as integer
        """
        minuend, subtrahend = problem.operands[:2]
        return self._apply_move_over_zero_borrow(minuend, subtrahend)

    def _apply_move_over_zero_borrow(self, minuend: int, subtrahend: int) -> int:
        """
        Apply the Move-Over-Zero-Borrow algorithm.

        The key insight: when we skip a 0, we don't decrement it.
        Later, when we process that column (0-N), we need to borrow AGAIN,
        which double-decrements the leftmost digit.
        """
        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend).zfill(len(minuend_str))

        minuend_digits = [int(d) for d in minuend_str]
        subtrahend_digits = [int(d) for d in subtrahend_str]

        working_minuend = minuend_digits.copy()
        result_digits = []

        # Track which columns we skipped (they still have 0)
        skipped_zeros = set()

        # First pass: identify where we'll skip zeros when borrowing
        # Process right to left
        for i in range(len(working_minuend) - 1, -1, -1):
            top_digit = working_minuend[i]
            bottom_digit = subtrahend_digits[i]

            if top_digit < bottom_digit:
                # Need to borrow
                borrow_from = i - 1

                # MALRULE: Skip over zeros
                while borrow_from >= 0 and working_minuend[borrow_from] == 0:
                    skipped_zeros.add(borrow_from)  # Mark as skipped
                    borrow_from -= 1

                if borrow_from >= 0:
                    # Borrow from this column
                    working_minuend[borrow_from] -= 1
                    # The zeros in between are NOT changed (the malrule!)
                    # Only add 10 to current column
                    working_minuend[i] += 10

        # Reset for actual calculation
        working_minuend = minuend_digits.copy()
        result_digits = []

        # Second pass: calculate with the malrule
        for i in range(len(working_minuend) - 1, -1, -1):
            top_digit = working_minuend[i]
            bottom_digit = subtrahend_digits[i]

            if top_digit < bottom_digit:
                # Need to borrow
                borrow_from = i - 1

                # MALRULE: Skip over zeros without changing them
                zeros_skipped = []
                while borrow_from >= 0 and working_minuend[borrow_from] == 0:
                    zeros_skipped.append(borrow_from)
                    borrow_from -= 1

                if borrow_from >= 0:
                    # Borrow from this column
                    working_minuend[borrow_from] -= 1
                    # The zeros are NOT changed to 9 (the malrule!)
                    # Add 10 to current column
                    top_digit += 10
                    digit_result = top_digit - bottom_digit
                else:
                    # No column to borrow from
                    digit_result = abs(top_digit - bottom_digit)

                result_digits.insert(0, digit_result)
            else:
                digit_result = top_digit - bottom_digit
                result_digits.insert(0, digit_result)

        result_str = ''.join(str(d) for d in result_digits).lstrip('0') or '0'
        return int(result_str)

    def _generate_concise_steps(self, problem: Problem, minuend: int,
                                 subtrahend: int, malrule_result: int) -> List[str]:
        """
        Generate concise steps showing only formulas and values.
        """
        steps = []
        steps.append(f"Question: {problem.text}")

        template = problem.metadata.get('template', '')
        if template == 'word_problem' or 'word' in template.lower():
            steps.append(f"Formula: {minuend} - {subtrahend}")

        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend).zfill(len(minuend_str))

        minuend_digits = [int(d) for d in minuend_str]
        subtrahend_digits = [int(d) for d in subtrahend_str]

        working_minuend = minuend_digits.copy()

        for i in range(len(working_minuend) - 1, -1, -1):
            top_digit = working_minuend[i]
            bottom_digit = subtrahend_digits[i]
            col_num = len(working_minuend) - i

            if top_digit < bottom_digit:
                borrow_from = i - 1
                while borrow_from >= 0 and working_minuend[borrow_from] == 0:
                    borrow_from -= 1

                if borrow_from >= 0:
                    working_minuend[borrow_from] -= 1
                    top_digit += 10
                    digit_result = top_digit - bottom_digit
                    steps.append(f"Column {col_num}: {top_digit} - {bottom_digit} = {digit_result}")
                else:
                    digit_result = abs(top_digit - bottom_digit)
                    steps.append(f"Column {col_num}: |{top_digit} - {bottom_digit}| = {digit_result}")
            else:
                digit_result = top_digit - bottom_digit
                steps.append(f"Column {col_num}: {top_digit} - {bottom_digit} = {digit_result}")

        steps.append(f"Answer: {malrule_result}")
        return steps

    def _generate_verbose_steps(self, problem: Problem, minuend: int,
                                 subtrahend: int, malrule_result: int) -> List[str]:
        """
        Generate verbose steps with full explanations.
        """
        steps = []
        steps.append(f"Problem: {minuend} - {subtrahend}")
        steps.append("")
        steps.append(f"MALRULE: {self.get_name()}")
        steps.append("Student believes: 'When I see a 0, I skip over it to borrow from the next column'")
        steps.append("")

        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend).zfill(len(minuend_str))

        minuend_digits = [int(d) for d in minuend_str]
        subtrahend_digits = [int(d) for d in subtrahend_str]

        working_minuend = minuend_digits.copy()

        steps.append("Working right to left:")
        steps.append("")

        for i in range(len(working_minuend) - 1, -1, -1):
            top_digit = working_minuend[i]
            bottom_digit = subtrahend_digits[i]
            col_name = ["ones", "tens", "hundreds", "thousands", "ten-thousands"][len(working_minuend) - 1 - i] \
                       if len(working_minuend) - 1 - i < 5 else f"column {len(working_minuend) - i}"

            steps.append(f"Column {len(working_minuend) - i} ({col_name}): {top_digit} - {bottom_digit}")

            if top_digit < bottom_digit:
                steps.append(f"  Need to borrow: {top_digit} < {bottom_digit}")

                borrow_from = i - 1
                zeros_skipped = []
                while borrow_from >= 0 and working_minuend[borrow_from] == 0:
                    zeros_skipped.append(borrow_from)
                    borrow_from -= 1

                if zeros_skipped:
                    steps.append(f"  Looking left: found 0(s) at position(s) {[len(working_minuend) - z for z in zeros_skipped]}")
                    steps.append(f"  MALRULE: Skip the zero(s) and borrow from position {len(working_minuend) - borrow_from}")
                    steps.append(f"  (WRONG! Should cascade: 0 becomes 10, then 9 after lending right)")

                if borrow_from >= 0:
                    old_val = working_minuend[borrow_from]
                    working_minuend[borrow_from] -= 1
                    steps.append(f"  Borrow: {old_val} becomes {working_minuend[borrow_from]}")
                    steps.append(f"  Zero(s) NOT changed (MALRULE - they should become 9)")
                    top_digit += 10
                    digit_result = top_digit - bottom_digit
                    steps.append(f"  {top_digit} - {bottom_digit} = {digit_result}")
                else:
                    digit_result = abs(top_digit - bottom_digit)
                    steps.append(f"  Cannot borrow - using |{top_digit} - {bottom_digit}| = {digit_result}")
            else:
                digit_result = top_digit - bottom_digit
                steps.append(f"  {top_digit} - {bottom_digit} = {digit_result}")

            steps.append("")

        steps.append(f"Answer: {malrule_result} (INCORRECT)")
        steps.append(f"Correct answer would be: {minuend - subtrahend}")

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Move-Over-Zero-Borrow malrule.

        Args:
            problem: Problem instance with minuend and subtrahend
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with incorrect answer and steps
        """
        minuend, subtrahend = problem.operands[:2]
        malrule_result = self.calculate_expected_answer(problem)

        if verbose:
            steps = self._generate_verbose_steps(problem, minuend, subtrahend, malrule_result)
        else:
            steps = self._generate_concise_steps(problem, minuend, subtrahend, malrule_result)

        return Solution(
            answer=str(malrule_result),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
