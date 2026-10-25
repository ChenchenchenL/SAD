"""
Malrule algorithm for Swap-Ratios-Or-Units error.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class SwapRatiosOrUnitsMalrule(Malrule):
    """
    Students set up proportions with swapped or inverted positions.

    Example: If 3 items cost $6, how much do 5 items cost?
    Student: 3/6 = x/5 (swaps unknown position) → x = 2.5 (wrong!)
    Correct: 3/6 = 5/x → x = 10
    """

    def get_name(self) -> str:
        return "Proportion Setup Error (Inverted Ratio Positions)"

    def get_description(self) -> str:
        return (
            "Student incorrectly sets up proportion equations by placing values in wrong "
            "positions, inverting the relationship between quantities. This includes confusing "
            "direct and inverse proportions, and misaligning corresponding terms in the equation."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Compute malrule answer algorithmically
        problem_type = problem.metadata.get('problem_type', 'basic_cost_quantity')
        
        if problem_type == 'basic_cost_quantity':
            q1 = problem.metadata['quantity1']
            c1 = problem.metadata['cost1']
            q2 = problem.metadata['quantity2']
            return round((q1 * q2) / c1, 2)
        elif problem_type == 'speed_time_distance':
            distance1 = problem.metadata['distance1']
            time1 = problem.metadata['time1']
            time2 = problem.metadata['time2']
            # Malrule: distance1/time1 = time2/x → x = (time1 * time2) / distance1
            return round((time1 * time2) / distance1, 2)
        elif problem_type == 'recipe_scaling':
            ingredient_amount = problem.metadata['ingredient_amount']
            servings1 = problem.metadata['servings1']
            servings2 = problem.metadata['servings2']
            # Malrule: ingredient/servings1 = servings2/x → x = (servings1 * servings2) / ingredient
            return round((servings1 * servings2) / ingredient_amount, 2)
        elif problem_type == 'map_scale':
            map_dist1 = problem.metadata['map_dist1']
            actual_dist1 = problem.metadata['actual_dist1']
            actual_dist2 = problem.metadata['actual_dist2']
            # Malrule: map1/actual1 = actual2/x → x = (actual1 * actual2) / map1
            return round((actual_dist1 * actual_dist2) / map_dist1, 2)
        elif problem_type == 'density_volume_mass':
            mass1 = problem.metadata['mass1']
            volume1 = problem.metadata['volume1']
            volume2 = problem.metadata['volume2']
            # Malrule: mass1/volume1 = volume2/x → x = (volume1 * volume2) / mass1
            return round((volume1 * volume2) / mass1, 2)
        
        # Fallback
        return round(problem.metadata.get('malrule_answer', 0), 2)

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
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

        # MALRULE: q1/c1 = x/q2 → x = (q1 * q2) / c1
        malrule_answer = (q1 * q2) / c1

        # Calculate correct answer independently
        correct_answer = (c1 * q2) / q1

        if verbose:
            steps = self._generate_verbose_basic(q1, c1, q2, malrule_answer, correct_answer)
        else:
            steps = self._generate_concise_basic(q1, c1, q2, malrule_answer, correct_answer)

        return Solution(
            answer=round(malrule_answer, 2),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _generate_concise_basic(self, q1, c1, q2, malrule_answer, correct_answer):
        """Generate concise steps for basic cost/quantity problem (malrule)."""
        return [
            f"Question: If {q1} items cost ${c1}, how much do {q2} items cost?",
            f"Formula: {q1}/{c1} = x/{q2}",
            f"Step 1: {q1} × {q2} = {c1} × x",
            f"Step 2: {q1 * q2} = {c1}x",
            f"Step 3: x = {q1 * q2}/{c1}",
            f"Step 4: x = {malrule_answer:.2f}",
            f"Answer: ${malrule_answer:.2f}"
        ]

    def _generate_verbose_basic(self, q1, c1, q2, malrule_answer, correct_answer):
        """Generate verbose steps for basic cost/quantity problem (malrule)."""
        steps = []
        steps.append(f"Problem: If {q1} items cost ${c1}, how much do {q2} items cost?")
        steps.append("")
        steps.append("MALRULE: Set up proportion but swap unknown position")
        steps.append(f"  MALRULE REASONING: 'Put unknown in numerator instead of denominator'")
        steps.append("")
        steps.append(f"Step 1: Set up (INCORRECT) proportion")
        steps.append(f"  Student writes: {q1}/{c1} = x/{q2}")
        steps.append(f"  (Swapped! Should be {q1}/{c1} = {q2}/x)")
        steps.append("")
        steps.append(f"Step 2: Cross multiply")
        steps.append(f"  {q1} × {q2} = {c1} × x")
        steps.append(f"  {q1 * q2} = {c1}x")
        steps.append("")
        steps.append(f"Step 3: Solve for x")
        steps.append(f"  x = {q1 * q2}/{c1}")
        steps.append(f"  x = {malrule_answer:.2f}")
        steps.append("")
        steps.append(f"Final Answer: ${malrule_answer:.2f} (INCORRECT - wrong proportion setup!)")
        steps.append(f"  Should be: {q1}/{c1} = {q2}/x → x = {correct_answer:.2f}")
        return steps

    def _handle_speed_time_distance(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle speed/time/distance with swapped unknown position."""
        distance1 = problem.metadata['distance1']
        time1 = problem.metadata['time1']
        time2 = problem.metadata['time2']

        # MALRULE: distance1/time1 = time2/x → x = (time1 * time2) / distance1
        malrule_answer = (time1 * time2) / distance1

        # Calculate correct answer independently
        correct_answer = (distance1 * time2) / time1

        if verbose:
            steps = self._generate_verbose_speed_time_distance(problem, distance1, time1, time2, malrule_answer, correct_answer)
        else:
            steps = self._generate_concise_speed_time_distance(problem, distance1, time1, time2, malrule_answer, correct_answer)

        return Solution(
            answer=round(malrule_answer, 2),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _generate_concise_speed_time_distance(self, problem, distance1, time1, time2, malrule_answer, correct_answer):
        """Generate concise steps for speed/time/distance problem (malrule)."""
        return [
            f"Question: {problem.text}",
            f"Formula: {distance1}/{time1} = {time2}/x",
            f"Step 1: {distance1} × x = {time1} × {time2}",
            f"Step 2: {distance1}x = {time1 * time2}",
            f"Step 3: x = {time1 * time2}/{distance1}",
            f"Step 4: x = {malrule_answer:.2f}",
            f"Answer: {malrule_answer:.2f} miles"
        ]

    def _generate_verbose_speed_time_distance(self, problem, distance1, time1, time2, malrule_answer, correct_answer):
        """Generate verbose steps for speed/time/distance problem (malrule)."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: Set up proportion but swap unknown position")
        steps.append(f"  MALRULE REASONING: 'Put unknown in denominator instead of numerator'")
        steps.append("")
        steps.append(f"Step 1: Set up (INCORRECT) proportion")
        steps.append(f"  Student writes: {distance1}/{time1} = {time2}/x")
        steps.append(f"  (Swapped! Should be {distance1}/{time1} = x/{time2})")
        steps.append("")
        steps.append(f"Step 2: Cross multiply")
        steps.append(f"  {distance1} × x = {time1} × {time2}")
        steps.append(f"  {distance1}x = {time1 * time2}")
        steps.append("")
        steps.append(f"Step 3: Solve for x")
        steps.append(f"  x = {time1 * time2}/{distance1}")
        steps.append(f"  x = {malrule_answer:.2f}")
        steps.append("")
        steps.append(f"Final Answer: {malrule_answer:.2f} miles (INCORRECT - swapped unknown!)")
        steps.append(f"  Correct: {distance1}/{time1} = x/{time2} → x = {correct_answer:.2f}")
        return steps

    def _handle_recipe_scaling(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle recipe scaling with swapped unknown position."""
        ingredient_amount = problem.metadata['ingredient_amount']
        servings1 = problem.metadata['servings1']
        servings2 = problem.metadata['servings2']
        ingredient_name = problem.metadata['ingredient_name']

        # MALRULE: ingredient/servings1 = servings2/x → x = (servings1 * servings2) / ingredient
        malrule_answer = (servings1 * servings2) / ingredient_amount

        # Calculate correct answer independently
        correct_answer = (ingredient_amount * servings2) / servings1

        if verbose:
            steps = self._generate_verbose_recipe_scaling(problem, ingredient_amount, servings1, servings2, ingredient_name, malrule_answer, correct_answer)
        else:
            steps = self._generate_concise_recipe_scaling(problem, ingredient_amount, servings1, servings2, ingredient_name, malrule_answer, correct_answer)

        return Solution(
            answer=round(malrule_answer, 2),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _generate_concise_recipe_scaling(self, problem, ingredient_amount, servings1, servings2, ingredient_name, malrule_answer, correct_answer):
        """Generate concise steps for recipe scaling problem (malrule)."""
        return [
            f"Question: {problem.text}",
            f"Formula: {ingredient_amount}/{servings1} = {servings2}/x",
            f"Step 1: {ingredient_amount} × x = {servings1} × {servings2}",
            f"Step 2: {ingredient_amount}x = {servings1 * servings2}",
            f"Step 3: x = {servings1 * servings2}/{ingredient_amount}",
            f"Step 4: x = {malrule_answer:.2f}",
            f"Answer: {malrule_answer:.2f} {ingredient_name}"
        ]

    def _generate_verbose_recipe_scaling(self, problem, ingredient_amount, servings1, servings2, ingredient_name, malrule_answer, correct_answer):
        """Generate verbose steps for recipe scaling problem (malrule)."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: Set up proportion but swap unknown position")
        steps.append(f"  MALRULE REASONING: 'Put unknown in denominator instead of numerator'")
        steps.append("")
        steps.append(f"Step 1: Set up (INCORRECT) proportion")
        steps.append(f"  Student writes: {ingredient_amount}/{servings1} = {servings2}/x")
        steps.append(f"  (Swapped! Should be {ingredient_amount}/{servings1} = x/{servings2})")
        steps.append("")
        steps.append(f"Step 2: Cross multiply")
        steps.append(f"  {ingredient_amount} × x = {servings1} × {servings2}")
        steps.append(f"  {ingredient_amount}x = {servings1 * servings2}")
        steps.append("")
        steps.append(f"Step 3: Solve for x")
        steps.append(f"  x = {servings1 * servings2}/{ingredient_amount}")
        steps.append(f"  x = {malrule_answer:.2f}")
        steps.append("")
        steps.append(f"Final Answer: {malrule_answer:.2f} {ingredient_name} (INCORRECT - swapped!)")
        steps.append(f"  Correct: {ingredient_amount}/{servings1} = x/{servings2} → x = {correct_answer:.2f}")
        return steps

    def _handle_map_scale(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle map scale with swapped unknown position."""
        map_dist1 = problem.metadata['map_dist1']
        actual_dist1 = problem.metadata['actual_dist1']
        actual_dist2 = problem.metadata['actual_dist2']

        # MALRULE: map1/actual1 = actual2/x → x = (actual1 * actual2) / map1
        malrule_answer = (actual_dist1 * actual_dist2) / map_dist1

        # Calculate correct answer independently
        correct_answer = (map_dist1 * actual_dist2) / actual_dist1

        if verbose:
            steps = self._generate_verbose_map_scale(problem, map_dist1, actual_dist1, actual_dist2, malrule_answer, correct_answer)
        else:
            steps = self._generate_concise_map_scale(problem, map_dist1, actual_dist1, actual_dist2, malrule_answer, correct_answer)

        return Solution(
            answer=round(malrule_answer, 2),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _generate_concise_map_scale(self, problem, map_dist1, actual_dist1, actual_dist2, malrule_answer, correct_answer):
        """Generate concise steps for map scale problem (malrule)."""
        return [
            f"Question: {problem.text}",
            f"Formula: {map_dist1}/{actual_dist1} = {actual_dist2}/x",
            f"Step 1: {map_dist1} × x = {actual_dist1} × {actual_dist2}",
            f"Step 2: {map_dist1}x = {actual_dist1 * actual_dist2}",
            f"Step 3: x = {actual_dist1 * actual_dist2}/{map_dist1}",
            f"Step 4: x = {malrule_answer:.2f}",
            f"Answer: {malrule_answer:.2f} cm"
        ]

    def _generate_verbose_map_scale(self, problem, map_dist1, actual_dist1, actual_dist2, malrule_answer, correct_answer):
        """Generate verbose steps for map scale problem (malrule)."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: Set up proportion but swap unknown position")
        steps.append(f"  MALRULE REASONING: 'Put unknown in denominator instead of numerator'")
        steps.append("")
        steps.append(f"Step 1: Set up (INCORRECT) proportion")
        steps.append(f"  Student writes: {map_dist1}/{actual_dist1} = {actual_dist2}/x")
        steps.append(f"  (Swapped! Should be {map_dist1}/{actual_dist1} = x/{actual_dist2})")
        steps.append("")
        steps.append(f"Step 2: Cross multiply")
        steps.append(f"  {map_dist1} × x = {actual_dist1} × {actual_dist2}")
        steps.append(f"  {map_dist1}x = {actual_dist1 * actual_dist2}")
        steps.append("")
        steps.append(f"Step 3: Solve for x")
        steps.append(f"  x = {actual_dist1 * actual_dist2}/{map_dist1}")
        steps.append(f"  x = {malrule_answer:.2f}")
        steps.append("")
        steps.append(f"Final Answer: {malrule_answer:.2f} cm (INCORRECT - swapped!)")
        steps.append(f"  Correct: {map_dist1}/{actual_dist1} = x/{actual_dist2} → x = {correct_answer:.2f}")
        return steps

    def _handle_density_volume_mass(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle density with swapped unknown position."""
        mass1 = problem.metadata['mass1']
        volume1 = problem.metadata['volume1']
        volume2 = problem.metadata['volume2']
        mass_unit = problem.metadata['mass_unit']
        volume_unit = problem.metadata['volume_unit']

        # MALRULE: mass1/volume1 = volume2/x → x = (volume1 * volume2) / mass1
        malrule_answer = (volume1 * volume2) / mass1

        # Calculate correct answer independently
        correct_answer = (mass1 * volume2) / volume1

        if verbose:
            steps = self._generate_verbose_density_volume_mass(problem, mass1, volume1, volume2, mass_unit, volume_unit, malrule_answer, correct_answer)
        else:
            steps = self._generate_concise_density_volume_mass(problem, mass1, volume1, volume2, mass_unit, volume_unit, malrule_answer, correct_answer)

        return Solution(
            answer=round(malrule_answer, 2),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _generate_concise_density_volume_mass(self, problem, mass1, volume1, volume2, mass_unit, volume_unit, malrule_answer, correct_answer):
        """Generate concise steps for density/volume/mass problem (malrule)."""
        return [
            f"Question: {problem.text}",
            f"Formula: {mass1}/{volume1} = {volume2}/x",
            f"Step 1: {mass1} × x = {volume1} × {volume2}",
            f"Step 2: {mass1}x = {volume1 * volume2}",
            f"Step 3: x = {volume1 * volume2}/{mass1}",
            f"Step 4: x = {malrule_answer:.2f}",
            f"Answer: {malrule_answer:.2f} {mass_unit}"
        ]

    def _generate_verbose_density_volume_mass(self, problem, mass1, volume1, volume2, mass_unit, volume_unit, malrule_answer, correct_answer):
        """Generate verbose steps for density/volume/mass problem (malrule)."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: Set up proportion but swap unknown position")
        steps.append(f"  MALRULE REASONING: 'Put unknown in denominator instead of numerator'")
        steps.append("")
        steps.append(f"Step 1: Set up (INCORRECT) proportion")
        steps.append(f"  Student writes: {mass1}/{volume1} = {volume2}/x")
        steps.append(f"  (Swapped! Should be {mass1}/{volume1} = x/{volume2})")
        steps.append("")
        steps.append(f"Step 2: Cross multiply")
        steps.append(f"  {mass1} × x = {volume1} × {volume2}")
        steps.append(f"  {mass1}x = {volume1 * volume2}")
        steps.append("")
        steps.append(f"Step 3: Solve for x")
        steps.append(f"  x = {volume1 * volume2}/{mass1}")
        steps.append(f"  x = {malrule_answer:.2f}")
        steps.append("")
        steps.append(f"Final Answer: {malrule_answer:.2f} {mass_unit} (INCORRECT - swapped!)")
        steps.append(f"  Correct: {mass1}/{volume1} = x/{volume2} → x = {correct_answer:.2f}")
        return steps
