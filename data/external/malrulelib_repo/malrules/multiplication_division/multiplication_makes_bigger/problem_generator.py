"""
Problem generator for Multiplication-Makes-Bigger malrule.

Generates multiplication problems with factors less than 1 to elicit the
misconception that multiplication always makes numbers bigger.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional, List
from utils import ProblemGenerator, Problem, DifficultyLevel


class MultiplicationProblemGenerator(ProblemGenerator):
    """
    Generates multiplication problems to elicit Multiplication-Makes-Bigger malrule.

    Focus on problems where at least one factor is less than 1 (decimals or fractions),
    causing the product to be smaller than one or both factors.

    Templates:
    1. basic_decimal_multiplication - Multiply decimals less than 1
    2. fraction_multiplication - Multiply fractions less than 1
    3. money_context - Shopping/spending fractional amounts
    4. measurement_context - Recipe/measurement with fractional scaling
    5. percent_discount - Percentage/discount calculations
    """

    def get_name(self) -> str:
        return "Multiplication-Makes-Bigger Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates multiplication problems with factors less than 1 "
            "(decimals or fractions) to elicit the misconception that "
            "multiplication always produces larger results."
        )

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_decimal_multiplication',
            'fraction_multiplication',
            'money_context',
            'measurement_context',
            'percent_discount',
            'area_rectangle',
            'probability_compound',
            'compound_scaling',
            'rate_distance',
            'volume_box'
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level and difficulty."""
        # For this malrule, we need decimals less than 1
        ranges = {
            3: {
                DifficultyLevel.EASY: (1, 9),      # 0.1 to 0.9
                DifficultyLevel.MEDIUM: (1, 9),
                DifficultyLevel.HARD: (10, 99),    # 0.10 to 0.99
            },
            4: {
                DifficultyLevel.EASY: (1, 9),
                DifficultyLevel.MEDIUM: (10, 99),
                DifficultyLevel.HARD: (10, 99),
            },
            5: {
                DifficultyLevel.EASY: (1, 9),
                DifficultyLevel.MEDIUM: (10, 99),
                DifficultyLevel.HARD: (100, 999),  # 0.100 to 0.999
            },
            6: {
                DifficultyLevel.EASY: (10, 99),
                DifficultyLevel.MEDIUM: (10, 99),
                DifficultyLevel.HARD: (100, 999),
            }
        }

        lvl = self.level if self.level in ranges else 4
        return {'decimal': ranges[lvl][self.difficulty]}

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate a multiplication problem based on selected template.

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
        if template == 'basic_decimal_multiplication':
            return self._generate_basic_decimal_multiplication(seed)
        elif template == 'fraction_multiplication':
            return self._generate_fraction_multiplication(seed)
        elif template == 'money_context':
            return self._generate_money_context(seed)
        elif template == 'measurement_context':
            return self._generate_measurement_context(seed)
        elif template == 'percent_discount':
            return self._generate_percent_discount(seed)
        elif template == 'area_rectangle':
            return self._generate_area_rectangle(seed)
        elif template == 'probability_compound':
            return self._generate_probability_compound(seed)
        elif template == 'compound_scaling':
            return self._generate_compound_scaling(seed)
        elif template == 'rate_distance':
            return self._generate_rate_distance(seed)
        elif template == 'volume_box':
            return self._generate_volume_box(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_decimal_multiplication(self, seed=None) -> Problem:
        """Generate basic decimal multiplication problem."""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['decimal']

        # Generate two decimals less than 1
        num1 = random.randint(min_val, max_val)
        num2 = random.randint(min_val, max_val)

        # Determine decimal places based on difficulty
        if max_val < 10:
            factor1 = num1 / 10.0
            factor2 = num2 / 10.0
        elif max_val < 100:
            factor1 = num1 / 100.0
            factor2 = num2 / 100.0
        else:
            factor1 = num1 / 1000.0
            factor2 = num2 / 1000.0

        # Calculate answers
        correct_product = factor1 * factor2

        # Malrule answer: add instead (because product is smaller)
        malrule_answer = factor1 + factor2

        problem_texts = [
            f"What is {factor1} × {factor2}?",
            f"Calculate: {factor1} × {factor2}",
            f"Multiply {factor1} by {factor2}",
        ]
        problem_text = random.choice(problem_texts)

        return Problem(
            text=problem_text,
            operands=[factor1, factor2],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'factor1': factor1,
                'factor2': factor2,
                'correct_answer': f'{correct_product:.4f}',
                'malrule_answer': f'{malrule_answer:.4f}',
                'template': 'basic_decimal_multiplication',
                'problem_type': 'basic_multiplication'
            }
        )

    def _generate_fraction_multiplication(self, seed=None) -> Problem:
        """Generate fraction multiplication problem."""
        if seed is not None:
            random.seed(seed)

        # Generate two fractions less than 1
        numerator1 = random.randint(1, 3)
        denominator1 = random.choice([2, 3, 4, 5, 6])
        while numerator1 >= denominator1:
            numerator1 = random.randint(1, 3)

        numerator2 = random.randint(1, 3)
        denominator2 = random.choice([2, 3, 4, 5, 6])
        while numerator2 >= denominator2:
            numerator2 = random.randint(1, 3)

        factor1 = numerator1 / denominator1
        factor2 = numerator2 / denominator2

        frac1_str = f"{numerator1}/{denominator1}"
        frac2_str = f"{numerator2}/{denominator2}"

        # Calculate answers
        correct_product = factor1 * factor2

        # Malrule answer: add instead
        malrule_answer = factor1 + factor2

        problem_texts = [
            f"What is {frac1_str} × {frac2_str}?",
            f"Multiply {frac1_str} by {frac2_str}",
            f"Calculate: {frac1_str} × {frac2_str}",
        ]
        problem_text = random.choice(problem_texts)

        return Problem(
            text=problem_text,
            operands=[factor1, factor2],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'factor1': factor1,
                'factor2': factor2,
                'numerator1': numerator1,
                'denominator1': denominator1,
                'numerator2': numerator2,
                'denominator2': denominator2,
                'fraction1_str': frac1_str,
                'fraction2_str': frac2_str,
                'correct_answer': f'{correct_product:.4f}',
                'malrule_answer': f'{malrule_answer:.4f}',
                'template': 'fraction_multiplication',
                'problem_type': 'fraction_multiplication'
            }
        )

    def _generate_money_context(self, seed=None) -> Problem:
        """Generate money/shopping context problem."""
        if seed is not None:
            random.seed(seed)

        # Base amount of money
        base_amount = random.choice([10, 12, 15, 20, 24, 30, 40, 50])

        # Fraction to spend/save (less than 1)
        fraction_decimal = random.choice([0.25, 0.5, 0.75, 0.3, 0.6, 0.4, 0.2, 0.8])

        factor1 = float(base_amount)
        factor2 = fraction_decimal

        # Calculate answers
        correct_product = factor1 * factor2

        # Malrule answer: add instead
        malrule_answer = factor1 + factor2

        contexts = [
            f"You have ${factor1:.0f}. You spend {factor2} of it. How much did you spend?",
            f"Sarah saves ${factor1:.0f}. She uses {factor2} of her savings. How much did she use?",
            f"A store has a sale: pay {factor2} of the regular price. If an item costs ${factor1:.0f}, what is the sale price?",
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[factor1, factor2],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'factor1': factor1,
                'factor2': factor2,
                'correct_answer': f'${correct_product:.2f}',
                'malrule_answer': f'${malrule_answer:.2f}',
                'template': 'money_context',
                'problem_type': 'money_calculation'
            }
        )

    def _generate_measurement_context(self, seed=None) -> Problem:
        """Generate recipe/measurement context problem."""
        if seed is not None:
            random.seed(seed)

        # Base amount
        base_amount = random.choice([2, 3, 4, 6, 8, 10, 12])

        # Fractional scaling (less than 1)
        fraction_decimal = random.choice([0.5, 0.25, 0.75, 0.33, 0.67, 0.4, 0.6])

        factor1 = float(base_amount)
        factor2 = fraction_decimal

        # Calculate answers
        correct_product = factor1 * factor2

        # Malrule answer: add instead
        malrule_answer = factor1 + factor2

        unit = random.choice(['cups', 'liters', 'kilograms', 'ounces', 'tablespoons'])
        contexts = [
            f"A recipe calls for {factor1:.0f} {unit} of flour. You're making {factor2} of the recipe. How much flour do you need?",
            f"You need {factor1:.0f} {unit} of water. If you only use {factor2} of the amount, how much water is that?",
            f"The recipe requires {factor1:.0f} {unit}. You're scaling it to {factor2} of the original size. How much do you need?",
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[factor1, factor2],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'factor1': factor1,
                'factor2': factor2,
                'unit': unit,
                'correct_answer': f'{correct_product:.2f} {unit}',
                'malrule_answer': f'{malrule_answer:.2f} {unit}',
                'template': 'measurement_context',
                'problem_type': 'measurement_scaling'
            }
        )

    def _generate_percent_discount(self, seed=None) -> Problem:
        """Generate percentage/discount context problem."""
        if seed is not None:
            random.seed(seed)

        # Original price
        price = random.choice([20, 25, 30, 40, 50, 60, 80, 100])

        # Discount rate (as decimal less than 1)
        discount_rate = random.choice([0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5])

        factor1 = float(price)
        factor2 = discount_rate

        # Calculate answers
        correct_product = factor1 * factor2

        # Malrule answer: add instead
        malrule_answer = factor1 + factor2

        contexts = [
            f"A ${factor1:.0f} item has a {int(factor2*100)}% discount. How much is the discount amount?",
            f"Calculate {factor2} of ${factor1:.0f} to find the discount.",
            f"An item costs ${factor1:.0f}. With a {int(factor2*100)}% discount, how much is saved?",
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[factor1, factor2],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'factor1': factor1,
                'factor2': factor2,
                'discount_percent': int(factor2 * 100),
                'correct_answer': f'${correct_product:.2f}',
                'malrule_answer': f'${malrule_answer:.2f}',
                'template': 'percent_discount',
                'problem_type': 'percentage_calculation'
            }
        )

    def _generate_area_rectangle(self, seed=None) -> Problem:
        """Generate rectangle area problem with dimensions < 1."""
        if seed is not None:
            random.seed(seed)

        # Rectangle dimensions less than 1
        length = random.choice([0.5, 0.6, 0.7, 0.75, 0.8, 0.9, 0.4, 0.3])
        width = random.choice([0.5, 0.6, 0.7, 0.75, 0.8, 0.9, 0.4, 0.3])

        factor1 = length
        factor2 = width

        # Calculate answers
        correct_product = factor1 * factor2

        # Malrule answer: add instead
        malrule_answer = factor1 + factor2

        unit = random.choice(['meters', 'feet', 'yards', 'kilometers'])
        contexts = [
            f"A rectangular garden is {factor1} {unit} long and {factor2} {unit} wide. What is its area in square {unit}?",
            f"Find the area of a rectangle with length {factor1} {unit} and width {factor2} {unit}.",
            f"A small plot of land measures {factor1} {unit} by {factor2} {unit}. Calculate the area.",
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[factor1, factor2],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'factor1': factor1,
                'factor2': factor2,
                'length': length,
                'width': width,
                'unit': unit,
                'correct_answer': f'{correct_product:.4f} square {unit}',
                'malrule_answer': f'{malrule_answer:.4f} {unit}',
                'template': 'area_rectangle',
                'problem_type': 'area_calculation'
            }
        )

    def _generate_probability_compound(self, seed=None) -> Problem:
        """Generate compound probability problem."""
        if seed is not None:
            random.seed(seed)

        # Probabilities less than 1
        prob1 = random.choice([0.5, 0.6, 0.7, 0.75, 0.8, 0.25, 0.4, 0.3])
        prob2 = random.choice([0.5, 0.6, 0.7, 0.75, 0.8, 0.25, 0.4, 0.3])

        factor1 = prob1
        factor2 = prob2

        # Calculate answers
        correct_product = factor1 * factor2

        # Malrule answer: add instead
        malrule_answer = factor1 + factor2

        contexts = [
            f"The probability of rain is {factor1} and the probability of a power outage is {factor2}. What is the probability that both events occur (assuming independence)?",
            f"Event A has probability {factor1} and Event B has probability {factor2}. If they are independent, what is P(A and B)?",
            f"A coin has a {factor1} chance of landing heads. If you flip it twice, and the probability of a certain outcome on the second flip is {factor2}, what is the probability of both outcomes occurring?",
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[factor1, factor2],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'factor1': factor1,
                'factor2': factor2,
                'probability1': prob1,
                'probability2': prob2,
                'correct_answer': f'{correct_product:.4f}',
                'malrule_answer': f'{malrule_answer:.4f}',
                'template': 'probability_compound',
                'problem_type': 'probability_multiplication'
            }
        )

    def _generate_compound_scaling(self, seed=None) -> Problem:
        """Generate compound scaling problem ('a of b')."""
        if seed is not None:
            random.seed(seed)

        # Two scaling factors less than 1
        scale1 = random.choice([0.5, 0.6, 0.75, 0.8, 0.4, 0.25, 0.3])
        scale2 = random.choice([0.5, 0.6, 0.75, 0.8, 0.4, 0.25, 0.3])

        factor1 = scale1
        factor2 = scale2

        # Calculate answers
        correct_product = factor1 * factor2

        # Malrule answer: add instead
        malrule_answer = factor1 + factor2

        contexts = [
            f"If you take {factor1} of {factor2} of a cake, what fraction of the whole cake do you have?",
            f"A store gives {factor1} off during a sale, then an additional {factor2} off the sale price. What is the total discount multiplier?",
            f"You use {factor1} of your savings, and {factor2} of that amount for a purchase. What fraction of your total savings did you spend?",
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[factor1, factor2],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'factor1': factor1,
                'factor2': factor2,
                'scale1': scale1,
                'scale2': scale2,
                'correct_answer': f'{correct_product:.4f}',
                'malrule_answer': f'{malrule_answer:.4f}',
                'template': 'compound_scaling',
                'problem_type': 'compound_fraction'
            }
        )

    def _generate_rate_distance(self, seed=None) -> Problem:
        """Generate rate × time = distance problem with rate or time < 1."""
        if seed is not None:
            random.seed(seed)

        # Rate or time less than 1
        if random.choice([True, False]):
            # Rate < 1
            rate = random.choice([0.5, 0.6, 0.75, 0.8, 0.25, 0.4, 0.3])
            time = random.choice([2, 3, 4, 5, 6])
        else:
            # Time < 1
            rate = random.choice([20, 30, 40, 50, 60])
            time = random.choice([0.5, 0.6, 0.75, 0.8, 0.25, 0.4, 0.3])

        factor1 = float(rate)
        factor2 = float(time)

        # Calculate answers
        correct_product = factor1 * factor2

        # Malrule answer: add instead
        malrule_answer = factor1 + factor2

        rate_unit = random.choice(['miles per hour', 'km per hour', 'meters per second'])
        contexts = [
            f"A car travels at {factor1} {rate_unit} for {factor2} hours. How far does it travel?",
            f"If you walk at {factor1} {rate_unit} for {factor2} hours, what distance do you cover?",
            f"Calculate the distance: rate = {factor1} {rate_unit}, time = {factor2} hours.",
        ]
        problem_text = random.choice(contexts)

        distance_unit = rate_unit.split()[0]  # Extract just 'miles', 'km', or 'meters'

        return Problem(
            text=problem_text,
            operands=[factor1, factor2],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'factor1': factor1,
                'factor2': factor2,
                'rate': rate,
                'time': time,
                'rate_unit': rate_unit,
                'correct_answer': f'{correct_product:.4f} {distance_unit}',
                'malrule_answer': f'{malrule_answer:.4f}',
                'template': 'rate_distance',
                'problem_type': 'rate_time_distance'
            }
        )

    def _generate_volume_box(self, seed=None) -> Problem:
        """Generate volume problem with dimensions < 1."""
        if seed is not None:
            random.seed(seed)

        # Three dimensions less than 1
        length = random.choice([0.5, 0.6, 0.7, 0.75, 0.8, 0.4, 0.3])
        width = random.choice([0.5, 0.6, 0.7, 0.75, 0.8, 0.4, 0.3])
        height = random.choice([0.5, 0.6, 0.7, 0.75, 0.8, 0.4, 0.3])

        # For volume we need all three factors
        # We'll compute as (length × width) × height
        factor1 = length * width
        factor2 = height

        # Calculate answers
        correct_product = factor1 * factor2

        # Malrule answer: add instead
        malrule_answer = factor1 + factor2

        unit = random.choice(['meters', 'feet', 'centimeters'])
        contexts = [
            f"A small box has dimensions {length} {unit} × {width} {unit} × {height} {unit}. What is its volume?",
            f"Calculate the volume of a rectangular prism with length {length} {unit}, width {width} {unit}, and height {height} {unit}.",
            f"Find the volume: l = {length} {unit}, w = {width} {unit}, h = {height} {unit}.",
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[factor1, factor2],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'factor1': factor1,
                'factor2': factor2,
                'length': length,
                'width': width,
                'height': height,
                'unit': unit,
                'correct_answer': f'{correct_product:.6f} cubic {unit}',
                'malrule_answer': f'{malrule_answer:.6f}',
                'template': 'volume_box',
                'problem_type': 'volume_calculation'
            }
        )
