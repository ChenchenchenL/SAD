"""
Problem generator for Strict-Left-To-Right malrule.

Generates order of operations problems where students evaluate strictly left-to-right,
ignoring PEMDAS/BODMAS precedence rules.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional, List
from utils import ProblemGenerator, Problem, DifficultyLevel


class OrderOfOperationsProblemGenerator(ProblemGenerator):
    """
    Generates order of operations problems to elicit Strict-Left-To-Right malrule.

    Creates expressions with mixed operations where left-to-right evaluation
    produces a different answer than correct PEMDAS/BODMAS order.
    """

    def get_name(self) -> str:
        return "Strict-Left-To-Right Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates arithmetic expressions with mixed operations that produce "
            "different answers when evaluated left-to-right vs. using correct "
            "order of operations (PEMDAS/BODMAS)."
        )

    def get_available_templates(self) -> List[str]:
        """Return list of exactly 5 templates for this malrule."""
        return [
            'add_mult',        # a + b × c
            'sub_mult',        # a - b × c
            'add_div',         # a + b ÷ c
            'sub_div',         # a - b ÷ c
            'word_problem'     # Real-world context
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level."""
        ranges = {
            5: {
                DifficultyLevel.EASY: (1, 10),
                DifficultyLevel.MEDIUM: (2, 20),
                DifficultyLevel.HARD: (5, 30),
            },
            6: {
                DifficultyLevel.EASY: (2, 15),
                DifficultyLevel.MEDIUM: (5, 25),
                DifficultyLevel.HARD: (10, 40),
            },
            7: {
                DifficultyLevel.EASY: (2, 20),
                DifficultyLevel.MEDIUM: (5, 30),
                DifficultyLevel.HARD: (10, 50),
            },
            8: {
                DifficultyLevel.EASY: (5, 25),
                DifficultyLevel.MEDIUM: (10, 40),
                DifficultyLevel.HARD: (15, 60),
            }
        }

        lvl = self.level if self.level in ranges else 6
        return {'operand': ranges[lvl][self.difficulty]}

    def _generate_add_mult(self, seed=None) -> Problem:
        """Generate addition before multiplication: a + b × c"""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['operand']

        a = random.randint(min_val, max_val)
        b = random.randint(2, 10)
        c = random.randint(2, 10)

        expression = f"{a} + {b} × {c}"

        # Correct: a + (b × c)
        correct_answer = a + (b * c)

        # Malrule: (a + b) × c (left-to-right)
        malrule_answer = (a + b) * c

        problem_texts = [
            f"Evaluate: {expression}",
            f"What is {expression}?",
            f"Calculate: {expression}",
            f"Solve: {expression}"
        ]

        return Problem(
            text=random.choice(problem_texts),
            operands=[a, b, c],
            operation='order_of_operations',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'add_mult',
                'problem_type': 'add_mult',
                'expression': expression,
                'operations': ['+', '×'],
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'a': a, 'b': b, 'c': c
            }
        )

    def _generate_sub_mult(self, seed=None) -> Problem:
        """Generate subtraction before multiplication: a - b × c"""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['operand']

        a = random.randint(min_val, max_val)
        b = random.randint(2, 8)
        c = random.randint(2, 8)

        # Ensure a > b*c for positive correct result
        if a <= b * c:
            a = b * c + random.randint(1, 10)

        expression = f"{a} - {b} × {c}"

        # Correct: a - (b × c)
        correct_answer = a - (b * c)

        # Malrule: (a - b) × c (left-to-right)
        malrule_answer = (a - b) * c

        problem_texts = [
            f"Evaluate: {expression}",
            f"What is {expression}?",
            f"Calculate: {expression}",
            f"Solve: {expression}"
        ]

        return Problem(
            text=random.choice(problem_texts),
            operands=[a, b, c],
            operation='order_of_operations',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'sub_mult',
                'problem_type': 'sub_mult',
                'expression': expression,
                'operations': ['-', '×'],
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'a': a, 'b': b, 'c': c
            }
        )

    def _generate_add_div(self, seed=None) -> Problem:
        """Generate addition before division: a + b ÷ c"""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['operand']

        a = random.randint(min_val, max_val)
        c = random.randint(2, 6)
        b = random.randint(1, 8) * c  # Make b divisible by c

        expression = f"{a} + {b} ÷ {c}"

        # Correct: a + (b ÷ c)
        correct_answer = a + (b // c)

        # Malrule: (a + b) ÷ c (left-to-right)
        malrule_answer = (a + b) // c

        problem_texts = [
            f"Evaluate: {expression}",
            f"What is {expression}?",
            f"Calculate: {expression}",
            f"Solve: {expression}"
        ]

        return Problem(
            text=random.choice(problem_texts),
            operands=[a, b, c],
            operation='order_of_operations',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'add_div',
                'problem_type': 'add_div',
                'expression': expression,
                'operations': ['+', '÷'],
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'a': a, 'b': b, 'c': c
            }
        )

    def _generate_sub_div(self, seed=None) -> Problem:
        """Generate subtraction before division: a - b ÷ c"""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['operand']

        a = random.randint(min_val, max_val)
        c = random.randint(2, 6)
        b = random.randint(1, 8) * c  # Make b divisible by c

        # Ensure a > b/c for positive correct result
        if a <= b // c:
            a = b // c + random.randint(1, 10)

        expression = f"{a} - {b} ÷ {c}"

        # Correct: a - (b ÷ c)
        correct_answer = a - (b // c)

        # Malrule: (a - b) ÷ c (left-to-right)
        # Check if (a - b) is divisible by c, if not adjust
        if (a - b) % c != 0:
            malrule_answer = (a - b) // c  # Integer division
        else:
            malrule_answer = (a - b) // c

        problem_texts = [
            f"Evaluate: {expression}",
            f"What is {expression}?",
            f"Calculate: {expression}",
            f"Solve: {expression}"
        ]

        return Problem(
            text=random.choice(problem_texts),
            operands=[a, b, c],
            operation='order_of_operations',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'sub_div',
                'problem_type': 'sub_div',
                'expression': expression,
                'operations': ['-', '÷'],
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'a': a, 'b': b, 'c': c
            }
        )

    def _generate_word_problem(self, seed=None) -> Problem:
        """Generate word problem requiring order of operations"""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['operand']

        # Scenario patterns: mostly add/sub before mult/div
        scenarios = []

        # Scenario 1: Shopping with multiple items
        base_amount = random.randint(5, 15)
        items_per_pack = random.randint(2, 6)
        num_packs = random.randint(2, 5)
        a, b, c = base_amount, num_packs, items_per_pack
        expression = f"{a} + {b} × {c}"

        correct = a + (b * c)
        malrule = (a + b) * c

        scenarios.append((
            f"Sarah has {a} pencils. She buys {b} packs with {c} pencils each. How many pencils does she have now?",
            expression,
            [a, b, c],
            ['+', '×'],
            correct,
            malrule
        ))

        # Scenario 2: Money problem
        total_money = random.randint(20, 50)
        num_friends = random.randint(2, 5)
        dollars_per_friend = random.randint(2, 8)
        a, b, c = total_money, num_friends, dollars_per_friend

        # Ensure positive result
        if a <= b * c:
            a = b * c + random.randint(5, 15)

        expression = f"{a} - {b} × {c}"

        correct = a - (b * c)
        malrule = (a - b) * c

        scenarios.append((
            f"Marcus has ${a}. He gives {b} friends ${c} each. How much money does he have left?",
            expression,
            [a, b, c],
            ['-', '×'],
            correct,
            malrule
        ))

        # Scenario 3: Division context
        total_items = random.randint(15, 40)
        c = random.randint(2, 5)
        items_to_share = random.randint(2, 8) * c  # Divisible by c
        a, b = total_items, items_to_share

        expression = f"{a} + {b} ÷ {c}"

        correct = a + (b // c)
        malrule = (a + b) // c

        scenarios.append((
            f"A class has {a} books. They receive {b} new books to split among {c} shelves. How many total books are on each shelf if the new books are divided equally?",
            expression,
            [a, b, c],
            ['+', '÷'],
            correct,
            malrule
        ))

        scenario = random.choice(scenarios)
        problem_text = scenario[0]
        expression = scenario[1]
        operands = scenario[2]
        operations = scenario[3]
        correct_answer = scenario[4]
        malrule_answer = scenario[5]

        return Problem(
            text=problem_text,
            operands=operands,
            operation='order_of_operations',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem',
                'problem_type': 'mixed_ops',
                'expression': expression,
                'operations': operations,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'a': operands[0], 'b': operands[1], 'c': operands[2]
            }
        )

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate an order of operations problem.

        Args:
            seed: Optional random seed for reproducibility
            template: Optional template name. If None, random template is chosen.

        Returns:
            Problem instance
        """
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            template = random.choice(self.get_available_templates())

        # Validate template
        if template not in self.get_available_templates():
            raise ValueError(f"Invalid template: {template}")

        # Generate based on template
        if template == 'add_mult':
            return self._generate_add_mult(seed)
        elif template == 'sub_mult':
            return self._generate_sub_mult(seed)
        elif template == 'add_div':
            return self._generate_add_div(seed)
        elif template == 'sub_div':
            return self._generate_sub_div(seed)
        elif template == 'word_problem':
            return self._generate_word_problem(seed)
        else:
            # Fallback to add_mult
            return self._generate_add_mult(seed)
