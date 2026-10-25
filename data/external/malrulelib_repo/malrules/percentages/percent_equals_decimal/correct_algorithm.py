"""
Correct algorithm for percentage/decimal conversion.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class PercentageConversionCorrectAlgorithm(CorrectAlgorithm):
    """Correctly converts between percentages and decimals."""

    def get_name(self) -> str:
        return "Correct Percentage Conversion"

    def get_description(self) -> str:
        return "Correctly converts between percent and decimal notation using division/multiplication by 100."

    def _generate_concise_steps(self, problem: Problem, correct_answer: float) -> List[str]:
        """Generate concise steps showing only formula and values."""
        steps = []
        conversion_type = problem.metadata['conversion_type']

        # Add question
        steps.append(problem.text)

        if conversion_type == 'percent_to_decimal':
            percent = problem.metadata['percent']
            steps.append(f"Formula: decimal = percent ÷ 100")
            steps.append(f"{percent} ÷ 100 = {correct_answer}")

        elif conversion_type == 'decimal_to_percent':
            decimal = problem.metadata['decimal']
            steps.append(f"Formula: percent = decimal × 100")
            steps.append(f"{decimal} × 100 = {correct_answer}")

        elif conversion_type == 'percent_in_calculation':
            percent = problem.metadata['percent']
            value = problem.metadata['value']
            decimal = percent / 100
            steps.append(f"Formula: result = (percent/100) × value")
            steps.append(f"{percent}/100 = {decimal}")
            steps.append(f"{decimal} × {value} = {correct_answer}")

        elif conversion_type == 'fraction_to_percent':
            numerator = problem.metadata['numerator']
            denominator = problem.metadata['denominator']
            decimal = numerator / denominator
            steps.append(f"Formula: percent = (numerator/denominator) × 100")
            steps.append(f"{numerator}/{denominator} = {decimal}")
            steps.append(f"{decimal} × 100 = {correct_answer}%")

        steps.append(f"Answer: {correct_answer}")
        return steps

    def _generate_verbose_steps(self, problem: Problem, correct_answer: float) -> List[str]:
        """Generate verbose steps with full explanations (original format)."""
        steps = []
        conversion_type = problem.metadata['conversion_type']

        if conversion_type == 'percent_to_decimal':
            percent = problem.metadata['percent']

            steps.append(f"Problem: Convert {percent}% to a decimal")
            steps.append("")
            steps.append("Remember: Percent means 'per hundred'")
            steps.append(f"  {percent}% = {percent} per 100 = {percent}/100")
            steps.append("")
            steps.append("Step 1: Divide by 100")
            steps.append(f"  {percent} ÷ 100 = {correct_answer}")
            steps.append("")
            steps.append("OR: Move decimal point 2 places left")
            steps.append(f"  {percent}. → {correct_answer}")
            steps.append("")
            steps.append(f"Final Answer: {correct_answer} ✓")

        elif conversion_type == 'decimal_to_percent':
            decimal = problem.metadata['decimal']

            steps.append(f"Problem: Convert {decimal} to a percentage")
            steps.append("")
            steps.append("Remember: To convert decimal to percent, multiply by 100")
            steps.append(f"  {decimal} × 100 = {correct_answer}")
            steps.append("")
            steps.append("OR: Move decimal point 2 places right")
            steps.append(f"  {decimal} → {correct_answer}%")
            steps.append("")
            steps.append("Verify: Does it make sense?")
            steps.append(f"  {decimal} is the same as {correct_answer}/100 = {correct_answer}% ✓")
            steps.append("")
            steps.append(f"Final Answer: {correct_answer}% ✓")

        elif conversion_type == 'percent_in_calculation':
            percent = problem.metadata['percent']
            value = problem.metadata['value']
            decimal = percent / 100

            steps.append(f"Problem: Calculate {percent}% of {value}")
            steps.append("")
            steps.append("Step 1: Convert percent to decimal")
            steps.append(f"  {percent}% = {percent}/100 = {decimal}")
            steps.append("")
            steps.append("Step 2: Multiply by the value")
            steps.append(f"  {decimal} × {value} = {correct_answer}")
            steps.append("")
            steps.append(f"Final Answer: {correct_answer} ✓")

        elif conversion_type == 'fraction_to_percent':
            numerator = problem.metadata['numerator']
            denominator = problem.metadata['denominator']
            decimal = numerator / denominator

            steps.append(f"Problem: Convert {numerator}/{denominator} to a percentage")
            steps.append("")
            steps.append("Step 1: Convert fraction to decimal")
            steps.append(f"  {numerator} ÷ {denominator} = {decimal}")
            steps.append("")
            steps.append("Step 2: Convert decimal to percent (multiply by 100)")
            steps.append(f"  {decimal} × 100 = {correct_answer}%")
            steps.append("")
            steps.append(f"Final Answer: {correct_answer}% ✓")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        conversion_type = problem.metadata['conversion_type']

        if conversion_type == 'percent_to_decimal':
            percent = problem.metadata['percent']
            correct_answer = percent / 100

        elif conversion_type == 'decimal_to_percent':
            decimal = problem.metadata['decimal']
            correct_answer = decimal * 100

        elif conversion_type == 'percent_in_calculation':
            percent = problem.metadata['percent']
            value = problem.metadata['value']
            decimal = percent / 100
            correct_answer = decimal * value

        elif conversion_type == 'fraction_to_percent':
            numerator = problem.metadata['numerator']
            denominator = problem.metadata['denominator']
            decimal = numerator / denominator
            correct_answer = decimal * 100
        else:
            raise ValueError(f"Unknown conversion_type: {conversion_type}")

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
