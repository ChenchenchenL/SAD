"""
Correct algorithm for radical addition.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class RadicalAdditionCorrectAlgorithm(CorrectAlgorithm):
    """Correctly adds radicals by simplifying each first."""

    def get_name(self) -> str:
        return "Correct Radical Addition"

    def get_description(self) -> str:
        return "Correctly adds radicals by simplifying each separately first."

    def _generate_concise_steps(self, problem: Problem, template: str, **kwargs) -> List[str]:
        """Generate concise steps with only formulas and values."""
        steps = []
        steps.append(f"Question: {problem.text}")

        if template in ['basic_addition', 'word_problem_addition']:
            square_a = kwargs['square_a']
            square_b = kwargs['square_b']
            base_a = kwargs['base_a']
            base_b = kwargs['base_b']
            correct_answer = kwargs['correct_answer']
            steps.append(f"√{square_a} + √{square_b}")
            steps.append(f"√{square_a} = {base_a}")
            steps.append(f"√{square_b} = {base_b}")
            steps.append(f"{base_a} + {base_b} = {correct_answer}")
            steps.append(f"Answer: {correct_answer}")

        elif template in ['basic_subtraction', 'word_problem_subtraction']:
            square_a = kwargs['square_a']
            square_b = kwargs['square_b']
            base_a = kwargs['base_a']
            base_b = kwargs['base_b']
            correct_answer = kwargs['correct_answer']
            steps.append(f"√{square_a} - √{square_b}")
            steps.append(f"√{square_a} = {base_a}")
            steps.append(f"√{square_b} = {base_b}")
            steps.append(f"{base_a} - {base_b} = {correct_answer}")
            steps.append(f"Answer: {correct_answer}")

        elif template in ['three_radicals', 'word_problem_three_radicals']:
            square_a = kwargs['square_a']
            square_b = kwargs['square_b']
            square_c = kwargs['square_c']
            base_a = kwargs['base_a']
            base_b = kwargs['base_b']
            base_c = kwargs['base_c']
            correct_answer = kwargs['correct_answer']
            steps.append(f"√{square_a} + √{square_b} + √{square_c}")
            steps.append(f"√{square_a} = {base_a}")
            steps.append(f"√{square_b} = {base_b}")
            steps.append(f"√{square_c} = {base_c}")
            steps.append(f"{base_a} + {base_b} + {base_c} = {correct_answer}")
            steps.append(f"Answer: {correct_answer}")

        elif template == 'word_problem_distance':
            square_a = kwargs['square_a']
            square_b = kwargs['square_b']
            base_a = kwargs['base_a']
            base_b = kwargs['base_b']
            correct_answer = kwargs['correct_answer']
            steps.append(f"Total distance = √{square_a} + √{square_b}")
            steps.append(f"√{square_a} = {base_a} meters")
            steps.append(f"√{square_b} = {base_b} meters")
            steps.append(f"{base_a} + {base_b} = {correct_answer}")
            steps.append(f"Answer: {correct_answer}")

        elif template in ['mixed_operations', 'word_problem_mixed']:
            square_a = kwargs['square_a']
            square_b = kwargs['square_b']
            square_c = kwargs['square_c']
            base_a = kwargs['base_a']
            base_b = kwargs['base_b']
            base_c = kwargs['base_c']
            correct_answer = kwargs['correct_answer']
            steps.append(f"√{square_a} + √{square_b} - √{square_c}")
            steps.append(f"√{square_a} = {base_a}")
            steps.append(f"√{square_b} = {base_b}")
            steps.append(f"√{square_c} = {base_c}")
            steps.append(f"{base_a} + {base_b} - {base_c} = {correct_answer}")
            steps.append(f"Answer: {correct_answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, template: str, **kwargs) -> List[str]:
        """Generate verbose steps with full explanations (original format)."""
        steps = []

        if template in ['basic_addition', 'word_problem_addition']:
            square_a = kwargs['square_a']
            square_b = kwargs['square_b']
            base_a = kwargs['base_a']
            base_b = kwargs['base_b']
            correct_answer = kwargs['correct_answer']
            sum_of_squares = kwargs['sum_of_squares']
            malrule_value = kwargs['malrule_value']

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("CORRECT METHOD: Simplify each radical FIRST, then add")
            steps.append("  Can't combine √a + √b = √(a+b) - this is WRONG!")
            steps.append("")
            steps.append(f"Step 1: Simplify first radical")
            steps.append(f"  √{square_a} = {base_a}")
            steps.append("")
            steps.append(f"Step 2: Simplify second radical")
            steps.append(f"  √{square_b} = {base_b}")
            steps.append("")
            steps.append(f"Step 3: Add the simplified values")
            steps.append(f"  {base_a} + {base_b} = {correct_answer}")
            steps.append("")
            steps.append(f"Final Answer: {correct_answer} ✓")
            steps.append("")
            steps.append(f"If we incorrectly combined: √({square_a}+{square_b}) = √{sum_of_squares} ≈ {malrule_value}")
            steps.append(f"  This is WRONG! {correct_answer} ≠ {malrule_value}")
            steps.append("")
            steps.append("Remember: √a + √b ≠ √(a+b)")

        elif template in ['basic_subtraction', 'word_problem_subtraction']:
            square_a = kwargs['square_a']
            square_b = kwargs['square_b']
            base_a = kwargs['base_a']
            base_b = kwargs['base_b']
            correct_answer = kwargs['correct_answer']
            diff_of_squares = kwargs['diff_of_squares']
            malrule_value = kwargs['malrule_value']

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("CORRECT METHOD: Simplify each radical FIRST, then subtract")
            steps.append("  Can't combine √a - √b = √(a-b) - this is WRONG!")
            steps.append("")
            steps.append(f"Step 1: Simplify first radical")
            steps.append(f"  √{square_a} = {base_a}")
            steps.append("")
            steps.append(f"Step 2: Simplify second radical")
            steps.append(f"  √{square_b} = {base_b}")
            steps.append("")
            steps.append(f"Step 3: Subtract the simplified values")
            steps.append(f"  {base_a} - {base_b} = {correct_answer}")
            steps.append("")
            steps.append(f"Final Answer: {correct_answer} ✓")
            steps.append("")
            steps.append(f"If we incorrectly combined: √({square_a}-{square_b}) = √{diff_of_squares} ≈ {malrule_value}")
            steps.append(f"  This is WRONG! {correct_answer} ≠ {malrule_value}")
            steps.append("")
            steps.append("Remember: √a - √b ≠ √(a-b)")

        elif template in ['three_radicals', 'word_problem_three_radicals']:
            square_a = kwargs['square_a']
            square_b = kwargs['square_b']
            square_c = kwargs['square_c']
            base_a = kwargs['base_a']
            base_b = kwargs['base_b']
            base_c = kwargs['base_c']
            correct_answer = kwargs['correct_answer']
            sum_of_squares = kwargs['sum_of_squares']
            malrule_value = kwargs['malrule_value']

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("CORRECT METHOD: Simplify each radical FIRST, then add")
            steps.append("  Can't combine √a + √b + √c = √(a+b+c) - this is WRONG!")
            steps.append("")
            steps.append(f"Step 1: Simplify first radical")
            steps.append(f"  √{square_a} = {base_a}")
            steps.append("")
            steps.append(f"Step 2: Simplify second radical")
            steps.append(f"  √{square_b} = {base_b}")
            steps.append("")
            steps.append(f"Step 3: Simplify third radical")
            steps.append(f"  √{square_c} = {base_c}")
            steps.append("")
            steps.append(f"Step 4: Add the simplified values")
            steps.append(f"  {base_a} + {base_b} + {base_c} = {correct_answer}")
            steps.append("")
            steps.append(f"Final Answer: {correct_answer} ✓")
            steps.append("")
            steps.append(f"If we incorrectly combined: √({square_a}+{square_b}+{square_c}) ≈ {malrule_value}")
            steps.append(f"  This is WRONG! {correct_answer} ≠ {malrule_value}")

        elif template == 'word_problem_distance':
            square_a = kwargs['square_a']
            square_b = kwargs['square_b']
            base_a = kwargs['base_a']
            base_b = kwargs['base_b']
            correct_answer = kwargs['correct_answer']
            sum_of_squares = kwargs['sum_of_squares']
            malrule_value = kwargs['malrule_value']

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("CORRECT METHOD: Simplify each distance FIRST, then add")
            steps.append("  Can't combine distances under one radical!")
            steps.append("")
            steps.append(f"Step 1: Simplify first distance")
            steps.append(f"  √{square_a} meters = {base_a} meters")
            steps.append("")
            steps.append(f"Step 2: Simplify second distance")
            steps.append(f"  √{square_b} meters = {base_b} meters")
            steps.append("")
            steps.append(f"Step 3: Add the simplified distances")
            steps.append(f"  {base_a} + {base_b} = {correct_answer}")
            steps.append("")
            steps.append(f"Final Answer: {correct_answer} ✓")
            steps.append("")
            steps.append(f"If we incorrectly combined: √({square_a}+{square_b}) ≈ {malrule_value}")
            steps.append(f"  This is WRONG! Walking {base_a}m then {base_b}m is {correct_answer}, not {malrule_value}!")

        elif template in ['mixed_operations', 'word_problem_mixed']:
            square_a = kwargs['square_a']
            square_b = kwargs['square_b']
            square_c = kwargs['square_c']
            base_a = kwargs['base_a']
            base_b = kwargs['base_b']
            base_c = kwargs['base_c']
            correct_answer = kwargs['correct_answer']
            mixed_squares = kwargs['mixed_squares']
            malrule_value = kwargs['malrule_value']

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("CORRECT METHOD: Simplify each radical FIRST, then perform operations")
            steps.append("  Can't combine √a + √b - √c = √(a+b-c) - this is WRONG!")
            steps.append("")
            steps.append(f"Step 1: Simplify first radical")
            steps.append(f"  √{square_a} = {base_a}")
            steps.append("")
            steps.append(f"Step 2: Simplify second radical")
            steps.append(f"  √{square_b} = {base_b}")
            steps.append("")
            steps.append(f"Step 3: Simplify third radical")
            steps.append(f"  √{square_c} = {base_c}")
            steps.append("")
            steps.append(f"Step 4: Perform the operations")
            steps.append(f"  {base_a} + {base_b} - {base_c} = {correct_answer}")
            steps.append("")
            steps.append(f"Final Answer: {correct_answer} ✓")
            steps.append("")
            steps.append(f"If we incorrectly combined: √({square_a}+{square_b}-{square_c}) ≈ {malrule_value}")
            steps.append(f"  This is WRONG! {correct_answer} ≠ {malrule_value}")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply the correct algorithm based on the template."""
        template = problem.metadata.get('template', 'basic_addition')

        if template == 'basic_addition' or template == 'word_problem_addition':
            return self._apply_basic_addition(problem, verbose)
        elif template == 'basic_subtraction' or template == 'word_problem_subtraction':
            return self._apply_basic_subtraction(problem, verbose)
        elif template == 'three_radicals' or template == 'word_problem_three_radicals':
            return self._apply_three_radicals(problem, verbose)
        elif template == 'word_problem_distance':
            return self._apply_word_problem_distance(problem, verbose)
        elif template == 'mixed_operations' or template == 'word_problem_mixed':
            return self._apply_mixed_operations(problem, verbose)
        else:
            # Default to basic_addition for backwards compatibility
            return self._apply_basic_addition(problem, verbose)

    def _apply_basic_addition(self, problem: Problem, verbose: bool = False) -> Solution:
        """Basic addition template: √a² + √b²"""
        square_a = problem.metadata['square_a']
        square_b = problem.metadata['square_b']

        # COMPUTE the answer algorithmically (don't use metadata['correct_answer'])
        base_a = int(square_a ** 0.5)
        base_b = int(square_b ** 0.5)

        # Check if this is a word problem to preserve units
        template = problem.metadata.get('template', 'basic_addition')
        if 'word_problem' in template:
            # Extract unit from metadata answer if available
            meta_answer = problem.metadata.get('correct_answer', '')
            if isinstance(meta_answer, str) and ' ' in meta_answer:
                unit = meta_answer.split(' ', 1)[1]
                correct_answer = f"{base_a + base_b} {unit}"
            else:
                correct_answer = str(base_a + base_b)
        else:
            correct_answer = str(base_a + base_b)

        # For comparison in steps, compute what the malrule would give
        sum_of_squares = square_a + square_b
        malrule_value = round(sum_of_squares ** 0.5, 2)

        # Generate steps based on verbose flag
        step_kwargs = {
            'square_a': square_a,
            'square_b': square_b,
            'base_a': base_a,
            'base_b': base_b,
            'correct_answer': correct_answer,
            'sum_of_squares': sum_of_squares,
            'malrule_value': malrule_value
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, template, **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, template, **step_kwargs)

        return Solution(
            answer=str(correct_answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _apply_basic_subtraction(self, problem: Problem, verbose: bool = False) -> Solution:
        """Basic subtraction template: √a² - √b²"""
        square_a = problem.metadata['square_a']
        square_b = problem.metadata['square_b']

        # COMPUTE the answer algorithmically
        base_a = int(square_a ** 0.5)
        base_b = int(square_b ** 0.5)

        # Check if this is a word problem to preserve units
        template = problem.metadata.get('template', 'basic_subtraction')
        if 'word_problem' in template:
            # Extract unit from metadata answer if available
            meta_answer = problem.metadata.get('correct_answer', '')
            if isinstance(meta_answer, str) and ' ' in meta_answer:
                unit = meta_answer.split(' ', 1)[1]
                correct_answer = f"{base_a - base_b} {unit}"
            else:
                correct_answer = str(base_a - base_b)
        else:
            correct_answer = str(base_a - base_b)

        # For comparison
        diff_of_squares = square_a - square_b
        malrule_value = round(diff_of_squares ** 0.5, 2)

        # Generate steps based on verbose flag
        step_kwargs = {
            'square_a': square_a,
            'square_b': square_b,
            'base_a': base_a,
            'base_b': base_b,
            'correct_answer': correct_answer,
            'diff_of_squares': diff_of_squares,
            'malrule_value': malrule_value
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, template, **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, template, **step_kwargs)

        return Solution(
            answer=str(correct_answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _apply_three_radicals(self, problem: Problem, verbose: bool = False) -> Solution:
        """Three radicals template: √a² + √b² + √c²"""
        square_a = problem.metadata['square_a']
        square_b = problem.metadata['square_b']
        square_c = problem.metadata['square_c']

        # COMPUTE the answer algorithmically
        base_a = int(square_a ** 0.5)
        base_b = int(square_b ** 0.5)
        base_c = int(square_c ** 0.5)

        # Check if this is a word problem to preserve units
        template = problem.metadata.get('template', 'three_radicals')
        if 'word_problem' in template:
            # Extract unit from metadata answer if available
            meta_answer = problem.metadata.get('correct_answer', '')
            if isinstance(meta_answer, str) and ' ' in meta_answer:
                unit = meta_answer.split(' ', 1)[1]
                correct_answer = f"{base_a + base_b + base_c} {unit}"
            else:
                correct_answer = str(base_a + base_b + base_c)
        else:
            correct_answer = str(base_a + base_b + base_c)

        # For comparison
        sum_of_squares = square_a + square_b + square_c
        malrule_value = round(sum_of_squares ** 0.5, 2)

        # Generate steps based on verbose flag
        step_kwargs = {
            'square_a': square_a,
            'square_b': square_b,
            'square_c': square_c,
            'base_a': base_a,
            'base_b': base_b,
            'base_c': base_c,
            'correct_answer': correct_answer,
            'sum_of_squares': sum_of_squares,
            'malrule_value': malrule_value
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, template, **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, template, **step_kwargs)

        return Solution(
            answer=str(correct_answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _apply_word_problem_distance(self, problem: Problem, verbose: bool = False) -> Solution:
        """Word problem distance template"""
        square_a = problem.metadata['square_a']
        square_b = problem.metadata['square_b']

        # COMPUTE the answer algorithmically
        base_a = int(square_a ** 0.5)
        base_b = int(square_b ** 0.5)

        # Extract unit from metadata answer if available
        meta_answer = problem.metadata.get('correct_answer', '')
        if isinstance(meta_answer, str) and ' ' in meta_answer:
            unit = meta_answer.split(' ', 1)[1]
            correct_answer = f"{base_a + base_b} {unit}"
        else:
            correct_answer = str(base_a + base_b)

        # For comparison
        sum_of_squares = square_a + square_b
        malrule_value = round(sum_of_squares ** 0.5, 2)

        template = 'word_problem_distance'

        # Generate steps based on verbose flag
        step_kwargs = {
            'square_a': square_a,
            'square_b': square_b,
            'base_a': base_a,
            'base_b': base_b,
            'correct_answer': correct_answer,
            'sum_of_squares': sum_of_squares,
            'malrule_value': malrule_value
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, template, **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, template, **step_kwargs)

        return Solution(
            answer=str(correct_answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _apply_mixed_operations(self, problem: Problem, verbose: bool = False) -> Solution:
        """Mixed operations template: √a² + √b² - √c²"""
        square_a = problem.metadata['square_a']
        square_b = problem.metadata['square_b']
        square_c = problem.metadata['square_c']

        # COMPUTE the answer algorithmically
        base_a = int(square_a ** 0.5)
        base_b = int(square_b ** 0.5)
        base_c = int(square_c ** 0.5)

        # Check if this is a word problem to preserve units
        template = problem.metadata.get('template', 'mixed_operations')
        if 'word_problem' in template:
            # Extract unit from metadata answer if available
            meta_answer = problem.metadata.get('correct_answer', '')
            if isinstance(meta_answer, str) and ' ' in meta_answer:
                unit = meta_answer.split(' ', 1)[1]
                correct_answer = f"{base_a + base_b - base_c} {unit}"
            else:
                correct_answer = str(base_a + base_b - base_c)
        else:
            correct_answer = str(base_a + base_b - base_c)

        # For comparison
        mixed_squares = square_a + square_b - square_c
        malrule_value = round(abs(mixed_squares) ** 0.5, 2)

        # Generate steps based on verbose flag
        step_kwargs = {
            'square_a': square_a,
            'square_b': square_b,
            'square_c': square_c,
            'base_a': base_a,
            'base_b': base_b,
            'base_c': base_c,
            'correct_answer': correct_answer,
            'mixed_squares': mixed_squares,
            'malrule_value': malrule_value
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, template, **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, template, **step_kwargs)

        return Solution(
            answer=str(correct_answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
