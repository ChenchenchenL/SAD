"""
Malrule algorithm for Count-Net-Perimeter-As-Surface-Area error.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class CountNetPerimeterAsSurfaceAreaMalrule(Malrule):
    """
    Students confuse perimeter with area when working with 3D nets.
    When given a net (unfolded 3D shape), they calculate the perimeter
    around the outside of the net instead of calculating the surface area.

    Example: Cube with side 3
    Student: Net perimeter = 12×3 = 36 (WRONG - this is perimeter!)
    Correct: Surface area = 6×(3²) = 54
    """

    def get_name(self) -> str:
        return "Count-Net-Perimeter-As-Surface-Area"

    def _generate_concise_steps(self, problem: Problem, malrule_answer, correct_surface_area) -> List[str]:
        """Generate concise steps with only formula and values."""
        shape_type = problem.metadata['shape_type']
        is_word_problem = problem.metadata.get('is_word_problem', False)

        steps = []
        steps.append(f"Question: {problem.text}")

        # Formula extraction step for word problem
        if is_word_problem:
            if shape_type == 'cube':
                side = problem.metadata['side']
                steps.append(f"Shape: Cube, side = {side}")
            elif shape_type == 'rectangular_prism':
                length = problem.metadata['length']
                width = problem.metadata['width']
                height = problem.metadata['height']
                steps.append(f"Shape: Rectangular prism, dimensions = {length}×{width}×{height}")
            elif shape_type == 'triangular_prism':
                base = problem.metadata['base']
                height_triangle = problem.metadata['height_triangle']
                length = problem.metadata['length']
                steps.append(f"Shape: Triangular prism, base = {base}, height = {height_triangle}, length = {length}")
            elif shape_type == 'pyramid':
                base_side = problem.metadata['base_side']
                slant_height = problem.metadata['slant_height']
                steps.append(f"Shape: Pyramid, base side = {base_side}, slant height = {slant_height}")

        # Malrule calculation steps based on shape type
        if shape_type == 'cube':
            side = problem.metadata['side']
            steps.append(f"Perimeter = 12 × side")
            steps.append(f"Perimeter = 12 × {side} = {malrule_answer}")
        elif shape_type == 'rectangular_prism':
            length = problem.metadata['length']
            width = problem.metadata['width']
            height = problem.metadata['height']
            steps.append(f"Perimeter = 4(l + w + h)")
            steps.append(f"Perimeter = 4({length} + {width} + {height}) = {malrule_answer}")
        elif shape_type == 'triangular_prism':
            steps.append(f"Net perimeter = {malrule_answer}")
        elif shape_type == 'pyramid':
            base_side = problem.metadata['base_side']
            slant_height = problem.metadata['slant_height']
            steps.append(f"Net perimeter = 4×{slant_height} + 4×{base_side}")
            steps.append(f"Net perimeter = {malrule_answer}")

        steps.append(f"Answer: {malrule_answer})")
        return steps

    def _generate_verbose_steps(self, problem: Problem, malrule_answer, correct_surface_area) -> List[str]:
        """Generate verbose steps with full explanations (original format)."""
        shape_type = problem.metadata['shape_type']
        template = problem.metadata.get('template', 'cube_net')
        is_word_problem = problem.metadata.get('is_word_problem', False)

        steps = []

        # For word problems, show extraction step
        if is_word_problem:
            steps.append(f"Word Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Extract information from the word problem")
            steps.append(f"  Shape type: {shape_type}")
            if shape_type == 'cube':
                side = problem.metadata['side']
                steps.append(f"  Side length: {side}")
            elif shape_type == 'rectangular_prism':
                length = problem.metadata['length']
                width = problem.metadata['width']
                height = problem.metadata['height']
                steps.append(f"  Dimensions: {length}×{width}×{height}")
            elif shape_type == 'triangular_prism':
                base = problem.metadata['base']
                height_triangle = problem.metadata['height_triangle']
                length = problem.metadata['length']
                steps.append(f"  Base: {base}, Triangle height: {height_triangle}, Length: {length}")
            elif shape_type == 'pyramid':
                base_side = problem.metadata['base_side']
                slant_height = problem.metadata['slant_height']
                steps.append(f"  Base side: {base_side}, Slant height: {slant_height}")
            steps.append("")
            steps.append("Step 2: Apply malrule (measure perimeter instead of surface area)")
            steps.append("")
        else:
            steps.append(f"Problem: {problem.text[:80]}...")
            steps.append("")

        steps.append("MALRULE: Measure perimeter of net instead of calculating surface area")
        steps.append(f"  MALRULE REASONING: 'I need to measure around the edge of this flat shape'")
        steps.append(f"                     'I'll find the perimeter of the net'")
        steps.append("")

        if shape_type == 'cube':
            side = problem.metadata['side']
            steps.append(f"Step 1: Identify the net shape")
            steps.append(f"  Cube side length = {side}")
            steps.append(f"  A cross-shaped cube net has 12 edge segments on its perimeter")
            steps.append(f"Step 2: MALRULE calculates perimeter instead of surface area")
            steps.append(f"  Perimeter = 12 × {side} = {malrule_answer}")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT - this is PERIMETER, not surface area!)")
            steps.append(f"  Should calculate: SA = 6 × ({side}²) = {correct_surface_area} square units")

        elif shape_type == 'rectangular_prism':
            length = problem.metadata['length']
            width = problem.metadata['width']
            height = problem.metadata['height']
            lw = length * width
            lh = length * height
            wh = width * height
            steps.append(f"Step 1: Identify dimensions")
            steps.append(f"  Dimensions: {length}×{width}×{height}")
            steps.append(f"Step 2: MALRULE calculates net perimeter instead of surface area")
            steps.append(f"  Perimeter = 4 × (length + width + height)")
            steps.append(f"  Perimeter = 4 × ({length} + {width} + {height}) = {malrule_answer}")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT - this is PERIMETER, not surface area!)")
            steps.append(f"  Should calculate: SA = 2({length}×{width} + {length}×{height} + {width}×{height}) = {correct_surface_area}")

        elif shape_type == 'triangular_prism':
            base = problem.metadata['base']
            height_triangle = problem.metadata['height_triangle']
            length = problem.metadata['length']
            steps.append(f"Step 1: Identify triangular prism dimensions")
            steps.append(f"  Base: {base}, Triangle height: {height_triangle}, Length: {length}")
            steps.append(f"Step 2: MALRULE measures net perimeter instead of surface area")
            steps.append(f"  Net perimeter ≈ {malrule_answer}")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT - this is PERIMETER, not surface area!)")
            steps.append(f"  Should calculate: SA = 2(triangle areas) + 3(rectangle areas) = {correct_surface_area}")

        elif shape_type == 'pyramid':
            base_side = problem.metadata['base_side']
            slant_height = problem.metadata['slant_height']
            steps.append(f"Step 1: Identify pyramid dimensions")
            steps.append(f"  Base side: {base_side}, Slant height: {slant_height}")
            steps.append(f"Step 2: MALRULE measures net perimeter instead of surface area")
            steps.append(f"  Net perimeter = 4×{slant_height} + 4×{base_side} = {malrule_answer}")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT - this is PERIMETER, not surface area!)")
            steps.append(f"  Should calculate: SA = base² + 4(triangle areas) = {correct_surface_area}")

        if template == 'word_problem_context':
            context_type = problem.metadata.get('context_type', 'box')
            steps.append("")
            steps.append(f"Note: This {context_type} problem requires AREA (square units), not perimeter (linear units)")

        steps.append("")
        steps.append(f"Perimeter measures LENGTH (linear units)")
        steps.append(f"Surface area measures AREA (square units)")

        return steps

    def get_description(self) -> str:
        return (
            "Student incorrectly calculates the perimeter around the outside edge of a net "
            "(unfolded 3D shape) instead of calculating the total surface area. This reflects "
            "confusion between linear measurement (perimeter) and area measurement, as well as "
            "difficulty transitioning between 2D nets and 3D spatial understanding."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Malrule: calculate net perimeter instead of surface area
        shape_type = problem.metadata['shape_type']

        if shape_type == 'cube':
            side = problem.metadata['side']
            return 12 * side
        elif shape_type == 'rectangular_prism':
            length = problem.metadata['length']
            width = problem.metadata['width']
            height = problem.metadata['height']
            return 4 * (length + width + height)
        else:
            # For complex shapes, use stored value
            return problem.metadata['net_perimeter']

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply malrule across all templates.

        Args:
            problem: The problem to solve
            verbose: If True, generate verbose steps; if False, generate concise steps (default: False)
        """
        shape_type = problem.metadata['shape_type']

        # Calculate net perimeter based on shape type
        if shape_type == 'cube':
            side = problem.metadata['side']
            net_perimeter = 12 * side
            correct_surface_area = 6 * (side ** 2)
        elif shape_type == 'rectangular_prism':
            length = problem.metadata['length']
            width = problem.metadata['width']
            height = problem.metadata['height']
            net_perimeter = 4 * (length + width + height)
            lw = length * width
            lh = length * height
            wh = width * height
            correct_surface_area = 2 * (lw + lh + wh)
        elif shape_type == 'triangular_prism':
            # Use stored values (complex calculation)
            net_perimeter = problem.metadata['net_perimeter']
            correct_surface_area = problem.metadata['surface_area']
        elif shape_type == 'pyramid':
            base_side = problem.metadata['base_side']
            slant_height = problem.metadata['slant_height']
            net_perimeter = 4 * slant_height + 4 * base_side
            base_area = base_side ** 2
            triangle_area = 0.5 * base_side * slant_height
            correct_surface_area = base_area + 4 * triangle_area
        else:
            net_perimeter = problem.metadata['net_perimeter']
            correct_surface_area = problem.metadata.get('surface_area', problem.metadata.get('correct_answer'))

        malrule_answer = net_perimeter

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, malrule_answer, correct_surface_area)
        else:
            steps = self._generate_concise_steps(problem, malrule_answer, correct_surface_area)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
