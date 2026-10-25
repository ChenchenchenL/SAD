"""
Correct outlier-aware representativeness algorithm.

Correctly identifies when outliers make the mean less representative and
recognizes that median is more appropriate for skewed data with outliers.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import CorrectAlgorithm, Problem, Solution
from typing import List, Tuple


# Helper functions to avoid importing statistics module (which conflicts with malrules.statistics package)
def _calculate_mean(data):
    """Calculate mean."""
    return sum(data) / len(data)


def _calculate_median(data):
    """Calculate median."""
    sorted_data = sorted(data)
    n = len(sorted_data)
    if n % 2 == 0:
        return (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
    else:
        return sorted_data[n // 2]


def _calculate_stdev(data):
    """Calculate standard deviation."""
    if len(data) < 2:
        raise ValueError("Need at least 2 data points")
    mean = _calculate_mean(data)
    variance = sum((x - mean) ** 2 for x in data) / (len(data) - 1)
    return variance ** 0.5


# Alias for compatibility
stats_mean = _calculate_mean
stats_median = _calculate_median
stats_stdev = _calculate_stdev


class StatisticsError(Exception):
    """Statistics error."""
    pass


def generate_concise_steps(problem_text, data, mean, median, sorted_data, outliers, result, is_word_problem=False, context=None):
    """
    Generate concise steps for outlier-aware representativeness evaluation.

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
    steps.append(f"Sorted: {sorted_data}, Median = {median}")

    # Outlier check
    if outliers:
        steps.append(f"Outliers: {outliers}")
    else:
        steps.append(f"No outliers detected")

    # Answer
    steps.append(result)

    return steps


def generate_verbose_steps(problem_text, data, mean, median, sorted_data, outliers, outlier_method, result, is_word_problem=False, context=None, has_outliers=False, difference=0):
    """
    Generate verbose steps for outlier-aware representativeness evaluation.

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
        steps.append(f"Step 2: Analyze representativeness of the mean")
    else:
        steps.append(f"Analyzing data: {data}")
        steps.append(f"Question: Is the mean representative of this data set?")
        steps.append(f"")

    # Step 1: Calculate mean
    steps.append(f"Step 1: Calculate the mean")
    steps.append(f"  Mean = {sum(data)} ÷ {len(data)} = {mean:.2f}")
    steps.append(f"")

    # Step 2: Calculate median
    steps.append(f"Step 2: Calculate the median")
    steps.append(f"  Sorted data: {sorted_data}")
    steps.append(f"  Median = {median}")
    steps.append(f"")

    # Step 3: Check for outliers
    steps.append(f"Step 3: Check for outliers (extreme values)")
    if outliers:
        steps.append(f"  Outlier(s) found: {outliers}")
        steps.append(f"  Detection method: {outlier_method}")
    steps.append(f"")

    # Step 4: Compare mean and median
    steps.append(f"Step 4: Compare mean and median")
    steps.append(f"  Mean = {mean:.2f}")
    steps.append(f"  Median = {median}")
    steps.append(f"  Difference = {difference:.2f}")
    steps.append(f"")

    # Step 5: Evaluate representativeness
    steps.append(f"Step 5: Evaluate representativeness")

    if has_outliers:
        steps.append(f"  Outliers detected: {outliers}")
        steps.append(f"  Outliers pull the mean away from typical values")
        outlier_val = outliers[0]
        if outlier_val > median:
            direction = "higher"
        else:
            direction = "lower"
        steps.append(f"  The outlier pulls the mean {direction} than typical values")
        steps.append(f"  Mean ({mean:.2f}) does not represent the typical value well")
        steps.append(f"  Median ({median}) stays closer to the center of typical values")
        steps.append(f"")
        steps.append(f"Conclusion: NO, the mean is NOT representative")
        steps.append(f"  Reason: Outlier(s) distort the mean")
        steps.append(f"  Better measure: Median = {median} (resistant to outliers)")
    elif difference > median * 0.2:
        steps.append(f"  Mean and median differ significantly")
        steps.append(f"  This suggests the data may be skewed")
        steps.append(f"  Mean may not represent typical values well")
        steps.append(f"")
        steps.append(f"Conclusion: Mean is less representative")
        steps.append(f"  Reason: Data appears skewed")
        steps.append(f"  Better measure: Median = {median}")
    else:
        steps.append(f"  No significant outliers detected")
        steps.append(f"  Mean and median are similar")
        steps.append(f"  Data appears roughly symmetric")
        steps.append(f"")
        steps.append(f"Conclusion: YES, the mean is representative")
        steps.append(f"  Reason: No outliers, data roughly symmetric")
        steps.append(f"  Mean ({mean:.2f}) accurately represents typical values")

    steps.append(f"")
    steps.append(f"Final answer: {result}")

    return steps


class IgnoreOutliersEffectCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for evaluating whether mean is representative.

    Correctly:
    1. Calculates both mean and median
    2. Identifies outliers (values far from typical range)
    3. Recognizes when outliers pull mean away from typical values
    4. Recommends median over mean for skewed data with outliers
    """

    def get_name(self) -> str:
        return "Correct Outlier-Aware Representativeness Evaluation"

    def get_description(self) -> str:
        return (
            "Correctly evaluates whether the mean is representative by checking for "
            "outliers. Recognizes that outliers pull the mean away from typical values "
            "and that median is more appropriate for skewed data."
        )

    def _identify_outliers(self, data: List[float]) -> Tuple[List[float], str]:
        """
        Identify outliers using simple clustering approach.

        For educational purposes, we use a simplified approach:
        - Calculate mean and standard deviation
        - Values more than 2.5 standard deviations from mean are outliers

        Args:
            data: List of numerical values

        Returns:
            Tuple of (outliers_list, description)
        """
        if len(data) < 3:
            return [], "Dataset too small to identify outliers"

        mean = stats_mean(data)

        # Handle case where all values are the same
        try:
            stdev = stats_stdev(data)
        except StatisticsError:
            return [], "No variation in data (all values identical)"

        if stdev == 0:
            return [], "No variation in data"

        # Simple outlier detection: values more than 2.5 std devs from mean
        outliers = []
        for value in data:
            z_score = abs((value - mean) / stdev)
            if z_score > 2.5:  # Commonly used threshold
                outliers.append(value)

        return outliers, f"Values more than 2.5 standard deviations from mean"

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct representativeness evaluation.

        Args:
            problem: Statistics problem with potential outliers
            verbose: If True, generate verbose steps; if False (default), generate concise steps

        Returns:
            Solution explaining whether mean is representative
        """
        template = problem.metadata.get('template', 'basic_outlier')

        # Handle comparison_problem specially
        if template == 'comparison_problem':
            return self._solve_comparison_problem(problem, verbose)

        data = problem.metadata.get('data', problem.operands)
        if not isinstance(data, list):
            data = problem.operands if isinstance(problem.operands, list) else [problem.operands]

        # Calculate statistics
        mean = stats_mean(data)
        median = stats_median(data)
        sorted_data = sorted(data)
        difference = abs(mean - median)

        # Check for outliers
        outliers, outlier_method = self._identify_outliers(data)

        # If statistical test doesn't flag outliers, check for large gaps
        if not outliers:
            typical_values = sorted_data[:-1]  # All except largest
            if len(typical_values) > 0:
                typical_range = max(typical_values) - min(typical_values)
                max_val = max(data)

                if typical_range > 0 and (max_val - max(typical_values)) > typical_range * 2:
                    outliers = [max_val]
                elif len(typical_values) > 0:
                    typical_values_high = sorted_data[1:]
                    min_val = min(data)
                    typical_range_high = max(typical_values_high) - min(typical_values_high)
                    if typical_range_high > 0 and (min(typical_values_high) - min_val) > typical_range_high * 2:
                        outliers = [min_val]

        # Determine result
        if outliers:
            result = f"No, the mean is not representative. The outlier(s) {outliers} pull the mean to {mean:.2f}, which is far from typical values. The median ({median}) is more representative."
        elif difference > median * 0.2:
            result = f"No, the mean is less representative. The data appears skewed (mean {mean:.2f} vs median {median}). The median is more representative of typical values."
        else:
            result = f"Yes, the mean is representative. No significant outliers detected, and mean ({mean:.2f}) is close to median ({median})."

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
                outlier_method=outlier_method,
                result=result,
                is_word_problem=is_word_problem,
                context=context,
                has_outliers=bool(outliers),
                difference=difference
            )
        else:
            steps = generate_concise_steps(
                problem_text=problem.text,
                data=data,
                mean=mean,
                median=median,
                sorted_data=sorted_data,
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

    def _solve_comparison_problem(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle comparison problems which compare two datasets."""
        correct_answer = problem.metadata['correct_answer']
        data1 = problem.metadata['data1']
        data2 = problem.metadata['data2']

        # Calculate statistics for both datasets
        mean1 = stats_mean(data1)
        median1 = stats_median(data1)
        outliers1, _ = self._identify_outliers(data1)
        mean2 = stats_mean(data2)
        median2 = stats_median(data2)
        outliers2, _ = self._identify_outliers(data2)

        if verbose:
            steps = []
            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("Correct approach: Check each dataset for outliers and representativeness")
            steps.append("")

            # Analyze Dataset 1
            steps.append(f"Dataset A: {sorted(data1)}")
            steps.append(f"  Mean: {mean1:.2f}, Median: {median1}")
            if outliers1:
                steps.append(f"  Outliers detected: {outliers1}")
                steps.append(f"  Mean is NOT representative (distorted by outliers)")
            else:
                steps.append(f"  No significant outliers")
                steps.append(f"  Mean is representative")
            steps.append("")

            # Analyze Dataset 2
            steps.append(f"Dataset B: {sorted(data2)}")
            steps.append(f"  Mean: {mean2:.2f}, Median: {median2}")
            if outliers2:
                steps.append(f"  Outliers detected: {outliers2}")
                steps.append(f"  Mean is NOT representative (distorted by outliers)")
            else:
                steps.append(f"  No significant outliers")
                steps.append(f"  Mean is representative")
            steps.append("")

            steps.append(f"Conclusion: {correct_answer}")
        else:
            # Concise steps
            steps = []
            steps.append(problem.text)
            steps.append(f"Dataset A: Mean = {mean1:.2f}, Median = {median1}, Outliers: {outliers1 if outliers1 else 'None'}")
            steps.append(f"Dataset B: Mean = {mean2:.2f}, Median = {median2}, Outliers: {outliers2 if outliers2 else 'None'}")
            steps.append(correct_answer)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
