"""
Add-Numerators-Add-Denominators malrule algorithm.

Implements the systematic error where students add both numerators
and denominators: a/b + c/d = (a+c)/(b+d)
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List
from math import gcd

class AddNumeratorsAddDenominatorsMalrule(Malrule):
    """
    Implements the Add-Numerators-Add-Denominators bug.

    Students incorrectly add fractions by adding numerators and denominators
    separately, treating the operation as if it works component-wise like
    adding whole numbers.
    """

    def get_name(self) -> str:
        return "Add-Numerators-Add-Denominators"

    def get_description(self) -> str:
        return (
            "When adding fractions with different denominators, students incorrectly "
            "add numerators together and denominators together, treating the operation "
            "as component-wise addition. For example: 1/2 + 1/3 = 2/5 (incorrect). "
            "This error reflects a fundamental misunderstanding where students treat "
            "fractions as two independent whole numbers rather than a single quantity "
            "representing a ratio. Research shows this stems from 'whole number bias' - "
            "the overgeneralization of whole-number arithmetic properties to fractions "
            "(Ni & Zhou, 2005; Behr et al., 1984)."
        )

    def _simplify_fraction(self, numerator: int, denominator: int):
        """Simplify a fraction."""
        if numerator == 0:
            return 0, denominator
        common = gcd(abs(numerator), abs(denominator))
        return numerator // common, denominator // common

    def calculate_expected_answer(self, problem: Problem) -> str:
        """
        Calculate the expected incorrect answer for this malrule.

        For Add-Numerators-Add-Denominators:
        - Sum all numerators
        - Sum all denominators
        - Simplify the result

        Args:
            problem: Fraction addition problem

        Returns:
            Expected incorrect answer in the form "num/den"
        """
        # Always calculate it from the operands
        fractions = problem.operands

        # MALRULE: Add all numerators, add all denominators
        result_num = sum(n for n, d in fractions)
        result_den = sum(d for n, d in fractions)

        # Simplify the (incorrect) result
        simplified_num, simplified_den = self._simplify_fraction(result_num, result_den)

        return f"{simplified_num}/{simplified_den}"

    def _generate_concise_steps(self, problem: Problem, fractions: list,
                                 result_num: int, result_den: int,
                                 simplified_num: int, simplified_den: int) -> list:
        """
        Generate concise steps for the malrule solution.

        Returns a list: [Question, step1, step2, ..., answer]
        """
        steps = []

        # Question
        steps.append(problem.text)

        # Formula extraction for word problems
        if len(fractions) == 2:
            (num1, den1), (num2, den2) = fractions
            steps.append(f"{num1}/{den1} + {num2}/{den2}")
        else:
            frac_str = " + ".join([f"{n}/{d}" for n, d in fractions])
            steps.append(frac_str)

        # Add numerators step
        nums = [n for n, d in fractions]
        nums_str = " + ".join(map(str, nums))
        steps.append(f"{nums_str} = {result_num}")

        # Add denominators step
        dens = [d for n, d in fractions]
        dens_str = " + ".join(map(str, dens))
        steps.append(f"{dens_str} = {result_den}")

        # Result step
        steps.append(f"{result_num}/{result_den}")

        # Simplify step if needed
        if (simplified_num, simplified_den) != (result_num, result_den):
            steps.append(f"{simplified_num}/{simplified_den}")

        # Final answer
        steps.append(f"{simplified_num}/{simplified_den}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, fractions: list,
                                 result_num: int, result_den: int,
                                 simplified_num: int, simplified_den: int) -> list:
        """
        Generate verbose steps for the malrule solution (original step format).
        """
        steps = []

        # Handle 2 or more fractions
        if len(fractions) == 2:
            (num1, den1), (num2, den2) = fractions
            steps.append(f"Adding {num1}/{den1} + {num2}/{den2}")
        else:
            frac_str = " + ".join([f"{n}/{d}" for n, d in fractions])
            steps.append(f"Adding {frac_str}")

        if len(fractions) == 2:
            num1, den1 = fractions[0]
            num2, den2 = fractions[1]
            steps.append(
                f"Add the numerators: {num1} + {num2} = {result_num}"
            )
            steps.append(
                f"Add the denominators: {den1} + {den2} = {result_den}"
            )
        else:
            nums = [n for n, d in fractions]
            dens = [d for n, d in fractions]
            nums_str = " + ".join(map(str, nums))
            dens_str = " + ".join(map(str, dens))
            steps.append(
                f"Add the numerators: {nums_str} = {result_num}"
            )
            steps.append(
                f"Add the denominators: {dens_str} = {result_den}"
            )

        steps.append(
            f"Result: {result_num}/{result_den}"
        )

        # Simplify the (incorrect) result
        if (simplified_num, simplified_den) != (result_num, result_den):
            steps.append(
                f"Simplify: {result_num}/{result_den} = {simplified_num}/{simplified_den}"
            )

        answer = f"{simplified_num}/{simplified_den}"
        steps.append(f"Final answer: {answer} (INCORRECT due to malrule)")

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Add-Numerators-Add-Denominators malrule.

        Args:
            problem: Fraction addition problem to solve
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with incorrect answer
        """
        fractions = problem.operands

        # MALRULE: Add all numerators, add all denominators
        result_num = sum(n for n, d in fractions)
        result_den = sum(d for n, d in fractions)

        # Simplify the (incorrect) result
        simplified_num, simplified_den = self._simplify_fraction(result_num, result_den)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(
                problem, fractions, result_num, result_den,
                simplified_num, simplified_den
            )
        else:
            steps = self._generate_concise_steps(
                problem, fractions, result_num, result_den,
                simplified_num, simplified_den
            )

        answer = f"{simplified_num}/{simplified_den}"

        return Solution(
            answer=answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
