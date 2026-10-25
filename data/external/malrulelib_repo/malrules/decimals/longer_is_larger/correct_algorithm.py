"""
Correct decimal comparison algorithm.

Implements the standard algorithm for comparing decimal numbers by value.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class DecimalComparisonCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for comparing decimal numbers.

    Compares decimals by their actual numerical value, not by the number
    of decimal places. Uses place value understanding.
    """

    def get_name(self) -> str:
        return "Correct Decimal Comparison Algorithm"

    def get_description(self) -> str:
        return (
            "The standard algorithm for comparing decimal numbers. Compare the "
            "whole number parts first. If equal, compare the decimal parts digit "
            "by digit from left to right (tenths, then hundredths, then thousandths, "
            "etc.). Trailing zeros don't affect value: 0.5 = 0.50 = 0.500."
        )

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
                steps.append(f"  Values to compare: {', '.join(map(str, decimals))}")
            else:  # two_number_comparison
                steps.append(f"  Values to compare: {decimals[0]} and {decimals[1]}")
            steps.append("")
            steps.append("Step 2: Compare using correct decimal comparison")
            steps.append("")
        else:
            steps.append(f"Problem: {problem.text}")
            steps.append("")

        steps.append("CORRECT METHOD: Compare decimals by place value")
        steps.append("")

        # Handle multiple decimals (find the largest)
        if len(decimals) > 2:
            steps.append(f"Comparing {', '.join(map(str, decimals))}")
            steps.append("Finding the largest value by comparing place values")
            steps.append("")
            steps.append(f"By comparing place values (tenths, hundredths, etc.):")
            steps.append(f"  The largest is: {correct_answer}")
            steps.append("")
            steps.append(f"Answer: {correct_answer} ✓")
        else:
            # Handle two decimals
            decimal1, decimal2 = decimals
            steps.append(f"Comparing {decimal1} and {decimal2}")

            # Compare the actual values
            if decimal1 == decimal2:
                steps.append(f"The numbers are equal: {decimal1} = {decimal2}")
                result_text = f"{decimal1} and {decimal2} are equal"
            else:
                str1 = str(decimal1)
                str2 = str(decimal2)

                # Split into whole and decimal parts
                if '.' in str1:
                    whole1, dec1 = str1.split('.')
                else:
                    whole1, dec1 = str1, '0'

                if '.' in str2:
                    whole2, dec2 = str2.split('.')
                else:
                    whole2, dec2 = str2, '0'

                # Compare whole parts first
                if int(whole1) != int(whole2):
                    steps.append(f"Whole number parts: {whole1} vs {whole2}")
                    if int(whole1) > int(whole2):
                        steps.append(f"Since {whole1} > {whole2}, we have {decimal1} > {decimal2}")
                    else:
                        steps.append(f"Since {whole2} > {whole1}, we have {decimal2} > {decimal1}")
                else:
                    # Whole parts equal, compare decimal parts
                    steps.append(f"Whole number parts are equal: {whole1} = {whole2}")

                    # Pad with trailing zeros to same length
                    max_len = max(len(dec1), len(dec2))
                    dec1_padded = dec1.ljust(max_len, '0')
                    dec2_padded = dec2.ljust(max_len, '0')

                    steps.append(f"Align decimal parts with trailing zeros:")
                    steps.append(f"  {decimal1} = {whole1}.{dec1_padded}")
                    steps.append(f"  {decimal2} = {whole2}.{dec2_padded}")

                    # Compare digit by digit
                    for i in range(max_len):
                        digit1 = int(dec1_padded[i])
                        digit2 = int(dec2_padded[i])

                        place_name = ['tenths', 'hundredths', 'thousandths', 'ten-thousandths'][i] if i < 4 else f'10^-{i+1}'

                        if digit1 != digit2:
                            steps.append(f"In {place_name} place: {digit1} vs {digit2}")
                            if digit1 > digit2:
                                steps.append(f"Since {digit1} > {digit2}, we have {decimal1} > {decimal2}")
                            else:
                                steps.append(f"Since {digit2} > {digit1}, we have {decimal2} > {decimal1}")
                            break
                    else:
                        steps.append("All decimal places are equal")

                result_text = f"{correct_answer} is larger"

            steps.append(f"Final answer: {result_text}")

        return steps

    def _generate_concise_steps(self, problem: Problem, decimals: List[float], correct_answer: str,
                                 is_word_problem: bool, word_problem_type: str, template: str) -> List[str]:
        """Generate concise steps with just formulas and values."""
        steps = [f"Problem: {problem.text}"]

        # For word problems, show extraction step
        if is_word_problem:
            if word_problem_type == 'three_number_ordering':
                steps.append(f"Values: {', '.join(map(str, decimals))}")
            else:
                steps.append(f"Values: {decimals[0]}, {decimals[1]}")

        # Handle multiple decimals
        if len(decimals) > 2:
            steps.append(f"Compare: {', '.join(map(str, decimals))}")
            steps.append(f"max({', '.join(map(str, decimals))}) = {correct_answer}")
        else:
            # Handle two decimals
            decimal1, decimal2 = decimals
            steps.append(f"{decimal1} vs {decimal2}")
            if decimal1 > decimal2:
                steps.append(f"{decimal1} > {decimal2}")
            elif decimal2 > decimal1:
                steps.append(f"{decimal2} > {decimal1}")
            else:
                steps.append(f"{decimal1} = {decimal2}")

        steps.append(correct_answer)

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct decimal comparison algorithm.

        Args:
            problem: Decimal comparison problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with correct comparison
        """
        # Check if this is a word problem
        is_word_problem = problem.metadata.get('is_word_problem', False)
        word_problem_type = problem.metadata.get('word_problem_type', None)
        template = problem.metadata.get('template', 'basic_comparison')
        decimals = problem.operands

        # Calculate correct answer by finding max value (NOT from metadata)
        larger = max(decimals)
        correct_answer = str(larger)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, decimals, correct_answer,
                                                  is_word_problem, word_problem_type, template)
        else:
            steps = self._generate_concise_steps(problem, decimals, correct_answer,
                                                  is_word_problem, word_problem_type, template)

        return Solution(
            answer=str(correct_answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
