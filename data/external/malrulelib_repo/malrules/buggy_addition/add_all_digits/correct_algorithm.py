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
    Correct algorithm for multi-digit addition with carrying/regrouping.
    """

    def get_name(self) -> str:
        return "Correct Addition Algorithm"

    def get_description(self) -> str:
        return (
            "The standard algorithm for multi-digit addition. Numbers are aligned "
            "by place value (ones under ones, tens under tens, etc.). Starting from "
            "the rightmost column (ones place), digits are added together. If the sum "
            "in any column is 10 or greater, we write the ones digit and carry the "
            "tens digit to the next column to the left. This process continues until "
            "all columns have been processed."
        )

    def _generate_concise_steps_for_addition(self, addend1: int, addend2: int) -> List[str]:
        """
        Generate concise steps for a single addition operation.

        Args:
            addend1: First addend
            addend2: Second addend

        Returns:
            List of concise step strings
        """
        steps = []

        # Convert to digit lists (rightmost digit first for easier processing)
        digits1 = [int(d) for d in str(addend1)][::-1]
        digits2 = [int(d) for d in str(addend2)][::-1]

        # Pad shorter number with zeros
        max_len = max(len(digits1), len(digits2))
        while len(digits1) < max_len:
            digits1.append(0)
        while len(digits2) < max_len:
            digits2.append(0)

        place_names = ['ones', 'tens', 'hundreds', 'thousands', 'ten-thousands']
        carry = 0

        # Process each column
        for i in range(max_len):
            d1 = digits1[i]
            d2 = digits2[i]
            place_name = place_names[i] if i < len(place_names) else f'10^{i}'

            column_sum = d1 + d2 + carry
            result_digit = column_sum % 10
            new_carry = column_sum // 10

            if carry > 0:
                steps.append(f"{place_name.capitalize()}: {d1} + {d2} + {carry} = {column_sum}")
            else:
                steps.append(f"{place_name.capitalize()}: {d1} + {d2} = {column_sum}")

            carry = new_carry

        if carry > 0:
            steps.append(f"Final carry: {carry}")

        return steps

    def _generate_verbose_steps_for_addition(self, addend1: int, addend2: int) -> List[str]:
        """
        Generate verbose steps for a single addition operation.

        Args:
            addend1: First addend
            addend2: Second addend

        Returns:
            List of verbose step strings
        """
        steps = []

        # Convert to digit lists (rightmost digit first for easier processing)
        digits1 = [int(d) for d in str(addend1)][::-1]
        digits2 = [int(d) for d in str(addend2)][::-1]

        # Pad shorter number with zeros
        max_len = max(len(digits1), len(digits2))
        while len(digits1) < max_len:
            digits1.append(0)
        while len(digits2) < max_len:
            digits2.append(0)

        place_names = ['ones', 'tens', 'hundreds', 'thousands', 'ten-thousands']
        carry = 0

        # Process each column
        for i in range(max_len):
            d1 = digits1[i]
            d2 = digits2[i]
            place_name = place_names[i] if i < len(place_names) else f'10^{i}'

            column_sum = d1 + d2 + carry

            if carry > 0:
                steps.append(
                    f"{place_name.capitalize()} place: {d1} + {d2} + {carry} (carry) = {column_sum}"
                )
            else:
                steps.append(f"{place_name.capitalize()} place: {d1} + {d2} = {column_sum}")

            if column_sum >= 10:
                result_digit = column_sum % 10
                new_carry = column_sum // 10
                steps.append(
                    f"  Write {result_digit}, carry {new_carry} to the next column"
                )
                carry = new_carry
            else:
                steps.append(f"  Write {column_sum}")
                carry = 0

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

        # Add question
        steps.append(f"Question: {problem.text}")

        addend1, addend2 = problem.operands[:2]
        steps.append(f"Formula: {addend1} + {addend2}")

        # Add column-by-column steps
        steps.extend(self._generate_concise_steps_for_addition(addend1, addend2))

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

        addend1, addend2 = problem.operands[:2]
        steps.append(f"Adding {addend1} and {addend2}")
        steps.append("")
        steps.append("CORRECT METHOD: Column-by-column addition with carrying")
        steps.append("")

        steps.extend(self._generate_verbose_steps_for_addition(addend1, addend2))

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
        addend1, addend2 = problem.operands[:2]
        answer = addend1 + addend2

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
