"""
Problem generator for Percentage-As-Index malrule.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, List, Optional
from utils import ProblemGenerator, Problem, DifficultyLevel


class PercentageAsIndexProblemGenerator(ProblemGenerator):
    """Generates percentage problems like 'X% of Y'."""

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_percentage',
            'word_problem_context',
            'percentage_increase',
            'percentage_decrease',
            'comparison_problem'
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        ranges = {
            5: {DifficultyLevel.EASY: (10, 50), DifficultyLevel.MEDIUM: (20, 100), DifficultyLevel.HARD: (50, 200)},
            6: {DifficultyLevel.EASY: (20, 80), DifficultyLevel.MEDIUM: (50, 150), DifficultyLevel.HARD: (100, 300)},
            7: {DifficultyLevel.EASY: (30, 100), DifficultyLevel.MEDIUM: (50, 200), DifficultyLevel.HARD: (100, 500)},
            8: {DifficultyLevel.EASY: (50, 150), DifficultyLevel.MEDIUM: (100, 300), DifficultyLevel.HARD: (200, 1000)},
        }
        lvl = self.level if self.level in ranges else 6
        return {'total': ranges[lvl][self.difficulty]}

    def generate(self, seed=None, template: Optional[str] = None) -> Problem:
        """
        Generate a percentage problem.

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
        if template == 'basic_percentage':
            return self._generate_basic_percentage(seed)
        elif template == 'word_problem_context':
            return self._generate_word_problem_context(seed)
        elif template == 'percentage_increase':
            return self._generate_percentage_increase(seed)
        elif template == 'percentage_decrease':
            return self._generate_percentage_decrease(seed)
        elif template == 'comparison_problem':
            return self._generate_comparison_problem(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_percentage(self, seed=None) -> Problem:
        if seed is not None:
            random.seed(seed)

        total_range = self.get_value_ranges()['total']
        min_total, max_total = total_range

        # Generate percentage (in whole numbers for simplicity)
        percentage = random.choice([10, 20, 25, 30, 40, 50, 60, 75, 80])

        # Generate total
        total = random.randint(min_total, max_total)

        # Correct answer: percentage * total / 100
        correct_answer = (percentage * total) / 100

        # Malrule answer: Student treats percentage as index
        # "30% of 50" → thinks "30" (the percentage number itself)
        # Or sometimes "30th item" but that's still just 30
        malrule_answer = percentage

        text = f"What is {percentage}% of {total}?"

        return Problem(
            text=text,
            operands=[percentage, total],
            operation='percentage',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'percentage': percentage,
                'total': total,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'basic_percentage'
            }
        )

    def _generate_word_problem_context(self, seed=None) -> Problem:
        """
        Generate word problem covering ALL applicable formula types with 3 variants each.

        Formula types for percentage_as_index:
        - basic_percentage: (p/100) × total
        - percentage_increase: total + (p/100) × total = total × (1 + p/100)
        - percentage_decrease: total - (p/100) × total = total × (1 - p/100)
        - find_total_from_percentage: part / (p/100)
        """
        if seed is not None:
            random.seed(seed)

        # Select formula type
        formula_types = [
            'basic_percentage',
            'percentage_increase',
            'percentage_decrease',
            'find_total_from_percentage'
        ]

        formula_type = random.choice(formula_types)
        variant = random.randint(0, 2)  # 3 variants per formula type

        total_range = self.get_value_ranges()['total']
        min_total, max_total = total_range

        if formula_type == 'basic_percentage':
            percentage = random.choice([10, 20, 25, 30, 40, 50, 60, 75, 80])
            total = random.randint(min_total, max_total)

            correct_answer = (percentage * total) / 100
            malrule_answer = percentage

            templates = [
                f"A store has {total} items in stock. {percentage}% of them are on sale. How many items are on sale?",
                f"A class has {total} students. {percentage}% of them passed the final exam. How many students passed?",
                f"A library has {total} books. {percentage}% are fiction. How many fiction books are there?"
            ]

            return Problem(
                text=templates[variant],
                operands=[percentage, total],
                operation='percentage',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'percentage': percentage,
                    'total': total,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'template': 'word_problem_context',
                    'formula_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        elif formula_type == 'percentage_increase':
            percentage = random.choice([10, 20, 25, 30, 40, 50])
            total = random.randint(min_total, max_total)

            increase = (percentage * total) / 100
            correct_answer = total + increase
            malrule_answer = total + percentage

            templates = [
                f"A store had {total} items. After restocking, inventory increased by {percentage}%. How many items does the store have now?",
                f"A population of {total} people increased by {percentage}% this year. What is the population now?",
                f"A plant was {total} cm tall. It grew {percentage}%. What is its height now?"
            ]

            return Problem(
                text=templates[variant],
                operands=[total, percentage],
                operation='percentage',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'percentage': percentage,
                    'total': total,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'template': 'word_problem_context',
                    'formula_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        elif formula_type == 'percentage_decrease':
            percentage = random.choice([10, 20, 25, 30, 40, 50])
            total = random.randint(min_total, max_total)

            decrease = (percentage * total) / 100
            correct_answer = total - decrease
            malrule_answer = total - percentage

            templates = [
                f"An item priced at ${total} is on sale for {percentage}% off. What is the sale price?",
                f"A tank held {total} liters of water. {percentage}% evaporated. How much water remains?",
                f"A company had {total} employees. After layoffs of {percentage}%, how many employees remain?"
            ]

            return Problem(
                text=templates[variant],
                operands=[total, percentage],
                operation='percentage',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'percentage': percentage,
                    'total': total,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'template': 'word_problem_context',
                    'formula_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        elif formula_type == 'find_total_from_percentage':
            percentage = random.choice([10, 20, 25, 40, 50])
            # Generate part first, then calculate total
            part = random.randint(min_total // 2, min_total)
            total = (part * 100) // percentage

            correct_answer = total
            malrule_answer = part // percentage if percentage != 0 else part

            templates = [
                f"In a class, {part} students passed, which is {percentage}% of the class. How many students are in the class?",
                f"A store sold {part} items on sale, which represents {percentage}% of total inventory. How many items were in the inventory?",
                f"{part} books are fiction, which is {percentage}% of all books in a library. How many books total?"
            ]

            return Problem(
                text=templates[variant],
                operands=[part, percentage],
                operation='percentage',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'percentage': percentage,
                    'part': part,
                    'total': total,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'template': 'word_problem_context',
                    'formula_type': formula_type,
                    'word_problem_variant': variant
                }
            )

    def _generate_percentage_increase(self, seed=None) -> Problem:
        """Template 3: Percentage increase problems."""
        if seed is not None:
            random.seed(seed)

        total_range = self.get_value_ranges()['total']
        min_total, max_total = total_range

        percentage = random.choice([10, 20, 25, 30, 40, 50])
        total = random.randint(min_total, max_total)

        # Correct: new value = total + (percentage/100 * total)
        increase = (percentage * total) / 100
        correct_answer = total + increase

        # Malrule: student thinks increase is just percentage
        # So new value = total + percentage
        malrule_answer = total + percentage

        text = f"Increase {total} by {percentage}%. What is the new value?"

        return Problem(
            text=text,
            operands=[total, percentage],
            operation='percentage',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'percentage': percentage,
                'total': total,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'percentage_increase'
            }
        )

    def _generate_percentage_decrease(self, seed=None) -> Problem:
        """Template 4: Percentage decrease or discount problems."""
        if seed is not None:
            random.seed(seed)

        total_range = self.get_value_ranges()['total']
        min_total, max_total = total_range

        percentage = random.choice([10, 20, 25, 30, 40, 50])
        total = random.randint(min_total, max_total)

        # Correct: new value = total - (percentage/100 * total)
        decrease = (percentage * total) / 100
        correct_answer = total - decrease

        # Malrule: student thinks decrease is just percentage
        # So new value = total - percentage
        malrule_answer = total - percentage

        text = f"A store offers {percentage}% off an item priced at ${total}. What is the sale price?"

        return Problem(
            text=text,
            operands=[total, percentage],
            operation='percentage',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'percentage': percentage,
                'total': total,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'percentage_decrease'
            }
        )

    def _generate_comparison_problem(self, seed=None) -> Problem:
        """Template 5: Compare two percentage calculations."""
        total_range = self.get_value_ranges()['total']
        min_total, max_total = total_range

        # Retry until we get different correct and malrule answers
        attempts = 0
        while attempts < 100:
            if seed is not None:
                random.seed(seed + attempts)

            # Generate two percentage problems
            percentage1 = random.choice([10, 20, 25, 30, 40, 50])
            total1 = random.randint(min_total, max_total)
            correct1 = (percentage1 * total1) / 100
            malrule1 = percentage1

            percentage2 = random.choice([10, 20, 25, 30, 40, 50])
            total2 = random.randint(min_total, max_total)
            correct2 = (percentage2 * total2) / 100

            # Determine comparison
            if correct1 > correct2:
                correct_answer = f"{percentage1}% of {total1} is greater"
            elif correct1 < correct2:
                correct_answer = f"{percentage2}% of {total2} is greater"
            else:
                correct_answer = "They are equal"

            if malrule1 > correct2:
                malrule_answer = f"{percentage1}% of {total1} is greater"
            elif malrule1 < correct2:
                malrule_answer = f"{percentage2}% of {total2} is greater"
            else:
                malrule_answer = "They are equal"

            # Ensure answers differ
            if correct_answer != malrule_answer:
                break
            attempts += 1

        text = f"Which is greater: {percentage1}% of {total1} or {percentage2}% of {total2}?"

        return Problem(
            text=text,
            operands=[percentage1, total1, percentage2, total2],
            operation='percentage',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'percentage': percentage1,
                'total': total1,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'comparison_problem'
            }
        )
