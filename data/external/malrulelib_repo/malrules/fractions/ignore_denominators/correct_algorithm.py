"""
Correct algorithm for all fraction operations.

Implements proper methods for adding, subtracting, multiplying, and dividing fractions.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from math import gcd
from utils import CorrectAlgorithm, Problem, Solution


class FractionCorrectAlgorithm(CorrectAlgorithm):
    """
    Implements correct fraction operations for all basic operations.

    Properly handles addition, subtraction (with common denominators),
    multiplication, and division of fractions, with simplification.
    """

    def get_name(self) -> str:
        return "Correct Fraction Operations"

    def get_description(self) -> str:
        return (
            "Standard algorithm for fraction operations: "
            "Addition/Subtraction (find LCD, convert fractions, operate, simplify), "
            "Multiplication (multiply numerators and denominators, simplify), "
            "Division (flip and multiply, simplify)."
        )

    def _generate_concise_steps(self, problem: Problem, num1: int, den1: int, num2: int, den2: int,
                                 operation: str, op_symbol: str, result_num: int, result_den: int,
                                 simplified_num: int, simplified_den: int) -> list:
        """
        Generate concise steps for the solution.

        Returns a list: [Question, step1, step2, ..., answer]
        """
        steps = []

        # Question
        steps.append(problem.text)

        # Formula extraction
        steps.append(f"{num1}/{den1} {op_symbol} {num2}/{den2}")

        if operation in ['addition', 'subtraction']:
            lcm = (den1 * den2) // gcd(den1, den2)
            mult1 = lcm // den1
            mult2 = lcm // den2
            new_num1 = num1 * mult1
            new_num2 = num2 * mult2

            # LCD step
            steps.append(f"LCM({den1}, {den2}) = {lcm}")

            # Convert fractions step
            steps.append(f"{new_num1}/{lcm} {op_symbol} {new_num2}/{lcm}")

            # Operation step
            if operation == 'addition':
                steps.append(f"{new_num1} + {new_num2} = {result_num}")
            else:
                steps.append(f"{new_num1} - {new_num2} = {result_num}")

            # Result step
            steps.append(f"{result_num}/{lcm}")

        elif operation == 'multiplication':
            # Multiply step
            steps.append(f"{num1} × {num2} = {result_num}")
            steps.append(f"{den1} × {den2} = {result_den}")
            steps.append(f"{result_num}/{result_den}")

        elif operation == 'division':
            # Flip and multiply step
            steps.append(f"{num1}/{den1} × {den2}/{num2}")
            steps.append(f"{num1} × {den2} = {result_num}")
            steps.append(f"{den1} × {num2} = {result_den}")
            steps.append(f"{result_num}/{result_den}")

        # Simplify step if needed
        if simplified_num != result_num or simplified_den != result_den:
            steps.append(f"{simplified_num}/{simplified_den}")

        # Final answer
        steps.append(f"{simplified_num}/{simplified_den}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, num1: int, den1: int, num2: int, den2: int,
                                 operation: str, op_symbol: str, result_num: int, result_den: int,
                                 simplified_num: int, simplified_den: int) -> list:
        """
        Generate verbose steps for the solution (original step format).
        """
        steps = []

        steps.append(f"Problem: {num1}/{den1} {op_symbol} {num2}/{den2}")
        steps.append("")

        if operation in ['addition', 'subtraction']:
            lcm = (den1 * den2) // gcd(den1, den2)
            mult1 = lcm // den1
            mult2 = lcm // den2
            new_num1 = num1 * mult1
            new_num2 = num2 * mult2

            # Step 1: Find common denominator
            steps.append("Step 1: Find common denominator")
            steps.append(f"  LCM of {den1} and {den2} is {lcm}")
            steps.append("")

            # Step 2: Convert fractions
            steps.append("Step 2: Convert fractions to common denominator")
            steps.append(f"  {num1}/{den1} = {num1}/{den1} × {mult1}/{mult1} = {new_num1}/{lcm}")
            steps.append(f"  {num2}/{den2} = {num2}/{den2} × {mult2}/{mult2} = {new_num2}/{lcm}")
            steps.append("")

            # Step 3: Perform operation
            steps.append(f"Step 3: {operation.capitalize()} numerators")
            if operation == 'addition':
                steps.append(f"  {new_num1}/{lcm} + {new_num2}/{lcm} = ({new_num1} + {new_num2})/{lcm} = {result_num}/{lcm}")
            else:  # subtraction
                steps.append(f"  {new_num1}/{lcm} - {new_num2}/{lcm} = ({new_num1} - {new_num2})/{lcm} = {result_num}/{lcm}")
            steps.append("")

        elif operation == 'multiplication':
            # Step 1: Multiply numerators and denominators
            steps.append("Step 1: Multiply numerators and denominators")
            steps.append(f"  ({num1} × {num2}) / ({den1} × {den2}) = {result_num}/{result_den}")
            steps.append("")

        elif operation == 'division':
            # Step 1: Flip second fraction and multiply
            steps.append("Step 1: Flip the second fraction and multiply")
            steps.append(f"  {num1}/{den1} ÷ {num2}/{den2} = {num1}/{den1} × {den2}/{num2}")
            steps.append("")

            # Step 2: Multiply
            steps.append("Step 2: Multiply numerators and denominators")
            steps.append(f"  ({num1} × {den2}) / ({den1} × {num2}) = {result_num}/{result_den}")
            steps.append("")

        # Final Step: Simplify
        steps.append(f"Step {3 if operation in ['addition', 'subtraction'] else 3}: Simplify")
        result_gcd = gcd(abs(result_num), result_den)
        if result_gcd > 1:
            steps.append(f"  GCD of {abs(result_num)} and {result_den} is {result_gcd}")
            steps.append(f"  {result_num}/{result_den} ÷ {result_gcd}/{result_gcd} = {simplified_num}/{simplified_den}")
        else:
            steps.append(f"  Fraction is already in simplest form")

        steps.append("")
        steps.append(f"Final Answer: {simplified_num}/{simplified_den}")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct fraction operations.

        Args:
            problem: Problem instance with fraction operands
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with correct answer and detailed steps
        """
        # Parse operands from problem.operands: [num1, den1, num2, den2]
        if len(problem.operands) >= 4:
            num1, den1, num2, den2 = problem.operands[0], problem.operands[1], problem.operands[2], problem.operands[3]
        else:
            raise ValueError(f"Expected at least 4 operands, got {len(problem.operands)}")

        # Determine operation from problem.operation or metadata
        if 'operation' in problem.metadata:
            operation = problem.metadata['operation']
        elif 'addition' in problem.operation:
            operation = 'addition'
        elif 'subtraction' in problem.operation:
            operation = 'subtraction'
        elif 'multiplication' in problem.operation:
            operation = 'multiplication'
        elif 'division' in problem.operation:
            operation = 'division'
        else:
            raise ValueError(f"Unknown operation: {problem.operation}")

        # Determine operation symbol
        if operation == 'addition':
            op_symbol = '+'
        elif operation == 'subtraction':
            op_symbol = '-'
        elif operation == 'multiplication':
            op_symbol = '×'
        elif operation == 'division':
            op_symbol = '÷'
        else:
            op_symbol = '+'

        # Calculate result based on operation
        if operation in ['addition', 'subtraction']:
            lcm = (den1 * den2) // gcd(den1, den2)
            mult1 = lcm // den1
            mult2 = lcm // den2
            new_num1 = num1 * mult1
            new_num2 = num2 * mult2

            if operation == 'addition':
                result_num = new_num1 + new_num2
            else:  # subtraction
                result_num = new_num1 - new_num2

            result_den = lcm

        elif operation == 'multiplication':
            result_num = num1 * num2
            result_den = den1 * den2

        elif operation == 'division':
            result_num = num1 * den2
            result_den = den1 * num2

        # Simplify
        result_gcd = gcd(abs(result_num), result_den)
        if result_gcd > 1:
            simplified_num = result_num // result_gcd
            simplified_den = result_den // result_gcd
        else:
            simplified_num = result_num
            simplified_den = result_den

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(
                problem, num1, den1, num2, den2, operation, op_symbol,
                result_num, result_den, simplified_num, simplified_den
            )
        else:
            steps = self._generate_concise_steps(
                problem, num1, den1, num2, den2, operation, op_symbol,
                result_num, result_den, simplified_num, simplified_den
            )

        return Solution(
            answer=f"{simplified_num}/{simplified_den}",
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
