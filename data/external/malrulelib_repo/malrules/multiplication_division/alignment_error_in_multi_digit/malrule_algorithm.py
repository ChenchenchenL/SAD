"""
Alignment-Error-In-Multi-Digit malrule algorithm.

Implements the systematic error where students misalign partial products
during multi-digit multiplication. They fail to shift the second partial
product one place to the left when multiplying by the tens digit.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List

class AlignmentErrorMalrule(Malrule):
    """
    Implements the Alignment-Error-In-Multi-Digit bug.

    Students correctly compute partial products but fail to align them properly.
    When multiplying by the tens digit, they don't shift the result one place
    left (multiply by 10), leading to incorrect sums.

    Example: 23 × 14
    Correct:   23 × 4 = 92
               23 × 10 = 230 (shifted left)
               92 + 230 = 322

    Malrule:   23 × 4 = 92
               23 × 1 = 23 (NOT shifted!)
               92 + 23 = 115 (WRONG!)
    """

    def get_name(self) -> str:
        return "Alignment-Error-In-Multi-Digit"

    def get_description(self) -> str:
        return (
            "A systematic procedural bug where students correctly compute partial products "
            "but fail to align them properly according to place value. When multiplying by "
            "the tens digit, students do not shift the partial product one place to the left, "
            "treating the tens digit as if it were in the ones place. For example, in 23 × 14, "
            "they compute 23×4=92 and 23×1=23, then add 92+23=115 instead of 92+230=322. "
            "This error was documented in Brown & Burton's (1978) BUGGY diagnostic system as "
            "a common procedural bug in multi-digit arithmetic algorithms."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Compute malrule answer (alignment error - don't shift)
        return self._apply_malrule(problem).answer

    def _generate_concise_steps(self, problem: Problem, num1: int, num2: int,
                                 malrule_answer: str, is_3digit: bool = False) -> list:
        """
        Generate concise steps for the malrule solution.

        Returns a list: [Question, step1, step2, ..., answer]
        """
        steps = []

        # Question
        steps.append(problem.text)

        # Formula extraction
        steps.append(f"{num1} × {num2}")

        if is_3digit:
            num2_ones = problem.metadata['num2_ones']
            num2_tens = problem.metadata['num2_tens']
            num2_hundreds = problem.metadata['num2_hundreds']

            partial1 = num1 * num2_ones
            partial2_calc = num1 * num2_tens
            partial3_calc = num1 * num2_hundreds

            # Partial products (malrule - no shifting)
            steps.append(f"{num1} × {num2_ones} = {partial1}")
            steps.append(f"{num1} × {num2_tens} = {partial2_calc}")
            steps.append(f"{num1} × {num2_hundreds} = {partial3_calc}")

            # Sum (malrule)
            steps.append(f"{partial1} + {partial2_calc} + {partial3_calc} = {malrule_answer}")
        else:
            num2_ones = problem.metadata.get('num2_ones', num2 % 10)
            num2_tens = problem.metadata.get('num2_tens', num2 // 10)

            partial1 = num1 * num2_ones
            partial2_calc = num1 * num2_tens

            # Partial products (malrule - no shifting)
            steps.append(f"{num1} × {num2_ones} = {partial1}")
            steps.append(f"{num1} × {num2_tens} = {partial2_calc}")

            # Sum (malrule)
            steps.append(f"{partial1} + {partial2_calc} = {malrule_answer}")

        # Final answer
        steps.append(malrule_answer)

        return steps

    def _generate_verbose_steps(self, problem: Problem, num1: int, num2: int,
                                 malrule_answer: str, is_3digit: bool = False) -> list:
        """
        Generate verbose steps for the malrule solution (original step format).
        """
        steps = []

        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: Misalign partial products (don't shift for place value)")
        steps.append("  Student thinks: 'Multiply by each digit and add'")
        steps.append("")

        if is_3digit:
            num2_ones = problem.metadata['num2_ones']
            num2_tens = problem.metadata['num2_tens']
            num2_hundreds = problem.metadata['num2_hundreds']

            partial1 = num1 * num2_ones
            partial2_calc = num1 * num2_tens
            partial3_calc = num1 * num2_hundreds

            steps.append(f"Multiplying {num1} × {num2}")
            steps.append(f"First partial product: {num1} × {num2_ones} = {partial1}")
            steps.append(f"Second partial product: {num1} × {num2_tens} = {partial2_calc}")
            steps.append(f"Third partial product: {num1} × {num2_hundreds} = {partial3_calc}")
            steps.append("")
            steps.append(f"MALRULE: Add without shifting!")
            steps.append(f"  {partial1} + {partial2_calc} + {partial3_calc} = {malrule_answer}")
            steps.append(f"  (Should be {partial1} + {partial2_calc*10} + {partial3_calc*100})")
        else:
            num2_ones = problem.metadata.get('num2_ones', num2 % 10)
            num2_tens = problem.metadata.get('num2_tens', num2 // 10)

            partial1 = num1 * num2_ones
            partial2_calc = num1 * num2_tens

            steps.append(f"Multiplying {num1} × {num2}")
            steps.append(f"First partial product: {num1} × {num2_ones} = {partial1}")
            steps.append(f"Second partial product: {num1} × {num2_tens} = {partial2_calc}")
            steps.append("")
            steps.append(f"MALRULE: Write {partial2_calc} directly below (not shifted left)")
            steps.append(f"  ERROR: Treating '{num2_tens}' as {num2_tens} ones instead of {num2_tens} tens")
            steps.append(f"  Adding: {partial1} + {partial2_calc} = {malrule_answer}")
            steps.append(f"  (Should be {partial1} + {partial2_calc*10} = {num1 * num2})")

        steps.append("")
        steps.append(f"Final Answer: {malrule_answer} (INCORRECT - failed to shift for place value)")
        steps.append("")
        steps.append("Missing: Understanding that place value requires shifting partial products")

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Alignment-Error malrule.

        Computes partial products correctly but doesn't shift the second
        partial product, treating the tens digit as a ones digit.

        Args:
            problem: Multiplication problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with incorrect answer
        """
        template = problem.metadata.get('template', 'basic_2x2')
        num1 = problem.metadata.get('num1', problem.operands[0])
        num2 = problem.metadata.get('num2', problem.operands[1])
        is_3digit = problem.metadata.get('is_3digit', False)

        # Compute malrule answer (never use metadata['malrule_answer'])
        if is_3digit:
            num2_ones = num2 % 10
            num2_tens = (num2 // 10) % 10
            num2_hundreds = num2 // 100

            partial1 = num1 * num2_ones
            partial2_malrule = num1 * num2_tens  # Should be × 10
            partial3_malrule = num1 * num2_hundreds  # Should be × 100

            malrule_answer = partial1 + partial2_malrule + partial3_malrule
        else:
            num2_ones = num2 % 10
            num2_tens = num2 // 10
            partial1 = num1 * num2_ones
            partial2_malrule = num1 * num2_tens  # Malrule: don't shift
            malrule_answer = str(partial1 + partial2_malrule)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, num1, num2, malrule_answer, is_3digit)
        else:
            steps = self._generate_concise_steps(problem, num1, num2, malrule_answer, is_3digit)

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
