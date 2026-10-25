"""
Correct algorithm for rounding to significant figures.

Implements the correct significant figures rules.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import CorrectAlgorithm, Problem, Solution
import math


class SignificantFiguresCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for rounding to significant figures.

    Follows the standard rules for identifying and rounding to significant figures.
    """

    def get_name(self) -> str:
        return "Correct Significant Figures Algorithm"

    def get_description(self) -> str:
        return (
            "To round to N significant figures:\n"
            "1. Identify the first N significant digits (ignoring leading zeros)\n"
            "2. Look at the (N+1)th significant digit\n"
            "3. If it's ≥5, round up; if <5, round down\n"
            "4. Keep all leading zeros (they don't count as significant)\n\n"
            "Rules for significant figures:\n"
            "• Leading zeros (before the first non-zero digit) are NOT significant\n"
            "• All non-zero digits are significant\n"
            "• Zeros between non-zero digits are significant\n"
            "• Trailing zeros after a decimal point are significant"
        )

    def _count_sig_figs(self, number_str: str) -> int:
        """Count significant figures in a number string."""
        # Remove decimal point
        cleaned = number_str.replace('.', '')

        # Remove leading zeros
        cleaned = cleaned.lstrip('0')

        # Count remaining digits
        return len(cleaned)

    def _round_to_sig_figs(self, number: float, sig_figs: int) -> str:
        """Round a number to N significant figures using string manipulation for precision."""
        if number == 0:
            return "0"

        # Convert to string to work with exact representation
        number_str = f"{number:.15f}".rstrip('0')  # Use high precision, remove trailing zeros

        # Find first non-zero digit
        decimal_idx = number_str.find('.')
        if decimal_idx == -1:
            # No decimal point (shouldn't happen for our test cases)
            return str(number)

        # Get digits after decimal point
        after_decimal = number_str[decimal_idx + 1:]

        # Find first significant digit position
        first_sig_idx = len(after_decimal) - len(after_decimal.lstrip('0'))

        # Get all significant digits
        sig_digits = after_decimal.lstrip('0')

        if len(sig_digits) <= sig_figs:
            # Already has correct number of sig figs or fewer
            return number_str

        # Need to round
        # Take first sig_figs digits
        keep_digits = sig_digits[:sig_figs]
        next_digit = int(sig_digits[sig_figs]) if sig_figs < len(sig_digits) else 0

        # Round up if next digit >= 5
        if next_digit >= 5:
            # Convert to integer, add 1, convert back
            keep_int = int(keep_digits) + 1
            keep_digits = str(keep_int)

        # Reconstruct the number
        leading_zeros = '0' * first_sig_idx
        result = '0.' + leading_zeros + keep_digits

        return result

    def _compute_number_from_inputs(self, calc_inputs: dict, steps: list) -> float:
        """Compute the number from calculation inputs."""
        operation = calc_inputs['operation']

        if operation == 'multiply':
            if 'length' in calc_inputs and 'width' in calc_inputs:
                length = calc_inputs['length']
                width = calc_inputs['width']
                steps.append(f"Computing area: {length} × {width}")
                return length * width
            elif 'side' in calc_inputs:
                side = calc_inputs['side']
                steps.append(f"Computing area: {side} × {side}")
                return side * side
            elif 'base' in calc_inputs and 'height' in calc_inputs:
                base = calc_inputs['base']
                height = calc_inputs['height']
                steps.append(f"Computing area: {base} × {height}")
                return base * height
            elif 'factor1' in calc_inputs and 'factor2' in calc_inputs:
                factor1 = calc_inputs['factor1']
                factor2 = calc_inputs['factor2']
                steps.append(f"Computing product: {factor1} × {factor2}")
                return factor1 * factor2
        elif operation == 'divide':
            numerator = calc_inputs['numerator']
            denominator = calc_inputs['denominator']
            steps.append(f"Computing quotient: {numerator} ÷ {denominator}")
            return numerator / denominator
        elif operation == 'square':
            side = calc_inputs['side']
            steps.append(f"Computing square: {side}²")
            return side * side

        raise ValueError(f"Unknown operation: {operation}")

    def generate_verbose_steps(self, problem: Problem, number: float, number_str: str,
                               sig_figs: int, answer: str, calc_inputs: dict = None) -> list:
        """Generate verbose step-by-step solution."""
        steps = []

        # Check if we need to compute the number from calculation inputs
        if calc_inputs:
            self._compute_number_from_inputs(calc_inputs, steps)

        steps.append(f"Rounding {number_str} to {sig_figs} significant figures")

        # Identify leading zeros
        decimal_index = number_str.find('.')
        if decimal_index != -1:
            after_decimal = number_str[decimal_index + 1:]
            leading_zeros = len(after_decimal) - len(after_decimal.lstrip('0'))
            steps.append(
                f"Leading zeros (after decimal, before first non-zero): {leading_zeros}"
            )
            steps.append(f"Leading zeros do NOT count as significant figures")

        # Identify significant digits
        # Remove the "0." prefix and leading zeros
        sig_part = number_str.replace('0.', '').lstrip('0')
        current_sig_figs = len(sig_part)

        steps.append(
            f"Significant digits in {number_str}: '{sig_part}' ({current_sig_figs} sig figs)"
        )

        if current_sig_figs <= sig_figs:
            steps.append(
                f"Number already has {current_sig_figs} sig figs, "
                f"which is ≤ {sig_figs}, so no rounding needed"
            )
        else:
            steps.append(
                f"Take the first {sig_figs} significant digits and round based "
                f"on the {sig_figs + 1}th digit"
            )

        steps.append(f"Result: {answer}")
        steps.append(f"Final answer: {answer}")

        return steps

    def generate_concise_steps(self, problem: Problem, number: float, number_str: str,
                               sig_figs: int, answer: str, calc_inputs: dict = None) -> list:
        """Generate concise step-by-step solution."""
        steps = []

        # Add question
        steps.append(problem.text)

        # Add calculation step if needed
        if calc_inputs:
            operation = calc_inputs['operation']
            if operation == 'multiply':
                if 'length' in calc_inputs and 'width' in calc_inputs:
                    steps.append(f"{calc_inputs['length']} × {calc_inputs['width']} = {number_str}")
                elif 'side' in calc_inputs:
                    steps.append(f"{calc_inputs['side']} × {calc_inputs['side']} = {number_str}")
                elif 'base' in calc_inputs and 'height' in calc_inputs:
                    steps.append(f"{calc_inputs['base']} × {calc_inputs['height']} = {number_str}")
                elif 'factor1' in calc_inputs and 'factor2' in calc_inputs:
                    steps.append(f"{calc_inputs['factor1']} × {calc_inputs['factor2']} = {number_str}")
            elif operation == 'divide':
                steps.append(f"{calc_inputs['numerator']} ÷ {calc_inputs['denominator']} = {number_str}")
            elif operation == 'square':
                steps.append(f"{calc_inputs['side']}² = {number_str}")

        # Add rounding step
        sig_part = number_str.replace('0.', '').lstrip('0')
        steps.append(f"Round {number_str} to {sig_figs} sig figs: first {sig_figs} significant digits of {sig_part}")

        # Add answer
        steps.append(answer)

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct significant figures rounding algorithm.

        Args:
            problem: Significant figures problem to solve
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with correct answer
        """
        # Get sig_figs from operands (now only contains sig_figs)
        sig_figs = problem.operands[0]

        # Check if we need to compute the number from calculation inputs
        calc_inputs = None
        if 'calculation_inputs' in problem.metadata:
            calc_inputs = problem.metadata['calculation_inputs']
            temp_steps = []
            number = self._compute_number_from_inputs(calc_inputs, temp_steps)
            number_str = f"{number:.15f}".rstrip('0').rstrip('.')
        else:
            # For basic rounding problems, get the number from metadata
            number = problem.metadata['number']
            number_str = problem.metadata.get('number_str', str(number))

        # Round to N sig figs
        answer = self._round_to_sig_figs(number, sig_figs)

        # Generate steps based on verbose flag
        if verbose:
            steps = self.generate_verbose_steps(problem, number, number_str, sig_figs, answer, calc_inputs)
        else:
            steps = self.generate_concise_steps(problem, number, number_str, sig_figs, answer, calc_inputs)

        return Solution(
            answer=answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
