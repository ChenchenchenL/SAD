"""
Malrule algorithm for Add-Under-Common-Root error.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class AddUnderCommonRootMalrule(Malrule):
    """
    Students combine separate radicals under one root: √a + √b = √(a+b).

    Example: √4 + √9
    Student: √(4+9) = √13 ≈ 3.6 (wrong!)
    Correct: 2 + 3 = 5
    """

    def _generate_concise_steps(self, problem: Problem, template: str, **kwargs) -> List[str]:
        """Generate concise steps with only formulas and values."""
        steps = []
        steps.append(f"Question: {problem.text}")

        if template in ['basic_addition', 'word_problem_addition']:
            square_a = kwargs['square_a']
            square_b = kwargs['square_b']
            sum_of_squares = kwargs['sum_of_squares']
            malrule_answer = kwargs['malrule_answer']
            steps.append(f"√{square_a} + √{square_b}")
            steps.append(f"√{square_a} + √{square_b} = √({square_a}+{square_b})")
            steps.append(f"√{sum_of_squares} = {malrule_answer}")
            steps.append(f"Answer: {malrule_answer}")

        elif template in ['basic_subtraction', 'word_problem_subtraction']:
            square_a = kwargs['square_a']
            square_b = kwargs['square_b']
            diff_of_squares = kwargs['diff_of_squares']
            malrule_answer = kwargs['malrule_answer']
            steps.append(f"√{square_a} - √{square_b}")
            steps.append(f"√{square_a} - √{square_b} = √({square_a}-{square_b})")
            steps.append(f"√{diff_of_squares} = {malrule_answer}")
            steps.append(f"Answer: {malrule_answer}")

        elif template in ['three_radicals', 'word_problem_three_radicals']:
            square_a = kwargs['square_a']
            square_b = kwargs['square_b']
            square_c = kwargs['square_c']
            sum_of_squares = kwargs['sum_of_squares']
            malrule_answer = kwargs['malrule_answer']
            steps.append(f"√{square_a} + √{square_b} + √{square_c}")
            steps.append(f"√{square_a} + √{square_b} + √{square_c} = √({square_a}+{square_b}+{square_c})")
            steps.append(f"√{sum_of_squares} = {malrule_answer}")
            steps.append(f"Answer: {malrule_answer}")

        elif template == 'word_problem_distance':
            square_a = kwargs['square_a']
            square_b = kwargs['square_b']
            sum_of_squares = kwargs['sum_of_squares']
            malrule_answer = kwargs['malrule_answer']
            steps.append(f"Total = √({square_a}+{square_b})")
            steps.append(f"√{sum_of_squares} = {malrule_answer}")
            steps.append(f"Answer: {malrule_answer}")

        elif template in ['mixed_operations', 'word_problem_mixed']:
            square_a = kwargs['square_a']
            square_b = kwargs['square_b']
            square_c = kwargs['square_c']
            mixed_squares = kwargs['mixed_squares']
            malrule_answer = kwargs['malrule_answer']
            steps.append(f"√{square_a} + √{square_b} - √{square_c}")
            steps.append(f"√{square_a} + √{square_b} - √{square_c} = √({square_a}+{square_b}-{square_c})")
            steps.append(f"√{abs(mixed_squares)} = {malrule_answer}")
            steps.append(f"Answer: {malrule_answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, template: str, **kwargs) -> List[str]:
        """Generate verbose steps with full explanations (original format)."""
        steps = []

        if template in ['basic_addition', 'word_problem_addition']:
            square_a = kwargs['square_a']
            square_b = kwargs['square_b']
            base_a = kwargs['base_a']
            base_b = kwargs['base_b']
            sum_of_squares = kwargs['sum_of_squares']
            malrule_answer = kwargs['malrule_answer']
            correct_answer = kwargs['correct_answer']

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("MALRULE: Combine radicals under common root")
            steps.append(f"  MALRULE REASONING: '√a + √b = √(a+b)'")
            steps.append(f"                     'Combine under one radical'")
            steps.append("")
            steps.append(f"Step 1: Add numbers under the radical (INCORRECT!)")
            steps.append(f"  √{square_a} + √{square_b} = √({square_a}+{square_b})")
            steps.append("")
            steps.append(f"Step 2: Simplify")
            steps.append(f"  = √{sum_of_squares}")
            steps.append(f"  ≈ {malrule_answer}")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT - can't combine like this!)")
            steps.append(f"  Should simplify each first: √{square_a} = {base_a}, √{square_b} = {base_b}")
            steps.append(f"  Then add: {base_a} + {base_b} = {correct_answer}")

        elif template in ['basic_subtraction', 'word_problem_subtraction']:
            square_a = kwargs['square_a']
            square_b = kwargs['square_b']
            base_a = kwargs['base_a']
            base_b = kwargs['base_b']
            diff_of_squares = kwargs['diff_of_squares']
            malrule_answer = kwargs['malrule_answer']
            correct_answer = kwargs['correct_answer']

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("MALRULE: Combine radicals under common root")
            steps.append(f"  MALRULE REASONING: '√a - √b = √(a-b)'")
            steps.append(f"                     'Combine under one radical'")
            steps.append("")
            steps.append(f"Step 1: Subtract numbers under the radical (INCORRECT!)")
            steps.append(f"  √{square_a} - √{square_b} = √({square_a}-{square_b})")
            steps.append("")
            steps.append(f"Step 2: Simplify")
            steps.append(f"  = √{diff_of_squares}")
            steps.append(f"  ≈ {malrule_answer}")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT - can't combine like this!)")
            steps.append(f"  Should simplify each first: √{square_a} = {base_a}, √{square_b} = {base_b}")
            steps.append(f"  Then subtract: {base_a} - {base_b} = {correct_answer}")

        elif template in ['three_radicals', 'word_problem_three_radicals']:
            square_a = kwargs['square_a']
            square_b = kwargs['square_b']
            square_c = kwargs['square_c']
            base_a = kwargs['base_a']
            base_b = kwargs['base_b']
            base_c = kwargs['base_c']
            sum_of_squares = kwargs['sum_of_squares']
            malrule_answer = kwargs['malrule_answer']
            correct_answer = kwargs['correct_answer']

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("MALRULE: Combine all radicals under common root")
            steps.append(f"  MALRULE REASONING: '√a + √b + √c = √(a+b+c)'")
            steps.append(f"                     'Combine all under one radical'")
            steps.append("")
            steps.append(f"Step 1: Add all numbers under the radical (INCORRECT!)")
            steps.append(f"  √{square_a} + √{square_b} + √{square_c} = √({square_a}+{square_b}+{square_c})")
            steps.append("")
            steps.append(f"Step 2: Simplify")
            steps.append(f"  = √{sum_of_squares}")
            steps.append(f"  ≈ {malrule_answer}")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT!)")
            steps.append(f"  Should simplify each first: √{square_a} = {base_a}, √{square_b} = {base_b}, √{square_c} = {base_c}")
            steps.append(f"  Then add: {base_a} + {base_b} + {base_c} = {correct_answer}")

        elif template == 'word_problem_distance':
            square_a = kwargs['square_a']
            square_b = kwargs['square_b']
            base_a = kwargs['base_a']
            base_b = kwargs['base_b']
            sum_of_squares = kwargs['sum_of_squares']
            malrule_answer = kwargs['malrule_answer']
            correct_answer = kwargs['correct_answer']

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("MALRULE: Combine radicals under common root")
            steps.append(f"  MALRULE REASONING: 'Total distance = √(distance₁ + distance₂)'")
            steps.append(f"                     'Combine under one radical'")
            steps.append("")
            steps.append(f"Step 1: Add distances under the radical (INCORRECT!)")
            steps.append(f"  Total = √({square_a}+{square_b})")
            steps.append("")
            steps.append(f"Step 2: Simplify")
            steps.append(f"  = √{sum_of_squares}")
            steps.append(f"  ≈ {malrule_answer}")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT!)")
            steps.append(f"  Should simplify each first: √{square_a} = {base_a}, √{square_b} = {base_b}")
            steps.append(f"  Then add: {base_a} + {base_b} = {correct_answer}")

        elif template in ['mixed_operations', 'word_problem_mixed']:
            square_a = kwargs['square_a']
            square_b = kwargs['square_b']
            square_c = kwargs['square_c']
            base_a = kwargs['base_a']
            base_b = kwargs['base_b']
            base_c = kwargs['base_c']
            mixed_squares = kwargs['mixed_squares']
            malrule_answer = kwargs['malrule_answer']
            correct_answer = kwargs['correct_answer']

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("MALRULE: Combine all radicals under common root")
            steps.append(f"  MALRULE REASONING: '√a + √b - √c = √(a+b-c)'")
            steps.append(f"                     'Combine all operations under one radical'")
            steps.append("")
            steps.append(f"Step 1: Apply operations under the radical (INCORRECT!)")
            steps.append(f"  √{square_a} + √{square_b} - √{square_c} = √({square_a}+{square_b}-{square_c})")
            steps.append("")
            steps.append(f"Step 2: Simplify")
            steps.append(f"  = √{abs(mixed_squares)}")
            steps.append(f"  ≈ {malrule_answer}")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT!)")
            steps.append(f"  Should simplify each first: √{square_a} = {base_a}, √{square_b} = {base_b}, √{square_c} = {base_c}")
            steps.append(f"  Then calculate: {base_a} + {base_b} - {base_c} = {correct_answer}")

        return steps

    def get_name(self) -> str:
        return "Add-Under-Common-Root"

    def get_description(self) -> str:
        return (
            "Students incorrectly combine separate radicals under a single root, "
            "believing √a + √b = √(a+b). This is a manifestation of the 'illusion "
            "of linearity' - the overgeneralization of the distributive property "
            "to non-linear operations. Research shows this error results from "
            "'students' overgeneralisation of the distributive law' (Matz, 1982; "
            "De Bock et al., 2007)."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        template = problem.metadata.get('template', 'basic_addition')

        # Extract squares from metadata
        square_a = problem.metadata.get('square_a')
        square_b = problem.metadata.get('square_b')

        # Handle different operations based on template
        if 'subtraction' in template:
            combined = square_a - square_b
        elif 'mixed' in template:
            square_c = problem.metadata.get('square_c')
            combined = square_a + square_b - square_c
        elif 'three' in template:
            square_c = problem.metadata.get('square_c')
            combined = square_a + square_b + square_c
        else:  # addition
            combined = square_a + square_b

        # Compute the malrule answer
        malrule_value = round(abs(combined) ** 0.5, 2)

        # Check if this has units
        correct_ans = problem.metadata.get('correct_answer', '')
        if isinstance(correct_ans, str) and ' ' in correct_ans:
            unit = correct_ans.split(' ', 1)[1]
            return f"{malrule_value} {unit}"

        return str(malrule_value)

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply the malrule based on the template."""
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

        # COMPUTE the malrule answer algorithmically
        sum_of_squares = square_a + square_b
        malrule_value = round(sum_of_squares ** 0.5, 2)

        # COMPUTE the correct answer for comparison
        base_a = int(square_a ** 0.5)
        base_b = int(square_b ** 0.5)
        correct_value = base_a + base_b

        # Check if this has units
        template = problem.metadata.get('template', 'basic_addition')
        if 'word_problem' in template:
            meta_answer = problem.metadata.get('correct_answer', '')
            if isinstance(meta_answer, str) and ' ' in meta_answer:
                unit = meta_answer.split(' ', 1)[1]
                malrule_answer = f"{malrule_value} {unit}"
                correct_answer = f"{correct_value} {unit}"
            else:
                malrule_answer = str(malrule_value)
                correct_answer = str(correct_value)
        else:
            malrule_answer = str(malrule_value)
            correct_answer = str(correct_value)

        # Generate steps based on verbose flag
        step_kwargs = {
            'square_a': square_a,
            'square_b': square_b,
            'base_a': base_a,
            'base_b': base_b,
            'sum_of_squares': sum_of_squares,
            'malrule_answer': malrule_answer,
            'correct_answer': correct_answer
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, template, **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, template, **step_kwargs)

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _apply_basic_subtraction(self, problem: Problem, verbose: bool = False) -> Solution:
        """Basic subtraction template: √a² - √b²"""
        square_a = problem.metadata['square_a']
        square_b = problem.metadata['square_b']

        # COMPUTE the malrule answer algorithmically
        diff_of_squares = square_a - square_b
        malrule_value = round(diff_of_squares ** 0.5, 2)

        # COMPUTE the correct answer for comparison
        base_a = int(square_a ** 0.5)
        base_b = int(square_b ** 0.5)
        correct_value = base_a - base_b

        # Check if this has units
        template = problem.metadata.get('template', 'basic_subtraction')
        if 'word_problem' in template:
            meta_answer = problem.metadata.get('correct_answer', '')
            if isinstance(meta_answer, str) and ' ' in meta_answer:
                unit = meta_answer.split(' ', 1)[1]
                malrule_answer = f"{malrule_value} {unit}"
                correct_answer = f"{correct_value} {unit}"
            else:
                malrule_answer = str(malrule_value)
                correct_answer = str(correct_value)
        else:
            malrule_answer = str(malrule_value)
            correct_answer = str(correct_value)

        # Generate steps based on verbose flag
        step_kwargs = {
            'square_a': square_a,
            'square_b': square_b,
            'base_a': base_a,
            'base_b': base_b,
            'diff_of_squares': diff_of_squares,
            'malrule_answer': malrule_answer,
            'correct_answer': correct_answer
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, template, **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, template, **step_kwargs)

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _apply_three_radicals(self, problem: Problem, verbose: bool = False) -> Solution:
        """Three radicals template: √a² + √b² + √c²"""
        square_a = problem.metadata['square_a']
        square_b = problem.metadata['square_b']
        square_c = problem.metadata['square_c']

        # COMPUTE the malrule answer algorithmically
        sum_of_squares = square_a + square_b + square_c
        malrule_value = round(sum_of_squares ** 0.5, 2)

        # COMPUTE the correct answer for comparison
        base_a = int(square_a ** 0.5)
        base_b = int(square_b ** 0.5)
        base_c = int(square_c ** 0.5)
        correct_value = base_a + base_b + base_c

        # Check if this has units
        template = problem.metadata.get('template', 'three_radicals')
        if 'word_problem' in template:
            meta_answer = problem.metadata.get('correct_answer', '')
            if isinstance(meta_answer, str) and ' ' in meta_answer:
                unit = meta_answer.split(' ', 1)[1]
                malrule_answer = f"{malrule_value} {unit}"
                correct_answer = f"{correct_value} {unit}"
            else:
                malrule_answer = str(malrule_value)
                correct_answer = str(correct_value)
        else:
            malrule_answer = str(malrule_value)
            correct_answer = str(correct_value)

        # Generate steps based on verbose flag
        step_kwargs = {
            'square_a': square_a,
            'square_b': square_b,
            'square_c': square_c,
            'base_a': base_a,
            'base_b': base_b,
            'base_c': base_c,
            'sum_of_squares': sum_of_squares,
            'malrule_answer': malrule_answer,
            'correct_answer': correct_answer
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, template, **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, template, **step_kwargs)

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _apply_word_problem_distance(self, problem: Problem, verbose: bool = False) -> Solution:
        """Word problem distance template"""
        square_a = problem.metadata['square_a']
        square_b = problem.metadata['square_b']

        # COMPUTE the malrule answer algorithmically
        sum_of_squares = square_a + square_b
        malrule_value = round(sum_of_squares ** 0.5, 2)

        # COMPUTE the correct answer for comparison
        base_a = int(square_a ** 0.5)
        base_b = int(square_b ** 0.5)

        # Extract unit
        meta_answer = problem.metadata.get('correct_answer', '')
        if isinstance(meta_answer, str) and ' ' in meta_answer:
            unit = meta_answer.split(' ', 1)[1]
            malrule_answer = f"{malrule_value} {unit}"
            correct_answer = f"{base_a + base_b} {unit}"
        else:
            malrule_answer = str(malrule_value)
            correct_answer = str(base_a + base_b)

        template = 'word_problem_distance'

        # Generate steps based on verbose flag
        step_kwargs = {
            'square_a': square_a,
            'square_b': square_b,
            'base_a': base_a,
            'base_b': base_b,
            'sum_of_squares': sum_of_squares,
            'malrule_answer': malrule_answer,
            'correct_answer': correct_answer
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, template, **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, template, **step_kwargs)

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _apply_mixed_operations(self, problem: Problem, verbose: bool = False) -> Solution:
        """Mixed operations template: √a² + √b² - √c²"""
        square_a = problem.metadata['square_a']
        square_b = problem.metadata['square_b']
        square_c = problem.metadata['square_c']

        # COMPUTE the malrule answer algorithmically
        mixed_squares = square_a + square_b - square_c
        malrule_value = round(abs(mixed_squares) ** 0.5, 2)

        # COMPUTE the correct answer for comparison
        base_a = int(square_a ** 0.5)
        base_b = int(square_b ** 0.5)
        base_c = int(square_c ** 0.5)
        correct_value = base_a + base_b - base_c

        # Check if this has units
        template = problem.metadata.get('template', 'mixed_operations')
        if 'word_problem' in template:
            meta_answer = problem.metadata.get('correct_answer', '')
            if isinstance(meta_answer, str) and ' ' in meta_answer:
                unit = meta_answer.split(' ', 1)[1]
                malrule_answer = f"{malrule_value} {unit}"
                correct_answer = f"{correct_value} {unit}"
            else:
                malrule_answer = str(malrule_value)
                correct_answer = str(correct_value)
        else:
            malrule_answer = str(malrule_value)
            correct_answer = str(correct_value)

        # Generate steps based on verbose flag
        step_kwargs = {
            'square_a': square_a,
            'square_b': square_b,
            'square_c': square_c,
            'base_a': base_a,
            'base_b': base_b,
            'base_c': base_c,
            'mixed_squares': mixed_squares,
            'malrule_answer': malrule_answer,
            'correct_answer': correct_answer
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, template, **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, template, **step_kwargs)

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
