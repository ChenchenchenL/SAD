"""
Correct algorithm for percentage relationship problems.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List, Any
from utils import CorrectAlgorithm, Problem, Solution


class PercentageRelationshipCorrectAlgorithm(CorrectAlgorithm):
    """Correctly calculates reverse percentage relationships."""

    def get_name(self) -> str:
        return "Correct Percentage Relationship"

    def get_description(self) -> str:
        return "Correctly calculates reverse percentage relationships using proper formula."

    def _generate_concise_steps(self, problem: Problem, correct_answer: Any, template: str) -> List[str]:
        """Generate concise steps showing only formula and values."""
        steps = []

        # Add question
        steps.append(problem.text)

        if template == 'basic_reverse_relationship':
            num1 = problem.metadata['num1']
            num2 = problem.metadata['num2']
            percentage = problem.metadata['percentage']

            steps.append(f"Formula: reverse_percent = (num2/num1) × 100")
            steps.append(f"({num2}/{num1}) × 100 = {correct_answer}%")

        elif template == 'percentage_increase':
            original = problem.metadata['original']
            new_value = problem.metadata['new_value']

            steps.append(f"Formula: decrease_percent = (difference/new_value) × 100")
            steps.append(f"difference = {new_value} - {original} = {new_value - original}")
            steps.append(f"({new_value - original}/{new_value}) × 100 = {correct_answer}%")

        elif template == 'percentage_decrease':
            original = problem.metadata['original']
            new_value = problem.metadata['new_value']

            steps.append(f"Formula: increase_percent = (difference/new_value) × 100")
            steps.append(f"difference = {original} - {new_value} = {original - new_value}")
            steps.append(f"({original - new_value}/{new_value}) × 100 = {correct_answer}%")

        elif template == 'comparison_statements':
            percentage = problem.metadata['percentage']

            steps.append(f"Formula: reverse_percent = (100/percentage) × 100")
            steps.append(f"(100/{percentage}) × 100 = {correct_answer}%")

        elif template == 'word_problem':
            formula_type = problem.metadata.get('formula_type')
            if formula_type == 'increase_then_reverse':
                original = problem.metadata['original']
                new_value = problem.metadata['new_value']
                steps.append(f"Formula: decrease_percent = (difference/new_value) × 100")
                steps.append(f"({new_value - original}/{new_value}) × 100 = {correct_answer}%")
            elif formula_type == 'decrease_then_reverse':
                original = problem.metadata['original']
                new_value = problem.metadata['new_value']
                steps.append(f"Formula: increase_percent = (difference/new_value) × 100")
                steps.append(f"({original - new_value}/{new_value}) × 100 = {correct_answer}%")
            elif formula_type == 'reverse_relationship':
                num1 = problem.metadata['num1']
                num2 = problem.metadata['num2']
                steps.append(f"Formula: reverse_percent = (num2/num1) × 100")
                steps.append(f"({num2}/{num1}) × 100 = {correct_answer}%")
            elif formula_type == 'comparison_asymmetry':
                percentage = problem.metadata['percentage']
                steps.append(f"Formula: reverse_percent = (100/percentage) × 100")
                steps.append(f"(100/{percentage}) × 100 = {correct_answer}%")

        steps.append(f"Answer: {correct_answer}%")
        return steps

    def _generate_verbose_steps(self, problem: Problem, correct_answer: Any, template: str) -> List[str]:
        """Generate verbose steps with full explanations (original format)."""
        steps = []

        if template == 'basic_reverse_relationship':
            num1 = problem.metadata['num1']
            num2 = problem.metadata['num2']
            percentage = problem.metadata['percentage']

            steps.append(f"Problem: If {num1} is {percentage}% of {num2},")
            steps.append(f"         what percent is {num2} of {num1}?")
            steps.append("")
            steps.append("Step 1: Understand the given relationship")
            steps.append(f"  {num1} = ({percentage}/100) × {num2}")
            steps.append(f"  {num1} = {(percentage/100) * num2} ✓")
            steps.append("")
            steps.append("Step 2: Set up reverse relationship")
            steps.append(f"  We want: {num2} = (x/100) × {num1}")
            steps.append("")
            steps.append("Step 3: Solve for x")
            steps.append(f"  x = ({num2}/{num1}) × 100")
            steps.append(f"  x = {round(num2/num1, 2)} × 100")
            steps.append(f"  x = {correct_answer}%")
            steps.append("")
            steps.append("Step 4: Verify")
            steps.append(f"  {correct_answer}% of {num1} = {round((correct_answer/100) * num1, 2)}")
            steps.append(f"  ≈ {num2} ✓")
            steps.append("")
            steps.append(f"Note: {num1} is {percentage}% of {num2}, but {num2} is {correct_answer}% of {num1}")
            steps.append("      Percentage relationships are NOT symmetric!")

        elif template == 'percentage_increase':
            original = problem.metadata['original']
            new_value = problem.metadata['new_value']
            increase_pct = problem.metadata['increase_pct']

            steps.append(f"Problem: Value increased from {original} to {new_value} ({increase_pct}% increase).")
            steps.append(f"         What is the percent decrease from {new_value} back to {original}?")
            steps.append("")
            steps.append("Step 1: Calculate the difference")
            steps.append(f"  Difference: {new_value} - {original} = {new_value - original}")
            steps.append("")
            steps.append("Step 2: Calculate percent decrease (use NEW value as base)")
            steps.append(f"  Percent decrease = (difference / new value) × 100")
            steps.append(f"  = ({new_value - original} / {new_value}) × 100")
            steps.append(f"  = {correct_answer}%")
            steps.append("")
            steps.append("Step 3: Verify")
            steps.append(f"  {correct_answer}% of {new_value} = {round((correct_answer/100) * new_value, 2)}")
            steps.append(f"  {new_value} - {round((correct_answer/100) * new_value, 2)} ≈ {original} ✓")
            steps.append("")
            steps.append(f"Note: {increase_pct}% increase requires {correct_answer}% decrease to reverse")
            steps.append("      The percentages are NOT the same!")

        elif template == 'percentage_decrease':
            original = problem.metadata['original']
            new_value = problem.metadata['new_value']
            decrease_pct = problem.metadata['decrease_pct']

            steps.append(f"Problem: Value decreased from {original} to {new_value} ({decrease_pct}% decrease).")
            steps.append(f"         What is the percent increase from {new_value} back to {original}?")
            steps.append("")
            steps.append("Step 1: Calculate the difference")
            steps.append(f"  Difference: {original} - {new_value} = {original - new_value}")
            steps.append("")
            steps.append("Step 2: Calculate percent increase (use NEW value as base)")
            steps.append(f"  Percent increase = (difference / new value) × 100")
            steps.append(f"  = ({original - new_value} / {new_value}) × 100")
            steps.append(f"  = {correct_answer}%")
            steps.append("")
            steps.append("Step 3: Verify")
            steps.append(f"  {correct_answer}% of {new_value} = {round((correct_answer/100) * new_value, 2)}")
            steps.append(f"  {new_value} + {round((correct_answer/100) * new_value, 2)} ≈ {original} ✓")
            steps.append("")
            steps.append(f"Note: {decrease_pct}% decrease requires {correct_answer}% increase to reverse")
            steps.append("      The percentages are NOT the same!")

        elif template == 'comparison_statements':
            percentage = problem.metadata['percentage']
            person1 = problem.metadata['person1']
            person2 = problem.metadata['person2']
            item = problem.metadata['item']

            steps.append(f"Problem: {person1} has {percentage}% as much {item} as {person2}.")
            steps.append(f"         What percent of {person1}'s {item} does {person2} have?")
            steps.append("")
            steps.append("Step 1: Set up the relationship")
            steps.append(f"  Let {person2}'s amount = B")
            steps.append(f"  Then {person1}'s amount = {percentage}% of B = {percentage/100}B")
            steps.append("")
            steps.append("Step 2: Find reverse percentage")
            steps.append(f"  We want: B as a percent of {person1}'s amount")
            steps.append(f"  B / ({percentage/100}B) × 100")
            steps.append(f"  = 1 / {percentage/100} × 100")
            steps.append(f"  = {100/percentage} × 100")
            steps.append(f"  = {correct_answer}%")
            steps.append("")
            steps.append(f"Example: If {person1} = {percentage}, {person2} = 100,")
            steps.append(f"         then {person2}/{person1} × 100 = {100/percentage} × 100 = {correct_answer}%")

        elif template == 'word_problem':
            formula_type = problem.metadata.get('formula_type')

            steps.append(f"Problem: {problem.text}")
            steps.append("")

            if formula_type == 'increase_then_reverse' or 'increase_pct' in problem.metadata:
                original = problem.metadata['original']
                new_value = problem.metadata['new_value']
                increase_pct = problem.metadata.get('increase_pct', 0)

                steps.append("Step 1: Calculate the difference")
                steps.append(f"  Difference: {new_value} - {original} = {new_value - original}")
                steps.append("")
                steps.append("Step 2: Calculate percent decrease (base = NEW value)")
                steps.append(f"  Percent = ({new_value - original} / {new_value}) × 100")
                steps.append(f"  = {correct_answer}%")
                steps.append("")
                steps.append(f"Note: {increase_pct}% increase requires {correct_answer}% decrease")
            elif formula_type == 'decrease_then_reverse' or 'decrease_pct' in problem.metadata:
                original = problem.metadata['original']
                new_value = problem.metadata['new_value']
                decrease_pct = problem.metadata.get('decrease_pct', 0)

                steps.append("Step 1: Calculate the difference")
                steps.append(f"  Difference: {original} - {new_value} = {original - new_value}")
                steps.append("")
                steps.append("Step 2: Calculate percent increase (base = NEW value)")
                steps.append(f"  Percent = ({original - new_value} / {new_value}) × 100")
                steps.append(f"  = {correct_answer}%")
                steps.append("")
                steps.append(f"Note: {decrease_pct}% decrease requires {correct_answer}% increase")
            elif formula_type == 'reverse_relationship':
                num1 = problem.metadata['num1']
                num2 = problem.metadata['num2']
                percentage = problem.metadata['percentage']
                steps.append(f"Step 1: Given {num1} is {percentage}% of {num2}")
                steps.append(f"Step 2: Find reverse: {num2} / {num1} × 100 = {correct_answer}%")
            elif formula_type == 'comparison_asymmetry':
                percentage = problem.metadata['percentage']
                steps.append(f"Step 1: If one has {percentage}% as much")
                steps.append(f"Step 2: Reverse: 100 / {percentage} × 100 = {correct_answer}%")

        steps.append("")
        steps.append(f"Final Answer: {correct_answer}% ✓")
        steps.append("")
        steps.append("Key insight: Percentage relationships depend on the BASE value!")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        template = problem.metadata.get('template', 'basic_reverse_relationship')

        # Calculate correct answer first
        if template == 'basic_reverse_relationship':
            num1 = problem.metadata['num1']
            num2 = problem.metadata['num2']
            correct_answer = round((num2 / num1) * 100) if num1 != 0 else 0

        elif template == 'percentage_increase':
            original = problem.metadata['original']
            new_value = problem.metadata['new_value']
            correct_answer = round(((new_value - original) / new_value) * 100, 1)

        elif template == 'percentage_decrease':
            original = problem.metadata['original']
            new_value = problem.metadata['new_value']
            correct_answer = round(((original - new_value) / new_value) * 100, 1)

        elif template == 'comparison_statements':
            percentage = problem.metadata['percentage']
            correct_answer = round((100 / percentage) * 100, 1)

        elif template == 'word_problem':
            formula_type = problem.metadata.get('formula_type')
            if formula_type == 'increase_then_reverse' or 'increase_pct' in problem.metadata:
                original = problem.metadata['original']
                new_value = problem.metadata['new_value']
                correct_answer = round(((new_value - original) / new_value) * 100, 1)
            elif formula_type == 'decrease_then_reverse' or 'decrease_pct' in problem.metadata:
                original = problem.metadata['original']
                new_value = problem.metadata['new_value']
                correct_answer = round(((original - new_value) / new_value) * 100, 1)
            elif formula_type == 'reverse_relationship':
                num1 = problem.metadata['num1']
                num2 = problem.metadata['num2']
                correct_answer = round((num2 / num1) * 100) if num1 != 0 else 0
            elif formula_type == 'comparison_asymmetry':
                percentage = problem.metadata['percentage']
                correct_answer = round((100 / percentage) * 100, 1)
            else:
                correct_answer = 0
        else:
            raise ValueError(f"Unknown template: {template}")

        if verbose:
            steps = self._generate_verbose_steps(problem, correct_answer, template)
        else:
            steps = self._generate_concise_steps(problem, correct_answer, template)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _solve_word_problem(self, problem: Problem, formula_type: str, verbose: bool = False) -> Solution:
        """Solve formula-based word problems."""
        if formula_type == 'increase_then_reverse':
            original = problem.metadata['original']
            new_value = problem.metadata['new_value']
            correct_answer = round(((new_value - original) / new_value) * 100, 1)

        elif formula_type == 'decrease_then_reverse':
            original = problem.metadata['original']
            new_value = problem.metadata['new_value']
            correct_answer = round(((original - new_value) / new_value) * 100, 1)

        elif formula_type == 'reverse_relationship':
            num1 = problem.metadata['num1']
            num2 = problem.metadata['num2']
            correct_answer = round((num2 / num1) * 100) if num1 != 0 else 0

        elif formula_type == 'comparison_asymmetry':
            percentage = problem.metadata['percentage']
            correct_answer = round((100 / percentage) * 100, 1)
        else:
            raise ValueError(f"Unknown formula_type: {formula_type}")

        if verbose:
            steps = self._generate_verbose_steps(problem, correct_answer, 'word_problem')
        else:
            steps = self._generate_concise_steps(problem, correct_answer, 'word_problem')

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
