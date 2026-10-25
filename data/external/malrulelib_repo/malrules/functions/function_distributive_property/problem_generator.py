"""
Problem generator for Function-Distributive-Property malrule.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple
from utils import ProblemGenerator, Problem, DifficultyLevel


class FunctionDistributivePropertyProblemGenerator(ProblemGenerator):
    """Generates function evaluation problems with addition in the input."""

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        ranges = {
            8: {
                DifficultyLevel.EASY: {'base': (2, 5), 'value1': (1, 5), 'value2': (1, 5)},
                DifficultyLevel.MEDIUM: {'base': (2, 6), 'value1': (2, 8), 'value2': (1, 6)},
                DifficultyLevel.HARD: {'base': (2, 8), 'value1': (3, 10), 'value2': (2, 8)}
            },
            9: {
                DifficultyLevel.EASY: {'base': (2, 6), 'value1': (2, 6), 'value2': (1, 6)},
                DifficultyLevel.MEDIUM: {'base': (2, 8), 'value1': (3, 10), 'value2': (2, 8)},
                DifficultyLevel.HARD: {'base': (3, 10), 'value1': (3, 12), 'value2': (2, 10)}
            },
            10: {
                DifficultyLevel.EASY: {'base': (2, 8), 'value1': (3, 10), 'value2': (2, 8)},
                DifficultyLevel.MEDIUM: {'base': (3, 10), 'value1': (3, 12), 'value2': (2, 10)},
                DifficultyLevel.HARD: {'base': (3, 12), 'value1': (4, 15), 'value2': (3, 12)}
            },
            11: {
                DifficultyLevel.EASY: {'base': (3, 10), 'value1': (3, 12), 'value2': (2, 10)},
                DifficultyLevel.MEDIUM: {'base': (3, 12), 'value1': (4, 15), 'value2': (3, 12)},
                DifficultyLevel.HARD: {'base': (4, 15), 'value1': (5, 20), 'value2': (4, 15)}
            }
        }
        lvl = self.level if self.level in ranges else 9
        return ranges[lvl][self.difficulty]

    def generate(self, seed=None) -> Problem:
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()

        # Choose problem type
        problem_types = ['square', 'scaled_square']

        # Add enhanced problem types for higher levels
        if self.level >= 9:
            problem_types.extend([
                'subtraction_input',      # f(x-a) → students think f(x) - f(a)
                'cubic_function',         # f(x) = x³
                'absolute_value',         # f(x) = |x+k|
                'word_problem_context',   # Real-world applications
            ])

        problem_type = random.choice(problem_types)

        # Generate two values
        x1 = random.randint(ranges['value1'][0], ranges['value1'][1])
        x2 = random.randint(ranges['value2'][0], ranges['value2'][1])

        # Handle enhanced problem types first
        if problem_type == 'subtraction_input':
            # f(x-a) where students think f(x) - f(a)
            a = random.choice([1, 2])
            input_diff = x1 - x2

            if a == 1:
                func_str = "x²"
            else:
                func_str = f"{a}x²"

            text = f"Given f(x) = {func_str}, evaluate f({x1}-{x2})"
            correct_answer = a * (input_diff ** 2)
            malrule_answer = a * (x1 ** 2) - a * (x2 ** 2)  # f(x1) - f(x2)

            return Problem(
                text=text,
                operands=[a, x1, x2],
                operation='function_evaluation_with_difference',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'coefficient': a,
                    'value1': x1,
                    'value2': x2,
                    'input_value': input_diff,
                    'operation': 'subtraction',
                    'problem_type': problem_type,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'function_type': 'quadratic'
                }
            )

        elif problem_type == 'cubic_function':
            # f(x) = x³ with addition
            input_sum = x1 + x2

            text = f"Given f(x) = x³, evaluate f({x1}+{x2})"
            correct_answer = input_sum ** 3
            malrule_answer = (x1 ** 3) + (x2 ** 3)  # f(x1) + f(x2)

            return Problem(
                text=text,
                operands=[1, x1, x2],
                operation='function_evaluation_cubic',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'coefficient': 1,
                    'value1': x1,
                    'value2': x2,
                    'input_value': input_sum,
                    'operation': 'addition',
                    'problem_type': problem_type,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'function_type': 'cubic'
                }
            )

        elif problem_type == 'absolute_value':
            # f(x) = |x| or f(x) = |x+k|
            k = random.randint(1, 4)
            input_sum = x1 + x2

            text = f"Given f(x) = |x+{k}|, evaluate f({x1}+{x2})"
            correct_answer = abs(input_sum + k)
            malrule_answer = abs(x1 + k) + abs(x2 + k)  # f(x1) + f(x2)

            return Problem(
                text=text,
                operands=[1, x1, x2],
                operation='function_evaluation_absolute',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'coefficient': 1,
                    'k_value': k,
                    'value1': x1,
                    'value2': x2,
                    'input_value': input_sum,
                    'operation': 'addition',
                    'problem_type': problem_type,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'function_type': 'absolute_value'
                }
            )

        elif problem_type == 'word_problem_context':
            # NEW: Comprehensive word problems covering ALL formula types
            # Select formula type from all applicable types
            formula_types = ['square', 'scaled_square', 'subtraction_input', 'cubic_function', 'absolute_value']
            formula_type = random.choice(formula_types)
            variant = random.randint(0, 2)  # 3 variants per formula type

            if formula_type == 'square':
                # Formula: f(x) = x², f(a+b)
                input_sum = x1 + x2
                correct_answer = input_sum ** 2
                malrule_answer = (x1 ** 2) + (x2 ** 2)

                templates = [
                    f"The area of a square with side length s is A(s) = s². Find the area when the side length is {x1}+{x2} cm.",
                    f"A function models growth: G(t) = t². Calculate G({x1}+{x2}).",
                    f"The power output P(v) = v² where v is velocity. Find P({x1}+{x2})."
                ]

                return Problem(
                    text=templates[variant],
                    operands=[1, x1, x2],
                    operation='function_evaluation_word',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'coefficient': 1,
                        'value1': x1,
                        'value2': x2,
                        'input_value': input_sum,
                        'operation': 'addition',
                        'problem_type': problem_type,
                        'correct_answer': correct_answer,
                        'malrule_answer': malrule_answer,
                        'function_type': 'quadratic',
                        'is_word_problem': True,
                        'word_problem_type': formula_type,
                        'word_problem_variant': variant
                    }
                )

            elif formula_type == 'scaled_square':
                # Formula: f(x) = ax², f(b+c)
                a = random.randint(2, 4)
                input_sum = x1 + x2
                correct_answer = a * (input_sum ** 2)
                malrule_answer = a * (x1 ** 2) + a * (x2 ** 2)

                templates = [
                    f"The cost function is C(x) = {a}x². Find C({x1}+{x2}).",
                    f"Energy stored in a spring is E(d) = {a}d² joules. Calculate E({x1}+{x2}).",
                    f"The surface area function is S(r) = {a}r². Find S({x1}+{x2})."
                ]

                return Problem(
                    text=templates[variant],
                    operands=[a, x1, x2],
                    operation='function_evaluation_word',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'coefficient': a,
                        'value1': x1,
                        'value2': x2,
                        'input_value': input_sum,
                        'operation': 'addition',
                        'problem_type': problem_type,
                        'correct_answer': correct_answer,
                        'malrule_answer': malrule_answer,
                        'function_type': 'quadratic',
                        'is_word_problem': True,
                        'word_problem_type': formula_type,
                        'word_problem_variant': variant
                    }
                )

            elif formula_type == 'subtraction_input':
                # Formula: f(x) = ax², f(b-c)
                a = random.choice([1, 2])
                input_diff = x1 - x2
                correct_answer = a * (input_diff ** 2)
                malrule_answer = a * (x1 ** 2) - a * (x2 ** 2)

                templates = [
                    f"The distance function is D(t) = {a if a > 1 else ''}t². Find the distance at time {x1}-{x2} hours.",
                    f"Temperature variance V(x) = {a if a > 1 else ''}x² degrees. Calculate V({x1}-{x2}).",
                    f"The profit function is P(n) = {a if a > 1 else ''}n² dollars. Find P({x1}-{x2})."
                ]

                return Problem(
                    text=templates[variant],
                    operands=[a, x1, x2],
                    operation='function_evaluation_word',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'coefficient': a,
                        'value1': x1,
                        'value2': x2,
                        'input_value': input_diff,
                        'operation': 'subtraction',
                        'problem_type': problem_type,
                        'correct_answer': correct_answer,
                        'malrule_answer': malrule_answer,
                        'function_type': 'quadratic',
                        'is_word_problem': True,
                        'word_problem_type': formula_type,
                        'word_problem_variant': variant
                    }
                )

            elif formula_type == 'cubic_function':
                # Formula: f(x) = x³, f(a+b)
                input_sum = x1 + x2
                correct_answer = input_sum ** 3
                malrule_answer = (x1 ** 3) + (x2 ** 3)

                templates = [
                    f"The volume of a cube with side s is V(s) = s³. Find the volume when s = {x1}+{x2} cm.",
                    f"A growth model is G(t) = t³. Calculate G({x1}+{x2}).",
                    f"The cubic function C(x) = x³ models expansion. Find C({x1}+{x2})."
                ]

                return Problem(
                    text=templates[variant],
                    operands=[1, x1, x2],
                    operation='function_evaluation_word',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'coefficient': 1,
                        'value1': x1,
                        'value2': x2,
                        'input_value': input_sum,
                        'operation': 'addition',
                        'problem_type': problem_type,
                        'correct_answer': correct_answer,
                        'malrule_answer': malrule_answer,
                        'function_type': 'cubic',
                        'is_word_problem': True,
                        'word_problem_type': formula_type,
                        'word_problem_variant': variant
                    }
                )

            else:  # absolute_value
                # Formula: f(x) = |x+k|, f(a+b)
                k = random.randint(1, 4)
                input_sum = x1 + x2
                correct_answer = abs(input_sum + k)
                malrule_answer = abs(x1 + k) + abs(x2 + k)

                templates = [
                    f"The error function E(x) = |x+{k}| measures deviation. Find E({x1}+{x2}).",
                    f"Distance from origin is D(x) = |x+{k}| units. Calculate D({x1}+{x2}).",
                    f"Absolute deviation A(x) = |x+{k}|. Find A({x1}+{x2})."
                ]

                return Problem(
                    text=templates[variant],
                    operands=[1, x1, x2],
                    operation='function_evaluation_word',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'coefficient': 1,
                        'k_value': k,
                        'value1': x1,
                        'value2': x2,
                        'input_value': input_sum,
                        'operation': 'addition',
                        'problem_type': problem_type,
                        'correct_answer': correct_answer,
                        'malrule_answer': malrule_answer,
                        'function_type': 'absolute_value',
                        'is_word_problem': True,
                        'word_problem_type': formula_type,
                        'word_problem_variant': variant
                    }
                )

        # Original problem types (square and scaled_square)
        if problem_type == 'square':
            a = 1  # f(x) = x²
        else:
            a = random.randint(2, 4)  # f(x) = ax²

        # Input is x1 + x2
        input_sum = x1 + x2

        # Correct answer: f(x1 + x2) = a(x1 + x2)²
        correct_answer = a * (input_sum ** 2)

        # Malrule answer: f(x1 + x2) = f(x1) + f(x2) = a*x1² + a*x2²
        malrule_answer = a * (x1 ** 2) + a * (x2 ** 2)

        # Format function string
        if a == 1:
            func_str = "x²"
        else:
            func_str = f"{a}x²"

        text = f"Given f(x) = {func_str}, evaluate f({x1}+{x2})"

        return Problem(
            text=text,
            operands=[a, x1, x2],
            operation='function_evaluation_with_sum',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'coefficient': a,
                'value1': x1,
                'value2': x2,
                'input_sum': input_sum,
                'input_value': input_sum,
                'operation': 'addition',
                'problem_type': problem_type,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'function_type': 'quadratic'
            }
        )
