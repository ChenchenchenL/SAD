"""
Correct algorithm for order of operations with parentheses.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class OrderOfOperationsCorrectAlgorithm(CorrectAlgorithm):
    """Implements correct order of operations respecting parentheses."""

    def get_name(self) -> str:
        return "Correct Order of Operations"

    def get_description(self) -> str:
        return "Correctly evaluates expressions by doing parentheses first, then following PEMDAS."

    def _evaluate_op(self, x, y, op):
        if op == '+':
            return x + y
        elif op == '-':
            return x - y
        elif op == '×':
            return x * y
        elif op == '÷':
            return x / y if y != 0 else 0
        return 0

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

        if template == 'basic_single_parentheses':
            values = problem.metadata.get('values', [problem.metadata['a'], problem.metadata['b'], problem.metadata['c']])
            operations = problem.metadata.get('operations', [problem.metadata['op1'], problem.metadata['op2']])
            a, b, c = values[0], values[1], values[2]
            op1, op2 = operations[0], operations[1]

            steps.append("Step 1: Evaluate parentheses FIRST")
            paren_result = self._evaluate_op(b, c, op2)
            steps.append(f"  ({b} {op2} {c}) = {paren_result}")
            steps.append("")

            steps.append("Step 2: Substitute and evaluate")
            steps.append(f"  {a} {op1} {paren_result}")
            result = self._evaluate_op(a, paren_result, op1)
            steps.append(f"  = {result}")
            steps.append("")

        elif template == 'nested_parentheses':
            values = problem.metadata['values']
            operations = problem.metadata['operations']
            a, b, c, d = values[0], values[1], values[2], values[3]
            op1, op2, op3 = operations[0], operations[1], operations[2]

            steps.append("Step 1: Evaluate INNERMOST parentheses first")
            inner_result = self._evaluate_op(c, d, op3)
            steps.append(f"  ({c} {op3} {d}) = {inner_result}")
            steps.append("")

            steps.append("Step 2: Evaluate next level of parentheses")
            middle_result = self._evaluate_op(b, inner_result, op2)
            steps.append(f"  ({b} {op2} {inner_result}) = {middle_result}")
            steps.append("")

            steps.append("Step 3: Final operation")
            result = self._evaluate_op(a, middle_result, op1)
            steps.append(f"  {a} {op1} {middle_result} = {result}")
            steps.append("")

        elif template == 'multiple_parentheses':
            values = problem.metadata['values']
            operations = problem.metadata['operations']
            a, b, c, d = values[0], values[1], values[2], values[3]
            op1, op2, op3 = operations[0], operations[1], operations[2]

            steps.append("Step 1: Evaluate left parentheses")
            left_result = self._evaluate_op(a, b, op1)
            steps.append(f"  ({a} {op1} {b}) = {left_result}")
            steps.append("")

            steps.append("Step 2: Evaluate right parentheses")
            right_result = self._evaluate_op(c, d, op3)
            steps.append(f"  ({c} {op3} {d}) = {right_result}")
            steps.append("")

            steps.append("Step 3: Combine results")
            result = self._evaluate_op(left_result, right_result, op2)
            steps.append(f"  {left_result} {op2} {right_result} = {result}")
            steps.append("")

        elif template == 'brackets_and_parentheses':
            values = problem.metadata['values']
            operations = problem.metadata['operations']
            a, b, c, d = values[0], values[1], values[2], values[3]
            op1, op2, op3 = operations[0], operations[1], operations[2]

            steps.append("Step 1: Evaluate innermost grouping (parentheses)")
            inner_result = self._evaluate_op(c, d, op3)
            steps.append(f"  ({c} {op3} {d}) = {inner_result}")
            steps.append("")

            steps.append("Step 2: Evaluate brackets")
            bracket_result = self._evaluate_op(b, inner_result, op2)
            steps.append(f"  [{b} {op2} {inner_result}] = {bracket_result}")
            steps.append("")

            steps.append("Step 3: Final operation")
            result = self._evaluate_op(a, bracket_result, op1)
            steps.append(f"  {a} {op1} {bracket_result} = {result}")
            steps.append("")

        elif template == 'word_problem':
            values = problem.metadata['values']
            operations = problem.metadata['operations']

            if len(values) == 3 and len(operations) == 2:
                expr = problem.metadata['expression']

                if expr.startswith('('):
                    a, b, c = values[0], values[1], values[2]
                    op2, op1 = operations[0], operations[1]

                    steps.append("Step 1: Evaluate parenthetical expression")
                    paren_result = self._evaluate_op(a, b, op2)
                    steps.append(f"  ({a} {op2} {b}) = {paren_result}")
                    steps.append("")

                    steps.append("Step 2: Complete calculation")
                    result = self._evaluate_op(paren_result, c, op1)
                    steps.append(f"  {paren_result} {op1} {c} = {result}")
                    steps.append("")
                else:
                    a, b, c = values[0], values[1], values[2]
                    op1, op2 = operations[0], operations[1]

                    steps.append("Step 1: Evaluate parenthetical expression")
                    paren_result = self._evaluate_op(b, c, op2)
                    steps.append(f"  ({b} {op2} {c}) = {paren_result}")
                    steps.append("")

                    steps.append("Step 2: Complete calculation")
                    result = self._evaluate_op(a, paren_result, op1)
                    steps.append(f"  {a} {op1} {paren_result} = {result}")
                    steps.append("")
            else:
                result = problem.metadata.get('correct_answer', 0)
                steps.append(f"  Result: {result}")
                steps.append("")

        else:
            result = problem.metadata.get('correct_answer', 0)
            steps.append(f"  Result: {result}")
            steps.append("")

        steps.append(f"Final Answer: {result} ✓")

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
            values = problem.metadata.get('values', [problem.metadata['a'], problem.metadata['b'], problem.metadata['c']])
            operations = problem.metadata.get('operations', [problem.metadata['op1'], problem.metadata['op2']])
            a, b, c = values[0], values[1], values[2]
            op1, op2 = operations[0], operations[1]

            paren_result = self._evaluate_op(b, c, op2)
            steps.append(f"({b} {op2} {c}) = {paren_result}")

            result = self._evaluate_op(a, paren_result, op1)
            steps.append(f"{a} {op1} {paren_result} = {result}")

        elif template == 'nested_parentheses':
            values = problem.metadata['values']
            operations = problem.metadata['operations']
            a, b, c, d = values[0], values[1], values[2], values[3]
            op1, op2, op3 = operations[0], operations[1], operations[2]

            inner_result = self._evaluate_op(c, d, op3)
            steps.append(f"({c} {op3} {d}) = {inner_result}")

            middle_result = self._evaluate_op(b, inner_result, op2)
            steps.append(f"({b} {op2} {inner_result}) = {middle_result}")

            result = self._evaluate_op(a, middle_result, op1)
            steps.append(f"{a} {op1} {middle_result} = {result}")

        elif template == 'multiple_parentheses':
            values = problem.metadata['values']
            operations = problem.metadata['operations']
            a, b, c, d = values[0], values[1], values[2], values[3]
            op1, op2, op3 = operations[0], operations[1], operations[2]

            left_result = self._evaluate_op(a, b, op1)
            steps.append(f"({a} {op1} {b}) = {left_result}")

            right_result = self._evaluate_op(c, d, op3)
            steps.append(f"({c} {op3} {d}) = {right_result}")

            result = self._evaluate_op(left_result, right_result, op2)
            steps.append(f"{left_result} {op2} {right_result} = {result}")

        elif template == 'brackets_and_parentheses':
            values = problem.metadata['values']
            operations = problem.metadata['operations']
            a, b, c, d = values[0], values[1], values[2], values[3]
            op1, op2, op3 = operations[0], operations[1], operations[2]

            inner_result = self._evaluate_op(c, d, op3)
            steps.append(f"({c} {op3} {d}) = {inner_result}")

            bracket_result = self._evaluate_op(b, inner_result, op2)
            steps.append(f"[{b} {op2} {inner_result}] = {bracket_result}")

            result = self._evaluate_op(a, bracket_result, op1)
            steps.append(f"{a} {op1} {bracket_result} = {result}")

        elif template == 'word_problem':
            values = problem.metadata['values']
            operations = problem.metadata['operations']

            if len(values) == 3 and len(operations) == 2:
                expr = problem.metadata['expression']

                if expr.startswith('('):
                    a, b, c = values[0], values[1], values[2]
                    op2, op1 = operations[0], operations[1]

                    paren_result = self._evaluate_op(a, b, op2)
                    steps.append(f"({a} {op2} {b}) = {paren_result}")

                    result = self._evaluate_op(paren_result, c, op1)
                    steps.append(f"{paren_result} {op1} {c} = {result}")
                else:
                    a, b, c = values[0], values[1], values[2]
                    op1, op2 = operations[0], operations[1]

                    paren_result = self._evaluate_op(b, c, op2)
                    steps.append(f"({b} {op2} {c}) = {paren_result}")

                    result = self._evaluate_op(a, paren_result, op1)
                    steps.append(f"{a} {op1} {paren_result} = {result}")
            else:
                result = problem.metadata.get('correct_answer', 0)

        else:
            result = problem.metadata.get('correct_answer', 0)

        steps.append(str(result))

        return steps, result

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
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
            is_correct=True,
            algorithm_name=self.get_name()
        )
