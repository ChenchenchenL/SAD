"""
Correct algorithm for function evaluation with sum in input.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class FunctionCompositionCorrectAlgorithm(CorrectAlgorithm):
    """Correctly evaluates functions by simplifying input first."""

    def get_name(self) -> str:
        return "Correct Function Evaluation"

    def get_description(self) -> str:
        return "Correctly evaluates functions by simplifying the input expression first."

    def _generate_concise_steps(self, problem: Problem, problem_type: str) -> List[str]:
        """Generate concise steps with only formulas and values."""
        steps = []

        if problem_type == 'subtraction_input':
            a = problem.metadata['coefficient']
            x1 = problem.metadata['value1']
            x2 = problem.metadata['value2']
            input_diff = problem.metadata.get('input_value', x1 - x2)
            correct_answer = a * (input_diff ** 2)
            func_str = "x²" if a == 1 else f"{a}x²"

            steps.append(f"f(x) = {func_str}, find f({x1}-{x2})")
            steps.append(f"{x1} - {x2} = {input_diff}")
            steps.append(f"f({input_diff}) = {a}({input_diff})² = {correct_answer}")
            steps.append(f"{correct_answer}")

        elif problem_type == 'cubic_function':
            x1 = problem.metadata['value1']
            x2 = problem.metadata['value2']
            input_sum = problem.metadata.get('input_value', x1 + x2)
            correct_answer = input_sum ** 3

            steps.append(f"f(x) = x³, find f({x1}+{x2})")
            steps.append(f"{x1} + {x2} = {input_sum}")
            steps.append(f"f({input_sum}) = ({input_sum})³ = {correct_answer}")
            steps.append(f"{correct_answer}")

        elif problem_type == 'absolute_value':
            x1 = problem.metadata['value1']
            x2 = problem.metadata['value2']
            k = problem.metadata['k_value']
            input_sum = problem.metadata.get('input_value', x1 + x2)
            correct_answer = abs(input_sum + k)

            steps.append(f"f(x) = |x+{k}|, find f({x1}+{x2})")
            steps.append(f"{x1} + {x2} = {input_sum}")
            steps.append(f"f({input_sum}) = |{input_sum}+{k}| = |{input_sum + k}| = {correct_answer}")
            steps.append(f"{correct_answer}")

        elif problem_type == 'word_problem_context':
            word_problem_type = problem.metadata.get('word_problem_type', 'square')

            if word_problem_type == 'square':
                x1 = problem.metadata['value1']
                x2 = problem.metadata['value2']
                input_value = problem.metadata.get('input_value', x1 + x2)
                correct_answer = input_value ** 2

                steps.append(f"{problem.text}")
                steps.append(f"f(x) = x², find f({x1}+{x2})")
                steps.append(f"{x1} + {x2} = {input_value}")
                steps.append(f"f({input_value}) = ({input_value})² = {correct_answer}")
                steps.append(f"{correct_answer}")

            elif word_problem_type == 'scaled_square':
                a = problem.metadata['coefficient']
                x1 = problem.metadata['value1']
                x2 = problem.metadata['value2']
                input_value = problem.metadata.get('input_value', x1 + x2)
                correct_answer = a * (input_value ** 2)

                steps.append(f"{problem.text}")
                steps.append(f"f(x) = {a}x², find f({x1}+{x2})")
                steps.append(f"{x1} + {x2} = {input_value}")
                steps.append(f"f({input_value}) = {a}({input_value})² = {a} × {input_value**2} = {correct_answer}")
                steps.append(f"{correct_answer}")

            elif word_problem_type == 'subtraction_input':
                a = problem.metadata['coefficient']
                x1 = problem.metadata['value1']
                x2 = problem.metadata['value2']
                input_value = problem.metadata.get('input_value', x1 - x2)
                correct_answer = a * (input_value ** 2)
                func_str = "x²" if a == 1 else f"{a}x²"

                steps.append(f"{problem.text}")
                steps.append(f"f(x) = {func_str}, find f({x1}-{x2})")
                steps.append(f"{x1} - {x2} = {input_value}")
                steps.append(f"f({input_value}) = {a if a > 1 else ''}({input_value})² = {correct_answer}")
                steps.append(f"{correct_answer}")

            elif word_problem_type == 'cubic_function':
                x1 = problem.metadata['value1']
                x2 = problem.metadata['value2']
                input_value = problem.metadata.get('input_value', x1 + x2)
                correct_answer = input_value ** 3

                steps.append(f"{problem.text}")
                steps.append(f"f(x) = x³, find f({x1}+{x2})")
                steps.append(f"{x1} + {x2} = {input_value}")
                steps.append(f"f({input_value}) = ({input_value})³ = {correct_answer}")
                steps.append(f"{correct_answer}")

            elif word_problem_type == 'absolute_value':
                x1 = problem.metadata['value1']
                x2 = problem.metadata['value2']
                k = problem.metadata['k_value']
                input_value = problem.metadata.get('input_value', x1 + x2)
                correct_answer = abs(input_value + k)

                steps.append(f"{problem.text}")
                steps.append(f"f(x) = |x+{k}|, find f({x1}+{x2})")
                steps.append(f"{x1} + {x2} = {input_value}")
                steps.append(f"f({input_value}) = |{input_value}+{k}| = |{input_value + k}| = {correct_answer}")
                steps.append(f"{correct_answer}")
            else:
                # Fallback to square
                x1 = problem.metadata['value1']
                x2 = problem.metadata['value2']
                input_value = problem.metadata.get('input_value', x1 + x2)
                correct_answer = input_value ** 2

                steps.append(f"{problem.text}")
                steps.append(f"f(x) = x², find f({x1}+{x2})")
                steps.append(f"{x1} + {x2} = {input_value}")
                steps.append(f"f({input_value}) = ({input_value})² = {correct_answer}")
                steps.append(f"{correct_answer}")
        else:
            # Original problem types (square and scaled_square)
            a = problem.metadata['coefficient']
            x1 = problem.metadata['value1']
            x2 = problem.metadata['value2']
            input_sum = problem.metadata.get('input_sum', problem.metadata.get('input_value', x1 + x2))
            correct_answer = a * (input_sum ** 2)
            func_str = "x²" if a == 1 else f"{a}x²"

            steps.append(f"f(x) = {func_str}, find f({x1}+{x2})")
            steps.append(f"{x1} + {x2} = {input_sum}")
            steps.append(f"f({input_sum}) = {a}({input_sum})² = {a} × {input_sum**2} = {correct_answer}")
            steps.append(f"{correct_answer}")

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
        correct_answer = a * (input_sum ** 2)
        func_str = "x²" if a == 1 else f"{a}x²"

        steps = []
        steps.append(f"Problem: Given f(x) = {func_str}, evaluate f({x1}+{x2})")
        steps.append("")
        steps.append("CORRECT METHOD: Simplify input FIRST, then apply function")
        steps.append("  Functions DON'T distribute like multiplication!")
        steps.append("")
        steps.append(f"Step 1: Simplify the input expression")
        steps.append(f"  {x1} + {x2} = {input_sum}")
        steps.append("")
        steps.append(f"Step 2: Apply the function to the simplified input")
        steps.append(f"  f({input_sum}) = {a}({input_sum})²")
        steps.append(f"  = {a} × {input_sum**2}")
        steps.append(f"  = {correct_answer}")
        steps.append("")
        steps.append(f"Final Answer: f({x1}+{x2}) = {correct_answer} ✓")
        steps.append("")
        steps.append(f"Note: If we incorrectly distributed: f({x1}) + f({x2}) = {a * (x1**2)} + {a * (x2**2)} = {problem.metadata['malrule_answer']}")
        steps.append(f"      This is WRONG! {correct_answer} ≠ {problem.metadata['malrule_answer']}")
        return steps

    def _verbose_subtraction_input(self, problem: Problem) -> List[str]:
        """Verbose steps for subtraction input problems."""
        a = problem.metadata['coefficient']
        x1 = problem.metadata['value1']
        x2 = problem.metadata['value2']
        input_diff = problem.metadata.get('input_value', x1 - x2)
        correct_answer = a * (input_diff ** 2)
        func_str = "x²" if a == 1 else f"{a}x²"

        steps = []
        steps.append(f"Problem: Given f(x) = {func_str}, evaluate f({x1}-{x2})")
        steps.append("")
        steps.append("CORRECT METHOD: Simplify input FIRST, then apply function")
        steps.append("  f(x-a) ≠ f(x) - f(a)")
        steps.append("")
        steps.append(f"Step 1: Simplify the input expression")
        steps.append(f"  {x1} - {x2} = {input_diff}")
        steps.append("")
        steps.append(f"Step 2: Apply the function to the simplified input")
        steps.append(f"  f({input_diff}) = {a}({input_diff})²")
        steps.append(f"  = {a} × {input_diff**2}")
        steps.append(f"  = {correct_answer}")
        steps.append("")
        steps.append(f"Final Answer: f({x1}-{x2}) = {correct_answer} ✓")
        steps.append("")
        steps.append(f"Note: If we incorrectly used f(x) - f(a): f({x1}) - f({x2}) = {a * (x1**2)} - {a * (x2**2)} = {problem.metadata['malrule_answer']}")
        steps.append(f"      This is WRONG! {correct_answer} ≠ {problem.metadata['malrule_answer']}")
        return steps

    def _verbose_cubic_function(self, problem: Problem) -> List[str]:
        """Verbose steps for cubic function problems."""
        x1 = problem.metadata['value1']
        x2 = problem.metadata['value2']
        input_sum = problem.metadata.get('input_value', x1 + x2)
        correct_answer = input_sum ** 3

        steps = []
        steps.append(f"Problem: Given f(x) = x³, evaluate f({x1}+{x2})")
        steps.append("")
        steps.append("CORRECT METHOD: Simplify input FIRST, then apply function")
        steps.append("  (x+a)³ ≠ x³ + a³")
        steps.append("")
        steps.append(f"Step 1: Simplify the input expression")
        steps.append(f"  {x1} + {x2} = {input_sum}")
        steps.append("")
        steps.append(f"Step 2: Apply the function to the simplified input")
        steps.append(f"  f({input_sum}) = ({input_sum})³")
        steps.append(f"  = {correct_answer}")
        steps.append("")
        steps.append(f"Final Answer: f({x1}+{x2}) = {correct_answer} ✓")
        steps.append("")
        steps.append(f"Note: If we incorrectly distributed: f({x1}) + f({x2}) = {x1**3} + {x2**3} = {problem.metadata['malrule_answer']}")
        steps.append(f"      This is WRONG! {correct_answer} ≠ {problem.metadata['malrule_answer']}")
        return steps

    def _verbose_absolute_value(self, problem: Problem) -> List[str]:
        """Verbose steps for absolute value problems."""
        x1 = problem.metadata['value1']
        x2 = problem.metadata['value2']
        k = problem.metadata['k_value']
        input_sum = problem.metadata.get('input_value', x1 + x2)
        correct_answer = abs(input_sum + k)

        steps = []
        steps.append(f"Problem: Given f(x) = |x+{k}|, evaluate f({x1}+{x2})")
        steps.append("")
        steps.append("CORRECT METHOD: Simplify input FIRST, then apply function")
        steps.append("  |x+a| ≠ |x| + |a|")
        steps.append("")
        steps.append(f"Step 1: Simplify the input expression")
        steps.append(f"  {x1} + {x2} = {input_sum}")
        steps.append("")
        steps.append(f"Step 2: Apply the function to the simplified input")
        steps.append(f"  f({input_sum}) = |{input_sum}+{k}|")
        steps.append(f"  = |{input_sum + k}|")
        steps.append(f"  = {correct_answer}")
        steps.append("")
        steps.append(f"Final Answer: f({x1}+{x2}) = {correct_answer} ✓")
        steps.append("")
        steps.append(f"Note: If we incorrectly distributed: f({x1}) + f({x2}) = |{x1}+{k}| + |{x2}+{k}| = {problem.metadata['malrule_answer']}")
        steps.append(f"      This is WRONG! {correct_answer} ≠ {problem.metadata['malrule_answer']}")
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
            return self._verbose_word_problem_absolute(problem)
        else:
            return self._verbose_word_problem_square(problem)

    def _verbose_word_problem_square(self, problem: Problem) -> List[str]:
        """Verbose steps for word problems with f(x) = x² formula."""
        x1 = problem.metadata['value1']
        x2 = problem.metadata['value2']
        input_value = problem.metadata.get('input_value', x1 + x2)
        correct_answer = input_value ** 2

        steps = []
        steps.append(f"Word Problem: {problem.text}")
        steps.append("")
        steps.append("Step 1: Extract the mathematical function")
        steps.append(f"  Function: f(x) = x²")
        steps.append(f"  Need to find: f({x1}+{x2})")
        steps.append("")
        steps.append("Step 2: Simplify the input FIRST")
        steps.append(f"  {x1} + {x2} = {input_value}")
        steps.append("")
        steps.append("Step 3: Apply the function")
        steps.append(f"  f({input_value}) = ({input_value})²")
        steps.append(f"  = {correct_answer}")
        steps.append("")
        steps.append(f"Final Answer: {correct_answer} ✓")
        steps.append("")
        steps.append(f"Why not f({x1}) + f({x2})? Functions don't distribute!")
        steps.append(f"  Incorrect approach: {x1}² + {x2}² = {problem.metadata['malrule_answer']} ✗")
        return steps

    def _verbose_word_problem_scaled_square(self, problem: Problem) -> List[str]:
        """Verbose steps for word problems with f(x) = ax² formula."""
        a = problem.metadata['coefficient']
        x1 = problem.metadata['value1']
        x2 = problem.metadata['value2']
        input_value = problem.metadata.get('input_value', x1 + x2)
        correct_answer = a * (input_value ** 2)

        steps = []
        steps.append(f"Word Problem: {problem.text}")
        steps.append("")
        steps.append("Step 1: Extract the mathematical function")
        steps.append(f"  Function: f(x) = {a}x²")
        steps.append(f"  Need to find: f({x1}+{x2})")
        steps.append("")
        steps.append("Step 2: Simplify the input FIRST")
        steps.append(f"  {x1} + {x2} = {input_value}")
        steps.append("")
        steps.append("Step 3: Apply the function")
        steps.append(f"  f({input_value}) = {a}({input_value})²")
        steps.append(f"  = {a} × {input_value**2}")
        steps.append(f"  = {correct_answer}")
        steps.append("")
        steps.append(f"Final Answer: {correct_answer} ✓")
        steps.append("")
        steps.append(f"Why not f({x1}) + f({x2})? Functions don't distribute!")
        steps.append(f"  Incorrect: {a}×{x1}² + {a}×{x2}² = {problem.metadata['malrule_answer']} ✗")
        return steps

    def _verbose_word_problem_subtraction(self, problem: Problem) -> List[str]:
        """Verbose steps for word problems with f(x-a) formula."""
        a = problem.metadata['coefficient']
        x1 = problem.metadata['value1']
        x2 = problem.metadata['value2']
        input_value = problem.metadata.get('input_value', x1 - x2)
        correct_answer = a * (input_value ** 2)
        func_str = "x²" if a == 1 else f"{a}x²"

        steps = []
        steps.append(f"Word Problem: {problem.text}")
        steps.append("")
        steps.append("Step 1: Extract the mathematical function")
        steps.append(f"  Function: f(x) = {func_str}")
        steps.append(f"  Need to find: f({x1}-{x2})")
        steps.append("")
        steps.append("Step 2: Simplify the input FIRST")
        steps.append(f"  {x1} - {x2} = {input_value}")
        steps.append("")
        steps.append("Step 3: Apply the function")
        steps.append(f"  f({input_value}) = {a if a > 1 else ''}({input_value})²")
        steps.append(f"  = {correct_answer}")
        steps.append("")
        steps.append(f"Final Answer: {correct_answer} ✓")
        steps.append("")
        steps.append(f"Why not f({x1}) - f({x2})? Functions don't distribute!")
        steps.append(f"  Incorrect: {problem.metadata['malrule_answer']} ✗")
        return steps

    def _verbose_word_problem_cubic(self, problem: Problem) -> List[str]:
        """Verbose steps for word problems with f(x) = x³ formula."""
        x1 = problem.metadata['value1']
        x2 = problem.metadata['value2']
        input_value = problem.metadata.get('input_value', x1 + x2)
        correct_answer = input_value ** 3

        steps = []
        steps.append(f"Word Problem: {problem.text}")
        steps.append("")
        steps.append("Step 1: Extract the mathematical function")
        steps.append(f"  Function: f(x) = x³")
        steps.append(f"  Need to find: f({x1}+{x2})")
        steps.append("")
        steps.append("Step 2: Simplify the input FIRST")
        steps.append(f"  {x1} + {x2} = {input_value}")
        steps.append("")
        steps.append("Step 3: Apply the function")
        steps.append(f"  f({input_value}) = ({input_value})³")
        steps.append(f"  = {correct_answer}")
        steps.append("")
        steps.append(f"Final Answer: {correct_answer} ✓")
        steps.append("")
        steps.append(f"Why not f({x1}) + f({x2})? Functions don't distribute!")
        steps.append(f"  Incorrect: {x1}³ + {x2}³ = {problem.metadata['malrule_answer']} ✗")
        return steps

    def _verbose_word_problem_absolute(self, problem: Problem) -> List[str]:
        """Verbose steps for word problems with f(x) = |x+k| formula."""
        x1 = problem.metadata['value1']
        x2 = problem.metadata['value2']
        k = problem.metadata['k_value']
        input_value = problem.metadata.get('input_value', x1 + x2)
        correct_answer = abs(input_value + k)

        steps = []
        steps.append(f"Word Problem: {problem.text}")
        steps.append("")
        steps.append("Step 1: Extract the mathematical function")
        steps.append(f"  Function: f(x) = |x+{k}|")
        steps.append(f"  Need to find: f({x1}+{x2})")
        steps.append("")
        steps.append("Step 2: Simplify the input FIRST")
        steps.append(f"  {x1} + {x2} = {input_value}")
        steps.append("")
        steps.append("Step 3: Apply the function")
        steps.append(f"  f({input_value}) = |{input_value}+{k}|")
        steps.append(f"  = |{input_value + k}|")
        steps.append(f"  = {correct_answer}")
        steps.append("")
        steps.append(f"Final Answer: {correct_answer} ✓")
        steps.append("")
        steps.append(f"Why not f({x1}) + f({x2})? Functions don't distribute!")
        steps.append(f"  Incorrect: |{x1}+{k}| + |{x2}+{k}| = {problem.metadata['malrule_answer']} ✗")
        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        problem_type = problem.metadata.get('problem_type', 'square')

        # Compute the correct answer based on problem type
        if problem_type == 'subtraction_input':
            a = problem.metadata['coefficient']
            x1 = problem.metadata['value1']
            x2 = problem.metadata['value2']
            input_diff = problem.metadata.get('input_value', x1 - x2)
            correct_answer = a * (input_diff ** 2)
        elif problem_type == 'cubic_function':
            x1 = problem.metadata['value1']
            x2 = problem.metadata['value2']
            input_sum = problem.metadata.get('input_value', x1 + x2)
            correct_answer = input_sum ** 3
        elif problem_type == 'absolute_value':
            x1 = problem.metadata['value1']
            x2 = problem.metadata['value2']
            k = problem.metadata['k_value']
            input_sum = problem.metadata.get('input_value', x1 + x2)
            correct_answer = abs(input_sum + k)
        elif problem_type == 'word_problem_context':
            word_problem_type = problem.metadata.get('word_problem_type', 'square')
            if word_problem_type == 'square':
                x1 = problem.metadata['value1']
                x2 = problem.metadata['value2']
                input_value = problem.metadata.get('input_value', x1 + x2)
                correct_answer = input_value ** 2
            elif word_problem_type == 'scaled_square':
                a = problem.metadata['coefficient']
                x1 = problem.metadata['value1']
                x2 = problem.metadata['value2']
                input_value = problem.metadata.get('input_value', x1 + x2)
                correct_answer = a * (input_value ** 2)
            elif word_problem_type == 'subtraction_input':
                a = problem.metadata['coefficient']
                x1 = problem.metadata['value1']
                x2 = problem.metadata['value2']
                input_value = problem.metadata.get('input_value', x1 - x2)
                correct_answer = a * (input_value ** 2)
            elif word_problem_type == 'cubic_function':
                x1 = problem.metadata['value1']
                x2 = problem.metadata['value2']
                input_value = problem.metadata.get('input_value', x1 + x2)
                correct_answer = input_value ** 3
            elif word_problem_type == 'absolute_value':
                x1 = problem.metadata['value1']
                x2 = problem.metadata['value2']
                k = problem.metadata['k_value']
                input_value = problem.metadata.get('input_value', x1 + x2)
                correct_answer = abs(input_value + k)
            else:
                x1 = problem.metadata['value1']
                x2 = problem.metadata['value2']
                input_value = problem.metadata.get('input_value', x1 + x2)
                correct_answer = input_value ** 2
        else:
            # Original problem types (square and scaled_square)
            a = problem.metadata['coefficient']
            x1 = problem.metadata['value1']
            x2 = problem.metadata['value2']
            input_sum = problem.metadata.get('input_sum', problem.metadata.get('input_value', x1 + x2))
            correct_answer = a * (input_sum ** 2)

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
