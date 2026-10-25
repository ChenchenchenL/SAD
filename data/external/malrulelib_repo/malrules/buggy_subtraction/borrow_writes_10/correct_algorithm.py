"""
Correct algorithm for subtraction with proper borrowing cascade.

Reference: Brown & Burton (1978). Diagnostic models for procedural bugs
in basic mathematical skills. Cognitive Science, 2(2), 155-192.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class SubtractionCorrectAlgorithm(CorrectAlgorithm):
    """
    Implements correct subtraction with proper borrowing cascade through zeros.

    When borrowing through a zero column:
    1. Find the next non-zero digit to the left
    2. Decrement that digit by 1
    3. All intermediate zeros become 9 (not 10!)
    4. Add 10 to the column that needs to borrow

    Example: 1300 - 522 = 778
      Ones: 0 - 2, borrow needed, cascade through two zeros
      Thousands: 1 -> 0
      Hundreds: 0 -> 9
      Tens: 0 -> 9 (would be 10 in the malrule!)
      Ones: 0 -> 10
      Now: 0-0=0, 9-5=2 (with borrow from hundreds), 9-2=7, 10-2=8
      Wait, let me recalculate...

      Actually for 1300 - 522:
      Ones: 0 - 2, need borrow. Tens is 0, hundreds is 3.
      Borrow from hundreds: 3 -> 2
      Tens: 0 -> 9 (receives 10, gives 1 to ones)
      Ones: 0 -> 10
      Ones: 10 - 2 = 8
      Tens: 9 - 2 = 7
      Hundreds: 2 - 5, need borrow from thousands
      Thousands: 1 -> 0
      Hundreds: 2 -> 12
      Hundreds: 12 - 5 = 7
      Thousands: 0 - 0 = 0
      Result: 778
    """

    def get_name(self) -> str:
        return "Correct Subtraction with Borrowing"

    def get_description(self) -> str:
        return (
            "Correctly performs subtraction with proper borrowing cascade "
            "through zero digits. When borrowing through zeros, each zero "
            "becomes 9 (receiving 10 from left, giving 1 to right). Only "
            "the final column in the cascade receives the full +10."
        )

    def _generate_concise_steps(self, problem: Problem, minuend: int, subtrahend: int, result: int) -> List[str]:
        """
        Generate concise steps showing only formulas and values.

        Args:
            problem: The problem instance
            minuend: The number being subtracted from
            subtrahend: The number being subtracted
            result: The computed result

        Returns:
            List of concise step strings
        """
        steps = []

        # Add question
        steps.append(f"Question: {problem.text}")

        # Add formula extraction for word problems
        template = problem.metadata.get('template', '')
        if template == 'word_problem' or 'word' in template.lower():
            steps.append(f"Formula: {minuend} - {subtrahend}")

        # Convert to digit lists
        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend).zfill(len(minuend_str))

        minuend_digits = [int(d) for d in minuend_str]
        subtrahend_digits = [int(d) for d in subtrahend_str]

        # Create working copy
        working_minuend = minuend_digits.copy()

        # Process each digit right to left
        for i in range(len(working_minuend) - 1, -1, -1):
            top_digit = working_minuend[i]
            bottom_digit = subtrahend_digits[i]
            col_num = len(working_minuend) - i

            if top_digit < bottom_digit:
                # Find next non-zero digit to borrow from
                borrow_from = i - 1
                cascade_positions = []

                while borrow_from >= 0 and working_minuend[borrow_from] == 0:
                    cascade_positions.append(borrow_from)
                    borrow_from -= 1

                if borrow_from >= 0:
                    working_minuend[borrow_from] -= 1
                    for pos in cascade_positions:
                        working_minuend[pos] = 9  # Correct: 9, not 10
                    top_digit += 10
                    working_minuend[i] = top_digit

                digit_result = top_digit - bottom_digit
                steps.append(f"Column {col_num}: {top_digit} - {bottom_digit} = {digit_result}")
            else:
                digit_result = top_digit - bottom_digit
                steps.append(f"Column {col_num}: {top_digit} - {bottom_digit} = {digit_result}")

        # Add answer
        steps.append(f"Answer: {result}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, minuend: int, subtrahend: int, result: int) -> List[str]:
        """
        Generate verbose steps with full explanations.

        Args:
            problem: The problem instance
            minuend: The number being subtracted from
            subtrahend: The number being subtracted
            result: The computed result

        Returns:
            List of verbose step strings
        """
        steps = []
        steps.append(f"Problem: {minuend} - {subtrahend}")
        steps.append("")

        # Convert to digit lists
        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend).zfill(len(minuend_str))

        minuend_digits = [int(d) for d in minuend_str]
        subtrahend_digits = [int(d) for d in subtrahend_str]

        # Create working copy
        working_minuend = minuend_digits.copy()

        steps.append("Working right to left with proper borrowing:")
        steps.append("")

        # Process each digit right to left
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
                        steps.append(f"  Cascading through zeros at columns: {[len(working_minuend) - p for p in cascade_positions]}")

                    working_minuend[borrow_from] -= 1
                    steps.append(f"  Borrow from column {len(working_minuend) - borrow_from}: {working_minuend[borrow_from] + 1} becomes {working_minuend[borrow_from]}")

                    for pos in cascade_positions:
                        working_minuend[pos] = 9
                        steps.append(f"  Column {len(working_minuend) - pos}: 0 becomes 9 (receives 10, gives 1)")

                    top_digit += 10
                    working_minuend[i] = top_digit

                    steps.append(f"  Current column: {top_digit - 10} becomes {top_digit}")
                    steps.append(f"  Now: {top_digit} - {bottom_digit} = {top_digit - bottom_digit}")

            else:
                steps.append(f"  {top_digit} - {bottom_digit} = {top_digit - bottom_digit}")

            steps.append("")

        steps.append(f"Final Answer: {result}")

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
        # Extract operands from problem
        minuend, subtrahend = problem.operands[:2]

        # Calculate correct answer
        result = minuend - subtrahend

        # Generate steps based on verbose flag
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
