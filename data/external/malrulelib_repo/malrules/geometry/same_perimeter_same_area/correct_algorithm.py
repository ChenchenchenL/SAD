"""
Correct algorithm for area calculation.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class AreaCalculationCorrectAlgorithm(CorrectAlgorithm):
    """Correctly calculates area regardless of perimeter."""

    def get_name(self) -> str:
        return "Correct Area Calculation"

    def get_description(self) -> str:
        return "Correctly calculates area using dimensions, independent of perimeter."

    def _generate_concise_steps(self, problem: Problem, correct_answer) -> List[str]:
        """Generate concise steps with only formula and values."""
        l1 = problem.metadata['length1']
        w1 = problem.metadata['width1']
        l2 = problem.metadata['length2']
        w2 = problem.metadata['width2']
        is_word_problem = problem.metadata.get('is_word_problem', False)

        steps = []
        steps.append(f"Question: {problem.text}")

        if is_word_problem:
            perimeter1 = 2 * (l1 + w1)
            steps.append(f"Rectangle A: {l1} × {w1}, Rectangle B: {l2} × {w2}")
            steps.append(f"Both have perimeter = {perimeter1}")

        steps.append(f"Area = length × width")
        steps.append(f"Area B = {l2} × {w2} = {correct_answer}")
        steps.append(f"Answer: {correct_answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, correct_answer) -> List[str]:
        """Generate verbose steps with full explanations (original format)."""
        l1 = problem.metadata['length1']
        w1 = problem.metadata['width1']
        l2 = problem.metadata['length2']
        w2 = problem.metadata['width2']
        is_word_problem = problem.metadata.get('is_word_problem', False)

        area1 = l1 * w1
        area2 = l2 * w2
        perimeter1 = 2 * (l1 + w1)
        perimeter2 = 2 * (l2 + w2)

        steps = []

        # For word problems, show extraction step
        if is_word_problem:
            steps.append(f"Word Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Extract information from the word problem")
            steps.append(f"  Both rectangles have perimeter {perimeter1} units")
            steps.append(f"  Rectangle A: {l1} × {w1}")
            steps.append(f"  Rectangle B: {l2} × {w2}")
            steps.append(f"  Question: Find area of Rectangle B")
            steps.append("")
            steps.append("Step 2: Calculate area using dimensions")
            steps.append("")
        else:
            steps.append(f"Problem: Rectangle A: {l1}×{w1}, Rectangle B: {l2}×{w2}")
            steps.append(f"Both have same perimeter. Find area of Rectangle B.")
            steps.append("")

        steps.append("CORRECT METHOD: Calculate area from dimensions")
        steps.append("  Perimeter and area are DIFFERENT measurements!")
        steps.append("")
        steps.append(f"Step 1: Verify both have same perimeter")
        steps.append(f"  Perimeter A = 2({l1} + {w1}) = {perimeter1}")
        steps.append(f"  Perimeter B = 2({l2} + {w2}) = {perimeter2}")
        steps.append(f"  Same perimeter: {perimeter1}")
        steps.append("")
        steps.append(f"Step 2: Calculate area of Rectangle A (for comparison)")
        steps.append(f"  Area A = {l1} × {w1} = {area1}")
        steps.append("")
        steps.append(f"Step 3: Calculate area of Rectangle B")
        steps.append(f"  Area B = {l2} × {w2} = {area2}")
        steps.append("")
        steps.append(f"Final Answer: Area of Rectangle B = {correct_answer}")
        steps.append("")
        steps.append(f"Important: Same perimeter ({perimeter1}) but DIFFERENT areas ({area1} vs {area2})!")
        steps.append(f"  Perimeter measures distance AROUND (boundary)")
        steps.append(f"  Area measures space INSIDE (surface)")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply correct algorithm.

        Args:
            problem: The problem to solve
            verbose: If True, generate verbose steps; if False, generate concise steps (default: False)
        """
        # Extract dimensions
        l2 = problem.metadata['length2']
        w2 = problem.metadata['width2']

        # Calculate correct answer
        correct_answer = l2 * w2

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, correct_answer)
        else:
            steps = self._generate_concise_steps(problem, correct_answer)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
