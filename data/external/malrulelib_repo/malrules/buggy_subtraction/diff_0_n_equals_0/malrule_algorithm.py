"""
Malrule algorithm for Diff-0-N=0 error.

When the top digit in a column is 0 and the bottom digit is N (N > 0),
students write 0 as the result instead of borrowing from the next column.

Research: Brown & Burton (1978) - Diagnostic models for procedural bugs
in basic mathematical skills. Cognitive Science, 2(2), 155-192.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class Diff0NEquals0Malrule(Malrule):
    """
    Implements the Diff-0-N=0 malrule from Brown & Burton (1978).

    When the top digit in a column is 0 and the bottom digit is non-zero,
    the student writes 0 as the result (0-N=0) instead of borrowing.

    Example from the paper: 140 - 21 = 120 (correct: 119)
        - Ones: 0-1, student writes 0 (MALRULE!)
        - Tens: 4-2=2
        - Hundreds: 1-0=1
        - Result: 120 (INCORRECT)

    This is DIFFERENT from the related DIFF/0-N=N malrule where students
    write N instead of 0.
    """

    def get_name(self) -> str:
        return "DIFF/0-N=0"

    def get_description(self) -> str:
        return (
            "Whenever the top digit in a column is 0, the student writes 0 in the answer; "
            "i.e., 0-N=0. This bug occurs in the COMPLETE COLUMN procedure when students "
            "see a 0 in the minuend and simply write 0 without considering that borrowing "
            "is required. This is documented in Brown & Burton's (1978) BUGGY system. "
            "Example: 140 - 21 = 120 (correct: 119)"
        )

    def calculate_expected_answer(self, problem: Problem) -> int:
        """
        Calculate the expected incorrect answer for this malrule.

        For Diff-0-N=0:
        - When the top digit is 0 and the bottom digit is N (N > 0),
          the student writes 0 instead of borrowing and computing correctly.

        Args:
            problem: Subtraction problem

        Returns:
            Expected incorrect answer as integer
        """
        # Extract operands from problem
        minuend, subtrahend = problem.operands[:2]

        # Convert to digit arrays
        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend).zfill(len(minuend_str))

        minuend_digits = [int(d) for d in minuend_str]
        subtrahend_digits = [int(d) for d in subtrahend_str]

        # Perform subtraction with malrule
        result_digits = []
        working_minuend = minuend_digits[:]

        for i in range(len(working_minuend) - 1, -1, -1):
            # MALRULE: If top digit is 0 and bottom digit is non-zero, write 0
            if minuend_digits[i] == 0 and subtrahend_digits[i] > 0:
                # Bug: write 0 instead of borrowing
                result_digits.insert(0, 0)

            elif working_minuend[i] < subtrahend_digits[i]:
                # Need to borrow (do it correctly for non-zero positions)
                if i > 0:
                    borrow_from = i - 1
                    while borrow_from >= 0 and working_minuend[borrow_from] == 0:
                        working_minuend[borrow_from] = 9
                        borrow_from -= 1

                    if borrow_from >= 0:
                        working_minuend[borrow_from] -= 1
                        working_minuend[i] += 10

                digit_result = working_minuend[i] - subtrahend_digits[i]
                result_digits.insert(0, digit_result)

            else:
                # Can subtract normally
                digit_result = working_minuend[i] - subtrahend_digits[i]
                result_digits.insert(0, digit_result)

        return int(''.join(map(str, result_digits)))

    def _generate_concise_steps(self, problem: Problem, minuend: int, subtrahend: int,
                                 result: int, minuend_str: str, subtrahend_str: str,
                                 minuend_digits: List[int], subtrahend_digits: List[int]) -> List[str]:
        """Generate concise steps with only formulas and values."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: {minuend} - {subtrahend}")

        # Perform subtraction with malrule
        result_digits = []
        working_minuend = minuend_digits[:]

        place_names = ['ones', 'tens', 'hundreds', 'thousands', 'ten-thousands']

        for i in range(len(working_minuend) - 1, -1, -1):
            place_idx = len(working_minuend) - 1 - i
            place_name = place_names[place_idx] if place_idx < len(place_names) else f'10^{place_idx}'

            # MALRULE: If top digit is 0 and bottom digit is non-zero, write 0
            if minuend_digits[i] == 0 and subtrahend_digits[i] > 0:
                digit_result = 0
                result_digits.insert(0, digit_result)
                steps.append(f"{place_name.capitalize()}: 0 - {subtrahend_digits[i]} = 0 (MALRULE)")

            elif working_minuend[i] < subtrahend_digits[i]:
                if i > 0:
                    borrow_from = i - 1
                    while borrow_from >= 0 and working_minuend[borrow_from] == 0:
                        working_minuend[borrow_from] = 9
                        borrow_from -= 1

                    if borrow_from >= 0:
                        working_minuend[borrow_from] -= 1
                        working_minuend[i] += 10

                digit_result = working_minuend[i] - subtrahend_digits[i]
                result_digits.insert(0, digit_result)
                steps.append(f"{place_name.capitalize()}: {working_minuend[i]} - {subtrahend_digits[i]} = {digit_result}")
            else:
                digit_result = working_minuend[i] - subtrahend_digits[i]
                result_digits.insert(0, digit_result)
                steps.append(f"{place_name.capitalize()}: {working_minuend[i]} - {subtrahend_digits[i]} = {digit_result}")

        steps.append(f"Answer: {result} (INCORRECT)")
        return steps

    def _generate_verbose_steps(self, problem: Problem, minuend: int, subtrahend: int,
                                 result: int, minuend_str: str, subtrahend_str: str,
                                 minuend_digits: List[int], subtrahend_digits: List[int]) -> List[str]:
        """Generate verbose steps with detailed explanations."""
        steps = []
        steps.append(f"Problem: {minuend} - {subtrahend}")
        steps.append("")
        steps.append(f"MALRULE: {self.get_name()}")
        steps.append("  Student believes: 'When the top digit is 0, the answer is 0'")
        steps.append("")
        steps.append("  " + minuend_str)
        steps.append("- " + subtrahend_str)
        steps.append("  " + "-" * len(minuend_str))

        # Perform subtraction with malrule
        result_digits = []
        working_minuend = minuend_digits[:]

        place_names = ['ones', 'tens', 'hundreds', 'thousands', 'ten-thousands']

        for i in range(len(working_minuend) - 1, -1, -1):
            place_idx = len(working_minuend) - 1 - i
            place_name = place_names[place_idx] if place_idx < len(place_names) else f'10^{place_idx}'

            # MALRULE: If top digit is 0 and bottom digit is non-zero, write 0
            if minuend_digits[i] == 0 and subtrahend_digits[i] > 0:
                steps.append("")
                steps.append(f"{place_name.capitalize()} place: 0 - {subtrahend_digits[i]}")
                steps.append(f"  MALRULE APPLIED: 0 - {subtrahend_digits[i]} = 0")
                steps.append(f"  Student reasoning: 'Zero minus anything is zero'")

                digit_result = 0
                result_digits.insert(0, digit_result)

            elif working_minuend[i] < subtrahend_digits[i]:
                steps.append("")
                steps.append(f"{place_name.capitalize()} place: {working_minuend[i]} - {subtrahend_digits[i]}")
                steps.append(f"  {working_minuend[i]} < {subtrahend_digits[i]}, need to borrow")

                if i > 0:
                    borrow_from = i - 1
                    while borrow_from >= 0 and working_minuend[borrow_from] == 0:
                        working_minuend[borrow_from] = 9
                        borrow_from -= 1

                    if borrow_from >= 0:
                        working_minuend[borrow_from] -= 1
                        working_minuend[i] += 10
                        steps.append(f"  After borrowing: {working_minuend[i]} - {subtrahend_digits[i]}")

                digit_result = working_minuend[i] - subtrahend_digits[i]
                result_digits.insert(0, digit_result)
                steps.append(f"  = {digit_result}")

            else:
                digit_result = working_minuend[i] - subtrahend_digits[i]
                result_digits.insert(0, digit_result)

        steps.append("")
        steps.append(f"Result: {result} (INCORRECT)")
        steps.append(f"Correct answer would be: {minuend - subtrahend}")
        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the DIFF/0-N=0 malrule.

        When top digit is 0 and bottom digit is N > 0, student writes 0.

        Args:
            problem: Problem instance with minuend and subtrahend
            verbose: If True, generate detailed steps; if False, generate concise steps

        Returns:
            Solution with incorrect answer and student's reasoning
        """
        # Extract operands from problem
        minuend, subtrahend = problem.operands[:2]

        # Convert to digit arrays
        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend).zfill(len(minuend_str))

        minuend_digits = [int(d) for d in minuend_str]
        subtrahend_digits = [int(d) for d in subtrahend_str]

        # Calculate the malrule result
        result = self.calculate_expected_answer(problem)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, minuend, subtrahend, int(result),
                                                  minuend_str, subtrahend_str,
                                                  minuend_digits, subtrahend_digits)
        else:
            steps = self._generate_concise_steps(problem, minuend, subtrahend, int(result),
                                                  minuend_str, subtrahend_str,
                                                  minuend_digits, subtrahend_digits)

        return Solution(
            answer=str(result),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
