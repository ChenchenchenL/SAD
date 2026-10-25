"""
Correct place value decomposition algorithm.

Implements the correct method for interpreting place value decompositions
by multiplying each place value and adding the results.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution

class PlaceValueDecompositionCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for interpreting place value decompositions.

    Properly calculates the value by multiplying each place value count
    by its place value and summing the results.
    """

    def get_name(self) -> str:
        return "Correct Place Value Decomposition"

    def get_description(self) -> str:
        return (
            "The correct method for interpreting place value decompositions. "
            "Each place value label represents a quantity to be multiplied by "
            "its place value, then all values are added together. For example, "
            "'2 hundreds 13 tens 1 ones' means 2×100 + 13×10 + 1×1 = 200 + 130 + 1 = 331."
        )

    def _generate_concise_steps(self, problem: Problem, thousands: int, hundreds: int,
                                 tens: int, ones: int, correct_answer: str) -> List[str]:
        """Generate concise steps with only formulas and values."""
        steps = []
        steps.append(f"Question: {problem.text}")

        # Build formula
        formula_parts = []
        if thousands > 0:
            formula_parts.append(f"{thousands} × 1000")
        if hundreds > 0:
            formula_parts.append(f"{hundreds} × 100")
        if tens > 0:
            formula_parts.append(f"{tens} × 10")
        if ones > 0:
            formula_parts.append(f"{ones} × 1")
        steps.append(f"Formula: {' + '.join(formula_parts)}")

        # Calculate each place value
        if thousands > 0:
            steps.append(f"{thousands} × 1000 = {thousands * 1000}")
        if hundreds > 0:
            steps.append(f"{hundreds} × 100 = {hundreds * 100}")
        if tens > 0:
            steps.append(f"{tens} × 10 = {tens * 10}")
        if ones > 0:
            steps.append(f"{ones} × 1 = {ones}")

        # Sum
        values = []
        if thousands > 0:
            values.append(str(thousands * 1000))
        if hundreds > 0:
            values.append(str(hundreds * 100))
        if tens > 0:
            values.append(str(tens * 10))
        if ones > 0:
            values.append(str(ones))
        steps.append(f"{' + '.join(values)} = {correct_answer}")

        steps.append(f"Answer: {correct_answer}")
        return steps

    def _generate_verbose_steps(self, problem: Problem, thousands: int, hundreds: int,
                                 tens: int, ones: int, correct_answer: str) -> List[str]:
        """Generate verbose steps with detailed explanations."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD: Understand place values as MULTIPLICATIVE")
        steps.append("  Each label represents a QUANTITY of that place value")
        steps.append("")

        # Calculate each place value
        calculations = []
        total = 0

        if thousands > 0:
            value = thousands * 1000
            total += value
            calculations.append(f"{thousands} × 1000 = {value}")
            steps.append(f"Thousands: {thousands} thousand{'s' if thousands != 1 else ''} = {thousands} × 1000 = {value}")

        if hundreds > 0:
            value = hundreds * 100
            total += value
            calculations.append(f"{hundreds} × 100 = {value}")
            steps.append(f"Hundreds: {hundreds} hundred{'s' if hundreds != 1 else ''} = {hundreds} × 100 = {value}")

        if tens > 0:
            value = tens * 10
            total += value
            calculations.append(f"{tens} × 10 = {value}")
            steps.append(f"Tens: {tens} ten{'s' if tens != 1 else ''} = {tens} × 10 = {value}")

        if ones > 0:
            value = ones * 1
            total += value
            calculations.append(f"{ones} × 1 = {value}")
            steps.append(f"Ones: {ones} one{'s' if ones != 1 else ''} = {ones} × 1 = {value}")

        # Add them all together
        steps.append("")
        addition = " + ".join(calculations)
        steps.append(f"Adding the values: {addition} = {total}")
        steps.append("")
        steps.append(f"Final Answer: {correct_answer} ✓")
        steps.append("")
        steps.append("Key concept: Place values are MULTIPLIED, then ADDED")
        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct place value decomposition interpretation.

        Args:
            problem: Place value decomposition problem to solve
            verbose: If True, generate detailed steps; if False, generate concise steps

        Returns:
            Solution with correct answer
        """
        template = problem.metadata.get('template', 'basic_regrouped_tens')

        thousands = problem.metadata.get('thousands', problem.operands[0])
        hundreds = problem.metadata.get('hundreds', problem.operands[1])
        tens = problem.metadata.get('tens', problem.operands[2])
        ones = problem.metadata.get('ones', problem.operands[3])

        # Calculate correct answer using place value logic
        # Each place value count is multiplied by its place value and summed
        correct_answer = str(thousands * 1000 + hundreds * 100 + tens * 10 + ones)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, thousands, hundreds, tens, ones, correct_answer)
        else:
            steps = self._generate_concise_steps(problem, thousands, hundreds, tens, ones, correct_answer)

        return Solution(
            answer=str(correct_answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
