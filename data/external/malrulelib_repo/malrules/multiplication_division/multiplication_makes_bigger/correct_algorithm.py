"""
Correct multiplication algorithm.

Implements the standard algorithm for multiplying numbers,
including decimals and fractions less than 1.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import CorrectAlgorithm, Problem, Solution


class MultiplicationCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for multiplication.

    Multiplies numbers correctly, understanding that:
    - Multiplying by numbers < 1 makes the result smaller
    - Multiplying by numbers > 1 makes the result larger
    - Multiplying by 1 keeps the number the same
    """

    def get_name(self) -> str:
        return "Correct Multiplication Algorithm"

    def get_description(self) -> str:
        return (
            "The standard algorithm for multiplying numbers. Correctly handles "
            "multiplication with decimals and fractions, understanding that multiplying "
            "by values less than 1 produces a smaller result (scaling down) and "
            "multiplying by values greater than 1 produces a larger result (scaling up)."
        )

    def _generate_concise_steps(self, problem: Problem, correct_answer: str, product: float) -> list:
        """Generate concise steps with only formula and values."""
        template = problem.metadata.get('template', 'basic_decimal_multiplication')
        factor1, factor2 = problem.operands
        steps = []
        steps.append(f"Question: {problem.text}")

        if template == 'fraction_multiplication':
            frac1 = problem.metadata.get('fraction1_str', str(factor1))
            frac2 = problem.metadata.get('fraction2_str', str(factor2))
            steps.append(f"{frac1} × {frac2}")
            steps.append(f"= {factor1} × {factor2}")
            steps.append(f"= {product:.4f}")
        elif template == 'area_rectangle':
            length = problem.metadata.get('length', factor1)
            width = problem.metadata.get('width', factor2)
            steps.append(f"Area = {length} × {width}")
            steps.append(f"= {product:.4f}")
        elif template == 'volume_box':
            length = problem.metadata.get('length', 0)
            width = problem.metadata.get('width', 0)
            height = problem.metadata.get('height', 0)
            steps.append(f"Volume = {length} × {width} × {height}")
            steps.append(f"= {product:.6f}")
        elif template == 'probability_compound':
            prob1 = problem.metadata.get('probability1', factor1)
            prob2 = problem.metadata.get('probability2', factor2)
            steps.append(f"P(A and B) = {prob1} × {prob2}")
            steps.append(f"= {product:.4f}")
        elif template == 'compound_scaling':
            steps.append(f"{factor1} × {factor2}")
            steps.append(f"= {product:.4f}")
        elif template == 'rate_distance':
            rate = problem.metadata.get('rate', factor1)
            time = problem.metadata.get('time', factor2)
            steps.append(f"Distance = {rate} × {time}")
            steps.append(f"= {product:.4f}")
        else:
            steps.append(f"{factor1} × {factor2}")
            steps.append(f"= {product:.4f}")

        steps.append(f"Answer: {correct_answer}")
        return steps

    def _generate_verbose_steps(self, problem: Problem, correct_answer: str, product: float) -> list:
        """Generate verbose steps with full explanations."""
        template = problem.metadata.get('template', 'basic_decimal_multiplication')
        factor1, factor2 = problem.operands
        steps = []

        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD: Understanding multiplication with numbers < 1")
        steps.append("")

        # Provide template-specific context
        if template == 'fraction_multiplication':
            frac1 = problem.metadata.get('fraction1_str', str(factor1))
            frac2 = problem.metadata.get('fraction2_str', str(factor2))
            steps.append(f"Multiplying {frac1} × {frac2}")
            steps.append(f"First convert to decimals: {frac1} = {factor1}, {frac2} = {factor2}")
        elif template == 'area_rectangle':
            length = problem.metadata.get('length', factor1)
            width = problem.metadata.get('width', factor2)
            steps.append(f"Area of rectangle: length × width")
            steps.append(f"Area = {length} × {width}")
        elif template == 'volume_box':
            length = problem.metadata.get('length', 0)
            width = problem.metadata.get('width', 0)
            height = problem.metadata.get('height', 0)
            steps.append(f"Volume of box: length × width × height")
            steps.append(f"Volume = {length} × {width} × {height}")
            steps.append(f"= ({length} × {width}) × {height} = {factor1} × {factor2}")
        elif template == 'probability_compound':
            prob1 = problem.metadata.get('probability1', factor1)
            prob2 = problem.metadata.get('probability2', factor2)
            steps.append(f"Compound probability: P(A and B) = P(A) × P(B)")
            steps.append(f"P(A and B) = {prob1} × {prob2}")
        elif template == 'compound_scaling':
            steps.append(f"Compound scaling: 'a of b' means a × b")
            steps.append(f"{factor1} of {factor2} = {factor1} × {factor2}")
        elif template == 'rate_distance':
            rate = problem.metadata.get('rate', factor1)
            time = problem.metadata.get('time', factor2)
            steps.append(f"Distance formula: distance = rate × time")
            steps.append(f"Distance = {rate} × {time}")
        elif template in ['money_context', 'measurement_context', 'percent_discount']:
            steps.append(f"Real-world interpretation: '{problem.text}'")
            steps.append(f"This is asking: {factor1} × {factor2}")
        else:
            steps.append(f"Multiplying {factor1} × {factor2}")

        steps.append("")

        # Explain the meaning based on the factors
        if factor1 < 1 and factor2 < 1:
            steps.append(f"KEY INSIGHT: Both factors are less than 1")
            steps.append(f"  Multiplying by {factor1} means 'taking {factor1} of' {factor2}")
            steps.append(f"  Or: multiplying by {factor2} means 'taking {factor2} of' {factor1}")
            steps.append(f"  Either way, we're taking a fraction of a fraction, which is smaller")
        elif factor1 < 1:
            steps.append(f"KEY INSIGHT: {factor1} is less than 1")
            steps.append(f"  Multiplying by {factor1} means 'taking {factor1} of' {factor2}")
            steps.append(f"  This makes the result smaller than {factor2}")
        elif factor2 < 1:
            steps.append(f"KEY INSIGHT: {factor2} is less than 1")
            steps.append(f"  Multiplying by {factor2} means 'taking {factor2} of' {factor1}")
            steps.append(f"  This makes the result smaller than {factor1}")
        else:
            steps.append(f"Both factors are greater than or equal to 1")
            steps.append(f"The product will be greater than or equal to both factors")

        steps.append("")
        steps.append(f"Computing: {factor1} × {factor2} = {product:.4f}")
        steps.append("")

        # Add verification note
        if factor1 < 1 or factor2 < 1:
            larger_factor = max(factor1, factor2)
            if product < larger_factor:
                steps.append(f"Verification: {product:.4f} < {larger_factor}")
                steps.append(f"  CORRECT - multiplying by a number < 1 makes it smaller!")
        else:
            smaller_factor = min(factor1, factor2)
            if product >= smaller_factor:
                steps.append(f"Verification: {product:.4f} >= {smaller_factor} (Correct)")

        steps.append("")
        steps.append(f"Answer: {correct_answer}")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct multiplication algorithm.

        Args:
            problem: Multiplication problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with correct product
        """
        template = problem.metadata.get('template', 'basic_decimal_multiplication')
        factor1, factor2 = problem.operands

        # Compute the product (never use metadata['correct_answer'])
        product = factor1 * factor2

        # Format answer based on template
        if template in ['money_context', 'percent_discount']:
            correct_answer = f"${product:.2f}"
        elif template in ['measurement_context']:
            unit = problem.metadata.get('unit', '')
            correct_answer = f"{product:.2f} {unit}"
        elif template == 'area_rectangle':
            unit = problem.metadata.get('unit', 'meters')
            correct_answer = f"{product:.4f} square {unit}"
        elif template == 'volume_box':
            unit = problem.metadata.get('unit', 'meters')
            correct_answer = f"{product:.6f} cubic {unit}"
        elif template == 'rate_distance':
            rate_unit = problem.metadata.get('rate_unit', 'miles per hour')
            distance_unit = rate_unit.split()[0]
            correct_answer = f"{product:.4f} {distance_unit}"
        else:
            # Default: just numeric
            correct_answer = f"{product:.4f}"

        if verbose:
            steps = self._generate_verbose_steps(problem, correct_answer, product)
        else:
            steps = self._generate_concise_steps(problem, correct_answer, product)

        return Solution(
            answer=str(correct_answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
