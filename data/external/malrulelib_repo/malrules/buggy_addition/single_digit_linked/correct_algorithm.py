"""
Correct addition algorithm.

Implements the standard algorithm for multi-digit addition with carrying.
"""

import sys
sys.path.append('/Users/kitetsu/nlp_mac/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class AdditionCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for addition operations.
    """

    def get_name(self) -> str:
        return "Correct Addition Algorithm"

    def get_description(self) -> str:
        return (
            "The standard algorithm for addition. Numbers are aligned by place value "
            "(ones with ones, tens with tens, etc.) and added column by column from "
            "right to left. When a column sum exceeds 9, we carry 1 to the next "
            "column. This correctly combines the values represented by the digits."
        )

    def _generate_concise_steps_for_addition(self, num1: int, num2: int) -> List[str]:
        """
        Generate concise steps for a single addition operation.

        Args:
            num1: First operand
            num2: Second operand

        Returns:
            List of concise step strings
        """
        steps = []

        # Convert to digit lists (rightmost digit first for easier processing)
        num1_digits = [int(d) for d in str(num1)][::-1]
        num2_digits = [int(d) for d in str(num2)][::-1]

        # Pad shorter number with zeros
        max_len = max(len(num1_digits), len(num2_digits))
        while len(num1_digits) < max_len:
            num1_digits.append(0)
        while len(num2_digits) < max_len:
            num2_digits.append(0)

        place_names = ['ones', 'tens', 'hundreds', 'thousands']
        carry = 0

        # Process each column
        for i in range(max_len):
            top_digit = num1_digits[i]
            bottom_digit = num2_digits[i]
            place_name = place_names[i] if i < len(place_names) else f'10^{i}'

            column_sum = top_digit + bottom_digit + carry
            result_digit = column_sum % 10
            carry = column_sum // 10

            if carry > 0:
                steps.append(f"{place_name.capitalize()}: {top_digit} + {bottom_digit} = {column_sum}, write {result_digit}, carry {carry}")
            else:
                if i > 0 and num1_digits[i-1] + num2_digits[i-1] >= 10:
                    steps.append(f"{place_name.capitalize()}: {top_digit} + {bottom_digit} + 1 = {column_sum}, write {result_digit}")
                else:
                    steps.append(f"{place_name.capitalize()}: {top_digit} + {bottom_digit} = {result_digit}")

        if carry > 0:
            steps.append(f"Final carry: {carry}")

        return steps

    def _generate_verbose_steps_for_addition(self, num1: int, num2: int) -> List[str]:
        """
        Generate verbose steps for a single addition operation.

        Args:
            num1: First operand
            num2: Second operand

        Returns:
            List of verbose step strings
        """
        steps = []

        # Convert to digit lists (rightmost digit first for easier processing)
        num1_digits = [int(d) for d in str(num1)][::-1]
        num2_digits = [int(d) for d in str(num2)][::-1]

        # Pad shorter number with zeros
        max_len = max(len(num1_digits), len(num2_digits))
        while len(num1_digits) < max_len:
            num1_digits.append(0)
        while len(num2_digits) < max_len:
            num2_digits.append(0)

        place_names = ['ones', 'tens', 'hundreds', 'thousands']
        carry = 0

        # Process each column
        for i in range(max_len):
            top_digit = num1_digits[i]
            bottom_digit = num2_digits[i]
            place_name = place_names[i] if i < len(place_names) else f'10^{i}'

            column_sum = top_digit + bottom_digit + carry

            if carry > 0:
                steps.append(
                    f"{place_name.capitalize()} place: {top_digit} + {bottom_digit} + {carry} (carried) = {column_sum}"
                )
            else:
                steps.append(
                    f"{place_name.capitalize()} place: {top_digit} + {bottom_digit} = {column_sum}"
                )

            result_digit = column_sum % 10
            carry = column_sum // 10

            if carry > 0:
                steps.append(
                    f"  Write {result_digit}, carry {carry} to the next column"
                )
            else:
                steps.append(f"  Write {result_digit}")

        if carry > 0:
            steps.append(f"Write final carry: {carry}")

        return steps

    def _generate_concise_steps(self, problem: Problem, answer: int) -> List[str]:
        """
        Generate concise steps showing only formulas and values.

        Args:
            problem: The problem instance
            answer: The computed answer

        Returns:
            List of concise step strings
        """
        steps = []
        num1, num2 = problem.operands[:2]

        # Add question
        steps.append(f"Question: {problem.text}")

        # Add formula extraction for word problems
        template = problem.metadata.get('template', '')
        if 'word' in template.lower():
            steps.append(f"Formula: {num1} + {num2}")

        # Add column-by-column steps
        steps.extend(self._generate_concise_steps_for_addition(num1, num2))

        # Add answer
        steps.append(f"Answer: {answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, answer: int) -> List[str]:
        """
        Generate verbose steps with full explanations.

        Args:
            problem: The problem instance
            answer: The computed answer

        Returns:
            List of verbose step strings
        """
        steps = []
        num1, num2 = problem.operands[:2]

        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD: Standard Addition Algorithm")
        steps.append(f"Adding {num1} and {num2}")
        steps.append("")

        steps.extend(self._generate_verbose_steps_for_addition(num1, num2))

        steps.append("")
        steps.append(f"Final answer: {answer}")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct addition algorithm.

        Args:
            problem: Addition problem to solve
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with correct answer
        """
        # Calculate the correct answer
        num1, num2 = problem.operands[:2]
        answer = num1 + num2

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, answer)
        else:
            steps = self._generate_concise_steps(problem, answer)

        return Solution(
            answer=str(answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
