"""
Correct algorithm for expanding non-distributive operations.
This version actually parses and computes expressions without using metadata answers.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import re
from typing import List, Tuple, Optional
from utils import CorrectAlgorithm, Problem, Solution


class AlgebraExpansionCorrectAlgorithm(CorrectAlgorithm):
    """Correctly expands non-distributive operations by parsing and computing."""

    def get_name(self) -> str:
        return "Correct Algebra Expansion"

    def get_description(self) -> str:
        return "Correctly expands binomial squares and handles non-distributive operations."

    def _generate_verbose_square_binomial_steps(self, var: str, constant: int, is_subtraction: bool, result_str: str) -> List[str]:
        """Generate verbose steps for square binomial expansion."""
        steps = []
        if is_subtraction:
            steps.append(f"Problem: ({var}-{constant})²")
            steps.append("")
            steps.append("Expand using: (a-b)² = a² - 2ab + b²")
            steps.append("")
            steps.append(f"Where a = {var} and b = {constant}")
            steps.append("")
            steps.append(f"Step 1: {var}² (first term squared)")
            steps.append(f"Step 2: -2·{var}·{constant} = -{2*constant}{var} (middle term)")
            steps.append(f"Step 3: {constant}² = {constant**2} (last term squared)")
            steps.append("")
        else:
            steps.append(f"Problem: ({var}+{constant})²")
            steps.append("")
            steps.append("Expand using: (a+b)² = a² + 2ab + b²")
            steps.append("")
            steps.append(f"Where a = {var} and b = {constant}")
            steps.append("")
            steps.append(f"Step 1: {var}² (first term squared)")
            steps.append(f"Step 2: 2·{var}·{constant} = {2*constant}{var} (middle term)")
            steps.append(f"Step 3: {constant}² = {constant**2} (last term squared)")
            steps.append("")
        steps.append(f"Combine: {result_str}")
        steps.append("")
        steps.append(f"Final Answer: {result_str} ✓")
        return steps

    def _generate_concise_square_binomial_steps(self, problem_text: str, var: str, constant: int, is_subtraction: bool, result_str: str) -> List[str]:
        """Generate concise steps for square binomial expansion."""
        steps = []
        steps.append(problem_text)
        if is_subtraction:
            steps.append(f"({var}-{constant})²")
            steps.append(f"(a-b)² = a² - 2ab + b²")
            steps.append(f"{var}²")
            steps.append(f"-2·{var}·{constant} = -{2*constant}{var}")
            steps.append(f"{constant}² = {constant**2}")
            steps.append(f"{result_str}")
        else:
            steps.append(f"({var}+{constant})²")
            steps.append(f"(a+b)² = a² + 2ab + b²")
            steps.append(f"{var}²")
            steps.append(f"2·{var}·{constant} = {2*constant}{var}")
            steps.append(f"{constant}² = {constant**2}")
            steps.append(f"{result_str}")
        return steps

    def _generate_verbose_sqrt_sum_steps(self, num1: int, num2: int, is_pythagorean: bool, result: float) -> List[str]:
        """Generate verbose steps for sqrt sum computation."""
        steps = []
        if is_pythagorean:
            sum_of_squares = num1**2 + num2**2
            steps.append(f"Problem: √({num1}²+{num2}²)")
            steps.append("")
            steps.append("IMPORTANT: Square root does NOT distribute over addition")
            steps.append(f"  √(a²+b²) ≠ √a² + √b²")
            steps.append("")
            steps.append(f"Step 1: Calculate squares inside the radical")
            steps.append(f"  {num1}² = {num1**2}")
            steps.append(f"  {num2}² = {num2**2}")
            steps.append("")
            steps.append(f"Step 2: Add the squares")
            steps.append(f"  {num1**2} + {num2**2} = {sum_of_squares}")
            steps.append("")
            steps.append(f"Step 3: Take square root of the sum")
            steps.append(f"  √{sum_of_squares} = {result}")
            steps.append("")
            steps.append(f"Final Answer: {result} ✓")
        else:
            sum_value = num1 + num2
            steps.append(f"Problem: √({num1}+{num2})")
            steps.append("")
            steps.append("IMPORTANT: Square root does NOT distribute over addition")
            steps.append(f"  √(a+b) ≠ √a + √b")
            steps.append("")
            steps.append(f"Step 1: Add inside the radical first")
            steps.append(f"  {num1} + {num2} = {sum_value}")
            steps.append("")
            steps.append(f"Step 2: Take square root of the sum")
            steps.append(f"  √{sum_value} = {result}")
            steps.append("")
            steps.append(f"Final Answer: {result} ✓")
        return steps

    def _generate_concise_sqrt_sum_steps(self, problem_text: str, num1: int, num2: int, is_pythagorean: bool, result: float) -> List[str]:
        """Generate concise steps for sqrt sum computation."""
        steps = []
        steps.append(problem_text)
        if is_pythagorean:
            sum_of_squares = num1**2 + num2**2
            steps.append(f"√({num1}²+{num2}²)")
            steps.append(f"{num1}² = {num1**2}")
            steps.append(f"{num2}² = {num2**2}")
            steps.append(f"{num1**2} + {num2**2} = {sum_of_squares}")
            steps.append(f"√{sum_of_squares} = {result}")
        else:
            sum_value = num1 + num2
            steps.append(f"√({num1}+{num2})")
            steps.append(f"{num1} + {num2} = {sum_value}")
            steps.append(f"√{sum_value} = {result}")
        return steps

    def _parse_square_binomial(self, expression: str) -> Optional[Tuple[str, int, bool]]:
        """
        Parse expressions like (x+3)², (x-5)², (y+7)²
        Returns: (variable, constant, is_subtraction) or None
        """
        # Pattern: (var±num)²
        pattern = r'\(([a-z])([+\-])(\d+)\)²'
        match = re.match(pattern, expression)
        if match:
            var = match.group(1)
            sign = match.group(2)
            num = int(match.group(3))
            is_subtraction = (sign == '-')
            return (var, num, is_subtraction)
        return None

    def _parse_sqrt_sum(self, expression: str) -> Optional[Tuple[int, int, bool]]:
        """
        Parse expressions like √(9+16), √(3²+4²)
        Returns: (num1, num2, is_pythagorean) or None
        """
        # Pattern 1: √(a²+b²) - Pythagorean form
        pattern_pyth = r'√\((\d+)²\+(\d+)²\)'
        match = re.match(pattern_pyth, expression)
        if match:
            num1 = int(match.group(1))
            num2 = int(match.group(2))
            return (num1, num2, True)

        # Pattern 2: √(a+b) - Simple sum
        pattern_sum = r'√\((\d+)\+(\d+)\)'
        match = re.match(pattern_sum, expression)
        if match:
            num1 = int(match.group(1))
            num2 = int(match.group(2))
            return (num1, num2, False)

        return None

    def _expand_square_binomial(self, var: str, constant: int, is_subtraction: bool) -> Tuple[str, List[str]]:
        """
        Correctly expand (x+a)² or (x-a)²
        (x+a)² = x² + 2ax + a²
        (x-a)² = x² - 2ax + a²
        """
        steps = []

        if is_subtraction:
            steps.append(f"Problem: ({var}-{constant})²")
            steps.append("")
            steps.append("Expand using: (a-b)² = a² - 2ab + b²")
            steps.append("")
            steps.append(f"Where a = {var} and b = {constant}")
            steps.append("")
            steps.append(f"Step 1: {var}² (first term squared)")
            steps.append(f"Step 2: -2·{var}·{constant} = -{2*constant}{var} (middle term)")
            steps.append(f"Step 3: {constant}² = {constant**2} (last term squared)")
            steps.append("")

            # Build result string: x² - 2ax + a²
            result_str = f"{var}² - {2*constant}{var} + {constant**2}"
        else:
            steps.append(f"Problem: ({var}+{constant})²")
            steps.append("")
            steps.append("Expand using: (a+b)² = a² + 2ab + b²")
            steps.append("")
            steps.append(f"Where a = {var} and b = {constant}")
            steps.append("")
            steps.append(f"Step 1: {var}² (first term squared)")
            steps.append(f"Step 2: 2·{var}·{constant} = {2*constant}{var} (middle term)")
            steps.append(f"Step 3: {constant}² = {constant**2} (last term squared)")
            steps.append("")

            # Build result string: x² + 2ax + a²
            result_str = f"{var}² + {2*constant}{var} + {constant**2}"

        steps.append(f"Combine: {result_str}")
        steps.append("")
        steps.append(f"Final Answer: {result_str} ✓")

        return result_str, steps

    def _compute_sqrt_sum(self, num1: int, num2: int, is_pythagorean: bool) -> Tuple[float, List[str]]:
        """
        Correctly compute √(a+b) or √(a²+b²)
        """
        steps = []

        if is_pythagorean:
            # √(a²+b²)
            sum_of_squares = num1**2 + num2**2
            result = round(sum_of_squares ** 0.5, 2)

            steps.append(f"Problem: √({num1}²+{num2}²)")
            steps.append("")
            steps.append("IMPORTANT: Square root does NOT distribute over addition")
            steps.append(f"  √(a²+b²) ≠ √a² + √b²")
            steps.append("")
            steps.append(f"Step 1: Calculate squares inside the radical")
            steps.append(f"  {num1}² = {num1**2}")
            steps.append(f"  {num2}² = {num2**2}")
            steps.append("")
            steps.append(f"Step 2: Add the squares")
            steps.append(f"  {num1**2} + {num2**2} = {sum_of_squares}")
            steps.append("")
            steps.append(f"Step 3: Take square root of the sum")
            steps.append(f"  √{sum_of_squares} = {result}")
            steps.append("")
            steps.append(f"Final Answer: {result} ✓")
        else:
            # √(a+b)
            sum_value = num1 + num2
            result = round(sum_value ** 0.5, 2)

            steps.append(f"Problem: √({num1}+{num2})")
            steps.append("")
            steps.append("IMPORTANT: Square root does NOT distribute over addition")
            steps.append(f"  √(a+b) ≠ √a + √b")
            steps.append("")
            steps.append(f"Step 1: Add inside the radical first")
            steps.append(f"  {num1} + {num2} = {sum_value}")
            steps.append("")
            steps.append(f"Step 2: Take square root of the sum")
            steps.append(f"  √{sum_value} = {result}")
            steps.append("")
            steps.append(f"Final Answer: {result} ✓")

        return result, steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        operation = problem.metadata['operation']
        expression = problem.metadata.get('expression', '')

        if operation == 'square_binomial':
            # Parse and expand binomial square
            parsed = self._parse_square_binomial(expression)
            if parsed:
                var, constant, is_subtraction = parsed
            else:
                # Fallback to metadata if parsing fails
                var = problem.metadata['variable']
                constant = problem.metadata['constant']
                is_subtraction = problem.metadata.get('is_subtraction', False)

            # Calculate result
            if is_subtraction:
                result_str = f"{var}² - {2*constant}{var} + {constant**2}"
            else:
                result_str = f"{var}² + {2*constant}{var} + {constant**2}"

            # Generate steps based on verbose flag
            if verbose:
                steps = self._generate_verbose_square_binomial_steps(var, constant, is_subtraction, result_str)
            else:
                steps = self._generate_concise_square_binomial_steps(problem.text, var, constant, is_subtraction, result_str)

            return Solution(
                answer=result_str,
                steps=steps,
                is_correct=True,
                algorithm_name=self.get_name()
            )

        else:  # sqrt_sum
            # Parse and compute square root
            parsed = self._parse_sqrt_sum(expression)
            if parsed:
                num1, num2, is_pythagorean = parsed
            else:
                # Fallback to metadata if parsing fails
                num1 = problem.metadata['num1']
                num2 = problem.metadata['num2']
                is_pythagorean = problem.metadata.get('is_pythagorean', False)

            # Calculate result
            if is_pythagorean:
                sum_of_squares = num1**2 + num2**2
                result = round(sum_of_squares ** 0.5, 2)
            else:
                sum_value = num1 + num2
                result = round(sum_value ** 0.5, 2)

            # Generate steps based on verbose flag
            if verbose:
                steps = self._generate_verbose_sqrt_sum_steps(num1, num2, is_pythagorean, result)
            else:
                steps = self._generate_concise_sqrt_sum_steps(problem.text, num1, num2, is_pythagorean, result)

            return Solution(
                answer=result,
                steps=steps,
                is_correct=True,
                algorithm_name=self.get_name()
            )
