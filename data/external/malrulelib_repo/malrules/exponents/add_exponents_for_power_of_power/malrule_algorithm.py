"""
Malrule algorithm for Add-Exponents-For-Power-Of-Power.

Students think: (a³)⁵ = a⁸ instead of (a³)⁵ = a¹⁵
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import List

class AddExponentsForPowerOfPowerMalrule(Malrule):
    """Student adds exponents instead of multiplying them for power of power."""

    def get_name(self):
        return "Add-Exponents-For-Power-Of-Power"

    def get_description(self):
        return (
            "Student adds exponents instead of multiplying them when computing power of a power. "
            "For example, (a³)⁵ = a⁸ instead of a¹⁵. Research indicates this error originates "
            "from overgeneralizing the product rule for exponents to power-of-power situations."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Malrule: Add exponents instead of multiply
        # (x^m)^n becomes x^(m+n) instead of x^(m*n)
        # (cx^m)^n becomes c*x^(m+n) instead of c^n*x^(m*n) - forgets to raise coefficient
        inner_exp = problem.metadata['inner_exponent']
        outer_exp = problem.metadata['outer_exponent']
        coefficient = problem.metadata.get('coefficient', None)
        base = problem.metadata.get('base', None)
        additional_exp = problem.metadata.get('additional_exponent', None)
        result_exp = inner_exp + outer_exp  # WRONG - should multiply
        variable = problem.metadata.get('variable', 'x')

        # Handle product_of_powers: (x^m)^n × x^p malrule = x^(m+n+p) [WRONG]
        if additional_exp is not None:
            result_exp = result_exp + additional_exp

        if base is not None:
            # Numerical evaluation malrule: (base^m)^n = base^(m+n) [WRONG]
            return base ** result_exp
        elif coefficient is not None and coefficient != 1:
            # Malrule also forgets to raise coefficient to power
            return f"{coefficient}{variable}^{result_exp}"
        else:
            return f"{variable}^{result_exp}"

    def _generate_concise_steps(self, problem: Problem, malrule_answer) -> List[str]:
        """Generate concise steps showing only formula and values."""
        template = problem.metadata.get('template', 'basic_power_of_power')
        is_word_problem = problem.metadata.get('is_word_problem', False)
        word_problem_type = problem.metadata.get('word_problem_type', None)

        inner_exp = problem.metadata['inner_exponent']
        outer_exp = problem.metadata['outer_exponent']
        variable = problem.metadata.get('variable', 'x')

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
            steps.append(f"{inner_exp} + {outer_exp} = {inner_exp + outer_exp}")
            steps.append(f"{base}^{inner_exp + outer_exp} = {malrule_answer}")
        elif template == 'product_of_powers':
            additional_exp = problem.metadata['additional_exponent']
            steps.append(f"{inner_exp} + {outer_exp} + {additional_exp} = {inner_exp + outer_exp + additional_exp}")
            steps.append(f"{malrule_answer}")
        else:  # basic or with_coefficient
            if 'coefficient' in problem.metadata and problem.metadata['coefficient'] > 1:
                coeff = problem.metadata['coefficient']
                steps.append(f"{inner_exp} + {outer_exp} = {inner_exp + outer_exp}")
                steps.append(f"{coeff}{variable}^({inner_exp} + {outer_exp}) = {malrule_answer}")
            else:
                steps.append(f"{inner_exp} + {outer_exp} = {inner_exp + outer_exp}")
                steps.append(f"{malrule_answer}")

        # Answer
        steps.append(f"{malrule_answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, malrule_answer) -> List[str]:
        """Generate verbose steps with full explanations (original behavior)."""
        template = problem.metadata.get('template', 'basic_power_of_power')
        is_word_problem = problem.metadata.get('is_word_problem', False)
        word_problem_type = problem.metadata.get('word_problem_type', None)

        inner_exp = problem.metadata['inner_exponent']
        outer_exp = problem.metadata['outer_exponent']

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
            steps.append("Step 2: Apply malrule (incorrectly add exponents)")
            steps.append("")
        else:
            steps.append(f"Problem: {problem.text}")
            steps.append("")

        steps.append("MALRULE: Add the exponents (confusing with product rule)")
        steps.append(f"  Student thinks: (a^m)^n = a^(m+n)")
        steps.append("")

        if template == 'numerical_evaluation':
            base = problem.metadata['base']
            steps.append(f"Step 1: Add the exponents (INCORRECT)")
            steps.append(f"  {inner_exp} + {outer_exp} = {inner_exp + outer_exp}")
            steps.append(f"Step 2: Evaluate")
            steps.append(f"  {base}^{inner_exp + outer_exp} = {malrule_answer}")
        elif template == 'product_of_powers':
            additional_exp = problem.metadata['additional_exponent']
            steps.append(f"Step 1: Add all the exponents (INCORRECT)")
            steps.append(f"  {inner_exp} + {outer_exp} + {additional_exp} = {inner_exp + outer_exp + additional_exp}")
            steps.append(f"Student's answer: {malrule_answer}")
        elif template == 'word_problem':
            steps.append(f"Step 1: Add the exponents (INCORRECT)")
            steps.append(f"  {inner_exp} + {outer_exp} = {inner_exp + outer_exp}")
            steps.append(f"Student's answer: {malrule_answer}")
        else:  # basic or with_coefficient
            if 'coefficient' in problem.metadata and problem.metadata['coefficient'] > 1:
                coeff = problem.metadata['coefficient']
                steps.append(f"Step 1: Add the exponents (INCORRECT)")
                steps.append(f"  {inner_exp} + {outer_exp} = {inner_exp + outer_exp}")
                steps.append(f"  Coefficient: {coeff} (student forgets to raise it)")
                steps.append(f"Student's answer: {malrule_answer}")
            else:
                steps.append(f"Step 1: Add the exponents (INCORRECT)")
                steps.append(f"  {inner_exp} + {outer_exp} = {inner_exp + outer_exp}")
                steps.append(f"Student's answer: {malrule_answer}")

        steps.append("")
        steps.append(
            f"INCORRECT! Student adds exponents ({inner_exp}+{outer_exp}={inner_exp+outer_exp}) "
            f"instead of multiplying ({inner_exp}×{outer_exp}={inner_exp*outer_exp}). "
            f"Power of a power rule: (a^m)^n = a^(m×n), NOT a^(m+n)."
        )

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply the add-exponents-for-power-of-power malrule.

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
