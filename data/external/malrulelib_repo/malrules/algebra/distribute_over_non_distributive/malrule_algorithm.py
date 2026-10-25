"""
Malrule algorithm for Distribute-Over-Non-Distributive.
This version actually parses and computes the INCORRECT expansion without using metadata answers.

Students incorrectly apply distributive property to non-distributive operations.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import re
from typing import Dict, Any, List, Tuple, Optional
from utils import Malrule, Problem, Solution

class DistributeOverNonDistributiveMalrule(Malrule):
    """Incorrectly distributes operations over non-distributive cases."""

    def get_name(self) -> str:
        return "Distribute-Over-Non-Distributive Malrule"

    def get_description(self) -> str:
        return (
            "Students incorrectly extend the distributive property to operations that "
            "do not distribute, such as exponentiation and square roots. This overgeneralization "
            "leads to errors like (a+b)² = a² + b² (missing the middle term) and "
            "√(a+b) = √a + √b (incorrectly distributing the square root)."
        )

    def _generate_verbose_square_binomial_steps(self, var: str, constant: int, is_subtraction: bool, result_str: str) -> List[str]:
        """Generate verbose steps for malrule square binomial expansion."""
        steps = []
        if is_subtraction:
            steps.append(f"Problem: ({var}-{constant})²")
            steps.append("")
            steps.append("MALRULE: Distribute the square")
            steps.append(f"  ({var}-{constant})² = {var}² + {constant}²")
            steps.append(f"  MALRULE REASONING: 'Square distributes over subtraction'")
            steps.append("")
            steps.append(f"Calculate: {var}²")
            steps.append(f"Calculate: {constant}² = {constant**2}")
            steps.append("")
            steps.append(f"Expanding: {var}² + {constant**2}")
            steps.append("")
            steps.append(f"Final Answer: {var}² + {constant**2} ✗")
            steps.append(f"(INCORRECT: Missing middle term -{2*constant}{var})")
        else:
            steps.append(f"Problem: ({var}+{constant})²")
            steps.append("")
            steps.append("MALRULE: Distribute the square")
            steps.append(f"  ({var}+{constant})² = {var}² + {constant}²")
            steps.append(f"  MALRULE REASONING: 'Square distributes over addition'")
            steps.append("")
            steps.append(f"Calculate: {var}²")
            steps.append(f"Calculate: {constant}² = {constant**2}")
            steps.append("")
            steps.append(f"Expanding: {var}² + {constant**2}")
            steps.append("")
            steps.append(f"Final Answer: {var}² + {constant**2} ✗")
            steps.append(f"(INCORRECT: Missing middle term {2*constant}{var})")
        return steps

    def _generate_concise_square_binomial_steps(self, problem_text: str, var: str, constant: int, is_subtraction: bool, result_str: str) -> List[str]:
        """Generate concise steps for malrule square binomial expansion."""
        steps = []
        steps.append(problem_text)
        if is_subtraction:
            steps.append(f"({var}-{constant})²")
            steps.append(f"({var}-{constant})² = {var}² + {constant}²")
            steps.append(f"{var}²")
            steps.append(f"{constant}² = {constant**2}")
            steps.append(f"{result_str}")
        else:
            steps.append(f"({var}+{constant})²")
            steps.append(f"({var}+{constant})² = {var}² + {constant}²")
            steps.append(f"{var}²")
            steps.append(f"{constant}² = {constant**2}")
            steps.append(f"{result_str}")
        return steps

    def _generate_verbose_sqrt_sum_steps(self, num1: int, num2: int, is_pythagorean: bool, result) -> List[str]:
        """Generate verbose steps for malrule sqrt sum computation."""
        steps = []
        if is_pythagorean:
            steps.append(f"Problem: √({num1}²+{num2}²)")
            steps.append("")
            steps.append("MALRULE: Distribute the square root")
            steps.append(f"  √({num1}²+{num2}²) = √{num1}² + √{num2}²")
            steps.append(f"  MALRULE REASONING: 'Square root distributes over addition'")
            steps.append("")
            steps.append(f"Calculate: √{num1}² = {num1}")
            steps.append(f"Calculate: √{num2}² = {num2}")
            steps.append(f"Add: {num1} + {num2} = {result}")
            steps.append("")
            steps.append(f"Final Answer: {result} ✗")
            correct = round((num1**2 + num2**2) ** 0.5, 2)
            steps.append(f"(INCORRECT: Should be {correct})")
        else:
            sqrt1 = round(num1 ** 0.5, 2)
            sqrt2 = round(num2 ** 0.5, 2)
            steps.append(f"Problem: √({num1}+{num2})")
            steps.append("")
            steps.append("MALRULE: Distribute the square root")
            steps.append(f"  √({num1}+{num2}) = √{num1} + √{num2}")
            steps.append(f"  MALRULE REASONING: 'Square root distributes over addition'")
            steps.append("")
            steps.append(f"Calculate: √{num1} = {sqrt1}")
            steps.append(f"Calculate: √{num2} = {sqrt2}")
            steps.append(f"Add: {sqrt1} + {sqrt2} = {result}")
            steps.append("")
            steps.append(f"Final Answer: {result} ✗")
            correct = round((num1 + num2) ** 0.5, 2)
            steps.append(f"(INCORRECT: Should be {correct})")
        return steps

    def _generate_concise_sqrt_sum_steps(self, problem_text: str, num1: int, num2: int, is_pythagorean: bool, result) -> List[str]:
        """Generate concise steps for malrule sqrt sum computation."""
        steps = []
        steps.append(problem_text)
        if is_pythagorean:
            steps.append(f"√({num1}²+{num2}²)")
            steps.append(f"√({num1}²+{num2}²) = √{num1}² + √{num2}²")
            steps.append(f"√{num1}² = {num1}")
            steps.append(f"√{num2}² = {num2}")
            steps.append(f"{num1} + {num2} = {result}")
        else:
            sqrt1 = round(num1 ** 0.5, 2)
            sqrt2 = round(num2 ** 0.5, 2)
            steps.append(f"√({num1}+{num2})")
            steps.append(f"√({num1}+{num2}) = √{num1} + √{num2}")
            steps.append(f"√{num1} = {sqrt1}")
            steps.append(f"√{num2} = {sqrt2}")
            steps.append(f"{sqrt1} + {sqrt2} = {result}")
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

    def _expand_square_binomial_malrule(self, var: str, constant: int, is_subtraction: bool) -> Tuple[str, List[str]]:
        """
        INCORRECTLY expand (x+a)² or (x-a)²
        Malrule: (x+a)² = x² + a² (missing middle term)
        Malrule: (x-a)² = x² + a² (missing middle term)
        """
        steps = []

        if is_subtraction:
            steps.append(f"Problem: ({var}-{constant})²")
            steps.append("")
            steps.append("MALRULE: Distribute the square")
            steps.append(f"  ({var}-{constant})² = {var}² + {constant}²")
            steps.append(f"  MALRULE REASONING: 'Square distributes over subtraction'")
            steps.append("")
            steps.append(f"Calculate: {var}²")
            steps.append(f"Calculate: {constant}² = {constant**2}")
            steps.append("")
            steps.append(f"Expanding: {var}² + {constant**2}")
            steps.append("")
            steps.append(f"Final Answer: {var}² + {constant**2} ✗")
            steps.append(f"(INCORRECT: Missing middle term -{2*constant}{var})")

            # Malrule result: x² + a² (same for both + and -)
            result_str = f"{var}² + {constant**2}"
        else:
            steps.append(f"Problem: ({var}+{constant})²")
            steps.append("")
            steps.append("MALRULE: Distribute the square")
            steps.append(f"  ({var}+{constant})² = {var}² + {constant}²")
            steps.append(f"  MALRULE REASONING: 'Square distributes over addition'")
            steps.append("")
            steps.append(f"Calculate: {var}²")
            steps.append(f"Calculate: {constant}² = {constant**2}")
            steps.append("")
            steps.append(f"Expanding: {var}² + {constant**2}")
            steps.append("")
            steps.append(f"Final Answer: {var}² + {constant**2} ✗")
            steps.append(f"(INCORRECT: Missing middle term {2*constant}{var})")

            # Malrule result: x² + a²
            result_str = f"{var}² + {constant**2}"

        return result_str, steps

    def _compute_sqrt_sum_malrule(self, num1: int, num2: int, is_pythagorean: bool) -> Tuple[float, List[str]]:
        """
        INCORRECTLY compute √(a+b) or √(a²+b²)
        Malrule: √(a+b) = √a + √b
        Malrule: √(a²+b²) = √a² + √b² = a + b
        """
        steps = []

        if is_pythagorean:
            # Malrule: √(a²+b²) = √a² + √b² = a + b
            result = num1 + num2

            steps.append(f"Problem: √({num1}²+{num2}²)")
            steps.append("")
            steps.append("MALRULE: Distribute the square root")
            steps.append(f"  √({num1}²+{num2}²) = √{num1}² + √{num2}²")
            steps.append(f"  MALRULE REASONING: 'Square root distributes over addition'")
            steps.append("")
            steps.append(f"Calculate: √{num1}² = {num1}")
            steps.append(f"Calculate: √{num2}² = {num2}")
            steps.append(f"Add: {num1} + {num2} = {result}")
            steps.append("")
            steps.append(f"Final Answer: {result} ✗")

            # Correct answer for comparison
            correct = round((num1**2 + num2**2) ** 0.5, 2)
            steps.append(f"(INCORRECT: Should be {correct})")
        else:
            # Malrule: √(a+b) = √a + √b
            sqrt1 = round(num1 ** 0.5, 2)
            sqrt2 = round(num2 ** 0.5, 2)
            result = round(sqrt1 + sqrt2, 2)

            steps.append(f"Problem: √({num1}+{num2})")
            steps.append("")
            steps.append("MALRULE: Distribute the square root")
            steps.append(f"  √({num1}+{num2}) = √{num1} + √{num2}")
            steps.append(f"  MALRULE REASONING: 'Square root distributes over addition'")
            steps.append("")
            steps.append(f"Calculate: √{num1} = {sqrt1}")
            steps.append(f"Calculate: √{num2} = {sqrt2}")
            steps.append(f"Add: {sqrt1} + {sqrt2} = {result}")
            steps.append("")
            steps.append(f"Final Answer: {result} ✗")

            # Correct answer for comparison
            correct = round((num1 + num2) ** 0.5, 2)
            steps.append(f"(INCORRECT: Should be {correct})")

        return result, steps

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        operation = problem.metadata['operation']
        expression = problem.metadata.get('expression', '')

        if operation == 'square_binomial':
            # Parse and expand with malrule
            parsed = self._parse_square_binomial(expression)
            if parsed:
                var, constant, is_subtraction = parsed
            else:
                # Fallback to metadata
                var = problem.metadata['variable']
                constant = problem.metadata['constant']
                is_subtraction = problem.metadata.get('is_subtraction', False)

            # Malrule: (x+a)² = x² + a² (missing middle term)
            return f"{var}² + {constant**2}"

        else:  # sqrt_sum
            # Parse and compute with malrule
            parsed = self._parse_sqrt_sum(expression)
            if parsed:
                num1, num2, is_pythagorean = parsed
            else:
                # Fallback to metadata
                num1 = problem.metadata['num1']
                num2 = problem.metadata['num2']
                is_pythagorean = problem.metadata.get('is_pythagorean', False)

            if is_pythagorean:
                # Malrule: √(a²+b²) = a + b
                return num1 + num2
            else:
                # Malrule: √(a+b) = √a + √b
                sqrt1 = round(num1 ** 0.5, 2)
                sqrt2 = round(num2 ** 0.5, 2)
                return round(sqrt1 + sqrt2, 2)

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply the distribute-over-non-distributive malrule."""
        operation = problem.metadata['operation']
        expression = problem.metadata.get('expression', '')

        if operation == 'square_binomial':
            # Parse and expand with malrule
            parsed = self._parse_square_binomial(expression)
            if parsed:
                var, constant, is_subtraction = parsed
            else:
                # Fallback to metadata if parsing fails
                var = problem.metadata['variable']
                constant = problem.metadata['constant']
                is_subtraction = problem.metadata.get('is_subtraction', False)

            # Calculate result
            result_str = f"{var}² + {constant**2}"

            # Generate steps based on verbose flag
            if verbose:
                steps = self._generate_verbose_square_binomial_steps(var, constant, is_subtraction, result_str)
            else:
                steps = self._generate_concise_square_binomial_steps(problem.text, var, constant, is_subtraction, result_str)

            return Solution(
                answer=result_str,
                steps=steps,
                is_correct=False,
                algorithm_name=self.get_name()
            )

        else:  # sqrt_sum
            # Parse and compute with malrule
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
                result = num1 + num2
            else:
                sqrt1 = round(num1 ** 0.5, 2)
                sqrt2 = round(num2 ** 0.5, 2)
                result = round(sqrt1 + sqrt2, 2)

            # Generate steps based on verbose flag
            if verbose:
                steps = self._generate_verbose_sqrt_sum_steps(num1, num2, is_pythagorean, result)
            else:
                steps = self._generate_concise_sqrt_sum_steps(problem.text, num1, num2, is_pythagorean, result)

            return Solution(
                answer=result,
                steps=steps,
                is_correct=False,
                algorithm_name=self.get_name()
            )
