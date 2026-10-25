"""
Malrule algorithm for Forget-Exponent-On-Coefficient.

Students forget to raise the coefficient to the outer power: (cx^m)^n = c·x^(mn)
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import List

class ForgetExponentOnCoefficientMalrule(Malrule):
    """Student forgets to raise coefficient when applying power of power."""

    def get_name(self):
        return "Forget-Exponent-On-Coefficient"

    def get_description(self):
        return (
            "Student forgets to raise coefficient to the outer power: (cx^m)^n = c·x^(mn). "
            "For example, (2x³)⁵ = 2x¹⁵ instead of 32x¹⁵. Research identifies this as part of "
            "the broader 'failure to consider parentheses when performing operations' (Egodawatte, 2011)."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Malrule: Forget to raise coefficient to outer power
        # (cx^m)^n becomes c · x^(mn) instead of c^n · x^(mn)
        template = problem.metadata.get('template', 'basic_power_of_power')
        word_problem_type = problem.metadata.get('word_problem_type', None)

        if template == 'multiple_variables' or word_problem_type == 'multiple_variables':
            coefficient = problem.metadata['coefficient']
            x_exponent = problem.metadata['x_exponent']
            y_exponent = problem.metadata['y_exponent']
            outer_exponent = problem.metadata['outer_exponent']
            new_x_exponent = x_exponent * outer_exponent
            new_y_exponent = y_exponent * outer_exponent
            x_part = "x" if new_x_exponent == 1 else f"x^{new_x_exponent}"
            y_part = "y" if new_y_exponent == 1 else f"y^{new_y_exponent}"
            return f"{coefficient}{x_part}{y_part}"
        else:
            coefficient = problem.metadata['coefficient']
            base_exponent = problem.metadata['base_exponent']
            outer_exponent = problem.metadata['outer_exponent']
            variable = problem.metadata.get('variable', 'x')  # Default to 'x' if not specified
            new_exponent = base_exponent * outer_exponent
            return f"{coefficient}{variable}^{new_exponent}"

    def _generate_concise_steps(self, problem: Problem, malrule_answer) -> List[str]:
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
            new_x_exponent = problem.metadata['new_x_exponent']
            new_y_exponent = problem.metadata['new_y_exponent']

            steps.append(f"x^{x_exponent} → x^({x_exponent}×{outer_exponent}) = x^{new_x_exponent}")
            steps.append(f"y^{y_exponent} → y^({y_exponent}×{outer_exponent}) = y^{new_y_exponent}")
            steps.append(f"{coefficient} (unchanged)")
            steps.append(f"{malrule_answer}")

        elif template in ['basic_power_of_power', 'larger_coefficients', 'negative_coefficient', 'word_problem'] or word_problem_type in ['basic_power_of_power', 'larger_coefficients', 'negative_coefficient']:
            coefficient = problem.metadata['coefficient']
            base_exponent = problem.metadata['base_exponent']
            outer_exponent = problem.metadata['outer_exponent']
            new_exponent = problem.metadata['new_exponent']

            steps.append(f"x^{base_exponent} → x^({base_exponent}×{outer_exponent}) = x^{new_exponent}")
            steps.append(f"{coefficient} (unchanged)")
            steps.append(f"{malrule_answer}")

        # Answer
        steps.append(f"{malrule_answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, malrule_answer) -> List[str]:
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
                # Format x and y parts
                x_part = "x" if x_exponent == 1 else f"x^{x_exponent}"
                y_part = "y" if y_exponent == 1 else f"y^{y_exponent}"
                steps.append(f"  Expression: ({coefficient}{x_part}{y_part})^{outer_exponent}")

            steps.append("")
            steps.append("Step 2: Apply malrule (incorrectly forget to raise coefficient)")
            steps.append("")
        else:
            steps.append(f"Problem: {problem.text}")
            steps.append("")

        if template == 'multiple_variables' or word_problem_type == 'multiple_variables':
            coefficient = problem.metadata['coefficient']
            x_exponent = problem.metadata['x_exponent']
            y_exponent = problem.metadata['y_exponent']
            outer_exponent = problem.metadata['outer_exponent']
            new_x_exponent = problem.metadata['new_x_exponent']
            new_y_exponent = problem.metadata['new_y_exponent']

            steps.append("MALRULE: Apply power rule to variables only, forget coefficient")
            step_prefix = "Step 3" if is_word_problem else "Step 1"
            steps.append(f"  {step_prefix}: Multiply exponents for each variable")
            steps.append(f"    x^{x_exponent} becomes x^({x_exponent}×{outer_exponent}) = x^{new_x_exponent}")
            steps.append(f"    y^{y_exponent} becomes y^({y_exponent}×{outer_exponent}) = y^{new_y_exponent}")
            step_prefix = "Step 4" if is_word_problem else "Step 2"
            steps.append(f"  {step_prefix}: Keep coefficient unchanged (INCORRECT)")
            steps.append(f"    Coefficient stays as {coefficient}")
            steps.append(f"  Student's answer: {malrule_answer}")

        elif template in ['basic_power_of_power', 'larger_coefficients', 'negative_coefficient', 'word_problem'] or word_problem_type in ['basic_power_of_power', 'larger_coefficients', 'negative_coefficient']:
            coefficient = problem.metadata['coefficient']
            base_exponent = problem.metadata['base_exponent']
            outer_exponent = problem.metadata['outer_exponent']
            new_exponent = problem.metadata['new_exponent']

            steps.append("MALRULE: Apply power rule to variable only, forget coefficient")
            step_prefix = "Step 3" if is_word_problem else "Step 1"
            steps.append(f"  {step_prefix}: Multiply the exponents for the variable")
            steps.append(f"    x^{base_exponent} becomes x^({base_exponent}×{outer_exponent}) = x^{new_exponent}")
            step_prefix = "Step 4" if is_word_problem else "Step 2"
            steps.append(f"  {step_prefix}: Keep coefficient unchanged (INCORRECT)")
            steps.append(f"    Coefficient stays as {coefficient}")
            steps.append(f"  Student's answer: {malrule_answer}")

        steps.append("")
        steps.append(
            "The student correctly multiplied the exponents for the variables "
            "but forgot to raise the coefficient to the outer power. "
            "They don't understand that the outer exponent applies to EVERYTHING inside the parentheses, "
            "including the coefficient."
        )

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply the forget-exponent-on-coefficient malrule.

        Args:
            problem: The problem to solve
            verbose: If True, generate verbose steps with explanations.
                    If False (default), generate concise steps with only formulas and values.
        """
        # CALCULATE malrule answer
        malrule_answer = self.calculate_expected_answer(problem)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, malrule_answer)
        else:
            steps = self._generate_concise_steps(problem, malrule_answer)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
