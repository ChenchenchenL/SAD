"""
Problem generator for Each-Fraction-Digit-Is-Ratio malrule.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, List, Optional
from math import gcd
from utils import ProblemGenerator, Problem, DifficultyLevel


class EachFractionDigitIsRatioProblemGenerator(ProblemGenerator):
    """Generates ratio simplification problems with multi-digit numbers."""

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_two_digit',
            'three_digit_ratios',
            'mismatched_lengths',
            'with_zeros',
            'word_problem_context'
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        ranges = {
            6: {
                DifficultyLevel.EASY: {'min_num': 10, 'max_num': 49, 'min_den': 10, 'max_den': 49},
                DifficultyLevel.MEDIUM: {'min_num': 10, 'max_num': 69, 'min_den': 10, 'max_den': 69},
                DifficultyLevel.HARD: {'min_num': 10, 'max_num': 89, 'min_den': 10, 'max_den': 89}
            },
            7: {
                DifficultyLevel.EASY: {'min_num': 10, 'max_num': 69, 'min_den': 10, 'max_den': 69},
                DifficultyLevel.MEDIUM: {'min_num': 10, 'max_num': 89, 'min_den': 10, 'max_den': 89},
                DifficultyLevel.HARD: {'min_num': 10, 'max_num': 99, 'min_den': 10, 'max_den': 99}
            },
            8: {
                DifficultyLevel.EASY: {'min_num': 10, 'max_num': 79, 'min_den': 10, 'max_den': 79},
                DifficultyLevel.MEDIUM: {'min_num': 10, 'max_num': 99, 'min_den': 10, 'max_den': 99},
                DifficultyLevel.HARD: {'min_num': 10, 'max_num': 99, 'min_den': 10, 'max_den': 99}
            }
        }
        lvl = self.level if self.level in ranges else 7
        return ranges[lvl][self.difficulty]

    def generate(self, seed=None, template: Optional[str] = None) -> Problem:
        """
        Generate a ratio simplification problem based on selected template.

        Args:
            seed: Optional random seed for reproducibility
            template: Specific template to use, or None for random selection

        Returns:
            Problem testing understanding of multi-digit ratio simplification
        """
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            template = random.choice(self.get_available_templates())

        # Generate based on template
        if template == 'basic_two_digit':
            return self._generate_basic_two_digit(seed)
        elif template == 'three_digit_ratios':
            return self._generate_three_digit_ratios(seed)
        elif template == 'mismatched_lengths':
            return self._generate_mismatched_lengths(seed)
        elif template == 'with_zeros':
            return self._generate_with_zeros(seed)
        elif template == 'word_problem_context':
            return self._generate_word_problem_context(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_two_digit(self, seed=None) -> Problem:
        """Generate basic two-digit ratio simplification problem."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()

        # Generate ratio that can be simplified (has common factor > 1)
        # We'll generate a simplified ratio first, then multiply both by a common factor
        attempts = 0
        max_attempts = 50

        while attempts < max_attempts:
            # Generate a multiplier to ensure the ratio can be simplified
            multiplier = random.randint(2, 5)

            # Generate base values
            base_num = random.randint(ranges['min_num'] // multiplier, ranges['max_num'] // multiplier)
            base_den = random.randint(ranges['min_den'] // multiplier, ranges['max_den'] // multiplier)

            # Ensure base values are coprime (GCD = 1) for cleaner problems
            if gcd(base_num, base_den) == 1 and base_num != base_den:
                numerator = base_num * multiplier
                denominator = base_den * multiplier

                # Ensure both are 2-digit numbers
                if numerator >= 10 and denominator >= 10:
                    # Ensure they're not equal (trivial case)
                    if numerator != denominator:
                        # Calculate correct simplified form
                        ratio_gcd = gcd(numerator, denominator)
                        simplified_num = numerator // ratio_gcd
                        simplified_den = denominator // ratio_gcd

                        # Calculate malrule answer (digit-by-digit simplification)
                        malrule_result = self._calculate_malrule_answer(numerator, denominator)

                        # Ensure malrule gives different answer than correct
                        if (malrule_result['num'] != simplified_num or
                            malrule_result['den'] != simplified_den):
                            break

            attempts += 1

        # Fallback if we couldn't generate a good problem
        if attempts >= max_attempts:
            numerator = 12
            denominator = 34
            ratio_gcd = gcd(numerator, denominator)
            simplified_num = numerator // ratio_gcd
            simplified_den = denominator // ratio_gcd
            malrule_result = self._calculate_malrule_answer(numerator, denominator)

        text = f"Simplify the ratio {numerator}:{denominator}"

        return Problem(
            text=text,
            operands=[numerator, denominator],
            operation='ratio_simplification',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'numerator': numerator,
                'denominator': denominator,
                'correct_num': simplified_num,
                'correct_den': simplified_den,
                'malrule_num': malrule_result['num'],
                'malrule_den': malrule_result['den'],
                'template': 'basic_two_digit'
            }
        )

    def _generate_three_digit_ratios(self, seed=None) -> Problem:
        """Generate three-digit ratio simplification problem."""
        if seed is not None:
            random.seed(seed)

        # Generate 3-digit ratios
        attempts = 0
        max_attempts = 50

        while attempts < max_attempts:
            multiplier = random.randint(2, 4)

            # Generate base values for 3-digit numbers
            base_num = random.randint(100 // multiplier, 999 // multiplier)
            base_den = random.randint(100 // multiplier, 999 // multiplier)

            if gcd(base_num, base_den) == 1 and base_num != base_den:
                numerator = base_num * multiplier
                denominator = base_den * multiplier

                # Ensure both are 3-digit numbers
                if numerator >= 100 and denominator >= 100 and numerator <= 999 and denominator <= 999:
                    ratio_gcd = gcd(numerator, denominator)
                    simplified_num = numerator // ratio_gcd
                    simplified_den = denominator // ratio_gcd

                    malrule_result = self._calculate_malrule_answer(numerator, denominator)

                    # Ensure malrule gives different answer than correct
                    if (malrule_result['num'] != simplified_num or
                        malrule_result['den'] != simplified_den):
                        break

            attempts += 1

        # Fallback
        if attempts >= max_attempts:
            numerator = 246
            denominator = 369
            ratio_gcd = gcd(numerator, denominator)
            simplified_num = numerator // ratio_gcd
            simplified_den = denominator // ratio_gcd
            malrule_result = self._calculate_malrule_answer(numerator, denominator)

        text = f"Simplify the ratio {numerator}:{denominator}"

        return Problem(
            text=text,
            operands=[numerator, denominator],
            operation='ratio_simplification',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'numerator': numerator,
                'denominator': denominator,
                'correct_num': simplified_num,
                'correct_den': simplified_den,
                'malrule_num': malrule_result['num'],
                'malrule_den': malrule_result['den'],
                'template': 'three_digit_ratios'
            }
        )

    def _generate_mismatched_lengths(self, seed=None) -> Problem:
        """Generate ratio with mismatched digit lengths (e.g., 12:345)."""
        if seed is not None:
            random.seed(seed)

        # Generate one 2-digit and one 3-digit number
        attempts = 0
        max_attempts = 50

        while attempts < max_attempts:
            multiplier = random.randint(2, 4)

            # Randomly choose which is longer
            if random.choice([True, False]):
                # numerator is 2-digit, denominator is 3-digit
                base_num = random.randint(10 // multiplier, 99 // multiplier)
                base_den = random.randint(100 // multiplier, 999 // multiplier)
            else:
                # numerator is 3-digit, denominator is 2-digit
                base_num = random.randint(100 // multiplier, 999 // multiplier)
                base_den = random.randint(10 // multiplier, 99 // multiplier)

            if gcd(base_num, base_den) == 1 and base_num != base_den:
                numerator = base_num * multiplier
                denominator = base_den * multiplier

                ratio_gcd = gcd(numerator, denominator)
                simplified_num = numerator // ratio_gcd
                simplified_den = denominator // ratio_gcd

                malrule_result = self._calculate_malrule_answer(numerator, denominator)

                # Ensure malrule gives different answer than correct
                if (malrule_result['num'] != simplified_num or
                    malrule_result['den'] != simplified_den):
                    break

            attempts += 1

        # Fallback
        if attempts >= max_attempts:
            numerator = 12
            denominator = 345
            ratio_gcd = gcd(numerator, denominator)
            simplified_num = numerator // ratio_gcd
            simplified_den = denominator // ratio_gcd
            malrule_result = self._calculate_malrule_answer(numerator, denominator)

        text = f"Simplify the ratio {numerator}:{denominator}"

        return Problem(
            text=text,
            operands=[numerator, denominator],
            operation='ratio_simplification',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'numerator': numerator,
                'denominator': denominator,
                'correct_num': simplified_num,
                'correct_den': simplified_den,
                'malrule_num': malrule_result['num'],
                'malrule_den': malrule_result['den'],
                'template': 'mismatched_lengths'
            }
        )

    def _generate_with_zeros(self, seed=None) -> Problem:
        """Generate ratio with zeros in the digits (e.g., 120:340)."""
        if seed is not None:
            random.seed(seed)

        # Generate ratios with zeros, but ensure they're simplifiable
        attempts = 0
        max_attempts = 50

        while attempts < max_attempts:
            multiplier = random.randint(2, 5)

            # Generate numbers with zeros (multiples of 10)
            base_num = random.randint(10, 99)
            base_den = random.randint(10, 99)

            # Multiply one or both by 10 to introduce zeros
            if random.choice([True, False]):
                numerator = base_num * 10 * multiplier
                denominator = base_den * multiplier
            else:
                numerator = base_num * multiplier
                denominator = base_den * 10 * multiplier

            if gcd(base_num, base_den) == 1 and base_num != base_den:
                if numerator >= 10 and denominator >= 10:
                    ratio_gcd = gcd(numerator, denominator)
                    simplified_num = numerator // ratio_gcd
                    simplified_den = denominator // ratio_gcd

                    malrule_result = self._calculate_malrule_answer(numerator, denominator)

                    # Ensure malrule gives different answer than correct
                    if (malrule_result['num'] != simplified_num or
                        malrule_result['den'] != simplified_den):
                        break

            attempts += 1

        # Fallback
        if attempts >= max_attempts:
            numerator = 120
            denominator = 340
            ratio_gcd = gcd(numerator, denominator)
            simplified_num = numerator // ratio_gcd
            simplified_den = denominator // ratio_gcd
            malrule_result = self._calculate_malrule_answer(numerator, denominator)

        text = f"Simplify the ratio {numerator}:{denominator}"

        return Problem(
            text=text,
            operands=[numerator, denominator],
            operation='ratio_simplification',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'numerator': numerator,
                'denominator': denominator,
                'correct_num': simplified_num,
                'correct_den': simplified_den,
                'malrule_num': malrule_result['num'],
                'malrule_den': malrule_result['den'],
                'template': 'with_zeros'
            }
        )

    def _generate_word_problem_context(self, seed=None) -> Problem:
        """Generate word problem requiring ratio simplification."""
        if seed is not None:
            random.seed(seed)

        # Generate simplifiable ratio
        attempts = 0
        max_attempts = 50

        while attempts < max_attempts:
            multiplier = random.randint(2, 5)
            base_num = random.randint(10, 99)
            base_den = random.randint(10, 99)

            if gcd(base_num, base_den) == 1 and base_num != base_den:
                numerator = base_num * multiplier
                denominator = base_den * multiplier

                if numerator >= 10 and denominator >= 10:
                    ratio_gcd = gcd(numerator, denominator)
                    simplified_num = numerator // ratio_gcd
                    simplified_den = denominator // ratio_gcd

                    malrule_result = self._calculate_malrule_answer(numerator, denominator)

                    if (malrule_result['num'] != simplified_num or
                        malrule_result['den'] != simplified_den):
                        break

            attempts += 1

        # Fallback
        if attempts >= max_attempts:
            numerator = 18
            denominator = 24
            ratio_gcd = gcd(numerator, denominator)
            simplified_num = numerator // ratio_gcd
            simplified_den = denominator // ratio_gcd
            malrule_result = self._calculate_malrule_answer(numerator, denominator)

        # Create different word problem contexts
        contexts = [
            {
                'type': 'recipe',
                'text': f"A recipe calls for {numerator} grams of flour and {denominator} grams of sugar. Write the simplified ratio of flour to sugar.",
                'context_desc': 'recipe proportions'
            },
            {
                'type': 'map_scale',
                'text': f"On a map, {numerator} centimeters represents {denominator} kilometers. Write the simplified ratio of map distance to actual distance.",
                'context_desc': 'map scale'
            },
            {
                'type': 'mixture',
                'text': f"A paint mixture combines {numerator} ml of red paint with {denominator} ml of blue paint. Simplify the ratio of red to blue paint.",
                'context_desc': 'paint mixture'
            },
            {
                'type': 'class_ratio',
                'text': f"A class has {numerator} students who prefer math and {denominator} students who prefer science. Write the simplified ratio of math to science preferences.",
                'context_desc': 'student preferences'
            }
        ]

        context = random.choice(contexts)
        text = context['text']

        return Problem(
            text=text,
            operands=[numerator, denominator],
            operation='ratio_simplification',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'numerator': numerator,
                'denominator': denominator,
                'correct_num': simplified_num,
                'correct_den': simplified_den,
                'malrule_num': malrule_result['num'],
                'malrule_den': malrule_result['den'],
                'context_type': context['type'],
                'context_desc': context['context_desc'],
                'template': 'word_problem_context'
            }
        )

    def _calculate_malrule_answer(self, numerator: int, denominator: int) -> Dict[str, int]:
        """
        Calculate the malrule answer by treating each digit pair as a separate ratio.

        For example: 12/34
        - First digit pair: 1/3 (can't simplify) → 1/3
        - Second digit pair: 2/4 (simplifies to 1/2) → 1/2
        - Concatenate: 11/32
        """
        num_str = str(numerator)
        den_str = str(denominator)

        # Pad to same length with leading zeros if needed
        max_len = max(len(num_str), len(den_str))
        num_str = num_str.zfill(max_len)
        den_str = den_str.zfill(max_len)

        result_num_digits = []
        result_den_digits = []

        # Process each digit pair
        for i in range(max_len):
            digit_num = int(num_str[i])
            digit_den = int(den_str[i])

            # Avoid division by zero
            if digit_den == 0:
                digit_den = 1  # Student might substitute 1 for 0

            # Find GCD of this digit pair
            if digit_num == 0:
                # 0/x = 0/1
                result_num_digits.append(0)
                result_den_digits.append(1)
            else:
                digit_gcd = gcd(digit_num, digit_den)
                simplified_digit_num = digit_num // digit_gcd
                simplified_digit_den = digit_den // digit_gcd
                result_num_digits.append(simplified_digit_num)
                result_den_digits.append(simplified_digit_den)

        # Concatenate digits to form final numbers
        malrule_num = int(''.join(str(d) for d in result_num_digits))
        malrule_den = int(''.join(str(d) for d in result_den_digits))

        return {'num': malrule_num, 'den': malrule_den}
