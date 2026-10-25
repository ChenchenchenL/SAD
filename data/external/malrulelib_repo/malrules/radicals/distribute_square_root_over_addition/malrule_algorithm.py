"""
Malrule algorithm for Distribute-Square-Root-Over-Addition error.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class DistributeSquareRootOverAdditionMalrule(Malrule):
    """
    Students distribute square root over addition: √(a²+b²) = a + b.

    Example: √(3²+4²) → Student: 3 + 4 = 7 (wrong!)
    Correct: √(9+16) = √25 = 5
    """

    def _generate_concise_steps(self, problem: Problem, problem_type: str, **kwargs) -> List[str]:
        """Generate concise steps with only formulas and values."""
        steps = []
        steps.append(f"Question: {problem.text}")

        if problem_type == 'basic_sum_of_squares':
            a = kwargs['a']
            b = kwargs['b']
            a_squared = kwargs['a_squared']
            b_squared = kwargs['b_squared']
            malrule_answer = kwargs['malrule_answer']
            steps.append(f"√({a}² + {b}²)")
            steps.append(f"√({a}²) + √({b}²) = {a} + {b}")
            steps.append(f"{a} + {b} = {malrule_answer}")
            steps.append(f"Answer: {malrule_answer}")

        elif problem_type == 'pythagorean_context':
            a = kwargs['a']
            b = kwargs['b']
            malrule_answer = kwargs['malrule_answer']
            steps.append(f"√({a}² + {b}²)")
            steps.append(f"√({a}²) + √({b}²) = {a} + {b}")
            steps.append(f"Answer: {malrule_answer}")

        elif problem_type in ['algebraic_expression', 'algebraic_word_problem']:
            const = kwargs['const']
            const_root = kwargs['const_root']
            x_val = kwargs['x_val']
            malrule_answer = kwargs['malrule_answer']
            steps.append(f"√(x² + {const})")
            steps.append(f"√(x²) + √{const} = x + {const_root}")
            if problem_type == 'algebraic_word_problem':
                steps.append(f"For x = {x_val}: {x_val} + {const_root} = {malrule_answer}")
            steps.append(f"Answer: {malrule_answer}")

        elif problem_type in ['subtraction_variant', 'subtraction_word_problem']:
            a = kwargs['a']
            b = kwargs['b']
            malrule_answer = kwargs['malrule_answer']
            steps.append(f"√({a}² - {b}²)")
            steps.append(f"√({a}²) - √({b}²) = {a} - {b}")
            steps.append(f"Answer: {malrule_answer}")

        elif problem_type == 'non_perfect_square':
            a = kwargs['a']
            b = kwargs['b']
            malrule_answer = kwargs['malrule_answer']
            steps.append(f"√({a}² + {b}²)")
            steps.append(f"√({a}²) + √({b}²) = {a} + {b}")
            steps.append(f"Answer: {malrule_answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, problem_type: str, **kwargs) -> List[str]:
        """Generate verbose steps with full explanations (original format)."""
        steps = []

        if problem_type == 'basic_sum_of_squares':
            a = kwargs['a']
            b = kwargs['b']
            a_squared = kwargs['a_squared']
            b_squared = kwargs['b_squared']
            sum_of_squares = kwargs['sum_of_squares']
            malrule_answer = kwargs['malrule_answer']
            correct_answer = kwargs['correct_answer']

            steps.append(f"Problem: Simplify √({a}² + {b}²)")
            steps.append("")
            steps.append("MALRULE: Square root distributes over addition")
            steps.append(f"  MALRULE REASONING: '√ applies to each term separately'")
            steps.append(f"                     '√(a² + b²) = √(a²) + √(b²)'")
            steps.append("")
            steps.append(f"Step 1: Take square root of first term")
            steps.append(f"  √({a}²) = {a}")
            steps.append("")
            steps.append(f"Step 2: Take square root of second term")
            steps.append(f"  √({b}²) = {b}")
            steps.append("")
            steps.append(f"Step 3: Add the results (INCORRECT!)")
            steps.append(f"  √({a}² + {b}²) = {a} + {b} = {malrule_answer}")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT - √ doesn't distribute!)")
            steps.append(f"  Should compute: {a}² + {b}² = {a_squared} + {b_squared} = {sum_of_squares}")
            steps.append(f"  Then: √{sum_of_squares} = {correct_answer:.2f}")

        elif problem_type == 'pythagorean_context':
            a = kwargs['a']
            b = kwargs['b']
            sum_of_squares = kwargs['sum_of_squares']
            malrule_answer = kwargs['malrule_answer']
            correct_answer = kwargs['correct_answer']

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("MALRULE: Square root distributes over addition")
            steps.append(f"  MALRULE REASONING: '√ applies to each term separately'")
            steps.append(f"                     'So √({a}² + {b}²) = {a} + {b}'")
            steps.append("")
            steps.append(f"Step 1: Take square root of {a}²")
            steps.append(f"  √({a}²) = {a}")
            steps.append("")
            steps.append(f"Step 2: Take square root of {b}²")
            steps.append(f"  √({b}²) = {b}")
            steps.append("")
            steps.append(f"Step 3: Add the results (INCORRECT!)")
            steps.append(f"  √({a}² + {b}²) = {a} + {b} = {malrule_answer}")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT!)")
            steps.append(f"  Should compute sum first: {a}² + {b}² = {sum_of_squares}")
            steps.append(f"  Then: √{sum_of_squares} = {correct_answer:.2f}")

        elif problem_type in ['algebraic_expression', 'algebraic_word_problem']:
            const = kwargs['const']
            const_root = kwargs['const_root']
            x_val = kwargs['x_val']
            malrule_answer = kwargs['malrule_answer']
            correct_answer = kwargs['correct_answer']
            malrule_expression = kwargs['malrule_expression']

            steps.append(f"Problem: Simplify √(x² + {const})")
            steps.append("")
            steps.append("MALRULE: Square root distributes over addition")
            steps.append(f"  MALRULE REASONING: '√(x² + {const}) = √(x²) + √{const}'")
            steps.append(f"                     '= x + {const_root}'")
            steps.append("")
            steps.append(f"MALRULE 'Simplification': √(x² + {const}) = x + {const_root} (INCORRECT!)")
            steps.append("")
            steps.append(f"If we substitute x = {x_val} to check:")
            steps.append(f"  Malrule gives: {x_val} + {const_root} = {malrule_expression}")
            steps.append(f"  But correct answer is: {correct_answer:.2f}")
            steps.append("")
            steps.append(f"Final Answer: x + {const_root} (INCORRECT expression!)")
            steps.append(f"  Cannot distribute square root over addition!")

        elif problem_type in ['subtraction_variant', 'subtraction_word_problem']:
            a = kwargs['a']
            b = kwargs['b']
            diff_of_squares = kwargs['diff_of_squares']
            malrule_answer = kwargs['malrule_answer']
            correct_answer = kwargs['correct_answer']

            steps.append(f"Problem: Simplify √({a}² - {b}²)")
            steps.append("")
            steps.append("MALRULE: Square root distributes over subtraction")
            steps.append(f"  MALRULE REASONING: '√ applies to each term separately'")
            steps.append(f"                     '√(a² - b²) = √(a²) - √(b²)'")
            steps.append("")
            steps.append(f"Step 1: Take square root of {a}²")
            steps.append(f"  √({a}²) = {a}")
            steps.append("")
            steps.append(f"Step 2: Take square root of {b}²")
            steps.append(f"  √({b}²) = {b}")
            steps.append("")
            steps.append(f"Step 3: Subtract the results (INCORRECT!)")
            steps.append(f"  √({a}² - {b}²) = {a} - {b} = {malrule_answer}")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT!)")
            steps.append(f"  Should compute: {a}² - {b}² = {diff_of_squares}")
            steps.append(f"  Then: √{diff_of_squares} = {correct_answer:.2f}")

        elif problem_type == 'non_perfect_square':
            a = kwargs['a']
            b = kwargs['b']
            sum_of_squares = kwargs['sum_of_squares']
            malrule_answer = kwargs['malrule_answer']
            correct_answer = kwargs['correct_answer']

            steps.append(f"Problem: Simplify √({a}² + {b}²)")
            steps.append("")
            steps.append("MALRULE: Square root distributes over addition")
            steps.append(f"  MALRULE REASONING: '√ applies to each term separately'")
            steps.append(f"                     '√(a² + b²) = √(a²) + √(b²) = a + b'")
            steps.append("")
            steps.append(f"Step 1: Take square root of {a}²")
            steps.append(f"  √({a}²) = {a}")
            steps.append("")
            steps.append(f"Step 2: Take square root of {b}²")
            steps.append(f"  √({b}²) = {b}")
            steps.append("")
            steps.append(f"Step 3: Add the results (INCORRECT!)")
            steps.append(f"  √({a}² + {b}²) = {a} + {b} = {malrule_answer}")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT!)")
            steps.append(f"  Note: This is NOT a Pythagorean triple!")
            steps.append(f"  Should compute: {a}² + {b}² = {sum_of_squares}")
            steps.append(f"  Then: √{sum_of_squares} ≈ {correct_answer:.4f}")
            steps.append(f"  Error is obvious: {malrule_answer} ≠ {correct_answer:.4f}")

        return steps

    def get_name(self) -> str:
        return "Distribute-Square-Root-Over-Addition"

    def get_description(self) -> str:
        return (
            "Students incorrectly distribute the square root over addition, believing "
            "√(a²+b²) = √(a²) + √(b²) = a + b. This is a classic manifestation of the "
            "'illusion of linearity' (De Bock et al., 2007) - students overgeneralize "
            "the distributive property from linear operations to non-linear ones. "
            "Matz (1982) identified this as resulting from 'students' overgeneralisation "
            "of the distributive law.'"
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Malrule: distribute square root over addition/subtraction
        problem_type = problem.metadata.get('problem_type', 'basic_sum_of_squares')

        # For algebraic expressions, return the expression form
        if problem_type == 'algebraic_expression':
            const = problem.metadata['constant']
            const_root = int(const ** 0.5)
            # Return expression form
            return f"x + {const_root}"
        elif problem_type == 'algebraic_word_problem':
            const = problem.metadata['constant']
            const_root = int(const ** 0.5)
            x_val = problem.metadata['x_value']
            # Return numeric value
            return x_val + const_root
        elif problem_type in ['subtraction_variant', 'subtraction_word_problem']:
            a = problem.metadata['a']
            b = problem.metadata['b']
            # √(a²-b²) → a - b (malrule)
            return a - b
        else:
            # √(a²+b²) → a + b (malrule)
            a = problem.metadata['a']
            b = problem.metadata['b']
            return a + b

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        problem_type = problem.metadata.get('problem_type', 'basic_sum_of_squares')

        # Handle enhanced problem types
        if problem_type == 'pythagorean_context':
            return self._handle_pythagorean_context(problem, verbose)
        elif problem_type == 'algebraic_expression':
            return self._handle_algebraic_expression(problem, verbose)
        elif problem_type == 'subtraction_variant':
            return self._handle_subtraction_variant(problem, verbose)
        elif problem_type == 'non_perfect_square':
            return self._handle_non_perfect_square(problem, verbose)
        elif problem_type == 'subtraction_word_problem':
            return self._handle_subtraction_variant(problem, verbose)
        elif problem_type == 'algebraic_word_problem':
            return self._handle_algebraic_expression(problem, verbose)

        # Original basic problem type
        a = problem.metadata['a']
        b = problem.metadata['b']

        # COMPUTE values independently
        a_squared = a ** 2
        b_squared = b ** 2
        sum_of_squares = a_squared + b_squared
        malrule_answer = a + b  # Student incorrectly distributes
        correct_answer = sum_of_squares ** 0.5

        # Generate steps based on verbose flag
        step_kwargs = {
            'a': a,
            'b': b,
            'a_squared': a_squared,
            'b_squared': b_squared,
            'sum_of_squares': sum_of_squares,
            'malrule_answer': malrule_answer,
            'correct_answer': correct_answer
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, problem_type, **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, problem_type, **step_kwargs)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _handle_pythagorean_context(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle Pythagorean theorem word problems with malrule."""
        a = problem.metadata['a']
        b = problem.metadata['b']

        # COMPUTE values independently
        a_squared = a ** 2
        b_squared = b ** 2
        sum_of_squares = a_squared + b_squared
        malrule_answer = a + b  # Student incorrectly distributes
        correct_answer = sum_of_squares ** 0.5

        # Generate steps based on verbose flag
        step_kwargs = {
            'a': a,
            'b': b,
            'sum_of_squares': sum_of_squares,
            'malrule_answer': malrule_answer,
            'correct_answer': correct_answer
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, 'pythagorean_context', **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, 'pythagorean_context', **step_kwargs)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _handle_algebraic_expression(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle algebraic expressions like √(x²+9) with malrule."""
        const = problem.metadata['constant']
        const_root = int(const ** 0.5)
        x_val = problem.metadata['x_value']
        problem_type = problem.metadata.get('problem_type', 'algebraic_expression')

        # COMPUTE values independently
        x_squared = x_val ** 2
        sum_value = x_squared + const
        correct_answer = sum_value ** 0.5

        # Determine the answer format based on problem type
        if problem_type == 'algebraic_word_problem':
            # For word problems, return numeric value
            malrule_answer = x_val + const_root
            malrule_expression = x_val + const_root
        else:
            # For algebraic expressions, return expression
            malrule_answer = f"x + {const_root}"
            malrule_expression = x_val + const_root

        # Generate steps based on verbose flag
        step_kwargs = {
            'const': const,
            'const_root': const_root,
            'x_val': x_val,
            'malrule_answer': malrule_answer,
            'correct_answer': correct_answer,
            'malrule_expression': malrule_expression
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, problem_type, **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, problem_type, **step_kwargs)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _handle_subtraction_variant(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle √(a²-b²) subtraction variant with malrule."""
        a = problem.metadata['a']
        b = problem.metadata['b']

        # COMPUTE values independently
        a_squared = a ** 2
        b_squared = b ** 2
        diff_of_squares = a_squared - b_squared
        malrule_answer = a - b  # Student incorrectly distributes
        correct_answer = diff_of_squares ** 0.5

        # Generate steps based on verbose flag
        step_kwargs = {
            'a': a,
            'b': b,
            'diff_of_squares': diff_of_squares,
            'malrule_answer': malrule_answer,
            'correct_answer': correct_answer
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, 'subtraction_variant', **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, 'subtraction_variant', **step_kwargs)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _handle_non_perfect_square(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle non-perfect square results with malrule."""
        a = problem.metadata['a']
        b = problem.metadata['b']

        # COMPUTE values independently
        a_squared = a ** 2
        b_squared = b ** 2
        sum_of_squares = a_squared + b_squared
        malrule_answer = a + b  # Student incorrectly distributes
        correct_answer = sum_of_squares ** 0.5

        # Generate steps based on verbose flag
        step_kwargs = {
            'a': a,
            'b': b,
            'sum_of_squares': sum_of_squares,
            'malrule_answer': malrule_answer,
            'correct_answer': correct_answer
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, 'non_perfect_square', **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, 'non_perfect_square', **step_kwargs)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
