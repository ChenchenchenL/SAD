"""
Malrule algorithm for Always-Borrow-Left error.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class AlwaysBorrowLeftMalrule(Malrule):
    """
    Students always borrow from immediate left column, even when not needed.

    Example: 85 - 23 → Student borrows unnecessarily
    """

    def get_name(self) -> str:
        return "Always-Borrow-Left"

    def get_description(self) -> str:
        return (
            "Students always borrow from the left column in subtraction, even when the "
            "top digit is greater than or equal to the bottom digit and borrowing is not "
            "needed. This represents an overgeneralization of the borrowing procedure, "
            "documented in the BUGGY diagnostic system (Brown & Burton, 1978) and further "
            "analyzed in VanLehn's (1990) repair theory research."
        )

    def calculate_expected_answer(self, problem: Problem) -> int:
        """
        Calculate the expected incorrect answer for this malrule.

        For Always-Borrow-Left:
        - Student ALWAYS borrows from left column for EVERY column (except leftmost)
        - Even if top digit >= bottom digit, student still borrows
        - When subtraction result is >= 10, student writes only the ones digit

        Example: 85 - 23
        - Ones: Student borrows (5+10) - 3 = 12, writes 2 (even though 5 >= 3!)
        - Tens: (8-1) - 2 = 5
        - Result: 52 (WRONG! Should be 62)

        Example: 987 - 543
        - Ones: Student borrows (7+10) - 3 = 14, writes 4, tens becomes 7
        - Tens: Student borrows (7+10) - 4 = 13, writes 3, hundreds becomes 8
        - Hundreds: 8 - 5 = 3
        - Result: 334 (WRONG! Should be 444)

        Args:
            problem: Subtraction problem

        Returns:
            Expected incorrect answer as integer
        """
        # Extract operands from problem
        minuend, subtrahend = problem.operands[:2]

        # Single digit - just subtract normally (no column to borrow from)
        if minuend < 10:
            return minuend - subtrahend

        # Get digits (rightmost first for easier column-by-column processing)
        min_digits = [int(d) for d in str(minuend)][::-1]
        sub_digits = [int(d) for d in str(subtrahend).zfill(len(str(minuend)))][::-1]

        result_digits = []

        # Process each column from right to left
        for i in range(len(min_digits)):
            if i < len(min_digits) - 1:
                # Not the leftmost column: ALWAYS borrow from left (malrule)
                borrowed_top = min_digits[i] + 10
                min_digits[i + 1] -= 1  # Decrement the column to the left

                diff = borrowed_top - sub_digits[i]
                # Take only the ones digit of the result
                result_digits.append(diff % 10)
            else:
                # Leftmost column: just subtract (no column to borrow from)
                diff = min_digits[i] - sub_digits[i]
                # Handle negative result (student might write 0 or get confused)
                if diff < 0:
                    diff = 0
                result_digits.append(diff)

        # Convert back to number (result_digits is in reverse order: ones, tens, ...)
        answer = 0
        for i, digit in enumerate(result_digits):
            answer += digit * (10 ** i)

        return answer

    def _generate_concise_steps(self, problem: Problem, minuend: int, subtrahend: int, malrule_answer: int) -> List[str]:
        """
        Generate concise steps showing only formulas and values.

        Args:
            problem: The problem instance
            minuend: The number being subtracted from
            subtrahend: The number being subtracted
            malrule_answer: The computed malrule answer

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

        # Get digits (rightmost first for processing)
        min_digits = [int(d) for d in str(minuend)][::-1]
        sub_digits = [int(d) for d in str(subtrahend).zfill(len(str(minuend)))][::-1]

        place_names = ['ones', 'tens', 'hundreds', 'thousands', 'ten-thousands']
        working_digits = min_digits.copy()

        # Process each column from right to left
        for i in range(len(min_digits)):
            place_name = place_names[i] if i < len(place_names) else f'10^{i}'

            if i < len(min_digits) - 1:
                # Not the leftmost column: ALWAYS borrow (malrule)
                original_top = working_digits[i]
                borrowed_top = original_top + 10
                working_digits[i + 1] -= 1

                diff = borrowed_top - sub_digits[i]
                result_digit = diff % 10

                steps.append(f"{place_name.capitalize()}: {borrowed_top} - {sub_digits[i]} = {diff}, write {result_digit}")
            else:
                # Leftmost column: just subtract (no column to borrow from)
                diff = working_digits[i] - sub_digits[i]
                if diff < 0:
                    diff = 0
                steps.append(f"{place_name.capitalize()}: {working_digits[i]} - {sub_digits[i]} = {diff}")

        # Add answer
        steps.append(f"Answer: {malrule_answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, minuend: int, subtrahend: int, malrule_answer: int, correct_answer: int) -> List[str]:
        """
        Generate verbose steps with full explanations.

        Args:
            problem: The problem instance
            minuend: The number being subtracted from
            subtrahend: The number being subtracted
            malrule_answer: The computed malrule answer
            correct_answer: The correct answer

        Returns:
            List of verbose step strings
        """
        steps = []
        steps.append(f"Problem: {minuend} - {subtrahend}")
        steps.append("")
        steps.append("MALRULE: Always borrow from left column for EVERY column")
        steps.append("  MALRULE REASONING: 'You always need to borrow in subtraction'")
        steps.append("")

        # Get digits (rightmost first for processing)
        min_digits = [int(d) for d in str(minuend)][::-1]
        sub_digits = [int(d) for d in str(subtrahend).zfill(len(str(minuend)))][::-1]

        place_names = ['ones', 'tens', 'hundreds', 'thousands', 'ten-thousands']
        working_digits = min_digits.copy()

        # Process each column from right to left
        for i in range(len(min_digits)):
            place_name = place_names[i] if i < len(place_names) else f'10^{i}'
            next_place = place_names[i + 1] if i + 1 < len(place_names) else f'10^{i+1}'

            if i < len(min_digits) - 1:
                # Not the leftmost column: ALWAYS borrow (malrule)
                original_top = working_digits[i]
                borrowed_top = original_top + 10
                working_digits[i + 1] -= 1

                diff = borrowed_top - sub_digits[i]
                result_digit = diff % 10

                steps.append(f"{place_name.capitalize()} place: {original_top} - {sub_digits[i]}")
                steps.append(f"  Borrow from {next_place} (even though {original_top} {'<' if original_top < sub_digits[i] else '>='} {sub_digits[i]}!)")
                steps.append(f"  {next_place.capitalize()}: {working_digits[i + 1] + 1} becomes {working_digits[i + 1]}")
                steps.append(f"  {place_name.capitalize()}: {original_top} becomes {borrowed_top}")
                steps.append(f"  {borrowed_top} - {sub_digits[i]} = {diff}, write {result_digit}")
                steps.append("")
            else:
                # Leftmost column: just subtract (no column to borrow from)
                diff = working_digits[i] - sub_digits[i]
                if diff < 0:
                    diff = 0
                steps.append(f"{place_name.capitalize()} place: {working_digits[i]} - {sub_digits[i]} = {diff}")
                steps.append("")

        steps.append(f"Final Answer: {malrule_answer} (INCORRECT - should be {correct_answer})")
        steps.append(f"  Borrowed unnecessarily {len(min_digits) - 1} time(s)!")

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Always-Borrow-Left malrule.

        Args:
            problem: Problem instance to solve
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with malrule answer and steps
        """
        # Extract operands from problem
        minuend, subtrahend = problem.operands[:2]
        malrule_answer = self.calculate_expected_answer(problem)
        correct_answer = minuend - subtrahend

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, minuend, subtrahend, malrule_answer, correct_answer)
        else:
            steps = self._generate_concise_steps(problem, minuend, subtrahend, malrule_answer)

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
