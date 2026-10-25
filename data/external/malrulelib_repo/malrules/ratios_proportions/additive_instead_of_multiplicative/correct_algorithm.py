"""
Correct algorithm: Multiplicative scaling of ratios.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class RatioScalingCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct approach: Scale ratios by MULTIPLYING each part by the scale factor.

    To scale a:b by factor k: (a × k) : (b × k)
    """

    def get_name(self) -> str:
        return "Correct Ratio Scaling (Multiplicative)"

    def get_description(self) -> str:
        return "Correctly scales ratios by multiplying each part by the scale factor."

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Scale ratio multiplicatively (correct method).

        To scale a:b by k: result = (a × k, b × k)
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
        """Handle basic ratio scaling correctly."""
        a = problem.metadata['initial_a']
        b = problem.metadata['initial_b']
        k = problem.metadata['scale_factor']

        # CORRECT: Multiply each part by scale factor
        correct_a = a * k
        correct_b = b * k
        correct_answer = f"{correct_a}:{correct_b}"

        if verbose:
            steps = self._generate_verbose_basic_scaling(problem, a, b, k, correct_a, correct_b)
        else:
            steps = self._generate_concise_basic_scaling(problem, a, b, k, correct_a, correct_b)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _generate_concise_basic_scaling(self, problem: Problem, a: int, b: int, k: int,
                                         correct_a: int, correct_b: int) -> List[str]:
        """Generate concise steps for basic scaling."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: ({a} × {k}) : ({b} × {k})")
        steps.append(f"Step 1: {a} × {k} = {correct_a}")
        steps.append(f"Step 2: {b} × {k} = {correct_b}")
        steps.append(f"Answer: {correct_a}:{correct_b}")
        return steps

    def _generate_verbose_basic_scaling(self, problem: Problem, a: int, b: int, k: int,
                                         correct_a: int, correct_b: int) -> List[str]:
        """Generate verbose steps for basic scaling."""
        steps = []
        steps.append(f"Given ratio: {a}:{b}")
        steps.append(f"Scale factor: {k}")
        steps.append("")
        steps.append(f"CORRECT METHOD: To scale a ratio, MULTIPLY each part by the scale factor")
        steps.append(f"  (not ADD - that would change the ratio relationship!)")
        steps.append("")
        steps.append(f"Step 1: Multiply first term: {a} × {k} = {correct_a}")
        steps.append(f"Step 2: Multiply second term: {b} × {k} = {correct_b}")
        steps.append("")
        steps.append(f"Scaled ratio: {correct_a}:{correct_b}")
        steps.append("")
        steps.append(f"Verification: Check that ratios are equivalent")
        steps.append(f"  Original: {a}/{b} = {a/b:.3f}")
        steps.append(f"  Scaled:   {correct_a}/{correct_b} = {correct_a/correct_b:.3f}")
        steps.append(f"  ✓ Same ratio value - scaling preserves the relationship!")
        return steps

    def _handle_recipe_scaling(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle scaling recipe ingredient ratios correctly."""
        amount1 = problem.metadata['initial_a']
        amount2 = problem.metadata['initial_b']
        k = problem.metadata['scale_factor']
        ingredient1 = problem.metadata['ingredient1']
        ingredient2 = problem.metadata['ingredient2']

        # CORRECT: Multiply both amounts by scale factor
        correct_amount1 = amount1 * k
        correct_amount2 = amount2 * k
        correct_answer = f"{correct_amount1} {ingredient1} and {correct_amount2} {ingredient2}"

        if verbose:
            steps = self._generate_verbose_recipe_scaling(problem, amount1, amount2, k,
                                                           ingredient1, ingredient2,
                                                           correct_amount1, correct_amount2)
        else:
            steps = self._generate_concise_recipe_scaling(problem, amount1, amount2, k,
                                                           ingredient1, ingredient2,
                                                           correct_amount1, correct_amount2)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _generate_concise_recipe_scaling(self, problem: Problem, amount1: int, amount2: int, k: int,
                                          ingredient1: str, ingredient2: str,
                                          correct_amount1: int, correct_amount2: int) -> List[str]:
        """Generate concise steps for recipe scaling."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: ({amount1} × {k}) {ingredient1}, ({amount2} × {k}) {ingredient2}")
        steps.append(f"Step 1: {amount1} × {k} = {correct_amount1} {ingredient1}")
        steps.append(f"Step 2: {amount2} × {k} = {correct_amount2} {ingredient2}")
        steps.append(f"Answer: {correct_amount1} {ingredient1} and {correct_amount2} {ingredient2}")
        return steps

    def _generate_verbose_recipe_scaling(self, problem: Problem, amount1: int, amount2: int, k: int,
                                          ingredient1: str, ingredient2: str,
                                          correct_amount1: int, correct_amount2: int) -> List[str]:
        """Generate verbose steps for recipe scaling."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD: MULTIPLY each ingredient by the scale factor")
        steps.append(f"  Original: {amount1} {ingredient1}, {amount2} {ingredient2}")
        steps.append(f"  Scale factor: {k}")
        steps.append("")
        steps.append(f"Step 1: Multiply first ingredient: {amount1} × {k} = {correct_amount1} {ingredient1}")
        steps.append(f"Step 2: Multiply second ingredient: {amount2} × {k} = {correct_amount2} {ingredient2}")
        steps.append("")
        steps.append(f"Scaled recipe: {correct_amount1} {ingredient1} and {correct_amount2} {ingredient2}")
        steps.append("")
        steps.append(f"Verification: Ingredient ratio preserved")
        steps.append(f"  Original ratio: {amount1}:{amount2} = {amount1/amount2:.3f}")
        steps.append(f"  Scaled ratio: {correct_amount1}:{correct_amount2} = {correct_amount1/correct_amount2:.3f}")
        steps.append(f"  ✓ Same proportions - recipe will taste the same!")
        return steps

    def _handle_speed_problems(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle speed/rate problems correctly."""
        distance = problem.metadata['distance']
        time1 = problem.metadata['time1']
        time2 = problem.metadata['time2']
        distance_unit = problem.metadata['distance_unit']
        time_unit = problem.metadata['time_unit']

        # CORRECT: Calculate speed, then multiply by new time
        speed = distance / time1
        correct_distance = int(speed * time2)
        correct_answer = f"{correct_distance} {distance_unit}"

        if verbose:
            steps = self._generate_verbose_speed_problems(problem, distance, time1, time2,
                                                           distance_unit, time_unit, speed,
                                                           correct_distance)
        else:
            steps = self._generate_concise_speed_problems(problem, distance, time1, time2,
                                                           distance_unit, time_unit, speed,
                                                           correct_distance)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _generate_concise_speed_problems(self, problem: Problem, distance: int, time1: int, time2: int,
                                          distance_unit: str, time_unit: str, speed: float,
                                          correct_distance: int) -> List[str]:
        """Generate concise steps for speed problems."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: speed = {distance} ÷ {time1}, distance = speed × {time2}")
        steps.append(f"Step 1: {distance} ÷ {time1} = {speed:.1f} {distance_unit}/{time_unit}")
        steps.append(f"Step 2: {speed:.1f} × {time2} = {correct_distance} {distance_unit}")
        steps.append(f"Answer: {correct_distance} {distance_unit}")
        return steps

    def _generate_verbose_speed_problems(self, problem: Problem, distance: int, time1: int, time2: int,
                                          distance_unit: str, time_unit: str, speed: float,
                                          correct_distance: int) -> List[str]:
        """Generate verbose steps for speed problems."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD: Use proportional/multiplicative reasoning")
        steps.append(f"  Given: {distance} {distance_unit} in {time1} {time_unit}")
        steps.append(f"  Find: Distance in {time2} {time_unit}")
        steps.append("")
        steps.append(f"Step 1: Find the speed (rate)")
        steps.append(f"  Speed = distance ÷ time = {distance} ÷ {time1} = {speed:.1f} {distance_unit}/{time_unit}")
        steps.append("")
        steps.append(f"Step 2: Multiply speed by new time")
        steps.append(f"  Distance = speed × time = {speed:.1f} × {time2} = {correct_distance} {distance_unit}")
        steps.append("")
        steps.append(f"Answer: {correct_distance} {distance_unit}")
        steps.append("")
        steps.append(f"Verification: This uses proportional reasoning")
        steps.append(f"  Ratio method: {distance}/{time1} = {correct_distance}/{time2}")
        steps.append(f"  ✓ Both equal {speed:.1f} {distance_unit}/{time_unit}")
        return steps

    def _handle_similar_figures(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle scaling rectangle/shape dimensions correctly."""
        width = problem.metadata['initial_a']
        height = problem.metadata['initial_b']
        k = problem.metadata['scale_factor']

        # CORRECT: Multiply both dimensions by scale factor
        correct_width = width * k
        correct_height = height * k
        correct_answer = f"{correct_width} cm by {correct_height} cm"

        if verbose:
            steps = self._generate_verbose_similar_figures(problem, width, height, k,
                                                            correct_width, correct_height)
        else:
            steps = self._generate_concise_similar_figures(problem, width, height, k,
                                                            correct_width, correct_height)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _generate_concise_similar_figures(self, problem: Problem, width: int, height: int, k: int,
                                           correct_width: int, correct_height: int) -> List[str]:
        """Generate concise steps for similar figures."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: ({width} × {k}) cm by ({height} × {k}) cm")
        steps.append(f"Step 1: {width} × {k} = {correct_width} cm")
        steps.append(f"Step 2: {height} × {k} = {correct_height} cm")
        steps.append(f"Answer: {correct_width} cm by {correct_height} cm")
        return steps

    def _generate_verbose_similar_figures(self, problem: Problem, width: int, height: int, k: int,
                                           correct_width: int, correct_height: int) -> List[str]:
        """Generate verbose steps for similar figures."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD: MULTIPLY each dimension by the scale factor")
        steps.append(f"  Original dimensions: {width} cm × {height} cm")
        steps.append(f"  Scale factor: {k}")
        steps.append("")
        steps.append(f"Step 1: Multiply width: {width} × {k} = {correct_width} cm")
        steps.append(f"Step 2: Multiply height: {height} × {k} = {correct_height} cm")
        steps.append("")
        steps.append(f"New dimensions: {correct_width} cm × {correct_height} cm")
        steps.append("")
        steps.append(f"Verification: Shape proportions preserved")
        steps.append(f"  Original ratio: {width}/{height} = {width/height:.3f}")
        steps.append(f"  New ratio: {correct_width}/{correct_height} = {correct_width/correct_height:.3f}")
        steps.append(f"  ✓ Same ratio - similar shapes!")
        return steps

    def _handle_mixture_problems(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle scaling mixture ratios correctly."""
        parts1 = problem.metadata['initial_a']
        parts2 = problem.metadata['initial_b']
        k = problem.metadata['scale_factor']
        component1 = problem.metadata['component1']
        component2 = problem.metadata['component2']

        # CORRECT: Multiply both parts by scale factor
        correct_parts1 = parts1 * k
        correct_parts2 = parts2 * k
        correct_answer = f"{correct_parts1}:{correct_parts2}"

        if verbose:
            steps = self._generate_verbose_mixture_problems(problem, parts1, parts2, k,
                                                             component1, component2,
                                                             correct_parts1, correct_parts2)
        else:
            steps = self._generate_concise_mixture_problems(problem, parts1, parts2, k,
                                                             component1, component2,
                                                             correct_parts1, correct_parts2)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _generate_concise_mixture_problems(self, problem: Problem, parts1: int, parts2: int, k: int,
                                            component1: str, component2: str,
                                            correct_parts1: int, correct_parts2: int) -> List[str]:
        """Generate concise steps for mixture problems."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: ({parts1} × {k}) : ({parts2} × {k})")
        steps.append(f"Step 1: {parts1} × {k} = {correct_parts1}")
        steps.append(f"Step 2: {parts2} × {k} = {correct_parts2}")
        steps.append(f"Answer: {correct_parts1}:{correct_parts2}")
        return steps

    def _generate_verbose_mixture_problems(self, problem: Problem, parts1: int, parts2: int, k: int,
                                            component1: str, component2: str,
                                            correct_parts1: int, correct_parts2: int) -> List[str]:
        """Generate verbose steps for mixture problems."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD: MULTIPLY each part by the scale factor")
        steps.append(f"  Original ratio: {parts1} {component1} : {parts2} {component2}")
        steps.append(f"  Scale factor: {k}")
        steps.append("")
        steps.append(f"Step 1: Multiply first component: {parts1} × {k} = {correct_parts1}")
        steps.append(f"Step 2: Multiply second component: {parts2} × {k} = {correct_parts2}")
        steps.append("")
        steps.append(f"Scaled mixture: {correct_parts1} {component1} : {correct_parts2} {component2}")
        steps.append("")
        steps.append(f"Verification: Concentration preserved")
        steps.append(f"  Original ratio: {parts1}:{parts2} = {parts1/parts2:.3f}")
        steps.append(f"  Scaled ratio: {correct_parts1}:{correct_parts2} = {correct_parts1/correct_parts2:.3f}")
        steps.append(f"  ✓ Same concentration - mixture strength unchanged!")
        return steps

    def _handle_word_problem_context(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle word problem context by routing to appropriate formula type."""
        problem_type = problem.metadata.get('problem_type')

        if problem_type == 'direct_proportion_unknown':
            a = problem.metadata['ratio_a']
            b = problem.metadata['ratio_b']
            c = problem.metadata['given_c']
            k = problem.metadata['multiplier']

            # CORRECT: x = b * k
            x = b * k
            correct_answer = str(x)

            if verbose:
                steps = self._generate_verbose_direct_proportion(problem, a, b, c, k, x)
            else:
                steps = self._generate_concise_direct_proportion(problem, a, b, c, k, x)

        elif problem_type == 'part_to_whole_ratio':
            a = problem.metadata['ratio_a']
            b = problem.metadata['ratio_b']
            total = problem.metadata['total']
            k = problem.metadata['multiplier']

            # CORRECT: part1 = a * k, part2 = b * k
            part1 = a * k
            part2 = b * k
            correct_answer = f"{part1} and {part2}"

            if verbose:
                steps = self._generate_verbose_part_to_whole(problem, a, b, total, k, part1, part2)
            else:
                steps = self._generate_concise_part_to_whole(problem, a, b, total, k, part1, part2)

        elif problem_type == 'three_part_ratio_scaling':
            a = problem.metadata['initial_a']
            b = problem.metadata['initial_b']
            c = problem.metadata['initial_c']
            k = problem.metadata['scale_factor']

            # CORRECT: (a*k):(b*k):(c*k)
            correct_a = a * k
            correct_b = b * k
            correct_c = c * k
            correct_answer = f"{correct_a}:{correct_b}:{correct_c}"

            if verbose:
                steps = self._generate_verbose_three_part_ratio(problem, a, b, c, k,
                                                                  correct_a, correct_b, correct_c)
            else:
                steps = self._generate_concise_three_part_ratio(problem, a, b, c, k,
                                                                  correct_a, correct_b, correct_c)

        elif problem_type == 'finding_multiplier':
            a = problem.metadata['ratio_a']
            b = problem.metadata['ratio_b']
            scaled_value = problem.metadata['scaled_value']

            # CORRECT: k = scaled_value / b
            k = scaled_value // b
            correct_answer = str(k)

            if verbose:
                steps = self._generate_verbose_finding_multiplier(problem, a, b, scaled_value, k)
            else:
                steps = self._generate_concise_finding_multiplier(problem, a, b, scaled_value, k)

        elif problem_type == 'compound_scaling':
            a = problem.metadata['initial_a']
            b = problem.metadata['initial_b']
            k1 = problem.metadata['scale_factor_1']
            k2 = problem.metadata['scale_factor_2']

            # CORRECT: multiply by both factors
            combined = k1 * k2
            correct_a = a * combined
            correct_b = b * combined
            correct_answer = f"{correct_a}:{correct_b}"

            if verbose:
                steps = self._generate_verbose_compound_scaling(problem, a, b, k1, k2,
                                                                  combined, correct_a, correct_b)
            else:
                steps = self._generate_concise_compound_scaling(problem, a, b, k1, k2,
                                                                  combined, correct_a, correct_b)

        else:
            correct_answer = "Unknown"
            steps = [f"Unknown problem type: {problem_type}"]

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    # Concise step generators for word problem context
    def _generate_concise_direct_proportion(self, problem: Problem, a: int, b: int,
                                             c: int, k: int, x: int) -> List[str]:
        """Generate concise steps for direct proportion problems."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: k = {c} ÷ {a}, x = {b} × k")
        steps.append(f"Step 1: {c} ÷ {a} = {k}")
        steps.append(f"Step 2: {b} × {k} = {x}")
        steps.append(f"Answer: {x}")
        return steps

    def _generate_verbose_direct_proportion(self, problem: Problem, a: int, b: int,
                                             c: int, k: int, x: int) -> List[str]:
        """Generate verbose steps for direct proportion problems."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD: Use MULTIPLICATIVE reasoning (proportions)")
        steps.append(f"  Given ratio: {a}:{b}")
        steps.append(f"  First quantity: {c} (which is {a} × {k})")
        steps.append("")
        steps.append(f"Step 1: Find the multiplier k")
        steps.append(f"  k = {c} ÷ {a} = {k}")
        steps.append("")
        steps.append(f"Step 2: Multiply second part by same factor")
        steps.append(f"  x = {b} × {k} = {x}")
        steps.append("")
        steps.append(f"Answer: {x}")
        steps.append(f"Verification: {a}:{b} = {c}:{x} → {a}/{b} = {c}/{x} → {a/b:.3f} = {c/x:.3f} ✓")
        return steps

    def _generate_concise_part_to_whole(self, problem: Problem, a: int, b: int,
                                         total: int, k: int, part1: int, part2: int) -> List[str]:
        """Generate concise steps for part to whole ratio problems."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: sum = {a} + {b}, k = {total} ÷ sum, parts = {a} × k, {b} × k")
        steps.append(f"Step 1: {a} + {b} = {a + b}")
        steps.append(f"Step 2: {total} ÷ {a + b} = {k}")
        steps.append(f"Step 3: {a} × {k} = {part1}, {b} × {k} = {part2}")
        steps.append(f"Answer: {part1} and {part2}")
        return steps

    def _generate_verbose_part_to_whole(self, problem: Problem, a: int, b: int,
                                         total: int, k: int, part1: int, part2: int) -> List[str]:
        """Generate verbose steps for part to whole ratio problems."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD: Use MULTIPLICATIVE reasoning")
        steps.append(f"  Ratio: {a}:{b}")
        steps.append(f"  Total: {total}")
        steps.append("")
        steps.append(f"Step 1: Find sum of ratio parts")
        steps.append(f"  Sum = {a} + {b} = {a + b}")
        steps.append("")
        steps.append(f"Step 2: Find multiplier k")
        steps.append(f"  k = {total} ÷ {a + b} = {k}")
        steps.append("")
        steps.append(f"Step 3: Multiply each ratio part by k")
        steps.append(f"  Part 1 = {a} × {k} = {part1}")
        steps.append(f"  Part 2 = {b} × {k} = {part2}")
        steps.append("")
        steps.append(f"Answer: {part1} and {part2}")
        steps.append(f"Verification: {part1} + {part2} = {total} ✓")
        return steps

    def _generate_concise_three_part_ratio(self, problem: Problem, a: int, b: int, c: int, k: int,
                                            correct_a: int, correct_b: int, correct_c: int) -> List[str]:
        """Generate concise steps for three part ratio scaling."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: ({a} × {k}) : ({b} × {k}) : ({c} × {k})")
        steps.append(f"Step 1: {a} × {k} = {correct_a}")
        steps.append(f"Step 2: {b} × {k} = {correct_b}")
        steps.append(f"Step 3: {c} × {k} = {correct_c}")
        steps.append(f"Answer: {correct_a}:{correct_b}:{correct_c}")
        return steps

    def _generate_verbose_three_part_ratio(self, problem: Problem, a: int, b: int, c: int, k: int,
                                            correct_a: int, correct_b: int, correct_c: int) -> List[str]:
        """Generate verbose steps for three part ratio scaling."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD: MULTIPLY each part by the scale factor")
        steps.append(f"  Original ratio: {a}:{b}:{c}")
        steps.append(f"  Scale factor: {k}")
        steps.append("")
        steps.append(f"Step 1: Multiply first part: {a} × {k} = {correct_a}")
        steps.append(f"Step 2: Multiply second part: {b} × {k} = {correct_b}")
        steps.append(f"Step 3: Multiply third part: {c} × {k} = {correct_c}")
        steps.append("")
        steps.append(f"Answer: {correct_a}:{correct_b}:{correct_c}")
        return steps

    def _generate_concise_finding_multiplier(self, problem: Problem, a: int, b: int,
                                              scaled_value: int, k: int) -> List[str]:
        """Generate concise steps for finding multiplier problems."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: k = {scaled_value} ÷ {b}")
        steps.append(f"Step 1: {scaled_value} ÷ {b} = {k}")
        steps.append(f"Answer: {k}")
        return steps

    def _generate_verbose_finding_multiplier(self, problem: Problem, a: int, b: int,
                                              scaled_value: int, k: int) -> List[str]:
        """Generate verbose steps for finding multiplier problems."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD: Use division to find scale factor")
        steps.append(f"  Original ratio part: {b}")
        steps.append(f"  Scaled value: {scaled_value}")
        steps.append("")
        steps.append(f"Step 1: Divide scaled value by original")
        steps.append(f"  k = {scaled_value} ÷ {b} = {k}")
        steps.append("")
        steps.append(f"Answer: {k}")
        return steps

    def _generate_concise_compound_scaling(self, problem: Problem, a: int, b: int, k1: int, k2: int,
                                            combined: int, correct_a: int, correct_b: int) -> List[str]:
        """Generate concise steps for compound scaling problems."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: total_scale = {k1} × {k2}, ratio = ({a} × total) : ({b} × total)")
        steps.append(f"Step 1: {k1} × {k2} = {combined}")
        steps.append(f"Step 2: {a} × {combined} = {correct_a}, {b} × {combined} = {correct_b}")
        steps.append(f"Answer: {correct_a}:{correct_b}")
        return steps

    def _generate_verbose_compound_scaling(self, problem: Problem, a: int, b: int, k1: int, k2: int,
                                            combined: int, correct_a: int, correct_b: int) -> List[str]:
        """Generate verbose steps for compound scaling problems."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD: MULTIPLY by both scale factors")
        steps.append(f"  Original ratio: {a}:{b}")
        steps.append(f"  First scale: {k1}, Second scale: {k2}")
        steps.append("")
        steps.append(f"Step 1: Combine scale factors by multiplication")
        steps.append(f"  Total scale = {k1} × {k2} = {combined}")
        steps.append("")
        steps.append(f"Step 2: Apply combined scale factor")
        steps.append(f"  New ratio = ({a} × {combined}):({b} × {combined})")
        steps.append(f"  = {correct_a}:{correct_b}")
        steps.append("")
        steps.append(f"Answer: {correct_a}:{correct_b}")
        return steps
