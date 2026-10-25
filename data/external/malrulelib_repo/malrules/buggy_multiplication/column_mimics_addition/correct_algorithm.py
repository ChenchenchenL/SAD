"""
Correct multiplication algorithm.

Implements the standard algorithm for multi-digit multiplication.
"""

import sys
sys.path.append('/Users/kitetsu/nlp_mac/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class MultiplicationCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for multi-digit multiplication using the standard algorithm.
    """

    def get_name(self) -> str:
        return "Correct Multiplication Algorithm"

    def get_description(self) -> str:
        return (
            "The standard algorithm for multi-digit multiplication. Each digit "
            "of the multiplier is multiplied by each digit of the multiplicand, "
            "with appropriate place value shifts. Partial products are then added "
            "together to get the final result. This process uses the distributive "
            "property: (a + b) x c = a x c + b x c."
        )

    def _generate_verbose_steps(self, problem: Problem) -> Solution:
        """Generate detailed correct solution."""
        multiplicand, multiplier = problem.operands[:2]
        answer = multiplicand * multiplier

        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD: Standard Multiplication Algorithm")
        steps.append("")

        # Show expanded form
        m1_digits = [int(d) for d in str(multiplicand)]
        m2_digits = [int(d) for d in str(multiplier)]

        steps.append(f"Multiplying {multiplicand} x {multiplier}:")
        steps.append("")

        # Compute partial products
        partial_products = []
        place_value = 1

        for i, d2 in enumerate(reversed(m2_digits)):
            partial = multiplicand * d2 * place_value
            position = "ones" if i == 0 else "tens" if i == 1 else "hundreds" if i == 2 else f"10^{i}"
            steps.append(f"  {multiplicand} x {d2} ({position} digit of {multiplier}) = {multiplicand * d2}")
            if i > 0:
                steps.append(f"    Shifted by {i} place(s): {partial}")
            partial_products.append(partial)
            place_value *= 10

        steps.append("")
        steps.append(f"  Sum of partial products: {' + '.join(str(p) for p in partial_products)}")
        steps.append(f"  = {sum(partial_products)}")
        steps.append("")
        steps.append(f"Answer: {answer}")

        return Solution(
            answer=str(answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _generate_concise_steps(self, problem: Problem) -> Solution:
        """Generate concise solution."""
        multiplicand, multiplier = problem.operands[:2]

        # Check metadata first
        if 'correct_answer' in problem.metadata:
            answer = str(problem.metadata['correct_answer'])
        else:
            answer = str(multiplicand * multiplier)

        steps = [
            f"Problem: {problem.text}",
            f"Calculation: {multiplicand} x {multiplier} = {answer}",
            f"Answer: {answer}"
        ]

        return Solution(
            answer=answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct multiplication algorithm.

        Args:
            problem: Multiplication problem to solve
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with correct answer
        """
        if verbose:
            return self._generate_verbose_steps(problem)
        else:
            return self._generate_concise_steps(problem)
