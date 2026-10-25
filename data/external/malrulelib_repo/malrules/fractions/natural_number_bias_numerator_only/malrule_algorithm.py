"""
Natural-Number-Bias-Numerator-Only malrule algorithm.

Implements the systematic error of comparing fractions by comparing
their numerators only - larger numerator = larger fraction.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List

class NaturalNumberBiasNumeratorOnlyMalrule(Malrule):
    """
    Implements the Natural-Number-Bias-Numerator-Only bug.

    Students incorrectly compare fractions by comparing numerators only.
    They believe larger numerator = larger fraction, ignoring denominators.

    Example: 3/4 < 5/8 because 3 < 5 (WRONG!)

    This is a very common misconception stemming from natural number bias.
    """

    def get_name(self) -> str:
        return "Natural-Number-Bias-Numerator-Only (Whole Number Bias)"

    def get_description(self) -> str:
        return (
            "Students incorrectly compare fractions by comparing their numerators only, "
            "ignoring the denominators entirely. They believe that a larger numerator means "
            "a larger fraction. For example: 3/4 < 5/8 because 3 < 5 (incorrect). This is a "
            "manifestation of the 'natural number bias' or 'whole number bias'—the tendency "
            "to apply natural number properties inappropriately to rational numbers."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Calculate it from the operands
        # num1 = problem.metadata['num1']
        # den1 = problem.metadata['den1']
        # num2 = problem.metadata['num2']
        # den2 = problem.metadata['den2']
        # # Malrule: compare by numerators only
        # if num1 > num2:
        #     return f"{num1}/{den1}"
        # elif num1 < num2:
        #     return f"{num2}/{den2}"
        # else:
        #     return "equal"
        return self._apply_malrule(problem).answer

    def _generate_concise_steps(self, problem: Problem, malrule_answer: str) -> list:
        """Generate concise steps with only formula and values."""
        template = problem.metadata.get('template', 'basic_comparison')

        steps = []
        steps.append(f"Question: {problem.text}")

        if template in ['multiple_choice', 'ordering', 'word_problem_multiple_choice', 'word_problem_ordering']:
            num1 = problem.metadata['num1']
            den1 = problem.metadata['den1']
            num2 = problem.metadata['num2']
            den2 = problem.metadata['den2']
            num3 = problem.metadata['num3']
            den3 = problem.metadata['den3']

            steps.append(f"Numerators: {num1}, {num2}, {num3}")
            if template in ['multiple_choice', 'word_problem_multiple_choice']:
                steps.append(f"Largest numerator: {num3}")
            else:
                steps.append(f"Order: {num1} < {num2} < {num3}")
        else:
            num1 = problem.metadata['num1']
            den1 = problem.metadata['den1']
            num2 = problem.metadata['num2']
            den2 = problem.metadata['den2']

            steps.append(f"Numerators: {num1} vs {num2}")
            if num1 > num2:
                steps.append(f"{num1} > {num2}")
            elif num1 < num2:
                steps.append(f"{num1} < {num2}")
            else:
                steps.append(f"{num1} = {num2}")

        steps.append(f"Answer: {malrule_answer}")
        return steps

    def _generate_verbose_steps(self, problem: Problem, malrule_answer: str) -> list:
        """Generate verbose steps with full explanations."""
        template = problem.metadata.get('template', 'basic_comparison')

        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: Compare fractions by looking at numerators only")
        steps.append("  Student thinks: 'Bigger numerator = bigger fraction'")
        steps.append("")

        if template in ['multiple_choice', 'ordering', 'word_problem_multiple_choice', 'word_problem_ordering']:
            num1 = problem.metadata['num1']
            den1 = problem.metadata['den1']
            num2 = problem.metadata['num2']
            den2 = problem.metadata['den2']
            num3 = problem.metadata['num3']
            den3 = problem.metadata['den3']

            steps.append(f"Fractions: {num1}/{den1}, {num2}/{den2}, {num3}/{den3}")
            steps.append(f"Look at numerators only: {num1}, {num2}, {num3}")
            steps.append("")

            if template in ['multiple_choice', 'word_problem_multiple_choice']:
                steps.append(f"Largest numerator is {num3}")
                steps.append(f"MALRULE: Choose {num3}/{den3} (INCORRECT - ignored denominators)")
            else:
                steps.append(f"Order by numerators: {num1} < {num2} < {num3}")
                steps.append(f"MALRULE: Order is {num1}/{den1}, {num2}/{den2}, {num3}/{den3}")
                steps.append("  (INCORRECT - ignored denominators)")
        else:
            num1 = problem.metadata['num1']
            den1 = problem.metadata['den1']
            num2 = problem.metadata['num2']
            den2 = problem.metadata['den2']

            steps.append(f"Comparing: {num1}/{den1} vs {num2}/{den2}")
            steps.append(f"Look at numerators only: {num1} vs {num2}")
            steps.append("")

            if num1 > num2:
                steps.append(f"Since {num1} > {num2}, the fraction {num1}/{den1} must be larger")
                steps.append(f"MALRULE REASONING: Bigger numerator = bigger fraction")
            elif num1 < num2:
                steps.append(f"Since {num1} < {num2}, the fraction {num1}/{den1} must be smaller")
                steps.append(f"MALRULE REASONING: Smaller numerator = smaller fraction")
            else:
                steps.append(f"Numerators are the same ({num1})")
                steps.append(f"The fractions must be equal (ignoring denominators)")

            steps.append("")
            steps.append(f"MALRULE: Answer is {malrule_answer} (INCORRECT - ignored denominators)")

        steps.append("")
        steps.append(f"Final Answer: {malrule_answer}")
        steps.append("")
        steps.append("Missing: Understanding that BOTH numerator AND denominator determine fraction size")

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Natural-Number-Bias-Numerator-Only malrule.

        Args:
            problem: Fraction comparison problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with incorrect numerator-only comparison
        """
        template = problem.metadata.get('template', 'basic_comparison')
        # Calculate for backwards compatibility
        if template in ['multiple_choice', 'ordering', 'word_problem_multiple_choice', 'word_problem_ordering']:
            num1 = problem.metadata['num1']
            den1 = problem.metadata['den1']
            num2 = problem.metadata['num2']
            den2 = problem.metadata['den2']
            num3 = problem.metadata['num3']
            den3 = problem.metadata['den3']
            if template in ['word_problem_multiple_choice', 'multiple_choice']:
                malrule_answer = f"{num3}/{den3}"
            else:
                malrule_answer = f"{num1}/{den1}, {num2}/{den2}, {num3}/{den3}"
        else:
            num1 = problem.metadata['num1']
            den1 = problem.metadata['den1']
            num2 = problem.metadata['num2']
            den2 = problem.metadata['den2']
            if num1 > num2:
                malrule_answer = f"{num1}/{den1}"
            elif num1 < num2:
                malrule_answer = f"{num2}/{den2}"
            else:
                malrule_answer = "equal"

        if verbose:
            steps = self._generate_verbose_steps(problem, malrule_answer)
        else:
            steps = self._generate_concise_steps(problem, malrule_answer)

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
