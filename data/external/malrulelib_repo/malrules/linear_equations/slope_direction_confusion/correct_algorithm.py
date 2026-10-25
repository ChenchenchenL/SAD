"""
Correct algorithm for slope direction understanding.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class SlopeDirectionCorrectAlgorithm(CorrectAlgorithm):
    """Correctly identifies positive slopes as increasing and negative slopes as decreasing."""

    def get_name(self) -> str:
        return "Correct Slope Direction Understanding"

    def get_description(self) -> str:
        return "Correctly identifies that positive slopes increase and negative slopes decrease from left to right."

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        template = problem.metadata.get('template', '')

        # Handle word problem context specially
        if template == 'word_problem_context':
            return self._solve_word_problem_context(problem, verbose)

        # Handle comparison problem specially
        if template == 'comparison_problem':
            return self._solve_comparison_problem(problem, verbose)

        # Handle fractional slope specially
        if template == 'fractional_slope':
            return self._solve_fractional_slope(problem, verbose)

        # Standard templates
        m = problem.metadata.get('slope')

        # COMPUTE directions from slope value
        if m > 0:
            # Positive slope: line goes up (increasing)
            correct_direction = "increasing"
            correct_description = "going up from left to right"
            malrule_direction = "decreasing"  # Malrule: confused!
        else:
            # Negative slope: line goes down (decreasing)
            correct_direction = "decreasing"
            correct_description = "going down from left to right"
            malrule_direction = "increasing"  # Malrule: confused!

        # Generate steps based on verbosity setting
        if verbose:
            steps = self._generate_verbose_steps_standard(problem, m, correct_direction, correct_description, malrule_direction)
        else:
            steps = self._generate_concise_steps_standard(problem, m, correct_direction)

        return Solution(
            answer=correct_direction,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _solve_fractional_slope(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle fractional slope problems."""
        numerator = problem.metadata.get('numerator')
        denominator = problem.metadata.get('denominator')
        slope_str = f"{numerator}/{denominator}"

        # COMPUTE direction from slope sign (numerator determines sign)
        if numerator > 0:
            correct_direction = "increasing"
        else:
            correct_direction = "decreasing"

        # Generate steps based on verbosity setting
        if verbose:
            steps = self._generate_verbose_steps_fractional(problem, numerator, denominator, slope_str, correct_direction)
        else:
            steps = self._generate_concise_steps_fractional(problem, numerator, denominator, slope_str, correct_direction)

        return Solution(
            answer=correct_direction,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _solve_comparison_problem(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle comparison problems."""
        slope_a = problem.metadata.get('slope_a')
        slope_b = problem.metadata.get('slope_b')

        # COMPUTE answer from slope signs
        # Typically A is positive (increasing), B is negative (decreasing)
        dir_a = "increasing" if slope_a > 0 else "decreasing"
        dir_b = "increasing" if slope_b > 0 else "decreasing"
        correct_answer = f"Line A is {dir_a}, Line B is {dir_b}"

        # Generate steps based on verbosity setting
        if verbose:
            steps = self._generate_verbose_steps_comparison(problem, slope_a, slope_b, dir_a, dir_b, correct_answer)
        else:
            steps = self._generate_concise_steps_comparison(problem, slope_a, slope_b, dir_a, dir_b, correct_answer)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _solve_word_problem_context(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle word problem context templates."""
        word_problem_subtype = problem.metadata.get('word_problem_subtype', '')

        # COMPUTE answers from problem subtype
        if word_problem_subtype == 'positive_trend':
            # Positive slope context (growth, increase, rise)
            correct_answer = "increasing"
            malrule_answer = "decreasing"
        elif word_problem_subtype == 'negative_trend':
            # Negative slope context (fall, drop, decrease)
            correct_answer = "decreasing"
            malrule_answer = "increasing"
        elif word_problem_subtype == 'compare_trends':
            # Comparison: A positive, B negative
            correct_answer = "A is increasing, B is decreasing"
            malrule_answer = "A is decreasing, B is increasing"
        else:
            # Fallback
            correct_answer = "increasing"
            malrule_answer = "decreasing"

        # Generate steps based on verbosity setting
        if verbose:
            steps = self._generate_verbose_steps_word_problem(problem, word_problem_subtype, correct_answer, malrule_answer)
        else:
            steps = self._generate_concise_steps_word_problem(problem, word_problem_subtype, correct_answer)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _generate_concise_steps_standard(self, problem: Problem, m: int, correct_direction: str) -> List[str]:
        """Generate concise steps for standard templates."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Given: slope = {m}")
        steps.append(f"Slope sign: {'positive' if m > 0 else 'negative'}")
        steps.append(f"Direction: {'positive → increasing' if m > 0 else 'negative → decreasing'}")
        steps.append(f"Answer: {correct_direction}")
        return steps

    def _generate_verbose_steps_standard(self, problem: Problem, m: int, correct_direction: str, correct_description: str, malrule_direction: str) -> List[str]:
        """Generate verbose steps for standard templates."""
        steps = []
        steps.append(f"Problem: Describe the direction of a line with slope {m}")
        steps.append("")
        steps.append("CORRECT METHOD: Use slope sign to determine direction")
        steps.append("  Positive slope (+) → line goes UP (increasing)")
        steps.append("  Negative slope (−) → line goes DOWN (decreasing)")
        steps.append("")
        steps.append(f"Step 1: Identify the slope value and its sign")
        steps.append(f"  Given: slope = {m}")

        if m > 0:
            steps.append(f"  The slope is POSITIVE ({m} > 0)")
        else:
            steps.append(f"  The slope is NEGATIVE ({m} < 0)")

        steps.append("")
        steps.append(f"Step 2: Apply the slope-direction relationship")

        if m > 0:
            steps.append(f"  Positive slope → line goes UP from left to right")
            steps.append(f"  The line is INCREASING as x increases")
            steps.append(f"  Visual: The line tilts upward to the right ↗")
        else:
            steps.append(f"  Negative slope → line goes DOWN from left to right")
            steps.append(f"  The line is DECREASING as x increases")
            steps.append(f"  Visual: The line tilts downward to the right ↘")

        steps.append("")
        steps.append(f"Step 3: State the direction")
        steps.append(f"  Direction: {correct_direction}")
        steps.append(f"  Description: The line is {correct_description}")
        steps.append("")
        steps.append(f"Step 4: Verify the relationship")

        if m > 0:
            steps.append(f"  As x increases, y also increases")
            steps.append(f"  Slope {m} is positive → increasing ✓")
        else:
            steps.append(f"  As x increases, y decreases")
            steps.append(f"  Slope {m} is negative → decreasing ✓")

        steps.append("")
        steps.append(f"Final Answer: {correct_direction} ✓")
        steps.append("")
        steps.append(f"Key concept: Slope SIGN determines direction")
        steps.append(f"  Positive (+) → UP/increasing")
        steps.append(f"  Negative (−) → DOWN/decreasing")
        steps.append(f"  NOT {malrule_direction} (that's the OPPOSITE direction!) ✗")
        return steps

    def _generate_concise_steps_fractional(self, problem: Problem, numerator: int, denominator: int, slope_str: str, correct_direction: str) -> List[str]:
        """Generate concise steps for fractional slope problems."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Given: slope = {slope_str}")
        steps.append(f"Numerator sign: {'positive' if numerator > 0 else 'negative'}")
        steps.append(f"Direction: {'positive → increasing' if numerator > 0 else 'negative → decreasing'}")
        steps.append(f"Answer: {correct_direction}")
        return steps

    def _generate_verbose_steps_fractional(self, problem: Problem, numerator: int, denominator: int, slope_str: str, correct_direction: str) -> List[str]:
        """Generate verbose steps for fractional slope problems."""
        steps = []
        steps.append(f"Problem: Direction of a line with slope {slope_str}")
        steps.append("")
        steps.append("CORRECT METHOD: Use slope sign to determine direction")
        steps.append("")
        steps.append(f"Step 1: Identify the slope sign")
        steps.append(f"  Given: slope = {slope_str}")
        steps.append(f"  Numerator: {numerator} ({'positive' if numerator > 0 else 'negative'})")
        steps.append(f"  Denominator: {denominator} (positive)")
        steps.append(f"  Overall slope: {'positive' if numerator > 0 else 'negative'}")
        steps.append("")
        steps.append(f"Step 2: Apply slope-direction relationship")

        if numerator > 0:
            steps.append(f"  Positive slope → line goes UP (increasing)")
        else:
            steps.append(f"  Negative slope → line goes DOWN (decreasing)")

        steps.append("")
        steps.append(f"Final Answer: {correct_direction} ✓")
        steps.append("")
        steps.append(f"Key: Sign of slope determines direction, not magnitude")
        return steps

    def _generate_concise_steps_comparison(self, problem: Problem, slope_a: int, slope_b: int, dir_a: str, dir_b: str, correct_answer: str) -> List[str]:
        """Generate concise steps for comparison problems."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Line A: slope = {slope_a} → {dir_a}")
        steps.append(f"Line B: slope = {slope_b} → {dir_b}")
        steps.append(f"Answer: {correct_answer}")
        return steps

    def _generate_verbose_steps_comparison(self, problem: Problem, slope_a: int, slope_b: int, dir_a: str, dir_b: str, correct_answer: str) -> List[str]:
        """Generate verbose steps for comparison problems."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD: Identify sign of each slope")
        steps.append("")
        steps.append(f"Line A: slope = {slope_a}")
        steps.append(f"  Positive slope → increasing")
        steps.append("")
        steps.append(f"Line B: slope = {slope_b}")
        steps.append(f"  Negative slope → decreasing")
        steps.append("")
        steps.append(f"ANSWER: {correct_answer}")
        steps.append("")
        steps.append("✓ Correctly applied slope-direction relationship")
        steps.append("  Positive (+) → UP/increasing")
        steps.append("  Negative (−) → DOWN/decreasing")
        return steps

    def _generate_concise_steps_word_problem(self, problem: Problem, word_problem_subtype: str, correct_answer: str) -> List[str]:
        """Generate concise steps for word problem context."""
        steps = []
        steps.append(f"Question: {problem.text}")

        if word_problem_subtype == 'positive_trend':
            m = problem.metadata.get('slope')
            steps.append(f"Extract: rate = {m} (increasing/rising)")
            steps.append(f"Direction: positive slope → increasing")
            steps.append(f"Answer: {correct_answer}")

        elif word_problem_subtype == 'negative_trend':
            m = problem.metadata.get('slope')
            steps.append(f"Extract: rate = {m} (decreasing/falling)")
            steps.append(f"Direction: negative slope → decreasing")
            steps.append(f"Answer: {correct_answer}")

        elif word_problem_subtype == 'compare_trends':
            slope_a = problem.metadata.get('slope_a')
            slope_b = problem.metadata.get('slope_b')
            steps.append(f"Extract: A slope = {slope_a}, B slope = {slope_b}")
            steps.append(f"A: positive → increasing, B: negative → decreasing")
            steps.append(f"Answer: {correct_answer}")

        return steps

    def _generate_verbose_steps_word_problem(self, problem: Problem, word_problem_subtype: str, correct_answer: str, malrule_answer: str) -> List[str]:
        """Generate verbose steps for word problem context."""
        steps = []
        steps.append(f"Problem: {problem.text[:100]}...")
        steps.append("")
        steps.append("CORRECT METHOD: Identify if trend/rate is going up or down")
        steps.append("")

        if word_problem_subtype == 'positive_trend':
            m = problem.metadata.get('slope')
            steps.append(f"Step 1: Identify the rate of change")
            steps.append(f"  Context describes: increasing/rising/growing at {m} units")
            steps.append("")
            steps.append(f"Step 2: Determine direction")
            steps.append(f"  When something increases/grows/rises → POSITIVE slope")
            steps.append(f"  Positive slope → INCREASING trend ✓")
            steps.append("")
            steps.append(f"Final Answer: {correct_answer} ✓")
            steps.append(f"  NOT {malrule_answer} (that's the opposite!) ✗")

        elif word_problem_subtype == 'negative_trend':
            m = problem.metadata.get('slope')
            steps.append(f"Step 1: Identify the rate of change")
            steps.append(f"  Context describes: decreasing/falling/dropping")
            steps.append("")
            steps.append(f"Step 2: Determine direction")
            steps.append(f"  When something decreases/falls/drops → NEGATIVE slope")
            steps.append(f"  Negative slope → DECREASING trend ✓")
            steps.append("")
            steps.append(f"Final Answer: {correct_answer} ✓")
            steps.append(f"  NOT {malrule_answer} (that's the opposite!) ✗")

        elif word_problem_subtype == 'compare_trends':
            slope_a = problem.metadata.get('slope_a')
            slope_b = problem.metadata.get('slope_b')
            steps.append(f"Step 1: Identify each trend")
            steps.append(f"  Trend A: growing/rising → positive slope → INCREASING")
            steps.append(f"  Trend B: falling/decreasing → negative slope → DECREASING")
            steps.append("")
            steps.append(f"Step 2: State both directions correctly")
            steps.append(f"  A has positive slope ({slope_a}) → increasing ✓")
            steps.append(f"  B has negative slope ({slope_b}) → decreasing ✓")
            steps.append("")
            steps.append(f"Final Answer: {correct_answer} ✓")
            steps.append(f"  NOT {malrule_answer} (that reverses both!) ✗")

        return steps
