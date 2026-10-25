"""
Correct mode calculation algorithm.

Correctly identifies the mode (most frequent value) or recognizes when
no mode exists (all values appear with equal frequency).
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import CorrectAlgorithm, Problem, Solution
from typing import List
from collections import Counter


def generate_concise_steps(problem_text, data, counts, max_count, modes, result, is_word_problem=False, context=None):
    """
    Generate concise steps for mode calculation.

    Returns a list: [Question, formula extraction step (if word problem), calculation steps, answer]
    """
    steps = []

    # Question
    steps.append(problem_text)

    # Formula extraction step for word problems
    if is_word_problem:
        steps.append(f"Data ({context}): {data}")

    # Frequency count (condensed)
    freq_str = ", ".join([f"{v}:{c}" for v, c in sorted(counts.items())])
    steps.append(f"Frequencies: {freq_str}")

    # Max frequency
    steps.append(f"Max frequency: {max_count}")

    # Answer
    steps.append(result)

    return steps


def generate_verbose_steps(problem_text, data, counts, max_count, modes, result, is_word_problem=False, context=None):
    """
    Generate verbose steps for mode calculation.

    Returns detailed steps with explanations (original behavior).
    """
    steps = []

    # For word problems, include the context
    if is_word_problem:
        steps.append(f"Problem: {problem_text}")
        steps.append(f"")
        steps.append(f"Step 1: Extract the data from the problem")
        steps.append(f"  Data ({context}): {data}")
        steps.append(f"")
        steps.append(f"Step 2: Find the mode (most frequent value)")
    else:
        steps.append(f"Analyzing data: {data}")
        steps.append(f"Finding the mode (most frequent value)...")

    # Count frequency of each value
    steps.append(f"Frequency count:")
    for value, count in sorted(counts.items()):
        steps.append(f"  Value {value} appears {count} time(s)")

    # Find maximum frequency
    steps.append(f"Maximum frequency: {max_count}")

    # Determine result based on how many values have max frequency
    if max_count == 1:
        steps.append(f"All values appear equally (once each)")
        steps.append(f"When no value appears more frequently than others, no mode exists")
        steps.append(f"ANSWER: {result}")
    elif len(modes) == 1:
        steps.append(f"Value {modes[0]} appears most frequently ({max_count} times)")
        steps.append(f"ANSWER: The mode is {result}")
    elif len(modes) == 2:
        steps.append(f"Two values tied for most frequent ({max_count} times each): {sorted(modes)}")
        steps.append(f"This data set is bimodal")
        steps.append(f"ANSWER: The modes are {result}")
    elif len(modes) == len(data):
        steps.append(f"All values appear with equal frequency ({max_count} times each)")
        steps.append(f"When all values appear equally, no mode exists")
        steps.append(f"ANSWER: {result}")
    else:
        steps.append(f"Multiple values tied for most frequent ({max_count} times each): {sorted(modes)}")
        steps.append(f"This data set is multimodal")
        steps.append(f"ANSWER: The modes are {result}")

    steps.append(f"Final answer: {result}")

    return steps


class ModeMustExistCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for mode calculation.

    Correctly identifies:
    1. Single mode (one value appears most frequently)
    2. Multiple modes / bimodal (two or more values tied for most frequent)
    3. No mode (all values appear with equal frequency)
    """

    def get_name(self) -> str:
        return "Correct Mode Calculation"

    def get_description(self) -> str:
        return (
            "Correctly calculates the mode by finding the most frequent value(s). "
            "Recognizes when no mode exists (all values appear equally) and reports "
            "'No mode' rather than forcing an incorrect answer."
        )

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct mode calculation.

        Args:
            problem: Mode calculation problem
            verbose: If True, generate verbose steps; if False (default), generate concise steps

        Returns:
            Solution with correct mode or "No mode"
        """
        template = problem.metadata.get('template', '')

        # Handle comparison problem specially
        if template == 'comparison_problem':
            return self._solve_comparison_problem(problem, verbose)

        data = problem.metadata.get('data', problem.operands)
        if not isinstance(data, list):
            data = problem.operands if isinstance(problem.operands, list) else [problem.operands]

        # Count frequency of each value
        counts = Counter(data)
        max_count = max(counts.values())
        modes = [value for value, count in counts.items() if count == max_count]

        # Determine result based on how many values have max frequency
        if max_count == 1:
            result = "No mode"
        elif len(modes) == 1:
            result = f"{modes[0]}"
        elif len(modes) == 2:
            result = f"{sorted(modes)}"
        elif len(modes) == len(data):
            result = "No mode"
        else:
            result = f"{sorted(modes)}"

        # Get problem context
        is_word_problem = problem.metadata.get('is_word_problem', False)
        context = problem.metadata.get('context', 'data')

        # Generate steps based on verbose setting
        if verbose:
            steps = generate_verbose_steps(
                problem_text=problem.text,
                data=data,
                counts=counts,
                max_count=max_count,
                modes=modes,
                result=result,
                is_word_problem=is_word_problem,
                context=context
            )
        else:
            steps = generate_concise_steps(
                problem_text=problem.text,
                data=data,
                counts=counts,
                max_count=max_count,
                modes=modes,
                result=result,
                is_word_problem=is_word_problem,
                context=context
            )

        return Solution(
            answer=result,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _solve_comparison_problem(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle comparison problems which compare two datasets."""
        correct_answer = problem.metadata.get('correct_answer', '')
        data_a = problem.metadata.get('data_a', [])
        data_b = problem.metadata.get('data_b', [])
        mode_a = problem.metadata.get('mode_a', None)

        # Analyze both datasets
        counts_a = Counter(data_a)
        max_count_a = max(counts_a.values())
        counts_b = Counter(data_b)
        max_count_b = max(counts_b.values())

        if verbose:
            steps = []
            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("Correct approach: Analyze each dataset for modes")
            steps.append("")

            # Analyze Dataset A
            steps.append(f"Dataset A: {data_a}")
            if max_count_a > 1:
                steps.append(f"  Value {mode_a} appears {max_count_a} times (most frequent)")
                steps.append(f"  Dataset A has a mode: {mode_a}")
            else:
                steps.append(f"  All values appear once")
                steps.append(f"  Dataset A has no mode")
            steps.append("")

            # Analyze Dataset B
            steps.append(f"Dataset B: {data_b}")
            if max_count_b == 1:
                steps.append(f"  All values appear once")
                steps.append(f"  Dataset B has no mode")
            else:
                modes_b = [value for value, count in counts_b.items() if count == max_count_b]
                if len(modes_b) == 1:
                    steps.append(f"  Value {modes_b[0]} appears {max_count_b} times")
                    steps.append(f"  Dataset B has a mode: {modes_b[0]}")
            steps.append("")

            steps.append(f"CONCLUSION: {correct_answer}")
            steps.append("")
            steps.append("✓ Correctly recognized that Dataset B has no mode")
            steps.append("✓ Mode exists only when a value appears more frequently than others")
        else:
            # Concise steps
            steps = []
            steps.append(problem.text)
            mode_a_str = f"Mode: {mode_a}" if max_count_a > 1 else "No mode"
            mode_b_str = "No mode" if max_count_b == 1 else f"Mode: {[v for v, c in counts_b.items() if c == max_count_b][0]}"
            steps.append(f"Dataset A: {mode_a_str}")
            steps.append(f"Dataset B: {mode_b_str}")
            steps.append(correct_answer)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
