"""
Malrule algorithm for Percent-Equals-Decimal error.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class PercentEqualsDecimalMalrule(Malrule):
    """
    Students confuse percent, decimal, and whole number notations.

    Example: 25% to decimal → Student thinks: 25 (should be 0.25)
    """

    def get_name(self) -> str:
        return "Percent-Decimal Notation Confusion"

    def get_description(self) -> str:
        return (
            "Students treat percent, decimal, and whole number notations as interchangeable, "
            "failing to recognize that percent means 'per hundred' and requires division by 100 "
            "to convert to decimal form. This reflects a broader difficulty with rational number "
            "notation where students do not understand that different symbolic representations "
            "indicate the same underlying quantity through different numerical expressions."
        )

    def _generate_concise_steps(self, problem: Problem, malrule_answer: Any) -> List[str]:
        """Generate concise steps showing only formula and values."""
        steps = []
        conversion_type = problem.metadata['conversion_type']

        # Add question
        steps.append(problem.text)

        if conversion_type == 'percent_to_decimal':
            percent = problem.metadata['percent']
            steps.append(f"Formula: decimal = percent")
            steps.append(f"{percent}% = {malrule_answer}")

        elif conversion_type == 'decimal_to_percent':
            decimal = problem.metadata['decimal']
            steps.append(f"Formula: percent = decimal")
            steps.append(f"{decimal} = {malrule_answer}%")

        elif conversion_type == 'percent_in_calculation':
            percent = problem.metadata['percent']
            value = problem.metadata['value']
            steps.append(f"Formula: result = percent × value")
            steps.append(f"{percent} × {value} = {malrule_answer}")

        elif conversion_type == 'fraction_to_percent':
            fraction = problem.metadata['fraction']
            decimal = problem.metadata['decimal']
            steps.append(f"Formula: percent = decimal")
            steps.append(f"{fraction} = {decimal} = {malrule_answer}%")

        steps.append(f"Answer: {malrule_answer}")
        return steps

    def _generate_verbose_steps(self, problem: Problem, malrule_answer: Any) -> List[str]:
        """Generate verbose steps with full explanations (original format)."""
        steps = []
        template = problem.metadata.get('template', 'percent_to_decimal')
        conversion_type = problem.metadata['conversion_type']

        if conversion_type == 'percent_to_decimal':
            percent = problem.metadata['percent']

            if template == 'word_problem':
                steps.append(f"Problem: {problem.text}")
                steps.append(f"Expression: Convert {percent}% to decimal")
            else:
                steps.append(f"Problem: Convert {percent}% to a decimal")
            steps.append("")
            steps.append("MALRULE: Percent and decimal are the same")
            steps.append(f"  MALRULE REASONING: '{percent}% is just {percent}'")
            steps.append(f"  'Remove the % sign and you have the answer'")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT - forgot to divide by 100!)")

        elif conversion_type == 'decimal_to_percent':
            decimal = problem.metadata['decimal']

            if template == 'word_problem':
                steps.append(f"Problem: {problem.text}")
                steps.append(f"Expression: Convert {decimal} to percentage")
            else:
                steps.append(f"Problem: Convert {decimal} to a percentage")
            steps.append("")
            steps.append("MALRULE: Decimal and percent are the same")
            steps.append(f"  MALRULE REASONING: '{decimal} is just {decimal}%'")
            steps.append(f"  'Just add the % sign'")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer}% (INCORRECT - forgot to multiply by 100!)")

        elif conversion_type == 'percent_in_calculation':
            percent = problem.metadata['percent']
            value = problem.metadata['value']

            steps.append(f"Problem: Calculate {percent}% of {value}")
            steps.append("")
            steps.append("MALRULE: Use percent value directly")
            steps.append(f"  MALRULE REASONING: '{percent}% of {value} means {percent} × {value}'")
            steps.append(f"  'The percent is the number to multiply by'")
            steps.append("")
            steps.append(f"Calculate: {percent} × {value} = {malrule_answer}")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT - should convert to decimal first!)")

        elif conversion_type == 'fraction_to_percent':
            fraction = problem.metadata['fraction']
            decimal = problem.metadata['decimal']

            steps.append(f"Problem: Convert {fraction} to a percentage")
            steps.append("")
            steps.append("MALRULE: Convert to decimal, then it's the same as percent")
            steps.append(f"  MALRULE REASONING: '{fraction} = {decimal}, so that's {decimal}%'")
            steps.append(f"  'Just convert to decimal and add %'")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer}% (INCORRECT - forgot to multiply by 100!)")

        return steps

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        conversion_type = problem.metadata['conversion_type']

        # Malrule: treat percent and decimal as the same
        if conversion_type == 'percent_to_decimal':
            # Student thinks 25% = 25
            return problem.metadata['percent']
        elif conversion_type == 'decimal_to_percent':
            # Student thinks 0.30 = 0.30%
            return problem.metadata['decimal']
        elif conversion_type == 'percent_in_calculation':
            # Student uses percent value directly: 30% of 50 = 30 × 50
            percent = problem.metadata['percent']
            value = problem.metadata['value']
            return percent * value
        elif conversion_type == 'fraction_to_percent':
            # Student converts to decimal and adds %: 3/4 = 0.75 = 0.75%
            return problem.metadata['decimal']

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        conversion_type = problem.metadata['conversion_type']

        # Calculate malrule answer
        if conversion_type == 'percent_to_decimal':
            percent = problem.metadata['percent']
            malrule_answer = percent

        elif conversion_type == 'decimal_to_percent':
            decimal = problem.metadata['decimal']
            malrule_answer = decimal

        elif conversion_type == 'percent_in_calculation':
            percent = problem.metadata['percent']
            value = problem.metadata['value']
            malrule_answer = percent * value

        elif conversion_type == 'fraction_to_percent':
            decimal = problem.metadata['decimal']
            malrule_answer = decimal
        else:
            raise ValueError(f"Unknown conversion_type: {conversion_type}")

        if verbose:
            steps = self._generate_verbose_steps(problem, malrule_answer)
        else:
            steps = self._generate_concise_steps(problem, malrule_answer)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
