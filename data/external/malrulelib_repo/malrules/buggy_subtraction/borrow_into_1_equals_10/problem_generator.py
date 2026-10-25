"""
Problem generator for Borrow-Into-1-Equals-10 malrule (BORROW/INTO/1=10).

Generates subtraction problems where borrowing lands on a digit that is 1,
which triggers the malrule where the student gets 10 instead of 11.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import random
from typing import Dict, Tuple, List
from utils import ProblemGenerator, Problem, DifficultyLevel


class BorrowInto1Equals10ProblemGenerator(ProblemGenerator):
    """
    Generates subtraction problems requiring borrowing into a column with ORIGINAL digit 1.

    The malrule only applies when the ORIGINAL digit in the minuend is 1, not when
    a digit becomes 1 due to prior borrows.

    Example: 321 - 89 has ORIGINAL ones digit of 1, which triggers the malrule
    when borrowing is needed (1 < 9, so we borrow, but student gets 10 not 11).
    """

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'ones_digit_is_1',
            'tens_digit_is_1',
            'multiple_1s',
            'word_problem'
        ]

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
        Generate a subtraction problem where ORIGINAL digit 1 needs borrowing.

        Returns:
            Problem instance requiring borrowing into a column with ORIGINAL digit 1
        """
        if seed is not None:
            random.seed(seed)

        templates = self.get_available_templates()
        template = random.choice(templates)

        if template == 'ones_digit_is_1':
            return self._generate_ones_digit_is_1()
        elif template == 'tens_digit_is_1':
            return self._generate_tens_digit_is_1()
        elif template == 'multiple_1s':
            return self._generate_multiple_1s()
        elif template == 'word_problem':
            return self._generate_word_problem()
        else:
            return self._generate_ones_digit_is_1()

    def _generate_ones_digit_is_1(self) -> Problem:
        """
        Generate problem like 321 - 89 where ORIGINAL ones digit is 1.

        Pattern: XY1 - AB where:
        - 1 < B (needs borrow, triggers malrule since original digit is 1)
        """
        max_attempts = 100
        for _ in range(max_attempts):
            # X: hundreds digit (must be >= 1)
            X = random.randint(2, 9)
            # Y: tens digit (must be >= 2 to allow borrow for ones)
            Y = random.randint(2, 9)
            # Z: ones digit is 1 (the trigger for malrule)
            Z = 1

            minuend = X * 100 + Y * 10 + Z

            # A: tens digit of subtrahend
            A = random.randint(0, Y - 2)  # Keep small so tens doesn't need borrow
            # B: ones digit of subtrahend (must be > 1 to need borrow)
            B = random.randint(2, 9)

            subtrahend = A * 10 + B

            if minuend > subtrahend:
                correct_answer = minuend - subtrahend
                malrule_answer = self._calculate_malrule_answer(minuend, subtrahend)

                if correct_answer != malrule_answer:
                    return Problem(
                        text=f"Calculate: {minuend} - {subtrahend}",
                        operands=[minuend, subtrahend],
                        operation='subtraction',
                        level=self.level,
                        difficulty=self.difficulty,
                        metadata={
                            'minuend': minuend,
                            'subtrahend': subtrahend,
                            'correct_answer': correct_answer,
                            'malrule_answer': malrule_answer,
                            'template': 'ones_digit_is_1',
                            'trigger_column': 'ones'
                        }
                    )

        # Fallback to paper example: 321 - 89
        return self._create_paper_example()

    def _generate_tens_digit_is_1(self) -> Problem:
        """
        Generate problem where ORIGINAL tens digit is 1 and needs borrowing.

        Pattern: X1Z - AB where:
        - Z < B (needs borrow from tens)
        - 1 < A (after decrement, tens column needs borrow)
        - The tens column has ORIGINAL digit 1
        """
        max_attempts = 100
        for _ in range(max_attempts):
            # X: hundreds digit (must be >= 2 to allow borrow for tens)
            X = random.randint(2, 9)
            # Y = 1: tens digit is already 1 (the trigger for malrule)
            Y = 1
            # Z: ones digit (small to need borrow)
            Z = random.randint(0, 5)

            minuend = X * 100 + Y * 10 + Z

            # A: tens digit of subtrahend (must be > 0 so after decrement, 1-1=0 < A)
            # Actually we need: after borrow for ones, tens = 1-1 = 0, then 0 < A
            # But wait - the malrule is on ORIGINAL digit, so if original tens is 1
            # and we borrow for ones (1->0), then we need to borrow for tens (0 < A)
            # The malrule won't apply since original digit 0 isn't 1 after decrement
            # Actually the malrule checks original_minuend_digits[i] == 1
            # So if original tens is 1, and we borrow INTO tens (add 10 to tens),
            # the malrule applies only if the ORIGINAL tens is 1
            # But if we need to borrow for ones first (Z < B), tens becomes 0
            # Then we check original_minuend_digits[1] which is still 1!
            # So malrule SHOULD apply

            # Actually looking more carefully: we process right to left
            # For Z < B: we borrow from tens, tens 1->0, ones becomes 11
            # For 0 < A: we need to borrow from hundreds, tens becomes 9
            # When borrowing into tens, original_minuend_digits[i] is checked
            # original_minuend_digits[1] = 1, so malrule applies!
            # Wait no - we're adding 10 to working_minuend[i], not to original
            # The check is: if original_minuend_digits[i] == 1: top_digit = 10
            # So even though working_minuend[i] was 0, if original was 1, malrule fires

            # Hmm, but that seems wrong based on my paper analysis...
            # Let me think again about 321 - 89:
            # Original: [3, 2, 1]
            # i=2 (ones): working[2]=1, original[2]=1, 1 < 9, borrow
            #   borrow_from=1, working[1]=2->1
            #   original[2]=1, so malrule: top_digit=10
            #   10-9=1

            # OK so for this template, we want the ORIGINAL tens digit to be 1
            # and we want borrowing into tens (meaning tens < subtrahend_tens after decrement)
            # If original tens is 1, after ones borrow it becomes 0
            # 0 < A means we need to borrow for tens
            # When we borrow into tens: original[1]=1, so malrule applies

            A = random.randint(1, 9)
            # B: ones digit of subtrahend (must be > Z to trigger first borrow)
            B = random.randint(Z + 1, 9)

            subtrahend = A * 10 + B

            if minuend > subtrahend:
                correct_answer = minuend - subtrahend
                malrule_answer = self._calculate_malrule_answer(minuend, subtrahend)

                if correct_answer != malrule_answer:
                    return Problem(
                        text=f"Calculate: {minuend} - {subtrahend}",
                        operands=[minuend, subtrahend],
                        operation='subtraction',
                        level=self.level,
                        difficulty=self.difficulty,
                        metadata={
                            'minuend': minuend,
                            'subtrahend': subtrahend,
                            'correct_answer': correct_answer,
                            'malrule_answer': malrule_answer,
                            'template': 'tens_digit_is_1',
                            'trigger_column': 'tens'
                        }
                    )

        # Fallback
        return self._create_paper_example()

    def _generate_multiple_1s(self) -> Problem:
        """
        Generate problem with multiple 1s that may trigger the malrule.

        Pattern: X11 - AB or 1Y1 - AB where multiple columns have original 1s.
        """
        max_attempts = 100
        for _ in range(max_attempts):
            # Pattern: X11 (both tens and ones are 1)
            X = random.randint(2, 9)
            minuend = X * 100 + 11  # X11

            # Need borrowing in ones (1 < B)
            A = random.randint(0, 8)
            B = random.randint(2, 9)

            subtrahend = A * 10 + B

            if minuend > subtrahend:
                correct_answer = minuend - subtrahend
                malrule_answer = self._calculate_malrule_answer(minuend, subtrahend)

                if correct_answer != malrule_answer:
                    return Problem(
                        text=f"Calculate: {minuend} - {subtrahend}",
                        operands=[minuend, subtrahend],
                        operation='subtraction',
                        level=self.level,
                        difficulty=self.difficulty,
                        metadata={
                            'minuend': minuend,
                            'subtrahend': subtrahend,
                            'correct_answer': correct_answer,
                            'malrule_answer': malrule_answer,
                            'template': 'multiple_1s',
                            'trigger_columns': 'ones and possibly tens'
                        }
                    )

        # Fallback
        return self._create_paper_example()

    def _generate_word_problem(self) -> Problem:
        """Generate a word problem variant with ORIGINAL digit 1."""
        contexts = [
            ('inventory', 'A warehouse had {minuend} items. After shipping {subtrahend} items, how many remain?'),
            ('attendance', 'A stadium held {minuend} people. After {subtrahend} people left, how many remained?'),
            ('money', 'A store had ${minuend} in sales. After ${subtrahend} in expenses, what is the profit?'),
            ('distance', 'A road is {minuend} meters long. After paving {subtrahend} meters, how much is left?')
        ]
        context, problem_template = random.choice(contexts)

        # Generate numbers that trigger the malrule
        # Use pattern XY1 where ones digit is 1
        X = random.randint(2, 9)
        Y = random.randint(2, 9)
        Z = 1  # ORIGINAL ones digit is 1
        minuend = X * 100 + Y * 10 + Z

        # A: tens digit, keep small so we don't need to borrow for tens
        A = random.randint(0, Y - 2)
        # B: ones digit, must be > 1 to trigger borrow
        B = random.randint(2, 9)
        subtrahend = A * 10 + B

        if minuend <= subtrahend:
            minuend, subtrahend = 321, 89  # fallback to paper example

        correct_answer = minuend - subtrahend
        malrule_answer = self._calculate_malrule_answer(minuend, subtrahend)

        return Problem(
            text=problem_template.format(minuend=minuend, subtrahend=subtrahend),
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'minuend': minuend,
                'subtrahend': subtrahend,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'word_problem',
                'context': context
            }
        )

    def _create_paper_example(self) -> Problem:
        """Create the exact example from Brown & Burton (1978): 321 - 89 = 231."""
        minuend = 321
        subtrahend = 89
        correct_answer = 232
        malrule_answer = 231

        return Problem(
            text=f"Calculate: {minuend} - {subtrahend}",
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'minuend': minuend,
                'subtrahend': subtrahend,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'paper_example',
                'source': 'Brown & Burton (1978)'
            }
        )

    def _calculate_malrule_answer(self, minuend: int, subtrahend: int) -> int:
        """
        Calculate the malrule answer for BORROW/INTO/1=10.

        When borrowing into a column whose ORIGINAL top digit is 1,
        the student gets 10 instead of 11. The malrule only applies
        to digits that were originally 1, not digits that became 1
        due to prior borrow decrements.

        Example: 321 - 89 = 231 (correct: 232)
        - Ones: ORIGINAL digit is 1, MALRULE: 10 - 9 = 1
        - Tens: Original digit was 2, NO malrule: 11 - 8 = 3
        """
        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend).zfill(len(minuend_str))

        # Keep ORIGINAL digits for malrule check
        original_minuend_digits = [int(d) for d in minuend_str]
        subtrahend_digits = [int(d) for d in subtrahend_str]

        working_minuend = original_minuend_digits.copy()
        result_digits = []

        # Process right to left
        for i in range(len(working_minuend) - 1, -1, -1):
            top_digit = working_minuend[i]
            bottom_digit = subtrahend_digits[i]

            if top_digit < bottom_digit:
                # Need to borrow
                if i > 0:
                    # Find column to borrow from
                    borrow_from = i - 1
                    while borrow_from >= 0 and working_minuend[borrow_from] == 0:
                        borrow_from -= 1

                    if borrow_from >= 0:
                        # Perform borrow
                        working_minuend[borrow_from] -= 1

                        # Handle cascade through zeros
                        for j in range(borrow_from + 1, i):
                            working_minuend[j] = 9

                        # MALRULE: Check ORIGINAL digit, not working digit
                        if original_minuend_digits[i] == 1:
                            top_digit = 10  # MALRULE: should be 11
                        else:
                            top_digit += 10  # Normal case

                        working_minuend[i] = top_digit

            digit_result = top_digit - bottom_digit
            result_digits.insert(0, digit_result)

        result_str = ''.join(str(d) for d in result_digits).lstrip('0') or '0'
        return int(result_str)
