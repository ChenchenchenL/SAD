"""
Correct algorithm for negative number arithmetic.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List, Dict, Any

import sympy as sp

from utils import CorrectAlgorithm, Problem, Solution


class NegativeArithmeticCorrectAlgorithm(CorrectAlgorithm):
    """Correctly performs arithmetic with negative numbers."""

    def get_name(self) -> str:
        return "Correct Negative Number Arithmetic"

    def get_description(self) -> str:
        return "Correctly handles arithmetic with negative numbers."

    def _generate_concise_steps(self, problem: Problem, template: str,
                                 correct_answer: Any, intermediate_data: Dict[str, Any]) -> List[str]:
        """
        Generate concise steps for the solution.

        Format: [Question, step (formula/values only), ..., answer]
        """
        steps = []

        # Question
        steps.append(f"Question: {problem.text}")

        operation_type = intermediate_data.get('operation_type', 'add_negative')
        num1 = intermediate_data.get('num1')
        num2 = intermediate_data.get('num2')

        if template == 'comparison_problem':
            steps.append(f"Evaluate both expressions")
            steps.append(f"Result: {correct_answer}")
        elif operation_type == 'add_negative':
            steps.append(f"{num1} + ({num2})")
            steps.append(f"{num1} + ({num2}) = {num1} - {abs(num2)}")
            steps.append(f"Result: {correct_answer}")
        else:  # subtract_negative
            steps.append(f"{num1} - ({num2})")
            steps.append(f"{num1} - ({num2}) = {num1} + {abs(num2)}")
            steps.append(f"Result: {correct_answer}")

        # Final answer
        steps.append(f"Answer: {correct_answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, template: str,
                                 correct_answer: Any, intermediate_data: Dict[str, Any]) -> List[str]:
        """
        Generate verbose steps for the solution (original step structure).
        """
        steps = []

        operation_type = intermediate_data.get('operation_type', 'add_negative')
        num1 = intermediate_data.get('num1')
        num2 = intermediate_data.get('num2')
        operator = intermediate_data.get('operator', '+')

        if template == 'comparison_problem':
            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("Correct approach: Evaluate both expressions")
            steps.append(f"Result: {correct_answer}")
            return steps

        steps.append(f"Problem: {num1} {operator} ({num2})")
        steps.append("")

        if operation_type == 'add_negative':
            steps.append(f"Adding a negative number:")
            steps.append(f"  {num1} + (-{abs(num2)}) = {num1} - {abs(num2)}")
            steps.append("")
            steps.append("Rule: Adding a negative = Subtracting the positive")
            steps.append(f"  {num1} - {abs(num2)} = {correct_answer}")
        else:  # subtract_negative
            steps.append(f"Subtracting a negative number:")
            steps.append(f"  {num1} - (-{abs(num2)}) = {num1} + {abs(num2)}")
            steps.append("")
            steps.append("Rule: Subtracting a negative = Adding the positive")
            steps.append(f"  {num1} + {abs(num2)} = {correct_answer}")

        steps.append("")
        steps.append(f"Final Answer: {correct_answer} ✓")
        steps.append("")
        steps.append("Key: Negative is part of the NUMBER, not the operation")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct negative number arithmetic.

        Args:
            problem: Problem instance
            verbose: If True, generate verbose steps; if False (default), generate concise steps

        Returns:
            Solution with correct answer
        """
        # Handle comparison_problem template specially
        template = problem.metadata.get('template', 'basic_arithmetic')

        operands = problem.operands
        operator = problem.metadata.get('operator', '+')
        operation_type = problem.metadata.get('operation_type', 'add_negative')

        # COMPUTE the correct answer from operands - never use metadata
        if template == 'comparison_problem':
            correct_answer = problem.metadata['correct_answer']
            num1, num2 = None, None
        elif template == 'multi_step_expression':
            # The expression has three signed operands; evaluate the whole text
            # instead of stopping after the first two operands.
            expression = problem.text.split(':', 1)[-1].strip()
            correct_answer = int(sp.sympify(expression))
            num1, num2 = operands[0], operands[1]
        elif len(operands) >= 2:
            num1, num2 = operands[0], operands[1]
            if operator == '+':
                correct_answer = num1 + num2
            else:  # operator == '-'
                correct_answer = num1 - num2
        else:
            num1 = operands[0]
            num2 = 0
            correct_answer = num1

        intermediate_data = {
            'num1': num1,
            'num2': num2,
            'operator': operator,
            'operation_type': operation_type
        }

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, template, correct_answer, intermediate_data)
        else:
            steps = self._generate_concise_steps(problem, template, correct_answer, intermediate_data)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
