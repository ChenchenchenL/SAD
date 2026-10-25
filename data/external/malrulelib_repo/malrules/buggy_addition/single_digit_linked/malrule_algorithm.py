"""
Single-Digit-Linked malrule algorithm.

Implements the systematic error where students link (append) single-digit
operands to the end of multi-digit operands instead of performing addition.
"""

import sys
sys.path.append('/Users/kitetsu/nlp_mac/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List

class SingleDigitLinkedMalrule(Malrule):
    """
    Implements the Single-Digit-Linked bug.

    Students link (append) single-digit operands onto the end of multi-digit
    operands instead of adding them. The single-digit number is always appended
    to the multi-digit number, regardless of which operand is first.

    Examples from Brown & Burton (1978):
    - 19 + 9 = 199 (correct: 28) - single digit 9 appended to 19
    - 23 + 6 = 236 (correct: 29) - single digit 6 appended to 23
    - 81 + 8 = 818 (correct: 89) - single digit 8 appended to 81
    - 8 + 12 = 128 (correct: 20) - single digit 8 appended to 12 (NOT 812!)
    """

    def get_name(self) -> str:
        return "Single-Digit-Linked"

    def get_description(self) -> str:
        return (
            "A systematic procedural bug where the student links (appends) single-digit "
            "operands onto the end of multi-digit operands instead of performing addition. "
            "The single-digit number is always appended to the multi-digit number, regardless "
            "of the order of operands in the problem. For example, in 8 + 12, the student "
            "appends 8 to 12, yielding 128 (NOT 812). This error indicates a fundamental "
            "confusion about place value and the operation of addition, where the student "
            "treats digits as characters to be concatenated rather than numbers to be combined."
        )

    def calculate_expected_answer(self, problem: Problem) -> str:
        """
        Calculate the expected incorrect answer for this malrule.

        For Single-Digit-Linked:
        - Identify which operand is single-digit (1-9)
        - Append the single-digit to the multi-digit operand
        - The single-digit is ALWAYS appended (placed after), not prepended

        Args:
            problem: Addition problem

        Returns:
            Expected incorrect answer as string
        """
        # Calculate from operands
        num1, num2 = problem.operands[:2]

        # Determine which is single-digit and which is multi-digit
        if num1 < 10 and num2 >= 10:
            # num1 is single-digit, append it to num2
            result = int(str(num2) + str(num1))
        elif num2 < 10 and num1 >= 10:
            # num2 is single-digit, append it to num1
            result = int(str(num1) + str(num2))
        else:
            # Both are single-digit or both are multi-digit (edge case)
            # Just concatenate in order
            result = int(str(num1) + str(num2))

        return str(result)

    def _generate_concise_steps(self, problem: Problem, malrule_answer: str) -> List[str]:
        """
        Generate concise steps showing only formulas and values.

        Args:
            problem: The problem instance
            malrule_answer: The computed malrule answer

        Returns:
            List of concise step strings
        """
        steps = []
        num1, num2 = problem.operands[:2]

        # Add question
        steps.append(f"Question: {problem.text}")

        # Identify single-digit and multi-digit
        if num1 < 10 and num2 >= 10:
            single_digit = num1
            multi_digit = num2
            position = "first"
        elif num2 < 10 and num1 >= 10:
            single_digit = num2
            multi_digit = num1
            position = "second"
        else:
            single_digit = num2
            multi_digit = num1
            position = "both same"

        # Show malrule application
        steps.append(f"Single digit ({single_digit}) linked to multi-digit ({multi_digit})")
        steps.append(f"Result: {multi_digit}{single_digit} = {malrule_answer}")
        steps.append(f"Answer: {malrule_answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, malrule_answer: str) -> List[str]:
        """
        Generate verbose steps with full explanations.

        Args:
            problem: The problem instance
            malrule_answer: The computed malrule answer

        Returns:
            List of verbose step strings
        """
        steps = []
        num1, num2 = problem.operands[:2]

        # Add problem statement
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append(f"MALRULE: {self.get_name()}")
        steps.append("  Student believes: 'Link (append) single-digit to multi-digit'")
        steps.append("")

        # Identify single-digit and multi-digit
        if num1 < 10 and num2 >= 10:
            single_digit = num1
            multi_digit = num2
            steps.append(f"Step 1: Identify single-digit operand: {single_digit} (first operand)")
            steps.append(f"Step 2: Identify multi-digit operand: {multi_digit} (second operand)")
        elif num2 < 10 and num1 >= 10:
            single_digit = num2
            multi_digit = num1
            steps.append(f"Step 1: Identify single-digit operand: {single_digit} (second operand)")
            steps.append(f"Step 2: Identify multi-digit operand: {multi_digit} (first operand)")
        else:
            single_digit = num2
            multi_digit = num1
            steps.append(f"Step 1: Both operands same type - treating {num1} as multi-digit")
            steps.append(f"Step 2: Treating {num2} as single-digit to append")

        # Show malrule application
        steps.append(f"Step 3: Link single-digit onto end of multi-digit: {multi_digit}|{single_digit}")
        steps.append(f"Step 4: Concatenate: '{multi_digit}' + '{single_digit}' = '{malrule_answer}'")
        steps.append("")
        steps.append(f"Answer: {malrule_answer} (INCORRECT)")

        correct_answer = num1 + num2
        steps.append(f"(Correct answer should be: {correct_answer})")

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Single-Digit-Linked malrule to solve the problem incorrectly.

        Args:
            problem: Addition problem to solve
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with incorrect answer due to Single-Digit-Linked bug
        """
        # Calculate the malrule answer
        malrule_answer = self.calculate_expected_answer(problem)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, malrule_answer)
        else:
            steps = self._generate_concise_steps(problem, malrule_answer)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
