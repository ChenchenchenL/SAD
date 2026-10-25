"""
Multiplication-Before-Division-Always malrule algorithm.

Implements the systematic error of believing multiplication must always
be performed before division, even when they appear left-to-right.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List

class MultiplicationBeforeDivisionAlwaysMalrule(Malrule):
    """
    Implements the Multiplication-Before-Division-Always bug.

    Students incorrectly believe that multiplication must ALWAYS be
    performed before division, misinterpreting PEMDAS as a strict
    sequence rather than understanding M and D have equal priority.

    Example: 6 ÷ 2 × 3 → 6 ÷ (2 × 3) = 6 ÷ 6 = 1 (WRONG! should be 9)

    This is a very common PEMDAS misconception.
    """

    def get_name(self) -> str:
        return "Multiplication-Before-Division-Always"

    def get_description(self) -> str:
        return (
            "Students incorrectly believe that multiplication must ALWAYS be "
            "performed before division. They interpret PEMDAS literally on a "
            "letter-by-letter basis, following the order of 'M' and 'D' to incorrectly "
            "believe that multiplication must be performed before division (Eaves et al., 2025). "
            "Example: 6 ÷ 2 × 3 becomes 6 ÷ 6 = 1 instead of 9."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Use metadata['malrule_answer'] if available (template-based)
        if 'malrule_answer' in problem.metadata and problem.metadata['malrule_answer'] is not None:
            return str(problem.metadata['malrule_answer'])

        # Backwards compatibility: calculate if not in metadata
        a = problem.metadata['a']
        b = problem.metadata['b']
        c = problem.metadata['c']

        # Malrule: do multiplication before division (INCORRECT)
        # a ÷ b × c becomes a ÷ (b × c)
        intermediate = b * c
        if intermediate != 0 and a % intermediate == 0:
            result = a // intermediate
        else:
            result = a / intermediate
            result = round(result, 2)

        return str(result)

    def generate_verbose_steps(self, problem: Problem, expression: str, template: str) -> tuple:
        """
        Generate verbose steps with full explanations.

        Args:
            problem: The problem instance
            expression: The mathematical expression
            template: The template type

        Returns:
            Tuple of (steps list, answer_str)
        """
        steps = []
        steps.append(f"Expression: {expression}")
        steps.append(f"MALRULE: In PEMDAS, M comes before D, so do multiplication first")

        # Handle multi-operation chain differently
        if template == 'multi_operation_chain':
            a = problem.metadata['a']
            d1 = problem.metadata['b']
            m = problem.metadata['c']
            d2 = problem.metadata['d']

            # Step 1: Multiplication first (WRONG!)
            intermediate = d1 * m
            steps.append(f"Step 1: {d1} × {m} = {intermediate}")
            steps.append(f"MALRULE REASONING: 'M before D' means multiplication always first")

            # Step 2: First division
            step1_mal = a // intermediate
            steps.append(f"Step 2: {a} ÷ {intermediate} = {step1_mal}")

            # Step 3: Second division
            result = step1_mal // d2
            steps.append(f"Step 3: {step1_mal} ÷ {d2} = {result}")
        else:
            # Standard a ÷ b × c format
            a = problem.metadata['a']
            b = problem.metadata['b']
            c = problem.metadata['c']

            # Step 1: Multiplication first (WRONG!)
            intermediate = b * c
            steps.append(f"Step 1: {b} × {c} = {intermediate}")
            steps.append(f"MALRULE REASONING: 'M before D' means multiplication always first")

            # Step 2: Division
            if intermediate != 0 and a % intermediate == 0:
                result = a // intermediate
                steps.append(f"Step 2: {a} ÷ {intermediate} = {result}")
            else:
                # Handle non-clean division
                result = a / intermediate
                steps.append(f"Step 2: {a} ÷ {intermediate} = {result:.2f}")
                result = round(result, 2)

        # Get the formatted answer from metadata if available
        if 'malrule_answer' in problem.metadata:
            answer_str = str(problem.metadata['malrule_answer'])
        else:
            answer_str = str(result)

        steps.append(f"\nFinal answer: {answer_str} (INCORRECT - did multiplication before division)")

        return steps, answer_str

    def generate_concise_steps(self, problem: Problem, expression: str, template: str) -> tuple:
        """
        Generate concise steps with only formulas and values.

        Args:
            problem: The problem instance
            expression: The mathematical expression
            template: The template type

        Returns:
            Tuple of (steps list, answer_str)
        """
        steps = []

        # Add question
        steps.append(problem.text)

        # Add formula extraction for word problems
        if template in ['word_problem_sharing', 'word_problem_measurement', 'word_problem_money']:
            steps.append(f"{expression}")

        # Handle multi-operation chain differently
        if template == 'multi_operation_chain':
            a = problem.metadata['a']
            d1 = problem.metadata['b']
            m = problem.metadata['c']
            d2 = problem.metadata['d']

            # Step 1: Multiplication first (WRONG!)
            intermediate = d1 * m
            steps.append(f"{d1} × {m} = {intermediate}")

            # Step 2: First division
            step1_mal = a // intermediate
            steps.append(f"{a} ÷ {intermediate} = {step1_mal}")

            # Step 3: Second division
            result = step1_mal // d2
            steps.append(f"{step1_mal} ÷ {d2} = {result}")
        else:
            # Standard a ÷ b × c format
            a = problem.metadata['a']
            b = problem.metadata['b']
            c = problem.metadata['c']

            # Step 1: Multiplication first (WRONG!)
            intermediate = b * c
            steps.append(f"{b} × {c} = {intermediate}")

            # Step 2: Division
            if intermediate != 0 and a % intermediate == 0:
                result = a // intermediate
                steps.append(f"{a} ÷ {intermediate} = {result}")
            else:
                # Handle non-clean division
                result = a / intermediate
                steps.append(f"{a} ÷ {intermediate} = {result:.2f}")
                result = round(result, 2)

        # Get the formatted answer from metadata if available
        if 'malrule_answer' in problem.metadata:
            answer_str = str(problem.metadata['malrule_answer'])
        else:
            answer_str = str(result)

        steps.append(answer_str)

        return steps, answer_str

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Multiplication-Before-Division-Always malrule.

        Args:
            problem: Order of operations problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with incorrect multiplication-first evaluation
        """
        expression = problem.metadata['expression']
        template = problem.metadata.get('template', 'basic_expression')

        # Use helper functions based on verbose flag
        if verbose:
            steps, answer_str = self.generate_verbose_steps(problem, expression, template)
        else:
            steps, answer_str = self.generate_concise_steps(problem, expression, template)

        return Solution(
            answer=answer_str,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
