"""
Problem generator for Ignore-Denominators malrule.

Generates fraction addition and subtraction problems that elicit
the misconception of ignoring denominators.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional
from math import gcd
from utils import ProblemGenerator, Problem, DifficultyLevel


class IgnoreDenominatorsProblemGenerator(ProblemGenerator):
    """
    Generates fraction problems with different denominators.

    Creates addition and subtraction problems where students might
    ignore denominators and only operate on numerators.
    """

    def get_name(self) -> str:
        return "Ignore-Denominators Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates fraction addition/subtraction problems to elicit "
            "the misconception of ignoring denominators."
        )

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level."""
        ranges = {
            4: {
                DifficultyLevel.EASY: {'numerator': (1, 5), 'denominator': (2, 6)},
                DifficultyLevel.MEDIUM: {'numerator': (1, 10), 'denominator': (2, 10)},
                DifficultyLevel.HARD: {'numerator': (1, 12), 'denominator': (2, 12)},
            },
            5: {
                DifficultyLevel.EASY: {'numerator': (1, 8), 'denominator': (2, 8)},
                DifficultyLevel.MEDIUM: {'numerator': (1, 12), 'denominator': (2, 12)},
                DifficultyLevel.HARD: {'numerator': (1, 20), 'denominator': (2, 20)},
            },
            6: {
                DifficultyLevel.EASY: {'numerator': (1, 10), 'denominator': (2, 12)},
                DifficultyLevel.MEDIUM: {'numerator': (1, 15), 'denominator': (2, 15)},
                DifficultyLevel.HARD: {'numerator': (1, 25), 'denominator': (2, 25)},
            },
            7: {
                DifficultyLevel.EASY: {'numerator': (1, 12), 'denominator': (2, 15)},
                DifficultyLevel.MEDIUM: {'numerator': (1, 20), 'denominator': (2, 20)},
                DifficultyLevel.HARD: {'numerator': (1, 30), 'denominator': (2, 30)},
            }
        }

        lvl = self.level if self.level in ranges else 5
        return ranges[lvl][self.difficulty]

    def generate(self, seed: Optional[int] = None) -> Problem:
        """
        Generate a fraction problem across all operations.

        Args:
            seed: Optional random seed for reproducibility

        Returns:
            Problem instance
        """
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        num_min, num_max = ranges['numerator']
        den_min, den_max = ranges['denominator']

        # Choose template
        templates = [
            'basic_addition',
            'basic_subtraction',
            'multiplication',
            'division',
            'word_problem',
            'word_problem_multiplication',
            'word_problem_division'
        ]
        template = random.choice(templates)

        if template == 'basic_addition':
            # Original: basic addition a/b + c/d
            num1 = random.randint(num_min, num_max)
            den1 = random.randint(den_min, den_max)

            # Ensure proper fraction for EASY
            if self.difficulty == DifficultyLevel.EASY and num1 >= den1:
                num1 = random.randint(num_min, den1 - 1) if den1 > 1 else 1

            # Generate second fraction with DIFFERENT denominator
            den2 = random.randint(den_min, den_max)
            attempts = 0
            while den2 == den1 and attempts < 10:
                den2 = random.randint(den_min, den_max)
                attempts += 1

            num2 = random.randint(num_min, num_max)
            if self.difficulty == DifficultyLevel.EASY and num2 >= den2:
                num2 = random.randint(num_min, den2 - 1) if den2 > 1 else 1

            # Calculate correct answer
            common_den = (den1 * den2) // gcd(den1, den2)
            new_num1 = num1 * (common_den // den1)
            new_num2 = num2 * (common_den // den2)
            result_num = new_num1 + new_num2
            result_den = common_den

            # Simplify result
            result_gcd = gcd(result_num, result_den)
            result_num //= result_gcd
            result_den //= result_gcd

            problem_text = f"Calculate: {num1}/{den1} + {num2}/{den2}"

            return Problem(
                text=problem_text,
                operands=[num1, den1, num2, den2],
                operation='fraction_addition',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'num1': num1,
                    'den1': den1,
                    'num2': num2,
                    'den2': den2,
                    'operation': 'addition',
                    'result_num': result_num,
                    'result_den': result_den,
                    'correct_answer': f"{result_num}/{result_den}",
                    'template': template
                }
            )

        elif template == 'basic_subtraction':
            # Subtraction: a/b - c/d
            num1 = random.randint(num_min, num_max)
            den1 = random.randint(den_min, den_max)

            if self.difficulty == DifficultyLevel.EASY and num1 >= den1:
                num1 = random.randint(num_min, den1 - 1) if den1 > 1 else 1

            den2 = random.randint(den_min, den_max)
            attempts = 0
            while den2 == den1 and attempts < 10:
                den2 = random.randint(den_min, den_max)
                attempts += 1

            num2 = random.randint(num_min, num_max)
            if self.difficulty == DifficultyLevel.EASY and num2 >= den2:
                num2 = random.randint(num_min, den2 - 1) if den2 > 1 else 1

            # Ensure num1/den1 > num2/den2 to avoid negative results
            if (num1 * den2) < (num2 * den1):
                num1, num2 = num2, num1
                den1, den2 = den2, den1

            # Calculate correct answer
            common_den = (den1 * den2) // gcd(den1, den2)
            new_num1 = num1 * (common_den // den1)
            new_num2 = num2 * (common_den // den2)
            result_num = new_num1 - new_num2
            result_den = common_den

            # Simplify result
            result_gcd = gcd(abs(result_num), result_den)
            result_num //= result_gcd
            result_den //= result_gcd

            problem_text = f"Calculate: {num1}/{den1} - {num2}/{den2}"

            return Problem(
                text=problem_text,
                operands=[num1, den1, num2, den2],
                operation='fraction_subtraction',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'num1': num1,
                    'den1': den1,
                    'num2': num2,
                    'den2': den2,
                    'operation': 'subtraction',
                    'result_num': result_num,
                    'result_den': result_den,
                    'correct_answer': f"{result_num}/{result_den}",
                    'template': template
                }
            )

        elif template == 'multiplication':
            # Multiplication: a/b × c/d
            num1 = random.randint(num_min, min(num_max, 10))
            den1 = random.randint(den_min, min(den_max, 10))
            num2 = random.randint(num_min, min(num_max, 10))
            den2 = random.randint(den_min, min(den_max, 10))

            # Ensure denominators are different
            attempts = 0
            while den2 == den1 and attempts < 10:
                den2 = random.randint(den_min, min(den_max, 10))
                attempts += 1

            # Calculate correct answer
            result_num = num1 * num2
            result_den = den1 * den2

            # Simplify result
            result_gcd = gcd(result_num, result_den)
            result_num //= result_gcd
            result_den //= result_gcd

            problem_text = f"Calculate: {num1}/{den1} × {num2}/{den2}"

            return Problem(
                text=problem_text,
                operands=[num1, den1, num2, den2],
                operation='fraction_multiplication',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'num1': num1,
                    'den1': den1,
                    'num2': num2,
                    'den2': den2,
                    'operation': 'multiplication',
                    'result_num': result_num,
                    'result_den': result_den,
                    'correct_answer': f"{result_num}/{result_den}",
                    'template': template
                }
            )

        elif template == 'division':
            # Division: a/b ÷ c/d
            num1 = random.randint(num_min, min(num_max, 10))
            den1 = random.randint(den_min, min(den_max, 10))
            num2 = random.randint(max(1, num_min), min(num_max, 10))  # Avoid dividing by zero
            den2 = random.randint(den_min, min(den_max, 10))

            # Ensure denominators are different
            attempts = 0
            while den2 == den1 and attempts < 10:
                den2 = random.randint(den_min, min(den_max, 10))
                attempts += 1

            # Calculate correct answer: (a/b) ÷ (c/d) = (a/b) × (d/c) = (a×d)/(b×c)
            result_num = num1 * den2
            result_den = den1 * num2

            # Simplify result
            result_gcd = gcd(result_num, result_den)
            result_num //= result_gcd
            result_den //= result_gcd

            problem_text = f"Calculate: {num1}/{den1} ÷ {num2}/{den2}"

            return Problem(
                text=problem_text,
                operands=[num1, den1, num2, den2],
                operation='fraction_division',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'num1': num1,
                    'den1': den1,
                    'num2': num2,
                    'den2': den2,
                    'operation': 'division',
                    'result_num': result_num,
                    'result_den': result_den,
                    'correct_answer': f"{result_num}/{result_den}",
                    'template': template
                }
            )

        elif template == 'word_problem':
            # Word problem contexts
            contexts = [
                ('pizza', 'addition', 'Maria ate {num1}/{den1} of a pizza and John ate {num2}/{den2} of the pizza. What fraction of the pizza did they eat in total?'),
                ('recipe', 'addition', 'A recipe calls for {num1}/{den1} cup of sugar and {num2}/{den2} cup of flour. How many cups of ingredients in total?'),
                ('distance', 'subtraction', 'A hiking trail is {num1}/{den1} mile long. After walking {num2}/{den2} mile, what fraction of the trail remains?'),
                ('time', 'subtraction', 'A task takes {num1}/{den1} hour. If {num2}/{den2} hour has passed, what fraction of an hour remains?')
            ]
            context, operation, problem_template = random.choice(contexts)

            # Generate fractions
            num1 = random.randint(num_min, min(num_max, 8))
            den1 = random.randint(den_min, min(den_max, 8))
            num2 = random.randint(num_min, min(num_max, 8))
            den2 = random.randint(den_min, min(den_max, 8))

            # Ensure different denominators
            attempts = 0
            while den2 == den1 and attempts < 10:
                den2 = random.randint(den_min, min(den_max, 8))
                attempts += 1

            # For subtraction, ensure num1/den1 > num2/den2
            if operation == 'subtraction':
                if (num1 * den2) < (num2 * den1):
                    num1, num2 = num2, num1
                    den1, den2 = den2, den1

            # Calculate correct answer
            if operation == 'addition':
                common_den = (den1 * den2) // gcd(den1, den2)
                new_num1 = num1 * (common_den // den1)
                new_num2 = num2 * (common_den // den2)
                result_num = new_num1 + new_num2
                result_den = common_den
            else:  # subtraction
                common_den = (den1 * den2) // gcd(den1, den2)
                new_num1 = num1 * (common_den // den1)
                new_num2 = num2 * (common_den // den2)
                result_num = new_num1 - new_num2
                result_den = common_den

            # Simplify result
            result_gcd = gcd(abs(result_num), result_den)
            result_num //= result_gcd
            result_den //= result_gcd

            problem_text = problem_template.format(num1=num1, den1=den1, num2=num2, den2=den2)

            return Problem(
                text=problem_text,
                operands=[num1, den1, num2, den2],
                operation=f'fraction_{operation}',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'num1': num1,
                    'den1': den1,
                    'num2': num2,
                    'den2': den2,
                    'operation': operation,
                    'result_num': result_num,
                    'result_den': result_den,
                    'correct_answer': f"{result_num}/{result_den}",
                    'template': template,
                    'context': context
                }
            )

        elif template == 'word_problem_multiplication':
            # Word problem for multiplication
            num1 = random.randint(num_min, min(num_max, 10))
            den1 = random.randint(den_min, min(den_max, 10))
            num2 = random.randint(num_min, min(num_max, 10))
            den2 = random.randint(den_min, min(den_max, 10))

            # Ensure denominators are different
            attempts = 0
            while den2 == den1 and attempts < 10:
                den2 = random.randint(den_min, min(den_max, 10))
                attempts += 1

            # Calculate correct answer
            result_num = num1 * num2
            result_den = den1 * den2

            # Simplify result
            result_gcd = gcd(result_num, result_den)
            result_num //= result_gcd
            result_den //= result_gcd

            # Calculate malrule answer: ignore denominators, multiply only numerators
            malrule_num = num1 * num2
            malrule_den = 1  # Treats result as whole number

            contexts = [
                f"A recipe calls for {num1}/{den1} cup of flour per batch. If you make {num2}/{den2} of a batch, how much flour do you need (in cups)?",
                f"A ribbon is {num1}/{den1} meter long. You need {num2}/{den2} of that length for a project. How long is the piece you need (in meters)?",
                f"A tank can hold {num1}/{den1} gallon of water. Currently it is {num2}/{den2} full. How many gallons of water are in the tank?"
            ]
            problem_text = random.choice(contexts)

            return Problem(
                text=problem_text,
                operands=[num1, den1, num2, den2],
                operation='fraction_multiplication',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'num1': num1,
                    'den1': den1,
                    'num2': num2,
                    'den2': den2,
                    'operation': 'multiplication',
                    'result_num': result_num,
                    'result_den': result_den,
                    'correct_answer': f"{result_num}/{result_den}",
                    'malrule_answer': f"{malrule_num}",
                    'template': template
                }
            )

        elif template == 'word_problem_division':
            # Word problem for division
            num1 = random.randint(num_min, min(num_max, 10))
            den1 = random.randint(den_min, min(den_max, 10))
            num2 = random.randint(max(1, num_min), min(num_max, 10))  # Avoid dividing by zero
            den2 = random.randint(den_min, min(den_max, 10))

            # Ensure denominators are different
            attempts = 0
            while den2 == den1 and attempts < 10:
                den2 = random.randint(den_min, min(den_max, 10))
                attempts += 1

            # Calculate correct answer: (a/b) ÷ (c/d) = (a/b) × (d/c) = (a×d)/(b×c)
            result_num = num1 * den2
            result_den = den1 * num2

            # Simplify result
            result_gcd = gcd(result_num, result_den)
            result_num //= result_gcd
            result_den //= result_gcd

            # Calculate malrule answer: ignore denominators, divide only numerators
            malrule_num = num1 // num2 if num1 >= num2 else 0  # Integer division, treating as whole numbers
            if malrule_num == 0:
                malrule_num = 1  # Avoid zero in answer
            malrule_den = 1  # Treats result as whole number

            contexts = [
                f"You have {num1}/{den1} of a pizza. If you divide it equally among {num2}/{den2} groups, how much pizza does each group get?",
                f"A rope is {num1}/{den1} meter long. You need to cut pieces that are each {num2}/{den2} meter. How many full pieces can you cut?",
                f"A container has {num1}/{den1} liter of juice. If each serving is {num2}/{den2} liter, how many servings can you make?"
            ]
            problem_text = random.choice(contexts)

            return Problem(
                text=problem_text,
                operands=[num1, den1, num2, den2],
                operation='fraction_division',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'num1': num1,
                    'den1': den1,
                    'num2': num2,
                    'den2': den2,
                    'operation': 'division',
                    'result_num': result_num,
                    'result_den': result_den,
                    'correct_answer': f"{result_num}/{result_den}",
                    'malrule_answer': f"{malrule_num}",
                    'template': template
                }
            )
