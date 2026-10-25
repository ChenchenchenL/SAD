"""
Correct algorithm for sequential percentage changes.

Implements the proper method of applying percentage changes sequentially,
where each percentage applies to the result of the previous change.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class PercentageCorrectAlgorithm(CorrectAlgorithm):
    """
    Implements correct sequential percentage change calculations.

    Properly applies each percentage change to the current value,
    not to the original value, recognizing that base values change.
    """

    def get_name(self) -> str:
        return "Sequential Percentage Application"

    def get_description(self) -> str:
        return (
            "Correct algorithm that applies percentage changes sequentially, "
            "with each change applied to the result of the previous change."
        )

    def _generate_concise_steps(self, problem: Problem, answer: float, intermediate_values: dict) -> List[str]:
        """Generate concise steps showing only formula and values."""
        steps = []
        problem_type = problem.metadata['problem_type']

        # Add question
        steps.append(problem.text)

        if problem_type == 'three_sequential_changes':
            initial = problem.metadata['initial_value']
            pct1 = problem.metadata['percentage1']
            pct2 = problem.metadata['percentage2']
            pct3 = problem.metadata['percentage3']
            after_first = intermediate_values['after_first']
            after_second = intermediate_values['after_second']

            steps.append(f"Formula: value × (1 + {pct1}/100) × (1 - {pct2}/100) × (1 + {pct3}/100)")
            steps.append(f"{initial} × {1 + pct1/100} = {after_first}")
            steps.append(f"{after_first} × {1 - pct2/100} = {after_second}")
            steps.append(f"{after_second} × {1 + pct3/100} = {answer}")

        elif problem_type == 'reverse_percentage':
            final_value = problem.metadata['final_value']
            pct1 = problem.metadata['percentage1']

            steps.append(f"Formula: original = final ÷ (1 + percentage/100)")
            steps.append(f"original = {final_value} ÷ {1 + pct1/100}")
            steps.append(f"original = {answer:.2f}")

        else:
            initial = problem.metadata['initial_value']
            pct1 = problem.metadata['percentage1']
            pct2 = problem.metadata['percentage2']
            after_first = intermediate_values['after_first']

            if problem_type in ['increase_then_decrease', 'word_problem_context']:
                steps.append(f"Formula: value × (1 + {pct1}/100) × (1 - {pct2}/100)")
                steps.append(f"{initial} × {1 + pct1/100} = {after_first}")
                steps.append(f"{after_first} × {1 - pct2/100} = {answer}")
            elif problem_type == 'decrease_then_increase':
                steps.append(f"Formula: value × (1 - {pct1}/100) × (1 + {pct2}/100)")
                steps.append(f"{initial} × {1 - pct1/100} = {after_first}")
                steps.append(f"{after_first} × {1 + pct2/100} = {answer}")
            elif problem_type == 'two_increases':
                steps.append(f"Formula: value × (1 + {pct1}/100) × (1 + {pct2}/100)")
                steps.append(f"{initial} × {1 + pct1/100} = {after_first}")
                steps.append(f"{after_first} × {1 + pct2/100} = {answer}")
            else:  # two_decreases, percentage_of_percentage
                steps.append(f"Formula: value × (1 - {pct1}/100) × (1 - {pct2}/100)")
                steps.append(f"{initial} × {1 - pct1/100} = {after_first}")
                steps.append(f"{after_first} × {1 - pct2/100} = {answer}")

        steps.append(f"Answer: {answer}")
        return steps

    def _generate_verbose_steps(self, problem: Problem, answer: float, intermediate_values: dict) -> List[str]:
        """Generate verbose steps with full explanations (original format)."""
        steps = []
        problem_type = problem.metadata['problem_type']

        if problem_type == 'three_sequential_changes':
            initial = problem.metadata['initial_value']
            pct1 = problem.metadata['percentage1']
            pct2 = problem.metadata['percentage2']
            pct3 = problem.metadata['percentage3']
            after_first = intermediate_values['after_first']
            after_second = intermediate_values['after_second']

            steps.append(f"Initial value: ${initial}")
            steps.append("")
            steps.append(f"Step 1: Apply first change (+{pct1}%)")
            steps.append(f"  Multiply by (1 + {pct1}/100) = {1 + pct1/100}")
            steps.append(f"  ${initial} × {1 + pct1/100} = ${after_first}")
            steps.append(f"After first change: ${after_first}")
            steps.append("")
            steps.append(f"Step 2: Apply second change (-{pct2}%) to NEW value ${after_first}")
            steps.append(f"  Multiply by (1 - {pct2}/100) = {1 - pct2/100}")
            steps.append(f"  ${after_first} × {1 - pct2/100} = ${after_second}")
            steps.append(f"After second change: ${after_second}")
            steps.append("")
            steps.append(f"Step 3: Apply third change (+{pct3}%) to NEW value ${after_second}")
            steps.append(f"  Multiply by (1 + {pct3}/100) = {1 + pct3/100}")
            steps.append(f"  ${after_second} × {1 + pct3/100} = ${answer}")
            steps.append("")
            steps.append(f"Final value: ${answer}")

        elif problem_type == 'reverse_percentage':
            final_value = problem.metadata['final_value']
            pct1 = problem.metadata['percentage1']

            steps.append(f"Final value: ${final_value}")
            steps.append(f"Percentage increase: {pct1}%")
            steps.append("")
            steps.append(f"We know: Original × (1 + {pct1}/100) = ${final_value}")
            steps.append(f"So: Original × {1 + pct1/100} = ${final_value}")
            steps.append(f"Therefore: Original = ${final_value} ÷ {1 + pct1/100}")
            steps.append(f"Original = ${answer:.2f}")
            steps.append("")
            steps.append(f"Check: ${answer:.2f} × {1 + pct1/100} = ${final_value}")

        else:
            initial = problem.metadata['initial_value']
            pct1 = problem.metadata['percentage1']
            pct2 = problem.metadata['percentage2']
            after_first = intermediate_values['after_first']

            steps.append(f"Initial value: ${initial}" if 'item' in problem.text.lower() or '$' in problem.text
                        else f"Initial value: {initial}")
            steps.append("")

            if problem_type in ['increase_then_decrease', 'two_increases', 'word_problem_context']:
                steps.append(f"Step 1: Apply first change (+{pct1}%)")
                steps.append(f"  Multiply by (1 + {pct1}/100) = {1 + pct1/100}")
                steps.append(f"  {initial} × {1 + pct1/100} = {after_first}")
            else:
                steps.append(f"Step 1: Apply first change (-{pct1}%)")
                steps.append(f"  Multiply by (1 - {pct1}/100) = {1 - pct1/100}")
                steps.append(f"  {initial} × {1 - pct1/100} = {after_first}")

            steps.append("")
            steps.append(f"After first change: {after_first}")
            steps.append("")

            if problem_type in ['increase_then_decrease', 'decrease_then_increase']:
                if 'increase_then_decrease' in problem_type:
                    steps.append(f"Step 2: Apply second change (-{pct2}%) to NEW value")
                    steps.append(f"  IMPORTANT: Apply to {after_first}, not original {initial}")
                    steps.append(f"  Multiply by (1 - {pct2}/100) = {1 - pct2/100}")
                    steps.append(f"  {after_first} × {1 - pct2/100} = {answer}")
                else:
                    steps.append(f"Step 2: Apply second change (+{pct2}%) to NEW value")
                    steps.append(f"  IMPORTANT: Apply to {after_first}, not original {initial}")
                    steps.append(f"  Multiply by (1 + {pct2}/100) = {1 + pct2/100}")
                    steps.append(f"  {after_first} × {1 + pct2/100} = {answer}")
            elif problem_type in ['two_increases']:
                steps.append(f"Step 2: Apply second change (+{pct2}%) to NEW value")
                steps.append(f"  IMPORTANT: Apply to {after_first}, not original {initial}")
                steps.append(f"  Multiply by (1 + {pct2}/100) = {1 + pct2/100}")
                steps.append(f"  {after_first} × {1 + pct2/100} = {answer}")
            else:
                steps.append(f"Step 2: Apply second change (-{pct2}%) to NEW value")
                steps.append(f"  IMPORTANT: Apply to {after_first}, not original {initial}")
                steps.append(f"  Multiply by (1 - {pct2}/100) = {1 - pct2/100}")
                steps.append(f"  {after_first} × {1 - pct2/100} = {answer}")

            steps.append("")
            steps.append(f"Final value: {answer}")
            steps.append("")
            steps.append("Why percentages don't simply add or cancel:")
            steps.append(f"  Each percentage applies to a DIFFERENT base value")
            if problem_type == 'increase_then_decrease':
                steps.append(f"  First {pct1}% of ${initial} = ${initial * pct1/100}")
                steps.append(f"  Second {pct2}% of ${after_first} = ${after_first * pct2/100}")
                steps.append(f"  These are different amounts!")

        return steps

    def _handle_three_sequential_changes(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle three sequential percentage changes."""
        initial = problem.metadata['initial_value']
        pct1 = problem.metadata['percentage1']
        pct2 = problem.metadata['percentage2']
        pct3 = problem.metadata['percentage3']

        # Calculate values
        after_first = initial * (1 + pct1/100)
        after_second = after_first * (1 - pct2/100)
        final = after_second * (1 + pct3/100)

        intermediate_values = {
            'after_first': after_first,
            'after_second': after_second
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, final, intermediate_values)
        else:
            steps = self._generate_concise_steps(problem, final, intermediate_values)

        return Solution(
            answer=final,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _handle_reverse_percentage(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle reverse percentage problem (find original given final)."""
        final_value = problem.metadata['final_value']
        pct1 = problem.metadata['percentage1']
        # COMPUTE the correct answer independently
        correct_original = final_value / (1 + pct1/100)

        intermediate_values = {}

        if verbose:
            steps = self._generate_verbose_steps(problem, round(correct_original, 2), intermediate_values)
        else:
            steps = self._generate_concise_steps(problem, round(correct_original, 2), intermediate_values)

        return Solution(
            answer=round(correct_original, 2),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply sequential percentage changes correctly.

        Args:
            problem: Problem instance with initial value and percentages
            verbose: If True, generate verbose explanatory steps; if False, generate concise steps

        Returns:
            Solution with correct answer and detailed steps
        """
        problem_type = problem.metadata['problem_type']

        # Handle special problem types
        if problem_type == 'three_sequential_changes':
            return self._handle_three_sequential_changes(problem, verbose)
        elif problem_type == 'reverse_percentage':
            return self._handle_reverse_percentage(problem, verbose)

        initial = problem.metadata['initial_value']
        pct1 = problem.metadata['percentage1']
        pct2 = problem.metadata['percentage2']

        # Calculate values first
        if problem_type in ['increase_then_decrease', 'two_increases', 'word_problem_context']:
            after_first = initial * (1 + pct1/100)
        else:
            after_first = initial * (1 - pct1/100)

        if problem_type in ['increase_then_decrease']:
            final = after_first * (1 - pct2/100)
        elif problem_type in ['decrease_then_increase']:
            final = after_first * (1 + pct2/100)
        elif problem_type in ['two_increases']:
            final = after_first * (1 + pct2/100)
        else:  # two_decreases, percentage_of_percentage
            final = after_first * (1 - pct2/100)

        intermediate_values = {'after_first': after_first}

        if verbose:
            steps = self._generate_verbose_steps(problem, final, intermediate_values)
        else:
            steps = self._generate_concise_steps(problem, final, intermediate_values)

        return Solution(
            answer=final,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
