"""
Problem generator for Stops-Borrow-At-Zero malrule.

Generates subtraction problems where borrowing encounters a zero
and should continue cascading.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple
from utils import ProblemGenerator, Problem, DifficultyLevel


class StopsBorrowAtZeroProblemGenerator(ProblemGenerator):
    """
    Generates subtraction problems requiring borrowing through zero.

    Example: 503 - 285 requires borrowing that encounters zero.
    """

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level and difficulty."""
        ranges = {
            3: {
                DifficultyLevel.EASY: (100, 500),
                DifficultyLevel.MEDIUM: (200, 700),
                DifficultyLevel.HARD: (300, 999),
            },
            4: {
                DifficultyLevel.EASY: (200, 800),
                DifficultyLevel.MEDIUM: (300, 1500),
                DifficultyLevel.HARD: (500, 2999),
            },
            5: {
                DifficultyLevel.EASY: (500, 2000),
                DifficultyLevel.MEDIUM: (1000, 5000),
                DifficultyLevel.HARD: (2000, 9999),
            }
        }

        lvl = self.level if self.level in ranges else 3
        return {'minuend': ranges[lvl][self.difficulty]}

    def generate(self, seed=None) -> Problem:
        """
        Generate a subtraction problem with zero that needs borrowing through.

        Returns:
            Problem instance requiring borrowing through zero
        """
        if seed is not None:
            random.seed(seed)

        value_range = self.get_value_ranges()['minuend']
        min_val, max_val = value_range

        # Choose template
        templates = [
            'single_middle_zero',
            'multiple_consecutive_zeros',
            'zero_near_beginning',
            'large_number_zeros',
            'word_problem'
        ]
        template = random.choice(templates)

        if template == 'single_middle_zero':
            # Original: Generate minuend with single zero in middle
            max_attempts = 1000
            for attempt in range(max_attempts):
                minuend = random.randint(min_val, max_val)
                minuend_str = str(minuend)

                # Check for zero in middle (not first or last)
                has_middle_zero = False
                zero_position = -1
                for i in range(1, len(minuend_str) - 1):
                    if minuend_str[i] == '0':
                        has_middle_zero = True
                        zero_position = i
                        break

                if has_middle_zero:
                    break

            # If not found naturally, construct one
            if not has_middle_zero:
                num_digits = len(str(max_val))
                if num_digits == 3:
                    # Like 503, 604, etc.
                    minuend = random.randint(1, 9) * 100 + random.randint(1, 9)
                else:
                    # For 4+ digits
                    digits = [random.randint(1, 9)]
                    for _ in range(num_digits - 2):
                        digits.append(random.randint(0, 9))
                    zero_idx = random.randint(1, len(digits) - 2)
                    digits[zero_idx] = 0
                    digits.append(random.randint(0, 9))
                    minuend = int(''.join(str(d) for d in digits))

                minuend_str = str(minuend)
                for i in range(1, len(minuend_str) - 1):
                    if minuend_str[i] == '0':
                        zero_position = i
                        break

            # Generate subtrahend that requires borrowing THROUGH the zero
            for attempt in range(max_attempts):
                subtrahend = random.randint(max(10, min_val // 2), minuend - 10)
                subtrahend_str = str(subtrahend).zfill(len(minuend_str))

                # Check if borrowing is needed RIGHT OF the zero position
                if zero_position + 1 < len(minuend_str):
                    position_right_of_zero = zero_position + 1
                    top_digit = int(minuend_str[position_right_of_zero])
                    bottom_digit = int(subtrahend_str[position_right_of_zero])

                    # CRITICAL: borrowing at this position will need to look left and hit zero
                    if top_digit < bottom_digit:
                        break

            # Fallback: construct subtrahend to force borrowing through zero
            if attempt == max_attempts - 1:
                subtrahend_digits = list(str(subtrahend).zfill(len(minuend_str)))

                if zero_position + 1 < len(minuend_str):
                    position_right_of_zero = zero_position + 1
                    top_digit = int(minuend_str[position_right_of_zero])
                    subtrahend_digits[position_right_of_zero] = str(min(9, top_digit + random.randint(1, 3)))

                subtrahend = int(''.join(subtrahend_digits))

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
                    'zero_position': zero_position,
                    'requires_borrow_through_zero': True,
                    'template': template
                }
            )

        elif template == 'multiple_consecutive_zeros':
            # Multiple consecutive zeros (e.g., 5003 - 2567)
            first_digit = random.randint(2, 9)
            last_digit = random.randint(1, 9)
            # Pattern: X00Y where X is first_digit, Y is last_digit
            minuend = first_digit * 1000 + last_digit

            # Subtrahend forces borrowing through both zeros
            subtrahend = random.randint(minuend // 3, minuend - 100)

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
                    'zero_count': 2,
                    'requires_borrow_through_zero': True,
                    'template': template
                }
            )

        elif template == 'zero_near_beginning':
            # Zero in second position (e.g., 503 - 267)
            # Pattern: X0Y where borrowing is needed from the 0
            first_digit = random.randint(2, 9)
            last_digit = random.randint(0, 5)  # Small last digit
            minuend = first_digit * 100 + last_digit  # X0Y pattern (503, 702, etc.)

            # Force borrowing through zero: make ones digit of subtrahend > last_digit
            sub_hundreds = random.randint(1, first_digit - 1)
            sub_tens = random.randint(1, 9)
            sub_ones = random.randint(last_digit + 1, 9)
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
                    'zero_position': 1,
                    'requires_borrow_through_zero': True,
                    'template': template
                }
            )

        elif template == 'large_number_zeros':
            # Large 5-digit numbers with multiple zeros
            # Pattern: X0Y0Z
            first = random.randint(1, 9)
            middle = random.randint(1, 9)
            last = random.randint(1, 9)
            minuend = first * 10000 + middle * 100 + last  # e.g., 50205

            # Subtrahend forces borrowing through zeros
            subtrahend = random.randint(minuend // 2, minuend - 1000)

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
                    'zero_count': 2,
                    'requires_borrow_through_zero': True,
                    'template': template,
                    'num_digits': 5
                }
            )

        elif template == 'word_problem':
            # Word problems with zeros
            contexts = [
                ('inventory', 'A warehouse had {minuend} items. After shipping {subtrahend} items, how many remain?'),
                ('attendance', 'A stadium held {minuend} people. After {subtrahend} people left, how many remained?'),
                ('money', 'A store had ${minuend} in sales. After ${subtrahend} in expenses, what is the profit?'),
                ('distance', 'A road is {minuend} meters long. After paving {subtrahend} meters, how much is left?')
            ]
            context, problem_template = random.choice(contexts)

            # Generate number with zero: X0Y pattern where Y is small
            first_digit = random.randint(3, 9)
            last_digit = random.randint(0, 5)  # Small last digit
            minuend = first_digit * 100 + last_digit  # e.g., 503, 704

            # Force borrowing through zero: ones digit of subtrahend > last_digit
            sub_hundreds = random.randint(1, first_digit - 2)
            sub_tens = random.randint(1, 9)
            sub_ones = random.randint(last_digit + 1, 9)
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
                    'zero_position': 1,
                    'requires_borrow_through_zero': True,
                    'template': template,
                    'context': context
                }
            )
