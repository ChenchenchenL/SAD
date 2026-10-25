"""
Malrule algorithm for Negative-Swaps-Operation error.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

# Helper functions are defined as methods within the class below

class NegativeSwapsOperationMalrule(Malrule):
    """
    Students think negative sign changes the operation.

    Example: 5 - (-3) → Student thinks negative swaps operation, so becomes 5 + 3... wait, or 5 - 3?
    Confusion about whether negative changes the operation or is part of number.
    """

    def get_name(self) -> str:
        return "Negative-Swaps-Operation (Sign-Operation Confusion)"

    def get_description(self) -> str:
        return (
            "Students confuse the negative sign's role as a number property with the operation "
            "being performed, leading to incorrect operation swapping. Vlassis (2004) identifies "
            "this as a failure to distinguish between the 'operative sign' (the operation: +, -) "
            "and the 'unary, predicative sign' (the negative property of a number). Students "
            "incorrectly believe that encountering a negative sign somehow changes the operation "
            "they should perform, rather than understanding it as a property of the operand."
        )

    def _generate_concise_steps(self, problem: Problem, template: str,
                                 malrule_answer: Any, intermediate_data: Dict[str, Any]) -> List[str]:
        """
        Generate concise steps for the malrule solution.

        Format: [Question, step (formula/values only), ..., answer]
        """
        steps = []

        # Question
        steps.append(f"Question: {problem.text}")

        operation_type = intermediate_data.get('operation_type', 'add_negative')
        num1 = intermediate_data.get('num1')
        num2 = intermediate_data.get('num2')

        if template == 'comparison_problem':
            steps.append(f"Negative with - stays -")
            steps.append(f"Result: {malrule_answer}")
        elif operation_type == 'add_negative':
            steps.append(f"{num1} + ({num2})")
            steps.append(f"Negative swaps + to +: {num1} + {abs(num2)} = {malrule_answer}")
        else:  # subtract_negative
            steps.append(f"{num1} - ({num2})")
            steps.append(f"Negative keeps -: {num1} - {abs(num2)} = {malrule_answer}")

        # Final answer
        steps.append(f"Answer: {malrule_answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, template: str,
                                 malrule_answer: Any, intermediate_data: Dict[str, Any]) -> List[str]:
        """
        Generate verbose steps for the malrule solution (original step structure).
        """
        steps = []

        operation_type = intermediate_data.get('operation_type', 'add_negative')
        num1 = intermediate_data.get('num1')
        num2 = intermediate_data.get('num2')
        operator = intermediate_data.get('operator', '+')

        if template == 'comparison_problem':
            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("MALRULE: Negative sign swaps the operation")
            steps.append(f"Result: {malrule_answer}")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} ✗ (INCORRECT)")
            return steps

        steps.append(f"Problem: {num1} {operator} ({num2})")
        steps.append("")
        steps.append("MALRULE: Negative sign swaps the operation")

        if operation_type == 'add_negative':
            steps.append(f"  MALRULE REASONING: 'Negative with + makes it -'")
            steps.append(f"  'So {num1} + (-{abs(num2)}) becomes {num1} - and negative swaps back to +'")
            steps.append(f"  Result: {num1} + {abs(num2)} = {malrule_answer}")
        else:  # subtract_negative
            steps.append(f"  MALRULE REASONING: 'Negative with - stays -'")
            steps.append(f"  'So {num1} - (-{abs(num2)}) becomes {num1} - {abs(num2)}'")
            steps.append(f"  Result: {num1} - {abs(num2)} = {malrule_answer}")

        steps.append("")
        steps.append(f"Final Answer: {malrule_answer} ✗ (INCORRECT)")

        return steps

    def calculate_expected_answer(self, problem: Problem):
        """
        Calculate the expected malrule answer (incorrect) for this problem.

        COMPUTES the answer by applying the malrule logic, never uses metadata.
        Malrule: Student thinks negative swaps operation.
        - For a + (-b): student thinks negative with + makes it +, so a + b
        - For a - (-b): student thinks negative with - stays -, so a - b
        """
        operands = problem.operands
        operator = problem.metadata.get('operator', '+')
        operation_type = problem.metadata.get('operation_type', 'add_negative')

        if len(operands) >= 2:
            num1, num2 = operands[0], operands[1]
            if operation_type == 'add_negative':
                # a + (-b), student thinks: negative swaps +, so becomes a + b
                malrule_answer = num1 + abs(num2)
            else:  # subtract_negative
                # a - (-b), student thinks: negative keeps -, so becomes a - b
                malrule_answer = num1 - abs(num2)
        else:
            malrule_answer = operands[0]

        return malrule_answer

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Negative-Swaps-Operation malrule.

        Args:
            problem: Problem instance
            verbose: If True, generate verbose steps; if False (default), generate concise steps

        Returns:
            Solution with incorrect answer
        """
        template = problem.metadata.get('template', 'basic_arithmetic')
        operands = problem.operands
        operator = problem.metadata.get('operator', '+')
        operation_type = problem.metadata.get('operation_type', 'add_negative')

        # COMPUTE the malrule answer - never use metadata
        malrule_answer = self.calculate_expected_answer(problem)

        if len(operands) >= 2:
            num1, num2 = operands[0], operands[1]
        else:
            num1 = operands[0]
            num2 = 0

        intermediate_data = {
            'num1': num1,
            'num2': num2,
            'operator': operator,
            'operation_type': operation_type
        }

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, template, malrule_answer, intermediate_data)
        else:
            steps = self._generate_concise_steps(problem, template, malrule_answer, intermediate_data)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
