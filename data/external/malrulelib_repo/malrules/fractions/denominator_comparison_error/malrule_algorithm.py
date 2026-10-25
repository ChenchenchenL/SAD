"""
Denominator-Comparison-Error malrule algorithm.

Implements the systematic error of comparing fractions by comparing
their denominators only - larger denominator = larger fraction.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List

class DenominatorComparisonErrorMalrule(Malrule):
    """
    Implements the Denominator-Comparison-Error bug.

    Students incorrectly compare fractions by comparing denominators only.
    They believe larger denominator = larger fraction.

    Example: 1/4 > 1/3 because 4 > 3 (WRONG!)

    This is a very common misconception, especially for unit fractions.
    """

    def get_name(self) -> str:
        return "Denominator-Comparison-Error"

    def get_description(self) -> str:
        return (
            "Students incorrectly compare fractions by focusing on the denominator value, "
            "believing that a larger denominator means a larger fraction. For example: "
            "1/4 > 1/3 because 4 > 3 (incorrect). This error reflects 'whole number bias' "
            "(Ni & Zhou, 2005) - the overgeneralization of whole-number comparison rules "
            "where larger numbers always mean 'more.' Students fail to understand the "
            "inverse relationship: larger denominators mean smaller pieces."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Get fraction components
        num1 = problem.metadata.get('num1', problem.metadata.get('a'))
        den1 = problem.metadata.get('den1', problem.metadata.get('b'))
        num2 = problem.metadata.get('num2', problem.metadata.get('c'))
        den2 = problem.metadata.get('den2', problem.metadata.get('d'))

        # Check if this is a 3-fraction ordering problem
        if 'num3' in problem.metadata:
            num3 = problem.metadata['num3']
            den3 = problem.metadata['den3']

            # Malrule: order by denominator size (smallest denom = smallest fraction)
            # Collect fractions with their denominators
            fractions = [
                (f"{num1}/{den1}", den1),
                (f"{num2}/{den2}", den2),
                (f"{num3}/{den3}", den3)
            ]
            # Sort by denominator (ascending) - malrule thinks small denom = small fraction
            fractions.sort(key=lambda x: x[1])
            # Return ordered list as string
            return ", ".join([f[0] for f in fractions])

        # Two-fraction comparison
        # Malrule: larger denominator = larger fraction (INCORRECT)
        if den1 > den2:
            return f"{num1}/{den1}"
        elif den1 < den2:
            return f"{num2}/{den2}"
        else:
            # Same denominator - compare numerators (this part is correct)
            if num1 > num2:
                return f"{num1}/{den1}"
            elif num1 < num2:
                return f"{num2}/{den2}"
            else:
                return "equal"

    def _generate_concise_steps_two_fractions(self, problem: Problem, num1: int, den1: int,
                                               num2: int, den2: int, answer: str) -> list:
        """Generate concise steps for two-fraction malrule comparison."""
        steps = []

        # Question
        steps.append(problem.text)

        # Formula extraction
        steps.append(f"{num1}/{den1} vs {num2}/{den2}")

        # Compare denominators step
        steps.append(f"{den1} vs {den2}")

        # Comparison result
        if den1 > den2:
            steps.append(f"{den1} > {den2}")
        elif den1 < den2:
            steps.append(f"{den1} < {den2}")
        else:
            steps.append(f"{den1} = {den2}")

        # Final answer
        steps.append(answer)

        return steps

    def _generate_concise_steps_three_fractions(self, problem: Problem, num1: int, den1: int,
                                                 num2: int, den2: int, num3: int, den3: int,
                                                 ordered: list, answer: str) -> list:
        """Generate concise steps for three-fraction malrule ordering."""
        steps = []

        # Question
        steps.append(problem.text)

        # Formula extraction
        steps.append(f"{num1}/{den1}, {num2}/{den2}, {num3}/{den3}")

        # Denominators step
        steps.append(f"Denominators: {den1}, {den2}, {den3}")

        # Ordered result
        steps.append(f"{', '.join(ordered)}")

        # Final answer
        steps.append(answer)

        return steps

    def _generate_verbose_steps_two_fractions(self, problem: Problem, num1: int, den1: int,
                                               num2: int, den2: int, answer: str, result: str) -> list:
        """Generate verbose steps for two-fraction malrule comparison (original format)."""
        steps = []

        steps.append(f"Comparing: {num1}/{den1} vs {num2}/{den2}")
        steps.append(f"MALRULE: Compare by looking at denominators")

        # Compare denominators
        steps.append(f"Look at denominators: {den1} vs {den2}")

        if den1 > den2:
            steps.append(f"Since {den1} > {den2}, the fraction {num1}/{den1} must be larger")
            steps.append(f"MALRULE REASONING: Bigger denominator = bigger fraction")
        elif den1 < den2:
            steps.append(f"Since {den1} < {den2}, the fraction {num1}/{den1} must be smaller")
            steps.append(f"MALRULE REASONING: Smaller denominator = smaller fraction")
        else:
            # Same denominator - student would look at numerators
            steps.append(f"Denominators are the same ({den1}), so look at numerators")
            if num1 > num2:
                steps.append(f"Since {num1} > {num2}, the fraction {num1}/{den1} is larger")
            elif num1 < num2:
                steps.append(f"Since {num1} < {num2}, the fraction {num1}/{den1} is smaller")

        steps.append(f"Answer: {answer}")

        return steps

    def _generate_verbose_steps_three_fractions(self, problem: Problem, num1: int, den1: int,
                                                 num2: int, den2: int, num3: int, den3: int,
                                                 ordered: list, answer: str) -> list:
        """Generate verbose steps for three-fraction malrule ordering (original format)."""
        steps = []

        steps.append(f"Ordering: {num1}/{den1}, {num2}/{den2}, {num3}/{den3}")
        steps.append(f"MALRULE: Order by denominator size")
        steps.append(f"MALRULE REASONING: Smaller denominator = smaller fraction")
        steps.append("")
        steps.append(f"Denominators: {den1}, {den2}, {den3}")
        steps.append(f"Ordered by denominator: {', '.join(ordered)}")
        steps.append("(INCORRECT - smaller denominator actually means LARGER fraction!)")

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Denominator-Comparison-Error malrule.

        Args:
            problem: Fraction comparison problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with incorrect denominator-based comparison (answer as string)
        """
        num1 = problem.metadata['num1']
        den1 = problem.metadata['den1']
        num2 = problem.metadata['num2']
        den2 = problem.metadata['den2']

        # Check if this is a 3-fraction ordering problem
        if 'num3' in problem.metadata:
            num3 = problem.metadata['num3']
            den3 = problem.metadata['den3']

            # Sort fractions by denominator
            fractions = [
                (f"{num1}/{den1}", den1),
                (f"{num2}/{den2}", den2),
                (f"{num3}/{den3}", den3)
            ]
            fractions.sort(key=lambda x: x[1])

            ordered = [f[0] for f in fractions]
            answer_str = ", ".join(ordered)

            if verbose:
                steps = self._generate_verbose_steps_three_fractions(
                    problem, num1, den1, num2, den2, num3, den3, ordered, answer_str
                )
            else:
                steps = self._generate_concise_steps_three_fractions(
                    problem, num1, den1, num2, den2, num3, den3, ordered, answer_str
                )

            return Solution(
                answer=answer_str,
                steps=steps,
                is_correct=False,
                algorithm_name=self.get_name()
            )

        # Two-fraction comparison
        if den1 > den2:
            result = f"{num1}/{den1} > {num2}/{den2}"
            answer = f"{num1}/{den1}"
        elif den1 < den2:
            result = f"{num1}/{den1} < {num2}/{den2}"
            answer = f"{num2}/{den2}"
        else:
            # Same denominator - student would look at numerators
            if num1 > num2:
                result = f"{num1}/{den1} > {num2}/{den2}"
                answer = f"{num1}/{den1}"
            elif num1 < num2:
                result = f"{num1}/{den1} < {num2}/{den2}"
                answer = f"{num2}/{den2}"
            else:
                result = f"{num1}/{den1} = {num2}/{den2}"
                answer = "equal"

        if verbose:
            steps = self._generate_verbose_steps_two_fractions(
                problem, num1, den1, num2, den2, answer, result
            )
        else:
            steps = self._generate_concise_steps_two_fractions(
                problem, num1, den1, num2, den2, answer
            )

        # Ensure answer is a string
        return Solution(
            answer=str(answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
