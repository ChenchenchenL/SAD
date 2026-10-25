"""
Malrule algorithm for Inverted-Conversion-Factor error.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class InvertedConversionFactorMalrule(Malrule):
    """
    Students invert the conversion fraction (multiply instead of divide or vice versa).

    Example: Convert 24 inches to feet (12 inches = 1 foot)
    Student: 24 × 12 = 288 (WRONG - inverted!)
    Correct: 24 ÷ 12 = 2 feet
    """

    def get_name(self) -> str:
        return "Inverted-Conversion-Factor"

    def get_description(self) -> str:
        return (
            "Students set up the conversion factor incorrectly by placing units in the wrong "
            "position (numerator vs. denominator), resulting in multiplication when division is "
            "required or vice versa. This is documented as one of the most common errors in "
            "dimensional analysis, where students fail to ensure that units cancel appropriately."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Malrule: invert the conversion fraction
        return problem.metadata['malrule_answer']

    def _generate_concise_steps_basic(self, problem: Problem, value, from_unit, to_unit, factor, malrule_answer) -> List[str]:
        """Generate concise steps for basic conversion malrule."""
        steps = []
        steps.append(f"Convert {value} {from_unit} to {to_unit}")
        steps.append(f"{factor} {from_unit} = 1 {to_unit}")
        steps.append(f"{value} {from_unit} × ({factor} {from_unit} / 1 {to_unit}) = {value} × {factor} = {malrule_answer}")
        steps.append(f"{malrule_answer}")
        return steps

    def _generate_verbose_steps_basic(self, problem: Problem, value, from_unit, to_unit, factor, malrule_answer) -> List[str]:
        """Generate verbose steps for basic conversion malrule."""
        steps = []
        steps.append(f"Problem: Convert {value} {from_unit} to {to_unit}")
        steps.append(f"Given: {factor} {from_unit} = 1 {to_unit}")
        steps.append("")
        steps.append("MALRULE: Set up conversion fraction INVERTED")
        steps.append(f"  MALRULE REASONING: 'Use the conversion factor {factor}'")
        steps.append(f"                     'Just multiply by it'")
        steps.append("")
        steps.append(f"Step 1: Set up (INCORRECT) conversion")
        steps.append(f"  {value} {from_unit} × ({factor} {from_unit} / 1 {to_unit})")
        steps.append(f"  (WRONG! Units don't cancel - {from_unit} appears twice!)")
        steps.append("")
        steps.append(f"Step 2: Calculate (ignoring units)")
        steps.append(f"  {value} × {factor} = {malrule_answer}")
        steps.append("")
        steps.append(f"Final Answer: {malrule_answer} (INCORRECT - inverted fraction!)")
        steps.append(f"  Should be: {value} × (1/{factor}) = {value/factor:.1f} {to_unit}")
        steps.append(f"  Check reasonableness: {malrule_answer} {to_unit} is way too large!")
        return steps

    def _generate_concise_steps_multi_step(self, problem: Problem, value, start_unit, mid_unit, end_unit, factor1, factor2, malrule_answer) -> List[str]:
        """Generate concise steps for multi-step conversion malrule."""
        steps = []
        steps.append(f"Convert {value} {start_unit} to {end_unit}")
        steps.append(f"{factor1} {start_unit} = 1 {mid_unit}")
        steps.append(f"{factor2} {mid_unit} = 1 {end_unit}")
        steps.append(f"{value} × {factor1} = {value * factor1} {mid_unit}")
        steps.append(f"{value * factor1} ÷ {factor2} = {malrule_answer} {end_unit}")
        steps.append(f"{malrule_answer} {end_unit}")
        return steps

    def _generate_verbose_steps_multi_step(self, problem: Problem, value, start_unit, mid_unit, end_unit, factor1, factor2, malrule_answer) -> List[str]:
        """Generate verbose steps for multi-step conversion malrule."""
        steps = []
        steps.append(f"Converting: {value} {start_unit} to {end_unit}")
        steps.append(f"MALRULE: Invert the conversion fraction in multi-step problem")
        steps.append("")
        steps.append(f"Step 1: Convert {start_unit} to {mid_unit}")
        steps.append(f"  {factor1} {start_unit} = 1 {mid_unit}")
        steps.append(f"  MALRULE: Student multiplies instead of divides")
        steps.append(f"  {value} × {factor1} = {value * factor1} {mid_unit} (WRONG!)")
        steps.append("")
        steps.append(f"Step 2: Convert {mid_unit} to {end_unit}")
        steps.append(f"  {factor2} {mid_unit} = 1 {end_unit}")
        steps.append(f"  {value * factor1} ÷ {factor2} = {malrule_answer} {end_unit}")
        steps.append("")
        steps.append(f"Answer: {malrule_answer} {end_unit} (INCORRECT - inverted at step 1)")
        steps.append(f"Should be: {value} ÷ {factor1} ÷ {factor2} = {value / factor1 / factor2} {end_unit}")
        return steps

    def _generate_concise_steps_imperial_to_metric(self, problem: Problem, value, from_unit, to_unit, inv_factor, correct_factor, malrule_answer) -> List[str]:
        """Generate concise steps for imperial to metric malrule."""
        steps = []
        steps.append(f"Convert {value} {from_unit} to {to_unit}")
        steps.append(f"1 {from_unit} = {correct_factor} {to_unit}")
        steps.append(f"{value} × {inv_factor} = {malrule_answer}")
        steps.append(f"{malrule_answer} {to_unit}")
        return steps

    def _generate_verbose_steps_imperial_to_metric(self, problem: Problem, value, from_unit, to_unit, inv_factor, correct_factor, malrule_answer) -> List[str]:
        """Generate verbose steps for imperial to metric malrule."""
        steps = []
        steps.append(f"Converting: {value} {from_unit} to {to_unit}")
        steps.append(f"MALRULE: Use inverted conversion factor")
        steps.append("")
        steps.append(f"Given: 1 {from_unit} = {correct_factor} {to_unit}")
        steps.append(f"MALRULE REASONING: 'I'll flip the fraction'")
        steps.append(f"                   'Use {inv_factor} instead'")
        steps.append("")
        steps.append(f"Calculation: {value} × {inv_factor} = {malrule_answer}")
        steps.append(f"Answer: {malrule_answer} {to_unit} (INCORRECT - inverted factor)")
        steps.append(f"Should use: {value} × {correct_factor} = {round(value * correct_factor, 2)} {to_unit}")
        return steps

    def _generate_concise_steps_word_problem(self, problem: Problem, value, from_unit, to_unit, factor, malrule_answer) -> List[str]:
        """Generate concise steps for word problem malrule."""
        steps = []
        steps.append(f"{problem.text}")
        steps.append(f"Convert {value} {from_unit} to {to_unit}")
        steps.append(f"{factor} {from_unit} = 1 {to_unit}")
        steps.append(f"{value} × {factor} = {malrule_answer}")
        steps.append(f"{malrule_answer} {to_unit}")
        return steps

    def _generate_verbose_steps_word_problem(self, problem: Problem, value, from_unit, to_unit, factor, malrule_answer) -> List[str]:
        """Generate verbose steps for word problem malrule."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: Set up conversion fraction INVERTED")
        steps.append(f"Identify: Need to convert {value} {from_unit} to {to_unit}")
        steps.append(f"Given: {factor} {from_unit} = 1 {to_unit}")
        steps.append(f"MALRULE REASONING: 'I see {factor}, so multiply by it'")
        steps.append("")
        steps.append(f"Calculation: {value} × {factor} = {malrule_answer}")
        steps.append(f"Answer: {malrule_answer} {to_unit} (INCORRECT - should divide not multiply)")
        steps.append(f"Correct: {value} ÷ {factor} = {value / factor} {to_unit}")
        return steps

    def _generate_concise_steps_compound_units(self, problem: Problem, value, from_unit, to_unit, inv_factor, correct_factor, malrule_answer) -> List[str]:
        """Generate concise steps for compound units malrule."""
        steps = []
        steps.append(f"Convert {value} {from_unit} to {to_unit}")
        steps.append(f"1 {from_unit} = {correct_factor} {to_unit}")
        steps.append(f"{value} × {inv_factor} = {malrule_answer}")
        steps.append(f"{malrule_answer} {to_unit}")
        return steps

    def _generate_verbose_steps_compound_units(self, problem: Problem, value, from_unit, to_unit, inv_factor, correct_factor, malrule_answer) -> List[str]:
        """Generate verbose steps for compound units malrule."""
        steps = []
        steps.append(f"Converting: {value} {from_unit} to {to_unit}")
        steps.append(f"MALRULE: Apply inverted conversion factor")
        steps.append("")
        steps.append(f"Given: 1 {from_unit} = {correct_factor} {to_unit}")
        steps.append(f"MALRULE REASONING: 'Compound units are confusing'")
        steps.append(f"                   'I'll use {inv_factor} instead'")
        steps.append("")
        steps.append(f"Calculation: {value} × {inv_factor} = {malrule_answer}")
        steps.append(f"Answer: {malrule_answer} {to_unit} (INCORRECT - inverted)")
        steps.append(f"Should be: {value} × {correct_factor} = {round(value * correct_factor, 2)} {to_unit}")
        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
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
        factor = problem.metadata['factor']

        # MALRULE: Invert the conversion (multiply instead of divide)
        malrule_answer = value * factor

        if verbose:
            steps = self._generate_verbose_steps_basic(problem, value, from_unit, to_unit, factor, malrule_answer)
        else:
            steps = self._generate_concise_steps_basic(problem, value, from_unit, to_unit, factor, malrule_answer)

        return Solution(
            answer=int(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _handle_multi_step_conversion(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle multi-step conversions with inversion at first step."""
        value = problem.metadata['value']
        start_unit = problem.metadata['start_unit']
        mid_unit = problem.metadata['mid_unit']
        end_unit = problem.metadata['end_unit']
        factor1 = problem.metadata['factor1']
        factor2 = problem.metadata['factor2']

        # MALRULE: Invert at first step (multiply instead of divide)
        malrule_answer = value * factor1 / factor2

        if verbose:
            steps = self._generate_verbose_steps_multi_step(problem, value, start_unit, mid_unit, end_unit, factor1, factor2, malrule_answer)
        else:
            steps = self._generate_concise_steps_multi_step(problem, value, start_unit, mid_unit, end_unit, factor1, factor2, malrule_answer)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _handle_imperial_to_metric(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle imperial to metric with inverted factor."""
        value = problem.metadata['value']
        from_unit = problem.metadata['from_unit']
        to_unit = problem.metadata['to_unit']
        inv_factor = problem.metadata['inv_factor']
        correct_factor = problem.metadata['correct_factor']

        # MALRULE: Use inverted factor
        malrule_answer = round(value * inv_factor, 2)

        if verbose:
            steps = self._generate_verbose_steps_imperial_to_metric(problem, value, from_unit, to_unit, inv_factor, correct_factor, malrule_answer)
        else:
            steps = self._generate_concise_steps_imperial_to_metric(problem, value, from_unit, to_unit, inv_factor, correct_factor, malrule_answer)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _handle_word_problem_context(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle word problem with inverted conversion."""
        value = problem.metadata['value']
        from_unit = problem.metadata['from_unit']
        to_unit = problem.metadata['to_unit']
        factor = problem.metadata['factor']

        # MALRULE: Multiply instead of divide
        malrule_answer = value * factor

        if verbose:
            steps = self._generate_verbose_steps_word_problem(problem, value, from_unit, to_unit, factor, malrule_answer)
        else:
            steps = self._generate_concise_steps_word_problem(problem, value, from_unit, to_unit, factor, malrule_answer)

        return Solution(
            answer=int(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _handle_compound_units(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle compound units with inverted factor."""
        value = problem.metadata['value']
        from_unit = problem.metadata['from_unit']
        to_unit = problem.metadata['to_unit']
        inv_factor = problem.metadata['inv_factor']
        correct_factor = problem.metadata['correct_factor']

        # MALRULE: Use inverted factor
        malrule_answer = round(value * inv_factor, 2)

        if verbose:
            steps = self._generate_verbose_steps_compound_units(problem, value, from_unit, to_unit, inv_factor, correct_factor, malrule_answer)
        else:
            steps = self._generate_concise_steps_compound_units(problem, value, from_unit, to_unit, inv_factor, correct_factor, malrule_answer)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
