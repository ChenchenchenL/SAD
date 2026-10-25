"""
Problem generator for Percent-Equals-Decimal malrule.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional, List
from utils import ProblemGenerator, Problem, DifficultyLevel


class PercentEqualsDecimalProblemGenerator(ProblemGenerator):
    """
    Generates percentage/decimal conversion problems.

    Templates:
    1. percent_to_decimal - Convert X% to decimal
    2. decimal_to_percent - Convert 0.X to percent
    3. percent_in_calculation - Calculate X% of Y
    4. fraction_to_percent - Convert fraction to percent
    5. word_problem - Real-world contexts
    """

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'percent_to_decimal',
            'decimal_to_percent',
            'percent_in_calculation',
            'fraction_to_percent',
            'word_problem'
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        ranges = {
            5: {DifficultyLevel.EASY: (1, 50), DifficultyLevel.MEDIUM: (1, 100), DifficultyLevel.HARD: (1, 200)},
            6: {DifficultyLevel.EASY: (1, 100), DifficultyLevel.MEDIUM: (1, 200), DifficultyLevel.HARD: (1, 500)},
            7: {DifficultyLevel.EASY: (1, 200), DifficultyLevel.MEDIUM: (1, 500), DifficultyLevel.HARD: (1, 1000)},
        }
        lvl = self.level if self.level in ranges else 6
        return {'values': ranges[lvl][self.difficulty]}

    def generate(self, seed=None, template: Optional[str] = None) -> Problem:
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            template = random.choice(self.get_available_templates())

        # Generate based on template
        if template == 'percent_to_decimal':
            return self._generate_percent_to_decimal(seed)
        elif template == 'decimal_to_percent':
            return self._generate_decimal_to_percent(seed)
        elif template == 'percent_in_calculation':
            return self._generate_percent_in_calculation(seed)
        elif template == 'fraction_to_percent':
            return self._generate_fraction_to_percent(seed)
        elif template == 'word_problem':
            return self._generate_word_problem(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_percent_to_decimal(self, seed=None) -> Problem:
        """
        Generate percent to decimal conversion (original template).

        Example: Convert 25% to decimal
        Correct: 0.25
        Malrule: 25
        """
        if seed is not None:
            random.seed(seed)

        # Common percentages
        percent = random.choice([5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 80, 90, 100])

        correct_answer = percent / 100
        malrule_answer = percent  # Student thinks 25% = 25

        text = f"Convert {percent}% to a decimal"

        return Problem(
            text=text,
            operands=[percent],
            operation='percentage_conversion',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'conversion_type': 'percent_to_decimal',
                'percent': percent,
                'decimal': correct_answer,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'percent_to_decimal'
            }
        )

    def _generate_decimal_to_percent(self, seed=None) -> Problem:
        """
        Generate decimal to percent conversion (original template).

        Example: Convert 0.30 to percent
        Correct: 30%
        Malrule: 0.30%
        """
        if seed is not None:
            random.seed(seed)

        # Create decimal from percentage
        percent = random.choice([5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 80, 90])
        decimal = percent / 100

        correct_answer = percent
        malrule_answer = decimal  # Student thinks 0.25 = 0.25%

        text = f"Convert {decimal} to a percentage"

        return Problem(
            text=text,
            operands=[decimal],
            operation='percentage_conversion',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'conversion_type': 'decimal_to_percent',
                'percent': correct_answer,
                'decimal': decimal,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'decimal_to_percent'
            }
        )

    def _generate_percent_in_calculation(self, seed=None) -> Problem:
        """
        Generate percent in calculation problem.

        Example: Calculate 25% of 80
        Correct: 0.25 × 80 = 20
        Malrule: 25 × 80 = 2000 (uses percent value directly)
        """
        if seed is not None:
            random.seed(seed)

        # Common percentages
        percent = random.choice([10, 20, 25, 30, 40, 50, 60, 75, 80])

        # Value to calculate percent of
        value = random.choice([20, 40, 50, 60, 80, 100, 120, 150, 200])

        decimal = percent / 100
        correct_answer = decimal * value
        malrule_answer = percent * value  # Student uses percent directly

        text = f"Calculate {percent}% of {value}"

        return Problem(
            text=text,
            operands=[percent, value],
            operation='percentage_calculation',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'conversion_type': 'percent_in_calculation',
                'percent': percent,
                'value': value,
                'decimal': decimal,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'percent_in_calculation'
            }
        )

    def _generate_fraction_to_percent(self, seed=None) -> Problem:
        """
        Generate fraction to percent conversion.

        Example: Convert 3/4 to a percentage
        Correct: 75%
        Malrule: 0.75% (converts to decimal, then adds %)
        """
        if seed is not None:
            random.seed(seed)

        # Common fractions
        fractions = [
            (1, 2, 50),   # 1/2 = 50%
            (1, 4, 25),   # 1/4 = 25%
            (3, 4, 75),   # 3/4 = 75%
            (1, 5, 20),   # 1/5 = 20%
            (2, 5, 40),   # 2/5 = 40%
            (3, 5, 60),   # 3/5 = 60%
            (4, 5, 80),   # 4/5 = 80%
            (1, 10, 10),  # 1/10 = 10%
            (3, 10, 30),  # 3/10 = 30%
        ]

        numerator, denominator, percent = random.choice(fractions)
        decimal = numerator / denominator

        correct_answer = percent
        malrule_answer = decimal  # Student: 1/2 = 0.5, so 0.5%

        text = f"Convert {numerator}/{denominator} to a percentage"

        return Problem(
            text=text,
            operands=[numerator, denominator],
            operation='percentage_conversion',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'conversion_type': 'fraction_to_percent',
                'numerator': numerator,
                'denominator': denominator,
                'fraction': f"{numerator}/{denominator}",
                'decimal': decimal,
                'percent': percent,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'fraction_to_percent'
            }
        )

    def _generate_word_problem(self, seed=None) -> Problem:
        """
        Generate word problem covering ALL applicable formula types with 3 variants each.

        Formula types for percent_equals_decimal:
        - percent_to_decimal: p% → p/100
        - decimal_to_percent: d → d*100%
        - percent_in_calculation: p% × value → (p/100) × value
        - fraction_to_percent: numerator/denominator → (numerator/denominator)*100%
        """
        if seed is not None:
            random.seed(seed)

        # Select formula type
        formula_types = [
            'percent_to_decimal',
            'decimal_to_percent',
            'percent_in_calculation',
            'fraction_to_percent'
        ]

        formula_type = random.choice(formula_types)
        variant = random.randint(0, 2)  # 3 variants per formula type

        if formula_type == 'percent_to_decimal':
            percent = random.choice([10, 15, 20, 25, 30, 40, 50, 60, 75])
            correct_answer = percent / 100
            malrule_answer = percent

            templates = [
                f"A store offers a {percent}% discount. What decimal should you multiply the price by to find the discount amount?",
                f"The sales tax in a city is {percent}%. Express this as a decimal for calculations.",
                f"You want to leave a {percent}% tip at a restaurant. Convert this percentage to a decimal."
            ]

            return Problem(
                text=templates[variant],
                operands=[percent],
                operation='percentage_conversion',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'conversion_type': 'percent_to_decimal',
                    'percent': percent,
                    'decimal': correct_answer,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'template': 'word_problem',
                    'formula_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        elif formula_type == 'decimal_to_percent':
            decimal = random.choice([0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50])
            correct_answer = decimal * 100
            malrule_answer = decimal

            templates = [
                f"A population grew by a factor of {decimal}. Express this growth as a percentage.",
                f"An account earned an interest rate of {decimal} in decimal form. What is this rate as a percentage?",
                f"The probability of an event is {decimal}. Convert this to a percentage."
            ]

            return Problem(
                text=templates[variant],
                operands=[decimal],
                operation='percentage_conversion',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'conversion_type': 'decimal_to_percent',
                    'percent': correct_answer,
                    'decimal': decimal,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'template': 'word_problem',
                    'formula_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        elif formula_type == 'percent_in_calculation':
            percent = random.choice([10, 20, 25, 30, 40, 50, 60, 75])
            value = random.choice([20, 40, 50, 60, 80, 100, 120, 150, 200])

            decimal = percent / 100
            correct_answer = decimal * value
            malrule_answer = percent * value

            templates = [
                f"A laptop costs ${value}. If you get a {percent}% discount, how much money do you save?",
                f"A class has {value} students. If {percent}% of them passed the exam, how many students passed?",
                f"A restaurant bill is ${value}. Calculate a {percent}% tip amount."
            ]

            return Problem(
                text=templates[variant],
                operands=[percent, value],
                operation='percentage_calculation',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'conversion_type': 'percent_in_calculation',
                    'percent': percent,
                    'value': value,
                    'decimal': decimal,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'template': 'word_problem',
                    'formula_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        elif formula_type == 'fraction_to_percent':
            fractions = [
                (1, 2, 50), (1, 4, 25), (3, 4, 75),
                (1, 5, 20), (2, 5, 40), (3, 5, 60),
                (1, 10, 10), (3, 10, 30)
            ]
            numerator, denominator, percent = random.choice(fractions)
            decimal = numerator / denominator

            correct_answer = percent
            malrule_answer = decimal

            templates = [
                f"In a survey, {numerator} out of {denominator} people preferred coffee. What percentage is this?",
                f"A student answered {numerator}/{denominator} of the questions correctly. Convert this to a percentage.",
                f"A recipe calls for {numerator}/{denominator} cup of sugar. Express this fraction as a percentage of a full cup."
            ]

            return Problem(
                text=templates[variant],
                operands=[numerator, denominator],
                operation='percentage_conversion',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'conversion_type': 'fraction_to_percent',
                    'numerator': numerator,
                    'denominator': denominator,
                    'fraction': f"{numerator}/{denominator}",
                    'decimal': decimal,
                    'percent': percent,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'template': 'word_problem',
                    'formula_type': formula_type,
                    'word_problem_variant': variant
                }
            )
