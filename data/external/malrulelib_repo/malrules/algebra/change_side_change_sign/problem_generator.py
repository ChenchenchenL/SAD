"""
Problem generator for Change-Side-Change-Sign malrule.

Generates simple linear equation problems where students need to
move terms across the equals sign.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional
from utils import ProblemGenerator, Problem, DifficultyLevel


class LinearEquationProblemGenerator(ProblemGenerator):
    """
    Generates linear equation problems to elicit Change-Side-Change-Sign.

    Creates simple one-step or two-step equations like:
    - x + 3 = 7
    - x - 5 = 2
    - 2x + 4 = 10
    """

    def get_name(self) -> str:
        return "Linear Equation Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates simple linear equations where students must move terms "
            "across the equals sign, eliciting the Change-Side-Change-Sign misconception."
        )

    def get_templates(self) -> list:
        """
        Get the list of available equation templates.

        Returns:
            List of template names available for generation
        """
        base_templates = ['x_plus_c', 'x_minus_c', 'c_minus_x', 'two_step']

        # Enhanced templates for higher levels
        if self.level >= 8:
            enhanced_templates = [
                'variables_on_both_sides',
                'negative_coefficients',
                'word_problem_context',
                'three_step_equation',
            ]
            return base_templates + enhanced_templates

        return base_templates

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level."""
        ranges = {
            7: {
                DifficultyLevel.EASY: (1, 10),
                DifficultyLevel.MEDIUM: (1, 20),
                DifficultyLevel.HARD: (1, 50),
            },
            8: {
                DifficultyLevel.EASY: (1, 15),
                DifficultyLevel.MEDIUM: (1, 30),
                DifficultyLevel.HARD: (1, 100),
            },
            9: {
                DifficultyLevel.EASY: (1, 20),
                DifficultyLevel.MEDIUM: (1, 50),
                DifficultyLevel.HARD: (1, 150),
            },
            10: {
                DifficultyLevel.EASY: (1, 30),
                DifficultyLevel.MEDIUM: (1, 75),
                DifficultyLevel.HARD: (1, 200),
            }
        }

        lvl = self.level if self.level in ranges else 7
        return {'value': ranges[lvl][self.difficulty]}

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate a linear equation problem.

        Args:
            seed: Optional random seed for reproducibility
            template: Optional template name to use (from get_templates())

        Returns:
            Problem instance
        """
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['value']

        # Choose equation type
        equation_types = ['x_plus_c', 'x_minus_c', 'c_minus_x', 'two_step']

        # Add enhanced problem types for higher levels
        if self.level >= 8:
            equation_types.extend([
                'variables_on_both_sides',    # 2x + 3 = x + 7
                'negative_coefficients',       # -x + 5 = 3 or -2x + 6 = 8
                'word_problem_context',        # Real-world equations
                'three_step_equation',         # 3x + 2 - 5 = 10
            ])

        # If template is specified, use it directly
        if template is not None:
            if template not in equation_types:
                raise ValueError(f"Unknown template '{template}'. Available templates: {equation_types}")
            equation_type = template
        elif self.difficulty == DifficultyLevel.EASY:
            equation_type = random.choice(['x_plus_c', 'x_minus_c'])
        elif self.difficulty == DifficultyLevel.MEDIUM:
            available_types = ['x_plus_c', 'x_minus_c', 'c_minus_x']
            if self.level >= 8:
                available_types.extend(['variables_on_both_sides', 'word_problem_context'])
            equation_type = random.choice(available_types)
        else:
            equation_type = random.choice(equation_types)

        # Generate equation
        if equation_type == 'x_plus_c':
            # x + c = result
            x_value = random.randint(min_val, max_val)
            c = random.randint(min_val, max_val)
            result = x_value + c
            equation = f"x + {c} = {result}"
            operation = '+'

        elif equation_type == 'x_minus_c':
            # x - c = result
            x_value = random.randint(min_val, max_val)
            c = random.randint(min_val, min(x_value, max_val))
            result = x_value - c
            equation = f"x - {c} = {result}"
            operation = '-'

        elif equation_type == 'c_minus_x':
            # c - x = result (less common but important)
            x_value = random.randint(min_val, max_val)
            c = random.randint(x_value, max_val)
            result = c - x_value
            equation = f"{c} - x = {result}"
            operation = '-_reversed'

        elif equation_type == 'two_step':
            # ax + b = c
            a = random.randint(2, 5)
            x_value = random.randint(min_val, max_val)
            b = random.randint(min_val, max_val)
            result = a * x_value + b
            equation = f"{a}x + {b} = {result}"
            operation = 'two_step'

        elif equation_type == 'variables_on_both_sides':
            # ax + b = cx + d where a > c
            x_value = random.randint(1, 15)
            a = random.randint(3, 6)
            c = random.randint(1, a-1)
            b = random.randint(1, 20)
            # Solve: ax + b = cx + d → (a-c)x = d - b → x = (d-b)/(a-c)
            # So d = (a-c)*x + b
            d = (a - c) * x_value + b

            equation = f"{a}x + {b} = {c}x + {d}"
            operation = 'variables_both_sides'

        elif equation_type == 'negative_coefficients':
            # -x + c = result or -ax + b = c
            use_simple = random.choice([True, False])

            if use_simple:
                # -x + c = result
                x_value = random.randint(1, max_val//2)
                c = random.randint(x_value, max_val)
                result = c - x_value
                equation = f"-x + {c} = {result}"
                operation = 'negative_coeff_simple'
            else:
                # -ax + b = c
                a = random.randint(2, 4)
                x_value = random.randint(1, 10)
                b = random.randint(10, 30)
                result = -a * x_value + b
                equation = f"-{a}x + {b} = {result}"
                operation = 'negative_coeff_two_step'

        elif equation_type == 'word_problem_context':
            # Real-world context covering multiple formula types
            # Each formula type has 3 different word problem templates

            # Select which formula type to embed
            formula_types = ['x_plus_c', 'x_minus_c', 'two_step']
            formula_type = random.choice(formula_types)
            variant = random.randint(0, 2)

            if formula_type == 'x_plus_c':
                # Formula: x + c = result
                x_value = random.randint(5, 25)
                c = random.randint(10, 40)
                result = x_value + c

                templates = [
                    f"Maria has some money. After receiving ${c}, she has ${result}. How much money (x) did she have initially?",
                    f"A box contains x apples. After adding {c} more apples, there are {result} apples total. How many apples (x) were initially in the box?",
                    f"The temperature was x degrees. It rose by {c} degrees to reach {result} degrees. What was the initial temperature (x)?"
                ]

                problem_text = templates[variant]
                equation = f"x + {c} = {result}"
                operation = 'word_problem'

            elif formula_type == 'x_minus_c':
                # Formula: x - c = result
                x_value = random.randint(min_val, max_val)
                c = random.randint(min_val, min(x_value, max_val))
                result = x_value - c

                templates = [
                    f"John had x dollars. After spending ${c}, he has ${result} left. How much money (x) did he have initially?",
                    f"A tank had x liters of water. After using {c} liters, {result} liters remain. How many liters (x) were initially in the tank?",
                    f"Sarah had x candies. After giving away {c} candies, she has {result} left. How many candies (x) did she have initially?"
                ]

                problem_text = templates[variant]
                equation = f"x - {c} = {result}"
                operation = 'word_problem'

            else:  # two_step
                # Formula: ax + b = result
                a = random.randint(2, 5)
                x_value = random.randint(min_val, max_val)
                b = random.randint(min_val, max_val)
                result = a * x_value + b

                templates = [
                    f"A taxi charges ${b} initially plus ${a} per mile. If the total fare is ${result}, how many miles (x) were traveled?",
                    f"A phone plan costs ${b} monthly plus ${a} per GB of data. If the bill is ${result}, how many GB (x) were used?",
                    f"Concert tickets cost ${a} each plus a ${b} booking fee. If the total cost is ${result}, how many tickets (x) were purchased?"
                ]

                problem_text = templates[variant]
                equation = f"{a}x + {b} = {result}"
                operation = 'word_problem'

        elif equation_type == 'three_step_equation':
            # 3x + a - b = c or similar
            x_value = random.randint(2, 15)
            coeff = random.randint(2, 5)
            a = random.randint(5, 20)
            b = random.randint(3, a-1)
            # coeff*x + a - b = result
            result = coeff * x_value + a - b

            equation = f"{coeff}x + {a} - {b} = {result}"
            operation = 'three_step'

        else:  # Default fallback
            x_value = random.randint(min_val, max_val)
            c = random.randint(min_val, max_val)
            result = x_value + c
            equation = f"x + {c} = {result}"
            operation = '+'

        # Handle problem text
        if equation_type != 'word_problem_context':
            problem_text = f"Solve for x: {equation}"

        # Build metadata
        metadata = {
            'equation': equation,
            'correct_x': x_value,
            'equation_type': equation_type,
            'operation': operation,
            'problem_type': equation_type
        }

        # Add word problem metadata if applicable
        if equation_type == 'word_problem_context':
            metadata['word_problem_type'] = formula_type
            metadata['word_problem_variant'] = variant

        return Problem(
            text=problem_text,
            operands=[x_value],
            operation='solve_equation',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )
