"""
Malrule algorithm for Slope-Is-Delta-X-Over-Delta-Y error.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class SlopeIsDeltaXOverDeltaYMalrule(Malrule):
    """
    Students invert the slope formula, calculating Δx/Δy instead of Δy/Δx.

    Example: Points (2,3) and (5,11)
    Student: slope = (5-2)/(11-3) = 3/8 (WRONG!)
    Correct: slope = (11-3)/(5-2) = 8/3
    """

    def get_name(self) -> str:
        return "Slope-Is-Delta-X-Over-Delta-Y"

    def get_description(self) -> str:
        return (
            "Student inverts the slope formula, calculating Δx/Δy instead of Δy/Δx. "
            "This error stems from rote memorization of 'rise over run' without "
            "understanding that rise (vertical/y-change) must be in the numerator "
            "and run (horizontal/x-change) in the denominator."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        from fractions import Fraction
        # Malrule: invert the slope formula Δx/Δy instead of Δy/Δx
        x1 = problem.metadata['x1']
        y1 = problem.metadata['y1']
        x2 = problem.metadata['x2']
        y2 = problem.metadata['y2']

        delta_x = x2 - x1
        delta_y = y2 - y1

        # COMPUTE malrule answer: slope = Δx/Δy (inverted!)
        malrule_slope_fraction = Fraction(delta_x, delta_y)
        malrule_answer = self._format_fraction(malrule_slope_fraction)

        # Add units for real-world problems
        template = problem.metadata.get('template', 'basic_two_points')
        if template == 'real_world_rate' and 'context_type' in problem.metadata:
            context_type = problem.metadata['context_type']
            interpretation = self._get_interpretation(context_type)
            malrule_answer = f"{malrule_answer} {interpretation}"

        return malrule_answer

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply the Slope-Is-Delta-X-Over-Delta-Y malrule across all templates."""
        from fractions import Fraction

        template = problem.metadata.get('template', 'basic_two_points')
        x1 = problem.metadata['x1']
        y1 = problem.metadata['y1']
        x2 = problem.metadata['x2']
        y2 = problem.metadata['y2']

        # COMPUTE deltas from coordinates
        delta_x = x2 - x1
        delta_y = y2 - y1

        # COMPUTE malrule answer: slope = Δx/Δy (inverted!)
        malrule_slope_fraction = Fraction(delta_x, delta_y)
        malrule_answer = self._format_fraction(malrule_slope_fraction)

        # COMPUTE correct answer for comparison in steps
        correct_slope_fraction = Fraction(delta_y, delta_x)
        correct_answer = self._format_fraction(correct_slope_fraction)

        # Add units for real-world problems
        if template == 'real_world_rate' and 'context_type' in problem.metadata:
            context_type = problem.metadata['context_type']
            interpretation = self._get_interpretation(context_type)
            malrule_answer = f"{malrule_answer} {interpretation}"
            correct_answer = f"{correct_answer} {interpretation}"

        # Generate steps based on verbosity setting
        if verbose:
            steps = self._generate_verbose_steps(problem, template, x1, y1, x2, y2, delta_x, delta_y, malrule_answer, correct_answer)
        else:
            steps = self._generate_concise_steps(problem, template, x1, y1, x2, y2, delta_x, delta_y, malrule_answer)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _format_fraction(self, frac):
        """Format a fraction for display."""
        from fractions import Fraction
        if isinstance(frac, Fraction):
            if frac.denominator == 1:
                return str(frac.numerator)
            else:
                return f"{frac.numerator}/{frac.denominator}"
        return str(frac)

    def _get_interpretation(self, context_type):
        """Get units interpretation for real-world context."""
        interpretations = {
            'cost_per_item': 'dollars per item',
            'distance_time': 'miles per hour',
            'elevation_distance': 'feet per mile',
            'temperature_time': 'degrees per hour',
            'water_level': 'inches per minute',
            'earnings_hours': 'dollars per hour'
        }
        return interpretations.get(context_type, 'units')

    def _generate_concise_steps(self, problem, template, x1, y1, x2, y2, delta_x, delta_y, malrule_answer) -> List[str]:
        """Generate concise steps with only formula and values."""
        steps = []
        steps.append(f"Question: {problem.text}")

        if template == 'real_world_rate':
            steps.append(f"Extract: Point 1 = ({x1}, {y1}), Point 2 = ({x2}, {y2})")
            steps.append(f"Formula: m = Δx/Δy")
            steps.append(f"Calculate: Δx = {delta_x}, Δy = {delta_y}")
            steps.append(f"Slope: m = {delta_x}/{delta_y} = {malrule_answer}")
            steps.append(f"Answer: {malrule_answer}")
        else:
            steps.append(f"Given: ({x1}, {y1}) and ({x2}, {y2})")
            steps.append(f"Formula: m = Δx/Δy")
            steps.append(f"Calculate: Δx = {delta_x}, Δy = {delta_y}")
            steps.append(f"Slope: m = {delta_x}/{delta_y} = {malrule_answer}")
            steps.append(f"Answer: {malrule_answer}")

        return steps

    def _generate_verbose_steps(self, problem, template, x1, y1, x2, y2, delta_x, delta_y, malrule_answer, correct_answer) -> List[str]:
        """Generate verbose steps with full explanations."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: Invert the slope formula")
        steps.append(f"  MALRULE REASONING: 'Use the change formula'")
        steps.append(f"                     'Slope = Δx/Δy' [WRONG!]")
        steps.append("")

        if template == 'real_world_rate':
            context_type = problem.metadata.get('context_type', 'unknown')
            steps.append(f"Step 1: Identify the two data points")
            steps.append(f"  Point 1: ({x1}, {y1})")
            steps.append(f"  Point 2: ({x2}, {y2})")
            steps.append("")
            steps.append(f"Step 2: Calculate changes")
            steps.append(f"  Δx = {x2} - {x1} = {delta_x}")
            steps.append(f"  Δy = {y2} - {y1} = {delta_y}")
            steps.append("")
            steps.append(f"Step 3: Apply WRONG formula (inverted!)")
            steps.append(f"  Student thinks: 'Rate = change in x / change in y'")
            steps.append(f"  m = Δx/Δy  [WRONG - should be Δy/Δx!]")
            steps.append(f"  m = {delta_x}/{delta_y}")
            steps.append(f"  m = {malrule_answer}")
        else:
            steps.append(f"Step 1: Calculate Δx (horizontal change)")
            steps.append(f"  Δx = x₂ - x₁ = {x2} - ({x1}) = {delta_x}")
            steps.append("")
            steps.append(f"Step 2: Calculate Δy (vertical change)")
            steps.append(f"  Δy = y₂ - y₁ = {y2} - ({y1}) = {delta_y}")
            steps.append("")
            steps.append(f"Step 3: Apply WRONG formula (inverted!)")
            steps.append(f"  m = Δx/Δy  [WRONG - should be Δy/Δx!]")
            steps.append(f"  m = {delta_x}/{delta_y}")
            steps.append(f"  m = {malrule_answer}")

        steps.append("")
        steps.append(f"Final Answer: {malrule_answer} (INCORRECT - formula is inverted!)")
        steps.append(f"  Should be: Δy/Δx = {delta_y}/{delta_x} = {correct_answer}")
        steps.append(f"  'Rise over run' = VERTICAL change / HORIZONTAL change")

        return steps
