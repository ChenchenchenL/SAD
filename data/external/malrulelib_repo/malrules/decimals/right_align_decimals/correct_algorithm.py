"""
Correct algorithm for decimal addition/subtraction.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class DecimalAdditionCorrectAlgorithm(CorrectAlgorithm):
    """
    Implements correct decimal addition/subtraction with proper alignment.
    """

    def get_name(self) -> str:
        return "Correct Decimal Addition/Subtraction"

    def get_description(self) -> str:
        return (
            "Correctly performs decimal operations by aligning numbers "
            "by their decimal points, maintaining proper place value."
        )

    def _generate_verbose_steps(self, problem: Problem, num1: float, num2: float,
                                 op_symbol: str, num3: float, answer_str: str,
                                 is_word_problem: bool, word_problem_type: str) -> List[str]:
        """Generate verbose, explanatory steps."""
        steps = []

        # For word problems, show extraction step
        if is_word_problem:
            steps.append(f"Word Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Extract the equation from the word problem")
            if word_problem_type == 'three_number_mixed':
                steps.append(f"  Equation: {num1} + {num2} - {num3}")
            else:
                steps.append(f"  Equation: {num1} {op_symbol} {num2}")
            steps.append("")
            steps.append("Step 2: Solve using proper decimal alignment")
            steps.append("")
        else:
            steps.append(f"Problem: {num1} {op_symbol} {num2}")
            steps.append("")

        # Get string representations
        num1_str = str(num1)
        num2_str = str(num2)

        steps.append("Step 1: Align by decimal point")
        steps.append(f"  IMPORTANT: Decimal points must line up vertically!")
        steps.append("")

        # Demonstrate correct alignment
        # Find decimal positions
        if '.' in num1_str:
            decimal_pos1 = num1_str.index('.')
        else:
            decimal_pos1 = len(num1_str)

        if '.' in num2_str:
            decimal_pos2 = num2_str.index('.')
        else:
            decimal_pos2 = len(num2_str)

        # Align by decimal point
        max_decimal_pos = max(decimal_pos1, decimal_pos2)

        # Add padding before decimal
        num1_display = ' ' * (max_decimal_pos - decimal_pos1) + num1_str
        num2_display = ' ' * (max_decimal_pos - decimal_pos2) + num2_str

        steps.append(f"  {num1_display}")
        steps.append(f"{op_symbol} {num2_display}")
        steps.append(f"  {'-' * max(len(num1_display), len(num2_display))}")
        steps.append("")

        # Optionally show with zeros padded
        # Equalize decimal places
        num1_parts = num1_str.split('.')
        num2_parts = num2_str.split('.')

        if len(num1_parts) == 1:
            num1_parts.append('')
        if len(num2_parts) == 1:
            num2_parts.append('')

        max_decimal_places = max(len(num1_parts[1]), len(num2_parts[1]))

        num1_decimal_padded = num1_parts[1].ljust(max_decimal_places, '0')
        num2_decimal_padded = num2_parts[1].ljust(max_decimal_places, '0')

        steps.append("Step 2: Pad with zeros if needed (for clarity)")
        steps.append(f"  {num1_parts[0]}.{num1_decimal_padded}")
        steps.append(f"{op_symbol} {num2_parts[0]}.{num2_decimal_padded}")
        steps.append("")

        # Perform operation
        if op_symbol == '+':
            result = round(num1 + num2, max_decimal_places)
            steps.append("Step 3: Add")
            steps.append(f"  {num1} + {num2} = {result}")
        else:
            result = round(num1 - num2, max_decimal_places)
            steps.append("Step 3: Subtract")
            steps.append(f"  {num1} - {num2} = {result}")

        steps.append("")
        steps.append(f"Final Answer: {answer_str} ✓")

        return steps

    def _generate_concise_steps(self, problem: Problem, num1: float, num2: float,
                                 op_symbol: str, num3: float, answer_str: str,
                                 is_word_problem: bool, word_problem_type: str) -> List[str]:
        """Generate concise steps with just formulas and values."""
        steps = [f"Problem: {problem.text}"]

        # For word problems, show extraction step
        if is_word_problem:
            if word_problem_type == 'three_number_mixed':
                steps.append(f"Equation: {num1} + {num2} - {num3}")
            else:
                steps.append(f"Equation: {num1} {op_symbol} {num2}")

        if num3 is not None:
            steps.append(f"{num1} + {num2} - {num3}")
            steps.append(f"= {answer_str}")
        else:
            if op_symbol == '+':
                steps.append(f"{num1} + {num2}")
            else:
                steps.append(f"{num1} - {num2}")
            steps.append(f"= {answer_str}")

        steps.append(answer_str)

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Correctly solve decimal addition/subtraction.

        Args:
            problem: Problem instance with decimal numbers
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with correct answer and detailed steps
        """
        # Check if this is a word problem
        is_word_problem = problem.metadata.get('is_word_problem', False)
        word_problem_type = problem.metadata.get('word_problem_type', None)

        # Calculate correct answer from problem data (NOT from metadata)
        num1 = problem.metadata['num1']
        num2 = problem.metadata['num2']
        op_symbol = problem.metadata['operation_symbol']
        num3 = problem.metadata.get('num3', None)

        # For three-number operations
        if num3 is not None:
            # Calculate num1 + num2 - num3
            result = round(num1 + num2 - num3, 2)
            answer_str = str(result)
        else:
            # Two-number operations
            num1_str = str(num1)
            num2_str = str(num2)

            num1_parts = num1_str.split('.')
            num2_parts = num2_str.split('.')

            if len(num1_parts) == 1:
                num1_parts.append('')
            if len(num2_parts) == 1:
                num2_parts.append('')

            max_decimal_places = max(len(num1_parts[1]), len(num2_parts[1]))

            if op_symbol == '+':
                result = round(num1 + num2, max_decimal_places)
            else:
                result = round(num1 - num2, max_decimal_places)
            answer_str = str(result)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, num1, num2, op_symbol, num3,
                                                  answer_str, is_word_problem, word_problem_type)
        else:
            steps = self._generate_concise_steps(problem, num1, num2, op_symbol, num3,
                                                  answer_str, is_word_problem, word_problem_type)

        return Solution(
            answer=answer_str,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
