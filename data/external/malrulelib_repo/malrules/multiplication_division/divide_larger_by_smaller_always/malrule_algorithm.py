"""
Malrule algorithm for Divide-Larger-By-Smaller-Always error.

Students believe division must always be larger ÷ smaller, so they
either reverse the operands or claim the problem is impossible.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class DivideLargerBySmallerAlwaysMalrule(Malrule):
    """
    Implements the Divide-Larger-By-Smaller-Always malrule.

    Students incorrectly believe that division must always be
    larger ÷ smaller. When presented with smaller ÷ larger,
    they reverse the operands.

    Example: 4 ÷ 6
    Correct: 4 ÷ 6 = 0.667 (or 2/3)
    Malrule: "Can't divide smaller by larger, must be 6 ÷ 4 = 1.5"
    """

    def get_name(self) -> str:
        return "Divide-Larger-By-Smaller-Always"

    def get_description(self) -> str:
        return (
            "A persistent misconception where students believe division must always involve "
            "a larger dividend divided by a smaller divisor. When presented with problems where "
            "the dividend is smaller than the divisor (e.g., 4 ÷ 6), students either reverse "
            "the operands or claim the problem is impossible. Fischbein et al. (1985) identified "
            "this as stemming from 'primitive intuitive models' where division is associated with "
            "sharing larger quantities among smaller groups."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
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

        # Malrule: reverse operands when dividend < divisor
        # Check if dividend < divisor
        if dividend < divisor:
            # Reverse the operands
            result = divisor / dividend
        else:
            # If dividend >= divisor, student computes correctly
            result = dividend / divisor

        return str(result)

    def _generate_concise_steps(self, problem: Problem, dividend: float, divisor: float,
                                 result: float, reversed_operands: bool) -> list:
        """
        Generate concise steps for the malrule solution.

        Returns a list: [Question, step1, step2, ..., answer]
        """
        steps = []

        # Question
        steps.append(problem.text)

        # Formula extraction
        steps.append(f"{dividend} ÷ {divisor}")

        if reversed_operands:
            # Reverse step
            steps.append(f"{divisor} ÷ {dividend}")

            # Division step
            steps.append(f"{divisor} ÷ {dividend} = {result}")
        else:
            # Division step
            steps.append(f"{dividend} ÷ {divisor} = {result}")

        # Final answer
        steps.append(str(result))

        return steps

    def _generate_verbose_steps(self, problem: Problem, dividend: float, divisor: float,
                                 result: float, reversed_operands: bool,
                                 template: str, context_type: str) -> list:
        """
        Generate verbose steps for the malrule solution (original step format).
        """
        steps = []

        # Add problem statement
        if template in ['word_problem_sharing', 'word_problem_measurement']:
            steps.append(f"Problem: {problem.text}")
            steps.append(f"Expression: {dividend} ÷ {divisor}")
        else:
            steps.append(f"Problem: {dividend} ÷ {divisor}")
        steps.append("")

        # Check if dividend < divisor
        if reversed_operands:
            steps.append("MALRULE: Check operand sizes")
            steps.append(f"  {dividend} is less than {divisor}")

            if context_type == 'sharing':
                steps.append(f"  MALRULE REASONING: 'Can't share {dividend} items among {divisor} people!'")
                steps.append(f"  MALRULE REASONING: 'Must be {divisor} items among {dividend} people'")
            elif context_type == 'measurement':
                steps.append(f"  MALRULE REASONING: 'Can't divide {dividend} into {divisor} pieces!'")
                steps.append(f"  MALRULE REASONING: 'Must be {divisor} divided into {dividend} pieces'")
            else:
                steps.append(f"  MALRULE REASONING: 'Can't divide smaller by larger!'")
                steps.append(f"  MALRULE REASONING: 'Must reverse to make it work'")
            steps.append("")

            # Reverse the operands
            steps.append("Step 1: Reverse operands")
            steps.append(f"  Change {dividend} ÷ {divisor} to {divisor} ÷ {dividend}")
            steps.append(f"  MALRULE: Division must be larger ÷ smaller")
            steps.append("")

            # Perform reversed division
            steps.append("Step 2: Divide")
            steps.append(f"  {divisor} ÷ {dividend} = {result}")
            steps.append("")

            steps.append(f"Final Answer: {result} (INCORRECT - operands were reversed!)")

        else:
            # If dividend >= divisor, student computes correctly
            steps.append("Operands are in correct order (larger ÷ smaller)")
            steps.append(f"  {dividend} ÷ {divisor} = {result}")
            steps.append("")
            steps.append(f"Final Answer: {result}")

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the divide-larger-by-smaller-always malrule.

        Students reverse operands when dividend < divisor.

        Args:
            problem: Problem instance with dividend and divisor
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with incorrect answer and student's reasoning
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

        template = problem.metadata.get('template', 'basic_smaller_dividend')
        context_type = problem.metadata.get('context_type', None)

        # Check if we need to reverse operands
        reversed_operands = dividend < divisor

        # Calculate result
        if reversed_operands:
            result = divisor / dividend
        else:
            result = dividend / divisor

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(
                problem, dividend, divisor, result, reversed_operands,
                template, context_type
            )
        else:
            steps = self._generate_concise_steps(
                problem, dividend, divisor, result, reversed_operands
            )

        return Solution(
            answer=str(result),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
