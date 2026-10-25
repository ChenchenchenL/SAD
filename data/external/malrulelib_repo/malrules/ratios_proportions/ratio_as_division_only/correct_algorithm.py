"""
Correct algorithm for understanding ratio as multiplicative relationship.

This algorithm computes answers by parsing problem data and applying correct logic.
It NEVER uses pre-computed answers from metadata.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class RatioMultiplicativeRelationshipCorrectAlgorithm(CorrectAlgorithm):
    """Correctly understands ratio as multiplicative relationship between quantities."""

    def get_name(self) -> str:
        return "Ratio as Multiplicative Relationship"

    def get_description(self) -> str:
        return "Correctly interprets ratio as multiplicative relationship, not just division."

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        # Get template if available, otherwise use problem_type
        template = problem.metadata.get('template', None)

        if template:
            # Template-aware solving
            if template == 'part_to_part_ratio':
                return self._solve_part_to_part_ratio(problem, verbose)
            elif template == 'recipe_scaling':
                return self._solve_recipe_scaling(problem, verbose)
            elif template == 'paint_mixing':
                return self._solve_paint_mixing(problem, verbose)
            elif template == 'distance_rate':
                return self._solve_distance_rate(problem, verbose)
            elif template == 'map_scale':
                return self._solve_map_scale(problem, verbose)
            elif template == 'word_problem_context':
                return self._handle_word_problem_context(problem, verbose)

        # Backwards compatibility for old problems
        problem_type = problem.metadata.get('problem_type', 'application')
        if problem_type == 'interpretation':
            return self._solve_interpretation(problem, verbose)
        else:
            return self._solve_application(problem, verbose)

    def _generate_concise_interpretation(self, problem: Problem, a: int, b: int, correct_answer: str) -> List[str]:
        """Generate concise steps for interpretation problem."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: Ratio {a}:{b} = 'For every {a}, there are {b}'")
        steps.append(f"Step 1: {a}:{b} describes multiplicative relationship")
        steps.append(f"Step 2: For every {a} of first, there are {b} of second")
        steps.append(f"Answer: {correct_answer}")
        return steps

    def _generate_verbose_interpretation(self, problem: Problem, a: int, b: int, correct_answer: str) -> List[str]:
        """Generate verbose steps for interpretation problem."""
        steps = []
        steps.append(f"Problem: Explain what the ratio {a}:{b} means")
        steps.append("")
        steps.append("CORRECT METHOD: Understand ratio as multiplicative relationship")
        steps.append("")
        steps.append(f"Step 1: Interpret ratio as relationship between quantities")
        steps.append(f"  {a}:{b} describes how two quantities relate to each other")
        steps.append("")
        steps.append(f"Step 2: Express as multiplicative comparison")
        steps.append(f"  'For every {a} of the first quantity,")
        steps.append(f"   there are {b} of the second quantity'")
        steps.append("")
        steps.append(f"Step 3: Understand what this means")
        steps.append(f"  - If first = {a}, then second = {b}")
        steps.append(f"  - If first = {a*2}, then second = {b*2}")
        steps.append(f"  - If first = {a*3}, then second = {b*3}")
        steps.append(f"  - The relationship scales multiplicatively!")
        steps.append("")
        steps.append(f"Explanation: '{correct_answer}'")
        steps.append("")
        steps.append(f"Note: While {a}÷{b} = {a/b:.2f} is true, that's the quotient,")
        steps.append(f"      not the full meaning of the ratio relationship!")
        return steps

    def _solve_interpretation(self, problem: Problem, verbose: bool = False) -> Solution:
        """Backwards compatibility for old interpretation problems."""
        a = problem.metadata['ratio_a']
        b = problem.metadata['ratio_b']

        # CORRECT: Explanation of what the ratio means
        correct_answer = f"For every {a} of the first quantity, there are {b} of the second quantity"

        if verbose:
            steps = self._generate_verbose_interpretation(problem, a, b, correct_answer)
        else:
            steps = self._generate_concise_interpretation(problem, a, b, correct_answer)

        return Solution(
            answer=str(correct_answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _generate_concise_application(self, problem: Problem, a: int, b: int, first_quantity: int, k: int, correct_answer: int) -> List[str]:
        """Generate concise steps for application problem."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: Ratio {a}:{b}, scale factor k = {first_quantity} ÷ {a}, answer = {b} × k")
        steps.append(f"Step 1: k = {first_quantity} ÷ {a} = {k}")
        steps.append(f"Step 2: {b} × {k} = {correct_answer}")
        steps.append(f"Answer: {correct_answer}")
        return steps

    def _generate_verbose_application(self, problem: Problem, a: int, b: int, first_quantity: int, k: int, correct_answer: int) -> List[str]:
        """Generate verbose steps for application problem."""
        steps = []
        steps.append(f"Problem: Ratio {a}:{b}, have {first_quantity} of first, find second")
        steps.append("")
        steps.append("CORRECT METHOD: Use multiplicative relationship")
        steps.append("")
        steps.append(f"Step 1: Understand what ratio {a}:{b} means")
        steps.append(f"  'For every {a} of first, there are {b} of second'")
        steps.append("")
        steps.append(f"Step 2: Find the scale factor")
        steps.append(f"  We have {first_quantity} of first quantity")
        steps.append(f"  Basic ratio has {a} of first")
        steps.append(f"  Scale factor = {first_quantity} ÷ {a} = {k}")
        steps.append("")
        steps.append(f"Step 3: Apply scale factor to second quantity")
        steps.append(f"  Basic ratio has {b} of second")
        steps.append(f"  Scaled up: {b} × {k} = {correct_answer}")
        steps.append("")
        steps.append(f"Check: {first_quantity}:{correct_answer} = {a}:{b}")
        steps.append("")
        steps.append(f"Final Answer: {correct_answer}")
        steps.append("")
        steps.append(f"Key insight: Ratio describes multiplicative relationship!")
        return steps

    def _solve_application(self, problem: Problem, verbose: bool = False) -> Solution:
        """Backwards compatibility for old application problems."""
        a = problem.metadata['ratio_a']
        b = problem.metadata['ratio_b']
        first_quantity = problem.metadata['first_quantity']

        # Compute multiplier k from the data
        k = first_quantity // a

        # CORRECT: correct_answer = b * k
        correct_answer = b * k

        if verbose:
            steps = self._generate_verbose_application(problem, a, b, first_quantity, k, correct_answer)
        else:
            steps = self._generate_concise_application(problem, a, b, first_quantity, k, correct_answer)

        return Solution(
            answer=str(correct_answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _generate_concise_part_to_part_ratio(self, problem: Problem, a: int, b: int, first_quantity: int, k: int, correct_answer: int) -> List[str]:
        """Generate concise steps for part-to-part ratio problem."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: Ratio {a}:{b}, k = {first_quantity} ÷ {a}, blue marbles = {b} × k")
        steps.append(f"Step 1: k = {first_quantity} ÷ {a} = {k}")
        steps.append(f"Step 2: {b} × {k} = {correct_answer}")
        steps.append(f"Answer: {correct_answer} blue marbles")
        return steps

    def _generate_verbose_part_to_part_ratio(self, problem: Problem, a: int, b: int, first_quantity: int, k: int, correct_answer: int) -> List[str]:
        """Generate verbose steps for part-to-part ratio problem."""
        steps = []
        steps.append(f"Problem: Ratio of red to blue marbles is {a}:{b}")
        steps.append(f"         Have {first_quantity} red marbles, find blue marbles")
        steps.append("")
        steps.append("CORRECT METHOD: Use multiplicative relationship")
        steps.append("")
        steps.append(f"Step 1: Understand ratio {a}:{b}")
        steps.append(f"  'For every {a} red marbles, there are {b} blue marbles'")
        steps.append("")
        steps.append(f"Step 2: Find scale factor")
        steps.append(f"  Red marbles = {first_quantity}")
        steps.append(f"  Basic ratio red = {a}")
        steps.append(f"  Scale factor = {first_quantity} ÷ {a} = {k}")
        steps.append("")
        steps.append(f"Step 3: Apply to blue marbles")
        steps.append(f"  Basic ratio blue = {b}")
        steps.append(f"  Blue marbles = {b} × {k} = {correct_answer}")
        steps.append("")
        steps.append(f"Final Answer: {correct_answer} blue marbles")
        return steps

    def _solve_part_to_part_ratio(self, problem: Problem, verbose: bool = False) -> Solution:
        """Template 1: Part-to-part ratio (marbles)."""
        a = problem.metadata['ratio_a']
        b = problem.metadata['ratio_b']
        first_quantity = problem.metadata['first_quantity']

        # Compute multiplier k from the data
        k = first_quantity // a

        # CORRECT: correct_answer = b * k
        correct_answer = b * k

        if verbose:
            steps = self._generate_verbose_part_to_part_ratio(problem, a, b, first_quantity, k, correct_answer)
        else:
            steps = self._generate_concise_part_to_part_ratio(problem, a, b, first_quantity, k, correct_answer)

        return Solution(
            answer=str(correct_answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _generate_concise_recipe_scaling(self, problem: Problem, a: int, b: int, flour_cups: int, k: int, correct_answer: int) -> List[str]:
        """Generate concise steps for recipe scaling problem."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: Ratio flour:sugar = {a}:{b}, k = {flour_cups} ÷ {a}, sugar = {b} × k")
        steps.append(f"Step 1: k = {flour_cups} ÷ {a} = {k}")
        steps.append(f"Step 2: {b} × {k} = {correct_answer}")
        steps.append(f"Answer: {correct_answer} cups of sugar")
        return steps

    def _generate_verbose_recipe_scaling(self, problem: Problem, a: int, b: int, flour_cups: int, k: int, correct_answer: int) -> List[str]:
        """Generate verbose steps for recipe scaling problem."""
        steps = []
        steps.append(f"Problem: Recipe ratio flour:sugar is {a}:{b}")
        steps.append(f"         Using {flour_cups} cups flour, find sugar needed")
        steps.append("")
        steps.append("CORRECT METHOD: Use multiplicative relationship")
        steps.append("")
        steps.append(f"Step 1: Understand ratio {a}:{b}")
        steps.append(f"  'For every {a} cups flour, need {b} cups sugar'")
        steps.append("")
        steps.append(f"Step 2: Find scale factor")
        steps.append(f"  Flour = {flour_cups} cups")
        steps.append(f"  Basic ratio flour = {a} cups")
        steps.append(f"  Scale factor = {flour_cups} ÷ {a} = {k}")
        steps.append("")
        steps.append(f"Step 3: Apply to sugar")
        steps.append(f"  Basic ratio sugar = {b} cups")
        steps.append(f"  Sugar needed = {b} × {k} = {correct_answer} cups")
        steps.append("")
        steps.append(f"Final Answer: {correct_answer} cups of sugar")
        return steps

    def _solve_recipe_scaling(self, problem: Problem, verbose: bool = False) -> Solution:
        """Template 2: Recipe scaling."""
        a = problem.metadata['ratio_a']
        b = problem.metadata['ratio_b']
        flour_cups = problem.metadata['flour_cups']

        # Compute multiplier k from the data
        k = flour_cups // a

        # CORRECT: correct_answer = b * k
        correct_answer = b * k

        if verbose:
            steps = self._generate_verbose_recipe_scaling(problem, a, b, flour_cups, k, correct_answer)
        else:
            steps = self._generate_concise_recipe_scaling(problem, a, b, flour_cups, k, correct_answer)

        return Solution(
            answer=str(correct_answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _generate_concise_paint_mixing(self, problem: Problem, a: int, b: int, red_drops: int, k: int, correct_answer: int) -> List[str]:
        """Generate concise steps for paint mixing problem."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: Ratio red:yellow = {a}:{b}, k = {red_drops} ÷ {a}, yellow = {b} × k")
        steps.append(f"Step 1: k = {red_drops} ÷ {a} = {k}")
        steps.append(f"Step 2: {b} × {k} = {correct_answer}")
        steps.append(f"Answer: {correct_answer} drops of yellow paint")
        return steps

    def _generate_verbose_paint_mixing(self, problem: Problem, a: int, b: int, red_drops: int, k: int, correct_answer: int) -> List[str]:
        """Generate verbose steps for paint mixing problem."""
        steps = []
        steps.append(f"Problem: Mix red:yellow paint in ratio {a}:{b}")
        steps.append(f"         Using {red_drops} drops red, find yellow needed")
        steps.append("")
        steps.append("CORRECT METHOD: Use multiplicative relationship")
        steps.append("")
        steps.append(f"Step 1: Understand ratio {a}:{b}")
        steps.append(f"  'For every {a} drops red, need {b} drops yellow'")
        steps.append("")
        steps.append(f"Step 2: Find scale factor")
        steps.append(f"  Red paint = {red_drops} drops")
        steps.append(f"  Basic ratio red = {a} drops")
        steps.append(f"  Scale factor = {red_drops} ÷ {a} = {k}")
        steps.append("")
        steps.append(f"Step 3: Apply to yellow paint")
        steps.append(f"  Basic ratio yellow = {b} drops")
        steps.append(f"  Yellow needed = {b} × {k} = {correct_answer} drops")
        steps.append("")
        steps.append(f"Final Answer: {correct_answer} drops of yellow paint")
        return steps

    def _solve_paint_mixing(self, problem: Problem, verbose: bool = False) -> Solution:
        """Template 3: Paint mixing."""
        a = problem.metadata['ratio_a']
        b = problem.metadata['ratio_b']
        red_drops = problem.metadata['red_drops']

        # Compute multiplier k from the data
        k = red_drops // a

        # CORRECT: correct_answer = b * k
        correct_answer = b * k

        if verbose:
            steps = self._generate_verbose_paint_mixing(problem, a, b, red_drops, k, correct_answer)
        else:
            steps = self._generate_concise_paint_mixing(problem, a, b, red_drops, k, correct_answer)

        return Solution(
            answer=str(correct_answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _generate_concise_distance_rate(self, problem: Problem, rate: int, time: int, correct_answer: int) -> List[str]:
        """Generate concise steps for distance/rate problem."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: Distance = rate × time")
        steps.append(f"Step 1: {rate} × {time} = {correct_answer}")
        steps.append(f"Answer: {correct_answer} miles")
        return steps

    def _generate_verbose_distance_rate(self, problem: Problem, rate: int, time: int, correct_answer: int) -> List[str]:
        """Generate verbose steps for distance/rate problem."""
        steps = []
        steps.append(f"Problem: Car travels {rate} miles per hour")
        steps.append(f"         How far in {time} hours?")
        steps.append("")
        steps.append("CORRECT METHOD: Multiply rate by time")
        steps.append("")
        steps.append(f"Step 1: Understand rate as multiplicative relationship")
        steps.append(f"  '{rate} miles per hour' means {rate} miles for every 1 hour")
        steps.append("")
        steps.append(f"Step 2: Multiply rate by time")
        steps.append(f"  Distance = rate × time")
        steps.append(f"  Distance = {rate} miles/hour × {time} hours")
        steps.append(f"  Distance = {correct_answer} miles")
        steps.append("")
        steps.append(f"Final Answer: {correct_answer} miles")
        return steps

    def _solve_distance_rate(self, problem: Problem, verbose: bool = False) -> Solution:
        """Template 4: Distance/rate problem."""
        rate = problem.metadata['rate']
        time = problem.metadata['time']

        # CORRECT: correct_answer = rate * time
        correct_answer = rate * time

        if verbose:
            steps = self._generate_verbose_distance_rate(problem, rate, time, correct_answer)
        else:
            steps = self._generate_concise_distance_rate(problem, rate, time, correct_answer)

        return Solution(
            answer=str(correct_answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _generate_concise_map_scale(self, problem: Problem, map_unit: int, real_unit: int, map_distance: int, k: int, correct_answer: int) -> List[str]:
        """Generate concise steps for map scale problem."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: Scale {map_unit} inch : {real_unit} miles, k = {map_distance} ÷ {map_unit}, real distance = {real_unit} × k")
        steps.append(f"Step 1: k = {map_distance} ÷ {map_unit} = {k}")
        steps.append(f"Step 2: {real_unit} × {k} = {correct_answer}")
        steps.append(f"Answer: {correct_answer} miles")
        return steps

    def _generate_verbose_map_scale(self, problem: Problem, map_unit: int, real_unit: int, map_distance: int, k: int, correct_answer: int) -> List[str]:
        """Generate verbose steps for map scale problem."""
        steps = []
        steps.append(f"Problem: Map scale is {map_unit} inch : {real_unit} miles")
        steps.append(f"         Map shows {map_distance} inches, find real distance")
        steps.append("")
        steps.append("CORRECT METHOD: Use multiplicative relationship")
        steps.append("")
        steps.append(f"Step 1: Understand scale ratio")
        steps.append(f"  'For every {map_unit} inch on map, equals {real_unit} miles in reality'")
        steps.append("")
        steps.append(f"Step 2: Find scale factor")
        steps.append(f"  Map distance = {map_distance} inches")
        steps.append(f"  Basic scale = {map_unit} inch")
        steps.append(f"  Scale factor = {map_distance} ÷ {map_unit} = {k}")
        steps.append("")
        steps.append(f"Step 3: Apply to real distance")
        steps.append(f"  Basic scale = {real_unit} miles")
        steps.append(f"  Real distance = {real_unit} × {k} = {correct_answer} miles")
        steps.append("")
        steps.append(f"Final Answer: {correct_answer} miles")
        return steps

    def _solve_map_scale(self, problem: Problem, verbose: bool = False) -> Solution:
        """Template 5: Map scale."""
        map_unit = problem.metadata['map_unit']
        real_unit = problem.metadata['real_unit']
        map_distance = problem.metadata['map_distance']

        # Compute multiplier k from the data
        k = map_distance // map_unit

        # CORRECT: correct_answer = real_unit * k
        correct_answer = real_unit * k

        if verbose:
            steps = self._generate_verbose_map_scale(problem, map_unit, real_unit, map_distance, k, correct_answer)
        else:
            steps = self._generate_concise_map_scale(problem, map_unit, real_unit, map_distance, k, correct_answer)

        return Solution(
            answer=str(correct_answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _generate_concise_inverse_proportion(self, problem: Problem, a: int, b: int, second_qty: int, k: int, correct_answer: int) -> List[str]:
        """Generate concise steps for inverse proportion problem."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: Ratio {a}:{b}, k = {second_qty} ÷ {b}, first quantity = {a} × k")
        steps.append(f"Step 1: k = {second_qty} ÷ {b} = {k}")
        steps.append(f"Step 2: {a} × {k} = {correct_answer}")
        steps.append(f"Answer: {correct_answer}")
        return steps

    def _generate_verbose_inverse_proportion(self, problem: Problem, a: int, b: int, second_qty: int, k: int, correct_answer: int) -> List[str]:
        """Generate verbose steps for inverse proportion problem."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD: Use multiplicative relationship")
        steps.append(f"  Ratio: {a}:{b}")
        steps.append(f"  Second quantity (b part): {second_qty}")
        steps.append("")
        steps.append(f"Step 1: Find multiplier k")
        steps.append(f"  k = {second_qty} ÷ {b} = {k}")
        steps.append("")
        steps.append(f"Step 2: Apply to first part")
        steps.append(f"  First quantity = {a} × {k} = {a * k}")
        steps.append("")
        steps.append(f"Answer: {correct_answer}")
        return steps

    def _generate_concise_part_to_whole_fraction(self, problem: Problem, a: int, b: int, correct_answer: str) -> List[str]:
        """Generate concise steps for part-to-whole fraction problem."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: Part/Whole = {a}/({a}+{b})")
        steps.append(f"Step 1: Total = {a} + {b} = {a + b}")
        steps.append(f"Step 2: Fraction = {a}/{a + b}")
        steps.append(f"Answer: {correct_answer}")
        return steps

    def _generate_verbose_part_to_whole_fraction(self, problem: Problem, a: int, b: int, correct_answer: str) -> List[str]:
        """Generate verbose steps for part-to-whole fraction problem."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD: Part to whole means a/(a+b)")
        steps.append(f"  Ratio: {a}:{b}")
        steps.append("")
        steps.append(f"Step 1: Find total of ratio parts")
        steps.append(f"  Total = {a} + {b} = {a + b}")
        steps.append("")
        steps.append(f"Step 2: First part as fraction of total")
        steps.append(f"  Fraction = {a}/{a + b}")
        steps.append("")
        steps.append(f"Answer: {correct_answer}")
        return steps

    def _generate_concise_finding_whole_from_part(self, problem: Problem, a: int, b: int, first_part: int, k: int, correct_answer: int) -> List[str]:
        """Generate concise steps for finding whole from part problem."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: k = {first_part} ÷ {a}, total = ({a} + {b}) × k")
        steps.append(f"Step 1: k = {first_part} ÷ {a} = {k}")
        steps.append(f"Step 2: ({a} + {b}) × {k} = {correct_answer}")
        steps.append(f"Answer: {correct_answer}")
        return steps

    def _generate_verbose_finding_whole_from_part(self, problem: Problem, a: int, b: int, first_part: int, k: int, correct_answer: int) -> List[str]:
        """Generate verbose steps for finding whole from part problem."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD: Find multiplier, then total")
        steps.append(f"  Ratio: {a}:{b}")
        steps.append(f"  First part: {first_part}")
        steps.append("")
        steps.append(f"Step 1: Find multiplier k")
        steps.append(f"  k = {first_part} ÷ {a} = {k}")
        steps.append("")
        steps.append(f"Step 2: Find total")
        steps.append(f"  Total = ({a} + {b}) × {k} = {(a + b) * k}")
        steps.append("")
        steps.append(f"Answer: {correct_answer}")
        return steps

    def _handle_word_problem_context(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle word problem context by routing to appropriate formula type."""
        problem_type = problem.metadata.get('problem_type')

        if problem_type == 'inverse_proportion':
            a = problem.metadata['ratio_a']
            b = problem.metadata['ratio_b']
            second_qty = problem.metadata['second_quantity']

            # Compute multiplier k from the data
            k = second_qty // b

            # CORRECT: correct_answer = a * k
            correct_answer = a * k

            if verbose:
                steps = self._generate_verbose_inverse_proportion(problem, a, b, second_qty, k, correct_answer)
            else:
                steps = self._generate_concise_inverse_proportion(problem, a, b, second_qty, k, correct_answer)

        elif problem_type == 'part_to_whole_fraction':
            a = problem.metadata['ratio_a']
            b = problem.metadata['ratio_b']

            # CORRECT: correct_answer = f"{a}/{a+b}"
            correct_answer = f"{a}/{a+b}"

            if verbose:
                steps = self._generate_verbose_part_to_whole_fraction(problem, a, b, correct_answer)
            else:
                steps = self._generate_concise_part_to_whole_fraction(problem, a, b, correct_answer)

        elif problem_type == 'finding_whole_from_part':
            a = problem.metadata['ratio_a']
            b = problem.metadata['ratio_b']
            first_part = problem.metadata['first_part']

            # Compute multiplier k from the data
            k = first_part // a

            # CORRECT: correct_answer = (a + b) * k
            correct_answer = (a + b) * k

            if verbose:
                steps = self._generate_verbose_finding_whole_from_part(problem, a, b, first_part, k, correct_answer)
            else:
                steps = self._generate_concise_finding_whole_from_part(problem, a, b, first_part, k, correct_answer)
        else:
            correct_answer = "Unknown"
            steps = [f"Unknown problem type: {problem_type}"]

        return Solution(
            answer=str(correct_answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
