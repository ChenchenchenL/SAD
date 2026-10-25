"""
Problem generator for Diff-0-N=0 malrule.

Generates subtraction problems where the minuend has a 0 digit in a position
where the subtrahend has a non-zero digit, eliciting the 0-N=0 misconception.

Research: Brown & Burton (1978) - Diagnostic models for procedural bugs
in basic mathematical skills. Cognitive Science, 2(2), 155-192.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import random
from typing import Dict, Tuple, Optional, List
from utils import ProblemGenerator, Problem, DifficultyLevel


class Diff0NEquals0ProblemGenerator(ProblemGenerator):
    """
    Generates subtraction problems with zeros in minuend positions.

    Creates problems where the minuend has zero digit(s) in positions
    where the subtrahend has non-zero digits, potentially triggering
    the 0-N=0 error.

    Templates:
    1. basic_zero_in_ones - Zero in ones place (paper example: 140 - 21)
    2. zero_in_tens - Zero in tens place (e.g., 305 - 147)
    3. multiple_zeros - Multiple columns with zeros
    4. word_problem - Real-world contexts
    5. three_digit - Three-digit problems with zero
    """

    def get_name(self) -> str:
        return "Diff-0-N=0 Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates subtraction problems with zero in minuend positions "
            "to elicit the 0-N=0 misconception where students write 0 "
            "instead of borrowing when the top digit is 0."
        )

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_zero_in_ones',
            'zero_in_tens',
            'multiple_zeros',
            'word_problem',
            'three_digit'
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level."""
        ranges = {
            2: {
                DifficultyLevel.EASY: (100, 500),
                DifficultyLevel.MEDIUM: (100, 900),
                DifficultyLevel.HARD: (100, 999),
            },
            3: {
                DifficultyLevel.EASY: (100, 900),
                DifficultyLevel.MEDIUM: (100, 9999),
                DifficultyLevel.HARD: (1000, 9999),
            },
            4: {
                DifficultyLevel.EASY: (100, 9999),
                DifficultyLevel.MEDIUM: (1000, 99999),
                DifficultyLevel.HARD: (10000, 99999),
            }
        }

        lvl = self.level if self.level in ranges else 3
        return {'minuend': ranges[lvl][self.difficulty]}

    def _calculate_correct_answer(self, minuend: int, subtrahend: int) -> int:
        """Calculate the correct answer for a subtraction problem."""
        return minuend - subtrahend

    def _calculate_malrule_answer(self, minuend: int, subtrahend: int) -> int:
        """
        Calculate the malrule answer for the 0-N=0 bug.

        When the top digit is 0 and bottom digit is N (N > 0),
        the student writes 0 instead of borrowing.
        """
        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend).zfill(len(minuend_str))

        minuend_digits = [int(d) for d in minuend_str]
        subtrahend_digits = [int(d) for d in subtrahend_str]

        result_digits = []
        working_minuend = minuend_digits[:]

        for i in range(len(working_minuend) - 1, -1, -1):
            # MALRULE: If top digit is 0 and bottom digit is non-zero, write 0
            if minuend_digits[i] == 0 and subtrahend_digits[i] > 0:
                result_digits.insert(0, 0)
            elif working_minuend[i] < subtrahend_digits[i]:
                # Need to borrow (do it correctly for non-zero positions)
                if i > 0:
                    borrow_from = i - 1
                    while borrow_from >= 0 and working_minuend[borrow_from] == 0:
                        working_minuend[borrow_from] = 9
                        borrow_from -= 1

                    if borrow_from >= 0:
                        working_minuend[borrow_from] -= 1
                        working_minuend[i] += 10

                digit_result = working_minuend[i] - subtrahend_digits[i]
                result_digits.insert(0, digit_result)
            else:
                digit_result = working_minuend[i] - subtrahend_digits[i]
                result_digits.insert(0, digit_result)

        return int(''.join(map(str, result_digits)))

    def _has_zero_minus_n_opportunity(self, minuend: int, subtrahend: int) -> bool:
        """
        Check if problem has at least one column where minuend digit is 0
        and subtrahend digit is non-zero.
        """
        if minuend <= subtrahend:
            return False

        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend).zfill(len(minuend_str))

        for m_digit, s_digit in zip(minuend_str, subtrahend_str):
            if int(m_digit) == 0 and int(s_digit) > 0:
                return True

        return False

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate a subtraction problem with zero requiring the 0-N=0 situation.

        Args:
            seed: Optional random seed for reproducibility
            template: Optional template name to use

        Returns:
            Problem instance
        """
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            template = random.choice(self.get_available_templates())

        # Generate based on template
        if template == 'basic_zero_in_ones':
            return self._generate_basic_zero_in_ones(seed)
        elif template == 'zero_in_tens':
            return self._generate_zero_in_tens(seed)
        elif template == 'multiple_zeros':
            return self._generate_multiple_zeros(seed)
        elif template == 'word_problem':
            return self._generate_word_problem(seed)
        elif template == 'three_digit':
            return self._generate_three_digit(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_zero_in_ones(self, seed: Optional[int] = None) -> Problem:
        """
        Generate problem with zero in ones place - matching the paper example.

        Example from Brown & Burton (1978): 140 - 21 = 120 (correct: 119)
        Pattern: XY0 - AB where ones place has 0 in minuend
        """
        if seed is not None:
            random.seed(seed)

        # Generate minuend ending in 0
        if self.difficulty == DifficultyLevel.EASY:
            num_digits = 3
        else:
            num_digits = random.choice([3, 4])

        minuend_digits = []

        # First digit: non-zero
        minuend_digits.append(random.randint(1, 9))

        # Middle digits: random
        for _ in range(num_digits - 2):
            minuend_digits.append(random.randint(1, 9))

        # Last digit is 0
        minuend_digits.append(0)

        minuend = int(''.join(map(str, minuend_digits)))

        # Generate subtrahend with non-zero ones digit to force 0-N situation
        subtrahend_digits = []
        for i in range(num_digits):
            if i == num_digits - 1:
                # Ones place: non-zero to trigger 0-N=0
                subtrahend_digits.append(random.randint(1, 9))
            elif i == 0:
                # First digit: smaller than minuend
                subtrahend_digits.append(random.randint(0, max(0, minuend_digits[0] - 1)))
            else:
                subtrahend_digits.append(random.randint(0, 9))

        subtrahend = int(''.join(map(str, subtrahend_digits)))

        # Ensure subtrahend < minuend
        if subtrahend >= minuend:
            subtrahend_digits[0] = 0
            subtrahend = int(''.join(map(str, subtrahend_digits)))

        correct_answer = self._calculate_correct_answer(minuend, subtrahend)
        malrule_answer = self._calculate_malrule_answer(minuend, subtrahend)

        return Problem(
            text=f"Calculate: {minuend} - {subtrahend}",
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'minuend': minuend,
                'subtrahend': subtrahend,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'template': 'basic_zero_in_ones',
                'problem_type': 'basic'
            }
        )

    def _generate_zero_in_tens(self, seed: Optional[int] = None) -> Problem:
        """
        Generate problem with zero in tens place.

        Example: 305 - 147, where tens column has 0-4
        Pattern: X0Y - ABC where tens place has 0 in minuend
        """
        if seed is not None:
            random.seed(seed)

        # Use 3-4 digit numbers
        num_digits = 3 if self.difficulty == DifficultyLevel.EASY else random.choice([3, 4])

        # Generate minuend with 0 in tens position
        minuend_digits = []

        # First digit: non-zero
        minuend_digits.append(random.randint(2, 9))

        # Position for zero (second from right = tens place)
        for i in range(1, num_digits - 1):
            if i == num_digits - 2:  # Tens position
                minuend_digits.append(0)
            else:
                minuend_digits.append(random.randint(1, 9))

        # Ones digit: can be anything
        minuend_digits.append(random.randint(1, 9))

        minuend = int(''.join(map(str, minuend_digits)))

        # Generate subtrahend with non-zero in tens position
        subtrahend_digits = []
        for i in range(num_digits):
            if i == num_digits - 2:  # Tens position
                subtrahend_digits.append(random.randint(1, 9))
            elif i == 0:
                subtrahend_digits.append(random.randint(0, max(0, minuend_digits[0] - 1)))
            else:
                subtrahend_digits.append(random.randint(0, 9))

        subtrahend = int(''.join(map(str, subtrahend_digits)))

        # Ensure subtrahend < minuend
        if subtrahend >= minuend:
            subtrahend_digits[0] = 0
            subtrahend = int(''.join(map(str, subtrahend_digits)))

        correct_answer = self._calculate_correct_answer(minuend, subtrahend)
        malrule_answer = self._calculate_malrule_answer(minuend, subtrahend)

        return Problem(
            text=f"Calculate: {minuend} - {subtrahend}",
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'minuend': minuend,
                'subtrahend': subtrahend,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'template': 'zero_in_tens',
                'problem_type': 'basic'
            }
        )

    def _generate_multiple_zeros(self, seed: Optional[int] = None) -> Problem:
        """
        Generate problem with multiple zeros.

        Example: 4004 - 1567, where multiple 0 positions have non-zero subtrahend digits
        """
        if seed is not None:
            random.seed(seed)

        # Use 4-5 digits for this template
        num_digits = 4 if self.difficulty == DifficultyLevel.EASY else 5

        # Generate minuend with multiple zeros
        minuend_digits = []

        # First digit: non-zero
        minuend_digits.append(random.randint(2, 9))

        # Add at least 2 zeros in different positions
        zero_count = 0
        for i in range(1, num_digits):
            if zero_count < 2 and random.random() < 0.6:
                minuend_digits.append(0)
                zero_count += 1
            else:
                minuend_digits.append(random.randint(1, 9))

        # Ensure we have at least 2 zeros
        if zero_count < 2:
            non_zero_positions = [i for i in range(1, num_digits) if minuend_digits[i] != 0]
            if non_zero_positions:
                position = random.choice(non_zero_positions)
                minuend_digits[position] = 0

        minuend = int(''.join(map(str, minuend_digits)))

        # Generate subtrahend with non-zero at zero positions
        subtrahend_digits = []
        for i in range(num_digits):
            if minuend_digits[i] == 0:
                subtrahend_digits.append(random.randint(1, 9))
            elif i == 0:
                subtrahend_digits.append(random.randint(0, max(0, minuend_digits[0] - 1)))
            else:
                subtrahend_digits.append(random.randint(0, max(0, minuend_digits[i] - 1)))

        subtrahend = int(''.join(map(str, subtrahend_digits)))

        # Ensure subtrahend < minuend
        if subtrahend >= minuend:
            subtrahend_digits[0] = max(1, minuend_digits[0] - 2)
            subtrahend = int(''.join(map(str, subtrahend_digits)))

        correct_answer = self._calculate_correct_answer(minuend, subtrahend)
        malrule_answer = self._calculate_malrule_answer(minuend, subtrahend)

        return Problem(
            text=f"Calculate: {minuend} - {subtrahend}",
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'minuend': minuend,
                'subtrahend': subtrahend,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'template': 'multiple_zeros',
                'problem_type': 'basic'
            }
        )

    def _generate_word_problem(self, seed: Optional[int] = None) -> Problem:
        """
        Generate word problem with zeros.

        Example: "A store had 140 items. 21 were sold. How many remain?"
        """
        if seed is not None:
            random.seed(seed)

        contexts = [
            {
                'type': 'inventory',
                'setup': 'A warehouse had {minuend} boxes in stock. They shipped out {subtrahend} boxes. How many boxes remain?',
            },
            {
                'type': 'money',
                'setup': 'Sarah had ${minuend} in her bank account. She withdrew ${subtrahend}. How much money does she have left?',
            },
            {
                'type': 'distance',
                'setup': 'A hiking trail is {minuend} meters long. After walking {subtrahend} meters, how many meters are left to hike?',
            },
            {
                'type': 'population',
                'setup': 'A town had {minuend} residents. {subtrahend} people moved away. How many residents remain?',
            },
            {
                'type': 'attendance',
                'setup': 'A stadium has {minuend} seats. {subtrahend} seats are occupied. How many seats are empty?',
            }
        ]

        context = random.choice(contexts)

        # Generate minuend with zero(s)
        num_digits = 3 if self.difficulty == DifficultyLevel.EASY else 4

        minuend_digits = []
        minuend_digits.append(random.randint(1, 9))

        # Add at least one zero
        zero_placed = False
        for i in range(1, num_digits):
            if not zero_placed and (i == num_digits - 1 or random.random() < 0.5):
                minuend_digits.append(0)
                zero_placed = True
            else:
                minuend_digits.append(random.randint(1, 9))

        minuend = int(''.join(map(str, minuend_digits)))

        # Generate subtrahend with non-zero at zero position(s)
        subtrahend_digits = []
        for i in range(num_digits):
            if minuend_digits[i] == 0:
                subtrahend_digits.append(random.randint(1, 9))
            elif i == 0:
                subtrahend_digits.append(random.randint(0, max(0, minuend_digits[0] - 1)))
            else:
                subtrahend_digits.append(random.randint(0, max(0, minuend_digits[i] - 1)))

        subtrahend = int(''.join(map(str, subtrahend_digits)))

        # Ensure subtrahend < minuend
        if subtrahend >= minuend:
            subtrahend = minuend // 2

        correct_answer = self._calculate_correct_answer(minuend, subtrahend)
        malrule_answer = self._calculate_malrule_answer(minuend, subtrahend)

        problem_text = context['setup'].format(minuend=minuend, subtrahend=subtrahend)

        return Problem(
            text=problem_text,
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'minuend': minuend,
                'subtrahend': subtrahend,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'template': 'word_problem',
                'problem_type': 'word_problem',
                'context_type': context['type']
            }
        )

    def _generate_three_digit(self, seed: Optional[int] = None) -> Problem:
        """
        Generate three-digit problem with zero.

        Example: 340 - 125 = 220 (malrule) vs 215 (correct)
        """
        if seed is not None:
            random.seed(seed)

        # Generate 3-digit minuend with at least one zero
        minuend_digits = []

        # First digit: non-zero
        minuend_digits.append(random.randint(1, 9))

        # Decide where to place zero
        zero_position = random.choice([1, 2])  # tens or ones

        for i in range(1, 3):
            if i == zero_position:
                minuend_digits.append(0)
            else:
                minuend_digits.append(random.randint(1, 9))

        minuend = int(''.join(map(str, minuend_digits)))

        # Generate subtrahend with non-zero at zero position
        subtrahend_digits = []
        for i in range(3):
            if minuend_digits[i] == 0:
                subtrahend_digits.append(random.randint(1, 9))
            elif i == 0:
                subtrahend_digits.append(random.randint(0, max(0, minuend_digits[0] - 1)))
            else:
                subtrahend_digits.append(random.randint(0, 9))

        subtrahend = int(''.join(map(str, subtrahend_digits)))

        # Ensure subtrahend < minuend
        if subtrahend >= minuend:
            subtrahend_digits[0] = 0
            subtrahend = int(''.join(map(str, subtrahend_digits)))

        correct_answer = self._calculate_correct_answer(minuend, subtrahend)
        malrule_answer = self._calculate_malrule_answer(minuend, subtrahend)

        return Problem(
            text=f"Calculate: {minuend} - {subtrahend}",
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'minuend': minuend,
                'subtrahend': subtrahend,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'template': 'three_digit',
                'problem_type': 'basic'
            }
        )
