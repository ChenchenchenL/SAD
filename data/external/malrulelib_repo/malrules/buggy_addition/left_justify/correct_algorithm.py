"""
Correct addition algorithm.

Implements the standard algorithm for multi-digit addition with carrying,
using proper right-alignment (place value alignment).
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class AdditionCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for multi-digit addition with proper place value alignment.

    Numbers are right-aligned (ones place aligned with ones place, tens with tens, etc.)
    and added column by column from right to left, carrying when necessary.
    """

    def get_name(self) -> str:
        return "Correct Addition Algorithm"

    def get_description(self) -> str:
        return (
            "The standard algorithm for multi-digit addition. Numbers are aligned "
            "on the right side (place value alignment), ensuring that ones are added "
            "to ones, tens to tens, etc. When the sum of a column exceeds 9, we "
            "write the ones digit and carry the tens digit to the next column."
        )

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct addition algorithm.

        Args:
            problem: Addition problem to solve
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with correct answer
        """
        num1, num2 = problem.operands[:2]

        # Check metadata first
        if 'correct_answer' in problem.metadata:
            answer = int(problem.metadata['correct_answer'])
        else:
            answer = num1 + num2

        if verbose:
            steps = self._generate_verbose_steps(num1, num2, answer)
        else:
            steps = self._generate_concise_steps(problem, num1, num2, answer)

        return Solution(
            answer=str(answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _generate_concise_steps(self, problem: Problem, num1: int, num2: int, answer: int) -> List[str]:
        """Generate concise steps showing only formulas and values."""
        steps = []
        steps.append(f"Question: {problem.text}")

        # Show alignment note if numbers have different lengths
        str1 = str(num1)
        str2 = str(num2)
        if len(str1) != len(str2):
            steps.append(f"Right-align by place value")

        # Pad shorter number with leading spaces for display
        max_len = max(len(str1), len(str2))
        display1 = str1.rjust(max_len)
        display2 = str2.rjust(max_len)

        # Add column by column (showing carry if needed)
        steps.append(f"Add: {num1} + {num2}")

        # Column-by-column breakdown
        str1_padded = str1.zfill(max_len)
        str2_padded = str2.zfill(max_len)

        place_names = ['ones', 'tens', 'hundreds', 'thousands', 'ten-thousands']
        carry = 0

        for i in range(max_len - 1, -1, -1):
            place_idx = max_len - 1 - i
            place_name = place_names[place_idx] if place_idx < len(place_names) else f"10^{place_idx}"

            d1 = int(str1_padded[i])
            d2 = int(str2_padded[i])
            col_sum = d1 + d2 + carry

            if carry > 0:
                steps.append(f"{place_name.capitalize()}: {d1} + {d2} + {carry} = {col_sum}")
            else:
                steps.append(f"{place_name.capitalize()}: {d1} + {d2} = {col_sum}")

            carry = col_sum // 10

        steps.append(f"Answer: {answer}")
        return steps

    def _generate_verbose_steps(self, num1: int, num2: int, answer: int) -> List[str]:
        """Generate verbose steps with full explanations."""
        steps = []
        steps.append(f"Adding {num1} and {num2}")
        steps.append("")
        steps.append("CORRECT METHOD: Right-align by place value")

        str1 = str(num1)
        str2 = str(num2)
        max_len = max(len(str1), len(str2))

        if len(str1) != len(str2):
            steps.append(f"  {num1} has {len(str1)} digit(s)")
            steps.append(f"  {num2} has {len(str2)} digit(s)")
            steps.append("  Align from the right (ones place with ones place)")
        steps.append("")

        # Show visual alignment
        display1 = str1.rjust(max_len + 2)
        display2 = str2.rjust(max_len + 2)
        steps.append(f"  {display1}")
        steps.append(f" +{display2}")
        steps.append("  " + "-" * (max_len + 1))
        steps.append("")

        # Column-by-column addition
        str1_padded = str1.zfill(max_len)
        str2_padded = str2.zfill(max_len)

        place_names = ['ones', 'tens', 'hundreds', 'thousands', 'ten-thousands']
        carry = 0

        steps.append("Step-by-step addition (right to left):")

        for i in range(max_len - 1, -1, -1):
            place_idx = max_len - 1 - i
            place_name = place_names[place_idx] if place_idx < len(place_names) else f"10^{place_idx}"

            d1 = int(str1_padded[i])
            d2 = int(str2_padded[i])
            col_sum = d1 + d2 + carry

            if carry > 0:
                steps.append(f"  {place_name.capitalize()} place: {d1} + {d2} + {carry} (carry) = {col_sum}")
            else:
                steps.append(f"  {place_name.capitalize()} place: {d1} + {d2} = {col_sum}")

            if col_sum >= 10:
                steps.append(f"    Write {col_sum % 10}, carry {col_sum // 10}")

            carry = col_sum // 10

        if carry > 0:
            steps.append(f"  Final carry: {carry}")

        steps.append("")
        steps.append(f"Final answer: {answer}")

        return steps
