"""
Correct algorithm for function evaluation with scalar multiplication.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class FunctionEvaluationCorrectAlgorithm(CorrectAlgorithm):
    """Correctly evaluates f(cx) by substituting cx into the function."""

    def get_name(self):
        return "Function Evaluation"

    def get_description(self):
        return "Evaluates f(cx) by substituting the entire expression cx for x"

    def _generate_concise_steps(self, problem: Problem, template: str, correct_answer) -> List[str]:
        """Generate concise steps with only formulas and values."""
        c = problem.metadata['scalar']
        x = problem.metadata['input']

        steps = []

        if template == 'word_problem':
            steps.append(f"{problem.text}")

        if template == 'quadratic_function':
            steps.append(f"f(x) = x², evaluate f({c}×{x})")
            steps.append(f"f({c}×{x}) = ({c}×{x})²")
            steps.append(f"= ({c*x})²")
            steps.append(f"= {correct_answer}")
        elif template == 'cubic_function':
            steps.append(f"f(x) = x³, evaluate f({c}×{x})")
            steps.append(f"f({c}×{x}) = ({c}×{x})³")
            steps.append(f"= ({c*x})³")
            steps.append(f"= {correct_answer}")
        elif template == 'absolute_value':
            a = problem.metadata['shift']
            steps.append(f"f(x) = |x + {a}|, evaluate f({c}×{x})")
            steps.append(f"f({c}×{x}) = |{c}×{x} + {a}|")
            steps.append(f"= |{c*x} + {a}|")
            steps.append(f"= {correct_answer}")
        elif template == 'square_root':
            steps.append(f"f(x) = √x, evaluate f({c}×{x})")
            steps.append(f"f({c}×{x}) = √({c}×{x})")
            steps.append(f"= √{c*x}")
            steps.append(f"= {correct_answer}")
        elif template == 'word_problem':
            word_problem_type = problem.metadata.get('word_problem_type', problem.metadata.get('context_type', 'quadratic_function'))
            if word_problem_type in ['quadratic_function', 'square_area', 'energy']:
                steps.append(f"f({c}×{x}) = ({c}×{x})²")
                steps.append(f"= ({c*x})²")
                steps.append(f"= {correct_answer}")
            elif word_problem_type in ['cubic_function', 'cube_volume']:
                steps.append(f"f({c}×{x}) = ({c}×{x})³")
                steps.append(f"= ({c*x})³")
                steps.append(f"= {correct_answer}")
            elif word_problem_type == 'absolute_value':
                a = problem.metadata.get('shift', 0)
                steps.append(f"f({c}×{x}) = |{c}×{x} + {a}|")
                steps.append(f"= |{c*x} + {a}|")
                steps.append(f"= {correct_answer}")
            elif word_problem_type == 'square_root':
                steps.append(f"f({c}×{x}) = √({c}×{x})")
                steps.append(f"= √{c*x}")
                steps.append(f"= {correct_answer}")

        steps.append(f"{correct_answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, template: str, correct_answer) -> List[str]:
        """Generate verbose steps with full explanations (original format)."""
        c = problem.metadata['scalar']
        x = problem.metadata['input']

        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD: Substitute the entire expression")
        steps.append("")

        if template == 'quadratic_function':
            steps.append(f"  f({c}×{x}) means substitute '{c}×{x}' for 'x' in f(x) = x²")
            steps.append(f"  f({c}×{x}) = ({c}×{x})²")
            steps.append(f"  = ({c*x})²")
            steps.append(f"  = {correct_answer}")
            steps.append("")
            steps.append("Comparison:")
            steps.append(f"  f({c}×{x}) = {correct_answer} ✓ (correct: substitute entire input)")
            steps.append(f"  {c}·f({x}) = {c}·{x**2} = {c * x**2} ✗ (wrong: factor out scalar)")

        elif template == 'cubic_function':
            steps.append(f"  f({c}×{x}) means substitute '{c}×{x}' for 'x' in f(x) = x³")
            steps.append(f"  f({c}×{x}) = ({c}×{x})³")
            steps.append(f"  = ({c*x})³")
            steps.append(f"  = {correct_answer}")
            steps.append("")
            steps.append("Comparison:")
            steps.append(f"  f({c}×{x}) = {correct_answer} ✓ (correct)")
            steps.append(f"  {c}·f({x}) = {c}·{x**3} = {c * x**3} ✗ (wrong)")

        elif template == 'absolute_value':
            a = problem.metadata['shift']
            steps.append(f"  f({c}×{x}) means substitute '{c}×{x}' for 'x' in f(x) = |x + {a}|")
            steps.append(f"  f({c}×{x}) = |{c}×{x} + {a}|")
            steps.append(f"  = |{c*x} + {a}|")
            steps.append(f"  = {correct_answer}")
            steps.append("")
            steps.append("Comparison:")
            steps.append(f"  f({c}×{x}) = |{c*x} + {a}| = {correct_answer} ✓ (correct)")
            steps.append(f"  {c}·f({x}) = {c}·|{x} + {a}| = {c}·{abs(x + a)} = {c * abs(x + a)} ✗ (wrong)")

        elif template == 'square_root':
            steps.append(f"  f({c}×{x}) means substitute '{c}×{x}' for 'x' in f(x) = √x")
            steps.append(f"  f({c}×{x}) = √({c}×{x})")
            steps.append(f"  = √{c*x}")
            steps.append(f"  = {correct_answer}")
            steps.append("")
            steps.append("Comparison:")
            steps.append(f"  f({c}×{x}) = √{c*x} = {correct_answer} ✓ (correct)")
            steps.append(f"  {c}·f({x}) = {c}·√{x} = {c}·{x**0.5} = {c * x**0.5} ✗ (wrong)")

        elif template == 'word_problem':
            word_problem_type = problem.metadata.get('word_problem_type', problem.metadata.get('context_type', 'quadratic_function'))
            steps.append(f"  Substitute the entire expression {c}×{x} into the function")

            if word_problem_type in ['quadratic_function', 'square_area', 'energy']:
                steps.append(f"  f({c}×{x}) = ({c}×{x})²")
                steps.append(f"  = ({c*x})²")
                steps.append(f"  = {correct_answer} square units")
            elif word_problem_type in ['cubic_function', 'cube_volume']:
                steps.append(f"  f({c}×{x}) = ({c}×{x})³")
                steps.append(f"  = ({c*x})³")
                steps.append(f"  = {correct_answer} cubic units")
            elif word_problem_type == 'absolute_value':
                a = problem.metadata.get('shift', 0)
                steps.append(f"  f({c}×{x}) = |({c}×{x}) + {a}|")
                steps.append(f"  = |{c*x} + {a}|")
                steps.append(f"  = {correct_answer} units")
            elif word_problem_type == 'square_root':
                steps.append(f"  f({c}×{x}) = √({c}×{x})")
                steps.append(f"  = √{c*x}")
                steps.append(f"  = {correct_answer}")

            steps.append("")
            steps.append("Comparison:")
            steps.append(f"  f({c}×{x}) = {correct_answer} ✓ (substitute entire input)")
            if word_problem_type in ['cubic_function', 'cube_volume']:
                steps.append(f"  {c}·f({x}) = {c}·{x**3} = {c * x**3} ✗ (incorrect factoring)")
            elif word_problem_type == 'absolute_value':
                a = problem.metadata.get('shift', 0)
                steps.append(f"  {c}·f({x}) = {c}·|{x} + {a}| = {c * abs(x + a)} ✗ (incorrect factoring)")
            elif word_problem_type == 'square_root':
                steps.append(f"  {c}·f({x}) = {c}·√{x} = {c}·{x**0.5} = {c * x**0.5} ✗ (incorrect factoring)")
            else:
                steps.append(f"  {c}·f({x}) = {c}·{x**2} = {c * x**2} ✗ (incorrect factoring)")

        steps.append("")
        steps.append(f"Answer: {correct_answer}")
        steps.append("")
        steps.append("Remember: f(cx) ≠ c·f(x) for most functions!")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct function evaluation algorithm across all templates.

        Args:
            problem: The function evaluation problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution showing correct substitution
        """
        template = problem.metadata.get('template', 'quadratic_function')
        c = problem.metadata['scalar']
        x = problem.metadata['input']

        # ACTUALLY COMPUTE THE ANSWER based on template
        if template == 'quadratic_function':
            # f(x) = x², f(c×x) = (c×x)²
            correct_answer = (c * x) ** 2
        elif template == 'cubic_function':
            # f(x) = x³, f(c×x) = (c×x)³
            correct_answer = (c * x) ** 3
        elif template == 'absolute_value':
            # f(x) = |x + a|, f(c×x) = |c×x + a|
            a = problem.metadata['shift']
            correct_answer = abs(c * x + a)
        elif template == 'square_root':
            # f(x) = √x, f(c×x) = √(c×x)
            correct_answer = (c * x) ** 0.5
        elif template == 'word_problem':
            # Route based on word_problem_type
            word_problem_type = problem.metadata.get('word_problem_type', problem.metadata.get('context_type', 'quadratic_function'))
            if word_problem_type in ['quadratic_function', 'square_area', 'energy']:
                correct_answer = (c * x) ** 2
            elif word_problem_type in ['cubic_function', 'cube_volume']:
                correct_answer = (c * x) ** 3
            elif word_problem_type == 'absolute_value':
                a = problem.metadata.get('shift', 0)
                correct_answer = abs(c * x + a)
            elif word_problem_type == 'square_root':
                correct_answer = (c * x) ** 0.5
            else:
                correct_answer = (c * x) ** 2
        else:
            # Default fallback
            correct_answer = (c * x) ** 2

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, template, correct_answer)
        else:
            steps = self._generate_concise_steps(problem, template, correct_answer)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
