"""
Malrule algorithm for Scalar-Multiplication-Inside-Or-Outside-Same.

Students confuse input multiplication with output multiplication: f(cx) = c·f(x)
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import Malrule, Problem, Solution

class ScalarMultiplicationInsideOrOutsideSameMalrule(Malrule):
    """Student treats f(cx) as equivalent to c·f(x)."""

    def get_name(self):
        return "Illusion-of-Linearity-Multiplicative"

    def get_description(self):
        return (
            "Student incorrectly applies the multiplicative (homogeneous) property of linear "
            "functions to nonlinear functions: f(cx) = c·f(x). This is a manifestation of the "
            "'illusion of linearity' (De Bock et al., 2007), where students overgeneralize "
            "properties that hold only for linear functions f(x) = kx. Matz (1982) identified "
            "f(ka) = kf(a) as a common algebraic error."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Malrule: incorrectly factor out scalar f(cx) = c·f(x)
        return problem.metadata['malrule_answer']

    def _generate_concise_steps(self, problem: Problem, template: str, malrule_answer) -> List[str]:
        """Generate concise steps with only formulas and values."""
        c = problem.metadata['scalar']
        x = problem.metadata['input']

        steps = []

        if template == 'word_problem':
            steps.append(f"{problem.text}")

        if template == 'quadratic_function':
            steps.append(f"f(x) = x², evaluate f({c}×{x})")
            steps.append(f"f({c}×{x}) = {c} · f({x})")
            steps.append(f"= {c} · ({x})²")
            steps.append(f"= {c} · {x**2}")
            steps.append(f"= {malrule_answer}")
        elif template == 'cubic_function':
            steps.append(f"f(x) = x³, evaluate f({c}×{x})")
            steps.append(f"f({c}×{x}) = {c} · f({x})")
            steps.append(f"= {c} · ({x})³")
            steps.append(f"= {c} · {x**3}")
            steps.append(f"= {malrule_answer}")
        elif template == 'absolute_value':
            a = problem.metadata['shift']
            steps.append(f"f(x) = |x + {a}|, evaluate f({c}×{x})")
            steps.append(f"f({c}×{x}) = {c} · f({x})")
            steps.append(f"= {c} · |{x} + {a}|")
            steps.append(f"= {c} · {abs(x + a)}")
            steps.append(f"= {malrule_answer}")
        elif template == 'square_root':
            steps.append(f"f(x) = √x, evaluate f({c}×{x})")
            steps.append(f"f({c}×{x}) = {c} · f({x})")
            steps.append(f"= {c} · √{x}")
            steps.append(f"= {c} · {x**0.5}")
            steps.append(f"= {malrule_answer}")
        elif template == 'word_problem':
            word_problem_type = problem.metadata.get('word_problem_type', problem.metadata.get('context_type', 'quadratic_function'))
            steps.append(f"f({c}×{x}) = {c} · f({x})")
            if word_problem_type in ['quadratic_function', 'square_area', 'energy']:
                steps.append(f"= {c} · ({x})²")
                steps.append(f"= {c} · {x**2}")
                steps.append(f"= {malrule_answer}")
            elif word_problem_type in ['cubic_function', 'cube_volume']:
                steps.append(f"= {c} · ({x})³")
                steps.append(f"= {c} · {x**3}")
                steps.append(f"= {malrule_answer}")
            elif word_problem_type == 'absolute_value':
                a = problem.metadata.get('shift', 0)
                steps.append(f"= {c} · |{x} + {a}|")
                steps.append(f"= {c} · {abs(x + a)}")
                steps.append(f"= {malrule_answer}")
            elif word_problem_type == 'square_root':
                steps.append(f"= {c} · √{x}")
                steps.append(f"= {c} · {x**0.5}")
                steps.append(f"= {malrule_answer}")

        steps.append(f"{malrule_answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, template: str, malrule_answer) -> List[str]:
        """Generate verbose steps with full explanations (original format)."""
        c = problem.metadata['scalar']
        x = problem.metadata['input']
        function = problem.metadata['function']

        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: Factor out the scalar (treating input and output multiplication as the same)")
        steps.append("")

        if template == 'quadratic_function':
            steps.append(f"  f({c}×{x}) = {c} · f({x})  [WRONG! Can't factor out scalar from input]")
            steps.append(f"  = {c} · ({x})²")
            steps.append(f"  = {c} · {x**2}")
            steps.append(f"  = {malrule_answer}")
            steps.append("")
            steps.append(f"Student's answer: {malrule_answer}")
            steps.append("")
            steps.append(
                f"WRONG! The student incorrectly assumes f({c}×{x}) = {c}·f({x}). "
                f"This confuses input multiplication (horizontal scaling) with "
                f"output multiplication (vertical scaling)."
            )

        elif template == 'cubic_function':
            steps.append(f"  f({c}×{x}) = {c} · f({x})  [WRONG! Can't factor out scalar from input]")
            steps.append(f"  = {c} · ({x})³")
            steps.append(f"  = {c} · {x**3}")
            steps.append(f"  = {malrule_answer}")
            steps.append("")
            steps.append(f"Student's answer: {malrule_answer}")
            steps.append("")
            steps.append(
                f"WRONG! For cubic functions, f({c}×{x}) ≠ {c}·f({x}). "
                f"The student treats input multiplication as output multiplication."
            )

        elif template == 'absolute_value':
            a = problem.metadata['shift']
            steps.append(f"  f({c}×{x}) = {c} · f({x})  [WRONG! Can't factor out scalar from input]")
            steps.append(f"  = {c} · |{x} + {a}|")
            steps.append(f"  = {c} · {abs(x + a)}")
            steps.append(f"  = {malrule_answer}")
            steps.append("")
            steps.append(f"Student's answer: {malrule_answer}")
            steps.append("")
            steps.append(
                f"WRONG! With f(x) = |x + {a}|, we have f({c}×{x}) = |{c}×{x} + {a}| = {abs(c*x + a)}, "
                f"NOT {c}·|{x} + {a}| = {malrule_answer}. The student confuses input and output multiplication."
            )

        elif template == 'square_root':
            steps.append(f"  f({c}×{x}) = {c} · f({x})  [WRONG! Can't factor out scalar from input]")
            steps.append(f"  = {c} · √{x}")
            steps.append(f"  = {c} · {x**0.5}")
            steps.append(f"  = {malrule_answer}")
            steps.append("")
            steps.append(f"Student's answer: {malrule_answer}")
            steps.append("")
            steps.append(
                f"WRONG! For square root functions, f({c}×{x}) = √({c}×{x}) = √{c*x}, "
                f"NOT {c}·√{x} = {malrule_answer}. These give different results!"
            )

        elif template == 'word_problem':
            word_problem_type = problem.metadata.get('word_problem_type', problem.metadata.get('context_type', 'quadratic_function'))
            steps.append(f"  Student incorrectly factors out the scalar:")
            steps.append(f"  When input is {c}×{x}, student thinks:")
            steps.append(f"  f({c}×{x}) = {c} · f({x})")
            steps.append(f"  = {c} · {function.replace('s', str(x)).replace('m', str(x))}")
            if word_problem_type in ['quadratic_function', 'square_area', 'energy']:
                steps.append(f"  = {c} · {x}²  = {c} · {x**2}")
            elif word_problem_type in ['cubic_function', 'cube_volume']:
                steps.append(f"  = {c} · {x}³  = {c} · {x**3}")
            elif word_problem_type == 'absolute_value':
                a = problem.metadata.get('shift', 0)
                steps.append(f"  = {c} · |{x} + {a}|  = {c} · {abs(x + a)}")
            elif word_problem_type == 'square_root':
                steps.append(f"  = {c} · √{x}  = {c} · {x**0.5}")
            steps.append(f"  = {malrule_answer}")
            steps.append("")
            steps.append(f"Student's answer: {malrule_answer}")
            steps.append("")
            steps.append(
                f"WRONG! The student treats the input multiplication as output multiplication. "
                f"When the input changes from {x} to {c}×{x}, you must substitute the ENTIRE "
                f"value into the function, not factor out the scalar."
            )

        steps.append("")
        steps.append(
            "The fundamental error: Confusing f(cx) with c·f(x). "
            "Input multiplication and output multiplication are NOT the same!"
        )

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the scalar-multiplication-inside-or-outside-same malrule across all templates.

        Args:
            problem: The function evaluation problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution showing incorrect factoring of scalar
        """
        template = problem.metadata.get('template', 'quadratic_function')
        c = problem.metadata['scalar']
        x = problem.metadata['input']

        # ACTUALLY COMPUTE THE MALRULE ANSWER
        # Student incorrectly factors out scalar: f(c×x) = c·f(x)
        if template == 'quadratic_function':
            # f(x) = x², malrule: f(c×x) = c·f(x) = c·x²
            malrule_answer = c * (x ** 2)
        elif template == 'cubic_function':
            # f(x) = x³, malrule: f(c×x) = c·f(x) = c·x³
            malrule_answer = c * (x ** 3)
        elif template == 'absolute_value':
            # f(x) = |x + a|, malrule: f(c×x) = c·f(x) = c·|x + a|
            a = problem.metadata['shift']
            malrule_answer = c * abs(x + a)
        elif template == 'square_root':
            # f(x) = √x, malrule: f(c×x) = c·f(x) = c·√x
            malrule_answer = c * (x ** 0.5)
        elif template == 'word_problem':
            # Route based on word_problem_type
            word_problem_type = problem.metadata.get('word_problem_type', problem.metadata.get('context_type', 'quadratic_function'))
            if word_problem_type in ['quadratic_function', 'square_area', 'energy']:
                malrule_answer = c * (x ** 2)
            elif word_problem_type in ['cubic_function', 'cube_volume']:
                malrule_answer = c * (x ** 3)
            elif word_problem_type == 'absolute_value':
                a = problem.metadata.get('shift', 0)
                malrule_answer = c * abs(x + a)
            elif word_problem_type == 'square_root':
                malrule_answer = c * (x ** 0.5)
            else:
                malrule_answer = c * (x ** 2)
        else:
            # Default fallback
            malrule_answer = c * (x ** 2)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, template, malrule_answer)
        else:
            steps = self._generate_concise_steps(problem, template, malrule_answer)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
