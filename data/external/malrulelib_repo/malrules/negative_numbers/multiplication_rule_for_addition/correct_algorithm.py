"""
Correct negative number addition/subtraction algorithm.

Implements proper rules for adding and subtracting negative numbers.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List, Dict, Any
from utils import CorrectAlgorithm, Problem, Solution


class NegativeAdditionCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for negative number addition/subtraction.

    Applies proper rules, not multiplication rules.
    """

    def get_name(self) -> str:
        return "Correct Negative Number Addition/Subtraction"

    def get_description(self) -> str:
        return (
            "Performs addition and subtraction with negative numbers correctly. "
            "Adding two negatives gives a more negative result. "
            "Subtracting a negative is the same as adding its opposite."
        )

    def _generate_concise_steps(self, problem: Problem, template: str,
                                 correct_answer: Any, unit_suffix: str,
                                 intermediate_data: Dict[str, Any]) -> List[str]:
        """
        Generate concise steps for the solution.

        Format: [Question, step (formula/values only), ..., answer]
        """
        steps = []

        # Question
        steps.append(f"Question: {problem.text}")

        # Template-specific concise steps
        if template == 'two_negatives_addition':
            num1 = intermediate_data.get('num1')
            num2 = intermediate_data.get('num2')
            steps.append(f"({num1}) + ({num2})")
            steps.append(f"|{num1}| + |{num2}| = {abs(num1)} + {abs(num2)} = {abs(num1) + abs(num2)}")
            steps.append(f"Both negative: -{abs(num1) + abs(num2)} = {correct_answer}")

        elif template == 'positive_minus_negative':
            num1 = intermediate_data.get('num1')
            num2 = intermediate_data.get('num2')
            opposite_num2 = -num2
            steps.append(f"{num1} - ({num2})")
            steps.append(f"{num1} - ({num2}) = {num1} + {opposite_num2}")
            steps.append(f"Result: {correct_answer}")

        elif template == 'word_problem_temperature':
            start_temp = intermediate_data.get('start_temp')
            change = intermediate_data.get('change')
            steps.append(f"{start_temp} - {change}")
            steps.append(f"Result: {correct_answer}")

        elif template == 'word_problem_elevation':
            start_depth = intermediate_data.get('start_depth')
            descend = intermediate_data.get('descend')
            steps.append(f"{start_depth} - {descend}")
            steps.append(f"Result: {correct_answer}")

        elif template == 'sequential_operations':
            num1 = intermediate_data.get('num1')
            num2 = intermediate_data.get('num2')
            num3 = intermediate_data.get('num3')
            temp = num1 + num2
            steps.append(f"({num1}) + ({num2}) + {num3}")
            steps.append(f"Step 1: {num1} + {num2} = {temp}")
            steps.append(f"Step 2: {temp} + {num3} = {correct_answer}")

        else:
            steps.append(f"Result: {correct_answer}")

        # Final answer
        final_answer = f"{correct_answer}{unit_suffix}" if unit_suffix else str(correct_answer)
        steps.append(f"Answer: {final_answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, template: str,
                                 correct_answer: Any, unit_suffix: str,
                                 intermediate_data: Dict[str, Any]) -> List[str]:
        """
        Generate verbose steps for the solution (original step structure).
        """
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD: Proper negative number operations")
        steps.append("")

        # Template-aware reasoning and calculation
        if template == 'two_negatives_addition':
            num1 = intermediate_data.get('num1')
            num2 = intermediate_data.get('num2')

            steps.append(f"Adding two negative numbers: ({num1}) + ({num2})")
            steps.append(f"Rule: When adding two negative numbers, add their absolute values")
            steps.append(f"and keep the negative sign")
            steps.append(f"|{num1}| + |{num2}| = {abs(num1)} + {abs(num2)} = {abs(num1) + abs(num2)}")
            steps.append(f"Both negative, so result is negative: {correct_answer}")
            steps.append(f"Final answer: {correct_answer} ✓")

        elif template == 'positive_minus_negative':
            num1 = intermediate_data.get('num1')
            num2 = intermediate_data.get('num2')
            opposite_num2 = -num2

            steps.append(f"Subtracting a negative: {num1} - ({num2})")
            steps.append(f"Rule: Subtracting a negative is the same as adding the opposite")
            steps.append(f"Rewrite as: {num1} + ({opposite_num2})")
            steps.append(f"Result: {correct_answer}")
            steps.append(f"Final answer: {correct_answer} ✓")

        elif template == 'word_problem_temperature':
            start_temp = intermediate_data.get('start_temp')
            change = intermediate_data.get('change')

            steps.append(f"Starting temperature: {start_temp}")
            steps.append(f"Temperature drops by: {change}")
            steps.append(f"Operation: {start_temp} - {change}")
            steps.append(f"Calculation: {start_temp} - {change} = {correct_answer}")
            steps.append(f"Final answer: {correct_answer}{unit_suffix} ✓")

        elif template == 'word_problem_elevation':
            start_depth = intermediate_data.get('start_depth')
            descend = intermediate_data.get('descend')

            steps.append(f"Starting elevation: {start_depth}m")
            steps.append(f"Descends: {descend}m")
            steps.append(f"Operation: {start_depth} - {descend}")
            steps.append(f"Calculation: {start_depth} - {descend} = {correct_answer}")
            steps.append(f"Final answer: {correct_answer}{unit_suffix} ✓")

        elif template == 'sequential_operations':
            num1 = intermediate_data.get('num1')
            num2 = intermediate_data.get('num2')
            num3 = intermediate_data.get('num3')
            temp = num1 + num2

            steps.append(f"Sequential operations: ({num1}) + ({num2}) + {num3}")
            steps.append(f"Step 1: ({num1}) + ({num2})")
            steps.append(f"Adding two negatives: {num1} + {num2} = {temp}")
            steps.append(f"Step 2: {temp} + {num3}")
            steps.append(f"Result: {temp} + {num3} = {correct_answer}")
            steps.append(f"Final answer: {correct_answer} ✓")

        else:
            expression = intermediate_data.get('expression', '')
            problem_type = intermediate_data.get('problem_type', '')

            steps.append(f"Expression: {expression}")

            if problem_type == 'neg_plus_neg':
                steps.append(f"Rule: Adding two negative numbers")
                steps.append(f"Add their absolute values and keep the negative sign")
            elif problem_type == 'neg_minus_neg':
                steps.append(f"Rule: Subtracting a negative number")
                steps.append(f"Subtracting a negative is adding the opposite")
            elif problem_type == 'pos_plus_neg':
                steps.append(f"Rule: Adding a negative number")
                steps.append(f"Adding a negative is like subtraction")
            else:
                steps.append(f"Rule: Adding negative and positive")
                steps.append(f"Find difference, use sign of larger absolute value")

            steps.append(f"Final answer: {correct_answer} ✓")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct negative number operations.

        Args:
            problem: Negative number problem
            verbose: If True, generate verbose steps; if False (default), generate concise steps

        Returns:
            Solution with correct evaluation
        """
        template = problem.metadata.get('template', None)
        operands = problem.operands
        operation = problem.operation

        # Calculate correct answer by parsing problem data and solving
        correct_answer = None
        unit_suffix = ""  # For temperature and elevation problems
        intermediate_data = {}

        # Template-aware reasoning and calculation
        if template == 'two_negatives_addition':
            num1 = problem.metadata.get('num1', operands[0])
            num2 = problem.metadata.get('num2', operands[1])
            correct_answer = num1 + num2
            intermediate_data = {'num1': num1, 'num2': num2}

        elif template == 'positive_minus_negative':
            num1 = problem.metadata.get('num1', operands[0])
            num2 = problem.metadata.get('num2', operands[1])
            correct_answer = num1 - num2
            intermediate_data = {'num1': num1, 'num2': num2}

        elif template == 'word_problem_temperature':
            start_temp = problem.metadata.get('start_temp', operands[0])
            change = problem.metadata.get('change', operands[1])
            correct_answer = start_temp - change
            unit_suffix = "°"
            intermediate_data = {'start_temp': start_temp, 'change': change}

        elif template == 'word_problem_elevation':
            start_depth = problem.metadata.get('start_depth', operands[0])
            descend = problem.metadata.get('descend', operands[1])
            correct_answer = start_depth - descend
            unit_suffix = "m"
            intermediate_data = {'start_depth': start_depth, 'descend': descend}

        elif template == 'sequential_operations':
            num1 = problem.metadata.get('num1', operands[0])
            num2 = problem.metadata.get('num2', operands[1])
            num3 = problem.metadata.get('num3', operands[2])
            temp = num1 + num2
            correct_answer = temp + num3
            intermediate_data = {'num1': num1, 'num2': num2, 'num3': num3}

        else:
            # Backwards compatibility for old format
            expression = problem.metadata.get('expression', '')
            problem_type = problem.metadata.get('problem_type', '')
            intermediate_data = {'expression': expression, 'problem_type': problem_type}

            if operation == 'sequential_operations' and len(operands) == 3:
                correct_answer = operands[0] + operands[1] + operands[2]
            elif operation == 'negative_subtraction':
                correct_answer = operands[0] - operands[1]
            else:  # negative_addition
                correct_answer = operands[0] + operands[1]

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, template, correct_answer, unit_suffix, intermediate_data)
        else:
            steps = self._generate_concise_steps(problem, template, correct_answer, unit_suffix, intermediate_data)

        # Format the final answer with unit suffix if applicable
        final_answer = f"{correct_answer}{unit_suffix}" if unit_suffix else str(correct_answer)

        return Solution(
            answer=final_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
