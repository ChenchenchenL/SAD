"""
Malrule algorithm for Percentage-As-Index error.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class PercentageAsIndexMalrule(Malrule):
    """
    Students treat percentage as a position marker or index.

    Example: "30% of 50" → Student thinks answer is 30 (the percentage itself)
    """

    def get_name(self) -> str:
        return "Percentage as Absolute Value (Ignoring Base)"

    def get_description(self) -> str:
        return (
            "Students treat the percentage number as an absolute value or index, ignoring "
            "the base/whole that the percentage applies to. They confuse the percentage "
            "value (e.g., 30) with the result of the percentage calculation (30% of Y). "
            "This reflects a failure to understand that 'percent' means 'per hundred' and "
            "requires multiplication by the base value divided by 100."
        )

    def _generate_concise_steps(self, problem: Problem, malrule_answer: Any, template: str) -> List[str]:
        """Generate concise steps showing only formula and values."""
        steps = []

        # Add question
        steps.append(problem.text)

        if template == 'comparison_problem':
            percentage1 = problem.metadata['percentage']
            percentage2 = problem.operands[2] if len(problem.operands) > 2 else percentage1
            steps.append(f"Formula: compare percentage values directly")
            steps.append(f"Compare {percentage1} vs {percentage2}")

        elif template == 'word_problem_context':
            formula_type = problem.metadata.get('formula_type', 'basic_percentage')
            percentage = problem.metadata['percentage']

            if formula_type == 'basic_percentage':
                steps.append(f"Formula: result = percentage")
                steps.append(f"result = {percentage}")
            elif formula_type == 'percentage_increase':
                total = problem.metadata['total']
                steps.append(f"Formula: result = total + percentage")
                steps.append(f"{total} + {percentage} = {malrule_answer}")
            elif formula_type == 'percentage_decrease':
                total = problem.metadata['total']
                steps.append(f"Formula: result = total - percentage")
                steps.append(f"{total} - {percentage} = {malrule_answer}")
            elif formula_type == 'find_total_from_percentage':
                part = problem.metadata['part']
                steps.append(f"Formula: total = part ÷ percentage")
                steps.append(f"{part} ÷ {percentage} = {malrule_answer}")

        elif template == 'percentage_increase':
            percentage = problem.metadata['percentage']
            total = problem.metadata['total']
            steps.append(f"Formula: result = total + percentage")
            steps.append(f"{total} + {percentage} = {malrule_answer}")

        elif template == 'percentage_decrease':
            percentage = problem.metadata['percentage']
            total = problem.metadata['total']
            steps.append(f"Formula: result = total - percentage")
            steps.append(f"{total} - {percentage} = {malrule_answer}")

        else:  # basic_percentage
            percentage = problem.metadata['percentage']
            steps.append(f"Formula: result = percentage")
            steps.append(f"result = {percentage}")

        steps.append(f"Answer: {malrule_answer}")
        return steps

    def _generate_verbose_steps(self, problem: Problem, malrule_answer: Any, template: str) -> List[str]:
        """Generate verbose steps with full explanations (original format)."""
        steps = []

        if template == 'comparison_problem':
            percentage1 = problem.metadata['percentage']
            total1 = problem.operands[1]
            percentage2 = problem.operands[2] if len(problem.operands) > 2 else percentage1

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("MALRULE approach: Use percentage as index value")
            steps.append(f"  Compare {percentage1} vs {percentage2} (ignoring the totals)")
            steps.append(f"Result: {malrule_answer}")

        elif template == 'word_problem_context':
            formula_type = problem.metadata.get('formula_type', 'basic_percentage')
            percentage = problem.metadata['percentage']

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("MALRULE: Percentage is just a number, not a proportion")
            steps.append("")

            if formula_type == 'basic_percentage':
                steps.append(f"MALRULE REASONING: '{percentage}% means the number {percentage}'")
                steps.append(f"Answer: {percentage}")
            elif formula_type == 'percentage_increase':
                total = problem.metadata['total']
                steps.append(f"MALRULE REASONING: Increase by {percentage}% means add {percentage}")
                steps.append(f"Answer: {total} + {percentage} = {malrule_answer}")
            elif formula_type == 'percentage_decrease':
                total = problem.metadata['total']
                steps.append(f"MALRULE REASONING: Decrease by {percentage}% means subtract {percentage}")
                steps.append(f"Answer: {total} - {percentage} = {malrule_answer}")
            elif formula_type == 'find_total_from_percentage':
                part = problem.metadata['part']
                steps.append(f"MALRULE REASONING: {percentage}% is just {percentage}, so divide {part} by {percentage}")
                steps.append(f"Answer: {part} ÷ {percentage} = {malrule_answer}")

            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT - percentage is not an index!)")

        elif template == 'percentage_increase':
            percentage = problem.metadata['percentage']
            total = problem.metadata['total']

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("MALRULE: Percentage is a position or index number")
            steps.append(f"  MALRULE REASONING: '{percentage}% means the {percentage}th position'")
            steps.append(f"                     'Or just the number {percentage} itself'")
            steps.append("")
            steps.append(f"Step 1: See 'increase by {percentage}%'")
            steps.append(f"  MALRULE: Increase means add {percentage} (the percentage number)")
            steps.append(f"  {total} + {percentage} = {malrule_answer}")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT - percentage is not an index!)")

        elif template == 'percentage_decrease':
            percentage = problem.metadata['percentage']
            total = problem.metadata['total']

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("MALRULE: Percentage is a position or index number")
            steps.append(f"  MALRULE REASONING: '{percentage}% means the {percentage}th position'")
            steps.append(f"                     'Or just the number {percentage} itself'")
            steps.append("")
            steps.append(f"Step 1: See '{percentage}% off'")
            steps.append(f"  MALRULE: Off means subtract {percentage} (the percentage number)")
            steps.append(f"  {total} - {percentage} = {malrule_answer}")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT - percentage is not an index!)")

        else:  # basic_percentage
            percentage = problem.metadata['percentage']

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("MALRULE: Percentage is a position or index number")
            steps.append(f"  MALRULE REASONING: '{percentage}% means the {percentage}th position'")
            steps.append(f"                     'Or just the number {percentage} itself'")
            steps.append("")
            steps.append(f"Step 1: See '{percentage}%'")
            steps.append(f"  MALRULE: The answer is {percentage} (the percentage number)")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT - percentage is not an index!)")

        return steps

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Malrule: treat percentage as index/position number
        template = problem.metadata.get('template', 'basic_percentage')
        percentage = problem.metadata['percentage']

        if template == 'basic_percentage':
            # Student thinks "X% of Y" means just X
            return percentage
        elif template == 'percentage_increase':
            # Student thinks "increase by X%" means add X
            total = problem.metadata['total']
            return total + percentage
        elif template == 'percentage_decrease':
            # Student thinks "decrease by X%" means subtract X
            total = problem.metadata['total']
            return total - percentage
        elif template == 'word_problem_context':
            formula_type = problem.metadata.get('formula_type', 'basic_percentage')
            if formula_type == 'basic_percentage':
                return percentage
            elif formula_type == 'percentage_increase':
                total = problem.metadata['total']
                return total + percentage
            elif formula_type == 'percentage_decrease':
                total = problem.metadata['total']
                return total - percentage
            elif formula_type == 'find_total_from_percentage':
                part = problem.metadata['part']
                return part // percentage if percentage != 0 else part
        elif template == 'comparison_problem':
            # For comparison, the malrule uses percentage values directly
            # This is complex, so we compute it in _solve_comparison_problem
            percentage1 = problem.metadata['percentage']
            # Need to access operands for both percentages
            if len(problem.operands) >= 2:
                # operands are [percentage1, total1, percentage2, total2]
                total1 = problem.operands[1]
                percentage2 = problem.operands[2] if len(problem.operands) > 2 else percentage
                # Malrule: compare percentage values directly, ignoring the totals
                if percentage > percentage2:
                    return f"{percentage}% of {total1} is greater"
                elif percentage < percentage2:
                    total2 = problem.operands[3] if len(problem.operands) > 3 else total1
                    return f"{percentage2}% of {total2} is greater"
                else:
                    return "They are equal"
            return percentage

        # Fallback
        return problem.metadata.get('malrule_answer', percentage)

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        template = problem.metadata.get('template', 'basic_percentage')

        # Handle comparison_problem specially
        if template == 'comparison_problem':
            return self._solve_comparison_problem(problem, verbose)

        # For word_problem_context, use formula_type to determine malrule application
        if template == 'word_problem_context':
            formula_type = problem.metadata.get('formula_type', 'basic_percentage')
            return self._apply_malrule_word_problem(problem, formula_type, verbose)

        percentage = problem.metadata['percentage']
        total = problem.metadata['total']

        if template == 'percentage_increase':
            malrule_answer = total + percentage
        elif template == 'percentage_decrease':
            malrule_answer = total - percentage
        else:  # basic_percentage
            malrule_answer = percentage

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
        """Apply malrule to word problems based on formula type."""
        percentage = problem.metadata['percentage']

        if formula_type == 'basic_percentage':
            malrule_answer = percentage

        elif formula_type == 'percentage_increase':
            total = problem.metadata['total']
            malrule_answer = total + percentage

        elif formula_type == 'percentage_decrease':
            total = problem.metadata['total']
            malrule_answer = total - percentage

        elif formula_type == 'find_total_from_percentage':
            part = problem.metadata['part']
            malrule_answer = part // percentage if percentage != 0 else part
        else:
            raise ValueError(f"Unknown formula_type: {formula_type}")

        if verbose:
            steps = self._generate_verbose_steps(problem, malrule_answer, 'word_problem_context')
        else:
            steps = self._generate_concise_steps(problem, malrule_answer, 'word_problem_context')

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _solve_comparison_problem(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle comparison problems which compare two percentage calculations."""
        percentage1 = problem.metadata['percentage']
        total1 = problem.operands[1]
        percentage2 = problem.operands[2] if len(problem.operands) > 2 else percentage1

        # Malrule: compare percentage values directly, ignoring the totals
        if percentage1 > percentage2:
            malrule_answer = f"{percentage1}% of {total1} is greater"
        elif percentage1 < percentage2:
            total2 = problem.operands[3] if len(problem.operands) > 3 else total1
            malrule_answer = f"{percentage2}% of {total2} is greater"
        else:
            malrule_answer = "They are equal"

        if verbose:
            steps = self._generate_verbose_steps(problem, malrule_answer, 'comparison_problem')
        else:
            steps = self._generate_concise_steps(problem, malrule_answer, 'comparison_problem')

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
