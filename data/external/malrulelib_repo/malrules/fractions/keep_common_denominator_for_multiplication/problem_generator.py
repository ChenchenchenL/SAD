"""
Problem generator for Keep-Common-Denominator-For-Multiplication malrule.
"""

import random
import sys
sys.path.append('/home/user/malrule-coding')

from typing import Optional, List
from utils import Problem, ProblemGenerator
from fractions import Fraction


class KeepCommonDenominatorForMultiplicationProblemGenerator(ProblemGenerator):
    """
    Generates fraction multiplication problems with same denominators.

    Templates:
    1. basic_common_denominator - Simple (a/b)×(c/b)
    2. three_fractions - Three fractions: (a/b)×(c/b)×(d/b)
    3. mixed_numbers - Mixed numbers with common denominator fractions
    4. larger_denominators - Common denominators 12-20
    5. word_problem - Real-world contexts (recipes, measurements)
    """

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_common_denominator',
            'three_fractions',
            'word_problem_three_fractions',
            'mixed_numbers',
            'word_problem_mixed',
            'larger_denominators',
            'word_problem'
        ]

    def get_value_ranges(self):
        """Return the value ranges for problem generation."""
        return {
            'numerator1': (1, 9),
            'numerator2': (1, 9),
            'denominator': (2, 12)
        }

    def generate(self, seed=None, template: Optional[str] = None):
        """Generate a fraction multiplication problem with common denominators."""
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            template = random.choice(self.get_available_templates())

        # Generate based on template
        if template == 'basic_common_denominator':
            return self._generate_basic_common_denominator(seed)
        elif template == 'three_fractions':
            return self._generate_three_fractions(seed)
        elif template == 'word_problem_three_fractions':
            return self._generate_word_problem_three_fractions(seed)
        elif template == 'mixed_numbers':
            return self._generate_mixed_numbers(seed)
        elif template == 'word_problem_mixed':
            return self._generate_word_problem_mixed(seed)
        elif template == 'larger_denominators':
            return self._generate_larger_denominators(seed)
        elif template == 'word_problem':
            return self._generate_word_problem(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_common_denominator(self, seed=None) -> Problem:
        """Generate basic (a/b)×(c/b) multiplication."""
        if seed is not None:
            random.seed(seed)

        a = random.randint(1, 9)
        c = random.randint(1, 9)
        b = random.randint(2, 12)

        # Ensure proper fractions
        while a >= b:
            a = random.randint(1, 9)
        while c >= b:
            c = random.randint(1, 9)

        # Correct: (a/b) × (c/b) = (a×c)/(b×b)
        correct_frac = Fraction(a * c, b * b)
        # Malrule: (a×c)/b (keeps common denominator)
        malrule_frac = Fraction(a * c, b)

        return Problem(
            text=f"Multiply: {a}/{b} × {c}/{b}",
            operands=[a, b, c, b],
            operation='fraction_multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'numerator1': a,
                'numerator2': c,
                'denominator': b,
                'correct_numerator': correct_frac.numerator,
                'correct_denominator': correct_frac.denominator,
                'malrule_numerator': malrule_frac.numerator,
                'malrule_denominator': malrule_frac.denominator,
                'correct_answer': f"{correct_frac.numerator}/{correct_frac.denominator}",
                'malrule_answer': f"{malrule_frac.numerator}/{malrule_frac.denominator}",
                'template': 'basic_common_denominator'
            }
        )

    def _generate_three_fractions(self, seed=None) -> Problem:
        """Generate three fractions with common denominator: (a/b)×(c/b)×(d/b)."""
        if seed is not None:
            random.seed(seed)

        a = random.randint(1, 5)
        c = random.randint(1, 5)
        d = random.randint(1, 5)
        b = random.randint(3, 8)

        while a >= b:
            a = random.randint(1, 5)
        while c >= b:
            c = random.randint(1, 5)
        while d >= b:
            d = random.randint(1, 5)

        # Correct: (a×c×d)/(b×b×b)
        correct_frac = Fraction(a * c * d, b * b * b)
        # Malrule: (a×c×d)/b (keeps common denominator)
        malrule_frac = Fraction(a * c * d, b)

        return Problem(
            text=f"Multiply: {a}/{b} × {c}/{b} × {d}/{b}",
            operands=[a, b, c, b, d, b],
            operation='fraction_multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'numerator1': a,
                'numerator2': c,
                'numerator3': d,
                'denominator': b,
                'correct_numerator': correct_frac.numerator,
                'correct_denominator': correct_frac.denominator,
                'malrule_numerator': malrule_frac.numerator,
                'malrule_denominator': malrule_frac.denominator,
                'correct_answer': f"{correct_frac.numerator}/{correct_frac.denominator}",
                'malrule_answer': f"{malrule_frac.numerator}/{malrule_frac.denominator}",
                'template': 'three_fractions'
            }
        )

    def _generate_mixed_numbers(self, seed=None) -> Problem:
        """Generate mixed numbers like 1 2/5 × 2 3/5."""
        if seed is not None:
            random.seed(seed)

        whole1 = random.randint(1, 3)
        whole2 = random.randint(1, 3)
        a = random.randint(1, 4)
        c = random.randint(1, 4)
        b = random.randint(5, 8)

        while a >= b:
            a = random.randint(1, 4)
        while c >= b:
            c = random.randint(1, 4)

        # Convert to improper fractions
        improper1 = whole1 * b + a
        improper2 = whole2 * b + c

        # Correct: (improper1/b) × (improper2/b) = (improper1×improper2)/(b×b)
        correct_frac = Fraction(improper1 * improper2, b * b)
        # Malrule: (improper1×improper2)/b
        malrule_frac = Fraction(improper1 * improper2, b)

        return Problem(
            text=f"Multiply: {whole1} {a}/{b} × {whole2} {c}/{b}",
            operands=[improper1, b, improper2, b],
            operation='fraction_multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'whole1': whole1,
                'whole2': whole2,
                'numerator1': a,
                'numerator2': c,
                'denominator': b,
                'improper1': improper1,
                'improper2': improper2,
                'correct_numerator': correct_frac.numerator,
                'correct_denominator': correct_frac.denominator,
                'malrule_numerator': malrule_frac.numerator,
                'malrule_denominator': malrule_frac.denominator,
                'correct_answer': f"{correct_frac.numerator}/{correct_frac.denominator}",
                'malrule_answer': f"{malrule_frac.numerator}/{malrule_frac.denominator}",
                'template': 'mixed_numbers'
            }
        )

    def _generate_larger_denominators(self, seed=None) -> Problem:
        """Generate problems with larger common denominators (12-20)."""
        if seed is not None:
            random.seed(seed)

        b = random.randint(12, 20)
        a = random.randint(1, b-1)
        c = random.randint(1, b-1)

        correct_frac = Fraction(a * c, b * b)
        malrule_frac = Fraction(a * c, b)

        return Problem(
            text=f"Multiply: {a}/{b} × {c}/{b}",
            operands=[a, b, c, b],
            operation='fraction_multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'numerator1': a,
                'numerator2': c,
                'denominator': b,
                'correct_numerator': correct_frac.numerator,
                'correct_denominator': correct_frac.denominator,
                'malrule_numerator': malrule_frac.numerator,
                'malrule_denominator': malrule_frac.denominator,
                'correct_answer': f"{correct_frac.numerator}/{correct_frac.denominator}",
                'malrule_answer': f"{malrule_frac.numerator}/{malrule_frac.denominator}",
                'template': 'larger_denominators'
            }
        )

    def _generate_word_problem(self, seed=None) -> Problem:
        """Generate real-world word problem contexts."""
        if seed is not None:
            random.seed(seed)

        contexts = [
            {
                'text': 'A recipe calls for {a}/{b} cup of sugar. If you make {c}/{b} of the recipe, how much sugar do you need (in cups)?',
                'context_type': 'recipe'
            },
            {
                'text': 'A rope is {a}/{b} meter long. You need {c}/{b} of that length. How long is the piece you need (in meters)?',
                'context_type': 'measurement'
            },
            {
                'text': 'A tank is {a}/{b} full. You drain {c}/{b} of what\'s in the tank. What fraction of the full tank did you drain?',
                'context_type': 'proportion'
            }
        ]

        context = random.choice(contexts)
        b = random.randint(4, 10)
        a = random.randint(1, b-1)
        c = random.randint(1, b-1)

        correct_frac = Fraction(a * c, b * b)
        malrule_frac = Fraction(a * c, b)

        problem_text = context['text'].format(a=a, b=b, c=c)

        return Problem(
            text=problem_text,
            operands=[a, b, c, b],
            operation='fraction_multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'numerator1': a,
                'numerator2': c,
                'denominator': b,
                'correct_numerator': correct_frac.numerator,
                'correct_denominator': correct_frac.denominator,
                'malrule_numerator': malrule_frac.numerator,
                'malrule_denominator': malrule_frac.denominator,
                'correct_answer': f"{correct_frac.numerator}/{correct_frac.denominator}",
                'malrule_answer': f"{malrule_frac.numerator}/{malrule_frac.denominator}",
                'context_type': context['context_type'],
                'template': 'word_problem'
            }
        )

    def _generate_word_problem_three_fractions(self, seed=None) -> Problem:
        """Generate word problem with three fractions with common denominators."""
        if seed is not None:
            random.seed(seed)

        a = random.randint(1, 5)
        c = random.randint(1, 5)
        d = random.randint(1, 5)
        b = random.randint(3, 8)

        while a >= b:
            a = random.randint(1, 5)
        while c >= b:
            c = random.randint(1, 5)
        while d >= b:
            d = random.randint(1, 5)

        # Correct: (a×c×d)/(b×b×b)
        correct_frac = Fraction(a * c * d, b * b * b)
        # Malrule: (a×c×d)/b (keeps common denominator)
        malrule_frac = Fraction(a * c * d, b)

        contexts = [
            f"A recipe calls for {a}/{b} cup of ingredient A. You need {c}/{b} of that amount of ingredient B, and {d}/{b} of that amount of ingredient C. How much of ingredient C do you need in total (in cups)?",
            f"A garden bed is {a}/{b} of an acre. The vegetable section is {c}/{b} of that, and the herb section is {d}/{b} of the vegetable section. What fraction of an acre is the herb section?",
            f"A book has {a}/{b} of its pages with illustrations. Of those, {c}/{b} are in color, and of the color illustrations, {d}/{b} are full-page. What fraction of the book's total pages are full-page color illustrations?"
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[a, b, c, b, d, b],
            operation='fraction_multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'numerator1': a,
                'numerator2': c,
                'numerator3': d,
                'denominator': b,
                'correct_numerator': correct_frac.numerator,
                'correct_denominator': correct_frac.denominator,
                'malrule_numerator': malrule_frac.numerator,
                'malrule_denominator': malrule_frac.denominator,
                'correct_answer': f"{correct_frac.numerator}/{correct_frac.denominator}",
                'malrule_answer': f"{malrule_frac.numerator}/{malrule_frac.denominator}",
                'template': 'word_problem_three_fractions'
            }
        )

    def _generate_word_problem_mixed(self, seed=None) -> Problem:
        """Generate word problem with mixed numbers having common denominators."""
        if seed is not None:
            random.seed(seed)

        whole1 = random.randint(1, 3)
        whole2 = random.randint(1, 3)
        a = random.randint(1, 4)
        c = random.randint(1, 4)
        b = random.randint(5, 8)

        while a >= b:
            a = random.randint(1, 4)
        while c >= b:
            c = random.randint(1, 4)

        # Convert to improper fractions
        improper1 = whole1 * b + a
        improper2 = whole2 * b + c

        # Correct: (improper1/b) × (improper2/b) = (improper1×improper2)/(b×b)
        correct_frac = Fraction(improper1 * improper2, b * b)
        # Malrule: (improper1×improper2)/b
        malrule_frac = Fraction(improper1 * improper2, b)

        contexts = [
            f"A rectangular garden is {whole1} {a}/{b} yards long and {whole2} {c}/{b} yards wide. What is the area of the garden in square yards?",
            f"Sarah walks {whole1} {a}/{b} miles per hour. If she walks for {whole2} {c}/{b} hours, how far does she walk (in miles)?",
            f"A recipe calls for {whole1} {a}/{b} cups of flour per batch. If you make {whole2} {c}/{b} batches, how much flour do you need in total (in cups)?"
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[improper1, b, improper2, b],
            operation='fraction_multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'whole1': whole1,
                'whole2': whole2,
                'numerator1': a,
                'numerator2': c,
                'denominator': b,
                'improper1': improper1,
                'improper2': improper2,
                'correct_numerator': correct_frac.numerator,
                'correct_denominator': correct_frac.denominator,
                'malrule_numerator': malrule_frac.numerator,
                'malrule_denominator': malrule_frac.denominator,
                'correct_answer': f"{correct_frac.numerator}/{correct_frac.denominator}",
                'malrule_answer': f"{malrule_frac.numerator}/{malrule_frac.denominator}",
                'template': 'word_problem_mixed'
            }
        )
