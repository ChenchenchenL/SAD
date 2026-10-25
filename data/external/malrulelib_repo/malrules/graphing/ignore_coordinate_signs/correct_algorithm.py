"""
Correct algorithm for coordinate plotting with signs.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class CoordinatePlottingWithSignsCorrectAlgorithm(CorrectAlgorithm):
    """Correctly plots coordinates respecting negative signs as directions."""

    def get_name(self) -> str:
        return "Correct Coordinate Plotting with Signs"

    def get_description(self) -> str:
        return "Correctly plots coordinates using signs to indicate direction (left/right, up/down)."

    def _generate_concise_steps(self, problem: Problem, template: str, correct_answer, is_word_problem: bool, word_problem_type: str = None) -> List[str]:
        """Generate concise steps with only formula and values."""
        steps = []

        # Question
        if is_word_problem:
            steps.append(f"Word Problem: {problem.text}")
            steps.append(f"Problem type: {word_problem_type}")
        else:
            steps.append(f"Problem: {problem.text}")

        if template == 'single_point_plotting':
            x = problem.metadata['x']
            y = problem.metadata['y']
            steps.append(f"x = {x}, y = {y}")
            steps.append(f"Plot: ({x}, {y})")
            steps.append(f"Answer: ({x}, {y})")

        elif template == 'all_four_quadrants':
            x = problem.metadata['x']
            y = problem.metadata['y']
            steps.append(f"Point: ({x}, {y})")
            steps.append(f"x = {x} ({'positive' if x >= 0 else 'negative'}), y = {y} ({'positive' if y >= 0 else 'negative'})")
            steps.append(f"Answer: Quadrant {correct_answer}")

        elif template == 'distance_between_points':
            x1, y1 = problem.metadata['x1'], problem.metadata['y1']
            x2, y2 = problem.metadata['x2'], problem.metadata['y2']
            dx = problem.metadata['dx']
            dy = problem.metadata['dy']
            steps.append(f"Point 1: ({x1}, {y1}), Point 2: ({x2}, {y2})")
            steps.append(f"d = sqrt((x2-x1)^2 + (y2-y1)^2)")
            steps.append(f"d = sqrt(({x2}-({x1}))^2 + ({y2}-({y1}))^2)")
            steps.append(f"d = sqrt({dx}^2 + {dy}^2) = {correct_answer}")
            steps.append(f"Answer: {correct_answer}")

        elif template == 'midpoint_calculation':
            x1, y1 = problem.metadata['x1'], problem.metadata['y1']
            x2, y2 = problem.metadata['x2'], problem.metadata['y2']
            steps.append(f"Point 1: ({x1}, {y1}), Point 2: ({x2}, {y2})")
            steps.append(f"M = ((x1+x2)/2, (y1+y2)/2)")
            steps.append(f"M = (({x1}+{x2})/2, ({y1}+{y2})/2)")
            steps.append(f"M = {correct_answer}")
            steps.append(f"Answer: {correct_answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, template: str, correct_answer, is_word_problem: bool, word_problem_type: str = None) -> List[str]:
        """Generate verbose steps with full explanations (original format)."""
        steps = []

        # For word problems, show extraction step first
        if is_word_problem:
            steps.append(f"Word Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Extract the coordinate problem from the word problem")
            steps.append(f"  Problem type: {word_problem_type}")
            steps.append("")
        else:
            steps.append(f"Problem: {problem.text}")
            steps.append("")

        steps.append("CORRECT METHOD: Signs indicate DIRECTION")
        steps.append("")

        if template == 'single_point_plotting':
            x = problem.metadata['x']
            y = problem.metadata['y']
            if is_word_problem:
                steps.append(f"Step 2: Interpret signs as directions")
            else:
                steps.append(f"Step 1: Interpret signs as directions")
            steps.append(f"  x = {x} → {'RIGHT' if x >= 0 else 'LEFT'} {abs(x)} units")
            steps.append(f"  y = {y} → {'UP' if y >= 0 else 'DOWN'} {abs(y)} units")
            steps.append("")
            steps.append(f"Final Answer: ({x}, {y}) ✓")

        elif template == 'all_four_quadrants':
            x = problem.metadata['x']
            y = problem.metadata['y']
            if is_word_problem:
                steps.append(f"Step 2: Determine quadrant using signs")
            else:
                steps.append(f"Step 1: Determine quadrant using signs")
            steps.append(f"  x = {x}, y = {y}")
            steps.append(f"  Quadrant {correct_answer}")
            steps.append("")
            steps.append(f"Final Answer: Quadrant {correct_answer} ✓")

        elif template == 'distance_between_points':
            x1, y1 = problem.metadata['x1'], problem.metadata['y1']
            x2, y2 = problem.metadata['x2'], problem.metadata['y2']
            dx = problem.metadata['dx']
            dy = problem.metadata['dy']
            if is_word_problem:
                steps.append(f"Step 2: Use actual coordinates (with signs)")
            else:
                steps.append(f"Step 1: Use actual coordinates (with signs)")
            steps.append(f"  Δx = {x2} - ({x1}) = {dx}")
            steps.append(f"  Δy = {y2} - ({y1}) = {dy}")
            steps.append(f"  Distance = √(({dx})² + ({dy})²) = {correct_answer}")
            steps.append("")
            steps.append(f"Final Answer: {correct_answer} ✓")

        elif template == 'midpoint_calculation':
            x1, y1 = problem.metadata['x1'], problem.metadata['y1']
            x2, y2 = problem.metadata['x2'], problem.metadata['y2']
            if is_word_problem:
                steps.append(f"Step 2: Use actual coordinates (with signs)")
            else:
                steps.append(f"Step 1: Use actual coordinates (with signs)")
            steps.append(f"  Midpoint = (({x1}+{x2})/2, ({y1}+{y2})/2)")
            steps.append(f"  = {correct_answer}")
            steps.append("")
            steps.append(f"Final Answer: {correct_answer} ✓")

        steps.append("")
        steps.append("Remember: Signs indicate DIRECTION, not values to ignore!")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply correct coordinate handling across all templates."""
        template = problem.metadata.get('template', 'single_point_plotting')

        # For word problems, use the embedded problem type
        is_word_problem = problem.metadata.get('is_word_problem', False)
        if is_word_problem:
            template = problem.metadata.get('word_problem_type', template)

        # Compute correct_answer based on template
        if template == 'single_point_plotting':
            x = problem.metadata['x']
            y = problem.metadata['y']
            correct_answer = (x, y)
        elif template == 'all_four_quadrants':
            x = problem.metadata['x']
            y = problem.metadata['y']
            # Determine quadrant based on x, y signs
            if x >= 0 and y >= 0:
                correct_answer = "I"
            elif x < 0 and y >= 0:
                correct_answer = "II"
            elif x < 0 and y < 0:
                correct_answer = "III"
            else:  # x >= 0 and y < 0
                correct_answer = "IV"
        elif template == 'distance_between_points':
            x1, y1 = problem.metadata['x1'], problem.metadata['y1']
            x2, y2 = problem.metadata['x2'], problem.metadata['y2']
            correct_answer = round(((x2-x1)**2 + (y2-y1)**2)**0.5, 2)
        elif template == 'midpoint_calculation':
            x1, y1 = problem.metadata['x1'], problem.metadata['y1']
            x2, y2 = problem.metadata['x2'], problem.metadata['y2']
            correct_answer = (round((x1+x2)/2, 1), round((y1+y2)/2, 1))
        else:
            correct_answer = None

        # Get word problem metadata
        word_problem_type = problem.metadata.get('word_problem_type', None)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, template, correct_answer, is_word_problem, word_problem_type)
        else:
            steps = self._generate_concise_steps(problem, template, correct_answer, is_word_problem, word_problem_type)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
