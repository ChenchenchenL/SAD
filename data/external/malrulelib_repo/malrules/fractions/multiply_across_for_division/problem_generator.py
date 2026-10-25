"""
Problem generator for Multiply-Across-For-Division malrule.
"""

import random
import sys
from fractions import Fraction
from typing import Dict, Tuple, Optional, List
sys.path.append('/home/user/malrule-coding')

from utils import Problem, ProblemGenerator, DifficultyLevel


class MultiplyAcrossForDivisionProblemGenerator(ProblemGenerator):
    """
    Generates fraction division problems.

    Templates:
    1. basic_fraction_division - (a/b) ÷ (c/d) standard form
    2. whole_number_divisor - (a/b) ÷ c where c is whole number
    3. whole_number_dividend - a ÷ (b/c) where a is whole number
    4. mixed_numbers - Division with mixed numbers
    5. word_problem - Real-world contexts
    """

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_fraction_division',
            'whole_number_divisor',
            'word_problem_whole_divisor',
            'whole_number_dividend',
            'word_problem_whole_dividend',
            'mixed_numbers',
            'word_problem_mixed',
            'word_problem'
        ]

    def get_value_ranges(self):
        """Return the value ranges for problem generation."""
        if self.difficulty == DifficultyLevel.EASY:
            return {
                'numerator': (1, 6),
                'denominator': (2, 6),
                'whole_number': (2, 8)
            }
        elif self.difficulty == DifficultyLevel.MEDIUM:
            return {
                'numerator': (1, 10),
                'denominator': (2, 10),
                'whole_number': (2, 12)
            }
        else:  # HARD
            return {
                'numerator': (1, 15),
                'denominator': (2, 15),
                'whole_number': (2, 20)
            }

    def generate(self, seed=None, template: Optional[str] = None):
        """
        Generate a fraction division problem.

        Args:
            seed: Optional random seed for reproducibility
            template: Optional template name

        Returns:
            Problem with fraction division
        """
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            template = random.choice(self.get_available_templates())

        # Generate based on template
        if template == 'basic_fraction_division':
            return self._generate_basic_fraction_division(seed)
        elif template == 'whole_number_divisor':
            return self._generate_whole_number_divisor(seed)
        elif template == 'word_problem_whole_divisor':
            return self._generate_word_problem_whole_divisor(seed)
        elif template == 'whole_number_dividend':
            return self._generate_whole_number_dividend(seed)
        elif template == 'word_problem_whole_dividend':
            return self._generate_word_problem_whole_dividend(seed)
        elif template == 'mixed_numbers':
            return self._generate_mixed_numbers(seed)
        elif template == 'word_problem_mixed':
            return self._generate_word_problem_mixed(seed)
        elif template == 'word_problem':
            return self._generate_word_problem(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_fraction_division(self, seed=None) -> Problem:
        """
        Generate basic fraction division problem (original template).

        Example: (3/4) ÷ (2/5)
        Correct: (3/4) × (5/2) = 15/8
        Malrule: (3/4) × (2/5) = 6/20 = 3/10 (forgets to flip)
        """
        if seed is not None:
            random.seed(seed)

        # Get value ranges based on difficulty
        ranges = self.get_value_ranges()

        # Generate first fraction a/b
        a = random.randint(ranges['numerator'][0], ranges['numerator'][1])
        b = random.randint(ranges['denominator'][0], ranges['denominator'][1])

        # Generate second fraction c/d
        c = random.randint(ranges['numerator'][0], ranges['numerator'][1])
        d = random.randint(ranges['denominator'][0], ranges['denominator'][1])

        # Avoid division by zero in malrule
        while c == 0:
            c = random.randint(ranges['numerator'][0], ranges['numerator'][1])

        # Correct: (a/b) ÷ (c/d) = (a/b) × (d/c) = (a×d)/(b×c)
        correct_num = a * d
        correct_den = b * c
        correct_frac = Fraction(correct_num, correct_den)

        # Malrule: (a/b) ÷ (c/d) = (a×c)/(b×d) [forgets to flip]
        malrule_num = a * c
        malrule_den = b * d
        malrule_frac = Fraction(malrule_num, malrule_den)

        problem_statement = f"Divide: ({a}/{b}) ÷ ({c}/{d})"

        metadata = {
            'a': a,
            'b': b,
            'c': c,
            'd': d,
            'correct_numerator': correct_frac.numerator,
            'correct_denominator': correct_frac.denominator,
            'malrule_numerator': malrule_frac.numerator,
            'malrule_denominator': malrule_frac.denominator,
            'correct_answer': f"{correct_frac.numerator}/{correct_frac.denominator}",
            'malrule_answer': f"{malrule_frac.numerator}/{malrule_frac.denominator}",
            'template': 'basic_fraction_division'
        }

        return Problem(
            text=problem_statement,
            operands=[a, b, c, d],
            operation='fraction_division',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_whole_number_divisor(self, seed=None) -> Problem:
        """
        Generate fraction ÷ whole number problem.

        Example: (3/4) ÷ 2
        Correct: (3/4) × (1/2) = 3/8
        Malrule: (3×2)/4 = 6/4 = 3/2 (multiplies instead of flipping to 1/2)
        """
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()

        # Generate fraction a/b
        a = random.randint(ranges['numerator'][0], ranges['numerator'][1])
        b = random.randint(ranges['denominator'][0], ranges['denominator'][1])

        # Generate whole number divisor
        c = random.randint(2, ranges['whole_number'][1])

        # Correct: (a/b) ÷ c = (a/b) × (1/c) = a/(b×c)
        correct_num = a
        correct_den = b * c
        correct_frac = Fraction(correct_num, correct_den)

        # Malrule: (a/b) ÷ c = (a×c)/b (multiplies instead of dividing)
        malrule_num = a * c
        malrule_den = b
        malrule_frac = Fraction(malrule_num, malrule_den)

        problem_text = f"Divide: ({a}/{b}) ÷ {c}"

        metadata = {
            'a': a,
            'b': b,
            'c': c,
            'd': 1,  # c = c/1
            'correct_numerator': correct_frac.numerator,
            'correct_denominator': correct_frac.denominator,
            'malrule_numerator': malrule_frac.numerator,
            'malrule_denominator': malrule_frac.denominator,
            'correct_answer': f"{correct_frac.numerator}/{correct_frac.denominator}",
            'malrule_answer': f"{malrule_frac.numerator}/{malrule_frac.denominator}",
            'template': 'whole_number_divisor'
        }

        return Problem(
            text=problem_text,
            operands=[a, b, c],
            operation='fraction_division',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_whole_number_dividend(self, seed=None) -> Problem:
        """
        Generate whole number ÷ fraction problem.

        Example: 6 ÷ (2/3)
        Correct: 6 × (3/2) = 18/2 = 9
        Malrule: 6 × (2/3) = 12/3 = 4 (forgets to flip)
        """
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()

        # Generate whole number dividend
        a = random.randint(2, ranges['whole_number'][1])

        # Generate fraction divisor c/d
        c = random.randint(ranges['numerator'][0], ranges['numerator'][1])
        d = random.randint(ranges['denominator'][0], ranges['denominator'][1])

        while c == 0:
            c = random.randint(ranges['numerator'][0], ranges['numerator'][1])

        # Correct: a ÷ (c/d) = a × (d/c) = (a×d)/c
        correct_num = a * d
        correct_den = c
        correct_frac = Fraction(correct_num, correct_den)

        # Malrule: a ÷ (c/d) = a × (c/d) = (a×c)/d (forgets to flip)
        malrule_num = a * c
        malrule_den = d
        malrule_frac = Fraction(malrule_num, malrule_den)

        problem_text = f"Divide: {a} ÷ ({c}/{d})"

        metadata = {
            'a': a,
            'b': 1,  # a = a/1
            'c': c,
            'd': d,
            'correct_numerator': correct_frac.numerator,
            'correct_denominator': correct_frac.denominator,
            'malrule_numerator': malrule_frac.numerator,
            'malrule_denominator': malrule_frac.denominator,
            'correct_answer': f"{correct_frac.numerator}/{correct_frac.denominator}",
            'malrule_answer': f"{malrule_frac.numerator}/{malrule_frac.denominator}",
            'template': 'whole_number_dividend'
        }

        return Problem(
            text=problem_text,
            operands=[a, c, d],
            operation='fraction_division',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_mixed_numbers(self, seed=None) -> Problem:
        """
        Generate division with mixed numbers.

        Example: 1½ ÷ 2¼ = (3/2) ÷ (9/4)
        Correct: (3/2) × (4/9) = 12/18 = 2/3
        Malrule: (3/2) × (9/4) = 27/8 (forgets to flip)
        """
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()

        # Generate first mixed number: whole1 + (a/b)
        whole1 = random.randint(1, 3)
        a = random.randint(1, ranges['denominator'][1] - 1)
        b = random.randint(2, ranges['denominator'][1])

        # Ensure a < b for proper fraction
        if a >= b:
            a = random.randint(1, b - 1)

        # Convert to improper fraction
        num1 = whole1 * b + a
        den1 = b

        # Generate second mixed number: whole2 + (c/d)
        whole2 = random.randint(1, 3)
        c = random.randint(1, ranges['denominator'][1] - 1)
        d = random.randint(2, ranges['denominator'][1])

        # Ensure c < d for proper fraction
        if c >= d:
            c = random.randint(1, d - 1)

        # Convert to improper fraction
        num2 = whole2 * d + c
        den2 = d

        # Correct: (num1/den1) ÷ (num2/den2) = (num1/den1) × (den2/num2)
        correct_num = num1 * den2
        correct_den = den1 * num2
        correct_frac = Fraction(correct_num, correct_den)

        # Malrule: forgets to flip
        malrule_num = num1 * num2
        malrule_den = den1 * den2
        malrule_frac = Fraction(malrule_num, malrule_den)

        problem_text = f"Divide: {whole1} {a}/{b} ÷ {whole2} {c}/{d}"

        metadata = {
            'a': num1,
            'b': den1,
            'c': num2,
            'd': den2,
            'whole1': whole1,
            'whole2': whole2,
            'frac1_num': a,
            'frac1_den': b,
            'frac2_num': c,
            'frac2_den': d,
            'correct_numerator': correct_frac.numerator,
            'correct_denominator': correct_frac.denominator,
            'malrule_numerator': malrule_frac.numerator,
            'malrule_denominator': malrule_frac.denominator,
            'correct_answer': f"{correct_frac.numerator}/{correct_frac.denominator}",
            'malrule_answer': f"{malrule_frac.numerator}/{malrule_frac.denominator}",
            'template': 'mixed_numbers'
        }

        return Problem(
            text=problem_text,
            operands=[num1, den1, num2, den2],
            operation='fraction_division',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_word_problem(self, seed=None) -> Problem:
        """
        Generate word problem with fraction division context.

        Example: "You have 3/4 of a pizza. Each serving is 1/8 of a pizza.
                  How many servings can you make?"
        Correct: (3/4) ÷ (1/8) = (3/4) × (8/1) = 24/4 = 6 servings
        Malrule: (3/4) × (1/8) = 3/32 servings (forgets to flip)
        """
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()

        contexts = [
            {
                'text': 'You have {a}/{b} of a pizza. Each serving is {c}/{d} of a pizza. How many servings can you make?',
                'context_type': 'pizza_servings',
                'unit': 'servings'
            },
            {
                'text': '{a}/{b} cups of flour are needed for a recipe. Each batch uses {c}/{d} cups. How many batches can you make?',
                'context_type': 'recipe_batches',
                'unit': 'batches'
            },
            {
                'text': 'A rope is {a}/{b} meters long. You need to cut it into pieces that are each {c}/{d} meters. How many pieces will you get?',
                'context_type': 'rope_pieces',
                'unit': 'pieces'
            },
            {
                'text': 'You have {a}/{b} hours to complete tasks. Each task takes {c}/{d} hours. How many tasks can you complete?',
                'context_type': 'tasks',
                'unit': 'tasks'
            }
        ]

        context = random.choice(contexts)

        # Generate fractions
        a = random.randint(ranges['numerator'][0], ranges['numerator'][1])
        b = random.randint(ranges['denominator'][0], ranges['denominator'][1])
        c = random.randint(ranges['numerator'][0], ranges['numerator'][1])
        d = random.randint(ranges['denominator'][0], ranges['denominator'][1])

        while c == 0:
            c = random.randint(ranges['numerator'][0], ranges['numerator'][1])

        # Make sure a/b > c/d for sensible word problems
        if a * d <= c * b:
            a, c = c, a
            b, d = d, b

        problem_text = context['text'].format(a=a, b=b, c=c, d=d)

        # Correct: (a/b) ÷ (c/d) = (a×d)/(b×c)
        correct_num = a * d
        correct_den = b * c
        correct_frac = Fraction(correct_num, correct_den)

        # Malrule: forgets to flip
        malrule_num = a * c
        malrule_den = b * d
        malrule_frac = Fraction(malrule_num, malrule_den)

        metadata = {
            'a': a,
            'b': b,
            'c': c,
            'd': d,
            'context_type': context['context_type'],
            'unit': context['unit'],
            'correct_numerator': correct_frac.numerator,
            'correct_denominator': correct_frac.denominator,
            'malrule_numerator': malrule_frac.numerator,
            'malrule_denominator': malrule_frac.denominator,
            'correct_answer': f"{correct_frac.numerator}/{correct_frac.denominator}",
            'malrule_answer': f"{malrule_frac.numerator}/{malrule_frac.denominator}",
            'template': 'word_problem'
        }

        return Problem(
            text=problem_text,
            operands=[a, b, c, d],
            operation='fraction_division',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_word_problem_whole_divisor(self, seed=None) -> Problem:
        """Generate word problem with fraction ÷ whole number."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()

        # Generate fraction a/b
        a = random.randint(ranges['numerator'][0], ranges['numerator'][1])
        b = random.randint(ranges['denominator'][0], ranges['denominator'][1])

        # Generate whole number divisor
        c = random.randint(2, min(ranges['whole_number'][1], 8))

        # Correct: (a/b) ÷ c = (a/b) × (1/c) = a/(b×c)
        correct_num = a
        correct_den = b * c
        correct_frac = Fraction(correct_num, correct_den)

        # Malrule: (a/b) ÷ c = (a×c)/b (multiplies instead of dividing)
        malrule_num = a * c
        malrule_den = b
        malrule_frac = Fraction(malrule_num, malrule_den)

        contexts = [
            f"You have {a}/{b} of a cake. If you divide it equally among {c} people, how much cake does each person get?",
            f"A ribbon is {a}/{b} meter long. You cut it into {c} equal pieces. How long is each piece (in meters)?",
            f"There are {a}/{b} liters of juice in a container. If you pour it equally into {c} glasses, how much juice is in each glass (in liters)?"
        ]
        problem_text = random.choice(contexts)

        metadata = {
            'a': a,
            'b': b,
            'c': c,
            'd': 1,  # c = c/1
            'correct_numerator': correct_frac.numerator,
            'correct_denominator': correct_frac.denominator,
            'malrule_numerator': malrule_frac.numerator,
            'malrule_denominator': malrule_frac.denominator,
            'correct_answer': f"{correct_frac.numerator}/{correct_frac.denominator}",
            'malrule_answer': f"{malrule_frac.numerator}/{malrule_frac.denominator}",
            'template': 'word_problem_whole_divisor'
        }

        return Problem(
            text=problem_text,
            operands=[a, b, c],
            operation='fraction_division',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_word_problem_whole_dividend(self, seed=None) -> Problem:
        """Generate word problem with whole number ÷ fraction."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()

        # Generate whole number dividend
        a = random.randint(2, min(ranges['whole_number'][1], 10))

        # Generate fraction divisor c/d
        c = random.randint(ranges['numerator'][0], ranges['numerator'][1])
        d = random.randint(ranges['denominator'][0], ranges['denominator'][1])

        while c == 0:
            c = random.randint(ranges['numerator'][0], ranges['numerator'][1])

        # Correct: a ÷ (c/d) = a × (d/c) = (a×d)/c
        correct_num = a * d
        correct_den = c
        correct_frac = Fraction(correct_num, correct_den)

        # Malrule: a ÷ (c/d) = a × (c/d) = (a×c)/d (forgets to flip)
        malrule_num = a * c
        malrule_den = d
        malrule_frac = Fraction(malrule_num, malrule_den)

        contexts = [
            f"You have {a} pizzas. If each serving is {c}/{d} of a pizza, how many servings can you make?",
            f"A rope is {a} meters long. You need to cut pieces that are each {c}/{d} meter. How many pieces can you cut?",
            f"You have {a} cups of flour. Each recipe requires {c}/{d} cup. How many recipes can you make?"
        ]
        problem_text = random.choice(contexts)

        metadata = {
            'a': a,
            'b': 1,  # a = a/1
            'c': c,
            'd': d,
            'correct_numerator': correct_frac.numerator,
            'correct_denominator': correct_frac.denominator,
            'malrule_numerator': malrule_frac.numerator,
            'malrule_denominator': malrule_frac.denominator,
            'correct_answer': f"{correct_frac.numerator}/{correct_frac.denominator}",
            'malrule_answer': f"{malrule_frac.numerator}/{malrule_frac.denominator}",
            'template': 'word_problem_whole_dividend'
        }

        return Problem(
            text=problem_text,
            operands=[a, c, d],
            operation='fraction_division',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_word_problem_mixed(self, seed=None) -> Problem:
        """Generate word problem with mixed numbers division."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()

        # Generate first mixed number: whole1 + (a/b)
        whole1 = random.randint(1, 3)
        a = random.randint(1, min(ranges['denominator'][1], 6) - 1)
        b = random.randint(2, min(ranges['denominator'][1], 8))

        # Ensure a < b for proper fraction
        if a >= b:
            a = random.randint(1, b - 1)

        # Convert to improper fraction
        num1 = whole1 * b + a
        den1 = b

        # Generate second mixed number: whole2 + (c/d)
        whole2 = random.randint(1, 3)
        c = random.randint(1, min(ranges['denominator'][1], 6) - 1)
        d = random.randint(2, min(ranges['denominator'][1], 8))

        # Ensure c < d for proper fraction
        if c >= d:
            c = random.randint(1, d - 1)

        # Convert to improper fraction
        num2 = whole2 * d + c
        den2 = d

        # Correct: (num1/den1) ÷ (num2/den2) = (num1/den1) × (den2/num2)
        correct_num = num1 * den2
        correct_den = den1 * num2
        correct_frac = Fraction(correct_num, correct_den)

        # Malrule: forgets to flip
        malrule_num = num1 * num2
        malrule_den = den1 * den2
        malrule_frac = Fraction(malrule_num, malrule_den)

        contexts = [
            f"A rectangular garden is {whole1} {a}/{b} meters long. Each row is {whole2} {c}/{d} meters wide. How many rows fit in the length?",
            f"You have {whole1} {a}/{b} cups of flour. Each muffin needs {whole2} {c}/{d} cups. How many muffins can you make?",
            f"A rope is {whole1} {a}/{b} meters long. You need pieces that are {whole2} {c}/{d} meters each. How many pieces can you cut?"
        ]
        problem_text = random.choice(contexts)

        metadata = {
            'a': num1,
            'b': den1,
            'c': num2,
            'd': den2,
            'whole1': whole1,
            'whole2': whole2,
            'frac1_num': a,
            'frac1_den': b,
            'frac2_num': c,
            'frac2_den': d,
            'correct_numerator': correct_frac.numerator,
            'correct_denominator': correct_frac.denominator,
            'malrule_numerator': malrule_frac.numerator,
            'malrule_denominator': malrule_frac.denominator,
            'correct_answer': f"{correct_frac.numerator}/{correct_frac.denominator}",
            'malrule_answer': f"{malrule_frac.numerator}/{malrule_frac.denominator}",
            'template': 'word_problem_mixed'
        }

        return Problem(
            text=problem_text,
            operands=[num1, den1, num2, den2],
            operation='fraction_division',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )
