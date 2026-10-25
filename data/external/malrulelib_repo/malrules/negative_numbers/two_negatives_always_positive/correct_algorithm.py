"""
Correct negative number subtraction algorithm.

Implements the standard algorithm for subtracting with negative numbers.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class NegativeSubtractionCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for negative number subtraction.

    Follows the rule: a - b = a + (-b)
    Subtraction is addition of the opposite.
    """

    def get_name(self) -> str:
        return "Correct Negative Number Subtraction Algorithm"

    def get_description(self) -> str:
        return (
            "The standard algorithm for subtracting with negative numbers. "
            "Subtraction is rewritten as addition of the opposite: a - b = a + (-b). "
            "Then normal integer addition rules apply: same signs add and keep sign, "
            "different signs subtract and take sign of larger absolute value."
        )

    def generate_concise_steps(self, problem: Problem, correct_answer: int, answer_str: str) -> List[str]:
        """
        Generate concise steps for the solution.

        Format: [Question, formula extraction (for word problems), calculation steps, answer]
        Only includes formula and values, no explanations.
        """
        template = problem.metadata.get('template', 'basic_subtraction')
        operands = problem.operands
        operation = problem.operation
        steps = []

        steps.append(f"Question: {problem.text}")

        # Handle multi-step problems (3 operands)
        if operation == 'multi_step' and len(operands) == 3:
            num1, num2, num3 = operands
            opposite_num2 = -num2
            temp_result = num1 + opposite_num2
            result = temp_result + num3
            steps.append(f"Formula: {num1} - ({num2}) + {num3}")
            steps.append(f"{num1} - ({num2}) = {num1} + ({opposite_num2}) = {temp_result}")
            steps.append(f"{temp_result} + {num3} = {result}")
            steps.append(f"Answer: {answer_str}")

        # Handle negative addition
        elif operation == 'negative_addition':
            num1, num2 = operands
            result = num1 + num2
            steps.append(f"Formula: ({num1}) + ({num2})")
            steps.append(f"|{num1}| + |{num2}| = {abs(num1)} + {abs(num2)} = {abs(result)}")
            steps.append(f"Answer: {answer_str}")

        # Handle negative multiplication
        elif operation == 'negative_multiplication':
            num1, num2 = operands
            result = num1 * num2
            steps.append(f"Formula: ({num1}) × ({num2})")
            steps.append(f"|{num1}| × |{num2}| = {abs(num1)} × {abs(num2)} = {abs(result)}")
            steps.append(f"Answer: {answer_str}")

        # Handle negative division
        elif operation == 'negative_division':
            num1, num2 = operands
            result = num1 // num2
            steps.append(f"Formula: ({num1}) ÷ ({num2})")
            steps.append(f"|{num1}| ÷ |{num2}| = {abs(num1)} ÷ {abs(num2)} = {abs(result)}")
            steps.append(f"Answer: {answer_str}")

        # Handle subtraction
        else:
            if len(operands) >= 2:
                num1, num2 = operands
            else:
                steps.append(f"Answer: {answer_str}")
                return steps

            opposite_num2 = -num2
            result = num1 + opposite_num2
            steps.append(f"Formula: {num1} - {num2}")
            steps.append(f"{num1} - {num2} = {num1} + ({opposite_num2}) = {result}")
            steps.append(f"Answer: {answer_str}")

        return steps

    def generate_verbose_steps(self, problem: Problem, correct_answer: int, answer_str: str) -> List[str]:
        """
        Generate verbose steps for the solution (original detailed format).

        Includes full explanations, rules, and reasoning.
        """
        template = problem.metadata.get('template', 'basic_subtraction')
        operands = problem.operands
        operation = problem.operation
        steps = []

        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD: Subtraction as addition of the opposite")
        steps.append("")

        # Handle multi-step problems (3 operands)
        if operation == 'multi_step' and len(operands) == 3:
            num1, num2, num3 = operands
            steps.append(f"Step 1: {num1} - ({num2})")
            opposite_num2 = -num2
            steps.append(f"Rewrite as: {num1} + ({opposite_num2}) = {num1 + opposite_num2}")
            temp_result = num1 + opposite_num2

            steps.append(f"Step 2: {temp_result} + {num3}")
            result = temp_result + num3
            steps.append(f"Result: {result}")
            steps.append(f"Final answer: {answer_str} ✓")

        # Handle negative addition
        elif operation == 'negative_addition':
            num1, num2 = operands
            steps.append(f"Adding two negative numbers")
            result = num1 + num2
            steps.append(f"|{num1}| + |{num2}| = {abs(num1)} + {abs(num2)} = {abs(result)}")
            steps.append(f"Both negative, so result is negative: {result}")
            steps.append(f"Final answer: {answer_str} ✓")

        # Handle negative multiplication
        elif operation == 'negative_multiplication':
            num1, num2 = operands
            steps.append(f"Multiplying two negative numbers")
            result = num1 * num2
            steps.append(f"Rule: negative × negative = positive")
            steps.append(f"|{num1}| × |{num2}| = {abs(num1)} × {abs(num2)} = {abs(result)}")
            steps.append(f"Result is positive: {result}")
            steps.append(f"Final answer: {answer_str} ✓")

        # Handle negative division
        elif operation == 'negative_division':
            num1, num2 = operands
            steps.append(f"Dividing two negative numbers")
            result = num1 // num2
            steps.append(f"Rule: negative ÷ negative = positive")
            steps.append(f"|{num1}| ÷ |{num2}| = {abs(num1)} ÷ {abs(num2)} = {abs(result)}")
            steps.append(f"Result is positive: {result}")
            steps.append(f"Final answer: {answer_str} ✓")

        # Handle subtraction
        else:
            if len(operands) < 2:
                steps.append(f"Final answer: {answer_str} ✓")
                return steps

            num1, num2 = operands

            # Convert subtraction to addition of the opposite
            opposite_num2 = -num2
            steps.append(f"Rewrite as addition of the opposite: {num1} - {num2} = {num1} + ({opposite_num2})")

            # Now perform the addition
            result = num1 + opposite_num2

            # Explain the addition step
            if (num1 >= 0 and opposite_num2 >= 0) or (num1 < 0 and opposite_num2 < 0):
                # Same signs: add absolute values, keep sign
                steps.append(f"Same signs: add absolute values and keep the sign")
                steps.append(f"|{num1}| + |{opposite_num2}| = {abs(num1)} + {abs(opposite_num2)} = {abs(result)}")
                if result < 0:
                    steps.append(f"Both negative, so result is negative: {result}")
                else:
                    steps.append(f"Both positive, so result is positive: {result}")
            else:
                # Different signs: subtract absolute values, take sign of larger
                steps.append(f"Different signs: subtract absolute values and take sign of larger")
                abs1, abs2 = abs(num1), abs(opposite_num2)
                if abs1 > abs2:
                    steps.append(f"|{num1}| > |{opposite_num2}|, so {abs1} - {abs2} = {abs1 - abs2}")
                    steps.append(f"Take sign of {num1}: result is {result}")
                elif abs2 > abs1:
                    steps.append(f"|{opposite_num2}| > |{num1}|, so {abs2} - {abs1} = {abs2 - abs1}")
                    steps.append(f"Take sign of {opposite_num2}: result is {result}")
                else:
                    steps.append(f"|{num1}| = |{opposite_num2}|, so result is 0")

            steps.append(f"Final answer: {answer_str} ✓")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct negative number operations algorithm.

        Args:
            problem: Negative number problem (subtraction, addition, multiplication, division, or multi-step)
            verbose: If True, generate verbose steps; if False, generate concise steps (default: False)

        Returns:
            Solution with correct answer
        """
        template = problem.metadata.get('template', 'basic_subtraction')
        operands = problem.operands
        operation = problem.operation

        # COMPUTE the correct answer from operands - never use metadata
        if operation == 'multi_step' and len(operands) == 3:
            correct_answer = operands[0] - operands[1] + operands[2]
        elif operation == 'negative_addition':
            correct_answer = operands[0] + operands[1]
        elif operation == 'negative_multiplication':
            correct_answer = operands[0] * operands[1]
        elif operation == 'negative_division':
            correct_answer = operands[0] // operands[1]
        else:  # subtraction operations
            if len(operands) >= 2:
                correct_answer = operands[0] - operands[1]
            else:
                correct_answer = operands[0]

        # For word problems, add appropriate units
        answer_str = str(correct_answer)
        if template == 'word_problem_temp':
            answer_str = f"{correct_answer}°"
        elif template == 'word_problem_money':
            answer_str = f"${correct_answer}"

        # Generate steps based on verbose flag
        if verbose:
            steps = self.generate_verbose_steps(problem, correct_answer, answer_str)
        else:
            steps = self.generate_concise_steps(problem, correct_answer, answer_str)

        return Solution(
            answer=answer_str,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
