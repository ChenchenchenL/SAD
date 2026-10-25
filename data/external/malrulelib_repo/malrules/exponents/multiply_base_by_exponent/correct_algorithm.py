"""
Correct algorithm for exponentiation.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import CorrectAlgorithm, Problem, Solution


class ExponentiationCorrectAlgorithm(CorrectAlgorithm):
    """Correctly evaluates exponentiation as repeated multiplication."""

    def get_name(self):
        return "Correct Exponentiation"

    def get_description(self):
        return "Evaluates a^b as repeated multiplication: a × a × ... × a (b times)"

    def _generate_concise_steps(self, problem: Problem, base: int, exponent: int, correct_answer: int) -> list:
        """
        Generate concise steps for the correct algorithm.

        Format: [Question, step, step, ..., answer]
        """
        is_word_problem = problem.metadata.get('is_word_problem', False)

        steps = []

        # Question
        steps.append(problem.text)

        # For word problems, include formula extraction
        if is_word_problem:
            steps.append(f"{base}^{exponent}")

        # Show the expansion
        multiplication = " × ".join([str(base)] * exponent)
        steps.append(f"{base}^{exponent} = {multiplication}")

        # Final calculation
        steps.append(f"= {correct_answer}")

        # Answer
        steps.append(f"Answer: {correct_answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, base: int, exponent: int, correct_answer: int) -> list:
        """
        Generate verbose steps for the correct algorithm (original implementation).
        """
        is_word_problem = problem.metadata.get('is_word_problem', False)
        word_problem_type = problem.metadata.get('word_problem_type', None)

        steps = []

        # For word problems, show extraction step
        if is_word_problem:
            steps.append(f"Word Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Extract the mathematical expression from the word problem")

            if word_problem_type == 'simple_numeric':
                steps.append(f"  Expression: {base}^{exponent}")
            elif word_problem_type == 'larger_exponent':
                steps.append(f"  Expression: {base}^{exponent}")

            steps.append("")
            steps.append("Step 2: Apply the exponentiation rule")
        else:
            steps.append(f"Problem: Evaluate {base}^{exponent}")
            steps.append("")

        steps.append("CORRECT METHOD: Repeated multiplication")
        steps.append(f"  {base}^{exponent} means '{base} multiplied by itself {exponent} times'")

        # Show the expansion
        multiplication = " × ".join([str(base)] * exponent)
        steps.append(f"  {base}^{exponent} = {multiplication}")

        # Show intermediate steps for small exponents
        if exponent <= 4:
            if exponent == 2:
                steps.append(f"  = {base * base}")
            elif exponent == 3:
                steps.append(f"  = {base} × {base} = {base * base}")
                steps.append(f"  = {base * base} × {base} = {correct_answer}")
            elif exponent == 4:
                steps.append(f"  = {base} × {base} = {base * base}")
                steps.append(f"  = {base * base} × {base} = {base * base * base}")
                steps.append(f"  = {base * base * base} × {base} = {correct_answer}")
        else:
            steps.append(f"  = {correct_answer}")

        steps.append("")
        steps.append(f"Answer: {correct_answer}")
        steps.append("")
        steps.append(
            f"Exponentiation is repeated multiplication. {base}^{exponent} means "
            f"we multiply {base} by itself {exponent} times: {multiplication} = {correct_answer}."
        )

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct exponentiation algorithm.

        Args:
            problem: The exponentiation problem
            verbose: If True, generate verbose steps; if False, generate concise steps (default: False)

        Returns:
            Solution showing correct repeated multiplication approach
        """
        # Parse parameters from metadata (NOT the answer)
        base = problem.metadata['base']
        exponent = problem.metadata['exponent']

        # CALCULATE the correct answer: base^exponent
        correct_answer = base ** exponent

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, base, exponent, correct_answer)
        else:
            steps = self._generate_concise_steps(problem, base, exponent, correct_answer)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
