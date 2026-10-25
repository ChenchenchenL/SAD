"""
Column-Mimics-Addition malrule algorithm.

Implements the systematic error where students treat multiplication like addition,
multiplying corresponding digits column by column. Additionally, the student
applies the WRITE/CARRY/FORGET/UNITS bug: when a column product is 10 or greater,
they write the carry digit (tens place) instead of the units digit.
"""

import sys
sys.path.append('/Users/kitetsu/nlp_mac/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List

class ColumnMimicsAdditionMalrule(Malrule):
    """
    Implements the Column-Mimics-Addition bug combined with Write-Carry-Forget-Units.

    This is a compound bug documented by Brown & Burton (1978):
    1. The student multiplies column by column like addition (corresponding digits)
    2. For each column product >= 10, the student writes the carry (tens digit)
       and forgets the units digit

    Example: 68 x 46 = 24
        - Ones: 8 x 6 = 48, writes 4 (carry), forgets 8 (units)
        - Tens: 6 x 4 = 24, writes 2 (carry), forgets 4 (units)
        - Result: 24 (instead of 3128)
    """

    def get_name(self) -> str:
        return "Column-Mimics-Addition"

    def get_description(self) -> str:
        return (
            "A compound procedural bug where the student's multiplication algorithm "
            "mimics the column behavior of addition---multiplying column by column "
            "instead of digit by digit. The student processes corresponding digits "
            "in each column (like in addition), but multiplies them instead of adding. "
            "Additionally, the student applies the WRITE/CARRY/FORGET/UNITS bug: when "
            "a column product is 10 or greater, they write only the carry digit (tens "
            "place) and forget the units digit. For products less than 10, they write "
            "the result normally.\n\n"
            "Example: 68 x 46 = 24 (correct: 3128)\n"
            "  - Column 1 (ones): 8 x 6 = 48, writes 4 (the carry), forgets 8\n"
            "  - Column 2 (tens): 6 x 4 = 24, writes 2 (the carry), forgets 4\n"
            "  - Final answer: 24"
        )

    def calculate_expected_answer(self, problem: Problem) -> Any:
        """
        Calculate the expected incorrect answer for this malrule.

        CRITICAL: This method calculates independently without calling solve().

        The malrule:
        1. Multiplies corresponding digits column by column
        2. For products >= 10, writes the carry (tens) instead of units
        3. For products < 10, writes the product normally
        4. When operands have different lengths, missing digits are treated as 1
           (multiplicative identity) - this matches the Brown & Burton (1978) examples

        Args:
            problem: Multiplication problem

        Returns:
            Expected incorrect answer as string
        """
        multiplicand, multiplier = problem.operands[:2]

        # Convert to digit lists (rightmost first for easier processing)
        m1_digits = [int(d) for d in str(multiplicand)][::-1]
        m2_digits = [int(d) for d in str(multiplier)][::-1]

        # Pad to same length using 1 (multiplicative identity) for missing digits
        # This matches the Brown & Burton (1978) examples where:
        # 734 x 37 = 792 (not 92), 2764 x 53 = 2731 (not 31)
        max_len = max(len(m1_digits), len(m2_digits))
        while len(m1_digits) < max_len:
            m1_digits.append(1)  # Use 1 (multiplicative identity) not 0
        while len(m2_digits) < max_len:
            m2_digits.append(1)  # Use 1 (multiplicative identity) not 0

        result_digits = []

        # Multiply column by column, applying write-carry-forget-units
        for i in range(max_len):
            product = m1_digits[i] * m2_digits[i]

            if product >= 10:
                # WRITE/CARRY/FORGET/UNITS: write the carry (tens digit)
                result_digits.append(product // 10)
            else:
                # Product < 10, write it normally
                result_digits.append(product)

        # Remove leading zeros
        while len(result_digits) > 1 and result_digits[-1] == 0:
            result_digits.pop()

        return str(int(''.join(str(d) for d in result_digits[::-1])))

    def _generate_verbose_steps(self, problem: Problem) -> Solution:
        """Generate detailed step-by-step solution showing the malrule."""
        multiplicand, multiplier = problem.operands[:2]

        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append(f"MALRULE: {self.get_name()}")
        steps.append("  Student's incorrect thinking:")
        steps.append("  'I'll multiply column by column, like I do with addition.'")
        steps.append("  'When I get a two-digit answer, I write the carry part.'")
        steps.append("")

        # Convert to digit lists (rightmost first)
        m1_digits = [int(d) for d in str(multiplicand)][::-1]
        m2_digits = [int(d) for d in str(multiplier)][::-1]

        # Pad to same length using 1 (multiplicative identity)
        max_len = max(len(m1_digits), len(m2_digits))
        while len(m1_digits) < max_len:
            m1_digits.append(1)
        while len(m2_digits) < max_len:
            m2_digits.append(1)

        place_names = ['ones', 'tens', 'hundreds', 'thousands', 'ten-thousands']
        result_digits = []

        steps.append(f"Processing {multiplicand} x {multiplier} column by column:")

        for i in range(max_len):
            place = place_names[i] if i < len(place_names) else f'10^{i}'
            d1 = m1_digits[i]
            d2 = m2_digits[i]
            product = d1 * d2

            if product >= 10:
                carry = product // 10
                units = product % 10
                steps.append(f"  {place.capitalize()}: {d1} x {d2} = {product}")
                steps.append(f"    -> Writes {carry} (the carry), forgets {units} (the units)")
                result_digits.append(carry)
            else:
                steps.append(f"  {place.capitalize()}: {d1} x {d2} = {product}")
                steps.append(f"    -> Writes {product}")
                result_digits.append(product)

        # Remove leading zeros
        while len(result_digits) > 1 and result_digits[-1] == 0:
            result_digits.pop()

        answer = str(int(''.join(str(d) for d in result_digits[::-1])))

        steps.append("")
        steps.append(f"Malrule Answer: {answer}")
        steps.append(f"Correct Answer: {multiplicand * multiplier}")
        steps.append("(INCORRECT due to Column-Mimics-Addition + Write-Carry-Forget-Units)")

        return Solution(
            answer=answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _generate_concise_steps(self, problem: Problem) -> Solution:
        """Generate concise solution."""
        multiplicand, multiplier = problem.operands[:2]
        answer = self.calculate_expected_answer(problem)

        # Convert to digit lists (rightmost first)
        m1_digits = [int(d) for d in str(multiplicand)][::-1]
        m2_digits = [int(d) for d in str(multiplier)][::-1]

        # Pad to same length using 1 (multiplicative identity)
        max_len = max(len(m1_digits), len(m2_digits))
        while len(m1_digits) < max_len:
            m1_digits.append(1)
        while len(m2_digits) < max_len:
            m2_digits.append(1)

        place_names = ['ones', 'tens', 'hundreds', 'thousands', 'ten-thousands']

        steps = [f"Problem: {problem.text}"]
        steps.append(f"Malrule: {self.get_name()}")

        for i in range(max_len):
            place = place_names[i] if i < len(place_names) else f'10^{i}'
            d1 = m1_digits[i]
            d2 = m2_digits[i]
            product = d1 * d2
            if product >= 10:
                steps.append(f"{place.capitalize()}: {d1} x {d2} = {product}, write {product // 10}")
            else:
                steps.append(f"{place.capitalize()}: {d1} x {d2} = {product}")

        steps.append(f"Answer: {answer}")

        return Solution(
            answer=answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Column-Mimics-Addition malrule to solve the problem incorrectly.

        Args:
            problem: Multiplication problem to solve
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with incorrect answer due to Column-Mimics-Addition bug
        """
        if verbose:
            return self._generate_verbose_steps(problem)
        else:
            return self._generate_concise_steps(problem)
