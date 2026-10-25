"""
Malrule algorithm for Diff-0-N=N error.

Students treat 0 - N as simply N, not understanding that subtraction
from zero requires borrowing.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class Diff0NEqualsNMalrule(Malrule):
    """
    Implements the Diff-0-N=N malrule.

    Students incorrectly handle 0 - N by simply writing N as the answer,
    not recognizing that they need to borrow from the left position.

    Example: 305 - 147
    Student sees tens column: 0 - 4, writes 4
    Gets 348 instead of 158 (WRONG!)
    """

    def get_name(self) -> str:
        return "Diff-0-N=N (Smaller-From-Larger Variant)"

    def get_description(self) -> str:
        return (
            "When the minuend digit is 0 and the subtrahend digit is N (where N > 0), "
            "the student writes N as the result instead of borrowing. This is a specific "
            "manifestation of the 'Smaller-From-Larger' bug documented in Brown & Burton's "
            "(1978) BUGGY system, where students subtract the smaller digit from the larger "
            "regardless of position. When encountering 0 - N, the student treats this as "
            "equivalent to N - 0 = N, avoiding the need to borrow."
        )

    def calculate_expected_answer(self, problem: Problem) -> int:
        """
        Calculate the expected incorrect answer for this malrule.

        For Diff-0-N=N:
        - When original minuend digit is 0 and subtrahend > 0:
          * MALRULE: Write subtrahend digit as result (0 - N = N)
        - Otherwise: Perform correct subtraction with proper borrowing

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
            # MALRULE: If ORIGINAL minuend digit is 0 and subtrahend digit is non-zero
            if minuend_digits[i] == 0 and subtrahend_digits[i] > 0:
                # Incorrectly just write the subtrahend digit
                digit_result = subtrahend_digits[i]
                result_digits.insert(0, digit_result)

            elif working_minuend[i] < subtrahend_digits[i]:
                # Need to borrow (do it correctly for non-zero positions)
                if i > 0:
                    # Cascade borrow through zeros
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

        for i in range(len(working_minuend) - 1, -1, -1):
            # MALRULE: If ORIGINAL minuend digit is 0 and subtrahend digit is non-zero
            if minuend_digits[i] == 0 and subtrahend_digits[i] > 0:
                digit_result = subtrahend_digits[i]
                result_digits.insert(0, digit_result)
                steps.append(f"0 - {subtrahend_digits[i]} = {digit_result}")

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
                steps.append(f"{working_minuend[i]} - {subtrahend_digits[i]} = {digit_result}")
            else:
                digit_result = working_minuend[i] - subtrahend_digits[i]
                result_digits.insert(0, digit_result)
                steps.append(f"{working_minuend[i]} - {subtrahend_digits[i]} = {digit_result}")

        steps.append(f"Answer: {result}")
        return steps

    def _generate_verbose_steps(self, problem: Problem, minuend: int, subtrahend: int,
                                 result: int, minuend_str: str, subtrahend_str: str,
                                 minuend_digits: List[int], subtrahend_digits: List[int]) -> List[str]:
        """Generate verbose steps with detailed explanations."""
        steps = []
        steps.append(f"Problem: {minuend} - {subtrahend}")
        steps.append("")
        steps.append("  " + minuend_str)
        steps.append("- " + subtrahend_str)
        steps.append("  " + "─" * len(minuend_str))

        # Perform subtraction with malrule
        result_digits = []
        working_minuend = minuend_digits[:]

        for i in range(len(working_minuend) - 1, -1, -1):
            # MALRULE: If ORIGINAL minuend digit is 0 and subtrahend digit is non-zero
            if minuend_digits[i] == 0 and subtrahend_digits[i] > 0:
                steps.append("")
                steps.append(f"Position {len(working_minuend) - i}: 0 - {subtrahend_digits[i]}")
                steps.append(f"MALRULE: 0 - {subtrahend_digits[i]} = {subtrahend_digits[i]}")
                steps.append(f"MALRULE REASONING: 'Zero minus something is just that number'")

                digit_result = subtrahend_digits[i]
                result_digits.insert(0, digit_result)

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
            else:
                digit_result = working_minuend[i] - subtrahend_digits[i]
                result_digits.insert(0, digit_result)

        steps.append("")
        steps.append(f"Result: {result} (INCORRECT)")
        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the diff-0-N=N malrule.

        Students write N when they see 0 - N.

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
