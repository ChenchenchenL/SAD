"""
Correct algorithm for calculating surface area from a net.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class NetSurfaceAreaCorrectAlgorithm(CorrectAlgorithm):
    """Correctly calculates surface area by finding area of each face and adding them."""

    def get_name(self) -> str:
        return "Correct Net Surface Area Calculation"

    def get_description(self) -> str:
        return "Correctly calculates surface area from a net by finding the area of each face and adding them together."

    def _generate_concise_steps(self, problem: Problem, correct_answer) -> List[str]:
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

        # Calculation steps based on shape type
        if shape_type == 'cube':
            side = problem.metadata['side']
            face_area = side ** 2
            steps.append(f"SA = 6 × side²")
            steps.append(f"SA = 6 × {side}² = 6 × {face_area} = {correct_answer}")
        elif shape_type == 'rectangular_prism':
            length = problem.metadata['length']
            width = problem.metadata['width']
            height = problem.metadata['height']
            lw = length * width
            lh = length * height
            wh = width * height
            steps.append(f"SA = 2(lw + lh + wh)")
            steps.append(f"SA = 2({length}×{width} + {length}×{height} + {width}×{height})")
            steps.append(f"SA = 2({lw} + {lh} + {wh}) = 2×{lw + lh + wh} = {correct_answer}")
        elif shape_type == 'triangular_prism':
            base = problem.metadata['base']
            height_triangle = problem.metadata['height_triangle']
            triangle_area = problem.metadata['triangle_area']
            steps.append(f"Triangle area = ½×{base}×{height_triangle} = {triangle_area}")
            steps.append(f"SA = 2×triangle + rectangular faces = {correct_answer}")
        elif shape_type == 'pyramid':
            base_side = problem.metadata['base_side']
            slant_height = problem.metadata['slant_height']
            base_area = base_side ** 2
            triangle_area = 0.5 * base_side * slant_height
            steps.append(f"Base area = {base_side}² = {base_area}")
            steps.append(f"Triangle area = ½×{base_side}×{slant_height} = {triangle_area}")
            steps.append(f"SA = {base_area} + 4×{triangle_area} = {correct_answer}")

        steps.append(f"Answer: {correct_answer} square units")
        return steps

    def _generate_verbose_steps(self, problem: Problem, correct_answer) -> List[str]:
        """Generate verbose steps with full explanations (original format)."""
        shape_type = problem.metadata['shape_type']
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
            steps.append("Step 2: Calculate surface area")
            steps.append("")
        else:
            steps.append(f"Problem: {problem.text[:80]}...")
            steps.append("")

        steps.append("CORRECT METHOD: Calculate area of each face, then add them")
        steps.append("")

        if shape_type == 'cube':
            side = problem.metadata['side']
            face_area = side ** 2
            surface_area = 6 * face_area
            steps.append(f"Step 1: Identify shape - Cube with side length {side}")
            steps.append(f"  A cube has 6 faces, each is a square")
            steps.append(f"Step 2: Calculate area of one face")
            steps.append(f"  Face area = side² = {side}² = {face_area}")
            steps.append(f"Step 3: Multiply by number of faces")
            steps.append(f"  SA = 6 × {face_area} = {surface_area}")

        elif shape_type == 'rectangular_prism':
            length = problem.metadata['length']
            width = problem.metadata['width']
            height = problem.metadata['height']
            lw = length * width
            lh = length * height
            wh = width * height
            surface_area = 2 * (lw + lh + wh)
            steps.append(f"Step 1: Identify dimensions - {length}×{width}×{height}")
            steps.append(f"  A rectangular prism has 6 faces (3 pairs)")
            steps.append(f"Step 2: Calculate each pair of face areas")
            steps.append(f"  Top/Bottom: {length}×{width} = {lw}")
            steps.append(f"  Front/Back: {length}×{height} = {lh}")
            steps.append(f"  Left/Right: {width}×{height} = {wh}")
            steps.append(f"Step 3: Add all faces (each type appears twice)")
            steps.append(f"  SA = 2({lw} + {lh} + {wh}) = 2×{lw + lh + wh} = {surface_area}")

        elif shape_type == 'triangular_prism':
            base = problem.metadata['base']
            height_triangle = problem.metadata['height_triangle']
            length = problem.metadata['length']
            triangle_area = problem.metadata['triangle_area']
            surface_area = problem.metadata['surface_area']
            steps.append(f"Step 1: Identify triangular prism")
            steps.append(f"  Base: {base}, Triangle height: {height_triangle}, Length: {length}")
            steps.append(f"Step 2: Calculate 2 triangular end faces")
            steps.append(f"  Triangle area = ½×base×height = ½×{base}×{height_triangle} = {triangle_area}")
            steps.append(f"  Two triangles: 2×{triangle_area} = {2*triangle_area}")
            steps.append(f"Step 3: Add 3 rectangular side faces + triangular ends")
            steps.append(f"  SA = {surface_area}")

        elif shape_type == 'pyramid':
            base_side = problem.metadata['base_side']
            slant_height = problem.metadata['slant_height']
            base_area = base_side ** 2
            triangle_area = 0.5 * base_side * slant_height
            surface_area = base_area + 4 * triangle_area
            steps.append(f"Step 1: Identify square pyramid")
            steps.append(f"  Base side: {base_side}, Slant height: {slant_height}")
            steps.append(f"Step 2: Calculate base area")
            steps.append(f"  Base = {base_side}² = {base_area}")
            steps.append(f"Step 3: Calculate 4 triangular faces")
            steps.append(f"  One triangle = ½×{base_side}×{slant_height} = {triangle_area}")
            steps.append(f"  Four triangles: 4×{triangle_area} = {4*triangle_area}")
            steps.append(f"Step 4: Add base + triangles")
            steps.append(f"  SA = {base_area} + {4*triangle_area} = {surface_area}")

        steps.append("")
        steps.append(f"Final Answer: {correct_answer} square units ✓")
        steps.append("")
        steps.append(f"Note: Surface area measures AREA (square units), NOT perimeter (linear units)")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply correct algorithm across all templates.

        Args:
            problem: The problem to solve
            verbose: If True, generate verbose steps; if False, generate concise steps (default: False)
        """
        shape_type = problem.metadata['shape_type']

        # Calculate the correct surface area based on shape type
        if shape_type == 'cube':
            side = problem.metadata['side']
            correct_answer = 6 * (side ** 2)
        elif shape_type == 'rectangular_prism':
            length = problem.metadata['length']
            width = problem.metadata['width']
            height = problem.metadata['height']
            lw = length * width
            lh = length * height
            wh = width * height
            correct_answer = 2 * (lw + lh + wh)
        elif shape_type == 'triangular_prism':
            # Use stored surface_area since it involves complex calculations
            correct_answer = problem.metadata['surface_area']
        elif shape_type == 'pyramid':
            base_side = problem.metadata['base_side']
            slant_height = problem.metadata['slant_height']
            base_area = base_side ** 2
            triangle_area = 0.5 * base_side * slant_height
            correct_answer = base_area + 4 * triangle_area
        else:
            # Fallback to stored value
            correct_answer = problem.metadata['correct_answer']

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
