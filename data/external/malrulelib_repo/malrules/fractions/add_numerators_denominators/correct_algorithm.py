"""
Correct fraction addition algorithm.

Implements the standard algorithm using common denominators.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import CorrectAlgorithm, Problem, Solution
from math import gcd


def lcm(a: int, b: int) -> int:
    """Calculate least common multiple."""
    return abs(a * b) // gcd(a, b)


class FractionAdditionCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for fraction addition.

    Uses common denominators to add fractions correctly.
    """

    def get_name(self) -> str:
        return "Correct Fraction Addition Algorithm"

    def get_description(self) -> str:
        return (
            "The standard algorithm for adding fractions. First, find a common "
            "denominator (usually the least common multiple of the two denominators). "
            "Convert both fractions to equivalent fractions with this common "
            "denominator. Add the numerators while keeping the denominator the same. "
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

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct fraction addition algorithm.

        Args:
            problem: Fraction addition problem to solve
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with correct answer
        """
        # Always calculate the answer from the operands
        return self._generate_solution_with_steps(problem, verbose)

    def _generate_concise_steps(self, problem: Problem, fractions: list, common_den: int,
                                 converted_nums: list, result_num: int,
                                 simplified_num: int, simplified_den: int) -> list:
        """
        Generate concise steps for the solution.

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

        # LCD step
        denominators = [d for _, d in fractions]
        if len(fractions) == 2:
            steps.append(f"LCM({denominators[0]}, {denominators[1]}) = {common_den}")
        else:
            den_str = ", ".join(map(str, denominators))
            steps.append(f"LCM({den_str}) = {common_den}")

        # Convert fractions step
        converted_fracs = " + ".join([f"{num}/{common_den}" for num in converted_nums])
        steps.append(converted_fracs)

        # Add numerators step
        nums_str = " + ".join(map(str, converted_nums))
        steps.append(f"{nums_str} = {result_num}")

        # Result step
        steps.append(f"{result_num}/{common_den}")

        # Simplify step if needed
        if (simplified_num, simplified_den) != (result_num, common_den):
            steps.append(f"{simplified_num}/{simplified_den}")

        # Final answer
        steps.append(f"{simplified_num}/{simplified_den}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, fractions: list, common_den: int,
                                 converted_nums: list, result_num: int,
                                 simplified_num: int, simplified_den: int) -> list:
        """
        Generate verbose steps for the solution (original step format).
        """
        steps = []

        # Handle 2 or more fractions
        if len(fractions) == 2:
            (num1, den1), (num2, den2) = fractions
            steps.append(f"Adding {num1}/{den1} + {num2}/{den2}")
        else:
            frac_str = " + ".join([f"{n}/{d}" for n, d in fractions])
            steps.append(f"Adding {frac_str}")

        # Find common denominator (LCD) for all fractions
        denominators = [d for _, d in fractions]

        if len(fractions) == 2:
            den1, den2 = denominators
            steps.append(f"Find common denominator: LCM({den1}, {den2}) = {common_den}")
        else:
            den_str = ", ".join(map(str, denominators))
            steps.append(f"Find common denominator: LCM({den_str}) = {common_den}")

        # Convert all fractions to common denominator
        for i, (num, den) in enumerate(fractions, 1):
            mult = common_den // den
            new_num = converted_nums[i - 1]

            if mult != 1:
                steps.append(
                    f"Convert {num}/{den} to equivalent fraction: "
                    f"{num}/{den} × {mult}/{mult} = {new_num}/{common_den}"
                )
            else:
                steps.append(f"Fraction {i}: {num}/{den} = {new_num}/{common_den}")

        # Add all numerators
        if len(converted_nums) == 2:
            steps.append(
                f"Add numerators: {converted_nums[0]} + {converted_nums[1]} = {result_num}"
            )
        else:
            nums_str = " + ".join(map(str, converted_nums))
            steps.append(
                f"Add numerators: {nums_str} = {result_num}"
            )

        steps.append(
            f"Keep the common denominator: {result_num}/{common_den}"
        )

        # Simplify if possible
        if (simplified_num, simplified_den) != (result_num, common_den):
            steps.append(
                f"Simplify: {result_num}/{common_den} = {simplified_num}/{simplified_den}"
            )

        # Always use calculated answer
        final_answer = f"{simplified_num}/{simplified_den}"

        steps.append(f"Final answer: {final_answer}")

        return steps

    def _generate_solution_with_steps(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Generate solution with full steps.

        Args:
            problem: Fraction addition problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with steps
        """
        fractions = problem.operands

        # Find common denominator (LCD) for all fractions
        denominators = [d for _, d in fractions]
        common_den = self._lcm_multiple(denominators)

        # Convert all fractions to common denominator
        converted_nums = []
        for num, den in fractions:
            mult = common_den // den
            new_num = num * mult
            converted_nums.append(new_num)

        # Add all numerators
        result_num = sum(converted_nums)

        # Simplify if possible
        simplified_num, simplified_den = self._simplify_fraction(result_num, common_den)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(
                problem, fractions, common_den, converted_nums,
                result_num, simplified_num, simplified_den
            )
        else:
            steps = self._generate_concise_steps(
                problem, fractions, common_den, converted_nums,
                result_num, simplified_num, simplified_den
            )

        # Always use calculated answer
        final_answer = f"{simplified_num}/{simplified_den}"

        return Solution(
            answer=final_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
