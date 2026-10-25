"""
Correct scientific notation conversion algorithm.

Implements the standard algorithm for converting numbers to scientific
notation by counting decimal places moved, not zeros.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import CorrectAlgorithm, Problem, Solution


class ScientificNotationCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for scientific notation conversion.

    Converts numbers to scientific notation by moving the decimal point
    to create a coefficient between 1 and 10, then counting how many
    places the decimal moved (this becomes the exponent).
    """

    def get_name(self) -> str:
        return "Correct Scientific Notation Conversion"

    def get_description(self) -> str:
        return (
            "The standard algorithm for converting to scientific notation. "
            "Move the decimal point to create a coefficient between 1 and 10, "
            "count the number of places moved (this is the exponent magnitude), "
            "and use positive exponent for large numbers, negative for small decimals."
        )

    def _generate_verbose_steps(self, problem: Problem, context: dict) -> list:
        """Generate verbose steps with full explanations."""
        steps = []
        number_str = context['number_str']
        number = context['number']
        coefficient_str = context['coefficient_str']
        exponent = context['exponent']
        result = context['result']

        steps.append(f"Converting {number_str} to scientific notation")
        steps.append("Step 1: Find the first non-zero digit")

        if number == 0:
            steps.append("Number is 0, which is 0 × 10^0")
        elif number >= 10:
            steps.append(f"Number is >= 10, so we move decimal point LEFT")
            steps.append(f"Moving decimal {exponent} places left: {number_str} -> {coefficient_str}")
            steps.append(f"Exponent is +{exponent} (moved left = positive)")
        elif number >= 1:
            steps.append(f"Number is already between 1 and 10")
            steps.append(f"Coefficient: {coefficient_str}, exponent: 0")
        else:
            steps.append(f"Number is < 1, so we move decimal point RIGHT")
            steps.append(f"Moving decimal {abs(exponent)} places right: {number_str} -> {coefficient_str}")
            steps.append(f"Exponent is {exponent} (moved right = negative)")

        steps.append(f"Scientific notation: {result}")

        # Verification
        verification_value = float(coefficient_str) * (10 ** exponent)
        steps.append(f"Verification: {coefficient_str} x 10^{exponent} = {verification_value}")
        if abs(verification_value - number) < 1e-10:
            steps.append(f"Matches original number {number_str}")

        steps.append(f"Final answer: {result}")
        return steps

    def _generate_concise_steps(self, problem: Problem, context: dict) -> list:
        """Generate concise steps with only formulas and values."""
        steps = []
        number_str = context['number_str']
        number = context['number']
        coefficient_str = context['coefficient_str']
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
        if number == 0:
            steps.append("0 = 0 x 10^0")
        elif number >= 10:
            steps.append(f"{number_str} -> {coefficient_str}")
            steps.append(f"Decimal moved {exponent} places left")
        elif number >= 1:
            steps.append(f"{number_str} = {coefficient_str} x 10^0")
        else:
            steps.append(f"{number_str} -> {coefficient_str}")
            steps.append(f"Decimal moved {abs(exponent)} places right")

        # Add answer
        steps.append(result)
        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct scientific notation conversion.

        Args:
            problem: Scientific notation conversion problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with correct conversion
        """
        # Compute the correct answer from the number string
        number_str = problem.operands[0]

        # Convert to float for calculation
        number = float(number_str)

        if number == 0:
            context = {
                'number_str': number_str,
                'number': number,
                'coefficient_str': '0',
                'exponent': 0,
                'result': '0 x 10^0'
            }
            if verbose:
                steps = self._generate_verbose_steps(problem, context)
            else:
                steps = self._generate_concise_steps(problem, context)
            return Solution(
                answer="0 x 10^0",
                steps=steps,
                is_correct=True,
                algorithm_name=self.get_name()
            )

        # Determine exponent by counting decimal places to move
        if number >= 10:
            # Large number: count moves left
            exponent = 0
            temp = number
            while temp >= 10:
                temp /= 10
                exponent += 1
            coefficient = number / (10 ** exponent)
        elif number >= 1:
            # Already in range [1, 10)
            exponent = 0
            coefficient = number
        else:  # number < 1
            # Small decimal: count moves right
            exponent = 0
            temp = number
            while temp < 1:
                temp *= 10
                exponent += 1
            coefficient = number * (10 ** exponent)
            exponent = -exponent

        # Format coefficient nicely (remove trailing zeros if appropriate)
        if coefficient == int(coefficient):
            coefficient_str = str(int(coefficient))
        else:
            coefficient_str = f"{coefficient:.10g}"

        # Create result
        result = f"{coefficient_str} x 10^{exponent}"

        context = {
            'number_str': number_str,
            'number': number,
            'coefficient_str': coefficient_str,
            'exponent': exponent,
            'result': result
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, context)
        else:
            steps = self._generate_concise_steps(problem, context)

        return Solution(
            answer=str(result),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
