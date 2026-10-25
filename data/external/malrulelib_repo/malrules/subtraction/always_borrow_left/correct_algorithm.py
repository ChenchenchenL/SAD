"""
Correct algorithm for subtraction.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class SubtractionCorrectAlgorithm(CorrectAlgorithm):
    """Correctly performs subtraction with borrowing only when needed."""

    def get_name(self) -> str:
        return "Correct Subtraction"

    def get_description(self) -> str:
        return "Correctly performs subtraction, borrowing only when top digit < bottom digit."

    def _generate_concise_steps(self, problem: Problem, minuend: int, subtrahend: int, answer: int) -> List[str]:
        """
        Generate concise steps showing only formulas and values.

        Args:
            problem: The problem instance
            minuend: The number being subtracted from
            subtrahend: The number being subtracted
            answer: The computed answer

        Returns:
            List of concise step strings
        """
        steps = []

        # Add question
        steps.append(f"Question: {problem.text}")

        # Add formula extraction for word problems
        template = problem.metadata.get('template', '')
        if template == 'word_problem' or 'word' in template.lower():
            steps.append(f"Formula: {minuend} - {subtrahend}")

        # Convert to digit lists (rightmost digit first for easier processing)
        minuend_digits = [int(d) for d in str(minuend)][::-1]
        subtrahend_digits = [int(d) for d in str(subtrahend)][::-1]

        # Pad subtrahend with zeros if needed
        while len(subtrahend_digits) < len(minuend_digits):
            subtrahend_digits.append(0)

        place_names = ['ones', 'tens', 'hundreds', 'thousands']

        # Process each column from right to left
        for i in range(len(minuend_digits)):
            top_digit = minuend_digits[i]
            bottom_digit = subtrahend_digits[i]
            place_name = place_names[i] if i < len(place_names) else f'10^{i}'

            if top_digit < bottom_digit:
                borrowed_top = top_digit + 10
                if i + 1 < len(minuend_digits):
                    minuend_digits[i + 1] -= 1
                result = borrowed_top - bottom_digit
                steps.append(f"{place_name.capitalize()}: {borrowed_top} - {bottom_digit} = {result}")
            else:
                result = top_digit - bottom_digit
                steps.append(f"{place_name.capitalize()}: {top_digit} - {bottom_digit} = {result}")

        # Add answer
        steps.append(f"Answer: {answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, minuend: int, subtrahend: int, answer: int) -> List[str]:
        """
        Generate verbose steps with full explanations.

        Args:
            problem: The problem instance
            minuend: The number being subtracted from
            subtrahend: The number being subtracted
            answer: The computed answer

        Returns:
            List of verbose step strings
        """
        steps = []
        steps.append(f"Problem: {minuend} - {subtrahend}")
        steps.append("")
        steps.append("Rule: Only borrow when top digit < bottom digit")
        steps.append("")

        # Convert to digit lists (rightmost digit first for easier processing)
        minuend_digits = [int(d) for d in str(minuend)][::-1]
        subtrahend_digits = [int(d) for d in str(subtrahend)][::-1]

        # Pad subtrahend with zeros if needed
        while len(subtrahend_digits) < len(minuend_digits):
            subtrahend_digits.append(0)

        place_names = ['ones', 'tens', 'hundreds', 'thousands']
        next_place_names = ['tens', 'hundreds', 'thousands', 'ten-thousands']

        # Process each column from right to left
        for i in range(len(minuend_digits)):
            top_digit = minuend_digits[i]
            bottom_digit = subtrahend_digits[i]
            place_name = place_names[i] if i < len(place_names) else f'10^{i}'

            if top_digit < bottom_digit:
                borrowed_top = top_digit + 10
                steps.append(
                    f"{place_name.capitalize()} place: {top_digit} < {bottom_digit}, "
                    f"so borrow from the next column"
                )
                if i + 1 < len(minuend_digits):
                    minuend_digits[i + 1] -= 1
                    next_place = next_place_names[i] if i < len(next_place_names) else f'10^{i+1}'
                    steps.append(
                        f"Borrowed from {next_place} place, reducing it by 1"
                    )
                result = borrowed_top - bottom_digit
                steps.append(
                    f"{place_name.capitalize()} place: {borrowed_top} - {bottom_digit} = {result}"
                )
            else:
                result = top_digit - bottom_digit
                steps.append(
                    f"{place_name.capitalize()} place: {top_digit} - {bottom_digit} = {result}"
                )

        steps.append("")
        steps.append(f"Final Answer: {answer} ✓")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct subtraction algorithm.

        Args:
            problem: Problem instance to solve
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with correct answer and steps
        """
        # Extract operands from problem
        minuend, subtrahend = problem.operands[:2]

        # Calculate answer
        # Convert to digit lists (rightmost digit first for easier processing)
        minuend_digits = [int(d) for d in str(minuend)][::-1]
        subtrahend_digits = [int(d) for d in str(subtrahend)][::-1]

        # Pad subtrahend with zeros if needed
        while len(subtrahend_digits) < len(minuend_digits):
            subtrahend_digits.append(0)

        result_digits = []

        # Process each column from right to left
        for i in range(len(minuend_digits)):
            top_digit = minuend_digits[i]
            bottom_digit = subtrahend_digits[i]

            if top_digit < bottom_digit:
                borrowed_top = top_digit + 10
                if i + 1 < len(minuend_digits):
                    minuend_digits[i + 1] -= 1
                result = borrowed_top - bottom_digit
                result_digits.append(result)
            else:
                result = top_digit - bottom_digit
                result_digits.append(result)

        # Convert result digits back to number
        while len(result_digits) > 1 and result_digits[-1] == 0:
            result_digits.pop()

        answer = int(''.join(str(d) for d in result_digits[::-1]))

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, minuend, subtrahend, answer)
        else:
            steps = self._generate_concise_steps(problem, minuend, subtrahend, answer)

        return Solution(
            answer=str(answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
