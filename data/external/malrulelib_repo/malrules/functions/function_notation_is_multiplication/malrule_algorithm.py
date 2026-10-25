"""
Malrule algorithm for Function-Notation-Is-Multiplication error.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class FunctionNotationIsMultiplicationMalrule(Malrule):
    """
    Students think f(x) means f × x (multiplication).

    Example: f(x) = 2x + 3, evaluate f(5) → Student: f × 5 or 2 × 5 = 10 (wrong!)
    """

    def get_name(self) -> str:
        return "Function-Notation-As-Multiplication"

    def get_description(self) -> str:
        return (
            "Student interprets f(x) as meaning f × x (multiplication) rather than "
            "function notation. This confusion arises because parentheses are used for "
            "both multiplication (e.g., 3(5) = 15) and function evaluation. Carlson (1995) "
            "found that students are unclear about what function names like f represent, "
            "often believing they are variables rather than process names."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Malrule: treat f(x) as f × x, computing coefficient × input
        return problem.metadata['malrule_answer']

    def _generate_concise_steps(self, problem: Problem, problem_type: str) -> List[str]:
        """Generate concise steps with only formulas and values."""
        steps = []

        if problem_type == 'simple_linear':
            a = problem.metadata['coefficient']
            b = problem.metadata['constant']
            x = problem.metadata['input']
            malrule_answer = a * x

            steps.append(f"f(x) = {a}x + {b}, find f({x})")
            steps.append(f"f({x}) = f × {x} = {a} × {x} = {malrule_answer}")
            steps.append(f"{malrule_answer}")

        elif problem_type == 'quadratic_function':
            a = problem.metadata['coefficient']
            b_coeff = problem.metadata.get('b_coefficient', 0)
            c = problem.metadata.get('c_constant', problem.metadata.get('constant', 0))
            x = problem.metadata['input']
            malrule_answer = a * x
            b_sign = '+' if b_coeff >= 0 else ''
            c_sign = '+' if c >= 0 else ''

            steps.append(f"f(x) = {a}x² {b_sign} {b_coeff}x {c_sign} {c}, find f({x})")
            steps.append(f"f({x}) = f × {x} = {a} × {x} = {malrule_answer}")
            steps.append(f"{malrule_answer}")

        elif problem_type == 'function_composition':
            a = problem.metadata['coefficient']
            c = problem.metadata['g_coefficient']
            x = problem.metadata['input']
            malrule_answer = a * c * x

            steps.append(f"f(x) = {a}x + {problem.metadata['constant']}, g(x) = {c}x + {problem.metadata['g_constant']}, find f(g({x}))")
            steps.append(f"f(g({x})) = f × g × {x} = {a} × {c} × {x} = {malrule_answer}")
            steps.append(f"{malrule_answer}")

        elif problem_type == 'absolute_value_function':
            a = problem.metadata['coefficient']
            b = problem.metadata['constant']
            x = problem.metadata['input']
            malrule_answer = a * x
            b_sign = '+' if b >= 0 else ''

            steps.append(f"f(x) = |{a}x {b_sign} {b}|, find f({x})")
            steps.append(f"f({x}) = f × {x} = {a} × {x} = {malrule_answer}")
            steps.append(f"{malrule_answer}")

        elif problem_type == 'word_problem_context':
            word_problem_type = problem.metadata.get('word_problem_type', 'simple_linear')
            steps.append(f"{problem.text}")

            if word_problem_type == 'simple_linear':
                a = problem.metadata['coefficient']
                x = problem.metadata['input']
                malrule_answer = a * x
                steps.append(f"f(x) = {a}x + {problem.metadata['constant']}, find f({x})")
                steps.append(f"f({x}) = f × {x} = {a} × {x} = {malrule_answer}")
                steps.append(f"{malrule_answer}")
            elif word_problem_type == 'quadratic_function':
                a = problem.metadata['coefficient']
                x = problem.metadata['input']
                malrule_answer = a * x
                steps.append(f"f(x) = {a}x² + ..., find f({x})")
                steps.append(f"f({x}) = f × {x} = {a} × {x} = {malrule_answer}")
                steps.append(f"{malrule_answer}")
            elif word_problem_type == 'function_composition':
                a = problem.metadata['coefficient']
                c = problem.metadata['g_coefficient']
                x = problem.metadata['input']
                malrule_answer = a * c * x
                steps.append(f"f(g({x})) = f × g × {x} = {a} × {c} × {x} = {malrule_answer}")
                steps.append(f"{malrule_answer}")
            elif word_problem_type == 'absolute_value_function':
                a = problem.metadata['coefficient']
                x = problem.metadata['input']
                malrule_answer = a * x
                steps.append(f"f({x}) = f × {x} = {a} × {x} = {malrule_answer}")
                steps.append(f"{malrule_answer}")
            else:
                a = problem.metadata['coefficient']
                x = problem.metadata['input']
                malrule_answer = a * x
                steps.append(f"f({x}) = f × {x} = {a} × {x} = {malrule_answer}")
                steps.append(f"{malrule_answer}")
        else:
            # Default to simple linear
            a = problem.metadata['coefficient']
            x = problem.metadata['input']
            malrule_answer = a * x

            steps.append(f"f(x) = {a}x + {problem.metadata['constant']}, find f({x})")
            steps.append(f"f({x}) = f × {x} = {a} × {x} = {malrule_answer}")
            steps.append(f"{malrule_answer}")

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
        malrule_answer = a * x

        steps = []
        steps.append(f"Problem: Given f(x) = {a}x + {b}, evaluate f({x})")
        steps.append("")
        steps.append("MALRULE: f(x) means f × x (multiplication)")
        steps.append(f"  MALRULE REASONING: 'Parentheses mean multiply'")
        steps.append(f"                     'f({x}) must mean f × {x}'")
        steps.append("")
        steps.append("Step 1: MALRULE - interpret f(x) as multiplication")
        steps.append(f"  'What does f equal? Look at f(x) = {a}x + {b}'")
        steps.append(f"  'Maybe f = {a}? So f × {x} = {a} × {x} = {malrule_answer}'")
        steps.append("")
        steps.append(f"Step 2: Ignore the +{b} part (confused)")
        steps.append("")
        steps.append(f"Final Answer: {malrule_answer} (INCORRECT - f(x) is notation, not multiplication!)")
        steps.append(f"  Should substitute {x} for x: {a}({x}) + {b} = {a * x + b}")
        return steps

    def _verbose_quadratic(self, problem: Problem) -> List[str]:
        """Verbose steps for quadratic problems."""
        a = problem.metadata['coefficient']
        b_coeff = problem.metadata.get('b_coefficient', 0)
        c = problem.metadata.get('c_constant', problem.metadata.get('constant', 0))
        x = problem.metadata['input']
        malrule_answer = a * x
        b_sign = '+' if b_coeff >= 0 else ''
        c_sign = '+' if c >= 0 else ''

        steps = []
        steps.append(f"Problem: Given f(x) = {a}x² {b_sign} {b_coeff}x {c_sign} {c}, evaluate f({x})")
        steps.append("")
        steps.append("MALRULE: f(x) means f × x (multiplication)")
        steps.append(f"  MALRULE REASONING: 'Parentheses mean multiply'")
        steps.append(f"                     'f({x}) must mean f × {x}'")
        steps.append("")
        steps.append("Step 1: MALRULE - interpret f(x) as multiplication")
        steps.append(f"  'What does f equal? Look at the coefficient: f = {a}'")
        steps.append(f"  'So f × {x} = {a} × {x} = {malrule_answer}'")
        steps.append("")
        steps.append(f"Step 2: Ignore the rest of the function (confused)")
        steps.append("")
        steps.append(f"Final Answer: {malrule_answer} (INCORRECT!)")
        steps.append(f"  Should substitute {x} for x: {a}({x})² {b_sign} {b_coeff}({x}) {c_sign} {c} = {a * (x**2) + b_coeff * x + c}")
        return steps

    def _verbose_composition(self, problem: Problem) -> List[str]:
        """Verbose steps for composition problems."""
        a = problem.metadata['coefficient']
        b = problem.metadata['constant']
        c = problem.metadata['g_coefficient']
        d = problem.metadata['g_constant']
        x = problem.metadata['input']
        malrule_answer = a * c * x

        steps = []
        steps.append(f"Problem: Given f(x) = {a}x + {b} and g(x) = {c}x + {d}, evaluate f(g({x}))")
        steps.append("")
        steps.append("MALRULE: f(g(x)) means f × g × x (multiplication)")
        steps.append(f"  MALRULE REASONING: 'Parentheses mean multiply'")
        steps.append(f"                     'f(g({x})) must mean f × g × {x}'")
        steps.append("")
        steps.append("Step 1: MALRULE - treat as multiplication")
        steps.append(f"  'f has coefficient {a}, g has coefficient {c}'")
        steps.append(f"  'So f × g × {x} = {a} × {c} × {x} = {malrule_answer}'")
        steps.append("")
        steps.append(f"Final Answer: {malrule_answer} (INCORRECT!)")
        g_of_x = c * x + d
        correct = a * g_of_x + b
        steps.append(f"  Should evaluate g({x}) = {g_of_x} first, then f({g_of_x}) = {correct}")
        return steps

    def _verbose_absolute_value(self, problem: Problem) -> List[str]:
        """Verbose steps for absolute value problems."""
        a = problem.metadata['coefficient']
        b = problem.metadata['constant']
        x = problem.metadata['input']
        malrule_answer = a * x
        b_sign = '+' if b >= 0 else ''

        steps = []
        steps.append(f"Problem: Given f(x) = |{a}x {b_sign} {b}|, evaluate f({x})")
        steps.append("")
        steps.append("MALRULE: f(x) means f × x (multiplication)")
        steps.append(f"  MALRULE REASONING: 'Parentheses mean multiply'")
        steps.append(f"                     'f({x}) must mean f × {x}'")
        steps.append("")
        steps.append("Step 1: MALRULE - interpret f(x) as multiplication")
        steps.append(f"  'Look at the coefficient: f = {a}'")
        steps.append(f"  'So f × {x} = {a} × {x} = {malrule_answer}'")
        steps.append("")
        steps.append(f"Step 2: Ignore the absolute value and constant (confused)")
        steps.append("")
        steps.append(f"Final Answer: {malrule_answer} (INCORRECT!)")
        correct = abs(a * x + b)
        steps.append(f"  Should substitute {x} for x: |{a}({x}) {b_sign} {b}| = {correct}")
        return steps

    def _verbose_word_problem(self, problem: Problem) -> List[str]:
        """Verbose steps for word problems."""
        word_problem_type = problem.metadata.get('word_problem_type', 'simple_linear')

        steps = []
        steps.append(f"Word Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: f(x) means f × x (multiplication)")
        steps.append("")

        if word_problem_type == 'simple_linear':
            a = problem.metadata['coefficient']
            b = problem.metadata['constant']
            x = problem.metadata['input']
            malrule_answer = a * x

            steps.append(f"Step 1: Extract the function f(x) = {a}x + {b}")
            steps.append(f"Step 2: MALRULE - f({x}) = f × {x} = {a} × {x} = {malrule_answer}")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT!)")
            steps.append(f"  Correct: {a}({x}) + {b} = {a * x + b}")
        elif word_problem_type == 'quadratic_function':
            a = problem.metadata['coefficient']
            x = problem.metadata['input']
            malrule_answer = a * x

            steps.append(f"Step 1: Extract the coefficient = {a}")
            steps.append(f"Step 2: MALRULE - f({x}) = f × {x} = {a} × {x} = {malrule_answer}")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT!)")
        else:
            a = problem.metadata['coefficient']
            x = problem.metadata['input']
            malrule_answer = a * x

            steps.append(f"Step 1: MALRULE - f({x}) = f × {x} = {a} × {x} = {malrule_answer}")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT!)")

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        problem_type = problem.metadata.get('problem_type', 'simple_linear')

        # Compute the malrule answer based on problem type
        if problem_type == 'simple_linear':
            a = problem.metadata['coefficient']
            x = problem.metadata['input']
            malrule_answer = a * x
        elif problem_type == 'quadratic_function':
            a = problem.metadata['coefficient']
            x = problem.metadata['input']
            malrule_answer = a * x
        elif problem_type == 'function_composition':
            a = problem.metadata['coefficient']
            c = problem.metadata['g_coefficient']
            x = problem.metadata['input']
            malrule_answer = a * c * x
        elif problem_type == 'absolute_value_function':
            a = problem.metadata['coefficient']
            x = problem.metadata['input']
            malrule_answer = a * x
        elif problem_type == 'word_problem_context':
            word_problem_type = problem.metadata.get('word_problem_type', 'simple_linear')
            if word_problem_type == 'function_composition':
                a = problem.metadata['coefficient']
                c = problem.metadata['g_coefficient']
                x = problem.metadata['input']
                malrule_answer = a * c * x
            else:
                a = problem.metadata['coefficient']
                x = problem.metadata['input']
                malrule_answer = a * x
        else:
            a = problem.metadata['coefficient']
            x = problem.metadata['input']
            malrule_answer = a * x

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, problem_type)
        else:
            steps = self._generate_concise_steps(problem, problem_type)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
