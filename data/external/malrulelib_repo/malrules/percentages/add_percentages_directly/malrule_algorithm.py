"""
Malrule algorithm for Add-Percentages-Directly error.

Students incorrectly add or subtract percentages directly without
considering that they apply to different base values.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class AddPercentagesDirectlyMalrule(Malrule):
    """
    Implements the Add-Percentages-Directly malrule.

    Students incorrectly combine percentages by adding or subtracting
    them directly, thinking "+20% then -20% cancels out" or
    "+20% then +30% = +50%".

    Example: $100 increased by 20% then decreased by 20%
    Correct: $100 × 1.20 × 0.80 = $96
    Malrule: +20% - 20% = 0%, so still $100 (WRONG!)
    """

    def get_name(self) -> str:
        return "Additive Reasoning with Percentages"

    def get_description(self) -> str:
        return (
            "Students incorrectly apply additive reasoning to percentage problems that "
            "require multiplicative thinking. They add or subtract percentages directly "
            "without recognizing that each percentage applies to a different base value. "
            "This reflects a fundamental gap in the transition from additive to multiplicative "
            "reasoning, which is one of the major barriers to mathematical development "
            "(Van Dooren, De Bock, & Verschaffel, 2010)."
        )

    def _generate_concise_steps(self, problem: Problem, result: float, net_percentage: float) -> List[str]:
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

            steps.append(f"Formula: +{pct1}% - {pct2}% + {pct3}% = {net_percentage:+}%")
            if net_percentage == 0:
                steps.append(f"{initial} (unchanged)")
            else:
                steps.append(f"{initial} × (1 + {net_percentage}/100) = {result}")

        elif problem_type == 'reverse_percentage':
            final_value = problem.metadata['final_value']
            pct1 = problem.metadata['percentage1']

            steps.append(f"Formula: original = final × (1 - percentage/100)")
            steps.append(f"original = {final_value} × {1 - pct1/100} = {result}")

        else:
            initial = problem.metadata['initial_value']
            pct1 = problem.metadata['percentage1']
            pct2 = problem.metadata['percentage2']

            if problem_type in ['increase_then_decrease', 'word_problem_context']:
                steps.append(f"Formula: +{pct1}% - {pct2}% = {net_percentage}%")
            elif problem_type == 'decrease_then_increase':
                steps.append(f"Formula: -{pct1}% + {pct2}% = {net_percentage}%")
            elif problem_type == 'two_increases':
                steps.append(f"Formula: +{pct1}% + {pct2}% = +{net_percentage}%")
            else:  # two_decreases
                steps.append(f"Formula: -{pct1}% - {pct2}% = -{net_percentage}%")

            if net_percentage == 0:
                steps.append(f"{initial} (unchanged)")
            else:
                steps.append(f"{initial} × (1 + {net_percentage}/100) = {result}")

        steps.append(f"Answer: {result}")
        return steps

    def _generate_verbose_steps(self, problem: Problem, result: float, net_percentage: float) -> List[str]:
        """Generate verbose steps with full explanations (original format)."""
        steps = []
        problem_type = problem.metadata['problem_type']

        if problem_type == 'three_sequential_changes':
            initial = problem.metadata['initial_value']
            pct1 = problem.metadata['percentage1']
            pct2 = problem.metadata['percentage2']
            pct3 = problem.metadata['percentage3']

            steps.append(f"Initial value: ${initial}")
            steps.append("")
            steps.append(f"MALRULE: Add all three percentages directly")
            steps.append(f"  +{pct1}% then -{pct2}% then +{pct3}%")
            steps.append(f"  Combined: +{pct1}% - {pct2}% + {pct3}% = {net_percentage:+}%")
            steps.append(f"MALRULE REASONING: Percentages add like regular numbers")

            if net_percentage > 0:
                steps.append(f"  Net increase of {net_percentage}%")
            elif net_percentage < 0:
                steps.append(f"  Net decrease of {-net_percentage}%")
            else:
                steps.append(f"  All changes cancel out, back to original")

            steps.append("")
            steps.append(f"Final value: ${result} (INCORRECT)")

        elif problem_type == 'reverse_percentage':
            final_value = problem.metadata['final_value']
            pct1 = problem.metadata['percentage1']

            steps.append(f"Final value: ${final_value}")
            steps.append(f"Percentage increase: {pct1}%")
            steps.append("")
            steps.append(f"MALRULE: Just subtract the percentage")
            steps.append(f"  If increased by {pct1}%, subtract {pct1}% to get original")
            steps.append(f"MALRULE REASONING: Addition and subtraction are opposites")
            steps.append(f"  Original = ${final_value} × (1 - {pct1}/100)")
            steps.append(f"  Original = ${final_value} × {1 - pct1/100}")
            steps.append(f"  Original = ${result}")
            steps.append("")
            steps.append(f"Final answer: ${result} (INCORRECT)")

        else:
            initial = problem.metadata['initial_value']
            pct1 = problem.metadata['percentage1']
            pct2 = problem.metadata['percentage2']

            steps.append(f"Initial value: ${initial}" if 'item' in problem.text.lower() or '$' in problem.text
                        else f"Initial value: {initial}")
            steps.append("")

            if problem_type in ['increase_then_decrease', 'word_problem_context']:
                steps.append(f"MALRULE: Add the percentages directly")
                steps.append(f"  +{pct1}% then -{pct2}%")
                steps.append(f"  Combined: +{pct1}% - {pct2}% = {pct1 - pct2}%")
                steps.append(f"MALRULE REASONING: Percentages add and subtract like regular numbers")

                if net_percentage == 0:
                    steps.append(f"  Since +{pct1}% and -{pct2}% cancel out, back to original value")
                elif net_percentage > 0:
                    steps.append(f"  Net increase of {net_percentage}%")
                else:
                    steps.append(f"  Net decrease of {-net_percentage}%")

            elif problem_type == 'decrease_then_increase':
                steps.append(f"MALRULE: Add the percentages directly")
                steps.append(f"  -{pct1}% then +{pct2}%")
                steps.append(f"  Combined: -{pct1}% + {pct2}% = {pct2 - pct1}%")
                steps.append(f"MALRULE REASONING: Percentages add and subtract like regular numbers")

                if net_percentage == 0:
                    steps.append(f"  Since -{pct1}% and +{pct2}% cancel out, back to original value")
                elif net_percentage > 0:
                    steps.append(f"  Net increase of {net_percentage}%")
                else:
                    steps.append(f"  Net decrease of {-net_percentage}%")

            elif problem_type == 'two_increases':
                steps.append(f"MALRULE: Add the percentages directly")
                steps.append(f"  +{pct1}% then +{pct2}%")
                steps.append(f"  Combined: +{pct1}% + {pct2}% = +{pct1 + pct2}%")
                steps.append(f"MALRULE REASONING: Two increases add together")
                steps.append(f"  Total increase of {net_percentage}%")

            else:  # two_decreases, percentage_of_percentage
                steps.append(f"MALRULE: Add the percentages directly")
                steps.append(f"  -{pct1}% then -{pct2}%")
                steps.append(f"  Combined: -{pct1}% - {pct2}% = -{pct1 + pct2}%")
                steps.append(f"MALRULE REASONING: Two decreases add together")
                steps.append(f"  Total decrease of {net_percentage}%")

            steps.append("")
            steps.append(f"Final value: {result} (INCORRECT)")

        return steps

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Malrule: add percentages directly instead of applying sequentially
        problem_type = problem.metadata['problem_type']

        # Handle special problem types
        if problem_type == 'three_sequential_changes':
            initial = problem.metadata['initial_value']
            pct1 = problem.metadata['percentage1']
            pct2 = problem.metadata['percentage2']
            pct3 = problem.metadata['percentage3']
            net_percentage = pct1 - pct2 + pct3
            if net_percentage == 0:
                return initial
            else:
                return initial * (1 + net_percentage/100)

        elif problem_type == 'reverse_percentage':
            final_value = problem.metadata['final_value']
            pct1 = problem.metadata['percentage1']
            return final_value * (1 - pct1/100)

        # Handle regular two-percentage problems
        initial = problem.metadata['initial_value']
        pct1 = problem.metadata['percentage1']
        pct2 = problem.metadata['percentage2']

        if problem_type in ['increase_then_decrease', 'word_problem_context']:
            net_percentage = pct1 - pct2
            if net_percentage == 0:
                return initial
            else:
                return initial * (1 + net_percentage/100)

        elif problem_type == 'decrease_then_increase':
            net_percentage = pct2 - pct1
            if net_percentage == 0:
                return initial
            else:
                return initial * (1 + net_percentage/100)

        elif problem_type == 'two_increases':
            net_percentage = pct1 + pct2
            return initial * (1 + net_percentage/100)

        else:  # two_decreases, percentage_of_percentage
            net_percentage = pct1 + pct2
            return initial * (1 - net_percentage/100)

    def _handle_three_sequential_changes(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle three sequential changes with malrule."""
        initial = problem.metadata['initial_value']
        pct1 = problem.metadata['percentage1']
        pct2 = problem.metadata['percentage2']
        pct3 = problem.metadata['percentage3']

        net_percentage = pct1 - pct2 + pct3
        if net_percentage == 0:
            result = initial
        else:
            result = initial * (1 + net_percentage/100)

        if verbose:
            steps = self._generate_verbose_steps(problem, result, net_percentage)
        else:
            steps = self._generate_concise_steps(problem, result, net_percentage)

        return Solution(
            answer=result,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _handle_reverse_percentage(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle reverse percentage with malrule."""
        final_value = problem.metadata['final_value']
        pct1 = problem.metadata['percentage1']

        # Incorrectly subtract percentage directly
        malrule_original = final_value * (1 - pct1/100)

        if verbose:
            steps = self._generate_verbose_steps(problem, malrule_original, pct1)
        else:
            steps = self._generate_concise_steps(problem, malrule_original, pct1)

        return Solution(
            answer=malrule_original,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the add-percentages-directly malrule.

        Students incorrectly combine percentages arithmetically.

        Args:
            problem: Problem instance with initial value and percentages
            verbose: If True, generate verbose explanatory steps; if False, generate concise steps

        Returns:
            Solution with incorrect answer and student's reasoning
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

        # MALRULE: Add or subtract the percentages directly
        if problem_type in ['increase_then_decrease', 'word_problem_context']:
            net_percentage = pct1 - pct2
            if net_percentage == 0:
                result = initial
            else:
                result = initial * (1 + net_percentage/100)

        elif problem_type == 'decrease_then_increase':
            net_percentage = pct2 - pct1
            if net_percentage == 0:
                result = initial
            else:
                result = initial * (1 + net_percentage/100)

        elif problem_type == 'two_increases':
            net_percentage = pct1 + pct2
            result = initial * (1 + net_percentage/100)

        else:  # two_decreases, percentage_of_percentage
            net_percentage = pct1 + pct2
            result = initial * (1 - net_percentage/100)

        if verbose:
            steps = self._generate_verbose_steps(problem, result, net_percentage)
        else:
            steps = self._generate_concise_steps(problem, result, net_percentage)

        return Solution(
            answer=result,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
