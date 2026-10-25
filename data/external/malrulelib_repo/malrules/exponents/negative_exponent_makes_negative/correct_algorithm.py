"""
Correct algorithm for negative exponents.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import CorrectAlgorithm, Problem, Solution


class NegativeExponentCorrectAlgorithm(CorrectAlgorithm):
    """Correctly evaluates negative exponents as reciprocals."""

    def get_name(self):
        return "Correct Negative Exponent"

    def get_description(self):
        return "Evaluates x^-n as 1/(x^n) - negative exponent creates reciprocal"

    def _generate_concise_steps(self, problem: Problem, base, negative_exp: int, positive_exp: int,
                                 correct_answer_fraction: str, correct_answer_decimal) -> list:
        """
        Generate concise steps for the correct algorithm.

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

        # Show the calculation
        if problem_type == 'fractional_base' and isinstance(base, float) and base < 1:
            denom = int(1/base)
            steps.append(f"(1/{denom})^{negative_exp} = 1/((1/{denom})^{positive_exp})")
            steps.append(f"= 1/(1/{denom**positive_exp})")
            steps.append(f"= {correct_answer_fraction}")
        else:
            steps.append(f"{base}^{negative_exp} = 1/({base}^{positive_exp})")
            steps.append(f"= 1/{int(base**positive_exp)}")
            steps.append(f"= {correct_answer_fraction}")

        # Answer
        steps.append(f"Answer: {correct_answer_fraction}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, base, negative_exp: int, positive_exp: int,
                                 correct_answer_fraction: str, correct_answer_decimal) -> list:
        """
        Generate verbose steps for the correct algorithm (original implementation).
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
            steps.append("Step 2: Apply the negative exponent rule")
        else:
            steps.append(f"Problem: Evaluate {base}^{negative_exp}")
            steps.append("")

        steps.append("CORRECT METHOD: Negative exponent means reciprocal")
        steps.append("")

        if not is_word_problem:
            steps.append("Step 1: Apply negative exponent rule")
        else:
            steps.append("  Apply negative exponent rule")

        if problem_type == 'fractional_base' and isinstance(base, float) and base < 1:
            denom = int(1/base)
            steps.append(f"  (1/{denom})^{negative_exp} = 1/((1/{denom})^{positive_exp})")
        else:
            steps.append(f"  {base}^{negative_exp} = 1/({base}^{positive_exp})")

        steps.append("")
        steps.append("  Rule: x^(-n) = 1/(x^n)")
        steps.append("  The negative exponent 'flips' the base to the denominator")
        steps.append("")

        step_num = 2 if not is_word_problem else 3
        steps.append(f"Step {step_num}: Evaluate the positive exponent")

        if problem_type == 'fractional_base' and isinstance(base, float) and base < 1:
            denom = int(1/base)
            steps.append(f"  (1/{denom})^{positive_exp} = 1/{denom**positive_exp}")
            steps.append(f"  So: 1/(1/{denom**positive_exp}) = {denom**positive_exp}")
        else:
            steps.append(f"  {base}^{positive_exp} = {base**positive_exp}")

        steps.append("")
        step_num += 1
        steps.append(f"Step {step_num}: Form the fraction")

        if problem_type == 'fractional_base':
            steps.append(f"  Result: {correct_answer_fraction}")
        else:
            steps.append(f"  1/{base**positive_exp} = {correct_answer_fraction}")

        steps.append("")
        steps.append(f"As a decimal: {correct_answer_decimal}")
        steps.append("")
        steps.append(f"Answer: {correct_answer_fraction} (or {correct_answer_decimal})")
        steps.append("")
        steps.append(
            f"The key is understanding that negative exponents create RECIPROCALS, not negative numbers. "
            f"The result {correct_answer_decimal} is positive! The negative in the exponent tells us "
            f"to take 1 divided by the base raised to the positive exponent."
        )

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct negative exponent algorithm.

        Args:
            problem: The negative exponent problem
            verbose: If True, generate verbose steps; if False, generate concise steps (default: False)

        Returns:
            Solution showing correct reciprocal approach
        """
        base = problem.metadata['base']
        negative_exp = problem.metadata['negative_exp']
        positive_exp = problem.metadata['positive_exp']
        correct_answer_fraction = problem.metadata['correct_answer_fraction']
        correct_answer_decimal = problem.metadata['correct_answer_decimal']

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, base, negative_exp, positive_exp,
                                                  correct_answer_fraction, correct_answer_decimal)
        else:
            steps = self._generate_concise_steps(problem, base, negative_exp, positive_exp,
                                                  correct_answer_fraction, correct_answer_decimal)

        return Solution(
            answer=correct_answer_fraction,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
