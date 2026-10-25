"""
Write-Carry-Forget-Units malrule algorithm.

Implements the systematic error where students write the carry digit and
forget to write the units digit when adding columns that produce a carry.
"""

import sys
sys.path.append('/Users/kitetsu/nlp_mac/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List

class WriteCarryForgetUnitsMalrule(Malrule):
    """
    Implements the Write-Carry-Forget-Units bug.

    When adding a column where the sum is 10 or more, the student writes
    only the carry digit (tens digit) and forgets to write the units digit.

    Example: 87 + 93
    - Column 1: 7+3=10, student writes 1 (the carry), forgets the 0
    - Column 2: 8+9=17, student writes 1 (the carry), forgets the 7
    - Result: 11 (WRONG! Correct is 180)
    """

    def get_name(self) -> str:
        return "Write-Carry-Forget-Units"

    def get_description(self) -> str:
        return (
            "A systematic procedural bug where the student writes the carry digit "
            "and forgets to write the units digit in the answer when a column sum "
            "is 10 or more. For example, in 87 + 93, the student computes 7+3=10, "
            "writes 1 (the carry digit) instead of 0, then 8+9=17, writes 1 (the "
            "carry digit) instead of 7, yielding 11 instead of the correct answer 180. "
            "This bug was documented by Brown & Burton (1978) in their analysis of "
            "systematic procedural errors in arithmetic."
        )

    def calculate_expected_answer(self, problem: Problem) -> Any:
        """
        Calculate the expected incorrect answer for this malrule.

        For Write-Carry-Forget-Units:
        - When column sum >= 10: write only the carry digit (tens digit)
        - When column sum < 10: write the units digit normally
        - IMPORTANT: The carry is NOT propagated to the next column!
          The student "forgets" about both the units digit AND the carry propagation.

        Args:
            problem: Addition problem

        Returns:
            Expected incorrect answer as string
        """
        # Calculate from operands
        addend1, addend2 = problem.operands[:2]
        return str(self._apply_malrule_to_two_numbers(addend1, addend2))

    def _apply_malrule_to_two_numbers(self, addend1: int, addend2: int) -> int:
        """
        Apply the Write-Carry-Forget-Units malrule to two numbers.

        The key insight from Brown & Burton (1978):
        - When sum >= 10, student writes the carry digit (tens place of sum)
        - The carry is NOT propagated to the next column
        - This explains examples like 365+574=819:
          * ones: 5+4=9 (write 9)
          * tens: 6+7=13 (write 1, the carry digit, forget the 3 AND don't propagate)
          * hundreds: 3+5=8 (write 8, no carry received)
          * Result: 819

        Args:
            addend1: First addend
            addend2: Second addend

        Returns:
            Incorrect result due to malrule
        """
        # Pad to same length
        max_len = max(len(str(addend1)), len(str(addend2)))
        addend1_digits = [int(d) for d in str(addend1).zfill(max_len)][::-1]
        addend2_digits = [int(d) for d in str(addend2).zfill(max_len)][::-1]

        result_digits = []

        # Process each column independently (no carry propagation!)
        for i in range(max_len):
            column_sum = addend1_digits[i] + addend2_digits[i]
            # Note: No carry is added from previous column!

            if column_sum >= 10:
                # MALRULE: Write the carry digit (tens place), forget the units
                result_digits.append(column_sum // 10)
            else:
                # Normal: write the units digit
                result_digits.append(column_sum)

        # No final carry is added (it was already "written" in the answer)

        # Remove leading zeros and convert to number
        while len(result_digits) > 1 and result_digits[-1] == 0:
            result_digits.pop()

        return int(''.join(str(d) for d in result_digits[::-1]))

    def _generate_concise_steps(self, problem: Problem) -> List[str]:
        """
        Generate concise steps showing the malrule calculation.

        Args:
            problem: The problem instance

        Returns:
            List of concise step strings
        """
        steps = []
        addend1, addend2 = problem.operands[:2]

        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: {addend1} + {addend2}")

        # Pad to same length
        max_len = max(len(str(addend1)), len(str(addend2)))
        addend1_digits = [int(d) for d in str(addend1).zfill(max_len)][::-1]
        addend2_digits = [int(d) for d in str(addend2).zfill(max_len)][::-1]

        place_names = ['ones', 'tens', 'hundreds', 'thousands', 'ten-thousands']

        # Process each column independently (no carry propagation in this malrule!)
        for i in range(max_len):
            d1 = addend1_digits[i]
            d2 = addend2_digits[i]
            column_sum = d1 + d2  # No carry added!
            place_name = place_names[i] if i < len(place_names) else f'10^{i}'

            steps.append(f"{place_name.capitalize()}: {d1} + {d2} = {column_sum}")

            if column_sum >= 10:
                steps.append(f"  -> Write {column_sum // 10} (carry digit), forget units")

        answer = self.calculate_expected_answer(problem)
        steps.append(f"Answer: {answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem) -> List[str]:
        """
        Generate verbose steps with full explanations.

        Args:
            problem: The problem instance

        Returns:
            List of verbose step strings
        """
        steps = []
        addend1, addend2 = problem.operands[:2]

        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append(f"MALRULE: {self.get_name()}")
        steps.append("  Student belief: 'When adding produces 10 or more, write the carry digit'")
        steps.append("  (The carry is written but NOT propagated to the next column)")
        steps.append("")
        steps.append(f"Adding {addend1} + {addend2}")

        # Pad to same length
        max_len = max(len(str(addend1)), len(str(addend2)))
        addend1_digits = [int(d) for d in str(addend1).zfill(max_len)][::-1]
        addend2_digits = [int(d) for d in str(addend2).zfill(max_len)][::-1]

        place_names = ['ones', 'tens', 'hundreds', 'thousands', 'ten-thousands']

        # Process each column independently (no carry propagation!)
        for i in range(max_len):
            d1 = addend1_digits[i]
            d2 = addend2_digits[i]
            column_sum = d1 + d2  # No carry added from previous column!
            place_name = place_names[i] if i < len(place_names) else f'10^{i}'

            steps.append("")
            steps.append(f"Step {i+1}: {place_name.capitalize()} place: {d1} + {d2} = {column_sum}")

            if column_sum >= 10:
                steps.append(f"  Sum is {column_sum} (>= 10)")
                steps.append(f"  MALRULE: Write {column_sum // 10} (the carry digit)")
                steps.append(f"  FORGOT: The units digit {column_sum % 10}")
                steps.append(f"  FORGOT: The carry is not propagated to next column")
            else:
                steps.append(f"  Sum is {column_sum} (< 10), no carry needed")
                steps.append(f"  Write {column_sum}")

        answer = self.calculate_expected_answer(problem)
        correct_answer = addend1 + addend2
        steps.append("")
        steps.append(f"Final Answer: {answer} (INCORRECT)")
        steps.append(f"Correct Answer would be: {correct_answer}")

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Write-Carry-Forget-Units malrule to solve the problem incorrectly.

        Args:
            problem: Addition problem to solve
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with incorrect answer due to Write-Carry-Forget-Units bug
        """
        # Calculate the malrule answer
        malrule_answer = self.calculate_expected_answer(problem)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem)
        else:
            steps = self._generate_concise_steps(problem)

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
