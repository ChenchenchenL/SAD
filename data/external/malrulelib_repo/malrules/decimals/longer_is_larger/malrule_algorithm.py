"""
Longer-Is-Larger malrule algorithm.

Implements the systematic error where students incorrectly believe that
more decimal digits means a larger number.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List

class LongerIsLargerMalrule(Malrule):
    """
    Implements the Longer-Is-Larger bug.

    Students incorrectly believe that a decimal number with more digits after
    the decimal point is larger. For example, they think 0.36 > 0.5 because
    36 > 5, treating the decimal portion as if it were a whole number.

    This stems from overgeneralizing whole number comparison rules to decimals.
    """

    def get_name(self) -> str:
        return "Longer-Is-Larger"

    def get_description(self) -> str:
        return (
            "When comparing decimal numbers, students incorrectly believe that "
            "more decimal digits means a larger number. For example, they think "
            "0.45 is larger than 0.8 because 0.45 has more digits. This stems from "
            "overgeneralizing whole number comparison rules to decimals, a phenomenon "
            "extensively documented by Steinle & Stacey (1998, 2004) as one of the "
            "most prevalent decimal misconceptions."
        )

    def calculate_expected_answer(self, problem: Problem) -> str:
        """
        Calculate the expected incorrect answer for this malrule.

        For Longer-Is-Larger:
        - Student counts decimal digits in each number
        - MALRULE: The one with MORE decimal digits is "larger"
        - If same number of digits, fall back to correct comparison

        Example: Compare 0.5 and 0.36
        - Correct: 0.5 > 0.36
        - MALRULE: 0.36 has 2 decimal digits, 0.5 has 1, so 0.36 is "larger"

        Args:
            problem: Decimal comparison problem

        Returns:
            Expected incorrect answer as string
        """
        decimals = problem.operands

        # Handle multiple decimals (find the one with most digits)
        if len(decimals) > 2:
            # Count decimal places for each
            digit_counts = []
            for d in decimals:
                str_d = str(d)
                if '.' in str_d:
                    decimal_part = str_d.split('.')[1]
                    digit_counts.append((d, len(decimal_part)))
                else:
                    digit_counts.append((d, 0))

            # MALRULE: Pick the one with the most decimal digits
            larger = max(digit_counts, key=lambda x: x[1])[0]
            return str(larger)

        # Handle two decimals
        decimal1, decimal2 = decimals

        # Convert to strings to count decimal places
        str1 = str(decimal1)
        str2 = str(decimal2)

        # Get decimal parts
        if '.' in str1:
            decimal_part1 = str1.split('.')[1]
        else:
            decimal_part1 = ''

        if '.' in str2:
            decimal_part2 = str2.split('.')[1]
        else:
            decimal_part2 = ''

        len1 = len(decimal_part1)
        len2 = len(decimal_part2)

        # MALRULE: More decimal digits means larger number
        if len1 > len2:
            return str(decimal1)
        elif len2 > len1:
            return str(decimal2)
        else:
            # Same number of digits - fall back to correct comparison
            return str(max(decimal1, decimal2))

    def _generate_verbose_steps(self, problem: Problem, decimals: List, malrule_answer: str,
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
            steps.append("Step 2: Apply malrule (longer is larger)")
            steps.append("")
        else:
            steps.append(f"Problem: {problem.text}")
            steps.append("")

        steps.append("MALRULE: Longer decimal (more digits) = larger number")
        steps.append("  Student belief: 'More decimal places means bigger value'")
        steps.append("")

        # Handle multiple decimals (find the one with most digits)
        if len(decimals) > 2:
            steps.append(f"Comparing {', '.join(map(str, decimals))}")
            steps.append("Counting decimal digits in each number:")

            # Count decimal places for each
            digit_counts = []
            for d in decimals:
                str_d = str(d)
                if '.' in str_d:
                    decimal_part = str_d.split('.')[1]
                    digit_counts.append((d, len(decimal_part)))
                else:
                    digit_counts.append((d, 0))
                steps.append(f"  {d} has {digit_counts[-1][1]} decimal digit(s)")

            # MALRULE: Pick the one with the most decimal digits
            longer_decimal = problem.metadata.get('longer_decimal', max(digit_counts, key=lambda x: x[1])[0])
            max_digits = max(digit_counts, key=lambda x: x[1])[1]

            steps.append("")
            steps.append(
                f"MALRULE REASONING: {longer_decimal} has the most decimal digits ({max_digits}), "
                f"so it must be the largest!"
            )
            steps.append("")
            steps.append(f"Answer: {malrule_answer} (INCORRECT - longer doesn't mean larger!)")

        else:
            # Handle two decimals
            decimal1, decimal2 = decimals

            # Convert to strings to count decimal places
            str1 = str(decimal1)
            str2 = str(decimal2)

            # Get decimal parts
            if '.' in str1:
                decimal_part1 = str1.split('.')[1]
            else:
                decimal_part1 = ''

            if '.' in str2:
                decimal_part2 = str2.split('.')[1]
            else:
                decimal_part2 = ''

            len1 = len(decimal_part1)
            len2 = len(decimal_part2)

            steps.append(f"Comparing {decimal1} and {decimal2}")
            steps.append(f"  {decimal1} has {len1} decimal digit(s)")
            steps.append(f"  {decimal2} has {len2} decimal digit(s)")
            steps.append("")

            # MALRULE: More decimal digits means larger number
            if len1 > len2:
                steps.append(
                    f"MALRULE REASONING: {decimal1} has more decimal digits ({len1} > {len2}), "
                    f"so {decimal1} must be larger!"
                )
            elif len2 > len1:
                steps.append(
                    f"MALRULE REASONING: {decimal2} has more decimal digits ({len2} > {len1}), "
                    f"so {decimal2} must be larger!"
                )
            else:
                steps.append(f"Same number of decimal digits, comparing values normally")

            steps.append("")
            steps.append(f"Answer: {malrule_answer} (INCORRECT - longer doesn't mean larger!)")

        return steps

    def _generate_concise_steps(self, problem: Problem, decimals: List, malrule_answer: str,
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
            place_counts = []
            for d in decimals:
                str_d = str(d)
                d_places = len(str_d.split('.')[1]) if '.' in str_d else 0
                place_counts.append(f"{d}:{d_places}")
            steps.append(f"Places: {', '.join(place_counts)}")
            steps.append(f"max_places = {malrule_answer}")
        else:
            # Handle two decimals
            decimal1, decimal2 = decimals
            str1 = str(decimal1)
            str2 = str(decimal2)
            len1 = len(str1.split('.')[1]) if '.' in str1 else 0
            len2 = len(str2.split('.')[1]) if '.' in str2 else 0
            steps.append(f"{decimal1}: {len1} places, {decimal2}: {len2} places")
            steps.append(f"max_places({decimal1}, {decimal2}) = {malrule_answer}")

        steps.append(malrule_answer)

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Longer-Is-Larger malrule to compare decimals incorrectly.

        Args:
            problem: Decimal comparison problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with incorrect comparison based on number of digits
        """
        # Check if this is a word problem
        is_word_problem = problem.metadata.get('is_word_problem', False)
        word_problem_type = problem.metadata.get('word_problem_type', None)
        template = problem.metadata.get('template', 'basic_comparison')
        decimals = problem.operands

        # Calculate malrule answer (NOT from metadata)
        malrule_answer = self.calculate_expected_answer(problem)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, decimals, malrule_answer,
                                                  is_word_problem, word_problem_type, template)
        else:
            steps = self._generate_concise_steps(problem, decimals, malrule_answer,
                                                  is_word_problem, word_problem_type, template)

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
