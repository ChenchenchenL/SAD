"""
Decimal-Places-Same-As-Sig-Figs malrule algorithm.

Implements the systematic error where students confuse decimal places
with significant figures.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List
from fractions import Fraction

class DecimalPlacesSameAsSigFigsMalrule(Malrule):
    """
    Implements the Decimal-Places-Same-As-Sig-Figs bug.

    Students confuse "round to N significant figures" with "round to N decimal places".
    """

    def get_name(self) -> str:
        return "Decimal-Places-Same-As-Sig-Figs"

    def get_description(self) -> str:
        return (
            "Students confuse decimal places with significant figures. When asked "
            "to round to N significant figures, they instead round to N decimal "
            "places. This confusion is documented in education research as being "
            "widespread, even occurring at university level among lecturers "
            "(Chemistry Stack Exchange community reports). For example, rounding "
            "0.00456 to 3 significant figures should give 0.00456 (all three "
            "non-zero digits are significant), but students incorrectly round to "
            "3 decimal places, giving 0.005."
        )

    def _round_to_decimal_places(self, number: float, decimal_places: int) -> str:
        """Round a number to N decimal places."""
        # Round to decimal places
        rounded = round(number, decimal_places)

        # Format with exactly that many decimal places
        format_str = f"{{:.{decimal_places}f}}"
        return format_str.format(rounded)

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

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Get sig_figs from operands
        sig_figs = problem.operands[0]

        # Compute or get the number
        if 'calculation_inputs' in problem.metadata:
            calc_inputs = problem.metadata['calculation_inputs']
            steps = []
            number = self._compute_number_from_inputs(calc_inputs, steps)
        else:
            number = problem.metadata['number']

        # Malrule: Confuse decimal places with significant figures
        return self._round_to_decimal_places(number, sig_figs)

    def generate_verbose_steps(self, problem: Problem, number: float, number_str: str,
                               sig_figs: int, answer: str, calc_inputs: dict = None) -> list:
        """Generate verbose step-by-step solution with malrule."""
        steps = []

        # Check if we need to compute the number from calculation inputs
        if calc_inputs:
            self._compute_number_from_inputs(calc_inputs, steps)

        steps.append(f"Rounding {number_str} to {sig_figs} significant figures")

        # MALRULE: Student confuses sig figs with decimal places
        steps.append(
            f"Student thinks '{sig_figs} significant figures' means "
            f"'{sig_figs} decimal places'"
        )

        steps.append(f"Round to {sig_figs} decimal places: {answer}")
        steps.append(f"Final answer: {answer} (INCORRECT due to malrule)")

        return steps

    def generate_concise_steps(self, problem: Problem, number: float, number_str: str,
                               sig_figs: int, answer: str, calc_inputs: dict = None) -> list:
        """Generate concise step-by-step solution with malrule."""
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

        # Add malrule step: round to decimal places instead of sig figs
        steps.append(f"Round {number_str} to {sig_figs} decimal places: {answer}")

        # Add answer
        steps.append(answer)

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Decimal-Places-Same-As-Sig-Figs malrule.

        Args:
            problem: Significant figures rounding problem to solve
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with incorrect answer
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

        # Malrule: Confuse decimal places with significant figures
        answer = self._round_to_decimal_places(number, sig_figs)

        # Generate steps based on verbose flag
        if verbose:
            steps = self.generate_verbose_steps(problem, number, number_str, sig_figs, answer, calc_inputs)
        else:
            steps = self.generate_concise_steps(problem, number, number_str, sig_figs, answer, calc_inputs)

        return Solution(
            answer=answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
