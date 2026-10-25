"""
Problem generator for Natural-Number-Bias-Numerator-Only malrule.

Generates fraction comparison problems that elicit the misconception
of comparing fractions by their numerators only.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional, List
from utils import ProblemGenerator, Problem, DifficultyLevel


class NaturalNumberBiasNumeratorOnlyProblemGenerator(ProblemGenerator):
    """
    Generates fraction comparison problems to elicit Natural-Number-Bias-Numerator-Only.

    Creates problems where students need to compare fractions with different
    numerators and denominators. The malrule predicts students will use numerator
    size only to determine which fraction is larger.

    Templates:
    1. basic_comparison - Simple two-fraction comparison
    2. visual_models - Problems with visual fraction models
    3. real_world_context - Pizza, money, or measurement contexts
    4. multiple_choice - Choose the largest from 3 fractions
    5. ordering - Put 3+ fractions in order from smallest to largest
    """

    def get_name(self) -> str:
        return "Natural Number Bias - Numerator Only Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates fraction comparison problems where comparing by "
            "numerator only gives the wrong answer."
        )

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_comparison',
            'visual_models',
            'real_world_context',
            'multiple_choice',
            'word_problem_multiple_choice',
            'ordering',
            'word_problem_ordering'
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level."""
        ranges = {
            4: {
                DifficultyLevel.EASY: (2, 8),
                DifficultyLevel.MEDIUM: (2, 12),
                DifficultyLevel.HARD: (3, 15),
            },
            5: {
                DifficultyLevel.EASY: (2, 10),
                DifficultyLevel.MEDIUM: (2, 15),
                DifficultyLevel.HARD: (3, 20),
            },
            6: {
                DifficultyLevel.EASY: (2, 12),
                DifficultyLevel.MEDIUM: (3, 20),
                DifficultyLevel.HARD: (5, 25),
            },
            7: {
                DifficultyLevel.EASY: (2, 15),
                DifficultyLevel.MEDIUM: (5, 25),
                DifficultyLevel.HARD: (5, 30),
            }
        }

        lvl = self.level if self.level in ranges else 5
        return {'numerator': ranges[lvl][self.difficulty]}

    def _create_fraction_pair(self, seed=None):
        """
        Generate two fractions where numerator comparison gives wrong answer.

        Returns: (num1, den1, num2, den2) where num1 < num2 but num1/den1 > num2/den2
        """
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['numerator']

        # Strategy: Create fractions where smaller numerator means larger fraction
        # Pick two different numerators where num1 < num2
        num1 = random.randint(min_val, max_val - 2)
        num2 = random.randint(num1 + 1, max_val)

        # Now pick denominators such that num1/den1 > num2/den2
        # Choose den2 first (larger)
        den2 = random.randint(max(min_val, num2 + 1), max_val + 5)

        # Choose den1 such that num1/den1 > num2/den2
        # We want num1*den2 > num2*den1, so den1 < num1*den2/num2
        max_den1 = int((num1 * den2) / num2) - 1
        if max_den1 < min_val:
            max_den1 = min_val

        den1 = random.randint(min_val, max(min_val, min(max_den1, num1 - 1)))

        # Ensure relationship is correct
        val1 = num1 / den1
        val2 = num2 / den2

        # If relationship is wrong, fix it
        if val1 <= val2:
            den1 = max(min_val, den1 // 2)
            if den1 < min_val:
                den1 = min_val

        return num1, den1, num2, den2

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate a fraction comparison problem based on selected template.

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
        if template == 'basic_comparison':
            return self._generate_basic_comparison(seed)
        elif template == 'visual_models':
            return self._generate_visual_models(seed)
        elif template == 'real_world_context':
            return self._generate_real_world_context(seed)
        elif template == 'multiple_choice':
            return self._generate_multiple_choice(seed)
        elif template == 'word_problem_multiple_choice':
            return self._generate_word_problem_multiple_choice(seed)
        elif template == 'ordering':
            return self._generate_ordering(seed)
        elif template == 'word_problem_ordering':
            return self._generate_word_problem_ordering(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_comparison(self, seed=None) -> Problem:
        """Generate basic two-fraction comparison."""
        if seed is not None:
            random.seed(seed)

        num1, den1, num2, den2 = self._create_fraction_pair(seed)

        # Determine correct answer
        val1 = num1 / den1
        val2 = num2 / den2

        if val1 > val2:
            correct_answer = f"{num1}/{den1}"
        elif val1 < val2:
            correct_answer = f"{num2}/{den2}"
        else:
            correct_answer = "equal"

        # Malrule answer: compare by numerators only
        if num1 > num2:
            malrule_answer = f"{num1}/{den1}"
        elif num1 < num2:
            malrule_answer = f"{num2}/{den2}"
        else:
            malrule_answer = "equal"

        problem_texts = [
            f"Which is larger: {num1}/{den1} or {num2}/{den2}?",
            f"Compare: {num1}/{den1} ___ {num2}/{den2}",
            f"Which fraction is greater: {num1}/{den1} or {num2}/{den2}?",
        ]
        problem_text = random.choice(problem_texts)

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
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'basic_comparison'
            }
        )

    def _generate_visual_models(self, seed=None) -> Problem:
        """Generate problem with visual fraction model description."""
        if seed is not None:
            random.seed(seed)

        num1, den1, num2, den2 = self._create_fraction_pair(seed)

        # Determine correct answer
        val1 = num1 / den1
        val2 = num2 / den2

        if val1 > val2:
            correct_answer = f"{num1}/{den1}"
        elif val1 < val2:
            correct_answer = f"{num2}/{den2}"
        else:
            correct_answer = "equal"

        # Malrule answer
        if num1 > num2:
            malrule_answer = f"{num1}/{den1}"
        elif num1 < num2:
            malrule_answer = f"{num2}/{den2}"
        else:
            malrule_answer = "equal"

        models = [
            f"Circle A is divided into {den1} equal parts with {num1} shaded. Circle B is divided into {den2} equal parts with {num2} shaded. Which circle has more shaded?",
            f"Bar model A shows {num1} out of {den1} sections shaded. Bar model B shows {num2} out of {den2} sections shaded. Which bar has a greater shaded portion?",
            f"Rectangle A is split into {den1} equal pieces, {num1} are colored. Rectangle B is split into {den2} equal pieces, {num2} are colored. Which has more colored area?",
        ]
        problem_text = random.choice(models)

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
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'visual_models'
            }
        )

    def _generate_real_world_context(self, seed=None) -> Problem:
        """Generate problem with real-world context."""
        if seed is not None:
            random.seed(seed)

        num1, den1, num2, den2 = self._create_fraction_pair(seed)

        # Determine correct answer
        val1 = num1 / den1
        val2 = num2 / den2

        if val1 > val2:
            correct_answer = f"{num1}/{den1}"
        elif val1 < val2:
            correct_answer = f"{num2}/{den2}"
        else:
            correct_answer = "equal"

        # Malrule answer
        if num1 > num2:
            malrule_answer = f"{num1}/{den1}"
        elif num1 < num2:
            malrule_answer = f"{num2}/{den2}"
        else:
            malrule_answer = "equal"

        contexts = [
            f"Maria ate {num1}/{den1} of a pizza and John ate {num2}/{den2} of an identical pizza. Who ate more pizza?",
            f"Bag A is {num1}/{den1} full of marbles. Bag B is {num2}/{den2} full of marbles. If the bags are the same size, which bag has more marbles?",
            f"Tank A has {num1}/{den1} of its capacity filled with water. Tank B has {num2}/{den2} of its capacity filled. If tanks are equal size, which has more water?",
            f"You walk {num1}/{den1} of a mile on Trail A and {num2}/{den2} of a mile on Trail B. Which trail did you walk farther on?",
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
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'real_world_context'
            }
        )

    def _generate_multiple_choice(self, seed=None) -> Problem:
        """Generate problem asking to choose the largest from 3 fractions."""
        if seed is not None:
            random.seed(seed)

        # Generate 3 fractions where numerator order != value order
        min_val, max_val = self.get_value_ranges()['numerator']

        # Create three numerators in ascending order
        num1 = random.randint(min_val, max_val - 4)
        num2 = random.randint(num1 + 1, max_val - 2)
        num3 = random.randint(num2 + 1, max_val)

        # Create denominators such that the fraction with smallest numerator is actually largest
        # Make den1 small (large fraction), den3 large (small fraction)
        den1 = random.randint(min_val, num1 - 1) if num1 > min_val else min_val
        den2 = random.randint(num2 - 2, num2 + 2)
        den3 = random.randint(num3 + 1, max_val + 5)

        # Calculate actual values
        val1 = num1 / den1
        val2 = num2 / den2
        val3 = num3 / den3

        # Find correct answer (largest fraction)
        if val1 >= val2 and val1 >= val3:
            correct_answer = f"{num1}/{den1}"
        elif val2 >= val1 and val2 >= val3:
            correct_answer = f"{num2}/{den2}"
        else:
            correct_answer = f"{num3}/{den3}"

        # Malrule answer: largest numerator
        malrule_answer = f"{num3}/{den3}"

        problem_text = f"Which fraction is the largest: {num1}/{den1}, {num2}/{den2}, or {num3}/{den3}?"

        return Problem(
            text=problem_text,
            operands=[num1, den1, num2, den2, num3, den3],
            operation='fraction_comparison',
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
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'multiple_choice'
            }
        )

    def _generate_ordering(self, seed=None) -> Problem:
        """Generate problem asking to order 3+ fractions from smallest to largest."""
        if seed is not None:
            random.seed(seed)

        # Generate 3 fractions
        min_val, max_val = self.get_value_ranges()['numerator']

        # Create three numerators in specific order
        num1 = random.randint(min_val, max_val - 4)
        num2 = random.randint(num1 + 1, max_val - 2)
        num3 = random.randint(num2 + 1, max_val)

        # Create denominators to make actual order different from numerator order
        den1 = random.randint(min_val, num1 - 1) if num1 > min_val else min_val
        den2 = random.randint(num2 - 1, num2 + 3)
        den3 = random.randint(num3 + 1, max_val + 5)

        # Calculate actual values and determine correct order
        fractions = [
            (num1, den1, num1/den1, f"{num1}/{den1}"),
            (num2, den2, num2/den2, f"{num2}/{den2}"),
            (num3, den3, num3/den3, f"{num3}/{den3}"),
        ]

        # Sort by actual value
        fractions_sorted = sorted(fractions, key=lambda x: x[2])
        correct_answer = ", ".join([f[3] for f in fractions_sorted])

        # Malrule answer: sort by numerator (num1, num2, num3)
        malrule_answer = f"{num1}/{den1}, {num2}/{den2}, {num3}/{den3}"

        problem_text = f"Order these fractions from smallest to largest: {num1}/{den1}, {num2}/{den2}, {num3}/{den3}"

        return Problem(
            text=problem_text,
            operands=[num1, den1, num2, den2, num3, den3],
            operation='fraction_comparison',
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
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'ordering'
            }
        )

    def _generate_word_problem_multiple_choice(self, seed=None) -> Problem:
        """Generate word problem asking to choose the largest from 3 fractions."""
        if seed is not None:
            random.seed(seed)

        # Generate 3 fractions where numerator order != value order
        min_val, max_val = self.get_value_ranges()['numerator']

        # Create three numerators in ascending order
        num1 = random.randint(min_val, max_val - 4)
        num2 = random.randint(num1 + 1, max_val - 2)
        num3 = random.randint(num2 + 1, max_val)

        # Create denominators such that the fraction with smallest numerator is actually largest
        # Make den1 small (large fraction), den3 large (small fraction)
        den1 = random.randint(min_val, num1 - 1) if num1 > min_val else min_val
        den2 = random.randint(num2 - 2, num2 + 2)
        den3 = random.randint(num3 + 1, max_val + 5)

        # Calculate actual values
        val1 = num1 / den1
        val2 = num2 / den2
        val3 = num3 / den3

        # Find correct answer (largest fraction)
        if val1 >= val2 and val1 >= val3:
            correct_answer = f"{num1}/{den1}"
        elif val2 >= val1 and val2 >= val3:
            correct_answer = f"{num2}/{den2}"
        else:
            correct_answer = f"{num3}/{den3}"

        # Malrule answer: largest numerator
        malrule_answer = f"{num3}/{den3}"

        contexts = [
            f"Three students ate different amounts of pizza. Alex ate {num1}/{den1} of a pizza, Bailey ate {num2}/{den2} of a pizza, and Casey ate {num3}/{den3} of a pizza. Who ate the most pizza?",
            f"Three jars contain different amounts of honey. Jar A is {num1}/{den1} full, Jar B is {num2}/{den2} full, and Jar C is {num3}/{den3} full. Which jar has the most honey?",
            f"Three runners completed different portions of a race. Runner 1 finished {num1}/{den1} of the course, Runner 2 finished {num2}/{den2}, and Runner 3 finished {num3}/{den3}. Which runner completed the largest fraction of the race?"
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[num1, den1, num2, den2, num3, den3],
            operation='fraction_comparison',
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
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'word_problem_multiple_choice'
            }
        )

    def _generate_word_problem_ordering(self, seed=None) -> Problem:
        """Generate word problem asking to order 3+ fractions from smallest to largest."""
        if seed is not None:
            random.seed(seed)

        # Generate 3 fractions
        min_val, max_val = self.get_value_ranges()['numerator']

        # Create three numerators in specific order
        num1 = random.randint(min_val, max_val - 4)
        num2 = random.randint(num1 + 1, max_val - 2)
        num3 = random.randint(num2 + 1, max_val)

        # Create denominators to make actual order different from numerator order
        den1 = random.randint(min_val, num1 - 1) if num1 > min_val else min_val
        den2 = random.randint(num2 - 1, num2 + 3)
        den3 = random.randint(num3 + 1, max_val + 5)

        # Calculate actual values and determine correct order
        fractions = [
            (num1, den1, num1/den1, f"{num1}/{den1}"),
            (num2, den2, num2/den2, f"{num2}/{den2}"),
            (num3, den3, num3/den3, f"{num3}/{den3}"),
        ]

        # Sort by actual value
        fractions_sorted = sorted(fractions, key=lambda x: x[2])
        correct_answer = ", ".join([f[3] for f in fractions_sorted])

        # Malrule answer: sort by numerator (num1, num2, num3)
        malrule_answer = f"{num1}/{den1}, {num2}/{den2}, {num3}/{den3}"

        contexts = [
            f"Three containers hold different amounts of water. Container A is {num1}/{den1} full, Container B is {num2}/{den2} full, and Container C is {num3}/{den3} full. Order these fractions from least to greatest.",
            f"Three friends completed different portions of their chores. Emma did {num1}/{den1} of her chores, Liam did {num2}/{den2} of his chores, and Olivia did {num3}/{den3} of her chores. Arrange these fractions from smallest to largest.",
            f"Three books have different amounts read. Book 1 is {num1}/{den1} read, Book 2 is {num2}/{den2} read, and Book 3 is {num3}/{den3} read. Order these fractions from least to greatest."
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[num1, den1, num2, den2, num3, den3],
            operation='fraction_comparison',
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
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'word_problem_ordering'
            }
        )
