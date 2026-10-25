"""
Multiplication-Makes-Bigger malrule algorithm.

Implements the systematic error where students incorrectly believe that
multiplication always produces a result larger than both factors.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List

class MultiplicationMakesBiggerMalrule(Malrule):
    """
    Implements the Multiplication-Makes-Bigger bug.

    Students incorrectly believe that multiplication ALWAYS makes numbers bigger.
    When multiplying by numbers less than 1 (like 0.5 × 0.2 = 0.1), they expect
    the result to be larger than both factors, not smaller.

    This stems from overgeneralizing from whole number multiplication where
    the product is typically larger than either factor (except ×1 or ×0).
    """

    def get_name(self) -> str:
        return "Multiplication-Makes-Bigger"

    def get_description(self) -> str:
        return (
            "A widespread misconception where students believe multiplication always produces "
            "a result larger than both factors. Fischbein et al. (1985) identified this as "
            "stemming from the 'primitive intuitive model' of multiplication as repeated addition, "
            "where results are always larger with whole numbers. When multiplying by decimals or "
            "fractions less than 1 (e.g., 0.5 × 0.2 = 0.1), students reject the correct answer "
            "as impossible because the product is smaller than both factors. They may substitute "
            "addition or refuse to accept the mathematically correct result."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        factor1, factor2 = problem.operands

        # Check if either factor is less than 1
        if factor1 < 1 or factor2 < 1:
            # Student computes correct product first
            correct_product = factor1 * factor2

            # But rejects it if it's smaller than either factor
            if correct_product < factor1 or correct_product < factor2:
                # Add instead (malrule behavior)
                result = factor1 + factor2
            else:
                # Accidentally correct case
                result = correct_product
        else:
            # Both factors >= 1, multiply normally
            result = factor1 * factor2

        return f"{result:.4f}"

    def _generate_concise_steps(self, problem: Problem, malrule_result: float, display_answer: str) -> list:
        """Generate concise steps with only formula and values."""
        template = problem.metadata.get('template', 'basic_decimal_multiplication')
        factor1, factor2 = problem.operands
        correct_product = factor1 * factor2
        steps = []
        steps.append(f"Question: {problem.text}")

        if factor1 < 1 or factor2 < 1:
            if template == 'fraction_multiplication':
                frac1 = problem.metadata.get('fraction1_str', str(factor1))
                frac2 = problem.metadata.get('fraction2_str', str(factor2))
                steps.append(f"{frac1} × {frac2} = {correct_product:.4f}")
            elif template == 'area_rectangle':
                length = problem.metadata.get('length', factor1)
                width = problem.metadata.get('width', factor2)
                steps.append(f"Area = {length} × {width} = {correct_product:.4f}")
            elif template == 'volume_box':
                length = problem.metadata.get('length', 0)
                width = problem.metadata.get('width', 0)
                height = problem.metadata.get('height', 0)
                steps.append(f"Volume = {length} × {width} × {height} = {correct_product:.6f}")
            elif template == 'probability_compound':
                steps.append(f"P(A and B) = {factor1} × {factor2} = {correct_product:.4f}")
            elif template == 'rate_distance':
                rate = problem.metadata.get('rate', factor1)
                time = problem.metadata.get('time', factor2)
                steps.append(f"Distance = {rate} × {time} = {correct_product:.4f}")
            else:
                steps.append(f"{factor1} × {factor2} = {correct_product:.4f}")

            if correct_product < factor1 or correct_product < factor2:
                steps.append(f"{factor1} + {factor2} = {malrule_result:.4f}")
        else:
            steps.append(f"{factor1} × {factor2} = {malrule_result:.4f}")

        steps.append(f"Answer: {display_answer}")
        return steps

    def _generate_verbose_steps(self, problem: Problem, malrule_result: float, display_answer: str) -> list:
        """Generate verbose steps with full explanations."""
        template = problem.metadata.get('template', 'basic_decimal_multiplication')
        factor1, factor2 = problem.operands
        correct_product = factor1 * factor2
        steps = []

        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: Multiplication always makes numbers bigger")
        steps.append("  Student belief: 'Multiplying makes things grow'")
        steps.append("")

        # Check if either factor is less than 1
        if factor1 < 1 or factor2 < 1:
            if template == 'fraction_multiplication':
                frac1 = problem.metadata.get('fraction1_str', str(factor1))
                frac2 = problem.metadata.get('fraction2_str', str(factor2))
                steps.append(f"Computing: {frac1} × {frac2}")
                steps.append(f"  = {factor1} × {factor2} = {correct_product:.4f}")
            elif template == 'area_rectangle':
                length = problem.metadata.get('length', factor1)
                width = problem.metadata.get('width', factor2)
                steps.append(f"Computing area: {length} × {width} = {correct_product:.4f}")
            elif template == 'volume_box':
                length = problem.metadata.get('length', 0)
                width = problem.metadata.get('width', 0)
                height = problem.metadata.get('height', 0)
                steps.append(f"Computing volume: {length} × {width} × {height}")
                steps.append(f"  = {factor1} × {factor2} = {correct_product:.4f}")
            elif template == 'probability_compound':
                steps.append(f"Computing: {factor1} × {factor2} = {correct_product:.4f}")
            elif template == 'compound_scaling':
                steps.append(f"Computing: {factor1} of {factor2} = {factor1} × {factor2} = {correct_product:.4f}")
            elif template == 'rate_distance':
                rate = problem.metadata.get('rate', factor1)
                time = problem.metadata.get('time', factor2)
                steps.append(f"Computing distance: {rate} × {time} = {correct_product:.4f}")
            else:
                steps.append(f"Computing: {factor1} × {factor2} = {correct_product:.4f}")

            # But rejects it because it's smaller
            if correct_product < factor1 or correct_product < factor2:
                steps.append("")
                steps.append(
                    f"But {correct_product:.4f} is smaller than {max(factor1, factor2)}! "
                    f"This can't be right..."
                )
                steps.append(f"MALRULE REASONING: Multiplication must make it bigger!")
                steps.append(f"  Maybe I should add instead? {factor1} + {factor2} = {malrule_result:.4f}")
                steps.append("")
                steps.append(f"Answer: {display_answer} (INCORRECT - added instead of multiplied)")
                steps.append(f"  Error: Student doesn't understand multiplication by numbers < 1")
            else:
                # Accidentally correct case
                steps.append("")
                steps.append(f"Answer: {display_answer} (accidentally correct)")
        else:
            # Both factors >= 1, student might get it right
            steps.append(f"Computing: {factor1} × {factor2} = {malrule_result:.4f}")
            steps.append("")
            steps.append(f"Answer: {display_answer}")

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Multiplication-Makes-Bigger malrule.

        Args:
            problem: Multiplication problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with incorrect answer

        Since students expect multiplication to make numbers bigger, when they
        encounter a result that's smaller, they may:
        1. Add the numbers instead
        2. Multiply and then think it's wrong
        3. Manipulate the result to be bigger

        For this implementation, we'll have them add when both factors < 1
        """
        template = problem.metadata.get('template', 'basic_decimal_multiplication')
        factor1, factor2 = problem.operands

        # Compute the correct product first
        correct_product = factor1 * factor2

        # Determine malrule behavior
        if factor1 < 1 or factor2 < 1:
            # Check if product is smaller than either factor
            if correct_product < factor1 or correct_product < factor2:
                # Student adds instead (malrule)
                malrule_result = factor1 + factor2
            else:
                # Accidentally correct
                malrule_result = correct_product
        else:
            # Both factors >= 1, student multiplies correctly
            malrule_result = correct_product

        # Format answer for display (with units)
        if template in ['money_context', 'percent_discount']:
            display_answer = f"${malrule_result:.2f}"
        elif template in ['measurement_context']:
            unit = problem.metadata.get('unit', '')
            display_answer = f"{malrule_result:.2f} {unit}"
        elif template == 'area_rectangle':
            unit = problem.metadata.get('unit', 'meters')
            # Malrule: wrong unit (just unit, not square unit)
            display_answer = f"{malrule_result:.4f} {unit}"
        elif template == 'volume_box':
            display_answer = f"{malrule_result:.6f}"
        elif template == 'rate_distance':
            rate_unit = problem.metadata.get('rate_unit', 'miles per hour')
            distance_unit = rate_unit.split()[0]
            display_answer = f"{malrule_result:.4f} {distance_unit}"
        else:
            display_answer = f"{malrule_result:.4f}"

        if verbose:
            steps = self._generate_verbose_steps(problem, malrule_result, display_answer)
        else:
            steps = self._generate_concise_steps(problem, malrule_result, display_answer)

        # Return numeric answer without units (always 4 decimal places)
        final_answer = f"{malrule_result:.4f}"

        return Solution(
            answer=final_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
