"""
Whole-Number-Thinking malrule algorithm for decimals.

Implements the systematic error of treating decimals like whole numbers
by ignoring the decimal point in various operations.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List

class WholeNumberThinkingMalrule(Malrule):
    """
    Implements the Whole-Number-Thinking bug for decimals.

    Students incorrectly treat decimals like whole numbers by ignoring
    the decimal point in operations.

    Examples:
    - Addition: 3.7 + 2.5 treated as 37 + 25 = 62
    - Comparison: 0.45 > 0.8 because 45 > 8
    - Subtraction: 5.8 - 2.3 treated as 58 - 23 = 35
    - Multiplication: 2.5 × 3 treated as 25 × 3 = 75

    This is a very common and fundamental misconception about decimals.
    """

    def get_name(self) -> str:
        return "Whole-Number-Thinking"

    def get_description(self) -> str:
        return (
            "Students incorrectly treat decimals as if they demonstrate the properties "
            "of whole numbers. This fundamental misconception, termed the 'Whole Number "
            "rule' by Resnick et al. (1989), leads to errors such as thinking 0.25 is "
            "greater than 0.7 because 25 > 7, or computing 3.7 + 2.5 = 62 by treating "
            "the numbers as 37 + 25."
        )

    def calculate_expected_answer(self, problem: Problem):
        """
        Calculate the expected incorrect answer for this malrule.

        Calculates the malrule answer by removing decimal points and
        treating numbers as whole numbers.

        Args:
            problem: Problem instance

        Returns:
            Expected incorrect answer as string
        """
        # Get template to determine how to calculate
        template = problem.metadata.get('template', 'unknown')
        decimal1 = problem.metadata.get('decimal1')
        decimal2 = problem.metadata.get('decimal2')

        # If decimal1 and decimal2 are not in metadata, try to get from operands
        if decimal1 is None and len(problem.operands) > 0:
            decimal1 = problem.operands[0]
        if decimal2 is None and len(problem.operands) > 1:
            decimal2 = problem.operands[1]

        # Remove decimal points to treat as whole numbers
        num1 = int(str(decimal1).replace('.', '')) if decimal1 is not None else 0
        num2 = int(str(decimal2).replace('.', '')) if decimal2 is not None else 0

        # Handle based on template
        if template == 'basic_addition' or (template == 'word_problem_context' and problem.metadata.get('word_problem_type') == 'addition'):
            return str(num1 + num2)
        elif template == 'basic_comparison' or (template == 'word_problem_context' and problem.metadata.get('word_problem_type') == 'comparison'):
            # Compare decimal parts as whole numbers
            str1 = str(decimal1)
            str2 = str(decimal2)
            if '.' in str1:
                decimal_part1 = str1.split('.')[1]
                num1 = int(decimal_part1) if decimal_part1 else 0
            else:
                num1 = 0
            if '.' in str2:
                decimal_part2 = str2.split('.')[1]
                num2 = int(decimal_part2) if decimal_part2 else 0
            else:
                num2 = 0
            return str(decimal1 if num1 > num2 else decimal2)
        elif template == 'subtraction' or (template == 'word_problem_context' and problem.metadata.get('word_problem_type') == 'subtraction'):
            return str(num1 - num2)
        elif template == 'multiplication' or (template == 'word_problem_context' and problem.metadata.get('word_problem_type') == 'multiplication'):
            multiplier = problem.metadata.get('multiplier', decimal2)
            num1 = int(str(decimal1).replace('.', ''))
            # If multiplier is also a decimal, convert it too
            if isinstance(multiplier, float):
                num2 = int(str(multiplier).replace('.', ''))
            else:
                num2 = multiplier
            return str(num1 * num2)
        elif template == 'word_problem':
            # Handle word_problem template
            operation_type = problem.metadata.get('operation_type')
            if operation_type == 'addition':
                return str(num1 + num2)
            elif operation_type == 'subtraction':
                return str(num1 - num2)
            elif operation_type == 'comparison':
                # Compare decimal parts as whole numbers
                str1 = str(decimal1)
                str2 = str(decimal2)
                if '.' in str1:
                    decimal_part1 = str1.split('.')[1]
                    num1 = int(decimal_part1) if decimal_part1 else 0
                else:
                    num1 = 0
                if '.' in str2:
                    decimal_part2 = str2.split('.')[1]
                    num2 = int(decimal_part2) if decimal_part2 else 0
                else:
                    num2 = 0
                return str(decimal1 if num1 > num2 else decimal2)
            else:
                return str(num1)
        else:
            return str(num1)

    def _generate_verbose_steps_addition(self, decimal1: float, decimal2: float,
                                          num1: int, num2: int, malrule_answer: str) -> List[str]:
        """Generate verbose steps for addition."""
        steps = []
        steps.append(f"Problem: {decimal1} + {decimal2}")
        steps.append(f"MALRULE: Ignore the decimal point and treat as whole numbers")
        steps.append(f"Convert {decimal1} → {num1} (remove decimal point)")
        steps.append(f"Convert {decimal2} → {num2} (remove decimal point)")
        steps.append(f"Add as whole numbers: {num1} + {num2} = {malrule_answer}")
        steps.append(f"(INCORRECT - ignored the decimal point)")
        return steps

    def _generate_concise_steps_addition(self, decimal1: float, decimal2: float,
                                          num1: int, num2: int, malrule_answer: str) -> List[str]:
        """Generate concise steps for addition."""
        return [
            f"Problem: {decimal1} + {decimal2}",
            f"{decimal1} → {num1}, {decimal2} → {num2}",
            f"{num1} + {num2} = {malrule_answer}",
            malrule_answer
        ]

    def _generate_verbose_steps_comparison(self, decimal1: float, decimal2: float,
                                            num1: int, num2: int, malrule_answer: str) -> List[str]:
        """Generate verbose steps for comparison."""
        steps = []
        steps.append(f"Problem: Which is larger: {decimal1} or {decimal2}?")
        steps.append(f"MALRULE: Compare the decimal parts as whole numbers")
        steps.append(f"Extract decimal parts: {decimal1} → {num1}, {decimal2} → {num2}")
        steps.append(f"Compare as whole numbers: {num1} vs {num2}")

        if num1 > num2:
            steps.append(f"Since {num1} > {num2}, conclude {decimal1} is larger")
        elif num1 < num2:
            steps.append(f"Since {num1} < {num2}, conclude {decimal2} is larger")
        else:
            steps.append(f"Since {num1} = {num2}, conclude they are equal")

        steps.append(f"Answer: {malrule_answer}")
        steps.append(f"(INCORRECT - compared decimal parts as whole numbers)")
        return steps

    def _generate_concise_steps_comparison(self, decimal1: float, decimal2: float,
                                            num1: int, num2: int, malrule_answer: str) -> List[str]:
        """Generate concise steps for comparison."""
        steps = [f"Problem: Which is larger: {decimal1} or {decimal2}?"]
        steps.append(f"Decimal parts: {num1} vs {num2}")
        if num1 > num2:
            steps.append(f"{num1} > {num2}")
        elif num1 < num2:
            steps.append(f"{num1} < {num2}")
        else:
            steps.append(f"{num1} = {num2}")
        steps.append(malrule_answer)
        return steps

    def _generate_verbose_steps_subtraction(self, decimal1: float, decimal2: float,
                                             num1: int, num2: int, malrule_answer: str) -> List[str]:
        """Generate verbose steps for subtraction."""
        steps = []
        steps.append(f"Problem: {decimal1} - {decimal2}")
        steps.append(f"MALRULE: Ignore the decimal point and treat as whole numbers")
        steps.append(f"Convert {decimal1} → {num1} (remove decimal point)")
        steps.append(f"Convert {decimal2} → {num2} (remove decimal point)")
        steps.append(f"Subtract as whole numbers: {num1} - {num2} = {malrule_answer}")
        steps.append(f"(INCORRECT - ignored the decimal point)")
        return steps

    def _generate_concise_steps_subtraction(self, decimal1: float, decimal2: float,
                                             num1: int, num2: int, malrule_answer: str) -> List[str]:
        """Generate concise steps for subtraction."""
        return [
            f"Problem: {decimal1} - {decimal2}",
            f"{decimal1} → {num1}, {decimal2} → {num2}",
            f"{num1} - {num2} = {malrule_answer}",
            malrule_answer
        ]

    def _generate_verbose_steps_multiplication(self, decimal1: float, multiplier,
                                                num1: int, num2, malrule_answer: str) -> List[str]:
        """Generate verbose steps for multiplication."""
        steps = []
        steps.append(f"Problem: {decimal1} × {multiplier}")
        steps.append(f"MALRULE: Ignore the decimal point and treat as whole number")
        steps.append(f"Convert {decimal1} → {num1} (remove decimal point)")
        steps.append(f"Multiply as whole numbers: {num1} × {num2} = {malrule_answer}")
        steps.append(f"(INCORRECT - ignored the decimal point)")
        return steps

    def _generate_concise_steps_multiplication(self, decimal1: float, multiplier,
                                                num1: int, num2, malrule_answer: str) -> List[str]:
        """Generate concise steps for multiplication."""
        return [
            f"Problem: {decimal1} × {multiplier}",
            f"{decimal1} → {num1}",
            f"{num1} × {num2} = {malrule_answer}",
            malrule_answer
        ]

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Whole-Number-Thinking malrule based on template.

        Args:
            problem: Problem instance
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with incorrect whole-number reasoning
        """
        template = problem.metadata.get('template', 'unknown')

        if template == 'basic_addition':
            return self._apply_addition_malrule(problem, verbose)
        elif template == 'basic_comparison':
            return self._apply_comparison_malrule(problem, verbose)
        elif template == 'subtraction':
            return self._apply_subtraction_malrule(problem, verbose)
        elif template == 'multiplication':
            return self._apply_multiplication_malrule(problem, verbose)
        elif template == 'word_problem':
            return self._apply_word_problem_malrule(problem, verbose)
        elif template == 'word_problem_context':
            return self._apply_word_problem_context_malrule(problem, verbose)
        else:
            # Fallback for unknown templates
            return Solution(
                answer=problem.metadata.get('malrule_answer', 'unknown'),
                steps=["Unknown template type"],
                is_correct=False,
                algorithm_name=self.get_name()
            )

    def _apply_addition_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply malrule for addition problems."""
        decimal1 = problem.metadata['decimal1']
        decimal2 = problem.metadata['decimal2']

        # Calculate malrule answer (NOT from metadata)
        num1 = int(str(decimal1).replace('.', ''))
        num2 = int(str(decimal2).replace('.', ''))
        malrule_answer = str(num1 + num2)

        if verbose:
            steps = self._generate_verbose_steps_addition(decimal1, decimal2, num1, num2, malrule_answer)
        else:
            steps = self._generate_concise_steps_addition(decimal1, decimal2, num1, num2, malrule_answer)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _apply_comparison_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply malrule for comparison problems."""
        decimal1 = problem.metadata['decimal1']
        decimal2 = problem.metadata['decimal2']

        # Calculate malrule answer (NOT from metadata)
        # Extract decimal parts and compare as whole numbers
        str1 = str(decimal1)
        str2 = str(decimal2)

        if '.' in str1:
            decimal_part1 = str1.split('.')[1]
            num1 = int(decimal_part1) if decimal_part1 else 0
        else:
            num1 = 0

        if '.' in str2:
            decimal_part2 = str2.split('.')[1]
            num2 = int(decimal_part2) if decimal_part2 else 0
        else:
            num2 = 0

        malrule_answer = str(decimal1 if num1 > num2 else decimal2)

        if verbose:
            steps = self._generate_verbose_steps_comparison(decimal1, decimal2, num1, num2, malrule_answer)
        else:
            steps = self._generate_concise_steps_comparison(decimal1, decimal2, num1, num2, malrule_answer)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _apply_subtraction_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply malrule for subtraction problems."""
        decimal1 = problem.metadata['decimal1']
        decimal2 = problem.metadata['decimal2']

        # Calculate malrule answer (NOT from metadata)
        num1 = int(str(decimal1).replace('.', ''))
        num2 = int(str(decimal2).replace('.', ''))
        malrule_answer = str(num1 - num2)

        if verbose:
            steps = self._generate_verbose_steps_subtraction(decimal1, decimal2, num1, num2, malrule_answer)
        else:
            steps = self._generate_concise_steps_subtraction(decimal1, decimal2, num1, num2, malrule_answer)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _apply_multiplication_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply malrule for multiplication problems."""
        decimal1 = problem.metadata['decimal1']
        multiplier = problem.metadata.get('multiplier', problem.metadata.get('decimal2', 1))

        # Calculate malrule answer (NOT from metadata)
        num1 = int(str(decimal1).replace('.', ''))
        # If multiplier is also a decimal, convert it too
        if isinstance(multiplier, float):
            num2 = int(str(multiplier).replace('.', ''))
        else:
            num2 = multiplier
        malrule_answer = str(num1 * num2)

        if verbose:
            steps = self._generate_verbose_steps_multiplication(decimal1, multiplier, num1, num2, malrule_answer)
        else:
            steps = self._generate_concise_steps_multiplication(decimal1, multiplier, num1, num2, malrule_answer)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _apply_word_problem_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply malrule for word problems."""
        operation_type = problem.metadata['operation_type']

        steps = []

        if operation_type == 'addition':
            decimal1 = problem.operands[0]
            decimal2 = problem.operands[1]
            num1 = int(str(decimal1).replace('.', ''))
            num2 = int(str(decimal2).replace('.', ''))
            malrule_answer = str(num1 + num2)
            if verbose:
                steps.append(f"Problem: {problem.text}")
                steps.append(f"MALRULE: Treat decimals as whole numbers")
                steps.append(f"Convert {decimal1} → {num1}, {decimal2} → {num2}")
                steps.append(f"Add as whole numbers: {num1} + {num2} = {malrule_answer}")
                steps.append(f"(INCORRECT - treated decimals as whole numbers)")
            else:
                steps.append(f"Problem: {problem.text}")
                steps.append(f"Equation: {decimal1} + {decimal2}")
                steps.append(f"{num1} + {num2} = {malrule_answer}")
                steps.append(malrule_answer)

        elif operation_type == 'subtraction':
            decimal1 = problem.operands[0]
            decimal2 = problem.operands[1]
            num1 = int(str(decimal1).replace('.', ''))
            num2 = int(str(decimal2).replace('.', ''))
            malrule_answer = str(num1 - num2)
            if verbose:
                steps.append(f"Problem: {problem.text}")
                steps.append(f"MALRULE: Treat decimals as whole numbers")
                steps.append(f"Convert {decimal1} → {num1}, {decimal2} → {num2}")
                steps.append(f"Subtract as whole numbers: {num1} - {num2} = {malrule_answer}")
                steps.append(f"(INCORRECT - treated decimals as whole numbers)")
            else:
                steps.append(f"Problem: {problem.text}")
                steps.append(f"Equation: {decimal1} - {decimal2}")
                steps.append(f"{num1} - {num2} = {malrule_answer}")
                steps.append(malrule_answer)

        elif operation_type == 'comparison':
            decimal1 = problem.operands[0]
            decimal2 = problem.operands[1]
            str1 = str(decimal1)
            str2 = str(decimal2)

            if '.' in str1:
                num1 = int(str1.split('.')[1])
            else:
                num1 = 0

            if '.' in str2:
                num2 = int(str2.split('.')[1])
            else:
                num2 = 0

            malrule_answer = str(decimal1 if num1 > num2 else decimal2)
            if verbose:
                steps.append(f"Problem: {problem.text}")
                steps.append(f"MALRULE: Treat decimals as whole numbers")
                steps.append(f"Compare decimal parts: {num1} vs {num2}")
                steps.append(f"Answer based on whole-number comparison: {malrule_answer}")
                steps.append(f"(INCORRECT - treated decimals as whole numbers)")
            else:
                steps.append(f"Problem: {problem.text}")
                steps.append(f"Compare: {num1} vs {num2}")
                steps.append(malrule_answer)

        else:
            malrule_answer = str(problem.operands[0])
            steps.append(f"Problem: {problem.text}")
            steps.append(malrule_answer)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _apply_word_problem_context_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply malrule for word_problem_context template."""
        word_problem_type = problem.metadata.get('word_problem_type', 'comparison')
        decimal1 = problem.metadata.get('decimal1')
        decimal2 = problem.metadata.get('decimal2')

        # Calculate malrule answer (NOT from metadata)
        num1 = int(str(decimal1).replace('.', ''))
        num2 = int(str(decimal2).replace('.', ''))

        if word_problem_type == 'comparison':
            # Compare decimal parts as whole numbers
            str1 = str(decimal1)
            str2 = str(decimal2)
            if '.' in str1:
                dec_part1 = int(str1.split('.')[1])
            else:
                dec_part1 = 0
            if '.' in str2:
                dec_part2 = int(str2.split('.')[1])
            else:
                dec_part2 = 0
            malrule_answer = str(decimal1 if dec_part1 > dec_part2 else decimal2)
        elif word_problem_type == 'addition':
            malrule_answer = str(num1 + num2)
        elif word_problem_type == 'subtraction':
            malrule_answer = str(num1 - num2)
        elif word_problem_type == 'multiplication':
            malrule_answer = str(num1 * num2)
        else:
            malrule_answer = str(num1)

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
            steps.append("Step 2: Apply malrule (treat as whole numbers)")
            steps.append("")
            steps.append("MALRULE: Ignore decimal point, treat as whole numbers")
            steps.append(f"  MALRULE REASONING: 'Just remove the dots and work with the numbers'")
            steps.append("")

            steps.append(f"Convert {decimal1} → {num1}, {decimal2} → {num2}")

            if word_problem_type == 'comparison':
                steps.append(f"Compare as whole numbers: {num1} vs {num2}")
                steps.append(f"Answer: {malrule_answer}")
            elif word_problem_type == 'addition':
                steps.append(f"Add as whole numbers: {num1} + {num2} = {malrule_answer}")
            elif word_problem_type == 'subtraction':
                steps.append(f"Subtract as whole numbers: {num1} - {num2} = {malrule_answer}")
            elif word_problem_type == 'multiplication':
                steps.append(f"Multiply as whole numbers: {num1} × {num2} = {malrule_answer}")

            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT - treated decimals as whole numbers!)")
        else:
            steps.append(f"Problem: {problem.text}")
            if word_problem_type == 'comparison':
                steps.append(f"Compare: {decimal1} vs {decimal2}")
                steps.append(f"Parts: {num1} vs {num2}")
            elif word_problem_type == 'addition':
                steps.append(f"Equation: {decimal1} + {decimal2}")
                steps.append(f"{num1} + {num2} = {malrule_answer}")
            elif word_problem_type == 'subtraction':
                steps.append(f"Equation: {decimal1} - {decimal2}")
                steps.append(f"{num1} - {num2} = {malrule_answer}")
            elif word_problem_type == 'multiplication':
                steps.append(f"Equation: {decimal1} × {decimal2}")
                steps.append(f"{num1} × {num2} = {malrule_answer}")
            steps.append(malrule_answer)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
