"""
Mean-Without-Understanding malrule algorithm.

Implements the systematic error where students calculate mean procedurally
without understanding what it represents. They apply the procedure correctly
but fail to recognize when the mean is misleading or non-representative.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List
from fractions import Fraction

def generate_concise_steps(problem_text, data, mean, result, is_word_problem=False, context=None):
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

    # Answer (malrule always claims mean is representative)
    steps.append(result)

    return steps

def generate_verbose_steps(problem_text, data, mean, result, question_type):
    """
    Generate verbose steps for the malrule algorithm.

    Returns detailed steps with explanations (original behavior).
    """
    steps = []

    steps.append(f"Analyzing data: {data}")
    steps.append(f"MALRULE: Always use mean as the primary measure")
    steps.append(f"Calculating mean: sum of all values ÷ count")
    steps.append(f"Sum: {' + '.join(map(str, data))} = {sum(data)}")
    steps.append(f"Count: {len(data)}")
    steps.append(f"Mean: {sum(data)} ÷ {len(data)} = {mean:.2f}")

    if question_type == 'calculate':
        steps.append(f"MALRULE ANSWER: {result}")
        steps.append(f"MALRULE ERROR: Computed correctly but no understanding of meaning")
    elif question_type == 'representative':
        steps.append(f"MALRULE THINKING: Mean is always representative")
        steps.append(f"MALRULE ANSWER: {result}")
        steps.append(f"MALRULE ERROR: Doesn't recognize outliers make mean non-representative!")
    elif question_type == 'which_measure':
        steps.append(f"MALRULE THINKING: Mean is always the best measure")
        steps.append(f"Median and mode are less important")
        steps.append(f"MALRULE ANSWER: {result}")
        steps.append(f"MALRULE ERROR: Doesn't consider whether data has outliers or is skewed!")
    elif question_type == 'good_measure':
        steps.append(f"MALRULE THINKING: Mean is always good")
        steps.append(f"MALRULE ANSWER: {result}")
        steps.append(f"MALRULE ERROR: Doesn't analyze data distribution!")
    else:
        steps.append(f"MALRULE ANSWER: {result}")
        steps.append(f"MALRULE ERROR: Always defaults to mean without critical thinking")

    return steps

class MeanWithoutUnderstandingMalrule(Malrule):
    """
    Implements the Mean-Without-Understanding bug.

    Students can calculate the mean correctly (add all values, divide by count)
    but don't understand what it represents. They:
    1. Always claim mean is "representative" even with outliers
    2. Always choose mean as "best measure" regardless of data distribution
    3. Don't recognize when mean is misleading
    4. Can't interpret what the mean tells them about the data

    Example: {1, 2, 2, 3, 100}
    Correct: Mean = 21.6, but median (2) is more representative due to outlier
    Malrule: Mean = 21.6, and this is "the typical value" (WRONG interpretation!)
    """

    def get_name(self) -> str:
        return "Mean-Without-Understanding"

    def get_description(self) -> str:
        return (
            "Students calculate mean procedurally (add all values, divide by count) without "
            "understanding what it represents. Research shows many students know how to compute "
            "means but do not know how to apply or interpret them (Konold & Pollatsek, 2002). "
            "They correctly compute the mean but: (1) claim it's always representative even with "
            "outliers, (2) always say mean is the 'best' measure regardless of distribution, "
            "(3) don't recognize when mean is misleading, and (4) can't explain what the mean "
            "tells them about the data."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Malrule: Calculate mean correctly but claim it's always representative
        solution = self._apply_malrule(problem)
        return solution.answer

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Mean-Without-Understanding malrule.

        Calculates mean correctly but always claims it's representative
        and always recommends mean as the best measure, even when inappropriate.

        Args:
            problem: Statistical interpretation problem
            verbose: If True, generate verbose steps; if False (default), generate concise steps
        """
        data = problem.metadata.get('data', problem.operands)
        if not isinstance(data, list):
            data = problem.operands if isinstance(problem.operands, list) else [problem.operands]

        problem_text_lower = problem.text.lower()

        # Calculate mean (student CAN do this)
        n = len(data)
        total = sum(data)
        mean = total / n

        # Determine question type and give malrule response
        if 'calculate' in problem_text_lower and 'mean' in problem_text_lower:
            question_type = 'calculate'
            result = f"{mean:.2f}"
        elif 'representative' in problem_text_lower or 'typical' in problem_text_lower:
            question_type = 'representative'
            result = f"Yes, the mean of {mean:.2f} is representative of the typical value."
        elif 'which measure' in problem_text_lower or 'best' in problem_text_lower or 'most appropriate' in problem_text_lower:
            question_type = 'which_measure'
            result = f"Mean ({mean:.2f}) is the best measure of center."
        elif 'good measure' in problem_text_lower or 'appropriate' in problem_text_lower:
            question_type = 'good_measure'
            result = f"Yes, the mean ({mean:.2f}) is a good measure of center for this data."
        else:
            question_type = 'generic'
            result = f"The mean is {mean:.2f}, which represents the typical value."

        # Get problem context
        is_word_problem = problem.metadata.get('is_word_problem', False)
        context = problem.metadata.get('context', 'data')

        # Generate steps based on verbose setting
        if verbose:
            steps = generate_verbose_steps(
                problem_text=problem.text,
                data=data,
                mean=mean,
                result=result,
                question_type=question_type
            )
        else:
            steps = generate_concise_steps(
                problem_text=problem.text,
                data=data,
                mean=mean,
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
