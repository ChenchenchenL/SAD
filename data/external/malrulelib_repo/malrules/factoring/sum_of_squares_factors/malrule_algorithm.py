"""
Malrule algorithm for Sum-Of-Squares-Factors.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution

class SumOfSquaresFactorsMalrule(Malrule):
    """Student incorrectly factors sum of squares."""

    def get_name(self):
        return "Sum-Of-Squares-Factors"

    def _generate_concise_steps(self, problem, template, expression, malrule_answer,
                                 is_word_problem=False, **kwargs):
        """Generate concise steps with only formulas and values."""
        steps = []

        if is_word_problem:
            steps.append(f"Word Problem: {problem.text}")
            steps.append(f"Expression to factor: {expression}")
        else:
            steps.append(f"Factor: {expression}")

        # steps.append(f"Student thinks a² + b² = (a+b)²")

        b = kwargs.get('b', None)
        if b is not None:
            steps.append(f"(x + {b})² = x² + {b**2}")

        steps.append(f"{malrule_answer}")
        return steps

    def _generate_verbose_steps(self, problem, template, expression, malrule_answer,
                                 is_word_problem=False, **kwargs):
        """Generate verbose steps with full explanations (original format)."""
        steps = []

        if is_word_problem:
            steps.append(f"Word Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Extract the expression from the word problem")
            steps.append(f"  Expression to factor: {expression}")
            steps.append("")
            steps.append("Step 2: Factor (student applies malrule)")
            steps.append("")
        else:
            steps.append(f"Problem: Factor {expression}")
            steps.append("")

        steps.append(f"MALRULE: Student thinks a² + b² = (a+b)²")
        steps.append("")

        if template == 'basic_sum_of_squares':
            b = kwargs.get('b', 0)
            steps.append(f"  Student sees x² + {b**2}")
            steps.append(f"  Student incorrectly factors as (x + {b})²")
            steps.append("")
            steps.append(f"Student's answer: {malrule_answer}")
            steps.append("")
            steps.append(f"WRONG! Expanding (x+{b})² = x² + {2*b}x + {b**2}, not x² + {b**2}")

        elif template == 'coefficient_on_x':
            a = kwargs.get('a', 0)
            c = kwargs.get('c', 0)
            steps.append(f"  Student sees {a}x² + {c**2}")
            steps.append(f"  Student incorrectly factors as ({a}x + {c})²")
            steps.append("")
            steps.append(f"Student's answer: {malrule_answer}")
            steps.append("")
            steps.append(f"WRONG! Expanding ({a}x+{c})² = {a**2}x² + {2*a*c}x + {c**2}, not {a}x² + {c**2}")

        elif template == 'both_variables':
            has_coeff = kwargs.get('has_coeff', False)
            steps.append(f"  Student sees {expression}")
            steps.append(f"  Student incorrectly factors as {malrule_answer}")
            steps.append("")
            steps.append(f"Student's answer: {malrule_answer}")
            steps.append("")
            if has_coeff:
                steps.append(f"WRONG! Sum of squares cannot be factored over real numbers")
            else:
                steps.append(f"WRONG! Expanding (x+y)² = x² + 2xy + y², not x² + y²")

        elif template == 'larger_coefficients':
            b = kwargs.get('b', 0)
            b_sq = kwargs.get('b_squared', b**2)
            steps.append(f"  Student sees x² + {b_sq}")
            steps.append(f"  Student recognizes {b_sq} = {b}²")
            steps.append(f"  Student incorrectly factors as (x + {b})²")
            steps.append("")
            steps.append(f"Student's answer: {malrule_answer}")
            steps.append("")
            steps.append(f"WRONG! Expanding (x+{b})² = x² + {2*b}x + {b**2}, not x² + {b**2}")

        else:  # word_problem or other
            steps.append(f"  Student attempts to factor {expression}")
            steps.append(f"  Student incorrectly applies pattern: {malrule_answer}")
            steps.append("")
            steps.append(f"Student's answer: {malrule_answer}")
            steps.append("")
            steps.append(f"WRONG! Sum of squares (a² + b²) CANNOT be factored over real numbers")

        steps.append("")
        steps.append("The fundamental error: a² + b² is PRIME over the reals (cannot be factored)")

        return steps

    def get_description(self):
        return (
            "Students incorrectly factor the sum of squares a² + b² as (a+b)², failing to "
            "recognize that sum of squares is irreducible over real numbers. This is documented "
            "as one of the most common algebraic misconceptions, arising from inappropriate "
            "generalization of the difference of squares pattern (Matz, 1982; Perso, 1991)."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Malrule: incorrectly factor a² + b² as (a+b)²
        template = problem.metadata.get('template', 'basic_sum_of_squares')

        if template == 'basic_sum_of_squares':
            b = problem.metadata.get('b', 1)
            return f"(x + {b})²"
        elif template == 'coefficient_on_x':
            a = problem.metadata.get('a', 1)
            c = problem.metadata.get('c', 1)
            return f"({a}x + {c})²"
        elif template == 'both_variables':
            has_coeff = problem.metadata.get('has_coeff', False)
            if has_coeff:
                a = problem.metadata.get('a', 1)
                b = problem.metadata.get('b', 1)
                return f"({a}x + {b}y)²"
            else:
                return "(x + y)²"
        elif template == 'larger_coefficients':
            b = problem.metadata.get('b', 1)
            return f"(x + {b})²"
        elif template == 'word_problem':
            # For word problems, delegate to embedded problem type
            word_problem_type = problem.metadata.get('word_problem_type', 'basic_sum_of_squares')
            # Create a new problem metadata with the template set to word_problem_type
            temp_problem = Problem(
                text=problem.text,
                operands=problem.operands,
                operation=problem.operation,
                level=problem.level,
                difficulty=problem.difficulty,
                metadata={**problem.metadata, 'template': word_problem_type}
            )
            return self.calculate_expected_answer(temp_problem)
        else:
            return "incorrectly factored"

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the sum-of-squares-factors malrule across all templates.

        Args:
            problem: The sum of squares problem
            verbose: If True, generate verbose steps; if False, generate concise steps (default)

        Returns:
            Solution showing the incorrect factorization
        """
        template = problem.metadata.get('template', 'basic_sum_of_squares')
        expression = problem.metadata['expression']
        is_word_problem = problem.metadata.get('is_word_problem', False)
        word_problem_type = problem.metadata.get('word_problem_type', None)

        # Calculate malrule answer
        malrule_answer = self.calculate_expected_answer(problem)

        # Build kwargs based on template
        kwargs = {'word_problem_type': word_problem_type}

        actual_template = word_problem_type if (template == 'word_problem' and word_problem_type) else template

        if actual_template == 'basic_sum_of_squares':
            b = problem.metadata['b']
            kwargs['b'] = b
        elif actual_template == 'coefficient_on_x':
            a = problem.metadata['a']
            c = problem.metadata['c']
            kwargs.update({'a': a, 'c': c})
        elif actual_template == 'both_variables':
            has_coeff = problem.metadata.get('has_coeff', False)
            kwargs['has_coeff'] = has_coeff
        elif actual_template == 'larger_coefficients':
            b = problem.metadata['b']
            b_squared = problem.metadata.get('b_squared', b**2)
            kwargs.update({'b': b, 'b_squared': b_squared})

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, actual_template, expression, malrule_answer,
                                                  is_word_problem=is_word_problem, **kwargs)
        else:
            steps = self._generate_concise_steps(problem, actual_template, expression, malrule_answer,
                                                  is_word_problem=is_word_problem, **kwargs)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
