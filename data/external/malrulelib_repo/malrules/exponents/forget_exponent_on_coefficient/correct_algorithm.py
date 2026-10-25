"""
Correct algorithm for power of power with coefficients.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import CorrectAlgorithm, Problem, Solution
from typing import List


class PowerOfPowerCorrectAlgorithm(CorrectAlgorithm):
    """Correctly applies (cx^m)^n = c^n · x^(mn)."""

    def get_name(self):
        return "Correct Power of Power with Coefficient"

    def get_description(self):
        return "Correctly applies (cx^m)^n = c^n · x^(mn) - raises both coefficient and variable to outer power"

    def _generate_concise_steps(self, problem: Problem, correct_answer) -> List[str]:
        """Generate concise steps showing only formula and values."""
        template = problem.metadata.get('template', 'basic_power_of_power')
        is_word_problem = problem.metadata.get('is_word_problem', False)
        word_problem_type = problem.metadata.get('word_problem_type', None)

        steps = []

        # Question
        steps.append(f"{problem.text}")

        # For word problems, show extraction step
        if is_word_problem:
            if word_problem_type == 'basic_power_of_power':
                coefficient = problem.metadata['coefficient']
                base_exponent = problem.metadata['base_exponent']
                outer_exponent = problem.metadata['outer_exponent']
                steps.append(f"({coefficient}x^{base_exponent})^{outer_exponent}")
            elif word_problem_type == 'larger_coefficients':
                coefficient = problem.metadata['coefficient']
                base_exponent = problem.metadata['base_exponent']
                outer_exponent = problem.metadata['outer_exponent']
                steps.append(f"({coefficient}x^{base_exponent})^{outer_exponent}")
            elif word_problem_type == 'negative_coefficient':
                coefficient = problem.metadata['coefficient']
                base_exponent = problem.metadata['base_exponent']
                outer_exponent = problem.metadata['outer_exponent']
                steps.append(f"({coefficient}x^{base_exponent})^{outer_exponent}")
            elif word_problem_type == 'multiple_variables':
                coefficient = problem.metadata['coefficient']
                x_exponent = problem.metadata['x_exponent']
                y_exponent = problem.metadata['y_exponent']
                outer_exponent = problem.metadata['outer_exponent']
                x_part = "x" if x_exponent == 1 else f"x^{x_exponent}"
                y_part = "y" if y_exponent == 1 else f"y^{y_exponent}"
                steps.append(f"({coefficient}{x_part}{y_part})^{outer_exponent}")

        # Calculation steps based on template
        if template == 'multiple_variables' or word_problem_type == 'multiple_variables':
            coefficient = problem.metadata['coefficient']
            x_exponent = problem.metadata['x_exponent']
            y_exponent = problem.metadata['y_exponent']
            outer_exponent = problem.metadata['outer_exponent']
            new_coefficient = problem.metadata['new_coefficient']
            new_x_exponent = problem.metadata['new_x_exponent']
            new_y_exponent = problem.metadata['new_y_exponent']

            steps.append(f"{coefficient}^{outer_exponent} = {new_coefficient}")
            steps.append(f"x^{x_exponent} → x^({x_exponent}×{outer_exponent}) = x^{new_x_exponent}")
            steps.append(f"y^{y_exponent} → y^({y_exponent}×{outer_exponent}) = y^{new_y_exponent}")
            steps.append(f"{correct_answer}")

        elif template in ['basic_power_of_power', 'larger_coefficients', 'negative_coefficient', 'word_problem'] or word_problem_type in ['basic_power_of_power', 'larger_coefficients', 'negative_coefficient']:
            coefficient = problem.metadata['coefficient']
            base_exponent = problem.metadata['base_exponent']
            outer_exponent = problem.metadata['outer_exponent']
            new_coefficient = problem.metadata['new_coefficient']
            new_exponent = problem.metadata['new_exponent']

            steps.append(f"{coefficient}^{outer_exponent} = {new_coefficient}")
            steps.append(f"x^{base_exponent} → x^({base_exponent}×{outer_exponent}) = x^{new_exponent}")
            steps.append(f"{new_coefficient} · x^{new_exponent} = {correct_answer}")

        # Answer
        steps.append(f"{correct_answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, correct_answer) -> List[str]:
        """Generate verbose steps with full explanations (original behavior)."""
        template = problem.metadata.get('template', 'basic_power_of_power')
        is_word_problem = problem.metadata.get('is_word_problem', False)
        word_problem_type = problem.metadata.get('word_problem_type', None)

        steps = []

        # For word problems, show extraction step
        if is_word_problem:
            steps.append(f"Word Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Extract the mathematical expression from the word problem")

            if word_problem_type == 'basic_power_of_power':
                coefficient = problem.metadata['coefficient']
                base_exponent = problem.metadata['base_exponent']
                outer_exponent = problem.metadata['outer_exponent']
                steps.append(f"  Expression: ({coefficient}x^{base_exponent})^{outer_exponent}")
            elif word_problem_type == 'larger_coefficients':
                coefficient = problem.metadata['coefficient']
                base_exponent = problem.metadata['base_exponent']
                outer_exponent = problem.metadata['outer_exponent']
                steps.append(f"  Expression: ({coefficient}x^{base_exponent})^{outer_exponent}")
            elif word_problem_type == 'negative_coefficient':
                coefficient = problem.metadata['coefficient']
                base_exponent = problem.metadata['base_exponent']
                outer_exponent = problem.metadata['outer_exponent']
                steps.append(f"  Expression: ({coefficient}x^{base_exponent})^{outer_exponent}")
            elif word_problem_type == 'multiple_variables':
                coefficient = problem.metadata['coefficient']
                x_exponent = problem.metadata['x_exponent']
                y_exponent = problem.metadata['y_exponent']
                outer_exponent = problem.metadata['outer_exponent']
                x_part = "x" if x_exponent == 1 else f"x^{x_exponent}"
                y_part = "y" if y_exponent == 1 else f"y^{y_exponent}"
                steps.append(f"  Expression: ({coefficient}{x_part}{y_part})^{outer_exponent}")

            steps.append("")
            steps.append("Step 2: Apply the power of a power rule - raise EVERYTHING to outer power")
            steps.append("")
        else:
            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("CORRECT METHOD: Raise EVERYTHING inside parentheses to outer power")
            steps.append("")

        if template == 'multiple_variables' or word_problem_type == 'multiple_variables':
            coefficient = problem.metadata['coefficient']
            x_exponent = problem.metadata['x_exponent']
            y_exponent = problem.metadata['y_exponent']
            outer_exponent = problem.metadata['outer_exponent']
            new_coefficient = problem.metadata['new_coefficient']
            new_x_exponent = problem.metadata['new_x_exponent']
            new_y_exponent = problem.metadata['new_y_exponent']

            step_prefix = "Step 3" if is_word_problem else "Step 1"
            steps.append(f"{step_prefix}: Raise coefficient to outer power")
            steps.append(f"  {coefficient}^{outer_exponent} = {new_coefficient}")
            steps.append("")
            step_prefix = "Step 4" if is_word_problem else "Step 2"
            steps.append(f"{step_prefix}: Multiply exponents for each variable")
            steps.append(f"  x^{x_exponent} becomes x^({x_exponent}×{outer_exponent}) = x^{new_x_exponent}")
            steps.append(f"  y^{y_exponent} becomes y^({y_exponent}×{outer_exponent}) = y^{new_y_exponent}")
            steps.append("")
            step_prefix = "Step 5" if is_word_problem else "Step 3"
            steps.append(f"{step_prefix}: Combine results")
            steps.append(f"  {correct_answer}")

        elif template in ['basic_power_of_power', 'larger_coefficients', 'negative_coefficient', 'word_problem'] or word_problem_type in ['basic_power_of_power', 'larger_coefficients', 'negative_coefficient']:
            coefficient = problem.metadata['coefficient']
            base_exponent = problem.metadata['base_exponent']
            outer_exponent = problem.metadata['outer_exponent']
            new_coefficient = problem.metadata['new_coefficient']
            new_exponent = problem.metadata['new_exponent']

            step_prefix = "Step 3" if is_word_problem else "Step 1"
            steps.append(f"{step_prefix}: Raise coefficient to outer power")
            steps.append(f"  {coefficient}^{outer_exponent} = {new_coefficient}")
            steps.append("")
            step_prefix = "Step 4" if is_word_problem else "Step 2"
            steps.append(f"{step_prefix}: Multiply exponents for variable (power of power rule)")
            steps.append(f"  (x^{base_exponent})^{outer_exponent} = x^({base_exponent}×{outer_exponent}) = x^{new_exponent}")
            steps.append("")
            step_prefix = "Step 5" if is_word_problem else "Step 3"
            steps.append(f"{step_prefix}: Combine results")
            steps.append(f"  {new_coefficient} · x^{new_exponent} = {correct_answer}")

        steps.append("")
        steps.append(f"Answer: {correct_answer}")
        steps.append("")
        steps.append(
            "The key is that the outer exponent applies to EVERYTHING inside the parentheses. "
            "We must raise both the coefficient and apply the power rule to variables."
        )

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply correct power of power algorithm.

        Args:
            problem: The problem to solve
            verbose: If True, generate verbose steps with explanations.
                    If False (default), generate concise steps with only formulas and values.
        """
        template = problem.metadata.get('template', 'basic_power_of_power')
        word_problem_type = problem.metadata.get('word_problem_type', None)

        # CALCULATE the correct answer based on template
        if template == 'multiple_variables' or word_problem_type == 'multiple_variables':
            coefficient = problem.metadata['coefficient']
            x_exponent = problem.metadata['x_exponent']
            y_exponent = problem.metadata['y_exponent']
            outer_exponent = problem.metadata['outer_exponent']
            new_coefficient = coefficient ** outer_exponent
            new_x_exponent = x_exponent * outer_exponent
            new_y_exponent = y_exponent * outer_exponent
            # Format as coefficient*x^new_x*y^new_y
            x_part = "x" if new_x_exponent == 1 else f"x^{new_x_exponent}"
            y_part = "y" if new_y_exponent == 1 else f"y^{new_y_exponent}"
            correct_answer = f"{new_coefficient}{x_part}{y_part}"
        else:
            # basic_power_of_power, larger_coefficients, negative_coefficient, word_problem
            coefficient = problem.metadata['coefficient']
            base_exponent = problem.metadata['base_exponent']
            outer_exponent = problem.metadata['outer_exponent']
            variable = problem.metadata.get('variable', 'x')  # Default to 'x' if not specified
            new_coefficient = coefficient ** outer_exponent
            new_exponent = base_exponent * outer_exponent
            correct_answer = f"{new_coefficient}{variable}^{new_exponent}"

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, correct_answer)
        else:
            steps = self._generate_concise_steps(problem, correct_answer)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
