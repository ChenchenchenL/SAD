"""
Mode-Must-Exist malrule algorithm.

Implements the systematic error where students believe every data set must
have a mode. When no value repeats, they incorrectly pick the largest value,
smallest value, or middle value as the "mode".
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List
import random

def generate_concise_steps(problem_text, data, counts, max_count, result, is_word_problem=False, context=None):
    """
    Generate concise steps for the malrule algorithm.

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

    # Answer
    steps.append(result)

    return steps

def generate_verbose_steps(problem_text, data, counts, max_count, result, is_word_problem=False, context=None):
    """
    Generate verbose steps for the malrule algorithm.

    Returns detailed steps with explanations (original behavior).
    """
    from collections import Counter

    steps = []

    # For word problems, include the context
    if is_word_problem:
        steps.append(f"Problem: {problem_text}")
        steps.append(f"")
        steps.append(f"MALRULE APPROACH: Force a mode to exist (pick largest/middle/smallest)")
        steps.append(f"Data extracted ({context}): {data}")
        steps.append(f"")
    else:
        steps.append(f"Analyzing data: {data}")
        steps.append(f"Looking for the mode (most frequent value)...")

    if max_count == 1:
        # All values appear once - no mode exists, but malrule student forces an answer
        steps.append(f"MALRULE THINKING: All values appear once")
        steps.append(f"MALRULE ERROR: 'Every dataset must have a mode, so I'll pick one'")
        steps.append(f"MALRULE STRATEGY: Pick the largest value")
        steps.append(f"Largest value: {max(data)}")
        steps.append(f"MALRULE ANSWER: The mode is {result}")
        steps.append(f"ERROR: Mode is about FREQUENCY, not magnitude!")
        steps.append(f"CORRECT: All values appear once, so NO MODE EXISTS")
    else:
        # There is an actual mode
        modes = [value for value, count in counts.items() if count == max_count]
        if len(modes) == 1:
            steps.append(f"Value {modes[0]} appears {max_count} times (most frequent)")
            steps.append(f"The mode is {result}")
        else:
            steps.append(f"Multiple values appear {max_count} times (most frequent)")
            steps.append(f"The modes are {result}")

    return steps

class ModeMustExistMalrule(Malrule):
    """
    Implements the Mode-Must-Exist bug.

    Students believe every data set must have a mode. When all values are
    unique (no repeats), they don't recognize "no mode" as a valid answer.
    Instead, they force an answer by picking:
    1. The largest value ("biggest must be the mode")
    2. The smallest value ("smallest must be the mode")
    3. The middle value ("middle value must be the mode")

    Example: {3, 7, 2, 9, 5}
    Correct: No mode (all values appear once)
    Malrule: 9 (picks largest), or 2 (picks smallest), or 5 (picks middle)
    """

    def get_name(self) -> str:
        return "Mode-Must-Exist"

    def get_description(self) -> str:
        return (
            "Students believe every data set must have a mode and struggle to distinguish "
            "between mode and frequency. When no value repeats (all values are unique), "
            "they don't recognize 'no mode' as a valid answer. Instead, they force an "
            "incorrect answer by picking the largest, smallest, or middle value, confusing "
            "mode with other statistical measures like maximum, minimum, or median."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Always compute the answer independently, never use metadata
        solution = self._apply_malrule(problem)
        return solution.answer

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Mode-Must-Exist malrule.

        When no mode exists (all values unique), incorrectly picks
        largest, smallest, or middle value as the "mode".

        Args:
            problem: Mode calculation problem
            verbose: If True, generate verbose steps; if False (default), generate concise steps
        """
        template = problem.metadata.get('template', '')

        # Handle comparison problem specially
        if template == 'comparison_problem':
            return self._solve_comparison_problem(problem, verbose)

        data = problem.metadata.get('data', problem.operands)
        if not isinstance(data, list):
            data = problem.operands if isinstance(problem.operands, list) else [problem.operands]

        # Check if all values are unique
        from collections import Counter
        counts = Counter(data)
        max_count = max(counts.values())

        if max_count == 1:
            # All values appear once - no mode exists, but malrule student forces an answer
            mode = max(data)
            result = f"{mode}"
        else:
            # There is an actual mode - malrule would get this right
            modes = [value for value, count in counts.items() if count == max_count]
            if len(modes) == 1:
                result = f"{modes[0]}"
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
                result=result,
                is_word_problem=is_word_problem,
                context=context
            )

        return Solution(
            answer=result,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _solve_comparison_problem(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle comparison problems which compare two datasets."""
        data_a = problem.metadata.get('data_a', [])
        data_b = problem.metadata.get('data_b', [])

        # Analyze Dataset A
        from collections import Counter
        counts_a = Counter(data_a)
        max_count_a = max(counts_a.values())

        if max_count_a > 1:
            modes_a = [value for value, count in counts_a.items() if count == max_count_a]
            mode_a = modes_a[0]
        else:
            mode_a = max(data_a)

        # Analyze Dataset B
        counts_b = Counter(data_b)
        max_count_b = max(counts_b.values())

        if max_count_b == 1:
            malrule_mode_b = max(data_b)
            mode_b_answer = f"Dataset B has mode ({malrule_mode_b})"
        else:
            modes_b = [value for value, count in counts_b.items() if count == max_count_b]
            mode_b = modes_b[0]
            mode_b_answer = f"Dataset B has mode ({mode_b})"

        # Construct malrule answer
        malrule_answer = f"Dataset A has mode ({mode_a}), {mode_b_answer}"

        if verbose:
            steps = []
            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("MALRULE THINKING: Every dataset must have a mode!")
            steps.append("")

            steps.append(f"Dataset A: {data_a}")
            if max_count_a > 1:
                steps.append(f"  Value {mode_a} appears {max_count_a} times")
                steps.append(f"  Mode of Dataset A: {mode_a}")
            else:
                steps.append(f"  MALRULE: All values appear once, picking largest: {mode_a}")
            steps.append("")

            steps.append(f"Dataset B: {data_b}")
            if max_count_b == 1:
                steps.append(f"  MALRULE ERROR: All values appear once, but I must pick one!")
                steps.append(f"  Picking largest value: {malrule_mode_b}")
                steps.append(f"  INCORRECT! Dataset B has no mode (all values unique)")
            steps.append("")

            steps.append(f"MALRULE ANSWER: {malrule_answer}")
            steps.append("")
            steps.append("ERROR: Dataset B has no mode - all values appear once!")
        else:
            # Concise steps
            steps = []
            steps.append(problem.text)
            steps.append(f"Dataset A: Mode = {mode_a}")
            mode_b_str = malrule_mode_b if max_count_b == 1 else modes_b[0]
            steps.append(f"Dataset B: Mode = {mode_b_str}")
            steps.append(malrule_answer)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
