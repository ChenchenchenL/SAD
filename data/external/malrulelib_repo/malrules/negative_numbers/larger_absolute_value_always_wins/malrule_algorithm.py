"""
Malrule algorithm for Larger-Absolute-Value-Always-Wins error.

Students incorrectly determine sign by always using the sign
of the number with the larger absolute value.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import re
from typing import Dict, List, Any, Tuple
from utils import Malrule, Problem, Solution

def _determine_result_sign(num1: int, num2: int, abs1: int, abs2: int) -> str:
    """Helper to determine result sign based on larger absolute value."""
    if abs1 > abs2:
        return '+' if num1 > 0 else '-'
    elif abs2 > abs1:
        return '+' if num2 > 0 else '-'
    else:
        return '+' if num1 > 0 else '-'

class LargerAbsoluteValueAlwaysWinsMalrule(Malrule):
    """
    Implements the Larger-Absolute-Value-Always-Wins malrule.

    Students use an overgeneralized rule: "The answer always has
    the sign of the number with the bigger absolute value."

    This works for some cases (like -8 + 3 = -5) but fails for others
    (like 3 - (-8) = 11, not -11).

    Example: 3 - (-8)
    Correct: 3 - (-8) = 3 + 8 = 11 (positive)
    Malrule: |8| > |3|, so 8's sign wins → answer is negative → -11
    """

    def get_name(self) -> str:
        return "Larger-Absolute-Value-Always-Wins (Overgeneralized Magnitude Rule)"

    def get_description(self) -> str:
        return (
            "Students incorrectly determine the sign of the result by always using the "
            "sign of the number with the larger absolute value, regardless of the operation. "
            "This represents an overgeneralization from addition of integers with different "
            "signs (where the rule works) to all integer operations. Makonye & Fakude (2016) "
            "classify this as a 'strategic error' where students apply a partially-correct "
            "strategy inappropriately. For subtraction like 3 - (-8), students incorrectly "
            "reason: '|8| > |3|, so use -8's sign' → -11 (wrong! correct answer is +11)."
        )

    def _generate_concise_steps(self, problem: Problem, num1: int, num2: int,
                                 op_symbol: str, result: int, abs1: int, abs2: int,
                                 result_sign: str, magnitude: int) -> List[str]:
        """
        Generate concise steps for the malrule solution.

        Format: [Question, step (formula/values only), ..., answer]
        """
        steps = []

        # Question (extract from word problem or use expression)
        if problem.metadata and problem.metadata.get('template') == 'word_problem':
            steps.append(f"Question: {problem.text}")
            steps.append(f"{num1} {op_symbol} ({num2})")
        else:
            steps.append(f"Question: {num1} {op_symbol} {num2}")

        # Concise malrule steps
        steps.append(f"|{num1}| = {abs1}, |{num2}| = {abs2}")

        if op_symbol == 'compare':
            winner = num1 if abs1 > abs2 else num2
            steps.append(f"Larger absolute value: {winner}")
        else:
            if abs1 > abs2:
                steps.append(f"|{num1}| > |{num2}|, sign from {num1}: {result_sign}")
            elif abs2 > abs1:
                steps.append(f"|{num2}| > |{num1}|, sign from {num2}: {result_sign}")
            else:
                steps.append(f"|{num1}| = |{num2}|, sign from {num1}: {result_sign}")

            steps.append(f"Magnitude: {magnitude}")
            steps.append(f"Result: {result_sign}{magnitude} = {result}")

        # Final answer
        steps.append(f"Answer: {result}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, num1: int, num2: int,
                                 op_symbol: str, result: int, abs1: int, abs2: int,
                                 result_sign: str, magnitude: int) -> List[str]:
        """
        Generate verbose steps for the malrule solution (original step structure).
        """
        steps = []
        steps.append(f"Problem: {num1} {op_symbol} {num2}")
        steps.append("")

        steps.append("Step 1: Find absolute values")
        steps.append(f"  |{num1}| = {abs1}")
        steps.append(f"  |{num2}| = {abs2}")
        steps.append("")

        # MALRULE: Determine sign by larger absolute value
        steps.append("Step 2: Determine sign")
        steps.append(f"  MALRULE: The sign of the larger absolute value always wins")

        if abs1 > abs2:
            steps.append(f"  |{num1}| > |{num2}|, so use sign of {num1}")
            steps.append(f"  MALRULE REASONING: '{num1} has bigger magnitude, its sign wins'")
        elif abs2 > abs1:
            steps.append(f"  |{num2}| > |{num1}|, so use sign of {num2}")
            steps.append(f"  MALRULE REASONING: '{num2} has bigger magnitude, its sign wins'")
        else:
            steps.append(f"  Equal absolute values, use sign of first number")
            steps.append(f"  MALRULE REASONING: 'When equal, first sign wins'")

        steps.append(f"  Result will be {result_sign}")
        steps.append("")

        if op_symbol == 'compare':
            # For comparison, just return the number with larger absolute value
            steps.append("Step 3: Choose based on absolute value")
            steps.append(f"  MALRULE: Pick the number with larger absolute value")
            steps.append(f"  {'num1' if abs1 > abs2 else 'num2'} has larger absolute value")
            steps.append("")
            steps.append(f"Final Answer: {result} (May be INCORRECT if signs matter!)")
            return steps

        steps.append("Step 3: Calculate magnitude")

        if op_symbol == '+':
            if (num1 > 0 and num2 > 0) or (num1 < 0 and num2 < 0):
                steps.append(f"  Same signs: add absolute values")
                steps.append(f"  {abs1} + {abs2} = {magnitude}")
            else:
                steps.append(f"  Different signs: subtract absolute values")
                steps.append(f"  |{abs1} - {abs2}| = {magnitude}")
        elif op_symbol == '-':
            steps.append(f"  For subtraction: subtract absolute values")
            steps.append(f"  |{abs1} - {abs2}| = {magnitude}")
        elif op_symbol == '÷':
            steps.append(f"  For division: divide absolute values")
            steps.append(f"  {abs1} ÷ {abs2} = {magnitude}")
        elif op_symbol == '×':
            steps.append(f"  For multiplication: multiply absolute values")
            steps.append(f"  {abs1} × {abs2} = {magnitude}")
        else:
            steps.append(f"  {abs1} - {abs2} = {magnitude}")

        steps.append("")

        # Apply sign
        steps.append("Step 4: Apply sign from Step 2")
        if result_sign == '-':
            steps.append(f"  Sign is negative: {magnitude} → {result}")
        else:
            steps.append(f"  Sign is positive: {magnitude} → {result}")

        steps.append("")
        steps.append(f"Final Answer: {result} (INCORRECT - sign rule doesn't depend only on magnitude!)")

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

    def calculate_expected_answer(self, problem: Problem) -> int:
        """
        Calculate the expected incorrect answer for this malrule.

        For Larger-Absolute-Value-Always-Wins:
        - Student finds which number has larger absolute value
        - MALRULE: Uses that number's sign for the answer
        - Then calculates magnitude and applies the sign

        Example: 3 - (-8)
        - |8| > |3|, so use -8's sign (negative)
        - Magnitude: |3 - (-8)| = |11| = 11
        - Apply negative sign: -11 (WRONG! Should be +11)

        Example: -8 + 3
        - |8| > |3|, so use -8's sign (negative)
        - Magnitude: |-8 + 3| = |-5| = 5
        - Apply negative sign: -5 (happens to be correct!)

        Args:
            problem: Problem with negative numbers

        Returns:
            Expected incorrect answer as integer
        """
        # Parse problem text to extract numbers and operation
        num1, num2, op_symbol = self._parse_problem(problem)

        # Find absolute values
        abs1 = abs(num1)
        abs2 = abs(num2)

        # MALRULE: Determine sign by larger absolute value
        if abs1 > abs2:
            result_sign = 1 if num1 > 0 else -1
        elif abs2 > abs1:
            result_sign = 1 if num2 > 0 else -1
        else:
            # Equal absolute values - use sign of first number
            result_sign = 1 if num1 > 0 else -1

        # Calculate magnitude based on operation
        if op_symbol == '+':
            if (num1 > 0 and num2 > 0) or (num1 < 0 and num2 < 0):
                # Same signs: add
                magnitude = abs1 + abs2
            else:
                # Different signs: subtract
                magnitude = abs(abs1 - abs2)
        elif op_symbol == '-':
            # Student subtracts absolute values
            magnitude = abs(abs1 - abs2)
        elif op_symbol == '÷':
            # Division: divide magnitudes
            magnitude = abs1 // abs2 if abs2 != 0 else abs1
        elif op_symbol == 'compare':
            # Comparison: return the number with larger absolute value
            # (which has the "winning" sign)
            return num1 if abs1 > abs2 else num2
        elif op_symbol == '×':
            # Multiplication: multiply magnitudes
            magnitude = abs1 * abs2
        else:
            # Default to subtraction
            magnitude = abs(abs1 - abs2)

        # Apply sign
        result = result_sign * magnitude
        return result

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the larger-absolute-value-always-wins malrule.

        Student finds which number has larger absolute value,
        then uses that number's sign for the answer.

        Args:
            problem: Problem instance with negative numbers
            verbose: If True, generate verbose steps; if False (default), generate concise steps

        Returns:
            Solution with incorrect answer and student's reasoning
        """
        # Parse problem text to extract numbers and operation
        num1, num2, op_symbol = self._parse_problem(problem)

        # Find absolute values
        abs1 = abs(num1)
        abs2 = abs(num2)

        # MALRULE: Determine sign by larger absolute value
        if abs1 > abs2:
            result_sign = '+' if num1 > 0 else '-'
        elif abs2 > abs1:
            result_sign = '+' if num2 > 0 else '-'
        else:
            # Equal absolute values
            result_sign = '+' if num1 > 0 else '-'

        # Calculate magnitude and result based on operation
        if op_symbol == 'compare':
            # For comparison, just return the number with larger absolute value
            result = num1 if abs1 > abs2 else num2
            magnitude = 0  # Not used for comparison
        elif op_symbol == '+':
            if (num1 > 0 and num2 > 0) or (num1 < 0 and num2 < 0):
                magnitude = abs1 + abs2
            else:
                magnitude = abs(abs1 - abs2)
            result = -magnitude if result_sign == '-' else magnitude
        elif op_symbol == '-':
            magnitude = abs(abs1 - abs2)
            result = -magnitude if result_sign == '-' else magnitude
        elif op_symbol == '÷':
            magnitude = abs1 // abs2 if abs2 != 0 else abs1
            result = -magnitude if result_sign == '-' else magnitude
        elif op_symbol == '×':
            magnitude = abs1 * abs2
            result = -magnitude if result_sign == '-' else magnitude
        else:
            magnitude = abs(abs1 - abs2)
            result = -magnitude if result_sign == '-' else magnitude

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, num1, num2, op_symbol, result,
                                                  abs1, abs2, result_sign, magnitude)
        else:
            steps = self._generate_concise_steps(problem, num1, num2, op_symbol, result,
                                                  abs1, abs2, result_sign, magnitude)

        return Solution(
            answer=result,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
