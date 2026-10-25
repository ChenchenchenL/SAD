"""
Problem generator for Slope-Is-Delta-X-Over-Delta-Y malrule.

Generates slope calculation problems where students may invert the formula.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from fractions import Fraction
from typing import Dict, Tuple, List, Optional
from utils import ProblemGenerator, Problem, DifficultyLevel


class SlopeIsDeltaXOverDeltaYProblemGenerator(ProblemGenerator):
    """
    Generates slope calculation problems using two points.

    Templates:
    1. basic_two_points - Simple two-point slope calculation
    2. larger_coordinates - Points with larger coordinate values (adds complexity)
    3. real_world_rate - Word problems about rates (where formula inversion is common)
    4. negative_coordinates - Both points have negative coordinates
    5. mixed_quadrants - Points in different quadrants
    """

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_two_points',
            'larger_coordinates',
            'real_world_rate',
            'negative_coordinates',
            'mixed_quadrants'
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        ranges = {
            7: {
                DifficultyLevel.EASY: {'min': -5, 'max': 10},
                DifficultyLevel.MEDIUM: {'min': -8, 'max': 15},
                DifficultyLevel.HARD: {'min': -10, 'max': 20}
            },
            8: {
                DifficultyLevel.EASY: {'min': -8, 'max': 12},
                DifficultyLevel.MEDIUM: {'min': -10, 'max': 15},
                DifficultyLevel.HARD: {'min': -15, 'max': 20}
            },
            9: {
                DifficultyLevel.EASY: {'min': -10, 'max': 15},
                DifficultyLevel.MEDIUM: {'min': -12, 'max': 20},
                DifficultyLevel.HARD: {'min': -15, 'max': 25}
            },
            10: {
                DifficultyLevel.EASY: {'min': -10, 'max': 15},
                DifficultyLevel.MEDIUM: {'min': -15, 'max': 20},
                DifficultyLevel.HARD: {'min': -20, 'max': 30}
            }
        }
        lvl = self.level if self.level in ranges else 8
        return ranges[lvl][self.difficulty]

    def generate(self, seed=None, template: Optional[str] = None) -> Problem:
        """
        Generate a slope calculation problem based on selected template.

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
        if template == 'basic_two_points':
            return self._generate_basic_two_points(seed)
        elif template == 'larger_coordinates':
            return self._generate_larger_coordinates(seed)
        elif template == 'real_world_rate':
            return self._generate_real_world_rate(seed)
        elif template == 'negative_coordinates':
            return self._generate_negative_coordinates(seed)
        elif template == 'mixed_quadrants':
            return self._generate_mixed_quadrants(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_two_points(self, seed=None) -> Problem:
        """Generate basic two-point slope calculation."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val = ranges['min']
        max_val = ranges['max']

        # Generate two distinct points with non-trivial slope
        x1, y1, x2, y2, delta_x, delta_y, slope, malrule_slope = self._generate_valid_points(
            min_val, max_val
        )

        # Format answers
        correct_answer_str = self._format_fraction(slope)
        malrule_answer_str = self._format_fraction(malrule_slope)

        text = f"Find the slope of the line passing through points ({x1}, {y1}) and ({x2}, {y2})."

        return Problem(
            text=text,
            operands=[x1, y1, x2, y2],
            operation='slope_calculation',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'x1': x1,
                'y1': y1,
                'x2': x2,
                'y2': y2,
                'delta_x': delta_x,
                'delta_y': delta_y,
                'slope': slope,
                'malrule_slope': malrule_slope,
                'correct_answer': correct_answer_str,
                'malrule_answer': malrule_answer_str,
                'template': 'basic_two_points'
            }
        )

    def _generate_larger_coordinates(self, seed=None) -> Problem:
        """Generate problem with larger coordinate values (10-30 range)."""
        if seed is not None:
            random.seed(seed)

        # Use larger range for coordinates
        min_val = 10
        max_val = 30

        x1, y1, x2, y2, delta_x, delta_y, slope, malrule_slope = self._generate_valid_points(
            min_val, max_val
        )

        correct_answer_str = self._format_fraction(slope)
        malrule_answer_str = self._format_fraction(malrule_slope)

        text = f"Find the slope of the line passing through points ({x1}, {y1}) and ({x2}, {y2})."

        return Problem(
            text=text,
            operands=[x1, y1, x2, y2],
            operation='slope_calculation',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'x1': x1,
                'y1': y1,
                'x2': x2,
                'y2': y2,
                'delta_x': delta_x,
                'delta_y': delta_y,
                'slope': slope,
                'malrule_slope': malrule_slope,
                'correct_answer': correct_answer_str,
                'malrule_answer': malrule_answer_str,
                'template': 'larger_coordinates'
            }
        )

    def _generate_real_world_rate(self, seed=None) -> Problem:
        """Generate word problem about rates with multiple question variations per context."""
        if seed is not None:
            random.seed(seed)

        # Generate points with positive values for real-world context
        min_val = 1
        max_val = 20

        x1, y1, x2, y2, delta_x, delta_y, slope, malrule_slope = self._generate_valid_points(
            min_val, max_val, ensure_positive=True
        )

        correct_answer_str = self._format_fraction(slope)
        malrule_answer_str = self._format_fraction(malrule_slope)

        # Three context scenarios, each with 3 question variations
        contexts = [
            {
                'type': 'cost_per_item',
                'interpretation': 'dollars per item',
                'questions': [
                    f"A store sells {x1} items for ${y1} and {x2} items for ${y2}. What is the cost per item (slope)?",
                    f"When buying {x1} items, the cost is ${y1}. When buying {x2} items, the cost is ${y2}. Calculate the unit price (slope).",
                    f"The price for {x1} units is ${y1}, and for {x2} units is ${y2}. Find the rate per item (slope)."
                ]
            },
            {
                'type': 'distance_time',
                'interpretation': 'miles per hour',
                'questions': [
                    f"A car travels {y1} miles in {x1} hours and {y2} miles in {x2} hours. What is the speed (slope)?",
                    f"After {x1} hours, a vehicle has gone {y1} miles. After {x2} hours, it has gone {y2} miles. Calculate the speed (slope).",
                    f"At time {x1} hours, distance is {y1} miles. At time {x2} hours, distance is {y2} miles. Find the rate of travel (slope)."
                ]
            },
            {
                'type': 'elevation_distance',
                'interpretation': 'feet per mile',
                'questions': [
                    f"A trail rises to {y1} feet elevation at {x1} miles and {y2} feet at {x2} miles. What is the grade (slope)?",
                    f"At {x1} miles along a path, elevation is {y1} feet. At {x2} miles, elevation is {y2} feet. Find the slope of the trail.",
                    f"The trail elevation is {y1} ft at the {x1}-mile mark and {y2} ft at the {x2}-mile mark. Calculate the gradient (slope)."
                ]
            },
            {
                'type': 'temperature_time',
                'interpretation': 'degrees per hour',
                'questions': [
                    f"Temperature is {y1}°F at {x1} hours and {y2}°F at {x2} hours. What is the rate of temperature change (slope)?",
                    f"After {x1} hours, the temperature is {y1} degrees. After {x2} hours, it is {y2} degrees. Find the heating rate (slope).",
                    f"At hour {x1}, temp is {y1}°F. At hour {x2}, temp is {y2}°F. Calculate the temperature change rate (slope)."
                ]
            },
            {
                'type': 'water_level',
                'interpretation': 'inches per minute',
                'questions': [
                    f"A pool's water level is {y1} inches at {x1} minutes and {y2} inches at {x2} minutes. What is the filling rate (slope)?",
                    f"After {x1} minutes, water depth is {y1} inches. After {x2} minutes, depth is {y2} inches. Find the rate (slope).",
                    f"At {x1} min, the level is {y1} in. At {x2} min, the level is {y2} in. Calculate the fill rate (slope)."
                ]
            },
            {
                'type': 'earnings_hours',
                'interpretation': 'dollars per hour',
                'questions': [
                    f"Working {x1} hours earns ${y1}, and {x2} hours earns ${y2}. What is the hourly wage (slope)?",
                    f"After {x1} hours, earnings are ${y1}. After {x2} hours, earnings are ${y2}. Find the pay rate (slope).",
                    f"For {x1} hrs of work, pay is ${y1}. For {x2} hrs, pay is ${y2}. Calculate hourly rate (slope)."
                ]
            }
        ]

        context = random.choice(contexts)
        question_text = random.choice(context['questions'])

        return Problem(
            text=question_text,
            operands=[x1, y1, x2, y2],
            operation='slope_calculation_real_world',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'x1': x1,
                'y1': y1,
                'x2': x2,
                'y2': y2,
                'delta_x': delta_x,
                'delta_y': delta_y,
                'slope': slope,
                'malrule_slope': malrule_slope,
                'correct_answer': f"{correct_answer_str} {context['interpretation']}",
                'malrule_answer': f"{malrule_answer_str} {context['interpretation']}",
                'context_type': context['type'],
                'template': 'real_world_rate'
            }
        )

    def _generate_negative_coordinates(self, seed=None) -> Problem:
        """Generate problem where both points have negative coordinates."""
        if seed is not None:
            random.seed(seed)

        # Use negative range
        min_val = -20
        max_val = -2

        x1, y1, x2, y2, delta_x, delta_y, slope, malrule_slope = self._generate_valid_points(
            min_val, max_val
        )

        correct_answer_str = self._format_fraction(slope)
        malrule_answer_str = self._format_fraction(malrule_slope)

        text = f"Find the slope of the line passing through points ({x1}, {y1}) and ({x2}, {y2})."

        return Problem(
            text=text,
            operands=[x1, y1, x2, y2],
            operation='slope_calculation',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'x1': x1,
                'y1': y1,
                'x2': x2,
                'y2': y2,
                'delta_x': delta_x,
                'delta_y': delta_y,
                'slope': slope,
                'malrule_slope': malrule_slope,
                'correct_answer': correct_answer_str,
                'malrule_answer': malrule_answer_str,
                'template': 'negative_coordinates'
            }
        )

    def _generate_mixed_quadrants(self, seed=None) -> Problem:
        """Generate problem with points in different quadrants."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val = ranges['min']
        max_val = ranges['max']

        # Ensure one point is in negative region, one in positive
        attempts = 0
        while attempts < 100:
            x1 = random.randint(min_val, -1)  # Negative x
            y1 = random.randint(min_val, max_val)
            x2 = random.randint(1, max_val)  # Positive x
            y2 = random.randint(min_val, max_val)

            # Calculate deltas
            delta_x = x2 - x1
            delta_y = y2 - y1

            # Avoid trivial slopes
            if delta_x == 0 or delta_y == 0:
                attempts += 1
                continue

            slope = Fraction(delta_y, delta_x)
            malrule_slope = Fraction(delta_x, delta_y)

            # Ensure slopes are different
            if slope != malrule_slope and abs(slope) != 1:
                break

            attempts += 1

        # Fallback if needed
        if attempts >= 100:
            x1, y1 = -4, 3
            x2, y2 = 5, 13
            delta_x = x2 - x1
            delta_y = y2 - y1
            slope = Fraction(delta_y, delta_x)
            malrule_slope = Fraction(delta_x, delta_y)

        correct_answer_str = self._format_fraction(slope)
        malrule_answer_str = self._format_fraction(malrule_slope)

        text = f"Find the slope of the line passing through points ({x1}, {y1}) and ({x2}, {y2})."

        return Problem(
            text=text,
            operands=[x1, y1, x2, y2],
            operation='slope_calculation',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'x1': x1,
                'y1': y1,
                'x2': x2,
                'y2': y2,
                'delta_x': delta_x,
                'delta_y': delta_y,
                'slope': slope,
                'malrule_slope': malrule_slope,
                'correct_answer': correct_answer_str,
                'malrule_answer': malrule_answer_str,
                'template': 'mixed_quadrants'
            }
        )

    def _generate_valid_points(self, min_val: int, max_val: int, ensure_positive: bool = False) -> tuple:
        """
        Generate two distinct points with non-trivial slope.

        Returns: (x1, y1, x2, y2, delta_x, delta_y, slope, malrule_slope)
        """
        attempts = 0
        while attempts < 100:
            x1 = random.randint(min_val, max_val)
            y1 = random.randint(min_val, max_val)
            x2 = random.randint(min_val, max_val)
            y2 = random.randint(min_val, max_val)

            # Ensure positive if required
            if ensure_positive:
                x1, y1 = abs(x1) + 1, abs(y1) + 1
                x2, y2 = abs(x2) + 1, abs(y2) + 1

            # Ensure points are distinct
            if x1 == x2 or y1 == y2:
                attempts += 1
                continue

            # Calculate deltas
            delta_x = x2 - x1
            delta_y = y2 - y1

            # Avoid undefined or zero slopes
            if delta_x == 0 or delta_y == 0:
                attempts += 1
                continue

            # Calculate slopes
            slope = Fraction(delta_y, delta_x)
            malrule_slope = Fraction(delta_x, delta_y)

            # Ensure slopes are different (avoid ±1 slopes)
            if slope == malrule_slope or abs(slope) == 1:
                attempts += 1
                continue

            return x1, y1, x2, y2, delta_x, delta_y, slope, malrule_slope

        # Fallback to known good values
        x1, y1 = 2, 3
        x2, y2 = 5, 11
        delta_x = 3
        delta_y = 8
        slope = Fraction(8, 3)
        malrule_slope = Fraction(3, 8)
        return x1, y1, x2, y2, delta_x, delta_y, slope, malrule_slope

    def _format_fraction(self, frac: Fraction) -> str:
        """Format a fraction for display."""
        if frac.denominator == 1:
            return str(frac.numerator)
        else:
            return f"{frac.numerator}/{frac.denominator}"
