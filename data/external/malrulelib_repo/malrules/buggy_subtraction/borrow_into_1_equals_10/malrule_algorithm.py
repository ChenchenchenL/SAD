"""
Malrule algorithm for Borrow-Into-1-Equals-10 (BORROW/INTO/1=10).

From Brown & Burton (1978): When borrowing into a column whose top digit is 1,
the student gets 10 instead of 11. The student treats the borrowed 10 as a
replacement rather than an addition to the existing digit.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class BorrowInto1Equals10Malrule(Malrule):
    """
    Implements the BORROW/INTO/1=10 malrule from Brown & Burton (1978).

    When borrowing into a column whose ORIGINAL top digit is 1, the student
    gets 10 instead of 11. The malrule only applies when the digit was
    originally 1 in the problem, not when it became 1 due to prior borrows.

    Example: 321 - 89 = 231 (correct: 232)
    - Ones: ORIGINAL digit is 1, MALRULE: 10 - 9 = 1 (should be 11 - 9 = 2)
    - Tens: Original digit was 2 (not 1), NO malrule: 11 - 8 = 3
    - Hundreds: 3 - 1 = 2
    - Result: 231 (WRONG! Should be 232)

    Network location: ADD TEN procedure
    """

    def get_name(self) -> str:
        return "Borrow-Into-1-Equals-10"

    def get_description(self) -> str:
        return (
            "A systematic procedural bug where when borrowing into a column "
            "whose ORIGINAL top digit is 1, the student gets 10 instead of 11. "
            "The student treats the borrowed 10 as replacing the existing digit "
            "rather than adding to it. This bug occurs in the ADD TEN procedure "
            "of the subtraction algorithm and only applies to digits that were "
            "originally 1 in the problem.\n\n"
            "Example: 321 - 89 = 231 (correct: 232)\n"
            "- In the ones column, the ORIGINAL digit is 1\n"
            "- When borrowing into this column, 1 + 10 should = 11\n"
            "- Student incorrectly gets 10 (ignoring the existing 1)\n"
            "- 10 - 9 = 1 instead of 11 - 9 = 2"
        )

    def calculate_expected_answer(self, problem: Problem) -> int:
        """
        Calculate the expected incorrect answer for BORROW/INTO/1=10.

        When borrowing into a column whose ORIGINAL top digit is 1, the student
        gets 10 instead of 11. The malrule only applies to digits that were
        originally 1 in the problem, not digits that became 1 due to prior
        borrow decrements.

        Example: 321 - 89 = 231 (correct: 232)
        - Ones: ORIGINAL digit is 1, MALRULE applies: 10 - 9 = 1
        - Tens: Original digit was 2 (became 1 after decrement), NO malrule: 11 - 8 = 3
        - Hundreds: 2

        Args:
            problem: Subtraction problem

        Returns:
            Expected incorrect answer as integer
        """
        # Calculate from operands
        minuend, subtrahend = problem.operands[:2]

        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend).zfill(len(minuend_str))

        # Keep ORIGINAL digits for malrule check
        original_minuend_digits = [int(d) for d in minuend_str]
        subtrahend_digits = [int(d) for d in subtrahend_str]

        # Working copy that gets modified during computation
        working_minuend = original_minuend_digits.copy()
        result_digits = []

        # Process right to left
        for i in range(len(working_minuend) - 1, -1, -1):
            top_digit = working_minuend[i]
            bottom_digit = subtrahend_digits[i]

            if top_digit < bottom_digit:
                # Need to borrow
                if i > 0:
                    # Find column to borrow from
                    borrow_from = i - 1
                    while borrow_from >= 0 and working_minuend[borrow_from] == 0:
                        borrow_from -= 1

                    if borrow_from >= 0:
                        # Perform borrow
                        working_minuend[borrow_from] -= 1

                        # Handle cascade through zeros
                        for j in range(borrow_from + 1, i):
                            working_minuend[j] = 9

                        # MALRULE: Check ORIGINAL digit, not working digit
                        # If the ORIGINAL digit was 1, student gets 10 instead of 11
                        if original_minuend_digits[i] == 1:
                            top_digit = 10  # MALRULE: should be 11
                        else:
                            top_digit += 10  # Normal case

                        working_minuend[i] = top_digit

            digit_result = top_digit - bottom_digit
            result_digits.insert(0, digit_result)

        result_str = ''.join(str(d) for d in result_digits).lstrip('0') or '0'
        return int(result_str)

    def _generate_verbose_steps(self, problem: Problem, minuend: int,
                                 subtrahend: int, malrule_result: int) -> List[str]:
        """Generate verbose steps with full explanations."""
        steps = []
        steps.append(f"Problem: {minuend} - {subtrahend}")
        steps.append("")
        steps.append(f"MALRULE: {self.get_name()}")
        steps.append("  Student believes: 'When borrowing into a 1, I get 10'")
        steps.append("  (Only applies when ORIGINAL digit is 1)")
        steps.append("")

        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend).zfill(len(minuend_str))

        # Keep ORIGINAL digits for malrule check
        original_minuend_digits = [int(d) for d in minuend_str]
        subtrahend_digits = [int(d) for d in subtrahend_str]

        working_minuend = original_minuend_digits.copy()

        steps.append("Working right to left:")
        steps.append("")

        malrule_triggered = False

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

                        # MALRULE: Check ORIGINAL digit, not working digit
                        if original_minuend_digits[i] == 1:
                            steps.append(f"  MALRULE APPLIED: ORIGINAL digit is 1, student gets 10 (not 11)")
                            steps.append(f"  (WRONG! Should be 1 + 10 = 11)")
                            top_digit = 10
                            malrule_triggered = True
                        else:
                            steps.append(f"  Add 10: {top_digit} + 10 = {top_digit + 10}")
                            top_digit += 10

                        working_minuend[i] = top_digit

                digit_result = top_digit - bottom_digit
                steps.append(f"  Compute: {top_digit} - {bottom_digit} = {digit_result}")
            else:
                digit_result = top_digit - bottom_digit
                steps.append(f"  {top_digit} - {bottom_digit} = {digit_result}")

            steps.append("")

        if malrule_triggered:
            steps.append(f"Final Answer: {malrule_result} (INCORRECT - used 10 instead of 11)")
        else:
            steps.append(f"Final Answer: {malrule_result}")

        return steps

    def _generate_concise_steps(self, problem: Problem, minuend: int,
                                 subtrahend: int, malrule_result: int) -> List[str]:
        """Generate concise steps showing only formulas and values."""
        steps = []

        steps.append(f"Question: {problem.text}")

        template = problem.metadata.get('template', '')
        if template == 'word_problem' or 'word' in template.lower():
            steps.append(f"Formula: {minuend} - {subtrahend}")

        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend).zfill(len(minuend_str))

        # Keep ORIGINAL digits for malrule check
        original_minuend_digits = [int(d) for d in minuend_str]
        subtrahend_digits = [int(d) for d in subtrahend_str]

        working_minuend = original_minuend_digits.copy()

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

                        # MALRULE: Check ORIGINAL digit
                        if original_minuend_digits[i] == 1:
                            top_digit = 10  # MALRULE
                        else:
                            top_digit += 10
                        working_minuend[i] = top_digit

                digit_result = top_digit - bottom_digit
                steps.append(f"Column {col_num}: {top_digit} - {bottom_digit} = {digit_result}")
            else:
                digit_result = top_digit - bottom_digit
                steps.append(f"Column {col_num}: {top_digit} - {bottom_digit} = {digit_result}")

        steps.append(f"Answer: {malrule_result}")

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the BORROW/INTO/1=10 malrule.

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
