"""
Correct algorithm for percentage calculations.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List, Any
from utils import CorrectAlgorithm, Problem, Solution


class PercentageCorrectAlgorithm(CorrectAlgorithm):
    """Correctly calculates percentages using proportion (X/100 × total)."""

    def get_name(self) -> str:
        return "Correct Percentage Calculation"

    def get_description(self) -> str:
        return "Correctly calculates percentages: X% of Y = (X/100) × Y"

    def _generate_concise_steps(self, problem: Problem, correct_answer: Any, template: str) -> List[str]:
        """Generate concise steps showing only formula and values."""
        steps = []

        # Add question
        steps.append(problem.text)

        if template == 'comparison_problem':
            percentage1 = problem.operands[0]
            total1 = problem.operands[1]
            percentage2 = problem.operands[2] if len(problem.operands) > 2 else percentage1
            total2 = problem.operands[3] if len(problem.operands) > 3 else total1
            correct1 = (percentage1 * total1) / 100
            correct2 = (percentage2 * total2) / 100

            steps.append(f"Formula: result = (percentage/100) × total")
            steps.append(f"{percentage1}% of {total1} = {correct1}")
            steps.append(f"{percentage2}% of {total2} = {correct2}")

        elif template == 'word_problem_context':
            formula_type = problem.metadata.get('formula_type', 'basic_percentage')
            percentage = problem.metadata['percentage']

            if formula_type == 'basic_percentage':
                total = problem.metadata['total']
                steps.append(f"Formula: result = (percentage/100) × total")
                steps.append(f"({percentage}/100) × {total} = {correct_answer}")
            elif formula_type == 'percentage_increase':
                total = problem.metadata['total']
                increase = (percentage * total) / 100
                steps.append(f"Formula: result = total + (percentage/100) × total")
                steps.append(f"increase = ({percentage}/100) × {total} = {increase}")
                steps.append(f"{total} + {increase} = {correct_answer}")
            elif formula_type == 'percentage_decrease':
                total = problem.metadata['total']
                decrease = (percentage * total) / 100
                steps.append(f"Formula: result = total - (percentage/100) × total")
                steps.append(f"decrease = ({percentage}/100) × {total} = {decrease}")
                steps.append(f"{total} - {decrease} = {correct_answer}")
            elif formula_type == 'find_total_from_percentage':
                part = problem.metadata['part']
                steps.append(f"Formula: total = part ÷ (percentage/100)")
                steps.append(f"{part} ÷ ({percentage}/100) = {correct_answer}")

        elif template == 'percentage_increase':
            percentage = problem.metadata['percentage']
            total = problem.metadata['total']
            increase = (percentage * total) / 100
            steps.append(f"Formula: result = total + (percentage/100) × total")
            steps.append(f"increase = ({percentage}/100) × {total} = {increase}")
            steps.append(f"{total} + {increase} = {correct_answer}")

        elif template == 'percentage_decrease':
            percentage = problem.metadata['percentage']
            total = problem.metadata['total']
            decrease = (percentage * total) / 100
            steps.append(f"Formula: result = total - (percentage/100) × total")
            steps.append(f"decrease = ({percentage}/100) × {total} = {decrease}")
            steps.append(f"{total} - {decrease} = {correct_answer}")

        else:  # basic_percentage
            percentage = problem.metadata['percentage']
            total = problem.metadata['total']
            steps.append(f"Formula: result = (percentage/100) × total")
            steps.append(f"({percentage}/100) × {total} = {correct_answer}")

        steps.append(f"Answer: {correct_answer}")
        return steps

    def _generate_verbose_steps(self, problem: Problem, correct_answer: Any, template: str) -> List[str]:
        """Generate verbose steps with full explanations (original format)."""
        steps = []

        if template == 'comparison_problem':
            percentage1 = problem.operands[0]
            total1 = problem.operands[1]
            percentage2 = problem.operands[2] if len(problem.operands) > 2 else percentage1
            total2 = problem.operands[3] if len(problem.operands) > 3 else total1
            correct1 = (percentage1 * total1) / 100
            correct2 = (percentage2 * total2) / 100

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("Correct approach: Calculate each percentage properly")
            steps.append(f"  {percentage1}% of {total1} = {correct1}")
            steps.append(f"  {percentage2}% of {total2} = {correct2}")
            steps.append(f"Result: {correct_answer}")

        elif template == 'word_problem_context':
            formula_type = problem.metadata.get('formula_type', 'basic_percentage')
            percentage = problem.metadata['percentage']

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("Method: Percentage means 'per hundred' (out of 100)")
            steps.append("")

            if formula_type == 'basic_percentage':
                total = problem.metadata['total']
                steps.append(f"Step 1: Convert {percentage}% to decimal: {percentage}/100 = {percentage/100}")
                steps.append(f"Step 2: Multiply by total: {percentage/100} × {total} = {correct_answer}")
            elif formula_type == 'percentage_increase':
                total = problem.metadata['total']
                increase = (percentage * total) / 100
                steps.append(f"Step 1: Calculate increase: {percentage}% of {total} = {increase}")
                steps.append(f"Step 2: Add to original: {total} + {increase} = {correct_answer}")
            elif formula_type == 'percentage_decrease':
                total = problem.metadata['total']
                decrease = (percentage * total) / 100
                steps.append(f"Step 1: Calculate decrease: {percentage}% of {total} = {decrease}")
                steps.append(f"Step 2: Subtract from original: {total} - {decrease} = {correct_answer}")
            elif formula_type == 'find_total_from_percentage':
                part = problem.metadata['part']
                steps.append(f"Step 1: Set up equation: {part} = {percentage}% of total")
                steps.append(f"Step 2: Solve: total = {part} ÷ ({percentage}/100) = {correct_answer}")

            steps.append("")
            steps.append(f"Final Answer: {correct_answer} ✓")

        elif template == 'percentage_increase':
            percentage = problem.metadata['percentage']
            total = problem.metadata['total']
            increase = (percentage * total) / 100

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("Method: Percentage means 'per hundred' (out of 100)")
            steps.append("")
            steps.append(f"Step 1: Calculate the increase")
            steps.append(f"  Increase = {percentage}% of {total}")
            steps.append(f"  = ({percentage}/100) × {total} = {increase}")
            steps.append("")
            steps.append(f"Step 2: Add to original value")
            steps.append(f"  New value = {total} + {increase} = {correct_answer}")
            steps.append("")
            steps.append(f"Final Answer: {correct_answer} ✓")

        elif template == 'percentage_decrease':
            percentage = problem.metadata['percentage']
            total = problem.metadata['total']
            decrease = (percentage * total) / 100

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("Method: Percentage means 'per hundred' (out of 100)")
            steps.append("")
            steps.append(f"Step 1: Calculate the discount")
            steps.append(f"  Discount = {percentage}% of {total}")
            steps.append(f"  = ({percentage}/100) × {total} = {decrease}")
            steps.append("")
            steps.append(f"Step 2: Subtract from original price")
            steps.append(f"  Sale price = {total} - {decrease} = {correct_answer}")
            steps.append("")
            steps.append(f"Final Answer: {correct_answer} ✓")

        else:  # basic_percentage
            percentage = problem.metadata['percentage']
            total = problem.metadata['total']

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("Method: Percentage means 'per hundred' (out of 100)")
            steps.append("")
            steps.append(f"Step 1: Convert percentage to decimal")
            steps.append(f"  {percentage}% = {percentage}/100 = {percentage/100}")
            steps.append("")
            steps.append(f"Step 2: Multiply by total ('of' means multiply)")
            steps.append(f"  {percentage/100} × {total} = {correct_answer}")
            steps.append("")
            steps.append(f"Final Answer: {correct_answer} ✓")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        template = problem.metadata.get('template', 'basic_percentage')

        # Handle comparison_problem specially
        if template == 'comparison_problem':
            return self._solve_comparison_problem(problem, verbose)

        # For word_problem_context, use formula_type to determine solving approach
        if template == 'word_problem_context':
            formula_type = problem.metadata.get('formula_type', 'basic_percentage')
            return self._solve_word_problem(problem, formula_type, verbose)

        percentage = problem.metadata['percentage']
        total = problem.metadata['total']

        if template == 'percentage_increase':
            increase = (percentage * total) / 100
            correct_answer = total + increase
        elif template == 'percentage_decrease':
            decrease = (percentage * total) / 100
            correct_answer = total - decrease
        else:  # basic_percentage
            correct_answer = (percentage * total) / 100

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
        """Solve word problems based on formula type."""
        percentage = problem.metadata['percentage']

        if formula_type == 'basic_percentage':
            total = problem.metadata['total']
            correct_answer = (percentage * total) / 100

        elif formula_type == 'percentage_increase':
            total = problem.metadata['total']
            increase = (percentage * total) / 100
            correct_answer = total + increase

        elif formula_type == 'percentage_decrease':
            total = problem.metadata['total']
            decrease = (percentage * total) / 100
            correct_answer = total - decrease

        elif formula_type == 'find_total_from_percentage':
            part = problem.metadata['part']
            correct_answer = (part * 100) // percentage if percentage != 0 else part
        else:
            raise ValueError(f"Unknown formula_type: {formula_type}")

        if verbose:
            steps = self._generate_verbose_steps(problem, correct_answer, 'word_problem_context')
        else:
            steps = self._generate_concise_steps(problem, correct_answer, 'word_problem_context')

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _solve_comparison_problem(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle comparison problems which compare two percentage calculations."""
        percentage1 = problem.operands[0]
        total1 = problem.operands[1]
        percentage2 = problem.operands[2] if len(problem.operands) > 2 else percentage1
        total2 = problem.operands[3] if len(problem.operands) > 3 else total1

        # Calculate the actual values
        correct1 = (percentage1 * total1) / 100
        correct2 = (percentage2 * total2) / 100

        # Determine comparison
        if correct1 > correct2:
            correct_answer = f"{percentage1}% of {total1} is greater"
        elif correct1 < correct2:
            correct_answer = f"{percentage2}% of {total2} is greater"
        else:
            correct_answer = "They are equal"

        if verbose:
            steps = self._generate_verbose_steps(problem, correct_answer, 'comparison_problem')
        else:
            steps = self._generate_concise_steps(problem, correct_answer, 'comparison_problem')

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
