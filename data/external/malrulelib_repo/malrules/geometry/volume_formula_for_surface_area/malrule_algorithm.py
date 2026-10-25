"""
Malrule algorithm for Volume-Formula-For-Surface-Area error.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class VolumeFormulaForSurfaceAreaMalrule(Malrule):
    """
    Students use volume formula V=lwh when asked for surface area.

    Example: Rectangular prism 3×4×5
    Student: V = 3×4×5 = 60 (WRONG - this is volume!)
    Correct: SA = 2(3×4 + 3×5 + 4×5) = 94
    """

    def get_name(self) -> str:
        return "Volume-Formula-For-Surface-Area"

    def _generate_concise_steps(self, problem: Problem, malrule_answer, correct_answer) -> List[str]:
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
            steps.append(f"V = s³")
            steps.append(f"V = {side}³ = {malrule_answer}")
        else:
            steps.append(f"V = l × w × h")
            steps.append(f"V = {length} × {width} × {height} = {malrule_answer}")

        steps.append(f"Answer: {malrule_answer}")
        return steps

    def _generate_verbose_steps(self, problem: Problem, malrule_answer, correct_answer) -> List[str]:
        """Generate verbose steps with full explanations (original format)."""
        template = problem.metadata.get('template', 'rectangular_prism')
        is_word_problem = problem.metadata.get('is_word_problem', False)
        length = problem.metadata['length']
        width = problem.metadata['width']
        height = problem.metadata['height']
        lw = length * width
        lh = length * height
        wh = width * height

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
            steps.append("Step 2: Apply malrule (use volume formula instead)")
            steps.append("")

        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: Use volume formula instead of surface area formula")
        steps.append(f"  MALRULE REASONING: 'I have 3 dimensions, so multiply them'")
        steps.append(f"                     'Surface area = l × w × h' (WRONG!)")
        steps.append("")

        if template == 'cube':
            side = problem.metadata['side']
            steps.append(f"Step 1: Apply WRONG formula for cube")
            steps.append(f"  Student thinks: 'Surface area of cube = s³'")
            steps.append(f"  V = s³ = {side}³ = {malrule_answer}")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT - this is VOLUME!)")
            steps.append(f"  Should use: SA = 6s² = 6×{side}² = {correct_answer} square units")
            steps.append(f"  Student confused V = s³ (volume) with SA = 6s² (surface area)")

        elif template == 'decimal_dimensions':
            steps.append(f"Step 1: Apply WRONG formula (volume instead of surface area)")
            steps.append(f"  V = l × w × h")
            steps.append(f"  V = {length} × {width} × {height}")
            steps.append(f"  V = {round(malrule_answer, 2)} cm³")
            steps.append("")
            steps.append(f"Final Answer: {round(malrule_answer, 2)} cm² (INCORRECT - this is VOLUME!)")
            steps.append(f"  Should use: SA = 2(lw + lh + wh) = {correct_answer} cm²")
            steps.append(f"  Notice: Used cm³ formula (volume) instead of cm² formula (surface area)")

        elif template == 'word_problem':
            steps.append(f"Step 1: Identify what's being asked")
            steps.append(f"  MALRULE: Student misreads 'surface area' as 'space inside'")
            steps.append(f"  Incorrectly uses: V = l × w × h")
            steps.append("")
            steps.append(f"Step 2: Apply WRONG formula")
            steps.append(f"  V = {length} × {width} × {height}")
            steps.append(f"  V = {malrule_answer}")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT - this is VOLUME!)")
            steps.append(f"  Should use: SA = 2(lw + lh + wh) = {correct_answer}")
            steps.append(f"  For wrapping/covering/painting, you need SURFACE AREA, not volume!")

        else:  # rectangular_prism, larger_dimensions
            steps.append(f"Step 1: Apply WRONG formula (volume instead of surface area)")
            steps.append(f"  V = l × w × h")
            steps.append(f"  V = {length} × {width} × {height}")
            steps.append(f"  V = {malrule_answer}")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT - this is VOLUME, not surface area!)")
            steps.append(f"  Should use: SA = 2(lw + lh + wh) = {correct_answer} square units")
            steps.append(f"  Volume measures space INSIDE (cubic units)")
            steps.append(f"  Surface area measures OUTSIDE covering (square units)")

        return steps

    def get_description(self) -> str:
        return (
            "Student incorrectly applies the volume formula (V=lwh) when asked to calculate "
            "surface area. This reflects confusion between two distinct 3D measurement concepts: "
            "volume (space inside) measured in cubic units, and surface area (total area of "
            "all faces) measured in square units."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Malrule: use volume formula V=lwh instead of surface area formula
        # Calculate volume from dimensions
        length = problem.metadata['length']
        width = problem.metadata['width']
        height = problem.metadata['height']
        return length * width * height

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply the Volume-Formula-For-Surface-Area malrule across all templates.

        Args:
            problem: Surface area problem to solve
            verbose: If True, generate verbose steps; if False, generate concise steps (default: False)

        Returns:
            Solution with incorrect answer (using volume formula)
        """
        # Extract dimensions
        length = problem.metadata['length']
        width = problem.metadata['width']
        height = problem.metadata['height']

        # Calculate volume (malrule answer) and surface area (correct answer)
        malrule_answer = length * width * height
        lw = length * width
        lh = length * height
        wh = width * height
        correct_answer = 2 * (lw + lh + wh)

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
