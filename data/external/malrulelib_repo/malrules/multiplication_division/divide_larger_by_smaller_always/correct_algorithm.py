"""
Correct algorithm for division, including smaller ÷ larger.

Implements proper division that works regardless of relative sizes
of dividend and divisor.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from math import gcd
from utils import CorrectAlgorithm, Problem, Solution


class DivisionCorrectAlgorithm(CorrectAlgorithm):
    """
    Implements correct division for all cases.

    Properly handles division where dividend < divisor, recognizing
    that the result is a fraction/decimal less than 1.
    """

    def get_name(self) -> str:
        return "Correct Division"

    def get_description(self) -> str:
        return (
            "Standard division algorithm that works for all values, "
            "including cases where dividend < divisor (result < 1)."
        )

    def _generate_concise_steps(self, problem: Problem, dividend: float, divisor: float,
                                 result: float) -> list:
        """
        Generate concise steps for the solution.

        Returns a list: [Question, step1, step2, ..., answer]
        """
        steps = []

        # Question
        steps.append(problem.text)

        # Formula extraction
        steps.append(f"{dividend} ÷ {divisor}")

        # Division step
        steps.append(f"{dividend} ÷ {divisor} = {result}")

        # Fraction representation (for integers)
        if isinstance(dividend, int) and isinstance(divisor, int):
            g = gcd(int(dividend), int(divisor))
            if g > 1:
                simplified_num = int(dividend) // g
                simplified_den = int(divisor) // g
                steps.append(f"{dividend}/{divisor} = {simplified_num}/{simplified_den}")

        # Final answer
        steps.append(str(result))

        return steps

    def _generate_verbose_steps(self, problem: Problem, dividend: float, divisor: float,
                                 result: float) -> list:
        """
        Generate verbose steps for the solution (original step format).
        """
        steps = []

        steps.append(f"Problem: {dividend} ÷ {divisor}")
        steps.append("")

        # Check relative sizes
        if dividend < divisor:
            steps.append("Observation: Dividend < Divisor")
            steps.append(f"  {dividend} is less than {divisor}")
            steps.append(f"  This means the answer will be less than 1")
            steps.append(f"  (A smaller quantity divided by a larger quantity)")
            steps.append("")

        # Perform division
        steps.append("Step 1: Divide")
        steps.append(f"  {dividend} ÷ {divisor} = {result}")
        steps.append("")

        # Explain as fraction
        steps.append("Step 2: Interpret as fraction")
        steps.append(f"  {dividend} ÷ {divisor} = {dividend}/{divisor}")

        # Simplify if possible (only for integers)
        if isinstance(dividend, int) and isinstance(divisor, int):
            g = gcd(int(dividend), int(divisor))
            if g > 1:
                simplified_num = int(dividend) // g
                simplified_den = int(divisor) // g
                steps.append(f"  Simplify: {dividend}/{divisor} = {simplified_num}/{simplified_den}")
                steps.append(f"  As decimal: {simplified_num}/{simplified_den} = {simplified_num / simplified_den}")
            else:
                steps.append(f"  As decimal: {dividend}/{divisor} = {result}")
        else:
            steps.append(f"  As decimal: {dividend}/{divisor} = {result}")

        steps.append("")

        # Verification
        steps.append("Step 3: Verify")
        steps.append(f"  Check: {result} × {divisor} = {result * divisor} ✓")
        steps.append("")

        steps.append(f"Final Answer: {result}")

        if dividend < divisor:
            steps.append("(Note: Answer is less than 1, which is correct!)")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct division.

        Args:
            problem: Problem instance with dividend and divisor
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with correct answer and detailed steps
        """
        # Parse dividend and divisor from problem operands
        # Do NOT use metadata answers - solve the problem independently
        if len(problem.operands) >= 2:
            dividend = problem.operands[0]
            divisor = problem.operands[1]
        else:
            raise ValueError(f"Problem must have at least 2 operands for division, got {len(problem.operands)}")

        # Convert to appropriate numeric type
        dividend = float(dividend) if not isinstance(dividend, (int, float)) else dividend
        divisor = float(divisor) if not isinstance(divisor, (int, float)) else divisor

        # Perform division
        result = dividend / divisor

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, dividend, divisor, result)
        else:
            steps = self._generate_concise_steps(problem, dividend, divisor, result)

        return Solution(
            answer=result,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
