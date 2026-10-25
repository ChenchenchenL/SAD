"""
Correct order of operations algorithm.

Implements proper PEMDAS/BODMAS evaluation.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import CorrectAlgorithm, Problem, Solution


class OrderOfOperationsCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for order of operations.

    Follows PEMDAS/BODMAS: Multiplication and Division before Addition and Subtraction.
    """

    def get_name(self) -> str:
        return "Correct Order of Operations (PEMDAS/BODMAS)"

    def get_description(self) -> str:
        return (
            "Evaluates expressions using correct operator precedence: "
            "Multiplication and Division (left-to-right), then Addition and Subtraction (left-to-right)."
        )

    def generate_verbose_steps(self, problem: Problem, expression: str, template: str) -> tuple:
        """
        Generate verbose steps with full explanations.

        Args:
            problem: The problem instance
            expression: The mathematical expression
            template: The template type

        Returns:
            Tuple of (steps list, correct_answer)
        """
        operands = list(problem.operands)  # Make a copy
        operations = list(problem.metadata['operations'])  # Make a copy

        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append(f"Expression: {expression}")
        steps.append("CORRECT METHOD: Using order of operations (PEMDAS/BODMAS)")
        steps.append("")

        # Handle expressions with any number of operations
        # First, do all multiplication and division (left-to-right)
        step_num = 1
        i = 0
        while i < len(operations):
            if operations[i] in ['×', '÷']:
                steps.append(f"Step {step_num}: Multiply/divide first - {operands[i]} {operations[i]} {operands[i+1]}")

                if operations[i] == '×':
                    result = operands[i] * operands[i + 1]
                else:  # ÷
                    result = operands[i] / operands[i + 1]

                steps.append(f"Result: {result}")

                # Replace the two operands and operation with the result
                operands = operands[:i] + [result] + operands[i+2:]
                operations = operations[:i] + operations[i+1:]
                step_num += 1
                # Don't increment i, check same position again
            else:
                i += 1

        # Now do all addition and subtraction (left-to-right)
        i = 0
        while i < len(operations):
            steps.append(f"Step {step_num}: {operands[i]} {operations[i]} {operands[i+1]}")

            if operations[i] == '+':
                result = operands[i] + operands[i + 1]
            else:  # -
                result = operands[i] - operands[i + 1]

            steps.append(f"Result: {result}")

            # Replace the two operands and operation with the result
            operands = operands[:i] + [result] + operands[i+2:]
            operations = operations[:i] + operations[i+1:]
            step_num += 1
            # Don't increment i, check same position again

        result = operands[0]

        # Convert to int if it's a whole number
        if isinstance(result, float) and result == int(result):
            result = int(result)

        correct_answer = str(result)
        steps.append("")
        steps.append(f"Final answer: {correct_answer} ✓")

        return steps, correct_answer

    def generate_concise_steps(self, problem: Problem, expression: str, template: str) -> tuple:
        """
        Generate concise steps with only formulas and values.

        Args:
            problem: The problem instance
            expression: The mathematical expression
            template: The template type

        Returns:
            Tuple of (steps list, correct_answer)
        """
        operands = list(problem.operands)  # Make a copy
        operations = list(problem.metadata['operations'])  # Make a copy

        steps = []

        # Add question
        steps.append(problem.text)

        # Add formula extraction for word problems
        if template == 'word_problem':
            steps.append(f"{expression}")

        # Handle expressions with any number of operations
        # First, do all multiplication and division (left-to-right)
        i = 0
        while i < len(operations):
            if operations[i] in ['×', '÷']:
                if operations[i] == '×':
                    result = operands[i] * operands[i + 1]
                else:  # ÷
                    result = operands[i] / operands[i + 1]

                steps.append(f"{operands[i]} {operations[i]} {operands[i+1]} = {result}")

                # Replace the two operands and operation with the result
                operands = operands[:i] + [result] + operands[i+2:]
                operations = operations[:i] + operations[i+1:]
                # Don't increment i, check same position again
            else:
                i += 1

        # Now do all addition and subtraction (left-to-right)
        i = 0
        while i < len(operations):
            if operations[i] == '+':
                result = operands[i] + operands[i + 1]
            else:  # -
                result = operands[i] - operands[i + 1]

            steps.append(f"{operands[i]} {operations[i]} {operands[i+1]} = {result}")

            # Replace the two operands and operation with the result
            operands = operands[:i] + [result] + operands[i+2:]
            operations = operations[:i] + operations[i+1:]
            # Don't increment i, check same position again

        result = operands[0]

        # Convert to int if it's a whole number
        if isinstance(result, float) and result == int(result):
            result = int(result)

        correct_answer = str(result)
        steps.append(correct_answer)

        return steps, correct_answer

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct order of operations.

        Args:
            problem: Order of operations problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with correct PEMDAS evaluation
        """
        template = problem.metadata.get('template', 'add_mult')
        expression = problem.metadata['expression']

        # Use helper functions based on verbose flag
        if verbose:
            steps, correct_answer = self.generate_verbose_steps(problem, expression, template)
        else:
            steps, correct_answer = self.generate_concise_steps(problem, expression, template)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
