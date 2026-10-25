"""
Left-Justify malrule algorithm.

Implements the systematic error where students align numbers on the left
instead of the right (place value alignment) when adding numbers of
different digit lengths.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List

class LeftJustifyMalrule(Malrule):
    """
    Implements the Left-Justify bug from Brown & Burton (1978).

    When the top number has fewer digits than the bottom number (or vice versa),
    students left-justify (align on the left) instead of right-justify
    (align on the right/place value alignment).

    Example: 23 + 456
    - Correct (right-justified):
          23
        +456
        ----
         479

    - Malrule (left-justified):
        230  (23 padded with 0 on right)
       +456
       ----
        686
    """

    def get_name(self) -> str:
        return "Left-Justify"

    def get_description(self) -> str:
        return (
            "A systematic procedural bug where the student aligns numbers on the left "
            "side instead of the right side (place value alignment) when adding numbers "
            "of different digit lengths. This causes the shorter number to be effectively "
            "multiplied by a power of 10. For example, in 23 + 456, the student aligns "
            "23 with the left side of 456, treating 23 as 230, yielding 686 instead of "
            "the correct answer 479. This is documented in Brown & Burton's 1978 paper "
            "on diagnostic models for procedural bugs in basic mathematical skills."
        )

    def calculate_expected_answer(self, problem: Problem) -> int:
        """
        Calculate the expected incorrect answer using left-justification.

        The shorter number is padded with zeros on the right to match
        the length of the longer number, then added.

        Args:
            problem: Addition problem

        Returns:
            Expected incorrect answer as integer

        CRITICAL: This method calculates independently - does NOT call solve().
        """
        # Calculate from operands
        num1, num2 = problem.operands[:2]
        return self._apply_left_justify(num1, num2)

    def _apply_left_justify(self, num1: int, num2: int) -> int:
        """
        Apply left-justify malrule to two numbers.

        Args:
            num1: First number
            num2: Second number

        Returns:
            Incorrect sum using left-justification
        """
        str1 = str(num1)
        str2 = str(num2)

        len1 = len(str1)
        len2 = len(str2)

        if len1 == len2:
            # Same length - no alignment difference
            return num1 + num2

        if len1 < len2:
            # num1 is shorter - pad with zeros on right
            diff = len2 - len1
            adjusted_num1 = num1 * (10 ** diff)
            return adjusted_num1 + num2
        else:
            # num2 is shorter - pad with zeros on right
            diff = len1 - len2
            adjusted_num2 = num2 * (10 ** diff)
            return num1 + adjusted_num2

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Left-Justify malrule to solve the problem incorrectly.

        Args:
            problem: Addition problem to solve
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with incorrect answer due to Left-Justify bug
        """
        if verbose:
            return self._generate_verbose_steps(problem)
        else:
            return self._generate_concise_steps(problem)

    def _generate_concise_steps(self, problem: Problem) -> Solution:
        """Generate concise steps showing only formulas and values."""
        num1, num2 = problem.operands[:2]
        malrule_answer = self.calculate_expected_answer(problem)

        steps = []
        steps.append(f"Question: {problem.text}")

        str1 = str(num1)
        str2 = str(num2)
        len1 = len(str1)
        len2 = len(str2)

        if len1 != len2:
            if len1 < len2:
                diff = len2 - len1
                adjusted = num1 * (10 ** diff)
                steps.append(f"Left-align: {num1} becomes {adjusted}")
                steps.append(f"Calculate: {adjusted} + {num2} = {malrule_answer}")
            else:
                diff = len1 - len2
                adjusted = num2 * (10 ** diff)
                steps.append(f"Left-align: {num2} becomes {adjusted}")
                steps.append(f"Calculate: {num1} + {adjusted} = {malrule_answer}")
        else:
            steps.append(f"Calculate: {num1} + {num2} = {malrule_answer}")

        steps.append(f"Answer: {malrule_answer}")

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _generate_verbose_steps(self, problem: Problem) -> Solution:
        """Generate verbose steps with full explanations."""
        num1, num2 = problem.operands[:2]
        malrule_answer = self.calculate_expected_answer(problem)

        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append(f"MALRULE: {self.get_name()}")
        steps.append("  Student belief: 'Numbers should be aligned from the left'")
        steps.append("")

        str1 = str(num1)
        str2 = str(num2)
        len1 = len(str1)
        len2 = len(str2)

        if len1 != len2:
            steps.append(f"Step 1: Identify different lengths")
            steps.append(f"  {num1} has {len1} digit(s)")
            steps.append(f"  {num2} has {len2} digit(s)")
            steps.append("")

            if len1 < len2:
                diff = len2 - len1
                adjusted = num1 * (10 ** diff)
                steps.append(f"Step 2: Left-justify alignment (INCORRECT)")
                steps.append(f"  Align {num1} on the left with {num2}")
                steps.append(f"  {num1} is treated as {adjusted} (padded with {diff} zero(s) on right)")
                steps.append("")
                steps.append(f"Step 3: Add the left-justified numbers")
                steps.append(f"  {adjusted} + {num2} = {malrule_answer}")
            else:
                diff = len1 - len2
                adjusted = num2 * (10 ** diff)
                steps.append(f"Step 2: Left-justify alignment (INCORRECT)")
                steps.append(f"  Align {num2} on the left with {num1}")
                steps.append(f"  {num2} is treated as {adjusted} (padded with {diff} zero(s) on right)")
                steps.append("")
                steps.append(f"Step 3: Add the left-justified numbers")
                steps.append(f"  {num1} + {adjusted} = {malrule_answer}")
        else:
            steps.append(f"Step 1: Numbers have same length ({len1} digits each)")
            steps.append(f"Step 2: Add normally: {num1} + {num2} = {malrule_answer}")

        steps.append("")
        steps.append(f"Answer: {malrule_answer} (INCORRECT due to Left-Justify)")

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
