"""
Problem generator for Swap-Ratios-Or-Units malrule.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple
from utils import ProblemGenerator, Problem, DifficultyLevel


class SwapRatiosOrUnitsProblemGenerator(ProblemGenerator):
    """Generates proportion problems where setup matters."""

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        ranges = {
            6: {
                DifficultyLevel.EASY: {'quantity': (2, 5), 'cost': (2, 8), 'new_quantity': (3, 8)},
                DifficultyLevel.MEDIUM: {'quantity': (2, 8), 'cost': (3, 12), 'new_quantity': (4, 10)},
                DifficultyLevel.HARD: {'quantity': (3, 10), 'cost': (4, 15), 'new_quantity': (5, 15)}
            },
            7: {
                DifficultyLevel.EASY: {'quantity': (2, 8), 'cost': (3, 12), 'new_quantity': (4, 10)},
                DifficultyLevel.MEDIUM: {'quantity': (3, 10), 'cost': (4, 15), 'new_quantity': (5, 15)},
                DifficultyLevel.HARD: {'quantity': (4, 12), 'cost': (5, 20), 'new_quantity': (6, 18)}
            },
            8: {
                DifficultyLevel.EASY: {'quantity': (3, 10), 'cost': (4, 15), 'new_quantity': (5, 15)},
                DifficultyLevel.MEDIUM: {'quantity': (4, 12), 'cost': (5, 20), 'new_quantity': (6, 18)},
                DifficultyLevel.HARD: {'quantity': (5, 15), 'cost': (6, 25), 'new_quantity': (8, 20)}
            },
            9: {
                DifficultyLevel.EASY: {'quantity': (4, 12), 'cost': (5, 20), 'new_quantity': (6, 18)},
                DifficultyLevel.MEDIUM: {'quantity': (5, 15), 'cost': (6, 25), 'new_quantity': (8, 20)},
                DifficultyLevel.HARD: {'quantity': (6, 20), 'cost': (8, 30), 'new_quantity': (10, 25)}
            }
        }
        lvl = self.level if self.level in ranges else 7
        return ranges[lvl][self.difficulty]

    def generate(self, seed=None) -> Problem:
        if seed is not None:
            random.seed(seed)

        # Choose problem type
        problem_types = ['basic_cost_quantity']

        # Add enhanced problem types for higher levels
        if self.level >= 7:
            problem_types.extend([
                'speed_time_distance',    # Speed/time/distance proportions
                'recipe_scaling',         # Recipe ingredient scaling
                'map_scale',              # Map scale with actual vs map distance
                'density_volume_mass',    # Density problems with mass and volume
            ])

        problem_type = random.choice(problem_types)

        # Handle enhanced problem types first
        if problem_type == 'speed_time_distance':
            # Speed/time/distance: distance/time = speed, student might swap
            speeds = [(60, 2, 120), (80, 3, 240), (50, 4, 200), (100, 5, 500)]
            distance1, time1, check = random.choice(speeds)

            ranges = self.get_value_ranges()
            time2 = random.randint(max(1, ranges['new_quantity'][0] - 1), ranges['new_quantity'][1])

            # Ensure time2 ≠ time1
            attempts = 0
            while time2 == time1 and attempts < 20:
                time2 = random.randint(max(1, ranges['new_quantity'][0] - 1), ranges['new_quantity'][1])
                attempts += 1

            # Correct: distance1/time1 = x/time2 → x = (distance1 * time2) / time1
            correct_answer = (distance1 * time2) / time1

            # Malrule: Swap unknown position: distance1/time1 = time2/x
            # Cross multiply: distance1 * x = time1 * time2 → x = (time1 * time2) / distance1
            malrule_answer = (time1 * time2) / distance1

            text = f"A car travels {distance1} miles in {time1} hours. At the same speed, how far will it travel in {time2} hours?"

            return Problem(
                text=text,
                operands=[distance1, time1, time2],
                operation='speed_proportion',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'problem_type': problem_type,
                    'distance1': distance1,
                    'time1': time1,
                    'time2': time2,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer
                }
            )

        elif problem_type == 'recipe_scaling':
            # Recipe scaling: flour/servings, student might swap
            recipes = [(2, 8, 'cups of flour'), (3, 12, 'eggs'), (4, 16, 'ounces of sugar'), (5, 20, 'tablespoons of butter')]
            ingredient_amount, servings1, ingredient_name = random.choice(recipes)

            ranges = self.get_value_ranges()
            servings2 = random.randint(ranges['new_quantity'][0], ranges['new_quantity'][1] + 2)

            # Ensure servings2 ≠ servings1
            attempts = 0
            while servings2 == servings1 and attempts < 20:
                servings2 = random.randint(ranges['new_quantity'][0], ranges['new_quantity'][1] + 2)
                attempts += 1

            # Correct: ingredient1/servings1 = x/servings2 → x = (ingredient_amount * servings2) / servings1
            correct_answer = (ingredient_amount * servings2) / servings1

            # Malrule: Swap unknown position: ingredient1/servings1 = servings2/x
            # Cross multiply: ingredient1 * x = servings1 * servings2 → x = (servings1 * servings2) / ingredient_amount
            malrule_answer = (servings1 * servings2) / ingredient_amount

            text = f"A recipe for {servings1} servings calls for {ingredient_amount} {ingredient_name}. How much do you need for {servings2} servings?"

            return Problem(
                text=text,
                operands=[ingredient_amount, servings1, servings2],
                operation='recipe_proportion',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'problem_type': problem_type,
                    'ingredient_amount': ingredient_amount,
                    'servings1': servings1,
                    'servings2': servings2,
                    'ingredient_name': ingredient_name,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer
                }
            )

        elif problem_type == 'map_scale':
            # Map scale: map_distance/actual_distance, student might swap
            scales = [(2, 50), (3, 75), (1, 25), (4, 100)]
            map_dist1, actual_dist1 = random.choice(scales)

            ranges = self.get_value_ranges()
            actual_dist2 = random.randint(ranges['new_quantity'][0] * 10, ranges['new_quantity'][1] * 15)

            # Correct: map1/actual1 = x/actual2 → x = (map_dist1 * actual_dist2) / actual_dist1
            correct_answer = (map_dist1 * actual_dist2) / actual_dist1

            # Malrule: Swap unknown position: map1/actual1 = actual2/x
            # Cross multiply: map1 * x = actual1 * actual2 → x = (actual_dist1 * actual_dist2) / map_dist1
            malrule_answer = (actual_dist1 * actual_dist2) / map_dist1

            text = f"On a map, {map_dist1} cm represents {actual_dist1} km. How many cm on the map would represent {actual_dist2} km?"

            return Problem(
                text=text,
                operands=[map_dist1, actual_dist1, actual_dist2],
                operation='map_scale_proportion',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'problem_type': problem_type,
                    'map_dist1': map_dist1,
                    'actual_dist1': actual_dist1,
                    'actual_dist2': actual_dist2,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer
                }
            )

        elif problem_type == 'density_volume_mass':
            # Density: mass/volume, student might swap
            densities = [(200, 50, 'grams', 'mL'), (300, 100, 'grams', 'cm³'), (150, 75, 'grams', 'mL')]
            mass1, volume1, mass_unit, volume_unit = random.choice(densities)

            ranges = self.get_value_ranges()
            volume2 = random.randint(ranges['new_quantity'][0] * 10, ranges['new_quantity'][1] * 15)

            # Correct: mass1/volume1 = x/volume2 → x = (mass1 * volume2) / volume1
            correct_answer = (mass1 * volume2) / volume1

            # Malrule: Swap unknown position: mass1/volume1 = volume2/x
            # Cross multiply: mass1 * x = volume1 * volume2 → x = (volume1 * volume2) / mass1
            malrule_answer = (volume1 * volume2) / mass1

            text = f"A substance has a mass of {mass1} {mass_unit} in {volume1} {volume_unit}. What mass would {volume2} {volume_unit} of the same substance have?"

            return Problem(
                text=text,
                operands=[mass1, volume1, volume2],
                operation='density_proportion',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'problem_type': problem_type,
                    'mass1': mass1,
                    'volume1': volume1,
                    'volume2': volume2,
                    'mass_unit': mass_unit,
                    'volume_unit': volume_unit,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer
                }
            )

        # Original basic problem type
        ranges = self.get_value_ranges()

        # Generate initial relationship: q1 items cost c1 dollars
        q1 = random.randint(ranges['quantity'][0], ranges['quantity'][1])
        c1 = random.randint(ranges['cost'][0], ranges['cost'][1])

        # Generate new quantity
        q2 = random.randint(ranges['new_quantity'][0], ranges['new_quantity'][1])

        # Ensure q2 ≠ q1
        attempts = 0
        while q2 == q1 and attempts < 20:
            q2 = random.randint(ranges['new_quantity'][0], ranges['new_quantity'][1])
            attempts += 1

        # Correct answer: Set up proportion correctly
        # Method: q1/c1 = q2/c2, so c2 = (q2 * c1) / q1
        correct_answer = (q2 * c1) / q1

        # Malrule answer: Swap the positions
        # Student sets up: q1/q2 = c1/c2 (quantities together, costs together - WRONG!)
        # This gives: c2 = (c1 * q2) / q1 (accidentally same formula!)
        #
        # Better malrule: Student inverts one side
        # Student: q1/c1 = c2/q2 (swaps unknown position)
        # This gives: c2 = (q1 * q2) / c1
        malrule_answer = (q1 * q2) / c1

        text = f"If {q1} items cost ${c1}, how much do {q2} items cost?"

        return Problem(
            text=text,
            operands=[q1, c1, q2],
            operation='proportion_setup',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'problem_type': 'basic_cost_quantity',
                'quantity1': q1,
                'cost1': c1,
                'quantity2': q2,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )
