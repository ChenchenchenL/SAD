"""
Correct algorithm for sum of squares.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import CorrectAlgorithm, Problem, Solution


class SumOfSquaresCorrectAlgorithm(CorrectAlgorithm):
    """Correctly recognizes sum of squares cannot be factored over reals."""

    def get_name(self):
        return "Correct Sum of Squares Recognition"

    def get_description(self):
        return "Recognizes that a² + b² cannot be factored over real numbers"

    def _generate_concise_steps(self, problem, template, expression, correct_answer,
                                 is_word_problem=False, **kwargs):
        """Generate concise steps with only formulas and values."""
        steps = []

        if is_word_problem:
            steps.append(f"Word Problem: {problem.text}")
            steps.append(f"Expression to factor: {expression}")
        else:
            steps.append(f"Factor: {expression}")

        steps.append(f"{expression} is a sum of squares")
        steps.append(f"a² + b² cannot be factored over reals")

        b = kwargs.get('b', None)
        if b is not None:
            steps.append(f"(x + {b})² = x² + {2*b}x + {b**2} ≠ {expression}")

        steps.append(f"{correct_answer}")
        return steps

    def _generate_verbose_steps(self, problem, template, expression, correct_answer,
                                 is_word_problem=False, **kwargs):
        """Generate verbose steps with full explanations (original format)."""
        steps = []

        if is_word_problem:
            steps.append(f"Word Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Extract the expression from the word problem")
            steps.append(f"  Expression to factor: {expression}")
            steps.append("")
            steps.append("Step 2: Analyze the expression")
            steps.append("")
        else:
            steps.append(f"Problem: Factor {expression}")
            steps.append("")

        steps.append("CORRECT METHOD: Recognize sum of squares pattern")
        steps.append(f"  {expression} is a sum of squares")
        steps.append("")
        steps.append("Key fact: a² + b² CANNOT be factored over real numbers")
        steps.append("(This is different from a² - b² which factors as (a-b)(a+b))")
        steps.append("")

        b = kwargs.get('b', None)
        if b is not None:
            steps.append(f"Check: Does it match perfect square? (x+{b})² = x² + {2*b}x + {b**2}")
            steps.append(f"  NO! Missing the middle term {2*b}x")
        else:
            steps.append("Sum of squares is PRIME over the reals")

        steps.append("")
        steps.append(f"Answer: {correct_answer}")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct sum of squares algorithm.

        Args:
            problem: The sum of squares problem
            verbose: If True, generate verbose steps; if False, generate concise steps (default)

        Returns:
            Solution showing that sum of squares is prime
        """
        expression = problem.metadata['expression']
        template = problem.metadata.get('template', 'basic_sum_of_squares')
        is_word_problem = problem.metadata.get('is_word_problem', False)
        word_problem_type = problem.metadata.get('word_problem_type', None)

        kwargs = {'word_problem_type': word_problem_type}

        # Calculate the correct answer based on template
        actual_template = word_problem_type if (template == 'word_problem' and word_problem_type) else template

        if actual_template == 'basic_sum_of_squares':
            b = problem.metadata['b']
            correct_answer = f"x² + {b**2} (prime/cannot be factored)"
            kwargs['b'] = b
        elif actual_template == 'coefficient_on_x':
            a = problem.metadata.get('a', 1)
            c = problem.metadata.get('c', 1)
            correct_answer = f"{a}x² + {c**2} (cannot be factored over reals)"
        elif actual_template == 'both_variables':
            has_coeff = problem.metadata.get('has_coeff', False)
            if has_coeff:
                a = problem.metadata.get('a', 1)
                b = problem.metadata.get('b', 1)
                correct_answer = f"{a}²x² + {b}²y² (cannot be factored)"
            else:
                correct_answer = "x² + y² (prime over reals)"
        elif actual_template == 'larger_coefficients':
            b = problem.metadata.get('b', 1)
            b_squared = problem.metadata.get('b_squared', b**2)
            correct_answer = f"x² + {b_squared} (cannot be factored)"
            kwargs['b'] = b
        else:
            correct_answer = f"{expression} (cannot be factored)"
            b = problem.metadata.get('b', None)
            if b is not None:
                kwargs['b'] = b

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, template, expression, correct_answer,
                                                  is_word_problem=is_word_problem, **kwargs)
        else:
            steps = self._generate_concise_steps(problem, template, expression, correct_answer,
                                                  is_word_problem=is_word_problem, **kwargs)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
