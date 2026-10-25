"""
Problem generator for Scalar-Multiplication-Inside-Or-Outside-Same malrule.

Generates problems where students confuse f(cx) with c·f(x).
"""

import random
import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, Tuple, Optional, List
from utils import Problem, ProblemGenerator, DifficultyLevel


class ScalarMultiplicationInsideOrOutsideSameProblemGenerator(ProblemGenerator):
    """
    Generates f(cx) evaluation problems.

    Templates:
    1. quadratic_function - f(x) = x²
    2. cubic_function - f(x) = x³
    3. absolute_value - f(x) = |x|
    4. square_root - f(x) = √x
    5. word_problem - Real-world contexts (area, volume)
    """

    def get_name(self) -> str:
        return "Scalar-Multiplication-Inside-Or-Outside-Same Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates function evaluation problems to elicit the misconception "
            "that f(cx) = c·f(x)."
        )

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'quadratic_function',
            'cubic_function',
            'absolute_value',
            'square_root',
            'word_problem'
        ]

    def get_value_ranges(self):
        """Return the value ranges for problem generation."""
        if self.difficulty == DifficultyLevel.EASY:
            return {
                'scalar': (2, 3),
                'input': (1, 4)
            }
        elif self.difficulty == DifficultyLevel.MEDIUM:
            return {
                'scalar': (2, 5),
                'input': (1, 6)
            }
        else:  # HARD
            return {
                'scalar': (2, 6),
                'input': (1, 8)
            }

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate a function evaluation problem with scalar multiplication.

        Args:
            seed: Optional random seed for reproducibility
            template: Optional template name to use

        Returns:
            Problem with f(cx) evaluation question
        """
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            template = random.choice(self.get_available_templates())

        # Generate based on template
        if template == 'quadratic_function':
            return self._generate_quadratic_function(seed)
        elif template == 'cubic_function':
            return self._generate_cubic_function(seed)
        elif template == 'absolute_value':
            return self._generate_absolute_value(seed)
        elif template == 'square_root':
            return self._generate_square_root(seed)
        elif template == 'word_problem':
            return self._generate_word_problem(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_quadratic_function(self, seed=None) -> Problem:
        """Generate f(x) = x² evaluation."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        c = random.randint(*ranges['scalar'])
        x = random.randint(*ranges['input'])

        # Correct: f(cx) = (cx)² = c²x²
        correct_answer = (c * x) ** 2

        # Malrule: f(cx) = c·f(x) = c·x²
        malrule_answer = c * (x ** 2)

        metadata = {
            'template': 'quadratic_function',
            'scalar': c,
            'input': x,
            'function': 'x²',
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer
        }

        return Problem(
            text=f"Given f(x) = x², evaluate f({c}×{x})",
            operands=[c, x],
            operation='function_evaluation',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_cubic_function(self, seed=None) -> Problem:
        """Generate f(x) = x³ evaluation."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        c = random.randint(*ranges['scalar'])
        x = random.randint(*ranges['input'])

        # Correct: f(cx) = (cx)³ = c³x³
        correct_answer = (c * x) ** 3

        # Malrule: f(cx) = c·f(x) = c·x³
        malrule_answer = c * (x ** 3)

        metadata = {
            'template': 'cubic_function',
            'scalar': c,
            'input': x,
            'function': 'x³',
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer
        }

        return Problem(
            text=f"Given f(x) = x³, evaluate f({c}×{x})",
            operands=[c, x],
            operation='function_evaluation',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_absolute_value(self, seed=None) -> Problem:
        """Generate f(x) = |x| evaluation."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        c = random.randint(*ranges['scalar'])
        x = random.randint(*ranges['input'])

        # Correct: f(cx) = |cx| = cx (for positive c and x)
        correct_answer = c * x

        # Malrule: f(cx) = c·f(x) = c·|x| = c·x (same for positive)
        # We need to use different values to show the difference
        # Let's use f(x) = |x+a| where a is a shift
        a = random.randint(1, 3)

        # Correct: f(cx) = |cx + a|
        correct_answer = abs(c * x + a)

        # Malrule: f(cx) = c·f(x) = c·|x + a|
        malrule_answer = c * abs(x + a)

        metadata = {
            'template': 'absolute_value',
            'scalar': c,
            'input': x,
            'shift': a,
            'function': f'|x + {a}|',
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer
        }

        return Problem(
            text=f"Given f(x) = |x + {a}|, evaluate f({c}×{x})",
            operands=[c, x, a],
            operation='function_evaluation',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_square_root(self, seed=None) -> Problem:
        """Generate f(x) = √x evaluation."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        c = random.randint(*ranges['scalar'])

        # Use perfect squares for cleaner arithmetic
        x_values = [1, 4, 9, 16, 25]
        x = random.choice([v for v in x_values if v <= ranges['input'][1]])

        # Correct: f(cx) = √(cx)
        correct_answer = (c * x) ** 0.5

        # Malrule: f(cx) = c·f(x) = c·√x
        malrule_answer = c * (x ** 0.5)

        metadata = {
            'template': 'square_root',
            'scalar': c,
            'input': x,
            'function': '√x',
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer
        }

        return Problem(
            text=f"Given f(x) = √x, evaluate f({c}×{x})",
            operands=[c, x],
            operation='function_evaluation',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_word_problem(self, seed=None) -> Problem:
        """Generate word problem context covering ALL formula types with 3 variants each."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        c = random.randint(*ranges['scalar'])
        x = random.randint(*ranges['input'])

        # Select formula type from all applicable types
        formula_types = ['quadratic_function', 'cubic_function', 'absolute_value', 'square_root']
        formula_type = random.choice(formula_types)
        variant = random.randint(0, 2)  # 3 variants per formula type

        if formula_type == 'quadratic_function':
            # Formula: f(x) = x², f(c×x)
            correct_answer = (c * x) ** 2
            malrule_answer = c * (x ** 2)

            templates = [
                f"The area of a square with side length s is A(s) = s². What is the area when the side length is {c}×{x} units?",
                f"The kinetic energy of an object with mass m is E(m) = m². If you increase mass by a factor of {c}, starting from {x} kg, what is the new energy?",
                f"Power output P(v) = v² where v is velocity. What is P({c}×{x})?"
            ]

            text = templates[variant]
            function_str = 's²'

        elif formula_type == 'cubic_function':
            # Formula: f(x) = x³, f(c×x)
            correct_answer = (c * x) ** 3
            malrule_answer = c * (x ** 3)

            templates = [
                f"The volume of a cube with side length s is V(s) = s³. What is the volume when the side length is {c}×{x} units?",
                f"A cubic growth function G(t) = t³ models expansion. Find G({c}×{x}).",
                f"Volume scales as V(r) = r³. Calculate V({c}×{x})."
            ]

            text = templates[variant]
            function_str = 's³'

        elif formula_type == 'absolute_value':
            # Formula: f(x) = |x + a|, f(c×x)
            a = random.randint(1, 3)
            correct_answer = abs(c * x + a)
            malrule_answer = c * abs(x + a)

            templates = [
                f"Error function E(x) = |x + {a}| measures deviation. Find E({c}×{x}).",
                f"Distance function D(x) = |x + {a}| from origin. Calculate D({c}×{x}).",
                f"Absolute offset A(x) = |x + {a}| units. What is A({c}×{x})?"
            ]

            text = templates[variant]
            function_str = f'|x + {a}|'

        else:  # square_root
            # Formula: f(x) = √x, f(c×x)
            # Use perfect squares for cleaner arithmetic
            x_values = [1, 4, 9, 16, 25]
            x = random.choice([v for v in x_values if v <= ranges['input'][1]])

            correct_answer = (c * x) ** 0.5
            malrule_answer = c * (x ** 0.5)

            templates = [
                f"The square root function S(x) = √x is used. Find S({c}×{x}).",
                f"Side length of square with area A is L(A) = √A. Calculate L({c}×{x}).",
                f"Standard deviation σ(x) = √x for variance x. What is σ({c}×{x})?"
            ]

            text = templates[variant]
            function_str = '√x'

        metadata = {
            'template': 'word_problem',
            'scalar': c,
            'input': x,
            'function': function_str,
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer,
            'is_word_problem': True,
            'word_problem_type': formula_type,
            'word_problem_variant': variant
        }

        if formula_type == 'absolute_value':
            metadata['shift'] = a

        return Problem(
            text=text,
            operands=[c, x],
            operation='function_evaluation',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )
