"""
Correct two-step equation solving algorithm.

Implements proper equation solving by applying operations to
entire sides of the equation.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import re
from typing import Tuple, List
from utils import CorrectAlgorithm, Problem, Solution


class TwoStepEquationCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for solving two-step equations.

    Properly applies division to ALL terms on a side.
    """

    def get_name(self) -> str:
        return "Correct Two-Step Equation Solving"

    def get_description(self) -> str:
        return (
            "Solves two-step equations correctly by applying operations "
            "to the ENTIRE side of the equation. For 2x + 4 = 10: "
            "first subtract 4 from both sides (2x = 6), then divide "
            "BOTH sides by 2 (x = 3)."
        )

    def _generate_verbose_steps(self, problem: Problem, equation: str, actual_equation_type: str,
                                 parsed: Tuple, is_word_problem: bool, answer) -> List[str]:
        """Generate verbose steps with detailed explanations."""
        steps = []

        # For word problems, show the extraction process
        if is_word_problem:
            steps.append(f"Word Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Extract the equation from the word problem")
            steps.append(f"  Equation: {equation}")
            steps.append("")
            steps.append("Step 2: Solve using proper algebraic steps")
            steps.append("")
        else:
            steps.append(f"Equation: {equation}")

        steps.append(f"Goal: Isolate x using inverse operations on BOTH sides")

        if actual_equation_type == 'three_term_addition':
            a, b, d, c = parsed
            total_constants = b + d

            steps.append(f"\nStep 1: Combine constants on left side: {b} + {d} = {total_constants}")
            steps.append(f"{a}x + {total_constants} = {c}")

            steps.append(f"\nStep 2: Subtract {total_constants} from BOTH sides")
            steps.append(f"{a}x + {total_constants} - {total_constants} = {c} - {total_constants}")
            intermediate = c - total_constants
            steps.append(f"{a}x = {intermediate}")

            steps.append(f"\nStep 3: Divide BOTH sides by {a}")
            steps.append(f"{a}x ÷ {a} = {intermediate} ÷ {a}")
            steps.append(f"x = {answer}")

            check = a * answer + b + d
            steps.append(f"\nFinal answer: x = {answer}")
            steps.append(f"Check: {a}({answer}) + {b} + {d} = {check} = {c} ✓")

        elif actual_equation_type == 'subtraction_form':
            a, neg_b, c = parsed
            b = -neg_b

            steps.append(f"\nStep 1: Add {b} to BOTH sides")
            steps.append(f"{a}x - {b} + {b} = {c} + {b}")
            intermediate = c + b
            steps.append(f"{a}x = {intermediate}")

            steps.append(f"\nStep 2: Divide BOTH sides by {a}")
            steps.append(f"{a}x ÷ {a} = {intermediate} ÷ {a}")
            steps.append(f"x = {answer}")

            steps.append(f"\nFinal answer: x = {answer}")
            steps.append(f"Check: {a}({answer}) - {b} = {a * answer - b} = {c} ✓")

        else:  # two_step_addition or fractional_coefficients (default)
            a, b, c = parsed

            steps.append(f"\nStep 1: Subtract {b} from BOTH sides")
            steps.append(f"{a}x + {b} - {b} = {c} - {b}")
            intermediate = c - b
            steps.append(f"{a}x = {intermediate}")

            steps.append(f"\nStep 2: Divide BOTH sides by {a}")
            steps.append(f"{a}x ÷ {a} = {intermediate} ÷ {a}")
            steps.append(f"x = {answer}")

            steps.append(f"\nFinal answer: x = {answer}")
            steps.append(f"Check: {a}({answer}) + {b} = {a * answer + b} = {c} ✓")

        return steps

    def _generate_concise_steps(self, problem: Problem, equation: str, actual_equation_type: str,
                                 parsed: Tuple, is_word_problem: bool, answer) -> List[str]:
        """Generate concise steps with only formulas and values."""
        steps = []

        # For word problems, show the extraction step
        if is_word_problem:
            steps.append(f"{problem.text}")
            steps.append(f"Equation: {equation}")
        else:
            steps.append(f"Solve for x: {equation}")

        if actual_equation_type == 'three_term_addition':
            a, b, d, c = parsed
            total_constants = b + d
            intermediate = c - total_constants

            steps.append(f"{a}x + {total_constants} = {c}")
            steps.append(f"{a}x = {intermediate}")
            steps.append(f"x = {answer}")

        elif actual_equation_type == 'subtraction_form':
            a, neg_b, c = parsed
            b = -neg_b
            intermediate = c + b

            steps.append(f"{a}x = {intermediate}")
            steps.append(f"x = {answer}")

        else:  # two_step_addition or fractional_coefficients (default)
            a, b, c = parsed
            intermediate = c - b

            steps.append(f"{a}x = {intermediate}")
            steps.append(f"x = {answer}")

        return steps

    def _parse_equation(self, equation_str: str, equation_type: str) -> Tuple:
        """Parse equation string to extract components."""
        equation_str = equation_str.strip()

        # Split by equals sign
        if '=' not in equation_str:
            raise ValueError(f"No equals sign found in: {equation_str}")

        left, right = equation_str.split('=')
        left = left.strip()
        right = right.strip()

        # Parse right side (constant c)
        c = float(right) if '.' in right else int(right)

        # Parse left side based on equation type
        if equation_type == 'three_term_addition':
            # Format: 2x + 3 + 4 = c
            match = re.match(r'([+-]?[\d.]+)x\s*([+-])\s*([\d.]+)\s*([+-])\s*([\d.]+)', left)
            if match:
                a = float(match.group(1)) if '.' in match.group(1) else int(match.group(1))
                sign1 = match.group(2)
                b = float(match.group(3)) if '.' in match.group(3) else int(match.group(3))
                if sign1 == '-':
                    b = -b
                sign2 = match.group(4)
                d = float(match.group(5)) if '.' in match.group(5) else int(match.group(5))
                if sign2 == '-':
                    d = -d
                return a, b, d, c

        elif equation_type == 'subtraction_form':
            # Format: 2x - 3 = c
            match = re.match(r'([+-]?[\d.]+)x\s*-\s*([\d.]+)', left)
            if match:
                a = float(match.group(1)) if '.' in match.group(1) else int(match.group(1))
                b = float(match.group(2)) if '.' in match.group(2) else int(match.group(2))
                return a, -b, c  # b is negative in subtraction form

        # Default: two_step_addition or fractional_coefficients format: ax + b = c
        match = re.match(r'([+-]?[\d.]+)x\s*([+-])\s*([\d.]+)', left)
        if match:
            a = float(match.group(1)) if '.' in match.group(1) else int(match.group(1))
            sign = match.group(2)
            b = float(match.group(3)) if '.' in match.group(3) else int(match.group(3))
            if sign == '-':
                b = -b
            return a, b, c

        raise ValueError(f"Cannot parse equation: {equation_str}")

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct two-step equation solving.

        Args:
            problem: Two-step equation problem
            verbose: If True, generate detailed steps; if False, generate concise steps

        Returns:
            Solution with correct steps
        """
        equation = problem.metadata['equation']
        equation_type = problem.metadata.get('equation_type', 'two_step_addition')
        word_problem_type = problem.metadata.get('word_problem_type', None)
        is_word_problem = problem.metadata.get('is_word_problem', False)

        # For word problems, use the embedded equation type
        if is_word_problem and word_problem_type:
            actual_equation_type = word_problem_type
        else:
            actual_equation_type = equation_type

        # Parse the equation
        parsed = self._parse_equation(equation, actual_equation_type)

        # Calculate the answer
        if actual_equation_type == 'three_term_addition':
            a, b, d, c = parsed
            total_constants = b + d
            intermediate = c - total_constants
            answer = intermediate / a
        elif actual_equation_type == 'subtraction_form':
            a, neg_b, c = parsed
            b = -neg_b
            intermediate = c + b
            answer = intermediate / a
        else:  # two_step_addition or fractional_coefficients (default)
            a, b, c = parsed
            intermediate = c - b
            answer = intermediate / a

        # Round if close to integer
        if abs(answer - round(answer)) < 0.01:
            answer = int(round(answer))
        else:
            answer = round(answer, 2)

        # Generate steps based on verbose setting
        if verbose:
            steps = self._generate_verbose_steps(problem, equation, actual_equation_type,
                                                  parsed, is_word_problem, answer)
        else:
            steps = self._generate_concise_steps(problem, equation, actual_equation_type,
                                                  parsed, is_word_problem, answer)

        return Solution(
            answer=answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
