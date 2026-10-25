"""
Correct addition algorithm.

Implements the standard algorithm for multi-digit addition with carrying.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class AdditionCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for multi-digit addition with carrying.

    The standard addition algorithm processes each column from right to left,
    properly resetting the carry after each column is processed.
    """

    def get_name(self) -> str:
        return "Correct Addition Algorithm"

    def get_description(self) -> str:
        return (
            "The standard algorithm for multi-digit addition. When the sum of "
            "digits in a column exceeds 9, we write the ones digit and carry "
            "the tens digit to the next column. The carry is reset after being "
            "added to each column. This process continues from right to left "
            "across all columns."
        )

    def _generate_concise_steps_for_addition(self, num1: int, num2: int) -> List[str]:
        """
        Generate concise steps for a single addition operation.

        Args:
            num1: First addend
            num2: Second addend

        Returns:
            List of concise step strings
        """
        steps = []

        num1_digits = [int(d) for d in str(num1)][::-1]
        num2_digits = [int(d) for d in str(num2)][::-1]

        max_len = max(len(num1_digits), len(num2_digits))
        while len(num1_digits) < max_len:
            num1_digits.append(0)
        while len(num2_digits) < max_len:
            num2_digits.append(0)

        place_names = ['ones', 'tens', 'hundreds', 'thousands', 'ten-thousands']
        carry = 0

        for i in range(max_len):
            place_name = place_names[i] if i < len(place_names) else f'10^{i}'
            d1, d2 = num1_digits[i], num2_digits[i]
            column_sum = d1 + d2 + carry

            if carry > 0:
                steps.append(f"{place_name.capitalize()}: {d1} + {d2} + {carry} = {column_sum}")
            else:
                steps.append(f"{place_name.capitalize()}: {d1} + {d2} = {column_sum}")

            if column_sum >= 10:
                carry = column_sum // 10
            else:
                carry = 0

        return steps

    def _generate_verbose_steps_for_addition(self, num1: int, num2: int) -> List[str]:
        """
        Generate verbose steps for a single addition operation.

        Args:
            num1: First addend
            num2: Second addend

        Returns:
            List of verbose step strings
        """
        steps = []

        num1_digits = [int(d) for d in str(num1)][::-1]
        num2_digits = [int(d) for d in str(num2)][::-1]

        max_len = max(len(num1_digits), len(num2_digits))
        while len(num1_digits) < max_len:
            num1_digits.append(0)
        while len(num2_digits) < max_len:
            num2_digits.append(0)

        place_names = ['ones', 'tens', 'hundreds', 'thousands', 'ten-thousands']
        carry = 0

        for i in range(max_len):
            place_name = place_names[i] if i < len(place_names) else f'10^{i}'
            d1, d2 = num1_digits[i], num2_digits[i]
            column_sum = d1 + d2 + carry

            steps.append(f"{place_name.capitalize()} place:")
            if carry > 0:
                steps.append(f"  {d1} + {d2} + carry {carry} = {column_sum}")
            else:
                steps.append(f"  {d1} + {d2} = {column_sum}")

            if column_sum >= 10:
                steps.append(f"  Write {column_sum % 10}, carry {column_sum // 10} to next column")
                carry = column_sum // 10
            else:
                steps.append(f"  Write {column_sum}")
                carry = 0  # Reset carry

        if carry > 0:
            steps.append(f"Final carry: {carry}")

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

        steps.append(f"Adding {num1} + {num2}")
        steps.append("")

        # Add column-by-column steps
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
        # Get answer from metadata or calculate
        if 'correct_answer' in problem.metadata:
            answer = int(problem.metadata['correct_answer'])
        else:
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
