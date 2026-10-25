"""
Subtract-Across malrule algorithm.

Implements the systematic error where students incorrectly subtract
both numerators and denominators: a/b - c/d = (a-c)/(b-d)
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List
from math import gcd

class SubtractAcrossMalrule(Malrule):
    """
    Implements the Subtract-Across bug.

    Students incorrectly subtract numerators AND subtract denominators.
    For example: 3/4 - 1/2 = (3-1)/(4-2) = 2/2 = 1 (incorrect, should be 1/4).

    This is parallel to the Add-Numerators-Add-Denominators malrule,
    applying the same flawed logic to subtraction.
    """

    def get_name(self) -> str:
        return "Subtract-Across (Independent Whole Number Error)"

    def get_description(self) -> str:
        return (
            "When subtracting fractions with different denominators, students incorrectly "
            "subtract the numerators AND subtract the denominators: a/b - c/d = (a-c)/(b-d). "
            "For example: 3/4 - 1/2 = (3-1)/(4-2) = 2/2 = 1 (incorrect; correct answer is 1/4). "
            "Brown & Quinn (2006) documented this error in their analysis of algebra students' "
            "fraction errors, finding that students 'demonstrated the error of adding or subtracting "
            "numerators and denominators across' by extending whole number operations to fractions."
        )

    def _simplify_fraction(self, numerator: int, denominator: int) -> tuple:
        """Simplify a fraction to lowest terms."""
        if numerator == 0:
            return 0, denominator
        if denominator == 0:
            return numerator, denominator  # Keep as-is for undefined case
        common = gcd(abs(numerator), abs(denominator))
        return numerator // common, denominator // common

    def calculate_expected_answer(self, problem: Problem) -> str:
        """
        Calculate the expected incorrect answer for this malrule.

        For Subtract-Across:
        - Subtract all numerators: num1 - num2 - num3 - ...
        - Subtract all denominators: den1 - den2 - den3 - ...
        - Simplify the result
        - Handle edge cases (denominator = 0 or negative)

        Args:
            problem: Fraction subtraction problem

        Returns:
            Expected incorrect answer in the form "num/den"
        """

        # Otherwise, calculate it (backwards compatibility)
        fractions = problem.operands

        # MALRULE: Subtract all numerators and subtract all denominators
        result_num = fractions[0][0]  # Start with first numerator
        result_den = fractions[0][1]  # Start with first denominator

        for i in range(1, len(fractions)):
            result_num -= fractions[i][0]
            result_den -= fractions[i][1]

        # Handle edge case where denominator becomes 0
        if result_den == 0:
            return f"{result_num}/0"

        # Handle negative denominator - move sign to numerator
        if result_den < 0:
            result_num = -result_num
            result_den = -result_den

        # Simplify the (incorrect) result
        simplified_num, simplified_den = self._simplify_fraction(result_num, result_den)

        return f"{simplified_num}/{simplified_den}"

    def _generate_concise_steps(self, problem: Problem, answer: str) -> list:
        """Generate concise steps with only formula and values."""
        fractions = problem.operands
        steps = []

        steps.append(f"Question: {problem.text}")

        result_num = fractions[0][0]
        result_den = fractions[0][1]

        for i in range(1, len(fractions)):
            result_num -= fractions[i][0]
            result_den -= fractions[i][1]

        if len(fractions) == 2:
            num1, den1 = fractions[0]
            num2, den2 = fractions[1]
            steps.append(f"{num1} - {num2} = {fractions[0][0] - fractions[1][0]}")
            steps.append(f"{den1} - {den2} = {fractions[0][1] - fractions[1][1]}")
        else:
            nums = [n for n, d in fractions]
            dens = [d for n, d in fractions]
            nums_str = " - ".join(map(str, nums))
            dens_str = " - ".join(map(str, dens))
            steps.append(f"{nums_str} = {result_num}")
            steps.append(f"{dens_str} = {result_den}")

        if result_den == 0:
            steps.append(f"= {result_num}/0")
        elif result_den < 0:
            result_num = -result_num
            result_den = -result_den
            steps.append(f"= {result_num}/{result_den}")
            simplified_num, simplified_den = self._simplify_fraction(result_num, result_den)
            if (simplified_num, simplified_den) != (result_num, result_den):
                steps.append(f"= {simplified_num}/{simplified_den}")
        else:
            steps.append(f"= {result_num}/{result_den}")
            simplified_num, simplified_den = self._simplify_fraction(result_num, result_den)
            if (simplified_num, simplified_den) != (result_num, result_den):
                steps.append(f"= {simplified_num}/{simplified_den}")

        steps.append(f"Answer: {answer}")
        return steps

    def _generate_verbose_steps(self, problem: Problem, answer: str) -> list:
        """Generate verbose steps with full explanations."""
        fractions = problem.operands
        steps = []

        if len(fractions) == 2:
            (num1, den1), (num2, den2) = fractions
            steps.append(f"Subtracting {num1}/{den1} - {num2}/{den2}")
        else:
            frac_str = " - ".join([f"{n}/{d}" for n, d in fractions])
            steps.append(f"Subtracting {frac_str}")

        result_num = fractions[0][0]
        result_den = fractions[0][1]

        for i in range(1, len(fractions)):
            result_num -= fractions[i][0]
            result_den -= fractions[i][1]

        if len(fractions) == 2:
            num1, den1 = fractions[0]
            num2, den2 = fractions[1]
            steps.append(f"Subtract the numerators: {num1} - {num2} = {fractions[0][0] - fractions[1][0]}")
            steps.append(f"Subtract the denominators: {den1} - {den2} = {fractions[0][1] - fractions[1][1]}")
        else:
            nums = [n for n, d in fractions]
            dens = [d for n, d in fractions]
            nums_str = " - ".join(map(str, nums))
            dens_str = " - ".join(map(str, dens))
            steps.append(f"Subtract the numerators: {nums_str} = {result_num}")
            steps.append(f"Subtract the denominators: {dens_str} = {result_den}")

        if result_den == 0:
            steps.append(f"Result: {result_num}/{result_den} = {result_num}/0 (UNDEFINED!)")
        elif result_den < 0:
            orig_num = result_num
            result_num = -result_num
            result_den = -result_den
            steps.append(f"Move negative sign to numerator: {result_num}/{result_den}")
            simplified_num, simplified_den = self._simplify_fraction(result_num, result_den)
            if (simplified_num, simplified_den) != (result_num, result_den):
                steps.append(f"Simplify: {result_num}/{result_den} = {simplified_num}/{simplified_den}")
            steps.append(f"Final answer: {answer} (INCORRECT due to malrule)")
        else:
            simplified_num, simplified_den = self._simplify_fraction(result_num, result_den)
            if (simplified_num, simplified_den) != (result_num, result_den):
                steps.append(f"Simplify: {result_num}/{result_den} = {simplified_num}/{simplified_den}")
            steps.append(f"Final answer: {answer} (INCORRECT due to malrule)")

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Subtract-Across malrule.

        Args:
            problem: Fraction subtraction problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with incorrect subtraction
        """
        answer = self.calculate_expected_answer(problem)

        if verbose:
            steps = self._generate_verbose_steps(problem, answer)
        else:
            steps = self._generate_concise_steps(problem, answer)

        return Solution(
            answer=answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
