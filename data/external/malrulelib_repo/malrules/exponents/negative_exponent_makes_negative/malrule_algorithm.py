"""
Malrule algorithm for Negative-Exponent-Makes-Negative.

Students think negative exponent makes the result negative: x^-n = -x^n
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution

class NegativeExponentMakesNegativeMalrule(Malrule):
    """Student thinks negative exponent negates the result."""

    def get_name(self):
        return "Negative-Exponent-Makes-Negative"

    def get_description(self):
        return (
            "Student thinks negative exponent makes the result negative: x^-n = -x^n. "
            "For example, 2^-2 = -4 instead of 1/4. Research by Cangelosi et al. (2013) "
            "identified this as the 'sticky sign' error that persists through college."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        base = problem.metadata['base']
        positive_exp = problem.metadata['positive_exp']
        # Malrule: Negative exponent makes result negative (INCORRECT)
        # x^-n becomes -(x^n)
        return -(base ** positive_exp)

    def _generate_concise_steps(self, problem: Problem, base, negative_exp: int, positive_exp: int, malrule_answer) -> list:
        """
        Generate concise steps for the malrule algorithm.

        Format: [Question, step, step, ..., answer]
        """
        is_word_problem = problem.metadata.get('is_word_problem', False)
        problem_type = problem.metadata.get('problem_type', 'simple_numeric')

        steps = []

        # Question
        steps.append(problem.text)

        # For word problems, include formula extraction
        if is_word_problem:
            if problem_type == 'fractional_base' and isinstance(base, float) and base < 1:
                denom = int(1/base)
                steps.append(f"(1/{denom})^{negative_exp}")
            else:
                steps.append(f"{base}^{negative_exp}")

        # Show the malrule calculation
        if problem_type == 'fractional_base' and isinstance(base, float) and base < 1:
            denom = int(1/base)
            steps.append(f"(1/{denom})^{negative_exp} = -((1/{denom})^{positive_exp})")
            steps.append(f"= -(1/{denom**positive_exp})")
            steps.append(f"= {malrule_answer}")
        else:
            steps.append(f"{base}^{negative_exp} = -{base}^{positive_exp}")
            steps.append(f"= -{int(base**positive_exp)}")
            steps.append(f"= {malrule_answer}")

        # Answer
        steps.append(f"Answer: {malrule_answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, base, negative_exp: int, positive_exp: int, malrule_answer) -> list:
        """
        Generate verbose steps for the malrule algorithm (original implementation).
        """
        is_word_problem = problem.metadata.get('is_word_problem', False)
        word_problem_type = problem.metadata.get('word_problem_type', None)
        problem_type = problem.metadata.get('problem_type', 'simple_numeric')

        steps = []

        # For word problems, show extraction step
        if is_word_problem:
            steps.append(f"Word Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Extract the mathematical expression from the word problem")

            if word_problem_type == 'simple_numeric':
                steps.append(f"  Expression: {base}^{negative_exp}")
            elif word_problem_type == 'larger_negative_exponent':
                steps.append(f"  Expression: {base}^{negative_exp}")
            elif word_problem_type == 'fractional_base':
                if isinstance(base, float) and base < 1:
                    denom = int(1/base)
                    steps.append(f"  Expression: (1/{denom})^{negative_exp}")
                else:
                    steps.append(f"  Expression: {base}^{negative_exp}")

            steps.append("")
            steps.append("Step 2: Apply malrule (incorrectly interpret negative exponent)")
            steps.append("")
        else:
            steps.append(f"Problem: Evaluate {base}^{negative_exp}")
            steps.append("")

        steps.append("MALRULE: Negative exponent makes the result negative")

        if problem_type == 'fractional_base' and isinstance(base, float) and base < 1:
            denom = int(1/base)
            steps.append(f"  Student thinks: (1/{denom})^{negative_exp} = -((1/{denom})^{positive_exp})")
            steps.append(f"  First compute: (1/{denom})^{positive_exp} = 1/{denom**positive_exp}")
            steps.append(f"  Then negate: -(1/{denom**positive_exp}) = {malrule_answer}")
        else:
            steps.append(f"  Student thinks: {base}^{negative_exp} = -{base}^{positive_exp}")
            steps.append(f"  First compute: {base}^{positive_exp} = {base**positive_exp}")
            steps.append(f"  Then negate: -{base**positive_exp} = {malrule_answer}")

        steps.append("")
        steps.append(f"Student's answer: {malrule_answer}")
        steps.append("")

        if problem_type == 'fractional_base' and isinstance(base, float) and base < 1:
            denom = int(1/base)
            steps.append(
                f"The student incorrectly interpreted the negative exponent as a negation operator. "
                f"They computed (1/{denom})^{positive_exp} = 1/{denom**positive_exp} and then negated it to get {malrule_answer}. "
                f"They don't understand that negative exponents create reciprocals, not negative numbers."
            )
        else:
            steps.append(
                f"The student incorrectly interpreted the negative exponent as a negation operator. "
                f"They computed {base}^{positive_exp} = {base**positive_exp} and then negated it to get {malrule_answer}. "
                f"They don't understand that negative exponents create reciprocals, not negative numbers."
            )

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the negative-exponent-makes-negative malrule.

        Args:
            problem: The negative exponent problem
            verbose: If True, generate verbose steps; if False, generate concise steps (default: False)

        Returns:
            Solution showing incorrect negation
        """
        base = problem.metadata['base']
        negative_exp = problem.metadata['negative_exp']
        positive_exp = problem.metadata['positive_exp']
        malrule_answer = problem.metadata['malrule_answer']

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, base, negative_exp, positive_exp, malrule_answer)
        else:
            steps = self._generate_concise_steps(problem, base, negative_exp, positive_exp, malrule_answer)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
