"""
Strict-Left-To-Right malrule algorithm.

Implements the systematic error of evaluating expressions strictly from
left to right, ignoring operator precedence.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List

class StrictLeftToRightMalrule(Malrule):
    """
    Implements the Strict-Left-To-Right bug.

    Students evaluate expressions from left to right regardless of operator
    precedence. For example: 3 + 4 × 2 = (3 + 4) × 2 = 14 instead of
    3 + (4 × 2) = 11.

    This is the most common order of operations error, affecting ~50% of students.
    """

    def get_name(self) -> str:
        return "Strict-Left-To-Right"

    def get_description(self) -> str:
        return (
            "Students evaluate arithmetic expressions strictly from left to right, "
            "ignoring operator precedence rules (PEMDAS/BODMAS). They perform operations "
            "in the order they appear, treating all operators as having equal priority. "
            "Research shows students 'found the result of the arithmetic expression by "
            "performing operations from left to right without paying attention to the "
            "order of operations' (Tabak, 2019)."
        )

    def calculate_expected_answer(self, problem: Problem) -> str:
        """
        Calculate the expected incorrect answer for this malrule.

        Uses metadata when available.

        Args:
            problem: Order of operations problem

        Returns:
            Expected incorrect answer as string
        """

        # Backwards compatibility
        operands = problem.operands
        operations = problem.metadata['operations']

        # Evaluate left-to-right (MALRULE)
        result = operands[0]

        for i, operation in enumerate(operations):
            next_operand = operands[i + 1]

            if operation == '+':
                result = result + next_operand
            elif operation == '-':
                result = result - next_operand
            elif operation == '×':
                result = result * next_operand
            elif operation == '÷':
                result = result // next_operand  # Integer division

        return str(result)

    def _evaluate_left_to_right(self, expression: str) -> float:
        """Evaluate expression strictly left-to-right."""
        # Parse and evaluate left-to-right
        # Handle simple cases with 3 operands and 2 operations
        tokens = expression.replace('×', '*').replace('÷', '/').split()

        result = float(tokens[0])
        i = 1
        while i < len(tokens):
            op = tokens[i]
            operand = float(tokens[i + 1])

            if op == '+':
                result = result + operand
            elif op == '-':
                result = result - operand
            elif op == '*':
                result = result * operand
            elif op == '/':
                result = result / operand

            i += 2

        return result

    def generate_verbose_steps(self, problem: Problem, expression: str, template: str) -> tuple:
        """
        Generate verbose steps with full explanations.

        Args:
            problem: The problem instance
            expression: The mathematical expression
            template: The template type

        Returns:
            Tuple of (steps list, malrule_answer)
        """
        # Get malrule answer from metadata if available
        if 'malrule_answer' in problem.metadata:
            malrule_answer = str(problem.metadata['malrule_answer'])
        else:
            malrule_answer = self.calculate_expected_answer(problem)

        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append(f"Expression: {expression}")
        steps.append("MALRULE: Evaluate from left to right (ignoring precedence)")
        steps.append("")

        # Parse the expression
        operands = problem.operands
        operations = problem.metadata['operations']

        # Evaluate left-to-right for any number of operations
        result = operands[0]

        for i, operation in enumerate(operations):
            next_operand = operands[i + 1]
            steps.append(f"Step {i + 1}: {result} {operation} {next_operand}")

            if operation == '+':
                result = result + next_operand
            elif operation == '-':
                result = result - next_operand
            elif operation == '×':
                result = result * next_operand
            elif operation == '÷':
                result = result // next_operand  # Integer division

            steps.append(f"  = {result}")

        steps.append("")
        steps.append(f"Final answer: {malrule_answer} ✗ (INCORRECT)")

        return steps, malrule_answer

    def generate_concise_steps(self, problem: Problem, expression: str, template: str) -> tuple:
        """
        Generate concise steps with only formulas and values.

        Args:
            problem: The problem instance
            expression: The mathematical expression
            template: The template type

        Returns:
            Tuple of (steps list, malrule_answer)
        """
        # Get malrule answer from metadata if available
        if 'malrule_answer' in problem.metadata:
            malrule_answer = str(problem.metadata['malrule_answer'])
        else:
            malrule_answer = self.calculate_expected_answer(problem)

        steps = []

        # Add question
        steps.append(problem.text)

        # Add formula extraction for word problems
        if template == 'word_problem':
            steps.append(f"{expression}")

        # Parse the expression
        operands = problem.operands
        operations = problem.metadata['operations']

        # Evaluate left-to-right for any number of operations
        result = operands[0]

        for i, operation in enumerate(operations):
            next_operand = operands[i + 1]
            old_result = result

            if operation == '+':
                result = result + next_operand
            elif operation == '-':
                result = result - next_operand
            elif operation == '×':
                result = result * next_operand
            elif operation == '÷':
                result = result // next_operand  # Integer division

            steps.append(f"{old_result} {operation} {next_operand} = {result}")

        steps.append(str(malrule_answer))

        return steps, malrule_answer

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Strict-Left-To-Right malrule.

        Args:
            problem: Order of operations problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with left-to-right evaluation
        """
        template = problem.metadata.get('template', 'add_mult')
        expression = problem.metadata['expression']

        # Use helper functions based on verbose flag
        if verbose:
            steps, malrule_answer = self.generate_verbose_steps(problem, expression, template)
        else:
            steps, malrule_answer = self.generate_concise_steps(problem, expression, template)

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
