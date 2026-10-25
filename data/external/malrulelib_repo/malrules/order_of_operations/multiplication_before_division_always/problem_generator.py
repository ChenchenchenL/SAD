"""
Problem generator for Multiplication-Before-Division-Always malrule.

Generates order of operations problems with multiplication and division
that appear left-to-right.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional
from utils import ProblemGenerator, Problem, DifficultyLevel


class MultiplicationDivisionOrderProblemGenerator(ProblemGenerator):
    """
    Generates order of operations problems to elicit Multiplication-Before-Division-Always.

    Creates expressions with division followed by multiplication where
    following strict "M before D" gives wrong answer.
    """

    def get_name(self) -> str:
        return "Multiplication/Division Order Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates expressions with multiplication and division appearing "
            "left-to-right, where treating 'M before D' as strict rule gives "
            "wrong answer. Example: 6 ÷ 2 × 3"
        )

    def get_available_templates(self) -> list:
        """Return list of available template names."""
        return [
            'basic_expression',
            'word_problem_sharing',
            'word_problem_measurement',
            'word_problem_money',
            'multi_operation_chain'
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level."""
        ranges = {
            6: {
                DifficultyLevel.EASY: (2, 6),
                DifficultyLevel.MEDIUM: (2, 9),
                DifficultyLevel.HARD: (2, 12),
            },
            7: {
                DifficultyLevel.EASY: (2, 10),
                DifficultyLevel.MEDIUM: (2, 15),
                DifficultyLevel.HARD: (2, 20),
            },
            8: {
                DifficultyLevel.EASY: (2, 12),
                DifficultyLevel.MEDIUM: (2, 20),
                DifficultyLevel.HARD: (2, 30),
            },
            9: {
                DifficultyLevel.EASY: (2, 15),
                DifficultyLevel.MEDIUM: (2, 25),
                DifficultyLevel.HARD: (2, 40),
            }
        }

        lvl = self.level if self.level in ranges else 7
        return {'value': ranges[lvl][self.difficulty]}

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate an order of operations problem.

        Args:
            seed: Optional random seed for reproducibility
            template: Optional template name to use

        Returns:
            Problem instance
        """
        if seed is not None:
            random.seed(seed)

        # If template specified, use it; otherwise pick random
        if template:
            if template not in self.get_available_templates():
                raise ValueError(f"Unknown template: {template}")
            template_name = template
        else:
            # For backwards compatibility, randomly select a template
            template_name = random.choice(self.get_available_templates())

        # Call the appropriate template method
        method_name = f'_generate_{template_name}'
        if hasattr(self, method_name):
            return getattr(self, method_name)()
        else:
            raise ValueError(f"Template method {method_name} not found")

    def _generate_basic_expression(self) -> Problem:
        """
        Template 1: Basic numerical expression (a ÷ b × c).

        Simple arithmetic expression with division followed by multiplication.
        Example: 12 ÷ 3 × 4
        Correct: (12 ÷ 3) × 4 = 4 × 4 = 16
        Malrule: 12 ÷ (3 × 4) = 12 ÷ 12 = 1
        """
        min_val, max_val = self.get_value_ranges()['value']

        # Choose b and c first
        b = random.randint(2, 6)
        c = random.randint(2, 6)

        # Choose a to be divisible by b for cleaner arithmetic
        a = b * random.randint(2, min(max_val // b, 10))

        # Create expression
        expression = f"{a} ÷ {b} × {c}"

        # Calculate correct answer (left-to-right)
        correct_answer = (a // b) * c

        # Calculate malrule answer (multiplication first)
        malrule_answer = a // (b * c)

        problem_text = f"Evaluate: {expression}"

        return Problem(
            text=problem_text,
            operands=[a, b, c],
            operation='order_of_operations',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'basic_expression',
                'problem_type': 'div_mult',  # Embed problem type
                'expression': expression,
                'a': a,
                'b': b,
                'c': c,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer)
            }
        )

    def _generate_word_problem_sharing(self) -> Problem:
        """
        Template 2: Word problem about sharing/dividing items.

        Context about dividing items into groups then multiplying.
        Example: "24 cookies divided into 3 groups. Each group size is multiplied by 2."
        Correct: (24 ÷ 3) × 2 = 8 × 2 = 16
        Malrule: 24 ÷ (3 × 2) = 24 ÷ 6 = 4
        """
        # Choose values that work well for sharing contexts
        a = random.choice([12, 18, 24, 30, 36, 48, 60])
        b = random.choice([2, 3, 4, 6])
        c = random.choice([2, 3, 4, 5])

        # Ensure a is divisible by both b and (b*c) for clean arithmetic
        while a % b != 0 or a % (b * c) != 0:
            a = random.choice([12, 18, 24, 30, 36, 48, 60, 72])

        items = random.choice(['cookies', 'candies', 'marbles', 'stickers', 'apples'])

        contexts = [
            f"There are {a} {items} divided into {b} equal groups. Each group size is then multiplied by {c}. How many {items} are in each group now?",
            f"Split {a} {items} into {b} equal piles. Then multiply the size of each pile by {c}. What is the new pile size?",
            f"{a} {items} are shared equally among {b} children. Each child's amount is then multiplied by {c}. How many {items} does each child have?",
        ]
        problem_text = random.choice(contexts)
        expression = f"{a} ÷ {b} × {c}"

        # Calculate correct answer (left-to-right)
        correct_answer = (a // b) * c

        # Calculate malrule answer (multiplication first)
        malrule_answer = a // (b * c)

        return Problem(
            text=problem_text,
            operands=[a, b, c],
            operation='order_of_operations',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_sharing',
                'problem_type': 'div_mult',
                'expression': expression,
                'a': a,
                'b': b,
                'c': c,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'items': items
            }
        )

    def _generate_word_problem_measurement(self) -> Problem:
        """
        Template 3: Word problem about measurements (length, weight, volume).

        Context about dividing measurements then multiplying.
        Example: "A 24 meter rope cut into 3 pieces. Each piece length is multiplied by 4."
        Correct: (24 ÷ 3) × 4 = 8 × 4 = 32 meters
        Malrule: 24 ÷ (3 × 4) = 24 ÷ 12 = 2 meters
        """
        # Choose values that work well for measurement contexts
        a = random.choice([20, 24, 30, 36, 40, 48, 60])
        b = random.choice([2, 3, 4, 5, 6])
        c = random.choice([2, 3, 4])

        # Ensure clean division
        while a % b != 0 or a % (b * c) != 0:
            a = random.choice([20, 24, 30, 36, 40, 48, 60])

        measurement_types = [
            ('meters', 'rope', 'length'),
            ('feet', 'board', 'length'),
            ('inches', 'ribbon', 'length'),
            ('liters', 'juice', 'volume'),
            ('kilograms', 'flour', 'weight'),
        ]
        unit, item, measure = random.choice(measurement_types)

        contexts = [
            f"A {a} {unit} {item} is cut into {b} equal pieces. Each piece's {measure} is then multiplied by {c}. What is {c} times the {measure} of one piece in {unit}?",
            f"Divide {a} {unit} of {item} by {b}, then multiply by {c}. How many {unit}?",
            f"You have {a} {unit} of {item}. Divide by {b}, then multiply by {c}. What's the result in {unit}?",
        ]
        problem_text = random.choice(contexts)
        expression = f"{a} ÷ {b} × {c}"

        # Calculate correct answer (left-to-right)
        correct_answer = (a // b) * c

        # Calculate malrule answer (multiplication first)
        malrule_answer = a // (b * c)

        return Problem(
            text=problem_text,
            operands=[a, b, c],
            operation='order_of_operations',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_measurement',
                'problem_type': 'div_mult',
                'expression': expression,
                'a': a,
                'b': b,
                'c': c,
                'correct_answer': f"{correct_answer} {unit}",
                'malrule_answer': f"{malrule_answer} {unit}",
                'unit': unit,
                'item': item
            }
        )

    def _generate_word_problem_money(self) -> Problem:
        """
        Template 4: Word problem about money/currency.

        Context about dividing money then multiplying.
        Example: "$36 divided among 3 people. Each share is multiplied by 2."
        Correct: ($36 ÷ 3) × 2 = $12 × 2 = $24
        Malrule: $36 ÷ (3 × 2) = $36 ÷ 6 = $6
        """
        # Choose values that work well for money contexts
        a = random.choice([12, 18, 24, 30, 36, 48, 60, 72])
        b = random.choice([2, 3, 4, 6])
        c = random.choice([2, 3, 4, 5])

        # Ensure clean division
        while a % b != 0 or a % (b * c) != 0:
            a = random.choice([12, 18, 24, 30, 36, 48, 60, 72, 90])

        contexts = [
            f"You have ${a}. You divide it equally among {b} friends. Each friend's share is then multiplied by {c}. How much does each friend have?",
            f"${a} is split {b} ways. Each share is then multiplied by {c}. What is each share worth now?",
            f"Divide ${a} equally among {b} people, then multiply each person's amount by {c}. How much does each person get?",
            f"A ${a} prize is divided into {b} equal parts. Each part is then multiplied by {c}. What is the value of each part?",
        ]
        problem_text = random.choice(contexts)
        expression = f"{a} ÷ {b} × {c}"

        # Calculate correct answer (left-to-right)
        correct_answer = (a // b) * c

        # Calculate malrule answer (multiplication first)
        malrule_answer = a // (b * c)

        return Problem(
            text=problem_text,
            operands=[a, b, c],
            operation='order_of_operations',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_money',
                'problem_type': 'div_mult',
                'expression': expression,
                'a': a,
                'b': b,
                'c': c,
                'correct_answer': f"${correct_answer}",
                'malrule_answer': f"${malrule_answer}"
            }
        )

    def _generate_multi_operation_chain(self) -> Problem:
        """
        Template 5: Multi-operation chain with division and multiplication.

        Longer expression with multiple operations in sequence.
        Example: 48 ÷ 4 × 3 ÷ 2
        Correct (left-to-right): (((48 ÷ 4) × 3) ÷ 2) = ((12 × 3) ÷ 2) = (36 ÷ 2) = 18
        Malrule (mult first): 48 ÷ (4 × 3) ÷ 2 = 48 ÷ 12 ÷ 2 = 4 ÷ 2 = 2
        """
        min_val, max_val = self.get_value_ranges()['value']

        # Start with larger value for multi-step
        d1 = random.randint(2, 4)  # First divisor
        m = random.randint(2, 5)   # Multiplier
        d2 = random.randint(2, 3)  # Second divisor

        # Build starting value to ensure clean division throughout
        a = d1 * m * d2 * random.randint(1, 3)

        expression = f"{a} ÷ {d1} × {m} ÷ {d2}"

        # Calculate correct answer (strict left-to-right)
        step1 = a // d1         # First division
        step2 = step1 * m       # Multiplication
        correct_answer = step2 // d2  # Second division

        # Calculate malrule answer (multiplication first)
        # Student does: 48 ÷ (4 × 3) ÷ 2
        intermediate = d1 * m
        step1_mal = a // intermediate
        malrule_answer = step1_mal // d2

        problem_text = f"Evaluate: {expression}"

        return Problem(
            text=problem_text,
            operands=[a, d1, m, d2],
            operation='order_of_operations',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'multi_operation_chain',
                'problem_type': 'div_mult_chain',
                'expression': expression,
                'a': a,
                'b': d1,
                'c': m,
                'd': d2,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer)
            }
        )
