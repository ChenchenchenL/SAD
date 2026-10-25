"""
Malrule algorithm for Ignore-Denominators error.

Students operate only on numerators, completely ignoring denominators.
They treat the problem as whole number arithmetic.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class IgnoreDenominatorsMalrule(Malrule):
    """
    Implements the Ignore-Denominators malrule.

    Students ignore denominators completely and only operate on numerators,
    treating the fraction operation as simple whole number arithmetic.

    Example: 2/3 + 1/5
    Correct: Find common denominator → 10/15 + 3/15 = 13/15
    Malrule: Ignore denominators → 2 + 1 = 3 (just adds numerators)
    """

    def get_name(self) -> str:
        return "Ignore-Denominators"

    def get_description(self) -> str:
        return (
            "Students operate only on numerators, completely ignoring denominators, "
            "treating fraction operations as whole-number arithmetic on the 'top numbers' "
            "only. For example: 2/3 + 1/5 = 3 (just adds 2+1). This error reflects a "
            "fundamental failure to understand that a fraction is a single number with "
            "magnitude, not two separate numbers. Research shows this stems from students "
            "processing 'numerator and denominator as two separate whole numbers' "
            "(Pitkethly & Hunting, 1996; Nunes & Bryant, 1996)."
        )

    def calculate_expected_answer(self, problem: Problem) -> str:
        """
        Calculate the expected incorrect answer for this malrule.

        For Ignore-Denominators:
        - Student completely ignores denominators
        - Only operates on numerators
        - MALRULE: num1 (operation) num2 (just the result, no fraction)

        Example: 2/3 + 1/5
        - Correct: 10/15 + 3/15 = 13/15
        - MALRULE: 2 + 1 = 3 (ignores denominators)

        Example: 5/8 - 2/3
        - Correct: 15/24 - 16/24 = -1/24
        - MALRULE: 5 - 2 = 3 (ignores denominators)

        Example: 2/3 × 4/5
        - Correct: 8/15
        - MALRULE: 2 × 4 = 8 (ignores denominators)

        Example: 3/4 ÷ 2/5
        - Correct: 15/8
        - MALRULE: 3 ÷ 2 = 1 (ignores denominators, integer division)

        Args:
            problem: Fraction problem

        Returns:
            Expected incorrect answer as string (just the numerator result)
        """
        # Parse operands from problem.operands: [num1, den1, num2, den2]
        if len(problem.operands) >= 4:
            num1, num2 = problem.operands[0], problem.operands[2]
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
            operation = 'addition'  # Default

        # MALRULE: Only operate on numerators, ignore denominators
        if operation == 'addition':
            result = num1 + num2
        elif operation == 'subtraction':
            result = num1 - num2
        elif operation == 'multiplication':
            result = num1 * num2
        elif operation == 'division':
            # Integer division (student just divides numerators)
            result = num1 // num2 if num2 != 0 else num1
        else:
            result = num1 + num2  # Default to addition

        return str(result)

    def _generate_concise_steps(self, problem: Problem, num1: int, den1: int, num2: int, den2: int,
                                 operation: str, op_symbol: str, result: int) -> list:
        """
        Generate concise steps for the malrule solution.

        Returns a list: [Question, step1, step2, ..., answer]
        """
        steps = []

        # Question
        steps.append(problem.text)

        # Formula extraction
        steps.append(f"{num1}/{den1} {op_symbol} {num2}/{den2}")

        # Operation on numerators only
        if operation == 'addition':
            steps.append(f"{num1} + {num2} = {result}")
        elif operation == 'subtraction':
            steps.append(f"{num1} - {num2} = {result}")
        elif operation == 'multiplication':
            steps.append(f"{num1} × {num2} = {result}")
        elif operation == 'division':
            steps.append(f"{num1} ÷ {num2} = {result}")

        # Final answer
        steps.append(str(result))

        return steps

    def _generate_verbose_steps(self, problem: Problem, num1: int, den1: int, num2: int, den2: int,
                                 operation: str, op_symbol: str, result: int) -> list:
        """
        Generate verbose steps for the malrule solution (original step format).
        """
        steps = []

        steps.append(f"Problem: {num1}/{den1} {op_symbol} {num2}/{den2}")
        steps.append("")

        # MALRULE: Only operate on numerators, ignore denominators
        steps.append("MALRULE: Ignore denominators, just operate on numerators")
        steps.append(f"  Look at top numbers: {num1} and {num2}")
        steps.append(f"  Bottom numbers don't matter, just focus on tops")
        steps.append("")

        if operation == 'addition':
            steps.append(f"Step 1: Add numerators")
            steps.append(f"  {num1} + {num2} = {result}")
            steps.append(f"  MALRULE REASONING: 'Just add the top numbers'")
        elif operation == 'subtraction':
            steps.append(f"Step 1: Subtract numerators")
            steps.append(f"  {num1} - {num2} = {result}")
            steps.append(f"  MALRULE REASONING: 'Just subtract the top numbers'")
        elif operation == 'multiplication':
            steps.append(f"Step 1: Multiply numerators")
            steps.append(f"  {num1} × {num2} = {result}")
            steps.append(f"  MALRULE REASONING: 'Just multiply the top numbers'")
        elif operation == 'division':
            steps.append(f"Step 1: Divide numerators")
            steps.append(f"  {num1} ÷ {num2} = {result}")
            steps.append(f"  MALRULE REASONING: 'Just divide the top numbers'")

        steps.append("")
        steps.append(f"Final Answer: {result} (ignoring denominators)")
        steps.append("(INCORRECT - denominators matter!)")

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the ignore-denominators malrule.

        Students only operate on numerators, ignoring denominators.

        Args:
            problem: Problem instance with fraction operands
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with incorrect answer and student's reasoning
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
            operation = 'addition'  # Default

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

        # MALRULE: Only operate on numerators, ignore denominators
        if operation == 'addition':
            result = num1 + num2
        elif operation == 'subtraction':
            result = num1 - num2
        elif operation == 'multiplication':
            result = num1 * num2
        elif operation == 'division':
            result = num1 // num2 if num2 != 0 else num1
        else:
            result = num1 + num2

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(
                problem, num1, den1, num2, den2, operation, op_symbol, result
            )
        else:
            steps = self._generate_concise_steps(
                problem, num1, den1, num2, den2, operation, op_symbol, result
            )

        return Solution(
            answer=str(result),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
