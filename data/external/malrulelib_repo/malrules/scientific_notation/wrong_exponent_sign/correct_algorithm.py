"""
Correct algorithm for scientific notation conversion.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class ScientificNotationCorrectAlgorithm(CorrectAlgorithm):
    """Correctly converts to scientific notation with proper exponent sign."""

    def get_name(self) -> str:
        return "Correct Scientific Notation Conversion"

    def get_description(self) -> str:
        return "Correctly determines exponent sign based on decimal movement direction."

    def _generate_verbose_steps(self, problem: Problem, context: dict) -> list:
        """Generate verbose steps with full explanations."""
        steps = []
        number_str = context['number_str']
        decimal_number = context['decimal_number']
        mantissa = context['mantissa']
        correct_exponent = context['correct_exponent']

        steps.append(f"Problem: Write {number_str} in scientific notation")
        steps.append("")
        steps.append("CORRECT METHOD: Sign depends on direction of decimal movement")
        steps.append("")
        steps.append(f"Step 1: Move decimal to get number between 1 and 10")
        steps.append(f"  {number_str} -> {mantissa}")
        steps.append(f"  Decimal moved {abs(correct_exponent)} places")
        steps.append("")
        steps.append(f"Step 2: Determine exponent sign from direction")

        if abs(decimal_number) < 1 and decimal_number != 0:
            steps.append(f"  Original number < 1 (small number)")
            steps.append(f"  Decimal moved RIGHT -> NEGATIVE exponent")
            steps.append(f"  Exponent: {correct_exponent}")
        elif abs(decimal_number) >= 10:
            steps.append(f"  Original number > 10 (large number)")
            steps.append(f"  Decimal moved LEFT -> POSITIVE exponent")
            steps.append(f"  Exponent: +{correct_exponent}")
        else:
            steps.append(f"  Number already between 1 and 10")
            steps.append(f"  Exponent: {correct_exponent}")

        steps.append("")
        steps.append(f"Step 3: Write in scientific notation")
        if correct_exponent >= 0:
            steps.append(f"  {mantissa} x 10^{correct_exponent}")
        else:
            steps.append(f"  {mantissa} x 10^({correct_exponent})")
        steps.append("")
        steps.append(f"Final Answer: {mantissa} x 10^{correct_exponent}")
        steps.append("")
        steps.append("Rule to remember:")
        steps.append("  Small number (< 1) -> NEGATIVE exponent")
        steps.append("  Large number (> 10) -> POSITIVE exponent")
        return steps

    def _generate_concise_steps(self, problem: Problem, context: dict) -> list:
        """Generate concise steps with only formulas and values."""
        steps = []
        number_str = context['number_str']
        decimal_number = context['decimal_number']
        mantissa = context['mantissa']
        correct_exponent = context['correct_exponent']
        is_word_problem = problem.metadata.get('is_word_problem', False)

        # Add question
        steps.append(problem.text)

        # Add formula extraction for word problems
        if is_word_problem:
            steps.append(f"{number_str}")

        # Add calculation steps
        steps.append(f"{number_str} -> {mantissa}")
        steps.append(f"Decimal moved {abs(correct_exponent)} places")

        if abs(decimal_number) < 1 and decimal_number != 0:
            steps.append(f"Moved right -> negative exponent")
        elif abs(decimal_number) >= 10:
            steps.append(f"Moved left -> positive exponent")

        # Add answer
        steps.append(f"{mantissa} x 10^{correct_exponent}")
        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct scientific notation conversion algorithm.

        Args:
            problem: Scientific notation conversion problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with correct answer
        """
        # Parse the input from metadata
        number_str = problem.metadata['number_str']
        decimal_number = problem.metadata['decimal_number']

        # Compute mantissa and exponent from the decimal number
        if decimal_number == 0:
            mantissa = 0
            correct_exponent = 0
        elif abs(decimal_number) >= 1:
            # Large number: move decimal left (positive exponent)
            mantissa = abs(decimal_number)
            correct_exponent = 0
            while mantissa >= 10:
                mantissa /= 10
                correct_exponent += 1
            if decimal_number < 0:
                mantissa = -mantissa
        else:
            # Small number: move decimal right (negative exponent)
            mantissa = abs(decimal_number)
            correct_exponent = 0
            while mantissa < 1:
                mantissa *= 10
                correct_exponent -= 1
            if decimal_number < 0:
                mantissa = -mantissa

        context = {
            'number_str': number_str,
            'decimal_number': decimal_number,
            'mantissa': mantissa,
            'correct_exponent': correct_exponent
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, context)
        else:
            steps = self._generate_concise_steps(problem, context)

        return Solution(
            answer=correct_exponent,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
