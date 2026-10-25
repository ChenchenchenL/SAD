"""
Correct two-digit addition algorithm with regrouping.

Implements the standard algorithm with proper carrying.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution

class TwoDigitAdditionCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for two-digit addition with regrouping.

    Uses place value understanding and carrying to add correctly.
    """

    def get_name(self) -> str:
        return "Correct Two-Digit Addition Algorithm"

    def get_description(self) -> str:
        return (
            "The standard algorithm for adding two-digit numbers. Add the ones "
            "column first. If the sum is 10 or more, write the ones digit and "
            "carry the tens digit to the tens column. Then add the tens column, "
            "including any carried value."
        )

    def _generate_concise_steps(self, problem: Problem, num1: int, num2: int,
                                 correct_answer_num: int, template: str) -> List[str]:
        """Generate concise steps with only formulas and values."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: {num1} + {num2}")

        if template == 'three_digit':
            hundreds1 = num1 // 100
            tens1 = (num1 // 10) % 10
            ones1 = num1 % 10
            hundreds2 = num2 // 100
            tens2 = (num2 // 10) % 10
            ones2 = num2 % 10

            ones_sum = ones1 + ones2
            ones_digit = ones_sum % 10
            ones_carry = ones_sum // 10
            steps.append(f"Ones: {ones1} + {ones2} = {ones_sum}")
            steps.append(f"Write {ones_digit}, carry {ones_carry}")

            tens_total = tens1 + tens2 + ones_carry
            tens_digit = tens_total % 10
            tens_carry = tens_total // 10
            steps.append(f"Tens: {tens1} + {tens2} + {ones_carry} = {tens_total}")
            steps.append(f"Write {tens_digit}, carry {tens_carry}")

            hundreds_total = hundreds1 + hundreds2 + tens_carry
            steps.append(f"Hundreds: {hundreds1} + {hundreds2} + {tens_carry} = {hundreds_total}")
        else:
            tens1 = num1 // 10
            ones1 = num1 % 10
            tens2 = num2 // 10
            ones2 = num2 % 10

            ones_sum = ones1 + ones2
            steps.append(f"Ones: {ones1} + {ones2} = {ones_sum}")

            if ones_sum >= 10:
                ones_digit = ones_sum % 10
                carry = ones_sum // 10
                steps.append(f"Write {ones_digit}, carry {carry}")
            else:
                carry = 0

            tens_total = tens1 + tens2 + carry
            if carry > 0:
                steps.append(f"Tens: {tens1} + {tens2} + {carry} = {tens_total}")
            else:
                steps.append(f"Tens: {tens1} + {tens2} = {tens_total}")

        steps.append(f"Answer: {correct_answer_num}")
        return steps

    def _generate_verbose_steps(self, problem: Problem, num1: int, num2: int,
                                 correct_answer_num: int, template: str) -> List[str]:
        """Generate verbose steps with detailed explanations."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD: Use place value understanding and carrying")
        steps.append("  Each column can only hold digits 0-9")
        steps.append("")

        if template == 'three_digit':
            hundreds1 = num1 // 100
            tens1 = (num1 // 10) % 10
            ones1 = num1 % 10
            hundreds2 = num2 // 100
            tens2 = (num2 // 10) % 10
            ones2 = num2 % 10

            steps.append(f"Adding {num1} + {num2}")
            steps.append("")

            ones_sum = ones1 + ones2
            ones_digit = ones_sum % 10
            ones_carry = ones_sum // 10
            steps.append(f"Ones: {ones1} + {ones2} = {ones_sum}")
            steps.append(f"  Write {ones_digit}, carry {ones_carry}")
            steps.append("")

            tens_total = tens1 + tens2 + ones_carry
            tens_digit = tens_total % 10
            tens_carry = tens_total // 10
            steps.append(f"Tens: {tens1} + {tens2} + {ones_carry} (carry) = {tens_total}")
            steps.append(f"  Write {tens_digit}, carry {tens_carry}")
            steps.append("")

            hundreds_total = hundreds1 + hundreds2 + tens_carry
            steps.append(f"Hundreds: {hundreds1} + {hundreds2} + {tens_carry} (carry) = {hundreds_total}")
            steps.append(f"  Write {hundreds_total}")

            correct_answer = str(correct_answer_num)
        else:
            tens1 = num1 // 10
            ones1 = num1 % 10
            tens2 = num2 // 10
            ones2 = num2 % 10

            steps.append(f"Adding {num1} + {num2}")
            steps.append("")

            ones_sum = ones1 + ones2
            steps.append(f"Ones column: {ones1} + {ones2} = {ones_sum}")

            if ones_sum >= 10:
                ones_digit = ones_sum % 10
                carry = ones_sum // 10
                steps.append(f"  {ones_sum} is too big for ones column!")
                steps.append(f"  Write {ones_digit} in ones, carry {carry} to tens ✓")
            else:
                ones_digit = ones_sum
                carry = 0
                steps.append(f"  Write {ones_digit} in ones column")

            steps.append("")

            tens_total = tens1 + tens2 + carry
            if carry > 0:
                steps.append(f"Tens column: {tens1} + {tens2} + {carry} (carry) = {tens_total}")
            else:
                steps.append(f"Tens column: {tens1} + {tens2} = {tens_total}")

            if tens_total >= 10:
                tens_digit = tens_total % 10
                hundreds_carry = tens_total // 10
                steps.append(f"  Write {tens_digit} in tens, carry {hundreds_carry} to hundreds")
            else:
                steps.append(f"  Write {tens_total} in tens place")

            if template == 'money_context':
                correct_answer = f'${correct_answer_num}'
            elif template == 'word_problem':
                context_type = problem.metadata.get('context_type', '')
                correct_answer = f'{correct_answer_num} {context_type}'
            else:
                correct_answer = str(correct_answer_num)

        steps.append("")
        steps.append(f"Final Answer: {correct_answer} ✓")
        steps.append("")
        steps.append("Key concept: Each column holds only 0-9; carry when sum ≥ 10")
        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct addition algorithm with proper regrouping.

        Uses logic to compute answers, not metadata values.

        Args:
            problem: Addition problem to solve
            verbose: If True, generate detailed steps; if False, generate concise steps

        Returns:
            Solution with correct answer
        """
        template = problem.metadata.get('template', 'basic_two_digit')
        num1, num2 = problem.operands

        # Compute correct answer using logic
        correct_answer_num = num1 + num2

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, num1, num2, correct_answer_num, template)
        else:
            steps = self._generate_concise_steps(problem, num1, num2, correct_answer_num, template)

        # Format answer based on template
        if template == 'money_context':
            correct_answer = f'${correct_answer_num}'
        elif template == 'word_problem':
            context_type = problem.metadata.get('context_type', '')
            correct_answer = f'{correct_answer_num} {context_type}'
        else:
            correct_answer = str(correct_answer_num)

        return Solution(
            answer=str(correct_answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
