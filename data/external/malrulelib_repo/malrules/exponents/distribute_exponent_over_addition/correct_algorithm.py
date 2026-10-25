"""
Correct algorithm for exponents over sums.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import CorrectAlgorithm, Problem, Solution
from typing import List


class ExponentOverSumCorrectAlgorithm(CorrectAlgorithm):
    """Correctly evaluates (a+b)^n by first computing the sum."""

    def get_name(self):
        return "Correct Exponent Over Sum"

    def get_description(self):
        return "Evaluates (a+b)^n by first computing (a+b), then raising to power n"

    def _generate_concise_steps(self, problem: Problem, correct_answer, sum_value) -> List[str]:
        """Generate concise steps showing only formula and values."""
        a = problem.metadata['a']
        b = problem.metadata['b']
        exponent = problem.metadata['exponent']
        is_word_problem = problem.metadata.get('is_word_problem', False)

        steps = []

        # Question
        steps.append(f"{problem.text}")

        # For word problems, show extraction step
        if is_word_problem:
            if 'c' in problem.metadata:
                c = problem.metadata['c']
                steps.append(f"({a} + {b} + {c})^{exponent}")
            else:
                steps.append(f"({a} + {b})^{exponent}")

        # Calculation steps
        if 'c' in problem.metadata:
            c = problem.metadata['c']
            steps.append(f"{a} + {b} + {c} = {sum_value}")
        else:
            steps.append(f"{a} + {b} = {sum_value}")

        steps.append(f"{sum_value}^{exponent} = {correct_answer}")

        # Answer
        steps.append(f"{correct_answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, correct_answer, sum_value) -> List[str]:
        """Generate verbose steps with full explanations (original behavior)."""
        a = problem.metadata['a']
        b = problem.metadata['b']
        exponent = problem.metadata['exponent']
        is_word_problem = problem.metadata.get('is_word_problem', False)
        word_problem_type = problem.metadata.get('word_problem_type', None)

        steps = []

        # For word problems, show extraction step
        if is_word_problem:
            steps.append(f"Word Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Extract the mathematical expression from the word problem")

            if word_problem_type == 'simple_two_term':
                steps.append(f"  Expression: ({a} + {b})^{exponent}")
            elif word_problem_type == 'three_term_square':
                c = problem.metadata['c']
                steps.append(f"  Expression: ({a} + {b} + {c})^{exponent}")
            elif word_problem_type == 'higher_power':
                steps.append(f"  Expression: ({a} + {b})^{exponent}")

            steps.append("")
            steps.append("Step 2: Apply the correct order of operations")
        else:
            steps.append(f"Problem: Evaluate ({a} + {b})^{exponent}")

        steps.append("")
        steps.append("CORRECT METHOD: Parentheses first, then exponent")
        steps.append("")

        step_num = 1 if not is_word_problem else 3
        steps.append(f"Step {step_num}: Evaluate the sum inside parentheses")

        if 'c' in problem.metadata:
            c = problem.metadata['c']
            steps.append(f"  {a} + {b} + {c} = {sum_value}")
        else:
            steps.append(f"  {a} + {b} = {sum_value}")

        steps.append("")
        step_num += 1
        steps.append(f"Step {step_num}: Raise the result to the power")

        if 'c' in problem.metadata:
            c = problem.metadata['c']
            steps.append(f"  ({a} + {b} + {c})^{exponent} = {sum_value}^{exponent}")
        else:
            steps.append(f"  ({a} + {b})^{exponent} = {sum_value}^{exponent}")

        # Show expansion for small exponents
        if exponent == 2:
            steps.append(f"  = {sum_value} × {sum_value}")
            steps.append(f"  = {correct_answer}")
        elif exponent == 3:
            steps.append(f"  = {sum_value} × {sum_value} × {sum_value}")
            steps.append(f"  = {sum_value * sum_value} × {sum_value}")
            steps.append(f"  = {correct_answer}")
        else:
            steps.append(f"  = {correct_answer}")

        steps.append("")

        # Add note about binomial expansion for exponent 2
        if exponent == 2:
            steps.append("Note: Alternatively using binomial expansion:")
            steps.append(f"  ({a} + {b})² = ({a} + {b})({a} + {b})")
            steps.append(f"  = {a}² + 2({a})({b}) + {b}²")
            steps.append(f"  = {a**2} + {2*a*b} + {b**2}")
            steps.append(f"  = {correct_answer}")
            steps.append("")

        steps.append(f"Answer: {correct_answer}")
        steps.append("")
        steps.append(
            f"The key is following order of operations: parentheses BEFORE exponents. "
            f"We cannot distribute exponents over addition like we can with multiplication."
        )

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct exponent over sum algorithm.

        Args:
            problem: The exponent over sum problem
            verbose: If True, generate verbose steps with explanations.
                    If False (default), generate concise steps with only formulas and values.

        Returns:
            Solution showing correct order of operations
        """
        a = problem.metadata['a']
        b = problem.metadata['b']
        exponent = problem.metadata['exponent']

        # CALCULATE correct answer: (a+b)^n
        sum_value = a + b
        if problem.metadata.get('c') is not None:
            c = problem.metadata['c']
            sum_value = a + b + c
        correct_answer = sum_value ** exponent

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, correct_answer, sum_value)
        else:
            steps = self._generate_concise_steps(problem, correct_answer, sum_value)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
