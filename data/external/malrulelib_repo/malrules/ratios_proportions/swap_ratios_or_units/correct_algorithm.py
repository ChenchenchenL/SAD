"""
Correct algorithm for setting up proportions.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class ProportionSetupCorrectAlgorithm(CorrectAlgorithm):
    """Correctly sets up proportions with matching positions."""

    def get_name(self) -> str:
        return "Correct Proportion Setup"

    def get_description(self) -> str:
        return "Correctly sets up proportions maintaining corresponding positions."

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        problem_type = problem.metadata.get('problem_type', 'basic_cost_quantity')

        # Handle enhanced problem types
        if problem_type == 'speed_time_distance':
            return self._handle_speed_time_distance(problem, verbose)
        elif problem_type == 'recipe_scaling':
            return self._handle_recipe_scaling(problem, verbose)
        elif problem_type == 'map_scale':
            return self._handle_map_scale(problem, verbose)
        elif problem_type == 'density_volume_mass':
            return self._handle_density_volume_mass(problem, verbose)

        # Original basic problem type
        q1 = problem.metadata['quantity1']
        c1 = problem.metadata['cost1']
        q2 = problem.metadata['quantity2']

        # CORRECT: c2 = (q2 * c1) / q1
        correct_answer = (q2 * c1) / q1

        if verbose:
            steps = self._generate_verbose_basic(q1, c1, q2, correct_answer)
        else:
            steps = self._generate_concise_basic(q1, c1, q2, correct_answer)

        return Solution(
            answer=round(correct_answer, 2),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _generate_concise_basic(self, q1, c1, q2, correct_answer):
        """Generate concise steps for basic cost/quantity problem."""
        return [
            f"Question: If {q1} items cost ${c1}, how much do {q2} items cost?",
            f"Formula: {q1}/{c1} = {q2}/x",
            f"Step 1: {q1} × x = {c1} × {q2}",
            f"Step 2: {q1}x = {c1 * q2}",
            f"Step 3: x = {c1 * q2}/{q1}",
            f"Step 4: x = {correct_answer:.2f}",
            f"Answer: ${correct_answer:.2f}"
        ]

    def _generate_verbose_basic(self, q1, c1, q2, correct_answer):
        """Generate verbose steps for basic cost/quantity problem."""
        steps = []
        steps.append(f"Problem: If {q1} items cost ${c1}, how much do {q2} items cost?")
        steps.append("")
        steps.append("CORRECT METHOD: Set up proportion with matching positions")
        steps.append("")
        steps.append(f"Step 1: Identify corresponding values")
        steps.append(f"  Quantity 1: {q1} items")
        steps.append(f"  Cost 1: ${c1}")
        steps.append(f"  Quantity 2: {q2} items")
        steps.append(f"  Cost 2: unknown (x)")
        steps.append("")
        steps.append(f"Step 2: Set up proportion (KEEP POSITIONS MATCHING!)")
        steps.append(f"  quantity1/cost1 = quantity2/cost2")
        steps.append(f"  {q1}/{c1} = {q2}/x")
        steps.append("")
        steps.append(f"Step 3: Cross multiply")
        steps.append(f"  {q1} × x = {c1} × {q2}")
        steps.append(f"  {q1}x = {c1 * q2}")
        steps.append("")
        steps.append(f"  Step 4: Solve for x")
        steps.append(f"  x = {c1 * q2}/{q1}")
        steps.append(f"  x = {correct_answer:.2f}")
        steps.append("")
        steps.append(f"Final Answer: ${correct_answer:.2f} ✓")
        steps.append("")
        steps.append(f"Check: Unit rate = ${c1}/{q1} = ${c1/q1:.2f} per item")
        steps.append(f"       {q2} items × ${c1/q1:.2f}/item = ${correct_answer:.2f} ✓")
        return steps

    def _handle_speed_time_distance(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle speed/time/distance proportions correctly."""
        distance1 = problem.metadata['distance1']
        time1 = problem.metadata['time1']
        time2 = problem.metadata['time2']

        # CORRECT: distance2 = (distance1 * time2) / time1
        correct_answer = (distance1 * time2) / time1

        if verbose:
            steps = self._generate_verbose_speed_time_distance(problem, distance1, time1, time2, correct_answer)
        else:
            steps = self._generate_concise_speed_time_distance(problem, distance1, time1, time2, correct_answer)

        return Solution(
            answer=round(correct_answer, 2),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _generate_concise_speed_time_distance(self, problem, distance1, time1, time2, correct_answer):
        """Generate concise steps for speed/time/distance problem."""
        return [
            f"Question: {problem.text}",
            f"Formula: {distance1}/{time1} = x/{time2}",
            f"Step 1: {distance1} × {time2} = {time1} × x",
            f"Step 2: {distance1 * time2} = {time1}x",
            f"Step 3: x = {distance1 * time2}/{time1}",
            f"Step 4: x = {correct_answer:.2f}",
            f"Answer: {correct_answer:.2f} miles"
        ]

    def _generate_verbose_speed_time_distance(self, problem, distance1, time1, time2, correct_answer):
        """Generate verbose steps for speed/time/distance problem."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD: Set up proportion with matching positions")
        steps.append(f"  distance1/time1 = distance2/time2")
        steps.append("")
        steps.append(f"Step 1: Identify known values")
        steps.append(f"  Distance 1: {distance1} miles")
        steps.append(f"  Time 1: {time1} hours")
        steps.append(f"  Time 2: {time2} hours")
        steps.append(f"  Distance 2: unknown (x)")
        steps.append("")
        steps.append(f"Step 2: Set up proportion")
        steps.append(f"  {distance1}/{time1} = x/{time2}")
        steps.append("")
        steps.append(f"Step 3: Cross multiply")
        steps.append(f"  {distance1} × {time2} = {time1} × x")
        steps.append(f"  {distance1 * time2} = {time1}x")
        steps.append("")
        steps.append(f"Step 4: Solve for x")
        steps.append(f"  x = {distance1 * time2}/{time1}")
        steps.append(f"  x = {correct_answer:.2f}")
        steps.append("")
        steps.append(f"Final Answer: {correct_answer:.2f} miles ✓")
        return steps

    def _handle_recipe_scaling(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle recipe scaling proportions correctly."""
        ingredient_amount = problem.metadata['ingredient_amount']
        servings1 = problem.metadata['servings1']
        servings2 = problem.metadata['servings2']
        ingredient_name = problem.metadata['ingredient_name']

        # CORRECT: ingredient2 = (ingredient_amount * servings2) / servings1
        correct_answer = (ingredient_amount * servings2) / servings1

        if verbose:
            steps = self._generate_verbose_recipe_scaling(problem, ingredient_amount, servings1, servings2, ingredient_name, correct_answer)
        else:
            steps = self._generate_concise_recipe_scaling(problem, ingredient_amount, servings1, servings2, ingredient_name, correct_answer)

        return Solution(
            answer=round(correct_answer, 2),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _generate_concise_recipe_scaling(self, problem, ingredient_amount, servings1, servings2, ingredient_name, correct_answer):
        """Generate concise steps for recipe scaling problem."""
        return [
            f"Question: {problem.text}",
            f"Formula: {ingredient_amount}/{servings1} = x/{servings2}",
            f"Step 1: {ingredient_amount} × {servings2} = {servings1} × x",
            f"Step 2: {ingredient_amount * servings2} = {servings1}x",
            f"Step 3: x = {ingredient_amount * servings2}/{servings1}",
            f"Step 4: x = {correct_answer:.2f}",
            f"Answer: {correct_answer:.2f} {ingredient_name}"
        ]

    def _generate_verbose_recipe_scaling(self, problem, ingredient_amount, servings1, servings2, ingredient_name, correct_answer):
        """Generate verbose steps for recipe scaling problem."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD: Set up proportion with matching positions")
        steps.append(f"  ingredient1/servings1 = ingredient2/servings2")
        steps.append("")
        steps.append(f"Step 1: Identify known values")
        steps.append(f"  Ingredient amount: {ingredient_amount} {ingredient_name}")
        steps.append(f"  Servings (original): {servings1}")
        steps.append(f"  Servings (new): {servings2}")
        steps.append("")
        steps.append(f"Step 2: Set up proportion")
        steps.append(f"  {ingredient_amount}/{servings1} = x/{servings2}")
        steps.append("")
        steps.append(f"Step 3: Cross multiply")
        steps.append(f"  {ingredient_amount} × {servings2} = {servings1} × x")
        steps.append(f"  {ingredient_amount * servings2} = {servings1}x")
        steps.append("")
        steps.append(f"Step 4: Solve for x")
        steps.append(f"  x = {ingredient_amount * servings2}/{servings1}")
        steps.append(f"  x = {correct_answer:.2f}")
        steps.append("")
        steps.append(f"Final Answer: {correct_answer:.2f} {ingredient_name} ✓")
        return steps

    def _handle_map_scale(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle map scale proportions correctly."""
        map_dist1 = problem.metadata['map_dist1']
        actual_dist1 = problem.metadata['actual_dist1']
        actual_dist2 = problem.metadata['actual_dist2']

        # CORRECT: map2 = (map_dist1 * actual_dist2) / actual_dist1
        correct_answer = (map_dist1 * actual_dist2) / actual_dist1

        if verbose:
            steps = self._generate_verbose_map_scale(problem, map_dist1, actual_dist1, actual_dist2, correct_answer)
        else:
            steps = self._generate_concise_map_scale(problem, map_dist1, actual_dist1, actual_dist2, correct_answer)

        return Solution(
            answer=round(correct_answer, 2),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _generate_concise_map_scale(self, problem, map_dist1, actual_dist1, actual_dist2, correct_answer):
        """Generate concise steps for map scale problem."""
        return [
            f"Question: {problem.text}",
            f"Formula: {map_dist1}/{actual_dist1} = x/{actual_dist2}",
            f"Step 1: {map_dist1} × {actual_dist2} = {actual_dist1} × x",
            f"Step 2: {map_dist1 * actual_dist2} = {actual_dist1}x",
            f"Step 3: x = {map_dist1 * actual_dist2}/{actual_dist1}",
            f"Step 4: x = {correct_answer:.2f}",
            f"Answer: {correct_answer:.2f} cm"
        ]

    def _generate_verbose_map_scale(self, problem, map_dist1, actual_dist1, actual_dist2, correct_answer):
        """Generate verbose steps for map scale problem."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD: Set up proportion with matching positions")
        steps.append(f"  map1/actual1 = map2/actual2")
        steps.append("")
        steps.append(f"Step 1: Identify known values")
        steps.append(f"  Map distance 1: {map_dist1} cm")
        steps.append(f"  Actual distance 1: {actual_dist1} km")
        steps.append(f"  Actual distance 2: {actual_dist2} km")
        steps.append("")
        steps.append(f"Step 2: Set up proportion")
        steps.append(f"  {map_dist1}/{actual_dist1} = x/{actual_dist2}")
        steps.append("")
        steps.append(f"Step 3: Cross multiply")
        steps.append(f"  {map_dist1} × {actual_dist2} = {actual_dist1} × x")
        steps.append(f"  {map_dist1 * actual_dist2} = {actual_dist1}x")
        steps.append("")
        steps.append(f"Step 4: Solve for x")
        steps.append(f"  x = {map_dist1 * actual_dist2}/{actual_dist1}")
        steps.append(f"  x = {correct_answer:.2f}")
        steps.append("")
        steps.append(f"Final Answer: {correct_answer:.2f} cm ✓")
        return steps

    def _handle_density_volume_mass(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle density (mass/volume) proportions correctly."""
        mass1 = problem.metadata['mass1']
        volume1 = problem.metadata['volume1']
        volume2 = problem.metadata['volume2']
        mass_unit = problem.metadata['mass_unit']
        volume_unit = problem.metadata['volume_unit']

        # CORRECT: mass2 = (mass1 * volume2) / volume1
        correct_answer = (mass1 * volume2) / volume1

        if verbose:
            steps = self._generate_verbose_density_volume_mass(problem, mass1, volume1, volume2, mass_unit, volume_unit, correct_answer)
        else:
            steps = self._generate_concise_density_volume_mass(problem, mass1, volume1, volume2, mass_unit, volume_unit, correct_answer)

        return Solution(
            answer=round(correct_answer, 2),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _generate_concise_density_volume_mass(self, problem, mass1, volume1, volume2, mass_unit, volume_unit, correct_answer):
        """Generate concise steps for density/volume/mass problem."""
        return [
            f"Question: {problem.text}",
            f"Formula: {mass1}/{volume1} = x/{volume2}",
            f"Step 1: {mass1} × {volume2} = {volume1} × x",
            f"Step 2: {mass1 * volume2} = {volume1}x",
            f"Step 3: x = {mass1 * volume2}/{volume1}",
            f"Step 4: x = {correct_answer:.2f}",
            f"Answer: {correct_answer:.2f} {mass_unit}"
        ]

    def _generate_verbose_density_volume_mass(self, problem, mass1, volume1, volume2, mass_unit, volume_unit, correct_answer):
        """Generate verbose steps for density/volume/mass problem."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD: Set up proportion with matching positions")
        steps.append(f"  mass1/volume1 = mass2/volume2")
        steps.append("")
        steps.append(f"Step 1: Identify known values")
        steps.append(f"  Mass 1: {mass1} {mass_unit}")
        steps.append(f"  Volume 1: {volume1} {volume_unit}")
        steps.append(f"  Volume 2: {volume2} {volume_unit}")
        steps.append("")
        steps.append(f"Step 2: Set up proportion")
        steps.append(f"  {mass1}/{volume1} = x/{volume2}")
        steps.append("")
        steps.append(f"Step 3: Cross multiply")
        steps.append(f"  {mass1} × {volume2} = {volume1} × x")
        steps.append(f"  {mass1 * volume2} = {volume1}x")
        steps.append("")
        steps.append(f"Step 4: Solve for x")
        steps.append(f"  x = {mass1 * volume2}/{volume1}")
        steps.append(f"  x = {correct_answer:.2f}")
        steps.append("")
        steps.append(f"Final Answer: {correct_answer:.2f} {mass_unit} ✓")
        return steps
