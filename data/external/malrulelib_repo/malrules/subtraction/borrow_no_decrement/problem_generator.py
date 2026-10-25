"""
Problem generator for Borrow-No-Decrement malrule.

Generates multi-digit subtraction problems that require borrowing.
"""

import random
from typing import Dict, Tuple, Optional
import sys
sys.path.append('/home/user/malrule-coding')

from utils import Problem, ProblemGenerator, DifficultyLevel, create_basic_arithmetic_template


class BorrowNoDecrementProblemGenerator(ProblemGenerator):
    """
    Generates subtraction problems that require borrowing.

    The problems are designed so that the Borrow-No-Decrement malrule
    will produce incorrect answers.
    """

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level and difficulty."""
        ranges = {
            2: {
                DifficultyLevel.EASY: (10, 50),
                DifficultyLevel.MEDIUM: (20, 80),
                DifficultyLevel.HARD: (40, 99),
            },
            3: {
                DifficultyLevel.EASY: (100, 300),
                DifficultyLevel.MEDIUM: (200, 600),
                DifficultyLevel.HARD: (400, 999),
            },
            4: {
                DifficultyLevel.EASY: (100, 500),
                DifficultyLevel.MEDIUM: (500, 2000),
                DifficultyLevel.HARD: (1000, 9999),
            }
        }

        # Default to level 3 if not in ranges
        lvl = self.level if self.level in ranges else 3
        return {'minuend': ranges[lvl][self.difficulty],
                'subtrahend': ranges[lvl][self.difficulty]}

    def _requires_borrowing(self, minuend: int, subtrahend: int) -> bool:
        """
        Check if subtraction requires borrowing.

        Args:
            minuend: Top number
            subtrahend: Bottom number

        Returns:
            True if borrowing is required
        """
        if minuend <= subtrahend:
            return False

        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend).zfill(len(minuend_str))

        # Check if any digit in subtrahend is larger than corresponding minuend digit
        for m_digit, s_digit in zip(minuend_str, subtrahend_str):
            if int(s_digit) > int(m_digit):
                return True

        return False

    def _count_borrows_needed(self, minuend: int, subtrahend: int) -> int:
        """
        Count how many columns require borrowing.

        Args:
            minuend: Top number
            subtrahend: Bottom number

        Returns:
            Number of columns that need borrowing
        """
        if minuend <= subtrahend:
            return 0

        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend).zfill(len(minuend_str))

        borrow_count = 0
        for m_digit, s_digit in zip(minuend_str, subtrahend_str):
            if int(s_digit) > int(m_digit):
                borrow_count += 1

        return borrow_count

    def _generate_problem_text(self, minuend: int, subtrahend: int, problem_type: str) -> str:
        """
        Generate problem text based on problem type.

        Args:
            minuend: Top number
            subtrahend: Bottom number
            problem_type: Type of problem context

        Returns:
            Formatted problem text
        """
        if problem_type == 'basic':
            template = create_basic_arithmetic_template('subtraction')
            return template.generate({'a': minuend, 'b': subtrahend})

        elif problem_type == 'multi_digit_large':
            # 4-5 digit problems with emphasis on larger numbers
            contexts = [
                f"What is {minuend} - {subtrahend}?",
                f"Calculate: {minuend} - {subtrahend}",
                f"Subtract {subtrahend} from {minuend}.",
                f"Find the difference between {minuend} and {subtrahend}.",
            ]
            return random.choice(contexts)

        elif problem_type == 'multiple_borrows':
            # Problems requiring borrowing in multiple columns
            contexts = [
                f"What is {minuend} - {subtrahend}?",
                f"Calculate: {minuend} - {subtrahend}",
                f"Subtract {subtrahend} from {minuend}.",
            ]
            return random.choice(contexts)

        elif problem_type == 'word_problem':
            # Real-world contexts
            if minuend < 100:
                contexts = [
                    f"A library had {minuend} books. After lending out {subtrahend} books, how many remain?",
                    f"Maria collected {minuend} seashells at the beach. She gave {subtrahend} to her friend. How many does she have left?",
                    f"A farmer harvested {minuend} apples. He sold {subtrahend} at the market. How many apples does he have now?",
                    f"There were {minuend} students at school. If {subtrahend} went on a field trip, how many stayed behind?",
                ]
            elif minuend < 1000:
                contexts = [
                    f"A store had {minuend} items in stock. After selling {subtrahend} items, how many remain?",
                    f"A concert venue has {minuend} seats. If {subtrahend} tickets were sold, how many seats are empty?",
                    f"A school has {minuend} students enrolled. If {subtrahend} students graduated, how many students remain?",
                    f"A bakery made {minuend} cookies. After selling {subtrahend} cookies, how many are left?",
                ]
            else:
                contexts = [
                    f"A city's population was {minuend}. After {subtrahend} people moved away, what is the new population?",
                    f"A company had {minuend} employees. After {subtrahend} employees retired, how many remain?",
                    f"An auditorium can hold {minuend} people. If {subtrahend} people left, how many are still there?",
                    f"A charity raised ${minuend}. After spending ${subtrahend} on supplies, how much money remains?",
                ]
            return random.choice(contexts)

        else:
            # Default to basic
            template = create_basic_arithmetic_template('subtraction')
            return template.generate({'a': minuend, 'b': subtrahend})

    def generate(self, seed: Optional[int] = None) -> Problem:
        """
        Generate a subtraction problem requiring borrowing.

        Args:
            seed: Optional random seed for reproducibility

        Returns:
            Problem instance
        """
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['minuend']

        # Choose problem type - weighted to include new templates
        problem_types = ['basic', 'word_problem']

        # Add multi_digit_large for larger numbers (level 4+)
        if self.level >= 4 or max_val >= 1000:
            problem_types.extend(['multi_digit_large', 'multi_digit_large'])  # Add twice for higher weight

        # Add multiple_borrows type
        problem_types.extend(['multiple_borrows'])

        problem_type = random.choice(problem_types)

        # For multi_digit_large, use larger ranges
        if problem_type == 'multi_digit_large':
            min_val = max(min_val, 1000)
            max_val = max(max_val, 9999)
            if max_val > 99999:
                max_val = 99999  # Cap at 5 digits

        # Try to generate a problem requiring borrowing
        max_attempts = 100
        for _ in range(max_attempts):
            minuend = random.randint(min_val, max_val)

            # Subtrahend should be smaller but require borrowing
            subtrahend_min = min_val
            subtrahend_max = minuend - 1

            if subtrahend_max <= subtrahend_min:
                continue

            subtrahend = random.randint(subtrahend_min, subtrahend_max)

            # Check borrowing requirements based on problem type
            requires_borrowing = self._requires_borrowing(minuend, subtrahend)
            borrow_count = self._count_borrows_needed(minuend, subtrahend)

            # For multiple_borrows type, ensure at least 2 borrows
            if problem_type == 'multiple_borrows' and borrow_count < 2:
                continue

            if requires_borrowing:
                # Create problem text based on type
                problem_text = self._generate_problem_text(minuend, subtrahend, problem_type)

                return Problem(
                    text=problem_text,
                    operands=[minuend, subtrahend],
                    operation='subtraction',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'requires_borrowing': True,
                        'borrow_count': borrow_count,
                        'problem_type': problem_type
                    }
                )

        # Fallback: generate any valid subtraction problem
        minuend = random.randint(min_val, max_val)
        subtrahend = random.randint(min_val // 2, minuend - 1)

        problem_text = self._generate_problem_text(minuend, subtrahend, problem_type)

        return Problem(
            text=problem_text,
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'requires_borrowing': self._requires_borrowing(minuend, subtrahend),
                'borrow_count': self._count_borrows_needed(minuend, subtrahend),
                'problem_type': problem_type
            }
        )
