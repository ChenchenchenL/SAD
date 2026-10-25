"""
Problem generator for Absolute-Value-Makes-Positive malrule.

Generates absolute value equations and inequalities where the right side is negative,
eliciting the misconception that absolute value can equal a negative number.
"""

import random
import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, Tuple, Optional, List
from utils import Problem, ProblemGenerator, DifficultyLevel


class AbsoluteValueMakesPositiveProblemGenerator(ProblemGenerator):
    """
    Generates |x| = k problems where k < 0 (no solution).

    Templates:
    1. basic_equation - Simple |x| = k where k < 0
    2. expression_inside - |x + a| = k where k < 0
    3. inequality - |x| < k or |x| > k where k < 0
    4. compound_expression - |ax + b| = k where k < 0
    5. word_problem - Real-world contexts (distance, temperature, money)
    """

    def get_name(self) -> str:
        return "Absolute-Value-Makes-Positive Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates absolute value equations and inequalities where the right side "
            "is negative, to elicit the misconception that students can 'reverse' the "
            "absolute value operation."
        )

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_equation',
            'expression_inside',
            'inequality',
            'compound_expression',
            'word_problem'
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Return the value ranges for problem generation."""
        ranges = {
            6: {
                DifficultyLevel.EASY: (-10, -1),
                DifficultyLevel.MEDIUM: (-15, -1),
                DifficultyLevel.HARD: (-20, -1),
            },
            7: {
                DifficultyLevel.EASY: (-10, -1),
                DifficultyLevel.MEDIUM: (-20, -1),
                DifficultyLevel.HARD: (-30, -1),
            },
            8: {
                DifficultyLevel.EASY: (-15, -1),
                DifficultyLevel.MEDIUM: (-25, -1),
                DifficultyLevel.HARD: (-40, -1),
            }
        }

        lvl = self.level if self.level in ranges else 7
        return {'negative_value': ranges[lvl][self.difficulty]}

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate an absolute value equation/inequality with negative right side.

        Args:
            seed: Optional random seed for reproducibility
            template: Optional template name to use

        Returns:
            Problem with |expression| = k where k < 0
        """
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            template = random.choice(self.get_available_templates())

        # Generate based on template
        if template == 'basic_equation':
            return self._generate_basic_equation(seed)
        elif template == 'expression_inside':
            return self._generate_expression_inside(seed)
        elif template == 'inequality':
            return self._generate_inequality(seed)
        elif template == 'compound_expression':
            return self._generate_compound_expression(seed)
        elif template == 'word_problem':
            return self._generate_word_problem(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_equation(self, seed=None) -> Problem:
        """Generate basic |x| = k where k < 0."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        negative_value = random.randint(*ranges['negative_value'])

        problem_statement = f"Solve: |x| = {negative_value}"
        correct_answer = "No solution"
        malrule_answer = f"x = {-negative_value}"

        metadata = {
            'template': 'basic_equation',
            'negative_value': negative_value,
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer
        }

        return Problem(
            text=problem_statement,
            operands=[negative_value],
            operation='absolute_value_equation',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_expression_inside(self, seed=None) -> Problem:
        """Generate |x + a| = k where k < 0."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        negative_value = random.randint(*ranges['negative_value'])
        a = random.randint(-10, 10)

        # Avoid a = 0 to make it non-trivial
        while a == 0:
            a = random.randint(-10, 10)

        sign_str = "+" if a >= 0 else ""
        problem_statement = f"Solve: |x {sign_str} {a}| = {negative_value}"
        correct_answer = "No solution"

        # Malrule: Student reverses sign, then solves
        # |x + 3| = -5 → x + 3 = 5 → x = 2
        malrule_answer = f"x = {-negative_value - a}"

        metadata = {
            'template': 'expression_inside',
            'negative_value': negative_value,
            'a': a,
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer
        }

        return Problem(
            text=problem_statement,
            operands=[negative_value, a],
            operation='absolute_value_equation',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_inequality(self, seed=None) -> Problem:
        """Generate |x| < k or |x| > k where k < 0."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        negative_value = random.randint(*ranges['negative_value'])

        # Randomly choose < or >
        inequality_type = random.choice(['<', '>'])

        problem_statement = f"Solve: |x| {inequality_type} {negative_value}"

        # Both have no solution since |x| >= 0 always
        correct_answer = "No solution"

        # Malrule: Student reverses sign
        if inequality_type == '<':
            # |x| < -5 → Student thinks x < 5, so x = {any number < 5}
            malrule_answer = f"x < {-negative_value}"
        else:
            # |x| > -5 → Student thinks x > 5, so x = {any number > 5}
            malrule_answer = f"x > {-negative_value}"

        metadata = {
            'template': 'inequality',
            'negative_value': negative_value,
            'inequality_type': inequality_type,
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer
        }

        return Problem(
            text=problem_statement,
            operands=[negative_value],
            operation='absolute_value_inequality',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_compound_expression(self, seed=None) -> Problem:
        """Generate |ax + b| = k where k < 0."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        negative_value = random.randint(*ranges['negative_value'])

        a = random.choice([2, 3, 4, 5, -2, -3])
        b = random.randint(-10, 10)

        # Format nicely
        if a == 1:
            expr = f"x"
        elif a == -1:
            expr = f"-x"
        else:
            expr = f"{a}x"

        sign_str = "+" if b >= 0 else ""
        if b != 0:
            expr += f" {sign_str} {b}"

        problem_statement = f"Solve: |{expr}| = {negative_value}"
        correct_answer = "No solution"

        # Malrule: Student reverses sign, then solves
        # |2x + 3| = -5 → 2x + 3 = 5 → 2x = 2 → x = 1
        reversed_value = -negative_value
        # Solve ax + b = reversed_value → x = (reversed_value - b) / a
        malrule_x = (reversed_value - b) // a if (reversed_value - b) % a == 0 else (reversed_value - b) / a

        if isinstance(malrule_x, float):
            malrule_answer = f"x = {malrule_x:.2f}"
        else:
            malrule_answer = f"x = {malrule_x}"

        metadata = {
            'template': 'compound_expression',
            'negative_value': negative_value,
            'a': a,
            'b': b,
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer
        }

        return Problem(
            text=problem_statement,
            operands=[negative_value, a, b],
            operation='absolute_value_equation',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_word_problem(self, seed=None) -> Problem:
        """Generate word problem with absolute value context covering all formula types."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()

        # Select which formula type to embed in the word problem
        formula_types = ['basic_x', 'x_plus_a', 'ax_plus_b']
        formula_type = random.choice(formula_types)

        if formula_type == 'basic_x':
            return self._generate_word_problem_basic_x(seed, ranges)
        elif formula_type == 'x_plus_a':
            return self._generate_word_problem_x_plus_a(seed, ranges)
        else:  # ax_plus_b
            return self._generate_word_problem_ax_plus_b(seed, ranges)

    def _generate_word_problem_basic_x(self, seed, ranges) -> Problem:
        """Generate word problems for |x| = k where k < 0."""
        if seed is not None:
            random.seed(seed)

        negative_value = random.randint(*ranges['negative_value'])

        contexts = [
            {
                'text': f"The distance from point A to point B is {negative_value} meters. If the position of B relative to A is x meters, solve |x| = {negative_value}. What are the possible positions?",
                'type': 'distance',
                'malrule': f"x = {-negative_value} meters"
            },
            {
                'text': f"A thermometer measures a temperature deviation of {negative_value} degrees from the standard. If the deviation is x, solve |x| = {negative_value}. What is the deviation?",
                'type': 'temperature',
                'malrule': f"x = {-negative_value} degrees"
            },
            {
                'text': f"An account balance difference is ${negative_value}. If the difference is x dollars, solve |x| = {negative_value}. What is the difference?",
                'type': 'money',
                'malrule': f"x = ${-negative_value}"
            }
        ]

        context = random.choice(contexts)

        problem_statement = context['text']
        correct_answer = "No solution (absolute value cannot be negative)"
        malrule_answer = context['malrule']

        metadata = {
            'template': 'word_problem',
            'word_problem_type': 'basic_x',
            'negative_value': negative_value,
            'context_type': context['type'],
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer
        }

        return Problem(
            text=problem_statement,
            operands=[negative_value],
            operation='absolute_value_equation',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_word_problem_x_plus_a(self, seed, ranges) -> Problem:
        """Generate word problems for |x + a| = k where k < 0."""
        if seed is not None:
            random.seed(seed)

        negative_value = random.randint(*ranges['negative_value'])
        a = random.randint(-10, 10)
        while a == 0:
            a = random.randint(-10, 10)

        sign_str = "+" if a >= 0 else ""

        contexts = [
            {
                'text': f"A drone starts at position x meters and moves {abs(a)} meters {'right' if a >= 0 else 'left'}. The distance from origin is {negative_value} meters. Solve |x {sign_str} {a}| = {negative_value}. What is x?",
                'type': 'distance',
                'malrule': f"x = {-negative_value - a} meters"
            },
            {
                'text': f"The temperature is x degrees. After a change of {a} degrees, the absolute temperature is {negative_value} degrees. Solve |x {sign_str} {a}| = {negative_value}. What is x?",
                'type': 'temperature',
                'malrule': f"x = {-negative_value - a} degrees"
            },
            {
                'text': f"An account has x dollars. After {'adding' if a >= 0 else 'removing'} ${abs(a)}, the absolute balance is ${negative_value}. Solve |x {sign_str} {a}| = {negative_value}. What is x?",
                'type': 'money',
                'malrule': f"x = ${-negative_value - a}"
            }
        ]

        context = random.choice(contexts)

        problem_statement = context['text']
        correct_answer = "No solution (absolute value cannot be negative)"
        malrule_answer = context['malrule']

        metadata = {
            'template': 'word_problem',
            'word_problem_type': 'x_plus_a',
            'negative_value': negative_value,
            'a': a,
            'context_type': context['type'],
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer
        }

        return Problem(
            text=problem_statement,
            operands=[negative_value, a],
            operation='absolute_value_equation',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_word_problem_ax_plus_b(self, seed, ranges) -> Problem:
        """Generate word problems for |ax + b| = k where k < 0."""
        if seed is not None:
            random.seed(seed)

        negative_value = random.randint(*ranges['negative_value'])
        a = random.choice([2, 3, 4, 5, -2, -3])
        b = random.randint(-10, 10)

        # Format expression
        if a == 1:
            expr = f"x"
        elif a == -1:
            expr = f"-x"
        else:
            expr = f"{a}x"

        sign_str = "+" if b >= 0 else ""
        if b != 0:
            expr += f" {sign_str} {b}"

        contexts = [
            {
                'text': f"A factory produces x items per hour for {abs(a)} hours, then {'adds' if b >= 0 else 'removes'} {abs(b)} items. The absolute production is {negative_value} items. Solve |{expr}| = {negative_value}. What is x?",
                'type': 'production',
                'malrule': f"x = {(-negative_value - b) // a if (-negative_value - b) % a == 0 else round((-negative_value - b) / a, 2)} items"
            },
            {
                'text': f"A car travels at x km/h for {abs(a)} hours, then {'adds' if b >= 0 else 'subtracts'} {abs(b)} km. The absolute distance is {negative_value} km. Solve |{expr}| = {negative_value}. What is x?",
                'type': 'distance',
                'malrule': f"x = {(-negative_value - b) // a if (-negative_value - b) % a == 0 else round((-negative_value - b) / a, 2)} km/h"
            },
            {
                'text': f"An investment grows by a factor of {a} times the initial amount x, then {'gains' if b >= 0 else 'loses'} ${abs(b)}. The absolute value is ${negative_value}. Solve |{expr}| = {negative_value}. What is x?",
                'type': 'money',
                'malrule': f"x = ${(-negative_value - b) // a if (-negative_value - b) % a == 0 else round((-negative_value - b) / a, 2)}"
            }
        ]

        context = random.choice(contexts)

        problem_statement = context['text']
        correct_answer = "No solution (absolute value cannot be negative)"
        malrule_answer = context['malrule']

        metadata = {
            'template': 'word_problem',
            'word_problem_type': 'ax_plus_b',
            'negative_value': negative_value,
            'a': a,
            'b': b,
            'context_type': context['type'],
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer
        }

        return Problem(
            text=problem_statement,
            operands=[negative_value, a, b],
            operation='absolute_value_equation',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

