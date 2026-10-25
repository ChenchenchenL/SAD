"""
Problem generator for Always-Borrow-Left malrule.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple
from utils import ProblemGenerator, Problem, DifficultyLevel


class AlwaysBorrowLeftProblemGenerator(ProblemGenerator):
    """Generates subtraction problems where borrowing isn't always needed."""

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        ranges = {
            2: {DifficultyLevel.EASY: (10, 50), DifficultyLevel.MEDIUM: (20, 99), DifficultyLevel.HARD: (50, 200)},
            3: {DifficultyLevel.EASY: (20, 99), DifficultyLevel.MEDIUM: (50, 200), DifficultyLevel.HARD: (100, 500)},
            4: {DifficultyLevel.EASY: (50, 200), DifficultyLevel.MEDIUM: (100, 500), DifficultyLevel.HARD: (200, 999)},
        }
        lvl = self.level if self.level in ranges else 3
        return {'values': ranges[lvl][self.difficulty]}

    def generate(self, seed=None) -> Problem:
        if seed is not None:
            random.seed(seed)

        value_range = self.get_value_ranges()['values']
        min_val, max_val = value_range

        # Choose template
        templates = [
            'two_digit_no_borrow',
            'three_digit_no_borrow',
            'large_digits_no_borrow',
            'multiple_columns_no_borrow',
            'word_problem'
        ]
        template = random.choice(templates)

        if template == 'two_digit_no_borrow':
            # 2-digit where NO column needs borrowing (top >= bottom for all)
            # This ensures malrule (always borrow) produces different answer
            # Pattern: AB - CD where A >= C and B >= D
            tens = random.randint(3, 9)
            ones = random.randint(2, 9)
            minuend = tens * 10 + ones

            # Subtrahend: each digit <= corresponding minuend digit
            sub_tens = random.randint(1, tens)
            sub_ones = random.randint(0, ones)
            subtrahend = sub_tens * 10 + sub_ones

            # Ensure subtrahend is at least 10
            if subtrahend < 10:
                subtrahend = 10
                sub_tens = 1
                sub_ones = 0

            correct_answer = minuend - subtrahend
            problem_text = f"Calculate: {minuend} - {subtrahend}"

            return Problem(
                text=problem_text,
                operands=[minuend, subtrahend],
                operation='subtraction',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'minuend': minuend,
                    'subtrahend': subtrahend,
                    'correct_answer': correct_answer,
                    'needs_borrow': False,
                    'template': template
                }
            )

        elif template == 'three_digit_no_borrow':
            # 3-digit problems where NO borrowing is needed in any column
            # Pattern: abc - def where a≥d, b≥e, c≥f
            hundreds = random.randint(3, 9)
            tens = random.randint(2, 9)
            ones = random.randint(2, 9)
            minuend = hundreds * 100 + tens * 10 + ones

            # Subtrahend: each digit ≤ corresponding minuend digit
            sub_hundreds = random.randint(1, hundreds)
            sub_tens = random.randint(0, tens)
            sub_ones = random.randint(0, ones)
            subtrahend = sub_hundreds * 100 + sub_tens * 10 + sub_ones

            correct_answer = minuend - subtrahend
            problem_text = f"Calculate: {minuend} - {subtrahend}"

            return Problem(
                text=problem_text,
                operands=[minuend, subtrahend],
                operation='subtraction',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'minuend': minuend,
                    'subtrahend': subtrahend,
                    'correct_answer': correct_answer,
                    'needs_borrow': False,
                    'template': template,
                    'num_digits': 3
                }
            )

        elif template == 'large_digits_no_borrow':
            # Problems with large digits (7, 8, 9) that don't need borrowing
            # Pattern: 8X - 5Y or 9X - 4Y where no borrowing needed
            first_digit = random.randint(7, 9)
            second_digit = random.randint(5, 9)
            minuend = first_digit * 10 + second_digit

            # Subtrahend: smaller digits
            sub_first = random.randint(3, first_digit - 1)
            sub_second = random.randint(0, second_digit)
            subtrahend = sub_first * 10 + sub_second

            correct_answer = minuend - subtrahend
            problem_text = f"Calculate: {minuend} - {subtrahend}"

            return Problem(
                text=problem_text,
                operands=[minuend, subtrahend],
                operation='subtraction',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'minuend': minuend,
                    'subtrahend': subtrahend,
                    'correct_answer': correct_answer,
                    'needs_borrow': False,
                    'template': template,
                    'large_digits': True
                }
            )

        elif template == 'multiple_columns_no_borrow':
            # 4-digit problems where NONE of the columns need borrowing
            # Pattern: abcd - efgh where a≥e, b≥f, c≥g, d≥h
            thousands = random.randint(3, 9)
            hundreds = random.randint(2, 9)
            tens = random.randint(2, 9)
            ones = random.randint(2, 9)
            minuend = thousands * 1000 + hundreds * 100 + tens * 10 + ones

            # Each digit of subtrahend ≤ corresponding minuend digit
            sub_thousands = random.randint(1, thousands)
            sub_hundreds = random.randint(0, hundreds)
            sub_tens = random.randint(0, tens)
            sub_ones = random.randint(0, ones)
            subtrahend = sub_thousands * 1000 + sub_hundreds * 100 + sub_tens * 10 + sub_ones

            correct_answer = minuend - subtrahend
            problem_text = f"Calculate: {minuend} - {subtrahend}"

            return Problem(
                text=problem_text,
                operands=[minuend, subtrahend],
                operation='subtraction',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'minuend': minuend,
                    'subtrahend': subtrahend,
                    'correct_answer': correct_answer,
                    'needs_borrow': False,
                    'template': template,
                    'num_digits': 4
                }
            )

        elif template == 'word_problem':
            # Word problems where no borrowing is needed
            contexts = [
                ('money', 'A student has ${minuend} and spends ${subtrahend}. How much is left?'),
                ('distance', 'A journey is {minuend} kilometers. After traveling {subtrahend} kilometers, how far is left?'),
                ('items', 'A store has {minuend} items and sells {subtrahend} items. How many remain?'),
                ('time', 'A task takes {minuend} minutes. After {subtrahend} minutes, how much time is left?')
            ]
            context, problem_template = random.choice(contexts)

            # Generate 2-digit or 3-digit problem with no borrowing needed
            if random.choice([True, False]):
                # 2-digit
                tens = random.randint(5, 9)
                ones = random.randint(3, 9)
                minuend = tens * 10 + ones
                sub_tens = random.randint(1, tens)
                sub_ones = random.randint(0, ones)
                subtrahend = sub_tens * 10 + sub_ones
            else:
                # 3-digit
                hundreds = random.randint(3, 9)
                tens = random.randint(2, 9)
                ones = random.randint(2, 9)
                minuend = hundreds * 100 + tens * 10 + ones
                sub_hundreds = random.randint(1, hundreds)
                sub_tens = random.randint(0, tens)
                sub_ones = random.randint(0, ones)
                subtrahend = sub_hundreds * 100 + sub_tens * 10 + sub_ones

            correct_answer = minuend - subtrahend
            problem_text = problem_template.format(minuend=minuend, subtrahend=subtrahend)

            return Problem(
                text=problem_text,
                operands=[minuend, subtrahend],
                operation='subtraction',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'minuend': minuend,
                    'subtrahend': subtrahend,
                    'correct_answer': correct_answer,
                    'needs_borrow': False,
                    'template': template,
                    'context': context
                }
            )
