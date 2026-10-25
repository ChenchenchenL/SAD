"""
Correct algorithm for subtraction with proper borrowing cascade.

This implements the standard subtraction algorithm that correctly
handles borrowing through zeros by cascading left until finding
a non-zero digit.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class SubtractionCorrectAlgorithm(CorrectAlgorithm):
    """
    Implements correct subtraction with proper borrowing cascade through zeros.

    When borrowing is needed and the next column contains zero:
    1. Continue cascading left until finding a non-zero digit
    2. Decrement that digit by 1
    3. Change all zeros passed through to 9
    4. Add 10 to the current column
    """

    def get_name(self) -> str:
        return "Correct Subtraction with Borrowing"

    def get_description(self) -> str:
        return (
            "Correctly performs subtraction with proper borrowing cascade "
            "through zero digits. When a borrow is needed from a column "
            "containing zero, the algorithm continues left until finding "
            "a non-zero digit, then cascades the borrow back through all "
            "intermediate zeros."
        )

    def _generate_verbose_steps(self, problem: Problem, minuend: int, subtrahend: int, result: int) -> List[str]:
        """Generate verbose steps with full explanations."""
        steps = []
        steps.append(f"Problem: {minuend} - {subtrahend}")
        steps.append("")

        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend).zfill(len(minuend_str))

        minuend_digits = [int(d) for d in minuend_str]
        subtrahend_digits = [int(d) for d in subtrahend_str]

        working_minuend = minuend_digits.copy()

        steps.append("Working right to left with proper borrowing:")
        steps.append("")

        for i in range(len(working_minuend) - 1, -1, -1):
            top_digit = working_minuend[i]
            bottom_digit = subtrahend_digits[i]

            steps.append(f"Column {len(working_minuend) - i}: {top_digit} - {bottom_digit}")

            if top_digit < bottom_digit:
                steps.append(f"  Need to borrow: {top_digit} < {bottom_digit}")

                borrow_from = i - 1
                cascade_positions = []

                while borrow_from >= 0 and working_minuend[borrow_from] == 0:
                    cascade_positions.append(borrow_from)
                    borrow_from -= 1

                if borrow_from >= 0:
                    if cascade_positions:
                        steps.append(f"  Cascading through zeros at positions: {[len(working_minuend) - p for p in cascade_positions]}")

                    working_minuend[borrow_from] -= 1
                    steps.append(f"  Borrow from position {len(working_minuend) - borrow_from}: {working_minuend[borrow_from] + 1} becomes {working_minuend[borrow_from]}")

                    for pos in cascade_positions:
                        working_minuend[pos] = 9
                        steps.append(f"  Position {len(working_minuend) - pos}: 0 becomes 9")

                    top_digit += 10
                    working_minuend[i] = top_digit

                    steps.append(f"  Current position: {top_digit - 10} becomes {top_digit}")
                    steps.append(f"  Now: {top_digit} - {bottom_digit} = {top_digit - bottom_digit}")

            else:
                steps.append(f"  {top_digit} - {bottom_digit} = {top_digit - bottom_digit}")

            steps.append("")

        steps.append(f"Final Answer: {result}")

        return steps

    def _generate_concise_steps(self, problem: Problem, minuend: int, subtrahend: int, result: int) -> List[str]:
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

        for i in range(len(working_minuend) - 1, -1, -1):
            top_digit = working_minuend[i]
            bottom_digit = subtrahend_digits[i]
            col_num = len(working_minuend) - i

            if top_digit < bottom_digit:
                borrow_from = i - 1
                cascade_positions = []

                while borrow_from >= 0 and working_minuend[borrow_from] == 0:
                    cascade_positions.append(borrow_from)
                    borrow_from -= 1

                if borrow_from >= 0:
                    working_minuend[borrow_from] -= 1
                    for pos in cascade_positions:
                        working_minuend[pos] = 9
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
        Correctly solve subtraction with proper borrowing cascade.

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
