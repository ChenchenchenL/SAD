"""
Correct statistical analysis algorithm with understanding.

Implements analysis of measures of center with conceptual understanding,
recognizing when mean is appropriate vs. when median/mode is better.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import CorrectAlgorithm, Problem, Solution
from typing import List


def generate_concise_steps(problem_text, data, mean, median, outliers, result, is_word_problem=False, context=None):
    """
    Generate concise steps for statistical analysis.

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

    # Median calculation
    steps.append(f"Sorted: {sorted(data)}, Median = {median:.2f}")

    # Outlier check
    if outliers:
        steps.append(f"Outliers: {outliers}")
    else:
        steps.append(f"No outliers detected")

    # Answer
    steps.append(result)

    return steps


def generate_verbose_steps(problem_text, data, mean, median, sorted_data, outliers, result, has_outliers, difference, question_type):
    """
    Generate verbose steps for statistical analysis.

    Returns detailed steps with explanations (original behavior).
    """
    steps = []

    steps.append(f"Analyzing data: {data}")
    steps.append(f"Sample size: {len(data)}")

    # Calculate mean
    steps.append(f"Calculating mean: {sum(data)} ÷ {len(data)} = {mean:.2f}")

    # Calculate median
    steps.append(f"Sorted data: {sorted_data}")
    steps.append(f"Median (middle value): {median:.2f}")

    # Check for outliers
    if outliers:
        steps.append(f"Outliers detected: {outliers}")
        steps.append(f"Outliers pull the mean away from typical values")
    else:
        steps.append(f"No significant outliers detected")

    # Compare mean and median
    if difference > median * 0.2:
        steps.append(f"Mean ({mean:.2f}) and median ({median:.2f}) differ significantly")
        steps.append(f"This suggests data is skewed or has outliers")
    else:
        steps.append(f"Mean ({mean:.2f}) and median ({median:.2f}) are similar")
        steps.append(f"This suggests data is roughly symmetric")

    # Add question-type specific steps
    if question_type == 'calculate':
        steps.append(f"Mean = {mean:.2f}")
        if has_outliers:
            steps.append(f"Note: This mean may not be representative due to outliers")
    elif question_type == 'representative':
        if has_outliers or difference > median * 0.2:
            steps.append(f"Analysis: Mean is pulled by outliers")
            steps.append(f"Most values cluster around {median:.2f}, not {mean:.2f}")
        else:
            steps.append(f"Analysis: No outliers, mean ≈ median")
    elif question_type == 'which_measure':
        if has_outliers or difference > median * 0.2:
            steps.append(f"Recommendation: Use MEDIAN")
            steps.append(f"Reason: Data has outliers/skew that distort the mean")
            steps.append(f"Mean = {mean:.2f}, Median = {median:.2f}")
            steps.append(f"Most values are closer to the median")
        else:
            steps.append(f"Recommendation: MEAN is appropriate")
            steps.append(f"Reason: Symmetric distribution, no outliers")
    elif question_type == 'good_measure':
        pass  # Result already captures this

    steps.append(f"ANSWER: {result}")
    steps.append(f"Final answer: {result}")

    return steps


class MeanWithUnderstandingCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for statistical analysis with understanding.

    Calculates mean correctly AND understands when it's appropriate.
    Recognizes outliers, skewed distributions, and recommends the most
    appropriate measure of center based on data characteristics.
    """

    def get_name(self) -> str:
        return "Correct Statistical Analysis with Understanding"

    def get_description(self) -> str:
        return (
            "Analyzes data to determine the most appropriate measure of center. "
            "Calculates mean correctly but also recognizes outliers and skewed "
            "distributions. Recommends median when data has outliers or is skewed, "
            "and mean when data is roughly symmetric without extreme values."
        )

    def _detect_outliers(self, data: List[float]) -> List[float]:
        """Detect outliers using IQR method (simplified)."""
        sorted_data = sorted(data)
        n = len(sorted_data)

        if n < 4:
            return []  # Too few points to detect outliers reliably

        # Calculate quartiles
        q1_idx = n // 4
        q3_idx = (3 * n) // 4
        q1 = sorted_data[q1_idx]
        q3 = sorted_data[q3_idx]
        iqr = q3 - q1

        # Outliers are beyond 1.5 * IQR from quartiles
        lower_fence = q1 - 1.5 * iqr
        upper_fence = q3 + 1.5 * iqr

        outliers = [x for x in data if x < lower_fence or x > upper_fence]
        return outliers

    def _calculate_median(self, data: List[float]) -> float:
        """Calculate median."""
        sorted_data = sorted(data)
        n = len(sorted_data)
        if n % 2 == 0:
            return (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
        else:
            return sorted_data[n//2]

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct statistical analysis with understanding.

        Args:
            problem: Statistical interpretation problem
            verbose: If True, generate verbose steps; if False (default), generate concise steps

        Returns:
            Solution with appropriate analysis
        """
        data = problem.metadata.get('data', problem.operands)
        if not isinstance(data, list):
            data = problem.operands if isinstance(problem.operands, list) else [problem.operands]

        problem_text_lower = problem.text.lower()

        # Calculate all measures
        n = len(data)
        total = sum(data)
        mean = total / n
        median = self._calculate_median(data)
        outliers = self._detect_outliers(data)
        sorted_data = sorted(data)
        has_outliers = bool(outliers)
        diff = abs(mean - median)

        # Determine question type
        if 'calculate' in problem_text_lower and 'mean' in problem_text_lower:
            question_type = 'calculate'
            result = f"{mean:.2f}"
            if has_outliers:
                result += f" (Note: may not be representative due to outliers)"
        elif 'representative' in problem_text_lower or 'typical' in problem_text_lower:
            question_type = 'representative'
            if has_outliers or diff > median * 0.2:
                result = f"No, the mean ({mean:.2f}) is NOT representative. The median ({median:.2f}) better represents the typical value because outliers skew the mean."
            else:
                result = f"Yes, the mean ({mean:.2f}) is representative. The data is roughly symmetric without outliers."
        elif 'which measure' in problem_text_lower or 'best' in problem_text_lower or 'most appropriate' in problem_text_lower:
            question_type = 'which_measure'
            if has_outliers or diff > median * 0.2:
                result = f"Median ({median:.2f}) is the best measure because the data has outliers or is skewed. The mean ({mean:.2f}) is pulled by extreme values and doesn't represent the typical value."
            else:
                result = f"Mean ({mean:.2f}) is appropriate because the data is roughly symmetric without outliers. Mean and median ({median:.2f}) are similar."
        elif 'good measure' in problem_text_lower or 'appropriate' in problem_text_lower:
            question_type = 'good_measure'
            if has_outliers or diff > median * 0.2:
                result = f"No, the mean ({mean:.2f}) is NOT a good measure for this data. The median ({median:.2f}) would be better because outliers make the mean non-representative."
            else:
                result = f"Yes, the mean ({mean:.2f}) is a good measure for this data. No outliers, and data is roughly symmetric."
        else:
            question_type = 'generic'
            if has_outliers or diff > median * 0.2:
                result = f"Mean = {mean:.2f}, Median = {median:.2f}. Due to outliers/skew, the median is more representative."
            else:
                result = f"Mean = {mean:.2f}, Median = {median:.2f}. Data is symmetric, so mean is appropriate."

        # Get problem context
        is_word_problem = problem.metadata.get('is_word_problem', False)
        context = problem.metadata.get('context', 'data')

        # Generate steps based on verbose setting
        if verbose:
            steps = generate_verbose_steps(
                problem_text=problem.text,
                data=data,
                mean=mean,
                median=median,
                sorted_data=sorted_data,
                outliers=outliers,
                result=result,
                has_outliers=has_outliers,
                difference=diff,
                question_type=question_type
            )
        else:
            steps = generate_concise_steps(
                problem_text=problem.text,
                data=data,
                mean=mean,
                median=median,
                outliers=outliers,
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
