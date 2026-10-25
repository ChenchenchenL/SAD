"""
Add-Coefficients-When-Multiplying malrule algorithm.

Implements the systematic error where students add the coefficients instead of
multiplying them when multiplying numbers in scientific notation.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List

class AddCoefficientsWhenMultiplyingMalrule(Malrule):
    """
    Implements the Add-Coefficients-When-Multiplying bug.

    Students correctly add the exponents when multiplying numbers in scientific
    notation, but they incorrectly add the coefficients instead of multiplying them.
    This likely stems from confusion between the two operations occurring in the
    same problem.
    """

    def get_name(self) -> str:
        return "Add-Coefficients-When-Multiplying"

    def get_description(self) -> str:
        return (
            "When multiplying numbers in scientific notation, students correctly "
            "add the exponents but incorrectly add the coefficients instead of "
            "multiplying them. For example, (4×10³)×(8×10⁵) should be (4×8)×10⁽³⁺⁵⁾ = "
            "32×10⁸ = 3.2×10⁹, but the student calculates (4+8)×10⁽³⁺⁵⁾ = 12×10⁸ = "
            "1.2×10⁹ (incorrect)."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Calculate malrule answer by applying the malrule logic
        solution = self._apply_malrule(problem)
        return solution.answer

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
            steps.append(f"MALRULE: Adding coefficients: {coef1} + {coef2} + {coef3} = {context['coef_result']}")
            steps.append(f"Adding exponents (correct): {exp1} + {exp2} + {exp3} = {context['exp_result']}")
        elif operation_type == 'division':
            coef1, exp1, coef2, exp2 = problem.operands
            num1_str = f"{coef1} × 10^{exp1}"
            num2_str = f"{coef2} × 10^{exp2}"
            steps.append(f"Dividing ({num1_str}) ÷ ({num2_str})")
            steps.append(f"MALRULE: Adding coefficients: {coef1} + {coef2} = {context['coef_result']}")
            steps.append(f"Subtracting exponents (correct): {exp1} - {exp2} = {context['exp_result']}")
        elif operation_type == 'mult_div':
            coef1, exp1, coef2, exp2, coef3, exp3 = problem.operands
            num1_str = f"{coef1} × 10^{exp1}"
            num2_str = f"{coef2} × 10^{exp2}"
            num3_str = f"{coef3} × 10^{exp3}"
            steps.append(f"Computing (({num1_str}) × ({num2_str})) ÷ ({num3_str})")
            steps.append(f"MALRULE: Adding all coefficients: {coef1} + {coef2} + {coef3} = {context['coef_result']}")
            steps.append(f"Handling exponents (correct): {exp1} + {exp2} - {exp3} = {context['exp_result']}")
        else:
            coef1, exp1, coef2, exp2 = problem.operands
            num1_str = f"{coef1} × 10^{exp1}"
            num2_str = f"{coef2} × 10^{exp2}"
            steps.append(f"Multiplying ({num1_str}) × ({num2_str})")
            steps.append(f"MALRULE: Adding coefficients: {coef1} + {coef2} = {context['coef_result']}")
            steps.append(f"Adding exponents: {exp1} + {exp2} = {context['exp_result']}")

        steps.append(f"Result: {context['result_str']}")

        if context.get('normalized'):
            steps.append(f"Normalizing: {context['final_answer']}")

        steps.append(f"INCORRECT ANSWER: {context['final_answer']}")
        steps.append(f"ERROR: Should have MULTIPLIED coefficients, not added them!")
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
            steps.append(f"{coef1} + {coef2} + {coef3} = {context['coef_result']}")
            steps.append(f"{exp1} + {exp2} + {exp3} = {context['exp_result']}")
        elif operation_type == 'division':
            coef1, exp1, coef2, exp2 = problem.operands
            steps.append(f"{coef1} + {coef2} = {context['coef_result']}")
            steps.append(f"{exp1} - {exp2} = {context['exp_result']}")
        elif operation_type == 'mult_div':
            coef1, exp1, coef2, exp2, coef3, exp3 = problem.operands
            steps.append(f"{coef1} + {coef2} + {coef3} = {context['coef_result']}")
            steps.append(f"{exp1} + {exp2} - {exp3} = {context['exp_result']}")
        else:
            coef1, exp1, coef2, exp2 = problem.operands
            steps.append(f"{coef1} + {coef2} = {context['coef_result']}")
            steps.append(f"{exp1} + {exp2} = {context['exp_result']}")

        # Add normalization step if needed
        if context.get('normalized'):
            steps.append(f"{context['result_str']} = {context['final_answer']}")

        # Add answer
        steps.append(context['final_answer'])
        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Add-Coefficients-When-Multiplying malrule.

        Adds the coefficients instead of multiplying/dividing them, but correctly handles exponents.

        Args:
            problem: Scientific notation problem to solve
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with malrule (incorrect) answer
        """
        num_factors = problem.metadata.get('num_factors', 2)
        operation_type = problem.metadata.get('operation_type', 'multiplication')

        # Handle different problem types
        if num_factors == 3:
            return self._apply_malrule_three_factor(problem, verbose)
        elif operation_type == 'division':
            return self._apply_malrule_division(problem, verbose)
        elif operation_type == 'mult_div':
            return self._apply_malrule_mult_div(problem, verbose)

        # Default: 2-factor multiplication
        coef1, exp1, coef2, exp2 = problem.operands

        # MALRULE: Add coefficients instead of multiplying
        coef_result = coef1 + coef2

        # Correctly add exponents
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
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _apply_malrule_three_factor(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply malrule to 3-factor multiplication."""
        coef1, exp1, coef2, exp2, coef3, exp3 = problem.operands

        # MALRULE: Add all coefficients instead of multiplying
        coef_result = coef1 + coef2 + coef3

        # Correctly add exponents
        exp_result = exp1 + exp2 + exp3

        result_str = f"{coef_result} × 10^{exp_result}"
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
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _apply_malrule_division(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply malrule to division."""
        coef1, exp1, coef2, exp2 = problem.operands

        # MALRULE: Add coefficients instead of dividing
        coef_result = coef1 + coef2

        # Correctly subtract exponents
        exp_result = exp1 - exp2

        result_str = f"{coef_result} × 10^{exp_result}"
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
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _apply_malrule_mult_div(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply malrule to multiplication then division."""
        coef1, exp1, coef2, exp2, coef3, exp3 = problem.operands

        # MALRULE: Add all coefficients instead of multiplying/dividing
        coef_result = coef1 + coef2 + coef3

        # Correctly handle exponents
        exp_result = exp1 + exp2 - exp3

        result_str = f"{coef_result} × 10^{exp_result}"
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
            is_correct=False,
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

    def _normalize_result(self, coef_result: float, exp_result: int, result_str: str, steps: list) -> str:
        """Normalize the result to proper scientific notation."""
        if coef_result >= 10:
            normalized_coef = coef_result
            exp_adjust = 0
            while normalized_coef >= 10:
                normalized_coef /= 10
                exp_adjust += 1
            normalized_exp = exp_result + exp_adjust
            normalized_str = f"{normalized_coef} × 10^{normalized_exp}"
            steps.append(f"Normalizing: {normalized_str}")
            return normalized_str
        elif coef_result < 1 and coef_result > 0:
            normalized_coef = coef_result
            exp_adjust = 0
            while normalized_coef < 1:
                normalized_coef *= 10
                exp_adjust -= 1
            normalized_exp = exp_result + exp_adjust
            normalized_str = f"{normalized_coef} × 10^{normalized_exp}"
            steps.append(f"Normalizing: {normalized_str}")
            return normalized_str
        else:
            return result_str
