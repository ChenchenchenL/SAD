"""
Correct algorithm for decimal comparison.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class DecimalComparisonCorrectAlgorithm(CorrectAlgorithm):
    """Correctly compares decimal numbers."""

    def get_name(self) -> str:
        return "Correct Decimal Comparison"

    def get_description(self) -> str:
        return "Correctly compares decimals by place value, not by number of digits."

    def _generate_verbose_steps(self, problem: Problem, decimals: List[float], correct_answer: str,
                                 is_word_problem: bool, word_problem_type: str, template: str) -> List[str]:
        """Generate verbose, explanatory steps."""
        steps = []

        # For word problems, show extraction step
        if is_word_problem:
            steps.append(f"Word Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Extract the values from the word problem")
            if word_problem_type == 'three_number_ordering':
                decimals_list = problem.metadata.get('decimals', problem.operands)
                steps.append(f"  Values to compare: {', '.join(map(str, decimals_list))}")
            else:  # two_number_comparison
                shorter = problem.metadata.get('shorter_decimal', problem.operands[0])
                longer = problem.metadata.get('longer_decimal', problem.operands[1])
                steps.append(f"  Values to compare: {shorter} and {longer}")
            steps.append("")
            steps.append("Step 2: Compare using correct decimal comparison")
            steps.append("")
        else:
            steps.append(f"Problem: {problem.text}")
            steps.append("")

        steps.append("Compare decimal values by place value (not by number of decimal places):")
        steps.append("")

        # Template-specific reasoning
        if template == 'basic_comparison' and 'shorter_decimal' in problem.metadata:
            shorter = problem.metadata.get('shorter_decimal')
            longer = problem.metadata.get('longer_decimal')
            steps.append(f"  {shorter} vs {longer}")
            steps.append(f"  Compare place by place: {longer} > {shorter}")
            steps.append(f"  Number of decimal places does not determine size")

        elif template == 'ordering' and 'decimals' in problem.metadata:
            decimals_list = problem.metadata.get('decimals', [])
            steps.append(f"  Comparing: {', '.join(map(str, decimals_list))}")
            steps.append(f"  Comparing actual values, not decimal place counts")
            steps.append(f"  Largest value: {correct_answer}")

        elif template == 'money_context' and 'shorter_amount' in problem.metadata:
            shorter = problem.metadata.get('shorter_amount')
            longer = problem.metadata.get('longer_amount')
            steps.append(f"  ${shorter} vs ${longer}")
            steps.append(f"  ${longer} > ${shorter}")
            steps.append(f"  More decimal places means more precise, not less value")

        elif template == 'measurement_context' and 'shorter_measure' in problem.metadata:
            shorter = problem.metadata.get('shorter_measure')
            longer = problem.metadata.get('longer_measure')
            unit = problem.metadata.get('unit', 'units')
            steps.append(f"  {shorter} {unit} vs {longer} {unit}")
            steps.append(f"  {longer} {unit} > {shorter} {unit}")
            steps.append(f"  Compare the actual numerical values")

        elif template == 'number_line' and 'shorter_decimal' in problem.metadata:
            shorter = problem.metadata.get('shorter_decimal')
            longer = problem.metadata.get('longer_decimal')
            steps.append(f"  {shorter} vs {longer}")
            steps.append(f"  {longer} is further right on the number line")
            steps.append(f"  {longer} > {shorter}")

        else:
            # Fallback for old-style metadata
            num_count = problem.metadata.get('num_count', 2)
            if num_count == 3:
                num1 = problem.metadata.get('num1')
                num2 = problem.metadata.get('num2')
                num3 = problem.metadata.get('num3')
                if num1 and num2 and num3:
                    steps.append(f"  {num1} vs {num2} vs {num3}")
            else:
                num1 = problem.metadata.get('num1')
                num2 = problem.metadata.get('num2')
                if num1 and num2:
                    steps.append(f"  {num1} vs {num2}")
                    if num1 > num2:
                        steps.append(f"  {num1} > {num2}")
                    elif num2 > num1:
                        steps.append(f"  {num2} > {num1}")

        steps.append("")
        steps.append(f"Final Answer: {correct_answer} ✓")

        return steps

    def _generate_concise_steps(self, problem: Problem, decimals: List[float], correct_answer: str,
                                 is_word_problem: bool, word_problem_type: str, template: str) -> List[str]:
        """Generate concise steps with just formulas and values."""
        steps = [f"Problem: {problem.text}"]

        # For word problems, show extraction step
        if is_word_problem:
            if word_problem_type == 'three_number_ordering':
                decimals_list = problem.metadata.get('decimals', problem.operands)
                steps.append(f"Values: {', '.join(map(str, decimals_list))}")
            else:  # two_number_comparison
                shorter = problem.metadata.get('shorter_decimal', problem.operands[0])
                longer = problem.metadata.get('longer_decimal', problem.operands[1])
                steps.append(f"Values: {shorter}, {longer}")

        # Template-specific concise steps
        if template == 'basic_comparison' and 'shorter_decimal' in problem.metadata:
            shorter = problem.metadata.get('shorter_decimal')
            longer = problem.metadata.get('longer_decimal')
            steps.append(f"{shorter} vs {longer}")
            steps.append(f"{longer} > {shorter}")

        elif template == 'ordering' and 'decimals' in problem.metadata:
            decimals_list = problem.metadata.get('decimals', [])
            steps.append(f"Compare: {', '.join(map(str, decimals_list))}")
            steps.append(f"max({', '.join(map(str, decimals_list))}) = {correct_answer}")

        elif template == 'money_context' and 'shorter_amount' in problem.metadata:
            shorter = problem.metadata.get('shorter_amount')
            longer = problem.metadata.get('longer_amount')
            steps.append(f"${shorter} vs ${longer}")
            steps.append(f"${longer} > ${shorter}")

        elif template == 'measurement_context' and 'shorter_measure' in problem.metadata:
            shorter = problem.metadata.get('shorter_measure')
            longer = problem.metadata.get('longer_measure')
            unit = problem.metadata.get('unit', 'units')
            steps.append(f"{shorter} {unit} vs {longer} {unit}")
            steps.append(f"{longer} > {shorter}")

        elif template == 'number_line' and 'shorter_decimal' in problem.metadata:
            shorter = problem.metadata.get('shorter_decimal')
            longer = problem.metadata.get('longer_decimal')
            steps.append(f"{shorter} vs {longer}")
            steps.append(f"{longer} > {shorter}")

        else:
            # Fallback
            steps.append(f"max({', '.join(map(str, decimals))}) = {correct_answer}")

        steps.append(correct_answer)

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the correct algorithm to solve the problem.

        Args:
            problem: The decimal comparison problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with correct answer and steps
        """
        # Check if this is a word problem
        is_word_problem = problem.metadata.get('is_word_problem', False)
        word_problem_type = problem.metadata.get('word_problem_type', None)
        template = problem.metadata.get('template', 'basic_comparison')

        # Calculate correct answer from operands (NOT from metadata)
        decimals = problem.operands
        correct_answer = str(max(decimals))

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, decimals, correct_answer,
                                                  is_word_problem, word_problem_type, template)
        else:
            steps = self._generate_concise_steps(problem, decimals, correct_answer,
                                                  is_word_problem, word_problem_type, template)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
