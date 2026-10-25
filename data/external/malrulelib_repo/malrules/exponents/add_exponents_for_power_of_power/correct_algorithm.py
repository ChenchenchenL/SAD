"""
Correct algorithm for power of power problems.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import CorrectAlgorithm, Problem, Solution
from typing import List


class PowerOfPowerCorrectAlgorithm(CorrectAlgorithm):
    """Correctly multiplies exponents for power of power."""

    def get_name(self):
        return "Correct Power of Power"

    def get_description(self):
        return "Correctly applies (a^m)^n = a^(m×n) by multiplying exponents"

    def _generate_concise_steps(self, problem: Problem, correct_answer) -> List[str]:
        """Generate concise steps showing only formula and values."""
        template = problem.metadata.get('template', 'basic_power_of_power')
        is_word_problem = problem.metadata.get('is_word_problem', False)
        word_problem_type = problem.metadata.get('word_problem_type', None)

        inner_exp = problem.metadata['inner_exponent']
        outer_exp = problem.metadata['outer_exponent']
        coefficient = problem.metadata.get('coefficient', None)
        base = problem.metadata.get('base', None)
        variable = problem.metadata.get('variable', 'x')
        additional_exp = problem.metadata.get('additional_exponent', None)

        steps = []

        # Question
        steps.append(f"{problem.text}")

        # For word problems, show extraction step
        if is_word_problem:
            if word_problem_type == 'basic_power_of_power':
                steps.append(f"({variable}^{inner_exp})^{outer_exp}")
            elif word_problem_type == 'with_coefficient':
                coeff = problem.metadata['coefficient']
                steps.append(f"({coeff}{variable}^{inner_exp})^{outer_exp}")
            elif word_problem_type == 'numerical_evaluation':
                base = problem.metadata['base']
                steps.append(f"({base}^{inner_exp})^{outer_exp}")
            elif word_problem_type == 'product_of_powers':
                additional_exp = problem.metadata['additional_exponent']
                steps.append(f"({variable}^{inner_exp})^{outer_exp} × {variable}^{additional_exp}")

        # Template-specific calculation steps
        if template == 'numerical_evaluation':
            base = problem.metadata['base']
            steps.append(f"{inner_exp} × {outer_exp} = {inner_exp * outer_exp}")
            steps.append(f"{base}^{inner_exp * outer_exp} = {correct_answer}")
        elif template == 'product_of_powers':
            additional_exp = problem.metadata['additional_exponent']
            steps.append(f"{inner_exp} × {outer_exp} = {inner_exp * outer_exp}")
            steps.append(f"{variable}^{inner_exp * outer_exp} × {variable}^{additional_exp}")
            steps.append(f"{inner_exp * outer_exp} + {additional_exp} = {inner_exp * outer_exp + additional_exp}")
            steps.append(f"{correct_answer}")
        elif template == 'with_coefficient':
            coeff = problem.metadata['coefficient']
            correct_coeff = problem.metadata['correct_coefficient']
            steps.append(f"{inner_exp} × {outer_exp} = {inner_exp * outer_exp}")
            steps.append(f"{coeff}^{outer_exp} = {correct_coeff}")
            steps.append(f"{correct_answer}")
        else:  # basic
            steps.append(f"{inner_exp} × {outer_exp} = {inner_exp * outer_exp}")
            steps.append(f"{correct_answer}")

        # Answer
        steps.append(f"{correct_answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, correct_answer) -> List[str]:
        """Generate verbose steps with full explanations (original behavior)."""
        template = problem.metadata.get('template', 'basic_power_of_power')
        is_word_problem = problem.metadata.get('is_word_problem', False)
        word_problem_type = problem.metadata.get('word_problem_type', None)

        inner_exp = problem.metadata['inner_exponent']
        outer_exp = problem.metadata['outer_exponent']
        coefficient = problem.metadata.get('coefficient', None)
        base = problem.metadata.get('base', None)

        # CALCULATE correct answer
        result_exp = inner_exp * outer_exp
        variable = problem.metadata.get('variable', 'x')
        additional_exp = problem.metadata.get('additional_exponent', None)

        # Handle product_of_powers template: (x^m)^n × x^p = x^(m*n+p)
        if additional_exp is not None:
            result_exp = result_exp + additional_exp

        steps = []

        # For word problems, show extraction step
        if is_word_problem:
            steps.append(f"Word Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Extract the mathematical expression from the word problem")

            if word_problem_type == 'basic_power_of_power':
                steps.append(f"  Expression: (x^{inner_exp})^{outer_exp}")
            elif word_problem_type == 'with_coefficient':
                coeff = problem.metadata['coefficient']
                steps.append(f"  Expression: ({coeff}x^{inner_exp})^{outer_exp}")
            elif word_problem_type == 'numerical_evaluation':
                base = problem.metadata['base']
                steps.append(f"  Expression: ({base}^{inner_exp})^{outer_exp}")
            elif word_problem_type == 'product_of_powers':
                additional_exp = problem.metadata['additional_exponent']
                steps.append(f"  Expression: (x^{inner_exp})^{outer_exp} × x^{additional_exp}")

            steps.append("")
            steps.append("Step 2: Apply the power of a power rule")
        else:
            steps.append(f"Problem: {problem.text}")
            steps.append("")

        steps.append("CORRECT METHOD: Power of a power - multiply exponents")
        steps.append("Rule: (a^m)^n = a^(m×n)")
        steps.append("")
        steps.append("Step 1: Multiply the exponents" if not is_word_problem else "  Multiply the exponents")
        steps.append(f"  {inner_exp} × {outer_exp} = {inner_exp * outer_exp}")

        if template == 'numerical_evaluation':
            base = problem.metadata['base']
            steps.append("")
            steps.append("Step 2: Evaluate the result")
            steps.append(f"  {base}^{inner_exp * outer_exp} = {correct_answer}")
        elif template == 'product_of_powers':
            additional_exp = problem.metadata['additional_exponent']
            steps.append("")
            steps.append("Step 2: Apply product rule for the additional term")
            steps.append(f"  x^{inner_exp * outer_exp} × x^{additional_exp}")
            steps.append(f"  = x^({inner_exp * outer_exp} + {additional_exp})")
            steps.append(f"  = {correct_answer}")
        elif template == 'with_coefficient':
            coeff = problem.metadata['coefficient']
            correct_coeff = problem.metadata['correct_coefficient']
            steps.append("")
            steps.append("Step 2: Raise the coefficient to the outer power")
            steps.append(f"  {coeff}^{outer_exp} = {correct_coeff}")
            steps.append(f"  Result: {correct_answer}")
        else:
            steps.append(f"  Result: {correct_answer}")

        steps.append("")
        steps.append("CORRECT! Power of a power uses MULTIPLICATION: (a^m)^n = a^(m×n)")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply correct power of power algorithm.

        Args:
            problem: The problem to solve
            verbose: If True, generate verbose steps with explanations.
                    If False (default), generate concise steps with only formulas and values.
        """
        template = problem.metadata.get('template', 'basic_power_of_power')

        inner_exp = problem.metadata['inner_exponent']
        outer_exp = problem.metadata['outer_exponent']
        coefficient = problem.metadata.get('coefficient', None)
        base = problem.metadata.get('base', None)

        # CALCULATE correct answer
        result_exp = inner_exp * outer_exp
        variable = problem.metadata.get('variable', 'x')
        additional_exp = problem.metadata.get('additional_exponent', None)

        # Handle product_of_powers template: (x^m)^n × x^p = x^(m*n+p)
        if additional_exp is not None:
            result_exp = result_exp + additional_exp

        if base is not None:
            # Numerical evaluation: (base^m)^n = base^(m*n)
            correct_answer = base ** result_exp
        elif coefficient is not None and coefficient != 1:
            # (cx^m)^n = c^n * x^(m*n)
            result_coeff = coefficient ** outer_exp
            correct_answer = f"{result_coeff}{variable}^{result_exp}"
        else:
            # (x^m)^n = x^(m*n)
            correct_answer = f"{variable}^{result_exp}"

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
