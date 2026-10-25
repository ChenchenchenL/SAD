"""
Malrule algorithm for Multiply-Exponents-When-Multiplying-Powers.

Students multiply exponents when multiplying powers: x^m × x^n = x^(m×n)
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution

class MultiplyExponentsWhenMultiplyingPowersMalrule(Malrule):
    """Student multiplies exponents instead of adding them."""

    def get_name(self):
        return "Multiply-Exponents-When-Multiplying-Powers"

    def get_description(self):
        return (
            "Student multiplies exponents when multiplying powers with the same base: "
            "x^m × x^n = x^(m×n). For example, x³ × x⁵ = x¹⁵ instead of x⁸. Research documents "
            "this as confusion between the product rule (add) and power rule (multiply)."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        if 'malrule_answer' in problem.metadata:
            malrule_answer = problem.metadata['malrule_answer']
            template = problem.metadata.get('template', 'basic_two_powers')

            # For numerical_base or word_problem, return the power notation
            if template == 'numerical_base':
                base = problem.metadata.get('base', 2)
                malrule_exp = problem.metadata.get('malrule_exponent', malrule_answer)
                return f"{base}^{malrule_exp}"
            elif template == 'word_problem':
                base = problem.metadata.get('base', 2)
                return f"{base}^{malrule_answer}"
            elif template == 'mixed_operations':
                if isinstance(malrule_answer, float):
                    return f"x^{malrule_answer:.1f}"
                return f"x^{malrule_answer}"
            else:
                # basic_two_powers, three_powers
                return f"x^{malrule_answer}"

        # Backwards compatibility
        m = problem.metadata.get('exponent1', 0)
        n = problem.metadata.get('exponent2', 0)
        return f"x^{m * n}"

    def _generate_concise_steps(self, problem: Problem, m: int, n: int, malrule_answer, answer_str: str) -> list:
        """
        Generate concise steps for the malrule algorithm.

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
            steps.append(f"x^{m} × x^{n} = x^({m}×{n})")
            steps.append(f"= x^{malrule_answer}")
        elif template == 'three_powers' or (is_word_problem and word_problem_type == 'three_powers'):
            c = problem.metadata['exponent3']
            steps.append(f"x^{m} × x^{n} × x^{c} = x^({m}×{n}×{c})")
            steps.append(f"= x^{malrule_answer}")
        elif template == 'numerical_base' or (is_word_problem and word_problem_type == 'numerical_base'):
            base = problem.metadata['base']
            malrule_exp = m * n
            steps.append(f"{base}^{m} × {base}^{n} = {base}^({m}×{n})")
            steps.append(f"= {base}^{malrule_exp}")
            steps.append(f"= {malrule_answer}")
        elif template == 'mixed_operations' or (is_word_problem and word_problem_type == 'mixed_operations'):
            c = problem.metadata['exponent3']
            steps.append(f"x^{m} × x^{n} = x^({m}×{n}) = x^{m*n}")
            steps.append(f"x^{m*n} ÷ x^{c} = x^({m*n}÷{c}) = x^{malrule_answer}")
        elif template == 'word_problem':
            base = problem.metadata.get('base', 2)
            steps.append(f"{base}^{m} × {base}^{n} = {base}^({m}×{n})")
            steps.append(f"= {base}^{malrule_answer}")
        else:
            steps.append(f"x^{m} × x^{n} = x^({m}×{n})")
            steps.append(f"= x^{malrule_answer}")

        # Answer
        steps.append(f"Answer: {answer_str}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, m: int, n: int, malrule_answer, answer_str: str) -> list:
        """
        Generate verbose steps for the malrule algorithm (original implementation).
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
            steps.append("Step 2: Apply malrule (incorrectly multiply exponents)")
            steps.append("")
        else:
            steps.append(f"Problem: {problem.text}")
            steps.append("")

        steps.append("MALRULE: Multiply the exponents")
        steps.append("")

        if template == 'basic_two_powers' or (is_word_problem and word_problem_type == 'basic_two_powers'):
            steps.append(f"  x^{m} × x^{n} = x^({m}×{n})")
            steps.append(f"  = x^{malrule_answer}")
        elif template == 'three_powers' or (is_word_problem and word_problem_type == 'three_powers'):
            c = problem.metadata['exponent3']
            steps.append(f"  x^{m} × x^{n} × x^{c} = x^({m}×{n}×{c})")
            steps.append(f"  = x^{malrule_answer}")
        elif template == 'numerical_base' or (is_word_problem and word_problem_type == 'numerical_base'):
            base = problem.metadata['base']
            malrule_exp = m * n
            steps.append(f"  {base}^{m} × {base}^{n} = {base}^({m}×{n})")
            steps.append(f"  = {base}^{malrule_exp}")
            steps.append(f"  = {malrule_answer}")
        elif template == 'mixed_operations' or (is_word_problem and word_problem_type == 'mixed_operations'):
            c = problem.metadata['exponent3']
            steps.append(f"  Student multiplies for × and divides for ÷:")
            steps.append(f"  x^{m} × x^{n} = x^({m}×{n}) = x^{m*n}")
            steps.append(f"  x^{m*n} ÷ x^{c} = x^({m*n}÷{c}) = x^{malrule_answer}")
        elif template == 'word_problem':
            base = problem.metadata.get('base', 2)
            steps.append(f"  Student multiplies exponents: {base}^{m} × {base}^{n} = {base}^({m}×{n})")
            steps.append(f"  = {base}^{malrule_answer}")

        steps.append("")
        steps.append(f"Student's answer: {answer_str}")
        steps.append("")

        if template in ['basic_two_powers', 'three_powers']:
            steps.append(
                f"The student incorrectly multiplies the exponents. "
                f"This confuses the product rule (add exponents) "
                f"with the power rule (multiply exponents for (x^m)^n)."
            )
        else:
            steps.append(
                f"The student incorrectly multiplies the exponents when multiplying powers "
                f"with the same base. The correct rule is to ADD the exponents."
            )

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the multiply-exponents malrule across all templates.

        Args:
            problem: The power multiplication problem
            verbose: If True, generate verbose steps; if False, generate concise steps (default: False)

        Returns:
            Solution showing incorrect multiplication of exponents
        """
        template = problem.metadata.get('template', 'basic_two_powers')
        is_word_problem = problem.metadata.get('is_word_problem', False)
        word_problem_type = problem.metadata.get('word_problem_type', None)

        # Parse parameters from metadata (NOT the malrule_answer)
        m = problem.metadata['exponent1']
        n = problem.metadata['exponent2']

        # CALCULATE the malrule answer based on template
        if template == 'basic_two_powers' or (is_word_problem and word_problem_type == 'basic_two_powers'):
            malrule_answer = m * n
            answer_str = f"x^{malrule_answer}"
        elif template == 'three_powers' or (is_word_problem and word_problem_type == 'three_powers'):
            c = problem.metadata['exponent3']
            malrule_answer = m * n * c
            answer_str = f"x^{malrule_answer}"
        elif template == 'numerical_base' or (is_word_problem and word_problem_type == 'numerical_base'):
            base = problem.metadata['base']
            malrule_exp = m * n
            malrule_answer = base ** malrule_exp
            answer_str = f"{base}^{malrule_exp}"
        elif template == 'mixed_operations' or (is_word_problem and word_problem_type == 'mixed_operations'):
            c = problem.metadata['exponent3']
            malrule_answer = (m * n) // c if (m * n) % c == 0 else (m * n) / c
            if isinstance(malrule_answer, float):
                answer_str = f"x^{malrule_answer:.1f}"
            else:
                answer_str = f"x^{malrule_answer}"
        elif template == 'word_problem':
            base = problem.metadata.get('base', 2)
            malrule_answer = m * n
            answer_str = f"{base}^{malrule_answer}"
        else:
            malrule_answer = m * n
            answer_str = f"x^{malrule_answer}"

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, m, n, malrule_answer, answer_str)
        else:
            steps = self._generate_concise_steps(problem, m, n, malrule_answer, answer_str)

        return Solution(
            answer=answer_str,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
