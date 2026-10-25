"""
Problem generator for Larger-Absolute-Value-Always-Wins malrule.

Generates negative number addition/subtraction problems where
sign determination matters.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple
from utils import ProblemGenerator, Problem, DifficultyLevel


class LargerAbsoluteValueAlwaysWinsProblemGenerator(ProblemGenerator):
    """
    Generates negative number problems for sign determination errors.

    Example: -8 + 3 (answer should be -5, not +5)
    Student thinks: larger absolute value is 8, so answer is negative (correct by chance)
    But: -3 + 8 (answer should be +5)
    Student thinks: larger absolute value is 8, so answer is positive (correct)
    ERROR shows in: 3 + (-8) - should be -5 but student might make error in process
    """

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level and difficulty."""
        ranges = {
            6: {
                DifficultyLevel.EASY: (1, 10),
                DifficultyLevel.MEDIUM: (1, 20),
                DifficultyLevel.HARD: (1, 50),
            },
            7: {
                DifficultyLevel.EASY: (1, 20),
                DifficultyLevel.MEDIUM: (1, 50),
                DifficultyLevel.HARD: (1, 100),
            },
            8: {
                DifficultyLevel.EASY: (1, 50),
                DifficultyLevel.MEDIUM: (1, 100),
                DifficultyLevel.HARD: (1, 500),
            },
            9: {
                DifficultyLevel.EASY: (1, 100),
                DifficultyLevel.MEDIUM: (1, 500),
                DifficultyLevel.HARD: (1, 1000),
            }
        }

        lvl = self.level if self.level in ranges else 7
        return {'operands': ranges[lvl][self.difficulty]}

    def generate(self, seed=None) -> Problem:
        """
        Generate a negative number problem across various operations.

        Focus on cases where malrule would give wrong answer.

        Returns:
            Problem instance with negative numbers
        """
        if seed is not None:
            random.seed(seed)

        value_range = self.get_value_ranges()['operands']
        min_val, max_val = value_range

        # Choose template
        templates = [
            'basic_addition_subtraction',
            'multiplication',
            'division',
            'comparison',
            'word_problem'
        ]
        template = random.choice(templates)

        if template == 'basic_addition_subtraction':
            # Original: addition/subtraction with negative numbers
            # Try up to 100 times to generate a valid problem
            for attempt in range(100):
                # Choose operation
                operation = random.choice(['addition', 'subtraction'])

                # Generate two numbers with different absolute values
                a = random.randint(min_val, max_val)
                b = random.randint(min_val, max_val)

                # Ensure they're different
                while abs(a) == abs(b):
                    b = random.randint(min_val, max_val)

                # Randomly assign signs to create interesting cases
                sign_choice = random.choice([
                    'pos_neg_add', 'neg_pos_add', 'neg_neg_add',
                    'pos_neg_sub', 'neg_pos_sub', 'neg_neg_sub',
                ])

                if sign_choice == 'pos_neg_add':
                    num1, num2 = min(a, b), -max(a, b)
                    op_symbol = '+'
                    correct_answer = num1 + num2
                elif sign_choice == 'neg_pos_add':
                    num1, num2 = -max(a, b), min(a, b)
                    op_symbol = '+'
                    correct_answer = num1 + num2
                elif sign_choice == 'neg_neg_add':
                    num1, num2 = -a, -b
                    op_symbol = '+'
                    correct_answer = num1 + num2
                elif sign_choice == 'pos_neg_sub':
                    num1, num2 = min(a, b), -max(a, b)
                    op_symbol = '-'
                    correct_answer = num1 - num2
                elif sign_choice == 'neg_pos_sub':
                    num1, num2 = -max(a, b), min(a, b)
                    op_symbol = '-'
                    correct_answer = num1 - num2
                else:  # neg_neg_sub
                    num1, num2 = -max(a, b), -min(a, b)
                    op_symbol = '-'
                    correct_answer = num1 - num2

                # Calculate malrule answer to validate it's different
                abs1 = abs(num1)
                abs2 = abs(num2)
                if abs1 > abs2:
                    result_sign = 1 if num1 > 0 else -1
                elif abs2 > abs1:
                    result_sign = 1 if num2 > 0 else -1
                else:
                    result_sign = 1 if num1 > 0 else -1

                if op_symbol == '+':
                    if (num1 > 0 and num2 > 0) or (num1 < 0 and num2 < 0):
                        magnitude = abs1 + abs2
                    else:
                        magnitude = abs(abs1 - abs2)
                else:  # subtraction
                    magnitude = abs(abs1 - abs2)

                malrule_answer = result_sign * magnitude
                if correct_answer != malrule_answer:
                    break

            problem_text = f"Calculate: {num1} {op_symbol} ({num2})" if num2 < 0 else f"Calculate: {num1} {op_symbol} {num2}"

            return Problem(
                text=problem_text,
                operands=[num1, num2],
                operation=operation,
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'num1': num1,
                    'num2': num2,
                    'operation_symbol': op_symbol,
                    'correct_answer': correct_answer,
                    'abs_num1': abs(num1),
                    'abs_num2': abs(num2),
                    'template': template
                }
            )

        elif template == 'multiplication':
            # Multiplication with negative numbers
            # Prefer neg_neg to expose malrule error more clearly
            a = random.randint(min_val, min(max_val, 20))
            b = random.randint(min_val, min(max_val, 20))

            # Prefer neg_neg and cases where positive has larger abs value
            sign_combo = random.choice(['neg_neg', 'neg_neg', 'pos_larger_abs', 'pos_neg'])

            if sign_combo == 'pos_larger_abs':
                # Positive (larger) × negative (smaller)
                # Ensure positive has larger abs value
                # Correct: pos × neg = negative
                # Malrule: positive has larger abs, so result is positive (WRONG!)
                if a > b:
                    num1, num2 = a, -b
                else:
                    num1, num2 = b, -a
            elif sign_combo == 'pos_neg':
                num1, num2 = a, -b
            else:  # neg_neg
                # Both negative
                # Correct: neg × neg = positive
                # Malrule: looks at magnitudes, may get sign wrong
                num1, num2 = -a, -b

            correct_answer = num1 * num2
            problem_text = f"Calculate: ({num1}) × ({num2})"

            return Problem(
                text=problem_text,
                operands=[num1, num2],
                operation='multiplication',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'num1': num1,
                    'num2': num2,
                    'operation_symbol': '×',
                    'correct_answer': correct_answer,
                    'abs_num1': abs(num1),
                    'abs_num2': abs(num2),
                    'template': template
                }
            )

        elif template == 'division':
            # Division with negative numbers
            # Prefer neg_neg and cases where malrule will fail
            b = random.randint(max(2, min_val), min(max_val, 10))
            a = b * random.randint(2, 5)  # Ensure clean division

            # Prefer neg_neg (should be positive, but malrule looks at magnitude)
            # and pos with larger abs value ÷ neg with smaller abs
            sign_combo = random.choice(['neg_neg', 'neg_neg', 'pos_neg_larger_dividend'])

            if sign_combo == 'pos_neg_larger_dividend':
                # Positive (larger) ÷ negative (smaller)
                # Correct: positive ÷ negative = negative
                # Malrule: positive has larger abs, so result is positive (WRONG!)
                num1, num2 = a, -b  # a > b, so |num1| > |num2|
            else:  # neg_neg
                # Both negative
                # Correct: negative ÷ negative = positive
                # Malrule: depends on which has larger abs value
                num1, num2 = -a, -b

            correct_answer = num1 // num2
            problem_text = f"Calculate: ({num1}) ÷ ({num2})"

            return Problem(
                text=problem_text,
                operands=[num1, num2],
                operation='division',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'num1': num1,
                    'num2': num2,
                    'operation_symbol': '÷',
                    'correct_answer': correct_answer,
                    'abs_num1': abs(num1),
                    'abs_num2': abs(num2),
                    'template': template
                }
            )

        elif template == 'comparison':
            # Comparing negative numbers
            # To expose the malrule, we should generate:
            # 1. Both negative (student picks one with smaller abs value - wrong!)
            # 2. Or positive with smaller abs value vs negative with larger abs value

            comparison_type = random.choice(['both_negative', 'pos_smaller_abs'])

            if comparison_type == 'both_negative':
                # Both negative: -5 vs -12
                # Correct: -5 > -12 (closer to zero)
                # Malrule: -12 has larger abs, so picks -12 (WRONG!)
                a = random.randint(min_val, min(max_val, 50))
                b = random.randint(min_val, min(max_val, 50))
                while a == b:
                    b = random.randint(min_val, min(max_val, 50))

                num1, num2 = -a, -b

            else:  # pos_smaller_abs
                # Positive with smaller abs vs negative with larger abs
                # Example: 5 vs -12
                # Correct: 5 > -12 (positive always wins)
                # Malrule: -12 has larger abs, so picks -12 (WRONG!)
                small = random.randint(min_val, min(max_val//2, 20))
                large = random.randint(small + 5, min(max_val, 50))

                # Randomly order them
                if random.choice([True, False]):
                    num1, num2 = small, -large
                else:
                    num1, num2 = -large, small

            problem_text = f"Which is greater: {num1} or {num2}?"

            return Problem(
                text=problem_text,
                operands=[num1, num2],
                operation='comparison',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'num1': num1,
                    'num2': num2,
                    'operation_symbol': 'compare',
                    'correct_answer': max(num1, num2),
                    'abs_num1': abs(num1),
                    'abs_num2': abs(num2),
                    'template': template
                }
            )

        elif template == 'word_problem':
            # Word problems with negative numbers - use subtraction to ensure malrule error
            # Pattern: small positive - large negative = large positive
            # But malrule thinks: large negative's sign wins, so result is negative (WRONG!)

            contexts = [
                'The temperature was {num1}°C. It then dropped by {abs_num2}°C from a baseline. What is the new temperature?',
                'Starting at {num1} meters, you move down {abs_num2} meters from sea level. What is your position?',
                'Your score is {num1}. You avoid losing {abs_num2} points. What is your score?'
            ]
            problem_template = random.choice(contexts)

            # Generate: small positive - large negative
            # This guarantees malrule gives wrong answer
            small = random.randint(min_val, min(max_val, 15))
            large = random.randint(small + 5, min(max_val, 30))  # Ensure large > small

            num1 = small  # Small positive
            num2 = -large  # Large negative
            op_symbol = '-'  # Subtraction

            # Rewrite: small - (-large) = small + large
            correct_answer = num1 - num2  # small + large (positive)

            problem_text = problem_template.format(num1=num1, abs_num2=num2)

            return Problem(
                text=problem_text,
                operands=[num1, num2],
                operation='subtraction',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'num1': num1,
                    'num2': num2,
                    'operation_symbol': op_symbol,
                    'correct_answer': correct_answer,
                    'abs_num1': abs(num1),
                    'abs_num2': abs(num2),
                    'template': template
                }
            )
