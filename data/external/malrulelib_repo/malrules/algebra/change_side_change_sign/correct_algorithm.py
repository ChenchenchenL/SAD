"""
Correct linear equation solving algorithm.

Implements proper equation solving by maintaining equality through
inverse operations.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import CorrectAlgorithm, Problem, Solution
import re


class LinearEquationCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for solving linear equations.

    Uses proper inverse operations to maintain equality.
    """

    def get_name(self) -> str:
        return "Correct Linear Equation Solving"

    def get_description(self) -> str:
        return (
            "Solves linear equations correctly by applying inverse operations "
            "to both sides of the equation to maintain equality. "
            "To move x + 3 = 7, subtract 3 from BOTH sides: x = 7 - 3 = 4."
        )

    def _generate_verbose_steps(self, equation: str, equation_type: str, params: dict, answer) -> list:
        """Generate verbose steps with detailed explanations (original format)."""
        steps = []
        steps.append(f"Equation: {equation}")
        steps.append(f"Goal: Isolate x by applying inverse operations to BOTH sides")

        if equation_type == 'x_plus_c':
            c, result = params['c'], params['result']
            steps.append(f"Step 1: Subtract {c} from BOTH sides")
            steps.append(f"x + {c} - {c} = {result} - {c}")
            steps.append(f"x = {result - c}")

        elif equation_type == 'x_minus_c':
            c, result = params['c'], params['result']
            steps.append(f"Step 1: Add {c} to BOTH sides")
            steps.append(f"x - {c} + {c} = {result} + {c}")
            steps.append(f"x = {result + c}")

        elif equation_type == 'c_minus_x':
            c, result = params['c'], params['result']
            steps.append(f"Step 1: Subtract {c} from BOTH sides")
            steps.append(f"{c} - x - {c} = {result} - {c}")
            steps.append(f"-x = {result - c}")
            steps.append(f"Step 2: Multiply BOTH sides by -1")
            steps.append(f"x = {c - result}")

        elif equation_type == 'two_step':
            a, b, c, sign = params['a'], params['b'], params['c'], params['sign']
            if sign == '+':
                steps.append(f"Step 1: Subtract {b} from BOTH sides")
                steps.append(f"{a}x + {b} - {b} = {c} - {b}")
                steps.append(f"{a}x = {c - b}")
                steps.append(f"Step 2: Divide BOTH sides by {a}")
                steps.append(f"x = {(c - b) // a}")
            else:  # sign == '-'
                steps.append(f"Step 1: Add {b} to BOTH sides")
                steps.append(f"{a}x - {b} + {b} = {c} + {b}")
                steps.append(f"{a}x = {c + b}")
                steps.append(f"Step 2: Divide BOTH sides by {a}")
                steps.append(f"x = {(c + b) // a}")

        elif equation_type == 'variables_on_both_sides':
            a, b, c, d = params['a'], params['b'], params['c'], params['d']
            sign1, sign2 = params['sign1'], params['sign2']
            b_signed = b if sign1 == '+' else -b
            d_signed = d if sign2 == '+' else -d
            steps.append(f"Step 1: Subtract {c}x from BOTH sides")
            steps.append(f"{a}x - {c}x {sign1} {b} = {c}x - {c}x {sign2} {d}")
            steps.append(f"{a - c}x {sign1} {b} = {d_signed}")
            if sign1 == '+':
                steps.append(f"Step 2: Subtract {b} from BOTH sides")
                steps.append(f"{a - c}x = {d_signed - b}")
            else:
                steps.append(f"Step 2: Add {b} to BOTH sides")
                steps.append(f"{a - c}x = {d_signed + b}")
            steps.append(f"Step 3: Divide BOTH sides by {a - c}")
            steps.append(f"x = {answer}")

        elif equation_type == 'negative_coefficients':
            if 'simple' in params:
                c, result = params['c'], params['result']
                sign = params['sign']
                c_signed = c if sign == '+' else -c
                if sign == '+':
                    steps.append(f"Step 1: Subtract {c} from BOTH sides")
                    steps.append(f"-x + {c} - {c} = {result} - {c}")
                else:
                    steps.append(f"Step 1: Add {c} to BOTH sides")
                    steps.append(f"-x - {c} + {c} = {result} + {c}")
                steps.append(f"-x = {result - c_signed}")
                steps.append(f"Step 2: Multiply BOTH sides by -1")
                steps.append(f"x = {answer}")
            else:
                a, b, c = params['a'], params['b'], params['c']
                sign = params['sign']
                b_signed = b if sign == '+' else -b
                if sign == '+':
                    steps.append(f"Step 1: Subtract {b} from BOTH sides")
                    steps.append(f"-{a}x + {b} - {b} = {c} - {b}")
                    steps.append(f"-{a}x = {c - b}")
                else:
                    steps.append(f"Step 1: Add {b} to BOTH sides")
                    steps.append(f"-{a}x - {b} + {b} = {c} + {b}")
                    steps.append(f"-{a}x = {c + b}")
                steps.append(f"Step 2: Divide BOTH sides by -{a}")
                steps.append(f"x = {answer}")

        elif equation_type == 'word_problem_context':
            if 'a' in params:
                # Two-step word problem: ax + b = c or ax - b = c
                a, b, c, sign = params['a'], params['b'], params['c'], params['sign']
                if sign == '+':
                    steps.append(f"Step 1: Subtract {b} from BOTH sides")
                    steps.append(f"{a}x + {b} - {b} = {c} - {b}")
                    steps.append(f"{a}x = {c - b}")
                    steps.append(f"Step 2: Divide BOTH sides by {a}")
                    steps.append(f"x = {(c - b) // a}")
                else:  # sign == '-'
                    steps.append(f"Step 1: Add {b} to BOTH sides")
                    steps.append(f"{a}x - {b} + {b} = {c} + {b}")
                    steps.append(f"{a}x = {c + b}")
                    steps.append(f"Step 2: Divide BOTH sides by {a}")
                    steps.append(f"x = {(c + b) // a}")
            else:
                # Simple word problem: x + c = result or x - c = result
                c, result, sign = params['c'], params['result'], params['sign']
                if sign == '+':
                    steps.append(f"Step 1: Subtract {c} from BOTH sides")
                    steps.append(f"x + {c} - {c} = {result} - {c}")
                    steps.append(f"x = {result - c}")
                else:  # sign == '-'
                    steps.append(f"Step 1: Add {c} to BOTH sides")
                    steps.append(f"x - {c} + {c} = {result} + {c}")
                    steps.append(f"x = {result + c}")

        elif equation_type == 'three_step_equation':
            coeff, a, b, result = params['coeff'], params['a'], params['b'], params['result']
            steps.append(f"Step 1: Simplify left side: {a} - {b} = {a - b}")
            steps.append(f"{coeff}x + {a - b} = {result}")
            steps.append(f"Step 2: Subtract {a - b} from BOTH sides")
            steps.append(f"{coeff}x = {result - (a - b)}")
            steps.append(f"Step 3: Divide BOTH sides by {coeff}")
            steps.append(f"x = {answer}")

        steps.append(f"\nAnswer: x = {answer}")
        steps.append(f"Check: Substitute x = {answer} back into original equation")

        return steps

    def _generate_concise_steps(self, problem_text: str, equation: str, equation_type: str, params: dict, answer) -> list:
        """Generate concise steps with only formulas and values."""
        steps = []
        steps.append(problem_text)

        if equation_type == 'x_plus_c':
            c, result = params['c'], params['result']
            steps.append(f"x + {c} = {result}")
            steps.append(f"x + {c} - {c} = {result} - {c}")
            steps.append(f"x = {result - c}")

        elif equation_type == 'x_minus_c':
            c, result = params['c'], params['result']
            steps.append(f"x - {c} = {result}")
            steps.append(f"x - {c} + {c} = {result} + {c}")
            steps.append(f"x = {result + c}")

        elif equation_type == 'c_minus_x':
            c, result = params['c'], params['result']
            steps.append(f"{c} - x = {result}")
            steps.append(f"{c} - x - {c} = {result} - {c}")
            steps.append(f"-x = {result - c}")
            steps.append(f"x = {c - result}")

        elif equation_type == 'two_step':
            a, b, c, sign = params['a'], params['b'], params['c'], params['sign']
            if sign == '+':
                steps.append(f"{a}x + {b} = {c}")
                steps.append(f"{a}x + {b} - {b} = {c} - {b}")
                steps.append(f"{a}x = {c - b}")
                steps.append(f"x = {(c - b) // a}")
            else:  # sign == '-'
                steps.append(f"{a}x - {b} = {c}")
                steps.append(f"{a}x - {b} + {b} = {c} + {b}")
                steps.append(f"{a}x = {c + b}")
                steps.append(f"x = {(c + b) // a}")

        elif equation_type == 'variables_on_both_sides':
            a, b, c, d = params['a'], params['b'], params['c'], params['d']
            sign1, sign2 = params['sign1'], params['sign2']
            b_signed = b if sign1 == '+' else -b
            d_signed = d if sign2 == '+' else -d
            steps.append(f"{a}x {sign1} {b} = {c}x {sign2} {d}")
            steps.append(f"{a}x - {c}x {sign1} {b} = {d_signed}")
            steps.append(f"{a - c}x {sign1} {b} = {d_signed}")
            steps.append(f"{a - c}x = {d_signed - b_signed}")
            steps.append(f"x = {answer}")

        elif equation_type == 'negative_coefficients':
            if 'simple' in params:
                c, result = params['c'], params['result']
                sign = params['sign']
                c_signed = c if sign == '+' else -c
                steps.append(f"-x {sign} {c} = {result}")
                steps.append(f"-x = {result - c_signed}")
                steps.append(f"x = {answer}")
            else:
                a, b, c = params['a'], params['b'], params['c']
                sign = params['sign']
                b_signed = b if sign == '+' else -b
                steps.append(f"-{a}x {sign} {b} = {c}")
                steps.append(f"-{a}x = {c - b_signed}")
                steps.append(f"x = {answer}")

        elif equation_type == 'word_problem_context':
            if 'a' in params:
                # Two-step word problem: ax + b = c or ax - b = c
                a, b, c, sign = params['a'], params['b'], params['c'], params['sign']
                if sign == '+':
                    steps.append(f"Equation: {a}x + {b} = {c}")
                    steps.append(f"{a}x + {b} - {b} = {c} - {b}")
                    steps.append(f"{a}x = {c - b}")
                    steps.append(f"x = {(c - b) // a}")
                else:  # sign == '-'
                    steps.append(f"Equation: {a}x - {b} = {c}")
                    steps.append(f"{a}x - {b} + {b} = {c} + {b}")
                    steps.append(f"{a}x = {c + b}")
                    steps.append(f"x = {(c + b) // a}")
            else:
                # Simple word problem: x + c = result or x - c = result
                c, result, sign = params['c'], params['result'], params['sign']
                if sign == '+':
                    steps.append(f"Equation: x + {c} = {result}")
                    steps.append(f"x + {c} - {c} = {result} - {c}")
                    steps.append(f"x = {result - c}")
                else:  # sign == '-'
                    steps.append(f"Equation: x - {c} = {result}")
                    steps.append(f"x - {c} + {c} = {result} + {c}")
                    steps.append(f"x = {result + c}")

        elif equation_type == 'three_step_equation':
            coeff, a, b, result = params['coeff'], params['a'], params['b'], params['result']
            steps.append(f"{coeff}x + {a} - {b} = {result}")
            steps.append(f"{coeff}x + {a - b} = {result}")
            steps.append(f"{coeff}x = {result - (a - b)}")
            steps.append(f"x = {answer}")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct equation solving.

        Args:
            problem: Linear equation problem
            verbose: If True, generate verbose steps; otherwise generate concise steps

        Returns:
            Solution with correct steps
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
            answer = result - c

        elif equation_type == 'x_minus_c':
            match = re.match(r'x - (\d+) = (-?\d+)', equation)
            c = int(match.group(1))
            result = int(match.group(2))
            params = {'c': c, 'result': result}
            answer = result + c

        elif equation_type == 'c_minus_x':
            match = re.match(r'(\d+) - x = (\d+)', equation)
            c = int(match.group(1))
            result = int(match.group(2))
            params = {'c': c, 'result': result}
            answer = c - result

        elif equation_type == 'two_step':
            match = re.match(r'(\d+)x ([+-]) (\d+) = (-?\d+)', equation)
            a = int(match.group(1))
            sign = match.group(2)
            b = int(match.group(3))
            c = int(match.group(4))
            params = {'a': a, 'b': b, 'c': c, 'sign': sign}
            if sign == '+':
                answer = (c - b) // a
            else:  # sign == '-'
                answer = (c + b) // a

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
            answer = (d_signed - b_signed) // (a - c)

        elif equation_type == 'negative_coefficients':
            if equation.startswith('-x'):
                match = re.match(r'-x ([+-]) (\d+) = (-?\d+)', equation)
                sign = match.group(1)
                c = int(match.group(2))
                result = int(match.group(3))
                c_signed = c if sign == '+' else -c
                params = {'c': c, 'result': result, 'simple': True, 'sign': sign}
                answer = -(result - c_signed)
            else:
                match = re.match(r'-(\d+)x ([+-]) (\d+) = (-?\d+)', equation)
                a = int(match.group(1))
                sign = match.group(2)
                b = int(match.group(3))
                c = int(match.group(4))
                b_signed = b if sign == '+' else -b
                params = {'a': a, 'b': b, 'c': c, 'sign': sign}
                answer = (c - b_signed) // (-a)

        elif equation_type == 'word_problem_context':
            # Check if it's a two-step equation first (ax + b = c or ax - b = c)
            two_step_match = re.match(r'(\d+)x ([+-]) (\d+) = (-?\d+)', equation)
            if two_step_match:
                a = int(two_step_match.group(1))
                sign = two_step_match.group(2)
                b = int(two_step_match.group(3))
                c = int(two_step_match.group(4))
                params = {'a': a, 'b': b, 'c': c, 'sign': sign}
                if sign == '+':
                    answer = (c - b) // a
                else:  # sign == '-'
                    answer = (c + b) // a
            else:
                # Simple equation: x + c = result or x - c = result
                match = re.match(r'x ([+-]) (\d+) = (-?\d+)', equation)
                sign = match.group(1)
                c = int(match.group(2))
                result = int(match.group(3))
                params = {'c': c, 'result': result, 'sign': sign}
                if sign == '+':
                    answer = result - c
                else:  # sign == '-'
                    answer = result + c

        elif equation_type == 'three_step_equation':
            match = re.match(r'(\d+)x \+ (\d+) - (\d+) = (\d+)', equation)
            coeff = int(match.group(1))
            a = int(match.group(2))
            b = int(match.group(3))
            result = int(match.group(4))
            params = {'coeff': coeff, 'a': a, 'b': b, 'result': result}
            answer = (result - (a - b)) // coeff

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
            is_correct=True,
            algorithm_name=self.get_name()
        )
