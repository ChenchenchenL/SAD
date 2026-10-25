"""
Correct algorithm for subtraction with proper borrowing.

Implements standard subtraction with correct ADD TEN procedure where
borrowing adds 10 to the existing digit (1 + 10 = 11, not just 10).
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class SubtractionCorrectAlgorithm(CorrectAlgorithm):
    """
    Implements correct subtraction with proper borrowing/regrouping.

    When borrowing, 10 is ADDED to the existing digit, so:
    - 1 + 10 = 11 (not 10)
    - 2 + 10 = 12
    - etc.
    """

    def get_name(self) -> str:
        return "Correct Subtraction with Borrowing"

    def get_description(self) -> str:
        return (
            "Correctly performs subtraction with proper borrowing (regrouping). "
            "When borrowing is needed, 10 is ADDED to the existing digit in that "
            "column. For example, if the digit is 1 and we borrow, we get "
            "1 + 10 = 11, not just 10. The column to the left is decremented by 1."
        )

    def _generate_verbose_steps(self, problem: Problem, minuend: int,
                                 subtrahend: int, result: int) -> List[str]:
        """Generate verbose steps with full explanations."""
        steps = []
        steps.append(f"Problem: {minuend} - {subtrahend}")
        steps.append("")
        steps.append("CORRECT METHOD:")
        steps.append("  When borrowing, ADD 10 to the existing digit")
        steps.append("")

        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend).zfill(len(minuend_str))

        minuend_digits = [int(d) for d in minuend_str]
        subtrahend_digits = [int(d) for d in subtrahend_str]

        working_minuend = minuend_digits.copy()

        steps.append("Working right to left with proper borrowing:")
        steps.append("")

        # Process right to left
        for i in range(len(working_minuend) - 1, -1, -1):
            top_digit = working_minuend[i]
            bottom_digit = subtrahend_digits[i]
            col_num = len(working_minuend) - i

            steps.append(f"Column {col_num}: {top_digit} - {bottom_digit}")

            if top_digit < bottom_digit:
                steps.append(f"  Need to borrow: {top_digit} < {bottom_digit}")

                if i > 0:
                    borrow_from = i - 1
                    cascade_positions = []

                    while borrow_from >= 0 and working_minuend[borrow_from] == 0:
                        cascade_positions.append(borrow_from)
                        borrow_from -= 1

                    if borrow_from >= 0:
                        working_minuend[borrow_from] -= 1
                        steps.append(f"  Borrow from column {len(working_minuend) - borrow_from}: "
                                   f"{working_minuend[borrow_from] + 1} becomes {working_minuend[borrow_from]}")

                        for pos in cascade_positions:
                            working_minuend[pos] = 9
                            steps.append(f"  Column {len(working_minuend) - pos}: 0 becomes 9")

                        # CORRECT: Add 10 to existing digit
                        original = top_digit
                        top_digit += 10
                        steps.append(f"  Add 10 to current digit: {original} + 10 = {top_digit}")
                        working_minuend[i] = top_digit

                digit_result = top_digit - bottom_digit
                steps.append(f"  Compute: {top_digit} - {bottom_digit} = {digit_result}")
            else:
                digit_result = top_digit - bottom_digit
                steps.append(f"  {top_digit} - {bottom_digit} = {digit_result}")

            steps.append("")

        steps.append(f"Final Answer: {result}")

        return steps

    def _generate_concise_steps(self, problem: Problem, minuend: int,
                                 subtrahend: int, result: int) -> List[str]:
        """Generate concise steps showing only formulas and values."""
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

        # Process right to left
        for i in range(len(working_minuend) - 1, -1, -1):
            top_digit = working_minuend[i]
            bottom_digit = subtrahend_digits[i]
            col_num = len(working_minuend) - i

            if top_digit < bottom_digit:
                if i > 0:
                    borrow_from = i - 1
                    while borrow_from >= 0 and working_minuend[borrow_from] == 0:
                        borrow_from -= 1

                    if borrow_from >= 0:
                        working_minuend[borrow_from] -= 1
                        for j in range(borrow_from + 1, i):
                            working_minuend[j] = 9

                        # CORRECT: Add 10
                        top_digit += 10
                        working_minuend[i] = top_digit

                digit_result = top_digit - bottom_digit
                steps.append(f"Column {col_num}: {top_digit} - {bottom_digit} = {digit_result}")
            else:
                digit_result = top_digit - bottom_digit
                steps.append(f"Column {col_num}: {top_digit} - {bottom_digit} = {digit_result}")

        steps.append(f"Answer: {result}")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Correctly solve subtraction with proper borrowing.

        Args:
            problem: Problem instance with minuend and subtrahend
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with correct answer and steps
        """
        minuend, subtrahend = problem.operands[:2]
        result = minuend - subtrahend

        if verbose:
            steps = self._generate_verbose_steps(problem, minuend, subtrahend, result)
        else:
            steps = self._generate_concise_steps(problem, minuend, subtrahend, result)

        return Solution(
            answer=str(result),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
