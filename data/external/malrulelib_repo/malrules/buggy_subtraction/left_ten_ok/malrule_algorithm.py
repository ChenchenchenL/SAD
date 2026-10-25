"""
Malrule algorithm for Left-Ten-OK error.

A variant of BORROW/FROM/ZERO where the student changes 0 to 9 without
further borrowing UNLESS the 0 is part of a 10 in the left part of the
top number.

Reference: Brown & Burton (1978). Diagnostic models for procedural bugs
in basic mathematical skills. Cognitive Science, 2(2), 155-192.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class LeftTenOkMalrule(Malrule):
    """
    Implements the Left-Ten-OK malrule (variant of BORROW/FROM/ZERO).

    When borrowing from a column with 0:
    - If the 0 is part of "10" at the leftmost position, borrow correctly
    - Otherwise, change 0 to 9 WITHOUT continuing the borrow cascade

    Example: 803 - 508
    - Ones: 3 < 8, need borrow. Look left: 0
    - The 0 is NOT part of "10" at left (it's part of "80")
    - BUG: Change 0 to 9, add 10 to ones, but don't decrement 8
    - 13 - 8 = 5 (ones)
    - 9 - 0 = 9 (tens)
    - 8 - 5 = 3 (hundreds)
    - Result: 395 (WRONG! Should be 295)

    But for 1003 - 508:
    - The "10" is at leftmost position
    - Student handles this correctly
    - Result: 495 (correct)
    """

    def get_name(self) -> str:
        return "Left-Ten-OK"

    def get_description(self) -> str:
        return (
            "A variant of the BORROW/FROM/ZERO bug where the student changes "
            "0 to 9 without further borrowing, UNLESS the 0 is part of '10' "
            "in the left part of the top number. When the leftmost digits "
            "form '10', the student recognizes this as a special case and "
            "borrows correctly. Otherwise, they apply the standard borrow-from-zero "
            "bug, writing 9 in place of 0 without decrementing the next column."
        )

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
            # For "1003", zeros are at positions 1 and 2
            # For "103", zero is at position 1
            first_nonzero_after_one = 1
            while first_nonzero_after_one < len(minuend_str) and minuend_str[first_nonzero_after_one] == '0':
                first_nonzero_after_one += 1

            # If the zero_position is within the "10..." prefix region, bug doesn't apply
            if zero_position >= 1 and zero_position < first_nonzero_after_one:
                return True

        return False

    def calculate_expected_answer(self, problem: Problem) -> Any:
        """
        Calculate the expected incorrect answer for this malrule.

        Bug behavior:
        - When borrowing from a zero, change 0 to 9 without further borrowing
        - UNLESS the zero is part of "10" at the leftmost position

        Args:
            problem: Subtraction problem

        Returns:
            Expected incorrect answer as string
        """
        minuend, subtrahend = problem.operands[:2]
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
        return result_str

    def _generate_verbose_steps(self, problem: Problem, minuend: int, subtrahend: int, malrule_result: str) -> List[str]:
        """Generate verbose steps with full explanations."""
        steps = []
        steps.append(f"Problem: {minuend} - {subtrahend}")
        steps.append("")

        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend).zfill(len(minuend_str))

        working_digits = [int(d) for d in minuend_str]
        subtrahend_digits = [int(d) for d in subtrahend_str]

        steps.append("MALRULE: Left-Ten-OK")
        steps.append("  Student changes 0 to 9 without borrowing,")
        steps.append("  UNLESS the 0 is part of '10' at leftmost position")
        steps.append("")
        steps.append("Working right to left:")
        steps.append("")

        bug_applied = False

        for i in range(len(working_digits) - 1, -1, -1):
            top = working_digits[i]
            bottom = subtrahend_digits[i]
            col_num = len(working_digits) - i

            steps.append(f"Column {col_num}: {top} - {bottom}")

            if top < bottom:
                steps.append(f"  Need to borrow: {top} < {bottom}")

                if i > 0:
                    if working_digits[i - 1] == 0:
                        if self._is_left_ten_pattern(minuend_str, i - 1):
                            steps.append(f"  Zero at position {i-1} is part of '10' at left")
                            steps.append(f"  Student recognizes this - borrows correctly!")

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

                            steps.append(f"  Cascaded through zeros correctly")
                            steps.append(f"  {top} - {bottom} = {top - bottom}")
                        else:
                            steps.append(f"  Looking left: found 0 (not part of '10' at left)")
                            steps.append(f"  MALRULE APPLIED: Change 0 to 9 without further borrowing!")
                            steps.append(f"  (WRONG! Should cascade left to find non-zero digit)")
                            working_digits[i - 1] = 9
                            top += 10
                            bug_applied = True
                            steps.append(f"  {top} - {bottom} = {top - bottom}")
                    else:
                        working_digits[i - 1] -= 1
                        top += 10
                        steps.append(f"  Borrowed from {working_digits[i - 1] + 1}: {top} - {bottom} = {top - bottom}")
            else:
                steps.append(f"  {top} - {bottom} = {top - bottom}")

            steps.append("")

        if bug_applied:
            steps.append(f"Final Answer: {malrule_result} (INCORRECT - failed to cascade borrow)")
        else:
            steps.append(f"Final Answer: {malrule_result}")

        return steps

    def _generate_concise_steps(self, problem: Problem, minuend: int, subtrahend: int, malrule_result: str) -> List[str]:
        """Generate concise steps showing only formulas and values."""
        steps = []
        steps.append(f"Question: {problem.text}")

        template = problem.metadata.get('template', '')
        if template == 'word_problem' or 'word' in template.lower():
            steps.append(f"Formula: {minuend} - {subtrahend}")

        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend).zfill(len(minuend_str))

        working_digits = [int(d) for d in minuend_str]
        subtrahend_digits = [int(d) for d in subtrahend_str]

        for i in range(len(working_digits) - 1, -1, -1):
            top = working_digits[i]
            bottom = subtrahend_digits[i]
            col_num = len(working_digits) - i

            if top < bottom:
                if i > 0:
                    if working_digits[i - 1] == 0:
                        if self._is_left_ten_pattern(minuend_str, i - 1):
                            # Correct cascade
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
                            # Bug applied
                            working_digits[i - 1] = 9
                            top += 10
                    else:
                        working_digits[i - 1] -= 1
                        top += 10

            digit_result = top - bottom
            steps.append(f"Column {col_num}: {top} - {bottom} = {digit_result}")

        steps.append(f"Answer: {malrule_result}")
        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Left-Ten-OK malrule.

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
