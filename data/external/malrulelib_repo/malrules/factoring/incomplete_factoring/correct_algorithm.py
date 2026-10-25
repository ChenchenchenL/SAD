"""
Correct algorithm for complete factoring.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import CorrectAlgorithm, Problem, Solution


class CompleteFactoringCorrectAlgorithm(CorrectAlgorithm):
    """Correctly factors completely by continuing until no more factoring possible."""

    def get_name(self):
        return "Complete Factoring"

    def get_description(self):
        return "Factors completely by recognizing and applying all applicable factoring patterns"

    def _generate_concise_steps(self, problem, template, expression, complete_answer,
                                 is_word_problem=False, **kwargs):
        """Generate concise steps with only formulas and values."""
        steps = []

        if is_word_problem:
            steps.append(f"Word Problem: {problem.text}")
            steps.append(f"Expression to factor: {expression}")
        else:
            steps.append(f"Factor completely: {expression}")

        if template == 'gcf_then_difference_of_squares' or (is_word_problem and kwargs.get('word_problem_type') == 'gcf_then_difference_of_squares'):
            gcf = kwargs.get('gcf', 1)
            b = kwargs.get('b', 0)
            if gcf != 1:
                steps.append(f"GCF = {gcf}")
                steps.append(f"{expression} = {gcf}(x² - {b**2})")
            steps.append(f"x² - {b**2} = (x + {b})(x - {b})")

        elif template == 'gcf_then_trinomial' or (is_word_problem and kwargs.get('word_problem_type') == 'gcf_then_trinomial'):
            gcf = kwargs.get('gcf', 1)
            p = kwargs.get('p', 0)
            q = kwargs.get('q', 0)
            b_coeff = kwargs.get('b_coeff', 0)
            c_coeff = kwargs.get('c_coeff', 0)
            steps.append(f"GCF = {gcf}")
            steps.append(f"{expression} = {gcf}(x² + {b_coeff}x + {c_coeff})")
            steps.append(f"{p} × {q} = {c_coeff}, {p} + {q} = {b_coeff}")
            steps.append(f"x² + {b_coeff}x + {c_coeff} = (x + {p})(x + {q})")

        elif template == 'gcf_then_perfect_square' or (is_word_problem and kwargs.get('word_problem_type') == 'gcf_then_perfect_square'):
            gcf = kwargs.get('gcf', 1)
            a = kwargs.get('a', 0)
            middle_coeff = kwargs.get('middle_coeff', 0)
            constant = kwargs.get('constant', 0)
            steps.append(f"GCF = {gcf}")
            steps.append(f"{expression} = {gcf}(x² + {middle_coeff}x + {constant})")
            steps.append(f"x² + {middle_coeff}x + {constant} = (x + {a})²")

        elif template == 'nested_factoring' or (is_word_problem and kwargs.get('word_problem_type') == 'nested_factoring'):
            b = kwargs.get('b', 0)
            steps.append(f"{expression} = x(x² - {b**2})")
            steps.append(f"x² - {b**2} = (x + {b})(x - {b})")

        steps.append(f"{complete_answer}")
        return steps

    def _generate_verbose_steps(self, problem, template, expression, complete_answer,
                                 is_word_problem=False, **kwargs):
        """Generate verbose steps with full explanations (original format)."""
        steps = []

        if is_word_problem:
            steps.append(f"Word Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Extract the expression from the word problem")
            steps.append(f"  Expression to factor: {expression}")
            steps.append("")
            steps.append("Step 2: Apply complete factoring method")
            steps.append("")
        else:
            steps.append(f"Problem: Factor completely: {problem.text}")
            steps.append("")

        steps.append("CORRECT METHOD: Factor completely (all steps)")
        steps.append("")
        steps.append("Strategy: Factor until no more factoring is possible")
        steps.append("")

        word_problem_type = kwargs.get('word_problem_type', template)
        actual_template = word_problem_type if is_word_problem else template
        step_offset = 2 if is_word_problem else 0

        if actual_template == 'gcf_then_difference_of_squares':
            gcf = kwargs.get('gcf', 1)
            b = kwargs.get('b', 0)

            steps.append(f"Step {1 + step_offset}: Find and factor out the GCF")
            if gcf == 1:
                steps.append(f"  GCF = 1 (no common factor to factor out)")
                steps.append(f"  Continue with: x² - {b**2}")
            else:
                steps.append(f"  GCF = {gcf}")
                steps.append(f"  {expression} = {gcf}(x² - {b**2})")
            steps.append("")
            steps.append(f"Step {2 + step_offset}: Check if the factored part can be factored further")
            steps.append(f"  Look at: x² - {b**2}")
            steps.append(f"  This is a difference of squares!")
            steps.append(f"  Pattern: a² - b² = (a + b)(a - b)")
            steps.append("")
            steps.append(f"Step {3 + step_offset}: Apply difference of squares formula")
            steps.append(f"  x² - {b**2} = (x + {b})(x - {b})")
            steps.append("")
            steps.append(f"Step {4 + step_offset}: Combine all factors")
            if gcf == 1:
                steps.append(f"  Final answer: (x + {b})(x - {b})")
            else:
                steps.append(f"  = {gcf}(x + {b})(x - {b})")

        elif actual_template == 'gcf_then_trinomial':
            gcf = kwargs.get('gcf', 1)
            p = kwargs.get('p', 0)
            q = kwargs.get('q', 0)
            b_coeff = kwargs.get('b_coeff', 0)
            c_coeff = kwargs.get('c_coeff', 0)

            steps.append(f"Step {1 + step_offset}: Factor out the GCF")
            steps.append(f"  GCF = {gcf}")
            steps.append(f"  {expression} = {gcf}(x² + {b_coeff}x + {c_coeff})")
            steps.append("")
            steps.append(f"Step {2 + step_offset}: Factor the trinomial")
            steps.append(f"  Need two numbers that multiply to {c_coeff} and add to {b_coeff}")
            steps.append(f"  {p} × {q} = {c_coeff} and {p} + {q} = {b_coeff} ✓")
            steps.append(f"  x² + {b_coeff}x + {c_coeff} = (x + {p})(x + {q})")
            steps.append("")
            steps.append(f"Step {3 + step_offset}: Combine all factors")
            steps.append(f"  = {gcf}(x + {p})(x + {q})")

        elif actual_template == 'gcf_then_perfect_square':
            gcf = kwargs.get('gcf', 1)
            a = kwargs.get('a', 0)
            middle_coeff = kwargs.get('middle_coeff', 0)
            constant = kwargs.get('constant', 0)

            steps.append(f"Step {1 + step_offset}: Factor out the GCF")
            steps.append(f"  GCF = {gcf}")
            steps.append(f"  {expression} = {gcf}(x² + {middle_coeff}x + {constant})")
            steps.append("")
            steps.append(f"Step {2 + step_offset}: Recognize the perfect square trinomial")
            steps.append(f"  Check: Is this a perfect square?")
            steps.append(f"  First term: x² = (x)²")
            steps.append(f"  Last term: {constant} = ({a})²")
            steps.append(f"  Middle term: {middle_coeff}x = 2 × x × {a}  ✓")
            steps.append(f"  Pattern: a² + 2ab + b² = (a + b)²")
            steps.append("")
            steps.append(f"Step {3 + step_offset}: Apply perfect square formula")
            steps.append(f"  x² + {middle_coeff}x + {constant} = (x + {a})²")
            steps.append("")
            steps.append(f"Step {4 + step_offset}: Combine all factors")
            steps.append(f"  = {gcf}(x + {a})²")

        elif actual_template == 'nested_factoring':
            b = kwargs.get('b', 0)

            steps.append(f"Step {1 + step_offset}: Factor out the common variable x")
            steps.append(f"  {expression} = x(x² - {b**2})")
            steps.append("")
            steps.append(f"Step {2 + step_offset}: Check if the factored part can be factored further")
            steps.append(f"  Look at: x² - {b**2}")
            steps.append(f"  This is a difference of squares!")
            steps.append(f"  Pattern: a² - b² = (a + b)(a - b)")
            steps.append("")
            steps.append(f"Step {3 + step_offset}: Apply difference of squares formula")
            steps.append(f"  x² - {b**2} = (x + {b})(x - {b})")
            steps.append("")
            steps.append(f"Step {4 + step_offset}: Combine all factors")
            steps.append(f"  = x(x + {b})(x - {b})")

        steps.append("")
        steps.append("Final Step: Verify it's completely factored")
        steps.append("  Each factor is either a number or linear (cannot factor further)")
        steps.append("  ✓ Expression is completely factored!")
        steps.append("")
        steps.append(f"Answer: {complete_answer}")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct complete factoring algorithm across all templates.

        Args:
            problem: The factoring problem
            verbose: If True, generate verbose steps; if False, generate concise steps (default)

        Returns:
            Solution showing complete factoring
        """
        template = problem.metadata.get('template', 'gcf_then_difference_of_squares')
        expression = problem.metadata['expression']

        # Check if this is a word problem
        is_word_problem = problem.metadata.get('is_word_problem', False)
        word_problem_type = problem.metadata.get('word_problem_type', None)

        # Build kwargs based on template
        kwargs = {'word_problem_type': word_problem_type}

        # Calculate complete answer based on template
        actual_template = word_problem_type if (template == 'word_problem' and word_problem_type) else template

        if actual_template == 'gcf_then_difference_of_squares':
            gcf = problem.metadata['gcf']
            b = problem.metadata['b']
            kwargs.update({'gcf': gcf, 'b': b})
            if gcf == 1:
                complete_answer = f"(x + {b})(x - {b})"
            else:
                complete_answer = f"{gcf}(x + {b})(x - {b})"

        elif actual_template == 'gcf_then_trinomial':
            gcf = problem.metadata['gcf']
            p = problem.metadata['p']
            q = problem.metadata['q']
            b_coeff = problem.metadata['b_coeff']
            c_coeff = problem.metadata['c_coeff']
            kwargs.update({'gcf': gcf, 'p': p, 'q': q, 'b_coeff': b_coeff, 'c_coeff': c_coeff})
            complete_answer = f"{gcf}(x + {p})(x + {q})"

        elif actual_template == 'gcf_then_perfect_square':
            gcf = problem.metadata['gcf']
            a = problem.metadata['a']
            middle_coeff = problem.metadata['middle_coeff']
            constant = problem.metadata['constant']
            kwargs.update({'gcf': gcf, 'a': a, 'middle_coeff': middle_coeff, 'constant': constant})
            complete_answer = f"{gcf}(x + {a})²"

        elif actual_template == 'nested_factoring':
            b = problem.metadata['b']
            kwargs.update({'b': b})
            complete_answer = f"x(x + {b})(x - {b})"

        else:
            complete_answer = "Unable to determine"

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, template, expression, complete_answer,
                                                  is_word_problem=is_word_problem, **kwargs)
        else:
            steps = self._generate_concise_steps(problem, template, expression, complete_answer,
                                                  is_word_problem=is_word_problem, **kwargs)

        return Solution(
            answer=complete_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
