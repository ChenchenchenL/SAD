"""
Problem generator for Divide-Larger-By-Smaller-Always malrule.

Generates division problems where dividend < divisor, eliciting the
misconception that such divisions are "impossible" or should be reversed.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional, List
from utils import ProblemGenerator, Problem, DifficultyLevel


class DivideLargerBySmallerAlwaysProblemGenerator(ProblemGenerator):
    """
    Generates division problems with smaller dividend.

    Templates:
    1. basic_smaller_dividend - Basic dividend < divisor
    2. fraction_result - Explicitly showing fraction results
    3. decimal_friendly - Numbers that produce nice decimals
    4. word_problem_sharing - Real-world sharing contexts
    5. word_problem_measurement - Real-world measurement contexts
    """

    def get_name(self) -> str:
        return "Divide-Larger-By-Smaller-Always Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates division problems where dividend < divisor, to elicit "
            "the misconception that division must be larger ÷ smaller."
        )

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_smaller_dividend',
            'fraction_result',
            'decimal_friendly',
            'word_problem_sharing',
            'word_problem_measurement',
            'money_sharing',
            'probability_ratio',
            'percentage_grade',
            'ratio_comparison',
            'scale_model'
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level."""
        ranges = {
            3: {
                DifficultyLevel.EASY: {'dividend': (1, 10), 'divisor': (2, 12)},
                DifficultyLevel.MEDIUM: {'dividend': (1, 20), 'divisor': (2, 25)},
                DifficultyLevel.HARD: {'dividend': (1, 50), 'divisor': (2, 60)},
            },
            4: {
                DifficultyLevel.EASY: {'dividend': (1, 15), 'divisor': (2, 20)},
                DifficultyLevel.MEDIUM: {'dividend': (1, 30), 'divisor': (2, 40)},
                DifficultyLevel.HARD: {'dividend': (1, 100), 'divisor': (2, 120)},
            },
            5: {
                DifficultyLevel.EASY: {'dividend': (1, 20), 'divisor': (2, 30)},
                DifficultyLevel.MEDIUM: {'dividend': (1, 50), 'divisor': (2, 75)},
                DifficultyLevel.HARD: {'dividend': (1, 100), 'divisor': (2, 150)},
            },
            6: {
                DifficultyLevel.EASY: {'dividend': (1, 30), 'divisor': (2, 40)},
                DifficultyLevel.MEDIUM: {'dividend': (1, 100), 'divisor': (2, 150)},
                DifficultyLevel.HARD: {'dividend': (1, 200), 'divisor': (2, 300)},
            }
        }

        lvl = self.level if self.level in ranges else 4
        return ranges[lvl][self.difficulty]

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate a division problem with dividend < divisor.

        Args:
            seed: Optional random seed for reproducibility
            template: Optional template name

        Returns:
            Problem instance
        """
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            template = random.choice(self.get_available_templates())

        # Generate based on template
        if template == 'basic_smaller_dividend':
            return self._generate_basic_smaller_dividend(seed)
        elif template == 'fraction_result':
            return self._generate_fraction_result(seed)
        elif template == 'decimal_friendly':
            return self._generate_decimal_friendly(seed)
        elif template == 'word_problem_sharing':
            return self._generate_word_problem_sharing(seed)
        elif template == 'word_problem_measurement':
            return self._generate_word_problem_measurement(seed)
        elif template == 'money_sharing':
            return self._generate_money_sharing(seed)
        elif template == 'probability_ratio':
            return self._generate_probability_ratio(seed)
        elif template == 'percentage_grade':
            return self._generate_percentage_grade(seed)
        elif template == 'ratio_comparison':
            return self._generate_ratio_comparison(seed)
        elif template == 'scale_model':
            return self._generate_scale_model(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_smaller_dividend(self, seed: Optional[int] = None) -> Problem:
        """
        Generate basic smaller dividend problem (original template).

        Example: 4 ÷ 6
        Correct: 4 ÷ 6 = 0.667 (or 2/3)
        Malrule: 6 ÷ 4 = 1.5 (reversed operands)
        """
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        div_min, div_max = ranges['dividend']
        dvs_min, dvs_max = ranges['divisor']

        # Generate divisor first
        divisor = random.randint(dvs_min, dvs_max)

        # Generate dividend that is LESS than divisor
        dividend = random.randint(div_min, min(div_max, divisor - 1))

        # Ensure dividend < divisor
        if dividend >= divisor:
            dividend = random.randint(div_min, divisor - 1)

        problem_text = f"Calculate: {dividend} ÷ {divisor}"

        return Problem(
            text=problem_text,
            operands=[dividend, divisor],
            operation='division',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'dividend': dividend,
                'divisor': divisor,
                'template': 'basic_smaller_dividend',
                'problem_type': 'basic_division'
            }
        )

    def _generate_fraction_result(self, seed: Optional[int] = None) -> Problem:
        """
        Generate problem that results in a simple fraction.

        Example: 2 ÷ 3 = 2/3, 3 ÷ 4 = 3/4
        Uses numbers that result in recognizable fractions.
        """
        if seed is not None:
            random.seed(seed)

        # Common fraction pairs (dividend, divisor)
        fraction_pairs = [
            (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 8),
            (2, 3), (2, 5), (2, 7),
            (3, 4), (3, 5), (3, 7), (3, 8),
            (4, 5), (4, 7),
            (5, 6), (5, 8)
        ]

        dividend, divisor = random.choice(fraction_pairs)

        problem_text = f"Calculate: {dividend} ÷ {divisor} (express as a fraction or decimal)"

        return Problem(
            text=problem_text,
            operands=[dividend, divisor],
            operation='division',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'dividend': dividend,
                'divisor': divisor,
                'template': 'fraction_result',
                'fraction_form': f"{dividend}/{divisor}",
                'problem_type': 'fraction_division'
            }
        )

    def _generate_decimal_friendly(self, seed: Optional[int] = None) -> Problem:
        """
        Generate problem that results in a nice decimal.

        Example: 2 ÷ 4 = 0.5, 1 ÷ 4 = 0.25, 3 ÷ 4 = 0.75
        Uses numbers that produce terminating decimals.
        """
        if seed is not None:
            random.seed(seed)

        # Decimal-friendly pairs (dividend, divisor, decimal)
        decimal_pairs = [
            (1, 2),   # 0.5
            (1, 4),   # 0.25
            (2, 4),   # 0.5
            (3, 4),   # 0.75
            (1, 5),   # 0.2
            (2, 5),   # 0.4
            (3, 5),   # 0.6
            (4, 5),   # 0.8
            (1, 8),   # 0.125
            (3, 8),   # 0.375
            (5, 8),   # 0.625
            (2, 10),  # 0.2
            (5, 10),  # 0.5
        ]

        dividend, divisor = random.choice(decimal_pairs)

        problem_text = f"Calculate: {dividend} ÷ {divisor}"

        return Problem(
            text=problem_text,
            operands=[dividend, divisor],
            operation='division',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'dividend': dividend,
                'divisor': divisor,
                'template': 'decimal_friendly',
                'problem_type': 'decimal_division'
            }
        )

    def _generate_word_problem_sharing(self, seed: Optional[int] = None) -> Problem:
        """
        Generate word problem with sharing context.

        Example: "4 cookies shared among 6 people. How many cookies does each person get?"
        Shows real-world context where smaller ÷ larger makes sense.
        """
        if seed is not None:
            random.seed(seed)

        # Generate numbers
        divisor = random.randint(4, 12)  # Number of people/groups
        dividend = random.randint(1, divisor - 1)  # Number of items (less than divisor)

        contexts = [
            {
                'text': f"{dividend} cookies shared equally among {divisor} people. How many cookies does each person get?",
                'item': 'cookies',
                'recipients': 'people'
            },
            {
                'text': f"{dividend} pizzas divided equally among {divisor} friends. How much pizza does each friend get?",
                'item': 'pizzas',
                'recipients': 'friends'
            },
            {
                'text': f"{dividend} liters of juice shared among {divisor} students. How many liters does each student get?",
                'item': 'liters',
                'recipients': 'students'
            },
            {
                'text': f"{dividend} dollars divided equally among {divisor} children. How much does each child get?",
                'item': 'dollars',
                'recipients': 'children'
            }
        ]

        context = random.choice(contexts)
        problem_text = context['text']

        return Problem(
            text=problem_text,
            operands=[dividend, divisor],
            operation='division',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'dividend': dividend,
                'divisor': divisor,
                'template': 'word_problem_sharing',
                'context_type': 'sharing',
                'item': context['item'],
                'recipients': context['recipients'],
                'problem_type': 'word_problem_sharing'
            }
        )

    def _generate_word_problem_measurement(self, seed: Optional[int] = None) -> Problem:
        """
        Generate word problem with measurement context.

        Example: "A 3-foot rope is cut into 5 equal pieces. How long is each piece?"
        Shows measurement division where smaller ÷ larger makes sense.
        """
        if seed is not None:
            random.seed(seed)

        # Generate numbers
        divisor = random.randint(4, 10)  # Number of pieces
        dividend = random.randint(1, divisor - 1)  # Length/amount (less than divisor)

        contexts = [
            {
                'text': f"A {dividend}-foot rope is cut into {divisor} equal pieces. How long is each piece in feet?",
                'measurement': 'foot/feet',
                'unit': 'feet'
            },
            {
                'text': f"{dividend} meters of ribbon is divided into {divisor} equal strips. How long is each strip in meters?",
                'measurement': 'meters',
                'unit': 'meters'
            },
            {
                'text': f"{dividend} hours of work time is split into {divisor} equal shifts. How long is each shift in hours?",
                'measurement': 'hours',
                'unit': 'hours'
            },
            {
                'text': f"{dividend} kilograms of flour is divided into {divisor} equal portions. How much does each portion weigh?",
                'measurement': 'kilograms',
                'unit': 'kilograms'
            }
        ]

        context = random.choice(contexts)
        problem_text = context['text']

        return Problem(
            text=problem_text,
            operands=[dividend, divisor],
            operation='division',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'dividend': dividend,
                'divisor': divisor,
                'template': 'word_problem_measurement',
                'context_type': 'measurement',
                'measurement': context['measurement'],
                'unit': context['unit'],
                'problem_type': 'word_problem_measurement'
            }
        )

    def _generate_money_sharing(self, seed: Optional[int] = None) -> Problem:
        """Generate money sharing problem: Money divided among more people."""
        if seed is not None:
            random.seed(seed)

        # Total money (smaller amount)
        money = random.randint(10, 100)
        # Number of people (larger than money amount)
        people = random.randint(money + 10, money + 50)

        dividend = float(money)
        divisor = float(people)

        problem_texts = [
            f"${dividend:.0f} is shared equally among {divisor:.0f} people. How much does each person get?",
            f"If {divisor:.0f} workers split ${dividend:.0f} equally, how much does each worker receive?",
            f"Divide ${dividend:.0f} among {divisor:.0f} students. How much does each student get?",
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
                'template': 'money_sharing',
                'problem_type': 'money_division'
            }
        )

    def _generate_probability_ratio(self, seed: Optional[int] = None) -> Problem:
        """Generate probability ratio problem: favorable/total outcomes."""
        if seed is not None:
            random.seed(seed)

        # Favorable outcomes (smaller)
        favorable = random.randint(1, 10)
        # Total outcomes (larger)
        total = random.randint(favorable + 2, favorable + 20)

        dividend = float(favorable)
        divisor = float(total)

        problem_texts = [
            f"A bag has {divisor:.0f} marbles, {dividend:.0f} are red. What is the probability of picking a red marble?",
            f"In {divisor:.0f} attempts, you succeeded {dividend:.0f} times. What is your success rate as a decimal?",
            f"If {dividend:.0f} out of {divisor:.0f} students passed, what fraction represents the passing rate?",
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
                'favorable': favorable,
                'total': total,
                'template': 'probability_ratio',
                'problem_type': 'probability_calculation'
            }
        )

    def _generate_percentage_grade(self, seed: Optional[int] = None) -> Problem:
        """Generate percentage grade problem: score/total as percentage."""
        if seed is not None:
            random.seed(seed)

        # Score achieved (smaller)
        score = random.randint(50, 95)
        # Total possible (larger)
        total = random.randint(100, 150)

        dividend = float(score)
        divisor = float(total)

        problem_texts = [
            f"You scored {dividend:.0f} out of {divisor:.0f} points. What is your score as a decimal?",
            f"Calculate the grade: {dividend:.0f} points earned out of {divisor:.0f} total points.",
            f"If the test had {divisor:.0f} points and you got {dividend:.0f}, what decimal represents your score?",
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
                'score': score,
                'total_points': total,
                'template': 'percentage_grade',
                'problem_type': 'percentage_calculation'
            }
        )

    def _generate_ratio_comparison(self, seed: Optional[int] = None) -> Problem:
        """Generate ratio comparison problem: Smaller to larger ratios."""
        if seed is not None:
            random.seed(seed)

        # Smaller quantity
        small = random.randint(3, 15)
        # Larger quantity
        large = random.randint(small + 5, small + 30)

        dividend = float(small)
        divisor = float(large)

        items = [
            ['apples', 'oranges'],
            ['cats', 'dogs'],
            ['boys', 'girls'],
            ['red cars', 'blue cars']
        ]
        item_pair = random.choice(items)

        problem_texts = [
            f"The ratio of {item_pair[0]} to {item_pair[1]} is {dividend:.0f}:{divisor:.0f}. Express this as a decimal.",
            f"There are {dividend:.0f} {item_pair[0]} and {divisor:.0f} {item_pair[1]}. What is {dividend:.0f} ÷ {divisor:.0f}?",
            f"Compare {dividend:.0f} {item_pair[0]} to {divisor:.0f} {item_pair[1]} by dividing: {dividend:.0f} ÷ {divisor:.0f}.",
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
                'template': 'ratio_comparison',
                'problem_type': 'ratio_calculation'
            }
        )

    def _generate_scale_model(self, seed: Optional[int] = None) -> Problem:
        """Generate scale model problem: Model size to actual size."""
        if seed is not None:
            random.seed(seed)

        # Model size (smaller)
        model_size = random.randint(5, 20)
        # Actual size (larger)
        actual_size = random.randint(model_size * 10, model_size * 100)

        dividend = float(model_size)
        divisor = float(actual_size)

        problem_texts = [
            f"A model is {dividend:.0f} cm tall. The real object is {divisor:.0f} cm. What is the scale ratio?",
            f"The model measures {dividend:.0f} inches, the actual is {divisor:.0f} inches. Calculate {dividend:.0f} ÷ {divisor:.0f}.",
            f"A scale model: {dividend:.0f} cm represents {divisor:.0f} cm. What decimal shows the scale?",
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
                'model_size': model_size,
                'actual_size': actual_size,
                'template': 'scale_model',
                'problem_type': 'scale_calculation'
            }
        )
