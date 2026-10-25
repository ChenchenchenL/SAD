"""
Correct algorithm for slope calculation.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class SlopeCalculationCorrectAlgorithm(CorrectAlgorithm):
    """Correctly calculates slope using m = Δy/Δx = (y₂-y₁)/(x₂-x₁)."""

    def get_name(self) -> str:
        return "Correct Slope Calculation"

    def get_description(self) -> str:
        return "Correctly calculates slope using m = Δy/Δx = (y₂-y₁)/(x₂-x₁)."

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply correct slope calculation across all templates."""
        from fractions import Fraction

        template = problem.metadata.get('template', 'basic_two_points')
        x1 = problem.metadata['x1']
        y1 = problem.metadata['y1']
        x2 = problem.metadata['x2']
        y2 = problem.metadata['y2']

        # COMPUTE deltas and slope from coordinates
        delta_x = x2 - x1
        delta_y = y2 - y1

        # COMPUTE correct answer: slope = Δy/Δx
        slope_fraction = Fraction(delta_y, delta_x)
        correct_answer = self._format_fraction(slope_fraction)

        # COMPUTE malrule answer: slope = Δx/Δy (inverted!)
        malrule_slope_fraction = Fraction(delta_x, delta_y)
        malrule_answer = self._format_fraction(malrule_slope_fraction)

        # Add units for real-world problems
        if template == 'real_world_rate' and 'context_type' in problem.metadata:
            # Extract interpretation from problem text or use default
            # Parse problem metadata for interpretation hints
            context_type = problem.metadata['context_type']
            interpretation = self._get_interpretation(context_type)
            correct_answer = f"{correct_answer} {interpretation}"
            malrule_answer = f"{malrule_answer} {interpretation}"

        # Generate steps based on verbosity setting
        if verbose:
            steps = self._generate_verbose_steps(problem, template, x1, y1, x2, y2, delta_x, delta_y, correct_answer, malrule_answer)
        else:
            steps = self._generate_concise_steps(problem, template, x1, y1, x2, y2, delta_x, delta_y, correct_answer)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
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

    def _generate_concise_steps(self, problem, template, x1, y1, x2, y2, delta_x, delta_y, correct_answer) -> List[str]:
        """Generate concise steps with only formula and values."""
        steps = []
        steps.append(f"Question: {problem.text}")

        if template == 'real_world_rate':
            steps.append(f"Extract: Point 1 = ({x1}, {y1}), Point 2 = ({x2}, {y2})")
            steps.append(f"Formula: m = Δy/Δx = (y₂-y₁)/(x₂-x₁)")
            steps.append(f"Calculate: Δy = {y2} - {y1} = {delta_y}, Δx = {x2} - {x1} = {delta_x}")
            steps.append(f"Slope: m = {delta_y}/{delta_x} = {correct_answer}")
            steps.append(f"Answer: {correct_answer}")
        else:
            steps.append(f"Given: ({x1}, {y1}) and ({x2}, {y2})")
            steps.append(f"Formula: m = Δy/Δx = (y₂-y₁)/(x₂-x₁)")
            steps.append(f"Calculate: Δy = {delta_y}, Δx = {delta_x}")
            steps.append(f"Slope: m = {delta_y}/{delta_x} = {correct_answer}")
            steps.append(f"Answer: {correct_answer}")

        return steps

    def _generate_verbose_steps(self, problem, template, x1, y1, x2, y2, delta_x, delta_y, correct_answer, malrule_answer) -> List[str]:
        """Generate verbose steps with full explanations."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD: Use slope formula m = Δy/Δx")
        steps.append("  'Rise over run' = vertical change / horizontal change")
        steps.append("  Formula: m = (y₂ - y₁)/(x₂ - x₁)")
        steps.append("")

        if template == 'real_world_rate':
            context_type = problem.metadata.get('context_type', 'unknown')
            steps.append(f"Step 1: Identify the two data points")
            steps.append(f"  Point 1: ({x1}, {y1})")
            steps.append(f"  Point 2: ({x2}, {y2})")
            steps.append("")
            steps.append(f"Step 2: Calculate Δy (vertical change - RISE)")
            steps.append(f"  Δy = y₂ - y₁")
            steps.append(f"  Δy = {y2} - {y1}")
            steps.append(f"  Δy = {delta_y}")
            steps.append("")
            steps.append(f"Step 3: Calculate Δx (horizontal change - RUN)")
            steps.append(f"  Δx = x₂ - x₁")
            steps.append(f"  Δx = {x2} - {x1}")
            steps.append(f"  Δx = {delta_x}")
            steps.append("")
            steps.append(f"Step 4: Calculate slope using CORRECT formula")
            steps.append(f"  m = Δy/Δx  [Rise over run!]")
            steps.append(f"  m = {delta_y}/{delta_x}")
            steps.append(f"  m = {correct_answer}")
        else:
            steps.append(f"Step 1: Calculate Δy (vertical change - RISE)")
            steps.append(f"  Δy = y₂ - y₁")
            steps.append(f"  Δy = {y2} - ({y1})")
            steps.append(f"  Δy = {delta_y}")
            steps.append("")
            steps.append(f"Step 2: Calculate Δx (horizontal change - RUN)")
            steps.append(f"  Δx = x₂ - x₁")
            steps.append(f"  Δx = {x2} - ({x1})")
            steps.append(f"  Δx = {delta_x}")
            steps.append("")
            steps.append(f"Step 3: Calculate slope using CORRECT formula")
            steps.append(f"  m = Δy/Δx  [Rise over run!]")
            steps.append(f"  m = {delta_y}/{delta_x}")
            steps.append(f"  m = {correct_answer}")

        steps.append("")
        steps.append(f"Final Answer: {correct_answer} ✓")
        steps.append("")
        steps.append(f"Key concept: Rise over run = VERTICAL/HORIZONTAL = Δy/Δx")
        steps.append(f"  NOT Δx/Δy (which would be {malrule_answer}) ✗")
        steps.append(f"  Remember: y values go in the NUMERATOR!")

        return steps
