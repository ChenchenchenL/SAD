"""
Problem generator for fraction addition malrule.

Generates fraction addition problems with different denominators.
"""

import random
from typing import Dict, Tuple, Optional
from math import gcd
import sys
sys.path.append('/home/user/malrule-coding')

from utils import Problem, ProblemGenerator, DifficultyLevel, create_fraction_template


class FractionAdditionProblemGenerator(ProblemGenerator):
    """
    Generates fraction addition problems.

    Problems use different denominators to elicit the malrule.
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

    def _lcm(self, a: int, b: int) -> int:
        """Calculate least common multiple."""
        return abs(a * b) // gcd(a, b)

    def _lcm_multiple(self, numbers: list) -> int:
        """Calculate LCM of multiple numbers."""
        result = numbers[0]
        for i in range(1, len(numbers)):
            result = self._lcm(result, numbers[i])
        return result

    def _calculate_correct_answer(self, fractions: list) -> str:
        """Calculate correct answer for fraction addition."""
        denominators = [d for _, d in fractions]
        common_den = self._lcm_multiple(denominators)

        # Convert all fractions and add numerators
        result_num = sum(n * (common_den // d) for n, d in fractions)

        # Simplify
        simplified_num, simplified_den = self._simplify_fraction(result_num, common_den)
        return f"{simplified_num}/{simplified_den}"

    def _calculate_malrule_answer(self, fractions: list) -> str:
        """Calculate malrule answer (add numerators and denominators)."""
        # MALRULE: Add all numerators and add all denominators
        result_num = sum(n for n, _ in fractions)
        result_den = sum(d for _, d in fractions)

        # Simplify the (incorrect) result
        simplified_num, simplified_den = self._simplify_fraction(result_num, result_den)
        return f"{simplified_num}/{simplified_den}"

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
            template = create_fraction_template('addition')
            num1, den1 = fractions[0]
            num2, den2 = fractions[1]
            return template.generate({
                'num1': num1, 'den1': den1,
                'num2': num2, 'den2': den2
            })

        elif problem_type == 'three_fractions':
            num1, den1 = fractions[0]
            num2, den2 = fractions[1]
            num3, den3 = fractions[2]
            contexts = [
                f"What is {num1}/{den1} + {num2}/{den2} + {num3}/{den3}?",
                f"Add {num1}/{den1}, {num2}/{den2}, and {num3}/{den3}.",
                f"Calculate: {num1}/{den1} + {num2}/{den2} + {num3}/{den3}",
                f"Find the sum: {num1}/{den1} + {num2}/{den2} + {num3}/{den3}",
            ]
            return random.choice(contexts)

        elif problem_type == 'word_problem':
            num1, den1 = fractions[0]
            num2, den2 = fractions[1]

            contexts = [
                f"Sarah ate {num1}/{den1} of a pizza and John ate {num2}/{den2} of the same pizza. What fraction of the pizza did they eat together?",
                f"A recipe calls for {num1}/{den1} cup of flour and {num2}/{den2} cup of sugar. How many cups of dry ingredients are needed in total?",
                f"Tom walked {num1}/{den1} of a mile to school and then {num2}/{den2} of a mile to the library. What total distance did he walk?",
                f"Maria completed {num1}/{den1} of her homework before dinner and {num2}/{den2} after dinner. What fraction of her homework is done?",
                f"A bottle was {num1}/{den1} full of juice. After adding {num2}/{den2} of a bottle more, how full is it now?",
                f"Jake painted {num1}/{den1} of the fence in the morning and {num2}/{den2} in the afternoon. What fraction of the fence is painted?",
            ]
            return random.choice(contexts)

        elif problem_type == 'word_problem_three_fractions':
            num1, den1 = fractions[0]
            num2, den2 = fractions[1]
            num3, den3 = fractions[2]

            contexts = [
                f"Sarah ate {num1}/{den1} of a pizza, John ate {num2}/{den2} of the pizza, and Emma ate {num3}/{den3} of the pizza. What fraction of the pizza did they eat in total?",
                f"A recipe requires {num1}/{den1} cup of flour, {num2}/{den2} cup of sugar, and {num3}/{den3} cup of oats. How many total cups of dry ingredients are needed?",
                f"Tom walked {num1}/{den1} of a mile to school, {num2}/{den2} of a mile to the library, and {num3}/{den3} of a mile to the park. What total distance did he walk?",
            ]
            return random.choice(contexts)

        elif problem_type == 'word_problem_improper':
            num1, den1 = fractions[0]
            num2, den2 = fractions[1]

            contexts = [
                f"A baker made {num1}/{den1} batches of cookies in the morning and {num2}/{den2} batches in the afternoon. How many batches did the baker make in total?",
                f"Maria ran {num1}/{den1} laps around the track and then ran {num2}/{den2} more laps. How many laps did she run altogether?",
                f"A container holds {num1}/{den1} liters of water and another holds {num2}/{den2} liters. If you combine them, how many liters do you have?",
            ]
            return random.choice(contexts)

        elif problem_type == 'word_problem_mixed':
            num1, den1 = fractions[0]
            num2, den2 = fractions[1]

            # Convert to mixed numbers for display
            if num1 >= den1:
                whole1 = num1 // den1
                frac_num1 = num1 % den1
                frac1_str = f"{whole1} {frac_num1}/{den1}" if frac_num1 > 0 else str(whole1)
            else:
                frac1_str = f"{num1}/{den1}"

            if num2 >= den2:
                whole2 = num2 // den2
                frac_num2 = num2 % den2
                frac2_str = f"{whole2} {frac_num2}/{den2}" if frac_num2 > 0 else str(whole2)
            else:
                frac2_str = f"{num2}/{den2}"

            contexts = [
                f"A carpenter used {frac1_str} boards for a shelf and {frac2_str} boards for a table. How many boards were used in total?",
                f"Emma spent {frac1_str} hours studying math and {frac2_str} hours studying science. How many hours did she study altogether?",
                f"A recipe needs {frac1_str} cups of milk and {frac2_str} cups of cream. How many total cups of liquid are needed?",
            ]
            return random.choice(contexts)

        elif problem_type == 'improper':
            # For improper fractions, use as-is (numerators can be >= denominators)
            num1, den1 = fractions[0]
            num2, den2 = fractions[1]
            contexts = [
                f"What is {num1}/{den1} + {num2}/{den2}?",
                f"Add {num1}/{den1} and {num2}/{den2}.",
                f"Calculate: {num1}/{den1} + {num2}/{den2}",
                f"Find the sum of {num1}/{den1} and {num2}/{den2}.",
            ]
            return random.choice(contexts)

        elif problem_type == 'mixed':
            # Convert to mixed numbers for display
            num1, den1 = fractions[0]
            num2, den2 = fractions[1]

            # Convert to mixed numbers if improper
            if num1 >= den1:
                whole1 = num1 // den1
                frac_num1 = num1 % den1
                frac1_str = f"{whole1} {frac_num1}/{den1}" if frac_num1 > 0 else str(whole1)
            else:
                frac1_str = f"{num1}/{den1}"

            if num2 >= den2:
                whole2 = num2 // den2
                frac_num2 = num2 % den2
                frac2_str = f"{whole2} {frac_num2}/{den2}" if frac_num2 > 0 else str(whole2)
            else:
                frac2_str = f"{num2}/{den2}"

            contexts = [
                f"What is {frac1_str} + {frac2_str}?",
                f"Add {frac1_str} and {frac2_str}.",
                f"Calculate: {frac1_str} + {frac2_str}",
                f"Find the sum of {frac1_str} and {frac2_str}.",
            ]
            return random.choice(contexts)

        else:
            # Default to basic
            template = create_fraction_template('addition')
            num1, den1 = fractions[0]
            num2, den2 = fractions[1]
            return template.generate({
                'num1': num1, 'den1': den1,
                'num2': num2, 'den2': den2
            })

    def generate(self, seed: Optional[int] = None) -> Problem:
        """
        Generate a fraction addition problem.

        Args:
            seed: Optional random seed for reproducibility

        Returns:
            Problem instance
        """
        if seed is not None:
            random.seed(seed)

        den_min, den_max = self.get_value_ranges()['denominator']

        # Choose problem type - now including word problem variants for all formula types
        problem_types = [
            'basic_two',
            'three_fractions',
            'word_problem',  # Basic two-fraction word problem
            'word_problem_three_fractions',  # NEW: Three-fraction word problem
            'improper',
            'word_problem_improper',  # NEW: Improper fraction word problem
            'mixed',
            'word_problem_mixed',  # NEW: Mixed number word problem
        ]

        # For level 5+, include more complex types with higher frequency
        if self.level >= 5:
            problem_types.extend([
                'three_fractions',
                'word_problem_three_fractions',
                'improper',
                'word_problem_improper',
                'mixed',
                'word_problem_mixed',
                'word_problem'
            ])

        problem_type = random.choice(problem_types)

        # Generate fractions based on problem type
        if problem_type in ['three_fractions', 'word_problem_three_fractions']:
            # Generate three fractions
            den1 = random.randint(den_min, min(den_max, 12))  # Keep reasonable for word problems
            den2 = random.randint(den_min, min(den_max, 12))
            den3 = random.randint(den_min, min(den_max, 12))

            # Ensure at least two denominators are different
            while den1 == den2 == den3:
                den2 = random.randint(den_min, min(den_max, 12))

            # Generate proper fractions
            num1 = random.randint(1, den1 - 1)
            num2 = random.randint(1, den2 - 1)
            num3 = random.randint(1, den3 - 1)

            # Simplify fractions
            num1, den1 = self._simplify_fraction(num1, den1)
            num2, den2 = self._simplify_fraction(num2, den2)
            num3, den3 = self._simplify_fraction(num3, den3)

            fractions = [(num1, den1), (num2, den2), (num3, den3)]

        elif problem_type in ['improper', 'mixed', 'word_problem_improper', 'word_problem_mixed']:
            # Generate improper fractions (numerator can be >= denominator)
            den1 = random.randint(den_min, min(den_max, 12))  # Keep denominators reasonable
            den2 = random.randint(den_min, min(den_max, 12))

            # Ensure denominators are different
            while den2 == den1:
                den2 = random.randint(den_min, min(den_max, 12))

            # Generate improper fractions
            num1 = random.randint(den1, den1 * 3)  # 1 to 3 times denominator
            num2 = random.randint(den2, den2 * 3)

            # Simplify fractions
            num1, den1 = self._simplify_fraction(num1, den1)
            num2, den2 = self._simplify_fraction(num2, den2)

            fractions = [(num1, den1), (num2, den2)]

        else:
            # Generate two proper fractions with different denominators
            # Handles: basic_two, word_problem
            den1 = random.randint(den_min, den_max)
            den2 = random.randint(den_min, den_max)

            # Ensure denominators are different to make malrule more apparent
            while den2 == den1:
                den2 = random.randint(den_min, den_max)

            # Generate numerators (proper fractions: numerator < denominator)
            num1 = random.randint(1, den1 - 1)
            num2 = random.randint(1, den2 - 1)

            # Simplify fractions
            num1, den1 = self._simplify_fraction(num1, den1)
            num2, den2 = self._simplify_fraction(num2, den2)

            fractions = [(num1, den1), (num2, den2)]

        # Calculate correct and malrule answers
        correct_answer = self._calculate_correct_answer(fractions)
        malrule_answer = self._calculate_malrule_answer(fractions)

        # Generate problem text
        problem_text = self._generate_problem_text(fractions, problem_type)

        return Problem(
            text=problem_text,
            operands=fractions,
            operation='fraction_addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'problem_type': problem_type,
                'num_fractions': len(fractions),
                'fractions': [f"{n}/{d}" for n, d in fractions],
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )
