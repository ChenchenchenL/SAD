"""
Correct algorithm for fraction division.
"""

import sys
from fractions import Fraction
sys.path.append('/home/user/malrule-coding')

from utils import CorrectAlgorithm, Problem, Solution


class FractionDivisionCorrectAlgorithm(CorrectAlgorithm):
    """Correctly divides fractions by multiplying by the reciprocal."""

    def get_name(self):
        return "Correct Fraction Division"

    def get_description(self):
        return "Correctly divides fractions by multiplying by the reciprocal (Keep-Change-Flip)"

    def _generate_concise_steps(self, problem: Problem, correct_answer: str) -> list:
        """Generate concise steps with only formula and values."""
        template = problem.metadata.get('template', 'basic_fraction_division')
        a = problem.metadata['a']
        b = problem.metadata['b']
        c = problem.metadata['c']
        d = problem.metadata['d']

        correct_frac = Fraction(a * d, b * c)
        correct_num = correct_frac.numerator
        correct_den = correct_frac.denominator

        steps = []
        steps.append(f"Question: {problem.text}")

        if template == 'basic_fraction_division':
            steps.append(f"({a}/{b}) ÷ ({c}/{d}) = ({a}/{b}) × ({d}/{c})")
            steps.append(f"= {a*d}/{b*c}")
        elif template == 'whole_number_divisor':
            steps.append(f"({a}/{b}) ÷ {c} = ({a}/{b}) × (1/{c})")
            steps.append(f"= {a}/{b*c}")
        elif template == 'whole_number_dividend':
            steps.append(f"{a} ÷ ({c}/{d}) = {a} × ({d}/{c})")
            steps.append(f"= {a*d}/{c}")
        elif template == 'mixed_numbers':
            steps.append(f"({a}/{b}) ÷ ({c}/{d}) = ({a}/{b}) × ({d}/{c})")
            steps.append(f"= {a*d}/{b*c}")
        elif template in ['word_problem', 'word_problem_whole_divisor', 'word_problem_whole_dividend', 'word_problem_mixed']:
            steps.append(f"({a}/{b}) ÷ ({c}/{d}) = ({a}/{b}) × ({d}/{c})")
            steps.append(f"= {a*d}/{b*c}")

        if a*d != correct_num or b*c != correct_den:
            steps.append(f"= {correct_answer}")

        steps.append(f"Answer: {correct_answer}")
        return steps

    def _generate_verbose_steps(self, problem: Problem, correct_answer: str) -> list:
        """Generate verbose steps with full explanations."""
        template = problem.metadata.get('template', 'basic_fraction_division')
        a = problem.metadata['a']
        b = problem.metadata['b']
        c = problem.metadata['c']
        d = problem.metadata['d']

        correct_frac = Fraction(a * d, b * c)
        correct_num = correct_frac.numerator
        correct_den = correct_frac.denominator

        steps = []

        if template == 'basic_fraction_division':
            steps.append(f"Problem: ({a}/{b}) ÷ ({c}/{d})")
            steps.append("")
            steps.append("CORRECT METHOD: Keep-Change-Flip")
            steps.append(f"  ({a}/{b}) × ({d}/{c}) = {a*d}/{b*c}")
            if a*d != correct_num or b*c != correct_den:
                steps.append(f"  = {correct_num}/{correct_den} (simplified)")

        elif template == 'whole_number_divisor':
            steps.append(f"Problem: ({a}/{b}) ÷ {c}")
            steps.append("")
            steps.append("CORRECT METHOD: Flip whole number to fraction")
            steps.append(f"  {c} = {c}/1, so reciprocal is 1/{c}")
            steps.append(f"  ({a}/{b}) × (1/{c}) = {a}/{b*c}")
            if a != correct_num or b*c != correct_den:
                steps.append(f"  = {correct_num}/{correct_den} (simplified)")

        elif template == 'whole_number_dividend':
            steps.append(f"Problem: {a} ÷ ({c}/{d})")
            steps.append("")
            steps.append("CORRECT METHOD: Flip fraction and multiply")
            steps.append(f"  {a} × ({d}/{c}) = {a*d}/{c}")
            if a*d != correct_num or c != correct_den:
                steps.append(f"  = {correct_num}/{correct_den} (simplified)")

        elif template == 'mixed_numbers':
            whole1 = problem.metadata['whole1']
            whole2 = problem.metadata['whole2']
            frac1_num = problem.metadata['frac1_num']
            frac1_den = problem.metadata['frac1_den']
            frac2_num = problem.metadata['frac2_num']
            frac2_den = problem.metadata['frac2_den']

            steps.append(f"Problem: {whole1} {frac1_num}/{frac1_den} ÷ {whole2} {frac2_num}/{frac2_den}")
            steps.append("")
            steps.append("Step 1: Convert to improper fractions")
            steps.append(f"  {a}/{b} ÷ {c}/{d}")
            steps.append("")
            steps.append("Step 2: Keep-Change-Flip")
            steps.append(f"  ({a}/{b}) × ({d}/{c}) = {a*d}/{b*c}")
            if a*d != correct_num or b*c != correct_den:
                steps.append(f"  = {correct_num}/{correct_den} (simplified)")

        elif template in ['word_problem', 'word_problem_whole_divisor', 'word_problem_whole_dividend', 'word_problem_mixed']:
            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append(f"  This becomes: ({a}/{b}) ÷ ({c}/{d})")
            steps.append("")
            steps.append("CORRECT METHOD: Keep-Change-Flip")
            steps.append(f"  ({a}/{b}) × ({d}/{c}) = {a*d}/{b*c}")
            if a*d != correct_num or b*c != correct_den:
                steps.append(f"  = {correct_num}/{correct_den} (simplified)")

        steps.append("")
        steps.append(f"Answer: {correct_answer}")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct fraction division algorithm.

        Args:
            problem: The fraction division problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution showing correct approach (multiply by reciprocal)
        """
        a = problem.metadata['a']
        b = problem.metadata['b']
        c = problem.metadata['c']
        d = problem.metadata['d']

        # Calculate the correct answer by dividing fractions
        # (a/b) ÷ (c/d) = (a/b) × (d/c) = (a×d)/(b×c)
        correct_frac = Fraction(a * d, b * c)
        correct_num = correct_frac.numerator
        correct_den = correct_frac.denominator
        correct_answer = f"{correct_num}/{correct_den}"

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
