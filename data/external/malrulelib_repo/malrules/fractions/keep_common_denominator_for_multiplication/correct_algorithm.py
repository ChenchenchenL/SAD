"""
Correct algorithm for fraction multiplication.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import CorrectAlgorithm, Problem, Solution


class FractionMultiplicationCorrectAlgorithm(CorrectAlgorithm):
    """Correctly multiplies fractions: (a/b)×(c/d) = (a×c)/(b×d)."""

    def get_name(self):
        return "Fraction Multiplication"

    def get_description(self):
        return "Multiplies fractions by multiplying numerators and denominators"

    def _generate_concise_steps(self, problem: Problem, correct_answer: str) -> list:
        """Generate concise steps with only formula and values."""
        template = problem.metadata.get('template', 'basic_common_denominator')
        b = problem.metadata['denominator']
        correct_num = problem.metadata['correct_numerator']
        correct_den = problem.metadata['correct_denominator']

        steps = []
        steps.append(f"Question: {problem.text}")

        if template == 'three_fractions':
            a = problem.metadata['numerator1']
            c = problem.metadata['numerator2']
            d = problem.metadata['numerator3']
            steps.append(f"{a}/{b} × {c}/{b} × {d}/{b} = ({a}×{c}×{d}) / ({b}×{b}×{b})")
            steps.append(f"= {a*c*d}/{b*b*b}")
        elif template == 'mixed_numbers':
            improper1 = problem.metadata['improper1']
            improper2 = problem.metadata['improper2']
            steps.append(f"{improper1}/{b} × {improper2}/{b} = ({improper1}×{improper2}) / ({b}×{b})")
            steps.append(f"= {improper1*improper2}/{b*b}")
        else:  # basic_common_denominator, larger_denominators, word_problem
            a = problem.metadata['numerator1']
            c = problem.metadata['numerator2']
            steps.append(f"{a}/{b} × {c}/{b} = ({a}×{c}) / ({b}×{b})")
            steps.append(f"= {a*c}/{b*b}")

        if correct_answer != str(correct_num) + "/" + str(correct_den):
            steps.append(f"= {correct_answer}")

        steps.append(f"Answer: {correct_answer}")
        return steps

    def _generate_verbose_steps(self, problem: Problem, correct_answer: str) -> list:
        """Generate verbose steps with full explanations."""
        template = problem.metadata.get('template', 'basic_common_denominator')
        correct_num = problem.metadata['correct_numerator']
        correct_den = problem.metadata['correct_denominator']
        b = problem.metadata['denominator']

        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD: Multiply numerators AND denominators")
        steps.append("")

        if template == 'three_fractions':
            a = problem.metadata['numerator1']
            c = problem.metadata['numerator2']
            d = problem.metadata['numerator3']
            steps.append(f"  {a}/{b} × {c}/{b} × {d}/{b} = ({a}×{c}×{d}) / ({b}×{b}×{b})")
            steps.append(f"  = {a*c*d}/{b*b*b}")
        elif template == 'mixed_numbers':
            whole1 = problem.metadata['whole1']
            whole2 = problem.metadata['whole2']
            a = problem.metadata['numerator1']
            c = problem.metadata['numerator2']
            improper1 = problem.metadata['improper1']
            improper2 = problem.metadata['improper2']
            steps.append(f"  Convert to improper: {whole1} {a}/{b} = {improper1}/{b}, {whole2} {c}/{b} = {improper2}/{b}")
            steps.append(f"  Multiply: {improper1}/{b} × {improper2}/{b} = ({improper1}×{improper2}) / ({b}×{b})")
            steps.append(f"  = {improper1*improper2}/{b*b}")
        else:  # basic_common_denominator, larger_denominators, word_problem
            a = problem.metadata['numerator1']
            c = problem.metadata['numerator2']
            steps.append(f"  {a}/{b} × {c}/{b} = ({a}×{c}) / ({b}×{b})")
            steps.append(f"  = {a*c}/{b*b}")

        if correct_answer != str(correct_num) + "/" + str(correct_den):
            steps.append(f"  Simplify: {correct_answer}")

        steps.append("")
        steps.append(f"Answer: {correct_answer}")
        steps.append("")
        steps.append(
            f"To multiply fractions, we multiply numerators AND denominators. "
            f"Even though fractions share denominator {b}, we still multiply it."
        )

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply correct fraction multiplication algorithm."""
        correct_num = problem.metadata['correct_numerator']
        correct_den = problem.metadata['correct_denominator']
        correct_answer = problem.metadata.get('correct_answer', f"{correct_num}/{correct_den}")

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
