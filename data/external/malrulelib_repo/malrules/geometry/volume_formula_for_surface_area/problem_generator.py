"""
Problem generator for Volume-Formula-For-Surface-Area malrule.

Generates surface area problems where students might use volume formula instead.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, List, Optional
from utils import ProblemGenerator, Problem, DifficultyLevel


class VolumeFormulaForSurfaceAreaProblemGenerator(ProblemGenerator):
    """
    Generates surface area problems for various 3D shapes.

    Templates:
    1. rectangular_prism - Standard rectangular prism with different l, w, h
    2. cube - Cube where all dimensions are equal
    3. larger_dimensions - Rectangular prisms with larger numbers
    4. decimal_dimensions - Prisms with decimal dimensions (harder)
    5. word_problem - Real-world contexts (boxes, rooms, packages)
    """

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'rectangular_prism',
            'cube',
            'larger_dimensions',
            'decimal_dimensions',
            'word_problem'
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        ranges = {
            5: {
                DifficultyLevel.EASY: {'min': 2, 'max': 5},
                DifficultyLevel.MEDIUM: {'min': 3, 'max': 7},
                DifficultyLevel.HARD: {'min': 4, 'max': 10}
            },
            6: {
                DifficultyLevel.EASY: {'min': 3, 'max': 6},
                DifficultyLevel.MEDIUM: {'min': 4, 'max': 8},
                DifficultyLevel.HARD: {'min': 5, 'max': 12}
            },
            7: {
                DifficultyLevel.EASY: {'min': 4, 'max': 8},
                DifficultyLevel.MEDIUM: {'min': 5, 'max': 10},
                DifficultyLevel.HARD: {'min': 6, 'max': 15}
            },
            8: {
                DifficultyLevel.EASY: {'min': 5, 'max': 10},
                DifficultyLevel.MEDIUM: {'min': 6, 'max': 12},
                DifficultyLevel.HARD: {'min': 8, 'max': 20}
            }
        }
        lvl = self.level if self.level in ranges else 6
        return ranges[lvl][self.difficulty]

    def generate(self, seed=None, template: Optional[str] = None) -> Problem:
        """
        Generate a surface area problem based on selected template.

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

        # Generate based on template
        if template == 'rectangular_prism':
            return self._generate_rectangular_prism(seed)
        elif template == 'cube':
            return self._generate_cube(seed)
        elif template == 'larger_dimensions':
            return self._generate_larger_dimensions(seed)
        elif template == 'decimal_dimensions':
            return self._generate_decimal_dimensions(seed)
        elif template == 'word_problem':
            return self._generate_word_problem(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_rectangular_prism(self, seed=None) -> Problem:
        """Generate standard rectangular prism with different dimensions."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val = ranges['min']
        max_val = ranges['max']

        # Generate three distinct dimensions for a rectangular prism
        length = random.randint(min_val, max_val)
        width = random.randint(min_val, max_val)
        height = random.randint(min_val, max_val)

        # Ensure dimensions are not all the same (avoid cube for this template)
        attempts = 0
        while length == width == height and attempts < 10:
            length = random.randint(min_val, max_val)
            width = random.randint(min_val, max_val)
            height = random.randint(min_val, max_val)
            attempts += 1

        # Calculate surface area (correct answer)
        # SA = 2(lw + lh + wh)
        lw = length * width
        lh = length * height
        wh = width * height
        surface_area = 2 * (lw + lh + wh)

        # Calculate volume (malrule answer)
        # V = lwh
        volume = length * width * height

        text = f"Find the surface area of a rectangular prism with length {length}, width {width}, and height {height}."

        return Problem(
            text=text,
            operands=[length, width, height],
            operation='surface_area_rectangular_prism',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'length': length,
                'width': width,
                'height': height,
                'lw': lw,
                'lh': lh,
                'wh': wh,
                'surface_area': surface_area,
                'volume': volume,
                'correct_answer': surface_area,
                'malrule_answer': volume,
                'template': 'rectangular_prism',
                'shape_type': 'rectangular_prism'
            }
        )

    def _generate_cube(self, seed=None) -> Problem:
        """Generate cube where all dimensions are equal."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val = ranges['min']
        max_val = ranges['max']

        # All dimensions are the same for a cube
        side = random.randint(min_val, max_val)
        length = width = height = side

        # Calculate surface area (correct answer)
        # SA = 6s² for a cube
        surface_area = 6 * side * side

        # Calculate volume (malrule answer)
        # V = s³
        volume = side * side * side

        text = f"Find the surface area of a cube with side length {side}."

        return Problem(
            text=text,
            operands=[side, side, side],
            operation='surface_area_cube',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'length': side,
                'width': side,
                'height': side,
                'side': side,
                'lw': side * side,
                'lh': side * side,
                'wh': side * side,
                'surface_area': surface_area,
                'volume': volume,
                'correct_answer': surface_area,
                'malrule_answer': volume,
                'template': 'cube',
                'shape_type': 'cube'
            }
        )

    def _generate_larger_dimensions(self, seed=None) -> Problem:
        """Generate rectangular prism with larger dimensions."""
        if seed is not None:
            random.seed(seed)

        # Use larger numbers for increased difficulty
        min_val = 10
        max_val = 25

        length = random.randint(min_val, max_val)
        width = random.randint(min_val, max_val)
        height = random.randint(min_val, max_val)

        # Ensure not all the same
        attempts = 0
        while length == width == height and attempts < 10:
            height = random.randint(min_val, max_val)
            attempts += 1

        # Calculate surface area (correct answer)
        lw = length * width
        lh = length * height
        wh = width * height
        surface_area = 2 * (lw + lh + wh)

        # Calculate volume (malrule answer)
        volume = length * width * height

        text = f"Calculate the surface area of a rectangular prism with dimensions {length} × {width} × {height}."

        return Problem(
            text=text,
            operands=[length, width, height],
            operation='surface_area_rectangular_prism',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'length': length,
                'width': width,
                'height': height,
                'lw': lw,
                'lh': lh,
                'wh': wh,
                'surface_area': surface_area,
                'volume': volume,
                'correct_answer': surface_area,
                'malrule_answer': volume,
                'template': 'larger_dimensions',
                'shape_type': 'rectangular_prism'
            }
        )

    def _generate_decimal_dimensions(self, seed=None) -> Problem:
        """Generate prism with decimal dimensions."""
        if seed is not None:
            random.seed(seed)

        # Use decimals (one decimal place)
        length = round(random.uniform(2.5, 8.5), 1)
        width = round(random.uniform(2.5, 8.5), 1)
        height = round(random.uniform(2.5, 8.5), 1)

        # Ensure not all the same
        attempts = 0
        while length == width == height and attempts < 10:
            height = round(random.uniform(2.5, 8.5), 1)
            attempts += 1

        # Calculate surface area (correct answer)
        lw = length * width
        lh = length * height
        wh = width * height
        surface_area = 2 * (lw + lh + wh)

        # Calculate volume (malrule answer)
        volume = length * width * height

        text = f"Find the surface area of a rectangular prism with length {length} cm, width {width} cm, and height {height} cm."

        return Problem(
            text=text,
            operands=[length, width, height],
            operation='surface_area_rectangular_prism',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'length': length,
                'width': width,
                'height': height,
                'lw': round(lw, 2),
                'lh': round(lh, 2),
                'wh': round(wh, 2),
                'surface_area': round(surface_area, 2),
                'volume': round(volume, 2),
                'correct_answer': round(surface_area, 2),
                'malrule_answer': round(volume, 2),
                'template': 'decimal_dimensions',
                'shape_type': 'rectangular_prism'
            }
        )

    def _generate_word_problem(self, seed=None) -> Problem:
        """Generate word problem covering ALL shape types with 3 variants each."""
        if seed is not None:
            random.seed(seed)

        # Select which shape type to embed
        shape_types = ['rectangular_prism', 'cube']
        shape_type = random.choice(shape_types)
        variant = random.randint(0, 2)  # 3 variants per shape type

        ranges = self.get_value_ranges()
        min_val = ranges['min']
        max_val = ranges['max']

        if shape_type == 'cube':
            side = random.randint(min_val, max_val)
            surface_area = 6 * side * side
            volume = side * side * side

            templates = [
                f"A gift box is a cube with side length {side} inches. How much wrapping paper is needed to cover the entire box?",
                f"A storage cube measures {side} feet on each side. What is the total surface area that needs to be painted?",
                f"A cubic container has side length {side} cm. What is the total surface area of material needed to construct it?"
            ]

            text = templates[variant]

            return Problem(
                text=text,
                operands=[side, side, side],
                operation='surface_area_cube',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'length': side,
                    'width': side,
                    'height': side,
                    'side': side,
                    'lw': side * side,
                    'lh': side * side,
                    'wh': side * side,
                    'surface_area': surface_area,
                    'volume': volume,
                    'correct_answer': f'{surface_area}',
                    'malrule_answer': f'{volume}',
                    'template': 'word_problem',
                    'shape_type': 'cube',
                    'is_word_problem': True,
                    'word_problem_type': shape_type,
                    'word_problem_variant': variant
                }
            )

        else:  # rectangular_prism
            length = random.randint(min_val, max_val)
            width = random.randint(min_val, max_val)
            height = random.randint(min_val, max_val)

            # Ensure not all the same
            attempts = 0
            while length == width == height and attempts < 10:
                height = random.randint(min_val, max_val)
                attempts += 1

            lw = length * width
            lh = length * height
            wh = width * height
            surface_area = 2 * (lw + lh + wh)
            volume = length * width * height

            templates = [
                f"A shipping box has dimensions {length} cm × {width} cm × {height} cm. What is the total surface area of cardboard used?",
                f"A storage container measures {length} feet long, {width} feet wide, and {height} feet tall. What is the total surface area that needs to be painted?",
                f"A rectangular fish tank has length {length} inches, width {width} inches, and height {height} inches. How much glass (in square inches) is needed to construct all faces?"
            ]

            text = templates[variant]

            return Problem(
                text=text,
                operands=[length, width, height],
                operation='surface_area_rectangular_prism',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'length': length,
                    'width': width,
                    'height': height,
                    'lw': lw,
                    'lh': lh,
                    'wh': wh,
                    'surface_area': surface_area,
                    'volume': volume,
                    'correct_answer': f'{surface_area}',
                    'malrule_answer': f'{volume}',
                    'template': 'word_problem',
                    'shape_type': 'rectangular_prism',
                    'is_word_problem': True,
                    'word_problem_type': shape_type,
                    'word_problem_variant': variant
                }
            )
