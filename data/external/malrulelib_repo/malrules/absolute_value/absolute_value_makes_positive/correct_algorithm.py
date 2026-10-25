"""
Correct algorithm for absolute value equations.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import CorrectAlgorithm, Problem, Solution


class AbsoluteValueEquationCorrectAlgorithm(CorrectAlgorithm):
    """Correctly recognizes when |x| = k has no solution (k < 0)."""

    def get_name(self):
        return "Correct Absolute Value Equation"

    def get_description(self):
        return "Correctly recognizes that |x| = k has no solution when k < 0"

    def _generate_verbose_steps(self, problem: Problem, template: str, negative_value: int, correct_answer: str) -> list:
        """Generate verbose, explanatory steps."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")

        # Handle word problems by detecting embedded formula type
        if template == 'word_problem':
            word_problem_type = problem.metadata.get('word_problem_type', 'basic_x')
            steps.append("CORRECT METHOD: Identify the embedded equation and analyze")
            steps.append("")

            if word_problem_type == 'basic_x':
                steps.append(f"Step 1: Identify the equation")
                steps.append(f"  The problem asks us to solve: |x| = {negative_value}")
            elif word_problem_type == 'x_plus_a':
                a = problem.metadata.get('a', 0)
                sign_str = "+" if a >= 0 else ""
                steps.append(f"Step 1: Identify the equation")
                steps.append(f"  The problem asks us to solve: |x {sign_str} {a}| = {negative_value}")
            else:  # ax_plus_b
                a = problem.metadata.get('a', 2)
                b = problem.metadata.get('b', 0)
                if a == 1:
                    expr = f"x"
                elif a == -1:
                    expr = f"-x"
                else:
                    expr = f"{a}x"
                sign_str = "+" if b >= 0 else ""
                if b != 0:
                    expr += f" {sign_str} {b}"
                steps.append(f"Step 1: Identify the equation")
                steps.append(f"  The problem asks us to solve: |{expr}| = {negative_value}")

            steps.append("")
            steps.append("Step 2: Check if solution is possible")
            steps.append("  Key Insight: Absolute value represents DISTANCE")
            steps.append("  • Distance is always non-negative")
            steps.append("  • Therefore, |expression| ≥ 0 for any expression")
            steps.append("")
            steps.append("Analysis:")
            steps.append(f"  We need: |expression| = {negative_value}")
            steps.append(f"  But {negative_value} < 0")
            steps.append("  And |expression| ≥ 0 always")
            steps.append("")
            steps.append(f"  Since {negative_value} < 0, there is no solution")
            steps.append("")
            steps.append(f"Answer: {correct_answer}")
        else:
            steps.append("CORRECT METHOD: Check if solution is possible")
            steps.append("")
            steps.append("Key Insight: What is absolute value?")
            steps.append("  • |x| represents the DISTANCE from 0 to x")
            steps.append("  • Distance is always non-negative: |x| ≥ 0")
            steps.append("  • Therefore, |x| can NEVER be negative")
            steps.append("")
            steps.append("Analysis:")
            steps.append(f"  We need: |expression| = {negative_value}")
            steps.append(f"  But {negative_value} < 0")
            steps.append("  And |expression| ≥ 0 for all values")
            steps.append("")
            steps.append(f"  Since {negative_value} < 0, there is no solution")
            steps.append("")
            steps.append(f"Answer: {correct_answer}")
            steps.append("")
            steps.append(
                f"The key is understanding that absolute value ALWAYS produces a non-negative output. "
                f"The equation asks for a value whose absolute value is {negative_value}, "
                f"which is impossible since absolute values cannot be negative."
            )

        return steps

    def _generate_concise_steps(self, problem: Problem, template: str, negative_value: int, correct_answer: str) -> list:
        """Generate concise steps with just formulas and values."""
        steps = [f"Problem: {problem.text}"]

        # Handle word problems by detecting embedded formula type
        if template == 'word_problem':
            word_problem_type = problem.metadata.get('word_problem_type', 'basic_x')

            if word_problem_type == 'basic_x':
                steps.append(f"|x| = {negative_value}")
            elif word_problem_type == 'x_plus_a':
                a = problem.metadata.get('a', 0)
                sign_str = "+" if a >= 0 else ""
                steps.append(f"|x {sign_str} {a}| = {negative_value}")
            else:  # ax_plus_b
                a = problem.metadata.get('a', 2)
                b = problem.metadata.get('b', 0)
                if a == 1:
                    expr = f"x"
                elif a == -1:
                    expr = f"-x"
                else:
                    expr = f"{a}x"
                sign_str = "+" if b >= 0 else ""
                if b != 0:
                    expr += f" {sign_str} {b}"
                steps.append(f"|{expr}| = {negative_value}")

            steps.append(f"|expression| ≥ 0, but {negative_value} < 0")
        else:
            steps.append(f"|expression| = {negative_value}")
            steps.append(f"|expression| ≥ 0, but {negative_value} < 0")

        steps.append(correct_answer)
        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct absolute value equation algorithm.

        Args:
            problem: The absolute value equation problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution showing no solution for negative right side
        """
        template = problem.metadata.get('template', 'basic_equation')
        negative_value = problem.metadata['negative_value']

        # Actually compute the correct answer: always "No solution" for negative values
        if template == 'word_problem':
            correct_answer = "No solution (absolute value cannot be negative)"
        else:
            correct_answer = "No solution"

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, template, negative_value, correct_answer)
        else:
            steps = self._generate_concise_steps(problem, template, negative_value, correct_answer)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
