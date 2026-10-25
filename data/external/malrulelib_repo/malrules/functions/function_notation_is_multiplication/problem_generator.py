"""
Problem generator for Function-Notation-Is-Multiplication malrule.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple
from utils import ProblemGenerator, Problem, DifficultyLevel


class FunctionNotationIsMultiplicationProblemGenerator(ProblemGenerator):
    """Generates function evaluation problems."""

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        ranges = {
            8: {DifficultyLevel.EASY: (1, 10), DifficultyLevel.MEDIUM: (1, 15), DifficultyLevel.HARD: (1, 20)},
            9: {DifficultyLevel.EASY: (1, 15), DifficultyLevel.MEDIUM: (1, 20), DifficultyLevel.HARD: (1, 30)},
            10: {DifficultyLevel.EASY: (1, 20), DifficultyLevel.MEDIUM: (1, 30), DifficultyLevel.HARD: (1, 50)},
            11: {DifficultyLevel.EASY: (1, 20), DifficultyLevel.MEDIUM: (1, 40), DifficultyLevel.HARD: (1, 50)},
        }
        lvl = self.level if self.level in ranges else 9
        return {'values': ranges[lvl][self.difficulty]}

    def generate(self, seed=None, template=None) -> Problem:
        if seed is not None:
            random.seed(seed)

        val_range = self.get_value_ranges()['values']
        min_val, max_val = val_range

        # Choose problem type
        problem_types = ['simple_linear']

        # Add enhanced problem types for higher levels
        if self.level >= 9:
            problem_types.extend([
                'quadratic_function',          # f(x) = ax² + bx + c
                'function_composition',        # f(g(x)) interpreted as f×g×x
                'absolute_value_function',     # f(x) = |ax + b|
                'word_problem_context',        # Real-world function contexts
            ])
        if template is not None:
            problem_type = template
        else:
            problem_type = random.choice(problem_types)

        if problem_type == 'simple_linear':
            # Generate simple linear function f(x) = ax + b
            a = random.randint(1, 5)  # Coefficient
            b = random.randint(-10, 10)  # Constant

            # Generate input value
            x = random.randint(min_val, max_val)

            # Correct answer: f(x) = ax + b
            correct_answer = a * x + b

            # Malrule answer: Student thinks f(x) means f × x
            # They compute coefficient times x, miss the +b
            malrule_answer = a * x

            text = f"Given f(x) = {a}x + {b}, evaluate f({x})"

        elif problem_type == 'quadratic_function':
            # Quadratic function: f(x) = ax² + bx + c
            a = random.randint(1, 3)
            b = random.randint(-5, 5)
            c = random.randint(-10, 10)

            x = random.randint(1, 5)  # Smaller x for quadratics

            # Correct answer: ax² + bx + c
            correct_answer = a * (x ** 2) + b * x + c

            # Malrule: Student thinks f(x) is multiplication, computes a × x
            malrule_answer = a * x

            # Format the function nicely
            b_sign = '+' if b >= 0 else ''
            c_sign = '+' if c >= 0 else ''
            text = f"Given f(x) = {a}x² {b_sign} {b}x {c_sign} {c}, evaluate f({x})"

            # Store complete metadata for quadratic functions
            return Problem(
                text=text,
                operands=[a, b, c, x],
                operation='function_evaluation',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'coefficient': a,
                    'b_coefficient': b,
                    'c_constant': c,
                    'constant': c,  # For compatibility
                    'input': x,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'problem_type': problem_type
                }
            )

        elif problem_type == 'function_composition':
            # Composition like f(g(x)) where student thinks it's f × g × x
            # Let's use f(x) = 2x + 1 and g(x) = x + 3, then f(g(2))
            a = random.randint(2, 4)  # f coefficient
            b = random.randint(1, 5)  # f constant
            c = random.randint(1, 4)  # g coefficient
            d = random.randint(1, 6)  # g constant

            x = random.randint(1, 4)

            # Correct: f(g(x)) = f(cx + d) = a(cx + d) + b
            g_of_x = c * x + d
            correct_answer = a * g_of_x + b

            # Malrule: Student thinks f(g(x)) = f × g × x
            # They might compute: a × c × x
            malrule_answer = a * c * x

            text = f"Given f(x) = {a}x + {b} and g(x) = {c}x + {d}, evaluate f(g({x}))"

            # Return with complete metadata
            return Problem(
                text=text,
                operands=[a, b, c, d, x],
                operation='function_evaluation',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'coefficient': a,
                    'constant': b,
                    'input': x,
                    'g_coefficient': c,
                    'g_constant': d,
                    'inner_result': g_of_x,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'problem_type': problem_type
                }
            )

        elif problem_type == 'absolute_value_function':
            # Absolute value function: f(x) = |ax + b|
            a = random.randint(2, 5)
            b = random.randint(-8, -1)  # Negative so we might get negative inside

            x = random.randint(1, 3)  # Small x

            # Correct answer: |ax + b|
            correct_answer = abs(a * x + b)

            # Malrule: Student thinks f(x) is f × x, computes a × x
            malrule_answer = a * x

            b_sign = '+' if b >= 0 else ''
            text = f"Given f(x) = |{a}x {b_sign} {b}|, evaluate f({x})"

            # Return with complete metadata
            return Problem(
                text=text,
                operands=[a, b, x],
                operation='function_evaluation',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'coefficient': a,
                    'constant': b,
                    'input': x,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'problem_type': problem_type
                }
            )

        elif problem_type == 'word_problem_context':
            # NEW: Comprehensive word problems covering ALL formula types
            # Select formula type from all applicable types
            formula_types = ['simple_linear', 'quadratic_function', 'function_composition', 'absolute_value_function']
            formula_type = random.choice(formula_types)
            variant = random.randint(0, 2)  # 3 variants per formula type

            if formula_type == 'simple_linear':
                # Formula: f(x) = ax + b
                a = random.randint(3, 8)
                b = random.randint(10, 30)
                x = random.randint(2, 6)

                correct_answer = a * x + b
                malrule_answer = a * x

                templates = [
                    f"The cost function for producing x items is C(x) = {a}x + {b} dollars. Find C({x}).",
                    f"The temperature T(h) after h hours is T(h) = {a}h + {b} degrees. What is T({x})?",
                    f"A taxi charges F(m) = {a}m + {b} dollars for m miles. Calculate F({x})."
                ]

                text = templates[variant]

                return Problem(
                    text=text,
                    operands=[a, b, x],
                    operation='function_evaluation',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'coefficient': a,
                        'constant': b,
                        'input': x,
                        'correct_answer': correct_answer,
                        'malrule_answer': malrule_answer,
                        'problem_type': problem_type,
                        'is_word_problem': True,
                        'word_problem_type': formula_type,
                        'word_problem_variant': variant
                    }
                )

            elif formula_type == 'quadratic_function':
                # Formula: f(x) = ax² + bx + c
                a = random.randint(1, 3)
                b = random.randint(-5, 5)
                c = random.randint(-10, 10)
                x = random.randint(1, 5)

                correct_answer = a * (x ** 2) + b * x + c
                malrule_answer = a * x

                b_sign = '+' if b >= 0 else ''
                c_sign = '+' if c >= 0 else ''

                templates = [
                    f"The profit function is P(x) = {a}x² {b_sign} {b}x {c_sign} {c} dollars for x units. Find P({x}).",
                    f"The trajectory height is H(t) = {a}t² {b_sign} {b}t {c_sign} {c} meters at time t. Calculate H({x}).",
                    f"Energy efficiency E(n) = {a}n² {b_sign} {b}n {c_sign} {c} for n machines. What is E({x})?"
                ]

                text = templates[variant]

                return Problem(
                    text=text,
                    operands=[a, b, c, x],
                    operation='function_evaluation',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'coefficient': a,
                        'constant': c,
                        'input': x,
                        'b_coefficient': b,
                        'c_constant': c,
                        'correct_answer': correct_answer,
                        'malrule_answer': malrule_answer,
                        'problem_type': problem_type,
                        'is_word_problem': True,
                        'word_problem_type': formula_type,
                        'word_problem_variant': variant
                    }
                )

            elif formula_type == 'function_composition':
                # Formula: f(g(x))
                a = random.randint(2, 4)
                b = random.randint(1, 5)
                c = random.randint(1, 4)
                d = random.randint(1, 6)
                x = random.randint(1, 4)

                g_of_x = c * x + d
                correct_answer = a * g_of_x + b
                malrule_answer = a * c * x

                templates = [
                    f"A machine process has two stages: g(x) = {c}x + {d} and f(x) = {a}x + {b}. Find f(g({x})).",
                    f"Temperature conversion: g(x) = {c}x + {d} converts to Celsius, f(x) = {a}x + {b} adds offset. Calculate f(g({x})).",
                    f"Production stages: first g(x) = {c}x + {d}, then f(x) = {a}x + {b}. What is f(g({x}))?"
                ]

                text = templates[variant]

                return Problem(
                    text=text,
                    operands=[a, b, c, d, x],
                    operation='function_evaluation',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'coefficient': a,
                        'constant': b,
                        'input': x,
                        'g_coefficient': c,
                        'g_constant': d,
                        'inner_result': g_of_x,
                        'correct_answer': correct_answer,
                        'malrule_answer': malrule_answer,
                        'problem_type': problem_type,
                        'is_word_problem': True,
                        'word_problem_type': formula_type,
                        'word_problem_variant': variant
                    }
                )

            else:  # absolute_value_function
                # Formula: f(x) = |ax + b|
                a = random.randint(2, 5)
                b = random.randint(-8, -1)
                x = random.randint(1, 3)

                correct_answer = abs(a * x + b)
                malrule_answer = a * x

                b_sign = '+' if b >= 0 else ''

                templates = [
                    f"The error margin E(x) = |{a}x {b_sign} {b}| units for x trials. Find E({x}).",
                    f"Absolute deviation D(x) = |{a}x {b_sign} {b}| from target. Calculate D({x}).",
                    f"Distance from zero: F(x) = |{a}x {b_sign} {b}| units. What is F({x})?"
                ]

                text = templates[variant]

                return Problem(
                    text=text,
                    operands=[a, b, x],
                    operation='function_evaluation',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'coefficient': a,
                        'constant': b,
                        'input': x,
                        'correct_answer': correct_answer,
                        'malrule_answer': malrule_answer,
                        'problem_type': problem_type,
                        'is_word_problem': True,
                        'word_problem_type': formula_type,
                        'word_problem_variant': variant
                    }
                )

        else:  # Default fallback - simple linear
            a = random.randint(1, 5)
            b = random.randint(-10, 10)
            x = random.randint(min_val, max_val)
            correct_answer = a * x + b
            malrule_answer = a * x
            text = f"Given f(x) = {a}x + {b}, evaluate f({x})"
            problem_type = 'simple_linear'

        # Create metadata for simple_linear (default case)
        metadata = {
            'coefficient': a,
            'constant': b,
            'input': x,
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer,
            'problem_type': problem_type
        }

        return Problem(
            text=text,
            operands=[a, b, x],
            operation='function_evaluation',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )
