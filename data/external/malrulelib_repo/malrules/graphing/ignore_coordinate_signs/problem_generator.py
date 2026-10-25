"""
Problem generator for Ignore-Coordinate-Signs malrule.

Generates coordinate problems where students may ignore negative signs.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, List, Optional
from utils import ProblemGenerator, Problem, DifficultyLevel


class IgnoreCoordinateSignsProblemGenerator(ProblemGenerator):
    """
    Generates coordinate plotting problems with negative values.

    Templates:
    1. single_point_plotting - Plot a single point with negative coordinate(s)
    2. all_four_quadrants - Identify which quadrant a point is in
    3. distance_between_points - Find distance between two points
    4. midpoint_calculation - Find midpoint between two points
    5. word_problem - Real-world contexts (temperature, elevation, maps)
    """

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'single_point_plotting',
            'all_four_quadrants',
            'distance_between_points',
            'midpoint_calculation',
            'word_problem'
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        ranges = {
            5: {
                DifficultyLevel.EASY: {'coordinate': (-5, 5)},
                DifficultyLevel.MEDIUM: {'coordinate': (-8, 8)},
                DifficultyLevel.HARD: {'coordinate': (-10, 10)}
            },
            6: {
                DifficultyLevel.EASY: {'coordinate': (-8, 8)},
                DifficultyLevel.MEDIUM: {'coordinate': (-10, 10)},
                DifficultyLevel.HARD: {'coordinate': (-12, 12)}
            },
            7: {
                DifficultyLevel.EASY: {'coordinate': (-10, 10)},
                DifficultyLevel.MEDIUM: {'coordinate': (-12, 12)},
                DifficultyLevel.HARD: {'coordinate': (-15, 15)}
            },
            8: {
                DifficultyLevel.EASY: {'coordinate': (-12, 12)},
                DifficultyLevel.MEDIUM: {'coordinate': (-15, 15)},
                DifficultyLevel.HARD: {'coordinate': (-20, 20)}
            }
        }
        lvl = self.level if self.level in ranges else 6
        return ranges[lvl][self.difficulty]

    def generate(self, seed=None, template: Optional[str] = None) -> Problem:
        """
        Generate a coordinate problem based on selected template.

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
        if template == 'single_point_plotting':
            return self._generate_single_point_plotting(seed)
        elif template == 'all_four_quadrants':
            return self._generate_all_four_quadrants(seed)
        elif template == 'distance_between_points':
            return self._generate_distance_between_points(seed)
        elif template == 'midpoint_calculation':
            return self._generate_midpoint_calculation(seed)
        elif template == 'word_problem':
            return self._generate_word_problem(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_single_point_plotting(self, seed=None) -> Problem:
        """Generate basic point plotting with at least one negative coordinate."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['coordinate']

        # Generate x and y coordinates
        x = random.randint(min_val, max_val)
        y = random.randint(min_val, max_val)

        # Ensure at least one coordinate is negative to trigger the malrule
        attempts = 0
        while x >= 0 and y >= 0 and attempts < 20:
            x = random.randint(min_val, max_val)
            y = random.randint(min_val, max_val)
            attempts += 1

        # Correct answer: (x, y) with proper signs
        correct_answer = (x, y)

        # Malrule answer: (|x|, |y|) - student ignores negative signs
        malrule_answer = (abs(x), abs(y))

        text = f"Plot the point ({x}, {y}) on a coordinate plane."

        return Problem(
            text=text,
            operands=[x, y],
            operation='coordinate_plotting',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'x': x,
                'y': y,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'single_point_plotting'
            }
        )

    def _generate_all_four_quadrants(self, seed=None) -> Problem:
        """Generate problem asking which quadrant a point is in."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['coordinate']

        # Generate point in quadrants II, III, or IV (NOT I, to ensure malrule differs)
        # This ensures at least one negative coordinate
        quadrants = [
            (2, 'II', lambda: (random.randint(min_val, -1), random.randint(1, max_val))),
            (3, 'III', lambda: (random.randint(min_val, -1), random.randint(min_val, -1))),
            (4, 'IV', lambda: (random.randint(1, max_val), random.randint(min_val, -1)))
        ]

        quadrant_num, correct_quadrant, coord_generator = random.choice(quadrants)
        x, y = coord_generator()

        # Malrule: student uses absolute values, always gets Quadrant I
        malrule_quadrant = 'I'

        text = f"Which quadrant contains the point ({x}, {y})?"

        return Problem(
            text=text,
            operands=[x, y],
            operation='quadrant_identification',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'x': x,
                'y': y,
                'correct_answer': correct_quadrant,
                'malrule_answer': malrule_quadrant,
                'template': 'all_four_quadrants'
            }
        )

    def _generate_distance_between_points(self, seed=None) -> Problem:
        """Generate distance calculation between two points."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['coordinate']

        # Generate two points ensuring they span across axes to avoid malrule=correct edge cases
        x1 = random.randint(min_val, max_val)
        y1 = random.randint(min_val, max_val)
        x2 = random.randint(min_val, max_val)
        y2 = random.randint(min_val, max_val)

        # Ensure at least one coordinate has opposite signs AND avoid zeros
        # This ensures malrule gives different answer
        attempts = 0
        while ((x1 >= 0 and y1 >= 0 and x2 >= 0 and y2 >= 0) or
               x1 == 0 or y1 == 0 or x2 == 0 or y2 == 0 or
               ((x1 > 0) == (x2 > 0) and (y1 > 0) == (y2 > 0))) and attempts < 20:
            x1 = random.randint(min_val, max_val)
            y1 = random.randint(min_val, max_val)
            x2 = random.randint(min_val, max_val)
            y2 = random.randint(min_val, max_val)
            attempts += 1

        # Calculate correct distance using distance formula
        dx = x2 - x1
        dy = y2 - y1
        correct_distance = round((dx**2 + dy**2)**0.5, 2)

        # Malrule: student uses absolute values
        malrule_dx = abs(x2) - abs(x1)
        malrule_dy = abs(y2) - abs(y1)
        malrule_distance = round((malrule_dx**2 + malrule_dy**2)**0.5, 2)

        text = f"Find the distance between points ({x1}, {y1}) and ({x2}, {y2})."

        return Problem(
            text=text,
            operands=[x1, y1, x2, y2],
            operation='distance_calculation',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'x1': x1,
                'y1': y1,
                'x2': x2,
                'y2': y2,
                'dx': dx,
                'dy': dy,
                'correct_answer': correct_distance,
                'malrule_answer': malrule_distance,
                'template': 'distance_between_points'
            }
        )

    def _generate_midpoint_calculation(self, seed=None) -> Problem:
        """Generate midpoint calculation between two points."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['coordinate']

        # Generate two points with at least one negative coordinate
        x1 = random.randint(min_val, max_val)
        y1 = random.randint(min_val, max_val)
        x2 = random.randint(min_val, max_val)
        y2 = random.randint(min_val, max_val)

        # Ensure at least one coordinate is negative
        attempts = 0
        while (x1 >= 0 and y1 >= 0 and x2 >= 0 and y2 >= 0) and attempts < 20:
            x1 = random.randint(min_val, max_val)
            y1 = random.randint(min_val, max_val)
            attempts += 1

        # Calculate correct midpoint
        midpoint_x = round((x1 + x2) / 2, 1)
        midpoint_y = round((y1 + y2) / 2, 1)
        correct_midpoint = (midpoint_x, midpoint_y)

        # Malrule: student uses absolute values
        malrule_midpoint_x = round((abs(x1) + abs(x2)) / 2, 1)
        malrule_midpoint_y = round((abs(y1) + abs(y2)) / 2, 1)
        malrule_midpoint = (malrule_midpoint_x, malrule_midpoint_y)

        text = f"Find the midpoint between ({x1}, {y1}) and ({x2}, {y2})."

        return Problem(
            text=text,
            operands=[x1, y1, x2, y2],
            operation='midpoint_calculation',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'x1': x1,
                'y1': y1,
                'x2': x2,
                'y2': y2,
                'correct_answer': correct_midpoint,
                'malrule_answer': malrule_midpoint,
                'template': 'midpoint_calculation'
            }
        )

    def _generate_word_problem(self, seed=None) -> Problem:
        """Generate word problem covering ALL formula types with 3 variants each."""
        if seed is not None:
            random.seed(seed)

        # Select which formula type to embed
        formula_types = ['single_point_plotting', 'all_four_quadrants',
                        'distance_between_points', 'midpoint_calculation']
        formula_type = random.choice(formula_types)
        variant = random.randint(0, 2)  # 3 variants per formula type

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['coordinate']

        if formula_type == 'single_point_plotting':
            # Generate x and y coordinates with at least one negative
            x = random.randint(min_val, max_val)
            y = random.randint(min_val, max_val)

            # Ensure at least one coordinate is negative
            attempts = 0
            while x >= 0 and y >= 0 and attempts < 20:
                x = random.randint(min_val, max_val)
                y = random.randint(min_val, max_val)
                attempts += 1

            correct_answer = (x, y)
            malrule_answer = (abs(x), abs(y))

            templates = [
                f"A treasure is buried at coordinates ({x}, {y}) on a map. What are the coordinates of the treasure location?",
                f"A drone is hovering at position ({x}, {y}) on a coordinate grid. What are the exact coordinates of the drone?",
                f"In a video game, your character is at location ({x}, {y}). Record the coordinates of your position."
            ]

            return Problem(
                text=templates[variant],
                operands=[x, y],
                operation='coordinate_plotting',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'x': x,
                    'y': y,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'template': 'word_problem',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        elif formula_type == 'all_four_quadrants':
            # Generate point in quadrants II, III, or IV (with at least one negative)
            quadrants = [
                (2, 'II', lambda: (random.randint(min_val, -1), random.randint(1, max_val))),
                (3, 'III', lambda: (random.randint(min_val, -1), random.randint(min_val, -1))),
                (4, 'IV', lambda: (random.randint(1, max_val), random.randint(min_val, -1)))
            ]

            quadrant_num, correct_quadrant, coord_generator = random.choice(quadrants)
            x, y = coord_generator()
            malrule_quadrant = 'I'  # Student uses absolute values, always gets Quadrant I

            templates = [
                f"A satellite is positioned at coordinates ({x}, {y}). Which quadrant of the coordinate system is it in?",
                f"On a city map, a landmark is at ({x}, {y}). Determine which quadrant contains this landmark.",
                f"A robot's sensor detects an object at ({x}, {y}). In which quadrant is this object located?"
            ]

            return Problem(
                text=templates[variant],
                operands=[x, y],
                operation='quadrant_identification',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'x': x,
                    'y': y,
                    'correct_answer': correct_quadrant,
                    'malrule_answer': malrule_quadrant,
                    'template': 'word_problem',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        elif formula_type == 'distance_between_points':
            # Generate two points ensuring they span across axes to avoid malrule=correct edge cases
            x1 = random.randint(min_val, max_val)
            y1 = random.randint(min_val, max_val)
            x2 = random.randint(min_val, max_val)
            y2 = random.randint(min_val, max_val)

            # Ensure at least one coordinate has opposite signs AND avoid zeros
            # This ensures malrule gives different answer
            attempts = 0
            while ((x1 >= 0 and y1 >= 0 and x2 >= 0 and y2 >= 0) or
                   x1 == 0 or y1 == 0 or x2 == 0 or y2 == 0 or
                   ((x1 > 0) == (x2 > 0) and (y1 > 0) == (y2 > 0))) and attempts < 20:
                x1 = random.randint(min_val, max_val)
                y1 = random.randint(min_val, max_val)
                x2 = random.randint(min_val, max_val)
                y2 = random.randint(min_val, max_val)
                attempts += 1

            # Calculate correct distance
            dx = x2 - x1
            dy = y2 - y1
            correct_distance = round((dx**2 + dy**2)**0.5, 2)

            # Malrule: student uses absolute values
            malrule_dx = abs(x2) - abs(x1)
            malrule_dy = abs(y2) - abs(y1)
            malrule_distance = round((malrule_dx**2 + malrule_dy**2)**0.5, 2)

            templates = [
                f"A ship travels from port A at ({x1}, {y1}) to port B at ({x2}, {y2}). What is the straight-line distance between the ports?",
                f"An airplane flies from checkpoint ({x1}, {y1}) to checkpoint ({x2}, {y2}). Calculate the direct distance traveled.",
                f"On a treasure map, two landmarks are at ({x1}, {y1}) and ({x2}, {y2}). Find the distance between them."
            ]

            return Problem(
                text=templates[variant],
                operands=[x1, y1, x2, y2],
                operation='distance_calculation',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'x1': x1,
                    'y1': y1,
                    'x2': x2,
                    'y2': y2,
                    'dx': dx,
                    'dy': dy,
                    'correct_answer': correct_distance,
                    'malrule_answer': malrule_distance,
                    'template': 'word_problem',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        else:  # midpoint_calculation
            # Generate two points with at least one negative coordinate
            x1 = random.randint(min_val, max_val)
            y1 = random.randint(min_val, max_val)
            x2 = random.randint(min_val, max_val)
            y2 = random.randint(min_val, max_val)

            # Ensure at least one coordinate is negative
            attempts = 0
            while (x1 >= 0 and y1 >= 0 and x2 >= 0 and y2 >= 0) and attempts < 20:
                x1 = random.randint(min_val, max_val)
                y1 = random.randint(min_val, max_val)
                attempts += 1

            # Calculate correct midpoint
            midpoint_x = round((x1 + x2) / 2, 1)
            midpoint_y = round((y1 + y2) / 2, 1)
            correct_midpoint = (midpoint_x, midpoint_y)

            # Malrule: student uses absolute values
            malrule_midpoint_x = round((abs(x1) + abs(x2)) / 2, 1)
            malrule_midpoint_y = round((abs(y1) + abs(y2)) / 2, 1)
            malrule_midpoint = (malrule_midpoint_x, malrule_midpoint_y)

            templates = [
                f"On a map, City A is at ({x1}, {y1}) and City B is at ({x2}, {y2}). Find the coordinates of the point halfway between them.",
                f"Two radio towers are located at ({x1}, {y1}) and ({x2}, {y2}). What are the coordinates of the midpoint between them?",
                f"A hiking trail has markers at ({x1}, {y1}) and ({x2}, {y2}). Determine the coordinates of the point exactly in the middle."
            ]

            return Problem(
                text=templates[variant],
                operands=[x1, y1, x2, y2],
                operation='midpoint_calculation',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'x1': x1,
                    'y1': y1,
                    'x2': x2,
                    'y2': y2,
                    'correct_answer': correct_midpoint,
                    'malrule_answer': malrule_midpoint,
                    'template': 'word_problem',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )
