"""
Problem generator for Same-Area-Same-Perimeter malrule.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple
from utils import ProblemGenerator, Problem, DifficultyLevel


class SameAreaSamePerimeterProblemGenerator(ProblemGenerator):
    """Generates rectangle comparison problems with same area but different perimeters."""

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        ranges = {
            4: {
                DifficultyLevel.EASY: {'length': (2, 6)},
                DifficultyLevel.MEDIUM: {'length': (3, 8)},
                DifficultyLevel.HARD: {'length': (4, 10)}
            },
            5: {
                DifficultyLevel.EASY: {'length': (3, 8)},
                DifficultyLevel.MEDIUM: {'length': (4, 10)},
                DifficultyLevel.HARD: {'length': (5, 12)}
            },
            6: {
                DifficultyLevel.EASY: {'length': (4, 10)},
                DifficultyLevel.MEDIUM: {'length': (5, 12)},
                DifficultyLevel.HARD: {'length': (6, 15)}
            },
            7: {
                DifficultyLevel.EASY: {'length': (5, 12)},
                DifficultyLevel.MEDIUM: {'length': (6, 15)},
                DifficultyLevel.HARD: {'length': (8, 20)}
            }
        }
        lvl = self.level if self.level in ranges else 5
        return ranges[lvl][self.difficulty]

    def generate(self, seed=None) -> Problem:
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['length']

        # Choose problem type
        problem_types = ['rectangle_comparison']

        # Add enhanced problem types for higher levels
        if self.level >= 5:
            problem_types.extend([
                'triangle_comparison',     # Triangles with same area, different perimeters
                'fencing_optimization',    # Word problem with area constraint
                'composite_shapes',        # L-shapes with same area
                'square_vs_rectangle',     # Square compared to elongated rectangle
                'word_problem_context',    # Word problems covering all formula types
            ])

        problem_type = random.choice(problem_types)

        # Handle enhanced problem types first
        if problem_type == 'triangle_comparison':
            # Two triangles with same area but different perimeters
            # Triangle: Area = 1/2 * base * height
            base1 = random.randint(4, 8)
            height1 = random.randint(4, 8)
            area = base1 * height1 // 2

            # Find different base/height for same area
            base2 = base1 * 2
            height2 = height1 // 2 if height1 % 2 == 0 else height1

            # For simplicity, assume right triangles
            # Perimeter = base + height + hypotenuse
            import math
            hyp1 = math.sqrt(base1**2 + height1**2)
            hyp2 = math.sqrt(base2**2 + height2**2)

            perimeter1 = base1 + height1 + hyp1
            perimeter2 = base2 + height2 + hyp2

            correct_answer = round(perimeter2, 1)
            malrule_answer = round(perimeter1, 1)

            text = f"Triangle A has base {base1} and height {height1}. Triangle B has base {base2} and height {height2}. Both have the same area. What is the perimeter of Triangle B (assuming right triangles)?"

            return Problem(
                text=text,
                operands=[base1, height1, base2, height2],
                operation='triangle_perimeter_comparison',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'base1': base1,
                    'height1': height1,
                    'base2': base2,
                    'height2': height2,
                    'area': area,
                    'perimeter1': round(perimeter1, 1),
                    'perimeter2': round(perimeter2, 1),
                    'problem_type': problem_type,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer
                }
            )

        elif problem_type == 'fencing_optimization':
            # Word problem: fencing a rectangular garden with fixed area
            area = random.choice([24, 36, 48])
            factors = [(i, area // i) for i in range(1, area + 1) if area % i == 0]

            # Pick two different configurations
            idx1 = len(factors) // 2
            l1, w1 = factors[idx1]
            idx2 = 0
            l2, w2 = factors[idx2]

            perimeter1 = 2 * (l1 + w1)
            perimeter2 = 2 * (l2 + w2)

            correct_answer = perimeter2
            malrule_answer = perimeter1

            text = f"A farmer has two rectangular garden designs, both with area {area} square meters. Design A is {l1}m × {w1}m. Design B is {l2}m × {w2}m. How much fencing is needed for Design B?"

            return Problem(
                text=text,
                operands=[l1, w1, l2, w2],
                operation='fencing_word_problem',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'length1': l1,
                    'width1': w1,
                    'length2': l2,
                    'width2': w2,
                    'area': area,
                    'perimeter1': perimeter1,
                    'perimeter2': perimeter2,
                    'problem_type': problem_type,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'context': 'fencing'
                }
            )

        elif problem_type == 'composite_shapes':
            # L-shaped figures with same area but different perimeters
            # L-shape A: 2×3 rectangle + 2×2 square
            # L-shape B: 1×6 rectangle + 2×3 rectangle
            area = random.choice([10, 12, 14, 16])

            # Simple L-shape perimeters (just count outer edges)
            # For area 12: L-shape A might have perimeter 16, L-shape B might have perimeter 20
            perimeter1 = random.randint(14, 18)
            perimeter2 = perimeter1 + random.randint(4, 8)

            correct_answer = perimeter2
            malrule_answer = perimeter1

            text = f"Two L-shaped figures both have area {area} square units. Figure A has perimeter {perimeter1} units. What is the perimeter of Figure B?"

            return Problem(
                text=text,
                operands=[area, perimeter1, perimeter2, 0],
                operation='composite_shape_comparison',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'area': area,
                    'perimeter1': perimeter1,
                    'perimeter2': perimeter2,
                    'problem_type': problem_type,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer
                }
            )

        elif problem_type == 'square_vs_rectangle':
            # Compare square to elongated rectangle with same area
            # e.g., 4×4 square (area 16) vs 8×2 rectangle (area 16)
            side = random.choice([4, 5, 6])
            area = side * side

            # Find elongated rectangle with same area
            l2 = side * 2
            w2 = side // 2 if side % 2 == 0 else area // l2

            perimeter1 = 4 * side  # square
            perimeter2 = 2 * (l2 + w2)  # rectangle

            correct_answer = perimeter2
            malrule_answer = perimeter1

            text = f"A square with side length {side} and a rectangle {l2}×{w2} have the same area. What is the perimeter of the rectangle?"

            return Problem(
                text=text,
                operands=[side, side, l2, w2],
                operation='square_vs_rectangle_comparison',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'side': side,
                    'length': l2,
                    'width': w2,
                    'area': area,
                    'perimeter1': perimeter1,
                    'perimeter2': perimeter2,
                    'problem_type': problem_type,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer
                }
            )

        elif problem_type == 'word_problem_context':
            return self._generate_word_problem_context(min_val, max_val)

        # Original rectangle comparison problem type
        # Pick a target area
        target_area = random.randint(8, 24)

        # Find two different factorizations of target_area
        # that give different perimeters
        factors = []
        for i in range(1, target_area + 1):
            if target_area % i == 0:
                factors.append((i, target_area // i))

        # Pick two different factor pairs
        if len(factors) >= 2:
            # Pick first pair (more square-like for smaller perimeter)
            idx1 = len(factors) // 2
            l1, w1 = factors[idx1]

            # Pick second pair (more elongated for larger perimeter)
            idx2 = 0 if idx1 != 0 else len(factors) - 1
            l2, w2 = factors[idx2]
        else:
            # Fallback to simple case
            l1, w1 = 4, 2
            l2, w2 = 8, 1
            target_area = 8

        # Calculate perimeters
        perimeter1 = 2 * (l1 + w1)
        perimeter2 = 2 * (l2 + w2)

        # Ensure perimeters are different
        attempts = 0
        while perimeter1 == perimeter2 and attempts < 10:
            target_area = random.randint(8, 24)
            factors = [(i, target_area // i) for i in range(1, target_area + 1) if target_area % i == 0]
            if len(factors) >= 2:
                idx1 = len(factors) // 2
                l1, w1 = factors[idx1]
                idx2 = 0
                l2, w2 = factors[idx2]
                perimeter1 = 2 * (l1 + w1)
                perimeter2 = 2 * (l2 + w2)
            attempts += 1

        # Correct answer: perimeter of second rectangle
        correct_answer = perimeter2

        # Malrule answer: Student thinks same area = same perimeter
        malrule_answer = perimeter1

        text = f"Rectangle A: {l1}×{w1}. Rectangle B: {l2}×{w2}. Both have the same area. What is the perimeter of Rectangle B?"

        return Problem(
            text=text,
            operands=[l1, w1, l2, w2],
            operation='rectangle_perimeter_comparison',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'length1': l1,
                'width1': w1,
                'length2': l2,
                'width2': w2,
                'area1': l1 * w1,
                'area2': l2 * w2,
                'perimeter1': perimeter1,
                'perimeter2': perimeter2,
                'problem_type': problem_type,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_word_problem_context(self, min_val: int, max_val: int) -> Problem:
        """Generate word problem covering rectangle comparison with 3 variants."""
        variant = random.randint(0, 2)  # 3 variants

        # Pick a target area
        target_area = random.randint(12, 24)

        # Find two different factorizations of target_area
        factors = [(i, target_area // i) for i in range(1, target_area + 1) if target_area % i == 0]

        # Pick two different factor pairs
        if len(factors) >= 2:
            # Pick first pair (more square-like for smaller perimeter)
            idx1 = len(factors) // 2
            l1, w1 = factors[idx1]

            # Pick second pair (more elongated for larger perimeter)
            idx2 = 0 if idx1 != 0 else len(factors) - 1
            l2, w2 = factors[idx2]
        else:
            # Fallback to simple case
            l1, w1 = 4, 3
            l2, w2 = 12, 1
            target_area = 12

        # Calculate perimeters
        perimeter1 = 2 * (l1 + w1)
        perimeter2 = 2 * (l2 + w2)

        # Correct answer: perimeter of second rectangle
        correct_answer = perimeter2

        # Malrule answer: Student thinks same area = same perimeter
        malrule_answer = perimeter1

        templates = [
            f"Two garden plots both have area {target_area} square meters. Plot A is {l1}m × {w1}m. Plot B is {l2}m × {w2}m. How much fencing is needed to enclose Plot B?",
            f"Two rectangular rugs both cover {target_area} square feet. Rug A measures {l1}ft × {w1}ft. Rug B measures {l2}ft × {w2}ft. What is the perimeter of Rug B (the length of trim needed)?",
            f"Two posters both have area {target_area} square inches. Poster A is {l1}in × {w1}in. Poster B is {l2}in × {w2}in. How much frame material (perimeter) is needed for Poster B?"
        ]

        text = templates[variant]

        return Problem(
            text=text,
            operands=[l1, w1, l2, w2],
            operation='rectangle_perimeter_comparison',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'length1': l1,
                'width1': w1,
                'length2': l2,
                'width2': w2,
                'area1': l1 * w1,
                'area2': l2 * w2,
                'perimeter1': perimeter1,
                'perimeter2': perimeter2,
                'problem_type': 'word_problem_context',
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'is_word_problem': True,
                'word_problem_type': 'rectangle_same_area',
                'word_problem_variant': variant
            }
        )
