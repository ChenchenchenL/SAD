"""
Correct algorithm for order of operations.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class OrderOfOperationsCorrectAlgorithm(CorrectAlgorithm):
    """Correctly applies order of operations with left-to-right for equal priority."""

    def get_name(self) -> str:
        return "Correct Order of Operations"

    def get_description(self) -> str:
        return "Correctly applies order of operations: M/D are equal priority (left-to-right), A/S are equal priority (left-to-right)."

    def _evaluate_with_pemdas_verbose(self, operands, operations, steps):
        """Evaluate expression with PEMDAS rules (verbose output)."""
        operands = list(operands)  # Make a copy
        operations = list(operations)  # Make a copy

        step_num = 1

        # First pass: multiplication and division (left-to-right)
        i = 0
        while i < len(operations):
            if operations[i] in ['×', '÷']:
                steps.append(f"Step {step_num}: {operands[i]} {operations[i]} {operands[i+1]}")

                if operations[i] == '×':
                    result = operands[i] * operands[i + 1]
                else:  # ÷
                    result = operands[i] / operands[i + 1]

                steps.append(f"  = {result}")

                # Replace the two operands and operation with the result
                operands = operands[:i] + [result] + operands[i+2:]
                operations = operations[:i] + operations[i+1:]
                step_num += 1
                # Don't increment i, check same position again
            else:
                i += 1

        # Second pass: addition and subtraction (left-to-right)
        i = 0
        while i < len(operations):
            steps.append(f"Step {step_num}: {operands[i]} {operations[i]} {operands[i+1]}")

            if operations[i] == '+':
                result = operands[i] + operands[i + 1]
            else:  # -
                result = operands[i] - operands[i + 1]

            steps.append(f"  = {result}")

            # Replace the two operands and operation with the result
            operands = operands[:i] + [result] + operands[i+2:]
            operations = operations[:i] + operations[i+1:]
            step_num += 1
            # Don't increment i, check same position again

        return operands[0]

    def _evaluate_with_pemdas_concise(self, operands, operations, steps):
        """Evaluate expression with PEMDAS rules (concise output)."""
        operands = list(operands)  # Make a copy
        operations = list(operations)  # Make a copy

        # First pass: multiplication and division (left-to-right)
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

        # Second pass: addition and subtraction (left-to-right)
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

        return operands[0]

    def generate_verbose_steps(self, problem: Problem, expression: str, template: str) -> tuple:
        """
        Generate verbose steps with full explanations.

        Args:
            problem: The problem instance
            expression: The mathematical expression
            template: The template type

        Returns:
            Tuple of (steps list, result)
        """
        problem_type = problem.metadata['problem_type']

        steps = []
        steps.append(f"Problem: {expression}")
        steps.append("")
        steps.append("Rule: Operations of equal priority are evaluated LEFT TO RIGHT")

        # Parse expression parts
        parts = expression.split()
        operands = []
        operations = []

        for i, part in enumerate(parts):
            if i % 2 == 0:  # Even indices are operands
                operands.append(int(part))
            else:  # Odd indices are operations
                operations.append(part)

        if template in ['longer_expressions', 'mixed_operations']:
            # Handle complex expressions with PEMDAS
            steps.append("")
            if problem_type == 'mult_div':
                steps.append("  Multiplication and Division have EQUAL priority (left-to-right)")
            else:
                # For mixed operations, handle M/D first, then A/S
                steps.append("  Multiplication/Division first (left-to-right), then Addition/Subtraction")

            result = self._evaluate_with_pemdas_verbose(operands, operations, steps)

        elif problem_type == 'mult_div':
            steps.append("  Multiplication and Division have EQUAL priority")
            steps.append("")

            steps.append(f"Step 1: Work left to right")
            result = operands[0] / operands[1]
            steps.append(f"  First operation: {operands[0]} ÷ {operands[1]} = {result}")
            steps.append("")
            steps.append(f"Step 2: Continue left to right")
            result = result * operands[2]
            # Convert to int if whole number
            if result == int(result):
                result = int(result)
            steps.append(f"  {operands[0] / operands[1]} × {operands[2]} = {result}")

        else:  # add_sub
            steps.append("  Addition and Subtraction have EQUAL priority")
            steps.append("")

            steps.append(f"Step 1: Work left to right")
            result = operands[0] - operands[1]
            steps.append(f"  First operation: {operands[0]} - {operands[1]} = {result}")
            steps.append("")
            steps.append(f"Step 2: Continue left to right")
            result = result + operands[2]
            steps.append(f"  {operands[0] - operands[1]} + {operands[2]} = {result}")

        # Ensure result is int if it's a whole number
        if isinstance(result, float) and result == int(result):
            result = int(result)

        steps.append("")
        steps.append(f"Final Answer: {result} ✓")
        steps.append("")
        steps.append("Key: PEMDAS should be thought of as PE-MD-AS (3 groups)")
        steps.append("     Within each group, work LEFT TO RIGHT")

        return steps, result

    def generate_concise_steps(self, problem: Problem, expression: str, template: str) -> tuple:
        """
        Generate concise steps with only formulas and values.

        Args:
            problem: The problem instance
            expression: The mathematical expression
            template: The template type

        Returns:
            Tuple of (steps list, result)
        """
        problem_type = problem.metadata['problem_type']

        steps = []

        # Add question
        steps.append(problem.text)

        # Add formula extraction for word problems
        if template == 'word_problem':
            steps.append(f"{expression}")

        # Parse expression parts
        parts = expression.split()
        operands = []
        operations = []

        for i, part in enumerate(parts):
            if i % 2 == 0:  # Even indices are operands
                operands.append(int(part))
            else:  # Odd indices are operations
                operations.append(part)

        if template in ['longer_expressions', 'mixed_operations']:
            # Handle complex expressions with PEMDAS
            result = self._evaluate_with_pemdas_concise(operands, operations, steps)

        elif problem_type == 'mult_div':
            result = operands[0] / operands[1]
            steps.append(f"{operands[0]} ÷ {operands[1]} = {result}")
            old_result = result
            result = result * operands[2]
            # Convert to int if whole number
            if result == int(result):
                result = int(result)
            steps.append(f"{old_result} × {operands[2]} = {result}")

        else:  # add_sub
            result = operands[0] - operands[1]
            steps.append(f"{operands[0]} - {operands[1]} = {result}")
            old_result = result
            result = result + operands[2]
            steps.append(f"{old_result} + {operands[2]} = {result}")

        # Ensure result is int if it's a whole number
        if isinstance(result, float) and result == int(result):
            result = int(result)

        steps.append(str(result))

        return steps, result

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        expression = problem.metadata['expression']
        template = problem.metadata.get('template', 'basic')

        # Use helper functions based on verbose flag
        if verbose:
            steps, result = self.generate_verbose_steps(problem, expression, template)
        else:
            steps, result = self.generate_concise_steps(problem, expression, template)

        return Solution(
            answer=result,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
