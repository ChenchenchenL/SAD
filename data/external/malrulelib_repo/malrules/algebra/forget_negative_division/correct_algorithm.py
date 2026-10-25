"""
Correct algorithm for solving inequalities with negative coefficients.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import re
from typing import List, Tuple
from utils import CorrectAlgorithm, Problem, Solution


class InequalitySolvingCorrectAlgorithm(CorrectAlgorithm):
    """Correctly solves inequalities, flipping sign when dividing by negative."""

    def get_name(self) -> str:
        return "Correct Inequality Solving"

    def get_description(self) -> str:
        return "Correctly solves inequalities, remembering to flip sign when multiplying/dividing by negative."

    def _generate_verbose_steps(self, inequality: str, actual_template: str, parsed: Tuple,
                                 correct_sign: str, solution_value, inequality_sign: str) -> List[str]:
        """Generate verbose steps with detailed explanations."""
        steps = []
        steps.append(f"Problem: {inequality}")
        steps.append("")

        if actual_template == 'two_step':
            coefficient, added_const, rhs_const, _ = parsed
            intermediate = rhs_const - added_const

            if coefficient == -1:
                coeff_str = "-x"
            else:
                coeff_str = f"{coefficient}x"

            steps.append(f"Step 1: Subtract {added_const} from both sides")
            steps.append(f"  {coeff_str} {inequality_sign} {intermediate}")
            steps.append("")
            steps.append(f"Step 2: Divide by {coefficient}")
            steps.append(f"IMPORTANT: {coefficient} is NEGATIVE - must FLIP the inequality sign")
            steps.append(f"  x {correct_sign} {intermediate}/{coefficient}  (sign flipped!)")
            steps.append(f"  x {correct_sign} {solution_value}")
            constant_for_test = rhs_const

            steps.append("")
            steps.append("Verify with a test value:")
            if correct_sign in ['>', '≥']:
                test_value = solution_value + 1
            else:
                test_value = solution_value - 1
            test_result = coefficient * test_value + added_const
            steps.append(f"  Try x = {test_value}:")
            steps.append(f"  {coefficient} × {test_value} + {added_const} = {test_result}")
            satisfies = self._check_satisfies(test_result, constant_for_test, inequality_sign)
            steps.append(f"  Is {test_result} {inequality_sign} {constant_for_test}? {satisfies} ✓")

        elif actual_template == 'fraction_coefficient':
            numerator, denominator, constant, _ = parsed
            reciprocal = denominator / numerator

            steps.append(f"Goal: Isolate x by multiplying both sides by the reciprocal")
            steps.append("")
            steps.append(f"Coefficient is {numerator}/{denominator}")
            steps.append(f"IMPORTANT: The coefficient is NEGATIVE")
            steps.append("           When multiplying by negative, FLIP the inequality sign")
            steps.append("")
            steps.append(f"Multiply both sides by {denominator}/{numerator}:")
            steps.append(f"  x {correct_sign} {constant} × {denominator}/{numerator}  (sign flipped!)")
            steps.append(f"  x {correct_sign} {solution_value}")

        else:  # basic_one_step or word_problem
            coefficient, constant, _ = parsed

            steps.append(f"Goal: Isolate x by dividing both sides by {coefficient}")
            steps.append("")
            steps.append(f"IMPORTANT: {coefficient} is NEGATIVE")
            steps.append("           When dividing by negative, FLIP the inequality sign")
            steps.append("")
            steps.append(f"Divide both sides by {coefficient}:")
            steps.append(f"  x {correct_sign} {constant}/{coefficient}  (sign flipped!)")
            steps.append(f"  x {correct_sign} {solution_value}")
            constant_for_test = constant

            steps.append("")
            steps.append("Verify with a test value:")
            if correct_sign in ['>', '≥']:
                test_value = solution_value + 1
            else:
                test_value = solution_value - 1
            test_result = coefficient * test_value
            steps.append(f"  Try x = {test_value}:")
            steps.append(f"  {coefficient} × {test_value} = {test_result}")
            satisfies = self._check_satisfies(test_result, constant_for_test, inequality_sign)
            steps.append(f"  Is {test_result} {inequality_sign} {constant_for_test}? {satisfies} ✓")

        steps.append("")
        steps.append(f"Final Answer: x {correct_sign} {solution_value} ✓")

        return steps

    def _generate_concise_steps(self, inequality: str, actual_template: str, parsed: Tuple,
                                 correct_sign: str, solution_value, inequality_sign: str) -> List[str]:
        """Generate concise steps with only formulas and values."""
        steps = []
        steps.append(f"Solve: {inequality}")

        if actual_template == 'two_step':
            coefficient, added_const, rhs_const, _ = parsed
            intermediate = rhs_const - added_const

            if coefficient == -1:
                coeff_str = "-x"
            else:
                coeff_str = f"{coefficient}x"

            steps.append(f"{coeff_str} {inequality_sign} {intermediate}")
            steps.append(f"x {correct_sign} {solution_value}")

        elif actual_template == 'fraction_coefficient':
            numerator, denominator, constant, _ = parsed
            steps.append(f"x {correct_sign} {solution_value}")

        else:  # basic_one_step or word_problem
            coefficient, constant, _ = parsed
            steps.append(f"x {correct_sign} {solution_value}")

        return steps

    def _check_satisfies(self, test_result, constant, inequality_sign: str) -> bool:
        """Check if test result satisfies the inequality."""
        if inequality_sign == '<':
            return test_result < constant
        elif inequality_sign == '>':
            return test_result > constant
        elif inequality_sign == '≤':
            return test_result <= constant
        elif inequality_sign == '≥':
            return test_result >= constant
        return False

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

    def _flip_sign(self, sign: str) -> str:
        """Flip inequality sign."""
        flip_map = {'<': '>', '>': '<', '≤': '≥', '≥': '≤'}
        return flip_map.get(sign, sign)

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct inequality solving algorithm.

        Args:
            problem: Inequality problem
            verbose: If True, generate detailed steps; if False, generate concise steps

        Returns:
            Solution with correct steps
        """
        inequality = problem.metadata['inequality']
        template = problem.metadata.get('template', 'basic_one_step')

        # For word problems, use the embedded word_problem_type as the actual template
        if template == 'word_problem':
            actual_template = problem.metadata.get('word_problem_type', 'basic_one_step')
        else:
            actual_template = template

        # Parse the inequality to extract components
        parsed = self._parse_inequality(inequality, actual_template)

        # Calculate solution based on template
        if actual_template == 'two_step':
            coefficient, added_const, rhs_const, inequality_sign = parsed
            intermediate = rhs_const - added_const
            correct_sign = self._flip_sign(inequality_sign)
            solution_value = intermediate / coefficient

        elif actual_template == 'fraction_coefficient':
            numerator, denominator, constant, inequality_sign = parsed
            reciprocal = denominator / numerator
            correct_sign = self._flip_sign(inequality_sign)
            solution_value = constant * reciprocal

        else:  # basic_one_step or word_problem
            coefficient, constant, inequality_sign = parsed
            correct_sign = self._flip_sign(inequality_sign)
            solution_value = constant / coefficient

        # Round if close to integer
        if abs(solution_value - round(solution_value)) < 0.01:
            solution_value = int(round(solution_value))
        else:
            solution_value = round(solution_value, 2)

        # Generate steps based on verbose setting
        if verbose:
            steps = self._generate_verbose_steps(inequality, actual_template, parsed,
                                                  correct_sign, solution_value, inequality_sign)
        else:
            steps = self._generate_concise_steps(inequality, actual_template, parsed,
                                                  correct_sign, solution_value, inequality_sign)

        # Return as string representation
        result_str = f"x {correct_sign} {solution_value}"

        return Solution(
            answer=result_str,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
