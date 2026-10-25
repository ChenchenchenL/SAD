"""
Two-Negatives-Always-Positive malrule algorithm.

Implements the systematic error where students incorrectly apply
the multiplication rule "two negatives make a positive" to subtraction.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List

class TwoNegativesAlwaysPositiveMalrule(Malrule):
    """
    Implements the Two-Negatives-Always-Positive bug.

    Students incorrectly apply the multiplication rule (-) × (-) = (+)
    to subtraction operations. When they see two negative signs (either
    in the numbers or the operation), they think the result should be positive.

    Examples:
    - -5 - 6 = 11 (thinking "two negatives make positive")
    - -5 - (-8) = 13 (same flawed reasoning)
    - 3 - (-7) might be done correctly (only one negative)

    This stems from overgeneralizing the multiplication rule to all operations.
    """

    def get_name(self) -> str:
        return "Two-Negatives-Always-Positive (Overgeneralization of Multiplication Rule)"

    def get_description(self) -> str:
        return (
            "Students incorrectly apply the multiplication rule 'two negatives make a positive' "
            "to subtraction and addition operations. This represents what Makonye & Fakude (2016) "
            "term 'surface understanding' where students remember rules like 'negative and negative "
            "becomes positive' and apply them indiscriminately across operations. For example, "
            "students compute -5 - 6 = 11 because they see the negative sign in -5 and the "
            "subtraction operation as 'two negatives' that should combine to make a positive result. "
            "Vlassis (2004) identifies this as stemming from students' failure to distinguish between "
            "the 'operative sign' (subtraction) and the 'unary, predicative sign' (negativity of a number)."
        )

    def calculate_expected_answer(self, problem: Problem) -> str:
        """
        Calculate the expected incorrect answer for this malrule.

        COMPUTES the answer by applying the malrule logic, never uses metadata.
        Returns answer as-is (with units if present).

        Args:
            problem: Negative number operation problem

        Returns:
            Expected incorrect answer as string
        """
        template = problem.metadata.get('template', 'basic_subtraction')
        operands = problem.operands
        operation = problem.operation

        # Handle word problem templates specially - they have different malrule logic
        if template == 'word_problem_temp':
            # start_temp is negative, drop is positive
            # Malrule: student gets confused and computes abs(a - b)
            start_temp, drop = operands[0], operands[1]
            a, b = abs(start_temp), drop
            if a > b:
                malrule_answer = abs(a - b)
            else:
                malrule_answer = abs(b - a)
            answer_str = f"{malrule_answer}°"
            return answer_str

        elif template == 'word_problem_money':
            # balance is negative, withdrawal is positive
            # Malrule: student gets confused and computes abs(a - b) or (b - a)
            balance, withdrawal = operands[0], operands[1]
            a, b = abs(balance), withdrawal
            if a > b:
                malrule_answer = abs(a - b)
            else:
                malrule_answer = b - a  # Note: not abs() for this case
            answer_str = f"${malrule_answer}"
            return answer_str

        # Handle multi-step problems (3 operands)
        if operation == 'multi_step' and len(operands) == 3:
            num1, num2, num3 = operands
            # Malrule: applies "two negatives = positive" to first part
            temp_result = abs(num1) + abs(num2)
            malrule_answer = temp_result + num3
        # Handle negative addition
        elif operation == 'negative_addition':
            num1, num2 = operands
            # Malrule: two negatives make positive
            malrule_answer = abs(num1) + abs(num2)
        # Handle negative multiplication - CORRECT here!
        elif operation == 'negative_multiplication':
            num1, num2 = operands
            malrule_answer = num1 * num2
        # Handle negative division - CORRECT here!
        elif operation == 'negative_division':
            num1, num2 = operands
            malrule_answer = num1 // num2
        # Handle subtraction
        else:
            if len(operands) >= 2:
                num1, num2 = operands[0], operands[1]
            else:
                return str(operands[0])

            pattern = problem.metadata.get('pattern', '')

            if pattern == 'negative_minus_negative':
                # -a - (-b): student thinks two negatives make positive
                a, b = abs(num1), abs(num2)
                malrule_answer = a + b
            elif pattern == 'positive_minus_negative':
                # a - (-b): student sees subtraction and negative, makes it positive difference
                a, b = abs(num1), abs(num2)
                malrule_answer = abs(a - b)
            else:
                # General case: check for negatives
                if num2 < 0:
                    # Subtracting a negative: |num1| + |num2|
                    malrule_answer = abs(num1) + abs(num2)
                elif num1 < 0:
                    # Negative minus positive: |num1| + |num2|
                    malrule_answer = abs(num1) + abs(num2)
                else:
                    # Positive minus positive: normal subtraction
                    malrule_answer = num1 - num2

        # Return answer as string
        return str(malrule_answer)

    def generate_concise_steps(self, problem: Problem, malrule_answer: str) -> List[str]:
        """
        Generate concise steps for the malrule solution.

        Format: [Question, formula extraction (for word problems), calculation steps, answer]
        Only includes formula and values, no explanations.
        """
        template = problem.metadata.get('template', 'basic_subtraction')
        operands = problem.operands
        operation = problem.operation
        steps = []

        steps.append(f"Question: {problem.text}")

        # Template-aware step generation
        if operation == 'multi_step' and len(operands) == 3:
            num1, num2, num3 = operands
            temp = abs(num1) + abs(num2)
            steps.append(f"Formula: {num1} - ({num2}) + {num3}")
            steps.append(f"|{num1}| + |{num2}| = {temp}")
            steps.append(f"{temp} + {num3} = {malrule_answer}")
            steps.append(f"Answer: {malrule_answer}")

        elif template == 'addition_negatives':
            num1, num2 = operands
            steps.append(f"Formula: ({num1}) + ({num2})")
            steps.append(f"|{num1}| + |{num2}| = {malrule_answer}")
            steps.append(f"Answer: {malrule_answer}")

        elif template in ['word_problem_temp', 'word_problem_money']:
            num1, num2 = operands if len(operands) >= 2 else [operands[0], 0]
            if template == 'word_problem_temp':
                steps.append(f"Formula: {num1}° - {num2}°")
            else:
                steps.append(f"Formula: ${num1} - ${num2}")
            display_answer = malrule_answer.lstrip('$').rstrip('°CF ')
            steps.append(f"|{abs(num1)}| - |{num2}| = {display_answer}")
            steps.append(f"Answer: {malrule_answer}")

        else:  # basic_subtraction
            num1, num2 = operands
            if num2 < 0:
                steps.append(f"Formula: {num1} - ({num2})")
                steps.append(f"|{num1}| + |{num2}| = {abs(num1)} + {abs(num2)} = {malrule_answer}")
            else:
                if num1 < 0:
                    steps.append(f"Formula: {num1} - {num2}")
                    steps.append(f"|{num1}| + |{num2}| = {abs(num1)} + {abs(num2)} = {malrule_answer}")
                else:
                    steps.append(f"Formula: {num1} - {num2}")
                    steps.append(f"{num1} - {num2} = {malrule_answer}")
            steps.append(f"Answer: {malrule_answer}")

        return steps

    def generate_verbose_steps(self, problem: Problem, malrule_answer: str) -> List[str]:
        """
        Generate verbose steps for the malrule solution (original detailed format).

        Includes full explanations, rules, and reasoning.
        """
        template = problem.metadata.get('template', 'basic_subtraction')
        operands = problem.operands
        operation = problem.operation
        steps = []

        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: Two negatives always make a positive")
        steps.append("")

        # Template-aware reasoning
        if template == 'multi_step' and len(operands) == 3:
            num1, num2, num3 = operands
            steps.append(f"Step 1: {num1} - ({num2})")
            steps.append("Student sees two negatives (negative number AND subtraction of negative)")
            steps.append(f"Incorrectly applies 'two negatives = positive'")
            temp = abs(num1) + abs(num2)
            steps.append(f"Computes: |{num1}| + |{num2}| = {temp}")
            steps.append("")
            steps.append(f"Step 2: {temp} + {num3} = {malrule_answer}")
            steps.append("")
            steps.append(f"Final answer: {malrule_answer} ✗ (INCORRECT)")

        elif template == 'addition_negatives':
            num1, num2 = operands
            steps.append(f"Adding two negative numbers: ({num1}) + ({num2})")
            steps.append("Student sees 'two negatives' and thinks result must be positive")
            steps.append(f"Incorrectly computes: |{num1}| + |{num2}| = {malrule_answer}")
            steps.append("")
            steps.append(f"Final answer: {malrule_answer} ✗ (INCORRECT)")

        elif template in ['word_problem_temp', 'word_problem_money']:
            num1, num2 = operands if len(operands) >= 2 else [operands[0], 0]

            if template == 'word_problem_temp':
                context = "temperature"
                unit = "°"
            else:
                context = "money/balance"
                unit = "$"

            steps.append(f"Starting value: {num1}")
            steps.append(f"Change: subtract {num2}")
            steps.append(f"Student sees negative {context} and subtraction as 'two negatives'")
            steps.append("Incorrectly thinks: two negatives make positive")

            # Strip unit for display
            display_answer = malrule_answer.lstrip('$').rstrip('°CF ')
            steps.append(f"Incorrectly computes: {display_answer}")
            steps.append("")
            steps.append(f"Final answer: {malrule_answer} ✗ (INCORRECT)")

        else:  # basic_subtraction
            num1, num2 = operands

            if num2 < 0:
                steps.append(f"Subtracting a negative: {num1} - ({num2})")
                steps.append("Student sees 'two negatives': subtraction AND negative number")
                steps.append("Incorrectly applies 'two negatives = positive'")
                steps.append(f"Computes: |{num1}| + |{num2}| = {abs(num1)} + {abs(num2)} = {malrule_answer}")
            else:
                if num1 < 0:
                    steps.append(f"Negative number minus positive: {num1} - {num2}")
                    steps.append("Student sees 'two negatives': negative number AND subtraction")
                    steps.append("Incorrectly applies 'two negatives = positive'")
                    steps.append(f"Computes: |{num1}| + |{num2}| = {abs(num1)} + {abs(num2)} = {malrule_answer}")
                else:
                    steps.append(f"Positive minus positive: {num1} - {num2}")
                    steps.append("Normal subtraction")
                    steps.append(f"Answer: {malrule_answer}")

            steps.append("")
            steps.append(f"Final answer: {malrule_answer} ✗ (INCORRECT)")

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Two-Negatives-Always-Positive malrule.

        Args:
            problem: Negative number problem (subtraction, addition, multiplication, division, or multi-step)
            verbose: If True, generate verbose steps; if False, generate concise steps (default: False)

        Returns:
            Solution with incorrect application of multiplication rule to other operations
        """
        template = problem.metadata.get('template', 'basic_subtraction')
        operands = problem.operands
        operation = problem.operation

        # COMPUTE the malrule answer - never use metadata
        malrule_answer_raw = self.calculate_expected_answer(problem)

        # Generate steps based on verbose flag
        if verbose:
            steps = self.generate_verbose_steps(problem, malrule_answer_raw)
        else:
            steps = self.generate_concise_steps(problem, malrule_answer_raw)

        return Solution(
            answer=str(malrule_answer_raw),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
