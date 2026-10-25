"""
Malrule algorithm for Zero-Exponent-Equals-Zero.

Students think: a^0 = 0 instead of a^0 = 1
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution

class ZeroExponentEqualsZeroMalrule(Malrule):
    """Student thinks zero exponent equals zero."""

    def get_name(self):
        return "Zero-Exponent-Equals-Zero"

    def get_description(self):
        return (
            "Student thinks a^0 = 0 instead of a^0 = 1. For example, 5^0 = 0 instead of 5^0 = 1. "
            "Research by Ulusoy (2019) found only 30.9% of students correctly answered that a^0 = 1."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Malrule: a^0 = 0 (student thinks zero exponent means zero result)
        # This applies to all templates - the malrule answer is always 0
        return 0

    def _generate_concise_steps(self, problem: Problem, malrule_answer: int) -> list:
        """
        Generate concise steps for the malrule algorithm.

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

        # Show the malrule calculation based on template
        if template == 'basic_zero_exponent' or (is_word_problem and word_problem_type == 'basic_zero_exponent'):
            base = problem.metadata['base']
            steps.append(f"{base}^0 = 0")
        elif template == 'expression_simplification' or (is_word_problem and word_problem_type == 'expression_simplification'):
            coefficient = problem.metadata['coefficient']
            variable = problem.metadata['variable']
            expression_type = problem.metadata['expression_type']
            if expression_type == 'coefficient_times':
                steps.append(f"{variable}^0 = 0")
                steps.append(f"{coefficient}{variable}^0 = {coefficient} × 0 = 0")
            else:
                steps.append(f"({coefficient}{variable})^0 = 0")
        elif template == 'exponent_rules' or (is_word_problem and word_problem_type == 'exponent_rules'):
            base = problem.metadata['base']
            power = problem.metadata['power']
            steps.append(f"{base}^{power}/{base}^{power} = {base}^({power}-{power}) = {base}^0")
            steps.append(f"{base}^0 = 0")
        elif template == 'polynomial_evaluation' or (is_word_problem and word_problem_type == 'polynomial_evaluation'):
            coefficient = problem.metadata['coefficient']
            variable = problem.metadata['variable']
            steps.append(f"{variable}^0 = 0")
            steps.append(f"{coefficient}{variable}^0 = {coefficient} × 0 = 0")
        elif template == 'word_problem':
            base = problem.metadata['base']
            steps.append(f"{base}^0 = 0")

        # Answer
        steps.append(f"Answer: {malrule_answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, malrule_answer: int) -> list:
        """
        Generate verbose steps for the malrule algorithm (original implementation).
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
            steps.append("Step 2: Apply malrule (incorrectly think a^0 = 0)")
            steps.append("")

        if template == 'basic_zero_exponent' or (is_word_problem and word_problem_type == 'basic_zero_exponent'):
            base = problem.metadata['base']
            if not is_word_problem:
                steps.append(f"Problem: Evaluate {base}^0")
                steps.append("")
            steps.append("MALRULE: Zero exponent means zero result")
            steps.append(f"  Student thinks: {base}^0 = 0")
            steps.append("  Reasoning: 'Zero in the exponent means zero in the answer'")
            steps.append("  Or: 'Multiplying by something zero times gives zero'")
            steps.append("")
            steps.append(f"Student's answer: {malrule_answer}")

        elif template == 'expression_simplification' or (is_word_problem and word_problem_type == 'expression_simplification'):
            coefficient = problem.metadata['coefficient']
            variable = problem.metadata['variable']
            expression_type = problem.metadata['expression_type']

            if expression_type == 'coefficient_times':
                if not is_word_problem:
                    steps.append(f"Problem: Simplify {coefficient}{variable}^0")
                    steps.append("")
                steps.append("MALRULE: Zero exponent means zero")
                steps.append(f"  Student thinks: {variable}^0 = 0")
                steps.append(f"  So: {coefficient}{variable}^0 = {coefficient} × 0 = 0")
                steps.append("  Reasoning: 'Zero exponent means the variable becomes zero'")
                steps.append("")
                steps.append(f"Student's answer: {malrule_answer}")
            else:  # parentheses
                if not is_word_problem:
                    steps.append(f"Problem: Simplify ({coefficient}{variable})^0")
                    steps.append("")
                steps.append("MALRULE: Zero exponent means zero result")
                steps.append(f"  Student thinks: ({coefficient}{variable})^0 = 0")
                steps.append("  Reasoning: 'Anything to the zero power equals zero'")
                steps.append("")
                steps.append(f"Student's answer: {malrule_answer}")

        elif template == 'exponent_rules' or (is_word_problem and word_problem_type == 'exponent_rules'):
            base = problem.metadata['base']
            power = problem.metadata['power']
            is_variable = problem.metadata['is_variable']

            if not is_word_problem:
                steps.append(f"Problem: Simplify {base}^{power}/{base}^{power}")
                steps.append("")
            steps.append("MALRULE: Apply exponent rule, then interpret zero exponent as zero")
            steps.append(f"  Step 1: {base}^{power}/{base}^{power} = {base}^({power}-{power}) = {base}^0")
            steps.append(f"  Step 2: MALRULE - {base}^0 = 0")
            steps.append("  Reasoning: 'Zero exponent means zero result'")
            steps.append("")
            steps.append(f"Student's answer: {malrule_answer}")

        elif template == 'polynomial_evaluation' or (is_word_problem and word_problem_type == 'polynomial_evaluation'):
            coefficient = problem.metadata['coefficient']
            variable = problem.metadata['variable']
            x_value = problem.metadata['x_value']

            if not is_word_problem:
                steps.append(f"Problem: Evaluate {coefficient}{variable}^0 when {variable} = {x_value}")
                steps.append("")
            steps.append("MALRULE: Zero exponent means zero")
            steps.append(f"  Student thinks: {variable}^0 = 0 (regardless of {variable}'s value)")
            steps.append(f"  So: {coefficient}{variable}^0 = {coefficient} × 0 = 0")
            steps.append("  Reasoning: 'Zero exponent makes the whole term zero'")
            steps.append("")
            steps.append(f"Student's answer: {malrule_answer}")

        elif template == 'word_problem':
            base = problem.metadata['base']
            context_type = problem.metadata['context_type']

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("MALRULE: Zero exponent means zero result")
            steps.append(f"  Student thinks: {base}^0 = 0")

            if context_type == 'bacteria_growth':
                steps.append("  Reasoning: 'After 0 hours, there's no growth, so the multiplier is 0'")
            elif context_type == 'investment':
                steps.append("  Reasoning: 'After 0 years, there's no growth, so the factor is 0'")
            elif context_type == 'doubling':
                steps.append("  Reasoning: 'At the start (chapter 0), the multiplier is 0'")
            elif context_type == 'files':
                steps.append("  Reasoning: 'At step 0, no files are created, so the answer is 0'")
            else:
                steps.append("  Reasoning: 'Zero in the exponent means zero in the result'")

            steps.append("")
            steps.append(f"Student's answer: {malrule_answer}")

        steps.append("")
        steps.append(
            f"The student incorrectly interprets the zero exponent as producing zero. "
            f"They don't understand that a^0 = 1 by definition and by the exponent division rule."
        )

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the zero-exponent-equals-zero malrule.

        Args:
            problem: The zero exponent problem
            verbose: If True, generate verbose steps; if False, generate concise steps (default: False)

        Returns:
            Solution showing incorrect reasoning (a^0 = 0)
        """
        # CALCULATE the malrule answer: a^0 = 0 [WRONG - should be 1]
        malrule_answer = 0

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
