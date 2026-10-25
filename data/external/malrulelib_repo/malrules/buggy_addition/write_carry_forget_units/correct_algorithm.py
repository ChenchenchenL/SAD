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
            "The standard algorithm for multi-digit addition. When the sum of "
            "digits in a column is 10 or more, we write the units digit in the "
            "answer and carry the tens digit to the next column. This process "
            "is repeated across all columns from right to left."
        )

    def _generate_concise_steps_for_addition(self, addend1: int, addend2: int) -> List[str]:
        """
        Generate concise steps for a single addition operation.

        Args:
            addend1: First number
            addend2: Second number

        Returns:
            List of concise step strings
        """
        steps = []

        # Pad to same length
        max_len = max(len(str(addend1)), len(str(addend2)))
        addend1_digits = [int(d) for d in str(addend1).zfill(max_len)][::-1]
        addend2_digits = [int(d) for d in str(addend2).zfill(max_len)][::-1]

        place_names = ['ones', 'tens', 'hundreds', 'thousands', 'ten-thousands']
        carry = 0

        for i in range(max_len):
            d1 = addend1_digits[i]
            d2 = addend2_digits[i]
            column_sum = d1 + d2 + carry
            place_name = place_names[i] if i < len(place_names) else f'10^{i}'

            if carry > 0:
                steps.append(f"{place_name.capitalize()}: {d1} + {d2} + {carry} = {column_sum}")
            else:
                steps.append(f"{place_name.capitalize()}: {d1} + {d2} = {column_sum}")

            if column_sum >= 10:
                steps.append(f"  -> Write {column_sum % 10}, carry {column_sum // 10}")
                carry = column_sum // 10
            else:
                carry = 0

        if carry > 0:
            steps.append(f"Final carry: {carry}")

        return steps

    def _generate_verbose_steps_for_addition(self, addend1: int, addend2: int) -> List[str]:
        """
        Generate verbose steps for a single addition operation.

        Args:
            addend1: First number
            addend2: Second number

        Returns:
            List of verbose step strings
        """
        steps = []

        # Pad to same length
        max_len = max(len(str(addend1)), len(str(addend2)))
        addend1_digits = [int(d) for d in str(addend1).zfill(max_len)][::-1]
        addend2_digits = [int(d) for d in str(addend2).zfill(max_len)][::-1]

        place_names = ['ones', 'tens', 'hundreds', 'thousands', 'ten-thousands']
        next_place_names = ['tens', 'hundreds', 'thousands', 'ten-thousands', 'hundred-thousands']
        carry = 0

        for i in range(max_len):
            d1 = addend1_digits[i]
            d2 = addend2_digits[i]
            column_sum = d1 + d2 + carry
            place_name = place_names[i] if i < len(place_names) else f'10^{i}'

            if carry > 0:
                steps.append(
                    f"{place_name.capitalize()} place: {d1} + {d2} + {carry} (carry) = {column_sum}"
                )
            else:
                steps.append(
                    f"{place_name.capitalize()} place: {d1} + {d2} = {column_sum}"
                )

            if column_sum >= 10:
                next_place = next_place_names[i] if i < len(next_place_names) else f'10^{i+1}'
                steps.append(
                    f"Write {column_sum % 10} in {place_name} place, carry {column_sum // 10} to {next_place}"
                )
                carry = column_sum // 10
            else:
                steps.append(f"Write {column_sum} in {place_name} place")
                carry = 0

        if carry > 0:
            steps.append(f"Write final carry {carry}")

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
        addend1, addend2 = problem.operands[:2]

        # Add question
        steps.append(f"Question: {problem.text}")

        # Add formula extraction for word problems
        template = problem.metadata.get('template', '')
        if 'word' in template.lower():
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

        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD:")
        steps.append(f"Adding {addend1} + {addend2}")
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
        # Calculate the correct answer from operands
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
