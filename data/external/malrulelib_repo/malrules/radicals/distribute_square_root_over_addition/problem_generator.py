"""
Problem generator for Distribute-Square-Root-Over-Addition malrule.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, List, Optional
from utils import ProblemGenerator, Problem, DifficultyLevel


class DistributeSquareRootOverAdditionProblemGenerator(ProblemGenerator):
    """Generates square root problems of form √(a²+b²)."""

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        ranges = {
            8: {
                DifficultyLevel.EASY: {'value': (2, 5)},
                DifficultyLevel.MEDIUM: {'value': (3, 8)},
                DifficultyLevel.HARD: {'value': (4, 10)}
            },
            9: {
                DifficultyLevel.EASY: {'value': (3, 6)},
                DifficultyLevel.MEDIUM: {'value': (3, 10)},
                DifficultyLevel.HARD: {'value': (5, 12)}
            },
            10: {
                DifficultyLevel.EASY: {'value': (3, 8)},
                DifficultyLevel.MEDIUM: {'value': (4, 12)},
                DifficultyLevel.HARD: {'value': (5, 15)}
            }
        }
        lvl = self.level if self.level in ranges else 9
        return ranges[lvl][self.difficulty]

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_sum_of_squares',
            'pythagorean_context',
            'algebraic_expression',
            'subtraction_variant',
            'non_perfect_square',
            'word_problem_subtraction',
            'word_problem_algebraic'
        ]

    def generate(self, seed=None, template: Optional[str] = None) -> Problem:
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            # Choose problem type
            problem_types = ['basic_sum_of_squares']

            # Add enhanced problem types for higher levels
            if self.level >= 8:
                problem_types.extend([
                    'pythagorean_context',      # Distance/right triangle word problems
                    'algebraic_expression',     # With variables like √(x²+9)
                    'subtraction_variant',      # √(a²-b²) confusion
                    'non_perfect_square',       # Emphasize irrational results
                    'word_problem_subtraction',  # Word problems for subtraction
                    'word_problem_algebraic'     # Word problems for algebraic
                ])

            template = random.choice(problem_types)

        # Route to appropriate template handler
        if template == 'word_problem_subtraction':
            return self._generate_word_problem_subtraction(seed)
        elif template == 'word_problem_algebraic':
            return self._generate_word_problem_algebraic(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['value']

        problem_type = template

        # Generate a and b values
        a = random.randint(min_val, max_val)
        b = random.randint(min_val, max_val)

        # Ensure a ≠ b for more interesting problems
        attempts = 0
        while a == b and attempts < 20:
            b = random.randint(min_val, max_val)
            attempts += 1

        # Handle enhanced problem types first
        if problem_type == 'pythagorean_context':
            # Word problem with distance or right triangle
            contexts = [
                (f"A ladder is {a} meters from a wall and reaches {b} meters high. How long is the ladder?",
                 "ladder"),
                (f"You walk {a} blocks east and {b} blocks north. What is the straight-line distance from your starting point?",
                 "distance"),
                (f"A right triangle has legs of length {a} and {b}. What is the length of the hypotenuse?",
                 "triangle"),
            ]

            context_text, context_type = random.choice(contexts)

            a_squared = a ** 2
            b_squared = b ** 2
            sum_of_squares = a_squared + b_squared
            correct_answer = sum_of_squares ** 0.5
            malrule_answer = a + b

            return Problem(
                text=context_text,
                operands=[a, b],
                operation='pythagorean_word_problem',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'a': a,
                    'b': b,
                    'a_squared': a_squared,
                    'b_squared': b_squared,
                    'sum_of_squares': sum_of_squares,
                    'problem_type': problem_type,
                    'context': context_type,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer
                }
            )

        elif problem_type == 'algebraic_expression':
            # Expression with variable like √(x²+9)
            # Use a² as the constant for variety
            const = random.choice([4, 9, 16, 25])  # Perfect squares
            const_root = int(const ** 0.5)

            text = f"Simplify √(x² + {const})"

            # For testing purposes, we'll substitute a value for x
            x_val = random.randint(3, 8)
            x_squared = x_val ** 2
            sum_value = x_squared + const
            correct_answer = sum_value ** 0.5
            malrule_answer = f"x + {const_root}"  # String representation

            return Problem(
                text=text,
                operands=[x_val, const_root],
                operation='algebraic_radical_simplification',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'variable': 'x',
                    'x_value': x_val,
                    'constant': const,
                    'const_root': const_root,
                    'x_squared': x_squared,
                    'sum_value': sum_value,
                    'problem_type': problem_type,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'correct_expression': f"√({x_squared} + {const})",
                    'malrule_expression': f"{x_val} + {const_root}"
                }
            )

        elif problem_type == 'subtraction_variant':
            # √(a²-b²) where students might incorrectly do a-b
            # Ensure a > b for positive result
            if a < b:
                a, b = b, a

            a_squared = a ** 2
            b_squared = b ** 2
            diff_of_squares = a_squared - b_squared
            correct_answer = diff_of_squares ** 0.5
            malrule_answer = a - b  # Student incorrectly distributes

            text = f"Simplify √({a}² - {b}²)"

            return Problem(
                text=text,
                operands=[a, b],
                operation='square_root_diff_of_squares',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'a': a,
                    'b': b,
                    'a_squared': a_squared,
                    'b_squared': b_squared,
                    'diff_of_squares': diff_of_squares,
                    'problem_type': problem_type,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer
                }
            )

        elif problem_type == 'non_perfect_square':
            # Use values that don't form a Pythagorean triple
            # to emphasize that distribution error is more obvious
            non_triple_pairs = [(2, 3), (2, 5), (3, 5), (4, 5), (5, 7), (6, 7)]
            a, b = random.choice(non_triple_pairs)

            a_squared = a ** 2
            b_squared = b ** 2
            sum_of_squares = a_squared + b_squared
            correct_answer = sum_of_squares ** 0.5
            malrule_answer = a + b

            text = f"Simplify √({a}² + {b}²)"

            return Problem(
                text=text,
                operands=[a, b],
                operation='square_root_non_perfect_square',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'a': a,
                    'b': b,
                    'a_squared': a_squared,
                    'b_squared': b_squared,
                    'sum_of_squares': sum_of_squares,
                    'problem_type': problem_type,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer
                }
            )

        # Original basic problem type
        # Calculate values
        a_squared = a ** 2
        b_squared = b ** 2
        sum_of_squares = a_squared + b_squared

        # Correct answer: √(a²+b²)
        correct_answer = sum_of_squares ** 0.5

        # Malrule answer: a + b (distributing square root)
        malrule_answer = a + b

        text = f"Simplify √({a}² + {b}²)"

        return Problem(
            text=text,
            operands=[a, b],
            operation='square_root_sum_of_squares',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'a': a,
                'b': b,
                'a_squared': a_squared,
                'b_squared': b_squared,
                'sum_of_squares': sum_of_squares,
                'problem_type': problem_type,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_word_problem_subtraction(self, seed: Optional[int] = None) -> Problem:
        """Generate word problems for subtraction variant √(a²-b²) with 3 context variants."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['value']

        a = random.randint(min_val, max_val)
        b = random.randint(min_val, max_val)

        # Ensure a > b for positive result
        if a < b:
            a, b = b, a

        a_squared = a ** 2
        b_squared = b ** 2
        diff_of_squares = a_squared - b_squared
        correct_answer = diff_of_squares ** 0.5
        malrule_answer = a - b  # Student incorrectly distributes

        # Three context variants
        contexts = [
            {
                'type': 'velocity',
                'text': f"A particle's velocity components satisfy v² = {a_squared} - {b_squared}. What is the magnitude of velocity v? (Calculate √({a}² - {b}²))",
                'answer_unit': 'units'
            },
            {
                'type': 'geometry',
                'text': f"The difference between two square areas is {a_squared} - {b_squared}. If the larger square has side {a} and the smaller has side {b}, what is √({a}² - {b}²)?",
                'answer_unit': 'units'
            },
            {
                'type': 'physics',
                'text': f"In a physics problem, you need to calculate √({a}² - {b}²) where the values represent measurements. What is the result?",
                'answer_unit': 'units'
            }
        ]

        context = random.choice(contexts)

        return Problem(
            text=context['text'],
            operands=[a, b],
            operation='square_root_diff_of_squares',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_subtraction',
                'context_type': context['type'],
                'problem_type': 'subtraction_word_problem',
                'a': a,
                'b': b,
                'a_squared': a_squared,
                'b_squared': b_squared,
                'diff_of_squares': diff_of_squares,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_word_problem_algebraic(self, seed: Optional[int] = None) -> Problem:
        """Generate word problems for algebraic expressions √(x²+k) with 3 context variants."""
        if seed is not None:
            random.seed(seed)

        # Use a² as the constant for variety
        const = random.choice([4, 9, 16, 25])  # Perfect squares
        const_root = int(const ** 0.5)

        # For testing purposes, we'll substitute a value for x
        x_val = random.randint(3, 8)
        x_squared = x_val ** 2
        sum_value = x_squared + const
        correct_answer = sum_value ** 0.5
        malrule_answer = x_val + const_root

        # Three context variants
        contexts = [
            {
                'type': 'diagonal',
                'text': f"A rectangle has one side of length x and another of length {const_root}. If x = {x_val}, what is the exact length of the diagonal? (Calculate √(x² + {const}))",
                'answer_unit': 'units'
            },
            {
                'type': 'distance',
                'text': f"The distance formula gives d = √(x² + {const}). If x = {x_val}, what is the distance d?",
                'answer_unit': 'units'
            },
            {
                'type': 'function',
                'text': f"Evaluate the function f(x) = √(x² + {const}) when x = {x_val}. What is f({x_val})?",
                'answer_unit': 'units'
            }
        ]

        context = random.choice(contexts)

        return Problem(
            text=context['text'],
            operands=[x_val, const_root],
            operation='algebraic_radical_simplification',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_algebraic',
                'context_type': context['type'],
                'problem_type': 'algebraic_word_problem',
                'variable': 'x',
                'x_value': x_val,
                'constant': const,
                'const_root': const_root,
                'x_squared': x_squared,
                'sum_value': sum_value,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'correct_expression': f"√({x_squared} + {const})",
                'malrule_expression': f"{x_val} + {const_root}"
            }
        )
