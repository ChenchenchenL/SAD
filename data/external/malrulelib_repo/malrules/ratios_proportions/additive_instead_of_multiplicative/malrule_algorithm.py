"""
Malrule algorithm: Students use addition instead of multiplication when scaling ratios.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class AdditiveInsteadOfMultiplicativeMalrule(Malrule):
    """
    Malrule: Students use additive scaling instead of multiplicative scaling.

    Example: Scale 2:3 by factor 4
    Student: 2+4=6, 3+4=7 → 6:7 (WRONG)
    Correct: 2×4=8, 3×4=12 → 8:12
    """

    def get_name(self) -> str:
        return "Additive Strategy Error (Constant Difference)"

    def get_description(self) -> str:
        return (
            "Student applies additive reasoning instead of multiplicative reasoning when "
            "working with proportions. The student computes the difference between values "
            "and adds this constant to find missing values, rather than using the "
            "multiplicative scale factor."
        )

    def calculate_expected_answer(self, problem: Problem) -> str:
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Compute malrule answer algorithmically based on problem type/template
        template = problem.metadata.get('template', 'basic_scaling')

        if template == 'basic_scaling':
            a = problem.metadata['initial_a']
            b = problem.metadata['initial_b']
            k = problem.metadata['scale_factor']
            return f"{a + k}:{b + k}"

        elif template == 'recipe_scaling':
            amount1 = problem.metadata['initial_a']
            amount2 = problem.metadata['initial_b']
            k = problem.metadata['scale_factor']
            ingredient1 = problem.metadata['ingredient1']
            ingredient2 = problem.metadata['ingredient2']
            return f"{amount1 + k} {ingredient1} and {amount2 + k} {ingredient2}"

        elif template == 'speed_problems':
            distance = problem.metadata['distance']
            time1 = problem.metadata['time1']
            time2 = problem.metadata['time2']
            distance_unit = problem.metadata['distance_unit']
            time_diff = time2 - time1
            return f"{distance + time_diff} {distance_unit}"

        elif template == 'similar_figures':
            width = problem.metadata['initial_a']
            height = problem.metadata['initial_b']
            k = problem.metadata['scale_factor']
            return f"{width + k} cm by {height + k} cm"

        elif template == 'mixture_problems':
            parts1 = problem.metadata['initial_a']
            parts2 = problem.metadata['initial_b']
            k = problem.metadata['scale_factor']
            return f"{parts1 + k}:{parts2 + k}"

        elif template == 'word_problem_context':
            problem_type = problem.metadata.get('problem_type')

            if problem_type == 'direct_proportion_unknown':
                a = problem.metadata['ratio_a']
                b = problem.metadata['ratio_b']
                c = problem.metadata['given_c']
                difference = c - a
                return str(b + difference)

            elif problem_type == 'part_to_whole_ratio':
                a = problem.metadata['ratio_a']
                b = problem.metadata['ratio_b']
                k = problem.metadata['multiplier']
                return f"{a + k} and {b + k}"

            elif problem_type == 'three_part_ratio_scaling':
                a = problem.metadata['initial_a']
                b = problem.metadata['initial_b']
                c = problem.metadata['initial_c']
                k = problem.metadata['scale_factor']
                return f"{a + k}:{b + k}:{c + k}"

            elif problem_type == 'finding_multiplier':
                b = problem.metadata['ratio_b']
                scaled_value = problem.metadata['scaled_value']
                return str(scaled_value - b)

            elif problem_type == 'compound_scaling':
                a = problem.metadata['initial_a']
                b = problem.metadata['initial_b']
                k1 = problem.metadata['scale_factor_1']
                k2 = problem.metadata['scale_factor_2']
                return f"{a + k1 + k2}:{b + k1 + k2}"

        # Fallback to metadata if we can't compute
        return problem.metadata.get('malrule_answer', 'unknown')

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Implement incorrect (additive) scaling.

        Instead of: new_ratio = (a × k, b × k)
        Student does: new_ratio = (a + k, b + k)
        """
        template = problem.metadata.get('template', 'basic_scaling')

        # Route to appropriate handler based on template
        if template == 'basic_scaling':
            return self._handle_basic_scaling(problem, verbose)
        elif template == 'recipe_scaling':
            return self._handle_recipe_scaling(problem, verbose)
        elif template == 'speed_problems':
            return self._handle_speed_problems(problem, verbose)
        elif template == 'similar_figures':
            return self._handle_similar_figures(problem, verbose)
        elif template == 'mixture_problems':
            return self._handle_mixture_problems(problem, verbose)
        elif template == 'word_problem_context':
            return self._handle_word_problem_context(problem, verbose)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _handle_basic_scaling(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle basic ratio scaling with additive error."""
        a = problem.metadata['initial_a']
        b = problem.metadata['initial_b']
        k = problem.metadata['scale_factor']

        # INCORRECT: Add scale factor to each part
        malrule_a = a + k
        malrule_b = b + k
        malrule_answer = f"{malrule_a}:{malrule_b}"

        if verbose:
            steps = self._generate_verbose_basic_scaling(problem, a, b, k, malrule_a, malrule_b)
        else:
            steps = self._generate_concise_basic_scaling(problem, a, b, k, malrule_a, malrule_b)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _generate_concise_basic_scaling(self, problem: Problem, a: int, b: int, k: int,
                                         malrule_a: int, malrule_b: int) -> List[str]:
        """Generate concise steps for basic scaling malrule."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: ({a} + {k}) : ({b} + {k})")
        steps.append(f"Step 1: {a} + {k} = {malrule_a}")
        steps.append(f"Step 2: {b} + {k} = {malrule_b}")
        steps.append(f"Answer: {malrule_a}:{malrule_b}")
        return steps

    def _generate_verbose_basic_scaling(self, problem: Problem, a: int, b: int, k: int,
                                         malrule_a: int, malrule_b: int) -> List[str]:
        """Generate verbose steps for basic scaling malrule."""
        steps = []
        steps.append(f"Given ratio: {a}:{b}")
        steps.append(f"Scale factor: {k}")
        steps.append("")
        steps.append(f"MALRULE: 'Scale by {k}' means ADD {k} to each part")
        steps.append(f"  MALRULE REASONING: 'Scale means make bigger'")
        steps.append(f"                     'Bigger means add more'")
        steps.append("")
        steps.append(f"Step 1: Add {k} to first term: {a} + {k} = {malrule_a}")
        steps.append(f"Step 2: Add {k} to second term: {b} + {k} = {malrule_b}")
        steps.append("")
        steps.append(f"Final Answer: {malrule_a}:{malrule_b} (INCORRECT - should MULTIPLY, not ADD!)")
        steps.append(f"  Correct would be: {a}×{k} : {b}×{k} = {a*k}:{b*k}")
        steps.append(f"  Check: {a}/{b} = {a/b:.3f}, but {malrule_a}/{malrule_b} = {malrule_a/malrule_b:.3f} (different ratios!)")
        return steps

    def _handle_recipe_scaling(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle scaling recipe with additive error."""
        amount1 = problem.metadata['initial_a']
        amount2 = problem.metadata['initial_b']
        k = problem.metadata['scale_factor']
        ingredient1 = problem.metadata['ingredient1']
        ingredient2 = problem.metadata['ingredient2']

        # INCORRECT: Add to both amounts
        malrule_amount1 = amount1 + k
        malrule_amount2 = amount2 + k
        malrule_answer = f"{malrule_amount1} {ingredient1} and {malrule_amount2} {ingredient2}"

        if verbose:
            steps = self._generate_verbose_recipe_scaling(problem, amount1, amount2, k,
                                                           ingredient1, ingredient2,
                                                           malrule_amount1, malrule_amount2)
        else:
            steps = self._generate_concise_recipe_scaling(problem, amount1, amount2, k,
                                                           ingredient1, ingredient2,
                                                           malrule_amount1, malrule_amount2)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _generate_concise_recipe_scaling(self, problem: Problem, amount1: int, amount2: int, k: int,
                                          ingredient1: str, ingredient2: str,
                                          malrule_amount1: int, malrule_amount2: int) -> List[str]:
        """Generate concise steps for recipe scaling malrule."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: ({amount1} + {k}) {ingredient1}, ({amount2} + {k}) {ingredient2}")
        steps.append(f"Step 1: {amount1} + {k} = {malrule_amount1} {ingredient1}")
        steps.append(f"Step 2: {amount2} + {k} = {malrule_amount2} {ingredient2}")
        steps.append(f"Answer: {malrule_amount1} {ingredient1} and {malrule_amount2} {ingredient2}")
        return steps

    def _generate_verbose_recipe_scaling(self, problem: Problem, amount1: int, amount2: int, k: int,
                                          ingredient1: str, ingredient2: str,
                                          malrule_amount1: int, malrule_amount2: int) -> List[str]:
        """Generate verbose steps for recipe scaling malrule."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append(f"MALRULE: 'Scale by {k}' means ADD {k} to each ingredient")
        steps.append(f"  MALRULE REASONING: 'Need {k} times as much'")
        steps.append(f"                     'So add {k} to each amount'")
        steps.append("")
        steps.append(f"Step 1: Add {k} to first ingredient: {amount1} + {k} = {malrule_amount1} {ingredient1}")
        steps.append(f"Step 2: Add {k} to second ingredient: {amount2} + {k} = {malrule_amount2} {ingredient2}")
        steps.append("")
        steps.append(f"Scaled recipe: {malrule_amount1} {ingredient1} and {malrule_amount2} {ingredient2} (INCORRECT!)")
        steps.append(f"  Correct: {amount1}×{k} = {amount1 * k} {ingredient1}, {amount2}×{k} = {amount2 * k} {ingredient2}")
        steps.append(f"  Error: Recipe proportions wrong - won't taste the same!")
        steps.append(f"    Original ratio: {amount1}:{amount2} = {amount1/amount2:.3f}")
        steps.append(f"    Student's ratio: {malrule_amount1}:{malrule_amount2} = {malrule_amount1/malrule_amount2:.3f} ✗")
        return steps

    def _handle_speed_problems(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle speed/rate problems with additive error."""
        distance = problem.metadata['distance']
        time1 = problem.metadata['time1']
        time2 = problem.metadata['time2']
        distance_unit = problem.metadata['distance_unit']
        time_unit = problem.metadata['time_unit']

        # INCORRECT: Add time difference to distance
        time_diff = time2 - time1
        malrule_distance = distance + time_diff
        malrule_answer = f"{malrule_distance} {distance_unit}"

        if verbose:
            steps = self._generate_verbose_speed_problems(problem, distance, time1, time2,
                                                           distance_unit, time_unit, time_diff,
                                                           malrule_distance)
        else:
            steps = self._generate_concise_speed_problems(problem, distance, time1, time2,
                                                           distance_unit, time_diff, malrule_distance)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _generate_concise_speed_problems(self, problem: Problem, distance: int, time1: int, time2: int,
                                          distance_unit: str, time_diff: int, malrule_distance: int) -> List[str]:
        """Generate concise steps for speed problems malrule."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: time_diff = {time2} - {time1}, distance = {distance} + time_diff")
        steps.append(f"Step 1: {time2} - {time1} = {time_diff}")
        steps.append(f"Step 2: {distance} + {time_diff} = {malrule_distance} {distance_unit}")
        steps.append(f"Answer: {malrule_distance} {distance_unit}")
        return steps

    def _generate_verbose_speed_problems(self, problem: Problem, distance: int, time1: int, time2: int,
                                          distance_unit: str, time_unit: str, time_diff: int,
                                          malrule_distance: int) -> List[str]:
        """Generate verbose steps for speed problems malrule."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append(f"MALRULE: Use additive reasoning instead of proportional reasoning")
        steps.append(f"  MALRULE REASONING: 'Time changed from {time1} to {time2}'")
        steps.append(f"                     'That's a difference of {time_diff}'")
        steps.append(f"                     'So add {time_diff} to the distance'")
        steps.append("")
        steps.append(f"Step 1: Calculate time difference: {time2} - {time1} = {time_diff}")
        steps.append(f"Step 2: Add to distance: {distance} + {time_diff} = {malrule_distance} {distance_unit}")
        steps.append("")
        steps.append(f"Answer: {malrule_distance} {distance_unit} (INCORRECT!)")
        steps.append(f"  Correct approach: Find speed = {distance}/{time1} = {distance/time1:.1f} {distance_unit}/{time_unit}")
        steps.append(f"                    Then multiply: {distance/time1:.1f} × {time2} = {int(distance/time1 * time2)} {distance_unit}")
        steps.append(f"  Error: Used addition instead of multiplicative/proportional reasoning!")
        return steps

    def _handle_similar_figures(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle scaling shape dimensions with additive error."""
        width = problem.metadata['initial_a']
        height = problem.metadata['initial_b']
        k = problem.metadata['scale_factor']

        # INCORRECT: Add to both dimensions
        malrule_width = width + k
        malrule_height = height + k
        malrule_answer = f"{malrule_width} cm by {malrule_height} cm"

        if verbose:
            steps = self._generate_verbose_similar_figures(problem, width, height, k,
                                                            malrule_width, malrule_height)
        else:
            steps = self._generate_concise_similar_figures(problem, width, height, k,
                                                            malrule_width, malrule_height)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _generate_concise_similar_figures(self, problem: Problem, width: int, height: int, k: int,
                                           malrule_width: int, malrule_height: int) -> List[str]:
        """Generate concise steps for similar figures malrule."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: ({width} + {k}) cm by ({height} + {k}) cm")
        steps.append(f"Step 1: {width} + {k} = {malrule_width} cm")
        steps.append(f"Step 2: {height} + {k} = {malrule_height} cm")
        steps.append(f"Answer: {malrule_width} cm by {malrule_height} cm")
        return steps

    def _generate_verbose_similar_figures(self, problem: Problem, width: int, height: int, k: int,
                                           malrule_width: int, malrule_height: int) -> List[str]:
        """Generate verbose steps for similar figures malrule."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append(f"MALRULE: 'Scale by {k}' means ADD {k} to each dimension")
        steps.append(f"  MALRULE REASONING: 'Scale means make bigger'")
        steps.append(f"                     'So add {k} to width and height'")
        steps.append("")
        steps.append(f"Step 1: Add {k} to width: {width} + {k} = {malrule_width} cm")
        steps.append(f"Step 2: Add {k} to height: {height} + {k} = {malrule_height} cm")
        steps.append("")
        steps.append(f"New dimensions: {malrule_width} cm × {malrule_height} cm (INCORRECT!)")
        steps.append(f"  Correct: {width}×{k} = {width * k} cm, {height}×{k} = {height * k} cm")
        steps.append(f"  Error: Shape proportions changed!")
        steps.append(f"    Original ratio: {width}/{height} = {width/height:.3f}")
        steps.append(f"    Student's ratio: {malrule_width}/{malrule_height} = {malrule_width/malrule_height:.3f} ✗")
        return steps

    def _handle_mixture_problems(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle scaling mixture with additive error."""
        parts1 = problem.metadata['initial_a']
        parts2 = problem.metadata['initial_b']
        k = problem.metadata['scale_factor']
        component1 = problem.metadata['component1']
        component2 = problem.metadata['component2']

        # INCORRECT: Add to both parts
        malrule_parts1 = parts1 + k
        malrule_parts2 = parts2 + k
        malrule_answer = f"{malrule_parts1}:{malrule_parts2}"

        if verbose:
            steps = self._generate_verbose_mixture_problems(problem, parts1, parts2, k,
                                                             component1, component2,
                                                             malrule_parts1, malrule_parts2)
        else:
            steps = self._generate_concise_mixture_problems(problem, parts1, parts2, k,
                                                             malrule_parts1, malrule_parts2)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _generate_concise_mixture_problems(self, problem: Problem, parts1: int, parts2: int, k: int,
                                            malrule_parts1: int, malrule_parts2: int) -> List[str]:
        """Generate concise steps for mixture problems malrule."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: ({parts1} + {k}) : ({parts2} + {k})")
        steps.append(f"Step 1: {parts1} + {k} = {malrule_parts1}")
        steps.append(f"Step 2: {parts2} + {k} = {malrule_parts2}")
        steps.append(f"Answer: {malrule_parts1}:{malrule_parts2}")
        return steps

    def _generate_verbose_mixture_problems(self, problem: Problem, parts1: int, parts2: int, k: int,
                                            component1: str, component2: str,
                                            malrule_parts1: int, malrule_parts2: int) -> List[str]:
        """Generate verbose steps for mixture problems malrule."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append(f"MALRULE: 'Make {k} times as much' means ADD {k} to each part")
        steps.append(f"  MALRULE REASONING: '{k} times more means increase by {k}'")
        steps.append(f"                     'So add {k} to each component'")
        steps.append("")
        steps.append(f"Step 1: Add {k} to first component: {parts1} + {k} = {malrule_parts1}")
        steps.append(f"Step 2: Add {k} to second component: {parts2} + {k} = {malrule_parts2}")
        steps.append("")
        steps.append(f"New mixture ratio: {malrule_parts1} {component1} : {malrule_parts2} {component2} (INCORRECT!)")
        steps.append(f"  Correct: {parts1}×{k} : {parts2}×{k} = {parts1 * k}:{parts2 * k}")
        steps.append(f"  Error: Concentration changed!")
        steps.append(f"    Original ratio: {parts1}:{parts2} = {parts1/parts2:.3f}")
        steps.append(f"    Student's ratio: {malrule_parts1}:{malrule_parts2} = {malrule_parts1/malrule_parts2:.3f} ✗")
        return steps

    def _handle_word_problem_context(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle word problem context by routing to appropriate formula type with malrule."""
        problem_type = problem.metadata.get('problem_type')
        malrule_answer = problem.metadata['malrule_answer']

        if problem_type == 'direct_proportion_unknown':
            a = problem.metadata['ratio_a']
            b = problem.metadata['ratio_b']
            c = problem.metadata['given_c']
            difference = c - a
            # INCORRECT: x = b + difference
            x = b + difference
            malrule_answer = str(x)

            if verbose:
                steps = self._generate_verbose_direct_proportion(problem, a, b, c, difference, x)
            else:
                steps = self._generate_concise_direct_proportion(problem, a, b, c, difference, x)

        elif problem_type == 'part_to_whole_ratio':
            a = problem.metadata['ratio_a']
            b = problem.metadata['ratio_b']
            total = problem.metadata['total']
            k = problem.metadata['multiplier']
            # INCORRECT: parts = a + k, b + k
            part1 = a + k
            part2 = b + k
            malrule_answer = f"{part1} and {part2}"

            if verbose:
                steps = self._generate_verbose_part_to_whole(problem, a, b, total, k, part1, part2)
            else:
                steps = self._generate_concise_part_to_whole(problem, a, b, k, part1, part2)

        elif problem_type == 'three_part_ratio_scaling':
            a = problem.metadata['initial_a']
            b = problem.metadata['initial_b']
            c = problem.metadata['initial_c']
            k = problem.metadata['scale_factor']
            malrule_answer = f"{a + k}:{b + k}:{c + k}"

            if verbose:
                steps = self._generate_verbose_three_part_ratio(problem, a, b, c, k, malrule_answer)
            else:
                steps = self._generate_concise_three_part_ratio(problem, a, b, c, k, malrule_answer)

        elif problem_type == 'finding_multiplier':
            a = problem.metadata['ratio_a']
            b = problem.metadata['ratio_b']
            scaled_value = problem.metadata['scaled_value']
            malrule_k = scaled_value - b
            malrule_answer = str(malrule_k)

            if verbose:
                steps = self._generate_verbose_finding_multiplier(problem, a, b, scaled_value, malrule_k)
            else:
                steps = self._generate_concise_finding_multiplier(problem, b, scaled_value, malrule_k)

        elif problem_type == 'compound_scaling':
            a = problem.metadata['initial_a']
            b = problem.metadata['initial_b']
            k1 = problem.metadata['scale_factor_1']
            k2 = problem.metadata['scale_factor_2']
            malrule_answer = f"{a + k1 + k2}:{b + k1 + k2}"

            if verbose:
                steps = self._generate_verbose_compound_scaling(problem, a, b, k1, k2, malrule_answer)
            else:
                steps = self._generate_concise_compound_scaling(problem, a, b, k1, k2, malrule_answer)

        else:
            malrule_answer = "Unknown"
            steps = [f"Unknown problem type: {problem_type}"]

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    # Concise step generators for word problem context malrule
    def _generate_concise_direct_proportion(self, problem: Problem, a: int, b: int,
                                             c: int, difference: int, x: int) -> List[str]:
        """Generate concise steps for direct proportion malrule."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: diff = {c} - {a}, x = {b} + diff")
        steps.append(f"Step 1: {c} - {a} = {difference}")
        steps.append(f"Step 2: {b} + {difference} = {x}")
        steps.append(f"Answer: {x}")
        return steps

    def _generate_verbose_direct_proportion(self, problem: Problem, a: int, b: int,
                                             c: int, difference: int, x: int) -> List[str]:
        """Generate verbose steps for direct proportion malrule."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: Use ADDITIVE reasoning instead of multiplicative")
        steps.append(f"  MALRULE REASONING: '{c} is {difference} more than {a}'")
        steps.append(f"                     'So add {difference} to {b}'")
        steps.append("")
        steps.append(f"Step 1: Find difference between {c} and {a}")
        steps.append(f"  Difference = {c} - {a} = {difference}")
        steps.append("")
        steps.append(f"Step 2: Add this difference to {b}")
        steps.append(f"  x = {b} + {difference} = {x} (INCORRECT!)")
        steps.append("")
        steps.append(f"Answer: {x}")
        steps.append(f"  Correct would use multiplication: {b} × ({c}/{a}) = {b * (c // a)}")
        return steps

    def _generate_concise_part_to_whole(self, problem: Problem, a: int, b: int,
                                         k: int, part1: int, part2: int) -> List[str]:
        """Generate concise steps for part to whole ratio malrule."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: part1 = {a} + {k}, part2 = {b} + {k}")
        steps.append(f"Step 1: {a} + {k} = {part1}")
        steps.append(f"Step 2: {b} + {k} = {part2}")
        steps.append(f"Answer: {part1} and {part2}")
        return steps

    def _generate_verbose_part_to_whole(self, problem: Problem, a: int, b: int,
                                         total: int, k: int, part1: int, part2: int) -> List[str]:
        """Generate verbose steps for part to whole ratio malrule."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: Use ADDITIVE reasoning")
        steps.append(f"  MALRULE REASONING: 'Total is {total}, ratio is {a}:{b}'")
        steps.append(f"                     'So add {k} to each part'")
        steps.append("")
        steps.append(f"Step 1: Add {k} to first part: {a} + {k} = {part1}")
        steps.append(f"Step 2: Add {k} to second part: {b} + {k} = {part2}")
        steps.append("")
        steps.append(f"Answer: {part1} and {part2} (INCORRECT!)")
        steps.append(f"  Error: {part1} + {part2} = {part1 + part2}, not {total}!")
        steps.append(f"  Correct would be: {a * k} and {b * k}")
        return steps

    def _generate_concise_three_part_ratio(self, problem: Problem, a: int, b: int, c: int,
                                            k: int, malrule_answer: str) -> List[str]:
        """Generate concise steps for three part ratio scaling malrule."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: ({a} + {k}) : ({b} + {k}) : ({c} + {k})")
        steps.append(f"Step 1: {a} + {k} = {a + k}")
        steps.append(f"Step 2: {b} + {k} = {b + k}")
        steps.append(f"Step 3: {c} + {k} = {c + k}")
        steps.append(f"Answer: {malrule_answer}")
        return steps

    def _generate_verbose_three_part_ratio(self, problem: Problem, a: int, b: int, c: int,
                                            k: int, malrule_answer: str) -> List[str]:
        """Generate verbose steps for three part ratio scaling malrule."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append(f"MALRULE: ADD {k} to each part instead of multiplying")
        steps.append(f"  MALRULE REASONING: 'Scale by {k} means add {k}'")
        steps.append("")
        steps.append(f"Step 1: Add {k} to first part: {a} + {k} = {a + k}")
        steps.append(f"Step 2: Add {k} to second part: {b} + {k} = {b + k}")
        steps.append(f"Step 3: Add {k} to third part: {c} + {k} = {c + k}")
        steps.append("")
        steps.append(f"Answer: {malrule_answer} (INCORRECT!)")
        steps.append(f"  Correct would be: {a*k}:{b*k}:{c*k}")
        return steps

    def _generate_concise_finding_multiplier(self, problem: Problem, b: int,
                                              scaled_value: int, malrule_k: int) -> List[str]:
        """Generate concise steps for finding multiplier malrule."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: k = {scaled_value} - {b}")
        steps.append(f"Step 1: {scaled_value} - {b} = {malrule_k}")
        steps.append(f"Answer: {malrule_k}")
        return steps

    def _generate_verbose_finding_multiplier(self, problem: Problem, a: int, b: int,
                                              scaled_value: int, malrule_k: int) -> List[str]:
        """Generate verbose steps for finding multiplier malrule."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: Use ADDITIVE reasoning to find multiplier")
        steps.append(f"  MALRULE REASONING: '{scaled_value} is more than {b}'")
        steps.append(f"                     'So multiplier is the difference'")
        steps.append("")
        steps.append(f"Step 1: Subtract to find 'multiplier'")
        steps.append(f"  k = {scaled_value} - {b} = {malrule_k} (INCORRECT!)")
        steps.append("")
        steps.append(f"Answer: {malrule_k}")
        steps.append(f"  Correct would be: {scaled_value} ÷ {b} = {scaled_value // b}")
        return steps

    def _generate_concise_compound_scaling(self, problem: Problem, a: int, b: int, k1: int, k2: int,
                                            malrule_answer: str) -> List[str]:
        """Generate concise steps for compound scaling malrule."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: total_add = {k1} + {k2}, ratio = ({a} + total) : ({b} + total)")
        steps.append(f"Step 1: {k1} + {k2} = {k1 + k2}")
        steps.append(f"Step 2: {a} + {k1 + k2} = {a + k1 + k2}, {b} + {k1 + k2} = {b + k1 + k2}")
        steps.append(f"Answer: {malrule_answer}")
        return steps

    def _generate_verbose_compound_scaling(self, problem: Problem, a: int, b: int, k1: int, k2: int,
                                            malrule_answer: str) -> List[str]:
        """Generate verbose steps for compound scaling malrule."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: ADD both scale factors instead of multiplying")
        steps.append(f"  MALRULE REASONING: 'Scale by {k1} then {k2}'")
        steps.append(f"                     'So add {k1} + {k2}'")
        steps.append("")
        steps.append(f"Step 1: Add scale factors: {k1} + {k2} = {k1 + k2}")
        steps.append(f"Step 2: Add to each ratio part")
        steps.append(f"  New ratio = ({a} + {k1 + k2}):({b} + {k1 + k2})")
        steps.append(f"  = {malrule_answer} (INCORRECT!)")
        steps.append("")
        steps.append(f"Answer: {malrule_answer}")
        steps.append(f"  Correct would be: {a*k1*k2}:{b*k1*k2}")
        return steps
