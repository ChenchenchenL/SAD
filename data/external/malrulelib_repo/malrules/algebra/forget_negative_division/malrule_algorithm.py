"""
Malrule algorithm for Forget-Negative-Division error.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import re
from typing import Dict, List, Any, Tuple
from utils import Malrule, Problem, Solution

class ForgetNegativeDivisionMalrule(Malrule):
    """
    Students forget to flip inequality sign when dividing/multiplying by negative.

    Example: -2x < 6 → Student divides by -2: x < -3 (WRONG, should be x > -3)
    """

    def get_name(self) -> str:
        return "Forget-Negative-Division"

    def get_description(self) -> str:
        return (
            "Students neglect the crucial rule that multiplying or dividing an inequality "
            "by a negative coefficient reverses the direction of the inequality sign. "
            "They mistakenly equate the process of solving inequalities with equations, "
            "treating them as identical procedures."
        )

    def _generate_verbose_steps(self, inequality: str, actual_template: str, parsed: Tuple,
                                 malrule_sign: str, solution_value) -> List[str]:
        """Generate verbose steps with detailed explanations."""
        steps = []
        steps.append(f"Problem: {inequality}")
        steps.append("")

        if actual_template == 'two_step':
            coefficient, added_const, rhs_const, inequality_sign = parsed
            intermediate = rhs_const - added_const

            if coefficient == -1:
                coeff_str = "-x"
            else:
                coeff_str = f"{coefficient}x"

            steps.append("MALRULE: Solve step by step, but forget to flip sign when dividing by negative")
            steps.append(f"Step 1: Subtract {added_const} from both sides")
            steps.append(f"  {coeff_str} {inequality_sign} {intermediate}")
            steps.append("")
            steps.append(f"Step 2: Divide by {coefficient}")
            steps.append(f"  MALRULE: 'Just divide like normal equation, don't flip sign'")
            steps.append(f"  x {malrule_sign} {intermediate}/{coefficient}")
            steps.append(f"  x {malrule_sign} {solution_value}")

        elif actual_template == 'fraction_coefficient':
            numerator, denominator, constant, inequality_sign = parsed

            steps.append("MALRULE: Multiply by reciprocal (forget to flip sign)")
            steps.append(f"  MALRULE REASONING: 'Just multiply like normal equation'")
            steps.append("")
            steps.append(f"Multiply both sides by {denominator}/{numerator}:")
            steps.append(f"  x {malrule_sign} {constant} × {denominator}/{numerator}")
            steps.append(f"  x {malrule_sign} {solution_value}")

        else:  # basic_one_step or word_problem
            coefficient, constant, inequality_sign = parsed

            steps.append("MALRULE: Divide by coefficient (forget to flip sign)")
            steps.append(f"  MALRULE REASONING: 'Just divide like normal equation'")
            steps.append("")
            steps.append(f"Divide both sides by {coefficient}:")
            steps.append(f"  x {malrule_sign} {constant}/{coefficient}")
            steps.append(f"  x {malrule_sign} {solution_value}")

        steps.append("")
        steps.append(f"Final Answer: x {malrule_sign} {solution_value} (INCORRECT - forgot to flip sign!)")
        steps.append("")
        steps.append(f"Error: When dividing by NEGATIVE, must FLIP the inequality sign!")

        return steps

    def _generate_concise_steps(self, inequality: str, actual_template: str, parsed: Tuple,
                                 malrule_sign: str, solution_value) -> List[str]:
        """Generate concise steps with only formulas and values."""
        steps = []
        steps.append(f"Solve: {inequality}")

        if actual_template == 'two_step':
            coefficient, added_const, rhs_const, inequality_sign = parsed
            intermediate = rhs_const - added_const

            if coefficient == -1:
                coeff_str = "-x"
            else:
                coeff_str = f"{coefficient}x"

            steps.append(f"{coeff_str} {inequality_sign} {intermediate}")
            steps.append(f"x {malrule_sign} {solution_value}")

        elif actual_template == 'fraction_coefficient':
            numerator, denominator, constant, inequality_sign = parsed
            steps.append(f"x {malrule_sign} {solution_value}")

        else:  # basic_one_step or word_problem
            coefficient, constant, inequality_sign = parsed
            steps.append(f"x {malrule_sign} {solution_value}")

        return steps

    def _parse_inequality(self, inequality_str: str, template: str) -> Tuple:
        """Parse inequality string to extract components."""
        inequality_str = inequality_str.strip()

        # Extract inequality sign
        inequality_sign = None
        for sign in ['≤', '≥', '<', '>']:
            if sign in inequality_str:
                inequality_sign = sign
                break

        if not inequality_sign:
            raise ValueError(f"No inequality sign found in: {inequality_str}")

        # Split by inequality sign
        left, right = inequality_str.split(inequality_sign)
        left = left.strip()
        right = right.strip()

        # Parse right side (constant)
        rhs_constant = float(right) if '.' in right else int(right)

        # Parse left side based on template
        if template == 'two_step':
            # Format: -3x + 5 or -3x - 5
            match = re.match(r'([+-]?\d*)x\s*([+-])\s*(\d+)', left)
            if match:
                coef_str = match.group(1)
                if coef_str == '' or coef_str == '+':
                    coefficient = 1
                elif coef_str == '-':
                    coefficient = -1
                else:
                    coefficient = int(coef_str)

                sign = match.group(2)
                added_const = int(match.group(3))
                if sign == '-':
                    added_const = -added_const

                return coefficient, added_const, rhs_constant, inequality_sign

        elif template == 'fraction_coefficient':
            # Format: -1/2x or -1/3x
            match = re.match(r'([+-]?\d+)/(\d+)x', left)
            if match:
                numerator = int(match.group(1))
                denominator = int(match.group(2))
                return numerator, denominator, rhs_constant, inequality_sign

        # Default: basic_one_step format: -2x or -3x
        match = re.match(r'([+-]?\d*)x', left)
        if match:
            coef_str = match.group(1)
            if coef_str == '' or coef_str == '+':
                coefficient = 1
            elif coef_str == '-':
                coefficient = -1
            else:
                coefficient = int(coef_str)
            return coefficient, rhs_constant, inequality_sign

        raise ValueError(f"Cannot parse inequality: {inequality_str}")

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        inequality = problem.metadata['inequality']
        template = problem.metadata.get('template', 'basic_one_step')

        # Parse to get values
        parsed = self._parse_inequality(inequality, template)

        if template == 'two_step':
            coefficient, added_const, rhs_const, inequality_sign = parsed
            intermediate = rhs_const - added_const
            solution_value = intermediate / coefficient
        elif template == 'fraction_coefficient':
            numerator, denominator, constant, inequality_sign = parsed
            reciprocal = denominator / numerator
            solution_value = constant * reciprocal
        else:
            coefficient, constant, inequality_sign = parsed
            solution_value = constant / coefficient

        # Round if close to integer
        if abs(solution_value - round(solution_value)) < 0.01:
            solution_value = int(round(solution_value))
        else:
            solution_value = round(solution_value, 2)

        # Malrule: DON'T flip sign when dividing by negative
        malrule_sign = inequality_sign
        return f"x {malrule_sign} {solution_value}"

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Forget-Negative-Division malrule.

        Args:
            problem: Inequality problem
            verbose: If True, generate detailed steps; if False, generate concise steps

        Returns:
            Solution with incorrect (non-flipped) inequality sign
        """
        inequality = problem.metadata['inequality']
        template = problem.metadata.get('template', 'basic_one_step')

        # For word problems, use the embedded word_problem_type as the actual template
        if template == 'word_problem':
            actual_template = problem.metadata.get('word_problem_type', 'basic_one_step')
        else:
            actual_template = template

        # Parse the inequality
        parsed = self._parse_inequality(inequality, actual_template)

        # Calculate solution based on template
        if actual_template == 'two_step':
            coefficient, added_const, rhs_const, inequality_sign = parsed
            intermediate = rhs_const - added_const
            solution_value = intermediate / coefficient
            malrule_sign = inequality_sign  # DON'T flip (that's the error)

        elif actual_template == 'fraction_coefficient':
            numerator, denominator, constant, inequality_sign = parsed
            reciprocal = denominator / numerator
            solution_value = constant * reciprocal
            malrule_sign = inequality_sign  # DON'T flip

        else:  # basic_one_step or word_problem
            coefficient, constant, inequality_sign = parsed
            solution_value = constant / coefficient
            malrule_sign = inequality_sign  # DON'T flip

        # Round if close to integer
        if abs(solution_value - round(solution_value)) < 0.01:
            solution_value = int(round(solution_value))
        else:
            solution_value = round(solution_value, 2)

        # Generate steps based on verbose setting
        if verbose:
            steps = self._generate_verbose_steps(inequality, actual_template, parsed,
                                                  malrule_sign, solution_value)
        else:
            steps = self._generate_concise_steps(inequality, actual_template, parsed,
                                                  malrule_sign, solution_value)

        # Return as string representation
        result_str = f"x {malrule_sign} {solution_value}"

        return Solution(
            answer=result_str,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
