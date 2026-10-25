"""
Problem generator for Reverse-Percentage-Error malrule.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional, List
from utils import ProblemGenerator, Problem, DifficultyLevel


class ReversePercentageErrorProblemGenerator(ProblemGenerator):
    """
    Generates percentage relationship problems.

    Templates:
    1. basic_reverse_relationship - Direct reverse percentage questions
    2. percentage_increase - Problems involving percentage increase relationships
    3. percentage_decrease - Problems involving percentage decrease relationships
    4. comparison_statements - Comparing two quantities with percentages
    5. word_problem - Real-world contexts with reverse relationships
    """

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_reverse_relationship',
            'percentage_increase',
            'percentage_decrease',
            'comparison_statements',
            'word_problem'
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        ranges = {
            7: {DifficultyLevel.EASY: (10, 50), DifficultyLevel.MEDIUM: (20, 100), DifficultyLevel.HARD: (50, 200)},
            8: {DifficultyLevel.EASY: (20, 100), DifficultyLevel.MEDIUM: (50, 200), DifficultyLevel.HARD: (100, 500)},
            9: {DifficultyLevel.EASY: (50, 200), DifficultyLevel.MEDIUM: (100, 500), DifficultyLevel.HARD: (200, 1000)},
        }
        lvl = self.level if self.level in ranges else 8
        return {'values': ranges[lvl][self.difficulty]}

    def generate(self, seed=None, template: Optional[str] = None) -> Problem:
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            template = random.choice(self.get_available_templates())

        # Generate based on template
        if template == 'basic_reverse_relationship':
            return self._generate_basic_reverse_relationship(seed)
        elif template == 'percentage_increase':
            return self._generate_percentage_increase(seed)
        elif template == 'percentage_decrease':
            return self._generate_percentage_decrease(seed)
        elif template == 'comparison_statements':
            return self._generate_comparison_statements(seed)
        elif template == 'word_problem':
            return self._generate_word_problem(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_reverse_relationship(self, seed=None) -> Problem:
        """
        Generate basic reverse relationship problem (original template).

        Example: If 20 is 50% of 40, what percent is 40 of 20?
        Correct: 200%
        Malrule: 50% (student thinks it's symmetric)
        """
        if seed is not None:
            random.seed(seed)

        value_range = self.get_value_ranges()['values']
        min_val, max_val = value_range

        # Choose a percentage (less than 100% for interesting case)
        percentages = [25, 40, 50, 60, 75, 80]
        percentage = random.choice(percentages)

        # Generate two numbers where num1 is percentage% of num2
        num2 = random.randint(min_val, max_val)
        num1 = round((percentage / 100) * num2)

        # Calculate correct reverse relationship
        correct_reverse_pct = round((num2 / num1) * 100) if num1 != 0 else 0

        # Malrule: student thinks it's the same percentage in reverse
        malrule_reverse_pct = percentage

        problem_text = f"If {num1} is {percentage}% of {num2}, what percent is {num2} of {num1}?"

        return Problem(
            text=problem_text,
            operands=[num1, num2, percentage],
            operation='percentage_relationship',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': num1,
                'num2': num2,
                'percentage': percentage,
                'correct_answer': correct_reverse_pct,
                'malrule_answer': malrule_reverse_pct,
                'relationship': f"{num1} is {percentage}% of {num2}",
                'template': 'basic_reverse_relationship'
            }
        )

    def _generate_percentage_increase(self, seed=None) -> Problem:
        """
        Generate percentage increase problem.

        Example: A price increased from $50 to $75 (50% increase).
        If the price decreases from $75 to $50, what is the percent decrease?
        Correct: 33.33%
        Malrule: 50% (student thinks increase and decrease are symmetric)
        """
        if seed is not None:
            random.seed(seed)

        value_range = self.get_value_ranges()['values']
        min_val, max_val = value_range

        # Choose increase percentage
        increase_percentages = [20, 25, 50, 75, 100]
        increase_pct = random.choice(increase_percentages)

        # Original value
        original = random.randint(min_val // 2, max_val // 2)
        new_value = round(original * (1 + increase_pct / 100))

        # Calculate correct decrease percentage from new back to original
        # (new - original) / new * 100
        correct_decrease_pct = round(((new_value - original) / new_value) * 100, 1)

        # Malrule: student thinks it's the same percentage
        malrule_decrease_pct = increase_pct

        problem_text = (f"A value increased from {original} to {new_value}, which is a {increase_pct}% increase. "
                       f"If the value decreases from {new_value} back to {original}, what is the percent decrease?")

        return Problem(
            text=problem_text,
            operands=[original, new_value, increase_pct],
            operation='percentage_relationship',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'original': original,
                'new_value': new_value,
                'increase_pct': increase_pct,
                'correct_answer': correct_decrease_pct,
                'malrule_answer': malrule_decrease_pct,
                'template': 'percentage_increase'
            }
        )

    def _generate_percentage_decrease(self, seed=None) -> Problem:
        """
        Generate percentage decrease problem.

        Example: A price decreased from $80 to $60 (25% decrease).
        If the price increases from $60 to $80, what is the percent increase?
        Correct: 33.33%
        Malrule: 25% (student thinks decrease and increase are symmetric)
        """
        if seed is not None:
            random.seed(seed)

        value_range = self.get_value_ranges()['values']
        min_val, max_val = value_range

        # Choose decrease percentage
        decrease_percentages = [20, 25, 40, 50]
        decrease_pct = random.choice(decrease_percentages)

        # Original value
        original = random.randint(min_val, max_val)
        new_value = round(original * (1 - decrease_pct / 100))

        # Calculate correct increase percentage from new back to original
        # (original - new) / new * 100
        correct_increase_pct = round(((original - new_value) / new_value) * 100, 1)

        # Malrule: student thinks it's the same percentage
        malrule_increase_pct = decrease_pct

        problem_text = (f"A value decreased from {original} to {new_value}, which is a {decrease_pct}% decrease. "
                       f"If the value increases from {new_value} back to {original}, what is the percent increase?")

        return Problem(
            text=problem_text,
            operands=[original, new_value, decrease_pct],
            operation='percentage_relationship',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'original': original,
                'new_value': new_value,
                'decrease_pct': decrease_pct,
                'correct_answer': correct_increase_pct,
                'malrule_answer': malrule_increase_pct,
                'template': 'percentage_decrease'
            }
        )

    def _generate_comparison_statements(self, seed=None) -> Problem:
        """
        Generate comparison statement problem.

        Example: "Tom has 25% as much money as Sarah. What percent of Tom's money does Sarah have?"
        Correct: 400%
        Malrule: 25% (student thinks comparison is symmetric)
        """
        if seed is not None:
            random.seed(seed)

        # Choose a percentage
        percentages = [20, 25, 40, 50, 75, 80]
        percentage = random.choice(percentages)

        contexts = [
            ("Tom", "Sarah", "money"),
            ("Car A", "Car B", "speed"),
            ("Box A", "Box B", "weight"),
            ("Tree A", "Tree B", "height"),
            ("Store A", "Store B", "sales")
        ]

        person1, person2, item = random.choice(contexts)

        # If person1 has percentage% as much as person2,
        # then person2 has (100/percentage)% as much as person1
        correct_reverse_pct = round((100 / percentage) * 100, 1)

        # Malrule: student thinks it's the same percentage
        malrule_reverse_pct = percentage

        problem_text = (f"{person1} has {percentage}% as much {item} as {person2}. "
                       f"What percent of {person1}'s {item} does {person2} have?")

        return Problem(
            text=problem_text,
            operands=[percentage],
            operation='percentage_relationship',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'percentage': percentage,
                'person1': person1,
                'person2': person2,
                'item': item,
                'correct_answer': correct_reverse_pct,
                'malrule_answer': malrule_reverse_pct,
                'template': 'comparison_statements'
            }
        )

    def _generate_word_problem(self, seed=None) -> Problem:
        """
        Generate word problem covering ALL applicable formula types with 3 variants each.

        Formula types for reverse_percentage_error:
        - increase_then_reverse: After increase by p%, what % decrease to get back?
        - decrease_then_reverse: After decrease by p%, what % increase to get back?
        - reverse_relationship: If A is p% of B, what % is B of A?
        - comparison_asymmetry: If A has p% as much as B, what % does B have of A?
        """
        if seed is not None:
            random.seed(seed)

        # Select formula type
        formula_types = [
            'increase_then_reverse',
            'decrease_then_reverse',
            'reverse_relationship',
            'comparison_asymmetry'
        ]

        formula_type = random.choice(formula_types)
        variant = random.randint(0, 2)  # 3 variants per formula type

        value_range = self.get_value_ranges()['values']
        min_val, max_val = value_range

        if formula_type == 'increase_then_reverse':
            # After increase by p%, what % decrease to get back?
            increase_percentages = [20, 25, 50, 75, 100]
            increase_pct = random.choice(increase_percentages)
            original = random.randint(min_val // 2, max_val // 2)
            new_value = round(original * (1 + increase_pct / 100))

            correct_decrease_pct = round(((new_value - original) / new_value) * 100, 1)
            malrule_decrease_pct = increase_pct

            templates = [
                f"An investment of ${original} increased by {increase_pct}% to ${new_value}. If it decreases back to ${original}, what is the percent decrease?",
                f"A population grew from {original} to {new_value} people, a {increase_pct}% increase. If it shrinks back to {original}, what is the percent decrease?",
                f"A stock price rose from ${original} to ${new_value} ({increase_pct}% gain). If it falls back to ${original}, what is the percent loss?"
            ]

            return Problem(
                text=templates[variant],
                operands=[original, new_value, increase_pct],
                operation='percentage_relationship',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'original': original,
                    'new_value': new_value,
                    'increase_pct': increase_pct,
                    'correct_answer': correct_decrease_pct,
                    'malrule_answer': malrule_decrease_pct,
                    'template': 'word_problem',
                    'formula_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        elif formula_type == 'decrease_then_reverse':
            # After decrease by p%, what % increase to get back?
            decrease_percentages = [10, 20, 25, 40, 50]
            decrease_pct = random.choice(decrease_percentages)
            original = random.randint(100, 200)
            new_value = round(original * (1 - decrease_pct / 100))

            correct_increase_pct = round(((original - new_value) / new_value) * 100, 1)
            malrule_increase_pct = decrease_pct

            templates = [
                f"A jacket priced at ${original} was reduced by {decrease_pct}% to ${new_value}. After the sale, the price was raised back to ${original}. What was the percent increase?",
                f"A person's weight decreased from {original} lbs to {new_value} lbs ({decrease_pct}% loss). To regain back to {original} lbs, what percent must they gain?",
                f"A company's revenue fell from ${original} million to ${new_value} million ({decrease_pct}% drop). What percent increase is needed to return to ${original} million?"
            ]

            return Problem(
                text=templates[variant],
                operands=[original, new_value, decrease_pct],
                operation='percentage_relationship',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'original': original,
                    'new_value': new_value,
                    'decrease_pct': decrease_pct,
                    'correct_answer': correct_increase_pct,
                    'malrule_answer': malrule_increase_pct,
                    'template': 'word_problem',
                    'formula_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        elif formula_type == 'reverse_relationship':
            # If A is p% of B, what % is B of A?
            percentages = [20, 25, 40, 50, 75, 80]
            percentage = random.choice(percentages)

            num2 = random.randint(min_val, max_val)
            num1 = round((percentage / 100) * num2)

            correct_reverse_pct = round((num2 / num1) * 100) if num1 != 0 else 0
            malrule_reverse_pct = percentage

            templates = [
                f"If {num1} is {percentage}% of {num2}, what percent is {num2} of {num1}?",
                f"A store sold {num1} items, which is {percentage}% of inventory ({num2} items). What percent of sold items ({num1}) does the total inventory ({num2}) represent?",
                f"Team A scored {num1} points, which is {percentage}% of Team B's {num2} points. What percent of Team A's score is Team B's score?"
            ]

            return Problem(
                text=templates[variant],
                operands=[num1, num2, percentage],
                operation='percentage_relationship',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'num1': num1,
                    'num2': num2,
                    'percentage': percentage,
                    'correct_answer': correct_reverse_pct,
                    'malrule_answer': malrule_reverse_pct,
                    'relationship': f"{num1} is {percentage}% of {num2}",
                    'template': 'word_problem',
                    'formula_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        elif formula_type == 'comparison_asymmetry':
            # If A has p% as much as B, what % does B have of A?
            percentages = [20, 25, 40, 50, 75, 80]
            percentage = random.choice(percentages)

            correct_reverse_pct = round((100 / percentage) * 100, 1)
            malrule_reverse_pct = percentage

            contexts = [
                ("Tom", "Sarah", "money"),
                ("Car A", "Car B", "speed"),
                ("Box A", "Box B", "weight"),
                ("Store A", "Store B", "sales")
            ]
            person1, person2, item = random.choice(contexts)

            templates = [
                f"{person1} has {percentage}% as much {item} as {person2}. What percent of {person1}'s {item} does {person2} have?",
                f"If {person1}'s {item} is {percentage}% of {person2}'s {item}, then {person2}'s {item} is what percent of {person1}'s {item}?",
                f"{person1} earned {percentage}% of what {person2} earned in {item}. What percentage did {person2} earn compared to {person1}?"
            ]

            return Problem(
                text=templates[variant],
                operands=[percentage],
                operation='percentage_relationship',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'percentage': percentage,
                    'person1': person1,
                    'person2': person2,
                    'item': item,
                    'correct_answer': correct_reverse_pct,
                    'malrule_answer': malrule_reverse_pct,
                    'template': 'word_problem',
                    'formula_type': formula_type,
                    'word_problem_variant': variant
                }
            )
