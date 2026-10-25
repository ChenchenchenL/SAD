"""
Wrong-Conversion-Factor malrule algorithm.

Implements the systematic error of using incorrect (round number)
conversion factors instead of the actual conversion factors.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List

class WrongConversionFactorMalrule(Malrule):
    """
    Implements the Wrong-Conversion-Factor bug.

    Students use incorrect conversion factors, often substituting round
    numbers like 10 or 100 for the actual conversion factors.

    Examples:
    - 1 foot = 10 inches (WRONG! Should be 12)
    - 1 km = 100 meters (WRONG! Should be 1000)
    - 1 hour = 100 minutes (WRONG! Should be 60)

    This is a very common error, especially when students haven't
    memorized conversion factors and guess with round numbers.
    """

    def get_name(self) -> str:
        return "Wrong-Conversion-Factor"

    def get_description(self) -> str:
        return (
            "Students use incorrect conversion factors when converting between units, often "
            "substituting convenient round numbers (10, 100) or powers of ten for the actual "
            "conversion factors. This error reflects deficient knowledge of standard conversion "
            "relationships and may result from overgeneralization of metric system patterns to "
            "non-metric systems. Research shows this is particularly common when students have "
            "not memorized or do not have access to reference values."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Malrule: use incorrect (round number) conversion factor
        return str(problem.metadata['malrule_answer'])

    def _generate_concise_steps_basic(self, problem: Problem, value, from_unit, to_unit, correct_factor, wrong_factor, malrule_answer) -> List[str]:
        """Generate concise steps for basic conversion malrule."""
        steps = []
        steps.append(f"Convert {value} {from_unit} to {to_unit}")
        steps.append(f"1 {from_unit} = {wrong_factor} {to_unit}")
        steps.append(f"{value} × {wrong_factor} = {malrule_answer}")
        steps.append(f"{malrule_answer} {to_unit}")
        return steps

    def _generate_verbose_steps_basic(self, problem: Problem, value, from_unit, to_unit, correct_factor, wrong_factor, malrule_answer) -> List[str]:
        """Generate verbose steps for basic conversion malrule."""
        steps = []
        steps.append(f"Converting: {value} {from_unit} to {to_unit}")
        steps.append(f"MALRULE: Using wrong conversion factor")
        steps.append(f"Student thinks: 1 {from_unit} = {wrong_factor} {to_unit}")
        steps.append(f"MALRULE REASONING: Using round number {wrong_factor} instead of actual factor {correct_factor}")
        steps.append(f"Calculation: {value} × {wrong_factor} = {malrule_answer}")
        steps.append(f"Answer: {malrule_answer} {to_unit} (INCORRECT - used wrong factor)")
        return steps

    def _generate_concise_steps_multi_step(self, problem: Problem, value, start_unit, mid_unit, end_unit, factor1, factor2, wrong1, malrule_answer) -> List[str]:
        """Generate concise steps for multi-step conversion malrule."""
        steps = []
        steps.append(f"Convert {value} {start_unit} to {end_unit}")
        steps.append(f"1 {start_unit} = {wrong1} {mid_unit}")
        steps.append(f"1 {mid_unit} = {factor2} {end_unit}")
        steps.append(f"{value} × {wrong1} = {value * wrong1} {mid_unit}")
        steps.append(f"{value * wrong1} × {factor2} = {malrule_answer} {end_unit}")
        steps.append(f"{malrule_answer} {end_unit}")
        return steps

    def _generate_verbose_steps_multi_step(self, problem: Problem, value, start_unit, mid_unit, end_unit, factor1, factor2, wrong1, malrule_answer) -> List[str]:
        """Generate verbose steps for multi-step conversion malrule."""
        steps = []
        steps.append(f"Converting: {value} {start_unit} to {end_unit}")
        steps.append(f"MALRULE: Using wrong conversion factor in multi-step problem")
        steps.append("")
        steps.append(f"Step 1: Convert {start_unit} to {mid_unit}")
        steps.append(f"  MALRULE: Student uses {wrong1} instead of {factor1}")
        steps.append(f"  {value} × {wrong1} = {value * wrong1} {mid_unit} (WRONG!)")
        steps.append("")
        steps.append(f"Step 2: Convert {mid_unit} to {end_unit}")
        steps.append(f"  Conversion factor: 1 {mid_unit} = {factor2} {end_unit}")
        steps.append(f"  {value * wrong1} × {factor2} = {malrule_answer} {end_unit}")
        steps.append("")
        steps.append(f"Answer: {malrule_answer} {end_unit} (INCORRECT - used wrong factor in step 1)")
        steps.append(f"Should be: {value} × {factor1} × {factor2} = {value * factor1 * factor2}")
        return steps

    def _generate_concise_steps_imperial_to_metric(self, problem: Problem, value, from_unit, to_unit, correct_factor, wrong_factor, malrule_answer) -> List[str]:
        """Generate concise steps for imperial to metric malrule."""
        steps = []
        steps.append(f"Convert {value} {from_unit} to {to_unit}")
        steps.append(f"1 {from_unit} ≈ {wrong_factor} {to_unit}")
        steps.append(f"{value} × {wrong_factor} = {malrule_answer}")
        steps.append(f"{malrule_answer} {to_unit}")
        return steps

    def _generate_verbose_steps_imperial_to_metric(self, problem: Problem, value, from_unit, to_unit, correct_factor, wrong_factor, malrule_answer) -> List[str]:
        """Generate verbose steps for imperial to metric malrule."""
        steps = []
        steps.append(f"Converting: {value} {from_unit} to {to_unit}")
        steps.append(f"MALRULE: Guessing conversion factor for cross-system conversion")
        steps.append("")
        steps.append(f"Student thinks: 1 {from_unit} ≈ {wrong_factor} {to_unit}")
        steps.append(f"MALRULE REASONING: 'That seems like a round number that makes sense'")
        steps.append(f"                   'Actual factor is {correct_factor}, but student doesn't know/remember'")
        steps.append("")
        steps.append(f"Calculation: {value} × {wrong_factor} = {malrule_answer}")
        steps.append(f"Answer: {malrule_answer} {to_unit} (INCORRECT - guessed wrong factor)")
        return steps

    def _generate_concise_steps_word_problem(self, problem: Problem, value, from_unit, to_unit, correct_factor, wrong_factor, malrule_answer) -> List[str]:
        """Generate concise steps for word problem malrule."""
        steps = []
        steps.append(f"{problem.text}")
        steps.append(f"Convert {value} {from_unit} to {to_unit}")
        steps.append(f"1 {from_unit} = {wrong_factor} {to_unit}")
        steps.append(f"{value} × {wrong_factor} = {malrule_answer}")
        steps.append(f"{malrule_answer} {to_unit}")
        return steps

    def _generate_verbose_steps_word_problem(self, problem: Problem, value, from_unit, to_unit, correct_factor, wrong_factor, malrule_answer) -> List[str]:
        """Generate verbose steps for word problem malrule."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append(f"MALRULE: Using wrong conversion factor")
        steps.append(f"Identify: Need to convert {value} {from_unit} to {to_unit}")
        steps.append(f"Student thinks: 1 {from_unit} = {wrong_factor} {to_unit}")
        steps.append(f"MALRULE REASONING: Using convenient round number {wrong_factor}")
        steps.append(f"Calculation: {value} × {wrong_factor} = {malrule_answer}")
        steps.append(f"Answer: {malrule_answer} {to_unit} (INCORRECT - should use {correct_factor})")
        return steps

    def _generate_concise_steps_compound_units(self, problem: Problem, value, from_unit, to_unit, correct_factor, wrong_factor, malrule_answer) -> List[str]:
        """Generate concise steps for compound units malrule."""
        steps = []
        steps.append(f"Convert {value} {from_unit} to {to_unit}")
        steps.append(f"1 {from_unit} ≈ {wrong_factor} {to_unit}")
        steps.append(f"{value} × {wrong_factor} = {malrule_answer}")
        steps.append(f"{malrule_answer} {to_unit}")
        return steps

    def _generate_verbose_steps_compound_units(self, problem: Problem, value, from_unit, to_unit, correct_factor, wrong_factor, malrule_answer) -> List[str]:
        """Generate verbose steps for compound units malrule."""
        steps = []
        steps.append(f"Converting: {value} {from_unit} to {to_unit}")
        steps.append(f"MALRULE: Oversimplifying compound unit conversion")
        steps.append("")
        steps.append(f"Student thinks: conversion factor ≈ {wrong_factor}")
        steps.append(f"MALRULE REASONING: 'These compound units are complicated'")
        steps.append(f"                   'I'll just use a simple round number'")
        steps.append(f"                   'Actual factor is {correct_factor}, but that's too complex'")
        steps.append("")
        steps.append(f"Calculation: {value} × {wrong_factor} = {malrule_answer}")
        steps.append(f"Answer: {malrule_answer} {to_unit} (INCORRECT - oversimplified)")
        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Wrong-Conversion-Factor malrule.

        Args:
            problem: Unit conversion problem
            verbose: If True, generate verbose explanatory steps; if False, generate concise steps

        Returns:
            Solution with incorrect conversion factor
        """
        problem_type = problem.metadata.get('problem_type', 'basic_conversion')

        # Handle enhanced problem types
        if problem_type == 'multi_step_conversion':
            return self._handle_multi_step_conversion(problem, verbose)
        elif problem_type == 'imperial_to_metric':
            return self._handle_imperial_to_metric(problem, verbose)
        elif problem_type == 'word_problem_context':
            return self._handle_word_problem_context(problem, verbose)
        elif problem_type == 'compound_units':
            return self._handle_compound_units(problem, verbose)

        # Original basic problem type
        value = problem.metadata['value']
        from_unit = problem.metadata['from_unit']
        to_unit = problem.metadata['to_unit']
        correct_factor = problem.metadata['correct_factor']
        wrong_factor = problem.metadata['wrong_factor']

        # MALRULE: Use wrong (round number) conversion factor
        malrule_answer = value * wrong_factor

        if verbose:
            steps = self._generate_verbose_steps_basic(problem, value, from_unit, to_unit, correct_factor, wrong_factor, malrule_answer)
        else:
            steps = self._generate_concise_steps_basic(problem, value, from_unit, to_unit, correct_factor, wrong_factor, malrule_answer)

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _handle_multi_step_conversion(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle multi-step conversions with wrong factor at first step."""
        value = problem.metadata['value']
        start_unit = problem.metadata['start_unit']
        mid_unit = problem.metadata['mid_unit']
        end_unit = problem.metadata['end_unit']
        factor1 = problem.metadata['factor1']
        factor2 = problem.metadata['factor2']
        wrong1 = problem.metadata['wrong_factor1']

        # MALRULE: Use wrong factor at first step
        malrule_answer = value * wrong1 * factor2

        if verbose:
            steps = self._generate_verbose_steps_multi_step(problem, value, start_unit, mid_unit, end_unit, factor1, factor2, wrong1, malrule_answer)
        else:
            steps = self._generate_concise_steps_multi_step(problem, value, start_unit, mid_unit, end_unit, factor1, factor2, wrong1, malrule_answer)

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _handle_imperial_to_metric(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle imperial to metric with guessed round number."""
        value = problem.metadata['value']
        from_unit = problem.metadata['from_unit']
        to_unit = problem.metadata['to_unit']
        correct_factor = problem.metadata['correct_factor']
        wrong_factor = problem.metadata['wrong_factor']

        # MALRULE: Use wrong (guessed) conversion factor
        malrule_answer = round(value * wrong_factor, 2)

        if verbose:
            steps = self._generate_verbose_steps_imperial_to_metric(problem, value, from_unit, to_unit, correct_factor, wrong_factor, malrule_answer)
        else:
            steps = self._generate_concise_steps_imperial_to_metric(problem, value, from_unit, to_unit, correct_factor, wrong_factor, malrule_answer)

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _handle_word_problem_context(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle word problem with wrong conversion factor."""
        value = problem.metadata['value']
        from_unit = problem.metadata['from_unit']
        to_unit = problem.metadata['to_unit']
        correct_factor = problem.metadata['correct_factor']
        wrong_factor = problem.metadata['wrong_factor']

        # MALRULE: Use wrong (round number) conversion factor
        malrule_answer = value * wrong_factor

        if verbose:
            steps = self._generate_verbose_steps_word_problem(problem, value, from_unit, to_unit, correct_factor, wrong_factor, malrule_answer)
        else:
            steps = self._generate_concise_steps_word_problem(problem, value, from_unit, to_unit, correct_factor, wrong_factor, malrule_answer)

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _handle_compound_units(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle compound units with oversimplified wrong factor."""
        value = problem.metadata['value']
        from_unit = problem.metadata['from_unit']
        to_unit = problem.metadata['to_unit']
        correct_factor = problem.metadata['correct_factor']
        wrong_factor = problem.metadata['wrong_factor']

        # MALRULE: Use oversimplified wrong factor
        malrule_answer = round(value * wrong_factor, 2)

        if verbose:
            steps = self._generate_verbose_steps_compound_units(problem, value, from_unit, to_unit, correct_factor, wrong_factor, malrule_answer)
        else:
            steps = self._generate_concise_steps_compound_units(problem, value, from_unit, to_unit, correct_factor, wrong_factor, malrule_answer)

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
