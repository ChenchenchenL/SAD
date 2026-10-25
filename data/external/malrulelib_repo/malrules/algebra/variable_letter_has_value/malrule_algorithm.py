"""
Malrule algorithm for Variable-Letter-Has-Value error.
This version calculates the assumed value based on alphabet position.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import re
from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class VariableLetterHasValueMalrule(Malrule):
    """
    Students believe variable letters have inherent fixed values.

    Example: x + 5 = 12 → Student thinks "x is always 10"
    """

    def get_name(self) -> str:
        return "Variable-Letter-Has-Value"

    def get_description(self) -> str:
        return (
            "Students believe that algebraic letters have inherent fixed values, often "
            "based on the letter's position in the alphabet (e.g., x=10, a=1) or other "
            "associations. This is a manifestation of the broader 'letter-as-object' "
            "misconception where letters are not understood as representing variable quantities."
        )

    def _generate_verbose_steps(self, problem: Problem, template: str, variable: str,
                                 assumed_value: int) -> List[str]:
        """Generate verbose steps with detailed explanations."""
        steps = []

        equation = problem.metadata.get('equation', '')

        if template == 'basic_addition':
            constant = problem.metadata['constant']
            result = problem.metadata['result']
            if not equation:
                equation = f"{variable} + {constant} = {result}"

            steps.append(f"Problem: {equation}")
            steps.append("")
            steps.append(f"MALRULE: Variable {variable} has fixed value")
            steps.append(f"  MALRULE REASONING: '{variable} always equals {assumed_value}'")
            self._add_variable_reasoning(steps, variable)
            steps.append("")
            steps.append(f"Substitute {variable} = {assumed_value}:")
            steps.append(f"  {assumed_value} + {constant} = {assumed_value + constant}")
            steps.append("")
            steps.append(f"Check: Does {assumed_value + constant} = {result}?")
            if (assumed_value + constant) == result:
                steps.append(f"  Yes! {assumed_value + constant} = {result} ✓ (lucky coincidence!)")
            else:
                steps.append(f"  No! {assumed_value + constant} ≠ {result}")
                steps.append(f"  (But student ignores this contradiction)")

        elif template == 'basic_subtraction':
            constant = problem.metadata['constant']
            result = problem.metadata['result']
            if not equation:
                equation = f"{variable} - {constant} = {result}"

            steps.append(f"Problem: {equation}")
            steps.append("")
            steps.append(f"MALRULE: Variable {variable} has fixed value")
            steps.append(f"  MALRULE REASONING: '{variable} always equals {assumed_value}'")
            self._add_variable_reasoning(steps, variable)
            steps.append("")
            steps.append(f"Substitute {variable} = {assumed_value}:")
            steps.append(f"  {assumed_value} - {constant} = {assumed_value - constant}")
            steps.append("")
            steps.append(f"Check: Does {assumed_value - constant} = {result}?")
            if (assumed_value - constant) == result:
                steps.append(f"  Yes! {assumed_value - constant} = {result} ✓ (lucky coincidence!)")
            else:
                steps.append(f"  No! {assumed_value - constant} ≠ {result}")
                steps.append(f"  (But student ignores this contradiction)")

        elif template == 'basic_multiplication':
            coefficient = problem.metadata['coefficient']
            result = problem.metadata['result']
            if not equation:
                equation = f"{coefficient}{variable} = {result}"

            steps.append(f"Problem: {equation}")
            steps.append("")
            steps.append(f"MALRULE: Variable {variable} has fixed value")
            steps.append(f"  MALRULE REASONING: '{variable} always equals {assumed_value}'")
            self._add_variable_reasoning(steps, variable)
            steps.append("")
            steps.append(f"Substitute {variable} = {assumed_value}:")
            steps.append(f"  {coefficient} × {assumed_value} = {coefficient * assumed_value}")
            steps.append("")
            steps.append(f"Check: Does {coefficient * assumed_value} = {result}?")
            if (coefficient * assumed_value) == result:
                steps.append(f"  Yes! {coefficient * assumed_value} = {result} ✓ (lucky coincidence!)")
            else:
                steps.append(f"  No! {coefficient * assumed_value} ≠ {result}")
                steps.append(f"  (But student ignores this contradiction)")

        elif template == 'two_step_equation':
            coefficient = problem.metadata['coefficient']
            constant = problem.metadata['constant']
            result = problem.metadata['result']
            if not equation:
                equation = f"{coefficient}{variable} + {constant} = {result}"

            steps.append(f"Problem: {equation}")
            steps.append("")
            steps.append(f"MALRULE: Variable {variable} has fixed value")
            steps.append(f"  MALRULE REASONING: '{variable} always equals {assumed_value}'")
            self._add_variable_reasoning(steps, variable)
            steps.append("")
            steps.append(f"Substitute {variable} = {assumed_value}:")
            steps.append(f"  {coefficient} × {assumed_value} + {constant} = {coefficient * assumed_value + constant}")
            steps.append("")
            steps.append(f"Check: Does {coefficient * assumed_value + constant} = {result}?")
            if (coefficient * assumed_value + constant) == result:
                steps.append(f"  Yes! {coefficient * assumed_value + constant} = {result} ✓ (lucky coincidence!)")
            else:
                steps.append(f"  No! {coefficient * assumed_value + constant} ≠ {result}")
                steps.append(f"  (But student ignores this contradiction)")

        elif template == 'word_problem':
            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append(f"MALRULE: Variable {variable} has fixed value")
            steps.append(f"  MALRULE REASONING: '{variable} always equals {assumed_value}'")
            self._add_variable_reasoning(steps, variable)
            steps.append("")
            steps.append(f"Student's answer: {variable} = {assumed_value}")
            steps.append("")
            steps.append(f"(Student doesn't solve the problem; just states what {variable} 'must be')")

        steps.append("")
        steps.append(f"Final Answer: {variable} = {assumed_value}")
        steps.append("")
        steps.append(f"INCORRECT! Variables don't have fixed values - they are unknowns to be solved for.")

        return steps

    def _generate_concise_steps(self, problem: Problem, template: str, variable: str,
                                 assumed_value: int) -> List[str]:
        """Generate concise steps with only formulas and values."""
        steps = []

        equation = problem.metadata.get('equation', '')

        if template == 'basic_addition':
            constant = problem.metadata['constant']
            result = problem.metadata['result']
            if not equation:
                equation = f"{variable} + {constant} = {result}"
            steps.append(f"Solve for {variable}: {equation}")
            steps.append(f"{variable} = {assumed_value}")

        elif template == 'basic_subtraction':
            constant = problem.metadata['constant']
            result = problem.metadata['result']
            if not equation:
                equation = f"{variable} - {constant} = {result}"
            steps.append(f"Solve for {variable}: {equation}")
            steps.append(f"{variable} = {assumed_value}")

        elif template == 'basic_multiplication':
            coefficient = problem.metadata['coefficient']
            result = problem.metadata['result']
            if not equation:
                equation = f"{coefficient}{variable} = {result}"
            steps.append(f"Solve for {variable}: {equation}")
            steps.append(f"{variable} = {assumed_value}")

        elif template == 'two_step_equation':
            coefficient = problem.metadata['coefficient']
            constant = problem.metadata['constant']
            result = problem.metadata['result']
            if not equation:
                equation = f"{coefficient}{variable} + {constant} = {result}"
            steps.append(f"Solve for {variable}: {equation}")
            steps.append(f"{variable} = {assumed_value}")

        elif template == 'word_problem':
            steps.append(f"{problem.text}")
            steps.append(f"{variable} = {assumed_value}")

        return steps

    def _get_assumed_value(self, variable: str) -> int:
        """
        Calculate the assumed value for a variable based on student misconceptions.

        Common student misconceptions (from research):
        - x = 10 (students incorrectly think x is the 10th letter)
        - n = 1 (students think "n" stands for "number one")
        - a = 1 (first letter)
        - y = 25 (25th letter)
        - b = 2 (second letter)
        - c = 3 (third letter)
        """
        # Common variable misconceptions based on research
        # Note: Some of these are incorrect alphabet positions (e.g., x=10 when x is actually 24th)
        # but reflect actual student beliefs documented in research
        assumed_values = {
            'x': 10,  # Students often think x=10 (though x is actually 24th letter)
            'n': 1,   # Students think "n" for "number one"
            'a': 1,   # First letter (correct)
            'y': 25,  # 25th letter (correct)
            'b': 2,   # Second letter (correct)
            'c': 3,   # Third letter (correct)
            'd': 4,   # Fourth letter (correct)
            'e': 5,   # Fifth letter (correct)
        }

        # If we have a specific mapping for this variable, use it
        if variable in assumed_values:
            return assumed_values[variable]

        # Otherwise, use actual alphabet position (a=1, b=2, ..., z=26)
        if len(variable) == 1 and variable.isalpha():
            return ord(variable.lower()) - ord('a') + 1

        # Fallback
        return 1

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        variable = problem.metadata['variable']
        return self._get_assumed_value(variable)

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Variable-Letter-Has-Value malrule.

        Args:
            problem: Algebraic equation problem
            verbose: If True, generate detailed steps; if False, generate concise steps

        Returns:
            Solution with incorrect (assumed) value
        """
        template = problem.metadata.get('template', 'basic_addition')
        variable = problem.metadata['variable']

        # Calculate assumed value based on variable letter
        assumed_value = self._get_assumed_value(variable)

        # Generate steps based on verbose setting
        if verbose:
            steps = self._generate_verbose_steps(problem, template, variable, assumed_value)
        else:
            steps = self._generate_concise_steps(problem, template, variable, assumed_value)

        return Solution(
            answer=assumed_value,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _add_variable_reasoning(self, steps: List[str], variable: str):
        """Add explanation for why student thinks variable has this value."""
        assumed_value = self._get_assumed_value(variable)

        # Explanations based on research into student misconceptions
        reasoning_map = {
            'x': "x is 10th letter of alphabet",
            'n': "n for 'number one'",
            'a': "a is first letter",
            'y': "y is 25th letter",
            'b': "b is second letter",
            'c': "c is third letter",
            'd': "d is fourth letter",
            'e': "e is fifth letter",
        }

        if variable in reasoning_map:
            steps.append(f"  ({reasoning_map[variable]})")
        else:
            # For other letters, explain based on alphabet position
            steps.append(f"  ({variable} is {assumed_value}th letter of alphabet)")
