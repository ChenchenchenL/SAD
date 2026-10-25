"""
Correct algorithm for function evaluation.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class FunctionEvaluationCorrectAlgorithm(CorrectAlgorithm):
    """Correctly evaluates functions by substituting input for variable."""

    def get_name(self) -> str:
        return "Correct Function Evaluation"

    def get_description(self) -> str:
        return "Correctly evaluates functions by substituting the input value for the variable."

    def _generate_concise_steps(self, problem: Problem, problem_type: str) -> List[str]:
        """Generate concise steps with only formulas and values."""
        steps = []

        if problem_type == 'simple_linear':
            a = problem.metadata['coefficient']
            b = problem.metadata['constant']
            x = problem.metadata['input']
            correct_answer = a * x + b

            steps.append(f"f(x) = {a}x + {b}, find f({x})")
            steps.append(f"f({x}) = {a}({x}) + {b} = {a * x} + {b} = {correct_answer}")
            steps.append(f"{correct_answer}")

        elif problem_type == 'quadratic_function':
            a = problem.metadata['coefficient']
            b_coeff = problem.metadata.get('b_coefficient', 0)
            c = problem.metadata.get('c_constant', problem.metadata.get('constant', 0))
            x = problem.metadata['input']
            correct_answer = a * (x ** 2) + b_coeff * x + c
            b_sign = '+' if b_coeff >= 0 else ''
            c_sign = '+' if c >= 0 else ''

            steps.append(f"f(x) = {a}x² {b_sign} {b_coeff}x {c_sign} {c}, find f({x})")
            steps.append(f"f({x}) = {a}({x})² {b_sign} {b_coeff}({x}) {c_sign} {c}")
            steps.append(f"f({x}) = {a * (x**2)} {b_sign} {b_coeff * x} {c_sign} {c} = {correct_answer}")
            steps.append(f"{correct_answer}")

        elif problem_type == 'function_composition':
            a = problem.metadata['coefficient']
            b = problem.metadata['constant']
            c = problem.metadata['g_coefficient']
            d = problem.metadata['g_constant']
            x = problem.metadata['input']
            g_of_x = c * x + d
            correct_answer = a * g_of_x + b

            steps.append(f"f(x) = {a}x + {b}, g(x) = {c}x + {d}, find f(g({x}))")
            steps.append(f"g({x}) = {c}({x}) + {d} = {g_of_x}")
            steps.append(f"f({g_of_x}) = {a}({g_of_x}) + {b} = {a * g_of_x} + {b} = {correct_answer}")
            steps.append(f"{correct_answer}")

        elif problem_type == 'absolute_value_function':
            a = problem.metadata['coefficient']
            b = problem.metadata['constant']
            x = problem.metadata['input']
            inner_value = a * x + b
            correct_answer = abs(inner_value)
            b_sign = '+' if b >= 0 else ''

            steps.append(f"f(x) = |{a}x {b_sign} {b}|, find f({x})")
            steps.append(f"f({x}) = |{a}({x}) {b_sign} {b}| = |{inner_value}| = {correct_answer}")
            steps.append(f"{correct_answer}")

        elif problem_type == 'word_problem_context':
            word_problem_type = problem.metadata.get('word_problem_type', 'simple_linear')
            steps.append(f"{problem.text}")
            # Route to underlying formula type
            if word_problem_type == 'simple_linear':
                a = problem.metadata['coefficient']
                b = problem.metadata['constant']
                x = problem.metadata['input']
                correct_answer = a * x + b
                steps.append(f"f(x) = {a}x + {b}, find f({x})")
                steps.append(f"f({x}) = {a}({x}) + {b} = {a * x} + {b} = {correct_answer}")
                steps.append(f"{correct_answer}")
            elif word_problem_type == 'quadratic_function':
                a = problem.metadata['coefficient']
                b_coeff = problem.metadata.get('b_coefficient', 0)
                c = problem.metadata.get('c_constant', problem.metadata.get('constant', 0))
                x = problem.metadata['input']
                correct_answer = a * (x ** 2) + b_coeff * x + c
                b_sign = '+' if b_coeff >= 0 else ''
                c_sign = '+' if c >= 0 else ''
                steps.append(f"f(x) = {a}x² {b_sign} {b_coeff}x {c_sign} {c}, find f({x})")
                steps.append(f"f({x}) = {a}({x})² {b_sign} {b_coeff}({x}) {c_sign} {c} = {correct_answer}")
                steps.append(f"{correct_answer}")
            elif word_problem_type == 'function_composition':
                a = problem.metadata['coefficient']
                b = problem.metadata['constant']
                c = problem.metadata['g_coefficient']
                d = problem.metadata['g_constant']
                x = problem.metadata['input']
                g_of_x = c * x + d
                correct_answer = a * g_of_x + b
                steps.append(f"f(x) = {a}x + {b}, g(x) = {c}x + {d}, find f(g({x}))")
                steps.append(f"g({x}) = {g_of_x}, f({g_of_x}) = {correct_answer}")
                steps.append(f"{correct_answer}")
            elif word_problem_type == 'absolute_value_function':
                a = problem.metadata['coefficient']
                b = problem.metadata['constant']
                x = problem.metadata['input']
                inner_value = a * x + b
                correct_answer = abs(inner_value)
                b_sign = '+' if b >= 0 else ''
                steps.append(f"f(x) = |{a}x {b_sign} {b}|, find f({x})")
                steps.append(f"f({x}) = |{inner_value}| = {correct_answer}")
                steps.append(f"{correct_answer}")
            else:
                a = problem.metadata['coefficient']
                b = problem.metadata['constant']
                x = problem.metadata['input']
                correct_answer = a * x + b
                steps.append(f"f(x) = {a}x + {b}, find f({x})")
                steps.append(f"f({x}) = {correct_answer}")
                steps.append(f"{correct_answer}")
        else:
            # Default to simple linear
            a = problem.metadata['coefficient']
            b = problem.metadata['constant']
            x = problem.metadata['input']
            correct_answer = a * x + b

            steps.append(f"f(x) = {a}x + {b}, find f({x})")
            steps.append(f"f({x}) = {a}({x}) + {b} = {a * x} + {b} = {correct_answer}")
            steps.append(f"{correct_answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, problem_type: str) -> List[str]:
        """Generate verbose steps with full explanations (original format)."""
        if problem_type == 'simple_linear':
            return self._verbose_simple_linear(problem)
        elif problem_type == 'quadratic_function':
            return self._verbose_quadratic(problem)
        elif problem_type == 'function_composition':
            return self._verbose_composition(problem)
        elif problem_type == 'absolute_value_function':
            return self._verbose_absolute_value(problem)
        elif problem_type == 'word_problem_context':
            return self._verbose_word_problem(problem)
        else:
            return self._verbose_simple_linear(problem)

    def _verbose_simple_linear(self, problem: Problem) -> List[str]:
        """Verbose steps for simple linear problems."""
        a = problem.metadata['coefficient']
        b = problem.metadata['constant']
        x = problem.metadata['input']
        correct_answer = a * x + b

        steps = []
        steps.append(f"Problem: Given f(x) = {a}x + {b}, evaluate f({x})")
        steps.append("")
        steps.append("Definition: f(x) means the OUTPUT when INPUT is x")
        steps.append("  NOT multiplication! It's function notation")
        steps.append("")
        steps.append(f"Step 1: Substitute {x} for every x in the function")
        steps.append(f"  f(x) = {a}x + {b}")
        steps.append(f"  f({x}) = {a}({x}) + {b}")
        steps.append("")
        steps.append("Step 2: Evaluate the expression")
        steps.append(f"  = {a * x} + {b}")
        steps.append(f"  = {correct_answer}")
        steps.append("")
        steps.append(f"Final Answer: f({x}) = {correct_answer} ✓")
        steps.append("")
        steps.append("Remember: f(x) is NOTATION (f of x), NOT multiplication (f times x)")
        return steps

    def _verbose_quadratic(self, problem: Problem) -> List[str]:
        """Verbose steps for quadratic problems."""
        a = problem.metadata['coefficient']
        b_coeff = problem.metadata.get('b_coefficient', 0)
        c = problem.metadata.get('c_constant', problem.metadata.get('constant', 0))
        x = problem.metadata['input']
        correct_answer = a * (x ** 2) + b_coeff * x + c
        b_sign = '+' if b_coeff >= 0 else ''
        c_sign = '+' if c >= 0 else ''

        steps = []
        steps.append(f"Problem: Given f(x) = {a}x² {b_sign} {b_coeff}x {c_sign} {c}, evaluate f({x})")
        steps.append("")
        steps.append("Definition: f(x) is function notation, not multiplication")
        steps.append("")
        steps.append(f"Step 1: Substitute {x} for every x in the function")
        steps.append(f"  f({x}) = {a}({x})² {b_sign} {b_coeff}({x}) {c_sign} {c}")
        steps.append("")
        steps.append("Step 2: Evaluate each term")
        steps.append(f"  = {a} × {x**2} {b_sign} {b_coeff * x} {c_sign} {c}")
        steps.append(f"  = {a * (x**2)} {b_sign} {b_coeff * x} {c_sign} {c}")
        steps.append(f"  = {correct_answer}")
        steps.append("")
        steps.append(f"Final Answer: f({x}) = {correct_answer} ✓")
        return steps

    def _verbose_composition(self, problem: Problem) -> List[str]:
        """Verbose steps for composition problems."""
        a = problem.metadata['coefficient']
        b = problem.metadata['constant']
        c = problem.metadata['g_coefficient']
        d = problem.metadata['g_constant']
        x = problem.metadata['input']
        g_of_x = c * x + d
        correct_answer = a * g_of_x + b

        steps = []
        steps.append(f"Problem: Given f(x) = {a}x + {b} and g(x) = {c}x + {d}, evaluate f(g({x}))")
        steps.append("")
        steps.append("Step 1: Evaluate the inner function g({})".format(x))
        steps.append(f"  g({x}) = {c}({x}) + {d}")
        steps.append(f"  g({x}) = {c * x} + {d}")
        steps.append(f"  g({x}) = {g_of_x}")
        steps.append("")
        steps.append(f"Step 2: Substitute result into outer function f")
        steps.append(f"  f(g({x})) = f({g_of_x})")
        steps.append(f"  f({g_of_x}) = {a}({g_of_x}) + {b}")
        steps.append(f"  = {a * g_of_x} + {b}")
        steps.append(f"  = {correct_answer}")
        steps.append("")
        steps.append(f"Final Answer: f(g({x})) = {correct_answer} ✓")
        return steps

    def _verbose_absolute_value(self, problem: Problem) -> List[str]:
        """Verbose steps for absolute value problems."""
        a = problem.metadata['coefficient']
        b = problem.metadata['constant']
        x = problem.metadata['input']
        inner_value = a * x + b
        correct_answer = abs(inner_value)
        b_sign = '+' if b >= 0 else ''

        steps = []
        steps.append(f"Problem: Given f(x) = |{a}x {b_sign} {b}|, evaluate f({x})")
        steps.append("")
        steps.append("Step 1: Substitute {} for x".format(x))
        steps.append(f"  f({x}) = |{a}({x}) {b_sign} {b}|")
        steps.append("")
        steps.append("Step 2: Evaluate inside the absolute value")
        steps.append(f"  = |{a * x} {b_sign} {b}|")
        steps.append(f"  = |{inner_value}|")
        steps.append("")
        steps.append("Step 3: Apply absolute value")
        steps.append(f"  = {correct_answer}")
        steps.append("")
        steps.append(f"Final Answer: f({x}) = {correct_answer} ✓")
        return steps

    def _verbose_word_problem(self, problem: Problem) -> List[str]:
        """Verbose steps for word problems."""
        word_problem_type = problem.metadata.get('word_problem_type', 'simple_linear')

        steps = []
        steps.append(f"Word Problem: {problem.text}")
        steps.append("")

        if word_problem_type == 'simple_linear':
            a = problem.metadata['coefficient']
            b = problem.metadata['constant']
            x = problem.metadata['input']
            correct_answer = a * x + b

            steps.append("Step 1: Extract the mathematical function")
            steps.append(f"  Function: f(x) = {a}x + {b}")
            steps.append(f"  Need to find: f({x})")
            steps.append("")
            steps.append(f"Step 2: Substitute {x} for x")
            steps.append(f"  f({x}) = {a}({x}) + {b}")
            steps.append(f"  = {a * x} + {b}")
            steps.append(f"  = {correct_answer}")
            steps.append("")
            steps.append(f"Final Answer: {correct_answer} ✓")
        elif word_problem_type == 'quadratic_function':
            a = problem.metadata['coefficient']
            b_coeff = problem.metadata.get('b_coefficient', 0)
            c = problem.metadata.get('c_constant', problem.metadata.get('constant', 0))
            x = problem.metadata['input']
            correct_answer = a * (x ** 2) + b_coeff * x + c

            steps.append("Step 1: Extract the mathematical function")
            steps.append(f"  Function: f(x) = {a}x² + {b_coeff}x + {c}")
            steps.append(f"  Need to find: f({x})")
            steps.append("")
            steps.append(f"Step 2: Substitute and evaluate")
            steps.append(f"  f({x}) = {a}({x})² + {b_coeff}({x}) + {c}")
            steps.append(f"  = {correct_answer}")
            steps.append("")
            steps.append(f"Final Answer: {correct_answer} ✓")
        else:
            # Default linear
            a = problem.metadata['coefficient']
            b = problem.metadata['constant']
            x = problem.metadata['input']
            correct_answer = a * x + b

            steps.append(f"f(x) = {a}x + {b}, f({x}) = {correct_answer}")
            steps.append("")
            steps.append(f"Final Answer: {correct_answer} ✓")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        problem_type = problem.metadata.get('problem_type', 'simple_linear')

        # Compute the correct answer based on problem type
        if problem_type == 'simple_linear':
            a = problem.metadata['coefficient']
            b = problem.metadata['constant']
            x = problem.metadata['input']
            correct_answer = a * x + b
        elif problem_type == 'quadratic_function':
            a = problem.metadata['coefficient']
            b_coeff = problem.metadata.get('b_coefficient', 0)
            c = problem.metadata.get('c_constant', problem.metadata.get('constant', 0))
            x = problem.metadata['input']
            correct_answer = a * (x ** 2) + b_coeff * x + c
        elif problem_type == 'function_composition':
            a = problem.metadata['coefficient']
            b = problem.metadata['constant']
            c = problem.metadata['g_coefficient']
            d = problem.metadata['g_constant']
            x = problem.metadata['input']
            g_of_x = c * x + d
            correct_answer = a * g_of_x + b
        elif problem_type == 'absolute_value_function':
            a = problem.metadata['coefficient']
            b = problem.metadata['constant']
            x = problem.metadata['input']
            correct_answer = abs(a * x + b)
        elif problem_type == 'word_problem_context':
            word_problem_type = problem.metadata.get('word_problem_type', 'simple_linear')
            if word_problem_type == 'simple_linear':
                a = problem.metadata['coefficient']
                b = problem.metadata['constant']
                x = problem.metadata['input']
                correct_answer = a * x + b
            elif word_problem_type == 'quadratic_function':
                a = problem.metadata['coefficient']
                b_coeff = problem.metadata.get('b_coefficient', 0)
                c = problem.metadata.get('c_constant', problem.metadata.get('constant', 0))
                x = problem.metadata['input']
                correct_answer = a * (x ** 2) + b_coeff * x + c
            elif word_problem_type == 'function_composition':
                a = problem.metadata['coefficient']
                b = problem.metadata['constant']
                c = problem.metadata['g_coefficient']
                d = problem.metadata['g_constant']
                x = problem.metadata['input']
                g_of_x = c * x + d
                correct_answer = a * g_of_x + b
            elif word_problem_type == 'absolute_value_function':
                a = problem.metadata['coefficient']
                b = problem.metadata['constant']
                x = problem.metadata['input']
                correct_answer = abs(a * x + b)
            else:
                a = problem.metadata['coefficient']
                b = problem.metadata['constant']
                x = problem.metadata['input']
                correct_answer = a * x + b
        else:
            a = problem.metadata['coefficient']
            b = problem.metadata['constant']
            x = problem.metadata['input']
            correct_answer = a * x + b

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, problem_type)
        else:
            steps = self._generate_concise_steps(problem, problem_type)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
