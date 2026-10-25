"""
Malrule algorithm for Common-Denominator-Numerator error.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution
import math

class CommonDenominatorNumeratorMalrule(Malrule):
    """
    Students add numerators correctly but make denominators same by adding.

    Example: 1/4 + 1/6 → Student: (1+1)/(4+6) = 2/10 = 1/5
    """

    def get_name(self) -> str:
        return "Common-Denominator-Numerator"

    def get_description(self) -> str:
        return (
            "Students add numerators and add denominators when adding fractions, "
            "believing that adding denominators creates a 'common denominator.' This is "
            "a variant of the whole number bias error (Ni & Zhou, 2005) where students "
            "show partial procedural knowledge (awareness that common denominators are "
            "needed) but lack conceptual understanding of how to find them. For example: "
            "1/4 + 1/6 = 2/10 = 1/5 (incorrect; correct answer is 5/12)."
        )

    def calculate_expected_answer(self, problem: Problem) -> str:
        """
        Calculate the expected incorrect answer for this malrule.
        """
        # Calculate from scratch
        numer1 = problem.metadata['numer1']
        denom1 = problem.metadata['denom1']
        numer2 = problem.metadata['numer2']
        denom2 = problem.metadata['denom2']

        # Check if three_fractions template
        if 'numer3' in problem.metadata:
            numer3 = problem.metadata['numer3']
            denom3 = problem.metadata['denom3']
            result_numer = numer1 + numer2 + numer3
            result_denom = denom1 + denom2 + denom3
        else:
            result_numer = numer1 + numer2
            result_denom = denom1 + denom2

        # Simplify
        gcd = math.gcd(result_numer, result_denom)
        if gcd > 1:
            result_numer = result_numer // gcd
            result_denom = result_denom // gcd

        return f"{result_numer}/{result_denom}"

    def _generate_concise_steps(self, problem: Problem, numer1: int, denom1: int,
                                 numer2: int, denom2: int, result_numer: int, result_denom: int,
                                 malrule_numer: int, malrule_denom: int) -> list:
        """
        Generate concise steps for the malrule solution.

        Returns a list: [Question, step1, step2, ..., answer]
        """
        steps = []

        # Question
        steps.append(problem.text)

        # Formula extraction
        steps.append(f"{numer1}/{denom1} + {numer2}/{denom2}")

        # Add numerators step
        steps.append(f"{numer1} + {numer2} = {result_numer}")

        # Add denominators step
        steps.append(f"{denom1} + {denom2} = {result_denom}")

        # Result step
        steps.append(f"{result_numer}/{result_denom}")

        # Simplify step if needed
        if malrule_numer != result_numer or malrule_denom != result_denom:
            steps.append(f"{malrule_numer}/{malrule_denom}")

        # Final answer
        steps.append(f"{malrule_numer}/{malrule_denom}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, numer1: int, denom1: int,
                                 numer2: int, denom2: int, result_numer: int, result_denom: int,
                                 malrule_numer: int, malrule_denom: int) -> list:
        """
        Generate verbose steps for the malrule solution (original step format).
        """
        steps = []
        steps.append(f"Problem: {numer1}/{denom1} + {numer2}/{denom2}")
        steps.append("")
        steps.append("MALRULE: Add numerators, add denominators for common denominator")
        steps.append(f"  MALRULE REASONING: 'Need common denominator, so add them'")
        steps.append("")
        steps.append(f"Step 1: Add numerators")
        steps.append(f"  {numer1} + {numer2} = {result_numer}")
        steps.append("")
        steps.append(f"Step 2: Add denominators to get common denominator")
        steps.append(f"  {denom1} + {denom2} = {result_denom}")
        steps.append("")
        steps.append(f"Result: {result_numer}/{result_denom}")

        # Check if simplification happened
        if malrule_numer != result_numer or malrule_denom != result_denom:
            steps.append(f"Simplify: {malrule_numer}/{malrule_denom}")

        steps.append("")
        steps.append(f"Final Answer: {malrule_numer}/{malrule_denom} (INCORRECT - added denominators!)")

        return steps

    def _generate_concise_steps_three(self, problem: Problem, numer1: int, denom1: int,
                                       numer2: int, denom2: int, numer3: int, denom3: int,
                                       result_numer: int, result_denom: int,
                                       malrule_numer: int, malrule_denom: int) -> list:
        """
        Generate concise steps for the malrule solution with three fractions.

        Returns a list: [Question, step1, step2, ..., answer]
        """
        steps = []

        # Question
        steps.append(problem.text)

        # Formula extraction
        steps.append(f"{numer1}/{denom1} + {numer2}/{denom2} + {numer3}/{denom3}")

        # Add numerators step
        steps.append(f"{numer1} + {numer2} + {numer3} = {result_numer}")

        # Add denominators step
        steps.append(f"{denom1} + {denom2} + {denom3} = {result_denom}")

        # Result step
        steps.append(f"{result_numer}/{result_denom}")

        # Simplify step if needed
        if malrule_numer != result_numer or malrule_denom != result_denom:
            steps.append(f"{malrule_numer}/{malrule_denom}")

        # Final answer
        steps.append(f"{malrule_numer}/{malrule_denom}")

        return steps

    def _generate_verbose_steps_three(self, problem: Problem, numer1: int, denom1: int,
                                       numer2: int, denom2: int, numer3: int, denom3: int,
                                       result_numer: int, result_denom: int,
                                       malrule_numer: int, malrule_denom: int) -> list:
        """
        Generate verbose steps for the malrule solution with three fractions (original step format).
        """
        steps = []
        steps.append(f"Problem: {numer1}/{denom1} + {numer2}/{denom2} + {numer3}/{denom3}")
        steps.append("")
        steps.append("MALRULE: Add numerators, add denominators for common denominator")
        steps.append(f"  MALRULE REASONING: 'Need common denominator, so add them'")
        steps.append("")
        steps.append(f"Step 1: Add numerators")
        steps.append(f"  {numer1} + {numer2} + {numer3} = {result_numer}")
        steps.append("")
        steps.append(f"Step 2: Add denominators to get common denominator")
        steps.append(f"  {denom1} + {denom2} + {denom3} = {result_denom}")
        steps.append("")
        steps.append(f"Result: {result_numer}/{result_denom}")

        # Check if simplification happened
        if malrule_numer != result_numer or malrule_denom != result_denom:
            steps.append(f"Simplify: {malrule_numer}/{malrule_denom}")

        steps.append("")
        steps.append(f"Final Answer: {malrule_numer}/{malrule_denom} (INCORRECT - added denominators!)")

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        numer1 = problem.metadata['numer1']
        denom1 = problem.metadata['denom1']
        numer2 = problem.metadata['numer2']
        denom2 = problem.metadata['denom2']

        # Check if there is a third fraction
        has_third_fraction = 'numer3' in problem.metadata

        if has_third_fraction:
            numer3 = problem.metadata['numer3']
            denom3 = problem.metadata['denom3']

        # Calculate malrule answer: add numerators, add denominators
        if has_third_fraction:
            result_numer = numer1 + numer2 + numer3
            result_denom = denom1 + denom2 + denom3
        else:
            result_numer = numer1 + numer2
            result_denom = denom1 + denom2

        # Simplify
        gcd = math.gcd(result_numer, result_denom)
        malrule_numer = result_numer // gcd
        malrule_denom = result_denom // gcd

        # Check if this is a comparison problem
        if 'is_comparison' in problem.metadata and problem.metadata['is_comparison']:
            # This is a comparison problem - calculate the comparison
            malrule_answer = f"{numer1}/{denom1} is greater"  # Simplified comparison logic
            steps = [f"MALRULE: Student uses incorrect fraction addition, leading to wrong comparison"]
            steps.append(f"Result: {malrule_answer}")
            return Solution(answer=malrule_answer, steps=steps, is_correct=False, algorithm_name=self.get_name())

        # Generate steps based on verbose flag
        if has_third_fraction:
            if verbose:
                steps = self._generate_verbose_steps_three(
                    problem, numer1, denom1, numer2, denom2, numer3, denom3,
                    result_numer, result_denom, malrule_numer, malrule_denom
                )
            else:
                steps = self._generate_concise_steps_three(
                    problem, numer1, denom1, numer2, denom2, numer3, denom3,
                    result_numer, result_denom, malrule_numer, malrule_denom
                )
        else:
            if verbose:
                steps = self._generate_verbose_steps(
                    problem, numer1, denom1, numer2, denom2,
                    result_numer, result_denom, malrule_numer, malrule_denom
                )
            else:
                steps = self._generate_concise_steps(
                    problem, numer1, denom1, numer2, denom2,
                    result_numer, result_denom, malrule_numer, malrule_denom
                )

        return Solution(
            answer=f"{malrule_numer}/{malrule_denom}",
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
