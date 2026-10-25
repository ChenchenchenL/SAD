"""
Add-All-Digits malrule algorithm.

Implements the systematic error where students always sum up all the digits
with no regard to columns or place value.
"""

import sys
sys.path.append('/Users/kitetsu/nlp_mac/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List

class AddAllDigitsMalrule(Malrule):
    """
    Implements the Add-All-Digits bug.

    Students sum all individual digits from both numbers without regard
    to place value or column alignment. This represents a fundamental
    misunderstanding of how multi-digit addition works.
    """

    def get_name(self) -> str:
        return "Add-All-Digits"

    def get_description(self) -> str:
        return (
            "A systematic procedural bug where the student always sums up all the "
            "digits with no regard to columns or place value. Instead of aligning "
            "digits by place value (ones with ones, tens with tens, etc.) and adding "
            "column by column with carrying, the student simply adds every individual "
            "digit together to get a single sum. For example, in 17 + 5, the student "
            "computes 1 + 7 + 5 = 13 instead of correctly aligning and adding to get 22. "
            "This is documented in Brown & Burton (1978) as one of the fundamental "
            "addition bugs that shows complete misunderstanding of place value."
        )

    def calculate_expected_answer(self, problem: Problem) -> Any:
        """
        Calculate the expected incorrect answer for this malrule.

        For Add-All-Digits:
        - Sum all individual digits from all operands
        - No regard to place value or column alignment

        Args:
            problem: Addition problem

        Returns:
            Expected incorrect answer (sum of all digits)
        """

        # Calculate from operands
        total = 0
        for operand in problem.operands:
            for digit in str(operand):
                total += int(digit)

        return str(total)

    def _sum_all_digits_with_steps(self, problem: Problem) -> tuple:
        """
        Calculate the sum of all digits and generate the calculation string.

        Args:
            problem: The problem with operands

        Returns:
            Tuple of (sum, calculation_string, digit_list)
        """
        digits = []
        for operand in problem.operands:
            for digit in str(operand):
                digits.append(int(digit))

        calculation = ' + '.join(str(d) for d in digits)
        total = sum(digits)

        return total, calculation, digits

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

        # Get operands
        addend1, addend2 = problem.operands[:2]
        steps.append(f"Formula: {addend1} + {addend2}")

        # Show the malrule calculation
        total, calculation, digits = self._sum_all_digits_with_steps(problem)
        steps.append(f"MALRULE: Sum all digits: {calculation} = {malrule_answer}")

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

        # Add question
        steps.append(f"Question: {problem.text}")
        steps.append("")

        # Get operands
        addend1, addend2 = problem.operands[:2]

        steps.append(f"MALRULE: Add-All-Digits")
        steps.append(f"  Student's incorrect reasoning: 'Add all the digits together'")
        steps.append("")

        # Show the breakdown
        digits1 = [int(d) for d in str(addend1)]
        digits2 = [int(d) for d in str(addend2)]

        steps.append(f"Step 1: Extract all digits from {addend1}: {', '.join(str(d) for d in digits1)}")
        steps.append(f"Step 2: Extract all digits from {addend2}: {', '.join(str(d) for d in digits2)}")

        all_digits = digits1 + digits2
        steps.append(f"Step 3: All digits: {', '.join(str(d) for d in all_digits)}")

        total, calculation, _ = self._sum_all_digits_with_steps(problem)
        steps.append(f"Step 4: Sum all digits: {calculation} = {malrule_answer}")

        steps.append("")
        steps.append(f"Final answer: {malrule_answer} (INCORRECT due to Add-All-Digits)")
        steps.append(f"Correct answer should be: {addend1 + addend2}")

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Add-All-Digits malrule to solve the problem incorrectly.

        Args:
            problem: Addition problem to solve
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with incorrect answer due to Add-All-Digits bug
        """
        # Calculate the malrule answer
        malrule_answer = int(self.calculate_expected_answer(problem))

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
