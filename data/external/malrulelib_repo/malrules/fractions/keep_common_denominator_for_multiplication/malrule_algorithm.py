"""
Malrule algorithm for Keep-Common-Denominator-For-Multiplication.

Students keep the common denominator when multiplying fractions: (a/b)×(c/b) = (a×c)/b
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
import math

class KeepCommonDenominatorForMultiplicationMalrule(Malrule):
    """Student keeps common denominator instead of multiplying denominators."""

    def get_name(self):
        return "Keep-Common-Denominator-For-Multiplication"

    def get_description(self):
        return (
            "Students incorrectly keep the common denominator when multiplying fractions "
            "with like denominators: (a/b)×(c/b) = (a×c)/b instead of (a×c)/(b×b). "
            "For example, (2/5)×(3/5) = 6/5 instead of the correct answer 6/25. This is an "
            "overgeneralization error where students apply the fraction addition rule "
            "(keep the common denominator) to multiplication. Newton et al. (2014) found "
            "students were particularly prone to this error on like-denominator problems."
        )

    def calculate_expected_answer(self, problem: Problem) -> str:
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Backwards compatibility
        malrule_num = problem.metadata['malrule_numerator']
        malrule_den = problem.metadata['malrule_denominator']
        return f"{malrule_num}/{malrule_den}"

    def _generate_concise_steps(self, problem: Problem, malrule_answer: str) -> list:
        """Generate concise steps with only formula and values."""
        template = problem.metadata.get('template', 'basic_common_denominator')
        b = problem.metadata['denominator']
        malrule_num = problem.metadata['malrule_numerator']
        malrule_den = problem.metadata['malrule_denominator']

        steps = []
        steps.append(f"Question: {problem.text}")

        if template == 'three_fractions':
            a = problem.metadata['numerator1']
            c = problem.metadata['numerator2']
            d = problem.metadata['numerator3']
            steps.append(f"{a}/{b} × {c}/{b} × {d}/{b} = ({a}×{c}×{d})/{b}")
            steps.append(f"= {a*c*d}/{b}")
        elif template == 'mixed_numbers':
            improper1 = problem.metadata['improper1']
            improper2 = problem.metadata['improper2']
            steps.append(f"{improper1}/{b} × {improper2}/{b} = ({improper1}×{improper2})/{b}")
            steps.append(f"= {improper1*improper2}/{b}")
        else:  # basic_common_denominator, larger_denominators, word_problem
            a = problem.metadata['numerator1']
            c = problem.metadata['numerator2']
            steps.append(f"{a}/{b} × {c}/{b} = ({a}×{c})/{b}")
            steps.append(f"= {a*c}/{b}")

        if str(malrule_num) + "/" + str(malrule_den) != malrule_answer:
            steps.append(f"= {malrule_answer}")

        steps.append(f"Answer: {malrule_answer}")
        return steps

    def _generate_verbose_steps(self, problem: Problem, malrule_answer: str) -> list:
        """Generate verbose steps with full explanations."""
        template = problem.metadata.get('template', 'basic_common_denominator')
        b = problem.metadata['denominator']
        malrule_num = problem.metadata['malrule_numerator']
        malrule_den = problem.metadata['malrule_denominator']

        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: Keep the common denominator (treating multiplication like addition)")
        steps.append("")

        if template == 'three_fractions':
            a = problem.metadata['numerator1']
            c = problem.metadata['numerator2']
            d = problem.metadata['numerator3']
            steps.append(f"  All fractions have denominator {b}, so keep it")
            steps.append(f"  Multiply numerators: {a} × {c} × {d} = {a*c*d}")
            steps.append(f"  = {a*c*d}/{b}")
        elif template == 'mixed_numbers':
            whole1 = problem.metadata['whole1']
            whole2 = problem.metadata['whole2']
            a = problem.metadata['numerator1']
            c = problem.metadata['numerator2']
            improper1 = problem.metadata['improper1']
            improper2 = problem.metadata['improper2']
            steps.append(f"  Convert to improper: {whole1} {a}/{b} = {improper1}/{b}, {whole2} {c}/{b} = {improper2}/{b}")
            steps.append(f"  Both have denominator {b}, so keep it")
            steps.append(f"  Multiply numerators: {improper1} × {improper2} = {improper1*improper2}")
            steps.append(f"  = {improper1*improper2}/{b}")
        else:  # basic_common_denominator, larger_denominators, word_problem
            a = problem.metadata['numerator1']
            c = problem.metadata['numerator2']
            steps.append(f"  Both fractions have denominator {b}, so keep it")
            steps.append(f"  Multiply numerators: {a} × {c} = {a*c}")
            steps.append(f"  = {a*c}/{b}")

        if str(malrule_num) + "/" + str(malrule_den) != malrule_answer:
            steps.append(f"  Simplify: {malrule_answer}")

        steps.append("")
        steps.append(f"Student's answer: {malrule_answer}")
        steps.append("")
        steps.append(
            f"The student incorrectly keeps the common denominator {b}, overgeneralizing "
            f"the addition rule to multiplication. In multiplication, we must multiply "
            f"both numerators AND denominators."
        )

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply the keep-common-denominator malrule."""
        if 'malrule_answer' in problem.metadata:
            malrule_answer = self.calculate_expected_answer(problem)
        else:
            malrule_num = problem.metadata['malrule_numerator']
            malrule_den = problem.metadata['malrule_denominator']
            malrule_answer = f"{malrule_num}/{malrule_den}"

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
