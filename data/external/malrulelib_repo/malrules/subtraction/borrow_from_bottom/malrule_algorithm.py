"""
Malrule algorithm for Borrow-From-Bottom error.

Students borrow from the bottom number (subtrahend) instead of the top number (minuend).
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class BorrowFromBottomMalrule(Malrule):
    """
    Students borrow from the bottom number instead of the top number.

    Example: 53 - 28 → Student borrows from bottom: 53 - 1(18) = 45 (wrong)
    The student adds 10 to the top ones digit but decrements the bottom tens digit.
    """

    def get_name(self) -> str:
        return "Borrow-From-Bottom"

    def get_description(self) -> str:
        return (
            "When borrowing is needed, students incorrectly decrement the subtrahend "
            "(bottom number) instead of the minuend (top number). They add 10 to the "
            "top digit correctly but reduce the wrong number's tens digit. This error, "
            "documented in Brown & Burton's (1978) BUGGY system, shows a fundamental "
            "misunderstanding of which number is being decomposed during regrouping."
        )

    def _compute_malrule_result(self, minuend: int, subtrahend: int) -> int:
        """
        Compute the incorrect answer by borrowing from bottom number.

        MALRULE: When borrowing is needed:
        - Add 10 to top digit (correct part)
        - But decrement BOTTOM number's next digit instead of top (wrong part)

        When the bottom number's next digit is 0, the student cascades the
        borrow within the bottom number (borrow-across-zero applied to bottom).
        If the cascade runs out of digits (no higher digit to borrow from),
        the student can't borrow and falls back to smaller-from-larger.

        Args:
            minuend: Top number (what we're subtracting from)
            subtrahend: Bottom number (what we're subtracting)

        Returns:
            Incorrect result from malrule
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
                # MALRULE: Try to borrow from BOTTOM number instead of top
                borrow_successful = False

                if i + 1 < len(sub_digits):
                    j = i + 1
                    # Track which digits we might set to 9 during cascade
                    zeros_to_cascade = []
                    while j < len(sub_digits) and sub_digits[j] == 0:
                        zeros_to_cascade.append(j)
                        j += 1

                    # Only cascade if we found a non-zero digit to borrow from
                    if j < len(sub_digits):
                        # Cascade successful: set intermediate zeros to 9
                        for k in zeros_to_cascade:
                            sub_digits[k] = 9
                        # Decrement the digit we borrowed from
                        sub_digits[j] -= 1
                        borrow_successful = True

                if borrow_successful:
                    # MALRULE: Add 10 to top digit (student does this)
                    top_digit += 10
                    result = top_digit - bottom_digit
                else:
                    # Cascade failed: no digit to borrow from in bottom number
                    # Student falls back to smaller-from-larger for this column
                    result = bottom_digit - top_digit
            else:
                # No borrowing needed
                result = top_digit - bottom_digit

            result_digits.append(result)

        # Remove leading zeros and convert to int
        while len(result_digits) > 1 and result_digits[-1] == 0:
            result_digits.pop()

        return int(''.join(str(d) for d in result_digits[::-1]))

    def calculate_expected_answer(self, problem: Problem) -> int:
        """
        Calculate the expected incorrect answer for this malrule.

        Parses operands from problem and computes result independently.
        """
        minuend, subtrahend = problem.operands[:2]
        return self._compute_malrule_result(minuend, subtrahend)

    def _generate_verbose_steps(self, minuend: int, subtrahend: int, malrule_answer: int) -> List[str]:
        """
        Generate verbose steps with detailed explanations for malrule.

        Args:
            minuend: The top number
            subtrahend: The bottom number
            malrule_answer: The computed incorrect result

        Returns:
            List of verbose step strings
        """
        min_str = str(minuend)
        sub_str = str(subtrahend).zfill(len(min_str))

        min_digits = [int(d) for d in min_str][::-1]
        sub_digits = [int(d) for d in sub_str][::-1]
        working_sub_digits = sub_digits.copy()

        column_names = ['Ones', 'Tens', 'Hundreds', 'Thousands', 'Ten-thousands']

        steps = []
        steps.append(f"Problem: {minuend} - {subtrahend}")
        steps.append("")
        steps.append("MALRULE: Borrow from BOTTOM number instead of top")
        steps.append("  Student reasoning: 'Need to borrow... change the bottom number'")
        steps.append("")

        for i in range(len(min_digits)):
            col_name = column_names[i] if i < len(column_names) else f"Column {i}"
            top = min_digits[i]
            bot = working_sub_digits[i]

            step_num = i + 1
            steps.append(f"Step {step_num}: {col_name} column - {top} - {bot}")

            if top < bot:
                steps.append(f"  {top} < {bot}, so need to borrow")
                steps.append(f"  MALRULE: Try to borrow from BOTTOM number!")

                borrow_successful = False
                if i + 1 < len(working_sub_digits):
                    j = i + 1
                    borrow_col = column_names[j] if j < len(column_names) else f"Column {j}"

                    zeros_found = []
                    temp_j = j
                    while temp_j < len(working_sub_digits) and working_sub_digits[temp_j] == 0:
                        zeros_found.append(temp_j)
                        temp_j += 1

                    if temp_j < len(working_sub_digits):
                        borrow_successful = True
                        if zeros_found:
                            steps.append(f"  Bottom {borrow_col} is 0, must cascade borrow")
                            for k in zeros_found:
                                working_sub_digits[k] = 9
                            cascade_col = column_names[temp_j] if temp_j < len(column_names) else f"Column {temp_j}"
                            steps.append(f"  Cascade: decrement bottom {cascade_col} {working_sub_digits[temp_j]} → {working_sub_digits[temp_j] - 1}")
                            working_sub_digits[temp_j] -= 1
                        else:
                            steps.append(f"  Decrement bottom {borrow_col}: {working_sub_digits[j]} → {working_sub_digits[j] - 1}")
                            working_sub_digits[j] -= 1

                if borrow_successful:
                    top += 10
                    result = top - bot
                    steps.append(f"  Add 10 to top {col_name}: {min_digits[i]} + 10 = {top}")
                    steps.append(f"  Subtract: {top} - {bot} = {result}")
                else:
                    steps.append(f"  Cannot borrow from bottom (no higher digit available)")
                    steps.append(f"  Fallback: smaller-from-larger")
                    result = bot - top
                    steps.append(f"  Subtract: {bot} - {top} = {result}")
            else:
                steps.append(f"  {top} >= {bot}, no borrow needed")
                result = top - bot
                steps.append(f"  Subtract: {top} - {bot} = {result}")

            steps.append("")

        steps.append(f"Final Answer: {malrule_answer} (INCORRECT - borrowed from bottom!)")

        return steps

    def _generate_concise_steps(self, minuend: int, subtrahend: int, malrule_answer: int) -> List[str]:
        """
        Generate concise steps with only formulas and values for malrule.

        Args:
            minuend: The top number
            subtrahend: The bottom number
            malrule_answer: The computed incorrect result

        Returns:
            List of concise step strings
        """
        min_str = str(minuend)
        sub_str = str(subtrahend).zfill(len(min_str))

        min_digits = [int(d) for d in min_str][::-1]
        sub_digits = [int(d) for d in sub_str][::-1]
        working_sub_digits = sub_digits.copy()

        steps = []
        steps.append(f"{minuend} - {subtrahend}")

        for i in range(len(min_digits)):
            top = min_digits[i]
            bot = working_sub_digits[i]

            if top < bot:
                borrow_successful = False
                if i + 1 < len(working_sub_digits):
                    j = i + 1
                    zeros_found = []
                    temp_j = j
                    while temp_j < len(working_sub_digits) and working_sub_digits[temp_j] == 0:
                        zeros_found.append(temp_j)
                        temp_j += 1

                    if temp_j < len(working_sub_digits):
                        borrow_successful = True
                        for k in zeros_found:
                            working_sub_digits[k] = 9
                        working_sub_digits[temp_j] -= 1

                if borrow_successful:
                    top += 10
                    result = top - bot
                else:
                    result = bot - top
            else:
                result = top - bot

            steps.append(f"{top} - {bot} = {result}")

        steps.append(f"{malrule_answer}")

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Borrow-From-Bottom malrule.

        Parses operands from problem and computes result independently.
        Shows detailed steps for any number of digits.

        Args:
            problem: Problem instance with minuend and subtrahend
            verbose: If True, generate verbose steps; if False, generate concise steps
        """
        minuend, subtrahend = problem.operands[:2]

        # Calculate malrule result independently
        malrule_answer = self._compute_malrule_result(minuend, subtrahend)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(minuend, subtrahend, malrule_answer)
        else:
            steps = self._generate_concise_steps(minuend, subtrahend, malrule_answer)

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
