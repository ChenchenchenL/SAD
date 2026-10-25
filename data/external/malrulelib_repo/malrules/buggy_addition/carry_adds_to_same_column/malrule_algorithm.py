"""
Carry-Adds-To-Same-Column malrule algorithm.

Implements the systematic error where students add the units digit and carry
digit together when a column sum exceeds 9, writing the combined result in
the same column instead of carrying to the next column.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List

class CarryAddsToSameColumnMalrule(Malrule):
    """
    Implements the Carry-Adds-To-Same-Column bug.

    When a column adds to more than 9, the student adds the units digit and
    the carry digit together and writes that result in the current column.
    The carry is NOT propagated to the next column.

    Example: 7+5=12, student computes 1+2=3 and writes 3 (instead of writing
    2 and carrying 1 to the next column).
    """

    def get_name(self) -> str:
        return "Carry-Adds-To-Same-Column"

    def get_description(self) -> str:
        return (
            "A systematic procedural bug where, when a column sum exceeds 9, "
            "the student adds the units digit and carry digit together and writes "
            "that combined result in the current column. The carry is NOT propagated "
            "to the next column. For example, in 17 + 5, the ones column computes "
            "7+5=12, then the student adds 1+2=3 and writes 3 in the ones column. "
            "The tens column then computes 1+0=1. Result: 13 instead of 22. "
            "This bug may arise from confusion about Method 2 (left-to-right addition) "
            "where carries are written under the same column."
        )

    def calculate_expected_answer(self, problem: Problem) -> Any:
        """
        Calculate the expected incorrect answer for this malrule.

        For Carry-Adds-To-Same-Column:
        - When a column sum > 9, add units and carry digits together
        - Write that combined result in the current column
        - Do NOT carry to the next column

        Args:
            problem: Addition problem

        Returns:
            Expected incorrect answer as string
        """
        # Calculate from operands
        addend1, addend2 = problem.operands[:2]

        # Convert to digit lists (rightmost digit first for easier processing)
        addend1_digits = [int(d) for d in str(addend1)][::-1]
        addend2_digits = [int(d) for d in str(addend2)][::-1]

        # Pad to same length
        max_len = max(len(addend1_digits), len(addend2_digits))
        while len(addend1_digits) < max_len:
            addend1_digits.append(0)
        while len(addend2_digits) < max_len:
            addend2_digits.append(0)

        result_digits = []

        # Process each column - NO carry to next column
        for i in range(max_len):
            column_sum = addend1_digits[i] + addend2_digits[i]

            if column_sum > 9:
                # MALRULE: Add units digit and carry digit together
                units_digit = column_sum % 10
                carry_digit = column_sum // 10
                combined = units_digit + carry_digit
                result_digits.append(combined)
            else:
                # No carry needed, just use the sum
                result_digits.append(column_sum)

        # Remove leading zeros
        while len(result_digits) > 1 and result_digits[-1] == 0:
            result_digits.pop()

        return str(int(''.join(str(d) for d in result_digits[::-1])))

    def _generate_concise_steps(self, problem: Problem, malrule_answer: str) -> List[str]:
        """
        Generate concise steps showing only formulas and values.

        Args:
            problem: The problem instance
            malrule_answer: The computed malrule answer

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
        steps.extend(self._generate_column_steps_concise(addend1, addend2))

        # Add answer
        steps.append(f"Answer: {malrule_answer}")

        return steps

    def _generate_column_steps_concise(self, addend1: int, addend2: int) -> List[str]:
        """Generate concise column-by-column steps."""
        steps = []

        # Convert to digit lists (rightmost digit first)
        addend1_digits = [int(d) for d in str(addend1)][::-1]
        addend2_digits = [int(d) for d in str(addend2)][::-1]

        # Pad to same length
        max_len = max(len(addend1_digits), len(addend2_digits))
        while len(addend1_digits) < max_len:
            addend1_digits.append(0)
        while len(addend2_digits) < max_len:
            addend2_digits.append(0)

        place_names = ['ones', 'tens', 'hundreds', 'thousands']

        for i in range(max_len):
            d1 = addend1_digits[i]
            d2 = addend2_digits[i]
            column_sum = d1 + d2
            place_name = place_names[i] if i < len(place_names) else f'10^{i}'

            if column_sum > 9:
                units = column_sum % 10
                carry = column_sum // 10
                combined = units + carry
                steps.append(f"{place_name.capitalize()}: {d1} + {d2} = {column_sum}, then {units} + {carry} = {combined}")
            else:
                steps.append(f"{place_name.capitalize()}: {d1} + {d2} = {column_sum}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, malrule_answer: str) -> List[str]:
        """
        Generate verbose steps with full explanations.

        Args:
            problem: The problem instance
            malrule_answer: The computed malrule answer

        Returns:
            List of verbose step strings
        """
        steps = []
        addend1, addend2 = problem.operands[:2]

        steps.append(f"Adding {addend1} + {addend2}")
        steps.append("")
        steps.append(f"MALRULE: {self.get_name()}")
        steps.append("  When column sum > 9, add units digit and carry digit together")
        steps.append("")

        # Add column-by-column steps
        steps.extend(self._generate_column_steps_verbose(addend1, addend2))

        steps.append(f"Final answer: {malrule_answer} (INCORRECT due to Carry-Adds-To-Same-Column)")

        return steps

    def _generate_column_steps_verbose(self, addend1: int, addend2: int) -> List[str]:
        """Generate verbose column-by-column steps."""
        steps = []

        # Convert to digit lists (rightmost digit first)
        addend1_digits = [int(d) for d in str(addend1)][::-1]
        addend2_digits = [int(d) for d in str(addend2)][::-1]

        # Pad to same length
        max_len = max(len(addend1_digits), len(addend2_digits))
        while len(addend1_digits) < max_len:
            addend1_digits.append(0)
        while len(addend2_digits) < max_len:
            addend2_digits.append(0)

        place_names = ['ones', 'tens', 'hundreds', 'thousands']

        for i in range(max_len):
            d1 = addend1_digits[i]
            d2 = addend2_digits[i]
            column_sum = d1 + d2
            place_name = place_names[i] if i < len(place_names) else f'10^{i}'

            if column_sum > 9:
                units = column_sum % 10
                carry = column_sum // 10
                combined = units + carry
                steps.append(
                    f"{place_name.capitalize()} place: {d1} + {d2} = {column_sum} (more than 9), "
                    f"so add units and carry: {units} + {carry} = {combined}, write {combined}"
                )
            else:
                steps.append(
                    f"{place_name.capitalize()} place: {d1} + {d2} = {column_sum}, write {column_sum}"
                )

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Carry-Adds-To-Same-Column malrule to solve the problem incorrectly.

        Args:
            problem: Addition problem to solve
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with incorrect answer due to Carry-Adds-To-Same-Column bug
        """
        # Calculate the malrule answer
        malrule_answer = self.calculate_expected_answer(problem)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, malrule_answer)
        else:
            steps = self._generate_concise_steps(problem, malrule_answer)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
