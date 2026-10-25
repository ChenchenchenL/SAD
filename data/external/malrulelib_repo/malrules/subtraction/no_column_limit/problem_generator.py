"""
Problem generator for No-Column-Limit malrule.

Generates addition problems where column sums exceed 9, demonstrating
the error where students write full sums instead of carrying.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, List, Optional
from utils import ProblemGenerator, Problem, DifficultyLevel


class NoColumnLimitProblemGenerator(ProblemGenerator):
    """
    Generates addition problems that demonstrate No-Column-Limit error.

    Templates:
    1. basic_two_digit - Original 2-digit + 2-digit with ones regrouping
    2. three_digit - 3-digit + 3-digit showing error across multiple places
    3. multiple_carries - Problems where multiple columns sum > 9
    4. money_context - Dollar amounts requiring regrouping
    5. word_problem - Real-world contexts (students, items, points)
    """

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_two_digit',
            'three_digit',
            'multiple_carries',
            'money_context',
            'word_problem'
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level and difficulty."""
        ranges = {
            2: {
                DifficultyLevel.EASY: {'tens': (1, 4), 'ones': (5, 9)},
                DifficultyLevel.MEDIUM: {'tens': (1, 6), 'ones': (5, 9)},
                DifficultyLevel.HARD: {'tens': (1, 8), 'ones': (6, 9)}
            },
            3: {
                DifficultyLevel.EASY: {'tens': (1, 5), 'ones': (5, 9)},
                DifficultyLevel.MEDIUM: {'tens': (1, 7), 'ones': (5, 9)},
                DifficultyLevel.HARD: {'tens': (1, 9), 'ones': (6, 9)}
            },
            4: {
                DifficultyLevel.EASY: {'tens': (1, 6), 'ones': (5, 9)},
                DifficultyLevel.MEDIUM: {'tens': (1, 8), 'ones': (5, 9)},
                DifficultyLevel.HARD: {'tens': (1, 9), 'ones': (6, 9)}
            }
        }
        lvl = self.level if self.level in ranges else 2
        return ranges[lvl][self.difficulty]

    def generate(self, seed=None, template: Optional[str] = None) -> Problem:
        """
        Generate a problem based on selected template.

        Args:
            seed: Optional random seed for reproducibility
            template: Specific template to use, or None for random selection

        Returns:
            Problem instance
        """
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            template = random.choice(self.get_available_templates())

        # Generate based on template
        if template == 'basic_two_digit':
            return self._generate_basic_two_digit(seed)
        elif template == 'three_digit':
            return self._generate_three_digit(seed)
        elif template == 'multiple_carries':
            return self._generate_multiple_carries(seed)
        elif template == 'money_context':
            return self._generate_money_context(seed)
        elif template == 'word_problem':
            return self._generate_word_problem(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_two_digit(self, seed=None) -> Problem:
        """Generate basic 2-digit + 2-digit with ones regrouping."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        tens_min, tens_max = ranges['tens']
        ones_min, ones_max = ranges['ones']

        # Generate first number
        tens1 = random.randint(tens_min, tens_max)
        ones1 = random.randint(ones_min, ones_max)
        num1 = tens1 * 10 + ones1

        # Generate second number - ensure ones sum to at least 10
        tens2 = random.randint(tens_min, tens_max)

        # Make sure ones1 + ones2 >= 10 to require regrouping
        min_ones2 = max(ones_min, 10 - ones1)
        ones2 = random.randint(min_ones2, ones_max)

        # Ensure ones1 + ones2 >= 10
        attempts = 0
        while ones1 + ones2 < 10 and attempts < 20:
            ones2 = random.randint(ones_min, ones_max)
            attempts += 1

        num2 = tens2 * 10 + ones2

        # Calculate answers
        correct_answer = num1 + num2
        ones_sum = ones1 + ones2
        tens_sum = tens1 + tens2
        malrule_answer = str(tens_sum) + str(ones_sum)  # Concatenate sums

        return Problem(
            text=f"What is {num1} + {num2}?",
            operands=[num1, num2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': num1,
                'num2': num2,
                'tens1': tens1,
                'ones1': ones1,
                'tens2': tens2,
                'ones2': ones2,
                'ones_sum': ones_sum,
                'tens_sum': tens_sum,
                'correct_answer': str(correct_answer),
                'malrule_answer': malrule_answer,
                'template': 'basic_two_digit'
            }
        )

    def _generate_three_digit(self, seed=None) -> Problem:
        """Generate 3-digit + 3-digit showing error across multiple places."""
        if seed is not None:
            random.seed(seed)

        # Generate 3-digit numbers with at least one carry needed
        hundreds1 = random.randint(1, 4)
        tens1 = random.randint(2, 7)
        ones1 = random.randint(5, 9)
        num1 = hundreds1 * 100 + tens1 * 10 + ones1

        hundreds2 = random.randint(1, 3)
        tens2 = random.randint(2, 6)
        # Ensure ones sum >= 10
        ones2 = random.randint(10 - ones1, 9)
        num2 = hundreds2 * 100 + tens2 * 10 + ones2

        # Calculate answers
        correct_answer = num1 + num2
        ones_sum = ones1 + ones2
        tens_sum = tens1 + tens2
        hundreds_sum = hundreds1 + hundreds2

        # Malrule: concatenate all sums
        malrule_answer = str(hundreds_sum) + str(tens_sum) + str(ones_sum)

        return Problem(
            text=f"Calculate: {num1} + {num2}",
            operands=[num1, num2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': num1,
                'num2': num2,
                'hundreds1': hundreds1,
                'tens1': tens1,
                'ones1': ones1,
                'hundreds2': hundreds2,
                'tens2': tens2,
                'ones2': ones2,
                'ones_sum': ones_sum,
                'tens_sum': tens_sum,
                'hundreds_sum': hundreds_sum,
                'correct_answer': str(correct_answer),
                'malrule_answer': malrule_answer,
                'template': 'three_digit'
            }
        )

    def _generate_multiple_carries(self, seed=None) -> Problem:
        """Generate problem where both ones AND tens sums exceed 9."""
        if seed is not None:
            random.seed(seed)

        # Choose numbers where both columns need carrying
        # Ones: must sum >= 10
        ones1 = random.randint(6, 9)
        ones2 = random.randint(10 - ones1, 9)

        # Tens: must sum >= 10 (before any carry)
        tens1 = random.randint(5, 9)
        tens2 = random.randint(10 - tens1, 9)

        num1 = tens1 * 10 + ones1
        num2 = tens2 * 10 + ones2

        # Calculate answers
        correct_answer = num1 + num2
        ones_sum = ones1 + ones2
        tens_sum = tens1 + tens2

        # Malrule: concatenate multi-digit sums
        malrule_answer = str(tens_sum) + str(ones_sum)

        return Problem(
            text=f"Add: {num1} + {num2}",
            operands=[num1, num2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': num1,
                'num2': num2,
                'tens1': tens1,
                'ones1': ones1,
                'tens2': tens2,
                'ones2': ones2,
                'ones_sum': ones_sum,
                'tens_sum': tens_sum,
                'correct_answer': str(correct_answer),
                'malrule_answer': malrule_answer,
                'template': 'multiple_carries'
            }
        )

    def _generate_money_context(self, seed=None) -> Problem:
        """Generate money addition problem."""
        if seed is not None:
            random.seed(seed)

        # Dollar amounts that require regrouping in ones place
        tens1 = random.randint(1, 6)
        ones1 = random.randint(5, 9)
        dollars1 = tens1 * 10 + ones1

        tens2 = random.randint(1, 5)
        ones2 = random.randint(10 - ones1, 9)
        dollars2 = tens2 * 10 + ones2

        # Calculate answers
        correct_answer = dollars1 + dollars2
        ones_sum = ones1 + ones2
        tens_sum = tens1 + tens2
        malrule_answer = str(tens_sum) + str(ones_sum)

        return Problem(
            text=f"You have ${dollars1} and earn ${dollars2} more. How much do you have total?",
            operands=[dollars1, dollars2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': dollars1,
                'num2': dollars2,
                'tens1': tens1,
                'ones1': ones1,
                'tens2': tens2,
                'ones2': ones2,
                'ones_sum': ones_sum,
                'tens_sum': tens_sum,
                'correct_answer': f'${correct_answer}',
                'malrule_answer': f'${malrule_answer}',
                'template': 'money_context'
            }
        )

    def _generate_word_problem(self, seed=None) -> Problem:
        """Generate word problem context."""
        if seed is not None:
            random.seed(seed)

        contexts = [
            ('students', 'There are {n1} students in one class and {n2} in another. How many students total?'),
            ('books', 'A library gets {n1} new books on Monday and {n2} on Tuesday. How many new books total?'),
            ('points', 'You scored {n1} points in the first game and {n2} in the second. What is your total score?'),
            ('marbles', 'Tom has {n1} marbles and gets {n2} more. How many marbles does he have?')
        ]

        context_type, text_template = random.choice(contexts)

        # Generate numbers with regrouping
        tens1 = random.randint(1, 6)
        ones1 = random.randint(5, 9)
        num1 = tens1 * 10 + ones1

        tens2 = random.randint(1, 5)
        ones2 = random.randint(10 - ones1, 9)
        num2 = tens2 * 10 + ones2

        # Calculate answers
        correct_answer = num1 + num2
        ones_sum = ones1 + ones2
        tens_sum = tens1 + tens2
        malrule_answer_num = str(tens_sum) + str(ones_sum)

        return Problem(
            text=text_template.format(n1=num1, n2=num2),
            operands=[num1, num2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': num1,
                'num2': num2,
                'tens1': tens1,
                'ones1': ones1,
                'tens2': tens2,
                'ones2': ones2,
                'ones_sum': ones_sum,
                'tens_sum': tens_sum,
                'correct_answer': f'{correct_answer} {context_type}',
                'malrule_answer': f'{malrule_answer_num} {context_type}',
                'context_type': context_type,
                'template': 'word_problem'
            }
        )
