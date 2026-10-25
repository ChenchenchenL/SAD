"""
Correct algorithm for subtraction.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class SubtractionCorrectAlgorithm(CorrectAlgorithm):
    """Correctly performs subtraction with borrowing only when needed."""

    def get_name(self) -> str:
        return "Correct Subtraction"

    def get_description(self) -> str:
        return "Correctly performs subtraction, borrowing only when top digit < bottom digit."

    def _compute_correct_result(self, minuend: int, subtrahend: int) -> int:
        """
        Compute correct subtraction result using digit-by-digit algorithm.

        This method computes the result using proper borrowing from the
        minuend (top number) when needed, without using any pre-computed answer.

        Args:
            minuend: Top number (what we're subtracting from)
            subtrahend: Bottom number (what we're subtracting)

        Returns:
            Correct result of minuend - subtrahend
        """
        # Convert to digit lists (reversed for easier right-to-left processing)
        min_str = str(minuend)
        sub_str = str(subtrahend).zfill(len(min_str))

        min_digits = [int(d) for d in min_str][::-1]
        sub_digits = [int(d) for d in sub_str][::-1]

        result_digits = []

        # Process each column from right to left
        for i in range(len(min_digits)):
            top_digit = min_digits[i]
            bottom_digit = sub_digits[i]

            # Check if borrowing is needed
            if top_digit < bottom_digit:
                # CORRECT: Borrow from TOP number's next column
                # Add 10 to current top digit
                top_digit += 10
                # Decrement the next column in the TOP number
                # Handle borrow across zero: cascade if next digit is 0
                j = i + 1
                while j < len(min_digits) and min_digits[j] == 0:
                    min_digits[j] = 9
                    j += 1
                if j < len(min_digits):
                    min_digits[j] -= 1

            result = top_digit - bottom_digit
            result_digits.append(result)

        # Remove leading zeros and convert to int
        while len(result_digits) > 1 and result_digits[-1] == 0:
            result_digits.pop()

        return int(''.join(str(d) for d in result_digits[::-1]))

    def _generate_verbose_steps(self, minuend: int, subtrahend: int, computed_answer: int) -> List[str]:
        """
        Generate verbose steps with detailed explanations.

        Args:
            minuend: The top number
            subtrahend: The bottom number
            computed_answer: The computed result

        Returns:
            List of verbose step strings
        """
        steps = []
        steps.append(f"Problem: {minuend} - {subtrahend}")
        steps.append("")
        steps.append("Rule: Only borrow when top digit < bottom digit")
        steps.append("      Borrow FROM the top number (minuend)")
        steps.append("")

        min_str = str(minuend)
        sub_str = str(subtrahend).zfill(len(min_str))

        min_digits = [int(d) for d in min_str][::-1]
        sub_digits = [int(d) for d in sub_str][::-1]
        working_min_digits = min_digits.copy()

        column_names = ['Ones', 'Tens', 'Hundreds', 'Thousands', 'Ten-thousands']

        for i in range(len(min_digits)):
            col_name = column_names[i] if i < len(column_names) else f"Column {i}"
            top = working_min_digits[i]
            bot = sub_digits[i]

            steps.append(f"{col_name} place: {top} - {bot}")

            if top < bot:
                steps.append(f"  {top} < {bot}, so NEED to borrow from top")

                j = i + 1
                borrow_from_col = column_names[j] if j < len(column_names) else f"Column {j}"

                if j < len(working_min_digits):
                    if working_min_digits[j] == 0:
                        steps.append(f"  {borrow_from_col} is 0, must borrow across zero")
                        k = j
                        while k < len(working_min_digits) and working_min_digits[k] == 0:
                            working_min_digits[k] = 9
                            k += 1
                        if k < len(working_min_digits):
                            working_min_digits[k] -= 1
                    else:
                        steps.append(f"  Borrow: {borrow_from_col} {working_min_digits[j]} → {working_min_digits[j] - 1}, {col_name} {top} → {top + 10}")
                        working_min_digits[j] -= 1

                top += 10
                result = top - bot
                steps.append(f"  Subtract: {top} - {bot} = {result}")
            else:
                steps.append(f"  {top} >= {bot}, NO need to borrow")
                result = top - bot
                steps.append(f"  Subtract: {top} - {bot} = {result}")

            steps.append("")

        steps.append(f"Final Answer: {computed_answer} ✓")

        return steps

    def _generate_concise_steps(self, minuend: int, subtrahend: int, computed_answer: int) -> List[str]:
        """
        Generate concise steps with only formulas and values.

        Args:
            minuend: The top number
            subtrahend: The bottom number
            computed_answer: The computed result

        Returns:
            List of concise step strings
        """
        steps = []
        steps.append(f"{minuend} - {subtrahend}")

        min_str = str(minuend)
        sub_str = str(subtrahend).zfill(len(min_str))

        min_digits = [int(d) for d in min_str][::-1]
        sub_digits = [int(d) for d in sub_str][::-1]
        working_min_digits = min_digits.copy()

        for i in range(len(min_digits)):
            top = working_min_digits[i]
            bot = sub_digits[i]

            if top < bot:
                j = i + 1
                if j < len(working_min_digits):
                    if working_min_digits[j] == 0:
                        k = j
                        while k < len(working_min_digits) and working_min_digits[k] == 0:
                            working_min_digits[k] = 9
                            k += 1
                        if k < len(working_min_digits):
                            working_min_digits[k] -= 1
                    else:
                        working_min_digits[j] -= 1

                top += 10

            result = top - bot
            steps.append(f"{top} - {bot} = {result}")

        steps.append(f"{computed_answer}")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the correct subtraction algorithm.

        Computes the result using logic only, without relying on metadata.

        Args:
            problem: Problem instance with minuend and subtrahend
            verbose: If True, generate verbose steps; if False, generate concise steps
        """
        # Extract operands from problem
        operands = problem.operands
        minuend, subtrahend = operands[:2]

        # Multi-step items carry three operands; apply every subtraction in order.
        if len(operands) >= 3:
            computed_answer = operands[0]
            for value in operands[1:]:
                computed_answer -= value
        else:
            # Compute the answer using our algorithm - NO metadata usage
            computed_answer = self._compute_correct_result(minuend, subtrahend)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(minuend, subtrahend, computed_answer)
        else:
            steps = self._generate_concise_steps(minuend, subtrahend, computed_answer)

        return Solution(
            answer=computed_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
