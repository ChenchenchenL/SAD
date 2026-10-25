"""
Count-All-Zeros-For-Exponent malrule algorithm.

Implements the systematic error where students count ALL zeros in a number
when determining the exponent for scientific notation, without considering
whether zeros are leading, trailing, or between significant digits.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List
import random

class CountAllZerosMalrule(Malrule):
    """
    Implements the Count-All-Zeros-For-Exponent bug.

    Students incorrectly count ALL zeros in a number to determine the exponent,
    rather than counting the number of decimal places the decimal point moves.

    Examples:
    - 0.00450 has 3 leading zeros, so exponent should be -3 (4.50 x 10^-3)
      Malrule: Counts 4 zeros total, might use 10^4 or 10^-4

    - 3000 should be 3 x 10^3 (moved decimal 3 places left)
      Malrule: Counts 3 zeros, uses 10^3 (accidentally correct!) or formats wrong

    The malrule shows confusion about what the exponent represents.
    """

    def get_name(self) -> str:
        return "Count-All-Zeros-For-Exponent"

    def get_description(self) -> str:
        return (
            "Students count ALL zeros in a number when determining the exponent "
            "for scientific notation, without considering their placement. They don't "
            "distinguish between leading zeros, trailing zeros, and zeros between "
            "significant digits. Instead of counting decimal places moved, they simply "
            "count zeros and use that as the exponent magnitude."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Compute the malrule answer by applying the malrule logic
        solution = self._apply_malrule(problem)
        return solution.answer

    def _generate_verbose_steps(self, problem: Problem, context: dict) -> list:
        """Generate verbose steps with full explanations."""
        steps = []
        number_str = context['number_str']
        total_zeros = context['total_zeros']
        coefficient = context['coefficient']
        exponent = context['exponent']
        is_decimal = context['is_decimal']
        result = context['result']

        steps.append(f"Converting {number_str} to scientific notation")
        steps.append(f"MALRULE: Counting all zeros in the number")
        steps.append(f"Found {total_zeros} zeros in {number_str}")

        if is_decimal:
            steps.append(f"MALRULE: Since number is less than 1, using negative exponent: -{total_zeros}")
        else:
            steps.append(f"MALRULE: Since number is large, using positive exponent: {total_zeros}")

        steps.append(f"MALRULE ANSWER: {result}")
        steps.append(f"ERROR: Counted zeros instead of counting decimal places moved!")
        return steps

    def _generate_concise_steps(self, problem: Problem, context: dict) -> list:
        """Generate concise steps with only formulas and values."""
        steps = []
        number_str = context['number_str']
        total_zeros = context['total_zeros']
        coefficient = context['coefficient']
        exponent = context['exponent']
        result = context['result']
        is_word_problem = problem.metadata.get('is_word_problem', False)
        template = problem.metadata.get('template', '')

        # Add question
        steps.append(problem.text)

        # Add formula extraction for word problems
        if is_word_problem or 'word_problem' in template:
            steps.append(f"{number_str}")

        # Add calculation steps
        steps.append(f"Zeros count: {total_zeros}")
        steps.append(f"Coefficient: {coefficient}")
        steps.append(f"Exponent: {exponent}")

        # Add answer
        steps.append(result)
        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Count-All-Zeros malrule.

        Counts all zeros in the number and uses that count (or its negative)
        as the exponent, regardless of whether it's correct.

        Args:
            problem: Scientific notation conversion problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with malrule (incorrect) answer
        """
        # Compute the malrule answer from the number string
        number_str = problem.operands[0]

        # Count total zeros
        total_zeros = number_str.count('0')

        # Determine if it's a small decimal or large number
        is_decimal = '.' in number_str and float(number_str) < 1
        is_large = '.' not in number_str or float(number_str) >= 10

        # Extract the significant digits (non-zero part)
        number_float = float(number_str)

        # Get non-zero digits
        stripped = number_str.replace('.', '').lstrip('0').rstrip('0')
        if not stripped:
            stripped = '0'

        # Get coefficient (simplified - take significant digits)
        sig_digits = number_str.replace('.', '').lstrip('0')
        if not sig_digits:
            coefficient = 0.0
        else:
            # Place decimal after first digit
            if len(sig_digits) == 1:
                coefficient = float(sig_digits)
            else:
                coefficient = float(sig_digits[0] + '.' + sig_digits[1:])

        # MALRULE: Use total zero count as exponent magnitude
        exponent = total_zeros

        # Determine sign (student might get this right or wrong)
        if is_decimal:
            exponent = -total_zeros

        # Format the answer
        result = f"{coefficient} x 10^{exponent}"

        context = {
            'number_str': number_str,
            'total_zeros': total_zeros,
            'coefficient': coefficient,
            'exponent': exponent,
            'is_decimal': is_decimal,
            'result': result
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, context)
        else:
            steps = self._generate_concise_steps(problem, context)

        return Solution(
            answer=str(result),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
