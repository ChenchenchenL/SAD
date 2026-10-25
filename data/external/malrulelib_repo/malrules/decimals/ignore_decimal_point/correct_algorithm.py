"""
Correct algorithm for decimal arithmetic.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class DecimalArithmeticCorrectAlgorithm(CorrectAlgorithm):
    """Correctly performs decimal arithmetic operations."""

    def get_name(self) -> str:
        return "Correct Decimal Arithmetic"

    def get_description(self) -> str:
        return "Correctly performs operations with decimal numbers, respecting place value."

    def _generate_verbose_steps(self, problem: Problem, num1: float, num2: float,
                                 operator: str, operation: str, correct_answer_str: str,
                                 is_word_problem: bool, word_problem_type: str) -> List[str]:
        """Generate verbose, explanatory steps."""
        steps = []

        # For word problems, show extraction step
        if is_word_problem:
            steps.append(f"Word Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Extract the equation from the word problem")
            steps.append(f"  Equation: {num1} {operator} {num2}")
            steps.append("")
            steps.append("Step 2: Solve using proper decimal arithmetic")
            steps.append("")
        else:
            steps.append(f"Problem: {problem.text}")
            steps.append("")

        steps.append("CORRECT METHOD: Respecting decimal place value")
        steps.append("")

        if operation == 'addition':
            steps.append("Step 1: Align decimal points")
            steps.append(f"  {num1}")
            steps.append(f"+ {num2}")
            steps.append("  -----")
            steps.append("")
            steps.append("Step 2: Add from right to left")
            steps.append(f"  {num1} + {num2} = {correct_answer_str}")

        elif operation == 'subtraction':
            steps.append("Step 1: Align decimal points")
            steps.append(f"  {num1}")
            steps.append(f"- {num2}")
            steps.append("  -----")
            steps.append("")
            steps.append("Step 2: Subtract from right to left")
            steps.append(f"  {num1} - {num2} = {correct_answer_str}")

        elif operation == 'division':
            steps.append("Step 1: Perform division with decimals")
            steps.append(f"  {num1} ÷ {num2}")
            steps.append("")
            steps.append(f"Step 2: Calculate: {num1} ÷ {num2} = {correct_answer_str}")
            steps.append("")
            steps.append("  ✓ Decimal points are considered in division")

        else:  # multiplication
            steps.append("Step 1: Multiply ignoring decimals first")
            num1_str = str(num1)
            num2_str = str(num2)

            temp_product = int(num1_str.replace('.', '')) * int(num2_str.replace('.', ''))
            steps.append(f"  {num1_str.replace('.', '')} × {num2_str.replace('.', '')} = {temp_product}")
            steps.append("")
            steps.append(f"Step 2: Count decimal places ({len(num1_str.split('.')[1])} + {len(num2_str.split('.')[1])} = {len(num1_str.split('.')[1]) + len(num2_str.split('.')[1])})")
            steps.append(f"Step 3: Place decimal point: {correct_answer_str}")
            steps.append("")
            steps.append("  ✓ Decimal point placement is critical!")

        steps.append("")
        steps.append(f"Answer: {correct_answer_str} ✓")

        return steps

    def _generate_concise_steps(self, problem: Problem, num1: float, num2: float,
                                 operator: str, operation: str, correct_answer_str: str,
                                 is_word_problem: bool, word_problem_type: str) -> List[str]:
        """Generate concise steps with just formulas and values."""
        steps = [f"Problem: {problem.text}"]

        # For word problems, show extraction step
        if is_word_problem:
            steps.append(f"Equation: {num1} {operator} {num2}")

        if operation == 'addition':
            steps.append(f"{num1} + {num2}")
            steps.append(f"= {correct_answer_str}")

        elif operation == 'subtraction':
            steps.append(f"{num1} - {num2}")
            steps.append(f"= {correct_answer_str}")

        elif operation == 'division':
            steps.append(f"{num1} ÷ {num2}")
            steps.append(f"= {correct_answer_str}")

        else:  # multiplication
            steps.append(f"{num1} × {num2}")
            steps.append(f"= {correct_answer_str}")

        steps.append(correct_answer_str)

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the correct algorithm to solve the problem.

        Args:
            problem: The decimal arithmetic problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with correct answer and steps
        """
        # Check if this is a word problem
        is_word_problem = problem.metadata.get('is_word_problem', False)
        word_problem_type = problem.metadata.get('word_problem_type', None)

        num1 = problem.metadata['num1']
        num2 = problem.metadata['num2']
        operator = problem.metadata['operator']
        operation = problem.metadata['operation']

        # Calculate correct answer from the problem data (NOT from metadata)
        if operation == 'multiplication':
            correct_answer = round(num1 * num2, 2)
        elif operation == 'division':
            correct_answer = round(num1 / num2, 2) if num2 != 0 else 0
        elif operation == 'addition':
            correct_answer = round(num1 + num2, 2)
        elif operation == 'subtraction':
            correct_answer = round(num1 - num2, 2)
        else:
            correct_answer = round(num1 * num2, 2)

        # Format the answer appropriately
        correct_answer_str = str(correct_answer)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, num1, num2, operator, operation,
                                                  correct_answer_str, is_word_problem, word_problem_type)
        else:
            steps = self._generate_concise_steps(problem, num1, num2, operator, operation,
                                                  correct_answer_str, is_word_problem, word_problem_type)

        return Solution(
            answer=correct_answer_str,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
