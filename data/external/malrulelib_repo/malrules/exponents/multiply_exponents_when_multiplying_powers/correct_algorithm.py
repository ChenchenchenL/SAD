"""
Correct algorithm for multiplying powers with the same base.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import CorrectAlgorithm, Problem, Solution


class ProductRuleCorrectAlgorithm(CorrectAlgorithm):
    """Correctly applies the product rule: x^m × x^n = x^(m+n)."""

    def get_name(self):
        return "Product Rule for Exponents"

    def get_description(self):
        return "Applies the product rule: x^m × x^n = x^(m+n)"

    def _generate_concise_steps(self, problem: Problem, m: int, n: int, correct_answer, answer_str: str) -> list:
        """
        Generate concise steps for the correct algorithm.

        Format: [Question, step, step, ..., answer]
        """
        template = problem.metadata.get('template', 'basic_two_powers')
        is_word_problem = problem.metadata.get('is_word_problem', False)
        word_problem_type = problem.metadata.get('word_problem_type', None)

        steps = []

        # Question
        steps.append(problem.text)

        # For word problems, include formula extraction
        if is_word_problem:
            if word_problem_type == 'basic_two_powers':
                steps.append(f"x^{m} × x^{n}")
            elif word_problem_type == 'three_powers':
                c = problem.metadata['exponent3']
                steps.append(f"x^{m} × x^{n} × x^{c}")
            elif word_problem_type == 'numerical_base':
                base = problem.metadata['base']
                steps.append(f"{base}^{m} × {base}^{n}")
            elif word_problem_type == 'mixed_operations':
                c = problem.metadata['exponent3']
                steps.append(f"x^{m} × x^{n} ÷ x^{c}")

        # Show the calculation based on template
        if template == 'basic_two_powers' or (is_word_problem and word_problem_type == 'basic_two_powers'):
            steps.append(f"x^{m} × x^{n} = x^({m}+{n})")
            steps.append(f"= x^{correct_answer}")
        elif template == 'three_powers' or (is_word_problem and word_problem_type == 'three_powers'):
            c = problem.metadata['exponent3']
            steps.append(f"x^{m} × x^{n} × x^{c} = x^({m}+{n}+{c})")
            steps.append(f"= x^{correct_answer}")
        elif template == 'numerical_base' or (is_word_problem and word_problem_type == 'numerical_base'):
            base = problem.metadata['base']
            correct_exp = m + n
            steps.append(f"{base}^{m} × {base}^{n} = {base}^({m}+{n})")
            steps.append(f"= {base}^{correct_exp}")
            steps.append(f"= {correct_answer}")
        elif template == 'mixed_operations' or (is_word_problem and word_problem_type == 'mixed_operations'):
            c = problem.metadata['exponent3']
            steps.append(f"x^{m} × x^{n} = x^({m}+{n}) = x^{m+n}")
            steps.append(f"x^{m+n} ÷ x^{c} = x^({m+n}-{c}) = x^{correct_answer}")
        else:
            steps.append(f"x^{m} × x^{n} = x^({m}+{n})")
            steps.append(f"= x^{correct_answer}")

        # Answer
        steps.append(f"Answer: {answer_str}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, m: int, n: int, correct_answer, answer_str: str) -> list:
        """
        Generate verbose steps for the correct algorithm (original implementation).
        """
        template = problem.metadata.get('template', 'basic_two_powers')
        is_word_problem = problem.metadata.get('is_word_problem', False)
        word_problem_type = problem.metadata.get('word_problem_type', None)

        steps = []

        # For word problems, show extraction step
        if is_word_problem:
            steps.append(f"Word Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Extract the mathematical expression from the word problem")

            if word_problem_type == 'basic_two_powers':
                steps.append(f"  Expression: x^{m} × x^{n}")
            elif word_problem_type == 'three_powers':
                c = problem.metadata['exponent3']
                steps.append(f"  Expression: x^{m} × x^{n} × x^{c}")
            elif word_problem_type == 'numerical_base':
                base = problem.metadata['base']
                steps.append(f"  Expression: {base}^{m} × {base}^{n}")
            elif word_problem_type == 'mixed_operations':
                c = problem.metadata['exponent3']
                steps.append(f"  Expression: x^{m} × x^{n} ÷ x^{c}")

            steps.append("")
            steps.append("Step 2: Apply the product rule")
            steps.append("")
        else:
            steps.append(f"Problem: {problem.text}")
            steps.append("")

        steps.append("CORRECT METHOD: Product Rule")
        steps.append(f"  When multiplying powers with the same base, ADD the exponents:")

        if template == 'basic_two_powers' or (is_word_problem and word_problem_type == 'basic_two_powers'):
            steps.append(f"  x^{m} × x^{n} = x^({m}+{n})")
            steps.append(f"  = x^{correct_answer}")
        elif template == 'three_powers' or (is_word_problem and word_problem_type == 'three_powers'):
            c = problem.metadata['exponent3']
            steps.append(f"  x^{m} × x^{n} × x^{c} = x^({m}+{n}+{c})")
            steps.append(f"  = x^{correct_answer}")
        elif template == 'numerical_base' or (is_word_problem and word_problem_type == 'numerical_base'):
            base = problem.metadata['base']
            correct_exp = m + n
            steps.append(f"  {base}^{m} × {base}^{n} = {base}^({m}+{n})")
            steps.append(f"  = {base}^{correct_exp}")
            steps.append(f"  = {correct_answer}")
        elif template == 'mixed_operations' or (is_word_problem and word_problem_type == 'mixed_operations'):
            c = problem.metadata['exponent3']
            steps.append(f"  First, multiply: x^{m} × x^{n} = x^({m}+{n}) = x^{m+n}")
            steps.append(f"  Then, divide: x^{m+n} ÷ x^{c} = x^({m+n}-{c}) = x^{correct_answer}")
        else:
            steps.append(f"  x^{m} × x^{n} = x^({m}+{n})")
            steps.append(f"  = x^{correct_answer}")

        steps.append("")

        if not is_word_problem or word_problem_type not in ['numerical_base']:
            steps.append("Verification by expansion:")
            steps.append(f"  x^{m} = x · x · ... · x ({m} times)")
            steps.append(f"  x^{n} = x · x · ... · x ({n} times)")
            if template == 'three_powers' or (is_word_problem and word_problem_type == 'three_powers'):
                c = problem.metadata['exponent3']
                steps.append(f"  x^{c} = x · x · ... · x ({c} times)")
                steps.append(f"  x^{m} × x^{n} × x^{c} = x multiplied by itself ({m}+{n}+{c}) = {correct_answer} times")
            elif template == 'mixed_operations' or (is_word_problem and word_problem_type == 'mixed_operations'):
                c = problem.metadata['exponent3']
                steps.append(f"  Multiplying gives {m+n} factors, dividing by x^{c} removes {c} factors")
                steps.append(f"  Result: x^{correct_answer}")
            else:
                steps.append(f"  x^{m} × x^{n} = x multiplied by itself ({m}+{n}) = {correct_answer} times")

        steps.append("")
        steps.append(f"Answer: {answer_str}")
        steps.append("")
        steps.append(
            f"The product rule states that when multiplying powers with the same base, "
            f"we add the exponents."
        )

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct product rule algorithm.

        Args:
            problem: The power multiplication problem
            verbose: If True, generate verbose steps; if False, generate concise steps (default: False)

        Returns:
            Solution showing correct addition of exponents
        """
        template = problem.metadata.get('template', 'basic_two_powers')
        is_word_problem = problem.metadata.get('is_word_problem', False)
        word_problem_type = problem.metadata.get('word_problem_type', None)

        # Parse parameters from metadata (NOT answers)
        m = problem.metadata['exponent1']
        n = problem.metadata['exponent2']

        # CALCULATE the correct answer based on template
        if template == 'basic_two_powers' or (is_word_problem and word_problem_type == 'basic_two_powers'):
            correct_answer = m + n
            answer_str = f"x^{correct_answer}"
        elif template == 'three_powers' or (is_word_problem and word_problem_type == 'three_powers'):
            c = problem.metadata['exponent3']
            correct_answer = m + n + c
            answer_str = f"x^{correct_answer}"
        elif template == 'numerical_base' or (is_word_problem and word_problem_type == 'numerical_base'):
            base = problem.metadata['base']
            correct_exp = m + n
            correct_answer = base ** correct_exp
            answer_str = str(correct_answer)
        elif template == 'mixed_operations' or (is_word_problem and word_problem_type == 'mixed_operations'):
            c = problem.metadata['exponent3']
            correct_answer = m + n - c
            answer_str = f"x^{correct_answer}"
        else:  # word_problem (old format)
            correct_answer = m + n
            answer_str = f"x^{correct_answer}"

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, m, n, correct_answer, answer_str)
        else:
            steps = self._generate_concise_steps(problem, m, n, correct_answer, answer_str)

        return Solution(
            answer=answer_str,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
