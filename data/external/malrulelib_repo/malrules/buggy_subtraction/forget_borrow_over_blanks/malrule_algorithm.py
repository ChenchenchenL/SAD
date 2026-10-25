"""
FORGET/BORROW/OVER/BLANKS malrule algorithm.

Implements the systematic error where students forget to borrow over blank
columns when the minuend has fewer digits than the subtrahend.

Research: Brown & Burton (1978) "Diagnostic Models for Procedural Bugs"
Network location: COLUMN SEQUENCE procedure
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List

class ForgetBorrowOverBlanksMalrule(Malrule):
    """
    Implements the FORGET/BORROW/OVER/BLANKS bug.

    When the top number (minuend) has fewer digits than the bottom number
    (subtrahend), students forget to borrow over the blank columns. They
    treat the implicit zeros as not participating in the borrowing chain
    and often apply smaller-from-larger in those columns.

    Example: 85 - 127
    - Student treats blank hundreds column incorrectly
    - Does not properly borrow from the non-existent column
    - May compute: ones 15-7=8, tens 7-2=5, hundreds 0-1 -> uses 1-0=1
    - Gets 158 instead of -42 (negative result)
    """

    def get_name(self) -> str:
        return "Forget-Borrow-Over-Blanks"

    def get_description(self) -> str:
        return (
            "A systematic procedural bug where the student forgets to borrow over "
            "blank columns when the minuend (top number) has fewer digits than the "
            "subtrahend (bottom number). The student incorrectly processes the "
            "'blank' positions (implicit zeros) without properly propagating borrows. "
            "For example, in 85 - 127, the student may treat the hundreds column as "
            "simply 1-0 or 0-1 (using smaller-from-larger), yielding an incorrect "
            "positive result instead of recognizing that the operation produces a "
            "negative number or requires special handling. This bug is located in "
            "the COLUMN SEQUENCE procedure of Brown & Burton's procedural network."
        )

    def calculate_expected_answer(self, problem: Problem) -> Any:
        """
        Calculate the expected incorrect answer for this malrule.

        FORGET/BORROW/OVER/BLANKS:
        - Process columns normally where minuend has digits
        - In blank columns, use smaller-from-larger instead of proper borrowing

        Args:
            problem: Subtraction problem

        Returns:
            Expected incorrect answer
        """
        minuend, subtrahend = problem.operands[:2]
        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend)
        max_len = max(len(minuend_str), len(subtrahend_str))

        # Pad minuend with zeros
        minuend_padded = minuend_str.zfill(max_len)

        result_digits = []
        borrow = 0

        # Process from right to left
        for i in range(max_len - 1, -1, -1):
            m_digit = int(minuend_padded[i])
            s_digit = int(subtrahend_str[i]) if i < len(subtrahend_str) else 0

            # Check if this is a "blank" column (where original minuend had no digit)
            original_minuend_pos = i - (max_len - len(minuend_str))
            is_blank_column = original_minuend_pos < 0

            m_digit_after_borrow = m_digit - borrow
            borrow = 0

            if is_blank_column:
                # MALRULE: In blank columns, don't properly handle borrowing
                # Just do smaller from larger (ignoring borrow chain)
                if m_digit_after_borrow < 0:
                    m_digit_after_borrow = 0  # Treat negative as 0
                if m_digit_after_borrow < s_digit:
                    result_digits.append(s_digit - m_digit_after_borrow)
                else:
                    result_digits.append(m_digit_after_borrow - s_digit)
            else:
                # Normal borrowing within the original minuend's columns
                if m_digit_after_borrow < s_digit:
                    # Need to borrow
                    m_digit_after_borrow += 10
                    borrow = 1
                result_digits.append(m_digit_after_borrow - s_digit)

        # Reverse to get correct order and convert to number
        result_digits.reverse()

        # Remove leading zeros
        while len(result_digits) > 1 and result_digits[0] == 0:
            result_digits.pop(0)

        return str(int(''.join(str(d) for d in result_digits)))

    def _generate_concise_steps(self, problem: Problem, malrule_answer: str) -> List[str]:
        """
        Generate concise steps showing the malrule application.

        Args:
            problem: The problem instance
            malrule_answer: The computed malrule answer

        Returns:
            List of concise step strings
        """
        steps = []
        minuend, subtrahend = problem.operands[:2]

        steps.append(f"Question: {problem.text}")
        steps.append(f"Malrule: Forget-Borrow-Over-Blanks")

        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend)
        max_len = max(len(minuend_str), len(subtrahend_str))
        minuend_padded = minuend_str.zfill(max_len)

        steps.append(f"Setup: {minuend_padded} - {subtrahend_str}")

        place_names = ['ones', 'tens', 'hundreds', 'thousands', 'ten-thousands']
        borrow = 0

        # Process from right to left
        for i in range(max_len - 1, -1, -1):
            col_idx = max_len - 1 - i
            place_name = place_names[col_idx] if col_idx < len(place_names) else f'10^{col_idx}'

            m_digit = int(minuend_padded[i])
            s_digit = int(subtrahend_str[i]) if i < len(subtrahend_str) else 0

            original_minuend_pos = i - (max_len - len(minuend_str))
            is_blank_column = original_minuend_pos < 0

            m_digit_after_borrow = m_digit - borrow
            borrow = 0

            if is_blank_column:
                if m_digit_after_borrow < 0:
                    m_digit_after_borrow = 0
                if m_digit_after_borrow < s_digit:
                    result = s_digit - m_digit_after_borrow
                    steps.append(f"{place_name.capitalize()}: BLANK column, {s_digit}-{m_digit_after_borrow}={result}")
                else:
                    result = m_digit_after_borrow - s_digit
                    steps.append(f"{place_name.capitalize()}: BLANK column, {m_digit_after_borrow}-{s_digit}={result}")
            else:
                if m_digit_after_borrow < s_digit:
                    m_digit_after_borrow += 10
                    borrow = 1
                    result = m_digit_after_borrow - s_digit
                    steps.append(f"{place_name.capitalize()}: {m_digit_after_borrow}-{s_digit}={result} (borrowed)")
                else:
                    result = m_digit_after_borrow - s_digit
                    steps.append(f"{place_name.capitalize()}: {m_digit_after_borrow}-{s_digit}={result}")

        steps.append(f"Answer: {malrule_answer} (INCORRECT)")

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
        minuend, subtrahend = problem.operands[:2]

        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append(f"MALRULE: Forget-Borrow-Over-Blanks")
        steps.append(f"  Student believes: 'I only need to borrow within the digits I can see'")
        steps.append("")

        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend)
        max_len = max(len(minuend_str), len(subtrahend_str))
        minuend_padded = minuend_str.zfill(max_len)

        steps.append(f"Setting up: {minuend} vs {subtrahend}")
        steps.append(f"Padded minuend: {minuend_padded}")
        steps.append(f"Note: Minuend has {len(minuend_str)} digits, subtrahend has {len(subtrahend_str)} digits")
        steps.append("")

        place_names = ['ones', 'tens', 'hundreds', 'thousands', 'ten-thousands']
        borrow = 0

        # Process from right to left
        for i in range(max_len - 1, -1, -1):
            col_idx = max_len - 1 - i
            place_name = place_names[col_idx] if col_idx < len(place_names) else f'10^{col_idx}'

            m_digit = int(minuend_padded[i])
            s_digit = int(subtrahend_str[i]) if i < len(subtrahend_str) else 0

            original_minuend_pos = i - (max_len - len(minuend_str))
            is_blank_column = original_minuend_pos < 0

            m_digit_after_borrow = m_digit - borrow
            borrow = 0

            if is_blank_column:
                steps.append(f"{place_name.capitalize()} place (BLANK in original minuend):")
                steps.append(f"  Top digit: {m_digit} (implicit zero)")
                steps.append(f"  Bottom digit: {s_digit}")
                if m_digit_after_borrow < 0:
                    m_digit_after_borrow = 0
                if m_digit_after_borrow < s_digit:
                    result = s_digit - m_digit_after_borrow
                    steps.append(f"  MALRULE: Cannot borrow from nothing, use smaller-from-larger")
                    steps.append(f"  {s_digit} - {m_digit_after_borrow} = {result}")
                else:
                    result = m_digit_after_borrow - s_digit
                    steps.append(f"  {m_digit_after_borrow} - {s_digit} = {result}")
            else:
                steps.append(f"{place_name.capitalize()} place:")
                steps.append(f"  Top digit: {m_digit}" + (f" (after borrow: {m_digit - 1})" if borrow else ""))
                steps.append(f"  Bottom digit: {s_digit}")
                if m_digit_after_borrow < s_digit:
                    m_digit_after_borrow += 10
                    borrow = 1
                    result = m_digit_after_borrow - s_digit
                    steps.append(f"  Need to borrow: {m_digit_after_borrow} - {s_digit} = {result}")
                else:
                    result = m_digit_after_borrow - s_digit
                    steps.append(f"  {m_digit_after_borrow} - {s_digit} = {result}")

            steps.append("")

        steps.append(f"Final Answer: {malrule_answer}")
        steps.append(f"(INCORRECT due to Forget-Borrow-Over-Blanks bug)")
        steps.append(f"Correct answer would be: {minuend - subtrahend}")

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the FORGET/BORROW/OVER/BLANKS malrule to solve the problem incorrectly.

        Args:
            problem: Subtraction problem to solve
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with incorrect answer due to the malrule
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
