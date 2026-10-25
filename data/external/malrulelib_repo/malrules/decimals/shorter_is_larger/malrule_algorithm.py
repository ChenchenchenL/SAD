"""
Malrule algorithm for Shorter-Is-Larger error.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class ShorterIsLargerMalrule(Malrule):
    """
    Students believe fewer decimal places means larger number.
    Opposite of Longer-Is-Larger.

    Example: 0.5 > 0.36 because 0.5 is "shorter"
    """

    def get_name(self) -> str:
        return "Shorter-Is-Larger"

    def get_description(self) -> str:
        return (
            "Students incorrectly believe that decimals with fewer decimal places are "
            "larger. For example, they think 0.3 is larger than 0.496. This misconception "
            "is linked to denominator-focused thinking, reciprocal thinking, or fraction "
            "knowledge interference (Steinle & Stacey, 1998; Resnick et al., 1989)."
        )

    def calculate_expected_answer(self, problem: Problem) -> str:
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Calculate malrule answer from operands (NOT from metadata)
        decimals = problem.operands

        # Count decimal places for each number
        digit_counts = []
        for d in decimals:
            str_d = str(d)
            if '.' in str_d:
                decimal_part = str_d.split('.')[1]
                digit_counts.append((d, len(decimal_part)))
            else:
                digit_counts.append((d, 0))

        # MALRULE: The one with FEWEST decimal digits is "larger"
        # If tie in decimal places, use the max value as fallback
        min_digits = min(digit_counts, key=lambda x: x[1])[1]
        candidates_with_min_digits = [d for d, count in digit_counts if count == min_digits]

        # If multiple have same min digits, pick the max among them
        shorter_decimal = max(candidates_with_min_digits)

        # Check if we need to format with $ for money context
        template = problem.metadata.get('template', '')
        if template == 'money_context':
            return f'${shorter_decimal}'

        return str(shorter_decimal)

    def _generate_verbose_steps(self, problem: Problem, decimals: List[float], malrule_answer: str,
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
            steps.append("Step 2: Apply malrule (shorter is larger)")
            steps.append("")
        else:
            steps.append(f"Problem: {problem.text}")
            steps.append("")

        steps.append("MALRULE: Shorter decimal (fewer decimal places) is larger")
        steps.append("")

        # Template-specific reasoning
        if template == 'basic_comparison':
            # Calculate decimal places for each number
            if len(decimals) >= 2:
                d1, d2 = decimals[0], decimals[1]
                d1_str = str(d1)
                d2_str = str(d2)
                d1_places = len(d1_str.split('.')[1]) if '.' in d1_str else 0
                d2_places = len(d2_str.split('.')[1]) if '.' in d2_str else 0

                steps.append(f"  {d1} has {d1_places} decimal place(s)")
                steps.append(f"  {d2} has {d2_places} decimal place(s)")
                steps.append(f"  MALRULE REASONING: 'Fewer places means closer to whole number, so larger'")

                if d1_places < d2_places:
                    steps.append(f"  {d1} is shorter, so {d1} is larger")
                elif d2_places < d1_places:
                    steps.append(f"  {d2} is shorter, so {d2} is larger")
                else:
                    steps.append(f"  Same number of places, comparing values normally")

        elif template == 'ordering':
            steps.append("MALRULE REASONING: 'The decimal with fewest places is largest'")
            steps.append(f"  Comparing {len(decimals)} decimals by number of decimal places")
            for d in decimals:
                d_str = str(d)
                d_places = len(d_str.split('.')[1]) if '.' in d_str else 0
                steps.append(f"    {d} has {d_places} decimal place(s)")
            steps.append(f"  Shortest decimal is considered largest")

        elif template == 'money_context':
            if len(decimals) >= 2:
                d1, d2 = decimals[0], decimals[1]
                d1_str = str(d1)
                d2_str = str(d2)
                d1_places = len(d1_str.split('.')[1]) if '.' in d1_str else 0
                d2_places = len(d2_str.split('.')[1]) if '.' in d2_str else 0
                steps.append(f"  ${d1} has {d1_places} decimal place(s)")
                steps.append(f"  ${d2} has {d2_places} decimal place(s)")
                steps.append(f"  MALRULE REASONING: 'Less precision means more money'")
                shorter_decimal = d1 if d1_places < d2_places else d2
                steps.append(f"  ${shorter_decimal} is shorter, so ${shorter_decimal} is more")

        elif template == 'measurement_context':
            unit = problem.metadata.get('unit', 'units')
            if len(decimals) >= 2:
                d1, d2 = decimals[0], decimals[1]
                d1_str = str(d1)
                d2_str = str(d2)
                d1_places = len(d1_str.split('.')[1]) if '.' in d1_str else 0
                d2_places = len(d2_str.split('.')[1]) if '.' in d2_str else 0
                steps.append(f"  {d1} {unit} has {d1_places} decimal place(s)")
                steps.append(f"  {d2} {unit} has {d2_places} decimal place(s)")
                steps.append(f"  MALRULE REASONING: 'Fewer places means larger measurement'")
                shorter_decimal = d1 if d1_places < d2_places else d2
                steps.append(f"  {shorter_decimal} {unit} is shorter, so it's greater")

        elif template == 'number_line':
            if len(decimals) >= 2:
                d1, d2 = decimals[0], decimals[1]
                d1_str = str(d1)
                d2_str = str(d2)
                d1_places = len(d1_str.split('.')[1]) if '.' in d1_str else 0
                d2_places = len(d2_str.split('.')[1]) if '.' in d2_str else 0
                steps.append(f"  {d1} has {d1_places} decimal place(s)")
                steps.append(f"  {d2} has {d2_places} decimal place(s)")
                steps.append(f"  MALRULE REASONING: 'Shorter decimals are further right on number line'")
                shorter_decimal = d1 if d1_places < d2_places else d2
                steps.append(f"  {shorter_decimal} is shorter, so it's greater")

        else:
            # Fallback: show decimal place counts for all operands
            steps.append("  Counting decimal places:")
            for d in decimals:
                d_str = str(d)
                d_places = len(d_str.split('.')[1]) if '.' in d_str else 0
                steps.append(f"    {d} has {d_places} decimal place(s)")
            steps.append(f"  MALRULE REASONING: 'Fewest places means closest to whole number, so largest'")

        steps.append("")
        steps.append(f"Final Answer: {malrule_answer} (INCORRECT - confused length with value!)")

        return steps

    def _generate_concise_steps(self, problem: Problem, decimals: List[float], malrule_answer: str,
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
        if template == 'basic_comparison':
            if len(decimals) >= 2:
                d1, d2 = decimals[0], decimals[1]
                d1_str = str(d1)
                d2_str = str(d2)
                d1_places = len(d1_str.split('.')[1]) if '.' in d1_str else 0
                d2_places = len(d2_str.split('.')[1]) if '.' in d2_str else 0
                steps.append(f"{d1}: {d1_places} places, {d2}: {d2_places} places")
                steps.append(f"min_places({d1}, {d2}) = {malrule_answer}")

        elif template == 'ordering':
            place_counts = []
            for d in decimals:
                d_str = str(d)
                d_places = len(d_str.split('.')[1]) if '.' in d_str else 0
                place_counts.append(f"{d}:{d_places}")
            steps.append(f"Places: {', '.join(place_counts)}")
            steps.append(f"shortest = {malrule_answer}")

        elif template == 'money_context':
            if len(decimals) >= 2:
                d1, d2 = decimals[0], decimals[1]
                d1_str = str(d1)
                d2_str = str(d2)
                d1_places = len(d1_str.split('.')[1]) if '.' in d1_str else 0
                d2_places = len(d2_str.split('.')[1]) if '.' in d2_str else 0
                steps.append(f"${d1}: {d1_places} places, ${d2}: {d2_places} places")
                steps.append(f"min_places(${d1}, ${d2}) = {malrule_answer}")

        elif template == 'measurement_context':
            unit = problem.metadata.get('unit', 'units')
            if len(decimals) >= 2:
                d1, d2 = decimals[0], decimals[1]
                d1_str = str(d1)
                d2_str = str(d2)
                d1_places = len(d1_str.split('.')[1]) if '.' in d1_str else 0
                d2_places = len(d2_str.split('.')[1]) if '.' in d2_str else 0
                steps.append(f"{d1} {unit}: {d1_places} places, {d2} {unit}: {d2_places} places")
                steps.append(f"min_places = {malrule_answer}")

        elif template == 'number_line':
            if len(decimals) >= 2:
                d1, d2 = decimals[0], decimals[1]
                d1_str = str(d1)
                d2_str = str(d2)
                d1_places = len(d1_str.split('.')[1]) if '.' in d1_str else 0
                d2_places = len(d2_str.split('.')[1]) if '.' in d2_str else 0
                steps.append(f"{d1}: {d1_places} places, {d2}: {d2_places} places")
                steps.append(f"min_places = {malrule_answer}")

        else:
            # Fallback
            place_counts = []
            for d in decimals:
                d_str = str(d)
                d_places = len(d_str.split('.')[1]) if '.' in d_str else 0
                place_counts.append(f"{d}:{d_places}")
            steps.append(f"Places: {', '.join(place_counts)}")

        steps.append(malrule_answer)

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the malrule to solve the problem incorrectly.

        Args:
            problem: The decimal comparison problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with incorrect answer based on shorter-is-larger logic
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
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
