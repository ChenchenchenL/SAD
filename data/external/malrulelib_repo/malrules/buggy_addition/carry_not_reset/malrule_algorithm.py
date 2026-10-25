"""
Carry-Not-Reset malrule algorithm.

Implements the systematic error where students forget to reset the carry
register after each column, causing carries to accumulate across columns.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List

class CarryNotResetMalrule(Malrule):
    """
    Implements the Carry-Not-Reset bug from Brown & Burton (1978).

    After determining the carry, the student forgets to reset the "carry register"
    to zero and hence the amount carried is accumulated across the columns.

    Example: 328 + 917 = 1345 (correct: 1245)
      - 8+7=15, write 5, carry 1
      - 2+1=3, plus carry 1 = 4, but carry NOT reset (still 1)
      - 3+9=12, plus carry 1 (still there!) = 13

    Physical explanation from Brown & Burton: "Child might use his fingers to
    remember the carry and forget to bend back his fingers, or counters,
    after each carry is added."
    """

    def get_name(self) -> str:
        return "Carry-Not-Reset"

    def get_description(self) -> str:
        return (
            "A systematic procedural bug in addition where the student forgets "
            "to reset the carry register to zero after processing each column. "
            "Instead of resetting the carry after adding it to a column, the "
            "carry value accumulates across columns. For example, in 328 + 917, "
            "the student writes 5 (from 8+7=15), carries 1, then computes 2+1+1=4, "
            "but instead of resetting the carry to 0, keeps it at 1. In the next "
            "column, 3+9+1=13, so the final answer is 1345 instead of 1245. "
            "This bug was identified by Brown & Burton (1978) in their BUGGY "
            "diagnostic system for arithmetic procedures."
        )

    def calculate_expected_answer(self, problem: Problem) -> Any:
        """
        Calculate the expected incorrect answer for the Carry-Not-Reset malrule.

        CRITICAL: This method calculates independently and does NOT call solve().

        Args:
            problem: Addition problem

        Returns:
            Expected incorrect answer as string
        """
        # Calculate from operands
        num1, num2 = problem.operands[:2]
        return str(self._calculate_malrule_answer(num1, num2))

    def _calculate_malrule_answer(self, num1: int, num2: int) -> int:
        """
        Calculate the answer using the Carry-Not-Reset malrule.

        The bug: After a carry is generated, the student forgets to reset it to 0.
        The carry persists across columns even when the column sum < 10.
        However, the carry doesn't accumulate - it just never gets cleared.

        Example: 328 + 917 = 1345 (correct: 1245)
          - Col 0: 8+7=15, write 5, carry=1
          - Col 1: 2+1+1=4, write 4, carry should be 0 but stays 1 (BUG!)
          - Col 2: 3+9+1=13, write 3, carry=1 (new carry replaces old)
          - Final: write 1
          - Result: 1345

        Args:
            num1: First addend
            num2: Second addend

        Returns:
            Malrule answer (with persistent, non-resetting carry)
        """
        num1_digits = [int(d) for d in str(num1)][::-1]
        num2_digits = [int(d) for d in str(num2)][::-1]

        # Pad to same length
        max_len = max(len(num1_digits), len(num2_digits))
        while len(num1_digits) < max_len:
            num1_digits.append(0)
        while len(num2_digits) < max_len:
            num2_digits.append(0)

        result_digits = []
        carry = 0  # MALRULE: This never gets reset to 0!

        for i in range(max_len):
            column_sum = num1_digits[i] + num2_digits[i] + carry

            if column_sum >= 10:
                result_digits.append(column_sum % 10)
                # New carry generated - update carry value
                carry = column_sum // 10
            else:
                result_digits.append(column_sum)
                # MALRULE: No new carry, but old carry persists (NOT reset to 0!)
                # carry stays at its current value

        # Add any remaining carry
        if carry > 0:
            for digit in str(carry)[::-1]:
                result_digits.append(int(digit))

        # Convert back to integer
        result_digits = result_digits[::-1]
        return int(''.join(str(d) for d in result_digits))

    def _generate_concise_steps(self, problem: Problem, malrule_answer: int) -> List[str]:
        """
        Generate concise steps showing only formulas and values.

        Args:
            problem: The problem instance
            malrule_answer: The computed malrule answer

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
                steps.append(f"  Write {column_sum % 10}, carry {column_sum // 10}")
                carry = column_sum // 10
            else:
                if carry > 0:
                    steps.append(f"  Write {column_sum}, carry stays {carry} (NOT reset!)")

        if carry > 0:
            steps.append(f"Final carry: {carry}")

        steps.append(f"Answer: {malrule_answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, malrule_answer: int) -> List[str]:
        """
        Generate verbose steps with full explanations.

        Args:
            problem: The problem instance
            malrule_answer: The computed malrule answer

        Returns:
            List of verbose step strings
        """
        steps = []
        num1, num2 = problem.operands[:2]

        steps.append(f"Adding {num1} + {num2}")
        steps.append("")
        steps.append("MALRULE: Carry-Not-Reset")
        steps.append("  Student forgets to reset carry to 0 after each column")
        steps.append("")

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
                new_carry = column_sum // 10
                steps.append(f"  Write {column_sum % 10}, carry becomes {new_carry}")
                carry = new_carry
            else:
                steps.append(f"  Write {column_sum}")
                if carry > 0:
                    steps.append(f"  MALRULE: Carry stays {carry} (should reset to 0!)")

        if carry > 0:
            steps.append(f"")
            steps.append(f"Final carry: {carry}")

        steps.append("")
        steps.append(f"Final answer: {malrule_answer} (INCORRECT due to Carry-Not-Reset)")
        steps.append(f"Correct answer would be: {num1 + num2}")

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Carry-Not-Reset malrule to solve the problem incorrectly.

        Args:
            problem: Addition problem to solve
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with incorrect answer due to Carry-Not-Reset bug
        """
        # Calculate the malrule answer
        malrule_answer = int(self.calculate_expected_answer(problem))

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, malrule_answer)
        else:
            steps = self._generate_concise_steps(problem, malrule_answer)

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
