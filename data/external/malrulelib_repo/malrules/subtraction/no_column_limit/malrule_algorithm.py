"""
No-Column-Limit malrule algorithm.

Implements the systematic error where students write multi-digit sums
directly in one column without understanding place value limits.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List

class NoColumnLimitMalrule(Malrule):
    """
    Implements the No-Column-Limit bug.

    Students write entire column sums (e.g., 8+7=15) directly in the ones
    column without carrying, resulting in concatenated digits.
    """

    def get_name(self) -> str:
        return "No-Column-Limit"

    def get_description(self) -> str:
        return (
            "When adding multi-digit numbers, students write the entire column sum "
            "directly in that column without regrouping, failing to understand the "
            "base-10 constraint that each place value position can only hold a single "
            "digit (0-9). For example, in 48+17, students compute 8+7=15 and write '15' "
            "in the ones column, producing concatenated results like '415' instead of "
            "the correct answer 65. This error, documented by the Colorado Department "
            "of Education, indicates a fundamental misunderstanding of place value."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem using logic."""
        template = problem.metadata.get('template', 'basic_two_digit')
        num1, num2 = problem.operands

        if template == 'three_digit':
            # Compute digit decomposition for 3-digit numbers
            hundreds1 = num1 // 100
            tens1 = (num1 // 10) % 10
            ones1 = num1 % 10
            hundreds2 = num2 // 100
            tens2 = (num2 // 10) % 10
            ones2 = num2 % 10

            # Compute column sums and concatenate
            ones_sum = ones1 + ones2
            tens_sum = tens1 + tens2
            hundreds_sum = hundreds1 + hundreds2
            malrule_answer_num = str(hundreds_sum) + str(tens_sum) + str(ones_sum)
            return malrule_answer_num
        else:
            # Compute digit decomposition for 2-digit numbers
            tens1 = num1 // 10
            ones1 = num1 % 10
            tens2 = num2 // 10
            ones2 = num2 % 10

            # Compute column sums and concatenate
            ones_sum = ones1 + ones2
            tens_sum = tens1 + tens2
            malrule_answer_num = str(tens_sum) + str(ones_sum)

            # Apply format based on template
            if template == 'money_context':
                return f'${malrule_answer_num}'
            elif template == 'word_problem':
                context_type = problem.metadata.get('context_type', '')
                return f'{malrule_answer_num} {context_type}'
            else:
                return malrule_answer_num

    def _generate_concise_steps(self, problem: Problem, num1: int, num2: int,
                                 malrule_answer: str, template: str) -> List[str]:
        """Generate concise steps with only formulas and values."""
        steps = []
        steps.append(f"Question: {problem.text}")
        steps.append(f"Formula: {num1} + {num2}")

        if template == 'three_digit':
            hundreds1 = num1 // 100
            tens1 = (num1 // 10) % 10
            ones1 = num1 % 10
            hundreds2 = num2 // 100
            tens2 = (num2 // 10) % 10
            ones2 = num2 % 10

            ones_sum = ones1 + ones2
            tens_sum = tens1 + tens2
            hundreds_sum = hundreds1 + hundreds2

            steps.append(f"Ones: {ones1} + {ones2} = {ones_sum}")
            steps.append(f"Tens: {tens1} + {tens2} = {tens_sum}")
            steps.append(f"Hundreds: {hundreds1} + {hundreds2} = {hundreds_sum}")
            steps.append(f"Concatenate: {hundreds_sum}{tens_sum}{ones_sum}")
        else:
            tens1 = num1 // 10
            ones1 = num1 % 10
            tens2 = num2 // 10
            ones2 = num2 % 10

            ones_sum = ones1 + ones2
            tens_sum = tens1 + tens2

            steps.append(f"Ones: {ones1} + {ones2} = {ones_sum}")
            steps.append(f"Tens: {tens1} + {tens2} = {tens_sum}")
            steps.append(f"Concatenate: {tens_sum}{ones_sum}")

        # Strip formatting for answer
        answer_num = ''.join(filter(str.isdigit, malrule_answer))
        steps.append(f"Answer: {answer_num}")
        return steps

    def _generate_verbose_steps(self, problem: Problem, num1: int, num2: int,
                                 malrule_answer: str, template: str) -> List[str]:
        """Generate verbose steps with detailed explanations."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: Write entire column sums without understanding place value limits")
        steps.append("  Student thinks: 'I can write any number in a column'")
        steps.append("")

        if template == 'three_digit':
            hundreds1 = num1 // 100
            tens1 = (num1 // 10) % 10
            ones1 = num1 % 10
            hundreds2 = num2 // 100
            tens2 = (num2 // 10) % 10
            ones2 = num2 % 10

            ones_sum = ones1 + ones2
            tens_sum = tens1 + tens2
            hundreds_sum = hundreds1 + hundreds2

            malrule_answer_num = str(hundreds_sum) + str(tens_sum) + str(ones_sum)

            steps.append(f"Adding {num1} + {num2}")
            steps.append("")
            steps.append(f"Ones column: {ones1} + {ones2} = {ones_sum}")
            steps.append(f"  MALRULE: Write '{ones_sum}' in ones column (should carry!)")
            steps.append("")
            steps.append(f"Tens column: {tens1} + {tens2} = {tens_sum}")
            steps.append(f"  MALRULE: Write '{tens_sum}' in tens column")
            steps.append("")
            steps.append(f"Hundreds column: {hundreds1} + {hundreds2} = {hundreds_sum}")
            steps.append(f"  MALRULE: Write '{hundreds_sum}' in hundreds column")
            steps.append("")
            steps.append(f"MALRULE: Concatenate all sums → {malrule_answer_num}")
        else:
            tens1 = num1 // 10
            ones1 = num1 % 10
            tens2 = num2 // 10
            ones2 = num2 % 10

            ones_sum = ones1 + ones2
            tens_sum = tens1 + tens2

            malrule_answer_num = str(tens_sum) + str(ones_sum)

            steps.append(f"Adding {num1} + {num2}")
            steps.append("")
            steps.append(f"Ones column: {ones1} + {ones2} = {ones_sum}")
            steps.append(f"  MALRULE: Write '{ones_sum}' in the ones column")
            steps.append(f"  (Student doesn't understand that {ones_sum} is too big for one column!)")
            steps.append("")
            steps.append(f"Tens column: {tens1} + {tens2} = {tens_sum}")
            steps.append(f"  MALRULE: Write '{tens_sum}' in the tens column")
            steps.append("")
            steps.append(f"MALRULE: Concatenate sums → {malrule_answer_num}")

        steps.append("")
        steps.append(f"Final Answer: {malrule_answer} (INCORRECT - no place value understanding!)")
        steps.append("")
        steps.append("Missing: Understanding that each column can only hold digits 0-9")
        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the No-Column-Limit malrule across all templates.

        Uses logic to compute answers, not metadata values.

        Args:
            problem: Addition problem to solve
            verbose: If True, generate detailed steps; if False, generate concise steps

        Returns:
            Solution with incorrect answer
        """
        template = problem.metadata.get('template', 'basic_two_digit')
        num1, num2 = problem.operands

        # Calculate malrule answer using logic
        malrule_answer = self.calculate_expected_answer(problem)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, num1, num2, malrule_answer, template)
        else:
            steps = self._generate_concise_steps(problem, num1, num2, malrule_answer, template)

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
