"""
Correct algorithm for solving linear equations.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import re
from typing import List, Tuple, Optional
from utils import CorrectAlgorithm, Problem, Solution


class LinearEquationCorrectAlgorithm(CorrectAlgorithm):
    """Correctly solves linear equations by subtracting from both sides."""

    def get_name(self) -> str:
        return "Correct Linear Equation Solving"

    def get_description(self) -> str:
        return "Correctly solves equations by subtracting matching terms from both sides."

    def _generate_verbose_steps(self, problem: Problem, equation_type: str, a: int, b: int, c: int, d: Optional[int], correct_answer, template: str, equation_str: str = None) -> List[str]:
        """Generate verbose steps with detailed explanations (original format)."""
        steps = []

        # For word problems, show the extraction process
        if template == 'word_problem_context':
            steps.append(f"Word Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Extract the embedded equation")
            steps.append(f"  Equation: {equation_str}")
            steps.append("")
            steps.append("Step 2: Solve the equation using proper algebraic steps")
            steps.append("")

        # Format problem text and steps based on equation type
        if equation_type == 'both_sides_constant':
            if template != 'word_problem_context':
                steps.append(f"Problem: {a}x + {d} = {b}x + {c}")
                steps.append("")
            steps.append("Goal: Isolate x by getting all x terms on one side")
            steps.append("")
            steps.append(f"Step 1: Subtract {b}x from both sides")
            steps.append(f"  {a}x + {d} - {b}x = {b}x + {c} - {b}x")
            steps.append(f"  {a - b}x + {d} = {c}")
            steps.append("")
            steps.append(f"Step 2: Subtract {d} from both sides")
            steps.append(f"  {a - b}x = {c} - {d}")
            steps.append(f"  {a - b}x = {c - d}")
            steps.append("")
            steps.append(f"Step 3: Divide both sides by {a - b}")
            steps.append(f"  x = {c - d}/{a - b}")
            steps.append(f"  x = {correct_answer}")

        elif equation_type == 'three_term_equation':
            if template != 'word_problem_context':
                steps.append(f"Problem: {a}x = {b}x + {c}x + {d}")
                steps.append("")
            steps.append("Goal: Isolate x by getting all x terms on one side")
            steps.append("")
            steps.append(f"Step 1: Subtract {b}x from both sides")
            steps.append(f"  {a}x - {b}x = {b}x + {c}x + {d} - {b}x")
            steps.append(f"  {a - b}x = {c}x + {d}")
            steps.append("")
            steps.append(f"Step 2: Subtract {c}x from both sides")
            steps.append(f"  {a - b}x - {c}x = {c}x + {d} - {c}x")
            steps.append(f"  {a - b - c}x = {d}")
            steps.append("")
            steps.append(f"Step 3: Divide both sides by {a - b - c}")
            steps.append(f"  x = {d}/{a - b - c}")
            steps.append(f"  x = {correct_answer}")

        else:  # basic_equation
            if template != 'word_problem_context':
                steps.append(f"Problem: {a}x = {b}x + {c}")
                steps.append("")
            steps.append("Goal: Isolate x by getting all x terms on one side")
            steps.append("")
            steps.append(f"Step 1: Subtract {b}x from both sides")
            steps.append(f"  {a}x - {b}x = {b}x + {c} - {b}x")
            steps.append(f"  {a - b}x = {c}")
            steps.append("")
            steps.append(f"Step 2: Divide both sides by {a - b}")
            steps.append(f"  x = {c}/{a - b}")
            steps.append(f"  x = {correct_answer}")

        steps.append("")
        steps.append(f"Final Answer: x = {correct_answer} ✓")

        return steps

    def _generate_concise_steps(self, problem: Problem, equation_type: str, a: int, b: int, c: int, d: Optional[int], correct_answer, template: str, equation_str: str = None) -> List[str]:
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
            steps.append(f"{a}x + {d} - {b}x = {b}x + {c} - {b}x")
            steps.append(f"{a - b}x + {d} = {c}")
            steps.append(f"{a - b}x = {c} - {d}")
            steps.append(f"{a - b}x = {c - d}")
            steps.append(f"x = {c - d}/{a - b}")
            steps.append(f"x = {correct_answer}")

        elif equation_type == 'three_term_equation':
            steps.append(f"{a}x = {b}x + {c}x + {d}")
            steps.append(f"{a}x - {b}x = {b}x + {c}x + {d} - {b}x")
            steps.append(f"{a - b}x = {c}x + {d}")
            steps.append(f"{a - b}x - {c}x = {c}x + {d} - {c}x")
            steps.append(f"{a - b - c}x = {d}")
            steps.append(f"x = {d}/{a - b - c}")
            steps.append(f"x = {correct_answer}")

        else:  # basic_equation
            steps.append(f"{a}x = {b}x + {c}")
            steps.append(f"{a}x - {b}x = {b}x + {c} - {b}x")
            steps.append(f"{a - b}x = {c}")
            steps.append(f"x = {c}/{a - b}")
            steps.append(f"x = {correct_answer}")

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

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        template = problem.metadata.get('template', 'basic_equation')

        # Handle comparison_problem specially
        if template == 'comparison_problem':
            return self._solve_comparison_problem(problem, verbose=verbose)

        # For word problems, extract the equation from problem text or construct it
        if template == 'word_problem_context':
            # Word problems have the equation embedded in them
            # We need to construct the equation from metadata
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

        # Calculate the correct answer
        if equation_type == 'both_sides_constant':
            correct_answer = (c - d) // (a - b) if (c - d) % (a - b) == 0 else (c - d) / (a - b)
        elif equation_type == 'three_term_equation':
            correct_answer = d // (a - b - c) if d % (a - b - c) == 0 else d / (a - b - c)
        else:  # basic_equation
            correct_answer = c // (a - b) if c % (a - b) == 0 else c / (a - b)

        if isinstance(correct_answer, float) and correct_answer.is_integer():
            correct_answer = int(correct_answer)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, equation_type, a, b, c, d, correct_answer, template, equation_str)
        else:
            steps = self._generate_concise_steps(problem, equation_type, a, b, c, d, correct_answer, template, equation_str)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _solve_comparison_problem(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle comparison problems which compare two equation solutions."""
        # Parse the two equations from problem text
        a1, b1, c1, a2, b2, c2 = self._parse_comparison_problem(problem.text)

        # Solve both equations correctly
        # Equation 1: a1*x = b1*x + c1 → x = c1/(a1 - b1)
        solution1 = c1 / (a1 - b1)
        if solution1.is_integer():
            solution1 = int(solution1)

        # Equation 2: a2*x = b2*x + c2 → x = c2/(a2 - b2)
        solution2 = c2 / (a2 - b2)
        if solution2.is_integer():
            solution2 = int(solution2)

        # Compare solutions
        if solution1 > solution2:
            correct_answer = f"{a1}x = {b1}x + {c1} has larger solution"
        elif solution1 < solution2:
            correct_answer = f"{a2}x = {b2}x + {c2} has larger solution"
        else:
            correct_answer = "Both have equal solutions"

        if verbose:
            steps = self._generate_verbose_comparison_steps(problem, a1, b1, c1, a2, b2, c2, solution1, solution2, correct_answer)
        else:
            steps = self._generate_concise_comparison_steps(problem, a1, b1, c1, a2, b2, c2, solution1, solution2, correct_answer)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _generate_verbose_comparison_steps(self, problem: Problem, a1: int, b1: int, c1: int, a2: int, b2: int, c2: int, solution1, solution2, correct_answer: str) -> List[str]:
        """Generate verbose steps for comparison problem."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("Correct approach: Solve each equation properly by subtracting")
        steps.append("")
        steps.append(f"Equation 1: {a1}x = {b1}x + {c1}")
        steps.append(f"  {a1}x - {b1}x = {c1}")
        steps.append(f"  {a1 - b1}x = {c1}")
        steps.append(f"  x = {c1}/{a1 - b1} = {solution1}")
        steps.append("")
        steps.append(f"Equation 2: {a2}x = {b2}x + {c2}")
        steps.append(f"  {a2}x - {b2}x = {c2}")
        steps.append(f"  {a2 - b2}x = {c2}")
        steps.append(f"  x = {c2}/{a2 - b2} = {solution2}")
        steps.append("")
        steps.append(f"Comparison: {solution1} vs {solution2}")
        steps.append(f"Result: {correct_answer}")
        return steps

    def _generate_concise_comparison_steps(self, problem: Problem, a1: int, b1: int, c1: int, a2: int, b2: int, c2: int, solution1, solution2, correct_answer: str) -> List[str]:
        """Generate concise steps for comparison problem."""
        steps = []
        steps.append(problem.text)
        steps.append(f"{a1}x = {b1}x + {c1}")
        steps.append(f"{a1}x - {b1}x = {c1}")
        steps.append(f"{a1 - b1}x = {c1}")
        steps.append(f"x = {c1}/{a1 - b1} = {solution1}")
        steps.append(f"{a2}x = {b2}x + {c2}")
        steps.append(f"{a2}x - {b2}x = {c2}")
        steps.append(f"{a2 - b2}x = {c2}")
        steps.append(f"x = {c2}/{a2 - b2} = {solution2}")
        steps.append(f"{solution1} vs {solution2}")
        steps.append(correct_answer)
        return steps
