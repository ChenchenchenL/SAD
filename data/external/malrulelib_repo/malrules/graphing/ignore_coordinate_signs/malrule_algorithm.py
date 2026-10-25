"""
Malrule algorithm for Ignore-Coordinate-Signs error.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class IgnoreCoordinateSignsMalrule(Malrule):
    """
    Students ignore negative signs in coordinates, treating all values as positive.

    Example: Plot (-3, 4)
    Student: "Negative signs are confusing, I'll just use the numbers"
    Student plots: (3, 4) instead
    Correct: (-3, 4) - signs indicate direction!
    """

    def get_name(self) -> str:
        return "Ignore-Coordinate-Signs"

    def get_description(self) -> str:
        return (
            "Student ignores or misuses the signs of coordinates, treating negative values "
            "as positive (absolute values) when plotting points or identifying quadrants. "
            "Research shows students often fail to recognize that signs indicate direction "
            "on the coordinate plane."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Malrule: ignore negative signs, use absolute values
        template = problem.metadata.get('template', 'single_point_plotting')

        # For word problems, use the embedded problem type
        is_word_problem = problem.metadata.get('is_word_problem', False)
        if is_word_problem:
            template = problem.metadata.get('word_problem_type', template)

        if template == 'single_point_plotting':
            x = problem.metadata['x']
            y = problem.metadata['y']
            malrule_answer = (abs(x), abs(y))
        elif template == 'all_four_quadrants':
            # Absolute values always land in Quadrant I
            malrule_answer = "I"
        elif template == 'distance_between_points':
            x1, y1 = problem.metadata['x1'], problem.metadata['y1']
            x2, y2 = problem.metadata['x2'], problem.metadata['y2']
            malrule_answer = round(((abs(x2)-abs(x1))**2 + (abs(y2)-abs(y1))**2)**0.5, 2)
        elif template == 'midpoint_calculation':
            x1, y1 = problem.metadata['x1'], problem.metadata['y1']
            x2, y2 = problem.metadata['x2'], problem.metadata['y2']
            malrule_answer = (round((abs(x1)+abs(x2))/2, 1), round((abs(y1)+abs(y2))/2, 1))
        else:
            malrule_answer = None

        return malrule_answer

    def _generate_concise_steps(self, problem: Problem, template: str, malrule_answer, correct_answer, is_word_problem: bool, word_problem_type: str = None) -> List[str]:
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
            steps.append(f"Given: ({x}, {y})")
            steps.append(f"|{x}| = {abs(x)}, |{y}| = {abs(y)}")
            steps.append(f"Plot: ({abs(x)}, {abs(y)})")
            steps.append(f"Answer: ({abs(x)}, {abs(y)})")

        elif template == 'all_four_quadrants':
            x = problem.metadata['x']
            y = problem.metadata['y']
            steps.append(f"Given: ({x}, {y})")
            steps.append(f"(|{x}|, |{y}|) = ({abs(x)}, {abs(y)})")
            steps.append(f"({abs(x)}, {abs(y)}) -> Quadrant I")
            steps.append(f"Answer: Quadrant {malrule_answer}")

        elif template == 'distance_between_points':
            x1, y1 = problem.metadata['x1'], problem.metadata['y1']
            x2, y2 = problem.metadata['x2'], problem.metadata['y2']
            steps.append(f"Point 1: ({x1}, {y1}) -> ({abs(x1)}, {abs(y1)})")
            steps.append(f"Point 2: ({x2}, {y2}) -> ({abs(x2)}, {abs(y2)})")
            steps.append(f"d = sqrt((|x2|-|x1|)^2 + (|y2|-|y1|)^2)")
            steps.append(f"d = sqrt(({abs(x2)}-{abs(x1)})^2 + ({abs(y2)}-{abs(y1)})^2)")
            steps.append(f"d = {malrule_answer}")
            steps.append(f"Answer: {malrule_answer}")

        elif template == 'midpoint_calculation':
            x1, y1 = problem.metadata['x1'], problem.metadata['y1']
            x2, y2 = problem.metadata['x2'], problem.metadata['y2']
            steps.append(f"Point 1: ({x1}, {y1}) -> ({abs(x1)}, {abs(y1)})")
            steps.append(f"Point 2: ({x2}, {y2}) -> ({abs(x2)}, {abs(y2)})")
            steps.append(f"M = ((|x1|+|x2|)/2, (|y1|+|y2|)/2)")
            steps.append(f"M = (({abs(x1)}+{abs(x2)})/2, ({abs(y1)}+{abs(y2)})/2)")
            steps.append(f"M = {malrule_answer}")
            steps.append(f"Answer: {malrule_answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, template: str, malrule_answer, correct_answer, is_word_problem: bool, word_problem_type: str = None) -> List[str]:
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

        steps.append("MALRULE: Ignore negative signs - just use the numbers")
        steps.append(f"  MALRULE REASONING: 'Negative signs are confusing, just use the numbers'")
        steps.append("")

        if template == 'single_point_plotting':
            x = problem.metadata['x']
            y = problem.metadata['y']
            if is_word_problem:
                steps.append(f"Step 2: Look at coordinates ({x}, {y})")
            else:
                steps.append(f"Step 1: Look at coordinates ({x}, {y})")
            steps.append(f"  Student ignores signs: '{abs(x)}' and '{abs(y)}'")
            steps.append(f"  Student plots: ({abs(x)}, {abs(y)})")
            steps.append("")
            steps.append(f"Final Answer: ({abs(x)}, {abs(y)}) (INCORRECT!)")
            steps.append(f"  Correct: ({x}, {y}) - signs show DIRECTION")

        elif template == 'all_four_quadrants':
            x = problem.metadata['x']
            y = problem.metadata['y']
            if is_word_problem:
                steps.append(f"Step 2: Student looks at ({x}, {y})")
            else:
                steps.append(f"Step 1: Student looks at ({x}, {y})")
            steps.append(f"  Ignores signs → thinks it's ({abs(x)}, {abs(y)})")
            steps.append(f"  ({abs(x)}, {abs(y)}) is always in Quadrant I")
            steps.append("")
            steps.append(f"Final Answer: Quadrant {malrule_answer} (INCORRECT!)")
            steps.append(f"  Correct: Quadrant {correct_answer}")

        elif template == 'distance_between_points':
            x1, y1 = problem.metadata['x1'], problem.metadata['y1']
            x2, y2 = problem.metadata['x2'], problem.metadata['y2']
            if is_word_problem:
                steps.append(f"Step 2: Student uses absolute values")
            else:
                steps.append(f"Step 1: Student uses absolute values")
            steps.append(f"  Point 1: ({x1}, {y1}) → ({abs(x1)}, {abs(y1)})")
            steps.append(f"  Point 2: ({x2}, {y2}) → ({abs(x2)}, {abs(y2)})")
            steps.append(f"  Distance with abs values = {malrule_answer}")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT!)")
            steps.append(f"  Correct: {correct_answer}")

        elif template == 'midpoint_calculation':
            x1, y1 = problem.metadata['x1'], problem.metadata['y1']
            x2, y2 = problem.metadata['x2'], problem.metadata['y2']
            if is_word_problem:
                steps.append(f"Step 2: Student uses absolute values")
            else:
                steps.append(f"Step 1: Student uses absolute values")
            steps.append(f"  Midpoint of (|{x1}|, |{y1}|) and (|{x2}|, |{y2}|)")
            steps.append(f"  = {malrule_answer}")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT!)")
            steps.append(f"  Correct: {correct_answer}")

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply the Ignore-Coordinate-Signs malrule across all templates."""
        template = problem.metadata.get('template', 'single_point_plotting')

        # For word problems, use the embedded problem type
        is_word_problem = problem.metadata.get('is_word_problem', False)
        if is_word_problem:
            template = problem.metadata.get('word_problem_type', template)

        # Compute malrule_answer based on template (using absolute values)
        if template == 'single_point_plotting':
            x = problem.metadata['x']
            y = problem.metadata['y']
            malrule_answer = (abs(x), abs(y))
            correct_answer = (x, y)
        elif template == 'all_four_quadrants':
            x = problem.metadata['x']
            y = problem.metadata['y']
            # Absolute values always land in Quadrant I
            malrule_answer = "I"
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
            malrule_answer = round(((abs(x2)-abs(x1))**2 + (abs(y2)-abs(y1))**2)**0.5, 2)
            correct_answer = round(((x2-x1)**2 + (y2-y1)**2)**0.5, 2)
        elif template == 'midpoint_calculation':
            x1, y1 = problem.metadata['x1'], problem.metadata['y1']
            x2, y2 = problem.metadata['x2'], problem.metadata['y2']
            malrule_answer = (round((abs(x1)+abs(x2))/2, 1), round((abs(y1)+abs(y2))/2, 1))
            correct_answer = (round((x1+x2)/2, 1), round((y1+y2)/2, 1))
        else:
            malrule_answer = None
            correct_answer = None

        # Get word problem metadata
        word_problem_type = problem.metadata.get('word_problem_type', None)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, template, malrule_answer, correct_answer, is_word_problem, word_problem_type)
        else:
            steps = self._generate_concise_steps(problem, template, malrule_answer, correct_answer, is_word_problem, word_problem_type)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
