"""
Change-Side-Change-Sign malrule algorithm.

Implements the systematic error of believing that moving a term
across the equals sign simply requires changing its sign.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List
import re

class ChangeSideChangeSignMalrule(Malrule):
    """
    Implements the Change-Side-Change-Sign bug.

    Students incorrectly believe that when moving a term from one side
    of an equation to the other, you simply change its sign (+ becomes -,
    - becomes +). They don't understand that you must apply the same
    operation to both sides.

    Example: x + 3 = 7 → x = 7 + 3 = 10 (WRONG! should be x = 7 - 3 = 4)

    This is called the "transition model" error and is extremely common.
    """

    def get_name(self) -> str:
        return "Change-Side-Change-Sign"

    def get_description(self) -> str:
        return (
            "Students use the 'transition model' of algebraic manipulation, incorrectly "
            "believing that moving a term across the equals sign simply requires changing "
            "its sign. They do not understand that solving equations requires applying "
            "inverse operations to both sides to maintain equality. This reflects a "
            "fundamental misunderstanding of the equals sign as a relational symbol."
        )

    def _generate_verbose_steps(self, equation: str, equation_type: str, params: dict, answer) -> List[str]:
        """Generate verbose steps with detailed explanations (original format)."""
        steps = []
        steps.append(f"Equation: {equation}")
        steps.append(f"MALRULE: Move terms across equals sign and change their sign")

        if equation_type == 'x_plus_c':
            c, result = params['c'], params['result']
            steps.append(f"Move +{c} to the right side and change sign to -{c}... wait no!")
            steps.append(f"MALRULE REASONING: When moving across =, + becomes -")
            steps.append(f"So x + {c} = {result} becomes x = {result} + {c}")
            steps.append(f"WRONG! Student changed the wrong sign!")
            steps.append(f"x = {result + c}")

        elif equation_type == 'x_minus_c':
            c, result = params['c'], params['result']
            steps.append(f"Move -{c} to the right side and change sign to +{c}... wait no!")
            steps.append(f"MALRULE REASONING: When moving across =, - becomes +")
            steps.append(f"So x - {c} = {result} becomes x = {result} - {c}")
            steps.append(f"WRONG! Student changed the wrong sign!")
            steps.append(f"x = {result - c}")

        elif equation_type == 'c_minus_x':
            c, result = params['c'], params['result']
            steps.append(f"Move {c} to right side, change sign: x = result - {c}?")
            steps.append(f"MALRULE CONFUSION: Not sure which terms to move")
            steps.append(f"Student attempts: -{c} - x = {result} - {c}?")
            steps.append(f"x = {result} - {c}")

        elif equation_type == 'two_step':
            a, b, c, sign = params['a'], params['b'], params['c'], params['sign']
            if sign == '+':
                steps.append(f"Move +{b} across and change sign")
                steps.append(f"MALRULE: {a}x = {c} + {b}")
                steps.append(f"{a}x = {c + b}")
                steps.append(f"Divide both sides by {a}")
                steps.append(f"x = {(c + b) // a}")
            else:  # sign == '-'
                steps.append(f"Move -{b} across and change sign")
                steps.append(f"MALRULE: {a}x = {c} - {b}")
                steps.append(f"{a}x = {c - b}")
                steps.append(f"Divide both sides by {a}")
                steps.append(f"x = {(c - b) // a}")

        elif equation_type == 'variables_on_both_sides':
            a, b, c, d = params['a'], params['b'], params['c'], params['d']
            sign1, sign2 = params['sign1'], params['sign2']
            b_signed = b if sign1 == '+' else -b
            d_signed = d if sign2 == '+' else -d
            steps.append(f"MALRULE: Move {c}x to left without subtracting from both sides")
            steps.append(f"Student writes: {a}x + {c}x {sign1} {b} = {d_signed}")
            steps.append(f"{a + c}x {sign1} {b} = {d_signed}")
            if sign1 == '+':
                steps.append(f"Then move +{b} to right, correctly this time")
                steps.append(f"{a + c}x = {d_signed} - {b}")
                steps.append(f"{a + c}x = {d_signed - b}")
            else:
                steps.append(f"Then move -{b} to right, correctly this time")
                steps.append(f"{a + c}x = {d_signed} + {b}")
                steps.append(f"{a + c}x = {d_signed + b}")
            steps.append(f"x = {(d_signed - b_signed) // (a + c)}")

        elif equation_type == 'negative_coefficients':
            if 'simple' in params:
                c, result = params['c'], params['result']
                sign = params['sign']
                c_signed = c if sign == '+' else -c
                if sign == '+':
                    steps.append(f"Move +{c} to right, change sign")
                    steps.append(f"-x = {result} + {c}")
                    steps.append(f"-x = {result + c}")
                else:
                    steps.append(f"Move -{c} to right, change sign")
                    steps.append(f"-x = {result} - {c}")
                    steps.append(f"-x = {result - c}")
                steps.append(f"x = {-(result + c_signed)}")
            else:
                a, b, c = params['a'], params['b'], params['c']
                sign = params['sign']
                b_signed = b if sign == '+' else -b
                if sign == '+':
                    steps.append(f"Move +{b} to right, change sign")
                    steps.append(f"-{a}x = {c} + {b}")
                else:
                    steps.append(f"Move -{b} to right, change sign")
                    steps.append(f"-{a}x = {c} - {b}")
                steps.append(f"x = {(c + b_signed) // (-a)}")

        elif equation_type == 'word_problem_context':
            if 'a' in params:
                # Two-step word problem: ax + b = c or ax - b = c
                a, b, c, sign = params['a'], params['b'], params['c'], params['sign']
                if sign == '+':
                    steps.append(f"Move +{b} across and change sign")
                    steps.append(f"MALRULE: {a}x = {c} + {b}")
                    steps.append(f"{a}x = {c + b}")
                    steps.append(f"Divide both sides by {a}")
                    steps.append(f"x = {(c + b) // a}")
                else:  # sign == '-'
                    steps.append(f"Move -{b} across and change sign")
                    steps.append(f"MALRULE: {a}x = {c} - {b}")
                    steps.append(f"{a}x = {c - b}")
                    steps.append(f"Divide both sides by {a}")
                    steps.append(f"x = {(c - b) // a}")
            else:
                # Simple word problem: x + c = result or x - c = result
                c, result, sign = params['c'], params['result'], params['sign']
                if sign == '+':
                    steps.append(f"MALRULE: Move +{c} across, change sign")
                    steps.append(f"x = {result} + {c}")
                    steps.append(f"x = {result + c}")
                else:  # sign == '-'
                    steps.append(f"MALRULE: Move -{c} across, change sign")
                    steps.append(f"x = {result} - {c}")
                    steps.append(f"x = {result - c}")

        elif equation_type == 'three_step_equation':
            coeff, a, b, result = params['coeff'], params['a'], params['b'], params['result']
            steps.append(f"MALRULE: Move +{a} and -{b} across, change signs")
            steps.append(f"{coeff}x = {result} + {a} - {b}")
            steps.append(f"{coeff}x = {result + a - b}")
            steps.append(f"x = {(result + a - b) // coeff}")

        steps.append(f"\nFinal answer: x = {answer} (INCORRECT - used change-side-change-sign)")

        return steps

    def _generate_concise_steps(self, problem_text: str, equation: str, equation_type: str, params: dict, answer) -> List[str]:
        """Generate concise steps with only formulas and values."""
        steps = []
        steps.append(problem_text)

        if equation_type == 'x_plus_c':
            c, result = params['c'], params['result']
            steps.append(f"x + {c} = {result}")
            steps.append(f"x = {result} + {c}")
            steps.append(f"x = {result + c}")

        elif equation_type == 'x_minus_c':
            c, result = params['c'], params['result']
            steps.append(f"x - {c} = {result}")
            steps.append(f"x = {result} - {c}")
            steps.append(f"x = {result - c}")

        elif equation_type == 'c_minus_x':
            c, result = params['c'], params['result']
            steps.append(f"{c} - x = {result}")
            steps.append(f"x = {result} - {c}")

        elif equation_type == 'two_step':
            a, b, c, sign = params['a'], params['b'], params['c'], params['sign']
            if sign == '+':
                steps.append(f"{a}x + {b} = {c}")
                steps.append(f"{a}x = {c} + {b}")
                steps.append(f"{a}x = {c + b}")
                steps.append(f"x = {(c + b) // a}")
            else:  # sign == '-'
                steps.append(f"{a}x - {b} = {c}")
                steps.append(f"{a}x = {c} - {b}")
                steps.append(f"{a}x = {c - b}")
                steps.append(f"x = {(c - b) // a}")

        elif equation_type == 'variables_on_both_sides':
            a, b, c, d = params['a'], params['b'], params['c'], params['d']
            sign1, sign2 = params['sign1'], params['sign2']
            b_signed = b if sign1 == '+' else -b
            d_signed = d if sign2 == '+' else -d
            steps.append(f"{a}x {sign1} {b} = {c}x {sign2} {d}")
            steps.append(f"{a}x + {c}x {sign1} {b} = {d_signed}")
            steps.append(f"{a + c}x {sign1} {b} = {d_signed}")
            steps.append(f"{a + c}x = {d_signed - b_signed}")
            steps.append(f"x = {(d_signed - b_signed) // (a + c)}")

        elif equation_type == 'negative_coefficients':
            if 'simple' in params:
                c, result = params['c'], params['result']
                sign = params['sign']
                c_signed = c if sign == '+' else -c
                steps.append(f"-x {sign} {c} = {result}")
                if sign == '+':
                    steps.append(f"-x = {result} + {c}")
                else:
                    steps.append(f"-x = {result} - {c}")
                steps.append(f"x = {-(result + c_signed)}")
            else:
                a, b, c = params['a'], params['b'], params['c']
                sign = params['sign']
                b_signed = b if sign == '+' else -b
                steps.append(f"-{a}x {sign} {b} = {c}")
                if sign == '+':
                    steps.append(f"-{a}x = {c} + {b}")
                else:
                    steps.append(f"-{a}x = {c} - {b}")
                steps.append(f"x = {(c + b_signed) // (-a)}")

        elif equation_type == 'word_problem_context':
            if 'a' in params:
                # Two-step word problem: ax + b = c or ax - b = c
                a, b, c, sign = params['a'], params['b'], params['c'], params['sign']
                if sign == '+':
                    steps.append(f"Equation: {a}x + {b} = {c}")
                    steps.append(f"{a}x = {c} + {b}")
                    steps.append(f"{a}x = {c + b}")
                    steps.append(f"x = {(c + b) // a}")
                else:  # sign == '-'
                    steps.append(f"Equation: {a}x - {b} = {c}")
                    steps.append(f"{a}x = {c} - {b}")
                    steps.append(f"{a}x = {c - b}")
                    steps.append(f"x = {(c - b) // a}")
            else:
                # Simple word problem: x + c = result or x - c = result
                c, result, sign = params['c'], params['result'], params['sign']
                if sign == '+':
                    steps.append(f"Equation: x + {c} = {result}")
                    steps.append(f"x = {result} + {c}")
                    steps.append(f"x = {result + c}")
                else:  # sign == '-'
                    steps.append(f"Equation: x - {c} = {result}")
                    steps.append(f"x = {result} - {c}")
                    steps.append(f"x = {result - c}")

        elif equation_type == 'three_step_equation':
            coeff, a, b, result = params['coeff'], params['a'], params['b'], params['result']
            steps.append(f"{coeff}x + {a} - {b} = {result}")
            steps.append(f"{coeff}x = {result} + {a} - {b}")
            steps.append(f"{coeff}x = {result + a - b}")
            steps.append(f"x = {(result + a - b) // coeff}")

        return steps

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        equation = problem.metadata['equation']
        equation_type = problem.metadata['equation_type']

        if equation_type == 'x_plus_c':
            # x + c = result → malrule: x = result + c (wrong!)
            match = re.match(r'x \+ (\d+) = (\d+)', equation)
            c = int(match.group(1))
            result = int(match.group(2))
            return result + c
        elif equation_type == 'x_minus_c':
            # x - c = result → malrule: x = result - c (wrong!)
            match = re.match(r'x - (\d+) = (-?\d+)', equation)
            c = int(match.group(1))
            result = int(match.group(2))
            return result - c
        elif equation_type == 'c_minus_x':
            # c - x = result → malrule: x = result - c (confused)
            match = re.match(r'(\d+) - x = (\d+)', equation)
            c = int(match.group(1))
            result = int(match.group(2))
            return result - c
        elif equation_type == 'two_step':
            # ax + b = c → malrule: ax = c + b, x = (c + b) / a (wrong!)
            match = re.match(r'(\d+)x \+ (\d+) = (\d+)', equation)
            a = int(match.group(1))
            b = int(match.group(2))
            c = int(match.group(3))
            return (c + b) // a
        else:
            # No fallback - all equation types should be handled above
            raise ValueError(
                f"Unsupported equation_type '{equation_type}' in calculate_expected_answer. "
                f"All equation types should be explicitly implemented."
            )

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Change-Side-Change-Sign malrule.

        Args:
            problem: Linear equation problem
            verbose: If True, generate verbose steps; otherwise generate concise steps

        Returns:
            Solution with incorrect sign-change procedure
        """
        equation = problem.metadata['equation']
        equation_type = problem.metadata['equation_type']

        # Parse equation and calculate answer
        params = {}
        answer = None

        if equation_type == 'x_plus_c':
            match = re.match(r'x \+ (\d+) = (\d+)', equation)
            c = int(match.group(1))
            result = int(match.group(2))
            params = {'c': c, 'result': result}
            answer = result + c

        elif equation_type == 'x_minus_c':
            match = re.match(r'x - (\d+) = (-?\d+)', equation)
            c = int(match.group(1))
            result = int(match.group(2))
            params = {'c': c, 'result': result}
            answer = result - c

        elif equation_type == 'c_minus_x':
            match = re.match(r'(\d+) - x = (\d+)', equation)
            c = int(match.group(1))
            result = int(match.group(2))
            params = {'c': c, 'result': result}
            answer = result - c

        elif equation_type == 'two_step':
            match = re.match(r'(\d+)x ([+-]) (\d+) = (-?\d+)', equation)
            a = int(match.group(1))
            sign = match.group(2)
            b = int(match.group(3))
            c = int(match.group(4))
            params = {'a': a, 'b': b, 'c': c, 'sign': sign}
            # Malrule: incorrectly change sign when moving term
            if sign == '+':
                answer = (c + b) // a  # Wrong: should be (c - b) // a
            else:  # sign == '-'
                answer = (c - b) // a  # Wrong: should be (c + b) // a

        elif equation_type == 'variables_on_both_sides':
            match = re.match(r'(\d+)?x ([+-]) (\d+) = (\d+)?x ([+-]) (\d+)', equation)
            a = int(match.group(1)) if match.group(1) else 1
            sign1 = match.group(2)
            b = int(match.group(3))
            c = int(match.group(4)) if match.group(4) else 1
            sign2 = match.group(5)
            d = int(match.group(6))
            # Convert signs to multipliers
            b_signed = b if sign1 == '+' else -b
            d_signed = d if sign2 == '+' else -d
            params = {'a': a, 'b': b, 'c': c, 'd': d, 'sign1': sign1, 'sign2': sign2}
            # Malrule: adds coefficient instead of subtracting when moving x terms
            answer = (d_signed - b_signed) // (a + c)

        elif equation_type == 'negative_coefficients':
            if equation.startswith('-x'):
                match = re.match(r'-x ([+-]) (\d+) = (-?\d+)', equation)
                sign = match.group(1)
                c = int(match.group(2))
                result = int(match.group(3))
                # Malrule: incorrectly changes sign when moving
                c_signed = c if sign == '+' else -c
                params = {'c': c, 'result': result, 'simple': True, 'sign': sign}
                # Malrule: changes + to - or - to + when moving
                answer = -(result + c_signed)  # Wrong application of sign change
            else:
                match = re.match(r'-(\d+)x ([+-]) (\d+) = (-?\d+)', equation)
                a = int(match.group(1))
                sign = match.group(2)
                b = int(match.group(3))
                c = int(match.group(4))
                b_signed = b if sign == '+' else -b
                params = {'a': a, 'b': b, 'c': c, 'sign': sign}
                # Malrule: changes + to - or - to + when moving
                answer = (c + b_signed) // (-a)  # Wrong application of sign change

        elif equation_type == 'word_problem_context':
            # Check if it's a two-step equation first (ax + b = c or ax - b = c)
            two_step_match = re.match(r'(\d+)x ([+-]) (\d+) = (-?\d+)', equation)
            if two_step_match:
                a = int(two_step_match.group(1))
                sign = two_step_match.group(2)
                b = int(two_step_match.group(3))
                c = int(two_step_match.group(4))
                params = {'a': a, 'b': b, 'c': c, 'sign': sign}
                # Malrule: incorrectly change sign when moving term
                if sign == '+':
                    answer = (c + b) // a  # Wrong: should be (c - b) // a
                else:  # sign == '-'
                    answer = (c - b) // a  # Wrong: should be (c + b) // a
            else:
                # Simple equation: x + c = result or x - c = result
                match = re.match(r'x ([+-]) (\d+) = (-?\d+)', equation)
                sign = match.group(1)
                c = int(match.group(2))
                result = int(match.group(3))
                params = {'c': c, 'result': result, 'sign': sign}
                # Malrule: incorrectly change sign when moving term
                if sign == '+':
                    answer = result + c  # Wrong: should be result - c
                else:  # sign == '-'
                    answer = result - c  # Wrong: should be result + c

        elif equation_type == 'three_step_equation':
            match = re.match(r'(\d+)x \+ (\d+) - (\d+) = (\d+)', equation)
            coeff = int(match.group(1))
            a = int(match.group(2))
            b = int(match.group(3))
            result = int(match.group(4))
            params = {'coeff': coeff, 'a': a, 'b': b, 'result': result}
            answer = (result + a - b) // coeff

        else:
            raise ValueError(
                f"Unsupported equation_type '{equation_type}' for equation '{equation}'. "
                f"All equation types should be explicitly implemented."
            )

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(equation, equation_type, params, answer)
        else:
            steps = self._generate_concise_steps(problem.text, equation, equation_type, params, answer)

        return Solution(
            answer=answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
