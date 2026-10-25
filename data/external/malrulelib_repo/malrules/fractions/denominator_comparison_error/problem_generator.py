"""
Problem generator for Denominator-Comparison-Error malrule.

Generates fraction comparison problems that elicit the misconception
of comparing fractions by their denominators only.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional, List
from utils import ProblemGenerator, Problem, DifficultyLevel


class FractionComparisonProblemGenerator(ProblemGenerator):
    """
    Generates fraction comparison problems to elicit Denominator-Comparison-Error.

    Creates problems where students need to compare fractions with different
    denominators. The malrule predicts students will use denominator size
    to determine which fraction is larger.
    """

    def get_name(self) -> str:
        return "Fraction Comparison Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates fraction comparison problems where comparing by "
            "denominator size gives the wrong answer."
        )

    def get_available_templates(self) -> List[str]:
        """Return list of available template names."""
        return [
            'basic_two_fractions',
            'three_fractions_ordering',
            'word_problem_three_fractions',
            'mixed_comparisons',
            'word_problem_mixed',
            'real_world_context',
            'benchmark_comparison'
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level."""
        ranges = {
            3: {
                DifficultyLevel.EASY: (2, 6),
                DifficultyLevel.MEDIUM: (2, 8),
                DifficultyLevel.HARD: (2, 10),
            },
            4: {
                DifficultyLevel.EASY: (2, 8),
                DifficultyLevel.MEDIUM: (2, 12),
                DifficultyLevel.HARD: (2, 15),
            },
            5: {
                DifficultyLevel.EASY: (2, 10),
                DifficultyLevel.MEDIUM: (2, 15),
                DifficultyLevel.HARD: (3, 20),
            },
            6: {
                DifficultyLevel.EASY: (2, 12),
                DifficultyLevel.MEDIUM: (3, 20),
                DifficultyLevel.HARD: (5, 30),
            }
        }

        lvl = self.level if self.level in ranges else 5
        return {'denominator': ranges[lvl][self.difficulty]}

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate a fraction comparison problem.

        Args:
            seed: Optional random seed for reproducibility
            template: Optional template name to use. If None, randomly chosen.

        Returns:
            Problem instance with correct_answer and malrule_answer in metadata
        """
        if seed is not None:
            random.seed(seed)

        # Choose template if not specified
        if template is None:
            template = random.choice(self.get_available_templates())

        # Validate template
        if template not in self.get_available_templates():
            raise ValueError(f"Unknown template: {template}. Must be one of {self.get_available_templates()}")

        # Call appropriate template method
        if template == 'basic_two_fractions':
            return self._generate_basic_two_fractions()
        elif template == 'three_fractions_ordering':
            return self._generate_three_fractions_ordering()
        elif template == 'word_problem_three_fractions':
            return self._generate_word_problem_three_fractions()
        elif template == 'mixed_comparisons':
            return self._generate_mixed_comparisons()
        elif template == 'word_problem_mixed':
            return self._generate_word_problem_mixed()
        elif template == 'real_world_context':
            return self._generate_real_world_context()
        elif template == 'benchmark_comparison':
            return self._generate_benchmark_comparison()

    def _generate_basic_two_fractions(self) -> Problem:
        """Generate basic two-fraction comparison problem."""
        min_val, max_val = self.get_value_ranges()['denominator']

        problem_type = random.choice(['unit_fractions', 'same_numerator', 'different_both'])

        if problem_type == 'unit_fractions':
            # Unit fractions: 1/a vs 1/b where a > b
            # Correct: 1/a < 1/b (larger denominator = smaller fraction)
            # Malrule: 1/a > 1/b (larger denominator = larger fraction - WRONG!)
            den1 = random.randint(min_val + 2, max_val)
            den2 = random.randint(min_val, den1 - 1)
            num1, num2 = 1, 1

        elif problem_type == 'same_numerator':
            # Same numerator: n/a vs n/b where a > b
            # Correct: n/a < n/b, but malrule says n/a > n/b
            num1 = num2 = random.randint(1, 5)
            den1 = random.randint(min_val + 2, max_val)
            den2 = random.randint(min_val, den1 - 1)

        else:  # different_both
            # Different numerators and denominators
            # Create cases where larger denominator actually means smaller fraction
            den1 = random.randint(min_val + 3, max_val)
            den2 = random.randint(min_val, den1 - 2)

            # Ensure fraction1 < fraction2 despite den1 > den2
            num2 = random.randint(2, 8)
            max_num1 = int((num2 * den1) / den2) - 1
            if max_num1 < 1:
                max_num1 = 1
            num1 = random.randint(1, max(1, max_num1))

        # Create problem text
        problem_texts = [
            f"Which is larger: {num1}/{den1} or {num2}/{den2}?",
            f"Compare: {num1}/{den1} ___ {num2}/{den2}",
            f"Which fraction is greater: {num1}/{den1} or {num2}/{den2}?",
        ]
        problem_text = random.choice(problem_texts)

        # Calculate correct answer using cross-multiplication
        cross1 = num1 * den2
        cross2 = num2 * den1
        if cross1 > cross2:
            correct_answer = f"{num1}/{den1}"
        elif cross1 < cross2:
            correct_answer = f"{num2}/{den2}"
        else:
            correct_answer = "equal"

        # Calculate malrule answer (larger denominator = larger fraction)
        if den1 > den2:
            malrule_answer = f"{num1}/{den1}"
        elif den1 < den2:
            malrule_answer = f"{num2}/{den2}"
        else:
            # Same denominator - compare numerators (this is correct)
            if num1 > num2:
                malrule_answer = f"{num1}/{den1}"
            elif num1 < num2:
                malrule_answer = f"{num2}/{den2}"
            else:
                malrule_answer = "equal"

        return Problem(
            text=problem_text,
            operands=[num1, den1, num2, den2],
            operation='fraction_comparison',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'fraction1': f"{num1}/{den1}",
                'fraction2': f"{num2}/{den2}",
                'num1': num1,
                'den1': den1,
                'num2': num2,
                'den2': den2,
                'problem_type': problem_type,
                'template': 'basic_two_fractions',
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_three_fractions_ordering(self) -> Problem:
        """Generate ordering problem with three fractions."""
        min_val, max_val = self.get_value_ranges()['denominator']

        # Generate 3 fractions with different denominators
        dens = random.sample(range(min_val, min(max_val, 12) + 1), 3)
        dens.sort(reverse=True)  # Largest first
        den1, den2, den3 = dens

        # Make numerators such that fractions are ordered differently
        num1 = random.randint(1, min(5, den1 - 1))
        num2 = random.randint(1, min(5, den2 - 1))
        num3 = random.randint(1, min(5, den3 - 1))

        problem_text = f"Order from smallest to largest: {num1}/{den1}, {num2}/{den2}, {num3}/{den3}"

        # Calculate correct ordering
        fractions_with_values = [
            (f"{num1}/{den1}", num1 / den1),
            (f"{num2}/{den2}", num2 / den2),
            (f"{num3}/{den3}", num3 / den3)
        ]
        fractions_with_values.sort(key=lambda x: x[1])
        correct_answer = ", ".join([f[0] for f in fractions_with_values])

        # Malrule: order by denominator size (smallest denom = smallest fraction - WRONG!)
        fractions_with_dens = [
            (f"{num1}/{den1}", den1),
            (f"{num2}/{den2}", den2),
            (f"{num3}/{den3}", den3)
        ]
        fractions_with_dens.sort(key=lambda x: x[1])
        malrule_answer = ", ".join([f[0] for f in fractions_with_dens])

        return Problem(
            text=problem_text,
            operands=[num1, den1, num2, den2, num3, den3],
            operation='fraction_ordering',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'fraction1': f"{num1}/{den1}",
                'fraction2': f"{num2}/{den2}",
                'fraction3': f"{num3}/{den3}",
                'num1': num1,
                'den1': den1,
                'num2': num2,
                'den2': den2,
                'num3': num3,
                'den3': den3,
                'template': 'three_fractions_ordering',
                'num_fractions': 3,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_mixed_comparisons(self) -> Problem:
        """Generate problem with proper vs improper fractions."""
        min_val, max_val = self.get_value_ranges()['denominator']

        # One proper fraction (num < den) vs one improper (num >= den)
        den1 = random.randint(min_val + 2, max_val)
        num1 = random.randint(1, den1 - 1)  # Proper

        den2 = random.randint(min_val, den1 - 1)
        num2 = random.randint(den2, den2 + 5)  # Improper

        problem_text = f"Which is larger: {num1}/{den1} or {num2}/{den2}?"

        # Correct answer: improper fraction is always >= 1, proper is always < 1
        # So num2/den2 is always larger
        correct_answer = f"{num2}/{den2}"

        # Malrule answer: larger denominator = larger fraction
        if den1 > den2:
            malrule_answer = f"{num1}/{den1}"
        elif den1 < den2:
            malrule_answer = f"{num2}/{den2}"
        else:
            # Same denominator - compare numerators
            if num1 > num2:
                malrule_answer = f"{num1}/{den1}"
            else:
                malrule_answer = f"{num2}/{den2}"

        return Problem(
            text=problem_text,
            operands=[num1, den1, num2, den2],
            operation='fraction_comparison',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'fraction1': f"{num1}/{den1}",
                'fraction2': f"{num2}/{den2}",
                'num1': num1,
                'den1': den1,
                'num2': num2,
                'den2': den2,
                'template': 'mixed_comparisons',
                'fraction1_type': 'proper',
                'fraction2_type': 'improper',
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_real_world_context(self) -> Problem:
        """Generate word problem with real-world context."""
        min_val, max_val = self.get_value_ranges()['denominator']

        contexts = [
            ('pizza', 'Maria ate {num1}/{den1} of a pizza and John ate {num2}/{den2} of a pizza. Which fraction is larger?'),
            ('distance', 'Sara ran {num1}/{den1} of a mile and Tom ran {num2}/{den2} of a mile. Which fraction is larger?'),
            ('time', 'One task took {num1}/{den1} of an hour and another took {num2}/{den2} of an hour. Which fraction represents more time?'),
            ('measurement', 'One board is {num1}/{den1} meter long and another is {num2}/{den2} meter long. Which fraction is greater?')
        ]
        context, problem_template = random.choice(contexts)

        # Generate unit fractions to ensure malrule gives wrong answer
        # Unit fractions: larger denominator = SMALLER value
        den1 = random.randint(min_val + 2, min(max_val, 10))
        den2 = random.randint(min_val, den1 - 1)
        num1 = 1  # Unit fraction
        num2 = 1  # Unit fraction

        problem_text = problem_template.format(num1=num1, den1=den1, num2=num2, den2=den2)

        # Correct: 1/den1 < 1/den2 (since den1 > den2)
        correct_answer = f"{num2}/{den2}"

        # Malrule: larger denominator = larger fraction
        malrule_answer = f"{num1}/{den1}"

        return Problem(
            text=problem_text,
            operands=[num1, den1, num2, den2],
            operation='fraction_comparison',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'fraction1': f"{num1}/{den1}",
                'fraction2': f"{num2}/{den2}",
                'num1': num1,
                'den1': den1,
                'num2': num2,
                'den2': den2,
                'template': 'real_world_context',
                'context': context,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_benchmark_comparison(self) -> Problem:
        """Generate problem comparing to benchmark values like 1/2 or 1."""
        min_val, max_val = self.get_value_ranges()['denominator']

        benchmark_type = random.choice(['half', 'one'])

        if benchmark_type == 'half':
            # Compare to 1/2 - ensure malrule gives WRONG answer
            den1 = random.randint(max(4, min_val + 2), min(max_val, 12))
            # Ensure num1/den1 < 1/2 (so num1 < den1/2)
            max_num = int(den1 / 2) - 1
            num1 = random.randint(1, max(1, max_num))

            problem_text = f"Which is larger: {num1}/{den1} or 1/2?"

            # Correct: 1/2 is larger
            correct_answer = "1/2"

            # Malrule: larger denominator = larger fraction (den1 > 2)
            malrule_answer = f"{num1}/{den1}"

            return Problem(
                text=problem_text,
                operands=[num1, den1, 1, 2],
                operation='fraction_comparison',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'fraction1': f"{num1}/{den1}",
                    'fraction2': "1/2",
                    'num1': num1,
                    'den1': den1,
                    'num2': 1,
                    'den2': 2,
                    'template': 'benchmark_comparison',
                    'benchmark': 'half',
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer
                }
            )
        else:  # one
            # Compare to 1 (represented as 1/1)
            den1 = random.randint(max(2, min_val), min(max_val, 10))
            num1 = random.randint(1, den1 - 1)  # Less than 1

            problem_text = f"Which is larger: {num1}/{den1} or 1?"

            # Correct: 1 is larger
            correct_answer = "1"

            # Malrule: larger denominator = larger fraction (den1 > 1)
            malrule_answer = f"{num1}/{den1}"

            return Problem(
                text=problem_text,
                operands=[num1, den1, 1, 1],
                operation='fraction_comparison',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'fraction1': f"{num1}/{den1}",
                    'fraction2': "1",
                    'num1': num1,
                    'den1': den1,
                    'num2': 1,
                    'den2': 1,
                    'template': 'benchmark_comparison',
                    'benchmark': 'one',
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer
                }
            )

    def _generate_word_problem_three_fractions(self) -> Problem:
        """Generate word problem with three fractions ordering."""
        min_val, max_val = self.get_value_ranges()['denominator']

        # Generate 3 fractions with different denominators
        dens = random.sample(range(min_val, min(max_val, 12) + 1), 3)
        dens.sort(reverse=True)  # Largest first
        den1, den2, den3 = dens

        # Make numerators such that fractions are ordered differently
        num1 = random.randint(1, min(5, den1 - 1))
        num2 = random.randint(1, min(5, den2 - 1))
        num3 = random.randint(1, min(5, den3 - 1))

        # Calculate correct ordering
        fractions_with_values = [
            (f"{num1}/{den1}", num1 / den1),
            (f"{num2}/{den2}", num2 / den2),
            (f"{num3}/{den3}", num3 / den3)
        ]
        fractions_with_values.sort(key=lambda x: x[1])
        correct_answer = ", ".join([f[0] for f in fractions_with_values])

        # Malrule: order by denominator size (smallest denom = smallest fraction - WRONG!)
        fractions_with_dens = [
            (f"{num1}/{den1}", den1),
            (f"{num2}/{den2}", den2),
            (f"{num3}/{den3}", den3)
        ]
        fractions_with_dens.sort(key=lambda x: x[1])
        malrule_answer = ", ".join([f[0] for f in fractions_with_dens])

        contexts = [
            f"Three students completed different fractions of their reading. Amy read {num1}/{den1} of her book, Ben read {num2}/{den2} of his book, and Carla read {num3}/{den3} of her book. Order these fractions from smallest to largest.",
            f"In a baking competition, three contestants used different amounts of flour. Chef A used {num1}/{den1} bag, Chef B used {num2}/{den2} bag, and Chef C used {num3}/{den3} bag. Arrange these amounts from least to greatest.",
            f"Three runners completed different portions of a race. Runner 1 finished {num1}/{den1} of the course, Runner 2 finished {num2}/{den2}, and Runner 3 finished {num3}/{den3}. Order these fractions from smallest to largest."
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[num1, den1, num2, den2, num3, den3],
            operation='fraction_ordering',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'fraction1': f"{num1}/{den1}",
                'fraction2': f"{num2}/{den2}",
                'fraction3': f"{num3}/{den3}",
                'num1': num1,
                'den1': den1,
                'num2': num2,
                'den2': den2,
                'num3': num3,
                'den3': den3,
                'template': 'word_problem_three_fractions',
                'num_fractions': 3,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_word_problem_mixed(self) -> Problem:
        """Generate word problem with proper vs improper fractions."""
        min_val, max_val = self.get_value_ranges()['denominator']

        # One proper fraction (num < den) vs one improper (num >= den)
        den1 = random.randint(min_val + 2, min(max_val, 10))
        num1 = random.randint(1, den1 - 1)  # Proper

        den2 = random.randint(min_val, den1 - 1)
        num2 = random.randint(den2, den2 + 5)  # Improper

        # Correct answer: improper fraction is always >= 1, proper is always < 1
        # So num2/den2 is always larger
        correct_answer = f"{num2}/{den2}"

        # Malrule answer: larger denominator = larger fraction
        if den1 > den2:
            malrule_answer = f"{num1}/{den1}"
        elif den1 < den2:
            malrule_answer = f"{num2}/{den2}"
        else:
            # Same denominator - compare numerators
            if num1 > num2:
                malrule_answer = f"{num1}/{den1}"
            else:
                malrule_answer = f"{num2}/{den2}"

        contexts = [
            f"Sarah has {num1}/{den1} of a cake left from yesterday and baked {num2}/{den2} of a new cake today. Which fraction represents more cake?",
            f"Tank A is {num1}/{den1} full of water. Tank B contains {num2}/{den2} of its capacity in water. If the tanks are the same size, which has more water?",
            f"John ran {num1}/{den1} of a lap around the track. Maria ran {num2}/{den2} of a lap. Who ran farther?"
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[num1, den1, num2, den2],
            operation='fraction_comparison',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'fraction1': f"{num1}/{den1}",
                'fraction2': f"{num2}/{den2}",
                'num1': num1,
                'den1': den1,
                'num2': num2,
                'den2': den2,
                'template': 'word_problem_mixed',
                'fraction1_type': 'proper',
                'fraction2_type': 'improper',
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )
