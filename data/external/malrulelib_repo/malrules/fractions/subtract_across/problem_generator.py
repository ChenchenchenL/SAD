"""
Problem generator for fraction subtraction malrule.

Generates fraction subtraction problems with different denominators.
"""

import random
from typing import Dict, Tuple, Optional
from math import gcd
import sys
sys.path.append('/home/user/malrule-coding')

from utils import Problem, ProblemGenerator, DifficultyLevel, create_fraction_template


class FractionSubtractionProblemGenerator(ProblemGenerator):
    """
    Generates fraction subtraction problems.

    Problems use different denominators to elicit the Subtract-Across malrule.
    The first fraction (minuend) is larger than the second (subtrahend) to
    avoid negative results.
    """

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level and difficulty."""
        ranges = {
            4: {
                DifficultyLevel.EASY: (2, 6),      # denominators 2-6
                DifficultyLevel.MEDIUM: (2, 10),
                DifficultyLevel.HARD: (2, 12),
            },
            5: {
                DifficultyLevel.EASY: (2, 8),
                DifficultyLevel.MEDIUM: (2, 12),
                DifficultyLevel.HARD: (2, 16),
            },
            6: {
                DifficultyLevel.EASY: (2, 10),
                DifficultyLevel.MEDIUM: (2, 15),
                DifficultyLevel.HARD: (2, 20),
            },
            7: {
                DifficultyLevel.EASY: (2, 12),
                DifficultyLevel.MEDIUM: (2, 20),
                DifficultyLevel.HARD: (2, 30),
            }
        }

        # Default to level 5 if not in ranges
        lvl = self.level if self.level in ranges else 5
        return {'denominator': ranges[lvl][self.difficulty]}

    def _simplify_fraction(self, numerator: int, denominator: int) -> Tuple[int, int]:
        """Simplify a fraction to lowest terms."""
        if numerator == 0:
            return 0, denominator
        common = gcd(abs(numerator), abs(denominator))
        return numerator // common, denominator // common

    def _generate_problem_text(self, fractions: list, problem_type: str) -> str:
        """
        Generate problem text based on problem type.

        Args:
            fractions: List of (numerator, denominator) tuples
            problem_type: Type of problem context

        Returns:
            Formatted problem text
        """
        if problem_type == 'basic_two':
            num1, den1 = fractions[0]
            num2, den2 = fractions[1]
            contexts = [
                f"What is {num1}/{den1} - {num2}/{den2}?",
                f"Calculate: {num1}/{den1} - {num2}/{den2}",
                f"Find the difference: {num1}/{den1} - {num2}/{den2}",
                f"Subtract {num2}/{den2} from {num1}/{den1}."
            ]
            return random.choice(contexts)

        elif problem_type == 'three_fractions':
            num1, den1 = fractions[0]
            num2, den2 = fractions[1]
            num3, den3 = fractions[2]
            contexts = [
                f"What is {num1}/{den1} - {num2}/{den2} - {num3}/{den3}?",
                f"Calculate: {num1}/{den1} - {num2}/{den2} - {num3}/{den3}",
                f"Find the result: {num1}/{den1} - {num2}/{den2} - {num3}/{den3}",
                f"Subtract {num2}/{den2} and {num3}/{den3} from {num1}/{den1}."
            ]
            return random.choice(contexts)

        elif problem_type == 'word_problem':
            num1, den1 = fractions[0]
            num2, den2 = fractions[1]

            contexts = [
                f"Sarah had {num1}/{den1} of a pizza. She gave away {num2}/{den2} of the pizza. What fraction does she have left?",
                f"A tank was {num1}/{den1} full of water. After using {num2}/{den2} of the tank, how full is it now?",
                f"Tom had {num1}/{den1} of his homework done. He realized {num2}/{den2} was incorrect. What fraction of correct homework does he have?",
                f"Maria ran {num1}/{den1} of a mile, then walked back {num2}/{den2} of a mile. What is the net distance forward?",
                f"A recipe needs {num1}/{den1} cup of sugar but you only want to use {num2}/{den2} cup less. How much sugar should you use?",
                f"Jake completed {num1}/{den1} of a project, but {num2}/{den2} needs to be redone. What fraction is truly complete?",
            ]
            return random.choice(contexts)

        elif problem_type == 'improper':
            # For improper fractions, use as-is
            num1, den1 = fractions[0]
            num2, den2 = fractions[1]
            contexts = [
                f"What is {num1}/{den1} - {num2}/{den2}?",
                f"Calculate: {num1}/{den1} - {num2}/{den2}",
                f"Find the difference: {num1}/{den1} - {num2}/{den2}",
                f"Subtract {num2}/{den2} from {num1}/{den1}."
            ]
            return random.choice(contexts)

        elif problem_type == 'negative_result':
            # Problem that results in negative answer
            num1, den1 = fractions[0]
            num2, den2 = fractions[1]
            contexts = [
                f"What is {num1}/{den1} - {num2}/{den2}?",
                f"Calculate: {num1}/{den1} - {num2}/{den2}",
                f"Find the difference: {num1}/{den1} - {num2}/{den2}",
                f"Subtract {num2}/{den2} from {num1}/{den1}."
            ]
            return random.choice(contexts)

        else:
            # Default to basic
            num1, den1 = fractions[0]
            num2, den2 = fractions[1]
            contexts = [
                f"What is {num1}/{den1} - {num2}/{den2}?",
                f"Calculate: {num1}/{den1} - {num2}/{den2}",
                f"Find the difference: {num1}/{den1} - {num2}/{den2}",
                f"Subtract {num2}/{den2} from {num1}/{den1}."
            ]
            return random.choice(contexts)

    def get_available_templates(self) -> list:
        """Return list of available template names."""
        return [
            'basic_subtraction',
            'word_problem_pizza',
            'three_fractions',
            'word_problem_three_fractions',  # NEW: Word problems with three fractions
            'improper_fractions',
            'word_problem_improper',  # NEW: Word problems with improper fractions
            'word_problem_measurement'
        ]

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate a fraction subtraction problem.

        Args:
            seed: Optional random seed for reproducibility
            template: Optional template name to use. If None, uses legacy generation.

        Returns:
            Problem instance
        """
        if seed is not None:
            random.seed(seed)

        # If template is specified, use template-based generation
        if template is not None:
            if template not in self.get_available_templates():
                raise ValueError(f"Unknown template: {template}")

            # Call the appropriate template method
            template_method = getattr(self, f'_generate_{template}')
            return template_method(seed)

        # Legacy generation below
        den_min, den_max = self.get_value_ranges()['denominator']

        # Choose problem type - weighted to include new templates
        problem_types = ['basic_two', 'three_fractions', 'word_problem', 'improper', 'negative_result']
        # For level 6+, include more complex types
        if self.level >= 6:
            problem_types.extend(['three_fractions', 'improper', 'negative_result', 'word_problem'])

        problem_type = random.choice(problem_types)

        # Generate fractions based on problem type
        if problem_type == 'three_fractions':
            # Generate three fractions
            den1 = random.randint(den_min, den_max)
            den2 = random.randint(den_min, den_max)
            den3 = random.randint(den_min, den_max)

            # Ensure at least two denominators are different
            while den1 == den2 == den3:
                den2 = random.randint(den_min, den_max)

            # Generate proper fractions independently
            # Ensure denominators are at least 3 to have valid ranges
            if den1 < 3:
                den1 = random.randint(3, max(den_max, 6))
            if den2 < 3:
                den2 = random.randint(3, max(den_max, 6))
            if den3 < 3:
                den3 = random.randint(3, max(den_max, 6))

            # Generate numerators for proper fractions
            num1 = random.randint(max(1, den1 // 2), den1 - 1)
            num2 = random.randint(1, den2 - 1)
            num3 = random.randint(1, den3 - 1)

            # Simplify fractions
            num1, den1 = self._simplify_fraction(num1, den1)
            num2, den2 = self._simplify_fraction(num2, den2)
            num3, den3 = self._simplify_fraction(num3, den3)

            fractions = [(num1, den1), (num2, den2), (num3, den3)]

        elif problem_type == 'improper':
            # Generate improper fractions
            den1 = random.randint(den_min, min(den_max, 12))
            den2 = random.randint(den_min, min(den_max, 12))

            # Ensure denominators are different
            while den2 == den1:
                den2 = random.randint(den_min, min(den_max, 12))

            # Generate improper fractions, first larger than second
            # To ensure result is positive: num1/den1 > num2/den2
            num1 = random.randint(den1 + 1, den1 * 3)  # Improper, at least den1+1
            num2 = random.randint(den2, den2 * 2)  # Improper, up to 2*den2

            # Ensure first fraction is larger to avoid negative results
            frac1_value = num1 / den1
            frac2_value = num2 / den2
            if frac1_value <= frac2_value:
                # Swap if first is smaller
                num1, den1, num2, den2 = num2, den2, num1, den1

            # Simplify fractions
            num1, den1 = self._simplify_fraction(num1, den1)
            num2, den2 = self._simplify_fraction(num2, den2)

            fractions = [(num1, den1), (num2, den2)]

        elif problem_type == 'negative_result':
            # Generate fractions where result will be negative
            den1 = random.randint(max(den_min, 3), den_max)  # At least 3 for valid ranges
            den2 = random.randint(max(den_min, 3), den_max)

            # Ensure denominators are different
            while den2 == den1:
                den2 = random.randint(max(den_min, 3), den_max)

            # Generate numerators where second fraction > first (negative result)
            # Make sure first is smaller than second
            num2 = random.randint(2, den2 - 1)  # Generate second first (larger fraction)
            num1 = random.randint(1, min(num2 - 1, den1 - 1))  # First must be smaller

            # Simplify fractions
            num1, den1 = self._simplify_fraction(num1, den1)
            num2, den2 = self._simplify_fraction(num2, den2)

            fractions = [(num1, den1), (num2, den2)]

        else:
            # Generate two proper fractions with different denominators
            den1 = random.randint(den_min, den_max)
            den2 = random.randint(den_min, den_max)

            # Ensure denominators are different
            while den2 == den1:
                den2 = random.randint(den_min, den_max)

            # Generate numerators (both proper fractions)
            num1 = random.randint(1, den1 - 1)
            num2 = random.randint(1, den2 - 1)

            # Ensure first fraction is larger than second to avoid negative results
            frac1_value = num1 / den1
            frac2_value = num2 / den2

            # If first fraction is smaller, swap them
            if frac1_value <= frac2_value:
                num1, den1, num2, den2 = num2, den2, num1, den1

            # Simplify fractions
            num1, den1 = self._simplify_fraction(num1, den1)
            num2, den2 = self._simplify_fraction(num2, den2)

            fractions = [(num1, den1), (num2, den2)]

        # Generate problem text
        problem_text = self._generate_problem_text(fractions, problem_type)

        return Problem(
            text=problem_text,
            operands=fractions,
            operation='fraction_subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'problem_type': problem_type,
                'num_fractions': len(fractions),
                'fractions': [f"{n}/{d}" for n, d in fractions]
            }
        )

    def _generate_basic_subtraction(self, seed: Optional[int] = None) -> Problem:
        """
        Template 1: Basic fraction subtraction with different denominators.

        Simple two-fraction subtraction problem that clearly elicits the subtract-across error.
        Example: 3/4 - 1/2 (correct: 1/4, malrule: 2/2 = 1)
        """
        if seed is not None:
            random.seed(seed)

        den_min, den_max = self.get_value_ranges()['denominator']

        # Generate two proper fractions with different denominators
        den1 = random.randint(den_min, den_max)
        den2 = random.randint(den_min, den_max)

        # Ensure denominators are different
        while den2 == den1:
            den2 = random.randint(den_min, den_max)

        # Generate proper fractions
        num1 = random.randint(1, den1 - 1)
        num2 = random.randint(1, den2 - 1)

        # Ensure first fraction is larger than second
        if num1 / den1 <= num2 / den2:
            num1, den1, num2, den2 = num2, den2, num1, den1

        # Simplify fractions
        num1, den1 = self._simplify_fraction(num1, den1)
        num2, den2 = self._simplify_fraction(num2, den2)

        fractions = [(num1, den1), (num2, den2)]

        # Calculate correct answer
        from math import gcd
        def lcm(a, b):
            return abs(a * b) // gcd(a, b)

        common_den = lcm(den1, den2)
        converted_num1 = num1 * (common_den // den1)
        converted_num2 = num2 * (common_den // den2)
        result_num = converted_num1 - converted_num2
        correct_num, correct_den = self._simplify_fraction(result_num, common_den)
        correct_answer = f"{correct_num}/{correct_den}"

        # Calculate malrule answer (subtract across)
        malrule_num = num1 - num2
        malrule_den = den1 - den2
        if malrule_den == 0:
            malrule_answer = f"{malrule_num}/0"
        elif malrule_den < 0:
            malrule_num = -malrule_num
            malrule_den = -malrule_den
            mal_num, mal_den = self._simplify_fraction(malrule_num, malrule_den)
            malrule_answer = f"{mal_num}/{mal_den}"
        else:
            mal_num, mal_den = self._simplify_fraction(malrule_num, malrule_den)
            malrule_answer = f"{mal_num}/{mal_den}"

        # Generate problem text
        contexts = [
            f"What is {num1}/{den1} - {num2}/{den2}?",
            f"Calculate: {num1}/{den1} - {num2}/{den2}",
            f"Find the difference: {num1}/{den1} - {num2}/{den2}",
            f"Subtract {num2}/{den2} from {num1}/{den1}."
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=fractions,
            operation='fraction_subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'basic_subtraction',
                'fractions': [f"{n}/{d}" for n, d in fractions],
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_word_problem_pizza(self, seed: Optional[int] = None) -> Problem:
        """
        Template 2: Word problem in pizza/food context.

        Uses real-world pizza or food scenarios to elicit the subtract-across error.
        Example: Sarah ate 3/4 of a pizza and gave away 1/3 of a pizza.
        """
        if seed is not None:
            random.seed(seed)

        den_min, den_max = self.get_value_ranges()['denominator']

        # Generate two proper fractions with different denominators
        den1 = random.randint(den_min, min(den_max, 12))  # Keep reasonable for food context
        den2 = random.randint(den_min, min(den_max, 12))

        # Ensure denominators are different
        while den2 == den1:
            den2 = random.randint(den_min, min(den_max, 12))

        # Generate proper fractions
        num1 = random.randint(1, den1 - 1)
        num2 = random.randint(1, den2 - 1)

        # Ensure first fraction is larger
        if num1 / den1 <= num2 / den2:
            num1, den1, num2, den2 = num2, den2, num1, den1

        # Simplify fractions
        num1, den1 = self._simplify_fraction(num1, den1)
        num2, den2 = self._simplify_fraction(num2, den2)

        fractions = [(num1, den1), (num2, den2)]

        # Calculate correct answer
        from math import gcd
        def lcm(a, b):
            return abs(a * b) // gcd(a, b)

        common_den = lcm(den1, den2)
        converted_num1 = num1 * (common_den // den1)
        converted_num2 = num2 * (common_den // den2)
        result_num = converted_num1 - converted_num2
        correct_num, correct_den = self._simplify_fraction(result_num, common_den)
        correct_answer = f"{correct_num}/{correct_den}"

        # Calculate malrule answer
        malrule_num = num1 - num2
        malrule_den = den1 - den2
        if malrule_den == 0:
            malrule_answer = f"{malrule_num}/0"
        elif malrule_den < 0:
            malrule_num = -malrule_num
            malrule_den = -malrule_den
            mal_num, mal_den = self._simplify_fraction(malrule_num, malrule_den)
            malrule_answer = f"{mal_num}/{mal_den}"
        else:
            mal_num, mal_den = self._simplify_fraction(malrule_num, malrule_den)
            malrule_answer = f"{mal_num}/{mal_den}"

        # Generate word problem
        contexts = [
            f"Sarah had {num1}/{den1} of a pizza. She gave away {num2}/{den2} of the pizza. What fraction does she have left?",
            f"A cake was {num1}/{den1} full. After eating {num2}/{den2} of the cake, how much is left?",
            f"Tom had {num1}/{den1} of a pie. He shared {num2}/{den2} of the pie with his friend. What fraction remains?",
            f"Maria baked cookies. {num1}/{den1} were chocolate chip and she gave away {num2}/{den2} of all the cookies. What fraction does she have left?",
            f"A sandwich is cut into pieces. Jake ate {num1}/{den1} of it and gave {num2}/{den2} to his sister. What fraction is left?",
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=fractions,
            operation='fraction_subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_pizza',
                'fractions': [f"{n}/{d}" for n, d in fractions],
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_three_fractions(self, seed: Optional[int] = None) -> Problem:
        """
        Template 3: Subtracting three fractions.

        Involves subtracting three fractions to elicit the subtract-across error multiple times.
        Example: 5/6 - 1/3 - 1/4
        """
        if seed is not None:
            random.seed(seed)

        den_min, den_max = self.get_value_ranges()['denominator']

        # Generate three proper fractions with different denominators
        den1 = random.randint(max(den_min, 4), min(den_max, 12))
        den2 = random.randint(den_min, min(den_max, 12))
        den3 = random.randint(den_min, min(den_max, 12))

        # Ensure at least two denominators are different
        while den1 == den2 == den3:
            den2 = random.randint(den_min, min(den_max, 12))

        # Generate proper fractions
        num1 = random.randint(max(2, den1 // 2), den1 - 1)  # Make first relatively large
        num2 = random.randint(1, den2 - 1)
        num3 = random.randint(1, den3 - 1)

        # Simplify fractions
        num1, den1 = self._simplify_fraction(num1, den1)
        num2, den2 = self._simplify_fraction(num2, den2)
        num3, den3 = self._simplify_fraction(num3, den3)

        fractions = [(num1, den1), (num2, den2), (num3, den3)]

        # Calculate correct answer
        from math import gcd
        def lcm(a, b):
            return abs(a * b) // gcd(a, b)

        def lcm_multiple(numbers):
            result = numbers[0]
            for i in range(1, len(numbers)):
                result = lcm(result, numbers[i])
            return result

        common_den = lcm_multiple([den1, den2, den3])
        converted_num1 = num1 * (common_den // den1)
        converted_num2 = num2 * (common_den // den2)
        converted_num3 = num3 * (common_den // den3)
        result_num = converted_num1 - converted_num2 - converted_num3
        correct_num, correct_den = self._simplify_fraction(result_num, common_den)
        correct_answer = f"{correct_num}/{correct_den}"

        # Calculate malrule answer (subtract across all three)
        malrule_num = num1 - num2 - num3
        malrule_den = den1 - den2 - den3
        if malrule_den == 0:
            malrule_answer = f"{malrule_num}/0"
        elif malrule_den < 0:
            malrule_num = -malrule_num
            malrule_den = -malrule_den
            mal_num, mal_den = self._simplify_fraction(malrule_num, malrule_den)
            malrule_answer = f"{mal_num}/{mal_den}"
        else:
            mal_num, mal_den = self._simplify_fraction(malrule_num, malrule_den)
            malrule_answer = f"{mal_num}/{mal_den}"

        # Generate problem text
        contexts = [
            f"What is {num1}/{den1} - {num2}/{den2} - {num3}/{den3}?",
            f"Calculate: {num1}/{den1} - {num2}/{den2} - {num3}/{den3}",
            f"Find the result: {num1}/{den1} - {num2}/{den2} - {num3}/{den3}",
            f"Subtract {num2}/{den2} and {num3}/{den3} from {num1}/{den1}."
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=fractions,
            operation='fraction_subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'three_fractions',
                'fractions': [f"{n}/{d}" for n, d in fractions],
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_improper_fractions(self, seed: Optional[int] = None) -> Problem:
        """
        Template 4: Subtraction with improper fractions.

        Uses improper fractions where the subtract-across error is more pronounced.
        Example: 7/4 - 5/3 (correct: 1/12, malrule: 2/1 = 2)
        """
        if seed is not None:
            random.seed(seed)

        den_min, den_max = self.get_value_ranges()['denominator']

        # Generate improper fractions
        den1 = random.randint(den_min, min(den_max, 10))
        den2 = random.randint(den_min, min(den_max, 10))

        # Ensure denominators are different
        while den2 == den1:
            den2 = random.randint(den_min, min(den_max, 10))

        # Generate improper fractions
        num1 = random.randint(den1 + 1, den1 * 3)  # Improper, at least den1+1
        num2 = random.randint(den2, den2 * 2)  # Improper, up to 2*den2

        # Ensure first fraction is larger
        if num1 / den1 <= num2 / den2:
            num1, den1, num2, den2 = num2, den2, num1, den1

        # Simplify fractions
        num1, den1 = self._simplify_fraction(num1, den1)
        num2, den2 = self._simplify_fraction(num2, den2)

        fractions = [(num1, den1), (num2, den2)]

        # Calculate correct answer
        from math import gcd
        def lcm(a, b):
            return abs(a * b) // gcd(a, b)

        common_den = lcm(den1, den2)
        converted_num1 = num1 * (common_den // den1)
        converted_num2 = num2 * (common_den // den2)
        result_num = converted_num1 - converted_num2
        correct_num, correct_den = self._simplify_fraction(result_num, common_den)
        correct_answer = f"{correct_num}/{correct_den}"

        # Calculate malrule answer
        malrule_num = num1 - num2
        malrule_den = den1 - den2
        if malrule_den == 0:
            malrule_answer = f"{malrule_num}/0"
        elif malrule_den < 0:
            malrule_num = -malrule_num
            malrule_den = -malrule_den
            mal_num, mal_den = self._simplify_fraction(malrule_num, malrule_den)
            malrule_answer = f"{mal_num}/{mal_den}"
        else:
            mal_num, mal_den = self._simplify_fraction(malrule_num, malrule_den)
            malrule_answer = f"{mal_num}/{mal_den}"

        # Generate problem text
        contexts = [
            f"What is {num1}/{den1} - {num2}/{den2}?",
            f"Calculate: {num1}/{den1} - {num2}/{den2}",
            f"Find the difference: {num1}/{den1} - {num2}/{den2}",
            f"Subtract {num2}/{den2} from {num1}/{den1}."
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=fractions,
            operation='fraction_subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'improper_fractions',
                'fractions': [f"{n}/{d}" for n, d in fractions],
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_word_problem_measurement(self, seed: Optional[int] = None) -> Problem:
        """
        Template 5: Word problem in measurement context.

        Uses measurement scenarios (distance, volume, etc.) to elicit the subtract-across error.
        Example: Maria ran 3/4 of a mile and walked back 1/2 of a mile.
        """
        if seed is not None:
            random.seed(seed)

        den_min, den_max = self.get_value_ranges()['denominator']

        # Generate two proper fractions with different denominators
        den1 = random.randint(den_min, min(den_max, 12))
        den2 = random.randint(den_min, min(den_max, 12))

        # Ensure denominators are different
        while den2 == den1:
            den2 = random.randint(den_min, min(den_max, 12))

        # Generate proper fractions
        num1 = random.randint(1, den1 - 1)
        num2 = random.randint(1, den2 - 1)

        # Ensure first fraction is larger
        if num1 / den1 <= num2 / den2:
            num1, den1, num2, den2 = num2, den2, num1, den1

        # Simplify fractions
        num1, den1 = self._simplify_fraction(num1, den1)
        num2, den2 = self._simplify_fraction(num2, den2)

        fractions = [(num1, den1), (num2, den2)]

        # Calculate correct answer
        from math import gcd
        def lcm(a, b):
            return abs(a * b) // gcd(a, b)

        common_den = lcm(den1, den2)
        converted_num1 = num1 * (common_den // den1)
        converted_num2 = num2 * (common_den // den2)
        result_num = converted_num1 - converted_num2
        correct_num, correct_den = self._simplify_fraction(result_num, common_den)
        correct_answer = f"{correct_num}/{correct_den}"

        # Calculate malrule answer
        malrule_num = num1 - num2
        malrule_den = den1 - den2
        if malrule_den == 0:
            malrule_answer = f"{malrule_num}/0"
        elif malrule_den < 0:
            malrule_num = -malrule_num
            malrule_den = -malrule_den
            mal_num, mal_den = self._simplify_fraction(malrule_num, malrule_den)
            malrule_answer = f"{mal_num}/{mal_den}"
        else:
            mal_num, mal_den = self._simplify_fraction(malrule_num, malrule_den)
            malrule_answer = f"{mal_num}/{mal_den}"

        # Generate word problem with measurement context
        contexts = [
            f"A container was {num1}/{den1} full of water. After using {num2}/{den2} of the container, what fraction is full now?",
            f"Maria ran {num1}/{den1} of a mile. She walked back {num2}/{den2} of a mile. What is the net distance forward?",
            f"A recipe needs {num1}/{den1} cup of flour. You decide to reduce it by {num2}/{den2} cup. How much flour should you use?",
            f"Jake completed {num1}/{den1} of a mile on his bike. He then went backwards {num2}/{den2} of a mile. What fraction of the mile is he ahead?",
            f"A tank had {num1}/{den1} gallons of gas. After using {num2}/{den2} gallons, what fraction of a gallon remains?",
            f"Sarah measured {num1}/{den1} meters of ribbon. She cut off {num2}/{den2} meters. What fraction of a meter is left?"
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=fractions,
            operation='fraction_subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_measurement',
                'fractions': [f"{n}/{d}" for n, d in fractions],
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_word_problem_three_fractions(self, seed: Optional[int] = None) -> Problem:
        """
        Template 6: Word problem with three fractions.

        Uses real-world scenarios involving subtraction of three fractions.
        Example: Sarah had 5/6 of a cake, gave 1/3 to Maria and 1/4 to Tom.
        """
        if seed is not None:
            random.seed(seed)

        den_min, den_max = self.get_value_ranges()['denominator']

        # Generate three proper fractions with different denominators
        den1 = random.randint(max(den_min, 4), min(den_max, 12))
        den2 = random.randint(den_min, min(den_max, 12))
        den3 = random.randint(den_min, min(den_max, 12))

        # Ensure at least two denominators are different
        while den1 == den2 == den3:
            den2 = random.randint(den_min, min(den_max, 12))

        # Generate proper fractions
        num1 = random.randint(max(2, den1 // 2), den1 - 1)  # Make first relatively large
        num2 = random.randint(1, den2 - 1)
        num3 = random.randint(1, den3 - 1)

        # Simplify fractions
        num1, den1 = self._simplify_fraction(num1, den1)
        num2, den2 = self._simplify_fraction(num2, den2)
        num3, den3 = self._simplify_fraction(num3, den3)

        fractions = [(num1, den1), (num2, den2), (num3, den3)]

        # Calculate correct answer
        from math import gcd
        def lcm(a, b):
            return abs(a * b) // gcd(a, b)

        def lcm_multiple(numbers):
            result = numbers[0]
            for i in range(1, len(numbers)):
                result = lcm(result, numbers[i])
            return result

        common_den = lcm_multiple([den1, den2, den3])
        converted_num1 = num1 * (common_den // den1)
        converted_num2 = num2 * (common_den // den2)
        converted_num3 = num3 * (common_den // den3)
        result_num = converted_num1 - converted_num2 - converted_num3
        correct_num, correct_den = self._simplify_fraction(result_num, common_den)
        correct_answer = f"{correct_num}/{correct_den}"

        # Calculate malrule answer (subtract across all three)
        malrule_num = num1 - num2 - num3
        malrule_den = den1 - den2 - den3
        if malrule_den == 0:
            malrule_answer = f"{malrule_num}/0"
        elif malrule_den < 0:
            malrule_num = -malrule_num
            malrule_den = -malrule_den
            mal_num, mal_den = self._simplify_fraction(malrule_num, malrule_den)
            malrule_answer = f"{mal_num}/{mal_den}"
        else:
            mal_num, mal_den = self._simplify_fraction(malrule_num, malrule_den)
            malrule_answer = f"{mal_num}/{mal_den}"

        # Generate word problem
        contexts = [
            f"Sarah had {num1}/{den1} of a cake. She gave {num2}/{den2} to Maria and {num3}/{den3} to Tom. What fraction of the cake does Sarah have left?",
            f"A water tank was {num1}/{den1} full. In the morning, {num2}/{den2} was used, and in the evening, {num3}/{den3} more was used. What fraction of the tank is still full?",
            f"Tom had {num1}/{den1} of his allowance saved. He spent {num2}/{den2} on a book and {num3}/{den3} on snacks. What fraction of his allowance does he have remaining?",
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=fractions,
            operation='fraction_subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_three_fractions',
                'fractions': [f"{n}/{d}" for n, d in fractions],
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_word_problem_improper(self, seed: Optional[int] = None) -> Problem:
        """
        Template 7: Word problem with improper fractions.

        Uses real-world scenarios involving improper fractions (batches, laps, etc.).
        Example: A baker made 7/4 batches of cookies and gave away 5/3 batches.
        """
        if seed is not None:
            random.seed(seed)

        den_min, den_max = self.get_value_ranges()['denominator']

        # Generate improper fractions
        den1 = random.randint(den_min, min(den_max, 10))
        den2 = random.randint(den_min, min(den_max, 10))

        # Ensure denominators are different
        while den2 == den1:
            den2 = random.randint(den_min, min(den_max, 10))

        # Generate improper fractions
        num1 = random.randint(den1 + 1, den1 * 3)  # Improper, at least den1+1
        num2 = random.randint(den2, den2 * 2)  # Improper, up to 2*den2

        # Ensure first fraction is larger
        if num1 / den1 <= num2 / den2:
            num1, den1, num2, den2 = num2, den2, num1, den1

        # Simplify fractions
        num1, den1 = self._simplify_fraction(num1, den1)
        num2, den2 = self._simplify_fraction(num2, den2)

        fractions = [(num1, den1), (num2, den2)]

        # Calculate correct answer
        from math import gcd
        def lcm(a, b):
            return abs(a * b) // gcd(a, b)

        common_den = lcm(den1, den2)
        converted_num1 = num1 * (common_den // den1)
        converted_num2 = num2 * (common_den // den2)
        result_num = converted_num1 - converted_num2
        correct_num, correct_den = self._simplify_fraction(result_num, common_den)
        correct_answer = f"{correct_num}/{correct_den}"

        # Calculate malrule answer
        malrule_num = num1 - num2
        malrule_den = den1 - den2
        if malrule_den == 0:
            malrule_answer = f"{malrule_num}/0"
        elif malrule_den < 0:
            malrule_num = -malrule_num
            malrule_den = -malrule_den
            mal_num, mal_den = self._simplify_fraction(malrule_num, malrule_den)
            malrule_answer = f"{mal_num}/{mal_den}"
        else:
            mal_num, mal_den = self._simplify_fraction(malrule_num, malrule_den)
            malrule_answer = f"{mal_num}/{mal_den}"

        # Generate word problem with improper fractions
        contexts = [
            f"A baker made {num1}/{den1} batches of cookies in the morning and sold {num2}/{den2} batches. How many batches does the baker have left?",
            f"Maria ran {num1}/{den1} laps around the track, then slowed down and walked back {num2}/{den2} laps. What is her net forward progress in laps?",
            f"A container had {num1}/{den1} liters of juice. After pouring out {num2}/{den2} liters, how many liters remain?",
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=fractions,
            operation='fraction_subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_improper',
                'fractions': [f"{n}/{d}" for n, d in fractions],
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )
