"""
Malrule algorithm for Stops-Borrow-At-Zero error.

Students stop the borrowing process entirely when they encounter
a zero, treating it as an insurmountable obstacle.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class StopsBorrowAtZeroMalrule(Malrule):
    """
    Implements the Stops-Borrow-At-Zero malrule.

    Students stop borrowing when they hit a zero, either:
    - Writing the difference as negative
    - Writing zero for that column
    - Getting confused and making up a result

    Example: 503 - 285
    Need to borrow for ones: 3 < 5
    Look left: see 0
    STOP! "Can't borrow from zero"
    Write negative or zero: 503 - 285 → gets 308 or similar wrong answer
    """

    def get_name(self) -> str:
        return "Stops-Borrow-At-Zero"

    def get_description(self) -> str:
        return (
            "A systematic procedural bug where the student stops the borrowing "
            "(regrouping) process entirely when encountering a zero in the column "
            "to the left, rather than cascading the borrow further left to find a "
            "non-zero digit. This bug is part of a family of zero-related borrowing "
            "errors documented in VanLehn's 'Mind Bugs' (1990) and the BUGGY/DEBUGGY "
            "diagnostic systems. When students reach an impasse at zero, they may "
            "write the absolute difference or simply give up on that column."
        )

    def calculate_expected_answer(self, problem: Problem) -> int:
        """
        Calculate the expected incorrect answer for this malrule.

        For Stops-Borrow-At-Zero:
        - When borrowing is needed and the next left digit is zero
        - MALRULE: Student STOPS borrowing and just writes positive difference
        - Student writes: |top_digit - bottom_digit|
        - For other columns, student computes normally

        Example: 503 - 285
        - Ones: 3 < 5, need to borrow. Look left: 0
        - MALRULE: Stop! Write |3 - 5| = 2
        - Tens: 0 - 8? Student confused, writes |0 - 8| = 8
        - Hundreds: 5 - 2 = 3
        - Result: 382 (WRONG! Should be 218)

        Args:
            problem: Subtraction problem

        Returns:
            Expected incorrect answer as integer
        """
        # Extract operands from problem
        minuend, subtrahend = problem.operands[:2]

        # Convert to digit lists
        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend).zfill(len(minuend_str))

        minuend_digits = [int(d) for d in minuend_str]
        subtrahend_digits = [int(d) for d in subtrahend_str]

        # Create working copy
        working_minuend = minuend_digits.copy()
        result_digits = []

        # Process each digit right to left
        for i in range(len(working_minuend) - 1, -1, -1):
            top_digit = working_minuend[i]
            bottom_digit = subtrahend_digits[i]

            # Check if borrowing is needed
            if top_digit < bottom_digit:
                # Check if we need to borrow from zero
                if i > 0 and working_minuend[i - 1] == 0:
                    # MALRULE: Stop at zero! Write positive difference
                    digit_result = abs(top_digit - bottom_digit)
                    result_digits.insert(0, digit_result)

                elif i > 0:
                    # Normal borrowing (not from zero)
                    working_minuend[i - 1] -= 1
                    top_digit += 10
                    digit_result = top_digit - bottom_digit
                    result_digits.insert(0, digit_result)

                else:
                    # Can't borrow (leftmost column) - take positive difference
                    digit_result = abs(top_digit - bottom_digit)
                    result_digits.insert(0, digit_result)

            else:
                # No borrowing needed
                digit_result = top_digit - bottom_digit
                result_digits.insert(0, digit_result)

        # Construct final answer
        result_str = ''.join(str(d) for d in result_digits).lstrip('0') or '0'
        return int(result_str)

    def _generate_concise_steps(self, problem: Problem, minuend: int, subtrahend: int, malrule_result: int) -> List[str]:
        """
        Generate concise steps showing only formulas and values.

        Args:
            problem: The problem instance
            minuend: The number being subtracted from
            subtrahend: The number being subtracted
            malrule_result: The computed malrule result

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

        # Convert to digit lists
        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend).zfill(len(minuend_str))

        minuend_digits = [int(d) for d in minuend_str]
        subtrahend_digits = [int(d) for d in subtrahend_str]

        # Create working copy
        working_minuend = minuend_digits.copy()

        # Process each digit right to left
        for i in range(len(working_minuend) - 1, -1, -1):
            top_digit = working_minuend[i]
            bottom_digit = subtrahend_digits[i]
            col_num = len(working_minuend) - i

            if top_digit < bottom_digit:
                if i > 0 and working_minuend[i - 1] == 0:
                    # MALRULE: Stop at zero
                    digit_result = abs(top_digit - bottom_digit)
                    steps.append(f"Column {col_num}: |{top_digit} - {bottom_digit}| = {digit_result}")
                elif i > 0:
                    # Normal borrowing
                    working_minuend[i - 1] -= 1
                    top_digit += 10
                    digit_result = top_digit - bottom_digit
                    steps.append(f"Column {col_num}: {top_digit} - {bottom_digit} = {digit_result}")
                else:
                    digit_result = abs(top_digit - bottom_digit)
                    steps.append(f"Column {col_num}: |{top_digit} - {bottom_digit}| = {digit_result}")
            else:
                digit_result = top_digit - bottom_digit
                steps.append(f"Column {col_num}: {top_digit} - {bottom_digit} = {digit_result}")

        # Add answer
        steps.append(f"Answer: {malrule_result}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, minuend: int, subtrahend: int, malrule_result: int) -> List[str]:
        """
        Generate verbose steps with full explanations.

        Args:
            problem: The problem instance
            minuend: The number being subtracted from
            subtrahend: The number being subtracted
            malrule_result: The computed malrule result

        Returns:
            List of verbose step strings
        """
        steps = []
        steps.append(f"Problem: {minuend} - {subtrahend}")
        steps.append("")

        # Convert to digit lists
        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend).zfill(len(minuend_str))

        minuend_digits = [int(d) for d in minuend_str]
        subtrahend_digits = [int(d) for d in subtrahend_str]

        # Create working copy
        working_minuend = minuend_digits.copy()

        steps.append("Working right to left:")
        steps.append("")

        stopped_at_zero = False

        # Process each digit right to left
        for i in range(len(working_minuend) - 1, -1, -1):
            top_digit = working_minuend[i]
            bottom_digit = subtrahend_digits[i]

            steps.append(f"Column {len(working_minuend) - i}: {top_digit} - {bottom_digit}")

            if top_digit < bottom_digit:
                steps.append(f"  Need to borrow: {top_digit} < {bottom_digit}")

                if i > 0 and working_minuend[i - 1] == 0:
                    steps.append(f"  Looking left: found 0")
                    steps.append(f"  MALRULE: Stop! Can't borrow from zero")
                    steps.append(f"  MALRULE REASONING: 'Zero means I can't continue, problem is stuck!'")
                    steps.append(f"  (WRONG! Should cascade left to find non-zero)")
                    steps.append("")

                    digit_result = abs(top_digit - bottom_digit)
                    steps.append(f"  Just write the difference: |{top_digit} - {bottom_digit}| = {digit_result}")
                    stopped_at_zero = True

                elif i > 0:
                    working_minuend[i - 1] -= 1
                    top_digit += 10
                    digit_result = top_digit - bottom_digit
                    steps.append(f"  Borrowed from left: {top_digit} - {bottom_digit} = {digit_result}")
                else:
                    digit_result = abs(top_digit - bottom_digit)
                    steps.append(f"  Cannot borrow (leftmost) - just take difference: {digit_result}")

            else:
                digit_result = top_digit - bottom_digit
                steps.append(f"  {top_digit} - {bottom_digit} = {digit_result}")

            steps.append("")

        if stopped_at_zero:
            steps.append(f"Final Answer: {malrule_result} (INCORRECT - stopped at zero instead of cascading)")
        else:
            steps.append(f"Final Answer: {malrule_result}")

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the stops-borrow-at-zero malrule.

        Args:
            problem: Problem instance with minuend and subtrahend
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with incorrect answer and steps
        """
        # Extract operands from problem
        minuend, subtrahend = problem.operands[:2]

        # Calculate malrule answer
        malrule_result = self.calculate_expected_answer(problem)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, minuend, subtrahend, malrule_result)
        else:
            steps = self._generate_concise_steps(problem, minuend, subtrahend, malrule_result)

        return Solution(
            answer=str(malrule_result),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
