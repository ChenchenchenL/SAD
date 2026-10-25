"""
Problem generator for Common-Denominator-Numerator malrule.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
import math
from typing import Dict, Tuple, List, Optional
from utils import ProblemGenerator, Problem, DifficultyLevel


class CommonDenominatorNumeratorProblemGenerator(ProblemGenerator):
    """Generates fraction addition problems."""

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_addition',
            'word_problem_context',
            'three_fractions',
            'word_problem_three_fractions',
            'visual_representation',
            'comparison_problem'
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        ranges = {
            5: {DifficultyLevel.EASY: (2, 6), DifficultyLevel.MEDIUM: (2, 10), DifficultyLevel.HARD: (2, 12)},
            6: {DifficultyLevel.EASY: (2, 8), DifficultyLevel.MEDIUM: (2, 12), DifficultyLevel.HARD: (2, 15)},
            7: {DifficultyLevel.EASY: (2, 10), DifficultyLevel.MEDIUM: (2, 15), DifficultyLevel.HARD: (2, 20)},
        }
        lvl = self.level if self.level in ranges else 6
        return {'denominators': ranges[lvl][self.difficulty]}

    def generate(self, seed=None, template: Optional[str] = None) -> Problem:
        """
        Generate a fraction addition problem.

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
        if template == 'basic_addition':
            return self._generate_basic_addition(seed)
        elif template == 'word_problem_context':
            return self._generate_word_problem_context(seed)
        elif template == 'three_fractions':
            return self._generate_three_fractions(seed)
        elif template == 'word_problem_three_fractions':
            return self._generate_word_problem_three_fractions(seed)
        elif template == 'visual_representation':
            return self._generate_visual_representation(seed)
        elif template == 'comparison_problem':
            return self._generate_comparison_problem(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_addition(self, seed=None) -> Problem:
        """Template 1: Basic fraction addition with different denominators."""
        if seed is not None:
            random.seed(seed)

        denom_range = self.get_value_ranges()['denominators']
        min_d, max_d = denom_range

        # Generate two fractions with different denominators
        denom1 = random.randint(min_d, max_d)
        denom2 = random.randint(min_d, max_d)

        # Make sure denominators are different
        while denom2 == denom1:
            denom2 = random.randint(min_d, max_d)

        # Generate numerators (less than denominators for proper fractions)
        numer1 = random.randint(1, denom1 - 1)
        numer2 = random.randint(1, denom2 - 1)

        # Calculate correct answer (find LCD)
        lcd = abs(denom1 * denom2) // math.gcd(denom1, denom2)
        mult1 = lcd // denom1
        mult2 = lcd // denom2

        correct_numer = numer1 * mult1 + numer2 * mult2
        correct_denom = lcd

        # Simplify if possible
        gcd_result = math.gcd(correct_numer, correct_denom)
        correct_numer //= gcd_result
        correct_denom //= gcd_result

        # Malrule answer: add numerators correctly, but add denominators too
        malrule_numer = numer1 + numer2
        malrule_denom = denom1 + denom2

        # Simplify malrule answer
        gcd_malrule = math.gcd(malrule_numer, malrule_denom)
        malrule_numer_simplified = malrule_numer // gcd_malrule
        malrule_denom_simplified = malrule_denom // gcd_malrule

        text = f"Calculate: {numer1}/{denom1} + {numer2}/{denom2}"

        return Problem(
            text=text,
            operands=[numer1, denom1, numer2, denom2],
            operation='fraction_addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'numer1': numer1,
                'denom1': denom1,
                'numer2': numer2,
                'denom2': denom2,
                'correct_numer': correct_numer,
                'correct_denom': correct_denom,
                'malrule_numer': malrule_numer_simplified,
                'malrule_denom': malrule_denom_simplified,
                'lcd': lcd,
                'template': 'basic_addition'
            }
        )

    def _generate_word_problem_context(self, seed=None) -> Problem:
        """Template 2: Word problem with real-world context."""
        problem = self._generate_basic_addition(seed)

        contexts = [
            ("Sarah ate {n1}/{d1} of a pizza", "Jake ate {n2}/{d2} of the same pizza", "fraction of the pizza eaten"),
            ("A recipe calls for {n1}/{d1} cup of sugar", "another {n2}/{d2} cup of sugar", "total cups of sugar"),
            ("Alex walked {n1}/{d1} of a mile", "then walked {n2}/{d2} of a mile more", "total miles walked"),
            ("{n1}/{d1} of the class are boys", "{n2}/{d2} of the class wear glasses", "fraction of class that are boys or wear glasses"),
            ("A tank is {n1}/{d1} full", "you add {n2}/{d2} more", "fraction full now")
        ]

        first_phrase, second_phrase, result = random.choice(contexts)
        n1 = problem.metadata['numer1']
        d1 = problem.metadata['denom1']
        n2 = problem.metadata['numer2']
        d2 = problem.metadata['denom2']

        problem.text = f"{first_phrase.format(n1=n1, d1=d1)} and {second_phrase.format(n2=n2, d2=d2)}. What is the {result}?"
        problem.metadata['template'] = 'word_problem_context'
        return problem

    def _generate_three_fractions(self, seed=None) -> Problem:
        """Template 3: Adding three fractions."""
        if seed is not None:
            random.seed(seed)

        denom_range = self.get_value_ranges()['denominators']
        min_d, max_d = denom_range

        # Generate three fractions with different denominators
        denom1 = random.randint(min_d, max_d)
        denom2 = random.randint(min_d, max_d)
        denom3 = random.randint(min_d, max_d)

        while denom2 == denom1:
            denom2 = random.randint(min_d, max_d)
        while denom3 == denom1 or denom3 == denom2:
            denom3 = random.randint(min_d, max_d)

        numer1 = random.randint(1, denom1 - 1)
        numer2 = random.randint(1, denom2 - 1)
        numer3 = random.randint(1, denom3 - 1)

        # Calculate LCD for all three
        lcd_12 = abs(denom1 * denom2) // math.gcd(denom1, denom2)
        lcd = abs(lcd_12 * denom3) // math.gcd(lcd_12, denom3)

        mult1 = lcd // denom1
        mult2 = lcd // denom2
        mult3 = lcd // denom3

        correct_numer = numer1 * mult1 + numer2 * mult2 + numer3 * mult3
        correct_denom = lcd

        gcd_result = math.gcd(correct_numer, correct_denom)
        correct_numer //= gcd_result
        correct_denom //= gcd_result

        # Malrule: add all numerators and all denominators
        malrule_numer = numer1 + numer2 + numer3
        malrule_denom = denom1 + denom2 + denom3

        gcd_malrule = math.gcd(malrule_numer, malrule_denom)
        malrule_numer_simplified = malrule_numer // gcd_malrule
        malrule_denom_simplified = malrule_denom // gcd_malrule

        text = f"Calculate: {numer1}/{denom1} + {numer2}/{denom2} + {numer3}/{denom3}"

        return Problem(
            text=text,
            operands=[numer1, denom1, numer2, denom2, numer3, denom3],
            operation='fraction_addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'numer1': numer1,
                'denom1': denom1,
                'numer2': numer2,
                'denom2': denom2,
                'numer3': numer3,
                'denom3': denom3,
                'correct_numer': correct_numer,
                'correct_denom': correct_denom,
                'malrule_numer': malrule_numer_simplified,
                'malrule_denom': malrule_denom_simplified,
                'lcd': lcd,
                'template': 'three_fractions'
            }
        )

    def _generate_visual_representation(self, seed=None) -> Problem:
        """Template 4: Problem with visual representation hint."""
        problem = self._generate_basic_addition(seed)
        n1 = problem.metadata['numer1']
        d1 = problem.metadata['denom1']
        n2 = problem.metadata['numer2']
        d2 = problem.metadata['denom2']
        problem.text = f"If you shade {n1}/{d1} of a circle and {n2}/{d2} of another equal circle, what fraction is shaded in total?"
        problem.metadata['template'] = 'visual_representation'
        return problem

    def _generate_comparison_problem(self, seed=None) -> Problem:
        """Template 5: Compare two fraction sums."""
        if seed is not None:
            random.seed(seed)

        # Generate two addition problems, retrying until correct and malrule differ
        attempts = 0
        while attempts < 100:
            problem1 = self._generate_basic_addition(seed + attempts if seed else None)
            problem2 = self._generate_basic_addition((seed + attempts + 1) if seed else None)

            n1 = problem1.metadata['numer1']
            d1 = problem1.metadata['denom1']
            n2 = problem1.metadata['numer2']
            d2 = problem1.metadata['denom2']

            n3 = problem2.metadata['numer1']
            d3 = problem2.metadata['denom1']
            n4 = problem2.metadata['numer2']
            d4 = problem2.metadata['denom2']

            sum1_correct = problem1.metadata['correct_numer'] / problem1.metadata['correct_denom']
            sum2_correct = problem2.metadata['correct_numer'] / problem2.metadata['correct_denom']

            sum1_malrule = problem1.metadata['malrule_numer'] / problem1.metadata['malrule_denom']

            if sum1_correct > sum2_correct:
                correct_answer = f"{n1}/{d1} + {n2}/{d2} is greater"
            elif sum1_correct < sum2_correct:
                correct_answer = f"{n3}/{d3} + {n4}/{d4} is greater"
            else:
                correct_answer = "They are equal"

            if sum1_malrule > sum2_correct:
                malrule_answer = f"{n1}/{d1} + {n2}/{d2} is greater"
            elif sum1_malrule < sum2_correct:
                malrule_answer = f"{n3}/{d3} + {n4}/{d4} is greater"
            else:
                malrule_answer = "They are equal"

            # Ensure the answers differ
            if correct_answer != malrule_answer:
                break
            attempts += 1

        problem1.text = f"Which is greater: {n1}/{d1} + {n2}/{d2} or {n3}/{d3} + {n4}/{d4}?"
        problem1.metadata['correct_answer'] = correct_answer
        problem1.metadata['malrule_answer'] = malrule_answer
        problem1.metadata['template'] = 'comparison_problem'
        return problem1

    def _generate_word_problem_three_fractions(self, seed=None) -> Problem:
        """Template: Word problem with three fractions addition."""
        if seed is not None:
            random.seed(seed)

        denom_range = self.get_value_ranges()['denominators']
        min_d, max_d = denom_range

        # Generate three fractions with different denominators
        denom1 = random.randint(min_d, min(max_d, 10))
        denom2 = random.randint(min_d, min(max_d, 10))
        denom3 = random.randint(min_d, min(max_d, 10))

        while denom2 == denom1:
            denom2 = random.randint(min_d, min(max_d, 10))
        while denom3 == denom1 or denom3 == denom2:
            denom3 = random.randint(min_d, min(max_d, 10))

        numer1 = random.randint(1, denom1 - 1)
        numer2 = random.randint(1, denom2 - 1)
        numer3 = random.randint(1, denom3 - 1)

        # Calculate LCD for all three
        lcd_12 = abs(denom1 * denom2) // math.gcd(denom1, denom2)
        lcd = abs(lcd_12 * denom3) // math.gcd(lcd_12, denom3)

        mult1 = lcd // denom1
        mult2 = lcd // denom2
        mult3 = lcd // denom3

        correct_numer = numer1 * mult1 + numer2 * mult2 + numer3 * mult3
        correct_denom = lcd

        gcd_result = math.gcd(correct_numer, correct_denom)
        correct_numer //= gcd_result
        correct_denom //= gcd_result

        # Malrule: add all numerators and all denominators
        malrule_numer = numer1 + numer2 + numer3
        malrule_denom = denom1 + denom2 + denom3

        gcd_malrule = math.gcd(malrule_numer, malrule_denom)
        malrule_numer_simplified = malrule_numer // gcd_malrule
        malrule_denom_simplified = malrule_denom // gcd_malrule

        contexts = [
            f"Three students are working on a group project. Emma completed {numer1}/{denom1} of the work, Liam completed {numer2}/{denom2}, and Olivia completed {numer3}/{denom3}. What fraction of the project have they completed in total?",
            f"A chef is making a sauce that requires {numer1}/{denom1} cup of tomatoes, {numer2}/{denom2} cup of onions, and {numer3}/{denom3} cup of peppers. How many total cups of vegetables are needed?",
            f"During a school fundraiser, Class A collected {numer1}/{denom1} of the goal, Class B collected {numer2}/{denom2}, and Class C collected {numer3}/{denom3}. What fraction of the fundraising goal did they collect together?"
        ]
        text = random.choice(contexts)

        return Problem(
            text=text,
            operands=[numer1, denom1, numer2, denom2, numer3, denom3],
            operation='fraction_addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'numer1': numer1,
                'denom1': denom1,
                'numer2': numer2,
                'denom2': denom2,
                'numer3': numer3,
                'denom3': denom3,
                'correct_numer': correct_numer,
                'correct_denom': correct_denom,
                'malrule_numer': malrule_numer_simplified,
                'malrule_denom': malrule_denom_simplified,
                'correct_answer': f"{correct_numer}/{correct_denom}",
                'malrule_answer': f"{malrule_numer_simplified}/{malrule_denom_simplified}",
                'lcd': lcd,
                'template': 'word_problem_three_fractions'
            }
        )
