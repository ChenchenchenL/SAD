"""
Malrule algorithm for Wrong-Exponent-Sign error.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class WrongExponentSignMalrule(Malrule):
    """
    Students use wrong sign for exponent in scientific notation.

    Example: Convert 0.0045 to scientific notation
    Student: "4.5 x 10^3" (positive instead of negative!)
    Correct: "4.5 x 10^-3"
    """

    def get_name(self) -> str:
        return "Wrong-Exponent-Sign"

    def get_description(self) -> str:
        return (
            "Students use the wrong sign for the exponent when converting numbers to "
            "scientific notation. This reflects a persistent error pattern where students "
            "incorrectly interpret negative signs in exponential expressions. Research shows "
            "that errors involving the negative sign are among the most common and persistent "
            "in algebraic problem solving, often surpassing errors with fractions or basic "
            "arithmetic (Booth et al., 2014; Cangelosi et al., 2013)."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        solution = self._apply_malrule(problem)
        return solution.answer

    def _generate_verbose_steps(self, problem: Problem, context: dict) -> list:
        """Generate verbose steps with full explanations."""
        steps = []
        number_str = context['number_str']
        decimal_number = context['decimal_number']
        mantissa = context['mantissa']
        correct_exponent = context['correct_exponent']
        malrule_exponent = context['malrule_exponent']

        steps.append(f"Problem: Write {number_str} in scientific notation")
        steps.append("")
        steps.append("MALRULE: Wrong sign for exponent")
        steps.append("")
        steps.append(f"  MALRULE REASONING: 'Count decimal places moved: {abs(correct_exponent)}'")
        steps.append(f"                     'But use wrong sign!'")
        steps.append("")
        steps.append(f"Step 1: Convert to form a.bc... x 10^n")
        steps.append(f"  {number_str} -> {mantissa}")
        steps.append(f"  Decimal moved {abs(correct_exponent)} places")
        steps.append("")
        steps.append(f"Step 2: Apply malrule - use WRONG sign for exponent")

        if abs(decimal_number) < 1 and decimal_number != 0:
            steps.append(f"  Number is small (< 1), so decimal moved RIGHT")
            steps.append(f"  Should be NEGATIVE exponent, but student uses POSITIVE")
            steps.append(f"  Wrong exponent: {malrule_exponent}")
        elif abs(decimal_number) >= 10:
            steps.append(f"  Number is large (> 10), so decimal moved LEFT")
            steps.append(f"  Should be POSITIVE exponent, but student uses NEGATIVE")
            steps.append(f"  Wrong exponent: {malrule_exponent}")
        else:
            steps.append(f"  Number already between 1 and 10")
            steps.append(f"  Student might still make a sign error")

        steps.append("")
        steps.append(f"Final Answer: {mantissa} x 10^{malrule_exponent} (INCORRECT - wrong sign!)")
        steps.append(f"  Should be: {mantissa} x 10^{correct_exponent}")
        return steps

    def _generate_concise_steps(self, problem: Problem, context: dict) -> list:
        """Generate concise steps with only formulas and values."""
        steps = []
        number_str = context['number_str']
        decimal_number = context['decimal_number']
        mantissa = context['mantissa']
        correct_exponent = context['correct_exponent']
        malrule_exponent = context['malrule_exponent']
        is_word_problem = problem.metadata.get('is_word_problem', False)

        # Add question
        steps.append(problem.text)

        # Add formula extraction for word problems
        if is_word_problem:
            steps.append(f"{number_str}")

        # Add calculation steps
        steps.append(f"{number_str} -> {mantissa}")
        steps.append(f"Decimal moved {abs(correct_exponent)} places")
        # steps.append(f"Wrong sign: {malrule_exponent}")

        # Add answer
        steps.append(f"{mantissa} x 10^{malrule_exponent}")
        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Wrong-Exponent-Sign malrule.

        Uses the wrong sign for the exponent when converting to scientific notation.

        Args:
            problem: Scientific notation conversion problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with malrule (incorrect) answer
        """
        # Parse the input from metadata
        number_str = problem.metadata['number_str']
        decimal_number = problem.metadata['decimal_number']

        # First, compute the CORRECT mantissa and exponent
        if decimal_number == 0:
            mantissa = 0
            correct_exponent = 0
            malrule_exponent = 0
        elif abs(decimal_number) >= 1:
            # Large number: move decimal left (should be positive exponent)
            mantissa = abs(decimal_number)
            correct_exponent = 0
            while mantissa >= 10:
                mantissa /= 10
                correct_exponent += 1
            if decimal_number < 0:
                mantissa = -mantissa
            # MALRULE: Use wrong sign
            malrule_exponent = -correct_exponent
        else:
            # Small number: move decimal right (should be negative exponent)
            mantissa = abs(decimal_number)
            correct_exponent = 0
            while mantissa < 1:
                mantissa *= 10
                correct_exponent -= 1
            if decimal_number < 0:
                mantissa = -mantissa
            # MALRULE: Use wrong sign (flip the negative to positive)
            malrule_exponent = -correct_exponent

        context = {
            'number_str': number_str,
            'decimal_number': decimal_number,
            'mantissa': mantissa,
            'correct_exponent': correct_exponent,
            'malrule_exponent': malrule_exponent
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, context)
        else:
            steps = self._generate_concise_steps(problem, context)

        return Solution(
            answer=malrule_exponent,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
