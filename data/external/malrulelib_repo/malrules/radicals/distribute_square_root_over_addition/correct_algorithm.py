"""
Correct algorithm for square root of sum of squares.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class SquareRootSimplificationCorrectAlgorithm(CorrectAlgorithm):
    """Correctly evaluates √(a²+b²) by simplifying inside first."""

    def get_name(self) -> str:
        return "Correct Square Root Simplification"

    def get_description(self) -> str:
        return "Correctly simplifies radicals by computing inside the radical first."

    def _generate_concise_steps(self, problem: Problem, problem_type: str, **kwargs) -> List[str]:
        """Generate concise steps with only formulas and values."""
        steps = []
        steps.append(f"Question: {problem.text}")

        if problem_type == 'basic_sum_of_squares':
            a = kwargs['a']
            b = kwargs['b']
            a_squared = kwargs['a_squared']
            b_squared = kwargs['b_squared']
            sum_of_squares = kwargs['sum_of_squares']
            correct_answer = kwargs['correct_answer']
            steps.append(f"√({a}² + {b}²)")
            steps.append(f"{a}² = {a_squared}")
            steps.append(f"{b}² = {b_squared}")
            steps.append(f"{a_squared} + {b_squared} = {sum_of_squares}")
            steps.append(f"√{sum_of_squares} = {correct_answer:.2f}")
            steps.append(f"Answer: {correct_answer:.2f}")

        elif problem_type == 'pythagorean_context':
            a = kwargs['a']
            b = kwargs['b']
            a_squared = kwargs['a_squared']
            b_squared = kwargs['b_squared']
            sum_of_squares = kwargs['sum_of_squares']
            correct_answer = kwargs['correct_answer']
            steps.append(f"c² = a² + b² = {a}² + {b}²")
            steps.append(f"{a}² = {a_squared}")
            steps.append(f"{b}² = {b_squared}")
            steps.append(f"{a_squared} + {b_squared} = {sum_of_squares}")
            steps.append(f"c = √{sum_of_squares} = {correct_answer:.2f}")
            steps.append(f"Answer: {correct_answer:.2f}")

        elif problem_type in ['algebraic_expression', 'algebraic_word_problem']:
            const = kwargs['const']
            x_val = kwargs['x_val']
            x_squared = kwargs['x_squared']
            sum_value = kwargs['sum_value']
            correct_answer = kwargs['correct_answer']
            steps.append(f"√(x² + {const}) where x = {x_val}")
            steps.append(f"x² = {x_val}² = {x_squared}")
            steps.append(f"{x_squared} + {const} = {sum_value}")
            steps.append(f"√{sum_value} = {correct_answer:.2f}")
            steps.append(f"Answer: {correct_answer:.2f}")

        elif problem_type in ['subtraction_variant', 'subtraction_word_problem']:
            a = kwargs['a']
            b = kwargs['b']
            a_squared = kwargs['a_squared']
            b_squared = kwargs['b_squared']
            diff_of_squares = kwargs['diff_of_squares']
            correct_answer = kwargs['correct_answer']
            steps.append(f"√({a}² - {b}²)")
            steps.append(f"{a}² = {a_squared}")
            steps.append(f"{b}² = {b_squared}")
            steps.append(f"{a_squared} - {b_squared} = {diff_of_squares}")
            steps.append(f"√{diff_of_squares} = {correct_answer:.2f}")
            steps.append(f"Answer: {correct_answer:.2f}")

        elif problem_type == 'non_perfect_square':
            a = kwargs['a']
            b = kwargs['b']
            a_squared = kwargs['a_squared']
            b_squared = kwargs['b_squared']
            sum_of_squares = kwargs['sum_of_squares']
            correct_answer = kwargs['correct_answer']
            steps.append(f"√({a}² + {b}²)")
            steps.append(f"{a}² = {a_squared}")
            steps.append(f"{b}² = {b_squared}")
            steps.append(f"{a_squared} + {b_squared} = {sum_of_squares}")
            steps.append(f"√{sum_of_squares} = {correct_answer:.4f}")
            steps.append(f"Answer: {correct_answer:.4f}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, problem_type: str, **kwargs) -> List[str]:
        """Generate verbose steps with full explanations (original format)."""
        steps = []

        if problem_type == 'basic_sum_of_squares':
            a = kwargs['a']
            b = kwargs['b']
            a_squared = kwargs['a_squared']
            b_squared = kwargs['b_squared']
            sum_of_squares = kwargs['sum_of_squares']
            correct_answer = kwargs['correct_answer']
            malrule_answer = kwargs['malrule_answer']

            steps.append(f"Problem: Simplify √({a}² + {b}²)")
            steps.append("")
            steps.append("CORRECT METHOD: Simplify INSIDE the radical first")
            steps.append("  Square root does NOT distribute over addition!")
            steps.append("")
            steps.append(f"Step 1: Calculate {a}²")
            steps.append(f"  {a}² = {a_squared}")
            steps.append("")
            steps.append(f"Step 2: Calculate {b}²")
            steps.append(f"  {b}² = {b_squared}")
            steps.append("")
            steps.append(f"Step 3: Add the squares")
            steps.append(f"  {a_squared} + {b_squared} = {sum_of_squares}")
            steps.append("")
            steps.append(f"Step 4: Take square root of the sum")
            steps.append(f"  √{sum_of_squares} = {correct_answer:.2f}")
            steps.append("")
            if correct_answer == int(correct_answer):
                steps.append(f"Final Answer: √({a}² + {b}²) = {int(correct_answer)} ✓")
                steps.append(f"  Note: This is a Pythagorean triple! ({a}, {b}, {int(correct_answer)})")
            else:
                steps.append(f"Final Answer: √({a}² + {b}²) = {correct_answer:.2f} ✓")
            steps.append("")
            steps.append(f"If we incorrectly distributed: √({a}²) + √({b}²) = {a} + {b} = {malrule_answer}")
            steps.append(f"  This is WRONG! {correct_answer:.2f} ≠ {malrule_answer}")

        elif problem_type == 'pythagorean_context':
            a = kwargs['a']
            b = kwargs['b']
            a_squared = kwargs['a_squared']
            b_squared = kwargs['b_squared']
            sum_of_squares = kwargs['sum_of_squares']
            correct_answer = kwargs['correct_answer']
            malrule_answer = kwargs['malrule_answer']

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("CORRECT METHOD: Use Pythagorean theorem")
            steps.append(f"  c² = a² + b² = {a}² + {b}²")
            steps.append("  Square root does NOT distribute!")
            steps.append("")
            steps.append(f"Step 1: Calculate {a}²")
            steps.append(f"  {a}² = {a_squared}")
            steps.append("")
            steps.append(f"Step 2: Calculate {b}²")
            steps.append(f"  {b}² = {b_squared}")
            steps.append("")
            steps.append(f"Step 3: Add: {a_squared} + {b_squared} = {sum_of_squares}")
            steps.append("")
            steps.append(f"Step 4: Take square root")
            steps.append(f"  √{sum_of_squares} = {correct_answer:.2f}")
            steps.append("")
            if correct_answer == int(correct_answer):
                steps.append(f"Final Answer: {int(correct_answer)} ✓")
            else:
                steps.append(f"Final Answer: {correct_answer:.2f} ✓")
            steps.append("")
            steps.append(f"WRONG approach: {a} + {b} = {malrule_answer}")
            steps.append(f"  Cannot simply add the sides!")

        elif problem_type in ['algebraic_expression', 'algebraic_word_problem']:
            const = kwargs['const']
            const_root = kwargs['const_root']
            x_val = kwargs['x_val']
            x_squared = kwargs['x_squared']
            sum_value = kwargs['sum_value']
            correct_answer = kwargs['correct_answer']
            malrule_expression = kwargs['malrule_expression']

            steps.append(f"Problem: Simplify √(x² + {const})")
            steps.append("")
            steps.append("CORRECT METHOD: Cannot simplify further in general form")
            steps.append(f"  √(x² + k) ≠ x + √k")
            steps.append("")
            steps.append(f"If we substitute x = {x_val} to evaluate:")
            steps.append(f"  √({x_val}² + {const})")
            steps.append(f"  = √({x_squared} + {const})")
            steps.append(f"  = √{sum_value}")
            steps.append(f"  = {correct_answer:.2f}")
            steps.append("")
            steps.append(f"Final Answer: √(x² + {const}) cannot be simplified")
            steps.append(f"  For x = {x_val}: answer is {correct_answer:.2f} ✓")
            steps.append("")
            steps.append(f"WRONG: √(x² + {const}) ≠ x + {const_root}")
            steps.append(f"  For x = {x_val}: {x_val} + {const_root} = {malrule_expression}")
            steps.append(f"  But correct answer is {correct_answer:.2f}")

        elif problem_type in ['subtraction_variant', 'subtraction_word_problem']:
            a = kwargs['a']
            b = kwargs['b']
            a_squared = kwargs['a_squared']
            b_squared = kwargs['b_squared']
            diff_of_squares = kwargs['diff_of_squares']
            correct_answer = kwargs['correct_answer']
            malrule_answer = kwargs['malrule_answer']

            steps.append(f"Problem: Simplify √({a}² - {b}²)")
            steps.append("")
            steps.append("CORRECT METHOD: Simplify INSIDE first")
            steps.append("  √(a² - b²) ≠ a - b")
            steps.append("")
            steps.append(f"Step 1: Calculate {a}²")
            steps.append(f"  {a}² = {a_squared}")
            steps.append("")
            steps.append(f"Step 2: Calculate {b}²")
            steps.append(f"  {b}² = {b_squared}")
            steps.append("")
            steps.append(f"Step 3: Subtract: {a_squared} - {b_squared} = {diff_of_squares}")
            steps.append("")
            steps.append(f"Step 4: Take square root")
            steps.append(f"  √{diff_of_squares} = {correct_answer:.2f}")
            steps.append("")
            if correct_answer == int(correct_answer):
                steps.append(f"Final Answer: √({a}² - {b}²) = {int(correct_answer)} ✓")
            else:
                steps.append(f"Final Answer: √({a}² - {b}²) = {correct_answer:.2f} ✓")
            steps.append("")
            steps.append(f"WRONG: {a} - {b} = {malrule_answer}")
            steps.append(f"  Cannot distribute square root over subtraction!")

        elif problem_type == 'non_perfect_square':
            a = kwargs['a']
            b = kwargs['b']
            a_squared = kwargs['a_squared']
            b_squared = kwargs['b_squared']
            sum_of_squares = kwargs['sum_of_squares']
            correct_answer = kwargs['correct_answer']
            malrule_answer = kwargs['malrule_answer']

            steps.append(f"Problem: Simplify √({a}² + {b}²)")
            steps.append("")
            steps.append("CORRECT METHOD: Simplify inside first")
            steps.append("  Note: This is NOT a Pythagorean triple")
            steps.append("")
            steps.append(f"Step 1: {a}² = {a_squared}")
            steps.append(f"Step 2: {b}² = {b_squared}")
            steps.append(f"Step 3: {a_squared} + {b_squared} = {sum_of_squares}")
            steps.append(f"Step 4: √{sum_of_squares} = {correct_answer:.4f}")
            steps.append("")
            steps.append(f"Final Answer: √({a}² + {b}²) = √{sum_of_squares} ≈ {correct_answer:.4f} ✓")
            steps.append(f"  This is irrational (cannot be simplified to an integer)")
            steps.append("")
            steps.append(f"WRONG: {a} + {b} = {malrule_answer}")
            steps.append(f"  Error is obvious: {correct_answer:.4f} ≠ {malrule_answer}")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        problem_type = problem.metadata.get('problem_type', 'basic_sum_of_squares')

        # Handle enhanced problem types
        if problem_type == 'pythagorean_context':
            return self._handle_pythagorean_context(problem, verbose)
        elif problem_type == 'algebraic_expression':
            return self._handle_algebraic_expression(problem, verbose)
        elif problem_type == 'subtraction_variant':
            return self._handle_subtraction_variant(problem, verbose)
        elif problem_type == 'non_perfect_square':
            return self._handle_non_perfect_square(problem, verbose)
        elif problem_type == 'subtraction_word_problem':
            return self._handle_subtraction_variant(problem, verbose)
        elif problem_type == 'algebraic_word_problem':
            return self._handle_algebraic_expression(problem, verbose)

        # Original basic problem type
        a = problem.metadata['a']
        b = problem.metadata['b']
        a_squared = a ** 2
        b_squared = b ** 2
        sum_of_squares = a_squared + b_squared

        # COMPUTE answer independently
        correct_answer = sum_of_squares ** 0.5
        malrule_answer = a + b

        # Generate steps based on verbose flag
        step_kwargs = {
            'a': a,
            'b': b,
            'a_squared': a_squared,
            'b_squared': b_squared,
            'sum_of_squares': sum_of_squares,
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, problem_type, **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, problem_type, **step_kwargs)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _handle_pythagorean_context(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle Pythagorean theorem word problems."""
        a = problem.metadata['a']
        b = problem.metadata['b']

        # COMPUTE values independently
        a_squared = a ** 2
        b_squared = b ** 2
        sum_of_squares = a_squared + b_squared
        correct_answer = sum_of_squares ** 0.5
        malrule_answer = a + b

        # Generate steps based on verbose flag
        step_kwargs = {
            'a': a,
            'b': b,
            'a_squared': a_squared,
            'b_squared': b_squared,
            'sum_of_squares': sum_of_squares,
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, 'pythagorean_context', **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, 'pythagorean_context', **step_kwargs)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _handle_algebraic_expression(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle algebraic expressions like √(x²+9)."""
        const = problem.metadata['constant']
        const_root = int(const ** 0.5)
        x_val = problem.metadata['x_value']

        # COMPUTE values independently
        x_squared = x_val ** 2
        sum_value = x_squared + const
        correct_answer = sum_value ** 0.5
        malrule_expression = x_val + const_root

        # Generate steps based on verbose flag
        step_kwargs = {
            'const': const,
            'const_root': const_root,
            'x_val': x_val,
            'x_squared': x_squared,
            'sum_value': sum_value,
            'correct_answer': correct_answer,
            'malrule_expression': malrule_expression
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, 'algebraic_expression', **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, 'algebraic_expression', **step_kwargs)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _handle_subtraction_variant(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle √(a²-b²) subtraction variant."""
        a = problem.metadata['a']
        b = problem.metadata['b']

        # COMPUTE values independently
        a_squared = a ** 2
        b_squared = b ** 2
        diff_of_squares = a_squared - b_squared
        correct_answer = diff_of_squares ** 0.5
        malrule_answer = a - b

        # Generate steps based on verbose flag
        step_kwargs = {
            'a': a,
            'b': b,
            'a_squared': a_squared,
            'b_squared': b_squared,
            'diff_of_squares': diff_of_squares,
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, 'subtraction_variant', **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, 'subtraction_variant', **step_kwargs)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _handle_non_perfect_square(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle non-perfect square results."""
        a = problem.metadata['a']
        b = problem.metadata['b']

        # COMPUTE values independently
        a_squared = a ** 2
        b_squared = b ** 2
        sum_of_squares = a_squared + b_squared
        correct_answer = sum_of_squares ** 0.5
        malrule_answer = a + b

        # Generate steps based on verbose flag
        step_kwargs = {
            'a': a,
            'b': b,
            'a_squared': a_squared,
            'b_squared': b_squared,
            'sum_of_squares': sum_of_squares,
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, 'non_perfect_square', **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, 'non_perfect_square', **step_kwargs)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
