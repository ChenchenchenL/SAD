"""
Malrule algorithm for Ignore-Decimal-Point error.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class IgnoreDecimalPointMalrule(Malrule):
    """
    Students ignore the decimal point and treat numbers as whole numbers.

    Example: 3.5 + 2.3 → Student sees 35 + 23 = 58
    """

    def get_name(self) -> str:
        return "Ignore-Decimal-Point"

    def get_description(self) -> str:
        return (
            "Students ignore the decimal point and treat decimal numbers as whole numbers, "
            "applying whole number arithmetic procedures without regard to place value. "
            "This error stems from students computing by relying solely on syntax-based rules "
            "where semantic knowledge has no effect on performance (Hiebert & Wearne, 1985)."
        )

    def calculate_expected_answer(self, problem: Problem):
        """
        Calculate the expected incorrect answer for this malrule.

        For Ignore-Decimal-Point:
        - Remove decimal points from both numbers
        - Treat them as integers
        - Perform the operation as whole number arithmetic

        Args:
            problem: Decimal arithmetic problem

        Returns:
            Expected incorrect answer as string
        """
        num1 = problem.metadata['num1']
        num2 = problem.metadata['num2']
        operation = problem.metadata['operation']

        # Convert to integers by removing decimal point
        num1_as_int = int(str(num1).replace('.', ''))
        num2_as_int = int(str(num2).replace('.', ''))

        # Perform operation on integers (MALRULE)
        if operation == 'addition':
            result = num1_as_int + num2_as_int
        elif operation == 'subtraction':
            result = num1_as_int - num2_as_int
        elif operation == 'multiplication':
            result = num1_as_int * num2_as_int
        elif operation == 'division':
            # Division: treat as integer division
            result = num1_as_int // num2_as_int if num2_as_int != 0 else num1_as_int
        else:
            result = num1_as_int * num2_as_int

        return str(result)

    def _generate_verbose_steps(self, problem: Problem, num1: float, num2: float,
                                 operator: str, operation: str, malrule_answer: str,
                                 num1_as_int: int, num2_as_int: int,
                                 is_word_problem: bool, word_problem_type: str) -> List[str]:
        """Generate verbose, explanatory steps."""
        steps = []

        # For word problems, show extraction step
        if is_word_problem:
            steps.append(f"Word Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Extract the equation from the word problem")
            steps.append(f"  Equation: {num1} {operator} {num2}")
            steps.append("")
            steps.append("Step 2: Apply malrule (ignore decimal point)")
            steps.append("")
        else:
            steps.append(f"Problem: {problem.text}")
            steps.append("")

        steps.append("MALRULE: Ignore the decimal point")
        steps.append(f"  MALRULE REASONING: 'Just remove the dots and work with the numbers'")
        steps.append("")

        steps.append(f"Convert {num1} → {num1_as_int} (remove decimal)")
        steps.append(f"Convert {num2} → {num2_as_int} (remove decimal)")
        steps.append("")

        if operation == 'addition':
            steps.append(f"Calculate: {num1_as_int} + {num2_as_int} = {malrule_answer}")
        elif operation == 'subtraction':
            steps.append(f"Calculate: {num1_as_int} - {num2_as_int} = {malrule_answer}")
        elif operation == 'division':
            steps.append(f"Calculate: {num1_as_int} ÷ {num2_as_int} = {malrule_answer}")
        else:  # multiplication
            steps.append(f"Calculate: {num1_as_int} × {num2_as_int} = {malrule_answer}")

        steps.append("")
        steps.append(f"Final Answer: {malrule_answer} (INCORRECT - ignored decimal point!)")

        return steps

    def _generate_concise_steps(self, problem: Problem, num1: float, num2: float,
                                 operator: str, operation: str, malrule_answer: str,
                                 num1_as_int: int, num2_as_int: int,
                                 is_word_problem: bool, word_problem_type: str) -> List[str]:
        """Generate concise steps with just formulas and values."""
        steps = [f"Problem: {problem.text}"]

        # For word problems, show extraction step
        if is_word_problem:
            steps.append(f"Equation: {num1} {operator} {num2}")

        steps.append(f"{num1} → {num1_as_int}, {num2} → {num2_as_int}")

        if operation == 'addition':
            steps.append(f"{num1_as_int} + {num2_as_int} = {malrule_answer}")
        elif operation == 'subtraction':
            steps.append(f"{num1_as_int} - {num2_as_int} = {malrule_answer}")
        elif operation == 'division':
            steps.append(f"{num1_as_int} ÷ {num2_as_int} = {malrule_answer}")
        else:  # multiplication
            steps.append(f"{num1_as_int} × {num2_as_int} = {malrule_answer}")

        steps.append(malrule_answer)

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the malrule to solve the problem incorrectly.

        Args:
            problem: The decimal arithmetic problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with incorrect answer (ignoring decimal point)
        """
        # Check if this is a word problem
        is_word_problem = problem.metadata.get('is_word_problem', False)
        word_problem_type = problem.metadata.get('word_problem_type', None)

        num1 = problem.metadata['num1']
        num2 = problem.metadata['num2']
        operator = problem.metadata['operator']
        operation = problem.metadata['operation']

        # Calculate malrule answer (NOT from metadata)
        num1_as_int = int(str(num1).replace('.', ''))
        num2_as_int = int(str(num2).replace('.', ''))

        if operation == 'multiplication':
            malrule_answer = str(num1_as_int * num2_as_int)
        elif operation == 'division':
            malrule_answer = str(num1_as_int // num2_as_int if num2_as_int != 0 else num1_as_int)
        elif operation == 'addition':
            malrule_answer = str(num1_as_int + num2_as_int)
        elif operation == 'subtraction':
            malrule_answer = str(num1_as_int - num2_as_int)
        else:
            malrule_answer = str(num1_as_int * num2_as_int)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, num1, num2, operator, operation,
                                                  malrule_answer, num1_as_int, num2_as_int,
                                                  is_word_problem, word_problem_type)
        else:
            steps = self._generate_concise_steps(problem, num1, num2, operator, operation,
                                                  malrule_answer, num1_as_int, num2_as_int,
                                                  is_word_problem, word_problem_type)

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
