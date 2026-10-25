"""
Malrule algorithm for Reverse-Percentage-Error.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class ReversePercentageErrorMalrule(Malrule):
    """
    Students incorrectly believe percentage relationships are symmetric.

    Example: If A is 50% of B, student thinks B is 50% of A
    """

    def get_name(self) -> str:
        return "Percentage Reversal Asymmetry Error"

    def get_description(self) -> str:
        return (
            "Students incorrectly believe that percentage relationships are symmetric or "
            "reversible. They assume that if a value increased by X%, it can return to the "
            "original by decreasing X%, or that if A is X% of B, then B is X% of A. This "
            "misconception stems from overgeneralizing the commutative property of addition "
            "and multiplication to percentage relationships, which are inherently asymmetric "
            "because each percentage is calculated relative to a different base value."
        )

    def _generate_concise_steps(self, problem: Problem, malrule_answer: Any, template: str) -> List[str]:
        """Generate concise steps showing only formula and values."""
        steps = []

        # Add question
        steps.append(problem.text)

        if template == 'basic_reverse_relationship':
            percentage = problem.metadata['percentage']
            steps.append(f"Formula: reverse_percent = same percentage")
            steps.append(f"reverse_percent = {malrule_answer}%")

        elif template == 'percentage_increase':
            steps.append(f"Formula: decrease to reverse = same percentage")
            steps.append(f"decrease_percent = {malrule_answer}%")

        elif template == 'percentage_decrease':
            steps.append(f"Formula: increase to reverse = same percentage")
            steps.append(f"increase_percent = {malrule_answer}%")

        elif template == 'comparison_statements':
            steps.append(f"Formula: reverse_percent = same percentage")
            steps.append(f"reverse_percent = {malrule_answer}%")

        elif template == 'word_problem':
            formula_type = problem.metadata.get('formula_type')
            if formula_type in ['increase_then_reverse', None] and 'increase_pct' in problem.metadata:
                steps.append(f"Formula: decrease to reverse = same percentage")
            elif formula_type == 'decrease_then_reverse' or 'decrease_pct' in problem.metadata:
                steps.append(f"Formula: increase to reverse = same percentage")
            elif formula_type in ['reverse_relationship', 'comparison_asymmetry']:
                steps.append(f"Formula: reverse_percent = same percentage")
            steps.append(f"result = {malrule_answer}%")

        steps.append(f"Answer: {malrule_answer}%")
        return steps

    def _generate_verbose_steps(self, problem: Problem, malrule_answer: Any, template: str) -> List[str]:
        """Generate verbose steps with full explanations (original format)."""
        steps = []

        if template == 'basic_reverse_relationship':
            num1 = problem.metadata['num1']
            num2 = problem.metadata['num2']
            percentage = problem.metadata['percentage']

            steps.append(f"Problem: If {num1} is {percentage}% of {num2},")
            steps.append(f"         what percent is {num2} of {num1}?")
            steps.append("")
            steps.append("MALRULE: Percentage relationships are symmetric")
            steps.append(f"  MALRULE REASONING: 'The percentage works the same both ways'")
            steps.append("")
            steps.append(f"Given: {num1} is {percentage}% of {num2}")
            steps.append(f"Therefore (MALRULE): {num2} is {percentage}% of {num1}")
            steps.append("")
            steps.append(f"Check (malrule student doesn't do this):")
            steps.append(f"  {percentage}% of {num1} = {(percentage/100) * num1}")
            steps.append(f"  Does that equal {num2}? {(percentage/100) * num1 == num2}")

        elif template == 'percentage_increase':
            original = problem.metadata['original']
            new_value = problem.metadata['new_value']
            increase_pct = problem.metadata['increase_pct']

            steps.append(f"Problem: Value increased from {original} to {new_value} ({increase_pct}% increase).")
            steps.append(f"         What is the percent decrease from {new_value} back to {original}?")
            steps.append("")
            steps.append("MALRULE: Increase and decrease percentages are symmetric")
            steps.append(f"  MALRULE REASONING: 'If it increased by {increase_pct}%, it must decrease by {increase_pct}%'")
            steps.append("")
            steps.append(f"Given: Increased by {increase_pct}%")
            steps.append(f"Therefore (MALRULE): Decrease is also {increase_pct}%")
            steps.append("")
            steps.append(f"(Malrule student doesn't verify: {increase_pct}% of {new_value} = {(increase_pct/100) * new_value})")

        elif template == 'percentage_decrease':
            original = problem.metadata['original']
            new_value = problem.metadata['new_value']
            decrease_pct = problem.metadata['decrease_pct']

            steps.append(f"Problem: Value decreased from {original} to {new_value} ({decrease_pct}% decrease).")
            steps.append(f"         What is the percent increase from {new_value} back to {original}?")
            steps.append("")
            steps.append("MALRULE: Decrease and increase percentages are symmetric")
            steps.append(f"  MALRULE REASONING: 'If it decreased by {decrease_pct}%, it must increase by {decrease_pct}%'")
            steps.append("")
            steps.append(f"Given: Decreased by {decrease_pct}%")
            steps.append(f"Therefore (MALRULE): Increase is also {decrease_pct}%")
            steps.append("")
            steps.append("(Malrule student doesn't verify the calculation)")

        elif template == 'comparison_statements':
            percentage = problem.metadata['percentage']
            person1 = problem.metadata['person1']
            person2 = problem.metadata['person2']
            item = problem.metadata['item']

            steps.append(f"Problem: {person1} has {percentage}% as much {item} as {person2}.")
            steps.append(f"         What percent of {person1}'s {item} does {person2} have?")
            steps.append("")
            steps.append("MALRULE: Comparison percentages are symmetric")
            steps.append(f"  MALRULE REASONING: 'If {person1} has {percentage}% of {person2}'s,")
            steps.append(f"                      then {person2} has {percentage}% of {person1}'s'")
            steps.append("")
            steps.append(f"Given: {person1} = {percentage}% of {person2}")
            steps.append(f"Therefore (MALRULE): {person2} = {percentage}% of {person1}")

        elif template == 'word_problem':
            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("MALRULE: Percentage changes are symmetric/reversible")
            steps.append(f"  MALRULE REASONING: 'The percentage is the same going both directions'")
            steps.append("")

            formula_type = problem.metadata.get('formula_type')
            if formula_type in ['increase_then_reverse', None] and 'increase_pct' in problem.metadata:
                increase_pct = problem.metadata.get('increase_pct', malrule_answer)
                steps.append(f"Given: {increase_pct}% increase")
                steps.append(f"Therefore (MALRULE): {increase_pct}% decrease to reverse it")
            elif formula_type == 'decrease_then_reverse' or 'decrease_pct' in problem.metadata:
                decrease_pct = problem.metadata.get('decrease_pct', malrule_answer)
                steps.append(f"Given: {decrease_pct}% decrease")
                steps.append(f"Therefore (MALRULE): {decrease_pct}% increase to reverse it")
            elif formula_type in ['reverse_relationship', 'comparison_asymmetry']:
                percentage = problem.metadata.get('percentage', malrule_answer)
                steps.append(f"Given: {percentage}%")
                steps.append(f"Therefore (MALRULE): reverse is also {percentage}%")

        steps.append("")
        steps.append(f"Final Answer: {malrule_answer}%")
        steps.append("")
        steps.append("INCORRECT! Percentage relationships are NOT symmetric. ")
        steps.append("The percentage depends on which value is the base (denominator).")

        return steps

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Malrule: percentage relationships are symmetric/reversible
        template = problem.metadata.get('template', 'basic_reverse_relationship')

        if template in ['basic_reverse_relationship', 'comparison_statements']:
            # Student thinks the percentage is the same in reverse
            return problem.metadata['percentage']
        elif template == 'percentage_increase':
            # Student thinks the reverse decrease is the same percentage
            return problem.metadata['increase_pct']
        elif template == 'percentage_decrease':
            # Student thinks the reverse increase is the same percentage
            return problem.metadata['decrease_pct']
        elif template == 'word_problem':
            formula_type = problem.metadata.get('formula_type')
            if formula_type == 'increase_then_reverse':
                return problem.metadata['increase_pct']
            elif formula_type == 'decrease_then_reverse':
                return problem.metadata['decrease_pct']
            elif formula_type == 'reverse_relationship':
                return problem.metadata['percentage']
            elif formula_type == 'comparison_asymmetry':
                return problem.metadata['percentage']
            # Old format
            if 'increase_pct' in problem.metadata:
                return problem.metadata['increase_pct']
            else:
                return problem.metadata['decrease_pct']

        # Fallback - should not reach here
        return problem.metadata.get('malrule_answer', 0)

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        template = problem.metadata.get('template', 'basic_reverse_relationship')

        # Calculate malrule answer first
        if template == 'basic_reverse_relationship':
            malrule_answer = problem.metadata['percentage']

        elif template == 'percentage_increase':
            malrule_answer = problem.metadata['increase_pct']

        elif template == 'percentage_decrease':
            malrule_answer = problem.metadata['decrease_pct']

        elif template == 'comparison_statements':
            malrule_answer = problem.metadata['percentage']

        elif template == 'word_problem':
            formula_type = problem.metadata.get('formula_type')
            if formula_type:
                return self._apply_malrule_word_problem(problem, formula_type, verbose)

            if 'increase_pct' in problem.metadata:
                malrule_answer = problem.metadata['increase_pct']
            else:
                malrule_answer = problem.metadata['decrease_pct']
        else:
            raise ValueError(f"Unknown template: {template}")

        if verbose:
            steps = self._generate_verbose_steps(problem, malrule_answer, template)
        else:
            steps = self._generate_concise_steps(problem, malrule_answer, template)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _apply_malrule_word_problem(self, problem: Problem, formula_type: str, verbose: bool = False) -> Solution:
        """Apply malrule to formula-based word problems."""
        if formula_type == 'increase_then_reverse':
            malrule_answer = problem.metadata['increase_pct']

        elif formula_type == 'decrease_then_reverse':
            malrule_answer = problem.metadata['decrease_pct']

        elif formula_type == 'reverse_relationship':
            malrule_answer = problem.metadata['percentage']

        elif formula_type == 'comparison_asymmetry':
            malrule_answer = problem.metadata['percentage']
        else:
            raise ValueError(f"Unknown formula_type: {formula_type}")

        if verbose:
            steps = self._generate_verbose_steps(problem, malrule_answer, 'word_problem')
        else:
            steps = self._generate_concise_steps(problem, malrule_answer, 'word_problem')

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
