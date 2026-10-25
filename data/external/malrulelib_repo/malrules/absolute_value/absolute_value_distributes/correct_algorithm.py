"""
Correct algorithm for absolute value problems.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import CorrectAlgorithm, Problem, Solution


class AbsoluteValueCorrectAlgorithm(CorrectAlgorithm):
    """Correctly evaluates absolute value by computing expression first."""

    def get_name(self):
        return "Correct Absolute Value"

    def get_description(self):
        return "Correctly evaluates expression inside absolute value first, then applies absolute value"

    def _generate_verbose_steps(self, problem: Problem, template: str, x: int, expression: str,
                                expression_value: int, correct_answer: str) -> list:
        """Generate verbose, explanatory steps."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")

        # Handle word problems by detecting embedded formula type
        if template == 'word_problem':
            word_problem_type = problem.metadata.get('word_problem_type', 'x_plus_c')
            steps.append("CORRECT METHOD: Identify the embedded formula and solve")
            steps.append("")
            steps.append(f"Step 1: Identify the formula embedded in the word problem")
            steps.append(f"  The problem involves: |{expression}|")
            steps.append("")

            if word_problem_type == 'ax_plus_b':
                a = problem.metadata['coefficient']
                b = problem.metadata['constant']
                operation = problem.metadata['operation']
                steps.append("Step 2: Substitute x value into expression")
                steps.append(f"  |{expression}| becomes |{a}×{x} {operation} {abs(b)}|")
                steps.append("")
                steps.append("Step 3: Evaluate the expression INSIDE")
                steps.append(f"  {a}×{x} = {a*x}")
                steps.append(f"  {a*x} {operation} {abs(b)} = {expression_value}")
                steps.append("")
                steps.append("Step 4: Apply absolute value to the RESULT")
                steps.append(f"  |{expression_value}| = {correct_answer}")
            else:
                c = problem.metadata['constant']
                operation = problem.metadata['operation']
                steps.append("Step 2: Substitute x value into expression")
                if operation == '+':
                    steps.append(f"  |x + {c}| becomes |{x} + {c}|")
                else:
                    steps.append(f"  |x - {c}| becomes |{x} - {c}|")
                steps.append("")
                steps.append("Step 3: Evaluate the expression INSIDE")
                if operation == '+':
                    steps.append(f"  {x} + {c} = {expression_value}")
                else:
                    steps.append(f"  {x} - {c} = {expression_value}")
                steps.append("")
                steps.append("Step 4: Apply absolute value to the RESULT")
                steps.append(f"  |{expression_value}| = {correct_answer}")

            steps.append("")
            steps.append(f"Answer: {correct_answer}")
        else:
            c = problem.metadata['constant']
            operation = problem.metadata['operation']
            steps.append("CORRECT METHOD: Evaluate inside first, then apply absolute value")
            steps.append("")
            steps.append("Key principle: Absolute value is a FUNCTION")
            steps.append("  |expression| means: compute expression, then take absolute value")
            steps.append("  Order of operations: INSIDE first, THEN absolute value")
            steps.append("")

            if template == 'multiplication_inside':
                a = problem.metadata['coefficient']
                b = problem.metadata['constant']
                steps.append("Step 1: Substitute x value into expression")
                steps.append(f"  |{expression}| becomes |{a}×{x} {operation} {abs(b)}|")
                steps.append("")
                steps.append("Step 2: Evaluate the expression INSIDE")
                steps.append(f"  {a}×{x} = {a*x}")
                steps.append(f"  {a*x} {operation} {abs(b)} = {expression_value}")
                steps.append("")
                steps.append("Step 3: Apply absolute value to the RESULT")
                steps.append(f"  |{expression_value}| = {correct_answer}")
            else:
                steps.append("Step 1: Substitute x value into expression")
                if operation == '+':
                    steps.append(f"  |x + {c}| becomes |{x} + {c}|")
                else:
                    steps.append(f"  |x - {c}| becomes |{x} - {c}|")
                steps.append("")
                steps.append("Step 2: Evaluate the expression INSIDE the absolute value")
                if operation == '+':
                    steps.append(f"  {x} + {c} = {expression_value}")
                else:
                    steps.append(f"  {x} - {c} = {expression_value}")
                steps.append("")
                steps.append("Step 3: Apply absolute value to the RESULT")
                steps.append(f"  |{expression_value}| = {correct_answer}")

            steps.append("")
            steps.append(f"Answer: {correct_answer}")
            steps.append("")
            steps.append("Why this is important:")
            steps.append(f"  |{expression}| ≠ |x| {operation} {c if template != 'multiplication_inside' else abs(problem.metadata['constant'])}")
            steps.append(f"  Absolute value does NOT distribute!")

        return steps

    def _generate_concise_steps(self, problem: Problem, template: str, x: int, expression: str,
                                expression_value: int, correct_answer: str) -> list:
        """Generate concise steps with just formulas and values."""
        steps = [f"Problem: {problem.text}"]

        # Handle word problems by detecting embedded formula type
        if template == 'word_problem':
            word_problem_type = problem.metadata.get('word_problem_type', 'x_plus_c')
            steps.append(f"|{expression}|")

            if word_problem_type == 'ax_plus_b':
                a = problem.metadata['coefficient']
                b = problem.metadata['constant']
                operation = problem.metadata['operation']
                steps.append(f"|{a}×{x} {operation} {abs(b)}|")
                steps.append(f"|{a*x} {operation} {abs(b)}|")
                steps.append(f"|{expression_value}|")
            else:
                c = problem.metadata['constant']
                operation = problem.metadata['operation']
                if operation == '+':
                    steps.append(f"|{x} + {c}|")
                else:
                    steps.append(f"|{x} - {c}|")
                steps.append(f"|{expression_value}|")

            steps.append(correct_answer)
        else:
            c = problem.metadata['constant']
            operation = problem.metadata['operation']

            if template == 'multiplication_inside':
                a = problem.metadata['coefficient']
                b = problem.metadata['constant']
                steps.append(f"|{expression}|")
                steps.append(f"|{a}×{x} {operation} {abs(b)}|")
                steps.append(f"|{a*x} {operation} {abs(b)}|")
                steps.append(f"|{expression_value}|")
            else:
                steps.append(f"|{expression}|")
                if operation == '+':
                    steps.append(f"|{x} + {c}|")
                else:
                    steps.append(f"|{x} - {c}|")
                steps.append(f"|{expression_value}|")

            steps.append(correct_answer)

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct absolute value algorithm.

        Args:
            problem: The absolute value problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution showing correct approach
        """
        template = problem.metadata.get('template', 'basic_addition')
        x = problem.metadata['x_value']
        expression = problem.metadata['expression']
        expression_value = problem.metadata['expression_value']

        # Actually compute the correct answer: evaluate expression first, then take absolute value
        abs_value = abs(expression_value)

        # For word problems, format the answer appropriately
        if template == 'word_problem':
            context_type = problem.metadata.get('context_type', 'temperature')
            if context_type == 'temperature':
                correct_answer = f"{abs_value} degrees"
            elif context_type == 'distance':
                correct_answer = f"{abs_value} meters"
            elif context_type == 'money':
                correct_answer = f"${abs_value}"
            else:
                correct_answer = str(abs_value)
        else:
            correct_answer = str(abs_value)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, template, x, expression, expression_value, correct_answer)
        else:
            steps = self._generate_concise_steps(problem, template, x, expression, expression_value, correct_answer)

        return Solution(
            answer=str(correct_answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
