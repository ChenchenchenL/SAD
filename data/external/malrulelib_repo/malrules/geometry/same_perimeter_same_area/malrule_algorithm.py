"""
Malrule algorithm for Same-Perimeter-Same-Area error.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class SamePerimeterSameAreaMalrule(Malrule):
    """
    Students think same perimeter means same area.

    Example: Two rectangles with perimeter 10
    Student: "Same perimeter, so same area"
    Correct: Different dimensions = different areas
    """

    def get_name(self) -> str:
        return "Same-Perimeter-Same-Area"

    def _generate_concise_steps(self, problem: Problem, malrule_answer, correct_answer) -> List[str]:
        """Generate concise steps with only formula and values."""
        l1 = problem.metadata['length1']
        w1 = problem.metadata['width1']
        is_word_problem = problem.metadata.get('is_word_problem', False)

        steps = []
        steps.append(f"Question: {problem.text}")

        if is_word_problem:
            l2 = problem.metadata['length2']
            w2 = problem.metadata['width2']
            steps.append(f"Rectangle A: {l1} × {w1}, Rectangle B: {l2} × {w2}")

        steps.append(f"Same perimeter = same area")
        steps.append(f"Area B = Area A = {l1} × {w1} = {malrule_answer}")
        steps.append(f"Answer: {malrule_answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, malrule_answer, correct_answer) -> List[str]:
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
            steps.append("Step 2: Apply malrule (same perimeter = same area)")
            steps.append("")
        else:
            steps.append(f"Problem: Rectangle A: {l1}×{w1}, Rectangle B: {l2}×{w2}")
            steps.append(f"Both have same perimeter. Find area of Rectangle B.")
            steps.append("")

        steps.append("MALRULE: Same perimeter means same area")
        steps.append(f"  MALRULE REASONING: 'Same perimeter = same area'")
        steps.append(f"                     'If distance around is same, inside space is same'")
        steps.append("")
        steps.append(f"Step 1: Calculate area of Rectangle A")
        steps.append(f"  Area A = {l1} × {w1} = {area1}")
        steps.append("")
        steps.append(f"Step 2: Apply malrule - same perimeter means same area")
        steps.append(f"  Both rectangles have perimeter {perimeter1}")
        steps.append(f"  So Area B = Area A = {malrule_answer}")
        steps.append("")
        steps.append(f"Final Answer: {malrule_answer} (INCORRECT - perimeter does not equal area!)")
        steps.append(f"  Should calculate: {l2} × {w2} = {area2}")

        return steps

    def get_description(self) -> str:
        return (
            "Student incorrectly believes that figures having the same perimeter must also "
            "have the same area. This misconception reflects a failure to understand that "
            "perimeter (boundary length) and area (enclosed surface) are independent measures "
            "that can vary independently of each other."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Malrule: same perimeter means same area (return area of first shape)
        l1 = problem.metadata['length1']
        w1 = problem.metadata['width1']
        return l1 * w1

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply malrule.

        Args:
            problem: The problem to solve
            verbose: If True, generate verbose steps; if False, generate concise steps (default: False)
        """
        # Extract dimensions
        l1 = problem.metadata['length1']
        w1 = problem.metadata['width1']
        l2 = problem.metadata['length2']
        w2 = problem.metadata['width2']

        # Calculate answers
        malrule_answer = l1 * w1  # Using area of first rectangle
        correct_answer = l2 * w2  # Actual correct answer

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, malrule_answer, correct_answer)
        else:
            steps = self._generate_concise_steps(problem, malrule_answer, correct_answer)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
