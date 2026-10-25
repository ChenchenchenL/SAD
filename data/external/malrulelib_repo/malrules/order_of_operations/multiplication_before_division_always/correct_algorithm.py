"""
Correct order of operations algorithm.

Implements proper order of operations where multiplication and division
have equal priority and are evaluated left-to-right.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import CorrectAlgorithm, Problem, Solution


class OrderOfOperationsCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for order of operations.

    Follows proper PEMDAS/BODMAS rules where multiplication and division
    have equal priority and are evaluated left-to-right.
    """

    def get_name(self) -> str:
        return "Correct Order of Operations"

    def get_description(self) -> str:
        return (
            "Evaluates expressions correctly following PEMDAS/BODMAS. "
            "Multiplication and division have equal priority and are "
            "evaluated left-to-right. Example: 6 ÷ 2 × 3 = 3 × 3 = 9"
        )

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
        steps.append(f"Rule: Multiplication and division have equal priority")
        steps.append(f"Evaluate left-to-right")

        # Handle multi-operation chain differently
        if template == 'multi_operation_chain':
            a = problem.metadata['a']
            d1 = problem.metadata['b']
            m = problem.metadata['c']
            d2 = problem.metadata['d']

            # Step 1: First division (leftmost)
            step1 = a // d1
            steps.append(f"Step 1: {a} ÷ {d1} = {step1}")

            # Step 2: Multiplication
            step2 = step1 * m
            steps.append(f"Step 2: {step1} × {m} = {step2}")

            # Step 3: Second division
            result = step2 // d2
            steps.append(f"Step 3: {step2} ÷ {d2} = {result}")
        else:
            # Standard a ÷ b × c format
            a = problem.metadata['a']
            b = problem.metadata['b']
            c = problem.metadata['c']

            # Step 1: Division first (it's on the left)
            intermediate = a // b
            steps.append(f"Step 1: {a} ÷ {b} = {intermediate}")

            # Step 2: Multiplication
            result = intermediate * c
            steps.append(f"Step 2: {intermediate} × {c} = {result}")

        # Format answer with units if applicable
        if template == 'word_problem_money':
            answer_str = f"${result}"
        elif template == 'word_problem_measurement':
            unit = problem.metadata.get('unit', '')
            answer_str = f"{result} {unit}"
        else:
            answer_str = str(result)

        steps.append(f"\nFinal answer: {answer_str}")

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

            # Step 1: First division (leftmost)
            step1 = a // d1
            steps.append(f"{a} ÷ {d1} = {step1}")

            # Step 2: Multiplication
            step2 = step1 * m
            steps.append(f"{step1} × {m} = {step2}")

            # Step 3: Second division
            result = step2 // d2
            steps.append(f"{step2} ÷ {d2} = {result}")
        else:
            # Standard a ÷ b × c format
            a = problem.metadata['a']
            b = problem.metadata['b']
            c = problem.metadata['c']

            # Step 1: Division first (it's on the left)
            intermediate = a // b
            steps.append(f"{a} ÷ {b} = {intermediate}")

            # Step 2: Multiplication
            result = intermediate * c
            steps.append(f"{intermediate} × {c} = {result}")

        # Format answer with units if applicable
        if template == 'word_problem_money':
            answer_str = f"${result}"
        elif template == 'word_problem_measurement':
            unit = problem.metadata.get('unit', '')
            answer_str = f"{result} {unit}"
        else:
            answer_str = str(result)

        steps.append(answer_str)

        return steps, answer_str

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct order of operations.

        Args:
            problem: Order of operations problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with correct evaluation
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
            is_correct=True,
            algorithm_name=self.get_name()
        )
