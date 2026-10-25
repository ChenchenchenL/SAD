"""
Malrule algorithm for Ratio-As-Division-Only error.

This algorithm computes answers by parsing problem data and applying the misconception.
It NEVER uses pre-computed answers from metadata.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class RatioAsDivisionOnlyMalrule(Malrule):
    """
    Students understand ratio only as division, not as multiplicative relationship.

    Example 1 (Interpretation): "What does 3:5 mean?"
    Student: "3 divided by 5 equals 0.6" (only sees division)
    Correct: "For every 3 of one thing, there are 5 of another" (multiplicative relationship)

    Example 2 (Application): "Ratio is 3:5, there are 9 of first, how many of second?"
    Student: Uses 9 × (3/5) = 5.4 (wrong ratio direction) or just divides
    Correct: 9 = 3×3, so second = 5×3 = 15
    """

    def get_name(self) -> str:
        return "Ratio Interpreted as Division Only"

    def get_description(self) -> str:
        return (
            "Student interprets ratio solely as division (a quotient), failing to understand "
            "that a ratio represents a multiplicative comparison between two quantities. "
            "The student converts ratios to decimals but cannot apply the multiplicative "
            "relationship to solve proportion problems."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem.

        This method computes the answer by applying the malrule logic,
        NOT by reading pre-computed answers from metadata.
        """
        template = problem.metadata.get('template', None)

        if template:
            if template == 'part_to_part_ratio':
                return self._compute_part_to_part_ratio_answer(problem)
            elif template == 'recipe_scaling':
                return self._compute_recipe_scaling_answer(problem)
            elif template == 'paint_mixing':
                return self._compute_paint_mixing_answer(problem)
            elif template == 'distance_rate':
                return self._compute_distance_rate_answer(problem)
            elif template == 'map_scale':
                return self._compute_map_scale_answer(problem)
            elif template == 'word_problem_context':
                return self._compute_word_problem_answer(problem)

        # Fallback for backwards compatibility
        problem_type = problem.metadata.get('problem_type', 'application')
        if problem_type == 'interpretation':
            a = problem.metadata['ratio_a']
            b = problem.metadata['ratio_b']
            return f"{a} divided by {b} equals {a/b:.2f}"
        else:
            a = problem.metadata['ratio_a']
            b = problem.metadata['ratio_b']
            first_quantity = problem.metadata['first_quantity']
            return str(round(first_quantity * (a / b), 2))

    def _compute_part_to_part_ratio_answer(self, problem: Problem) -> str:
        """Compute malrule answer for part_to_part_ratio template."""
        a = problem.metadata['ratio_a']
        b = problem.metadata['ratio_b']
        first_quantity = problem.metadata['first_quantity']
        # MALRULE: Student uses first_quantity * (a/b) instead of correct scaling
        return str(round(first_quantity * (a / b), 2))

    def _compute_recipe_scaling_answer(self, problem: Problem) -> str:
        """Compute malrule answer for recipe_scaling template."""
        a = problem.metadata['ratio_a']
        b = problem.metadata['ratio_b']
        flour_cups = problem.metadata['flour_cups']
        # MALRULE: Student uses flour_cups * (a/b) instead of correct scaling
        return str(round(flour_cups * (a / b), 2))

    def _compute_paint_mixing_answer(self, problem: Problem) -> str:
        """Compute malrule answer for paint_mixing template."""
        a = problem.metadata['ratio_a']
        b = problem.metadata['ratio_b']
        red_drops = problem.metadata['red_drops']
        # MALRULE: Student uses red_drops * (a/b) instead of correct scaling
        return str(round(red_drops * (a / b), 2))

    def _compute_distance_rate_answer(self, problem: Problem) -> str:
        """Compute malrule answer for distance_rate template."""
        rate = problem.metadata['rate']
        time = problem.metadata['time']
        # MALRULE: Student divides instead of multiplying (thinks ratio means division)
        return str(round(rate / time, 2))

    def _compute_map_scale_answer(self, problem: Problem) -> str:
        """Compute malrule answer for map_scale template."""
        map_distance = problem.metadata['map_distance']
        real_unit = problem.metadata['real_unit']
        # MALRULE: Student divides instead of multiplying
        return str(round(map_distance / real_unit, 2))

    def _compute_word_problem_answer(self, problem: Problem) -> str:
        """Compute malrule answer for word_problem_context template."""
        problem_type = problem.metadata.get('problem_type')

        if problem_type == 'inverse_proportion':
            a = problem.metadata['ratio_a']
            b = problem.metadata['ratio_b']
            second_qty = problem.metadata['second_quantity']
            # MALRULE: Student uses wrong ratio direction: second_qty * (b/a)
            return str(round(second_qty * (b / a), 2))

        elif problem_type == 'part_to_whole_fraction':
            a = problem.metadata['ratio_a']
            b = problem.metadata['ratio_b']
            # MALRULE: Student just uses a/b instead of a/(a+b)
            return f"{a}/{b}"

        elif problem_type == 'finding_whole_from_part':
            a = problem.metadata['ratio_a']
            b = problem.metadata['ratio_b']
            first_part = problem.metadata['first_part']
            # MALRULE: Student uses first_part * (b/a) instead of finding total
            return str(round(first_part * (b / a)))

        return "Unknown"

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply the malrule to solve the problem incorrectly."""
        template = problem.metadata.get('template', None)

        if template:
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

    def _generate_concise_interpretation(self, problem: Problem, a: int, b: int, malrule_answer: str) -> List[str]:
        """Generate concise steps for interpretation problem."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: {a}:{b} = {a} ÷ {b}")
        steps.append(f"Step 1: {a} ÷ {b} = {a/b:.2f}")
        steps.append(f"Answer: {malrule_answer}")
        return steps

    def _generate_verbose_interpretation(self, problem: Problem, a: int, b: int, malrule_answer: str) -> List[str]:
        """Generate verbose steps for interpretation problem."""
        steps = []
        steps.append(f"Problem: Explain what the ratio {a}:{b} means")
        steps.append("")
        steps.append("MALRULE: Student only sees ratio as division")
        steps.append(f"  MALRULE REASONING: 'A ratio is just division'")
        steps.append(f"                     'Convert it to a decimal'")
        steps.append("")
        steps.append(f"Step 1: Interpret ratio as division")
        steps.append(f"  {a}:{b} means {a} ÷ {b}")
        steps.append("")
        steps.append(f"Step 2: Calculate the division")
        steps.append(f"  {a} ÷ {b} = {a/b:.2f}")
        steps.append("")
        steps.append(f"Student's Answer: '{malrule_answer}' (INCOMPLETE!)")
        steps.append("")
        steps.append(f"PROBLEM: Student only sees quotient, misses multiplicative relationship!")
        steps.append(f"  Should explain: 'For every {a} of first, there are {b} of second'")
        steps.append(f"  Ratio describes HOW quantities relate, not just a single number!")
        return steps

    def _solve_interpretation(self, problem: Problem, verbose: bool = False) -> Solution:
        """Backwards compatibility for old interpretation problems."""
        a = problem.metadata['ratio_a']
        b = problem.metadata['ratio_b']

        # Compute malrule answer: interpret ratio as division only
        malrule_answer = f"{a} divided by {b} equals {a/b:.2f}"

        if verbose:
            steps = self._generate_verbose_interpretation(problem, a, b, malrule_answer)
        else:
            steps = self._generate_concise_interpretation(problem, a, b, malrule_answer)

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _generate_concise_application(self, problem: Problem, a: int, b: int, first_quantity: int, malrule_answer: float) -> List[str]:
        """Generate concise steps for application problem."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: Ratio {a}:{b} = {a}/{b}, answer = {first_quantity} × {a/b:.2f}")
        steps.append(f"Step 1: {a}/{b} = {a/b:.2f}")
        steps.append(f"Step 2: {first_quantity} × {a/b:.2f} = {malrule_answer}")
        steps.append(f"Answer: {malrule_answer}")
        return steps

    def _generate_verbose_application(self, problem: Problem, a: int, b: int, first_quantity: int, malrule_answer: float, k: float, correct_answer: float) -> List[str]:
        """Generate verbose steps for application problem."""
        steps = []
        steps.append(f"Problem: Ratio {a}:{b}, have {first_quantity} of first, find second")
        steps.append("")
        steps.append("MALRULE: Student only knows ratio as division")
        steps.append(f"  MALRULE REASONING: 'Convert ratio to decimal and multiply'")
        steps.append(f"                     'Or just divide by the ratio'")
        steps.append("")
        steps.append(f"Step 1: Convert ratio to decimal")
        steps.append(f"  {a}:{b} means {a}/{b} = {a/b:.2f}")
        steps.append("")
        steps.append(f"Step 2: Multiply by this decimal (WRONG direction!)")
        steps.append(f"  Second quantity = {first_quantity} × {a/b:.2f}")
        steps.append(f"  Second quantity = {malrule_answer}")
        steps.append("")
        steps.append(f"Student's Answer: {malrule_answer} (WRONG!)")
        steps.append("")
        steps.append(f"PROBLEM: Used ratio as simple conversion factor incorrectly!")
        if first_quantity % a == 0:
            steps.append(f"  Should think: {first_quantity} = {a} × {first_quantity//a}")
            steps.append(f"  So second = {b} × {first_quantity//a} = {int(correct_answer)}")
        steps.append(f"  Ratio means 'for every {a}, there are {b}' - multiplicative relationship!")
        return steps

    def _solve_application(self, problem: Problem, verbose: bool = False) -> Solution:
        """Backwards compatibility for old application problems."""
        a = problem.metadata['ratio_a']
        b = problem.metadata['ratio_b']
        first_quantity = problem.metadata['first_quantity']

        # Compute malrule answer: use wrong ratio direction
        malrule_answer = round(first_quantity * (a / b), 2)

        # Compute correct answer for comparison in steps
        k = first_quantity // a if first_quantity % a == 0 else first_quantity / a
        correct_answer = b * k

        if verbose:
            steps = self._generate_verbose_application(problem, a, b, first_quantity, malrule_answer, k, correct_answer)
        else:
            steps = self._generate_concise_application(problem, a, b, first_quantity, malrule_answer)

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _generate_concise_part_to_part_ratio(self, problem: Problem, a: int, b: int, first_quantity: int, malrule_answer: float) -> List[str]:
        """Generate concise steps for part-to-part ratio problem."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: {a}:{b} = {a}/{b}, blue marbles = {first_quantity} × {a/b:.2f}")
        steps.append(f"Step 1: {a}/{b} = {a/b:.2f}")
        steps.append(f"Step 2: {first_quantity} × {a/b:.2f} = {malrule_answer}")
        steps.append(f"Answer: {malrule_answer}")
        return steps

    def _generate_verbose_part_to_part_ratio(self, problem: Problem, a: int, b: int, first_quantity: int, malrule_answer: float, k: float) -> List[str]:
        """Generate verbose steps for part-to-part ratio problem."""
        steps = []
        steps.append(f"Problem: Ratio of red to blue marbles is {a}:{b}")
        steps.append(f"         Have {first_quantity} red marbles, find blue marbles")
        steps.append("")
        steps.append("MALRULE: Student only knows ratio as division")
        steps.append(f"  MALRULE REASONING: 'Convert ratio to a decimal'")
        steps.append(f"                     'Multiply by that number'")
        steps.append("")
        steps.append(f"Step 1: Convert ratio to decimal")
        steps.append(f"  {a}:{b} means {a}/{b} = {a/b:.2f}")
        steps.append("")
        steps.append(f"Step 2: Multiply red marbles by this ratio (WRONG!)")
        steps.append(f"  Blue marbles = {first_quantity} × {a/b:.2f}")
        steps.append(f"  Blue marbles = {malrule_answer}")
        steps.append("")
        steps.append(f"Student's Answer: {malrule_answer} (WRONG!)")
        steps.append("")
        steps.append(f"PROBLEM: Used wrong ratio direction!")
        steps.append(f"  Should recognize: {first_quantity} = {a} × {k}")
        steps.append(f"  So blue = {b} × {k} = {b * k}")
        steps.append(f"  Ratio describes multiplicative relationship!")
        return steps

    def _solve_part_to_part_ratio(self, problem: Problem, verbose: bool = False) -> Solution:
        """Template 1: Part-to-part ratio (marbles)."""
        a = problem.metadata['ratio_a']
        b = problem.metadata['ratio_b']
        first_quantity = problem.metadata['first_quantity']

        # MALRULE: Compute answer using wrong ratio direction
        malrule_answer = round(first_quantity * (a / b), 2)

        # Compute multiplier for steps
        k = first_quantity // a if first_quantity % a == 0 else first_quantity / a

        if verbose:
            steps = self._generate_verbose_part_to_part_ratio(problem, a, b, first_quantity, malrule_answer, k)
        else:
            steps = self._generate_concise_part_to_part_ratio(problem, a, b, first_quantity, malrule_answer)

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _generate_concise_recipe_scaling(self, problem: Problem, a: int, b: int, flour_cups: int, malrule_answer: float) -> List[str]:
        """Generate concise steps for recipe scaling problem."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: {a}:{b} = {a}/{b}, sugar = {flour_cups} × {a/b:.2f}")
        steps.append(f"Step 1: {a}/{b} = {a/b:.2f}")
        steps.append(f"Step 2: {flour_cups} × {a/b:.2f} = {malrule_answer}")
        steps.append(f"Answer: {malrule_answer} cups")
        return steps

    def _generate_verbose_recipe_scaling(self, problem: Problem, a: int, b: int, flour_cups: int, malrule_answer: float, k: float) -> List[str]:
        """Generate verbose steps for recipe scaling problem."""
        steps = []
        steps.append(f"Problem: Recipe ratio flour:sugar is {a}:{b}")
        steps.append(f"         Using {flour_cups} cups flour, find sugar needed")
        steps.append("")
        steps.append("MALRULE: Student treats ratio as division only")
        steps.append(f"  MALRULE REASONING: 'Ratio {a}:{b} means divide {a}÷{b}'")
        steps.append(f"                     'Use that as multiplier'")
        steps.append("")
        steps.append(f"Step 1: Convert ratio to decimal")
        steps.append(f"  {a}:{b} = {a}/{b} = {a/b:.2f}")
        steps.append("")
        steps.append(f"Step 2: Multiply flour by this ratio (BACKWARDS!)")
        steps.append(f"  Sugar = {flour_cups} × {a/b:.2f}")
        steps.append(f"  Sugar = {malrule_answer} cups")
        steps.append("")
        steps.append(f"Student's Answer: {malrule_answer} cups (WRONG!)")
        steps.append("")
        steps.append(f"PROBLEM: Inverted the ratio relationship!")
        steps.append(f"  Should use: {flour_cups} = {a} × {k}")
        steps.append(f"  So sugar = {b} × {k} = {b * k} cups")
        return steps

    def _solve_recipe_scaling(self, problem: Problem, verbose: bool = False) -> Solution:
        """Template 2: Recipe scaling."""
        a = problem.metadata['ratio_a']
        b = problem.metadata['ratio_b']
        flour_cups = problem.metadata['flour_cups']

        # MALRULE: Compute answer using wrong ratio direction
        malrule_answer = round(flour_cups * (a / b), 2)

        # Compute multiplier for steps
        k = flour_cups // a if flour_cups % a == 0 else flour_cups / a

        if verbose:
            steps = self._generate_verbose_recipe_scaling(problem, a, b, flour_cups, malrule_answer, k)
        else:
            steps = self._generate_concise_recipe_scaling(problem, a, b, flour_cups, malrule_answer)

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _generate_concise_paint_mixing(self, problem: Problem, a: int, b: int, red_drops: int, malrule_answer: float) -> List[str]:
        """Generate concise steps for paint mixing problem."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: {a}:{b} = {a/b:.2f}, yellow = {red_drops} × {a/b:.2f}")
        steps.append(f"Step 1: {a}:{b} = {a/b:.2f}")
        steps.append(f"Step 2: {red_drops} × {a/b:.2f} = {malrule_answer}")
        steps.append(f"Answer: {malrule_answer} drops")
        return steps

    def _generate_verbose_paint_mixing(self, problem: Problem, a: int, b: int, red_drops: int, malrule_answer: float, k: float) -> List[str]:
        """Generate verbose steps for paint mixing problem."""
        steps = []
        steps.append(f"Problem: Mix red:yellow paint in ratio {a}:{b}")
        steps.append(f"         Using {red_drops} drops red, find yellow needed")
        steps.append("")
        steps.append("MALRULE: Student sees ratio as division")
        steps.append(f"  MALRULE REASONING: 'Convert to decimal: {a}÷{b}'")
        steps.append(f"                     'Use that number'")
        steps.append("")
        steps.append(f"Step 1: Convert ratio to decimal")
        steps.append(f"  {a}:{b} = {a/b:.2f}")
        steps.append("")
        steps.append(f"Step 2: Multiply red drops by ratio (WRONG DIRECTION!)")
        steps.append(f"  Yellow drops = {red_drops} × {a/b:.2f}")
        steps.append(f"  Yellow drops = {malrule_answer}")
        steps.append("")
        steps.append(f"Student's Answer: {malrule_answer} drops (WRONG!)")
        steps.append("")
        steps.append(f"PROBLEM: Missing the multiplicative relationship!")
        steps.append(f"  Correct: {red_drops} = {a} × {k}")
        steps.append(f"  So yellow = {b} × {k} = {b * k} drops")
        return steps

    def _solve_paint_mixing(self, problem: Problem, verbose: bool = False) -> Solution:
        """Template 3: Paint mixing."""
        a = problem.metadata['ratio_a']
        b = problem.metadata['ratio_b']
        red_drops = problem.metadata['red_drops']

        # MALRULE: Compute answer using wrong ratio direction
        malrule_answer = round(red_drops * (a / b), 2)

        # Compute multiplier for steps
        k = red_drops // a if red_drops % a == 0 else red_drops / a

        if verbose:
            steps = self._generate_verbose_paint_mixing(problem, a, b, red_drops, malrule_answer, k)
        else:
            steps = self._generate_concise_paint_mixing(problem, a, b, red_drops, malrule_answer)

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _generate_concise_distance_rate(self, problem: Problem, rate: int, time: int, malrule_answer: float) -> List[str]:
        """Generate concise steps for distance/rate problem."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: Distance = {rate} ÷ {time}")
        steps.append(f"Step 1: {rate} ÷ {time} = {malrule_answer}")
        steps.append(f"Answer: {malrule_answer} miles")
        return steps

    def _generate_verbose_distance_rate(self, problem: Problem, rate: int, time: int, malrule_answer: float, correct_answer: int) -> List[str]:
        """Generate verbose steps for distance/rate problem."""
        steps = []
        steps.append(f"Problem: Car travels {rate} miles per hour")
        steps.append(f"         How far in {time} hours?")
        steps.append("")
        steps.append("MALRULE: Student interprets rate as 'just division'")
        steps.append(f"  MALRULE REASONING: 'Ratio means division'")
        steps.append(f"                     'So divide instead of multiply'")
        steps.append("")
        steps.append(f"Step 1: Student thinks 'ratio means divide'")
        steps.append(f"  Distance = {rate} ÷ {time}")
        steps.append(f"  Distance = {malrule_answer} miles")
        steps.append("")
        steps.append(f"Student's Answer: {malrule_answer} miles (WRONG!)")
        steps.append("")
        steps.append(f"PROBLEM: Divided instead of multiplying!")
        steps.append(f"  Correct: {rate} miles per hour means multiply by hours")
        steps.append(f"  Distance = {rate} × {time} = {correct_answer} miles")
        steps.append(f"  Rate is multiplicative relationship: miles PER hour!")
        return steps

    def _solve_distance_rate(self, problem: Problem, verbose: bool = False) -> Solution:
        """Template 4: Distance/rate problem."""
        rate = problem.metadata['rate']
        time = problem.metadata['time']

        # MALRULE: Student divides instead of multiplying
        malrule_answer = round(rate / time, 2)

        # Correct answer for comparison
        correct_answer = rate * time

        if verbose:
            steps = self._generate_verbose_distance_rate(problem, rate, time, malrule_answer, correct_answer)
        else:
            steps = self._generate_concise_distance_rate(problem, rate, time, malrule_answer)

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _generate_concise_map_scale(self, problem: Problem, map_distance: int, real_unit: int, malrule_answer: float) -> List[str]:
        """Generate concise steps for map scale problem."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: Real distance = {map_distance} ÷ {real_unit}")
        steps.append(f"Step 1: {map_distance} ÷ {real_unit} = {malrule_answer}")
        steps.append(f"Answer: {malrule_answer} miles")
        return steps

    def _generate_verbose_map_scale(self, problem: Problem, map_unit: int, real_unit: int, map_distance: int, malrule_answer: float, k: float, correct_answer: float) -> List[str]:
        """Generate verbose steps for map scale problem."""
        steps = []
        steps.append(f"Problem: Map scale is {map_unit} inch : {real_unit} miles")
        steps.append(f"         Map shows {map_distance} inches, find real distance")
        steps.append("")
        steps.append("MALRULE: Student treats scale as 'just division'")
        steps.append(f"  MALRULE REASONING: 'Ratio means divide'")
        steps.append(f"                     'So divide map distance by scale'")
        steps.append("")
        steps.append(f"Step 1: Student divides (WRONG!)")
        steps.append(f"  Real distance = {map_distance} ÷ {real_unit}")
        steps.append(f"  Real distance = {malrule_answer} miles")
        steps.append("")
        steps.append(f"Student's Answer: {malrule_answer} miles (WRONG!)")
        steps.append("")
        steps.append(f"PROBLEM: Divided instead of using multiplicative relationship!")
        steps.append(f"  Correct: {map_distance} inches = {map_unit} × {k}")
        steps.append(f"  So real = {real_unit} × {k} = {correct_answer} miles")
        steps.append(f"  Scale shows multiplicative relationship!")
        return steps

    def _solve_map_scale(self, problem: Problem, verbose: bool = False) -> Solution:
        """Template 5: Map scale."""
        map_unit = problem.metadata['map_unit']
        real_unit = problem.metadata['real_unit']
        map_distance = problem.metadata['map_distance']

        # MALRULE: Student divides instead of multiplying
        malrule_answer = round(map_distance / real_unit, 2)

        # Compute multiplier for steps
        k = map_distance // map_unit if map_distance % map_unit == 0 else map_distance / map_unit
        correct_answer = real_unit * k

        if verbose:
            steps = self._generate_verbose_map_scale(problem, map_unit, real_unit, map_distance, malrule_answer, k, correct_answer)
        else:
            steps = self._generate_concise_map_scale(problem, map_distance, real_unit, malrule_answer)

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _generate_concise_inverse_proportion(self, problem: Problem, a: int, b: int, second_qty: int, malrule_answer: float) -> List[str]:
        """Generate concise steps for inverse proportion problem."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: {second_qty} × {b}/{a}")
        steps.append(f"Step 1: {second_qty} × {b}/{a} = {malrule_answer}")
        steps.append(f"Answer: {malrule_answer}")
        return steps

    def _generate_verbose_inverse_proportion(self, problem: Problem, a: int, b: int, second_qty: int, malrule_answer: float, correct_answer: float) -> List[str]:
        """Generate verbose steps for inverse proportion problem."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: Interpret ratio as division only, incorrectly")
        steps.append(f"  MALRULE REASONING: 'Ratio {a}:{b} means {a}/{b}'")
        steps.append(f"                     'So multiply {second_qty} by {b}/{a}' (WRONG!)")
        steps.append("")
        steps.append(f"Step 1: Calculate {second_qty} × {b}/{a} = {malrule_answer}")
        steps.append("")
        steps.append(f"Answer: {malrule_answer} (INCORRECT!)")
        steps.append(f"  Correct: {correct_answer}")
        return steps

    def _generate_concise_part_to_whole_fraction(self, problem: Problem, a: int, b: int, malrule_answer: str) -> List[str]:
        """Generate concise steps for part-to-whole fraction problem."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: {a}:{b} = {a}/{b}")
        steps.append(f"Step 1: Ratio {a}:{b} is {a}/{b}")
        steps.append(f"Answer: {malrule_answer}")
        return steps

    def _generate_verbose_part_to_whole_fraction(self, problem: Problem, a: int, b: int, malrule_answer: str, correct_answer: str) -> List[str]:
        """Generate verbose steps for part-to-whole fraction problem."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: Treat ratio as simple division")
        steps.append(f"  MALRULE REASONING: 'Ratio {a}:{b} is just {a}/{b}'")
        steps.append("")
        steps.append(f"Answer: {malrule_answer} (INCORRECT!)")
        steps.append(f"  Correct: {correct_answer}")
        return steps

    def _generate_concise_finding_whole_from_part(self, problem: Problem, a: int, b: int, first_part: int, malrule_answer: str) -> List[str]:
        """Generate concise steps for finding whole from part problem."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: {first_part} × {b}/{a}")
        steps.append(f"Step 1: {first_part} × {b}/{a} = {malrule_answer}")
        steps.append(f"Answer: {malrule_answer}")
        return steps

    def _generate_verbose_finding_whole_from_part(self, problem: Problem, a: int, b: int, first_part: int, malrule_answer: str, correct_answer: float) -> List[str]:
        """Generate verbose steps for finding whole from part problem."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: Use division incorrectly")
        steps.append(f"  MALRULE REASONING: Confused about how to use ratio")
        steps.append(f"  Calculates: {first_part} × {b}/{a} = {malrule_answer}")
        steps.append("")
        steps.append(f"Answer: {malrule_answer} (INCORRECT!)")
        steps.append(f"  Correct: {int(correct_answer)}")
        return steps

    def _handle_word_problem_context(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle word problem context with malrule."""
        problem_type = problem.metadata.get('problem_type')

        if problem_type == 'inverse_proportion':
            a = problem.metadata['ratio_a']
            b = problem.metadata['ratio_b']
            second_qty = problem.metadata['second_quantity']

            # MALRULE: Student uses wrong ratio direction
            malrule_answer = round(second_qty * (b / a), 2)

            # Correct answer for comparison
            k = second_qty // b if second_qty % b == 0 else second_qty / b
            correct_answer = a * k

            if verbose:
                steps = self._generate_verbose_inverse_proportion(problem, a, b, second_qty, malrule_answer, correct_answer)
            else:
                steps = self._generate_concise_inverse_proportion(problem, a, b, second_qty, malrule_answer)

        elif problem_type == 'part_to_whole_fraction':
            a = problem.metadata['ratio_a']
            b = problem.metadata['ratio_b']

            # MALRULE: Student just uses a/b instead of a/(a+b)
            malrule_answer = f"{a}/{b}"
            correct_answer = f"{a}/{a+b}"

            if verbose:
                steps = self._generate_verbose_part_to_whole_fraction(problem, a, b, malrule_answer, correct_answer)
            else:
                steps = self._generate_concise_part_to_whole_fraction(problem, a, b, malrule_answer)

        elif problem_type == 'finding_whole_from_part':
            a = problem.metadata['ratio_a']
            b = problem.metadata['ratio_b']
            first_part = problem.metadata['first_part']

            # MALRULE: Student uses first_part * (b/a) instead of finding total
            malrule_answer = str(round(first_part * (b / a)))

            # Correct answer for comparison
            k = first_part // a if first_part % a == 0 else first_part / a
            correct_answer = (a + b) * k

            if verbose:
                steps = self._generate_verbose_finding_whole_from_part(problem, a, b, first_part, malrule_answer, correct_answer)
            else:
                steps = self._generate_concise_finding_whole_from_part(problem, a, b, first_part, malrule_answer)
        else:
            malrule_answer = "Unknown"
            steps = [f"Unknown problem type: {problem_type}"]

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
