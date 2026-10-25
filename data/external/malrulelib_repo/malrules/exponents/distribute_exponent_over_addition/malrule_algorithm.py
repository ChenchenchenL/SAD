"""
Malrule algorithm for Distribute-Exponent-Over-Addition.

Students incorrectly distribute exponents over addition: (a+b)^n = a^n + b^n
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import List

class DistributeExponentOverAdditionMalrule(Malrule):
    """Student incorrectly distributes exponents over addition."""

    def get_name(self):
        return "Distribute-Exponent-Over-Addition"

    def get_description(self):
        return (
            "Student incorrectly distributes exponents over addition: (a+b)^n = a^n + b^n. "
            "For example, (2+3)² = 2² + 3² = 13 instead of 5² = 25. This is identified in "
            "research as the 'assumption of distributivity of exponents' (Matz, 1982)."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        a = problem.metadata['a']
        b = problem.metadata['b']
        exponent = problem.metadata['exponent']
        # Malrule: Distribute exponent over addition (INCORRECT)
        # (a+b)^n becomes a^n + b^n
        # (a+b+c)^n becomes a^n + b^n + c^n
        result = a**exponent + b**exponent
        # Check if there's a third term
        if 'c' in problem.metadata:
            c = problem.metadata['c']
            result += c**exponent
        return result

    def _generate_concise_steps(self, problem: Problem, malrule_answer) -> List[str]:
        """Generate concise steps showing only formula and values."""
        a = problem.metadata['a']
        b = problem.metadata['b']
        exponent = problem.metadata['exponent']
        is_word_problem = problem.metadata.get('is_word_problem', False)
        word_problem_type = problem.metadata.get('word_problem_type', None)

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
            steps.append(f"({a} + {b} + {c})^{exponent} = {a}^{exponent} + {b}^{exponent} + {c}^{exponent}")
            steps.append(f"{a**exponent} + {b**exponent} + {c**exponent} = {malrule_answer}")
        else:
            steps.append(f"({a} + {b})^{exponent} = {a}^{exponent} + {b}^{exponent}")
            steps.append(f"{a**exponent} + {b**exponent} = {malrule_answer}")

        # Answer
        steps.append(f"{malrule_answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, malrule_answer) -> List[str]:
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
            steps.append("Step 2: Apply malrule (incorrectly distribute exponent)")
            steps.append("")
        else:
            if 'c' in problem.metadata:
                c = problem.metadata['c']
                steps.append(f"Problem: Evaluate ({a} + {b} + {c})^{exponent}")
            else:
                steps.append(f"Problem: Evaluate ({a} + {b})^{exponent}")

        steps.append("")
        steps.append("MALRULE: Distribute exponent over addition")

        if 'c' in problem.metadata:
            c = problem.metadata['c']
            steps.append(f"  ({a} + {b} + {c})^{exponent} = {a}^{exponent} + {b}^{exponent} + {c}^{exponent}")
            steps.append(f"  = {a**exponent} + {b**exponent} + {c**exponent}")
            steps.append(f"  = {malrule_answer}")
        else:
            steps.append(f"  ({a} + {b})^{exponent} = {a}^{exponent} + {b}^{exponent}")
            steps.append(f"  = {a**exponent} + {b**exponent}")
            steps.append(f"  = {malrule_answer}")

        steps.append("")
        steps.append(f"Student's answer: {malrule_answer}")
        steps.append("")
        steps.append(
            f"The student incorrectly distributed the exponent over the addition, "
            f"treating it like the distributive property for multiplication. "
            f"They don't understand that (a+b)^n requires full binomial expansion, "
            f"not simple distribution."
        )

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the distribute-exponent-over-addition malrule.

        Args:
            problem: The exponent over sum problem
            verbose: If True, generate verbose steps with explanations.
                    If False (default), generate concise steps with only formulas and values.

        Returns:
            Solution showing incorrect distribution
        """
        # CALCULATE malrule answer
        malrule_answer = self.calculate_expected_answer(problem)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, malrule_answer)
        else:
            steps = self._generate_concise_steps(problem, malrule_answer)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
