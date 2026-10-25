"""
Correct fraction comparison algorithm.

Implements proper fraction comparison by finding common denominators
using LCM (Least Common Multiple).
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import CorrectAlgorithm, Problem, Solution
from math import gcd


def lcm(a: int, b: int) -> int:
    """Calculate least common multiple of two numbers."""
    return abs(a * b) // gcd(a, b)


def lcm_multiple(numbers: list) -> int:
    """Calculate LCM of multiple numbers."""
    result = numbers[0]
    for i in range(1, len(numbers)):
        result = lcm(result, numbers[i])
    return result


class FractionComparisonCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for comparing fractions.

    Uses common denominators (via LCM) to compare fractions properly.
    """

    def get_name(self) -> str:
        return "Correct Fraction Comparison"

    def get_description(self) -> str:
        return (
            "Compares fractions correctly by finding the LCM of the denominators "
            "and converting fractions to equivalent fractions with a common denominator. "
            "Both numerator and denominator are considered in the comparison."
        )

    def _generate_concise_steps(self, problem: Problem, correct_answer: str) -> list:
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

            # Find LCM of all three denominators
            common_den = lcm_multiple([den1, den2, den3])
            steps.append(f"LCM({den1}, {den2}, {den3}) = {common_den}")

            # Convert each fraction to equivalent fraction with common denominator
            equiv1_num = num1 * (common_den // den1)
            equiv2_num = num2 * (common_den // den2)
            equiv3_num = num3 * (common_den // den3)

            steps.append(f"{num1}/{den1} = {equiv1_num}/{common_den}")
            steps.append(f"{num2}/{den2} = {equiv2_num}/{common_den}")
            steps.append(f"{num3}/{den3} = {equiv3_num}/{common_den}")

            # Compare numerators
            steps.append(f"Compare numerators: {equiv1_num}, {equiv2_num}, {equiv3_num}")
        else:
            num1 = problem.metadata['num1']
            den1 = problem.metadata['den1']
            num2 = problem.metadata['num2']
            den2 = problem.metadata['den2']

            # Find LCM of the two denominators
            common_den = lcm(den1, den2)
            steps.append(f"LCM({den1}, {den2}) = {common_den}")

            # Convert to equivalent fractions
            equiv1_num = num1 * (common_den // den1)
            equiv2_num = num2 * (common_den // den2)

            steps.append(f"{num1}/{den1} = {equiv1_num}/{common_den}")
            steps.append(f"{num2}/{den2} = {equiv2_num}/{common_den}")

            # Compare numerators
            if equiv1_num > equiv2_num:
                steps.append(f"{equiv1_num} > {equiv2_num}")
            elif equiv1_num < equiv2_num:
                steps.append(f"{equiv1_num} < {equiv2_num}")
            else:
                steps.append(f"{equiv1_num} = {equiv2_num}")

        steps.append(f"Answer: {correct_answer}")
        return steps

    def _generate_verbose_steps(self, problem: Problem, correct_answer: str) -> list:
        """Generate verbose steps with full explanations."""
        template = problem.metadata.get('template', 'basic_comparison')

        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD: Find common denominator using LCM")
        steps.append("  Key: Must consider BOTH numerator and denominator!")
        steps.append("")

        if template in ['multiple_choice', 'ordering', 'word_problem_multiple_choice', 'word_problem_ordering']:
            num1 = problem.metadata['num1']
            den1 = problem.metadata['den1']
            num2 = problem.metadata['num2']
            den2 = problem.metadata['den2']
            num3 = problem.metadata['num3']
            den3 = problem.metadata['den3']

            steps.append(f"Comparing: {num1}/{den1}, {num2}/{den2}, {num3}/{den3}")
            steps.append("")

            # Find LCM of all three denominators
            common_den = lcm_multiple([den1, den2, den3])
            steps.append(f"Step 1: Find the LCM of the denominators")
            steps.append(f"  LCM({den1}, {den2}, {den3}) = {common_den}")
            steps.append("")

            # Convert each fraction
            equiv1_num = num1 * (common_den // den1)
            equiv2_num = num2 * (common_den // den2)
            equiv3_num = num3 * (common_den // den3)

            mult1 = common_den // den1
            mult2 = common_den // den2
            mult3 = common_den // den3

            steps.append("Step 2: Convert each fraction to equivalent fraction with common denominator")
            steps.append(f"  {num1}/{den1} × {mult1}/{mult1} = {equiv1_num}/{common_den}")
            steps.append(f"  {num2}/{den2} × {mult2}/{mult2} = {equiv2_num}/{common_den}")
            steps.append(f"  {num3}/{den3} × {mult3}/{mult3} = {equiv3_num}/{common_den}")
            steps.append("")

            steps.append("Step 3: Compare the numerators")
            steps.append(f"  Numerators: {equiv1_num}, {equiv2_num}, {equiv3_num}")

            # Sort fractions by equivalent numerators
            fractions_with_values = [
                (num1, den1, equiv1_num, f"{num1}/{den1}"),
                (num2, den2, equiv2_num, f"{num2}/{den2}"),
                (num3, den3, equiv3_num, f"{num3}/{den3}"),
            ]
            sorted_fracs = sorted(fractions_with_values, key=lambda x: x[2])

            if template in ['multiple_choice', 'word_problem_multiple_choice']:
                largest = max(fractions_with_values, key=lambda x: x[2])
                steps.append(f"  Largest numerator: {largest[2]}")
                steps.append("")
                steps.append(f"The largest fraction is: {correct_answer}")
            else:
                sorted_order = ", ".join([f[3] for f in sorted_fracs])
                steps.append(f"  Order from smallest to largest: {sorted_fracs[0][2]} < {sorted_fracs[1][2]} < {sorted_fracs[2][2]}")
                steps.append("")
                steps.append(f"Correct order from smallest to largest:")
                steps.append(f"  {sorted_order}")
        else:
            num1 = problem.metadata['num1']
            den1 = problem.metadata['den1']
            num2 = problem.metadata['num2']
            den2 = problem.metadata['den2']

            steps.append(f"Comparing: {num1}/{den1} vs {num2}/{den2}")
            steps.append("")

            # Find LCM
            common_den = lcm(den1, den2)
            steps.append(f"Step 1: Find the LCM of the denominators")
            steps.append(f"  LCM({den1}, {den2}) = {common_den}")
            steps.append("")

            # Convert fractions
            mult1 = common_den // den1
            mult2 = common_den // den2
            equiv1_num = num1 * mult1
            equiv2_num = num2 * mult2

            steps.append("Step 2: Convert to equivalent fractions with common denominator")
            steps.append(f"  {num1}/{den1} × {mult1}/{mult1} = {equiv1_num}/{common_den}")
            steps.append(f"  {num2}/{den2} × {mult2}/{mult2} = {equiv2_num}/{common_den}")
            steps.append("")

            steps.append("Step 3: Compare the numerators")
            if equiv1_num > equiv2_num:
                steps.append(f"  Since {equiv1_num} > {equiv2_num}, we have {num1}/{den1} > {num2}/{den2}")
            elif equiv1_num < equiv2_num:
                steps.append(f"  Since {equiv1_num} < {equiv2_num}, we have {num1}/{den1} < {num2}/{den2}")
            else:
                steps.append(f"  Since {equiv1_num} = {equiv2_num}, the fractions are equal")

        steps.append("")
        steps.append(f"Final Answer: {correct_answer}")
        steps.append("")
        steps.append("Key concept: Both numerator AND denominator determine fraction size")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct fraction comparison.

        Args:
            problem: Fraction comparison problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with correct comparison
        """
        # Calculate correct answer
        num1 = problem.metadata['num1']
        den1 = problem.metadata['den1']
        num2 = problem.metadata['num2']
        den2 = problem.metadata['den2']

        # Use correct_answer from metadata if available
        if 'correct_answer' in problem.metadata:
            correct_answer = problem.metadata['correct_answer']
        else:
            cross1 = num1 * den2
            cross2 = num2 * den1
            if cross1 > cross2:
                correct_answer = f"{num1}/{den1}"
            elif cross1 < cross2:
                correct_answer = f"{num2}/{den2}"
            else:
                correct_answer = "equal"

        if verbose:
            steps = self._generate_verbose_steps(problem, correct_answer)
        else:
            steps = self._generate_concise_steps(problem, correct_answer)

        return Solution(
            answer=str(correct_answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
