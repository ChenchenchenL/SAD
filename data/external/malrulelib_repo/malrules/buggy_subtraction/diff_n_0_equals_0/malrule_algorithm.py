"""
DIFF/N-0=0 malrule algorithm.

Implements the systematic error where students write 0 in the answer
whenever the bottom digit (subtrahend) is 0, instead of writing the top digit.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List

class DiffN0Equals0Malrule(Malrule):
    """
    Implements the DIFF/N-0=0 bug from Brown & Burton (1978).

    When the bottom digit in a column is 0, the student writes 0 in the answer
    instead of the top digit. The student incorrectly believes that N-0=0
    instead of the correct N-0=N.

    Example from Brown & Burton (1978):
    403 - 208 = 105 (Correct: 195)
      - Ones: 3-8 requires borrow -> 13-8=5 (correct)
      - Tens: 9-0, student writes 0 (BUG!) instead of 9
      - Hundreds: 3-2=1 (correct)
    """

    def get_name(self) -> str:
        return "DIFF/N-0=0"

    def get_description(self) -> str:
        return (
            "A systematic procedural bug where the student writes 0 in the answer "
            "whenever the bottom digit (subtrahend) in a column is 0. The student "
            "incorrectly believes N-0=0 instead of the correct N-0=N. This bug is "
            "documented in Brown & Burton (1978) and occurs in the COMPLETE COLUMN "
            "procedure of the subtraction algorithm. For example, in 403-208, when "
            "processing the tens column after borrowing (9-0), the student writes 0 "
            "instead of 9, yielding 105 instead of 195."
        )

    def calculate_expected_answer(self, problem: Problem) -> Any:
        """
        Calculate the expected incorrect answer for this malrule.

        For DIFF/N-0=0:
        - When bottom digit is 0, write 0 in the answer (BUG!)
        - Otherwise, perform normal subtraction with borrowing

        Args:
            problem: Subtraction problem

        Returns:
            Expected incorrect answer as string
        """
        # Calculate from operands
        minuend, subtrahend = problem.operands[:2]
        result = self._apply_malrule_to_two_numbers(minuend, subtrahend)
        return str(result)

    def _apply_malrule_to_two_numbers(self, minuend: int, subtrahend: int) -> int:
        """
        Apply DIFF/N-0=0 malrule to two numbers.

        The student correctly handles borrowing (including borrow-across-zero),
        but when they see 0 in the subtrahend (bottom), they write 0 instead
        of the actual difference (which would be the top digit minus zero = top digit).

        Args:
            minuend: Top number
            subtrahend: Bottom number (contains 0s that trigger the bug)

        Returns:
            Incorrect result due to malrule
        """
        # First, do a correct subtraction to get the properly borrowed minuend digits
        # This simulates the student correctly handling borrowing
        minuend_digits = [int(d) for d in str(minuend)][::-1]
        subtrahend_digits = [int(d) for d in str(subtrahend)][::-1]

        # Pad subtrahend with zeros if needed
        while len(subtrahend_digits) < len(minuend_digits):
            subtrahend_digits.append(0)

        # Make a copy of minuend digits that we'll modify with borrows
        working_minuend = minuend_digits.copy()

        result_digits = []

        # Process each column
        for i in range(len(working_minuend)):
            top_digit = working_minuend[i]
            bottom_digit = subtrahend_digits[i]

            # MALRULE: If bottom digit is 0, write 0 (not top digit)
            # The student ignores the actual top digit value
            if bottom_digit == 0:
                result_digits.append(0)  # BUG! Should be top_digit
                # No borrowing needed when bottom is 0
            else:
                # Normal subtraction with borrowing
                if top_digit < bottom_digit:
                    # Need to borrow - find a column to borrow from
                    # This handles borrow-across-zero correctly
                    borrow_col = i + 1
                    while borrow_col < len(working_minuend) and working_minuend[borrow_col] == 0:
                        working_minuend[borrow_col] = 9  # Borrowed through
                        borrow_col += 1
                    if borrow_col < len(working_minuend):
                        working_minuend[borrow_col] -= 1
                    top_digit += 10

                result_digits.append(top_digit - bottom_digit)

        # Remove leading zeros
        while len(result_digits) > 1 and result_digits[-1] == 0:
            result_digits.pop()

        return int(''.join(str(d) for d in result_digits[::-1]))

    def _generate_concise_steps_for_malrule(self, minuend: int, subtrahend: int) -> List[str]:
        """
        Generate concise steps for a single subtraction with malrule.

        Args:
            minuend: The number being subtracted from
            subtrahend: The number being subtracted (contains 0s)

        Returns:
            List of concise step strings
        """
        steps = []

        # Convert to digit lists (rightmost digit first)
        minuend_digits = [int(d) for d in str(minuend)][::-1]
        subtrahend_digits = [int(d) for d in str(subtrahend)][::-1]

        # Pad subtrahend with zeros if needed
        while len(subtrahend_digits) < len(minuend_digits):
            subtrahend_digits.append(0)

        # Working copy for borrowing
        working_minuend = minuend_digits.copy()
        place_names = ['ones', 'tens', 'hundreds', 'thousands']

        # Process each column
        for i in range(len(working_minuend)):
            top_digit = working_minuend[i]
            bottom_digit = subtrahend_digits[i]
            place_name = place_names[i] if i < len(place_names) else f'10^{i}'

            if bottom_digit == 0:
                # MALRULE: Write 0 when bottom is 0
                steps.append(f"{place_name.capitalize()}: {top_digit}-0 = 0")
            else:
                if top_digit < bottom_digit:
                    # Handle borrow-across-zero
                    borrow_col = i + 1
                    while borrow_col < len(working_minuend) and working_minuend[borrow_col] == 0:
                        working_minuend[borrow_col] = 9
                        borrow_col += 1
                    if borrow_col < len(working_minuend):
                        working_minuend[borrow_col] -= 1
                    borrowed_top = top_digit + 10
                    result = borrowed_top - bottom_digit
                    steps.append(f"{place_name.capitalize()}: {borrowed_top} - {bottom_digit} = {result}")
                else:
                    result = top_digit - bottom_digit
                    steps.append(f"{place_name.capitalize()}: {top_digit} - {bottom_digit} = {result}")

        return steps

    def _generate_verbose_steps_for_malrule(self, minuend: int, subtrahend: int) -> List[str]:
        """
        Generate verbose steps for a single subtraction with malrule.

        Args:
            minuend: The number being subtracted from
            subtrahend: The number being subtracted (contains 0s)

        Returns:
            List of verbose step strings
        """
        steps = []

        # Convert to digit lists (rightmost digit first)
        minuend_digits = [int(d) for d in str(minuend)][::-1]
        subtrahend_digits = [int(d) for d in str(subtrahend)][::-1]

        # Pad subtrahend with zeros if needed
        while len(subtrahend_digits) < len(minuend_digits):
            subtrahend_digits.append(0)

        # Working copy for borrowing
        working_minuend = minuend_digits.copy()
        place_names = ['ones', 'tens', 'hundreds', 'thousands']

        # Process each column
        for i in range(len(working_minuend)):
            top_digit = working_minuend[i]
            bottom_digit = subtrahend_digits[i]
            place_name = place_names[i] if i < len(place_names) else f'10^{i}'

            if bottom_digit == 0:
                # MALRULE: Write 0 when bottom is 0
                steps.append(
                    f"{place_name.capitalize()} place: bottom digit is 0, "
                    f"so write 0 (MALRULE: N-0=0 instead of N-0=N)"
                )
            else:
                if top_digit < bottom_digit:
                    # Handle borrow-across-zero
                    borrow_col = i + 1
                    while borrow_col < len(working_minuend) and working_minuend[borrow_col] == 0:
                        working_minuend[borrow_col] = 9
                        borrow_col += 1
                    if borrow_col < len(working_minuend):
                        working_minuend[borrow_col] -= 1
                    borrowed_top = top_digit + 10
                    steps.append(
                        f"{place_name.capitalize()} place: {top_digit} < {bottom_digit}, "
                        f"so borrow from the next column"
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

        minuend, subtrahend = problem.operands[:2]
        steps.append(f"Subtracting {subtrahend} from {minuend}")
        steps.append("")
        steps.append(f"MALRULE: {self.get_name()}")
        steps.append(f"  Student believes: 'N-0=0' (incorrect, should be N-0=N)")
        steps.append("")
        steps.extend(self._generate_verbose_steps_for_malrule(minuend, subtrahend))
        steps.append(f"Final answer: {malrule_answer} (INCORRECT due to N-0=0 bug)")

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the DIFF/N-0=0 malrule to solve the problem incorrectly.

        Args:
            problem: Subtraction problem to solve
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with incorrect answer due to N-0=0 bug
        """
        # Calculate the malrule answer
        malrule_answer = self.calculate_expected_answer(problem)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, int(malrule_answer))
        else:
            steps = self._generate_concise_steps(problem, int(malrule_answer))

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
