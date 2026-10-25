"""
Correct multi-digit multiplication algorithm.

Implements the standard algorithm for multi-digit multiplication with
proper alignment of partial products.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import CorrectAlgorithm, Problem, Solution


class MultiDigitMultiplicationCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for multi-digit multiplication.

    Properly aligns partial products by shifting left when multiplying
    by the tens digit (or higher place values).
    """

    def get_name(self) -> str:
        return "Correct Multi-Digit Multiplication Algorithm"

    def get_description(self) -> str:
        return (
            "The standard algorithm for multi-digit multiplication. Correctly computes "
            "partial products and shifts them appropriately based on place value. "
            "When multiplying by the tens digit, the partial product is shifted one "
            "place left (equivalent to multiplying by 10)."
        )

    def _generate_concise_steps(self, problem: Problem, num1: int, num2: int,
                                 numeric_answer: str, is_3digit: bool = False) -> list:
        """
        Generate concise steps for the solution.

        Returns a list: [Question, step1, step2, ..., answer]
        """
        steps = []

        # Question
        steps.append(problem.text)

        # Formula extraction
        steps.append(f"{num1} × {num2}")

        if is_3digit:
            num2_ones = problem.metadata['num2_ones']
            num2_tens = problem.metadata['num2_tens']
            num2_hundreds = problem.metadata['num2_hundreds']

            partial1 = num1 * num2_ones
            partial2_calc = num1 * num2_tens
            partial2 = partial2_calc * 10
            partial3_calc = num1 * num2_hundreds
            partial3 = partial3_calc * 100

            # Partial products
            steps.append(f"{num1} × {num2_ones} = {partial1}")
            steps.append(f"{num1} × {num2_tens} × 10 = {partial2}")
            steps.append(f"{num1} × {num2_hundreds} × 100 = {partial3}")

            # Sum
            steps.append(f"{partial1} + {partial2} + {partial3} = {numeric_answer}")
        else:
            num2_ones = problem.metadata.get('num2_ones', num2 % 10)
            num2_tens = problem.metadata.get('num2_tens', num2 // 10)

            partial1 = num1 * num2_ones
            partial2_calc = num1 * num2_tens
            partial2 = partial2_calc * 10

            # Partial products
            steps.append(f"{num1} × {num2_ones} = {partial1}")
            steps.append(f"{num1} × {num2_tens} × 10 = {partial2}")

            # Sum
            steps.append(f"{partial1} + {partial2} = {numeric_answer}")

        # Final answer
        steps.append(numeric_answer)

        return steps

    def _generate_verbose_steps(self, problem: Problem, num1: int, num2: int,
                                 numeric_answer: str, is_3digit: bool = False) -> list:
        """
        Generate verbose steps for the solution (original step format).
        """
        steps = []
        correct_answer = numeric_answer

        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD: Properly shift partial products for place value")
        steps.append("  Key: Multiply by the place value, not just the digit!")
        steps.append("")

        if is_3digit:
            num2_ones = problem.metadata['num2_ones']
            num2_tens = problem.metadata['num2_tens']
            num2_hundreds = problem.metadata['num2_hundreds']

            partial1 = num1 * num2_ones
            partial2_calc = num1 * num2_tens
            partial2 = partial2_calc * 10
            partial3_calc = num1 * num2_hundreds
            partial3 = partial3_calc * 100

            steps.append(f"Multiplying {num1} × {num2}")
            steps.append(f"First partial product: {num1} × {num2_ones} = {partial1}")
            steps.append(f"Second partial product: {num1} × {num2_tens} × 10 = {partial2}")
            steps.append(f"  ✓ CORRECT: Shifted left because {num2_tens} is in tens place")
            steps.append(f"Third partial product: {num1} × {num2_hundreds} × 100 = {partial3}")
            steps.append(f"  ✓ CORRECT: Shifted two places because {num2_hundreds} is in hundreds place")
            steps.append("")
            steps.append(f"Adding: {partial1} + {partial2} + {partial3} = {numeric_answer}")
        else:
            num2_ones = problem.metadata.get('num2_ones', num2 % 10)
            num2_tens = problem.metadata.get('num2_tens', num2 // 10)

            partial1 = num1 * num2_ones
            partial2_calc = num1 * num2_tens
            partial2 = partial2_calc * 10

            steps.append(f"Multiplying {num1} × {num2}")
            steps.append(f"First partial product: {num1} × {num2_ones} = {partial1}")
            steps.append(f"Second partial product calculation: {num1} × {num2_tens} = {partial2_calc}")
            steps.append("")
            steps.append(f"✓ CORRECT: Shift left (multiply by 10): {partial2_calc} × 10 = {partial2}")
            steps.append(f"  Why? Because {num2_tens} is in the TENS place = {num2_tens}×10")
            steps.append("")
            steps.append(f"Adding partial products: {partial1} + {partial2} = {numeric_answer}")
            steps.append("")
            steps.append(f"Expanded form: {num1} × ({num2_tens}×10 + {num2_ones})")
            steps.append(f"            = ({num1}×{num2_tens}×10) + ({num1}×{num2_ones})")
            steps.append(f"            = {partial2} + {partial1} = {numeric_answer}")

        steps.append("")
        steps.append(f"Final Answer: {correct_answer} ✓")
        steps.append("")
        steps.append("Key concept: Place value means shifting partial products left")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct multi-digit multiplication algorithm.

        Args:
            problem: Multiplication problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with correct product
        """
        template = problem.metadata.get('template', 'basic_2x2')
        num1 = problem.metadata.get('num1', problem.operands[0])
        num2 = problem.metadata.get('num2', problem.operands[1])

        # Compute correct answer (never use metadata['correct_answer'])
        numeric_answer = str(num1 * num2)
        correct_answer = numeric_answer

        is_3digit = problem.metadata.get('is_3digit', False)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, num1, num2, numeric_answer, is_3digit)
        else:
            steps = self._generate_concise_steps(problem, num1, num2, numeric_answer, is_3digit)

        return Solution(
            answer=str(correct_answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
