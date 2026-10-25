"""
Malrule algorithm for Incomplete-Factoring.

Students stop factoring before the expression is completely factored.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution

class IncompleteFactoringMalrule(Malrule):
    """Student stops factoring before expression is completely factored."""

    def get_name(self):
        return "Incomplete-Factoring"

    def _generate_concise_steps(self, problem, template, expression, incomplete_answer,
                                 is_word_problem=False, **kwargs):
        """Generate concise steps with only formulas and values."""
        steps = []

        if is_word_problem:
            steps.append(f"Word Problem: {problem.text}")
            steps.append(f"Expression to factor: {expression}")
        else:
            steps.append(f"Factor completely: {expression}")

        word_problem_type = kwargs.get('word_problem_type', template)
        actual_template = word_problem_type if is_word_problem else template

        if actual_template == 'gcf_then_difference_of_squares':
            gcf = kwargs.get('gcf', 1)
            b = kwargs.get('b', 0)
            if gcf == 1:
                steps.append(f"GCF = 1")
            else:
                steps.append(f"GCF = {gcf}")
                steps.append(f"{expression} = {gcf}(x² - {b**2})")

        elif actual_template == 'gcf_then_trinomial':
            gcf = kwargs.get('gcf', 1)
            b_coeff = kwargs.get('b_coeff', 0)
            c_coeff = kwargs.get('c_coeff', 0)
            steps.append(f"GCF = {gcf}")
            steps.append(f"{expression} = {gcf}(x² + {b_coeff}x + {c_coeff})")

        elif actual_template == 'gcf_then_perfect_square':
            gcf = kwargs.get('gcf', 1)
            middle_coeff = kwargs.get('middle_coeff', 0)
            constant = kwargs.get('constant', 0)
            steps.append(f"GCF = {gcf}")
            steps.append(f"{expression} = {gcf}(x² + {middle_coeff}x + {constant})")

        elif actual_template == 'nested_factoring':
            b = kwargs.get('b', 0)
            steps.append(f"{expression} = x(x² - {b**2})")

        steps.append(f"{incomplete_answer}")
        return steps

    def _generate_verbose_steps(self, problem, template, expression, incomplete_answer,
                                 is_word_problem=False, **kwargs):
        """Generate verbose steps with full explanations (original format)."""
        steps = []

        if is_word_problem:
            steps.append(f"Word Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Extract the expression from the word problem")
            steps.append(f"  Expression to factor: {expression}")
            steps.append("")
            steps.append("Step 2: Factor (but student stops too early)")
            steps.append("")
        else:
            steps.append(f"Problem: Factor completely: {problem.text}")
            steps.append("")

        steps.append("MALRULE: Stop after first factoring step (incomplete)")
        steps.append("")

        word_problem_type = kwargs.get('word_problem_type', template)
        actual_template = word_problem_type if is_word_problem else template

        if actual_template == 'gcf_then_difference_of_squares':
            gcf = kwargs.get('gcf', 1)
            b = kwargs.get('b', 0)
            coefficient = kwargs.get('coefficient', gcf)
            constant = kwargs.get('constant', gcf * b**2)

            steps.append("Step 1: Find the GCF")
            if gcf == 1:
                steps.append(f"  GCF = 1 (no common factor)")
                steps.append(f"  Expression: x² - {b**2}")
            else:
                steps.append(f"  GCF of {coefficient} and {constant} is {gcf}")
                steps.append("")
                steps.append("Step 2: Factor out the GCF")
                steps.append(f"  {expression}")
                steps.append(f"  = {gcf}(x² - {b**2})")
            steps.append("")
            steps.append(f"Student stops here: {incomplete_answer}")
            steps.append("")
            steps.append("Student thinks: 'I factored it, I'm done!'")
            steps.append("")
            steps.append(
                f"WRONG! The student stops after factoring out the GCF. "
                f"They don't recognize that x² - {b**2} is a difference of squares "
                f"that can be factored further as (x + {b})(x - {b})."
            )

        elif actual_template == 'gcf_then_trinomial':
            gcf = kwargs.get('gcf', 1)
            p = kwargs.get('p', 0)
            q = kwargs.get('q', 0)
            b_coeff = kwargs.get('b_coeff', 0)
            c_coeff = kwargs.get('c_coeff', 0)

            steps.append("Step 1: Factor out the GCF")
            steps.append(f"  GCF = {gcf}")
            steps.append(f"  {expression}")
            steps.append(f"  = {gcf}(x² + {b_coeff}x + {c_coeff})")
            steps.append("")
            steps.append(f"Student stops here: {incomplete_answer}")
            steps.append("")
            steps.append("Student thinks: 'I factored out the GCF, I'm done!'")
            steps.append("")
            steps.append(
                f"WRONG! The trinomial x² + {b_coeff}x + {c_coeff} can be factored further! "
                f"It factors as (x + {p})(x + {q}) since {p} × {q} = {c_coeff} and {p} + {q} = {b_coeff}. "
                f"The complete factorization is {gcf}(x + {p})(x + {q})."
            )

        elif actual_template == 'gcf_then_perfect_square':
            gcf = kwargs.get('gcf', 1)
            a = kwargs.get('a', 0)
            middle_coeff = kwargs.get('middle_coeff', 0)
            constant = kwargs.get('constant', 0)

            steps.append("Step 1: Factor out the GCF")
            steps.append(f"  GCF = {gcf}")
            steps.append(f"  {expression}")
            steps.append(f"  = {gcf}(x² + {middle_coeff}x + {constant})")
            steps.append("")
            steps.append(f"Student stops here: {incomplete_answer}")
            steps.append("")
            steps.append("Student thinks: 'I factored out the GCF, I'm done!'")
            steps.append("")
            steps.append(
                f"WRONG! The trinomial x² + {middle_coeff}x + {constant} is a perfect square! "
                f"Notice: {middle_coeff} = 2 × {a} and {constant} = {a}². "
                f"So x² + {middle_coeff}x + {constant} = (x + {a})². "
                f"The complete factorization is {gcf}(x + {a})²."
            )

        elif actual_template == 'nested_factoring':
            b = kwargs.get('b', 0)

            steps.append("Step 1: Factor out x")
            steps.append(f"  {expression}")
            steps.append(f"  = x(x² - {b**2})")
            steps.append("")
            steps.append(f"Student stops here: {incomplete_answer}")
            steps.append("")
            steps.append("Student thinks: 'I factored out x, I'm done!'")
            steps.append("")
            steps.append(
                f"WRONG! The factor (x² - {b**2}) can be factored further! "
                f"It's a difference of squares: x² - {b**2} = (x + {b})(x - {b}). "
                f"The complete factorization is x(x + {b})(x - {b})."
            )

        steps.append("")
        steps.append("The fundamental error: Stopping before complete factorization!")

        return steps

    def get_description(self):
        return (
            "Students terminate the factoring process prematurely, stopping after one "
            "factoring step without recognizing that further factorization is possible. "
            "For example, writing 2x² - 8 = 2(x² - 4) instead of the complete factorization "
            "2(x+2)(x-2). This reflects a procedural rather than conceptual understanding "
            "of what 'factor completely' means (Kieran, 1992; Vaiyavutjamai & Clements, 2006)."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Malrule: student stops after one factoring step (incomplete)
        template = problem.metadata.get('template', 'gcf_then_difference_of_squares')

        # For word problems, use the embedded formula type
        if problem.metadata.get('is_word_problem', False):
            template = problem.metadata.get('word_problem_type', template)

        if template == 'gcf_then_difference_of_squares':
            gcf = problem.metadata['gcf']
            b = problem.metadata['b']
            if gcf == 1:
                return f"x² - {b**2}"
            else:
                return f"{gcf}(x² - {b**2})"
        elif template == 'gcf_then_trinomial':
            gcf = problem.metadata['gcf']
            b_coeff = problem.metadata['b_coeff']
            c_coeff = problem.metadata['c_coeff']
            return f"{gcf}(x² + {b_coeff}x + {c_coeff})"
        elif template == 'gcf_then_perfect_square':
            gcf = problem.metadata['gcf']
            middle_coeff = problem.metadata['middle_coeff']
            constant = problem.metadata['constant']
            return f"{gcf}(x² + {middle_coeff}x + {constant})"
        elif template == 'nested_factoring':
            b = problem.metadata['b']
            return f"x(x² - {b**2})"
        else:
            return f"incomplete"

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the incomplete-factoring malrule across all templates.

        Args:
            problem: The factoring problem
            verbose: If True, generate verbose steps; if False, generate concise steps (default)

        Returns:
            Solution showing incomplete factoring (stops after first step)
        """
        template = problem.metadata.get('template', 'gcf_then_difference_of_squares')
        expression = problem.metadata['expression']

        # Check if this is a word problem
        is_word_problem = problem.metadata.get('is_word_problem', False)
        word_problem_type = problem.metadata.get('word_problem_type', None)

        # Build kwargs based on template
        kwargs = {'word_problem_type': word_problem_type}

        # Calculate incomplete answer based on template
        actual_template = word_problem_type if (template == 'word_problem' and word_problem_type) else template

        if actual_template == 'gcf_then_difference_of_squares':
            gcf = problem.metadata['gcf']
            b = problem.metadata['b']
            coefficient = problem.metadata.get('coefficient', gcf)
            constant = problem.metadata.get('constant', gcf * b**2)
            kwargs.update({'gcf': gcf, 'b': b, 'coefficient': coefficient, 'constant': constant})
            if gcf == 1:
                incomplete_answer = f"x² - {b**2}"
            else:
                incomplete_answer = f"{gcf}(x² - {b**2})"

        elif actual_template == 'gcf_then_trinomial':
            gcf = problem.metadata['gcf']
            p = problem.metadata['p']
            q = problem.metadata['q']
            b_coeff = problem.metadata['b_coeff']
            c_coeff = problem.metadata['c_coeff']
            kwargs.update({'gcf': gcf, 'p': p, 'q': q, 'b_coeff': b_coeff, 'c_coeff': c_coeff})
            incomplete_answer = f"{gcf}(x² + {b_coeff}x + {c_coeff})"

        elif actual_template == 'gcf_then_perfect_square':
            gcf = problem.metadata['gcf']
            a = problem.metadata['a']
            middle_coeff = problem.metadata['middle_coeff']
            constant = problem.metadata['constant']
            kwargs.update({'gcf': gcf, 'a': a, 'middle_coeff': middle_coeff, 'constant': constant})
            incomplete_answer = f"{gcf}(x² + {middle_coeff}x + {constant})"

        elif actual_template == 'nested_factoring':
            b = problem.metadata['b']
            kwargs.update({'b': b})
            incomplete_answer = f"x(x² - {b**2})"

        else:
            incomplete_answer = "incomplete"

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, template, expression, incomplete_answer,
                                                  is_word_problem=is_word_problem, **kwargs)
        else:
            steps = self._generate_concise_steps(problem, template, expression, incomplete_answer,
                                                  is_word_problem=is_word_problem, **kwargs)

        return Solution(
            answer=incomplete_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
