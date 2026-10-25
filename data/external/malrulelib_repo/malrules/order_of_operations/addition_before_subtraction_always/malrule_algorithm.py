"""
Addition-Before-Subtraction-Always malrule algorithm.

Implements the systematic error of believing addition must always
be performed before subtraction, even when they appear left-to-right.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import re
from utils import Malrule, Problem, Solution
from typing import Dict, Any, List, Tuple

class AdditionBeforeSubtractionAlwaysMalrule(Malrule):
    """
    Implements the Addition-Before-Subtraction-Always bug.

    Students incorrectly believe that addition must ALWAYS be
    performed before subtraction, misinterpreting PEMDAS as a strict
    sequence rather than understanding A and S have equal priority.

    Example: 10 - 3 + 2 → 10 - (3 + 2) = 10 - 5 = 5 (WRONG! should be 9)

    This is a very common PEMDAS misconception, companion to
    Multiplication-Before-Division-Always.
    """

    def get_name(self) -> str:
        return "Addition-Before-Subtraction-Always"

    def get_description(self) -> str:
        return (
            "Students incorrectly believe that addition must ALWAYS be "
            "performed before subtraction. They interpret PEMDAS literally on a "
            "letter-by-letter basis, following the order of 'A' and 'S' to incorrectly "
            "believe that addition must be performed before subtraction (Eaves et al., 2025). "
            "Example: 10 - 3 + 2 becomes 10 - 5 = 5 instead of 9."
        )

    def _parse_expression(self, expression: str) -> List[Tuple[int, str]]:
        """
        Parse expression into list of (number, operator_before_it) tuples.

        First number has operator None.

        Args:
            expression: Mathematical expression string

        Returns:
            List of (number, operator) tuples
        """
        tokens = re.findall(r'\d+|[+\-]', expression)
        nums_and_ops = [(int(tokens[0]), None)]
        for i in range(1, len(tokens), 2):
            op = tokens[i]
            num = int(tokens[i + 1])
            nums_and_ops.append((num, op))
        return nums_and_ops

    def _apply_malrule_logic(self, expression: str) -> Tuple[int, List[dict]]:
        """
        Apply the malrule logic: do all additions first, then subtractions.

        The malrule student sees `a - b + c` and groups `b + c` together
        because "addition comes before subtraction". This gives `a - (b + c)`.

        For example: 10 - 3 + 2
        - Step 1: Find addition 3 + 2 = 5 (groups terms around '+')
        - Step 2: Expression becomes 10 - 5
        - Step 3: Evaluate 10 - 5 = 5

        Args:
            expression: Mathematical expression string

        Returns:
            Tuple of (final_result, list of step dictionaries)
        """
        nums_and_ops = self._parse_expression(expression)
        steps = []

        # Process all additions first by grouping terms around '+'
        # When we see (num1, '-'), (num2, '+'), we group num1 + num2
        while True:
            # Find first '+' operation
            plus_idx = None
            for i, (num, op) in enumerate(nums_and_ops):
                if op == '+':
                    plus_idx = i
                    break

            if plus_idx is None:
                break

            # Group the number before and after the '+'
            prev_num, prev_op = nums_and_ops[plus_idx - 1]
            curr_num, curr_op = nums_and_ops[plus_idx]  # curr_op is '+'

            # Combine: prev_num + curr_num
            combined = prev_num + curr_num

            # Record the step
            steps.append({
                'operation': 'addition',
                'left': prev_num,
                'right': curr_num,
                'result': combined,
                'expression_before': self._reconstruct_expression(nums_and_ops),
            })

            # Replace in list
            nums_and_ops[plus_idx - 1] = (combined, prev_op)
            nums_and_ops.pop(plus_idx)

            # Record expression after
            steps[-1]['expression_after'] = self._reconstruct_expression(nums_and_ops)

        # Now evaluate remaining subtractions left-to-right
        result = nums_and_ops[0][0]
        for i in range(1, len(nums_and_ops)):
            num, op = nums_and_ops[i]
            old_result = result
            if op == '-':
                result -= num
                steps.append({
                    'operation': 'subtraction',
                    'left': old_result,
                    'right': num,
                    'result': result,
                })
            elif op == '+':
                # Shouldn't happen after the loop above, but handle just in case
                result += num
                steps.append({
                    'operation': 'addition',
                    'left': old_result,
                    'right': num,
                    'result': result,
                })

        return result, steps

    def _reconstruct_expression(self, nums_and_ops: List[Tuple[int, str]]) -> str:
        """
        Reconstruct expression string from nums_and_ops list.

        Args:
            nums_and_ops: List of (number, operator) tuples

        Returns:
            Expression string
        """
        if not nums_and_ops:
            return ""
        expr = str(nums_and_ops[0][0])
        for num, op in nums_and_ops[1:]:
            expr += f" {op} {num}"
        return expr

    def calculate_expected_answer(self, problem: Problem) -> str:
        """
        Calculate the expected incorrect answer for this malrule.

        For Addition-Before-Subtraction-Always:
        - Student groups terms around '+' operators and evaluates those first
        - Then evaluates remaining subtractions

        Example: 10 - 3 + 2
        - Correct: (10 - 3) + 2 = 7 + 2 = 9
        - MALRULE: 10 - (3 + 2) = 10 - 5 = 5  (addition first!)

        Args:
            problem: Order of operations problem with + and -

        Returns:
            Expected incorrect answer as string
        """
        # Use metadata['malrule_answer'] if available (template-based)
        if 'malrule_answer' in problem.metadata:
            return str(problem.metadata['malrule_answer'])

        # Apply the malrule logic
        expression = problem.metadata['expression']
        result, _ = self._apply_malrule_logic(expression)

        return str(result)

    def _format_answer_with_units(self, result: int, problem: Problem) -> str:
        """
        Format the answer with appropriate units based on template type.

        Args:
            result: The numeric result
            problem: The problem instance containing template metadata

        Returns:
            Formatted answer string with units if applicable
        """
        template = problem.metadata.get('template', 'simple_expression')

        if template == 'money_transaction':
            return f"${result}"
        elif template == 'temperature_change':
            unit = problem.metadata.get('unit', '°C')
            return f"{result}{unit}"
        elif template == 'elevation_change':
            unit = problem.metadata.get('unit', 'm')
            return f"{result}{unit}"
        elif template == 'score_tracking':
            return f"{result} points"
        else:
            return str(result)

    def generate_verbose_steps(self, problem: Problem, expression: str) -> tuple:
        """
        Generate verbose steps with full explanations.

        For `a - b + c`, the malrule student groups `b + c` first because
        "addition comes before subtraction", giving `a - (b + c)`.

        Args:
            problem: The problem instance
            expression: The mathematical expression

        Returns:
            Tuple of (steps list, final_answer string)
        """
        steps = []
        steps.append(f"Expression: {expression}")
        steps.append(f"MALRULE: In PEMDAS, A comes before S, so do additions first")

        # Apply the malrule logic and get step details
        final_result, malrule_steps = self._apply_malrule_logic(expression)

        step_num = 1
        for step in malrule_steps:
            if step['operation'] == 'addition':
                steps.append(
                    f"Step {step_num}: Do addition first: {step['left']} + {step['right']} = {step['result']}"
                )
                steps.append(f"MALRULE REASONING: 'A before S' means addition always first")
                if 'expression_after' in step:
                    steps.append(f"Expression becomes: {step['expression_after']}")
            elif step['operation'] == 'subtraction':
                steps.append(
                    f"Step {step_num}: Subtract: {step['left']} - {step['right']} = {step['result']}"
                )
            step_num += 1

        # Get the final answer with proper formatting (including units)
        final_answer = self._format_answer_with_units(final_result, problem)

        steps.append(f"\nFinal answer: {final_answer} (INCORRECT - did additions before subtractions)")

        return steps, final_answer

    def generate_concise_steps(self, problem: Problem, expression: str) -> tuple:
        """
        Generate concise steps with only formulas and values.

        For `a - b + c`, the malrule student groups `b + c` first because
        "addition comes before subtraction", giving `a - (b + c)`.

        Args:
            problem: The problem instance
            expression: The mathematical expression

        Returns:
            Tuple of (steps list, final_answer string)
        """
        steps = []

        # Add question
        steps.append(problem.text)

        # Add formula extraction for word problems
        template = problem.metadata.get('template', 'simple_expression')
        if template in ['money_transaction', 'temperature_change', 'elevation_change', 'score_tracking']:
            steps.append(f"{expression}")

        # Apply the malrule logic and get step details
        final_result, malrule_steps = self._apply_malrule_logic(expression)

        for step in malrule_steps:
            if step['operation'] == 'addition':
                steps.append(f"{step['left']} + {step['right']} = {step['result']}")
            elif step['operation'] == 'subtraction':
                steps.append(f"{step['left']} - {step['right']} = {step['result']}")

        # Get the final answer with proper formatting (including units)
        final_answer = self._format_answer_with_units(final_result, problem)

        steps.append(final_answer)

        return steps, final_answer

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Addition-Before-Subtraction-Always malrule.

        Args:
            problem: Order of operations problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with incorrect addition-first evaluation
        """
        expression = problem.metadata['expression']

        # Use helper functions based on verbose flag
        if verbose:
            steps, final_answer = self.generate_verbose_steps(problem, expression)
        else:
            steps, final_answer = self.generate_concise_steps(problem, expression)

        return Solution(
            answer=final_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
