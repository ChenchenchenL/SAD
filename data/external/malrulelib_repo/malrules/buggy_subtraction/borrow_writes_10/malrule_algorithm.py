"""
Malrule algorithm for Borrow-Writes-10 error.

When borrowing from a column where the top digit is 0, the student
borrows from the next column to the left correctly but writes 10
instead of 9 in this column.

Reference: Brown & Burton (1978). Diagnostic models for procedural bugs
in basic mathematical skills. Cognitive Science, 2(2), 155-192.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class BorrowWrites10Malrule(Malrule):
    """
    Implements the Borrow-Writes-10 malrule from Brown & Burton (1978).

    Bug description:
    When borrowing from a column where the top digit is 0, the student
    borrows from the next column to the left correctly but writes 10
    instead of 9 in this column.

    Example from the paper: 1300 - 522 = 788 (correct: 778)
      Ones column: 0 - 2, need to borrow
      Tens column has 0, so cascade to hundreds
      Hundreds: 3 becomes 2 (correct)
      Tens: 0 becomes 10 (BUG! should become 9)
      Ones: Gets +10, so 10 - 2 = 8
      Tens: 10 - 2 = 8 (BUG! should be 9 - 2 = 7)
      Hundreds: 2 - 5, need to borrow from thousands
      Thousands: 1 becomes 0
      Hundreds: 12 - 5 = 7
      Result: 788 (wrong, should be 778)

    Network location: ZERO procedure (writes 10 instead of 9)
    """

    def get_name(self) -> str:
        return "Borrow-Writes-10"

    def get_description(self) -> str:
        return (
            "A systematic procedural bug where, when borrowing from a column "
            "whose top digit is 0, the student correctly borrows from the next "
            "column to the left but writes 10 instead of 9 in the zero column. "
            "This represents a confusion about what happens to the intermediate "
            "zero column during cascade borrowing - the student treats it as "
            "receiving 10 (like the final column) rather than 9 (10 minus the 1 "
            "that continues rightward)."
        )

    def calculate_expected_answer(self, problem: Problem) -> Any:
        """
        Calculate the expected incorrect answer for this malrule.

        For Borrow-Writes-10:
        - When borrowing through a zero column
        - The zero becomes 10 (BUG) instead of 9 (correct)
        - This adds 1 to the result in that column

        Args:
            problem: Subtraction problem

        Returns:
            Expected incorrect answer as string
        """
        # Calculate from operands
        minuend, subtrahend = problem.operands[:2]

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

        # Handle any digits > 9 in result (shouldn't happen but be safe)
        final_result = []
        carry = 0
        for d in reversed(result_digits):
            d += carry
            carry = d // 10
            final_result.insert(0, d % 10)
        if carry > 0:
            final_result.insert(0, carry)

        result_str = ''.join(str(d) for d in final_result).lstrip('0') or '0'
        return str(int(result_str))

    def _generate_concise_steps(self, problem: Problem, minuend: int, subtrahend: int, malrule_result: int) -> List[str]:
        """
        Generate concise steps showing only formulas and values.

        Args:
            problem: The problem instance
            minuend: The number being subtracted from
            subtrahend: The number being subtracted
            malrule_result: The computed malrule result

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

        # Simplified column-by-column breakdown
        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend).zfill(len(minuend_str))

        minuend_digits = [int(d) for d in minuend_str]
        subtrahend_digits = [int(d) for d in subtrahend_str]

        working_minuend = minuend_digits.copy()

        # Process and show each column
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
                        working_minuend[pos] = 10  # MALRULE
                    top_digit += 10
                    working_minuend[i] = top_digit

            digit_result = working_minuend[i] - bottom_digit
            steps.append(f"Column {col_num}: {working_minuend[i]} - {bottom_digit} = {digit_result}")

        steps.append(f"Answer: {malrule_result}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, minuend: int, subtrahend: int, malrule_result: int) -> List[str]:
        """
        Generate verbose steps with full explanations.

        Args:
            problem: The problem instance
            minuend: The number being subtracted from
            subtrahend: The number being subtracted
            malrule_result: The computed malrule result

        Returns:
            List of verbose step strings
        """
        steps = []
        steps.append(f"Problem: {minuend} - {subtrahend}")
        steps.append("")

        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend).zfill(len(minuend_str))

        minuend_digits = [int(d) for d in minuend_str]
        subtrahend_digits = [int(d) for d in subtrahend_str]

        working_minuend = minuend_digits.copy()

        steps.append("Working right to left:")
        steps.append("")

        encountered_bug = False

        for i in range(len(working_minuend) - 1, -1, -1):
            top_digit = working_minuend[i]
            bottom_digit = subtrahend_digits[i]
            col_num = len(working_minuend) - i

            steps.append(f"Column {col_num}: {top_digit} - {bottom_digit}")

            if top_digit < bottom_digit:
                steps.append(f"  Need to borrow: {top_digit} < {bottom_digit}")

                borrow_from = i - 1
                cascade_positions = []

                while borrow_from >= 0 and working_minuend[borrow_from] == 0:
                    cascade_positions.append(borrow_from)
                    borrow_from -= 1

                if borrow_from >= 0:
                    if cascade_positions:
                        steps.append(f"  Found zero(s) to cascade through at column(s): {[len(working_minuend) - p for p in cascade_positions]}")
                        encountered_bug = True

                    steps.append(f"  Borrow from column {len(working_minuend) - borrow_from}: {working_minuend[borrow_from]} becomes {working_minuend[borrow_from] - 1}")
                    working_minuend[borrow_from] -= 1

                    for pos in cascade_positions:
                        steps.append(f"  MALRULE: Column {len(working_minuend) - pos}: 0 becomes 10 (should be 9!)")
                        working_minuend[pos] = 10

                    top_digit += 10
                    working_minuend[i] = top_digit
                    steps.append(f"  Current column: {top_digit - 10} becomes {top_digit}")

                digit_result = working_minuend[i] - bottom_digit
                steps.append(f"  {working_minuend[i]} - {bottom_digit} = {digit_result}")
            else:
                digit_result = top_digit - bottom_digit
                steps.append(f"  {top_digit} - {bottom_digit} = {digit_result}")

            steps.append("")

        if encountered_bug:
            steps.append(f"Final Answer: {malrule_result} (INCORRECT - wrote 10 instead of 9 in zero column)")
            steps.append("")
            steps.append("Error explanation:")
            steps.append("  When borrowing through zero, the zero should become 9, not 10")
            steps.append("  The zero receives 10 from the left but gives 1 to the right")
            steps.append("  10 - 1 = 9")
        else:
            steps.append(f"Final Answer: {malrule_result}")

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Borrow-Writes-10 malrule.

        Args:
            problem: Problem instance with minuend and subtrahend
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with incorrect answer and steps
        """
        minuend, subtrahend = problem.operands[:2]
        malrule_result = int(self.calculate_expected_answer(problem))

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
