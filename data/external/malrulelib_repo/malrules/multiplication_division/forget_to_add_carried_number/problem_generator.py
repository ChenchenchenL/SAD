"""
Problem generator for Forget-To-Add-Carried-Number malrule.
"""

import random
import sys
sys.path.append('/home/user/malrule-coding')

from typing import List, Optional
from utils import Problem, ProblemGenerator, DifficultyLevel


class ForgetToAddCarriedNumberProblemGenerator(ProblemGenerator):
    """
    Generates multiplication problems where carrying occurs.

    Templates:
    1. basic_two_digit_times_one - 2-digit × 1-digit multiplication
    2. three_digit_times_one - 3-digit × 1-digit (multiple carries)
    3. two_digit_times_two - 2-digit × 2-digit (partial products)
    4. money_context - Money multiplication problems
    5. word_problem - Real-world multiplication contexts
    """

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_two_digit_times_one',
            'three_digit_times_one',
            'two_digit_times_two',
            'money_context',
            'word_problem',
            'three_digit_times_two',
            'area_calculation',
            'total_cost_bulk',
            'distance_calculation',
            'array_larger'
        ]

    def get_value_ranges(self):
        """Return the value ranges for problem generation based on difficulty."""
        if self.difficulty == DifficultyLevel.EASY:
            return {
                'tens_digit': (1, 5),
                'ones_digit': (2, 9),
                'multiplier': (2, 5)
            }
        elif self.difficulty == DifficultyLevel.MEDIUM:
            return {
                'tens_digit': (1, 9),
                'ones_digit': (2, 9),
                'multiplier': (2, 9)
            }
        else:  # HARD
            return {
                'tens_digit': (3, 9),
                'ones_digit': (5, 9),
                'multiplier': (5, 9)
            }

    def generate(self, seed=None, template: Optional[str] = None):
        """
        Generate a multiplication problem with carrying.

        Args:
            seed: Optional random seed for reproducibility
            template: Optional template name to use

        Returns:
            Problem with multiplication that requires carrying
        """
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            template = random.choice(self.get_available_templates())

        # Generate based on template
        if template == 'basic_two_digit_times_one':
            return self._generate_basic_two_digit_times_one(seed)
        elif template == 'three_digit_times_one':
            return self._generate_three_digit_times_one(seed)
        elif template == 'two_digit_times_two':
            return self._generate_two_digit_times_two(seed)
        elif template == 'money_context':
            return self._generate_money_context(seed)
        elif template == 'word_problem':
            return self._generate_word_problem(seed)
        elif template == 'three_digit_times_two':
            return self._generate_three_digit_times_two(seed)
        elif template == 'area_calculation':
            return self._generate_area_calculation(seed)
        elif template == 'total_cost_bulk':
            return self._generate_total_cost_bulk(seed)
        elif template == 'distance_calculation':
            return self._generate_distance_calculation(seed)
        elif template == 'array_larger':
            return self._generate_array_larger(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_two_digit_times_one(self, seed=None) -> Problem:
        """Generate basic 2-digit × 1-digit problem."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()

        # Generate a 2-digit number
        tens_digit = random.randint(ranges['tens_digit'][0], ranges['tens_digit'][1])
        ones_digit = random.randint(ranges['ones_digit'][0], ranges['ones_digit'][1])
        multiplicand = tens_digit * 10 + ones_digit

        # Generate multiplier
        multiplier = random.randint(ranges['multiplier'][0], ranges['multiplier'][1])

        # Ensure ones product creates a carry (>= 10)
        attempts = 0
        while ones_digit * multiplier < 10 and attempts < 20:
            ones_digit = random.randint(ranges['ones_digit'][0], ranges['ones_digit'][1])
            multiplicand = tens_digit * 10 + ones_digit
            attempts += 1

        # Calculate correct answer
        correct_answer = multiplicand * multiplier

        # Calculate steps
        ones_product = ones_digit * multiplier
        ones_result = ones_product % 10
        carry = ones_product // 10
        tens_product = tens_digit * multiplier
        tens_with_carry = tens_product + carry

        # Malrule answer (forgets carry)
        tens_without_carry = tens_product
        malrule_answer = tens_without_carry * 10 + ones_result

        return Problem(
            text=f"{multiplicand} × {multiplier} = ?",
            operands=[multiplicand, multiplier],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'multiplicand': multiplicand,
                'multiplier': multiplier,
                'tens_digit': tens_digit,
                'ones_digit': ones_digit,
                'ones_product': ones_product,
                'ones_result': ones_result,
                'carry': carry,
                'tens_product': tens_product,
                'tens_with_carry': tens_with_carry,
                'tens_without_carry': tens_without_carry,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'template': 'basic_two_digit_times_one',
                'problem_type': 'basic_multiplication'
            }
        )

    def _generate_three_digit_times_one(self, seed=None) -> Problem:
        """Generate 3-digit × 1-digit problem with multiple carries."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()

        # Generate a 3-digit number
        hundreds_digit = random.randint(1, 5)
        tens_digit = random.randint(ranges['tens_digit'][0], ranges['tens_digit'][1])
        ones_digit = random.randint(ranges['ones_digit'][0], ranges['ones_digit'][1])
        multiplicand = hundreds_digit * 100 + tens_digit * 10 + ones_digit

        # Generate multiplier
        multiplier = random.randint(ranges['multiplier'][0], min(ranges['multiplier'][1], 7))

        # Ensure ones product creates a carry
        attempts = 0
        while ones_digit * multiplier < 10 and attempts < 20:
            ones_digit = random.randint(ranges['ones_digit'][0], ranges['ones_digit'][1])
            multiplicand = hundreds_digit * 100 + tens_digit * 10 + ones_digit
            attempts += 1

        # Calculate correct answer
        correct_answer = multiplicand * multiplier

        # Calculate step-by-step
        ones_product = ones_digit * multiplier
        ones_result = ones_product % 10
        carry_to_tens = ones_product // 10

        tens_product = tens_digit * multiplier
        tens_with_carry = tens_product + carry_to_tens
        tens_result = tens_with_carry % 10
        carry_to_hundreds = tens_with_carry // 10

        hundreds_product = hundreds_digit * multiplier
        hundreds_with_carry = hundreds_product + carry_to_hundreds

        # Malrule: forget carry from ones to tens
        tens_without_carry = tens_product
        malrule_tens_result = tens_without_carry % 10
        malrule_carry_to_hundreds = tens_without_carry // 10
        malrule_hundreds = hundreds_product + malrule_carry_to_hundreds
        malrule_answer = malrule_hundreds * 100 + malrule_tens_result * 10 + ones_result

        return Problem(
            text=f"Calculate: {multiplicand} × {multiplier}",
            operands=[multiplicand, multiplier],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'multiplicand': multiplicand,
                'multiplier': multiplier,
                'hundreds_digit': hundreds_digit,
                'tens_digit': tens_digit,
                'ones_digit': ones_digit,
                'ones_product': ones_product,
                'ones_result': ones_result,
                'carry_to_tens': carry_to_tens,
                'tens_product': tens_product,
                'tens_with_carry': tens_with_carry,
                'carry_to_hundreds': carry_to_hundreds,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'template': 'three_digit_times_one',
                'problem_type': 'multi_digit_multiplication'
            }
        )

    def _generate_two_digit_times_two(self, seed=None) -> Problem:
        """Generate 2-digit × 2-digit problem."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()

        # Generate first 2-digit number
        tens1 = random.randint(1, min(ranges['tens_digit'][1], 5))
        ones1 = random.randint(ranges['ones_digit'][0], min(ranges['ones_digit'][1], 7))
        num1 = tens1 * 10 + ones1

        # Generate second 2-digit number
        tens2 = random.randint(1, min(ranges['tens_digit'][1], 5))
        ones2 = random.randint(ranges['ones_digit'][0], min(ranges['ones_digit'][1], 7))
        num2 = tens2 * 10 + ones2

        # Ensure ones products create carries
        attempts = 0
        while (ones1 * ones2 < 10 or ones1 * tens2 < 10) and attempts < 20:
            ones1 = random.randint(ranges['ones_digit'][0], min(ranges['ones_digit'][1], 7))
            num1 = tens1 * 10 + ones1
            attempts += 1

        # Calculate correct answer
        correct_answer = num1 * num2

        # Calculate partial product 1 (num1 × ones2)
        pp1_ones = ones1 * ones2
        pp1_ones_digit = pp1_ones % 10
        pp1_carry = pp1_ones // 10
        pp1_tens = tens1 * ones2 + pp1_carry
        partial_product_1 = pp1_tens * 10 + pp1_ones_digit

        # Calculate partial product 2 (num1 × tens2, shifted left)
        pp2_ones = ones1 * tens2
        pp2_ones_digit = pp2_ones % 10
        pp2_carry = pp2_ones // 10
        pp2_tens = tens1 * tens2 + pp2_carry
        partial_product_2 = pp2_tens * 10 + pp2_ones_digit

        # Malrule: forget carry in first partial product
        malrule_pp1_tens = tens1 * ones2  # Missing the carry!
        malrule_pp1 = malrule_pp1_tens * 10 + pp1_ones_digit
        malrule_answer = malrule_pp1 + partial_product_2 * 10

        return Problem(
            text=f"Multiply: {num1} × {num2}",
            operands=[num1, num2],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': num1,
                'num2': num2,
                'tens1': tens1,
                'ones1': ones1,
                'tens2': tens2,
                'ones2': ones2,
                'partial_product_1': partial_product_1,
                'partial_product_2': partial_product_2,
                'pp1_carry': pp1_carry,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'template': 'two_digit_times_two',
                'problem_type': 'two_digit_by_two_digit'
            }
        )

    def _generate_money_context(self, seed=None) -> Problem:
        """Generate money multiplication problem."""
        if seed is not None:
            random.seed(seed)

        contexts = [
            {
                'item': 'toy',
                'text': 'A toy costs ${dollars}.{cents}. If you buy {mult} toys, how much do you spend?',
                'answer_format': '${answer}'
            },
            {
                'item': 'book',
                'text': 'Each book costs ${dollars}.{cents}. What is the total cost of {mult} books?',
                'answer_format': '${answer}'
            },
            {
                'item': 'ticket',
                'text': '{mult} movie tickets cost ${dollars}.{cents} each. What is the total cost?',
                'answer_format': '${answer}'
            }
        ]

        context = random.choice(contexts)
        ranges = self.get_value_ranges()

        # Generate price (in cents to avoid floating point)
        dollars = random.randint(ranges['tens_digit'][0], min(ranges['tens_digit'][1], 7))
        cents = random.randint(15, 95)

        # Ensure cents multiplication creates carry
        multiplier = random.randint(ranges['multiplier'][0], min(ranges['multiplier'][1], 7))
        attempts = 0
        while (cents % 10) * multiplier < 10 and attempts < 20:
            cents = random.randint(15, 95)
            attempts += 1

        price_cents = dollars * 100 + cents

        # Calculate correct total
        correct_total_cents = price_cents * multiplier
        correct_dollars = correct_total_cents // 100
        correct_cents = correct_total_cents % 100

        # Calculate malrule answer (forget carry when multiplying cents)
        ones_digit = cents % 10
        tens_digit = cents // 10

        ones_product = ones_digit * multiplier
        ones_result = ones_product % 10
        carry = ones_product // 10

        tens_product = tens_digit * multiplier
        # Malrule: forget carry in cents calculation
        malrule_cents = tens_product * 10 + ones_result
        malrule_dollars = dollars * multiplier + (malrule_cents // 100)
        malrule_cents = malrule_cents % 100

        malrule_total_cents = malrule_dollars * 100 + malrule_cents

        problem_text = context['text'].format(
            dollars=dollars,
            cents=f"{cents:02d}",
            mult=multiplier
        )

        correct_answer = context['answer_format'].format(
            answer=f"{correct_dollars}.{correct_cents:02d}"
        )
        malrule_answer = context['answer_format'].format(
            answer=f"{malrule_dollars}.{malrule_cents:02d}"
        )

        return Problem(
            text=problem_text,
            operands=[price_cents, multiplier],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'multiplicand': price_cents,
                'multiplier': multiplier,
                'tens_digit': tens_digit,
                'ones_digit': ones_digit,
                'ones_product': ones_product,
                'ones_result': ones_result,
                'carry': carry,
                'tens_product': tens_product,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'context_type': context['item'],
                'template': 'money_context',
                'problem_type': 'money_calculation'
            }
        )

    def _generate_word_problem(self, seed=None) -> Problem:
        """Generate real-world word problem."""
        if seed is not None:
            random.seed(seed)

        contexts = [
            {
                'text': 'A classroom has {mult} rows of desks. Each row has {num} desks. How many desks total?',
                'answer_format': '{answer} desks',
                'type': 'classroom'
            },
            {
                'text': 'A garden has {mult} rows of plants with {num} plants in each row. How many plants total?',
                'answer_format': '{answer} plants',
                'type': 'garden'
            },
            {
                'text': 'A parking lot has {mult} rows with {num} parking spaces in each row. How many spaces total?',
                'answer_format': '{answer} spaces',
                'type': 'parking'
            }
        ]

        context = random.choice(contexts)
        ranges = self.get_value_ranges()

        # Generate number with carry
        tens_digit = random.randint(ranges['tens_digit'][0], ranges['tens_digit'][1])
        ones_digit = random.randint(ranges['ones_digit'][0], ranges['ones_digit'][1])
        multiplicand = tens_digit * 10 + ones_digit

        multiplier = random.randint(ranges['multiplier'][0], ranges['multiplier'][1])

        # Ensure carrying occurs
        attempts = 0
        while ones_digit * multiplier < 10 and attempts < 20:
            ones_digit = random.randint(ranges['ones_digit'][0], ranges['ones_digit'][1])
            multiplicand = tens_digit * 10 + ones_digit
            attempts += 1

        # Calculate correct answer
        correct_answer_value = multiplicand * multiplier

        # Calculate steps
        ones_product = ones_digit * multiplier
        ones_result = ones_product % 10
        carry = ones_product // 10
        tens_product = tens_digit * multiplier

        # Malrule answer (forget carry)
        malrule_answer_value = tens_product * 10 + ones_result

        problem_text = context['text'].format(num=multiplicand, mult=multiplier)
        correct_answer = context['answer_format'].format(answer=correct_answer_value)
        malrule_answer = context['answer_format'].format(answer=malrule_answer_value)

        return Problem(
            text=problem_text,
            operands=[multiplicand, multiplier],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'multiplicand': multiplicand,
                'multiplier': multiplier,
                'tens_digit': tens_digit,
                'ones_digit': ones_digit,
                'ones_product': ones_product,
                'ones_result': ones_result,
                'carry': carry,
                'tens_product': tens_product,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'context_type': context['type'],
                'template': 'word_problem',
                'problem_type': 'word_problem'
            }
        )

    def _generate_three_digit_times_two(self, seed=None) -> Problem:
        """Generate 3-digit × 2-digit problem (e.g., 345 × 23)."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()

        # Generate 3-digit number
        hundreds = random.randint(1, 5)
        tens = random.randint(2, 9)
        ones = random.randint(2, 9)
        num1 = hundreds * 100 + tens * 10 + ones

        # Generate 2-digit number
        tens2 = random.randint(1, 4)
        ones2 = random.randint(2, 7)
        num2 = tens2 * 10 + ones2

        # Ensure carrying occurs
        attempts = 0
        while ones * ones2 < 10 and attempts < 20:
            ones = random.randint(2, 9)
            num1 = hundreds * 100 + tens * 10 + ones
            attempts += 1

        # Calculate correct answer
        correct_answer = num1 * num2

        # Calculate partial products for malrule
        # First partial: num1 × ones2
        pp1_ones = ones * ones2
        pp1_ones_result = pp1_ones % 10
        pp1_carry_to_tens = pp1_ones // 10

        pp1_tens = tens * ones2 + pp1_carry_to_tens
        pp1_tens_result = pp1_tens % 10
        pp1_carry_to_hundreds = pp1_tens // 10

        pp1_hundreds = hundreds * ones2 + pp1_carry_to_hundreds
        partial_product_1 = pp1_hundreds * 100 + pp1_tens_result * 10 + pp1_ones_result

        # Malrule: forget carry in first partial product
        malrule_pp1_tens = tens * ones2  # Forget to add carry!
        malrule_pp1_tens_result = malrule_pp1_tens % 10
        malrule_pp1_carry = malrule_pp1_tens // 10
        malrule_pp1_hundreds = hundreds * ones2 + malrule_pp1_carry
        malrule_pp1 = malrule_pp1_hundreds * 100 + malrule_pp1_tens_result * 10 + pp1_ones_result

        # Second partial: num1 × tens2 (shifted)
        partial_product_2 = num1 * tens2

        # Malrule answer
        malrule_answer = malrule_pp1 + partial_product_2 * 10

        problem_texts = [
            f"Calculate {num1} × {num2}",
            f"What is {num1} × {num2}?",
            f"Multiply: {num1} × {num2}"
        ]
        problem_text = random.choice(problem_texts)

        return Problem(
            text=problem_text,
            operands=[num1, num2],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': num1,
                'num2': num2,
                'hundreds': hundreds,
                'tens': tens,
                'ones': ones,
                'tens2': tens2,
                'ones2': ones2,
                'pp1_carry_to_tens': pp1_carry_to_tens,
                'partial_product_1': partial_product_1,
                'partial_product_2': partial_product_2,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'template': 'three_digit_times_two',
                'problem_type': 'large_multiplication'
            }
        )

    def _generate_area_calculation(self, seed=None) -> Problem:
        """Generate area problem with multi-digit dimensions requiring carrying."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()

        # Generate length (2-digit)
        tens1 = random.randint(ranges['tens_digit'][0], min(ranges['tens_digit'][1], 6))
        ones1 = random.randint(ranges['ones_digit'][0], ranges['ones_digit'][1])
        length = tens1 * 10 + ones1

        # Generate width (1-digit or 2-digit)
        width = random.randint(ranges['multiplier'][0], min(ranges['multiplier'][1], 9))

        # Ensure carrying occurs
        attempts = 0
        while ones1 * width < 10 and attempts < 20:
            ones1 = random.randint(ranges['ones_digit'][0], ranges['ones_digit'][1])
            length = tens1 * 10 + ones1
            attempts += 1

        # Calculate correct area
        correct_answer = length * width

        # Calculate malrule (forget carry)
        ones_product = ones1 * width
        ones_result = ones_product % 10
        carry = ones_product // 10
        tens_product = tens1 * width
        malrule_answer = tens_product * 10 + ones_result

        unit = random.choice(['meters', 'feet', 'yards', 'centimeters'])
        problem_texts = [
            f"A rectangular garden is {length} {unit} long and {width} {unit} wide. What is the area in square {unit}?",
            f"Find the area of a rectangle with length {length} {unit} and width {width} {unit}.",
            f"A field measures {length} {unit} by {width} {unit}. Calculate the area."
        ]
        problem_text = random.choice(problem_texts)

        return Problem(
            text=problem_text,
            operands=[length, width],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'multiplicand': length,
                'multiplier': width,
                'tens_digit': tens1,
                'ones_digit': ones1,
                'length': length,
                'width': width,
                'unit': unit,
                'ones_product': ones_product,
                'ones_result': ones_result,
                'carry': carry,
                'tens_product': tens_product,
                'correct_answer': f'{correct_answer} square {unit}',
                'malrule_answer': f'{malrule_answer} square {unit}',
                'template': 'area_calculation',
                'problem_type': 'area_calculation'
            }
        )

    def _generate_total_cost_bulk(self, seed=None) -> Problem:
        """Generate bulk purchase problem with larger prices."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()

        # Generate price (2-digit)
        tens = random.randint(ranges['tens_digit'][0], min(ranges['tens_digit'][1], 7))
        ones = random.randint(ranges['ones_digit'][0], ranges['ones_digit'][1])
        price = tens * 10 + ones

        # Generate quantity
        quantity = random.randint(ranges['multiplier'][0], min(ranges['multiplier'][1], 9))

        # Ensure carrying occurs
        attempts = 0
        while ones * quantity < 10 and attempts < 20:
            ones = random.randint(ranges['ones_digit'][0], ranges['ones_digit'][1])
            price = tens * 10 + ones
            attempts += 1

        # Calculate correct total
        correct_total = price * quantity

        # Calculate malrule (forget carry)
        ones_product = ones * quantity
        ones_result = ones_product % 10
        carry = ones_product // 10
        tens_product = tens * quantity
        malrule_total = tens_product * 10 + ones_result

        items = ['notebooks', 'pens', 'pencils', 'markers', 'erasers', 'folders']
        item = random.choice(items)

        problem_texts = [
            f"Each {item[:-1]} costs ${price}. If you buy {quantity} {item}, what is the total cost?",
            f"A store sells {item} for ${price} each. What is the cost of {quantity} {item}?",
            f"You need to buy {quantity} {item} at ${price} each. How much will you spend?"
        ]
        problem_text = random.choice(problem_texts)

        return Problem(
            text=problem_text,
            operands=[price, quantity],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'multiplicand': price,
                'multiplier': quantity,
                'tens_digit': tens,
                'ones_digit': ones,
                'price': price,
                'quantity': quantity,
                'item': item,
                'ones_product': ones_product,
                'ones_result': ones_result,
                'carry': carry,
                'tens_product': tens_product,
                'correct_answer': f'${correct_total}',
                'malrule_answer': f'${malrule_total}',
                'template': 'total_cost_bulk',
                'problem_type': 'bulk_purchase'
            }
        )

    def _generate_distance_calculation(self, seed=None) -> Problem:
        """Generate rate × time problem requiring carrying."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()

        # Generate rate (2-digit speed)
        tens = random.randint(ranges['tens_digit'][0], min(ranges['tens_digit'][1], 6))
        ones = random.randint(ranges['ones_digit'][0], ranges['ones_digit'][1])
        rate = tens * 10 + ones

        # Generate time (single digit hours)
        time = random.randint(ranges['multiplier'][0], min(ranges['multiplier'][1], 8))

        # Ensure carrying occurs
        attempts = 0
        while ones * time < 10 and attempts < 20:
            ones = random.randint(ranges['ones_digit'][0], ranges['ones_digit'][1])
            rate = tens * 10 + ones
            attempts += 1

        # Calculate correct distance
        correct_distance = rate * time

        # Calculate malrule (forget carry)
        ones_product = ones * time
        ones_result = ones_product % 10
        carry = ones_product // 10
        tens_product = tens * time
        malrule_distance = tens_product * 10 + ones_result

        unit = random.choice(['miles per hour', 'km per hour', 'meters per second'])
        distance_unit = unit.split()[0]

        problem_texts = [
            f"A car travels at {rate} {unit} for {time} hours. How far does it travel?",
            f"If you drive at {rate} {unit} for {time} hours, what distance do you cover?",
            f"Calculate the distance: speed = {rate} {unit}, time = {time} hours."
        ]
        problem_text = random.choice(problem_texts)

        return Problem(
            text=problem_text,
            operands=[rate, time],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'multiplicand': rate,
                'multiplier': time,
                'tens_digit': tens,
                'ones_digit': ones,
                'rate': rate,
                'time': time,
                'unit': unit,
                'ones_product': ones_product,
                'ones_result': ones_result,
                'carry': carry,
                'tens_product': tens_product,
                'correct_answer': f'{correct_distance} {distance_unit}',
                'malrule_answer': f'{malrule_distance} {distance_unit}',
                'template': 'distance_calculation',
                'problem_type': 'rate_time_distance'
            }
        )

    def _generate_array_larger(self, seed=None) -> Problem:
        """Generate larger array/grid problem."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()

        # Generate rows (2-digit)
        tens = random.randint(ranges['tens_digit'][0], min(ranges['tens_digit'][1], 6))
        ones = random.randint(ranges['ones_digit'][0], ranges['ones_digit'][1])
        rows = tens * 10 + ones

        # Generate columns
        columns = random.randint(ranges['multiplier'][0], min(ranges['multiplier'][1], 9))

        # Ensure carrying occurs
        attempts = 0
        while ones * columns < 10 and attempts < 20:
            ones = random.randint(ranges['ones_digit'][0], ranges['ones_digit'][1])
            rows = tens * 10 + ones
            attempts += 1

        # Calculate correct total
        correct_total = rows * columns

        # Calculate malrule (forget carry)
        ones_product = ones * columns
        ones_result = ones_product % 10
        carry = ones_product // 10
        tens_product = tens * columns
        malrule_total = tens_product * 10 + ones_result

        contexts = [
            {
                'text': f'An auditorium has {rows} rows with {columns} seats in each row. How many seats total?',
                'answer_format': '{answer} seats'
            },
            {
                'text': f'A parking lot has {rows} rows with {columns} parking spaces per row. How many total spaces?',
                'answer_format': '{answer} spaces'
            },
            {
                'text': f'A display has {rows} shelves with {columns} items on each shelf. How many items in total?',
                'answer_format': '{answer} items'
            }
        ]
        context = random.choice(contexts)

        problem_text = context['text']
        correct_answer = context['answer_format'].format(answer=correct_total)
        malrule_answer = context['answer_format'].format(answer=malrule_total)

        return Problem(
            text=problem_text,
            operands=[rows, columns],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'multiplicand': rows,
                'multiplier': columns,
                'tens_digit': tens,
                'ones_digit': ones,
                'rows': rows,
                'columns': columns,
                'ones_product': ones_product,
                'ones_result': ones_result,
                'carry': carry,
                'tens_product': tens_product,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'array_larger',
                'problem_type': 'array_multiplication'
            }
        )
