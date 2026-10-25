"""
Malrule algorithm for Function-Distributive-Property error.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class FunctionDistributivePropertyMalrule(Malrule):
    """
    Students think functions distribute over addition: f(x+a) = f(x) + f(a).

    Example: f(x) = x², f(5+2) → Student: f(5) + f(2) = 25 + 4 = 29 (wrong!)
    Correct: f(7) = 49
    """

    def get_name(self) -> str:
        return "Illusion-of-Linearity-Additive"

    def get_description(self) -> str:
        return (
            "Student incorrectly applies the additive property of linear functions to nonlinear "
            "functions: f(x+a) = f(x) + f(a). This error, termed the 'illusion of linearity' by "
            "De Bock et al. (2007), results from overgeneralization of the distributive law "
            "experienced extensively in arithmetic and early algebra (Matz, 1982)."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Malrule: incorrectly distribute function over addition f(x+a) = f(x) + f(a)
        return problem.metadata['malrule_answer']

    def _generate_concise_steps(self, problem: Problem, problem_type: str) -> List[str]:
        """Generate concise steps with only formulas and values."""
        steps = []

        if problem_type == 'subtraction_input':
            a = problem.metadata['coefficient']
            x1 = problem.metadata['value1']
            x2 = problem.metadata['value2']
            malrule_answer = a * (x1 ** 2) - a * (x2 ** 2)
            func_str = "x²" if a == 1 else f"{a}x²"

            steps.append(f"f(x) = {func_str}, find f({x1}-{x2})")
            steps.append(f"f({x1}) = {a}({x1})² = {a * (x1**2)}")
            steps.append(f"f({x2}) = {a}({x2})² = {a * (x2**2)}")
            steps.append(f"f({x1}-{x2}) = f({x1}) - f({x2}) = {a * (x1**2)} - {a * (x2**2)} = {malrule_answer}")
            steps.append(f"{malrule_answer}")

        elif problem_type == 'cubic_function':
            x1 = problem.metadata['value1']
            x2 = problem.metadata['value2']
            malrule_answer = (x1 ** 3) + (x2 ** 3)

            steps.append(f"f(x) = x³, find f({x1}+{x2})")
            steps.append(f"f({x1}) = ({x1})³ = {x1**3}")
            steps.append(f"f({x2}) = ({x2})³ = {x2**3}")
            steps.append(f"f({x1}+{x2}) = f({x1}) + f({x2}) = {x1**3} + {x2**3} = {malrule_answer}")
            steps.append(f"{malrule_answer}")

        elif problem_type == 'absolute_value':
            x1 = problem.metadata['value1']
            x2 = problem.metadata['value2']
            k = problem.metadata['k_value']
            malrule_answer = abs(x1 + k) + abs(x2 + k)

            steps.append(f"f(x) = |x+{k}|, find f({x1}+{x2})")
            steps.append(f"f({x1}) = |{x1}+{k}| = {abs(x1 + k)}")
            steps.append(f"f({x2}) = |{x2}+{k}| = {abs(x2 + k)}")
            steps.append(f"f({x1}+{x2}) = f({x1}) + f({x2}) = {abs(x1 + k)} + {abs(x2 + k)} = {malrule_answer}")
            steps.append(f"{malrule_answer}")

        elif problem_type == 'word_problem_context':
            word_problem_type = problem.metadata.get('word_problem_type', 'square')

            if word_problem_type == 'square':
                x1 = problem.metadata['value1']
                x2 = problem.metadata['value2']
                malrule_answer = (x1 ** 2) + (x2 ** 2)

                steps.append(f"{problem.text}")
                steps.append(f"f(x) = x², find f({x1}+{x2})")
                steps.append(f"f({x1}) = ({x1})² = {x1**2}")
                steps.append(f"f({x2}) = ({x2})² = {x2**2}")
                steps.append(f"f({x1}+{x2}) = f({x1}) + f({x2}) = {x1**2} + {x2**2} = {malrule_answer}")
                steps.append(f"{malrule_answer}")

            elif word_problem_type == 'scaled_square':
                a = problem.metadata['coefficient']
                x1 = problem.metadata['value1']
                x2 = problem.metadata['value2']
                malrule_answer = a * (x1 ** 2) + a * (x2 ** 2)

                steps.append(f"{problem.text}")
                steps.append(f"f(x) = {a}x², find f({x1}+{x2})")
                steps.append(f"f({x1}) = {a}({x1})² = {a * (x1**2)}")
                steps.append(f"f({x2}) = {a}({x2})² = {a * (x2**2)}")
                steps.append(f"f({x1}+{x2}) = f({x1}) + f({x2}) = {a * (x1**2)} + {a * (x2**2)} = {malrule_answer}")
                steps.append(f"{malrule_answer}")

            elif word_problem_type == 'subtraction_input':
                a = problem.metadata['coefficient']
                x1 = problem.metadata['value1']
                x2 = problem.metadata['value2']
                malrule_answer = a * (x1 ** 2) - a * (x2 ** 2)
                func_str = "x²" if a == 1 else f"{a}x²"

                steps.append(f"{problem.text}")
                steps.append(f"f(x) = {func_str}, find f({x1}-{x2})")
                steps.append(f"f({x1}) = {a if a > 1 else ''}({x1})² = {a * (x1**2)}")
                steps.append(f"f({x2}) = {a if a > 1 else ''}({x2})² = {a * (x2**2)}")
                steps.append(f"f({x1}-{x2}) = f({x1}) - f({x2}) = {a * (x1**2)} - {a * (x2**2)} = {malrule_answer}")
                steps.append(f"{malrule_answer}")

            elif word_problem_type == 'cubic_function':
                x1 = problem.metadata['value1']
                x2 = problem.metadata['value2']
                malrule_answer = (x1 ** 3) + (x2 ** 3)

                steps.append(f"{problem.text}")
                steps.append(f"f(x) = x³, find f({x1}+{x2})")
                steps.append(f"f({x1}) = ({x1})³ = {x1**3}")
                steps.append(f"f({x2}) = ({x2})³ = {x2**3}")
                steps.append(f"f({x1}+{x2}) = f({x1}) + f({x2}) = {x1**3} + {x2**3} = {malrule_answer}")
                steps.append(f"{malrule_answer}")

            elif word_problem_type == 'absolute_value':
                x1 = problem.metadata['value1']
                x2 = problem.metadata['value2']
                k = problem.metadata['k_value']
                malrule_answer = abs(x1 + k) + abs(x2 + k)

                steps.append(f"{problem.text}")
                steps.append(f"f(x) = |x+{k}|, find f({x1}+{x2})")
                steps.append(f"f({x1}) = |{x1}+{k}| = {abs(x1 + k)}")
                steps.append(f"f({x2}) = |{x2}+{k}| = {abs(x2 + k)}")
                steps.append(f"f({x1}+{x2}) = f({x1}) + f({x2}) = {abs(x1 + k)} + {abs(x2 + k)} = {malrule_answer}")
                steps.append(f"{malrule_answer}")
            else:
                x1 = problem.metadata['value1']
                x2 = problem.metadata['value2']
                malrule_answer = (x1 ** 2) + (x2 ** 2)

                steps.append(f"{problem.text}")
                steps.append(f"f(x) = x², find f({x1}+{x2})")
                steps.append(f"f({x1}) = ({x1})² = {x1**2}")
                steps.append(f"f({x2}) = ({x2})² = {x2**2}")
                steps.append(f"f({x1}+{x2}) = f({x1}) + f({x2}) = {x1**2} + {x2**2} = {malrule_answer}")
                steps.append(f"{malrule_answer}")
        else:
            # Original problem types (square and scaled_square)
            a = problem.metadata['coefficient']
            x1 = problem.metadata['value1']
            x2 = problem.metadata['value2']
            malrule_answer = a * (x1 ** 2) + a * (x2 ** 2)
            func_str = "x²" if a == 1 else f"{a}x²"

            steps.append(f"f(x) = {func_str}, find f({x1}+{x2})")
            steps.append(f"f({x1}) = {a}({x1})² = {a * (x1**2)}")
            steps.append(f"f({x2}) = {a}({x2})² = {a * (x2**2)}")
            steps.append(f"f({x1}+{x2}) = f({x1}) + f({x2}) = {a * (x1**2)} + {a * (x2**2)} = {malrule_answer}")
            steps.append(f"{malrule_answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, problem_type: str) -> List[str]:
        """Generate verbose steps with full explanations (original format)."""
        if problem_type == 'subtraction_input':
            return self._verbose_subtraction_input(problem)
        elif problem_type == 'cubic_function':
            return self._verbose_cubic_function(problem)
        elif problem_type == 'absolute_value':
            return self._verbose_absolute_value(problem)
        elif problem_type == 'word_problem_context':
            return self._verbose_word_problem_context(problem)
        else:
            return self._verbose_default(problem)

    def _verbose_default(self, problem: Problem) -> List[str]:
        """Verbose steps for default square/scaled_square problems."""
        a = problem.metadata['coefficient']
        x1 = problem.metadata['value1']
        x2 = problem.metadata['value2']
        input_sum = problem.metadata.get('input_sum', problem.metadata.get('input_value', x1 + x2))
        malrule_answer = a * (x1 ** 2) + a * (x2 ** 2)
        func_str = "x²" if a == 1 else f"{a}x²"

        steps = []
        steps.append(f"Problem: Given f(x) = {func_str}, evaluate f({x1}+{x2})")
        steps.append("")
        steps.append(f"MALRULE: Functions distribute over addition")
        steps.append(f"  MALRULE REASONING: 'Like multiplication: 3(5+2) = 3(5) + 3(2)'")
        steps.append(f"                     'So f({x1}+{x2}) = f({x1}) + f({x2})'")
        steps.append("")
        steps.append(f"Step 1: Evaluate f({x1})")
        steps.append(f"  f({x1}) = {a}({x1})² = {a * (x1**2)}")
        steps.append("")
        steps.append(f"Step 2: Evaluate f({x2})")
        steps.append(f"  f({x2}) = {a}({x2})² = {a * (x2**2)}")
        steps.append("")
        steps.append(f"Step 3: Add the results (INCORRECT STEP!)")
        steps.append(f"  f({x1}+{x2}) = f({x1}) + f({x2}) = {a * (x1**2)} + {a * (x2**2)} = {malrule_answer}")
        steps.append("")
        steps.append(f"Final Answer: {malrule_answer} (INCORRECT - functions don't distribute!)")
        steps.append(f"  Should evaluate input first: {x1}+{x2} = {input_sum}, then f({input_sum}) = {a * (input_sum**2)}")
        return steps

    def _verbose_subtraction_input(self, problem: Problem) -> List[str]:
        """Verbose steps for subtraction input problems."""
        a = problem.metadata['coefficient']
        x1 = problem.metadata['value1']
        x2 = problem.metadata['value2']
        input_diff = problem.metadata.get('input_value', x1 - x2)
        malrule_answer = a * (x1 ** 2) - a * (x2 ** 2)
        func_str = "x²" if a == 1 else f"{a}x²"

        steps = []
        steps.append(f"Problem: Given f(x) = {func_str}, evaluate f({x1}-{x2})")
        steps.append("")
        steps.append(f"MALRULE: Functions distribute over subtraction")
        steps.append(f"  MALRULE REASONING: 'Like multiplication with subtraction'")
        steps.append(f"                     'So f({x1}-{x2}) = f({x1}) - f({x2})'")
        steps.append("")
        steps.append(f"Step 1: Evaluate f({x1})")
        steps.append(f"  f({x1}) = {a}({x1})² = {a * (x1**2)}")
        steps.append("")
        steps.append(f"Step 2: Evaluate f({x2})")
        steps.append(f"  f({x2}) = {a}({x2})² = {a * (x2**2)}")
        steps.append("")
        steps.append(f"Step 3: Subtract the results (INCORRECT STEP!)")
        steps.append(f"  f({x1}-{x2}) = f({x1}) - f({x2}) = {a * (x1**2)} - {a * (x2**2)} = {malrule_answer}")
        steps.append("")
        steps.append(f"Final Answer: {malrule_answer} (INCORRECT - functions don't distribute!)")
        steps.append(f"  Should evaluate input first: {x1}-{x2} = {input_diff}, then f({input_diff}) = {a * (input_diff**2)}")
        return steps

    def _verbose_cubic_function(self, problem: Problem) -> List[str]:
        """Verbose steps for cubic function problems."""
        x1 = problem.metadata['value1']
        x2 = problem.metadata['value2']
        input_sum = problem.metadata.get('input_value', x1 + x2)
        malrule_answer = (x1 ** 3) + (x2 ** 3)

        steps = []
        steps.append(f"Problem: Given f(x) = x³, evaluate f({x1}+{x2})")
        steps.append("")
        steps.append(f"MALRULE: Functions distribute over addition")
        steps.append(f"  MALRULE REASONING: 'Addition distributes'")
        steps.append(f"                     'So f({x1}+{x2}) = f({x1}) + f({x2})'")
        steps.append("")
        steps.append(f"Step 1: Evaluate f({x1})")
        steps.append(f"  f({x1}) = ({x1})³ = {x1**3}")
        steps.append("")
        steps.append(f"Step 2: Evaluate f({x2})")
        steps.append(f"  f({x2}) = ({x2})³ = {x2**3}")
        steps.append("")
        steps.append(f"Step 3: Add the results (INCORRECT STEP!)")
        steps.append(f"  f({x1}+{x2}) = f({x1}) + f({x2}) = {x1**3} + {x2**3} = {malrule_answer}")
        steps.append("")
        steps.append(f"Final Answer: {malrule_answer} (INCORRECT!)")
        steps.append(f"  Should evaluate input first: {x1}+{x2} = {input_sum}, then f({input_sum}) = {input_sum**3}")
        return steps

    def _verbose_absolute_value(self, problem: Problem) -> List[str]:
        """Verbose steps for absolute value problems."""
        x1 = problem.metadata['value1']
        x2 = problem.metadata['value2']
        k = problem.metadata['k_value']
        input_sum = problem.metadata.get('input_value', x1 + x2)
        malrule_answer = abs(x1 + k) + abs(x2 + k)

        steps = []
        steps.append(f"Problem: Given f(x) = |x+{k}|, evaluate f({x1}+{x2})")
        steps.append("")
        steps.append(f"MALRULE: Functions distribute over addition")
        steps.append(f"  MALRULE REASONING: 'Addition distributes'")
        steps.append(f"                     'So f({x1}+{x2}) = f({x1}) + f({x2})'")
        steps.append("")
        steps.append(f"Step 1: Evaluate f({x1})")
        steps.append(f"  f({x1}) = |{x1}+{k}| = {abs(x1 + k)}")
        steps.append("")
        steps.append(f"Step 2: Evaluate f({x2})")
        steps.append(f"  f({x2}) = |{x2}+{k}| = {abs(x2 + k)}")
        steps.append("")
        steps.append(f"Step 3: Add the results (INCORRECT STEP!)")
        steps.append(f"  f({x1}+{x2}) = f({x1}) + f({x2}) = {abs(x1 + k)} + {abs(x2 + k)} = {malrule_answer}")
        steps.append("")
        steps.append(f"Final Answer: {malrule_answer} (INCORRECT!)")
        steps.append(f"  Should evaluate input first: {x1}+{x2} = {input_sum}, then f({input_sum}) = |{input_sum}+{k}|")
        return steps

    def _verbose_word_problem_context(self, problem: Problem) -> List[str]:
        """Verbose steps for word problem contexts."""
        word_problem_type = problem.metadata.get('word_problem_type', 'square')

        if word_problem_type == 'square':
            return self._verbose_word_problem_square(problem)
        elif word_problem_type == 'scaled_square':
            return self._verbose_word_problem_scaled_square(problem)
        elif word_problem_type == 'subtraction_input':
            return self._verbose_word_problem_subtraction(problem)
        elif word_problem_type == 'cubic_function':
            return self._verbose_word_problem_cubic(problem)
        elif word_problem_type == 'absolute_value':
            return self._verbose_word_problem_absolute_value(problem)
        else:
            return self._verbose_word_problem_square(problem)

    def _verbose_word_problem_square(self, problem: Problem) -> List[str]:
        """Verbose steps for word problems with f(x) = x² formula (malrule)."""
        x1 = problem.metadata['value1']
        x2 = problem.metadata['value2']
        input_value = problem.metadata.get('input_value', x1 + x2)
        malrule_answer = (x1 ** 2) + (x2 ** 2)

        steps = []
        steps.append(f"Word Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: Functions distribute over addition")
        steps.append(f"  MALRULE REASONING: 'f({x1}+{x2}) = f({x1}) + f({x2})'")
        steps.append("")
        steps.append(f"Step 1: Evaluate f({x1})")
        steps.append(f"  f({x1}) = ({x1})² = {x1**2}")
        steps.append("")
        steps.append(f"Step 2: Evaluate f({x2})")
        steps.append(f"  f({x2}) = ({x2})² = {x2**2}")
        steps.append("")
        steps.append(f"Step 3: Add the results (INCORRECT STEP!)")
        steps.append(f"  {x1**2} + {x2**2} = {malrule_answer}")
        steps.append("")
        steps.append(f"Final Answer: {malrule_answer} (INCORRECT!)")
        steps.append(f"  Correct: f({input_value}) = {input_value**2} = {problem.metadata['correct_answer']}")
        return steps

    def _verbose_word_problem_scaled_square(self, problem: Problem) -> List[str]:
        """Verbose steps for word problems with f(x) = ax² formula (malrule)."""
        a = problem.metadata['coefficient']
        x1 = problem.metadata['value1']
        x2 = problem.metadata['value2']
        input_value = problem.metadata.get('input_value', x1 + x2)
        malrule_answer = a * (x1 ** 2) + a * (x2 ** 2)

        steps = []
        steps.append(f"Word Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: Functions distribute over addition")
        steps.append(f"  MALRULE REASONING: 'f({x1}+{x2}) = f({x1}) + f({x2})'")
        steps.append("")
        steps.append(f"Step 1: Evaluate f({x1})")
        steps.append(f"  f({x1}) = {a}({x1})² = {a * (x1**2)}")
        steps.append("")
        steps.append(f"Step 2: Evaluate f({x2})")
        steps.append(f"  f({x2}) = {a}({x2})² = {a * (x2**2)}")
        steps.append("")
        steps.append(f"Step 3: Add the results (INCORRECT STEP!)")
        steps.append(f"  {a * (x1**2)} + {a * (x2**2)} = {malrule_answer}")
        steps.append("")
        steps.append(f"Final Answer: {malrule_answer} (INCORRECT!)")
        steps.append(f"  Correct: f({input_value}) = {a}×{input_value**2} = {problem.metadata['correct_answer']}")
        return steps

    def _verbose_word_problem_subtraction(self, problem: Problem) -> List[str]:
        """Verbose steps for word problems with f(x-a) formula (malrule)."""
        a = problem.metadata['coefficient']
        x1 = problem.metadata['value1']
        x2 = problem.metadata['value2']
        input_value = problem.metadata.get('input_value', x1 - x2)
        malrule_answer = a * (x1 ** 2) - a * (x2 ** 2)

        steps = []
        steps.append(f"Word Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: Functions distribute over subtraction")
        steps.append(f"  MALRULE REASONING: 'f({x1}-{x2}) = f({x1}) - f({x2})'")
        steps.append("")
        steps.append(f"Step 1: Evaluate f({x1})")
        steps.append(f"  f({x1}) = {a if a > 1 else ''}({x1})² = {a * (x1**2)}")
        steps.append("")
        steps.append(f"Step 2: Evaluate f({x2})")
        steps.append(f"  f({x2}) = {a if a > 1 else ''}({x2})² = {a * (x2**2)}")
        steps.append("")
        steps.append(f"Step 3: Subtract the results (INCORRECT STEP!)")
        steps.append(f"  {a * (x1**2)} - {a * (x2**2)} = {malrule_answer}")
        steps.append("")
        steps.append(f"Final Answer: {malrule_answer} (INCORRECT!)")
        steps.append(f"  Correct: f({input_value}) = {input_value**2} = {problem.metadata['correct_answer']}")
        return steps

    def _verbose_word_problem_cubic(self, problem: Problem) -> List[str]:
        """Verbose steps for word problems with f(x) = x³ formula (malrule)."""
        x1 = problem.metadata['value1']
        x2 = problem.metadata['value2']
        input_value = problem.metadata.get('input_value', x1 + x2)
        malrule_answer = (x1 ** 3) + (x2 ** 3)

        steps = []
        steps.append(f"Word Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: Functions distribute over addition")
        steps.append(f"  MALRULE REASONING: 'f({x1}+{x2}) = f({x1}) + f({x2})'")
        steps.append("")
        steps.append(f"Step 1: Evaluate f({x1})")
        steps.append(f"  f({x1}) = ({x1})³ = {x1**3}")
        steps.append("")
        steps.append(f"Step 2: Evaluate f({x2})")
        steps.append(f"  f({x2}) = ({x2})³ = {x2**3}")
        steps.append("")
        steps.append(f"Step 3: Add the results (INCORRECT STEP!)")
        steps.append(f"  {x1**3} + {x2**3} = {malrule_answer}")
        steps.append("")
        steps.append(f"Final Answer: {malrule_answer} (INCORRECT!)")
        steps.append(f"  Correct: f({input_value}) = {input_value**3} = {problem.metadata['correct_answer']}")
        return steps

    def _verbose_word_problem_absolute_value(self, problem: Problem) -> List[str]:
        """Verbose steps for word problems with f(x) = |x+k| formula (malrule)."""
        x1 = problem.metadata['value1']
        x2 = problem.metadata['value2']
        k = problem.metadata['k_value']
        input_value = problem.metadata.get('input_value', x1 + x2)
        malrule_answer = abs(x1 + k) + abs(x2 + k)

        steps = []
        steps.append(f"Word Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: Functions distribute over addition")
        steps.append(f"  MALRULE REASONING: 'f({x1}+{x2}) = f({x1}) + f({x2})'")
        steps.append("")
        steps.append(f"Step 1: Evaluate f({x1})")
        steps.append(f"  f({x1}) = |{x1}+{k}| = {abs(x1 + k)}")
        steps.append("")
        steps.append(f"Step 2: Evaluate f({x2})")
        steps.append(f"  f({x2}) = |{x2}+{k}| = {abs(x2 + k)}")
        steps.append("")
        steps.append(f"Step 3: Add the results (INCORRECT STEP!)")
        steps.append(f"  {abs(x1 + k)} + {abs(x2 + k)} = {malrule_answer}")
        steps.append("")
        steps.append(f"Final Answer: {malrule_answer} (INCORRECT!)")
        steps.append(f"  Correct: f({input_value}) = |{input_value}+{k}| = {problem.metadata['correct_answer']}")
        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        problem_type = problem.metadata.get('problem_type', 'square')

        # Compute the malrule answer based on problem type
        if problem_type == 'subtraction_input':
            a = problem.metadata['coefficient']
            x1 = problem.metadata['value1']
            x2 = problem.metadata['value2']
            malrule_answer = a * (x1 ** 2) - a * (x2 ** 2)
        elif problem_type == 'cubic_function':
            x1 = problem.metadata['value1']
            x2 = problem.metadata['value2']
            malrule_answer = (x1 ** 3) + (x2 ** 3)
        elif problem_type == 'absolute_value':
            x1 = problem.metadata['value1']
            x2 = problem.metadata['value2']
            k = problem.metadata['k_value']
            malrule_answer = abs(x1 + k) + abs(x2 + k)
        elif problem_type == 'word_problem_context':
            word_problem_type = problem.metadata.get('word_problem_type', 'square')
            if word_problem_type == 'square':
                x1 = problem.metadata['value1']
                x2 = problem.metadata['value2']
                malrule_answer = (x1 ** 2) + (x2 ** 2)
            elif word_problem_type == 'scaled_square':
                a = problem.metadata['coefficient']
                x1 = problem.metadata['value1']
                x2 = problem.metadata['value2']
                malrule_answer = a * (x1 ** 2) + a * (x2 ** 2)
            elif word_problem_type == 'subtraction_input':
                a = problem.metadata['coefficient']
                x1 = problem.metadata['value1']
                x2 = problem.metadata['value2']
                malrule_answer = a * (x1 ** 2) - a * (x2 ** 2)
            elif word_problem_type == 'cubic_function':
                x1 = problem.metadata['value1']
                x2 = problem.metadata['value2']
                malrule_answer = (x1 ** 3) + (x2 ** 3)
            elif word_problem_type == 'absolute_value':
                x1 = problem.metadata['value1']
                x2 = problem.metadata['value2']
                k = problem.metadata['k_value']
                malrule_answer = abs(x1 + k) + abs(x2 + k)
            else:
                x1 = problem.metadata['value1']
                x2 = problem.metadata['value2']
                malrule_answer = (x1 ** 2) + (x2 ** 2)
        else:
            # Original problem types (square and scaled_square)
            a = problem.metadata['coefficient']
            x1 = problem.metadata['value1']
            x2 = problem.metadata['value2']
            malrule_answer = a * (x1 ** 2) + a * (x2 ** 2)

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
