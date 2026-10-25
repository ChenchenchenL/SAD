"""
Malrule algorithm for PEMDAS-Strictly-Sequential error.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class PEMDASStrictlySequentialMalrule(Malrule):
    """
    Students treat PEMDAS as 6 separate sequential steps.

    They do ALL multiplication before ANY division, and ALL addition before ANY subtraction,
    instead of understanding M/D are equal priority (left-to-right) and A/S are equal priority.
    """

    def get_name(self) -> str:
        return "PEMDAS-Strictly-Sequential"

    def get_description(self) -> str:
        return (
            "Students treat PEMDAS as a strict six-step sequence rather than understanding "
            "it as four priority levels. Research shows 'for many students, PEMDAS implies "
            "that the order of operations consists of six steps, one for each letter of the "
            "acronym' when 'in fact, the order of operations consists of four steps' (Glidden, 2008)."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Parse and compute using malrule logic
        expression = problem.metadata['expression']
        return self._compute_malrule_answer(expression)[0]

    def _parse_expression(self, expression: str):
        """Parse expression into operands and operations."""
        parts = expression.split()
        operands = []
        operations = []

        for i, part in enumerate(parts):
            if i % 2 == 0:  # Even indices are operands
                try:
                    # Try to parse as number (could be int or float)
                    if '.' in part:
                        operands.append(float(part))
                    else:
                        operands.append(int(part))
                except ValueError:
                    operands.append(part)
            else:  # Odd indices are operations
                operations.append(part)

        return operands, operations

    def _compute_malrule_answer(self, expression: str):
        """
        Compute answer using malrule logic.

        Malrule: Process operations in strict order: ×, ÷, +, -
        Within each type, process left-to-right.

        Returns: (answer, computation_steps)
        """
        operands, operations = self._parse_expression(expression)

        # Make copies to avoid mutating original
        operands = list(operands)
        operations = list(operations)

        steps = []
        step_num = 1

        # Process in malrule order: ×, ÷, +, -
        operation_order = ['×', '÷', '+', '-']

        for op_type in operation_order:
            # Keep processing operations of this type until none remain
            i = 0
            while i < len(operations):
                if operations[i] == op_type:
                    # Apply this operation
                    left = operands[i]
                    right = operands[i + 1]

                    if op_type == '×':
                        result = left * right
                    elif op_type == '÷':
                        result = left / right
                    elif op_type == '+':
                        result = left + right
                    else:  # '-'
                        result = left - right

                    # Record step
                    steps.append((step_num, f"{left} {op_type} {right} = {result}"))
                    step_num += 1

                    # Replace operands[i] and operands[i+1] with result
                    operands = operands[:i] + [result] + operands[i+2:]
                    # Remove this operation
                    operations = operations[:i] + operations[i+1:]

                    # Don't increment i, check same position again
                else:
                    i += 1

        # Final answer should be the only remaining operand
        answer = operands[0] if operands else 0

        # Convert to int if it's a whole number
        if isinstance(answer, float) and answer == int(answer):
            answer = int(answer)

        return answer, steps

    def generate_verbose_steps(self, problem: Problem, expression: str) -> tuple:
        """
        Generate verbose steps with full explanations.

        Args:
            problem: The problem instance
            expression: The mathematical expression

        Returns:
            Tuple of (steps list, malrule_answer)
        """
        problem_type = problem.metadata['problem_type']

        steps = []
        steps.append(f"Problem: {expression}")
        steps.append("")
        steps.append("MALRULE: Strict PEMDAS sequence")

        if problem_type == 'mult_div':
            steps.append("  MALRULE REASONING: 'PEMDAS says M comes before D'")
            steps.append("  'Do ALL multiplication first, THEN division'")
        elif problem_type == 'add_sub':
            steps.append("  MALRULE REASONING: 'PEMDAS says A comes before S'")
            steps.append("  'Do ALL addition first, THEN subtraction'")
        elif problem_type == 'mixed':
            steps.append("  MALRULE REASONING: 'PEMDAS is strict: P-E-M-D-A-S'")
            steps.append("  'Do ALL M, then ALL D, then ALL A, then ALL S'")
        else:
            steps.append("  MALRULE REASONING: Strict sequential PEMDAS")

        steps.append("")

        # Compute using malrule
        malrule_answer, computation_steps = self._compute_malrule_answer(expression)

        # Add computation steps
        for step_num, step_text in computation_steps:
            steps.append(f"Step {step_num}: {step_text}")

        steps.append("")
        steps.append(f"Final Answer: {malrule_answer} (INCORRECT - wrong order!)")

        return steps, malrule_answer

    def generate_concise_steps(self, problem: Problem, expression: str) -> tuple:
        """
        Generate concise steps with only formulas and values.

        Args:
            problem: The problem instance
            expression: The mathematical expression

        Returns:
            Tuple of (steps list, malrule_answer)
        """
        steps = []

        # Add question
        steps.append(problem.text)

        # Add formula extraction for word problems
        template = problem.metadata.get('template', 'basic')
        if template == 'word_problem':
            steps.append(f"{expression}")

        # Compute using malrule
        malrule_answer, computation_steps = self._compute_malrule_answer(expression)

        # Add computation steps (just the formulas)
        for step_num, step_text in computation_steps:
            steps.append(step_text)

        steps.append(str(malrule_answer))

        return steps, malrule_answer

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        expression = problem.metadata['expression']

        # Use helper functions based on verbose flag
        if verbose:
            steps, malrule_answer = self.generate_verbose_steps(problem, expression)
        else:
            steps, malrule_answer = self.generate_concise_steps(problem, expression)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
