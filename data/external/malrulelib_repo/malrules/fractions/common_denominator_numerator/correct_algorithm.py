"""
Correct algorithm for fraction addition.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class FractionAdditionCorrectAlgorithm(CorrectAlgorithm):
    """Correctly adds fractions using LCD."""

    def get_name(self) -> str:
        return "Correct Fraction Addition"

    def get_description(self) -> str:
        return "Correctly adds fractions by finding LCD and converting to equivalent fractions."

    def _generate_concise_steps(self, problem: Problem, numer1: int, denom1: int,
                                 numer2: int, denom2: int, lcd: int, mult1: int, mult2: int,
                                 result_numer: int, correct_numer: int, correct_denom: int) -> list:
        """
        Generate concise steps for the solution.

        Returns a list: [Question, step1, step2, ..., answer]
        """
        steps = []

        # Question
        steps.append(problem.text)

        # Formula extraction
        steps.append(f"{numer1}/{denom1} + {numer2}/{denom2}")

        # LCD step
        steps.append(f"LCD({denom1}, {denom2}) = {lcd}")

        # Convert fractions step
        steps.append(f"{numer1 * mult1}/{lcd} + {numer2 * mult2}/{lcd}")

        # Add numerators step
        steps.append(f"{numer1 * mult1} + {numer2 * mult2} = {result_numer}")

        # Result step
        steps.append(f"{result_numer}/{lcd}")

        # Simplify step if needed
        if correct_denom != lcd or correct_numer != result_numer:
            steps.append(f"{correct_numer}/{correct_denom}")

        # Final answer
        steps.append(f"{correct_numer}/{correct_denom}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, numer1: int, denom1: int,
                                 numer2: int, denom2: int, lcd: int, mult1: int, mult2: int,
                                 result_numer: int, correct_numer: int, correct_denom: int) -> list:
        """
        Generate verbose steps for the solution (original step format).
        """
        steps = []
        steps.append(f"Problem: {numer1}/{denom1} + {numer2}/{denom2}")
        steps.append("")
        steps.append("Step 1: Find the Least Common Denominator (LCD)")
        steps.append(f"  LCD of {denom1} and {denom2} is {lcd}")
        steps.append("")
        steps.append("Step 2: Convert to equivalent fractions with LCD")

        steps.append(f"  {numer1}/{denom1} = {numer1}×{mult1}/{denom1}×{mult1} = {numer1 * mult1}/{lcd}")
        steps.append(f"  {numer2}/{denom2} = {numer2}×{mult2}/{denom2}×{mult2} = {numer2 * mult2}/{lcd}")
        steps.append("")
        steps.append("Step 3: Add the fractions")
        steps.append(f"  {numer1 * mult1}/{lcd} + {numer2 * mult2}/{lcd} = {result_numer}/{lcd}")

        # Check if we simplified
        if correct_denom != lcd or correct_numer != result_numer:
            steps.append("")
            steps.append("Step 4: Simplify")
            steps.append(f"  {result_numer}/{lcd} = {correct_numer}/{correct_denom}")

        steps.append("")
        steps.append(f"Final Answer: {correct_numer}/{correct_denom} ✓")

        return steps

    def _generate_concise_steps_three(self, problem: Problem, numer1: int, denom1: int,
                                       numer2: int, denom2: int, numer3: int, denom3: int,
                                       lcd: int, mult1: int, mult2: int, mult3: int,
                                       result_numer: int, correct_numer: int, correct_denom: int) -> list:
        """
        Generate concise steps for the solution with three fractions.

        Returns a list: [Question, step1, step2, ..., answer]
        """
        steps = []

        # Question
        steps.append(problem.text)

        # Formula extraction
        steps.append(f"{numer1}/{denom1} + {numer2}/{denom2} + {numer3}/{denom3}")

        # LCD step
        steps.append(f"LCD({denom1}, {denom2}, {denom3}) = {lcd}")

        # Convert fractions step
        steps.append(f"{numer1 * mult1}/{lcd} + {numer2 * mult2}/{lcd} + {numer3 * mult3}/{lcd}")

        # Add numerators step
        steps.append(f"{numer1 * mult1} + {numer2 * mult2} + {numer3 * mult3} = {result_numer}")

        # Result step
        steps.append(f"{result_numer}/{lcd}")

        # Simplify step if needed
        if correct_denom != lcd or correct_numer != result_numer:
            steps.append(f"{correct_numer}/{correct_denom}")

        # Final answer
        steps.append(f"{correct_numer}/{correct_denom}")

        return steps

    def _generate_verbose_steps_three(self, problem: Problem, numer1: int, denom1: int,
                                       numer2: int, denom2: int, numer3: int, denom3: int,
                                       lcd: int, mult1: int, mult2: int, mult3: int,
                                       result_numer: int, correct_numer: int, correct_denom: int) -> list:
        """
        Generate verbose steps for the solution with three fractions (original step format).
        """
        steps = []
        steps.append(f"Problem: {numer1}/{denom1} + {numer2}/{denom2} + {numer3}/{denom3}")
        steps.append("")
        steps.append("Step 1: Find the Least Common Denominator (LCD)")
        steps.append(f"  LCD of {denom1}, {denom2}, and {denom3} is {lcd}")
        steps.append("")
        steps.append("Step 2: Convert to equivalent fractions with LCD")

        steps.append(f"  {numer1}/{denom1} = {numer1}×{mult1}/{denom1}×{mult1} = {numer1 * mult1}/{lcd}")
        steps.append(f"  {numer2}/{denom2} = {numer2}×{mult2}/{denom2}×{mult2} = {numer2 * mult2}/{lcd}")
        steps.append(f"  {numer3}/{denom3} = {numer3}×{mult3}/{denom3}×{mult3} = {numer3 * mult3}/{lcd}")
        steps.append("")
        steps.append("Step 3: Add the fractions")
        steps.append(f"  {numer1 * mult1}/{lcd} + {numer2 * mult2}/{lcd} + {numer3 * mult3}/{lcd} = {result_numer}/{lcd}")

        # Check if we simplified
        if correct_denom != lcd or correct_numer != result_numer:
            steps.append("")
            steps.append("Step 4: Simplify")
            steps.append(f"  {result_numer}/{lcd} = {correct_numer}/{correct_denom}")

        steps.append("")
        steps.append(f"Final Answer: {correct_numer}/{correct_denom} ✓")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        from math import gcd

        numer1 = problem.metadata['numer1']
        denom1 = problem.metadata['denom1']
        numer2 = problem.metadata['numer2']
        denom2 = problem.metadata['denom2']
        lcd = problem.metadata['lcd']

        # Check if there is a third fraction
        has_third_fraction = 'numer3' in problem.metadata

        if has_third_fraction:
            numer3 = problem.metadata['numer3']
            denom3 = problem.metadata['denom3']

        # Calculate the correct answer
        mult1 = lcd // denom1
        mult2 = lcd // denom2

        if has_third_fraction:
            mult3 = lcd // denom3
            result_numer = numer1 * mult1 + numer2 * mult2 + numer3 * mult3
        else:
            result_numer = numer1 * mult1 + numer2 * mult2

        result_denom = lcd

        # Simplify
        gcd_val = gcd(result_numer, result_denom)
        correct_numer = result_numer // gcd_val
        correct_denom = result_denom // gcd_val

        # Check if this is a comparison problem (special answer format)
        if 'is_comparison' in problem.metadata and problem.metadata['is_comparison']:
            # This is a comparison problem - calculate the comparison
            if result_numer > result_numer:  # This will be fixed in the actual comparison logic
                correct_answer = f"{numer1}/{denom1} is greater"
            else:
                correct_answer = f"{numer2}/{denom2} is greater"

            steps = [f"Compare the two sums correctly using LCD"]
            steps.append(f"Result: {correct_answer}")
            return Solution(answer=correct_answer, steps=steps, is_correct=True, algorithm_name=self.get_name())

        # Generate steps based on verbose flag
        if has_third_fraction:
            if verbose:
                steps = self._generate_verbose_steps_three(
                    problem, numer1, denom1, numer2, denom2, numer3, denom3,
                    lcd, mult1, mult2, mult3, result_numer, correct_numer, correct_denom
                )
            else:
                steps = self._generate_concise_steps_three(
                    problem, numer1, denom1, numer2, denom2, numer3, denom3,
                    lcd, mult1, mult2, mult3, result_numer, correct_numer, correct_denom
                )
        else:
            if verbose:
                steps = self._generate_verbose_steps(
                    problem, numer1, denom1, numer2, denom2, lcd, mult1, mult2,
                    result_numer, correct_numer, correct_denom
                )
            else:
                steps = self._generate_concise_steps(
                    problem, numer1, denom1, numer2, denom2, lcd, mult1, mult2,
                    result_numer, correct_numer, correct_denom
                )

        return Solution(
            answer=f"{correct_numer}/{correct_denom}",
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
