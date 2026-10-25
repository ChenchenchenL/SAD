"""
Divide-One-Term-Only malrule algorithm.

Implements the systematic error of dividing only one term
instead of the entire side of an equation.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import re
from typing import Tuple, Dict, Any, List
from utils import Malrule, Problem, Solution

class DivideOneTermOnlyMalrule(Malrule):
    """
    Implements the Divide-One-Term-Only bug.

    Students incorrectly apply division to only one term (usually
    the term with the variable) instead of distributing it to all
    terms on that side of the equation.

    Example: 2x + 4 = 10
    - Correct: (2x + 4) ÷ 2 = 10 ÷ 2 → x + 2 = 5 → x = 3
    - Malrule: 2x ÷ 2 + 4 = 10 ÷ 2 → x + 4 = 5 → x = 1 (WRONG!)

    This is a very common distribution error in algebra.
    """

    def get_name(self) -> str:
        return "Divide-One-Term-Only"

    def get_description(self) -> str:
        return (
            "Students incorrectly apply division to only one term (typically the "
            "variable term) instead of distributing the operation to all terms on "
            "that side of the equation. This reflects a fundamental misunderstanding "
            "of how operations apply to entire expressions and the distributive property."
        )

    def _generate_verbose_steps(self, problem: Problem, equation: str, actual_equation_type: str,
                                 parsed: Tuple, is_word_problem: bool, answer, right_side) -> List[str]:
        """Generate verbose steps with detailed explanations."""
        steps = []

        # For word problems, show the extraction process
        if is_word_problem:
            steps.append(f"Word Problem: {problem.text}")
            steps.append("")
            steps.append("MALRULE APPROACH: Extract equation and divide only the x term")
            steps.append(f"  Extracted Equation: {equation}")
            steps.append("")
        else:
            steps.append(f"Equation: {equation}")

        if actual_equation_type == 'three_term_addition':
            a, b, d, c = parsed
            total_constants = b + d

            steps.append(f"MALRULE: Divide the x term by {a} to get x")
            steps.append(f"\nStep 1: Divide {a}x by {a}")
            steps.append(f"MALRULE REASONING: To get x alone, divide just the x term")
            steps.append(f"{a}x ÷ {a} + {b} + {d} = {c} ÷ {a}")
            steps.append(f"x + {b} + {d} = {right_side}")

            steps.append(f"\nStep 2: Subtract {b} + {d} = {total_constants} from both sides")
            steps.append(f"x = {right_side} - {total_constants}")
            steps.append(f"x = {answer}")

        elif actual_equation_type == 'subtraction_form':
            a, neg_b, c = parsed
            b = -neg_b

            steps.append(f"MALRULE: Divide the x term by {a} to get x")
            steps.append(f"\nStep 1: Divide {a}x by {a}")
            steps.append(f"MALRULE REASONING: To get x alone, divide just the x term")
            steps.append(f"{a}x ÷ {a} - {b} = {c} ÷ {a}")
            steps.append(f"x - {b} = {right_side}")

            steps.append(f"\nStep 2: Add {b} to both sides")
            steps.append(f"x = {right_side} + {b}")
            steps.append(f"x = {answer}")

        else:  # two_step_addition or fractional_coefficients (default)
            a, b, c = parsed

            steps.append(f"MALRULE: Divide the x term by {a} to get x")
            steps.append(f"\nStep 1: Divide {a}x by {a}")
            steps.append(f"MALRULE REASONING: To get x alone, divide just the x term")
            steps.append(f"{a}x ÷ {a} + {b} = {c} ÷ {a}")
            steps.append(f"x + {b} = {right_side}")

            steps.append(f"\nStep 2: Subtract {b} from both sides")
            steps.append(f"x = {right_side} - {b}")
            steps.append(f"x = {answer}")

        steps.append(f"\nFinal answer: x = {answer} (INCORRECT - only divided one term)")

        return steps

    def _generate_concise_steps(self, problem: Problem, equation: str, actual_equation_type: str,
                                 parsed: Tuple, is_word_problem: bool, answer, right_side) -> List[str]:
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

            steps.append(f"x + {b} + {d} = {right_side}")
            steps.append(f"x = {right_side} - {total_constants}")
            steps.append(f"x = {answer}")

        elif actual_equation_type == 'subtraction_form':
            a, neg_b, c = parsed
            b = -neg_b

            steps.append(f"x - {b} = {right_side}")
            steps.append(f"x = {answer}")

        else:  # two_step_addition or fractional_coefficients (default)
            a, b, c = parsed

            steps.append(f"x + {b} = {right_side}")
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

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        equation = problem.metadata['equation']
        equation_type = problem.metadata.get('equation_type', 'two_step_addition')
        word_problem_type = problem.metadata.get('word_problem_type', None)
        is_word_problem = problem.metadata.get('is_word_problem', False)

        # For word problems, use the embedded equation type
        if is_word_problem and word_problem_type:
            actual_equation_type = word_problem_type
        else:
            actual_equation_type = equation_type

        # Parse to get values
        parsed = self._parse_equation(equation, actual_equation_type)

        if actual_equation_type == 'three_term_addition':
            a, b, d, c = parsed
            # Student: x + b + d = c/a → x = c/a - b - d
            right_side = c / a if c % a != 0 else c // a
            answer = right_side - b - d
        elif actual_equation_type == 'subtraction_form':
            a, neg_b, c = parsed
            b = -neg_b
            # Student: x - b = c/a → x = c/a + b
            right_side = c / a if c % a != 0 else c // a
            answer = right_side + b
        else:  # two_step_addition or default
            a, b, c = parsed
            # Student: x + b = c/a → x = c/a - b
            right_side = c / a if c % a != 0 else c // a
            answer = right_side - b

        return round(answer, 2) if isinstance(answer, float) else answer

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Divide-One-Term-Only malrule.

        Args:
            problem: Two-step equation problem
            verbose: If True, generate detailed steps; if False, generate concise steps

        Returns:
            Solution with incorrect one-term division
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

        # Calculate answer and right_side based on equation type
        if actual_equation_type == 'three_term_addition':
            a, b, d, c = parsed
            # Calculate right side
            if isinstance(c / a, float) and abs(c / a - round(c / a)) > 0.01:
                right_side = round(c / a, 2)
            else:
                right_side = int(c // a) if c % a == 0 else round(c / a, 2)
            total_constants = b + d
            answer = right_side - total_constants

        elif actual_equation_type == 'subtraction_form':
            a, neg_b, c = parsed
            b = -neg_b
            if isinstance(c / a, float) and abs(c / a - round(c / a)) > 0.01:
                right_side = round(c / a, 2)
            else:
                right_side = int(c // a) if c % a == 0 else round(c / a, 2)
            answer = right_side + b

        else:  # two_step_addition or fractional_coefficients (default)
            a, b, c = parsed
            if isinstance(c / a, float) and abs(c / a - round(c / a)) > 0.01:
                right_side = round(c / a, 2)
            else:
                right_side = int(c // a) if c % a == 0 else round(c / a, 2)
            answer = right_side - b

        # Round answer if close to integer
        if isinstance(answer, float) and abs(answer - round(answer)) < 0.01:
            answer = int(round(answer))
        elif isinstance(answer, float):
            answer = round(answer, 2)

        # Generate steps based on verbose setting
        if verbose:
            steps = self._generate_verbose_steps(problem, equation, actual_equation_type,
                                                  parsed, is_word_problem, answer, right_side)
        else:
            steps = self._generate_concise_steps(problem, equation, actual_equation_type,
                                                  parsed, is_word_problem, answer, right_side)

        return Solution(
            answer=answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
