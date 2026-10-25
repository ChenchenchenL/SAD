"""
Problem generator for Sign-Errors-In-Factoring malrule.

IMPORTANT: The metadata fields 'correct_factored' and 'malrule_factored' are
stored ONLY for validation and testing purposes. The solving algorithms
(correct_algorithm.py and malrule_algorithm.py) MUST NOT use these fields.
They must solve the problem using the coefficients (a, b, c) and parameters
(p, q, k) stored in metadata.
"""

import random
import sys
sys.path.append('/home/user/malrule-coding')

from utils import Problem, ProblemGenerator


class SignErrorsInFactoringProblemGenerator(ProblemGenerator):
    """Generates quadratic factoring problems."""

    def get_value_ranges(self):
        """Return the value ranges for problem generation."""
        return {
            'factor1': (1, 6),
            'factor2': (1, 6),
            'sign_pattern': ['both_positive', 'both_negative', 'one_negative']
        }

    def generate(self, seed=None):
        """
        Generate a quadratic factoring problem.

        Args:
            seed: Optional random seed for reproducibility

        Returns:
            Problem with quadratic to factor
        """
        if seed is not None:
            random.seed(seed)

        # Choose problem type
        problem_types = ['both_positive', 'both_negative', 'one_negative']

        # Add enhanced problem types for higher levels
        if self.level >= 9:
            problem_types.extend([
                'leading_coefficient_not_one',  # 2x² + 7x + 3
                'difference_of_squares',        # x² - k²
                'perfect_square_trinomial',     # x² + 2kx + k²
                'word_problem_context',         # Area/geometry problems
            ])

        problem_type = random.choice(problem_types)

        # Generate two factors for basic types
        p = random.randint(1, 6)
        q = random.randint(1, 6)

        # Handle enhanced problem types first
        if problem_type == 'difference_of_squares':
            # x² - k² = (x - k)(x + k)
            k = random.randint(2, 8)
            quadratic = f"x² - {k**2}"
            correct_factored = f"(x - {k})(x + {k})"
            # Student error: uses both positive (most common error)
            malrule_factored = f"(x + {k})(x + {k})"

            metadata = {
                'quadratic': quadratic,
                'a': 1,
                'b': 0,
                'c': -(k**2),
                'k': k,
                'sign_pattern': problem_type,
                'problem_type': problem_type,
                'correct_factored': correct_factored,
                'malrule_factored': malrule_factored
            }

            return Problem(
                text=f"Factor: {quadratic}",
                operands=[1, 0, -(k**2)],
                operation='factoring',
                level=self.level,
                difficulty=self.difficulty,
                metadata=metadata
            )

        elif problem_type == 'perfect_square_trinomial':
            # x² + 2kx + k² = (x + k)² or x² - 2kx + k² = (x - k)²
            k = random.randint(2, 6)
            positive_pattern = random.choice([True, False])

            if positive_pattern:
                quadratic = f"x² + {2*k}x + {k**2}"
                correct_factored = f"(x + {k})²"
                # Student error: uses wrong sign
                malrule_factored = f"(x - {k})²"
            else:
                quadratic = f"x² - {2*k}x + {k**2}"
                correct_factored = f"(x - {k})²"
                # Student error: uses wrong sign
                malrule_factored = f"(x + {k})²"

            metadata = {
                'quadratic': quadratic,
                'a': 1,
                'b': 2*k if positive_pattern else -2*k,
                'c': k**2,
                'k': k,
                'sign_pattern': problem_type,
                'problem_type': problem_type,
                'correct_factored': correct_factored,
                'malrule_factored': malrule_factored
            }

            return Problem(
                text=f"Factor: {quadratic}",
                operands=[1, 2*k if positive_pattern else -2*k, k**2],
                operation='factoring',
                level=self.level,
                difficulty=self.difficulty,
                metadata=metadata
            )

        elif problem_type == 'leading_coefficient_not_one':
            # ax² + bx + c where a ≠ 1
            # For simplicity: (ax + p)(x + q) = ax² + (aq + p)x + pq
            a = random.choice([2, 3])
            p = random.randint(1, 4)
            q = random.randint(1, 4)

            b = a*q + p
            c = p*q

            quadratic = f"{a}x² + {b}x + {c}"
            correct_factored = f"({a}x + {p})(x + {q})"
            # Student error: gets signs wrong
            malrule_factored = f"({a}x - {p})(x - {q})"

            metadata = {
                'quadratic': quadratic,
                'a': a,
                'b': b,
                'c': c,
                'p': p,
                'q': q,
                'sign_pattern': problem_type,
                'problem_type': problem_type,
                'correct_factored': correct_factored,
                'malrule_factored': malrule_factored
            }

            return Problem(
                text=f"Factor: {quadratic}",
                operands=[a, b, c],
                operation='factoring',
                level=self.level,
                difficulty=self.difficulty,
                metadata=metadata
            )

        elif problem_type == 'word_problem_context':
            # Word problem requiring factoring - covering multiple formula types
            formula_types = ['both_positive', 'both_negative', 'one_negative', 'difference_of_squares', 'perfect_square_trinomial']
            formula_type = random.choice(formula_types)
            variant = random.randint(0, 2)

            if formula_type == 'both_positive':
                p = random.randint(2, 5)
                q = random.randint(2, 5)
                b = p + q
                c = p * q

                contexts = [
                    f"A rectangle has an area of x² + {b}x + {c}. Find expressions for its length and width.",
                    f"The expression x² + {b}x + {c} represents the number of tiles needed for a square patio. Factor this expression to find the dimensions.",
                    f"Factor x² + {b}x + {c} to find dimensions of a garden plot."
                ]

                quadratic = f"x² + {b}x + {c}"
                correct_factored = f"(x + {p})(x + {q})"
                malrule_factored = f"(x - {p})(x - {q})"
                a = 1

            elif formula_type == 'both_negative':
                p = random.randint(2, 5)
                q = random.randint(2, 5)
                b = -(p + q)
                c = p * q

                contexts = [
                    f"A physics model has expression x² - {abs(b)}x + {c}. Factor completely.",
                    f"Factor x² - {abs(b)}x + {c} for an engineering problem.",
                    f"The expression x² - {abs(b)}x + {c} appears in a calculation. Factor it."
                ]

                quadratic = f"x² - {abs(b)}x + {c}"
                correct_factored = f"(x - {p})(x - {q})"
                malrule_factored = f"(x + {p})(x + {q})"
                a = 1

            elif formula_type == 'one_negative':
                p = random.randint(2, 5)
                q = random.randint(2, 5)
                b = p - q
                c = -(p * q)

                b_str = f"+ {b}" if b >= 0 else f"- {abs(b)}"
                contexts = [
                    f"A business model has profit function x² {b_str}x - {abs(c)}. Factor it.",
                    f"Factor the expression x² {b_str}x - {abs(c)} for a projectile problem.",
                    f"The formula x² {b_str}x - {abs(c)} needs factoring. Factor it completely."
                ]

                quadratic = f"x² {b_str}x - {abs(c)}"
                correct_factored = f"(x + {p})(x - {q})"
                malrule_factored = f"(x - {p})(x + {q})"
                a = 1

            elif formula_type == 'difference_of_squares':
                k = random.randint(2, 8)
                contexts = [
                    f"The area difference is x² - {k**2}. Factor completely.",
                    f"Factor x² - {k**2} for a geometry application.",
                    f"The expression x² - {k**2} models a physical quantity. Factor it."
                ]

                quadratic = f"x² - {k**2}"
                correct_factored = f"(x - {k})(x + {k})"
                # Student error: uses both positive (most common error)
                malrule_factored = f"(x + {k})(x + {k})"
                a = 1
                b = 0
                c = -(k**2)
                p = k
                q = k

            else:  # perfect_square_trinomial
                k = random.randint(2, 6)
                positive_pattern = random.choice([True, False])

                if positive_pattern:
                    contexts = [
                        f"A square area is x² + {2*k}x + {k**2}. Factor it.",
                        f"Factor x² + {2*k}x + {k**2} for a design problem.",
                        f"The expression x² + {2*k}x + {k**2} needs factoring. Factor completely."
                    ]
                    quadratic = f"x² + {2*k}x + {k**2}"
                    correct_factored = f"(x + {k})²"
                    malrule_factored = f"(x - {k})²"
                    b = 2*k
                else:
                    contexts = [
                        f"Factor x² - {2*k}x + {k**2} for an application.",
                        f"The expression x² - {2*k}x + {k**2} models a scenario. Factor it.",
                        f"A formula has x² - {2*k}x + {k**2}. Factor completely."
                    ]
                    quadratic = f"x² - {2*k}x + {k**2}"
                    correct_factored = f"(x - {k})²"
                    malrule_factored = f"(x + {k})²"
                    b = -2*k

                a = 1
                c = k**2
                p = k
                q = k

            metadata = {
                'quadratic': quadratic,
                'a': a,
                'b': b,
                'c': c,
                'p': p,
                'q': q,
                'sign_pattern': problem_type,
                'problem_type': problem_type,
                'correct_factored': correct_factored,
                'malrule_factored': malrule_factored,
                'is_word_problem': True,
                'word_problem_type': formula_type,
                'word_problem_variant': variant
            }

            return Problem(
                text=contexts[variant],
                operands=[a, b, c],
                operation='factoring',
                level=self.level,
                difficulty=self.difficulty,
                metadata=metadata
            )

        # Now handle original sign patterns
        sign_pattern = problem_type

        if sign_pattern == 'both_positive':
            # (x + p)(x + q) = x² + (p+q)x + pq
            factor1_sign = '+'
            factor2_sign = '+'
            b = p + q  # coefficient of x
            c = p * q  # constant term
            correct_factored = f"(x + {p})(x + {q})"
            # Student error: uses wrong signs
            malrule_factored = f"(x - {p})(x - {q})"

        elif sign_pattern == 'both_negative':
            # (x - p)(x - q) = x² - (p+q)x + pq
            factor1_sign = '-'
            factor2_sign = '-'
            b = -(p + q)  # coefficient of x (negative)
            c = p * q  # constant term (positive)
            correct_factored = f"(x - {p})(x - {q})"
            # Student error: forgets to make both negative
            malrule_factored = f"(x + {p})(x + {q})"

        else:  # one_negative
            # (x + p)(x - q) = x² + (p-q)x - pq
            factor1_sign = '+'
            factor2_sign = '-'
            b = p - q  # coefficient of x
            c = -(p * q)  # constant term (negative)
            correct_factored = f"(x + {p})(x - {q})"
            # Student error: uses wrong sign combination
            malrule_factored = f"(x - {p})(x + {q})"

        # Build quadratic expression
        if b >= 0:
            if c >= 0:
                quadratic = f"x² + {b}x + {c}"
            else:
                quadratic = f"x² + {b}x - {abs(c)}"
        else:
            if c >= 0:
                quadratic = f"x² - {abs(b)}x + {c}"
            else:
                quadratic = f"x² - {abs(b)}x - {abs(c)}"

        problem_statement = f"Factor: {quadratic}"

        # Create metadata
        metadata = {
            'quadratic': quadratic,
            'a': 1,  # coefficient of x²
            'b': b,  # coefficient of x
            'c': c,  # constant term
            'p': p,
            'q': q,
            'sign_pattern': sign_pattern,
            'problem_type': sign_pattern,
            'correct_factored': correct_factored,
            'malrule_factored': malrule_factored
        }

        return Problem(
            text=problem_statement,
            operands=[1, b, c],
            operation='factoring',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )
