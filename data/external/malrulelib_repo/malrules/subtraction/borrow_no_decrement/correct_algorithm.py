"""
Correct subtraction algorithm.

Implements the standard algorithm for multi-digit subtraction with borrowing.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class SubtractionCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for multi-digit subtraction with borrowing/regrouping.
    """

    def get_name(self) -> str:
        return "Correct Subtraction Algorithm"

    def get_description(self) -> str:
        return (
            "The standard algorithm for multi-digit subtraction. When a digit "
            "in the subtrahend is larger than the corresponding digit in the "
            "minuend, we borrow 1 from the next column to the left (decrementing "
            "that digit) and add 10 to the current column. This process is "
            "repeated as needed across all columns."
        )

    def _generate_verbose_steps(self, minuend: int, subtrahend: int, answer: int) -> List[str]:
        """
        Generate verbose steps with detailed explanations.

        Args:
            minuend: The top number
            subtrahend: The bottom number
            answer: The computed result

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
                    f"so borrow from the next column"
                )

                if i + 1 < len(minuend_digits):
                    minuend_digits[i + 1] -= 1
                    steps.append(
                        f"Borrowed from {['tens', 'hundreds', 'thousands', 'ten-thousands'][i] if i < 4 else f'10^{i+1}'} "
                        f"place, reducing it by 1"
                    )

                result = borrowed_top - bottom_digit
                steps.append(
                    f"{place_name.capitalize()} place: {borrowed_top} - {bottom_digit} = {result}"
                )
            else:
                result = top_digit - bottom_digit
                steps.append(
                    f"{place_name.capitalize()} place: {top_digit} - {bottom_digit} = {result}"
                )

        steps.append(f"Final answer: {answer}")

        return steps

    def _generate_concise_steps(self, minuend: int, subtrahend: int, answer: int) -> List[str]:
        """
        Generate concise steps with only formulas and values.

        Args:
            minuend: The top number
            subtrahend: The bottom number
            answer: The computed result

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
                if i + 1 < len(minuend_digits):
                    minuend_digits[i + 1] -= 1
                result = borrowed_top - bottom_digit
                steps.append(f"{borrowed_top} - {bottom_digit} = {result}")
            else:
                result = top_digit - bottom_digit
                steps.append(f"{top_digit} - {bottom_digit} = {result}")

        steps.append(f"{answer}")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct subtraction algorithm.

        Args:
            problem: Subtraction problem to solve
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with correct answer
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
                # Need to borrow from next column
                borrowed_top = top_digit + 10

                # CORRECT: Decrement the next column
                if i + 1 < len(minuend_digits):
                    minuend_digits[i + 1] -= 1

                result = borrowed_top - bottom_digit
                result_digits.append(result)
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
            is_correct=True,
            algorithm_name=self.get_name()
        )
