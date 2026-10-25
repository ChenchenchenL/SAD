"""
Ignore-Outliers-Effect malrule algorithm.

Implements the systematic error where students don't recognize how outliers
affect the mean. They say "yes, mean is representative" without understanding
that outliers pull the mean away from typical values.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List

def _calculate_median(data):
    """Helper to calculate median without importing statistics module."""
    sorted_data = sorted(data)
    n = len(sorted_data)
    if n % 2 == 0:
        return (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
    else:
        return sorted_data[n // 2]

def generate_concise_steps(problem_text, data, mean, median_val, malrule_answer, is_word_problem=False, context=None):
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

    # Mean calculation
    steps.append(f"Mean = {sum(data)} ÷ {len(data)} = {mean:.2f}")

    # Answer (malrule ignores outlier analysis)
    steps.append(malrule_answer)

    return steps

def generate_verbose_steps(problem_text, data, mean, median_val, malrule_answer, is_word_problem=False, context=None):
    """
    Generate verbose steps for the malrule algorithm.

    Returns detailed steps with explanations (original behavior).
    """
    steps = []

    # For word problems, include the context
    if is_word_problem:
        steps.append(f"Problem: {problem_text}")
        steps.append(f"")
        steps.append(f"MALRULE APPROACH: Ignore outliers, assume mean is always representative")
        steps.append(f"Data extracted ({context}): {data}")
        steps.append(f"")
    else:
        steps.append(f"Analyzing data: {data}")

    # Calculate mean
    steps.append(f"Calculating mean: {sum(data)} ÷ {len(data)} = {mean:.2f}")

    # MALRULE: Student says mean is representative without considering outliers
    steps.append(f"MALRULE THINKING: 'I calculated the mean, so it must be representative'")
    steps.append(f"MALRULE ERROR: Ignoring whether extreme values distort the mean")
    steps.append(f"The mean is {mean:.2f}")
    steps.append(f"MALRULE ANSWER: {malrule_answer}")
    steps.append(f"")
    steps.append(f"ERROR: Student didn't check for outliers!")

    # Show what they missed
    sorted_data = sorted(data)
    if len(sorted_data) >= 3:
        next_to_max = sorted_data[-2]
        max_val = sorted_data[-1]
        next_to_min = sorted_data[1]
        min_val = sorted_data[0]

        has_high_outlier = (max_val - next_to_max) > (next_to_max - min(sorted_data[:-1])) * 2
        has_low_outlier = (next_to_min - min_val) > (max(sorted_data[1:]) - next_to_min) * 2

        if has_high_outlier or has_low_outlier:
            steps.append(f"MISSED: Data range is {min(data)} to {max(data)}")
            steps.append(f"MISSED: Most values cluster around {median_val}, but extreme value is {max(data) if has_high_outlier else min(data)}")
            steps.append(f"MISSED: Mean ({mean:.2f}) is pulled away from typical values by outlier")
            steps.append(f"MISSED: Median ({median_val}) better represents typical values")
            steps.append(f"CORRECT: No, mean is NOT representative when outliers are present")

    return steps

class IgnoreOutliersEffectMalrule(Malrule):
    """
    Implements the Ignore-Outliers-Effect bug.

    Students calculate the mean correctly but don't recognize that outliers
    make the mean less representative. They believe:
    1. "Mean is always the best measure of center"
    2. "If I can calculate it, it must be representative"
    3. They don't check if extreme values distort the mean
    4. They ignore the concept of "typical" vs "average with outliers"

    Example: {5, 6, 5, 7, 6, 50}
    Mean = 13.2 (pulled up by 50)
    Median = 6 (represents typical values)

    Correct: "No, mean is not representative. The outlier (50) pulls the mean
              to 13.2, far from typical values (5-7). Median (6) is better."
    Malrule: "Yes, mean is representative. Mean = 13.2, so that's the answer."
    """

    def get_name(self) -> str:
        return "Ignore-Outliers-Effect"

    def get_description(self) -> str:
        return (
            "Students don't recognize how outliers affect the mean. Research shows students "
            "are 'not only confused about the median and the mean but also unable to use and "
            "interpret information' about when each is appropriate (Zawojewski & Shaughnessy, 2000). "
            "When asked if the mean represents a data set with outliers, they say 'yes' without "
            "understanding that outliers pull the mean away from typical values. They fail to "
            "identify that median is more appropriate for skewed data."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Always compute the answer independently, never use metadata
        return self._apply_malrule(problem).answer

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Ignore-Outliers-Effect malrule.

        Student calculates mean correctly but doesn't recognize that outliers
        make it non-representative. They say "yes, mean is representative"
        without considering the effect of extreme values.

        Args:
            problem: Statistics problem with potential outliers
            verbose: If True, generate verbose steps; if False (default), generate concise steps
        """
        template = problem.metadata.get('template', 'basic_outlier')

        # Handle comparison_problem specially
        if template == 'comparison_problem':
            return self._solve_comparison_problem(problem, verbose)

        data = problem.metadata.get('data', problem.operands)
        if not isinstance(data, list):
            data = problem.operands if isinstance(problem.operands, list) else [problem.operands]

        # Calculate statistics
        mean = sum(data) / len(data)
        median_val = _calculate_median(data)

        # Determine the malrule answer based on question type
        problem_text_lower = problem.text.lower()

        if 'which dataset' in problem_text_lower or 'dataset a' in problem_text_lower or 'dataset b' in problem_text_lower:
            # Comparison problem - delegate to special handler
            return self._solve_comparison_problem(problem, verbose)
        elif 'which measure' in problem_text_lower or 'mean or median' in problem_text_lower:
            malrule_answer = f"Mean ({mean:.2f}) is always the best measure"
        elif 'choose' in problem_text_lower and 'measure' in problem_text_lower:
            malrule_answer = f"Mean ({mean:.2f}) is always the best measure"
        else:
            malrule_answer = "Yes, mean is representative"

        # Get problem context
        is_word_problem = problem.metadata.get('is_word_problem', False)
        context = problem.metadata.get('context', 'data')

        # Generate steps based on verbose setting
        if verbose:
            steps = generate_verbose_steps(
                problem_text=problem.text,
                data=data,
                mean=mean,
                median_val=median_val,
                malrule_answer=malrule_answer,
                is_word_problem=is_word_problem,
                context=context
            )
        else:
            steps = generate_concise_steps(
                problem_text=problem.text,
                data=data,
                mean=mean,
                median_val=median_val,
                malrule_answer=malrule_answer,
                is_word_problem=is_word_problem,
                context=context
            )

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _solve_comparison_problem(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle comparison problems which compare two datasets."""
        data1 = problem.metadata.get('data1', [])
        data2 = problem.metadata.get('data2', [])

        # Calculate means for both datasets
        mean1 = sum(data1) / len(data1) if data1 else 0
        mean2 = sum(data2) / len(data2) if data2 else 0

        # MALRULE: Student doesn't check for outliers, assumes both means are equally representative
        malrule_answer = "Both means are equally representative"

        if verbose:
            steps = []
            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("MALRULE approach: Don't check for outliers, just say both means are representative")

            if data1:
                steps.append(f"Dataset A mean: {mean1:.2f}")
            if data2:
                steps.append(f"Dataset B mean: {mean2:.2f}")

            steps.append(f"MALRULE ANSWER: {malrule_answer}")
            steps.append("")
            steps.append("ERROR: Didn't check which dataset has outliers!")
        else:
            # Concise steps
            steps = []
            steps.append(problem.text)
            steps.append(f"Dataset A: Mean = {mean1:.2f}")
            steps.append(f"Dataset B: Mean = {mean2:.2f}")
            steps.append(malrule_answer)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
