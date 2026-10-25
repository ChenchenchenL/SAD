"""
Negative-Outside-Same-As-Inside malrule algorithm.

Implements the systematic error where students confuse -√n with √-n.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List
import math

class NegativeOutsideSameAsInsideMalrule(Malrule):
    """
    Implements the Negative-Outside-Same-As-Inside bug.

    Students confuse -√n (negative outside) with √-n (negative inside),
    incorrectly claiming -√n has no real solution.
    """

    def get_name(self) -> str:
        return "Negative-Outside-Same-As-Inside"

    def get_description(self) -> str:
        return (
            "Students confuse -√n with √-n, failing to recognize that the domain "
            "of the radical function is restricted to nonnegative real numbers. "
            "They incorrectly believe that -√4 has no real solution because they "
            "treat the negative sign outside the radical as if it were inside. "
            "Research shows students are 'not aware that the domain of radical "
            "function is nonnegative real numbers' (Özkan, 2011), leading them "
            "to misinterpret valid expressions as undefined."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Malrule: Student always thinks "No real solution" because they confuse -√n with √-n
        return 'No real solution'

    def _generate_concise_steps(self, problem: Problem, template: str, **kwargs) -> list:
        """Generate concise steps for the malrule solution."""
        radicand = kwargs['radicand']
        malrule_answer = kwargs['malrule_answer']

        steps = [f"Question: {problem.text}"]

        # Extract formula for word problems
        if template in ['word_problem', 'word_problem_diverse', 'word_problem_combined_ops']:
            steps.append(f"Formula: -√{radicand}")

        # Student's incorrect reasoning
        steps.append(f"-√{radicand} = √(-{radicand})")
        steps.append(f"√(-{radicand}) = undefined")

        steps.append(f"Answer: {malrule_answer}")
        return steps

    def _generate_verbose_steps(self, problem: Problem, template: str, **kwargs) -> list:
        """Generate verbose steps for the malrule solution."""
        radicand = kwargs['radicand']
        malrule_answer = kwargs['malrule_answer']

        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: Confuse -√n with √-n")
        steps.append("")

        # Student incorrectly thinks negative sign is inside radical
        steps.append(f"Student thinks: -√{radicand} means √(-{radicand})")
        steps.append(f"This would be the square root of a negative number")
        steps.append(f"√(-{radicand}) has no real solution")
        steps.append("")
        steps.append(f"Student's answer: {malrule_answer}")
        steps.append("")
        steps.append(
            "The student confused the placement of the negative sign. "
            "The negative is OUTSIDE the radical, not inside it."
        )

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply the Negative-Outside-Same-As-Inside malrule."""
        template = problem.metadata.get('template', 'basic_negative_outside')
        radicand = problem.metadata.get('radicand', problem.operands[0])

        # COMPUTE malrule answer: always "No real solution" for this misconception
        malrule_answer = 'No real solution'

        # Build step_kwargs dictionary with all values needed for step generation
        step_kwargs = {
            'radicand': radicand,
            'malrule_answer': malrule_answer,
        }

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, template, **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, template, **step_kwargs)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
