"""
Correct algorithm for subtraction with proper borrowing.

Implements the standard algorithm for multi-digit subtraction,
correctly handling borrowing when the minuend digit is smaller
than the subtrahend digit (including when minuend digit is 0).

Research: Brown & Burton (1978) - Diagnostic models for procedural bugs
in basic mathematical skills. Cognitive Science, 2(2), 155-192.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class SubtractionCorrectAlgorithm(CorrectAlgorithm):
    """
    Implements correct subtraction with proper handling of borrowing.

    This is the standard algorithm that correctly borrows from left
    positions when needed, including when the current position is zero.
    """

    def get_name(self) -> str:
        return "Standard Subtraction with Borrowing"

    def get_description(self) -> str:
        return (
            "The standard algorithm for multi-digit subtraction. When a digit "
            "in the subtrahend is larger than the corresponding digit in the "
            "minuend (including when minuend digit is 0), we borrow 1 from the "
            "next column to the left (decrementing that digit) and add 10 to "
            "the current column. This process is repeated as needed across all "
            "columns, cascading through zeros if necessary."
        )

    def _generate_concise_steps(self, problem: Problem, minuend: int, subtrahend: int,
                                 result: int, minuend_str: str, subtrahend_str: str) -> List[str]:
        """Generate concise steps with only formulas and values."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: {minuend} - {subtrahend}")

        # Convert to digit arrays for step-by-step calculation
        minuend_digits = [int(d) for d in minuend_str]
        subtrahend_digits = [int(d) for d in subtrahend_str]
        working_minuend = minuend_digits[:]
        result_digits = []

        place_names = ['ones', 'tens', 'hundreds', 'thousands', 'ten-thousands']

        for i in range(len(working_minuend) - 1, -1, -1):
            place_idx = len(working_minuend) - 1 - i
            place_name = place_names[place_idx] if place_idx < len(place_names) else f'10^{place_idx}'

            if working_minuend[i] < subtrahend_digits[i]:
                # Need to borrow
                borrow_from = i - 1
                while borrow_from >= 0 and working_minuend[borrow_from] == 0:
                    borrow_from -= 1

                if borrow_from >= 0:
                    working_minuend[borrow_from] -= 1
                    for pos in range(borrow_from + 1, i):
                        if working_minuend[pos] == 0:
                            working_minuend[pos] = 9
                    working_minuend[i] += 10

            digit_result = working_minuend[i] - subtrahend_digits[i]
            result_digits.insert(0, digit_result)
            steps.append(f"{place_name.capitalize()}: {working_minuend[i]} - {subtrahend_digits[i]} = {digit_result}")

        steps.append(f"Answer: {result}")
        return steps

    def _generate_verbose_steps(self, problem: Problem, minuend: int, subtrahend: int,
                                 result: int, minuend_str: str, subtrahend_str: str) -> List[str]:
        """Generate verbose steps with detailed explanations."""
        steps = []
        steps.append(f"Problem: {minuend} - {subtrahend}")
        steps.append("")
        steps.append("CORRECT METHOD: Standard borrowing algorithm")
        steps.append("")
        steps.append(f"  {minuend_str}")
        steps.append(f"- {subtrahend_str}")
        steps.append(f"  {'-' * len(minuend_str)}")

        # Convert to digit arrays
        minuend_digits = [int(d) for d in minuend_str]
        subtrahend_digits = [int(d) for d in subtrahend_str]

        # Perform subtraction with borrowing
        result_digits = []
        working_minuend = minuend_digits[:]

        place_names = ['ones', 'tens', 'hundreds', 'thousands', 'ten-thousands']

        for i in range(len(working_minuend) - 1, -1, -1):
            place_idx = len(working_minuend) - 1 - i
            place_name = place_names[place_idx] if place_idx < len(place_names) else f'10^{place_idx}'

            if working_minuend[i] < subtrahend_digits[i]:
                # Need to borrow
                steps.append("")
                steps.append(f"{place_name.capitalize()} place: {working_minuend[i]} < {subtrahend_digits[i]}, need to borrow")

                # Find position to borrow from (cascade through zeros)
                borrow_from = i - 1
                positions_borrowed_through = []

                while borrow_from >= 0 and working_minuend[borrow_from] == 0:
                    positions_borrowed_through.append(borrow_from)
                    borrow_from -= 1

                if borrow_from >= 0:
                    # Execute the cascade
                    working_minuend[borrow_from] -= 1
                    borrow_place_idx = len(working_minuend) - 1 - borrow_from
                    borrow_place = place_names[borrow_place_idx] if borrow_place_idx < len(place_names) else f'10^{borrow_place_idx}'
                    steps.append(f"  Borrow from {borrow_place}: {working_minuend[borrow_from] + 1} -> {working_minuend[borrow_from]}")

                    # Convert all zeros in between to 9
                    for pos in positions_borrowed_through:
                        working_minuend[pos] = 9
                        pos_place_idx = len(working_minuend) - 1 - pos
                        pos_place = place_names[pos_place_idx] if pos_place_idx < len(place_names) else f'10^{pos_place_idx}'
                        steps.append(f"  {pos_place.capitalize()}: 0 -> 9 (borrowed through)")

                    # Add 10 to current position
                    working_minuend[i] += 10
                    steps.append(f"  {place_name.capitalize()}: {working_minuend[i] - 10} -> {working_minuend[i]}")

            # Perform subtraction at this position
            digit_result = working_minuend[i] - subtrahend_digits[i]
            result_digits.insert(0, digit_result)

            if working_minuend[i] != minuend_digits[i] or subtrahend_digits[i] != 0:
                steps.append(f"  {working_minuend[i]} - {subtrahend_digits[i]} = {digit_result}")

        steps.append("")
        steps.append(f"Result: {result}")
        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply standard subtraction with proper borrowing.

        Args:
            problem: Problem instance with minuend and subtrahend
            verbose: If True, generate detailed steps; if False, generate concise steps

        Returns:
            Solution with correct answer and detailed steps
        """
        # Extract operands from problem
        minuend, subtrahend = problem.operands[:2]

        # Convert to digit arrays
        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend).zfill(len(minuend_str))

        # Calculate result
        result = minuend - subtrahend

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, minuend, subtrahend, result,
                                                  minuend_str, subtrahend_str)
        else:
            steps = self._generate_concise_steps(problem, minuend, subtrahend, result,
                                                  minuend_str, subtrahend_str)

        return Solution(
            answer=str(result),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
