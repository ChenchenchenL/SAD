"""
Problem generator for Divide-One-Term-Only malrule.

Generates two-step linear equations where division must be applied
to multiple terms.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional
from utils import ProblemGenerator, Problem, DifficultyLevel


class TwoStepEquationProblemGenerator(ProblemGenerator):
    """
    Generates two-step equation problems to elicit Divide-One-Term-Only.

    Creates equations like ax + b = c where students must divide
    both terms by a.
    """

    def get_name(self) -> str:
        return "Two-Step Equation Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates two-step linear equations (ax + b = c) where students "
            "must divide both terms by the coefficient, eliciting the "
            "Divide-One-Term-Only misconception."
        )

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level."""
        ranges = {
            7: {
                DifficultyLevel.EASY: (1, 10),
                DifficultyLevel.MEDIUM: (1, 20),
                DifficultyLevel.HARD: (1, 30),
            },
            8: {
                DifficultyLevel.EASY: (1, 15),
                DifficultyLevel.MEDIUM: (1, 30),
                DifficultyLevel.HARD: (1, 50),
            },
            9: {
                DifficultyLevel.EASY: (1, 20),
                DifficultyLevel.MEDIUM: (1, 40),
                DifficultyLevel.HARD: (1, 70),
            },
            10: {
                DifficultyLevel.EASY: (1, 30),
                DifficultyLevel.MEDIUM: (1, 60),
                DifficultyLevel.HARD: (1, 100),
            }
        }

        lvl = self.level if self.level in ranges else 7
        return {'value': ranges[lvl][self.difficulty]}

    def generate(self, seed: Optional[int] = None) -> Problem:
        """
        Generate a two-step equation problem.

        Args:
            seed: Optional random seed for reproducibility

        Returns:
            Problem instance
        """
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['value']

        # Choose equation type
        equation_types = ['two_step_addition']  # Basic form: ax + b = c

        # Add enhanced problem types for higher levels
        if self.level >= 8:
            equation_types.extend([
                'three_term_addition',    # ax + b + d = c (3 terms on left)
                'fractional_coefficients', # 0.5x + b = c (decimal coefficients)
                'subtraction_form',        # ax - b = c (subtraction)
                'word_problem_context',    # Real-world contexts
            ])

        equation_type = random.choice(equation_types)

        if equation_type == 'two_step_addition':
            # Basic: ax + b = c
            a = random.randint(2, 5)
            x_value = random.randint(1, max_val)
            b = random.randint(2, max_val)
            c = a * x_value + b
            equation = f"{a}x + {b} = {c}"
            problem_text = f"Solve for x: {equation}"
            metadata = {
                'equation': equation,
                'equation_type': 'two_step_addition',
                'a': a,
                'b': b,
                'c': c,
                'correct_x': x_value
            }

        elif equation_type == 'three_term_addition':
            # ax + b + d = c (three terms on left side)
            a = random.randint(2, 5)
            x_value = random.randint(1, min(max_val, 10))
            b = random.randint(2, 10)
            d = random.randint(2, 10)
            c = a * x_value + b + d
            equation = f"{a}x + {b} + {d} = {c}"
            problem_text = f"Solve for x: {equation}"
            metadata = {
                'equation': equation,
                'equation_type': 'three_term_addition',
                'a': a,
                'b': b,
                'd': d,
                'c': c,
                'correct_x': x_value
            }

        elif equation_type == 'fractional_coefficients':
            # Fractional coefficient: 0.5x + b = c or 1.5x + b = c
            coefficients = [0.5, 1.5, 2.5, 0.25, 0.75]
            a = random.choice(coefficients)
            x_value = random.randint(2, min(max_val, 10))
            b = random.randint(2, 10)
            # Ensure c is reasonable
            c_raw = a * x_value + b
            c = round(c_raw, 2)
            equation = f"{a}x + {b} = {c}"
            problem_text = f"Solve for x: {equation}"
            metadata = {
                'equation': equation,
                'equation_type': 'fractional_coefficients',
                'a': a,
                'b': b,
                'c': c,
                'correct_x': x_value,
                'is_decimal': True
            }

        elif equation_type == 'subtraction_form':
            # ax - b = c (subtraction form)
            a = random.randint(2, 5)
            x_value = random.randint(1, max_val)
            b = random.randint(2, min(max_val, a * x_value))  # Keep result positive
            c = a * x_value - b
            equation = f"{a}x - {b} = {c}"
            problem_text = f"Solve for x: {equation}"
            metadata = {
                'equation': equation,
                'equation_type': 'subtraction_form',
                'a': a,
                'b': b,
                'c': c,
                'correct_x': x_value
            }

        elif equation_type == 'word_problem_context':
            # Real-world word problem covering ALL formula types
            # Each formula type has 3 different contexts

            # Select which formula type to embed
            formula_types = ['two_step_addition', 'three_term_addition', 'subtraction_form', 'fractional_coefficients']
            formula_type = random.choice(formula_types)
            variant = random.randint(0, 2)

            if formula_type == 'two_step_addition':
                # Formula: ax + b = c
                a = random.randint(2, 5)
                x_value = random.randint(2, 10)
                b = random.randint(10, 30)
                c = a * x_value + b

                templates = [
                    f"A car rental costs ${b} plus ${a} per day. If the total cost is ${c}, for how many days (x) was the car rented?",
                    f"A phone plan costs ${b} per month plus ${a} per gigabyte of data. If the total bill is ${c}, how many gigabytes (x) were used?",
                    f"A gym membership costs ${b} to join plus ${a} per month. If the total paid is ${c}, how many months (x) has the membership been active?"
                ]

                problem_text = templates[variant]
                equation = f"{a}x + {b} = {c}"
                metadata = {
                    'equation': equation,
                    'equation_type': 'two_step_addition',
                    'a': a,
                    'b': b,
                    'c': c,
                    'correct_x': x_value,
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }

            elif formula_type == 'three_term_addition':
                # Formula: ax + b + d = c
                a = random.randint(2, 5)
                x_value = random.randint(1, 8)
                b = random.randint(5, 15)
                d = random.randint(5, 15)
                c = a * x_value + b + d

                templates = [
                    f"Sarah buys x books at ${a} each, a notebook for ${b}, and a pen for ${d}. If the total is ${c}, how many books (x) did she buy?",
                    f"A taxi charges ${a} per mile for x miles, ${b} for the base fare, and ${d} for tolls. If the total fare is ${c}, how many miles (x) were traveled?",
                    f"A party costs ${a} per person for x people, ${b} for decorations, and ${d} for the venue. If the total cost is ${c}, how many people (x) attended?"
                ]

                problem_text = templates[variant]
                equation = f"{a}x + {b} + {d} = {c}"
                metadata = {
                    'equation': equation,
                    'equation_type': 'three_term_addition',
                    'a': a,
                    'b': b,
                    'd': d,
                    'c': c,
                    'correct_x': x_value,
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }

            elif formula_type == 'subtraction_form':
                # Formula: ax - b = c
                a = random.randint(2, 5)
                x_value = random.randint(3, 12)
                b = random.randint(5, 20)
                c = a * x_value - b

                templates = [
                    f"A store sells items at ${a} each. After a ${b} discount on the total, the final price is ${c}. How many items (x) were purchased?",
                    f"John earns ${a} per hour for x hours. After deducting ${b} for taxes, he has ${c}. How many hours (x) did he work?",
                    f"A water tank fills at {a} liters per minute for x minutes. After {b} liters leak out, {c} liters remain. How many minutes (x) did it fill?"
                ]

                problem_text = templates[variant]
                equation = f"{a}x - {b} = {c}"
                metadata = {
                    'equation': equation,
                    'equation_type': 'subtraction_form',
                    'a': a,
                    'b': b,
                    'c': c,
                    'correct_x': x_value,
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }

            else:  # fractional_coefficients
                # Formula: (decimal)x + b = c
                coefficients = [0.5, 1.5, 2.5]
                a = random.choice(coefficients)
                x_value = random.randint(4, 12)
                b = random.randint(5, 20)
                c = round(a * x_value + b, 2)

                templates = [
                    f"A recipe uses {a} cups of flour per batch for x batches, plus {b} cups for preparation. If the total flour used is {c} cups, how many batches (x) were made?",
                    f"A medication requires {a} ml per kilogram of body weight for x kilograms, plus {b} ml base dosage. If the total is {c} ml, what is the weight (x) in kg?",
                    f"A paint mixture uses {a} liters of color per gallon for x gallons, plus {b} liters of base. If the total is {c} liters, how many gallons (x) of color were used?"
                ]

                problem_text = templates[variant]
                equation = f"{a}x + {b} = {c}"
                metadata = {
                    'equation': equation,
                    'equation_type': 'fractional_coefficients',
                    'a': a,
                    'b': b,
                    'c': c,
                    'correct_x': x_value,
                    'is_word_problem': True,
                    'is_decimal': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }

        else:  # Fallback
            a = random.randint(2, 5)
            x_value = random.randint(1, max_val)
            b = random.randint(2, max_val)
            c = a * x_value + b
            equation = f"{a}x + {b} = {c}"
            problem_text = f"Solve for x: {equation}"
            metadata = {
                'equation': equation,
                'equation_type': 'two_step_addition',
                'a': a,
                'b': b,
                'c': c,
                'correct_x': x_value
            }

        return Problem(
            text=problem_text,
            operands=[x_value],
            operation='solve_two_step_equation',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )
