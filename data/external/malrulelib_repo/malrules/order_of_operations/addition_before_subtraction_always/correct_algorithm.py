"""
Correct order of operations algorithm for addition/subtraction.

Implements proper order of operations where addition and subtraction
have equal priority and are evaluated left-to-right.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import re
from utils import CorrectAlgorithm, Problem, Solution


class AddSubOrderCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for order of operations with addition/subtraction.

    Follows proper PEMDAS/BODMAS rules where addition and subtraction
    have equal priority and are evaluated left-to-right.
    """

    def get_name(self) -> str:
        return "Correct Order of Operations (Addition/Subtraction)"

    def get_description(self) -> str:
        return (
            "Evaluates expressions correctly following PEMDAS/BODMAS. "
            "Addition and subtraction have equal priority and are "
            "evaluated left-to-right. Example: 10 - 3 + 2 = 7 + 2 = 9"
        )

    def generate_verbose_steps(self, problem: Problem, expression: str, template: str) -> tuple:
        """
        Generate verbose steps with full explanations.

        Args:
            problem: The problem instance
            expression: The mathematical expression
            template: The template type

        Returns:
            Tuple of (steps list, final_answer string)
        """
        steps = []
        steps.append(f"Expression: {expression}")
        steps.append(f"Rule: Addition and subtraction have equal priority")
        steps.append(f"Evaluate left-to-right")

        # Extract numbers and operators
        tokens = re.findall(r'\d+|[+\-]', expression)

        # Start with the first number
        result = int(tokens[0])
        step_num = 1

        # Process each operation left-to-right
        i = 1
        while i < len(tokens):
            if i < len(tokens) - 1:
                operator = tokens[i]
                operand = int(tokens[i + 1])

                old_result = result
                if operator == '+':
                    result = result + operand
                    steps.append(f"Step {step_num}: {old_result} + {operand} = {result}")
                elif operator == '-':
                    result = result - operand
                    steps.append(f"Step {step_num}: {old_result} - {operand} = {result}")

                step_num += 1
                i += 2
            else:
                break

        # Format answer with units if applicable
        if template == 'money_transaction':
            final_answer = f"${result}"
        elif template == 'temperature_change':
            unit = problem.metadata.get('unit', '°C')
            final_answer = f"{result}{unit}"
        elif template == 'elevation_change':
            unit = problem.metadata.get('unit', 'm')
            final_answer = f"{result}{unit}"
        elif template == 'score_tracking':
            final_answer = f"{result} points"
        else:
            final_answer = str(result)

        steps.append(f"\nFinal answer: {final_answer}")

        return steps, final_answer

    def generate_concise_steps(self, problem: Problem, expression: str, template: str) -> tuple:
        """
        Generate concise steps with only formulas and values.

        Args:
            problem: The problem instance
            expression: The mathematical expression
            template: The template type

        Returns:
            Tuple of (steps list, final_answer string)
        """
        steps = []

        # Add question
        steps.append(problem.text)

        # Add formula extraction step for word problems
        if template in ['money_transaction', 'temperature_change', 'elevation_change', 'score_tracking']:
            steps.append(f"{expression}")

        # Extract numbers and operators
        tokens = re.findall(r'\d+|[+\-]', expression)

        # Start with the first number
        result = int(tokens[0])

        # Process each operation left-to-right
        i = 1
        while i < len(tokens):
            if i < len(tokens) - 1:
                operator = tokens[i]
                operand = int(tokens[i + 1])

                old_result = result
                if operator == '+':
                    result = result + operand
                    steps.append(f"{old_result} + {operand} = {result}")
                elif operator == '-':
                    result = result - operand
                    steps.append(f"{old_result} - {operand} = {result}")

                i += 2
            else:
                break

        # Format answer with units if applicable
        if template == 'money_transaction':
            final_answer = f"${result}"
        elif template == 'temperature_change':
            unit = problem.metadata.get('unit', '°C')
            final_answer = f"{result}{unit}"
        elif template == 'elevation_change':
            unit = problem.metadata.get('unit', 'm')
            final_answer = f"{result}{unit}"
        elif template == 'score_tracking':
            final_answer = f"{result} points"
        else:
            final_answer = str(result)

        steps.append(final_answer)

        return steps, final_answer

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct order of operations.

        Args:
            problem: Order of operations problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with correct evaluation
        """
        expression = problem.metadata['expression']
        template = problem.metadata.get('template', 'simple_expression')

        # Use helper functions based on verbose flag
        if verbose:
            steps, final_answer = self.generate_verbose_steps(problem, expression, template)
        else:
            steps, final_answer = self.generate_concise_steps(problem, expression, template)

        return Solution(
            answer=final_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
