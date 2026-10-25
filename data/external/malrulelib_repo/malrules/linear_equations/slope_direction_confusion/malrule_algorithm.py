"""
Malrule algorithm for Slope-Direction-Confusion error.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class SlopeDirectionConfusionMalrule(Malrule):
    """
    Students confuse positive and negative slope directions.
    They don't distinguish between the signs, saying negative slopes are "increasing"
    or positive slopes are "decreasing."

    Example 1: Slope = -2
    Student: "The line is increasing/going up" (WRONG!)
    Correct: "The line is decreasing/going down"

    Example 2: Slope = 3
    Student: "The line is decreasing/going down" (WRONG!)
    Correct: "The line is increasing/going up"
    """

    def get_name(self) -> str:
        return "Slope-Direction-Confusion"

    def get_description(self) -> str:
        return (
            "Student confuses positive and negative slope directions, incorrectly stating "
            "that negative slopes represent increasing functions or positive slopes represent "
            "decreasing functions. This reflects a disconnect between the algebraic sign of "
            "slope and its geometric interpretation on a graph."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        template = problem.metadata.get('template', '')

        if template == 'fractional_slope':
            numerator = problem.metadata.get('numerator')
            # Malrule: reverse the direction
            return "decreasing" if numerator > 0 else "increasing"

        elif template == 'comparison_problem':
            slope_a = problem.metadata.get('slope_a')
            slope_b = problem.metadata.get('slope_b')
            # Malrule: reverse both directions
            dir_a = "decreasing" if slope_a > 0 else "increasing"
            dir_b = "decreasing" if slope_b > 0 else "increasing"
            return f"Line A is {dir_a}, Line B is {dir_b}"

        elif template == 'word_problem_context':
            word_problem_subtype = problem.metadata.get('word_problem_subtype', '')
            if word_problem_subtype == 'positive_trend':
                return "decreasing"  # Malrule: reversed
            elif word_problem_subtype == 'negative_trend':
                return "increasing"  # Malrule: reversed
            elif word_problem_subtype == 'compare_trends':
                return "A is decreasing, B is increasing"  # Malrule: reversed
            else:
                return "decreasing"

        else:
            # Standard templates
            m = problem.metadata.get('slope')
            # Malrule: reverse the direction
            return "decreasing" if m > 0 else "increasing"

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
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

        # COMPUTE directions by reversing correct logic (malrule)
        if m > 0:
            # Positive slope: CORRECT would be "increasing"
            # MALRULE: confused, says "decreasing"
            malrule_direction = "decreasing"
            malrule_description = "going down from left to right"
            correct_direction = "increasing"
        else:
            # Negative slope: CORRECT would be "decreasing"
            # MALRULE: confused, says "increasing"
            malrule_direction = "increasing"
            malrule_description = "going up from left to right"
            correct_direction = "decreasing"

        # Generate steps based on verbosity setting
        if verbose:
            steps = self._generate_verbose_steps_standard(problem, m, malrule_direction, malrule_description, correct_direction)
        else:
            steps = self._generate_concise_steps_standard(problem, m, malrule_direction)

        return Solution(
            answer=malrule_direction,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _solve_fractional_slope(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle fractional slope problems."""
        numerator = problem.metadata.get('numerator')
        denominator = problem.metadata.get('denominator')
        slope_str = f"{numerator}/{denominator}"

        # COMPUTE directions (malrule: reversed)
        if numerator > 0:
            malrule_direction = "decreasing"  # Malrule: reversed
            correct_direction = "increasing"
        else:
            malrule_direction = "increasing"  # Malrule: reversed
            correct_direction = "decreasing"

        # Generate steps based on verbosity setting
        if verbose:
            steps = self._generate_verbose_steps_fractional(problem, numerator, denominator, slope_str, malrule_direction, correct_direction)
        else:
            steps = self._generate_concise_steps_fractional(problem, numerator, slope_str, malrule_direction)

        return Solution(
            answer=malrule_direction,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _solve_comparison_problem(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle comparison problems."""
        slope_a = problem.metadata.get('slope_a')
        slope_b = problem.metadata.get('slope_b')

        # COMPUTE answer (malrule: reverse both directions)
        dir_a = "decreasing" if slope_a > 0 else "increasing"
        dir_b = "decreasing" if slope_b > 0 else "increasing"
        malrule_answer = f"Line A is {dir_a}, Line B is {dir_b}"

        # Generate steps based on verbosity setting
        if verbose:
            steps = self._generate_verbose_steps_comparison(problem, slope_a, slope_b, dir_a, dir_b, malrule_answer)
        else:
            steps = self._generate_concise_steps_comparison(problem, slope_a, slope_b, dir_a, dir_b, malrule_answer)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _solve_word_problem_context(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle word problem context templates."""
        word_problem_subtype = problem.metadata.get('word_problem_subtype', '')

        # COMPUTE answers (malrule: reversed)
        if word_problem_subtype == 'positive_trend':
            correct_answer = "increasing"
            malrule_answer = "decreasing"  # Malrule: reversed
        elif word_problem_subtype == 'negative_trend':
            correct_answer = "decreasing"
            malrule_answer = "increasing"  # Malrule: reversed
        elif word_problem_subtype == 'compare_trends':
            correct_answer = "A is increasing, B is decreasing"
            malrule_answer = "A is decreasing, B is increasing"  # Malrule: reversed
        else:
            correct_answer = "increasing"
            malrule_answer = "decreasing"

        # Generate steps based on verbosity setting
        if verbose:
            steps = self._generate_verbose_steps_word_problem(problem, word_problem_subtype, malrule_answer)
        else:
            steps = self._generate_concise_steps_word_problem(problem, word_problem_subtype, malrule_answer)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _generate_concise_steps_standard(self, problem: Problem, m: int, malrule_direction: str) -> List[str]:
        """Generate concise steps for standard templates."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Given: slope = {m}")
        steps.append(f"Slope sign: {'positive' if m > 0 else 'negative'}")
        steps.append(f"Direction: {'positive → decreasing' if m > 0 else 'negative → increasing'}")
        steps.append(f"Answer: {malrule_direction}")
        return steps

    def _generate_verbose_steps_standard(self, problem: Problem, m: int, malrule_direction: str, malrule_description: str, correct_direction: str) -> List[str]:
        """Generate verbose steps for standard templates."""
        steps = []
        steps.append(f"Problem: Describe the direction of a line with slope {m}")
        steps.append("")
        steps.append("MALRULE: Student CONFUSES positive/negative slope directions")
        steps.append(f"  MALRULE REASONING: Student doesn't distinguish between signs")
        steps.append("")
        steps.append(f"Step 1: Look at the slope value")
        steps.append(f"  Given: slope = {m}")

        if m > 0:
            steps.append(f"  Student notices: The slope is positive")
        else:
            steps.append(f"  Student notices: The slope is negative")

        steps.append("")
        steps.append(f"Step 2: Determine direction (INCORRECTLY!)")
        steps.append(f"  MALRULE THINKING: Student confuses the sign-to-direction relationship")

        if m > 0:
            steps.append(f"  Student thinks: 'Positive slope means the line is {malrule_direction}'")
            steps.append(f"  [WRONG! Positive should mean INCREASING, not decreasing]")
        else:
            steps.append(f"  Student thinks: 'Negative slope means the line is {malrule_direction}'")
            steps.append(f"  [WRONG! Negative should mean DECREASING, not increasing]")

        steps.append("")
        steps.append(f"Step 3: State the direction (WRONG!)")
        steps.append(f"  Student says: The line is {malrule_direction}")
        steps.append(f"  Student says: The line is {malrule_description}")
        steps.append("")
        steps.append(f"Final Answer: {malrule_direction} (INCORRECT - confused the sign!)")
        steps.append(f"  ERROR: Slope {m} ({'positive' if m > 0 else 'negative'}) should mean {correct_direction}")
        steps.append(f"  Student got the direction BACKWARDS!")
        return steps

    def _generate_concise_steps_fractional(self, problem: Problem, numerator: int, slope_str: str, malrule_direction: str) -> List[str]:
        """Generate concise steps for fractional slope problems."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Given: slope = {slope_str}")
        steps.append(f"Numerator sign: {'positive' if numerator > 0 else 'negative'}")
        steps.append(f"Direction: {'positive → decreasing' if numerator > 0 else 'negative → increasing'}")
        steps.append(f"Answer: {malrule_direction}")
        return steps

    def _generate_verbose_steps_fractional(self, problem: Problem, numerator: int, denominator: int, slope_str: str, malrule_direction: str, correct_direction: str) -> List[str]:
        """Generate verbose steps for fractional slope problems."""
        steps = []
        steps.append(f"Problem: Direction of a line with slope {slope_str}")
        steps.append("")
        steps.append("MALRULE: Student confuses positive/negative slope directions")
        steps.append("")
        steps.append(f"Step 1: Look at the slope")
        steps.append(f"  Given: slope = {slope_str}")
        steps.append(f"  Numerator: {numerator} ({'positive' if numerator > 0 else 'negative'})")
        steps.append("")
        steps.append(f"Step 2: Determine direction (INCORRECTLY!)")
        steps.append(f"  MALRULE: Student confuses sign-to-direction")

        if numerator > 0:
            steps.append(f"  Student thinks: 'Positive slope = {malrule_direction}' [WRONG!]")
        else:
            steps.append(f"  Student thinks: 'Negative slope = {malrule_direction}' [WRONG!]")

        steps.append("")
        steps.append(f"Final Answer: {malrule_direction} (INCORRECT!)")
        steps.append(f"  ERROR: Slope {slope_str} is {'positive' if numerator > 0 else 'negative'}, should be {correct_direction}")
        return steps

    def _generate_concise_steps_comparison(self, problem: Problem, slope_a: int, slope_b: int, dir_a: str, dir_b: str, malrule_answer: str) -> List[str]:
        """Generate concise steps for comparison problems."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Line A: slope = {slope_a} → {dir_a}")
        steps.append(f"Line B: slope = {slope_b} → {dir_b}")
        steps.append(f"Answer: {malrule_answer}")
        return steps

    def _generate_verbose_steps_comparison(self, problem: Problem, slope_a: int, slope_b: int, dir_a: str, dir_b: str, malrule_answer: str) -> List[str]:
        """Generate verbose steps for comparison problems."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: Student confuses positive/negative slope directions")
        steps.append("")
        steps.append(f"Line A: slope = {slope_a} (positive)")
        steps.append(f"  MALRULE: Student thinks positive = decreasing [WRONG!]")
        steps.append(f"  Student says: Line A is decreasing")
        steps.append("")
        steps.append(f"Line B: slope = {slope_b} (negative)")
        steps.append(f"  MALRULE: Student thinks negative = increasing [WRONG!]")
        steps.append(f"  Student says: Line B is increasing")
        steps.append("")
        steps.append(f"MALRULE ANSWER: {malrule_answer}")
        steps.append("")
        steps.append("ERROR: Student has the directions BACKWARDS!")
        steps.append("  Positive slopes increase, negative slopes decrease")
        return steps

    def _generate_concise_steps_word_problem(self, problem: Problem, word_problem_subtype: str, malrule_answer: str) -> List[str]:
        """Generate concise steps for word problem context."""
        steps = []
        steps.append(f"Question: {problem.text}")

        if word_problem_subtype == 'positive_trend':
            m = problem.metadata.get('slope')
            steps.append(f"Extract: rate = {m} (increasing/rising)")
            steps.append(f"Direction: positive slope → decreasing")
            steps.append(f"Answer: {malrule_answer}")

        elif word_problem_subtype == 'negative_trend':
            m = problem.metadata.get('slope')
            steps.append(f"Extract: rate = {m} (decreasing/falling)")
            steps.append(f"Direction: negative slope → increasing")
            steps.append(f"Answer: {malrule_answer}")

        elif word_problem_subtype == 'compare_trends':
            slope_a = problem.metadata.get('slope_a')
            slope_b = problem.metadata.get('slope_b')
            steps.append(f"Extract: A slope = {slope_a}, B slope = {slope_b}")
            steps.append(f"A: positive → decreasing, B: negative → increasing")
            steps.append(f"Answer: {malrule_answer}")

        return steps

    def _generate_verbose_steps_word_problem(self, problem: Problem, word_problem_subtype: str, malrule_answer: str) -> List[str]:
        """Generate verbose steps for word problem context."""
        steps = []
        steps.append(f"Problem: {problem.text[:100]}...")
        steps.append("")
        steps.append("MALRULE: Student CONFUSES trend directions")
        steps.append(f"  MALRULE REASONING: Student doesn't correctly identify if increasing or decreasing")
        steps.append("")

        if word_problem_subtype == 'positive_trend':
            m = problem.metadata.get('slope')
            steps.append(f"Step 1: Read context")
            steps.append(f"  Context describes: growth/increase/rise")
            steps.append("")
            steps.append(f"Step 2: Determine direction (INCORRECTLY!)")
            steps.append(f"  MALRULE THINKING: Student confuses increase with decrease")
            steps.append(f"  Student thinks: 'This is {malrule_answer}' [WRONG!]")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT!)")
            steps.append(f"  ERROR: Growing/rising = increasing, not {malrule_answer}")

        elif word_problem_subtype == 'negative_trend':
            m = problem.metadata.get('slope')
            steps.append(f"Step 1: Read context")
            steps.append(f"  Context describes: falling/dropping/decreasing")
            steps.append("")
            steps.append(f"Step 2: Determine direction (INCORRECTLY!)")
            steps.append(f"  MALRULE THINKING: Student confuses decrease with increase")
            steps.append(f"  Student thinks: 'This is {malrule_answer}' [WRONG!]")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT!)")
            steps.append(f"  ERROR: Falling/dropping = decreasing, not {malrule_answer}")

        elif word_problem_subtype == 'compare_trends':
            slope_a = problem.metadata.get('slope_a')
            slope_b = problem.metadata.get('slope_b')
            steps.append(f"Step 1: Read both trends")
            steps.append(f"  Trend A: growing/rising (positive slope)")
            steps.append(f"  Trend B: falling/decreasing (negative slope)")
            steps.append("")
            steps.append(f"Step 2: Identify directions (INCORRECTLY!)")
            steps.append(f"  MALRULE: Student reverses both directions")
            steps.append(f"  Student thinks A is {malrule_answer.split(',')[0].split('is')[1].strip()}")
            steps.append(f"  Student thinks B is {malrule_answer.split(',')[1].split('is')[1].strip()}")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT!)")
            steps.append(f"  ERROR: Got BOTH directions backwards!")

        return steps
