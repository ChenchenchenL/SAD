"""
Malrule algorithm for Cancel-Across-Equals error.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import re
from typing import Dict, List, Any, Tuple
from utils import Malrule, Problem, Solution

class CancelAcrossEqualsMalrule(Malrule):
    """
    Students cancel matching variable terms from both sides without proper subtraction.

    Example: 2x = x + 5 → Student "cancels" x leaving: 2 = 5 (wrong!)
    """

    def get_name(self) -> str:
        return "Cancel-Across-Equals"

    def get_description(self) -> str:
        return (
            "Students incorrectly 'cancel' matching variable terms from both sides of an "
            "equation as if they were canceling factors in a fraction, rather than properly "
            "subtracting the terms from both sides. This reflects confusion between the "
            "procedures for simplifying fractions and solving equations."
        )

    def _generate_verbose_steps(self, problem: Problem, equation_type: str, a: int, b: int, c: int, d: int, malrule_answer, template: str, equation_str: str = None) -> List[str]:
        """Generate verbose steps with detailed explanations (original format)."""
        steps = []

        # For word problems, show the extraction process
        if template == 'word_problem_context':
            steps.append(f"Word Problem: {problem.text}")
            steps.append("")
            steps.append("MALRULE APPROACH: Extract equation and apply 'canceling'")
            steps.append("")
            steps.append(f"  Extracted Equation: {equation_str}")
            steps.append("")

        # Format problem text and steps based on equation type
        if equation_type == 'both_sides_constant':
            if template != 'word_problem_context':
                steps.append(f"Problem: {a}x + {d} = {b}x + {c}")
                steps.append("")
            steps.append("MALRULE: 'Cancel' matching x terms like in fractions")
            steps.append(f"  MALRULE REASONING: 'Both sides have x, so cancel them out'")
            steps.append("")
            steps.append(f"Step 1: See {a}x and {b}x - they both have x")
            steps.append(f"  MALRULE: 'Cancel' the {b}x from both sides")
            steps.append("")
            steps.append(f"Step 2: After 'canceling', left with:")
            steps.append(f"  {a}x + {d} = {c} → {a}x = {c} - {d} → {a}x = {c - d}")
            steps.append("")
            steps.append(f"Step 3: Divide by {a}:")
            steps.append(f"  x = {c - d}/{a} = {malrule_answer}")

        elif equation_type == 'three_term_equation':
            if template != 'word_problem_context':
                steps.append(f"Problem: {a}x = {b}x + {c}x + {d}")
                steps.append("")
            steps.append("MALRULE: 'Cancel' matching x terms like in fractions")
            steps.append(f"  MALRULE REASONING: 'All terms have x, so cancel them out'")
            steps.append("")
            steps.append(f"Step 1: See {a}x, {b}x, and {c}x - they all have x")
            steps.append(f"  MALRULE: 'Cancel' the {b}x and {c}x from both sides")
            steps.append("")
            steps.append(f"Step 2: After 'canceling', left with:")
            steps.append(f"  {a}x = {d}")
            steps.append("")
            steps.append(f"Step 3: Divide by {a}:")
            steps.append(f"  x = {d}/{a} = {malrule_answer}")

        else:  # basic_equation
            if template != 'word_problem_context':
                steps.append(f"Problem: {a}x = {b}x + {c}")
                steps.append("")
            steps.append("MALRULE: 'Cancel' matching x terms like in fractions")
            steps.append(f"  MALRULE REASONING: 'Both sides have x, so cancel them out'")
            steps.append("")
            steps.append(f"Step 1: See {a}x and {b}x - they both have x")
            steps.append(f"  MALRULE: 'Cancel' the {b}x from both sides (cross it out)")
            steps.append("")
            steps.append(f"Step 2: After 'canceling', left with:")
            steps.append(f"  {a}x = {c}")
            steps.append(f"  (WRONG! Should be {a}x - {b}x = {c})")
            steps.append("")
            steps.append(f"Step 3: Divide by {a}:")
            steps.append(f"  x = {c}/{a} = {malrule_answer}")

        steps.append("")
        steps.append(f"Final Answer: x = {malrule_answer} (INCORRECT - canceled instead of subtracting!)")

        return steps

    def _generate_concise_steps(self, problem: Problem, equation_type: str, a: int, b: int, c: int, d: int, malrule_answer, template: str, equation_str: str = None) -> List[str]:
        """Generate concise steps with only formulas and values."""
        steps = []

        # Question
        steps.append(problem.text)

        # For word problems, include equation extraction
        if template == 'word_problem_context':
            steps.append(f"Equation: {equation_str}")

        # Steps based on equation type
        if equation_type == 'both_sides_constant':
            steps.append(f"{a}x + {d} = {b}x + {c}")
            steps.append(f"{a}x + {d} = {c}")
            steps.append(f"{a}x = {c} - {d}")
            steps.append(f"{a}x = {c - d}")
            steps.append(f"x = {c - d}/{a}")
            steps.append(f"x = {malrule_answer}")

        elif equation_type == 'three_term_equation':
            steps.append(f"{a}x = {b}x + {c}x + {d}")
            steps.append(f"{a}x = {d}")
            steps.append(f"x = {d}/{a}")
            steps.append(f"x = {malrule_answer}")

        else:  # basic_equation
            steps.append(f"{a}x = {b}x + {c}")
            steps.append(f"{a}x = {c}")
            steps.append(f"x = {c}/{a}")
            steps.append(f"x = {malrule_answer}")

        return steps

    def _parse_equation(self, equation_str: str) -> Tuple:
        """Parse equation string to extract components and determine type."""
        equation_str = equation_str.strip()

        # Remove "Solve for x: " prefix if present
        if "Solve for x:" in equation_str:
            equation_str = equation_str.split("Solve for x:")[1].strip()

        # Split by equals sign
        if '=' not in equation_str:
            raise ValueError(f"No equals sign found in: {equation_str}")

        left, right = equation_str.split('=')
        left = left.strip()
        right = right.strip()

        # Detect equation type and parse
        # Type 1: ax + d = bx + c (both_sides_constant)
        match = re.match(r'([+-]?\d+)x\s*([+-])\s*([+-]?\d+)\s*=\s*([+-]?\d+)x\s*([+-])\s*([+-]?\d+)', equation_str)
        if match:
            a = int(match.group(1))
            sign1 = match.group(2)
            d = int(match.group(3))
            if sign1 == '-':
                d = -abs(d)
            else:
                d = abs(d)
            b = int(match.group(4))
            sign2 = match.group(5)
            c = int(match.group(6))
            if sign2 == '-':
                c = -abs(c)
            else:
                c = abs(c)
            return ('both_sides_constant', a, b, c, d)

        # Type 2: ax = bx + cx + d (three_term_equation)
        match = re.match(r'([+-]?\d+)x\s*=\s*([+-]?\d+)x\s*([+-])\s*([+-]?\d+)x\s*([+-])\s*([+-]?\d+)', equation_str)
        if match:
            a = int(match.group(1))
            b = int(match.group(2))
            sign1 = match.group(3)
            c_coeff = int(match.group(4))
            if sign1 == '-':
                c_coeff = -abs(c_coeff)
            else:
                c_coeff = abs(c_coeff)
            sign2 = match.group(5)
            d = int(match.group(6))
            if sign2 == '-':
                d = -abs(d)
            else:
                d = abs(d)
            return ('three_term_equation', a, b, c_coeff, d)

        # Type 3: ax = bx + c (basic_equation)
        match = re.match(r'([+-]?\d+)x\s*=\s*([+-]?\d+)x\s*([+-])\s*([+-]?\d+)', equation_str)
        if match:
            a = int(match.group(1))
            b = int(match.group(2))
            sign = match.group(3)
            c = int(match.group(4))
            if sign == '-':
                c = -abs(c)
            else:
                c = abs(c)
            return ('basic_equation', a, b, c)

        raise ValueError(f"Cannot parse equation: {equation_str}")

    def _parse_comparison_problem(self, text: str) -> Tuple:
        """Parse comparison problem to extract two equations."""
        # Format: "Which equation has a larger solution for x: 5x = 2x + 6 or 4x = 2x + 10?"
        match = re.search(r'(\d+)x\s*=\s*(\d+)x\s*\+\s*(\d+)\s+or\s+(\d+)x\s*=\s*(\d+)x\s*\+\s*(\d+)', text)
        if match:
            a1, b1, c1 = int(match.group(1)), int(match.group(2)), int(match.group(3))
            a2, b2, c2 = int(match.group(4)), int(match.group(5)), int(match.group(6))
            return a1, b1, c1, a2, b2, c2

        raise ValueError(f"Cannot parse comparison problem: {text}")

    def calculate_expected_answer(self, problem: Problem):
        """
        Calculate the expected malrule answer (incorrect) for this problem.

        Applies the cancellation malrule to calculate the answer.
        """
        template = problem.metadata.get('template', 'basic_equation')

        # Handle comparison_problem specially
        if template == 'comparison_problem':
            # Parse and solve both equations with malrule
            a1, b1, c1, a2, b2, c2 = self._parse_comparison_problem(problem.text)

            # Malrule: Cancel bx incorrectly
            # Equation 1: a1*x = b1*x + c1 → malrule: a1*x = c1 → x = c1/a1
            malrule1 = c1 / a1
            if malrule1.is_integer():
                malrule1 = int(malrule1)

            # Equation 2: a2*x = b2*x + c2 → correctly solve
            solution2 = c2 / (a2 - b2)
            if solution2.is_integer():
                solution2 = int(solution2)

            # Compare malrule1 with correct2
            if malrule1 > solution2:
                return f"{a1}x = {b1}x + {c1} has larger solution"
            elif malrule1 < solution2:
                return f"{a2}x = {b2}x + {c2} has larger solution"
            else:
                return "Both have equal solutions"

        # For word problems, construct equation from metadata
        if template == 'word_problem_context':
            word_problem_type = problem.metadata.get('word_problem_type', 'basic_equation')
            a = problem.metadata['a']
            b = problem.metadata['b']
            c = problem.metadata.get('c', 0)
            d = problem.metadata.get('d', None)
            equation_type = word_problem_type
        else:
            # Parse equation from problem text
            parsed = self._parse_equation(problem.text)
            equation_type = parsed[0]

            if equation_type == 'both_sides_constant':
                _, a, b, c, d = parsed
            elif equation_type == 'three_term_equation':
                _, a, b, c, d = parsed
            else:  # basic_equation
                _, a, b, c = parsed
                d = None

        # Calculate malrule answer based on equation type
        if equation_type == 'both_sides_constant':
            # ax + d = bx + c → malrule: cancel bx → ax + d = c → x = (c - d)/a
            malrule_answer = (c - d) / a
        elif equation_type == 'three_term_equation':
            # ax = bx + cx + d → malrule: cancel bx and cx → ax = d → x = d/a
            malrule_answer = d / a
        else:  # basic_equation
            # ax = bx + c → malrule: cancel bx → ax = c → x = c/a
            malrule_answer = c / a

        # Convert to integer if possible
        if isinstance(malrule_answer, float) and malrule_answer.is_integer():
            malrule_answer = int(malrule_answer)

        return malrule_answer

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        template = problem.metadata.get('template', 'basic_equation')

        # Handle comparison_problem specially
        if template == 'comparison_problem':
            return self._solve_comparison_problem(problem, verbose=verbose)

        # For word problems, construct equation from metadata
        if template == 'word_problem_context':
            word_problem_type = problem.metadata.get('word_problem_type', 'basic_equation')
            a = problem.metadata['a']
            b = problem.metadata['b']
            c = problem.metadata.get('c', 0)
            d = problem.metadata.get('d', None)

            # Construct equation string based on embedded type
            if word_problem_type == 'both_sides_constant':
                equation_str = f"{a}x + {d} = {b}x + {c}"
                equation_type = 'both_sides_constant'
            elif word_problem_type == 'three_term_equation':
                equation_str = f"{a}x = {b}x + {c}x + {d}"
                equation_type = 'three_term_equation'
            else:  # basic_equation
                equation_str = f"{a}x = {b}x + {c}"
                equation_type = 'basic_equation'
        else:
            # Parse equation from problem text
            parsed = self._parse_equation(problem.text)
            equation_type = parsed[0]
            equation_str = None

            if equation_type == 'both_sides_constant':
                _, a, b, c, d = parsed
            elif equation_type == 'three_term_equation':
                _, a, b, c, d = parsed
            else:  # basic_equation
                _, a, b, c = parsed
                d = None

        # Calculate malrule answer
        malrule_answer = self.calculate_expected_answer(problem)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, equation_type, a, b, c, d, malrule_answer, template, equation_str)
        else:
            steps = self._generate_concise_steps(problem, equation_type, a, b, c, d, malrule_answer, template, equation_str)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _solve_comparison_problem(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle comparison problems which compare two equation solutions."""
        # Parse the two equations from problem text
        a1, b1, c1, a2, b2, c2 = self._parse_comparison_problem(problem.text)

        # Apply malrule to first equation, solve second correctly
        # Equation 1 with malrule: a1*x = b1*x + c1 → cancel b1*x → a1*x = c1 → x = c1/a1
        malrule1 = c1 / a1
        if malrule1.is_integer():
            malrule1 = int(malrule1)

        # Equation 2 solved correctly: a2*x = b2*x + c2 → x = c2/(a2 - b2)
        solution2 = c2 / (a2 - b2)
        if solution2.is_integer():
            solution2 = int(solution2)

        # Compare malrule1 with correct solution2
        if malrule1 > solution2:
            malrule_answer = f"{a1}x = {b1}x + {c1} has larger solution"
        elif malrule1 < solution2:
            malrule_answer = f"{a2}x = {b2}x + {c2} has larger solution"
        else:
            malrule_answer = "Both have equal solutions"

        if verbose:
            steps = self._generate_verbose_comparison_steps(problem, a1, b1, c1, a2, b2, c2, malrule1, solution2, malrule_answer)
        else:
            steps = self._generate_concise_comparison_steps(problem, a1, b1, c1, a2, b2, c2, malrule1, solution2, malrule_answer)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _generate_verbose_comparison_steps(self, problem: Problem, a1: int, b1: int, c1: int, a2: int, b2: int, c2: int, malrule1, solution2, malrule_answer: str) -> List[str]:
        """Generate verbose steps for comparison problem with malrule."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE approach: Cancel x terms in each equation")
        steps.append("")
        steps.append(f"Equation 1: {a1}x = {b1}x + {c1}")
        steps.append(f"  MALRULE: Cancel {b1}x from both sides")
        steps.append(f"  {a1}x = {c1}")
        steps.append(f"  x = {c1}/{a1} = {malrule1}")
        steps.append("")
        steps.append(f"Equation 2: {a2}x = {b2}x + {c2}")
        steps.append(f"  {a2}x - {b2}x = {c2}")
        steps.append(f"  {a2 - b2}x = {c2}")
        steps.append(f"  x = {c2}/{a2 - b2} = {solution2}")
        steps.append("")
        steps.append(f"Comparison: {malrule1} vs {solution2}")
        steps.append(f"Result: {malrule_answer}")
        return steps

    def _generate_concise_comparison_steps(self, problem: Problem, a1: int, b1: int, c1: int, a2: int, b2: int, c2: int, malrule1, solution2, malrule_answer: str) -> List[str]:
        """Generate concise steps for comparison problem with malrule."""
        steps = []
        steps.append(problem.text)
        steps.append(f"{a1}x = {b1}x + {c1}")
        steps.append(f"{a1}x = {c1}")
        steps.append(f"x = {c1}/{a1} = {malrule1}")
        steps.append(f"{a2}x = {b2}x + {c2}")
        steps.append(f"{a2}x - {b2}x = {c2}")
        steps.append(f"{a2 - b2}x = {c2}")
        steps.append(f"x = {c2}/{a2 - b2} = {solution2}")
        steps.append(f"{malrule1} vs {solution2}")
        steps.append(malrule_answer)
        return steps
