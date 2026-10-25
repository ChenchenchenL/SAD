"""
Correct algorithm for surface area calculation.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class SurfaceAreaCalculationCorrectAlgorithm(CorrectAlgorithm):
    """Correctly calculates surface area using SA = 2(lw + lh + wh)."""

    def get_name(self) -> str:
        return "Correct Surface Area Calculation"

    def get_description(self) -> str:
        return "Correctly calculates surface area of rectangular prism using SA = 2(lw + lh + wh)."

    def _generate_concise_steps(self, problem: Problem, correct_answer) -> List[str]:
        """Generate concise steps with only formula and values."""
        template = problem.metadata.get('template', 'rectangular_prism')
        is_word_problem = problem.metadata.get('is_word_problem', False)
        length = problem.metadata['length']
        width = problem.metadata['width']
        height = problem.metadata['height']

        steps = []
        steps.append(f"Question: {problem.text}")

        if is_word_problem:
            shape_type = problem.metadata.get('shape_type', 'rectangular_prism')
            if shape_type == 'cube':
                side = problem.metadata.get('side', length)
                steps.append(f"Shape: Cube, side = {side}")
            else:
                steps.append(f"Shape: Rectangular prism, dimensions = {length}×{width}×{height}")

        if template == 'cube':
            side = problem.metadata['side']
            steps.append(f"SA = 6s²")
            steps.append(f"SA = 6 × {side}² = 6 × {side * side} = {correct_answer}")
        else:
            lw = length * width
            lh = length * height
            wh = width * height
            steps.append(f"SA = 2(lw + lh + wh)")
            steps.append(f"SA = 2({length}×{width} + {length}×{height} + {width}×{height})")
            steps.append(f"SA = 2({lw} + {lh} + {wh}) = 2×{lw + lh + wh} = {correct_answer}")

        steps.append(f"Answer: {correct_answer} square units")
        return steps

    def _generate_verbose_steps(self, problem: Problem, correct_answer) -> List[str]:
        """Generate verbose steps with full explanations (original format)."""
        template = problem.metadata.get('template', 'rectangular_prism')
        is_word_problem = problem.metadata.get('is_word_problem', False)
        length = problem.metadata['length']
        width = problem.metadata['width']
        height = problem.metadata['height']
        lw = length * width
        lh = length * height
        wh = width * height
        volume = length * width * height

        steps = []

        # For word problems, show extraction step
        if is_word_problem:
            shape_type = problem.metadata.get('shape_type', 'rectangular_prism')
            steps.append(f"Word Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Extract information from the word problem")
            if shape_type == 'cube':
                side = problem.metadata.get('side', length)
                steps.append(f"  Shape: Cube with side {side}")
            else:
                steps.append(f"  Shape: Rectangular prism {length} × {width} × {height}")
            steps.append(f"  Question: Find surface area")
            steps.append("")
            steps.append("Step 2: Calculate surface area using correct formula")
            steps.append("")

        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD: Use surface area formula")
        steps.append("  Surface area = total area of all 6 faces")
        steps.append("")

        if template == 'cube':
            side = problem.metadata['side']
            steps.append(f"For a CUBE with side s = {side}:")
            steps.append(f"  All 6 faces are squares with area s² = {side}² = {side * side}")
            steps.append(f"  Formula: SA = 6s²")
            steps.append("")
            steps.append(f"Step 1: Calculate surface area")
            steps.append(f"  SA = 6 × {side}²")
            steps.append(f"  SA = 6 × {side * side}")
            steps.append(f"  SA = {correct_answer}")
            steps.append("")
            steps.append(f"Final Answer: {correct_answer} square units")
            steps.append("")
            steps.append(f"Comparison:")
            steps.append(f"  Surface area (SA = 6s²) = {correct_answer} square units")
            steps.append(f"  Volume (V = s³) = {side}³ = {volume} cubic units (DIFFERENT!)")

        elif template == 'decimal_dimensions':
            surface_area = round(2 * (lw + lh + wh), 2)
            steps.append(f"Formula: SA = 2(lw + lh + wh)")
            steps.append("")
            steps.append(f"Step 1: Calculate area of each pair of faces")
            steps.append(f"  Top/Bottom (lw): {length} × {width} = {lw} cm²")
            steps.append(f"  Front/Back (lh): {length} × {height} = {lh} cm²")
            steps.append(f"  Left/Right (wh): {width} × {height} = {wh} cm²")
            steps.append("")
            steps.append(f"Step 2: Sum the face areas")
            steps.append(f"  Sum = {lw} + {lh} + {wh} = {lw + lh + wh} cm²")
            steps.append("")
            steps.append(f"Step 3: Multiply by 2")
            steps.append(f"  SA = 2 × {lw + lh + wh} = {surface_area} cm²")
            steps.append("")
            steps.append(f"Final Answer: {correct_answer} cm²")
            steps.append("")
            steps.append(f"Note: Volume = {length} × {width} × {height} = {volume} cm³ (different!)")

        elif template == 'word_problem':
            steps.append(f"Identify what's needed: SURFACE AREA (covering/wrapping/painting)")
            steps.append(f"  NOT volume (filling/capacity)")
            steps.append("")
            steps.append(f"Formula: SA = 2(lw + lh + wh)")
            steps.append("")
            steps.append(f"Step 1: Calculate area of each pair of faces")
            steps.append(f"  Top/Bottom: {length} × {width} = {lw}")
            steps.append(f"  Front/Back: {length} × {height} = {lh}")
            steps.append(f"  Left/Right: {width} × {height} = {wh}")
            steps.append("")
            steps.append(f"Step 2: Sum and double")
            steps.append(f"  SA = 2({lw} + {lh} + {wh})")
            steps.append(f"  SA = 2({lw + lh + wh})")
            steps.append(f"  SA = {correct_answer}")
            steps.append("")
            steps.append(f"Final Answer: {correct_answer}")
            steps.append("")
            steps.append(f"Why not volume? Volume ({volume}) measures space INSIDE")
            steps.append(f"  Surface area ({correct_answer}) measures OUTSIDE covering")

        else:  # rectangular_prism, larger_dimensions
            surface_area = 2 * (lw + lh + wh)
            steps.append(f"Formula: SA = 2(lw + lh + wh)")
            steps.append("")
            steps.append(f"Step 1: Calculate area of each pair of faces")
            steps.append(f"  Top/Bottom faces (lw): {length} × {width} = {lw}")
            steps.append(f"  Front/Back faces (lh): {length} × {height} = {lh}")
            steps.append(f"  Left/Right faces (wh): {width} × {height} = {wh}")
            steps.append("")
            steps.append(f"Step 2: Sum the face areas")
            steps.append(f"  Sum = {lw} + {lh} + {wh} = {lw + lh + wh}")
            steps.append("")
            steps.append(f"Step 3: Multiply by 2 (each type of face appears twice)")
            steps.append(f"  SA = 2 × {lw + lh + wh} = {surface_area}")
            steps.append("")
            steps.append(f"Final Answer: {correct_answer} square units")
            steps.append("")
            steps.append(f"Comparison:")
            steps.append(f"  Surface area (SA) = {correct_answer} square units")
            steps.append(f"  Volume (V = lwh) = {volume} cubic units (DIFFERENT!)")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply correct surface area calculation across all templates.

        Args:
            problem: Surface area problem to solve
            verbose: If True, generate verbose steps; if False, generate concise steps (default: False)

        Returns:
            Solution showing correct approach
        """
        # Extract dimensions
        length = problem.metadata['length']
        width = problem.metadata['width']
        height = problem.metadata['height']

        # Calculate surface area
        lw = length * width
        lh = length * height
        wh = width * height
        correct_answer = 2 * (lw + lh + wh)

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
