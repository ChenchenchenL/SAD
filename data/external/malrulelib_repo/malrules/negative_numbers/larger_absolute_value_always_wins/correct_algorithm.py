"""
Correct algorithm for negative number operations.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import re
from typing import List, Tuple, Dict, Any
from utils import CorrectAlgorithm, Problem, Solution


class NegativeNumbersCorrectAlgorithm(CorrectAlgorithm):
    """
    Implements correct negative number addition and subtraction.
    """

    def get_name(self) -> str:
        return "Correct Negative Number Operations"

    def get_description(self) -> str:
        return (
            "Correctly performs operations with negative numbers by "
            "properly applying sign rules based on the operation."
        )

    def _generate_concise_steps(self, problem: Problem, num1: int, num2: int,
                                 op_symbol: str, result: int,
                                 intermediate_data: Dict[str, Any]) -> List[str]:
        """
        Generate concise steps for the solution.

        Format: [Question, step (formula/values only), ..., answer]
        """
        steps = []

        # Question (extract from word problem or use expression)
        if problem.metadata and problem.metadata.get('template') == 'word_problem':
            steps.append(f"Question: {problem.text}")
            steps.append(f"{num1} {op_symbol} ({num2})")
        else:
            steps.append(f"Question: {num1} {op_symbol} {num2}")

        # Handle different operations with concise steps
        if op_symbol == 'compare':
            steps.append(f"|{num1}| = {abs(num1)}, |{num2}| = {abs(num2)}")
            steps.append(f"max({num1}, {num2}) = {result}")
        elif op_symbol == '×':
            steps.append(f"|{num1}| × |{num2}| = {abs(num1)} × {abs(num2)} = {abs(num1) * abs(num2)}")
            steps.append(f"Sign: {'+' if result >= 0 else '-'}")
            steps.append(f"Result: {result}")
        elif op_symbol == '÷':
            steps.append(f"|{num1}| ÷ |{num2}| = {abs(num1)} ÷ {abs(num2)} = {abs(num1) // abs(num2)}")
            steps.append(f"Sign: {'+' if result >= 0 else '-'}")
            steps.append(f"Result: {result}")
        elif op_symbol == '+':
            if num1 < 0 and num2 < 0:
                steps.append(f"|{num1}| + |{num2}| = {abs(num1)} + {abs(num2)} = {abs(num1) + abs(num2)}")
                steps.append(f"Both negative: -{abs(num1) + abs(num2)} = {result}")
            elif (num1 > 0 and num2 < 0) or (num1 < 0 and num2 > 0):
                steps.append(f"|{abs(num1)} - {abs(num2)}| = {abs(abs(num1) - abs(num2))}")
                steps.append(f"Result: {result}")
            else:
                steps.append(f"{num1} + {num2} = {result}")
        else:  # subtraction
            num2_opposite = -num2
            steps.append(f"{num1} - ({num2}) = {num1} + ({num2_opposite})")
            steps.append(f"Result: {result}")

        # Final answer
        steps.append(f"Answer: {result}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, num1: int, num2: int,
                                 op_symbol: str, result: int,
                                 intermediate_data: Dict[str, Any]) -> List[str]:
        """
        Generate verbose steps for the solution (original step structure).
        """
        steps = []
        steps.append(f"Problem: {num1} {op_symbol} {num2}")
        steps.append("")

        # Handle comparison operation
        if op_symbol == 'compare':
            steps.append("Step 1: Compare the two numbers")
            steps.append(f"  Comparing {num1} and {num2}")

            if num1 > 0 and num2 < 0:
                steps.append(f"  {num1} is positive, {num2} is negative")
                steps.append(f"  Positive numbers are always greater than negative numbers")
            elif num1 < 0 and num2 > 0:
                steps.append(f"  {num1} is negative, {num2} is positive")
                steps.append(f"  Positive numbers are always greater than negative numbers")
            elif num1 < 0 and num2 < 0:
                steps.append(f"  Both numbers are negative")
                steps.append(f"  For negative numbers, the one closer to zero is greater")
                steps.append(f"  |{num1}| = {abs(num1)}, |{num2}| = {abs(num2)}")
                steps.append(f"  Smaller absolute value means greater number when negative")
            else:
                steps.append(f"  Both numbers are positive")
                steps.append(f"  Compare normally: {max(num1, num2)} > {min(num1, num2)}")

            steps.append("")
            steps.append(f"Final Answer: {result} ✓")
            return steps

        # Handle multiplication
        if op_symbol == '×':
            steps.append("Step 1: Multiplication with negative numbers")
            steps.append("  Rules: negative × negative = positive")
            steps.append("         positive × negative = negative")
            steps.append("         negative × positive = negative")
            steps.append("")

            abs_result = abs(num1) * abs(num2)

            if (num1 < 0 and num2 < 0):
                steps.append(f"  Both negative: result is positive")
                steps.append(f"  |{num1}| × |{num2}| = {abs(num1)} × {abs(num2)} = {abs_result}")
                steps.append(f"  Two negatives make a positive: {result}")
            elif (num1 < 0) or (num2 < 0):
                steps.append(f"  One negative: result is negative")
                steps.append(f"  |{num1}| × |{num2}| = {abs(num1)} × {abs(num2)} = {abs_result}")
                steps.append(f"  Apply negative sign: {result}")
            else:
                steps.append(f"  Both positive: multiply normally")
                steps.append(f"  {num1} × {num2} = {result}")

            steps.append("")
            steps.append(f"Final Answer: {result} ✓")
            return steps

        # Handle division
        if op_symbol == '÷':
            steps.append("Step 1: Division with negative numbers")
            steps.append("  Rules: negative ÷ negative = positive")
            steps.append("         positive ÷ negative = negative")
            steps.append("         negative ÷ positive = negative")
            steps.append("")

            abs_result = abs(num1) // abs(num2)

            if (num1 < 0 and num2 < 0):
                steps.append(f"  Both negative: result is positive")
                steps.append(f"  |{num1}| ÷ |{num2}| = {abs(num1)} ÷ {abs(num2)} = {abs_result}")
                steps.append(f"  Two negatives make a positive: {result}")
            elif (num1 < 0) or (num2 < 0):
                steps.append(f"  One negative: result is negative")
                steps.append(f"  |{num1}| ÷ |{num2}| = {abs(num1)} ÷ {abs(num2)} = {abs_result}")
                steps.append(f"  Apply negative sign: {result}")
            else:
                steps.append(f"  Both positive: divide normally")
                steps.append(f"  {num1} ÷ {num2} = {result}")

            steps.append("")
            steps.append(f"Final Answer: {result} ✓")
            return steps

        # Process based on operation (addition and subtraction)
        if op_symbol == '+':
            steps.append("Step 1: Addition rules")

            if num1 > 0 and num2 > 0:
                steps.append("  Both positive: add normally")
                steps.append(f"  {num1} + {num2} = {result}")

            elif num1 < 0 and num2 < 0:
                steps.append("  Both negative: add absolute values, result is negative")
                abs_sum = abs(num1) + abs(num2)
                steps.append(f"  -(|{num1}| + |{num2}|) = -({abs(num1)} + {abs(num2)}) = {result}")

            elif num1 > 0 and num2 < 0:
                steps.append("  Positive + Negative: subtract absolute values")
                steps.append(f"  Find: {num1} + ({num2}) = {num1} - {abs(num2)}")
                if num1 > abs(num2):
                    steps.append(f"  Positive is larger: {num1} - {abs(num2)} = {result} (positive)")
                else:
                    steps.append(f"  Negative is larger: -({abs(num2)} - {num1}) = {result} (negative)")

            else:  # num1 < 0 and num2 > 0
                steps.append("  Negative + Positive: subtract absolute values")
                steps.append(f"  Find: ({num1}) + {num2} = {num2} - {abs(num1)}")
                if num2 > abs(num1):
                    steps.append(f"  Positive is larger: {num2} - {abs(num1)} = {result} (positive)")
                else:
                    steps.append(f"  Negative is larger: -({abs(num1)} - {num2}) = {result} (negative)")

        else:  # subtraction
            steps.append("Step 1: Subtraction rules")
            steps.append(f"  Rewrite: {num1} - ({num2}) = {num1} + ({-num2})")
            steps.append("")

            # Convert to addition
            num2_opposite = -num2

            steps.append("Step 2: Now solve as addition")

            if num1 > 0 and num2_opposite > 0:
                steps.append("  Both positive: add normally")
                steps.append(f"  {num1} + {num2_opposite} = {result}")

            elif num1 < 0 and num2_opposite < 0:
                steps.append("  Both negative: add absolute values, result is negative")
                abs_sum = abs(num1) + abs(num2_opposite)
                steps.append(f"  -(|{num1}| + |{num2_opposite}|) = -({abs(num1)} + {abs(num2_opposite)}) = {result}")

            elif num1 > 0 and num2_opposite < 0:
                steps.append("  Positive + Negative: subtract absolute values")
                if num1 > abs(num2_opposite):
                    steps.append(f"  Positive is larger: {num1} - {abs(num2_opposite)} = {result} (positive)")
                else:
                    steps.append(f"  Negative is larger: -({abs(num2_opposite)} - {num1}) = {result} (negative)")

            else:  # num1 < 0 and num2_opposite > 0
                steps.append("  Negative + Positive: subtract absolute values")
                if num2_opposite > abs(num1):
                    steps.append(f"  Positive is larger: {num2_opposite} - {abs(num1)} = {result} (positive)")
                else:
                    steps.append(f"  Negative is larger: -({abs(num1)} - {num2_opposite}) = {result} (negative)")

        steps.append("")
        steps.append(f"Final Answer: {result} ✓")

        return steps

    def _parse_problem(self, problem: Problem) -> Tuple[int, int, str]:
        """
        Parse the problem text to extract numbers and operation.

        Args:
            problem: Problem instance

        Returns:
            Tuple of (num1, num2, operation_symbol)
        """
        text = problem.text

        # Handle comparison questions
        if "Which is greater" in text or "Which is larger" in text:
            # Extract: "Which is greater: -5 or 12?"
            match = re.search(r':\s*(-?\d+)\s+or\s+(-?\d+)', text)
            if match:
                num1 = int(match.group(1))
                num2 = int(match.group(2))
                return num1, num2, 'compare'

        # Handle word problems - extract from metadata since text is contextual
        if problem.metadata and 'template' in problem.metadata:
            if problem.metadata['template'] == 'word_problem':
                # Word problems have structured metadata we can use
                # since the text is contextual and doesn't have explicit equation
                num1 = problem.metadata['num1']
                num2 = problem.metadata['num2']
                op_symbol = problem.metadata['operation_symbol']
                return num1, num2, op_symbol

        # Handle standard arithmetic: "Calculate: num1 op num2"
        # Remove "Calculate:" prefix if present
        if "Calculate:" in text:
            text = text.split("Calculate:")[1].strip()

        # Pattern to match: num1 op num2, where numbers can be in parentheses
        # Examples: "3 - (-8)", "(-5) + 12", "(-15) × (-6)"

        # Replace math symbols with standardized versions
        text = text.replace('×', '*').replace('÷', '/')

        # Try to match patterns with parentheses or without
        # Match: (num) op (num) or num op (num) or (num) op num or num op num
        pattern = r'\(?(-?\d+)\)?\s*([+\-*/])\s*\(?(-?\d+)\)?'
        match = re.search(pattern, text)

        if match:
            num1 = int(match.group(1))
            op_symbol = match.group(2)
            num2 = int(match.group(3))

            # Convert operation symbols
            if op_symbol == '*':
                op_symbol = '×'
            elif op_symbol == '/':
                op_symbol = '÷'

            return num1, num2, op_symbol

        # If parsing fails, fall back to metadata (should not happen with good problem generation)
        if problem.metadata:
            num1 = problem.metadata.get('num1', 0)
            num2 = problem.metadata.get('num2', 0)
            op_symbol = problem.metadata.get('operation_symbol', '+')
            return num1, num2, op_symbol

        raise ValueError(f"Could not parse problem text: {problem.text}")

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Correctly solve negative number operation.

        Args:
            problem: Problem instance with negative numbers
            verbose: If True, generate verbose steps; if False (default), generate concise steps

        Returns:
            Solution with correct answer and detailed steps
        """
        # Parse problem text to extract numbers and operation
        num1, num2, op_symbol = self._parse_problem(problem)

        # Calculate result based on operation
        if op_symbol == 'compare':
            result = max(num1, num2)
        elif op_symbol == '×':
            result = num1 * num2
        elif op_symbol == '÷':
            result = num1 // num2
        elif op_symbol == '+':
            result = num1 + num2
        else:  # subtraction
            result = num1 - num2

        # Prepare intermediate data for step generation
        intermediate_data = {}

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, num1, num2, op_symbol, result, intermediate_data)
        else:
            steps = self._generate_concise_steps(problem, num1, num2, op_symbol, result, intermediate_data)

        return Solution(
            answer=result,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
