"""
Correct fraction subtraction algorithm.

Implements the standard algorithm using common denominators.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import CorrectAlgorithm, Problem, Solution
from math import gcd


def lcm(a: int, b: int) -> int:
    """Calculate least common multiple."""
    return abs(a * b) // gcd(a, b)


class FractionSubtractionCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for fraction subtraction.

    Uses common denominators to subtract fractions correctly.
    """

    def get_name(self) -> str:
        return "Correct Fraction Subtraction Algorithm"

    def get_description(self) -> str:
        return (
            "The standard algorithm for subtracting fractions. First, find a common "
            "denominator (usually the least common multiple of the two denominators). "
            "Convert both fractions to equivalent fractions with this common "
            "denominator. Subtract the numerators while keeping the denominator the same. "
            "Simplify the result if possible."
        )

    def _simplify_fraction(self, numerator: int, denominator: int):
        """Simplify a fraction."""
        if numerator == 0:
            return 0, denominator
        common = gcd(abs(numerator), abs(denominator))
        return numerator // common, denominator // common

    def _lcm_multiple(self, numbers):
        """Calculate LCM of multiple numbers."""
        result = numbers[0]
        for i in range(1, len(numbers)):
            result = lcm(result, numbers[i])
        return result

    def _generate_concise_steps(self, problem: Problem, answer: str) -> list:
        """Generate concise steps with only formula and values."""
        fractions = problem.operands
        steps = []

        if len(fractions) == 2:
            (num1, den1), (num2, den2) = fractions
            steps.append(f"Question: {problem.text}")
        else:
            steps.append(f"Question: {problem.text}")

        denominators = [d for _, d in fractions]
        common_den = self._lcm_multiple(denominators)

        if len(fractions) == 2:
            steps.append(f"LCM({denominators[0]}, {denominators[1]}) = {common_den}")
        else:
            den_str = ", ".join(map(str, denominators))
            steps.append(f"LCM({den_str}) = {common_den}")

        converted_nums = []
        for num, den in fractions:
            mult = common_den // den
            new_num = num * mult
            converted_nums.append(new_num)
            steps.append(f"{num}/{den} = {new_num}/{common_den}")

        result_num = converted_nums[0]
        for i in range(1, len(converted_nums)):
            result_num -= converted_nums[i]

        if len(converted_nums) == 2:
            steps.append(f"{converted_nums[0]} - {converted_nums[1]} = {result_num}")
        else:
            nums_str = " - ".join(map(str, converted_nums))
            steps.append(f"{nums_str} = {result_num}")

        steps.append(f"= {result_num}/{common_den}")

        simplified_num, simplified_den = self._simplify_fraction(result_num, common_den)
        if (simplified_num, simplified_den) != (result_num, common_den):
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

        denominators = [d for _, d in fractions]
        common_den = self._lcm_multiple(denominators)

        if len(fractions) == 2:
            den1, den2 = denominators
            steps.append(f"Find common denominator: LCM({den1}, {den2}) = {common_den}")
        else:
            den_str = ", ".join(map(str, denominators))
            steps.append(f"Find common denominator: LCM({den_str}) = {common_den}")

        converted_nums = []
        for i, (num, den) in enumerate(fractions, 1):
            mult = common_den // den
            new_num = num * mult
            converted_nums.append(new_num)

            if mult != 1:
                steps.append(
                    f"Convert {num}/{den} to equivalent fraction: "
                    f"{num}/{den} × {mult}/{mult} = {new_num}/{common_den}"
                )
            else:
                steps.append(f"Fraction {i}: {num}/{den} = {new_num}/{common_den}")

        result_num = converted_nums[0]
        for i in range(1, len(converted_nums)):
            result_num -= converted_nums[i]

        if len(converted_nums) == 2:
            steps.append(f"Subtract numerators: {converted_nums[0]} - {converted_nums[1]} = {result_num}")
        else:
            nums_str = " - ".join(map(str, converted_nums))
            steps.append(f"Subtract numerators: {nums_str} = {result_num}")

        steps.append(f"Keep the common denominator: {result_num}/{common_den}")

        simplified_num, simplified_den = self._simplify_fraction(result_num, common_den)
        if (simplified_num, simplified_den) != (result_num, common_den):
            steps.append(f"Simplify: {result_num}/{common_den} = {simplified_num}/{simplified_den}")

        steps.append(f"Final answer: {answer}")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct fraction subtraction algorithm.

        Args:
            problem: Fraction subtraction problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with correct answer
        """
        # Calculate correct answer for any number of fractions
        from fractions import Fraction

        # Start with the first fraction
        result = Fraction(problem.operands[0][0], problem.operands[0][1])

        # Subtract all remaining fractions
        for i in range(1, len(problem.operands)):
            numerator, denominator = problem.operands[i]
            result -= Fraction(numerator, denominator)

        correct_answer = f"{result.numerator}/{result.denominator}"

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
