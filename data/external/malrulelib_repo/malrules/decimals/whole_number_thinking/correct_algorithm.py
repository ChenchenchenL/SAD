"""
Correct decimal algorithm.

Implements proper decimal operations with place value understanding.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class DecimalCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for decimal operations.

    Uses proper place value understanding for all decimal operations.
    """

    def get_name(self) -> str:
        return "Correct Decimal Algorithm"

    def get_description(self) -> str:
        return (
            "Performs decimal operations correctly using place value. "
            "Understands that the decimal point separates whole numbers from "
            "fractional parts (tenths, hundredths, etc.)."
        )

    def _generate_verbose_steps_addition(self, decimal1: float, decimal2: float,
                                          correct_answer: str) -> List[str]:
        """Generate verbose steps for addition."""
        steps = []
        steps.append(f"Problem: {decimal1} + {decimal2}")
        steps.append(f"Method: Line up decimal points and add")
        steps.append(f"")
        steps.append(f"  {decimal1:>6}")
        steps.append(f"+ {decimal2:>6}")
        steps.append(f"  ------")
        steps.append(f"  {correct_answer:>6}")
        steps.append(f"")
        steps.append(f"Answer: {correct_answer}")
        return steps

    def _generate_concise_steps_addition(self, decimal1: float, decimal2: float,
                                          correct_answer: str) -> List[str]:
        """Generate concise steps for addition."""
        return [
            f"Problem: {decimal1} + {decimal2}",
            f"{decimal1} + {decimal2}",
            f"= {correct_answer}",
            correct_answer
        ]

    def _generate_verbose_steps_comparison(self, decimal1: float, decimal2: float,
                                            correct_answer: str) -> List[str]:
        """Generate verbose steps for comparison."""
        steps = []
        steps.append(f"Problem: Which is larger: {decimal1} or {decimal2}?")
        steps.append(f"Method: Compare by place value")

        if decimal1 > decimal2:
            steps.append(f"Since {decimal1} > {decimal2}, the answer is {decimal1}")
            steps.append(f"")
            steps.append(f"Place value explanation:")
            steps.append(f"  {decimal1} is greater than {decimal2}")
        elif decimal1 < decimal2:
            steps.append(f"Since {decimal1} < {decimal2}, the answer is {decimal2}")
            steps.append(f"")
            steps.append(f"Place value explanation:")
            steps.append(f"  {decimal2} is greater than {decimal1}")
        else:
            steps.append(f"The decimals are equal: {decimal1} = {decimal2}")

        steps.append(f"")
        steps.append(f"Answer: {correct_answer}")
        return steps

    def _generate_concise_steps_comparison(self, decimal1: float, decimal2: float,
                                            correct_answer: str) -> List[str]:
        """Generate concise steps for comparison."""
        steps = [f"Problem: Which is larger: {decimal1} or {decimal2}?"]
        steps.append(f"{decimal1} vs {decimal2}")
        if decimal1 > decimal2:
            steps.append(f"{decimal1} > {decimal2}")
        elif decimal1 < decimal2:
            steps.append(f"{decimal2} > {decimal1}")
        else:
            steps.append(f"{decimal1} = {decimal2}")
        steps.append(correct_answer)
        return steps

    def _generate_verbose_steps_subtraction(self, decimal1: float, decimal2: float,
                                             correct_answer: str) -> List[str]:
        """Generate verbose steps for subtraction."""
        steps = []
        steps.append(f"Problem: {decimal1} - {decimal2}")
        steps.append(f"Method: Line up decimal points and subtract")
        steps.append(f"")
        steps.append(f"  {decimal1:>6}")
        steps.append(f"- {decimal2:>6}")
        steps.append(f"  ------")
        steps.append(f"  {correct_answer:>6}")
        steps.append(f"")
        steps.append(f"Answer: {correct_answer}")
        return steps

    def _generate_concise_steps_subtraction(self, decimal1: float, decimal2: float,
                                             correct_answer: str) -> List[str]:
        """Generate concise steps for subtraction."""
        return [
            f"Problem: {decimal1} - {decimal2}",
            f"{decimal1} - {decimal2}",
            f"= {correct_answer}",
            correct_answer
        ]

    def _generate_verbose_steps_multiplication(self, decimal1: float, multiplier,
                                                correct_answer: str) -> List[str]:
        """Generate verbose steps for multiplication."""
        steps = []
        steps.append(f"Problem: {decimal1} × {multiplier}")
        steps.append(f"Method: Multiply and count decimal places")
        steps.append(f"")
        steps.append(f"Step 1: {decimal1} has 1 decimal place")
        steps.append(f"Step 2: Multiply: {decimal1} × {multiplier} = {correct_answer}")
        steps.append(f"Step 3: Result has decimal places")
        steps.append(f"")
        steps.append(f"Answer: {correct_answer}")
        return steps

    def _generate_concise_steps_multiplication(self, decimal1: float, multiplier,
                                                correct_answer: str) -> List[str]:
        """Generate concise steps for multiplication."""
        return [
            f"Problem: {decimal1} × {multiplier}",
            f"{decimal1} × {multiplier}",
            f"= {correct_answer}",
            correct_answer
        ]

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct decimal algorithm based on template.

        Args:
            problem: Problem instance
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with correct reasoning
        """
        template = problem.metadata.get('template', 'unknown')

        if template == 'basic_addition':
            return self._apply_addition_correct(problem, verbose)
        elif template == 'basic_comparison':
            return self._apply_comparison_correct(problem, verbose)
        elif template == 'subtraction':
            return self._apply_subtraction_correct(problem, verbose)
        elif template == 'multiplication':
            return self._apply_multiplication_correct(problem, verbose)
        elif template == 'word_problem':
            return self._apply_word_problem_correct(problem, verbose)
        elif template == 'word_problem_context':
            return self._apply_word_problem_context_correct(problem, verbose)
        else:
            # Fallback for unknown templates
            return Solution(
                answer=problem.metadata.get('correct_answer', 'unknown'),
                steps=["Unknown template type"],
                is_correct=True,
                algorithm_name=self.get_name()
            )

    def _apply_addition_correct(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply correct algorithm for addition problems."""
        decimal1 = problem.metadata['decimal1']
        decimal2 = problem.metadata['decimal2']

        # Calculate correct answer (NOT from metadata)
        correct_answer = round(decimal1 + decimal2, 2)

        if verbose:
            steps = self._generate_verbose_steps_addition(decimal1, decimal2, str(correct_answer))
        else:
            steps = self._generate_concise_steps_addition(decimal1, decimal2, str(correct_answer))

        return Solution(
            answer=str(correct_answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _apply_comparison_correct(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply correct algorithm for comparison problems."""
        decimal1 = problem.metadata['decimal1']
        decimal2 = problem.metadata['decimal2']

        # Calculate correct answer (NOT from metadata)
        correct_answer = str(max(decimal1, decimal2))

        if verbose:
            steps = self._generate_verbose_steps_comparison(decimal1, decimal2, correct_answer)
        else:
            steps = self._generate_concise_steps_comparison(decimal1, decimal2, correct_answer)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _apply_subtraction_correct(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply correct algorithm for subtraction problems."""
        decimal1 = problem.metadata['decimal1']
        decimal2 = problem.metadata['decimal2']

        # Calculate correct answer (NOT from metadata)
        correct_answer = round(decimal1 - decimal2, 2)

        if verbose:
            steps = self._generate_verbose_steps_subtraction(decimal1, decimal2, str(correct_answer))
        else:
            steps = self._generate_concise_steps_subtraction(decimal1, decimal2, str(correct_answer))

        return Solution(
            answer=str(correct_answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _apply_multiplication_correct(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply correct algorithm for multiplication problems."""
        decimal1 = problem.metadata['decimal1']
        multiplier = problem.metadata.get('multiplier', problem.metadata.get('decimal2', 1))

        # Calculate correct answer (NOT from metadata)
        correct_answer = round(decimal1 * multiplier, 2)

        if verbose:
            steps = self._generate_verbose_steps_multiplication(decimal1, multiplier, str(correct_answer))
        else:
            steps = self._generate_concise_steps_multiplication(decimal1, multiplier, str(correct_answer))

        return Solution(
            answer=str(correct_answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _apply_word_problem_correct(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply correct algorithm for word problems."""
        operation_type = problem.metadata['operation_type']

        steps = []

        if operation_type == 'addition':
            decimal1 = problem.operands[0]
            decimal2 = problem.operands[1]
            correct_answer = str(round(decimal1 + decimal2, 2))
            if verbose:
                steps.append(f"Problem: {problem.text}")
                steps.append(f"")
                steps.append(f"Identify the operation: Addition")
                steps.append(f"Set up: {decimal1} + {decimal2}")
                steps.append(f"Line up decimal points and add")
                steps.append(f"Result: {correct_answer}")
            else:
                steps.append(f"Problem: {problem.text}")
                steps.append(f"Equation: {decimal1} + {decimal2}")
                steps.append(f"= {correct_answer}")
                steps.append(correct_answer)

        elif operation_type == 'subtraction':
            decimal1 = problem.operands[0]
            decimal2 = problem.operands[1]
            correct_answer = str(round(decimal1 - decimal2, 2))
            if verbose:
                steps.append(f"Problem: {problem.text}")
                steps.append(f"")
                steps.append(f"Identify the operation: Subtraction")
                steps.append(f"Set up: {decimal1} - {decimal2}")
                steps.append(f"Line up decimal points and subtract")
                steps.append(f"Result: {correct_answer}")
            else:
                steps.append(f"Problem: {problem.text}")
                steps.append(f"Equation: {decimal1} - {decimal2}")
                steps.append(f"= {correct_answer}")
                steps.append(correct_answer)

        elif operation_type == 'comparison':
            decimal1 = problem.operands[0]
            decimal2 = problem.operands[1]
            correct_answer = str(max(decimal1, decimal2))
            if verbose:
                steps.append(f"Problem: {problem.text}")
                steps.append(f"")
                steps.append(f"Identify the operation: Comparison")
                steps.append(f"Compare: {decimal1} vs {decimal2}")
                steps.append(f"Using place value: {correct_answer} is the answer")
            else:
                steps.append(f"Problem: {problem.text}")
                steps.append(f"Compare: {decimal1} vs {decimal2}")
                steps.append(f"max = {correct_answer}")
                steps.append(correct_answer)

        else:
            correct_answer = str(problem.operands[0])
            steps.append(f"Problem: {problem.text}")
            steps.append(correct_answer)

        if verbose:
            steps.append(f"")
            steps.append(f"Answer: {correct_answer}")

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _apply_word_problem_context_correct(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply correct algorithm for word_problem_context template."""
        word_problem_type = problem.metadata.get('word_problem_type', 'comparison')
        decimal1 = problem.metadata.get('decimal1')
        decimal2 = problem.metadata.get('decimal2')

        # Calculate correct answer (NOT from metadata)
        if word_problem_type == 'comparison':
            correct_answer = str(max(decimal1, decimal2))
        elif word_problem_type == 'addition':
            correct_answer = str(round(decimal1 + decimal2, 2))
        elif word_problem_type == 'subtraction':
            correct_answer = str(round(decimal1 - decimal2, 2))
        elif word_problem_type == 'multiplication':
            correct_answer = str(round(decimal1 * decimal2, 2))
        else:
            correct_answer = str(decimal1)

        steps = []

        if verbose:
            steps.append(f"Word Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Extract the equation from the word problem")

            if word_problem_type == 'comparison':
                steps.append(f"  Compare: {decimal1} vs {decimal2}")
            elif word_problem_type == 'addition':
                steps.append(f"  Equation: {decimal1} + {decimal2}")
            elif word_problem_type == 'subtraction':
                steps.append(f"  Equation: {decimal1} - {decimal2}")
            elif word_problem_type == 'multiplication':
                steps.append(f"  Equation: {decimal1} × {decimal2}")

            steps.append("")
            steps.append("Step 2: Solve correctly using decimal place value")
            steps.append("")
            steps.append("CORRECT METHOD: Respect decimal point and place value")
            steps.append(f"  Decimal points matter! {decimal1} and {decimal2} are NOT whole numbers")

            if word_problem_type == 'comparison':
                steps.append(f"  Compare by place value: {correct_answer} is larger")
            elif word_problem_type == 'addition':
                steps.append(f"  Line up decimal points and add: {correct_answer}")
            elif word_problem_type == 'subtraction':
                steps.append(f"  Line up decimal points and subtract: {correct_answer}")
            elif word_problem_type == 'multiplication':
                steps.append(f"  Multiply and place decimal correctly: {correct_answer}")

            steps.append("")
            steps.append(f"Answer: {correct_answer} ✓")
        else:
            steps.append(f"Problem: {problem.text}")
            if word_problem_type == 'comparison':
                steps.append(f"Compare: {decimal1} vs {decimal2}")
                steps.append(f"max = {correct_answer}")
            elif word_problem_type == 'addition':
                steps.append(f"{decimal1} + {decimal2}")
                steps.append(f"= {correct_answer}")
            elif word_problem_type == 'subtraction':
                steps.append(f"{decimal1} - {decimal2}")
                steps.append(f"= {correct_answer}")
            elif word_problem_type == 'multiplication':
                steps.append(f"{decimal1} × {decimal2}")
                steps.append(f"= {correct_answer}")
            steps.append(correct_answer)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
