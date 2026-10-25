"""
Multiplication-Rule-For-Addition malrule algorithm.

Implements the systematic error of applying multiplication rules
(like "two negatives make a positive") to addition/subtraction.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List
import re

# Helper functions are defined as methods within the class below

class MultiplicationRuleForAdditionMalrule(Malrule):
    """
    Implements the Multiplication-Rule-For-Addition bug.

    Students incorrectly apply multiplication rules to addition/subtraction
    with negative numbers. They think "two negatives make a positive" applies
    to addition, or confuse the rules between operations.

    Example: -3 + (-5) = +8 (WRONG! thinking two negatives = positive)
    Correct: -3 + (-5) = -8

    This is very common and related to Two-Negatives-Always-Positive.
    """

    def get_name(self) -> str:
        return "Multiplication-Rule-For-Addition (Operation-Rule Confusion)"

    def get_description(self) -> str:
        return (
            "Students incorrectly apply multiplication sign rules (like 'two negatives "
            "make a positive') to addition and subtraction operations. Makonye & Fakude "
            "(2016) found this is a 'specific case of surface understanding where students "
            "just remember rules such as negative and negative becomes positive and apply "
            "it indiscriminately.' Example: -3 + (-5) = +8 because students think negative "
            "+ negative = positive, confusing the multiplication rule with addition. This "
            "represents what Graeber & Johnson (1991) classified as 'overgeneralization' - "
            "one of the four main types of mathematical misconceptions."
        )

    def _generate_concise_steps(self, problem: Problem, template: str,
                                 malrule_answer: Any, unit_suffix: str,
                                 intermediate_data: Dict[str, Any]) -> List[str]:
        """
        Generate concise steps for the malrule solution.

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
            steps.append(f"Two negatives = positive (malrule)")
            steps.append(f"|{num1}| + |{num2}| = {abs(num1)} + {abs(num2)} = {malrule_answer}")

        elif template == 'positive_minus_negative':
            num1 = intermediate_data.get('num1')
            num2 = intermediate_data.get('num2')
            steps.append(f"{num1} - ({num2})")
            steps.append(f"Confused: {num1} - {abs(num2)} = {malrule_answer}")

        elif template == 'word_problem_temperature':
            start_temp = intermediate_data.get('start_temp')
            change = intermediate_data.get('change')
            steps.append(f"Negative + drop = two negatives (malrule)")
            steps.append(f"|{start_temp}| + {change} = {abs(start_temp)} + {change} = {malrule_answer}")

        elif template == 'word_problem_elevation':
            start_depth = intermediate_data.get('start_depth')
            descend = intermediate_data.get('descend')
            steps.append(f"Negative elevation + descend = two negatives (malrule)")
            steps.append(f"|{start_depth}| + {descend} = {abs(start_depth)} + {descend} = {malrule_answer}")

        elif template == 'sequential_operations':
            num1 = intermediate_data.get('num1')
            num2 = intermediate_data.get('num2')
            num3 = intermediate_data.get('num3')
            temp = abs(num1) + abs(num2)
            steps.append(f"({num1}) + ({num2}) + {num3}")
            steps.append(f"Two negatives = positive (malrule): {temp}")
            steps.append(f"{temp} + {num3} = {malrule_answer}")

        else:
            steps.append(f"Malrule applied: {malrule_answer}")

        # Final answer
        final_answer = f"{malrule_answer}{unit_suffix}" if unit_suffix else str(malrule_answer)
        steps.append(f"Answer: {final_answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, template: str,
                                 malrule_answer: Any, unit_suffix: str,
                                 intermediate_data: Dict[str, Any]) -> List[str]:
        """
        Generate verbose steps for the malrule solution (original step structure).
        """
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: Apply multiplication rules to addition/subtraction")
        steps.append("")

        # Template-aware reasoning and calculation
        if template == 'two_negatives_addition':
            num1 = intermediate_data.get('num1')
            num2 = intermediate_data.get('num2')

            steps.append(f"Adding two negative numbers: ({num1}) + ({num2})")
            steps.append("MALRULE REASONING: Two negatives make a positive (from multiplication)")
            steps.append(f"Student incorrectly thinks: negative + negative = positive")
            steps.append(f"Computes: |{num1}| + |{num2}| = {abs(num1)} + {abs(num2)} = {malrule_answer}")
            steps.append("")
            steps.append(f"Final answer: {malrule_answer} ✗ (INCORRECT)")

        elif template == 'positive_minus_negative':
            num1 = intermediate_data.get('num1')
            num2 = intermediate_data.get('num2')

            steps.append(f"Subtracting a negative: {num1} - ({num2})")
            steps.append("MALRULE CONFUSION: Student gets confused with double negatives")
            steps.append("Instead of converting to addition, they just subtract")
            steps.append(f"Incorrectly computes: {num1} - {abs(num2)} = {malrule_answer}")
            steps.append("")
            steps.append(f"Final answer: {malrule_answer} ✗ (INCORRECT)")

        elif template == 'word_problem_temperature':
            start_temp = intermediate_data.get('start_temp')
            change = intermediate_data.get('change')

            steps.append(f"Starting temperature: {start_temp}")
            steps.append(f"Temperature drops by: {change}")
            steps.append("MALRULE: Student sees 'negative' and 'drop' as two negatives")
            steps.append("Incorrectly thinks: two negatives make positive")
            steps.append(f"Incorrectly computes: |{start_temp}| + |{change}| = {abs(start_temp)} + {abs(change)} = {malrule_answer}")
            steps.append("")
            steps.append(f"Final answer: {malrule_answer}{unit_suffix} ✗ (INCORRECT)")

        elif template == 'word_problem_elevation':
            start_depth = intermediate_data.get('start_depth')
            descend = intermediate_data.get('descend')

            steps.append(f"Starting elevation: {start_depth}m")
            steps.append(f"Descends: {descend}m")
            steps.append("MALRULE: Student sees 'negative elevation' and 'descend' as two negatives")
            steps.append("Incorrectly thinks: two negatives make positive")
            steps.append(f"Incorrectly computes: |{start_depth}| + |{descend}| = {abs(start_depth)} + {abs(descend)} = {malrule_answer}")
            steps.append("")
            steps.append(f"Final answer: {malrule_answer}{unit_suffix} ✗ (INCORRECT)")

        elif template == 'sequential_operations':
            num1 = intermediate_data.get('num1')
            num2 = intermediate_data.get('num2')
            num3 = intermediate_data.get('num3')
            temp = abs(num1) + abs(num2)

            steps.append(f"Sequential operations: ({num1}) + ({num2}) + {num3}")
            steps.append(f"Step 1: ({num1}) + ({num2})")
            steps.append("MALRULE: Student sees two negatives and makes it positive")
            steps.append(f"Incorrectly computes: |{num1}| + |{num2}| = {abs(num1)} + {abs(num2)} = {temp}")
            steps.append("")
            steps.append(f"Step 2: {temp} + {num3} = {malrule_answer}")
            steps.append("")
            steps.append(f"Final answer: {malrule_answer} ✗ (INCORRECT)")

        else:
            expression = intermediate_data.get('expression', '')
            steps.append(f"Expression: {expression}")
            steps.append("MALRULE: Apply multiplication rules to addition/subtraction")
            steps.append("")
            steps.append(f"Final answer: {malrule_answer} ✗ (INCORRECT)")

        return steps

    def calculate_expected_answer(self, problem: Problem) -> str:
        """
        Calculate the expected incorrect answer for this malrule.

        Uses metadata when available. Returns answer as-is (with units if present).

        For Multiplication-Rule-For-Addition:
        - Student applies multiplication rules to addition/subtraction
        - MALRULE: "Two negatives make a positive" applied to addition

        Example: -3 + (-5)
        - Correct: -3 + (-5) = -8
        - MALRULE: "Two negatives = positive" → +8

        Args:
            problem: Negative number addition/subtraction problem

        Returns:
            Expected incorrect answer as string
        """
        # Use metadata if available
        if 'malrule_answer' in problem.metadata:
            return str(problem.metadata['malrule_answer'])

        # Backwards compatibility - calculate from old metadata format
        if 'expression' in problem.metadata and 'problem_type' in problem.metadata:
            expression = problem.metadata['expression']
            problem_type = problem.metadata['problem_type']

            # Extract numbers from expression
            numbers = re.findall(r'-?\d+', expression)

            if problem_type == 'neg_plus_neg':
                # -a + (-b) - student thinks two negatives = positive
                a = int(numbers[0])  # negative number
                b = int(numbers[1])  # negative number

                # MALRULE: Student adds absolute values and makes result positive
                result = abs(a) + abs(b)

            elif problem_type == 'neg_minus_neg':
                # -a - (-b) - confusion with rules
                a = int(numbers[0])
                b = int(numbers[1])

                # MALRULE: Various confusions - subtract wrong direction
                result = b - abs(a)

            elif problem_type == 'pos_plus_neg':
                # a + (-b) - might apply wrong rule
                a = int(numbers[0])
                b = int(numbers[1])

                # MALRULE: Student just adds absolute values
                result = abs(a) + abs(b)

            else:  # neg_plus_pos
                # -a + b - similar confusion
                a = int(numbers[0])
                b = int(numbers[1])

                # MALRULE: Student adds absolute values
                result = abs(a) + abs(b)

            return str(result)

        # Default fallback
        return "0"

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Multiplication-Rule-For-Addition malrule.

        Args:
            problem: Negative number problem
            verbose: If True, generate verbose steps; if False (default), generate concise steps

        Returns:
            Solution with incorrect multiplication-rule application
        """
        template = problem.metadata.get('template', None)
        operands = problem.operands

        # Calculate malrule answer by parsing problem data and applying misconception
        malrule_answer = None
        unit_suffix = ""  # For temperature and elevation problems
        intermediate_data = {}

        # Template-aware calculation
        if template == 'two_negatives_addition':
            num1 = problem.metadata.get('num1', operands[0])
            num2 = problem.metadata.get('num2', operands[1])
            malrule_answer = abs(num1) + abs(num2)
            intermediate_data = {'num1': num1, 'num2': num2}

        elif template == 'positive_minus_negative':
            num1 = problem.metadata.get('num1', operands[0])
            num2 = problem.metadata.get('num2', operands[1])
            malrule_answer = num1 - abs(num2)
            intermediate_data = {'num1': num1, 'num2': num2}

        elif template == 'word_problem_temperature':
            start_temp = problem.metadata.get('start_temp', operands[0])
            change = problem.metadata.get('change', operands[1])
            malrule_answer = abs(start_temp) + abs(change)
            unit_suffix = "°"
            intermediate_data = {'start_temp': start_temp, 'change': change}

        elif template == 'word_problem_elevation':
            start_depth = problem.metadata.get('start_depth', operands[0])
            descend = problem.metadata.get('descend', operands[1])
            malrule_answer = abs(start_depth) + abs(descend)
            unit_suffix = "m"
            intermediate_data = {'start_depth': start_depth, 'descend': descend}

        elif template == 'sequential_operations':
            num1 = problem.metadata.get('num1', operands[0])
            num2 = problem.metadata.get('num2', operands[1])
            num3 = problem.metadata.get('num3', operands[2])
            temp = abs(num1) + abs(num2)
            malrule_answer = temp + num3
            intermediate_data = {'num1': num1, 'num2': num2, 'num3': num3}

        else:
            # Backwards compatibility for old format
            expression = problem.metadata.get('expression', '')
            intermediate_data = {'expression': expression}
            malrule_answer = self.calculate_expected_answer(problem)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, template, malrule_answer, unit_suffix, intermediate_data)
        else:
            steps = self._generate_concise_steps(problem, template, malrule_answer, unit_suffix, intermediate_data)

        # Format the final answer with unit suffix if applicable
        final_answer = f"{malrule_answer}{unit_suffix}" if unit_suffix else str(malrule_answer)

        return Solution(
            answer=final_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
