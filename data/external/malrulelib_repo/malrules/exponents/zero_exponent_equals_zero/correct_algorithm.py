"""
Correct algorithm for zero exponents.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import CorrectAlgorithm, Problem, Solution


class ZeroExponentCorrectAlgorithm(CorrectAlgorithm):
    """Correctly evaluates zero exponents as 1."""

    def get_name(self):
        return "Correct Zero Exponent"

    def get_description(self):
        return "Evaluates a^0 = 1 for any non-zero base a"

    def _generate_concise_steps(self, problem: Problem, correct_answer: int) -> list:
        """
        Generate concise steps for the correct algorithm.

        Format: [Question, step, step, ..., answer]
        """
        template = problem.metadata.get('template', 'basic_zero_exponent')
        is_word_problem = problem.metadata.get('is_word_problem', False)
        word_problem_type = problem.metadata.get('word_problem_type', None)

        steps = []

        # Question
        steps.append(problem.text)

        # For word problems, include formula extraction
        if is_word_problem:
            if word_problem_type == 'basic_zero_exponent':
                base = problem.metadata['base']
                steps.append(f"{base}^0")
            elif word_problem_type == 'expression_simplification':
                coefficient = problem.metadata['coefficient']
                variable = problem.metadata['variable']
                expression_type = problem.metadata['expression_type']
                if expression_type == 'coefficient_times':
                    steps.append(f"{coefficient}{variable}^0")
                else:
                    steps.append(f"({coefficient}{variable})^0")
            elif word_problem_type == 'exponent_rules':
                base = problem.metadata['base']
                power = problem.metadata['power']
                steps.append(f"{base}^{power}/{base}^{power}")
            elif word_problem_type == 'polynomial_evaluation':
                coefficient = problem.metadata['coefficient']
                variable = problem.metadata['variable']
                x_value = problem.metadata['x_value']
                steps.append(f"{coefficient}{variable}^0 when {variable} = {x_value}")

        # Show the calculation based on template
        if template == 'basic_zero_exponent' or (is_word_problem and word_problem_type == 'basic_zero_exponent'):
            base = problem.metadata['base']
            steps.append(f"{base}^0 = 1")
        elif template == 'expression_simplification' or (is_word_problem and word_problem_type == 'expression_simplification'):
            coefficient = problem.metadata['coefficient']
            variable = problem.metadata['variable']
            expression_type = problem.metadata['expression_type']
            if expression_type == 'coefficient_times':
                steps.append(f"{variable}^0 = 1")
                steps.append(f"{coefficient}{variable}^0 = {coefficient} × 1 = {coefficient}")
            else:
                steps.append(f"({coefficient}{variable})^0 = 1")
        elif template == 'exponent_rules' or (is_word_problem and word_problem_type == 'exponent_rules'):
            base = problem.metadata['base']
            power = problem.metadata['power']
            steps.append(f"{base}^{power}/{base}^{power} = {base}^({power}-{power}) = {base}^0")
            steps.append(f"{base}^0 = 1")
        elif template == 'polynomial_evaluation' or (is_word_problem and word_problem_type == 'polynomial_evaluation'):
            coefficient = problem.metadata['coefficient']
            variable = problem.metadata['variable']
            steps.append(f"{variable}^0 = 1")
            steps.append(f"{coefficient}{variable}^0 = {coefficient} × 1 = {coefficient}")
        elif template == 'word_problem':
            base = problem.metadata['base']
            steps.append(f"{base}^0 = 1")

        # Answer
        steps.append(f"Answer: {correct_answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, correct_answer: int) -> list:
        """
        Generate verbose steps for the correct algorithm (original implementation).
        """
        template = problem.metadata.get('template', 'basic_zero_exponent')
        is_word_problem = problem.metadata.get('is_word_problem', False)
        word_problem_type = problem.metadata.get('word_problem_type', None)

        steps = []

        # For word problems, show extraction step
        if is_word_problem:
            steps.append(f"Word Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Extract the mathematical expression from the word problem")

            if word_problem_type == 'basic_zero_exponent':
                base = problem.metadata['base']
                steps.append(f"  Expression: {base}^0")
            elif word_problem_type == 'expression_simplification':
                coefficient = problem.metadata['coefficient']
                variable = problem.metadata['variable']
                expression_type = problem.metadata['expression_type']
                if expression_type == 'coefficient_times':
                    steps.append(f"  Expression: {coefficient}{variable}^0")
                else:
                    steps.append(f"  Expression: ({coefficient}{variable})^0")
            elif word_problem_type == 'exponent_rules':
                base = problem.metadata['base']
                power = problem.metadata['power']
                steps.append(f"  Expression: {base}^{power}/{base}^{power}")
            elif word_problem_type == 'polynomial_evaluation':
                coefficient = problem.metadata['coefficient']
                variable = problem.metadata['variable']
                x_value = problem.metadata['x_value']
                steps.append(f"  Expression: {coefficient}{variable}^0 when {variable} = {x_value}")

            steps.append("")
            steps.append("Step 2: Apply the zero exponent rule")
            steps.append("")

        if template == 'basic_zero_exponent' or (is_word_problem and word_problem_type == 'basic_zero_exponent'):
            base = problem.metadata['base']
            if not is_word_problem:
                steps.append(f"Problem: Evaluate {base}^0")
                steps.append("")
            steps.append("CORRECT METHOD: Any non-zero number to the zero power equals 1")
            steps.append("")
            step_prefix = "  " if is_word_problem else ""
            steps.append(f"{step_prefix}Step 1: Recognize the zero exponent rule" if not is_word_problem else "  Recognize the zero exponent rule")
            steps.append(f"  {base}^0 = 1")
            steps.append("")
            steps.append("  Rule: a^0 = 1 for any non-zero a")
            steps.append("")
            steps.append(f"Answer: {correct_answer}")

        elif template == 'expression_simplification' or (is_word_problem and word_problem_type == 'expression_simplification'):
            coefficient = problem.metadata['coefficient']
            variable = problem.metadata['variable']
            expression_type = problem.metadata['expression_type']

            if expression_type == 'coefficient_times':
                if not is_word_problem:
                    steps.append(f"Problem: Simplify {coefficient}{variable}^0")
                    steps.append("")
                steps.append("CORRECT METHOD: Apply zero exponent rule")
                steps.append(f"  {variable}^0 = 1")
                steps.append(f"  So: {coefficient}{variable}^0 = {coefficient} × 1 = {coefficient}")
                steps.append("")
                steps.append(f"Answer: {correct_answer}")
            else:  # parentheses
                if not is_word_problem:
                    steps.append(f"Problem: Simplify ({coefficient}{variable})^0")
                    steps.append("")
                steps.append("CORRECT METHOD: Apply zero exponent rule")
                steps.append(f"  ({coefficient}{variable})^0 = 1")
                steps.append("  (Any expression)^0 = 1")
                steps.append("")
                steps.append(f"Answer: {correct_answer}")

        elif template == 'exponent_rules' or (is_word_problem and word_problem_type == 'exponent_rules'):
            base = problem.metadata['base']
            power = problem.metadata['power']
            is_variable = problem.metadata['is_variable']

            if not is_word_problem:
                steps.append(f"Problem: Simplify {base}^{power}/{base}^{power}")
                steps.append("")
            steps.append("CORRECT METHOD: Apply exponent division rule")
            steps.append(f"  {base}^{power}/{base}^{power} = {base}^({power}-{power}) = {base}^0")
            steps.append(f"  {base}^0 = 1")
            steps.append("")
            steps.append(f"Answer: {correct_answer}")

        elif template == 'polynomial_evaluation' or (is_word_problem and word_problem_type == 'polynomial_evaluation'):
            coefficient = problem.metadata['coefficient']
            variable = problem.metadata['variable']
            x_value = problem.metadata['x_value']

            if not is_word_problem:
                steps.append(f"Problem: Evaluate {coefficient}{variable}^0 when {variable} = {x_value}")
                steps.append("")
            steps.append("CORRECT METHOD: Apply zero exponent rule")
            steps.append(f"  {variable}^0 = 1 (regardless of {variable}'s value)")
            steps.append(f"  So: {coefficient}{variable}^0 = {coefficient} × 1 = {coefficient}")
            steps.append("")
            steps.append(f"Answer: {correct_answer}")

        elif template == 'word_problem':
            base = problem.metadata['base']
            context_type = problem.metadata['context_type']

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("CORRECT METHOD: Apply zero exponent rule")
            steps.append(f"  {base}^0 = 1")

            if context_type == 'bacteria_growth':
                steps.append("  After 0 hours, the population multiplier is 1 (no change)")
            elif context_type == 'investment':
                steps.append("  After 0 years, the growth factor is 1 (no change)")
            elif context_type == 'doubling':
                steps.append("  At chapter 0 (the start), the multiplier is 1 (original amount)")
            elif context_type == 'files':
                steps.append("  At step 0, 1 file is created (the starting condition)")

            steps.append("")
            steps.append(f"Answer: {correct_answer}")

        steps.append("")
        steps.append(
            f"The key insight is that a^0 = 1 is NOT arbitrary! It follows from "
            f"the pattern of exponents and from the division rule. Any non-zero "
            f"number raised to the zero power equals 1."
        )

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct zero exponent algorithm.

        Args:
            problem: The zero exponent problem
            verbose: If True, generate verbose steps; if False, generate concise steps (default: False)

        Returns:
            Solution showing correct approach (a^0 = 1)
        """
        template = problem.metadata.get('template', 'basic_zero_exponent')
        is_word_problem = problem.metadata.get('is_word_problem', False)
        word_problem_type = problem.metadata.get('word_problem_type', None)

        # CALCULATE the correct answer based on the template
        if template in ['basic_zero_exponent', 'exponent_rules', 'word_problem'] or \
           (is_word_problem and word_problem_type in ['basic_zero_exponent', 'exponent_rules']):
            correct_answer = 1
        elif template == 'expression_simplification' or (is_word_problem and word_problem_type == 'expression_simplification'):
            expression_type = problem.metadata['expression_type']
            if expression_type == 'coefficient_times':
                correct_answer = problem.metadata['coefficient']
            else:
                correct_answer = 1
        elif template == 'polynomial_evaluation' or (is_word_problem and word_problem_type == 'polynomial_evaluation'):
            correct_answer = problem.metadata['coefficient']
        else:
            correct_answer = 1

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
