"""
Malrule algorithm for Multiply-Base-By-Exponent.

Students treat exponentiation as multiplication: a^b = a × b
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution

class MultiplyBaseByExponentMalrule(Malrule):
    """Student multiplies base by exponent instead of repeated multiplication."""

    def get_name(self):
        return "Multiply-Base-By-Exponent"

    def get_description(self):
        return (
            "Student treats exponentiation as multiplication: a^b = a × b. "
            "For example, 2³ = 2 × 3 = 6 instead of 2 × 2 × 2 = 8. Research by Ulusoy (2019) "
            "found this error originates from misunderstanding exponentiation as repeated multiplication."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        base = problem.metadata['base']
        exponent = problem.metadata['exponent']
        # Malrule: Multiply base by exponent (INCORRECT)
        # a^b becomes a × b
        return base * exponent

    def _generate_concise_steps(self, problem: Problem, base: int, exponent: int, malrule_answer: int) -> list:
        """
        Generate concise steps for the malrule algorithm.

        Format: [Question, step, step, ..., answer]
        """
        is_word_problem = problem.metadata.get('is_word_problem', False)

        steps = []

        # Question
        steps.append(problem.text)

        # For word problems, include formula extraction
        if is_word_problem:
            steps.append(f"{base}^{exponent}")

        # Show the malrule calculation
        steps.append(f"{base}^{exponent} = {base} × {exponent}")
        steps.append(f"= {malrule_answer}")

        # Answer
        steps.append(f"Answer: {malrule_answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, base: int, exponent: int, malrule_answer: int) -> list:
        """
        Generate verbose steps for the malrule algorithm (original implementation).
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
            steps.append("Step 2: Apply malrule (incorrectly multiply base by exponent)")
            steps.append("")
        else:
            steps.append(f"Problem: Evaluate {base}^{exponent}")
            steps.append("")

        steps.append("MALRULE: Multiply base by exponent")
        steps.append(f"  {base}^{exponent} = {base} × {exponent}")
        steps.append(f"  = {malrule_answer}")
        steps.append("")
        steps.append(f"Student's answer: {malrule_answer}")
        steps.append("")
        steps.append(
            f"The student incorrectly treats the exponent as a multiplier, "
            f"calculating {base} × {exponent} = {malrule_answer} instead of "
            f"understanding that {base}^{exponent} means '{base} multiplied by "
            f"itself {exponent} times'."
        )

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the multiply-base-by-exponent malrule.

        Args:
            problem: The exponentiation problem
            verbose: If True, generate verbose steps; if False, generate concise steps (default: False)

        Returns:
            Solution showing incorrect multiplication approach
        """
        # Parse parameters from metadata (NOT the malrule_answer)
        base = problem.metadata['base']
        exponent = problem.metadata['exponent']

        # CALCULATE the malrule answer: base * exponent [WRONG]
        malrule_answer = base * exponent

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, base, exponent, malrule_answer)
        else:
            steps = self._generate_concise_steps(problem, base, exponent, malrule_answer)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
