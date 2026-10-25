"""
Malrule algorithm for Ignore-Parentheses error.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class IgnoreParenthesesMalrule(Malrule):
    """
    Implements the Ignore-Parentheses malrule.

    Students ignore parentheses and evaluate left-to-right or
    apply PEMDAS without doing parentheses first.

    Example: 2 × (3 + 4)
    Correct: 2 × 7 = 14
    Malrule: 2 × 3 + 4 = 10 (ignores parentheses)
    """

    def get_name(self) -> str:
        return "Ignore-Parentheses"

    def get_description(self) -> str:
        return (
            "Students ignore parentheses and evaluate left-to-right or apply PEMDAS "
            "without respecting grouping symbols. Research shows students 'stated that "
            "only operations in brackets need to be performed first' without understanding "
            "that parentheses override all other precedence rules (Tabak, 2019)."
        )

    def calculate_expected_answer(self, problem: Problem) -> float:
        """
        Calculate the expected incorrect answer for this malrule.

        For Ignore-Parentheses:
        - Student ignores parentheses and evaluates left-to-right
        - MALRULE: Evaluate expressions left-to-right, ignoring all grouping symbols

        Example: 2 × (3 + 4)
        - Correct: 2 × 7 = 14
        - MALRULE: (2 × 3) + 4 = 6 + 4 = 10

        Example: 2 × (3 + (4 - 1))
        - Correct: 2 × (3 + 3) = 2 × 6 = 12
        - MALRULE: 2 × 3 + 4 - 1 = 6 + 4 - 1 = 9

        Args:
            problem: Order of operations problem with parentheses

        Returns:
            Expected incorrect answer as float
        """
        template = problem.metadata.get('template', 'basic_single_parentheses')

        if template == 'basic_single_parentheses':
            a = problem.metadata['a']
            b = problem.metadata['b']
            c = problem.metadata['c']
            op1 = problem.metadata['op1']
            op2 = problem.metadata['op2']

            # MALRULE: Evaluate left-to-right, ignoring parentheses
            # Step 1: a op1 b
            first_result = self._evaluate_op(a, b, op1)
            # Step 2: (result) op2 c
            result = self._evaluate_op(first_result, c, op2)
            return result

        elif template in ['nested_parentheses', 'multiple_parentheses', 'brackets_and_parentheses']:
            # For these templates, evaluate left-to-right with all values and operations
            values = problem.metadata['values']
            operations = problem.metadata['operations']

            # Start with first value
            result = values[0]

            # Apply operations left-to-right
            for i, op in enumerate(operations):
                result = self._evaluate_op(result, values[i + 1], op)

            return result

        elif template == 'word_problem':
            values = problem.metadata['values']
            operations = problem.metadata['operations']

            # Start with first value
            result = values[0]

            # Apply operations left-to-right
            for i, op in enumerate(operations):
                result = self._evaluate_op(result, values[i + 1], op)

            return result

        else:
            # Fallback to old behavior
            a = problem.metadata.get('a', 0)
            b = problem.metadata.get('b', 0)
            c = problem.metadata.get('c', 0)
            op1 = problem.metadata.get('op1', '+')
            op2 = problem.metadata.get('op2', '+')

            first_result = self._evaluate_op(a, b, op1)
            result = self._evaluate_op(first_result, c, op2)
            return result

    def generate_verbose_steps(self, problem: Problem, expression: str, template: str) -> tuple:
        """
        Generate verbose steps with full explanations.

        Args:
            problem: The problem instance
            expression: The mathematical expression
            template: The template type

        Returns:
            Tuple of (steps list, final_answer)
        """
        steps = []
        steps.append(f"Problem: {expression}")
        steps.append("")
        steps.append("MALRULE: Ignore parentheses/brackets, evaluate left-to-right")
        steps.append(f"  MALRULE REASONING: 'Grouping symbols don't matter, just go left to right'")
        steps.append(f"  (WRONG! Grouping symbols must be done first!)")
        steps.append("")

        if template == 'basic_single_parentheses':
            a = problem.metadata['a']
            b = problem.metadata['b']
            c = problem.metadata['c']
            op1 = problem.metadata['op1']
            op2 = problem.metadata['op2']

            # Evaluate without respecting parentheses - just left to right
            steps.append(f"Step 1: {a} {op1} {b}")
            first_result = self._evaluate_op(a, b, op1)
            steps.append(f"  = {first_result}")
            steps.append("")

            steps.append(f"Step 2: {first_result} {op2} {c}")
            result = self._evaluate_op(first_result, c, op2)
            steps.append(f"  = {result}")
            steps.append("")

        elif template in ['nested_parentheses', 'multiple_parentheses', 'brackets_and_parentheses', 'word_problem']:
            values = problem.metadata['values']
            operations = problem.metadata['operations']

            # Evaluate left-to-right
            result = values[0]
            steps.append(f"Starting value: {result}")
            steps.append("")

            for i, op in enumerate(operations):
                next_val = values[i + 1]
                steps.append(f"Step {i+1}: {result} {op} {next_val}")
                result = self._evaluate_op(result, next_val, op)
                steps.append(f"  = {result}")
                steps.append("")

        else:
            # Fallback
            result = self.calculate_expected_answer(problem)
            steps.append(f"Calculated result: {result}")
            steps.append("")

        steps.append(f"Final Answer: {result} (INCORRECT - ignored grouping symbols!)")

        return steps, result

    def generate_concise_steps(self, problem: Problem, expression: str, template: str) -> tuple:
        """
        Generate concise steps with only formulas and values.

        Args:
            problem: The problem instance
            expression: The mathematical expression
            template: The template type

        Returns:
            Tuple of (steps list, final_answer)
        """
        steps = []

        # Add question
        steps.append(problem.text)

        # Add formula extraction for word problems
        if template == 'word_problem':
            steps.append(f"{expression}")

        if template == 'basic_single_parentheses':
            a = problem.metadata['a']
            b = problem.metadata['b']
            c = problem.metadata['c']
            op1 = problem.metadata['op1']
            op2 = problem.metadata['op2']

            # Evaluate without respecting parentheses - just left to right
            first_result = self._evaluate_op(a, b, op1)
            steps.append(f"{a} {op1} {b} = {first_result}")

            result = self._evaluate_op(first_result, c, op2)
            steps.append(f"{first_result} {op2} {c} = {result}")

        elif template in ['nested_parentheses', 'multiple_parentheses', 'brackets_and_parentheses', 'word_problem']:
            values = problem.metadata['values']
            operations = problem.metadata['operations']

            # Evaluate left-to-right
            result = values[0]

            for i, op in enumerate(operations):
                next_val = values[i + 1]
                old_result = result
                result = self._evaluate_op(result, next_val, op)
                steps.append(f"{old_result} {op} {next_val} = {result}")

        else:
            # Fallback
            result = self.calculate_expected_answer(problem)

        steps.append(str(result))

        return steps, result

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        expression = problem.metadata['expression']
        template = problem.metadata.get('template', 'basic_single_parentheses')

        # Use helper functions based on verbose flag
        if verbose:
            steps, result = self.generate_verbose_steps(problem, expression, template)
        else:
            steps, result = self.generate_concise_steps(problem, expression, template)

        return Solution(
            answer=result,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _evaluate_op(self, x, y, op):
        if op == '+':
            return x + y
        elif op == '-':
            return x - y
        elif op == '×':
            return x * y
        elif op == '÷':
            return round(x / y, 2) if y != 0 else 0
        return 0
