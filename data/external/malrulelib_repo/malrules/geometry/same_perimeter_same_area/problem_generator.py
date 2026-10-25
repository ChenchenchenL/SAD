"""
Problem generator for Same-Perimeter-Same-Area malrule.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple
from utils import ProblemGenerator, Problem, DifficultyLevel


class SamePerimeterSameAreaProblemGenerator(ProblemGenerator):
    """Generates rectangle comparison problems with same perimeter but different areas."""

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
        problem_types = ['simple_rectangles']

        # Add enhanced problem types for higher levels
        if self.level >= 5:
            problem_types.extend([
                'square_vs_rectangle',      # Compare square to rectangle (same P, different A)
                'word_problem_garden',      # Real-world contexts (gardens, fences)
                'three_shapes_comparison',  # Compare 3 rectangles with same perimeter
                'extreme_dimensions',       # Very elongated shapes (10×1 vs 6×5)
                'word_problem_context',     # Word problems covering all formula types
            ])

        problem_type = random.choice(problem_types)

        if problem_type == 'simple_rectangles':
            # Generate first rectangle dimensions
            l1 = random.randint(min_val, max_val)
            w1 = random.randint(min_val // 2, l1)

            # Calculate perimeter of first rectangle
            perimeter1 = 2 * (l1 + w1)

            # Find second rectangle with SAME perimeter but DIFFERENT area
            half_perim = perimeter1 // 2

            # Try different l2 values to find one with different area
            attempts = 0
            area1 = l1 * w1
            found = False

            while not found and attempts < 50:
                l2 = random.randint(max(1, half_perim - max_val), min(max_val, half_perim - 1))
                w2 = half_perim - l2

                if w2 > 0 and w2 <= l2:
                    area2 = l2 * w2
                    if area2 != area1:
                        found = True
                        break
                attempts += 1

            # If couldn't find different area, force one
            if not found:
                l2 = l1 + 1
                w2 = w1 - 1
                if w2 < 1:
                    w2 = 1
                area2 = l2 * w2

            area1 = l1 * w1
            area2 = l2 * w2

            correct_answer = area2
            malrule_answer = area1

            text = f"Rectangle A: {l1}×{w1}. Rectangle B: {l2}×{w2}. Both have the same perimeter. What is the area of Rectangle B?"

        elif problem_type == 'square_vs_rectangle':
            # Square vs rectangle with same perimeter
            # Square maximizes area for given perimeter
            side = random.randint(3, 8)

            # Square dimensions
            l1 = side
            w1 = side
            perimeter1 = 4 * side
            area1 = side * side

            # Rectangle with same perimeter but different area
            # P = 2(l2 + w2), so l2 + w2 = 2*side
            half_perim = 2 * side
            l2 = side + random.randint(1, 3)
            w2 = half_perim - l2

            if w2 < 1:
                w2 = 1
                l2 = half_perim - w2

            area2 = l2 * w2

            correct_answer = area2
            malrule_answer = area1

            text = f"Square A has side {side}. Rectangle B is {l2}×{w2}. Both have the same perimeter. What is the area of Rectangle B?"

        elif problem_type == 'word_problem_garden':
            # Real-world garden/fence context
            l1 = random.randint(4, 10)
            w1 = random.randint(2, l1 - 1)

            perimeter1 = 2 * (l1 + w1)
            area1 = l1 * w1

            # Second garden with same perimeter
            half_perim = perimeter1 // 2
            l2 = l1 - random.randint(1, 2)
            w2 = half_perim - l2

            if w2 < 1 or l2 < 1:
                l2 = l1 - 1
                w2 = half_perim - l2

            area2 = l2 * w2

            correct_answer = area2
            malrule_answer = area1

            contexts = [
                f"Garden A is {l1}m × {w1}m. Garden B is {l2}m × {w2}m. Both use the same amount of fencing. What is the area of Garden B?",
                f"Two rectangular frames use the same length of wood. Frame A is {l1}cm × {w1}cm. Frame B is {l2}cm × {w2}cm. Find the area of Frame B.",
                f"Two pens have equal perimeters. Pen A: {l1}ft × {w1}ft. Pen B: {l2}ft × {w2}ft. What is Pen B's area?",
            ]
            text = random.choice(contexts)

        elif problem_type == 'three_shapes_comparison':
            # Compare THREE rectangles with same perimeter
            # This really tests the misconception
            perimeter = random.randint(16, 24)
            half_perim = perimeter // 2

            # Rectangle A
            l1 = random.randint(half_perim // 2 + 1, half_perim - 2)
            w1 = half_perim - l1
            area1 = l1 * w1

            # Rectangle B (more square-like, larger area)
            l2 = (half_perim + 1) // 2
            w2 = half_perim - l2
            area2 = l2 * w2

            # Rectangle C (elongated, smaller area)
            l3 = half_perim - 1
            w3 = 1
            area3 = l3 * w3

            # Ask about Rectangle B
            correct_answer = area2
            malrule_answer = area1

            text = f"Three rectangles all have perimeter {perimeter}. Rectangle A: {l1}×{w1}. Rectangle B: {l2}×{w2}. Rectangle C: {l3}×{w3}. What is the area of Rectangle B?"

            # Store extra metadata
            l2_val = l2
            w2_val = w2

        elif problem_type == 'extreme_dimensions':
            # Very elongated rectangle vs more square-like
            # Shows dramatic difference in areas
            perimeter = random.randint(20, 30)
            half_perim = perimeter // 2

            # Very elongated rectangle
            l1 = half_perim - 1
            w1 = 1
            area1 = l1 * w1

            # More balanced rectangle (much larger area!)
            l2 = (half_perim * 2) // 3
            w2 = half_perim - l2
            area2 = l2 * w2

            correct_answer = area2
            malrule_answer = area1

            text = f"Rectangle A: {l1}×{w1}. Rectangle B: {l2}×{w2}. Both have the same perimeter of {perimeter}. What is the area of Rectangle B?"

        elif problem_type == 'word_problem_context':
            return self._generate_word_problem_context(min_val, max_val)

        else:  # Default fallback
            l1 = random.randint(min_val, max_val)
            w1 = random.randint(min_val // 2, l1)
            perimeter1 = 2 * (l1 + w1)
            half_perim = perimeter1 // 2
            l2 = l1 - 1
            w2 = half_perim - l2
            if w2 < 1:
                w2 = 1
            area1 = l1 * w1
            area2 = l2 * w2
            correct_answer = area2
            malrule_answer = area1
            text = f"Rectangle A: {l1}×{w1}. Rectangle B: {l2}×{w2}. Both have the same perimeter. What is the area of Rectangle B?"

        # Create metadata
        metadata = {
            'length1': l1,
            'width1': w1,
            'length2': l2 if 'l2' in locals() else l2_val if 'l2_val' in locals() else l1,
            'width2': w2 if 'w2' in locals() else w2_val if 'w2_val' in locals() else w1,
            'perimeter1': 2 * (l1 + w1),
            'perimeter2': 2 * (l2 if 'l2' in locals() else l2_val if 'l2_val' in locals() else l1,
                              w2 if 'w2' in locals() else w2_val if 'w2_val' in locals() else w1).count(0) +
                         sum([l2 if 'l2' in locals() else l2_val if 'l2_val' in locals() else l1,
                              w2 if 'w2' in locals() else w2_val if 'w2_val' in locals() else w1]),
            'area1': area1,
            'area2': area2,
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer,
            'problem_type': problem_type
        }

        # Fix perimeter2 calculation
        l2_final = l2 if 'l2' in locals() else (l2_val if 'l2_val' in locals() else l1)
        w2_final = w2 if 'w2' in locals() else (w2_val if 'w2_val' in locals() else w1)
        metadata['perimeter2'] = 2 * (l2_final + w2_final)
        metadata['length2'] = l2_final
        metadata['width2'] = w2_final

        return Problem(
            text=text,
            operands=[l1, w1, l2_final, w2_final],
            operation='rectangle_area_comparison',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_word_problem_context(self, min_val: int, max_val: int) -> Problem:
        """Generate word problem covering rectangle comparison with 3 variants."""
        variant = random.randint(0, 2)  # 3 variants

        # Generate first rectangle dimensions
        l1 = random.randint(min_val, max_val)
        w1 = random.randint(min_val // 2, l1)

        # Calculate perimeter of first rectangle
        perimeter = 2 * (l1 + w1)

        # Find second rectangle with SAME perimeter but DIFFERENT area
        half_perim = perimeter // 2

        # Try different l2 values to find one with different area
        attempts = 0
        area1 = l1 * w1
        found = False

        while not found and attempts < 50:
            l2 = random.randint(max(1, half_perim - max_val), min(max_val, half_perim - 1))
            w2 = half_perim - l2

            if w2 > 0 and w2 <= l2:
                area2 = l2 * w2
                if area2 != area1:
                    found = True
                    break
            attempts += 1

        # If couldn't find different area, force one
        if not found:
            l2 = l1 + 1
            w2 = w1 - 1
            if w2 < 1:
                w2 = 1
            area2 = l2 * w2

        correct_answer = area2
        malrule_answer = area1

        templates = [
            f"Two gardens both use {perimeter} meters of fencing around their perimeters. Garden A is {l1}m × {w1}m. Garden B is {l2}m × {w2}m. What is the area of Garden B?",
            f"Two picture frames both use {perimeter} inches of frame material (perimeter). Frame A is {l1}in × {w1}in. Frame B is {l2}in × {w2}in. What is the area enclosed by Frame B?",
            f"Two rectangular pools both have a perimeter of {perimeter} feet. Pool A measures {l1}ft × {w1}ft. Pool B measures {l2}ft × {w2}ft. What is the area of Pool B?"
        ]

        text = templates[variant]

        return Problem(
            text=text,
            operands=[l1, w1, l2, w2],
            operation='rectangle_area_comparison',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'length1': l1,
                'width1': w1,
                'length2': l2,
                'width2': w2,
                'perimeter1': perimeter,
                'perimeter2': perimeter,
                'area1': area1,
                'area2': area2,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'problem_type': 'word_problem_context',
                'is_word_problem': True,
                'word_problem_type': 'rectangle_same_perimeter',
                'word_problem_variant': variant
            }
        )
