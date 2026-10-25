"""
Smaller-From-Larger malrule algorithm.

Implements the systematic error where students always subtract the smaller
digit from the larger digit, regardless of position (top or bottom).
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List

class SmallerFromLargerMalrule(Malrule):
    """
    Implements the Smaller-From-Larger bug.

    Students always subtract the smaller digit from the larger digit in each column,
    regardless of which number (minuend or subtrahend) contains the larger digit.
    They don't use borrowing because they simply avoid having to subtract a larger
    number from a smaller one by reversing the operation when needed.
    """

    def get_name(self) -> str:
        return "Smaller-From-Larger"

    def get_description(self) -> str:
        return (
            "A systematic procedural bug where the student always subtracts the smaller "
            "digit from the larger digit in each column, regardless of position (minuend "
            "or subtrahend). This error avoids borrowing by reversing the subtraction "
            "when the top digit is smaller than the bottom digit. For example, in 62 - 37, "
            "the student computes 7-2=5 in the ones column (instead of borrowing) and "
            "6-3=3 in the tens column, yielding 35 instead of the correct answer 25. "
            "This is one of the most extensively documented subtraction bugs in cognitive "
            "science research, identified through the BUGGY and DEBUGGY diagnostic systems."
        )

    def calculate_expected_answer(self, problem: Problem) -> int:
        """
        Calculate the expected incorrect answer for this malrule.

        For Smaller-From-Larger:
        - In each column, always subtract smaller digit from larger digit
        - MALRULE: Reverse operation when top < bottom (do bottom - top)
        - No borrowing is performed

        Args:
            problem: Subtraction problem

        Returns:
            Expected incorrect answer as integer
        """
        # Handle multi-step problems
        formula_type = problem.metadata.get('formula_type', 'result_unknown')
        if formula_type == 'multi_step' and len(problem.operands) == 3:
            minuend, subtrahend1, subtrahend2 = problem.operands
            # Apply malrule to first subtraction
            intermediate = self._apply_malrule_to_two_numbers(minuend, subtrahend1)
            # Apply malrule to second subtraction
            final_result = self._apply_malrule_to_two_numbers(intermediate, subtrahend2)
            return final_result

        minuend, subtrahend = problem.operands[:2]

        # Convert to digit lists (rightmost digit first for easier processing)
        minuend_digits = [int(d) for d in str(minuend)][::-1]
        subtrahend_digits = [int(d) for d in str(subtrahend)][::-1]

        # Pad subtrahend with zeros if needed
        while len(subtrahend_digits) < len(minuend_digits):
            subtrahend_digits.append(0)

        result_digits = []

        # Process each column - ALWAYS smaller from larger
        for i in range(len(minuend_digits)):
            top_digit = minuend_digits[i]
            bottom_digit = subtrahend_digits[i]

            # MALRULE: Always subtract smaller from larger
            if top_digit >= bottom_digit:
                result_digits.append(top_digit - bottom_digit)
            else:
                # REVERSE the operation (ERROR!)
                result_digits.append(bottom_digit - top_digit)

        # Convert result digits back to number
        # Remove leading zeros
        while len(result_digits) > 1 and result_digits[-1] == 0:
            result_digits.pop()

        return int(''.join(str(d) for d in result_digits[::-1]))

    def _generate_concise_steps_for_malrule(self, minuend: int, subtrahend: int) -> List[str]:
        """
        Generate concise steps for a single subtraction with malrule.

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

        # Process each column - ALWAYS smaller from larger
        for i in range(len(minuend_digits)):
            top_digit = minuend_digits[i]
            bottom_digit = subtrahend_digits[i]
            place_name = place_names[i] if i < len(place_names) else f'10^{i}'

            if top_digit >= bottom_digit:
                result = top_digit - bottom_digit
                steps.append(f"{place_name.capitalize()}: {top_digit} - {bottom_digit} = {result}")
            else:
                result = bottom_digit - top_digit
                steps.append(f"{place_name.capitalize()}: {bottom_digit} - {top_digit} = {result}")

        return steps

    def _generate_verbose_steps_for_malrule(self, minuend: int, subtrahend: int) -> List[str]:
        """
        Generate verbose steps for a single subtraction with malrule.

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

        # Process each column - ALWAYS smaller from larger
        for i in range(len(minuend_digits)):
            top_digit = minuend_digits[i]
            bottom_digit = subtrahend_digits[i]
            place_name = place_names[i] if i < len(place_names) else f'10^{i}'

            if top_digit >= bottom_digit:
                result = top_digit - bottom_digit
                steps.append(
                    f"{place_name.capitalize()} place: {top_digit} >= {bottom_digit}, "
                    f"so {top_digit} - {bottom_digit} = {result}"
                )
            else:
                result = bottom_digit - top_digit
                steps.append(
                    f"{place_name.capitalize()} place: {top_digit} < {bottom_digit}, "
                    f"so subtract smaller from larger: {bottom_digit} - {top_digit} = {result}"
                )

        return steps

    def _generate_concise_steps(self, problem: Problem, malrule_answer: int) -> List[str]:
        """
        Generate concise steps showing only formulas and values.

        Args:
            problem: The problem instance
            malrule_answer: The computed malrule answer

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

            # First subtraction with malrule
            intermediate = self._apply_malrule_to_two_numbers(minuend, subtrahend1)
            steps.append(f"Step 1: {minuend} - {subtrahend1} = {intermediate}")
            # Second subtraction with malrule
            steps.append(f"Step 2: {intermediate} - {subtrahend2} = {malrule_answer}")
        else:
            minuend, subtrahend = problem.operands[:2]

            # Add formula extraction for word problems
            template = problem.metadata.get('template', '')
            if 'word' in template.lower():
                steps.append(f"Formula: {minuend} - {subtrahend}")

            # Add column-by-column steps
            steps.extend(self._generate_concise_steps_for_malrule(minuend, subtrahend))

        # Add answer
        steps.append(f"Answer: {malrule_answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, malrule_answer: int) -> List[str]:
        """
        Generate verbose steps with full explanations.

        Args:
            problem: The problem instance
            malrule_answer: The computed malrule answer

        Returns:
            List of verbose step strings
        """
        steps = []
        formula_type = problem.metadata.get('formula_type', 'result_unknown')

        # Handle multi-step problems
        if formula_type == 'multi_step' and len(problem.operands) == 3:
            minuend, subtrahend1, subtrahend2 = problem.operands
            steps.append(f"Solving multi-step (with Smaller-From-Larger malrule): {minuend} - {subtrahend1} - {subtrahend2}")

            # First subtraction with malrule
            steps.extend(self._generate_verbose_steps_for_malrule(minuend, subtrahend1))
            intermediate = self._apply_malrule_to_two_numbers(minuend, subtrahend1)
            steps.append(f"After first subtraction: {intermediate}")

            # Second subtraction with malrule
            steps.extend(self._generate_verbose_steps_for_malrule(intermediate, subtrahend2))
            steps.append(f"Final answer: {malrule_answer} (INCORRECT due to Smaller-From-Larger)")
        else:
            minuend, subtrahend = problem.operands[:2]
            steps.append(f"Subtracting {subtrahend} from {minuend}")
            steps.extend(self._generate_verbose_steps_for_malrule(minuend, subtrahend))
            steps.append(f"Final answer: {malrule_answer} (INCORRECT due to Smaller-From-Larger)")

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Smaller-From-Larger malrule to solve the problem incorrectly.

        Args:
            problem: Subtraction problem to solve
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with incorrect answer due to Smaller-From-Larger bug
        """
        # Calculate the malrule answer
        malrule_answer = self.calculate_expected_answer(problem)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, malrule_answer)
        else:
            steps = self._generate_concise_steps(problem, malrule_answer)

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _apply_malrule_to_two_numbers(self, minuend: int, subtrahend: int) -> int:
        """
        Apply Smaller-From-Larger malrule to two numbers without detailed steps.

        Args:
            minuend: Top number
            subtrahend: Bottom number

        Returns:
            Incorrect result due to malrule
        """
        # Convert to digit lists (rightmost digit first for easier processing)
        minuend_digits = [int(d) for d in str(minuend)][::-1]
        subtrahend_digits = [int(d) for d in str(subtrahend)][::-1]

        # Pad subtrahend with zeros if needed
        while len(subtrahend_digits) < len(minuend_digits):
            subtrahend_digits.append(0)

        result_digits = []

        # Process each column - ALWAYS smaller from larger
        for i in range(len(minuend_digits)):
            top_digit = minuend_digits[i]
            bottom_digit = subtrahend_digits[i]

            # MALRULE: Always subtract smaller from larger
            if top_digit >= bottom_digit:
                result_digits.append(top_digit - bottom_digit)
            else:
                # REVERSE the operation (ERROR!)
                result_digits.append(bottom_digit - top_digit)

        # Convert result digits back to number
        # Remove leading zeros
        while len(result_digits) > 1 and result_digits[-1] == 0:
            result_digits.pop()

        return int(''.join(str(d) for d in result_digits[::-1]))

    def _apply_malrule_to_two_numbers_with_steps(self, minuend: int, subtrahend: int, steps: list) -> int:
        """
        Apply Smaller-From-Larger malrule to two numbers with detailed steps.

        Args:
            minuend: Top number
            subtrahend: Bottom number
            steps: List to append steps to

        Returns:
            Incorrect result due to malrule
        """
        # Convert to digit lists (rightmost digit first for easier processing)
        minuend_digits = [int(d) for d in str(minuend)][::-1]
        subtrahend_digits = [int(d) for d in str(subtrahend)][::-1]

        # Pad subtrahend with zeros if needed
        while len(subtrahend_digits) < len(minuend_digits):
            subtrahend_digits.append(0)

        result_digits = []

        # Process each column - ALWAYS smaller from larger
        for i in range(len(minuend_digits)):
            top_digit = minuend_digits[i]
            bottom_digit = subtrahend_digits[i]

            place_name = ['ones', 'tens', 'hundreds', 'thousands'][i] if i < 4 else f'10^{i}'

            # MALRULE: Always subtract smaller from larger
            if top_digit >= bottom_digit:
                # Top is larger or equal, so subtract normally
                result = top_digit - bottom_digit
                steps.append(
                    f"{place_name.capitalize()} place: {top_digit} >= {bottom_digit}, "
                    f"so {top_digit} - {bottom_digit} = {result}"
                )
                result_digits.append(result)
            else:
                # Bottom is larger, so REVERSE the operation (ERROR!)
                result = bottom_digit - top_digit
                steps.append(
                    f"{place_name.capitalize()} place: {top_digit} < {bottom_digit}, "
                    f"so subtract smaller from larger: {bottom_digit} - {top_digit} = {result}"
                )
                result_digits.append(result)

        # Convert result digits back to number
        # Remove leading zeros
        while len(result_digits) > 1 and result_digits[-1] == 0:
            result_digits.pop()

        return int(''.join(str(d) for d in result_digits[::-1]))
