"""
Malrule algorithm for Confuse-Slope-And-Intercept-Roles error.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class ConfuseSlopeAndInterceptRolesMalrule(Malrule):
    """
    Students swap the roles of slope (m) and y-intercept (b) in y = mx + b.
    They don't understand that m is the coefficient of x and b is the constant term.

    Example 1: Slope = 3, y-intercept = 5
    Student: y = 5x + 3 (WRONG! - swapped m and b)
    Correct: y = 3x + 5

    Example 2: What is the slope of y = 2x + 7?
    Student: slope = 7 (WRONG! - identified b instead of m)
    Correct: slope = 2
    """

    def get_name(self) -> str:
        return "Confuse-Slope-And-Intercept-Roles"

    def get_description(self) -> str:
        return (
            "Student swaps the roles of slope (m) and y-intercept (b) in y = mx + b, "
            "either writing equations with parameters reversed or identifying the constant "
            "term as slope and the coefficient as y-intercept. This reflects confusion about "
            "the distinct structural roles of coefficient and constant in function notation."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Malrule: swap slope and y-intercept roles
        template = problem.metadata.get('template', problem.metadata.get('problem_type', ''))
        m = problem.metadata['slope']
        b = problem.metadata['y_intercept']

        if template in ['write_equation', 'word_problem_context']:
            # Format equation with swapped roles: y = bx + m
            return self._format_equation(b, m)
        elif template in ['identify_slope', 'standard_form_identify']:
            # Student confuses slope with y-intercept
            return str(b)
        elif template == 'identify_y_intercept':
            # Student confuses y-intercept with slope
            return str(m)
        else:
            # Fallback
            return str(b)

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply malrule across all templates."""
        template = problem.metadata.get('template', problem.metadata['problem_type'])
        m = problem.metadata['slope']
        b = problem.metadata['y_intercept']

        # COMPUTE malrule answer by swapping roles
        if template in ['write_equation', 'word_problem_context']:
            # Format equation with swapped roles: y = bx + m
            malrule_answer = self._format_equation(b, m)
        elif template in ['identify_slope', 'standard_form_identify']:
            # Student confuses slope with y-intercept
            malrule_answer = str(b)
        elif template == 'identify_y_intercept':
            # Student confuses y-intercept with slope
            malrule_answer = str(m)
        else:
            # Fallback
            malrule_answer = str(b)

        # Generate steps based on verbosity setting
        if verbose:
            steps = self._generate_verbose_steps(problem, template, m, b, malrule_answer)
        else:
            steps = self._generate_concise_steps(problem, template, m, b, malrule_answer)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
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

    def _generate_concise_steps(self, problem: Problem, template: str, m: int, b: int, malrule_answer: str) -> List[str]:
        """Generate concise steps with only formula and values."""
        steps = []
        steps.append(f"Question: {problem.text}")

        if template == 'write_equation':
            steps.append(f"Formula: y = mx + b")
            steps.append(f"Given: slope (m) = {m}, y-intercept (b) = {b}")
            steps.append(f"y = {b}x + {m}")
            steps.append(f"Answer: {malrule_answer}")

        elif template == 'identify_slope':
            equation = problem.metadata['equation']
            steps.append(f"Given equation: {equation}")
            steps.append(f"Form: y = mx + b")
            steps.append(f"Slope = constant term = {b}")
            steps.append(f"Answer: {malrule_answer}")

        elif template == 'identify_y_intercept':
            equation = problem.metadata['equation']
            steps.append(f"Given equation: {equation}")
            steps.append(f"Form: y = mx + b")
            steps.append(f"Y-intercept = coefficient of x = {m}")
            steps.append(f"Answer: {malrule_answer}")

        elif template == 'standard_form_identify':
            equation = problem.metadata['equation']
            A = problem.metadata['A']
            B = problem.metadata['B']
            C = problem.metadata['C']
            steps.append(f"Given equation: {equation}")
            steps.append(f"Convert: y = {m}x + {b}")
            steps.append(f"Slope = y-intercept = {b}")
            steps.append(f"Answer: {malrule_answer}")

        elif template == 'word_problem_context':
            word_problem_subtype = problem.metadata.get('word_problem_subtype', 'write_equation')

            if word_problem_subtype == 'write_equation':
                steps.append(f"Extract: rate = {m}, starting value = {b}")
                steps.append(f"Formula: y = mx + b")
                steps.append(f"Substitute: y = {b}x + {m}")
                steps.append(f"Answer: {malrule_answer}")

            elif word_problem_subtype == 'identify_slope':
                steps.append(f"Extract: rate = {m}, starting value = {b}")
                steps.append(f"Slope = starting value = {b}")
                steps.append(f"Answer: {malrule_answer}")

            elif word_problem_subtype == 'identify_intercept':
                steps.append(f"Extract: rate = {m}, starting value = {b}")
                steps.append(f"Y-intercept = rate = {m}")
                steps.append(f"Answer: {malrule_answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, template: str, m: int, b: int, malrule_answer: str) -> List[str]:
        """Generate verbose steps with full explanations."""
        steps = []
        steps.append(f"Problem: {problem.text[:100]}...")
        steps.append("")
        steps.append("MALRULE: Student SWAPS the roles of slope and y-intercept")
        steps.append(f"  MALRULE REASONING: 'Confuses which value goes where'")
        steps.append("")

        if template == 'write_equation':
            steps.append(f"Step 1: Recall formula y = mx + b")
            steps.append(f"  Given: slope = {m}, y-intercept = {b}")
            steps.append("")
            steps.append(f"Step 2: Substitute values - IN WRONG PLACES!")
            steps.append(f"  MALRULE THINKING: 'Put y-intercept ({b}) with x'")
            steps.append(f"                    'Put slope ({m}) as constant'")
            steps.append(f"  Student writes: y = {b}x + {m} [SWAPPED!]")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT - roles swapped!)")
            steps.append(f"  ERROR: m={m} should be with x, b={b} should be constant")

        elif template == 'identify_slope':
            equation = problem.metadata['equation']
            steps.append(f"Step 1: Look at equation")
            steps.append(f"  Given: {equation}")
            steps.append("")
            steps.append(f"Step 2: Identify parts (INCORRECTLY!)")
            steps.append(f"  Coefficient of x: {m}")
            steps.append(f"  Constant term: {b}")
            steps.append(f"  MALRULE: 'Slope is the constant, so {b}' [WRONG!]")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT - that's y-intercept!)")
            steps.append(f"  ERROR: Slope is coefficient of x = {m}, not {b}")

        elif template == 'identify_y_intercept':
            equation = problem.metadata['equation']
            steps.append(f"Step 1: Look at equation")
            steps.append(f"  Given: {equation}")
            steps.append("")
            steps.append(f"Step 2: Identify parts (INCORRECTLY!)")
            steps.append(f"  Coefficient of x: {m}")
            steps.append(f"  Constant term: {b}")
            steps.append(f"  MALRULE: 'Y-intercept is coefficient of x, so {m}' [WRONG!]")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT - that's slope!)")
            steps.append(f"  ERROR: Y-intercept is constant = {b}, not {m}")

        elif template == 'standard_form_identify':
            equation = problem.metadata['equation']
            A = problem.metadata['A']
            B = problem.metadata['B']
            C = problem.metadata['C']
            steps.append(f"Step 1: Convert standard form to slope-intercept")
            steps.append(f"  Given: {equation}")
            steps.append(f"  Solve for y: y = -{A}/{B}x + {C}/{B}")
            steps.append(f"  This gives: y = {m}x + {b}")
            steps.append("")
            steps.append(f"Step 2: Identify slope (INCORRECTLY!)")
            steps.append(f"  MALRULE: Student confuses constant with slope")
            steps.append(f"  Student says: slope = {b} [WRONG - that's y-intercept!]")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT - swapped roles!)")
            steps.append(f"  ERROR: Slope is {m}, not {b}")

        elif template == 'word_problem_context':
            word_problem_subtype = problem.metadata.get('word_problem_subtype', 'write_equation')

            if word_problem_subtype == 'write_equation':
                steps.append(f"Step 1: Identify rate and starting value")
                steps.append(f"  Rate (change per unit): {m}")
                steps.append(f"  Starting value (initial amount): {b}")
                steps.append("")
                steps.append(f"Step 2: Write equation (INCORRECTLY!)")
                steps.append(f"  MALRULE: Student swaps roles")
                steps.append(f"  Puts starting value ({b}) with variable: {b}x")
                steps.append(f"  Puts rate ({m}) as constant: + {m}")
                steps.append(f"  Student writes: y = {b}x + {m} [SWAPPED!]")
                steps.append("")
                steps.append(f"Final Answer: {malrule_answer} (INCORRECT - roles swapped!)")
                steps.append(f"  ERROR: Rate ({m}) should be with x, starting ({b}) should be constant")

            elif word_problem_subtype == 'identify_slope':
                steps.append(f"Step 1: Read context")
                steps.append(f"  Context describes: rate = {m}, starting value = {b}")
                steps.append("")
                steps.append(f"Step 2: Identify slope (INCORRECTLY!)")
                steps.append(f"  MALRULE: Student confuses slope with starting value")
                steps.append(f"  Student thinks: 'Slope is the starting value'")
                steps.append(f"  Student answers: {b} [WRONG!]")
                steps.append("")
                steps.append(f"Final Answer: {malrule_answer} (INCORRECT - that's the starting value!)")
                steps.append(f"  ERROR: Slope is the rate ({m}), not the starting value ({b})")

            elif word_problem_subtype == 'identify_intercept':
                steps.append(f"Step 1: Read context")
                steps.append(f"  Context describes: rate = {m}, starting value = {b}")
                steps.append("")
                steps.append(f"Step 2: Identify y-intercept (INCORRECTLY!)")
                steps.append(f"  MALRULE: Student confuses y-intercept with rate")
                steps.append(f"  Student thinks: 'Y-intercept is the rate'")
                steps.append(f"  Student answers: {m} [WRONG!]")
                steps.append("")
                steps.append(f"Final Answer: {malrule_answer} (INCORRECT - that's the rate!)")
                steps.append(f"  ERROR: Y-intercept is the starting value ({b}), not the rate ({m})")

        return steps
