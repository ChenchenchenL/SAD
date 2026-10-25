"""
Problem generator for Ignore-Decimal-Point malrule.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple
from utils import ProblemGenerator, Problem, DifficultyLevel


class IgnoreDecimalPointProblemGenerator(ProblemGenerator):
    """
    Generates decimal arithmetic problems to elicit Ignore-Decimal-Point malrule.

    Students ignore decimal points and treat decimal numbers as whole numbers.
    For example: 2.3 × 1.5 becomes 23 × 15 = 345.

    Templates:
    1. basic_multiplication - Simple decimal multiplication
    2. division - Decimal division
    3. scientific_context - Scientific measurements
    4. money_context - Money/shopping problems
    5. measurement_context - Area/measurement problems
    """

    def get_name(self) -> str:
        return "Ignore-Decimal-Point Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates decimal arithmetic problems (multiplication and division) "
            "to elicit the misconception where students ignore decimal points "
            "and treat decimals as whole numbers."
        )

    def get_available_templates(self) -> list:
        """Return list of available problem templates."""
        return [
            'basic_multiplication',
            'division',
            'scientific_context',
            'money_context',
            'measurement_context',
            'word_problem_context'  # NEW: Covers all formula types with variants
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        ranges = {
            4: {DifficultyLevel.EASY: (1, 10), DifficultyLevel.MEDIUM: (1, 50), DifficultyLevel.HARD: (1, 100)},
            5: {DifficultyLevel.EASY: (1, 50), DifficultyLevel.MEDIUM: (1, 100), DifficultyLevel.HARD: (1, 500)},
            6: {DifficultyLevel.EASY: (1, 100), DifficultyLevel.MEDIUM: (1, 500), DifficultyLevel.HARD: (1, 1000)},
        }
        lvl = self.level if self.level in ranges else 5
        return {'values': ranges[lvl][self.difficulty]}

    def generate(self, seed=None, template=None) -> Problem:
        """
        Generate a decimal arithmetic problem based on selected template.

        Args:
            seed: Optional random seed for reproducibility
            template: Specific template to use, or None for random selection

        Returns:
            Problem instance
        """
        if seed is not None:
            random.seed(seed)

        value_range = self.get_value_ranges()['values']
        min_val, max_val = value_range

        # Select template
        if template is None:
            template = random.choice(self.get_available_templates())

        if template == 'basic_multiplication':
            # Original: simple multiplication
            whole1 = random.randint(min_val, max_val // 10)
            decimal1 = random.randint(1, 9)
            num1 = float(f"{whole1}.{decimal1}")

            whole2 = random.randint(min_val, max_val // 10)
            decimal2 = random.randint(1, 9)
            num2 = float(f"{whole2}.{decimal2}")

            correct_answer = num1 * num2
            num1_as_int = int(str(num1).replace('.', ''))
            num2_as_int = int(str(num2).replace('.', ''))
            malrule_answer = num1_as_int * num2_as_int

            problem_text = f"Calculate: {num1} × {num2}"

            return Problem(
                text=problem_text,
                operands=[num1, num2],
                operation='multiplication',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'num1': num1,
                    'num2': num2,
                    'operator': '×',
                    'correct_answer': f'{round(correct_answer, 2)}',
                    'malrule_answer': f'{malrule_answer}',
                    'operation': 'multiplication',
                    'template': template
                }
            )

        elif template == 'division':
            # Division: a.b ÷ c.d
            whole1 = random.randint(2, min(max_val // 10, 20))
            decimal1 = random.randint(1, 9)
            num1 = float(f"{whole1}.{decimal1}")

            whole2 = random.randint(1, min(max_val // 10, 5))
            decimal2 = random.randint(1, 9)
            num2 = float(f"{whole2}.{decimal2}")

            correct_answer = num1 / num2
            num1_as_int = int(str(num1).replace('.', ''))
            num2_as_int = int(str(num2).replace('.', ''))
            malrule_answer = num1_as_int // num2_as_int if num2_as_int != 0 else num1_as_int

            problem_text = f"Calculate: {num1} ÷ {num2}"

            return Problem(
                text=problem_text,
                operands=[num1, num2],
                operation='division',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'num1': num1,
                    'num2': num2,
                    'operator': '÷',
                    'correct_answer': f'{round(correct_answer, 2)}',
                    'malrule_answer': f'{malrule_answer}',
                    'operation': 'division',
                    'template': template
                }
            )

        elif template == 'scientific_context':
            # Scientific context: small numbers multiplication
            # Like wavelengths, measurements, etc.
            whole1 = random.randint(1, 5)
            decimal1 = random.randint(10, 99)
            num1 = float(f"{whole1}.{decimal1}")

            whole2 = random.randint(1, 5)
            decimal2 = random.randint(10, 99)
            num2 = float(f"{whole2}.{decimal2}")

            correct_answer = num1 * num2
            num1_as_int = int(str(num1).replace('.', ''))
            num2_as_int = int(str(num2).replace('.', ''))
            malrule_answer = num1_as_int * num2_as_int

            contexts = [
                ('wavelength', 'micrometers'),
                ('concentration', 'molar'),
                ('time', 'seconds')
            ]
            context, unit = random.choice(contexts)

            problem_text = f"A {context} of {num1} {unit} is multiplied by a factor of {num2}. What is the result?"

            return Problem(
                text=problem_text,
                operands=[num1, num2],
                operation='multiplication',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'num1': num1,
                    'num2': num2,
                    'operator': '×',
                    'correct_answer': f'{round(correct_answer, 2)}',
                    'malrule_answer': f'{malrule_answer}',
                    'operation': 'multiplication',
                    'template': template,
                    'context': context
                }
            )

        elif template == 'money_context':
            # Money: multiplication or division
            op_choice = random.choice(['multiply', 'divide'])

            if op_choice == 'multiply':
                price = random.randint(1, 20) + random.randint(1, 99) / 100
                quantity = random.randint(1, 5) + random.randint(1, 9) / 10

                correct_answer = price * quantity
                num1_as_int = int(str(price).replace('.', ''))
                num2_as_int = int(str(quantity).replace('.', ''))
                malrule_answer = num1_as_int * num2_as_int

                problem_text = f"If one item costs ${price} and you buy {quantity} items, what is the total cost?"

                return Problem(
                    text=problem_text,
                    operands=[price, quantity],
                    operation='multiplication',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'num1': price,
                        'num2': quantity,
                        'operator': '×',
                        'correct_answer': f'${round(correct_answer, 2)}',
                        'malrule_answer': f'{malrule_answer}',
                        'operation': 'multiplication',
                        'template': template,
                        'context': 'money'
                    }
                )
            else:
                total = random.randint(10, 50) + random.randint(1, 99) / 100
                people = random.randint(2, 5) + random.randint(1, 9) / 10

                correct_answer = total / people
                num1_as_int = int(str(total).replace('.', ''))
                num2_as_int = int(str(people).replace('.', ''))
                malrule_answer = num1_as_int // num2_as_int if num2_as_int != 0 else num1_as_int

                problem_text = f"If ${total} is divided equally among {people} people, how much does each person get?"

                return Problem(
                    text=problem_text,
                    operands=[total, people],
                    operation='division',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'num1': total,
                        'num2': people,
                        'operator': '÷',
                        'correct_answer': f'${round(correct_answer, 2)}',
                        'malrule_answer': f'{malrule_answer}',
                        'operation': 'division',
                        'template': template,
                        'context': 'money'
                    }
                )

        elif template == 'measurement_context':
            # Area or volume calculations
            whole1 = random.randint(1, 10)
            decimal1 = random.randint(1, 9)
            num1 = float(f"{whole1}.{decimal1}")

            whole2 = random.randint(1, 10)
            decimal2 = random.randint(1, 9)
            num2 = float(f"{whole2}.{decimal2}")

            correct_answer = num1 * num2
            num1_as_int = int(str(num1).replace('.', ''))
            num2_as_int = int(str(num2).replace('.', ''))
            malrule_answer = num1_as_int * num2_as_int

            problem_text = f"A rectangle has length {num1} meters and width {num2} meters. What is its area?"

            return Problem(
                text=problem_text,
                operands=[num1, num2],
                operation='multiplication',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'num1': num1,
                    'num2': num2,
                    'operator': '×',
                    'correct_answer': f'{round(correct_answer, 2)}',
                    'malrule_answer': f'{malrule_answer}',
                    'operation': 'multiplication',
                    'template': template,
                    'context': 'measurement'
                }
            )

        elif template == 'word_problem_context':
            return self._generate_word_problem_context(seed)

    def _generate_word_problem_context(self, seed=None):
        """Generate word problem covering ALL formula types with 3 variants each."""
        if seed is not None:
            random.seed(seed)

        # Select which formula type to embed
        formula_types = ['multiplication', 'division']
        formula_type = random.choice(formula_types)
        variant = random.randint(0, 2)  # 3 variants per formula type

        if formula_type == 'multiplication':
            # Formula: a.b × c.d
            whole1 = random.randint(1, 10)
            decimal1 = random.randint(1, 9)
            num1 = float(f"{whole1}.{decimal1}")

            whole2 = random.randint(1, 10)
            decimal2 = random.randint(1, 9)
            num2 = float(f"{whole2}.{decimal2}")

            correct_answer = num1 * num2
            num1_as_int = int(str(num1).replace('.', ''))
            num2_as_int = int(str(num2).replace('.', ''))
            malrule_answer = num1_as_int * num2_as_int

            templates = [
                f"A car travels at {num1} km per hour for {num2} hours. What is the total distance traveled?",
                f"A recipe uses {num1} cups of flour per batch. If you make {num2} batches, how much flour is needed?",
                f"A worker earns ${num1} per hour for {num2} hours. What is the total pay?"
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[num1, num2],
                operation='multiplication',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'num1': num1,
                    'num2': num2,
                    'operator': '×',
                    'correct_answer': f'{round(correct_answer, 2)}',
                    'malrule_answer': f'{malrule_answer}',
                    'operation': 'multiplication',
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        else:  # division
            # Formula: a.b ÷ c.d
            whole1 = random.randint(10, 30)
            decimal1 = random.randint(1, 9)
            num1 = float(f"{whole1}.{decimal1}")

            whole2 = random.randint(2, 5)
            decimal2 = random.randint(1, 9)
            num2 = float(f"{whole2}.{decimal2}")

            correct_answer = num1 / num2
            num1_as_int = int(str(num1).replace('.', ''))
            num2_as_int = int(str(num2).replace('.', ''))
            malrule_answer = num1_as_int // num2_as_int if num2_as_int != 0 else num1_as_int

            templates = [
                f"A rope {num1} meters long is cut into pieces of {num2} meters each. How many pieces are there?",
                f"If {num1} liters of juice is divided equally among {num2} containers, how much juice per container?",
                f"A distance of {num1} km is covered in {num2} hours. What is the average speed per hour?"
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[num1, num2],
                operation='division',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'num1': num1,
                    'num2': num2,
                    'operator': '÷',
                    'correct_answer': f'{round(correct_answer, 2)}',
                    'malrule_answer': f'{malrule_answer}',
                    'operation': 'division',
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )
