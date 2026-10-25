"""
Correct subtraction algorithm.

Implements the standard algorithm for multi-digit subtraction with borrowing,
including proper handling of cases where the minuend has fewer digits than
the subtrahend (resulting in negative numbers).

Research: Brown & Burton (1978) "Diagnostic Models for Procedural Bugs"
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class SubtractionCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for multi-digit subtraction with borrowing/regrouping.

    This implementation correctly handles:
    1. Standard subtraction with borrowing
    2. Cases where minuend < subtrahend (negative results)
    3. Proper treatment of implicit zeros in shorter numbers
    """

    def get_name(self) -> str:
        return "Correct Subtraction Algorithm"

    def get_description(self) -> str:
        return (
            "The standard algorithm for multi-digit subtraction. When a digit "
            "in the subtrahend is larger than the corresponding digit in the "
            "minuend, we borrow 1 from the next column to the left (decrementing "
            "that digit) and add 10 to the current column. If the minuend has "
            "fewer digits than the subtrahend, the result will be negative. "
            "This algorithm correctly handles implicit zeros in shorter numbers."
        )

    def _generate_concise_steps_for_subtraction(self, minuend: int, subtrahend: int) -> List[str]:
        """
        Generate concise steps for a single subtraction operation.

        Args:
            minuend: The number being subtracted from
            subtrahend: The number being subtracted

        Returns:
            List of concise step strings
        """
        steps = []

        # Handle case where result is negative
        if minuend < subtrahend:
            steps.append(f"Since {minuend} < {subtrahend}, result is negative")
            steps.append(f"Calculate {subtrahend} - {minuend} and negate")
            result = minuend - subtrahend
            steps.append(f"Result: {result}")
            return steps

        # Convert to digit lists (rightmost digit first for easier processing)
        minuend_digits = [int(d) for d in str(minuend)][::-1]
        subtrahend_digits = [int(d) for d in str(subtrahend)][::-1]

        # Pad subtrahend with zeros if needed
        while len(subtrahend_digits) < len(minuend_digits):
            subtrahend_digits.append(0)

        place_names = ['ones', 'tens', 'hundreds', 'thousands']

        # Process each column
        for i in range(len(minuend_digits)):
            top_digit = minuend_digits[i]
            bottom_digit = subtrahend_digits[i]
            place_name = place_names[i] if i < len(place_names) else f'10^{i}'

            if top_digit < bottom_digit:
                borrowed_top = top_digit + 10
                if i + 1 < len(minuend_digits):
                    minuend_digits[i + 1] -= 1
                result = borrowed_top - bottom_digit
                steps.append(f"{place_name.capitalize()}: {borrowed_top} - {bottom_digit} = {result} (borrowed)")
            else:
                result = top_digit - bottom_digit
                steps.append(f"{place_name.capitalize()}: {top_digit} - {bottom_digit} = {result}")

        return steps

    def _generate_verbose_steps_for_subtraction(self, minuend: int, subtrahend: int) -> List[str]:
        """
        Generate verbose steps for a single subtraction operation.

        Args:
            minuend: The number being subtracted from
            subtrahend: The number being subtracted

        Returns:
            List of verbose step strings
        """
        steps = []

        # Handle case where result is negative
        if minuend < subtrahend:
            steps.append(f"Comparing: {minuend} vs {subtrahend}")
            steps.append(f"Since {minuend} < {subtrahend}, the result will be negative")
            steps.append(f"To find the magnitude, calculate {subtrahend} - {minuend}")
            magnitude = subtrahend - minuend
            steps.append(f"Magnitude: {magnitude}")
            steps.append(f"Final result: -{magnitude}")
            return steps

        # Convert to digit lists (rightmost digit first for easier processing)
        minuend_digits = [int(d) for d in str(minuend)][::-1]
        subtrahend_digits = [int(d) for d in str(subtrahend)][::-1]

        # Pad subtrahend with zeros if needed
        while len(subtrahend_digits) < len(minuend_digits):
            subtrahend_digits.append(0)

        place_names = ['ones', 'tens', 'hundreds', 'thousands']
        next_place_names = ['tens', 'hundreds', 'thousands', 'ten-thousands']

        # Process each column
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

        return steps

    def _generate_concise_steps(self, problem: Problem, answer: int) -> List[str]:
        """
        Generate concise steps showing only formulas and values.

        Args:
            problem: The problem instance
            answer: The computed answer

        Returns:
            List of concise step strings
        """
        steps = []

        # Add question
        steps.append(f"Question: {problem.text}")

        minuend, subtrahend = problem.operands[:2]

        # Add column-by-column steps
        steps.extend(self._generate_concise_steps_for_subtraction(minuend, subtrahend))

        # Add answer
        steps.append(f"Answer: {answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, answer: int) -> List[str]:
        """
        Generate verbose steps with full explanations.

        Args:
            problem: The problem instance
            answer: The computed answer

        Returns:
            List of verbose step strings
        """
        steps = []
        minuend, subtrahend = problem.operands[:2]

        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD:")
        steps.append(f"Subtracting {subtrahend} from {minuend}")
        steps.append("")

        steps.extend(self._generate_verbose_steps_for_subtraction(minuend, subtrahend))

        steps.append("")
        steps.append(f"Final answer: {answer}")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct subtraction algorithm.

        Args:
            problem: Subtraction problem to solve
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with correct answer
        """
        # Check metadata first
        if 'correct_answer' in problem.metadata:
            answer = int(problem.metadata['correct_answer'])
        else:
            minuend, subtrahend = problem.operands[:2]
            answer = minuend - subtrahend

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, answer)
        else:
            steps = self._generate_concise_steps(problem, answer)

        return Solution(
            answer=str(answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
