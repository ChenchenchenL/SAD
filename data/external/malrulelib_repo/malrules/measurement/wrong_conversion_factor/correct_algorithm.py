"""
Correct unit conversion algorithm.

Implements proper unit conversion using correct conversion factors.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class UnitConversionCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for unit conversion.

    Uses the correct conversion factor to convert between units.
    """

    def get_name(self) -> str:
        return "Correct Unit Conversion"

    def get_description(self) -> str:
        return (
            "Converts between units correctly using the appropriate conversion factor. "
            "Multiplies the value by the correct conversion factor."
        )

    def _generate_concise_steps_basic(self, problem: Problem, value, from_unit, to_unit, correct_factor, correct_answer) -> List[str]:
        """Generate concise steps for basic conversion."""
        steps = []
        steps.append(f"Convert {value} {from_unit} to {to_unit}")
        steps.append(f"1 {from_unit} = {correct_factor} {to_unit}")
        steps.append(f"{value} {from_unit} × ({correct_factor} {to_unit} / 1 {from_unit}) = {value} × {correct_factor} = {correct_answer} {to_unit}")
        steps.append(f"{correct_answer} {to_unit}")
        return steps

    def _generate_verbose_steps_basic(self, problem: Problem, value, from_unit, to_unit, correct_factor, correct_answer) -> List[str]:
        """Generate verbose steps for basic conversion."""
        steps = []
        steps.append(f"Converting: {value} {from_unit} to {to_unit}")
        steps.append(f"Conversion factor: 1 {from_unit} = {correct_factor} {to_unit}")
        steps.append(f"Calculation: {value} × {correct_factor} = {correct_answer}")
        steps.append(f"\nDimensional analysis approach:")
        steps.append(f"{value} {from_unit} × ({correct_factor} {to_unit} / 1 {from_unit}) = {correct_answer} {to_unit}")
        steps.append(f"The {from_unit} units cancel out, leaving {to_unit}")
        steps.append(f"Answer: {correct_answer} {to_unit}")
        return steps

    def _generate_concise_steps_multi_step(self, problem: Problem, value, start_unit, mid_unit, end_unit, factor1, factor2, correct_answer) -> List[str]:
        """Generate concise steps for multi-step conversion."""
        steps = []
        steps.append(f"Convert {value} {start_unit} to {end_unit}")
        steps.append(f"1 {start_unit} = {factor1} {mid_unit}")
        steps.append(f"1 {mid_unit} = {factor2} {end_unit}")
        steps.append(f"{value} × {factor1} = {value * factor1} {mid_unit}")
        steps.append(f"{value * factor1} × {factor2} = {correct_answer} {end_unit}")
        steps.append(f"{correct_answer} {end_unit}")
        return steps

    def _generate_verbose_steps_multi_step(self, problem: Problem, value, start_unit, mid_unit, end_unit, factor1, factor2, correct_answer) -> List[str]:
        """Generate verbose steps for multi-step conversion."""
        steps = []
        steps.append(f"Converting: {value} {start_unit} to {end_unit}")
        steps.append(f"This requires TWO steps: {start_unit} → {mid_unit} → {end_unit}")
        steps.append("")
        steps.append(f"Step 1: Convert {start_unit} to {mid_unit}")
        steps.append(f"  Conversion factor: 1 {start_unit} = {factor1} {mid_unit}")
        steps.append(f"  {value} × {factor1} = {value * factor1} {mid_unit}")
        steps.append("")
        steps.append(f"Step 2: Convert {mid_unit} to {end_unit}")
        steps.append(f"  Conversion factor: 1 {mid_unit} = {factor2} {end_unit}")
        steps.append(f"  {value * factor1} × {factor2} = {correct_answer} {end_unit}")
        steps.append("")
        steps.append(f"Alternatively, multiply factors: {value} × {factor1} × {factor2} = {correct_answer}")
        steps.append(f"Answer: {correct_answer} {end_unit}")
        return steps

    def _generate_concise_steps_imperial_to_metric(self, problem: Problem, value, from_unit, to_unit, correct_factor, correct_answer) -> List[str]:
        """Generate concise steps for imperial to metric conversion."""
        steps = []
        steps.append(f"Convert {value} {from_unit} to {to_unit}")
        steps.append(f"1 {from_unit} ≈ {correct_factor} {to_unit}")
        steps.append(f"{value} × {correct_factor} = {correct_answer}")
        steps.append(f"{correct_answer} {to_unit}")
        return steps

    def _generate_verbose_steps_imperial_to_metric(self, problem: Problem, value, from_unit, to_unit, correct_factor, correct_answer) -> List[str]:
        """Generate verbose steps for imperial to metric conversion."""
        steps = []
        steps.append(f"Converting: {value} {from_unit} to {to_unit}")
        steps.append(f"Cross-system conversion (imperial ↔ metric)")
        steps.append(f"Conversion factor: 1 {from_unit} ≈ {correct_factor} {to_unit}")
        steps.append("")
        steps.append(f"Calculation: {value} × {correct_factor} = {correct_answer}")
        steps.append(f"Answer: {correct_answer} {to_unit}")
        return steps

    def _generate_concise_steps_word_problem(self, problem: Problem, value, from_unit, to_unit, correct_factor, correct_answer) -> List[str]:
        """Generate concise steps for word problem conversion."""
        steps = []
        steps.append(f"{problem.text}")
        steps.append(f"Convert {value} {from_unit} to {to_unit}")
        steps.append(f"1 {from_unit} = {correct_factor} {to_unit}")
        steps.append(f"{value} × {correct_factor} = {correct_answer}")
        steps.append(f"{correct_answer} {to_unit}")
        return steps

    def _generate_verbose_steps_word_problem(self, problem: Problem, value, from_unit, to_unit, correct_factor, correct_answer) -> List[str]:
        """Generate verbose steps for word problem conversion."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append(f"Identify: Need to convert {value} {from_unit} to {to_unit}")
        steps.append(f"Conversion factor: 1 {from_unit} = {correct_factor} {to_unit}")
        steps.append(f"Calculation: {value} × {correct_factor} = {correct_answer}")
        steps.append(f"Answer: {correct_answer} {to_unit}")
        return steps

    def _generate_concise_steps_compound_units(self, problem: Problem, value, from_unit, to_unit, correct_factor, correct_answer) -> List[str]:
        """Generate concise steps for compound unit conversion."""
        steps = []
        steps.append(f"Convert {value} {from_unit} to {to_unit}")
        steps.append(f"1 {from_unit} ≈ {correct_factor} {to_unit}")
        steps.append(f"{value} × {correct_factor} = {correct_answer}")
        steps.append(f"{correct_answer} {to_unit}")
        return steps

    def _generate_verbose_steps_compound_units(self, problem: Problem, value, from_unit, to_unit, correct_factor, correct_answer) -> List[str]:
        """Generate verbose steps for compound unit conversion."""
        steps = []
        steps.append(f"Converting: {value} {from_unit} to {to_unit}")
        steps.append(f"Compound unit conversion (involves both numerator and denominator)")
        steps.append(f"Conversion factor: 1 {from_unit} ≈ {correct_factor} {to_unit}")
        steps.append("")
        steps.append(f"Calculation: {value} × {correct_factor} = {correct_answer}")
        steps.append(f"Answer: {correct_answer} {to_unit}")
        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct unit conversion.

        Args:
            problem: Unit conversion problem
            verbose: If True, generate verbose explanatory steps; if False, generate concise steps

        Returns:
            Solution with correct conversion
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

        # CORRECT ALGORITHM: Multiply by the correct conversion factor
        correct_answer = value * correct_factor

        if verbose:
            steps = self._generate_verbose_steps_basic(problem, value, from_unit, to_unit, correct_factor, correct_answer)
        else:
            steps = self._generate_concise_steps_basic(problem, value, from_unit, to_unit, correct_factor, correct_answer)

        return Solution(
            answer=str(correct_answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _handle_multi_step_conversion(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle multi-step conversions with correct factors."""
        value = problem.metadata['value']
        start_unit = problem.metadata['start_unit']
        mid_unit = problem.metadata['mid_unit']
        end_unit = problem.metadata['end_unit']
        factor1 = problem.metadata['factor1']
        factor2 = problem.metadata['factor2']

        # CORRECT ALGORITHM: Multiply by both factors
        correct_answer = value * factor1 * factor2

        if verbose:
            steps = self._generate_verbose_steps_multi_step(problem, value, start_unit, mid_unit, end_unit, factor1, factor2, correct_answer)
        else:
            steps = self._generate_concise_steps_multi_step(problem, value, start_unit, mid_unit, end_unit, factor1, factor2, correct_answer)

        return Solution(
            answer=str(correct_answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _handle_imperial_to_metric(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle imperial to metric conversions with correct factors."""
        value = problem.metadata['value']
        from_unit = problem.metadata['from_unit']
        to_unit = problem.metadata['to_unit']
        correct_factor = problem.metadata['correct_factor']

        # CORRECT ALGORITHM: Multiply by correct factor
        correct_answer = round(value * correct_factor, 2)

        if verbose:
            steps = self._generate_verbose_steps_imperial_to_metric(problem, value, from_unit, to_unit, correct_factor, correct_answer)
        else:
            steps = self._generate_concise_steps_imperial_to_metric(problem, value, from_unit, to_unit, correct_factor, correct_answer)

        return Solution(
            answer=str(correct_answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _handle_word_problem_context(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle word problem contexts with correct factors."""
        value = problem.metadata['value']
        from_unit = problem.metadata['from_unit']
        to_unit = problem.metadata['to_unit']
        correct_factor = problem.metadata['correct_factor']

        # CORRECT ALGORITHM: Multiply by correct factor
        correct_answer = value * correct_factor

        if verbose:
            steps = self._generate_verbose_steps_word_problem(problem, value, from_unit, to_unit, correct_factor, correct_answer)
        else:
            steps = self._generate_concise_steps_word_problem(problem, value, from_unit, to_unit, correct_factor, correct_answer)

        return Solution(
            answer=str(correct_answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _handle_compound_units(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle compound unit conversions with correct factors."""
        value = problem.metadata['value']
        from_unit = problem.metadata['from_unit']
        to_unit = problem.metadata['to_unit']
        correct_factor = problem.metadata['correct_factor']

        # CORRECT ALGORITHM: Multiply by correct factor
        correct_answer = round(value * correct_factor, 2)

        if verbose:
            steps = self._generate_verbose_steps_compound_units(problem, value, from_unit, to_unit, correct_factor, correct_answer)
        else:
            steps = self._generate_concise_steps_compound_units(problem, value, from_unit, to_unit, correct_factor, correct_answer)

        return Solution(
            answer=str(correct_answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
