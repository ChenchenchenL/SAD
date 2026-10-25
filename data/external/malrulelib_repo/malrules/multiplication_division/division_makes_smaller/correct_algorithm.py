"""
Correct division algorithm.

Implements proper division including division by decimals less than 1.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import CorrectAlgorithm, Problem, Solution


class DivisionCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for division.

    Performs division correctly, understanding that dividing by a number less than 1
    produces a quotient larger than the dividend.
    """

    def get_name(self) -> str:
        return "Correct Division Algorithm"

    def get_description(self) -> str:
        return (
            "Performs division correctly. When dividing by a number less than 1, "
            "the quotient is larger than the dividend. Division by 0.5 is the same "
            "as multiplying by 2."
        )

    def _generate_concise_steps(self, problem: Problem, dividend: float, divisor: float,
                                 quotient: float, template: str) -> list:
        """
        Generate concise steps for the solution.

        Returns a list: [Question, step1, step2, ..., answer]
        """
        steps = []

        # Question
        steps.append(problem.text)

        # Formula extraction
        steps.append(f"{dividend} ÷ {divisor}")

        # Reciprocal insight for divisor < 1
        if divisor < 1:
            reciprocal = 1 / divisor
            steps.append(f"÷ {divisor} = × {reciprocal:.2f}")

        # Division step
        steps.append(f"{dividend} ÷ {divisor} = {quotient:.2f}")

        # Final answer
        steps.append(f"{quotient:.2f}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, dividend: float, divisor: float,
                                 quotient: float, template: str) -> list:
        """
        Generate verbose steps for the solution (original step format).
        """
        steps = []

        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD: Understanding division by numbers less than 1")
        steps.append("")

        # Provide template-specific context
        if template == 'fraction_division':
            frac_str = problem.metadata.get('fraction_str', str(divisor))
            steps.append(f"Dividing {dividend:.0f} ÷ {frac_str}")
            steps.append(f"First convert fraction to decimal: {frac_str} = {divisor}")
        elif template == 'time_conversion':
            steps.append(f"Time division: {dividend} hours ÷ {divisor} hours per shift")
        elif template == 'capacity_division':
            steps.append(f"Capacity division: {dividend} liters ÷ {divisor} liters per bottle")
        elif template == 'speed_calculation':
            steps.append(f"Speed formula: speed = distance ÷ time")
            steps.append(f"Speed = {dividend} ÷ {divisor}")
        elif template == 'recipe_scaling_up':
            steps.append(f"Recipe scaling: {dividend} for {divisor} portion → full portion")
            steps.append(f"Full amount = {dividend} ÷ {divisor}")
        elif template == 'unit_conversion':
            from_unit = problem.metadata.get('from_unit', '')
            to_unit = problem.metadata.get('to_unit', '')
            steps.append(f"Unit conversion: {dividend} {from_unit} ÷ {divisor} {from_unit} per {to_unit}")
        elif template in ['measurement_context', 'sharing_context', 'rate_context']:
            steps.append(f"Real-world interpretation: '{problem.text}'")
            steps.append(f"This is asking: {dividend} ÷ {divisor}")
        else:
            steps.append(f"Performing division: {dividend} ÷ {divisor}")

        steps.append("")

        # Provide explanation based on divisor
        if divisor < 1:
            reciprocal = 1 / divisor
            steps.append(f"✓ KEY INSIGHT: Dividing by {divisor} is the same as multiplying by {reciprocal:.2f}")
            steps.append(f"  Why? Because {divisor} × {reciprocal:.2f} = 1")
            steps.append("")
            steps.append(f"So: {dividend} ÷ {divisor} = {dividend} × {reciprocal:.2f} = {quotient:.2f}")
            steps.append("")
            steps.append(f"✓ IMPORTANT: When dividing by a number less than 1,")
            steps.append(f"  the result is LARGER than the dividend")
            steps.append(f"  ({quotient:.2f} > {dividend})")
        elif divisor == 1:
            steps.append(f"Dividing by 1 gives the same number: {dividend}")
        else:
            steps.append(f"Dividing by a number greater than 1 gives a smaller result")
            steps.append(f"  ({quotient:.2f} < {dividend})")

        steps.append("")
        steps.append(f"Final calculation: {dividend} ÷ {divisor} = {quotient:.2f}")
        steps.append("")
        steps.append(f"Answer: {quotient:.2f} ✓")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct division.

        Args:
            problem: Division problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with correct division
        """
        template = problem.metadata.get('template', 'basic_decimal_division')
        dividend = problem.metadata['dividend']
        divisor = problem.metadata['divisor']

        # Compute the quotient (never use metadata['correct_answer'])
        quotient = dividend / divisor
        correct_answer = f"{quotient:.2f}"

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, dividend, divisor, quotient, template)
        else:
            steps = self._generate_concise_steps(problem, dividend, divisor, quotient, template)

        return Solution(
            answer=str(correct_answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
