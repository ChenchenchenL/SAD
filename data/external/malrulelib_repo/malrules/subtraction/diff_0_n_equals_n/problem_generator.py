"""
Problem generator for Diff-0-N=N malrule.

Generates subtraction problems where minuend has zero in position(s)
that need borrowing, eliciting the misconception that 0 - N = N.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional, List
from utils import ProblemGenerator, Problem, DifficultyLevel


class Diff0NEqualsNProblemGenerator(ProblemGenerator):
    """
    Generates subtraction problems with zeros requiring borrowing.

    Creates problems where the minuend has zero digit(s) in positions
    where borrowing is needed, potentially triggering the 0-N=N error.

    Templates:
    1. basic_single_zero - Single zero in middle position (original template)
    2. multiple_zeros - Multiple columns with zeros (e.g., 4004 - 1567)
    3. zero_in_ones_place - Zero in ones place requiring borrow (e.g., 320 - 156)
    4. consecutive_zeros - Consecutive zeros in middle (e.g., 5003 - 2789)
    5. word_problem - Real-world contexts (money, inventory, distance)
    """

    def get_name(self) -> str:
        return "Diff-0-N=N Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates subtraction problems with zero in minuend positions "
            "that require borrowing, to elicit the 0-N=N misconception."
        )

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_single_zero',
            'multiple_zeros',
            'zero_in_ones_place',
            'consecutive_zeros',
            'word_problem'
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

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate a subtraction problem with zero requiring borrowing.

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
        if template == 'basic_single_zero':
            return self._generate_basic_single_zero(seed)
        elif template == 'multiple_zeros':
            return self._generate_multiple_zeros(seed)
        elif template == 'zero_in_ones_place':
            return self._generate_zero_in_ones_place(seed)
        elif template == 'consecutive_zeros':
            return self._generate_consecutive_zeros(seed)
        elif template == 'word_problem':
            return self._generate_word_problem(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_single_zero(self, seed: Optional[int] = None) -> Problem:
        """
        Generate basic single zero problem (original template).

        Example: 305 - 147, 607 - 238

        Pattern: X0Y - ABC where 0 position requires borrowing
        """
        if seed is not None:
            random.seed(seed)

        # Determine number of digits based on difficulty
        if self.difficulty == DifficultyLevel.EASY:
            num_digits = 3
        elif self.difficulty == DifficultyLevel.MEDIUM:
            num_digits = random.choice([3, 4])
        else:  # HARD
            num_digits = random.choice([4, 5])

        # Generate minuend with at least one zero in middle/right positions
        minuend_digits = []

        # First digit: non-zero
        minuend_digits.append(random.randint(1, 9))

        # Middle digits: include at least one zero
        zero_placed = False
        for i in range(1, num_digits - 1):
            if not zero_placed and (i == num_digits - 2 or random.random() < 0.5):
                minuend_digits.append(0)
                zero_placed = True
            else:
                minuend_digits.append(random.randint(0, 9))

        # Last digit
        minuend_digits.append(random.randint(0, 9))

        minuend = int(''.join(map(str, minuend_digits)))

        # Generate subtrahend that requires borrowing at zero position
        subtrahend_digits = []
        for i in range(num_digits):
            if minuend_digits[i] == 0:
                # Put non-zero here to force 0-N situation
                subtrahend_digits.append(random.randint(1, 9))
            elif i == num_digits - 1:
                # Last position: make it larger to trigger borrowing
                if minuend_digits[i] > 0 and minuend_digits[i] < 9:
                    subtrahend_digits.append(random.randint(minuend_digits[i] + 1, 9))
                elif minuend_digits[i] == 9:
                    # Can't be larger than 9, use 9 (still needs borrowing if ones digit is 0)
                    subtrahend_digits.append(9)
                else:
                    subtrahend_digits.append(random.randint(1, 9))
            else:
                # Other positions: random but less than or equal to minuend
                if minuend_digits[i] > 0:
                    subtrahend_digits.append(random.randint(0, minuend_digits[i]))
                else:
                    subtrahend_digits.append(0)

        subtrahend = int(''.join(map(str, subtrahend_digits)))

        # Ensure subtrahend < minuend
        if subtrahend >= minuend:
            subtrahend_digits[0] = max(1, minuend_digits[0] - 1)
            subtrahend = int(''.join(map(str, subtrahend_digits)))

        correct_answer = minuend - subtrahend

        return Problem(
            text=f"Calculate: {minuend} - {subtrahend}",
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'minuend': minuend,
                'subtrahend': subtrahend,
                'answer': correct_answer,
                'template': 'basic_single_zero'
            }
        )

    def _generate_multiple_zeros(self, seed: Optional[int] = None) -> Problem:
        """
        Generate problem with multiple zeros.

        Example: 4004 - 1567, 7002 - 3456

        Pattern: X0Y0Z - ABCDE where multiple 0 positions require borrowing
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
            if zero_count < 2 and random.random() < 0.5:
                minuend_digits.append(0)
                zero_count += 1
            else:
                minuend_digits.append(random.randint(0, 9))

        # Ensure we have at least 2 zeros
        if zero_count < 2:
            # Force a second zero
            position = random.choice([i for i in range(1, num_digits) if minuend_digits[i] != 0])
            minuend_digits[position] = 0

        minuend = int(''.join(map(str, minuend_digits)))

        # Generate subtrahend requiring borrowing at zero positions
        subtrahend_digits = []
        for i in range(num_digits):
            if minuend_digits[i] == 0:
                subtrahend_digits.append(random.randint(1, 9))
            else:
                subtrahend_digits.append(random.randint(0, max(0, minuend_digits[i] - 1)))

        subtrahend = int(''.join(map(str, subtrahend_digits)))

        # Ensure subtrahend < minuend
        if subtrahend >= minuend:
            subtrahend_digits[0] = max(1, minuend_digits[0] - 2)
            subtrahend = int(''.join(map(str, subtrahend_digits)))

        correct_answer = minuend - subtrahend

        return Problem(
            text=f"Calculate: {minuend} - {subtrahend}",
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'minuend': minuend,
                'subtrahend': subtrahend,
                'answer': correct_answer,
                'template': 'multiple_zeros'
            }
        )

    def _generate_zero_in_ones_place(self, seed: Optional[int] = None) -> Problem:
        """
        Generate problem with zero in ones place.

        Example: 320 - 156, 540 - 278

        Pattern: XY0 - ABC where ones place is 0 and requires borrowing
        """
        if seed is not None:
            random.seed(seed)

        # Use 3-4 digits
        num_digits = 3 if self.difficulty == DifficultyLevel.EASY else 4

        # Generate minuend ending in 0
        minuend_digits = []

        # All digits except last
        for i in range(num_digits - 1):
            if i == 0:
                minuend_digits.append(random.randint(2, 9))
            else:
                minuend_digits.append(random.randint(0, 9))

        # Last digit is 0
        minuend_digits.append(0)

        minuend = int(''.join(map(str, minuend_digits)))

        # Generate subtrahend with non-zero in ones place
        subtrahend_digits = []
        for i in range(num_digits):
            if i == num_digits - 1:
                # Ones place: non-zero to force borrowing from 0
                subtrahend_digits.append(random.randint(1, 9))
            else:
                subtrahend_digits.append(random.randint(0, max(0, minuend_digits[i] - 1)))

        subtrahend = int(''.join(map(str, subtrahend_digits)))

        # Ensure subtrahend < minuend
        if subtrahend >= minuend:
            subtrahend_digits[0] = max(1, minuend_digits[0] - 1)
            subtrahend = int(''.join(map(str, subtrahend_digits)))

        correct_answer = minuend - subtrahend

        return Problem(
            text=f"Calculate: {minuend} - {subtrahend}",
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'minuend': minuend,
                'subtrahend': subtrahend,
                'answer': correct_answer,
                'template': 'zero_in_ones_place'
            }
        )

    def _generate_consecutive_zeros(self, seed: Optional[int] = None) -> Problem:
        """
        Generate problem with consecutive zeros.

        Example: 5003 - 2789, 6000 - 2345

        Pattern: X00Y - ABCD where consecutive 0s require borrowing
        """
        if seed is not None:
            random.seed(seed)

        # Use 4-5 digits
        num_digits = 4 if self.difficulty == DifficultyLevel.EASY else 5

        # Generate minuend with consecutive zeros
        minuend_digits = []

        # First digit: non-zero
        minuend_digits.append(random.randint(3, 9))

        # Add 2-3 consecutive zeros
        zero_run = random.randint(2, min(3, num_digits - 2))
        for _ in range(zero_run):
            minuend_digits.append(0)

        # Fill remaining with random digits
        while len(minuend_digits) < num_digits:
            minuend_digits.append(random.randint(0, 9))

        minuend = int(''.join(map(str, minuend_digits)))

        # Generate subtrahend requiring borrowing through consecutive zeros
        subtrahend_digits = []
        for i in range(num_digits):
            if minuend_digits[i] == 0:
                subtrahend_digits.append(random.randint(1, 9))
            else:
                subtrahend_digits.append(random.randint(0, max(0, minuend_digits[i] - 1)))

        subtrahend = int(''.join(map(str, subtrahend_digits)))

        # Ensure subtrahend < minuend
        if subtrahend >= minuend:
            subtrahend_digits[0] = max(1, minuend_digits[0] - 2)
            subtrahend = int(''.join(map(str, subtrahend_digits)))

        correct_answer = minuend - subtrahend

        return Problem(
            text=f"Calculate: {minuend} - {subtrahend}",
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'minuend': minuend,
                'subtrahend': subtrahend,
                'answer': correct_answer,
                'template': 'consecutive_zeros'
            }
        )

    def _generate_word_problem(self, seed: Optional[int] = None) -> Problem:
        """
        Generate word problem with zeros.

        Example: "A store had 405 items. 178 were sold. How many remain?"

        Real-world contexts: money, inventory, distance, population
        """
        if seed is not None:
            random.seed(seed)

        contexts = [
            {
                'type': 'inventory',
                'setup': 'A warehouse had {minuend} boxes in stock. They shipped out {subtrahend} boxes. How many boxes remain?',
                'min_val': 300,
                'max_val': 9999
            },
            {
                'type': 'money',
                'setup': 'Sarah had ${minuend} in her bank account. She withdrew ${subtrahend}. How much money does she have left?',
                'min_val': 300,
                'max_val': 9999
            },
            {
                'type': 'distance',
                'setup': 'A hiking trail is {minuend} meters long. After walking {subtrahend} meters, how many meters are left to hike?',
                'min_val': 400,
                'max_val': 9999
            },
            {
                'type': 'population',
                'setup': 'A town had {minuend} residents. {subtrahend} people moved away. How many residents remain?',
                'min_val': 500,
                'max_val': 9999
            },
            {
                'type': 'attendance',
                'setup': 'A stadium has {minuend} seats. {subtrahend} tickets were sold. How many seats are still available?',
                'min_val': 1000,
                'max_val': 9999
            }
        ]

        context = random.choice(contexts)

        # Generate minuend with zero(s)
        if self.difficulty == DifficultyLevel.EASY:
            num_digits = 3
        else:
            num_digits = 4

        minuend_digits = []
        minuend_digits.append(random.randint(2, 9))

        # Add at least one zero
        zero_placed = False
        for i in range(1, num_digits):
            if not zero_placed and (i == num_digits - 1 or random.random() < 0.6):
                minuend_digits.append(0)
                zero_placed = True
            else:
                minuend_digits.append(random.randint(0, 9))

        minuend = int(''.join(map(str, minuend_digits)))

        # Ensure minuend is in valid range for context
        minuend = max(context['min_val'], min(minuend, context['max_val']))

        # Generate subtrahend requiring borrowing at zero position
        subtrahend_digits = []
        minuend_str = str(minuend)
        minuend_digits_final = [int(d) for d in minuend_str]

        for i in range(len(minuend_digits_final)):
            if minuend_digits_final[i] == 0:
                subtrahend_digits.append(random.randint(1, 9))
            else:
                subtrahend_digits.append(random.randint(0, max(0, minuend_digits_final[i] - 1)))

        subtrahend = int(''.join(map(str, subtrahend_digits)))

        # Ensure subtrahend < minuend
        if subtrahend >= minuend:
            subtrahend = minuend // 2

        correct_answer = minuend - subtrahend

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
                'answer': correct_answer,
                'template': 'word_problem',
                'context_type': context['type']
            }
        )
