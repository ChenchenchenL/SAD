"""
Correct scientific notation multiplication algorithm.

Implements the standard algorithm for multiplying numbers in scientific notation.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import CorrectAlgorithm, Problem, Solution


class ScientificNotationMultiplicationCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for multiplying numbers in scientific notation.

    When multiplying (a×10^m) × (b×10^n):
    1. Multiply the coefficients: a × b
    2. Add the exponents: m + n
    3. Normalize if needed (coefficient should be between 1 and 10)
    """

    def get_name(self) -> str:
        return "Correct Scientific Notation Multiplication Algorithm"

    def get_description(self) -> str:
        return (
            "The standard algorithm for multiplying numbers in scientific notation. "
            "Multiply the coefficients, add the exponents, and normalize the result "
            "so the coefficient is between 1 and 10."
        )

    def _generate_verbose_steps(self, problem: Problem, context: dict) -> list:
        """Generate verbose steps with full explanations."""
        steps = []
        operation_type = problem.metadata.get('operation_type', 'multiplication')
        num_factors = problem.metadata.get('num_factors', 2)

        if num_factors == 3:
            coef1, exp1, coef2, exp2, coef3, exp3 = problem.operands
            num1_str = f"{coef1} × 10^{exp1}"
            num2_str = f"{coef2} × 10^{exp2}"
            num3_str = f"{coef3} × 10^{exp3}"
            steps.append(f"Multiplying ({num1_str}) × ({num2_str}) × ({num3_str})")
            steps.append(f"Multiply coefficients: {coef1} × {coef2} × {coef3} = {context['coef_result']}")
            steps.append(f"Add exponents: {exp1} + {exp2} + {exp3} = {context['exp_result']}")
            steps.append(f"Result: {context['result_str']}")
        elif operation_type == 'division':
            coef1, exp1, coef2, exp2 = problem.operands
            num1_str = f"{coef1} × 10^{exp1}"
            num2_str = f"{coef2} × 10^{exp2}"
            steps.append(f"Dividing ({num1_str}) ÷ ({num2_str})")
            steps.append(f"Divide coefficients: {coef1} ÷ {coef2} = {context['coef_result']}")
            steps.append(f"Subtract exponents: {exp1} - {exp2} = {context['exp_result']}")
            steps.append(f"Result: {context['result_str']}")
        elif operation_type == 'mult_div':
            coef1, exp1, coef2, exp2, coef3, exp3 = problem.operands
            num1_str = f"{coef1} × 10^{exp1}"
            num2_str = f"{coef2} × 10^{exp2}"
            num3_str = f"{coef3} × 10^{exp3}"
            steps.append(f"Computing (({num1_str}) × ({num2_str})) ÷ ({num3_str})")
            steps.append(f"Multiply then divide coefficients: ({coef1} × {coef2}) ÷ {coef3} = {context['coef_result']}")
            steps.append(f"Add then subtract exponents: {exp1} + {exp2} - {exp3} = {context['exp_result']}")
            steps.append(f"Result: {context['result_str']}")
        else:
            coef1, exp1, coef2, exp2 = problem.operands
            num1_str = f"{coef1} × 10^{exp1}"
            num2_str = f"{coef2} × 10^{exp2}"
            steps.append(f"Multiplying ({num1_str}) × ({num2_str})")
            steps.append(f"Multiply coefficients: {coef1} × {coef2} = {context['coef_result']}")
            steps.append(f"Add exponents: {exp1} + {exp2} = {context['exp_result']}")
            steps.append(f"Result: {context['result_str']}")

        if context.get('normalized'):
            steps.append(f"Normalize (coefficient should be between 1 and 10): {context['final_answer']}")

        steps.append(f"Final answer: {context['final_answer']}")
        return steps

    def _generate_concise_steps(self, problem: Problem, context: dict) -> list:
        """Generate concise steps with only formulas and values."""
        steps = []
        operation_type = problem.metadata.get('operation_type', 'multiplication')
        num_factors = problem.metadata.get('num_factors', 2)
        is_word_problem = problem.metadata.get('is_word_problem', False)

        # Add question
        steps.append(problem.text)

        # Add formula extraction for word problems
        if is_word_problem:
            if num_factors == 3:
                coef1, exp1, coef2, exp2, coef3, exp3 = problem.operands
                num1_str = f"{coef1} × 10^{exp1}"
                num2_str = f"{coef2} × 10^{exp2}"
                num3_str = f"{coef3} × 10^{exp3}"
                steps.append(f"({num1_str}) × ({num2_str}) × ({num3_str})")
            elif operation_type == 'division':
                coef1, exp1, coef2, exp2 = problem.operands
                num1_str = f"{coef1} × 10^{exp1}"
                num2_str = f"{coef2} × 10^{exp2}"
                steps.append(f"({num1_str}) ÷ ({num2_str})")
            elif operation_type == 'mult_div':
                coef1, exp1, coef2, exp2, coef3, exp3 = problem.operands
                num1_str = f"{coef1} × 10^{exp1}"
                num2_str = f"{coef2} × 10^{exp2}"
                num3_str = f"{coef3} × 10^{exp3}"
                steps.append(f"(({num1_str}) × ({num2_str})) ÷ ({num3_str})")
            else:
                coef1, exp1, coef2, exp2 = problem.operands
                num1_str = f"{coef1} × 10^{exp1}"
                num2_str = f"{coef2} × 10^{exp2}"
                steps.append(f"({num1_str}) × ({num2_str})")

        # Add calculation steps
        if num_factors == 3:
            coef1, exp1, coef2, exp2, coef3, exp3 = problem.operands
            steps.append(f"{coef1} × {coef2} × {coef3} = {context['coef_result']}")
            steps.append(f"{exp1} + {exp2} + {exp3} = {context['exp_result']}")
        elif operation_type == 'division':
            coef1, exp1, coef2, exp2 = problem.operands
            steps.append(f"{coef1} ÷ {coef2} = {context['coef_result']}")
            steps.append(f"{exp1} - {exp2} = {context['exp_result']}")
        elif operation_type == 'mult_div':
            coef1, exp1, coef2, exp2, coef3, exp3 = problem.operands
            steps.append(f"({coef1} × {coef2}) ÷ {coef3} = {context['coef_result']}")
            steps.append(f"{exp1} + {exp2} - {exp3} = {context['exp_result']}")
        else:
            coef1, exp1, coef2, exp2 = problem.operands
            steps.append(f"{coef1} × {coef2} = {context['coef_result']}")
            steps.append(f"{exp1} + {exp2} = {context['exp_result']}")

        # Add normalization step if needed
        if context.get('normalized'):
            steps.append(f"{context['result_str']} = {context['final_answer']}")

        # Add answer
        steps.append(context['final_answer'])
        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct scientific notation multiplication/division algorithm.

        Args:
            problem: Scientific notation problem to solve
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with correct answer
        """
        num_factors = problem.metadata.get('num_factors', 2)
        operation_type = problem.metadata.get('operation_type', 'multiplication')

        # Handle different problem types
        if num_factors == 3:
            return self._solve_three_factor(problem, verbose)
        elif operation_type == 'division':
            return self._solve_division(problem, verbose)
        elif operation_type == 'mult_div':
            return self._solve_mult_div(problem, verbose)

        # Default: 2-factor multiplication
        coef1, exp1, coef2, exp2 = problem.operands

        # CORRECT: Multiply coefficients
        coef_result = coef1 * coef2

        # Add exponents
        exp_result = exp1 + exp2

        # Combine
        result_str = f"{coef_result} × 10^{exp_result}"

        # Normalize to proper scientific notation (coefficient between 1 and 10)
        normalized = False
        if coef_result >= 10:
            normalized_coef = coef_result
            exp_adjust = 0
            while normalized_coef >= 10:
                normalized_coef /= 10
                exp_adjust += 1
            normalized_exp = exp_result + exp_adjust
            final_answer = f"{normalized_coef} × 10^{normalized_exp}"
            normalized = True
        elif coef_result < 1 and coef_result > 0:
            normalized_coef = coef_result
            exp_adjust = 0
            while normalized_coef < 1:
                normalized_coef *= 10
                exp_adjust -= 1
            normalized_exp = exp_result + exp_adjust
            final_answer = f"{normalized_coef} × 10^{normalized_exp}"
            normalized = True
        else:
            final_answer = result_str

        context = {
            'coef_result': coef_result,
            'exp_result': exp_result,
            'result_str': result_str,
            'final_answer': final_answer,
            'normalized': normalized
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, context)
        else:
            steps = self._generate_concise_steps(problem, context)

        return Solution(
            answer=final_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _solve_three_factor(self, problem: Problem, verbose: bool = False) -> Solution:
        """Solve 3-factor multiplication: (a×10^m) × (b×10^n) × (c×10^p)"""
        coef1, exp1, coef2, exp2, coef3, exp3 = problem.operands

        # CORRECT: Multiply all coefficients
        coef_result = coef1 * coef2 * coef3

        # Add all exponents
        exp_result = exp1 + exp2 + exp3

        # Combine
        result_str = f"{coef_result} × 10^{exp_result}"

        # Normalize
        normalized = False
        final_answer = self._normalize_and_track(coef_result, exp_result)
        if final_answer != result_str:
            normalized = True

        context = {
            'coef_result': coef_result,
            'exp_result': exp_result,
            'result_str': result_str,
            'final_answer': final_answer,
            'normalized': normalized
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, context)
        else:
            steps = self._generate_concise_steps(problem, context)

        return Solution(
            answer=final_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _solve_division(self, problem: Problem, verbose: bool = False) -> Solution:
        """Solve division: (a×10^m) ÷ (b×10^n)"""
        coef1, exp1, coef2, exp2 = problem.operands

        # CORRECT: Divide coefficients
        coef_result = coef1 / coef2

        # Subtract exponents
        exp_result = exp1 - exp2

        # Combine
        result_str = f"{coef_result} × 10^{exp_result}"

        # Normalize
        normalized = False
        final_answer = self._normalize_and_track(coef_result, exp_result)
        if final_answer != result_str:
            normalized = True

        context = {
            'coef_result': coef_result,
            'exp_result': exp_result,
            'result_str': result_str,
            'final_answer': final_answer,
            'normalized': normalized
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, context)
        else:
            steps = self._generate_concise_steps(problem, context)

        return Solution(
            answer=final_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _solve_mult_div(self, problem: Problem, verbose: bool = False) -> Solution:
        """Solve ((a×10^m) × (b×10^n)) ÷ (c×10^p)"""
        coef1, exp1, coef2, exp2, coef3, exp3 = problem.operands

        # CORRECT: Multiply first two coefficients, then divide by third
        coef_result = (coef1 * coef2) / coef3

        # Add first two exponents, then subtract third
        exp_result = exp1 + exp2 - exp3

        # Combine
        result_str = f"{coef_result} × 10^{exp_result}"

        # Normalize
        normalized = False
        final_answer = self._normalize_and_track(coef_result, exp_result)
        if final_answer != result_str:
            normalized = True

        context = {
            'coef_result': coef_result,
            'exp_result': exp_result,
            'result_str': result_str,
            'final_answer': final_answer,
            'normalized': normalized
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, context)
        else:
            steps = self._generate_concise_steps(problem, context)

        return Solution(
            answer=final_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _normalize_and_track(self, coef: float, exp: int) -> str:
        """Normalize scientific notation and return the result string."""
        if coef >= 10:
            normalized_coef = coef
            exp_adjust = 0
            while normalized_coef >= 10:
                normalized_coef /= 10
                exp_adjust += 1
            normalized_exp = exp + exp_adjust
            return f"{normalized_coef} × 10^{normalized_exp}"
        elif coef < 1 and coef > 0:
            normalized_coef = coef
            exp_adjust = 0
            while normalized_coef < 1:
                normalized_coef *= 10
                exp_adjust -= 1
            normalized_exp = exp + exp_adjust
            return f"{normalized_coef} × 10^{normalized_exp}"
        else:
            return f"{coef} × 10^{exp}"

    def _normalize(self, coef: float, exp: int, steps: list) -> str:
        """Normalize scientific notation to have coefficient between 1 and 10."""
        if coef >= 10:
            normalized_coef = coef
            exp_adjust = 0
            while normalized_coef >= 10:
                normalized_coef /= 10
                exp_adjust += 1
            normalized_exp = exp + exp_adjust
            normalized_str = f"{normalized_coef} × 10^{normalized_exp}"
            steps.append(f"Normalize (coefficient should be between 1 and 10): {normalized_str}")
            return normalized_str
        elif coef < 1 and coef > 0:
            normalized_coef = coef
            exp_adjust = 0
            while normalized_coef < 1:
                normalized_coef *= 10
                exp_adjust -= 1
            normalized_exp = exp + exp_adjust
            normalized_str = f"{normalized_coef} × 10^{normalized_exp}"
            steps.append(f"Normalize (coefficient should be between 1 and 10): {normalized_str}")
            return normalized_str
        else:
            return f"{coef} × 10^{exp}"
