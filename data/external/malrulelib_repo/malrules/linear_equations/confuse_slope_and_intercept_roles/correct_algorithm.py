"""
Correct algorithm for slope and y-intercept identification and equation writing.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class SlopeInterceptCorrectAlgorithm(CorrectAlgorithm):
    """Correctly handles slope and y-intercept in their proper roles."""

    def get_name(self) -> str:
        return "Correct Slope-Intercept Understanding"

    def get_description(self) -> str:
        return "Correctly assigns m (slope) and b (y-intercept) to their proper roles in y = mx + b."

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply correct algorithm across all templates."""
        template = problem.metadata.get('template', problem.metadata['problem_type'])
        m = problem.metadata['slope']
        b = problem.metadata['y_intercept']

        # COMPUTE answers from problem data instead of pulling from metadata
        # Correct: use proper roles (m=slope, b=y-intercept)
        # Malrule: swap roles (m=y-intercept, b=slope)
        if template in ['write_equation', 'word_problem_context']:
            # Format equation: y = mx + b
            correct_answer = self._format_equation(m, b)
            malrule_answer = self._format_equation(b, m)  # Swapped!
        elif template in ['identify_slope', 'standard_form_identify']:
            # Identify slope from equation
            correct_answer = str(m)
            malrule_answer = str(b)  # Student confuses slope with y-intercept
        elif template == 'identify_y_intercept':
            # Identify y-intercept from equation
            correct_answer = str(b)
            malrule_answer = str(m)  # Student confuses y-intercept with slope
        else:
            # Fallback for unknown templates
            correct_answer = str(m)
            malrule_answer = str(b)

        # Generate steps based on verbosity setting
        if verbose:
            steps = self._generate_verbose_steps(problem, template, m, b, correct_answer, malrule_answer)
        else:
            steps = self._generate_concise_steps(problem, template, m, b, correct_answer)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _format_equation(self, m, b):
        """Format equation y = mx + b with proper sign handling."""
        # Format slope coefficient
        if m == 1:
            m_str = ""
        elif m == -1:
            m_str = "-"
        else:
            m_str = str(m)

        # Format the b term with proper sign
        if b >= 0:
            equation = f"y = {m_str}x + {b}"
        else:
            equation = f"y = {m_str}x - {abs(b)}"

        return equation

    def _generate_concise_steps(self, problem: Problem, template: str, m: int, b: int, correct_answer: str) -> List[str]:
        """Generate concise steps with only formula and values."""
        steps = []
        steps.append(f"Question: {problem.text}")

        if template == 'write_equation':
            steps.append(f"Formula: y = mx + b")
            steps.append(f"Given: slope (m) = {m}, y-intercept (b) = {b}")
            steps.append(f"Substitute: y = {m}x + {b}")
            steps.append(f"Answer: {correct_answer}")

        elif template == 'identify_slope':
            equation = problem.metadata['equation']
            steps.append(f"Given equation: {equation}")
            steps.append(f"Form: y = mx + b")
            steps.append(f"Slope (m) = coefficient of x = {m}")
            steps.append(f"Answer: {correct_answer}")

        elif template == 'identify_y_intercept':
            equation = problem.metadata['equation']
            steps.append(f"Given equation: {equation}")
            steps.append(f"Form: y = mx + b")
            steps.append(f"Y-intercept (b) = constant term = {b}")
            steps.append(f"Answer: {correct_answer}")

        elif template == 'standard_form_identify':
            equation = problem.metadata['equation']
            A = problem.metadata['A']
            B = problem.metadata['B']
            C = problem.metadata['C']
            steps.append(f"Given equation: {equation}")
            steps.append(f"Convert: {B}y = -{A}x + {C}")
            steps.append(f"Slope-intercept form: y = {m}x + {b}")
            steps.append(f"Slope = {m}")
            steps.append(f"Answer: {correct_answer}")

        elif template == 'word_problem_context':
            word_problem_subtype = problem.metadata.get('word_problem_subtype', 'write_equation')

            if word_problem_subtype == 'write_equation':
                steps.append(f"Extract: rate = {m}, starting value = {b}")
                steps.append(f"Formula: y = mx + b")
                steps.append(f"Substitute: y = {m}x + {b}")
                steps.append(f"Answer: {correct_answer}")

            elif word_problem_subtype == 'identify_slope':
                steps.append(f"Extract: rate = {m}, starting value = {b}")
                steps.append(f"Slope = rate of change = {m}")
                steps.append(f"Answer: {correct_answer}")

            elif word_problem_subtype == 'identify_intercept':
                steps.append(f"Extract: rate = {m}, starting value = {b}")
                steps.append(f"Y-intercept = starting value = {b}")
                steps.append(f"Answer: {correct_answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, template: str, m: int, b: int, correct_answer: str, malrule_answer: str) -> List[str]:
        """Generate verbose steps with full explanations."""
        steps = []
        steps.append(f"Problem: {problem.text[:100]}...")
        steps.append("")
        steps.append("CORRECT METHOD: Use proper roles for slope and y-intercept")
        steps.append("  m (slope) = coefficient of x")
        steps.append("  b (y-intercept) = constant term")
        steps.append("")

        if template == 'write_equation':
            steps.append(f"Step 1: Recall formula y = mx + b")
            steps.append(f"  Given: slope = {m}, y-intercept = {b}")
            steps.append("")
            steps.append(f"Step 2: Substitute (CORRECT POSITIONS!)")
            steps.append(f"  m goes with x: {m}x")
            steps.append(f"  b is constant: {'+' if b >= 0 else '-'} {abs(b)}")
            steps.append("")
            steps.append(f"Step 3: Verify")
            steps.append(f"  Slope = {m} (rate of change) ✓")
            steps.append(f"  Y-intercept = {b} (crosses y-axis) ✓")
            steps.append("")
            steps.append(f"Final Answer: {correct_answer} ✓")
            steps.append(f"  NOT {malrule_answer} (that swaps the roles!) ✗")

        elif template == 'identify_slope':
            equation = problem.metadata['equation']
            steps.append(f"Step 1: Recognize form")
            steps.append(f"  Given: {equation}")
            steps.append(f"  This is y = mx + b form")
            steps.append("")
            steps.append(f"Step 2: Identify coefficient of x")
            steps.append(f"  Coefficient of x = {m}")
            steps.append(f"  Constant term = {b}")
            steps.append("")
            steps.append(f"Step 3: State slope correctly")
            steps.append(f"  Slope = coefficient of x = {m} ✓")
            steps.append("")
            steps.append(f"Final Answer: {correct_answer} ✓")
            steps.append(f"  NOT {malrule_answer} (that's y-intercept!) ✗")

        elif template == 'identify_y_intercept':
            equation = problem.metadata['equation']
            steps.append(f"Step 1: Recognize form")
            steps.append(f"  Given: {equation}")
            steps.append(f"  This is y = mx + b form")
            steps.append("")
            steps.append(f"Step 2: Identify constant term")
            steps.append(f"  Coefficient of x = {m} (slope)")
            steps.append(f"  Constant term = {b} (y-intercept)")
            steps.append("")
            steps.append(f"Step 3: State y-intercept correctly")
            steps.append(f"  Y-intercept = constant = {b} ✓")
            steps.append("")
            steps.append(f"Final Answer: {correct_answer} ✓")
            steps.append(f"  NOT {malrule_answer} (that's slope!) ✗")

        elif template == 'standard_form_identify':
            equation = problem.metadata['equation']
            A = problem.metadata['A']
            B = problem.metadata['B']
            C = problem.metadata['C']
            steps.append(f"Step 1: Convert to slope-intercept form")
            steps.append(f"  Given: {equation}")
            steps.append(f"  Solve for y:")
            steps.append(f"  {B}y = -{A}x + {C}")
            steps.append(f"  y = -{A}/{B}x + {C}/{B}")
            steps.append(f"  y = {m}x + {b}")
            steps.append("")
            steps.append(f"Step 2: Identify slope")
            steps.append(f"  Slope = coefficient of x = {m} ✓")
            steps.append("")
            steps.append(f"Final Answer: {correct_answer} ✓")
            steps.append(f"  NOT {malrule_answer} (that confuses constant {C} with slope!) ✗")

        elif template == 'word_problem_context':
            word_problem_subtype = problem.metadata.get('word_problem_subtype', 'write_equation')

            if word_problem_subtype == 'write_equation':
                steps.append(f"Step 1: Identify rate and starting value from context")
                steps.append(f"  Rate (change per unit): {m} → this is slope")
                steps.append(f"  Starting value (initial amount): {b} → this is y-intercept")
                steps.append("")
                steps.append(f"Step 2: Write equation correctly")
                steps.append(f"  Rate ({m}) goes with variable: {m}x")
                steps.append(f"  Starting value ({b}) is constant: + {b}")
                steps.append(f"  Equation: y = {m}x + {b}")
                steps.append("")
                steps.append(f"Step 3: Verify roles")
                steps.append(f"  Slope = {m} (rate per unit) ✓")
                steps.append(f"  Y-intercept = {b} (starting value) ✓")
                steps.append("")
                steps.append(f"Final Answer: {correct_answer} ✓")
                steps.append(f"  NOT {malrule_answer} (that swaps rate and starting!) ✗")

            elif word_problem_subtype == 'identify_slope':
                steps.append(f"Step 1: Identify rate of change from context")
                steps.append(f"  Context describes: rate = {m}, starting value = {b}")
                steps.append("")
                steps.append(f"Step 2: Recognize slope as rate")
                steps.append(f"  Slope = rate of change = {m} ✓")
                steps.append(f"  Starting value = {b} (this is y-intercept, not slope)")
                steps.append("")
                steps.append(f"Step 3: State slope correctly")
                steps.append(f"  The slope (rate) is {m}")
                steps.append("")
                steps.append(f"Final Answer: {correct_answer} ✓")
                steps.append(f"  NOT {malrule_answer} (that's the starting value!) ✗")

            elif word_problem_subtype == 'identify_intercept':
                steps.append(f"Step 1: Identify starting value from context")
                steps.append(f"  Context describes: rate = {m}, starting value = {b}")
                steps.append("")
                steps.append(f"Step 2: Recognize y-intercept as starting value")
                steps.append(f"  Y-intercept = starting value = {b} ✓")
                steps.append(f"  Rate = {m} (this is slope, not y-intercept)")
                steps.append("")
                steps.append(f"Step 3: State y-intercept correctly")
                steps.append(f"  The y-intercept (starting value) is {b}")
                steps.append("")
                steps.append(f"Final Answer: {correct_answer} ✓")
                steps.append(f"  NOT {malrule_answer} (that's the rate!) ✗")

        return steps
