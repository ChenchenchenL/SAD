"""
Borrow-No-Decrement malrule algorithm.

Implements the systematic error where students borrow from the next column
but forget to decrement that column's digit.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List

class BorrowNoDecrementMalrule(Malrule):
    """
    Implements the Borrow-No-Decrement bug.

    Students correctly identify when borrowing is needed and correctly
    add 10 to the current digit, but they forget to reduce the borrowed-from
    digit by 1.
    """

    def get_name(self) -> str:
        return "Borrow-No-Decrement"

    def get_description(self) -> str:
        return (
            "When borrowing is required, students correctly add 10 to the current "
            "column's digit but forget to decrement the digit in the column they "
            "borrowed from. This is one of the most frequently documented subtraction "
            "bugs, first catalogued in Brown & Burton's (1978) BUGGY system and "
            "extensively analyzed in VanLehn's (1990) Mind Bugs. For example, in "
            "62 - 37, the student makes the ones column 12 - 7 = 5, but leaves the "
            "tens as 6 - 3 = 3, giving 35 instead of the correct answer 25."
        )

    def calculate_expected_answer(self, problem: Problem) -> int:
        """
        Calculate the expected incorrect answer for this malrule.

        For Borrow-No-Decrement:
        - When borrowing is needed: add 10 to current digit
        - MALRULE: DON'T decrement the borrowed-from digit
        - Continue subtraction normally

        Args:
            problem: Subtraction problem

        Returns:
            Expected incorrect answer as integer
        """
        minuend, subtrahend = problem.operands

        # Convert to digit lists (rightmost digit first for easier processing)
        minuend_digits = [int(d) for d in str(minuend)][::-1]
        subtrahend_digits = [int(d) for d in str(subtrahend)][::-1]

        # Pad subtrahend with zeros if needed
        while len(subtrahend_digits) < len(minuend_digits):
            subtrahend_digits.append(0)

        result_digits = []

        # Process each column
        for i in range(len(minuend_digits)):
            top_digit = minuend_digits[i]
            bottom_digit = subtrahend_digits[i]

            # Check if we need to borrow
            if top_digit < bottom_digit:
                # MALRULE: Borrow (add 10) but don't decrement the next column
                borrowed_top = top_digit + 10
                result_digits.append(borrowed_top - bottom_digit)
                # BUG: We don't do: minuend_digits[i+1] -= 1
            else:
                # No borrowing needed
                result_digits.append(top_digit - bottom_digit)

        # Convert result digits back to number
        # Remove leading zeros
        while len(result_digits) > 1 and result_digits[-1] == 0:
            result_digits.pop()

        return int(''.join(str(d) for d in result_digits[::-1]))

    def _generate_verbose_steps(self, minuend: int, subtrahend: int, answer: int) -> List[str]:
        """
        Generate verbose steps with detailed explanations for malrule.

        Args:
            minuend: The top number
            subtrahend: The bottom number
            answer: The computed incorrect result

        Returns:
            List of verbose step strings
        """
        steps = []
        steps.append(f"Subtracting {subtrahend} from {minuend}")

        minuend_digits = [int(d) for d in str(minuend)][::-1]
        subtrahend_digits = [int(d) for d in str(subtrahend)][::-1]

        while len(subtrahend_digits) < len(minuend_digits):
            subtrahend_digits.append(0)

        for i in range(len(minuend_digits)):
            top_digit = minuend_digits[i]
            bottom_digit = subtrahend_digits[i]

            place_name = ['ones', 'tens', 'hundreds', 'thousands'][i] if i < 4 else f'10^{i}'

            if top_digit < bottom_digit:
                borrowed_top = top_digit + 10
                steps.append(
                    f"{place_name.capitalize()} place: {top_digit} < {bottom_digit}, "
                    f"so borrow to make it {borrowed_top}"
                )
                steps.append(
                    f"{place_name.capitalize()} place: {borrowed_top} - {bottom_digit} = "
                    f"{borrowed_top - bottom_digit}"
                )
            else:
                result = top_digit - bottom_digit
                steps.append(
                    f"{place_name.capitalize()} place: {top_digit} - {bottom_digit} = {result}"
                )

        steps.append(f"Final answer: {answer} (INCORRECT due to Borrow-No-Decrement)")

        return steps

    def _generate_concise_steps(self, minuend: int, subtrahend: int, answer: int) -> List[str]:
        """
        Generate concise steps with only formulas and values for malrule.

        Args:
            minuend: The top number
            subtrahend: The bottom number
            answer: The computed incorrect result

        Returns:
            List of concise step strings
        """
        steps = []
        steps.append(f"{minuend} - {subtrahend}")

        minuend_digits = [int(d) for d in str(minuend)][::-1]
        subtrahend_digits = [int(d) for d in str(subtrahend)][::-1]

        while len(subtrahend_digits) < len(minuend_digits):
            subtrahend_digits.append(0)

        for i in range(len(minuend_digits)):
            top_digit = minuend_digits[i]
            bottom_digit = subtrahend_digits[i]

            if top_digit < bottom_digit:
                borrowed_top = top_digit + 10
                result = borrowed_top - bottom_digit
                steps.append(f"{borrowed_top} - {bottom_digit} = {result}")
            else:
                result = top_digit - bottom_digit
                steps.append(f"{top_digit} - {bottom_digit} = {result}")

        steps.append(f"{answer}")

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Borrow-No-Decrement malrule to solve the problem incorrectly.

        Args:
            problem: Subtraction problem to solve
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with incorrect answer due to Borrow-No-Decrement bug
        """
        minuend, subtrahend = problem.operands

        # Convert to digit lists (rightmost digit first for easier processing)
        minuend_digits = [int(d) for d in str(minuend)][::-1]
        subtrahend_digits = [int(d) for d in str(subtrahend)][::-1]

        # Pad subtrahend with zeros if needed
        while len(subtrahend_digits) < len(minuend_digits):
            subtrahend_digits.append(0)

        result_digits = []

        # Process each column
        for i in range(len(minuend_digits)):
            top_digit = minuend_digits[i]
            bottom_digit = subtrahend_digits[i]

            # Check if we need to borrow
            if top_digit < bottom_digit:
                # MALRULE: Borrow (add 10) but don't decrement the next column
                borrowed_top = top_digit + 10
                # BUG: We don't do: minuend_digits[i+1] -= 1
                result_digits.append(borrowed_top - bottom_digit)
            else:
                # No borrowing needed
                result = top_digit - bottom_digit
                result_digits.append(result)

        # Convert result digits back to number
        # Remove leading zeros
        while len(result_digits) > 1 and result_digits[-1] == 0:
            result_digits.pop()

        answer = int(''.join(str(d) for d in result_digits[::-1]))

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(minuend, subtrahend, answer)
        else:
            steps = self._generate_concise_steps(minuend, subtrahend, answer)

        return Solution(
            answer=str(answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
