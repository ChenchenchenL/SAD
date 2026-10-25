"""
Correct fraction comparison algorithm.

Implements proper fraction comparison by finding common denominators
or cross-multiplication.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import CorrectAlgorithm, Problem, Solution
import math


class FractionComparisonCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for comparing fractions.

    Uses cross-multiplication or common denominators to compare fractions properly.
    """

    def get_name(self) -> str:
        return "Correct Fraction Comparison"

    def get_description(self) -> str:
        return (
            "Compares fractions correctly using cross-multiplication or common denominators. "
            "Smaller denominator means larger piece size for same numerator."
        )
    def calculate_correct_answer(self, problem):
        """Calculate the correct comparison result as the larger/smaller fraction."""
        num1 = problem.metadata.get('num1', problem.metadata.get('a'))
        den1 = problem.metadata.get('den1', problem.metadata.get('b'))
        num2 = problem.metadata.get('num2', problem.metadata.get('c'))
        den2 = problem.metadata.get('den2', problem.metadata.get('d'))

        # Compare num1/den1 and num2/den2 by cross-multiplication
        # num1/den1 > num2/den2 iff num1*den2 > den1*num2
        cross1 = num1 * den2
        cross2 = num2 * den1

        if cross1 > cross2:
            # Handle special case of 1/1 = 1
            if num1 == 1 and den1 == 1:
                return "1"
            return f"{num1}/{den1}"
        elif cross1 < cross2:
            # Handle special case of 1/1 = 1
            if num2 == 1 and den2 == 1:
                return "1"
            return f"{num2}/{den2}"
        else:
            return "equal"



    def _generate_concise_steps_two_fractions(self, problem: Problem, num1: int, den1: int,
                                               num2: int, den2: int, cross1: int, cross2: int,
                                               answer: str) -> list:
        """Generate concise steps for two-fraction comparison."""
        steps = []

        # Question
        steps.append(problem.text)

        # Formula extraction
        steps.append(f"{num1}/{den1} vs {num2}/{den2}")

        # Cross multiplication step
        steps.append(f"{num1} × {den2} = {cross1}")
        steps.append(f"{num2} × {den1} = {cross2}")

        # Comparison step
        if cross1 > cross2:
            steps.append(f"{cross1} > {cross2}")
        elif cross1 < cross2:
            steps.append(f"{cross1} < {cross2}")
        else:
            steps.append(f"{cross1} = {cross2}")

        # Final answer
        steps.append(answer)

        return steps

    def _generate_concise_steps_three_fractions(self, problem: Problem, num1: int, den1: int,
                                                 num2: int, den2: int, num3: int, den3: int,
                                                 answer: str) -> list:
        """Generate concise steps for three-fraction ordering."""
        steps = []

        # Question
        steps.append(problem.text)

        # Formula extraction
        steps.append(f"{num1}/{den1}, {num2}/{den2}, {num3}/{den3}")

        # Decimal conversion step
        steps.append(f"{num1}/{den1} = {num1/den1:.4f}")
        steps.append(f"{num2}/{den2} = {num2/den2:.4f}")
        steps.append(f"{num3}/{den3} = {num3/den3:.4f}")

        # Final answer
        steps.append(answer)

        return steps

    def _generate_verbose_steps_two_fractions(self, problem: Problem, num1: int, den1: int,
                                               num2: int, den2: int, cross1: int, cross2: int,
                                               answer: str) -> list:
        """Generate verbose steps for two-fraction comparison (original format)."""
        steps = []
        steps.append(f"Comparing: {num1}/{den1} vs {num2}/{den2}")
        steps.append(f"Method: Cross-multiplication")
        steps.append(f"Cross multiply: {num1} × {den2} = {cross1}")
        steps.append(f"Cross multiply: {num2} × {den1} = {cross2}")

        if cross1 > cross2:
            steps.append(f"Since {cross1} > {cross2}, we have {num1}/{den1} > {num2}/{den2}")
        elif cross1 < cross2:
            steps.append(f"Since {cross1} < {cross2}, we have {num1}/{den1} < {num2}/{den2}")
        else:
            steps.append(f"Since {cross1} = {cross2}, the fractions are equal")

        steps.append(f"Answer: {answer}")

        # Alternative explanation using common denominators
        lcm = (den1 * den2) // math.gcd(den1, den2)
        equiv1_num = num1 * (lcm // den1)
        equiv2_num = num2 * (lcm // den2)

        steps.append(f"\nAlternative: Using common denominator {lcm}")
        steps.append(f"{num1}/{den1} = {equiv1_num}/{lcm}")
        steps.append(f"{num2}/{den2} = {equiv2_num}/{lcm}")
        steps.append(f"Compare numerators: {equiv1_num} vs {equiv2_num}")

        return steps

    def _generate_verbose_steps_three_fractions(self, problem: Problem, num1: int, den1: int,
                                                 num2: int, den2: int, num3: int, den3: int,
                                                 answer: str) -> list:
        """Generate verbose steps for three-fraction ordering (original format)."""
        steps = []
        steps.append(f"Ordering: {num1}/{den1}, {num2}/{den2}, {num3}/{den3}")
        steps.append("Method: Convert to decimal to compare")
        steps.append(f"{num1}/{den1} = {num1/den1:.4f}")
        steps.append(f"{num2}/{den2} = {num2/den2:.4f}")
        steps.append(f"{num3}/{den3} = {num3/den3:.4f}")
        steps.append(f"Correct ordering: {answer}")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct fraction comparison.

        Args:
            problem: Fraction comparison problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with correct comparison (answer as string)
        """
        num1 = problem.metadata['num1']
        den1 = problem.metadata['den1']
        num2 = problem.metadata['num2']
        den2 = problem.metadata['den2']

        # Check if this is a 3-fraction ordering problem
        if 'num3' in problem.metadata:
            num3 = problem.metadata['num3']
            den3 = problem.metadata['den3']

            fractions_with_values = [
                (f"{num1}/{den1}", num1 / den1),
                (f"{num2}/{den2}", num2 / den2),
                (f"{num3}/{den3}", num3 / den3)
            ]
            fractions_with_values.sort(key=lambda x: x[1])
            answer = ", ".join([f[0] for f in fractions_with_values])

            if verbose:
                steps = self._generate_verbose_steps_three_fractions(
                    problem, num1, den1, num2, den2, num3, den3, answer
                )
            else:
                steps = self._generate_concise_steps_three_fractions(
                    problem, num1, den1, num2, den2, num3, den3, answer
                )

            return Solution(
                answer=answer,
                steps=steps,
                is_correct=True,
                algorithm_name=self.get_name()
            )

        # Two-fraction comparison
        cross1 = num1 * den2
        cross2 = num2 * den1

        if cross1 > cross2:
            # Handle special case of 1/1 = 1
            if num1 == 1 and den1 == 1:
                answer = "1"
            else:
                answer = f"{num1}/{den1}"
        elif cross1 < cross2:
            # Handle special case of 1/1 = 1
            if num2 == 1 and den2 == 1:
                answer = "1"
            else:
                answer = f"{num2}/{den2}"
        else:
            answer = "equal"

        # Use pre-calculated correct_answer from metadata if available
        if 'correct_answer' in problem.metadata:
            answer = self.calculate_correct_answer(problem)

        if verbose:
            steps = self._generate_verbose_steps_two_fractions(
                problem, num1, den1, num2, den2, cross1, cross2, answer
            )
        else:
            steps = self._generate_concise_steps_two_fractions(
                problem, num1, den1, num2, den2, cross1, cross2, answer
            )

        return Solution(
            answer=str(answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
