"""
Correct subtraction algorithm.

Implements the standard algorithm for multi-digit subtraction with borrowing.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class SubtractionCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for multi-digit subtraction with borrowing/regrouping.
    """

    def get_name(self) -> str:
        return "Correct Subtraction Algorithm"

    def get_description(self) -> str:
        return (
            "The standard algorithm for multi-digit subtraction. When a digit "
            "in the subtrahend is larger than the corresponding digit in the "
            "minuend, we borrow 1 from the next column to the left (decrementing "
            "that digit) and add 10 to the current column. This process is "
            "repeated as needed across all columns."
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
                steps.append(f"{place_name.capitalize()}: {borrowed_top} - {bottom_digit} = {result}")
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

        formula_type = problem.metadata.get('formula_type', 'result_unknown')

        # Handle multi-step problems
        if formula_type == 'multi_step' and len(problem.operands) == 3:
            minuend, subtrahend1, subtrahend2 = problem.operands
            steps.append(f"Formula: {minuend} - {subtrahend1} - {subtrahend2}")

            # First subtraction
            intermediate = minuend - subtrahend1
            steps.append(f"Step 1: {minuend} - {subtrahend1} = {intermediate}")
            # Second subtraction
            steps.append(f"Step 2: {intermediate} - {subtrahend2} = {answer}")
        else:
            minuend, subtrahend = problem.operands[:2]

            # Add formula extraction for word problems
            template = problem.metadata.get('template', '')
            if 'word' in template.lower():
                steps.append(f"Formula: {minuend} - {subtrahend}")

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
        formula_type = problem.metadata.get('formula_type', 'result_unknown')

        # Handle multi-step problems
        if formula_type == 'multi_step' and len(problem.operands) == 3:
            minuend, subtrahend1, subtrahend2 = problem.operands
            steps.append(f"Solving multi-step: {minuend} - {subtrahend1} - {subtrahend2}")

            # First subtraction with detailed steps
            steps.extend(self._generate_verbose_steps_for_subtraction(minuend, subtrahend1))
            intermediate = minuend - subtrahend1
            steps.append(f"After first subtraction: {intermediate}")

            # Second subtraction with detailed steps
            steps.extend(self._generate_verbose_steps_for_subtraction(intermediate, subtrahend2))
            steps.append(f"Final answer: {answer}")
        else:
            minuend, subtrahend = problem.operands[:2]
            steps.append(f"Subtracting {subtrahend} from {minuend}")
            steps.extend(self._generate_verbose_steps_for_subtraction(minuend, subtrahend))
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
        # Handle different problem types based on metadata
        formula_type = problem.metadata.get('formula_type', 'result_unknown')

        # Calculate the correct answer
        if formula_type == 'multi_step' and len(problem.operands) == 3:
            minuend, subtrahend1, subtrahend2 = problem.operands
            answer = minuend - subtrahend1 - subtrahend2
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
