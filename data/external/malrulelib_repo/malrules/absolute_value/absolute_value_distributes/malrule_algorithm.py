"""
Malrule algorithm for Absolute-Value-Distributes.

Students think: |x+2| = |x| + 2 instead of evaluating inside first
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution

class AbsoluteValueDistributesMalrule(Malrule):
    """Student incorrectly distributes absolute value over addition/subtraction."""

    def get_name(self):
        return "Absolute-Value-Distributes"

    def get_description(self):
        return (
            "Students incorrectly distribute absolute value over addition or subtraction, "
            "treating |a+b| as |a|+|b|. This is an overgeneralization of the distributive "
            "property, where students apply learned algebraic rules (like distribution) to "
            "functions where they do not apply. The absolute value bars are visually similar "
            "to parentheses, reinforcing this erroneous application."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        template = problem.metadata.get('template', 'basic_addition')
        x = problem.metadata['x_value']

        # Apply malrule: distribute absolute value incorrectly
        if template == 'multiplication_inside' or (template == 'word_problem' and problem.metadata.get('word_problem_type') == 'ax_plus_b'):
            a = problem.metadata.get('coefficient', 2)
            b = problem.metadata.get('constant', 0)
            malrule_value = a * abs(x) + b
        else:
            c = problem.metadata.get('constant', 0)
            operation = problem.metadata.get('operation', '+')
            if operation == '+':
                malrule_value = abs(x) + c
            else:  # subtraction
                malrule_value = abs(x) - c

        # For word problems, format appropriately
        if template == 'word_problem':
            context_type = problem.metadata.get('context_type', 'temperature')
            if context_type == 'temperature':
                return f"{malrule_value} degrees"
            elif context_type == 'distance':
                return f"{malrule_value} meters"
            elif context_type == 'money':
                return f"${malrule_value}"
            else:
                return str(malrule_value)
        else:
            return str(malrule_value)

    def _generate_verbose_steps(self, problem: Problem, template: str, x: int, expression: str,
                                malrule_answer: str) -> list:
        """Generate verbose, explanatory steps."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")

        # Handle word problems by detecting embedded formula type
        if template == 'word_problem':
            word_problem_type = problem.metadata.get('word_problem_type', 'x_plus_c')
            steps.append("MALRULE: Student distributes absolute value in word problem")
            steps.append("")
            steps.append(f"Step 1: Identify the formula (student sees: |{expression}|)")
            steps.append("")

            if word_problem_type == 'ax_plus_b':
                a = problem.metadata['coefficient']
                b = problem.metadata['constant']
                operation = problem.metadata['operation']
                steps.append(f"  Student thinks: |{expression}| = |{a}x| {operation} {abs(b)}")
                steps.append(f"  = {a}|x| {operation} {abs(b)}")
                steps.append("")
                steps.append(f"Step 2: Apply absolute value to x")
                steps.append(f"  |x| = |{x}| = {abs(x)}")
                steps.append("")
                steps.append(f"Step 3: Calculate {a}|x|")
                steps.append(f"  {a} × {abs(x)} = {a * abs(x)}")
                steps.append("")
                steps.append(f"Step 4: Apply operation")
                steps.append(f"  {a * abs(x)} {operation} {abs(b)} = {malrule_answer}")
            else:
                c = problem.metadata['constant']
                operation = problem.metadata['operation']
                if operation == '+':
                    steps.append(f"  Student thinks: |x + {c}| = |x| + {c}")
                else:
                    steps.append(f"  Student thinks: |x - {c}| = |x| - {c}")
                steps.append("")
                steps.append(f"Step 2: Apply absolute value to x")
                steps.append(f"  |x| = |{x}| = {abs(x)}")
                steps.append("")
                steps.append(f"Step 3: Apply operation with constant")
                if operation == '+':
                    steps.append(f"  {abs(x)} + {c} = {malrule_answer}")
                else:
                    steps.append(f"  {abs(x)} - {c} = {malrule_answer}")

            steps.append("")
            steps.append(f"Student's answer: {malrule_answer}")
            steps.append("")
            steps.append(
                f"The student incorrectly distributes the absolute value in this word problem. "
                f"They should evaluate {expression} first, then take the absolute value."
            )
        else:
            c = problem.metadata['constant']
            operation = problem.metadata['operation']
            steps.append("MALRULE: Distribute absolute value over addition/subtraction")
            steps.append("")

            if template == 'multiplication_inside':
                a = problem.metadata['coefficient']
                b = problem.metadata['constant']
                steps.append(f"  Student thinks: |{expression}| = |{a}x| {operation} {abs(b)}")
                steps.append(f"  = {a}|x| {operation} {abs(b)}")
                steps.append("")
                steps.append(f"Step 1: Apply absolute value to x")
                steps.append(f"  |x| = |{x}| = {abs(x)}")
                steps.append("")
                steps.append(f"Step 2: Calculate {a}|x|")
                steps.append(f"  {a} × {abs(x)} = {a * abs(x)}")
                steps.append("")
                steps.append(f"Step 3: Apply operation")
                steps.append(f"  {a * abs(x)} {operation} {abs(b)} = {malrule_answer}")
            else:
                if operation == '+':
                    steps.append(f"  Student thinks: |x + {c}| = |x| + {c}")
                else:
                    steps.append(f"  Student thinks: |x - {c}| = |x| - {c}")
                steps.append("")
                steps.append(f"Step 1: Apply absolute value to x")
                steps.append(f"  |x| = |{x}| = {abs(x)}")
                steps.append("")
                steps.append(f"Step 2: Apply operation with constant")
                if operation == '+':
                    steps.append(f"  {abs(x)} + {c} = {malrule_answer}")
                else:
                    steps.append(f"  {abs(x)} - {c} = {malrule_answer}")

            steps.append("")
            steps.append(f"Student's answer: {malrule_answer}")
            steps.append("")
            steps.append(
                f"The student incorrectly distributes the absolute value. "
                f"They treat |{expression}| as if absolute value distributes over operations, "
                f"but it does NOT. The correct approach is to evaluate {expression} first, "
                f"then take the absolute value of the result."
            )

        return steps

    def _generate_concise_steps(self, problem: Problem, template: str, x: int, expression: str,
                                malrule_answer: str) -> list:
        """Generate concise steps with just formulas and values."""
        steps = [f"Problem: {problem.text}"]

        # Handle word problems by detecting embedded formula type
        if template == 'word_problem':
            word_problem_type = problem.metadata.get('word_problem_type', 'x_plus_c')
            steps.append(f"|{expression}|")

            if word_problem_type == 'ax_plus_b':
                a = problem.metadata['coefficient']
                b = problem.metadata['constant']
                operation = problem.metadata['operation']
                steps.append(f"{a}|x| {operation} {abs(b)}")
                steps.append(f"{a}×{abs(x)} {operation} {abs(b)}")
                steps.append(f"{a * abs(x)} {operation} {abs(b)}")
            else:
                c = problem.metadata['constant']
                operation = problem.metadata['operation']
                if operation == '+':
                    steps.append(f"|x| + {c}")
                else:
                    steps.append(f"|x| - {c}")
                steps.append(f"{abs(x)} {operation} {c}")

            steps.append(malrule_answer)
        else:
            c = problem.metadata['constant']
            operation = problem.metadata['operation']

            if template == 'multiplication_inside':
                a = problem.metadata['coefficient']
                b = problem.metadata['constant']
                steps.append(f"|{expression}|")
                steps.append(f"{a}|x| {operation} {abs(b)}")
                steps.append(f"{a}×{abs(x)} {operation} {abs(b)}")
                steps.append(f"{a * abs(x)} {operation} {abs(b)}")
            else:
                steps.append(f"|{expression}|")
                if operation == '+':
                    steps.append(f"|x| + {c}")
                else:
                    steps.append(f"|x| - {c}")
                steps.append(f"{abs(x)} {operation} {c}")

            steps.append(malrule_answer)

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the absolute-value-distributes malrule.

        Args:
            problem: The absolute value problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution showing incorrect reasoning (distributing absolute value)
        """
        template = problem.metadata.get('template', 'basic_addition')
        x = problem.metadata['x_value']
        expression = problem.metadata['expression']

        # Actually compute the malrule answer by distributing absolute value incorrectly
        if template == 'multiplication_inside' or (template == 'word_problem' and problem.metadata.get('word_problem_type') == 'ax_plus_b'):
            a = problem.metadata.get('coefficient', 2)
            b = problem.metadata.get('constant', 0)
            malrule_value = a * abs(x) + b
        else:
            c = problem.metadata.get('constant', 0)
            operation = problem.metadata.get('operation', '+')
            if operation == '+':
                malrule_value = abs(x) + c
            else:  # subtraction
                malrule_value = abs(x) - c

        # For word problems, format appropriately
        if template == 'word_problem':
            context_type = problem.metadata.get('context_type', 'temperature')
            if context_type == 'temperature':
                malrule_answer = f"{malrule_value} degrees"
            elif context_type == 'distance':
                malrule_answer = f"{malrule_value} meters"
            elif context_type == 'money':
                malrule_answer = f"${malrule_value}"
            else:
                malrule_answer = str(malrule_value)
        else:
            malrule_answer = str(malrule_value)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, template, x, expression, malrule_answer)
        else:
            steps = self._generate_concise_steps(problem, template, x, expression, malrule_answer)

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
