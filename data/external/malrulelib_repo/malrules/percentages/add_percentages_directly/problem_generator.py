"""
Problem generator for Add-Percentages-Directly malrule.

Generates percentage problems involving sequential percentage changes
or compound percentages that students might incorrectly solve by
simply adding the percentages.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional
from utils import ProblemGenerator, Problem, DifficultyLevel


class AddPercentagesProblemGenerator(ProblemGenerator):
    """
    Generates percentage problems with sequential changes.

    Creates problems where students might incorrectly add percentages
    directly instead of applying them sequentially to changing base values.
    """

    def get_name(self) -> str:
        return "Add Percentages Directly Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates problems with sequential percentage changes that "
            "elicit the misconception of adding percentages directly."
        )

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level."""
        ranges = {
            6: {
                DifficultyLevel.EASY: (10, 100),  # initial values
                DifficultyLevel.MEDIUM: (50, 200),
                DifficultyLevel.HARD: (100, 500),
            },
            7: {
                DifficultyLevel.EASY: (10, 200),
                DifficultyLevel.MEDIUM: (50, 500),
                DifficultyLevel.HARD: (100, 1000),
            },
            8: {
                DifficultyLevel.EASY: (50, 500),
                DifficultyLevel.MEDIUM: (100, 1000),
                DifficultyLevel.HARD: (200, 2000),
            },
            9: {
                DifficultyLevel.EASY: (100, 1000),
                DifficultyLevel.MEDIUM: (200, 2000),
                DifficultyLevel.HARD: (500, 5000),
            }
        }

        lvl = self.level if self.level in ranges else 7
        return {'initial_value': ranges[lvl][self.difficulty]}

    def get_percentage_ranges(self) -> Tuple[int, int]:
        """Get appropriate percentage ranges based on difficulty."""
        ranges = {
            DifficultyLevel.EASY: (10, 30),
            DifficultyLevel.MEDIUM: (5, 50),
            DifficultyLevel.HARD: (5, 75),
        }
        return ranges[self.difficulty]

    def generate(self, seed: Optional[int] = None) -> Problem:
        """
        Generate a sequential percentage change problem.

        Args:
            seed: Optional random seed for reproducibility

        Returns:
            Problem instance
        """
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['initial_value']
        min_pct, max_pct = self.get_percentage_ranges()

        # Choose problem type
        problem_types = ['increase_then_decrease', 'decrease_then_increase',
                        'two_increases', 'two_decreases']

        # Add enhanced problem types for higher levels
        if self.level >= 7:
            problem_types.extend([
                'three_sequential_changes',    # Three percentage changes in a row
                'percentage_of_percentage',    # Discount on discount (explicitly framed)
                'reverse_percentage',          # Find original given final value
                'word_problem_context',        # Real-world sales scenarios
            ])

        problem_type = random.choice(problem_types)

        # Generate initial value (use nice round numbers for easier calculation)
        initial = random.choice([10, 20, 25, 50, 100, 200, 500, 1000])
        initial = min(max(initial, min_val), max_val)

        # Generate percentages (use nice values)
        pct_values = [10, 15, 20, 25, 30, 40, 50]
        pct1 = random.choice([p for p in pct_values if min_pct <= p <= max_pct])
        pct2 = random.choice([p for p in pct_values if min_pct <= p <= max_pct])

        if problem_type == 'increase_then_decrease':
            # e.g., "A $100 item is marked up 20% then discounted 20%"
            problem_text = (
                f"A ${initial} item is increased by {pct1}%, "
                f"then decreased by {pct2}%. What is the final price?"
            )
            operation_desc = f"+{pct1}% then -{pct2}%"

        elif problem_type == 'decrease_then_increase':
            # e.g., "A $100 item is discounted 20% then marked up 20%"
            problem_text = (
                f"A ${initial} item is decreased by {pct1}%, "
                f"then increased by {pct2}%. What is the final price?"
            )
            operation_desc = f"-{pct1}% then +{pct2}%"

        elif problem_type == 'two_increases':
            # e.g., "A population increases by 20% then by 30%"
            problem_text = (
                f"A population of {initial} increases by {pct1}%, "
                f"then increases again by {pct2}%. What is the final population?"
            )
            operation_desc = f"+{pct1}% then +{pct2}%"

        elif problem_type == 'two_decreases':
            # e.g., "A value decreases by 20% then by 30%"
            problem_text = (
                f"A value of {initial} decreases by {pct1}%, "
                f"then decreases again by {pct2}%. What is the final value?"
            )
            operation_desc = f"-{pct1}% then -{pct2}%"

        elif problem_type == 'three_sequential_changes':
            # Three percentage changes in a row
            pct3 = random.choice([p for p in pct_values if min_pct <= p <= max_pct])

            problem_text = (
                f"A stock price of ${initial} increases by {pct1}%, "
                f"then decreases by {pct2}%, then increases by {pct3}%. "
                f"What is the final stock price?"
            )
            operation_desc = f"+{pct1}% then -{pct2}% then +{pct3}%"

            # Calculate through all three steps
            after_first = initial * (1 + pct1/100)
            after_second = after_first * (1 - pct2/100)
            final = after_second * (1 + pct3/100)

            return Problem(
                text=problem_text,
                operands=[initial, pct1, pct2, pct3],
                operation='percentage_sequential',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'initial_value': initial,
                    'percentage1': pct1,
                    'percentage2': pct2,
                    'percentage3': pct3,
                    'problem_type': problem_type,
                    'operation_desc': operation_desc,
                    'correct_answer': final,
                    'after_first_change': after_first,
                    'after_second_change': after_second
                }
            )

        elif problem_type == 'percentage_of_percentage':
            # Explicitly framed as "discount on discount"
            problem_text = (
                f"A store offers {pct1}% off all items, then gives an additional {pct2}% "
                f"off the sale price. If an item originally costs ${initial}, what is the final price?"
            )
            operation_desc = f"-{pct1}% off, then -{pct2}% off sale price"

            # Two sequential decreases
            after_first = initial * (1 - pct1/100)
            final = after_first * (1 - pct2/100)

            return Problem(
                text=problem_text,
                operands=[initial, pct1, pct2],
                operation='percentage_sequential',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'initial_value': initial,
                    'percentage1': pct1,
                    'percentage2': pct2,
                    'problem_type': problem_type,
                    'operation_desc': operation_desc,
                    'correct_answer': final,
                    'after_first_change': after_first
                }
            )

        elif problem_type == 'reverse_percentage':
            # Find original value given final value after percentage change
            # Work backwards: if final = initial * (1 + pct/100), then initial = final / (1 + pct/100)

            # Generate the "final" value first, then calculate what original should be
            apparent_final = initial  # This is what we'll call the "final" in the problem
            correct_original = apparent_final / (1 + pct1/100)

            problem_text = (
                f"After a {pct1}% increase, a price is now ${apparent_final}. "
                f"What was the original price?"
            )
            operation_desc = f"reverse +{pct1}%"

            return Problem(
                text=problem_text,
                operands=[apparent_final, pct1],
                operation='percentage_reverse',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'final_value': apparent_final,
                    'percentage1': pct1,
                    'problem_type': problem_type,
                    'operation_desc': operation_desc,
                    'correct_answer': correct_original,
                }
            )

        elif problem_type == 'word_problem_context':
            # Real-world scenario - redirect to comprehensive word problem generator
            return self._generate_word_problem_context(seed)

        # Calculate correct answer (sequential application) for basic types
        if problem_type == 'increase_then_decrease':
            after_first = initial * (1 + pct1/100)
            final = after_first * (1 - pct2/100)
        elif problem_type == 'decrease_then_increase':
            after_first = initial * (1 - pct1/100)
            final = after_first * (1 + pct2/100)
        elif problem_type == 'two_increases':
            after_first = initial * (1 + pct1/100)
            final = after_first * (1 + pct2/100)
        else:  # two_decreases
            after_first = initial * (1 - pct1/100)
            final = after_first * (1 - pct2/100)

        return Problem(
            text=problem_text,
            operands=[initial, pct1, pct2],
            operation='percentage_sequential',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'initial_value': initial,
                'percentage1': pct1,
                'percentage2': pct2,
                'problem_type': problem_type,
                'operation_desc': operation_desc,
                'correct_answer': final,
                'after_first_change': after_first
            }
        )

    def _generate_word_problem_context(self, seed=None) -> Problem:
        """
        Generate word problem covering ALL applicable formula types with 3 variants each.

        Formula types for add_percentages_directly:
        - two_sequential_increase_decrease: initial * (1+p1/100) * (1-p2/100)
        - two_sequential_decrease_increase: initial * (1-p1/100) * (1+p2/100)
        - two_sequential_increases: initial * (1+p1/100) * (1+p2/100)
        - two_sequential_decreases: initial * (1-p1/100) * (1-p2/100)
        - three_sequential_changes: initial * (1±p1/100) * (1±p2/100) * (1±p3/100)
        - percentage_of_percentage: initial * (1-p1/100) * (1-p2/100) (compound discount)
        - reverse_percentage: final / (1+p/100) (find original)
        """
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['initial_value']
        min_pct, max_pct = self.get_percentage_ranges()

        # Select formula type
        formula_types = [
            'two_sequential_increase_decrease',
            'two_sequential_decrease_increase',
            'two_sequential_increases',
            'two_sequential_decreases',
            'three_sequential_changes',
            'percentage_of_percentage',
            'reverse_percentage'
        ]

        formula_type = random.choice(formula_types)
        variant = random.randint(0, 2)  # 3 variants per formula type

        # Generate values
        initial = random.choice([10, 20, 25, 50, 100, 200, 500, 1000])
        initial = min(max(initial, min_val), max_val)

        pct_values = [10, 15, 20, 25, 30, 40, 50]
        pct1 = random.choice([p for p in pct_values if min_pct <= p <= max_pct])
        pct2 = random.choice([p for p in pct_values if min_pct <= p <= max_pct])

        if formula_type == 'two_sequential_increase_decrease':
            after_first = initial * (1 + pct1/100)
            final = after_first * (1 - pct2/100)

            templates = [
                f"A store increased the price of an item from ${initial} by {pct1}%, then offered a {pct2}% discount. What is the final price?",
                f"A stock valued at ${initial} rose {pct1}% in January, then fell {pct2}% in February. What is the stock value at the end of February?",
                f"Sarah's plant was {initial} cm tall. It grew {pct1}% in spring, then shrank {pct2}% in summer due to drought. What is its height now?"
            ]

            return Problem(
                text=templates[variant],
                operands=[initial, pct1, pct2],
                operation='percentage_sequential',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'initial_value': initial,
                    'percentage1': pct1,
                    'percentage2': pct2,
                    'problem_type': 'increase_then_decrease',
                    'operation_desc': f"+{pct1}% then -{pct2}%",
                    'correct_answer': final,
                    'after_first_change': after_first,
                    'formula_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        elif formula_type == 'two_sequential_decrease_increase':
            after_first = initial * (1 - pct1/100)
            final = after_first * (1 + pct2/100)

            templates = [
                f"A laptop originally priced at ${initial} was discounted by {pct1}%, then the sale price was increased by {pct2}%. What is the final price?",
                f"A town's population of {initial} people decreased by {pct1}% last year, then increased by {pct2}% this year. What is the population now?",
                f"Water in a tank decreased from {initial} liters by {pct1}% due to evaporation, then increased by {pct2}% after rain. How much water is in the tank?"
            ]

            return Problem(
                text=templates[variant],
                operands=[initial, pct1, pct2],
                operation='percentage_sequential',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'initial_value': initial,
                    'percentage1': pct1,
                    'percentage2': pct2,
                    'problem_type': 'decrease_then_increase',
                    'operation_desc': f"-{pct1}% then +{pct2}%",
                    'correct_answer': final,
                    'after_first_change': after_first,
                    'formula_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        elif formula_type == 'two_sequential_increases':
            after_first = initial * (1 + pct1/100)
            final = after_first * (1 + pct2/100)

            templates = [
                f"A company's profit of ${initial} million increased by {pct1}% in Q1, then by {pct2}% in Q2. What is the profit at the end of Q2?",
                f"A tree {initial} meters tall grew {pct1}% in year 1, then {pct2}% in year 2. How tall is it now?",
                f"An investment of ${initial} earned {pct1}% return in year 1 and {pct2}% return in year 2. What is its value now?"
            ]

            return Problem(
                text=templates[variant],
                operands=[initial, pct1, pct2],
                operation='percentage_sequential',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'initial_value': initial,
                    'percentage1': pct1,
                    'percentage2': pct2,
                    'problem_type': 'two_increases',
                    'operation_desc': f"+{pct1}% then +{pct2}%",
                    'correct_answer': final,
                    'after_first_change': after_first,
                    'formula_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        elif formula_type == 'two_sequential_decreases':
            after_first = initial * (1 - pct1/100)
            final = after_first * (1 - pct2/100)

            templates = [
                f"A car valued at ${initial} depreciated by {pct1}% in year 1, then by {pct2}% in year 2. What is its value now?",
                f"A glacier with {initial} million tons of ice lost {pct1}% in decade 1, then {pct2}% in decade 2. How much ice remains?",
                f"A company's workforce of {initial} employees decreased by {pct1}% in 2020, then by {pct2}% in 2021. How many employees remain?"
            ]

            return Problem(
                text=templates[variant],
                operands=[initial, pct1, pct2],
                operation='percentage_sequential',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'initial_value': initial,
                    'percentage1': pct1,
                    'percentage2': pct2,
                    'problem_type': 'two_decreases',
                    'operation_desc': f"-{pct1}% then -{pct2}%",
                    'correct_answer': final,
                    'after_first_change': after_first,
                    'formula_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        elif formula_type == 'three_sequential_changes':
            pct3 = random.choice([p for p in pct_values if min_pct <= p <= max_pct])

            after_first = initial * (1 + pct1/100)
            after_second = after_first * (1 - pct2/100)
            final = after_second * (1 + pct3/100)

            templates = [
                f"A stock priced at ${initial} increased {pct1}% in Q1, decreased {pct2}% in Q2, then increased {pct3}% in Q3. What is the price at the end of Q3?",
                f"A population of {initial} grew {pct1}% in year 1, shrank {pct2}% in year 2, then grew {pct3}% in year 3. What is the population now?",
                f"Real estate valued at ${initial} million appreciated {pct1}%, depreciated {pct2}%, then appreciated {pct3}%. What is its current value?"
            ]

            return Problem(
                text=templates[variant],
                operands=[initial, pct1, pct2, pct3],
                operation='percentage_sequential',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'initial_value': initial,
                    'percentage1': pct1,
                    'percentage2': pct2,
                    'percentage3': pct3,
                    'problem_type': 'three_sequential_changes',
                    'operation_desc': f"+{pct1}% then -{pct2}% then +{pct3}%",
                    'correct_answer': final,
                    'after_first_change': after_first,
                    'after_second_change': after_second,
                    'formula_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        elif formula_type == 'percentage_of_percentage':
            # Compound discount: first discount, then additional discount on sale price
            after_first = initial * (1 - pct1/100)
            final = after_first * (1 - pct2/100)

            templates = [
                f"A store offers {pct1}% off all items. A member gets an additional {pct2}% off the sale price. If an item costs ${initial}, what does a member pay?",
                f"During a sale, all {initial}-dollar items get {pct1}% off. Using a coupon gives {pct2}% off the already-reduced price. What is the final price?",
                f"A service normally costs ${initial}. Seniors get {pct1}% off, and with a loyalty card, an extra {pct2}% off the senior price. What is the final cost?"
            ]

            return Problem(
                text=templates[variant],
                operands=[initial, pct1, pct2],
                operation='percentage_sequential',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'initial_value': initial,
                    'percentage1': pct1,
                    'percentage2': pct2,
                    'problem_type': 'percentage_of_percentage',
                    'operation_desc': f"-{pct1}% off, then -{pct2}% off sale price",
                    'correct_answer': final,
                    'after_first_change': after_first,
                    'formula_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        elif formula_type == 'reverse_percentage':
            # Find original value given final value after percentage increase
            apparent_final = initial
            correct_original = apparent_final / (1 + pct1/100)

            templates = [
                f"After a {pct1}% price increase, an item now costs ${apparent_final}. What was the original price?",
                f"A company's revenue is ${apparent_final} million after a {pct1}% growth. What was the revenue before the growth?",
                f"A plant is now {apparent_final} cm tall after growing {pct1}%. How tall was it before?"
            ]

            return Problem(
                text=templates[variant],
                operands=[apparent_final, pct1],
                operation='percentage_reverse',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'final_value': apparent_final,
                    'percentage1': pct1,
                    'problem_type': 'reverse_percentage',
                    'operation_desc': f"reverse +{pct1}%",
                    'correct_answer': correct_original,
                    'formula_type': formula_type,
                    'word_problem_variant': variant
                }
            )
