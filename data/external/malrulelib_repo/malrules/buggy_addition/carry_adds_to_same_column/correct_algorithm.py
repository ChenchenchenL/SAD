"""
Correct addition algorithm.

Implements the standard algorithm for multi-digit addition with carrying.
"""

import sys
sys.path.append('/home/user/malrule-coding')

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
            "The standard algorithm for multi-digit addition. When a column sum "
            "exceeds 9, we write the units digit in that column and carry the tens "
            "digit to the next column to the left. This process is repeated as "
            "needed across all columns, ensuring proper place value handling."
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

        # Convert to digit lists (rightmost digit first for easier processing)
        addend1_digits = [int(d) for d in str(addend1)][::-1]
        addend2_digits = [int(d) for d in str(addend2)][::-1]

        # Pad to same length
        max_len = max(len(addend1_digits), len(addend2_digits))
        while len(addend1_digits) < max_len:
            addend1_digits.append(0)
        while len(addend2_digits) < max_len:
            addend2_digits.append(0)

        place_names = ['ones', 'tens', 'hundreds', 'thousands']
        carry = 0

        # Process each column
        for i in range(max_len):
            d1 = addend1_digits[i]
            d2 = addend2_digits[i]
            column_sum = d1 + d2 + carry
            place_name = place_names[i] if i < len(place_names) else f'10^{i}'

            if column_sum > 9:
                units = column_sum % 10
                new_carry = column_sum // 10
                if carry > 0:
                    steps.append(f"{place_name.capitalize()}: {d1} + {d2} + {carry} = {column_sum}, write {units}, carry {new_carry}")
                else:
                    steps.append(f"{place_name.capitalize()}: {d1} + {d2} = {column_sum}, write {units}, carry {new_carry}")
                carry = new_carry
            else:
                if carry > 0:
                    steps.append(f"{place_name.capitalize()}: {d1} + {d2} + {carry} = {column_sum}")
                else:
                    steps.append(f"{place_name.capitalize()}: {d1} + {d2} = {column_sum}")
                carry = 0

        # Handle final carry
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

        # Convert to digit lists (rightmost digit first for easier processing)
        addend1_digits = [int(d) for d in str(addend1)][::-1]
        addend2_digits = [int(d) for d in str(addend2)][::-1]

        # Pad to same length
        max_len = max(len(addend1_digits), len(addend2_digits))
        while len(addend1_digits) < max_len:
            addend1_digits.append(0)
        while len(addend2_digits) < max_len:
            addend2_digits.append(0)

        place_names = ['ones', 'tens', 'hundreds', 'thousands']
        next_place_names = ['tens', 'hundreds', 'thousands', 'ten-thousands']
        carry = 0

        # Process each column
        for i in range(max_len):
            d1 = addend1_digits[i]
            d2 = addend2_digits[i]
            column_sum = d1 + d2 + carry
            place_name = place_names[i] if i < len(place_names) else f'10^{i}'

            if column_sum > 9:
                units = column_sum % 10
                new_carry = column_sum // 10
                if carry > 0:
                    steps.append(
                        f"{place_name.capitalize()} place: {d1} + {d2} + {carry} (carry) = {column_sum}, "
                        f"which is more than 9"
                    )
                else:
                    steps.append(
                        f"{place_name.capitalize()} place: {d1} + {d2} = {column_sum}, which is more than 9"
                    )
                next_place = next_place_names[i] if i < len(next_place_names) else f'10^{i+1}'
                steps.append(f"Write {units} in {place_name} place, carry {new_carry} to {next_place} place")
                carry = new_carry
            else:
                if carry > 0:
                    steps.append(
                        f"{place_name.capitalize()} place: {d1} + {d2} + {carry} (carry) = {column_sum}"
                    )
                else:
                    steps.append(
                        f"{place_name.capitalize()} place: {d1} + {d2} = {column_sum}"
                    )
                carry = 0

        # Handle final carry
        if carry > 0:
            steps.append(f"Write {carry} in the leftmost position")

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

        steps.append(f"Adding {addend1} + {addend2}")
        steps.extend(self._generate_verbose_steps_for_addition(addend1, addend2))
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
