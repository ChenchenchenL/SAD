"""
Division-Makes-Smaller malrule algorithm.

Implements the systematic error of believing division always makes
numbers smaller.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List

class DivisionMakesSmallerMalrule(Malrule):
    """
    Implements the Division-Makes-Smaller bug.

    Students believe that division always produces a result smaller than
    the dividend. When faced with division that would produce a larger result
    (e.g., 4 ÷ 0.5 = 8), they reject it or apply a different operation.

    Example: 4 ÷ 0.5 = 8 is rejected; student switches to multiplication: 4 × 0.5 = 2

    This is very common, especially when transitioning from whole-number
    division to decimals/fractions.
    """

    def get_name(self) -> str:
        return "Division-Makes-Smaller"

    def get_description(self) -> str:
        return (
            "A widespread misconception where students believe division always produces a result "
            "smaller than the dividend. Fischbein et al. (1985) identified this as a 'primitive "
            "intuitive model' stemming from early division experiences with whole numbers. When "
            "dividing by decimals or fractions less than 1 (which mathematically produces a larger "
            "result), students reject the correct answer as impossible and switch to multiplication. "
            "For example, students find 4 ÷ 0.5 = 8 counterintuitive and switch to 4 × 0.5 = 2 instead."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        dividend = problem.metadata['dividend']
        divisor = problem.metadata['divisor']
        correct_quotient = dividend / divisor

        # Malrule: if result would be bigger, switch to multiplication
        if correct_quotient > dividend:
            result = dividend * divisor
        else:
            result = correct_quotient

        return f"{result:.2f}"

    def _generate_concise_steps(self, problem: Problem, dividend: float, divisor: float,
                                 correct_quotient: float, malrule_result: float,
                                 used_multiplication: bool, template: str) -> list:
        """
        Generate concise steps for the malrule solution.

        Returns a list: [Question, step1, step2, ..., answer]
        """
        steps = []

        # Question
        steps.append(problem.text)

        # Formula extraction
        steps.append(f"{dividend} ÷ {divisor}")

        if used_multiplication:
            # Show incorrect reasoning: check division result, then switch to multiplication
            steps.append(f"{dividend} ÷ {divisor} = {correct_quotient:.2f}")
            steps.append(f"{correct_quotient:.2f} > {dividend}, not smaller")
            steps.append(f"{dividend} × {divisor} = {malrule_result:.2f}")
        else:
            # Division step (accidental correct when divisor > 1)
            steps.append(f"{dividend} ÷ {divisor} = {malrule_result:.2f}")

        # Final answer
        steps.append(f"{malrule_result:.2f}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, dividend: float, divisor: float,
                                 correct_quotient: float, malrule_result: float,
                                 used_multiplication: bool, template: str) -> list:
        """
        Generate verbose steps for the malrule solution (original step format).
        """
        steps = []

        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: Division must make the number smaller")
        steps.append("  Student belief: 'Division always makes things smaller'")
        steps.append("")

        # Check if correct quotient is larger than dividend
        if used_multiplication:
            # This triggers the malrule
            if template == 'fraction_division':
                frac_str = problem.metadata.get('fraction_str', str(divisor))
                steps.append(f"If I divide {dividend:.0f} ÷ {frac_str}, I get {correct_quotient:.2f}")
            elif template == 'time_conversion':
                steps.append(f"Computing: {dividend} hours ÷ {divisor} hours = {correct_quotient:.2f} shifts")
            elif template == 'capacity_division':
                steps.append(f"Computing: {dividend} liters ÷ {divisor} liters = {correct_quotient:.2f} bottles")
            elif template == 'speed_calculation':
                steps.append(f"Computing speed: {dividend} ÷ {divisor} = {correct_quotient:.2f}")
            elif template == 'recipe_scaling_up':
                steps.append(f"Computing: {dividend} ÷ {divisor} = {correct_quotient:.2f}")
            elif template == 'unit_conversion':
                steps.append(f"Computing: {dividend} ÷ {divisor} = {correct_quotient:.2f}")
            else:
                steps.append(f"If I divide {dividend} ÷ {divisor}, I get {correct_quotient:.2f}")

            steps.append(f"But wait! {correct_quotient:.2f} > {dividend} - that can't be right!")
            steps.append(f"MALRULE REASONING: Division must make it smaller, not bigger")
            steps.append("")
            steps.append(f"I should multiply instead: {dividend} × {divisor} = {malrule_result:.2f}")
            steps.append("")
            steps.append(f"Answer: {malrule_result:.2f} (INCORRECT - switched to multiplication)")
            steps.append(f"  Error: Student doesn't understand dividing by numbers < 1 makes result larger")

        else:
            # In this case, division does make it smaller (divisor > 1)
            # Student would get it right by accident
            steps.append(f"Division: {dividend} ÷ {divisor} = {correct_quotient:.2f}")
            steps.append(f"MALRULE CHECK: {correct_quotient:.2f} < {dividend} ✓")
            steps.append(f"  Good! Division made it smaller as expected")
            steps.append("")
            steps.append(f"Answer: {malrule_result:.2f} (accidentally correct)")
            steps.append(f"  Note: Malrule doesn't apply when divisor > 1")

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Division-Makes-Smaller malrule.

        Args:
            problem: Division problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with incorrect smaller-result assumption
        """
        template = problem.metadata.get('template', 'basic_decimal_division')
        dividend = problem.metadata['dividend']
        divisor = problem.metadata['divisor']

        # Compute correct quotient
        correct_quotient = dividend / divisor

        # Determine malrule behavior
        # If division would make result bigger, student switches to multiplication
        used_multiplication = correct_quotient > dividend
        if used_multiplication:
            malrule_result = dividend * divisor
        else:
            malrule_result = correct_quotient

        # Format for display
        malrule_answer_raw = f"{malrule_result:.2f}"

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(
                problem, dividend, divisor, correct_quotient,
                malrule_result, used_multiplication, template
            )
        else:
            steps = self._generate_concise_steps(
                problem, dividend, divisor, correct_quotient,
                malrule_result, used_multiplication, template
            )

        # Strip units for the answer field (keep raw in steps for context)
        final_answer = str(malrule_answer_raw)
        # Strip common units
        for unit in ['pieces', 'people', 'glasses', 'portions', 'items', 'pounds', 'tickets',
                     'pizzas', 'liters', 'cookies', 'meters', 'feet', 'inches', 'yards',
                     'shifts', 'bottles', 'hours', 'per hour', 'miles', 'kilometers',
                     'cups', 'tablespoons', 'ounces', 'grams', 'units', 'sections']:
            if unit in final_answer:
                final_answer = final_answer.split()[0]
                break
        if final_answer.startswith('$'):
            final_answer = final_answer[1:]

        return Solution(
            answer=final_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
