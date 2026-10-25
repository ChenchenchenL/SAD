"""
Problem generator for Two-Negatives-Always-Positive malrule.

Generates negative number operations where students incorrectly apply
"two negatives make a positive" from multiplication to other contexts.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional, List
from utils import ProblemGenerator, Problem, DifficultyLevel


class NegativeSubtractionProblemGenerator(ProblemGenerator):
    """
    Generates negative number operation problems.

    Focus on cases where students incorrectly apply the "two negatives make a positive"
    rule from multiplication to subtraction or addition operations.
    """

    def get_name(self) -> str:
        return "Two-Negatives-Always-Positive Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates negative number operation problems where students are likely "
            "to incorrectly apply the multiplication rule (negative × negative = positive) "
            "to other operations like subtraction or addition."
        )

    def get_available_templates(self) -> List[str]:
        """Return list of exactly 5 templates for this malrule."""
        return [
            'basic_subtraction',      # -a - (-b) subtraction problems
            'addition_negatives',      # -a + (-b) addition problems
            'word_problem_temp',       # Temperature context
            'word_problem_money',      # Money/bank account context
            'multi_step'               # Multi-step operations
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level and difficulty."""
        ranges = {
            6: {
                DifficultyLevel.EASY: (1, 10),
                DifficultyLevel.MEDIUM: (5, 20),
                DifficultyLevel.HARD: (10, 50),
            },
            7: {
                DifficultyLevel.EASY: (1, 15),
                DifficultyLevel.MEDIUM: (10, 30),
                DifficultyLevel.HARD: (20, 75),
            },
            8: {
                DifficultyLevel.EASY: (1, 20),
                DifficultyLevel.MEDIUM: (10, 50),
                DifficultyLevel.HARD: (25, 100),
            },
            9: {
                DifficultyLevel.EASY: (5, 25),
                DifficultyLevel.MEDIUM: (15, 60),
                DifficultyLevel.HARD: (30, 150),
            }
        }

        lvl = self.level if self.level in ranges else 7
        return {'operand': ranges[lvl][self.difficulty]}

    def _generate_basic_subtraction(self, seed=None) -> Problem:
        """Generate basic subtraction with negatives: -a - (-b) or a - (-b)"""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['operand']

        # Generate two patterns
        pattern = random.choice(['negative_minus_negative', 'positive_minus_negative'])

        if pattern == 'negative_minus_negative':
            # -a - (-b)
            a = random.randint(min_val, max_val)
            b = random.randint(min_val, max_val)
            num1, num2 = -a, -b

            # Correct: -a - (-b) = -a + b
            correct_answer = num1 - num2

            # Malrule: student thinks two negatives make positive, so -a - (-b) = positive value
            # They might compute abs(a) + abs(b) or similar
            malrule_answer = abs(a) + abs(b)

            problem_text = f"What is {num1} - ({num2})?"

        else:  # positive_minus_negative
            # a - (-b)
            a = random.randint(min_val, max_val)
            b = random.randint(min_val, max_val)
            num1, num2 = a, -b

            # Correct: a - (-b) = a + b
            correct_answer = num1 - num2

            # Malrule: student sees two negatives (minus and negative) and makes it positive
            # They might compute a + b incorrectly or just |a - b|
            malrule_answer = abs(a - b)

            problem_text = f"What is {num1} - ({num2})?"

        return Problem(
            text=problem_text,
            operands=[num1, num2],
            operation='negative_subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'basic_subtraction',
                'pattern': pattern,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'num1': num1,
                'num2': num2
            }
        )

    def _generate_addition_negatives(self, seed=None) -> Problem:
        """Generate addition of two negatives: -a + (-b)"""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['operand']

        a = random.randint(min_val, max_val)
        b = random.randint(min_val, max_val)
        num1, num2 = -a, -b

        # Correct: -a + (-b) = -(a + b)
        correct_answer = num1 + num2

        # Malrule: student thinks two negatives make positive
        # So -a + (-b) becomes positive (a + b)
        malrule_answer = abs(a + b)

        problem_text = f"What is ({num1}) + ({num2})?"

        return Problem(
            text=problem_text,
            operands=[num1, num2],
            operation='negative_addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'addition_negatives',
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'num1': num1,
                'num2': num2
            }
        )

    def _generate_word_problem_temp(self, seed=None) -> Problem:
        """Generate temperature context problems"""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['operand']

        # Pattern: Temperature starts negative, then drops further
        a = random.randint(min_val, max_val)
        b = random.randint(min_val, max_val)
        start_temp = -a
        drop = b

        # Correct: -a - b (temperature gets more negative)
        correct_answer = start_temp - drop

        # Malrule: student sees "negative" and "drop" (subtraction) and makes it positive
        # They might think it becomes positive (a + b) or just get confused
        malrule_answer = abs(a - b) if a > b else abs(b - a)

        contexts = [
            f"The temperature was {start_temp}°C. It dropped by {drop}°C. What is the new temperature?",
            f"At midnight, the temperature was {start_temp}°F. By morning, it decreased by {drop}°F. What is the morning temperature?",
            f"The temperature in a freezer is {start_temp}°C. It drops another {drop}°C. What is the new temperature?",
            f"The outdoor temperature is {start_temp}°F and falls {drop}°F. What is the new temperature?",
        ]

        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[start_temp, drop],
            operation='negative_subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_temp',
                'correct_answer': f'{correct_answer}°',
                'malrule_answer': f'{malrule_answer}°',
                'start_temp': start_temp,
                'change': drop
            }
        )

    def _generate_word_problem_money(self, seed=None) -> Problem:
        """Generate money/bank account context problems"""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['operand']

        # Pattern: Negative balance (debt), then more withdrawal/charge
        a = random.randint(min_val, max_val)
        b = random.randint(min_val, max_val)
        balance = -a
        withdrawal = b

        # Correct: -a - b (debt increases)
        correct_answer = balance - withdrawal

        # Malrule: student might think negative debt and withdrawal make positive
        malrule_answer = abs(a - b) if a > b else (b - a)

        contexts = [
            f"Your bank account has a balance of ${balance}. You withdraw ${withdrawal}. What is your new balance?",
            f"A business has ${balance} (in debt). They spend ${withdrawal} more. What is their new balance?",
            f"Sarah's account shows ${balance}. She makes a ${withdrawal} purchase. What is her new balance?",
            f"The account balance is ${balance}. After a ${withdrawal} fee, what is the balance?",
        ]

        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[balance, withdrawal],
            operation='negative_subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_money',
                'correct_answer': f'${correct_answer}',
                'malrule_answer': f'${malrule_answer}',
                'balance': balance,
                'withdrawal': withdrawal
            }
        )

    def _generate_multi_step(self, seed=None) -> Problem:
        """Generate multi-step operations: -a - (-b) + c"""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['operand']

        a = random.randint(min_val, max_val)
        b = random.randint(min_val, max_val)
        c = random.randint(min_val, max_val)

        num1, num2, num3 = -a, -b, c

        # Correct: -a - (-b) + c = -a + b + c
        correct_answer = num1 - num2 + num3

        # Malrule: student applies "two negatives = positive" incorrectly
        # They might compute: (-a) and (-b) make positive, so (a + b) + c
        malrule_answer = abs(a + b) + c

        problem_texts = [
            f"Calculate: {num1} - ({num2}) + {num3}",
            f"What is {num1} - ({num2}) + {num3}?",
            f"Evaluate: {num1} - ({num2}) + {num3}",
            f"Find the value of {num1} - ({num2}) + {num3}.",
        ]

        problem_text = random.choice(problem_texts)

        return Problem(
            text=problem_text,
            operands=[num1, num2, num3],
            operation='multi_step',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'multi_step',
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'num1': num1,
                'num2': num2,
                'num3': num3
            }
        )

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate a negative number operation problem.

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
        if template == 'basic_subtraction':
            return self._generate_basic_subtraction(seed)
        elif template == 'addition_negatives':
            return self._generate_addition_negatives(seed)
        elif template == 'word_problem_temp':
            return self._generate_word_problem_temp(seed)
        elif template == 'word_problem_money':
            return self._generate_word_problem_money(seed)
        elif template == 'multi_step':
            return self._generate_multi_step(seed)
        else:
            # Fallback to basic_subtraction
            return self._generate_basic_subtraction(seed)
