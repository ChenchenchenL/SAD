"""
Problem generator for Count-Net-Perimeter-As-Surface-Area malrule.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional, List
from utils import ProblemGenerator, Problem, DifficultyLevel
import math


class CountNetPerimeterAsSurfaceAreaProblemGenerator(ProblemGenerator):
    """Generates 3D net surface area problems (cube and rectangular prism nets)."""

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'cube_net',
            'rectangular_prism_net',
            'triangular_prism_net',
            'pyramid_net',
            'word_problem_context'
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        ranges = {
            5: {
                DifficultyLevel.EASY: {'min': 2, 'max': 4},
                DifficultyLevel.MEDIUM: {'min': 3, 'max': 6},
                DifficultyLevel.HARD: {'min': 4, 'max': 8}
            },
            6: {
                DifficultyLevel.EASY: {'min': 2, 'max': 5},
                DifficultyLevel.MEDIUM: {'min': 3, 'max': 7},
                DifficultyLevel.HARD: {'min': 5, 'max': 10}
            },
            7: {
                DifficultyLevel.EASY: {'min': 3, 'max': 6},
                DifficultyLevel.MEDIUM: {'min': 4, 'max': 9},
                DifficultyLevel.HARD: {'min': 6, 'max': 12}
            },
            8: {
                DifficultyLevel.EASY: {'min': 4, 'max': 8},
                DifficultyLevel.MEDIUM: {'min': 5, 'max': 10},
                DifficultyLevel.HARD: {'min': 7, 'max': 15}
            }
        }
        lvl = self.level if self.level in ranges else 6
        return ranges[lvl][self.difficulty]

    def generate(self, seed=None, template: Optional[str] = None) -> Problem:
        """
        Generate a net surface area problem based on selected template.

        Args:
            seed: Optional random seed for reproducibility
            template: Specific template to use, or None for random selection

        Returns:
            Problem instance
        """
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            template = random.choice(self.get_available_templates())

        ranges = self.get_value_ranges()
        min_val = ranges['min']
        max_val = ranges['max']

        # Generate based on template
        if template == 'cube_net':
            return self._generate_cube_net(min_val, max_val)
        elif template == 'rectangular_prism_net':
            return self._generate_rectangular_prism_net(min_val, max_val)
        elif template == 'triangular_prism_net':
            return self._generate_triangular_prism_net(min_val, max_val)
        elif template == 'pyramid_net':
            return self._generate_pyramid_net(min_val, max_val)
        elif template == 'word_problem_context':
            return self._generate_word_problem_context(min_val, max_val)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_cube_net(self, min_val: int, max_val: int) -> Problem:
        """Generate a cube net problem."""
        side = random.randint(min_val, max_val)

        # Correct answer: Surface area = 6 × side²
        surface_area = 6 * (side ** 2)

        # Malrule answer: Net perimeter (cross-shaped net has 12 edge segments)
        # A cross-shaped cube net has 12 unit edges on its perimeter
        net_perimeter = 12 * side

        text = f"A cube with side length {side} is unfolded into a net. What is the surface area of the cube?"

        return Problem(
            text=text,
            operands=[side],
            operation='surface_area_from_net',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'shape_type': 'cube',
                'side': side,
                'surface_area': surface_area,
                'net_perimeter': net_perimeter,
                'correct_answer': surface_area,
                'malrule_answer': net_perimeter,
                'template': 'cube_net'
            }
        )

    def _generate_rectangular_prism_net(self, min_val: int, max_val: int) -> Problem:
        """Generate a rectangular prism net problem."""
        length = random.randint(min_val, max_val)
        width = random.randint(min_val, max_val)
        height = random.randint(min_val, max_val)

        # Ensure not all dimensions are equal (avoid cube)
        attempts = 0
        while length == width == height and attempts < 10:
            length = random.randint(min_val, max_val)
            width = random.randint(min_val, max_val)
            height = random.randint(min_val, max_val)
            attempts += 1

        # Correct answer: Surface area = 2(lw + lh + wh)
        lw = length * width
        lh = length * height
        wh = width * height
        surface_area = 2 * (lw + lh + wh)

        # Malrule answer: Net perimeter (standard cross configuration)
        # For a rectangular prism net in standard configuration:
        # Perimeter = 2(l + w) + 2(l + h) + 2(w + h) = 2(l+w+l+h+w+h) = 4(l+w+h)
        # Actually, for a typical T-shaped or cross net: varies by configuration
        # Using simplified: 2*(2l + 2w + 2h) = 4(l+w+h)
        net_perimeter = 4 * (length + width + height)

        text = f"A rectangular prism with dimensions {length}×{width}×{height} is unfolded into a net. What is the surface area of the prism?"

        return Problem(
            text=text,
            operands=[length, width, height],
            operation='surface_area_from_net',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'shape_type': 'rectangular_prism',
                'length': length,
                'width': width,
                'height': height,
                'lw': lw,
                'lh': lh,
                'wh': wh,
                'surface_area': surface_area,
                'net_perimeter': net_perimeter,
                'correct_answer': surface_area,
                'malrule_answer': net_perimeter,
                'template': 'rectangular_prism_net'
            }
        )

    def _generate_triangular_prism_net(self, min_val: int, max_val: int) -> Problem:
        """Generate a triangular prism net problem."""
        # Triangular prism: 2 triangular faces + 3 rectangular faces
        base = random.randint(min_val, max_val)
        height_triangle = random.randint(min_val, max_val)
        length = random.randint(min_val, max_val)

        # Correct answer: Surface area = 2 × (1/2 × base × height_triangle) + (base + 2×sides) × length
        # For simplicity, assume equilateral triangle or use base/height for area calculation
        triangle_area = 0.5 * base * height_triangle

        # Side length for rectangular faces - approximate for right triangle
        side1 = height_triangle  # vertical side
        side2 = math.sqrt(base**2 + height_triangle**2)  # hypotenuse approximation

        # Surface area = 2 triangular ends + 3 rectangular sides
        surface_area = 2 * triangle_area + (base * length) + (side1 * length) + (side2 * length)
        surface_area = round(surface_area, 2)

        # Malrule answer: Net perimeter - approximate as perimeter of unfolded shape
        # Triangle perimeter + rectangular strip perimeter
        triangle_perimeter = base + side1 + side2
        net_perimeter = round(2 * triangle_perimeter + 2 * length, 2)

        text = f"A triangular prism with base {base}, triangle height {height_triangle}, and length {length} is unfolded into a net. What is the surface area?"

        return Problem(
            text=text,
            operands=[base, height_triangle, length],
            operation='surface_area_from_net',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'shape_type': 'triangular_prism',
                'base': base,
                'height_triangle': height_triangle,
                'length': length,
                'triangle_area': triangle_area,
                'surface_area': surface_area,
                'net_perimeter': net_perimeter,
                'correct_answer': surface_area,
                'malrule_answer': net_perimeter,
                'template': 'triangular_prism_net'
            }
        )

    def _generate_pyramid_net(self, min_val: int, max_val: int) -> Problem:
        """Generate a square pyramid net problem."""
        # Square pyramid: 1 square base + 4 triangular faces
        base_side = random.randint(min_val, max_val)
        slant_height = random.randint(min_val, max_val)

        # Correct answer: Surface area = base² + 4 × (1/2 × base × slant_height)
        base_area = base_side ** 2
        triangle_area = 0.5 * base_side * slant_height
        surface_area = base_area + 4 * triangle_area

        # Malrule answer: Net perimeter
        # Net has square base with 4 triangles attached
        # Perimeter counts outer edges only
        # 4 sides of base (but shared with triangles) + 4 outer edges of triangles
        net_perimeter = 4 * slant_height + 4 * base_side

        text = f"A square pyramid with base side {base_side} and slant height {slant_height} is unfolded into a net. What is the surface area?"

        return Problem(
            text=text,
            operands=[base_side, slant_height],
            operation='surface_area_from_net',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'shape_type': 'pyramid',
                'base_side': base_side,
                'slant_height': slant_height,
                'base_area': base_area,
                'triangle_area': triangle_area,
                'surface_area': surface_area,
                'net_perimeter': net_perimeter,
                'correct_answer': surface_area,
                'malrule_answer': net_perimeter,
                'template': 'pyramid_net'
            }
        )

    def _generate_word_problem_context(self, min_val: int, max_val: int) -> Problem:
        """Generate word problem covering ALL shape types with 3 variants each."""
        # Select which shape type to embed
        shape_types = ['cube', 'rectangular_prism', 'triangular_prism', 'pyramid']
        shape_type = random.choice(shape_types)
        variant = random.randint(0, 2)  # 3 variants per shape type

        if shape_type == 'cube':
            side = random.randint(min_val, max_val)
            surface_area = 6 * (side ** 2)
            net_perimeter = 12 * side

            templates = [
                f"A gift box is a cube with side length {side} inches. If you want to cover the entire box with wrapping paper (including all faces), what is the total surface area you need to cover?",
                f"A storage cube has side length {side} cm. How many square centimeters of material are needed to construct all 6 faces of the cube?",
                f"A dice is a cube with side length {side} mm. What is the total surface area of the dice?"
            ]

            text = templates[variant]

            return Problem(
                text=text,
                operands=[side],
                operation='surface_area_word_problem',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'shape_type': 'cube',
                    'side': side,
                    'surface_area': surface_area,
                    'net_perimeter': net_perimeter,
                    'correct_answer': surface_area,
                    'malrule_answer': net_perimeter,
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': shape_type,
                    'word_problem_variant': variant
                }
            )

        elif shape_type == 'rectangular_prism':
            length = random.randint(min_val, max_val)
            width = random.randint(min_val, max_val)
            height = random.randint(min_val, max_val)

            # Ensure not all dimensions are equal (avoid cube)
            attempts = 0
            while length == width == height and attempts < 10:
                length = random.randint(min_val, max_val)
                width = random.randint(min_val, max_val)
                height = random.randint(min_val, max_val)
                attempts += 1

            lw = length * width
            lh = length * height
            wh = width * height
            surface_area = 2 * (lw + lh + wh)
            net_perimeter = 4 * (length + width + height)

            templates = [
                f"A shipping box has dimensions {length}×{width}×{height} cm. You need to paint all outer surfaces. What is the total surface area to paint?",
                f"A rectangular fish tank measures {length} inches long, {width} inches wide, and {height} inches tall. How much glass (in square inches) is needed to construct all faces?",
                f"A brick has dimensions {length}×{width}×{height} mm. What is the total surface area of the brick?"
            ]

            text = templates[variant]

            return Problem(
                text=text,
                operands=[length, width, height],
                operation='surface_area_word_problem',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'shape_type': 'rectangular_prism',
                    'length': length,
                    'width': width,
                    'height': height,
                    'lw': lw,
                    'lh': lh,
                    'wh': wh,
                    'surface_area': surface_area,
                    'net_perimeter': net_perimeter,
                    'correct_answer': surface_area,
                    'malrule_answer': net_perimeter,
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': shape_type,
                    'word_problem_variant': variant
                }
            )

        elif shape_type == 'triangular_prism':
            base = random.randint(min_val, max_val)
            height_triangle = random.randint(min_val, max_val)
            length = random.randint(min_val, max_val)

            triangle_area = 0.5 * base * height_triangle
            side1 = height_triangle
            side2 = math.sqrt(base**2 + height_triangle**2)
            surface_area = 2 * triangle_area + (base * length) + (side1 * length) + (side2 * length)
            surface_area = round(surface_area, 2)
            triangle_perimeter = base + side1 + side2
            net_perimeter = round(2 * triangle_perimeter + 2 * length, 2)

            templates = [
                f"A camping tent is shaped like a triangular prism with base {base} feet, triangle height {height_triangle} feet, and length {length} feet. What is the total fabric area needed to construct the tent (including the floor)?",
                f"A triangular prism-shaped chocolate bar has base {base} cm, triangle height {height_triangle} cm, and length {length} cm. What is the total surface area of the wrapper?",
                f"A roof section is shaped like a triangular prism with base {base} meters, triangle height {height_triangle} meters, and length {length} meters. How much roofing material (in square meters) is needed for all surfaces?"
            ]

            text = templates[variant]

            return Problem(
                text=text,
                operands=[base, height_triangle, length],
                operation='surface_area_word_problem',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'shape_type': 'triangular_prism',
                    'base': base,
                    'height_triangle': height_triangle,
                    'length': length,
                    'triangle_area': triangle_area,
                    'surface_area': surface_area,
                    'net_perimeter': net_perimeter,
                    'correct_answer': surface_area,
                    'malrule_answer': net_perimeter,
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': shape_type,
                    'word_problem_variant': variant
                }
            )

        else:  # pyramid
            base_side = random.randint(min_val, max_val)
            slant_height = random.randint(min_val, max_val)

            base_area = base_side ** 2
            triangle_area = 0.5 * base_side * slant_height
            surface_area = base_area + 4 * triangle_area
            net_perimeter = 4 * slant_height + 4 * base_side

            templates = [
                f"A gazebo has a square pyramid roof with base side {base_side} meters and slant height {slant_height} meters. What is the total surface area of the roof (including the base)?",
                f"An ancient pyramid monument has a square base with side {base_side} feet and slant height {slant_height} feet. What is the total surface area of the pyramid?",
                f"A square pyramid-shaped decoration has base side {base_side} cm and slant height {slant_height} cm. How much gold foil (in square cm) is needed to cover all surfaces?"
            ]

            text = templates[variant]

            return Problem(
                text=text,
                operands=[base_side, slant_height],
                operation='surface_area_word_problem',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'shape_type': 'pyramid',
                    'base_side': base_side,
                    'slant_height': slant_height,
                    'base_area': base_area,
                    'triangle_area': triangle_area,
                    'surface_area': surface_area,
                    'net_perimeter': net_perimeter,
                    'correct_answer': surface_area,
                    'malrule_answer': net_perimeter,
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': shape_type,
                    'word_problem_variant': variant
                }
            )
