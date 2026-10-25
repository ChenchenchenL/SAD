"""
Problem generator for Division-Makes-Smaller malrule.

Generates division problems with decimals/fractions less than 1 where
the result is actually larger than the dividend.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional, List
from utils import ProblemGenerator, Problem, DifficultyLevel


class DivisionWithDecimalsProblemGenerator(ProblemGenerator):
    """
    Generates division problems to elicit Division-Makes-Smaller malrule.

    Creates problems where dividing by a number less than 1 produces a
    quotient larger than the dividend, contradicting the student's expectation.

    Templates:
    1. basic_decimal_division - Standard decimal division (4 ÷ 0.5)
    2. fraction_division - Division by fractions less than 1 (6 ÷ 1/2)
    3. measurement_context - Cutting rope/boards into fractional pieces
    4. sharing_context - Dividing into fractional portions
    5. rate_context - Price/cost problems with fractional units
    """

    def get_name(self) -> str:
        return "Division with Decimals Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates division problems with decimal divisors less than 1 "
            "where the quotient is larger than the dividend, eliciting the "
            "misconception that division always makes numbers smaller."
        )

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_decimal_division',
            'fraction_division',
            'measurement_context',
            'sharing_context',
            'rate_context',
            'time_conversion',
            'capacity_division',
            'speed_calculation',
            'recipe_scaling_up',
            'unit_conversion'
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[float, float]]:
        """Get appropriate value ranges based on level."""
        ranges = {
            3: {
                DifficultyLevel.EASY: (2.0, 10.0),
                DifficultyLevel.MEDIUM: (5.0, 20.0),
                DifficultyLevel.HARD: (10.0, 50.0),
            },
            4: {
                DifficultyLevel.EASY: (2.0, 15.0),
                DifficultyLevel.MEDIUM: (5.0, 30.0),
                DifficultyLevel.HARD: (10.0, 60.0),
            },
            5: {
                DifficultyLevel.EASY: (2.0, 20.0),
                DifficultyLevel.MEDIUM: (5.0, 40.0),
                DifficultyLevel.HARD: (10.0, 80.0),
            },
            6: {
                DifficultyLevel.EASY: (2.0, 30.0),
                DifficultyLevel.MEDIUM: (10.0, 60.0),
                DifficultyLevel.HARD: (20.0, 100.0),
            }
        }

        lvl = self.level if self.level in ranges else 5
        return {'dividend': ranges[lvl][self.difficulty]}

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate a division problem based on selected template.

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
        if template == 'basic_decimal_division':
            return self._generate_basic_decimal_division(seed)
        elif template == 'fraction_division':
            return self._generate_fraction_division(seed)
        elif template == 'measurement_context':
            return self._generate_measurement_context(seed)
        elif template == 'sharing_context':
            return self._generate_sharing_context(seed)
        elif template == 'rate_context':
            return self._generate_rate_context(seed)
        elif template == 'time_conversion':
            return self._generate_time_conversion(seed)
        elif template == 'capacity_division':
            return self._generate_capacity_division(seed)
        elif template == 'speed_calculation':
            return self._generate_speed_calculation(seed)
        elif template == 'recipe_scaling_up':
            return self._generate_recipe_scaling_up(seed)
        elif template == 'unit_conversion':
            return self._generate_unit_conversion(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_decimal_division(self, seed=None) -> Problem:
        """Generate basic decimal division problem."""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['dividend']

        # Choose a dividend (whole number or simple decimal)
        dividend = round(random.uniform(min_val, min(max_val, 20)), 1)

        # Choose a decimal divisor less than 1
        divisor_choices = [0.1, 0.2, 0.25, 0.4, 0.5, 0.6, 0.75, 0.8]
        divisor = random.choice(divisor_choices)

        # Calculate answers
        correct_quotient = dividend / divisor

        # Malrule answer: multiply instead (because result would be larger)
        malrule_answer = dividend * divisor

        problem_texts = [
            f"What is {dividend} ÷ {divisor}?",
            f"Divide {dividend} by {divisor}",
            f"Calculate: {dividend} ÷ {divisor}",
        ]
        problem_text = random.choice(problem_texts)

        return Problem(
            text=problem_text,
            operands=[dividend, divisor],
            operation='division',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'dividend': dividend,
                'divisor': divisor,
                'correct_answer': f'{correct_quotient:.2f}',
                'malrule_answer': f'{malrule_answer:.2f}',
                'template': 'basic_decimal_division',
                'problem_type': 'basic_division'
            }
        )

    def _generate_fraction_division(self, seed=None) -> Problem:
        """Generate division by fraction problem."""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['dividend']

        # Choose a dividend (whole number)
        dividend = float(random.randint(int(min_val), min(int(max_val), 20)))

        # Common fractions less than 1
        fractions = [
            (1, 2, "1/2"),
            (1, 3, "1/3"),
            (1, 4, "1/4"),
            (2, 3, "2/3"),
            (3, 4, "3/4"),
            (2, 5, "2/5"),
            (3, 5, "3/5")
        ]
        num, denom, frac_str = random.choice(fractions)
        divisor = num / denom

        # Calculate answers
        correct_quotient = dividend / divisor

        # Malrule answer: multiply instead (because result would be larger)
        malrule_answer = dividend * divisor

        problem_texts = [
            f"What is {dividend:.0f} ÷ {frac_str}?",
            f"Divide {dividend:.0f} by {frac_str}",
            f"Calculate: {dividend:.0f} ÷ {frac_str}",
        ]
        problem_text = random.choice(problem_texts)

        return Problem(
            text=problem_text,
            operands=[dividend, divisor],
            operation='division',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'dividend': dividend,
                'divisor': divisor,
                'fraction_str': frac_str,
                'numerator': num,
                'denominator': denom,
                'correct_answer': f'{correct_quotient:.2f}',
                'malrule_answer': f'{malrule_answer:.2f}',
                'template': 'fraction_division',
                'problem_type': 'fraction_division'
            }
        )

    def _generate_measurement_context(self, seed=None) -> Problem:
        """Generate measurement context problem."""
        if seed is not None:
            random.seed(seed)

        # Total length to cut
        total_length = random.choice([4, 6, 8, 10, 12, 15, 20])

        # Fractional piece size
        piece_size = random.choice([0.5, 0.25, 0.2, 0.4, 0.75])

        dividend = float(total_length)
        divisor = piece_size

        # Calculate answers
        correct_quotient = dividend / divisor

        # Malrule answer: multiply instead (because result would be larger)
        malrule_answer = dividend * divisor

        unit = random.choice(['meters', 'feet', 'inches', 'yards'])
        contexts = [
            f"You have {dividend:.0f} {unit} of rope. How many {divisor} {unit} pieces can you cut?",
            f"A board is {dividend:.0f} {unit} long. If you cut it into pieces of {divisor} {unit}, how many pieces do you get?",
            f"How many {divisor} {unit} segments are in {dividend:.0f} {unit}?",
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[dividend, divisor],
            operation='division',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'dividend': dividend,
                'divisor': divisor,
                'unit': unit,
                'correct_answer': f'{correct_quotient:.0f} pieces',
                'malrule_answer': f'{malrule_answer:.1f} {unit}',
                'template': 'measurement_context',
                'problem_type': 'measurement_division'
            }
        )

    def _generate_sharing_context(self, seed=None) -> Problem:
        """Generate sharing/distribution context problem."""
        if seed is not None:
            random.seed(seed)

        # Total amount to share
        total_amount = random.choice([6, 8, 10, 12, 15, 20])

        # Fractional portion size
        portion_size = random.choice([0.5, 0.25, 0.75, 0.4, 0.6])

        dividend = float(total_amount)
        divisor = portion_size

        # Calculate answers
        correct_quotient = dividend / divisor

        # Malrule answer: multiply instead (because result would be larger)
        malrule_answer = dividend * divisor

        contexts = [
            {
                'text': f"You have {dividend:.0f} pizzas. Each person gets {divisor} of a pizza. How many people can you serve?",
                'correct_format': f'{correct_quotient:.0f} people',
                'malrule_format': f'{malrule_answer:.1f} pizzas'
            },
            {
                'text': f"There are {dividend:.0f} liters of juice. If each glass holds {divisor} liters, how many glasses can you fill?",
                'correct_format': f'{correct_quotient:.0f} glasses',
                'malrule_format': f'{malrule_answer:.1f} liters'
            },
            {
                'text': f"Share {dividend:.0f} cookies into portions of {divisor} cookies each. How many portions?",
                'correct_format': f'{correct_quotient:.0f} portions',
                'malrule_format': f'{malrule_answer:.1f} cookies'
            }
        ]
        context = random.choice(contexts)

        return Problem(
            text=context['text'],
            operands=[dividend, divisor],
            operation='division',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'dividend': dividend,
                'divisor': divisor,
                'correct_answer': context['correct_format'],
                'malrule_answer': context['malrule_format'],
                'template': 'sharing_context',
                'problem_type': 'sharing_division'
            }
        )

    def _generate_rate_context(self, seed=None) -> Problem:
        """Generate rate/price context problem."""
        if seed is not None:
            random.seed(seed)

        # Total amount of money
        total_cost = random.choice([10, 12, 15, 20, 24, 30])

        # Price per unit (fractional)
        price_per_unit = random.choice([0.5, 0.25, 0.75, 0.4, 0.6])

        dividend = float(total_cost)
        divisor = price_per_unit

        # Calculate answers
        correct_quotient = dividend / divisor

        # Malrule answer: multiply instead (because result would be larger)
        malrule_answer = dividend * divisor

        contexts = [
            {
                'text': f"You spend ${dividend:.0f} on items that cost ${divisor} each. How many items did you buy?",
                'correct_format': f'{correct_quotient:.0f} items',
                'malrule_format': f'${malrule_answer:.2f}'
            },
            {
                'text': f"At ${divisor} per pound, how many pounds can you buy with ${dividend:.0f}?",
                'correct_format': f'{correct_quotient:.0f} pounds',
                'malrule_format': f'${malrule_answer:.2f}'
            },
            {
                'text': f"Tickets cost ${divisor} each. How many can you buy with ${dividend:.0f}?",
                'correct_format': f'{correct_quotient:.0f} tickets',
                'malrule_format': f'${malrule_answer:.2f}'
            }
        ]
        context = random.choice(contexts)

        return Problem(
            text=context['text'],
            operands=[dividend, divisor],
            operation='division',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'dividend': dividend,
                'divisor': divisor,
                'correct_answer': context['correct_format'],
                'malrule_answer': context['malrule_format'],
                'template': 'rate_context',
                'problem_type': 'rate_calculation'
            }
        )

    def _generate_time_conversion(self, seed=None) -> Problem:
        """Generate time conversion problem: Hours divided into fractional shifts."""
        if seed is not None:
            random.seed(seed)

        # Total hours in a shift/day
        total_hours = random.choice([8, 10, 12, 16, 20, 24])

        # Fractional shift size (less than 1 hour)
        shift_fraction = random.choice([0.5, 0.25, 0.75, 0.4, 0.2])

        dividend = float(total_hours)
        divisor = shift_fraction

        # Calculate answers
        correct_quotient = dividend / divisor

        # Malrule answer: multiply instead (because result would be larger)
        malrule_answer = dividend * divisor

        contexts = [
            f"A {dividend:.0f}-hour workday is divided into shifts of {divisor} hours each. How many shifts are there?",
            f"You have {dividend:.0f} hours to complete tasks that take {divisor} hours each. How many tasks can you complete?",
            f"If {divisor} hours is one unit of time, how many such units are in {dividend:.0f} hours?",
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[dividend, divisor],
            operation='division',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'dividend': dividend,
                'divisor': divisor,
                'correct_answer': f'{correct_quotient:.0f} shifts',
                'malrule_answer': f'{malrule_answer:.1f} hours',
                'template': 'time_conversion',
                'problem_type': 'time_division'
            }
        )

    def _generate_capacity_division(self, seed=None) -> Problem:
        """Generate capacity division problem: Liters divided into fractional bottles."""
        if seed is not None:
            random.seed(seed)

        # Total liters
        total_liters = random.choice([6, 8, 10, 12, 15, 20])

        # Bottle capacity (fractional liters)
        bottle_capacity = random.choice([0.5, 0.25, 0.75, 0.4, 0.6])

        dividend = float(total_liters)
        divisor = bottle_capacity

        # Calculate answers
        correct_quotient = dividend / divisor

        # Malrule answer: multiply instead (because result would be larger)
        malrule_answer = dividend * divisor

        contexts = [
            f"You have {dividend:.0f} liters of water. How many {divisor}-liter bottles can you fill?",
            f"A tank contains {dividend:.0f} liters. If each container holds {divisor} liters, how many containers can you fill?",
            f"Divide {dividend:.0f} liters of juice into {divisor}-liter portions. How many portions?",
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[dividend, divisor],
            operation='division',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'dividend': dividend,
                'divisor': divisor,
                'correct_answer': f'{correct_quotient:.0f} bottles',
                'malrule_answer': f'{malrule_answer:.1f} liters',
                'template': 'capacity_division',
                'problem_type': 'capacity_calculation'
            }
        )

    def _generate_speed_calculation(self, seed=None) -> Problem:
        """Generate speed calculation problem: Speed = distance / time where divisor < 1."""
        if seed is not None:
            random.seed(seed)

        # Distance traveled
        distance = random.choice([10, 12, 15, 20, 24, 30])

        # Time (fractional hours)
        time = random.choice([0.5, 0.25, 0.75, 0.4, 0.6])

        dividend = float(distance)
        divisor = time

        # Calculate answers
        correct_quotient = dividend / divisor

        # Malrule answer: multiply instead (because result would be larger)
        malrule_answer = dividend * divisor

        unit = random.choice(['miles', 'kilometers'])
        contexts = [
            f"A car travels {dividend:.0f} {unit} in {divisor} hours. What is the speed in {unit} per hour?",
            f"If you cover {dividend:.0f} {unit} in {divisor} hours, what is your average speed?",
            f"Calculate the speed: distance = {dividend:.0f} {unit}, time = {divisor} hours.",
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[dividend, divisor],
            operation='division',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'dividend': dividend,
                'divisor': divisor,
                'distance': distance,
                'time': time,
                'unit': unit,
                'correct_answer': f'{correct_quotient:.1f} {unit} per hour',
                'malrule_answer': f'{malrule_answer:.1f} {unit}',
                'template': 'speed_calculation',
                'problem_type': 'speed_calculation'
            }
        )

    def _generate_recipe_scaling_up(self, seed=None) -> Problem:
        """Generate recipe scaling up problem (reverse direction)."""
        if seed is not None:
            random.seed(seed)

        # Original recipe amount
        original_amount = random.choice([2, 3, 4, 6, 8])

        # Scaling factor (less than 1 means fractional servings)
        scale_factor = random.choice([0.5, 0.25, 0.75, 0.4, 0.6])

        dividend = float(original_amount)
        divisor = scale_factor

        # Calculate answers
        correct_quotient = dividend / divisor

        # Malrule answer: multiply instead (because result would be larger)
        malrule_answer = dividend * divisor

        unit = random.choice(['cups', 'tablespoons', 'ounces', 'grams'])
        contexts = [
            f"A recipe uses {dividend:.0f} {unit} for {divisor} of the full batch. How much for a full batch?",
            f"If {divisor} portion requires {dividend:.0f} {unit}, how much for a whole portion?",
            f"You used {dividend:.0f} {unit} for {divisor} of the recipe. What's the full recipe amount?",
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[dividend, divisor],
            operation='division',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'dividend': dividend,
                'divisor': divisor,
                'unit': unit,
                'correct_answer': f'{correct_quotient:.1f} {unit}',
                'malrule_answer': f'{malrule_answer:.1f} {unit}',
                'template': 'recipe_scaling_up',
                'problem_type': 'recipe_scaling'
            }
        )

    def _generate_unit_conversion(self, seed=None) -> Problem:
        """Generate unit conversion problem with fractional divisors."""
        if seed is not None:
            random.seed(seed)

        # Amount to convert
        amount = random.choice([6, 8, 10, 12, 15, 20])

        # Conversion factor (fractional)
        conversion_factor = random.choice([0.5, 0.25, 0.75, 0.4, 0.6])

        dividend = float(amount)
        divisor = conversion_factor

        # Calculate answers
        correct_quotient = dividend / divisor

        # Malrule answer: multiply instead (because result would be larger)
        malrule_answer = dividend * divisor

        conversions = [
            {'from': 'meters', 'to': 'custom units'},
            {'from': 'kilograms', 'to': 'portions'},
            {'from': 'feet', 'to': 'sections'}
        ]
        conv = random.choice(conversions)

        contexts = [
            f"Convert {dividend:.0f} {conv['from']} to {conv['to']} where 1 {conv['to']} = {divisor} {conv['from']}. How many {conv['to']}?",
            f"If {divisor} {conv['from']} equals one {conv['to']}, how many {conv['to']} are in {dividend:.0f} {conv['from']}?",
            f"You have {dividend:.0f} {conv['from']}. With {divisor} {conv['from']} per {conv['to']}, how many {conv['to']}?",
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[dividend, divisor],
            operation='division',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'dividend': dividend,
                'divisor': divisor,
                'from_unit': conv['from'],
                'to_unit': conv['to'],
                'correct_answer': f'{correct_quotient:.1f} {conv["to"]}',
                'malrule_answer': f'{malrule_answer:.1f} {conv["from"]}',
                'template': 'unit_conversion',
                'problem_type': 'unit_conversion'
            }
        )
