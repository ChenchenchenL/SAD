"""
Problem generator for Absolute-Value-Distributes malrule.
"""

import random
import sys
sys.path.append('/home/user/malrule-coding')

from typing import List, Optional
from utils import Problem, ProblemGenerator, DifficultyLevel


class AbsoluteValueDistributesProblemGenerator(ProblemGenerator):
    """
    Generates absolute value distribution problems.

    Templates:
    1. basic_addition - |x + c| problems
    2. basic_subtraction - |x - c| problems
    3. negative_result_inside - Cases where expression inside is negative
    4. multiplication_inside - |ax + b| with coefficient on x
    5. word_problem - Real-world distance/temperature contexts
    """

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_addition',
            'basic_subtraction',
            'negative_result_inside',
            'multiplication_inside',
            'word_problem'
        ]

    def get_value_ranges(self):
        """Return the value ranges for problem generation."""
        if self.difficulty == DifficultyLevel.EASY:
            return {
                'x_value': (-5, 5),
                'constant': (1, 5),
                'coefficient': (2, 3)
            }
        elif self.difficulty == DifficultyLevel.MEDIUM:
            return {
                'x_value': (-10, 10),
                'constant': (1, 10),
                'coefficient': (2, 5)
            }
        else:  # HARD
            return {
                'x_value': (-20, 20),
                'constant': (1, 15),
                'coefficient': (2, 7)
            }

    def generate(self, seed=None, template: Optional[str] = None):
        """
        Generate an absolute value distribution problem.

        Args:
            seed: Optional random seed for reproducibility
            template: Optional template name to use

        Returns:
            Problem with absolute value expression
        """
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            template = random.choice(self.get_available_templates())

        # Generate based on template
        if template == 'basic_addition':
            return self._generate_basic_addition(seed)
        elif template == 'basic_subtraction':
            return self._generate_basic_subtraction(seed)
        elif template == 'negative_result_inside':
            return self._generate_negative_result_inside(seed)
        elif template == 'multiplication_inside':
            return self._generate_multiplication_inside(seed)
        elif template == 'word_problem':
            return self._generate_word_problem(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_addition(self, seed=None) -> Problem:
        """Generate basic |x + c| problems."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        x = random.randint(ranges['x_value'][0], ranges['x_value'][1])
        while x == 0:
            x = random.randint(ranges['x_value'][0], ranges['x_value'][1])

        c = random.randint(ranges['constant'][0], ranges['constant'][1])

        expression_value = x + c
        correct_answer = abs(expression_value)
        malrule_answer = abs(x) + c

        return Problem(
            text=f"Evaluate |x + {c}| when x = {x}",
            operands=[x, c],
            operation='absolute_value',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'x_value': x,
                'constant': c,
                'operation': '+',
                'expression': f"x + {c}",
                'expression_value': expression_value,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'template': 'basic_addition'
            }
        )

    def _generate_basic_subtraction(self, seed=None) -> Problem:
        """Generate basic |x - c| problems."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        x = random.randint(ranges['x_value'][0], ranges['x_value'][1])
        while x == 0:
            x = random.randint(ranges['x_value'][0], ranges['x_value'][1])

        c = random.randint(ranges['constant'][0], ranges['constant'][1])

        expression_value = x - c
        correct_answer = abs(expression_value)
        malrule_answer = abs(x) - c

        return Problem(
            text=f"Evaluate |x - {c}| when x = {x}",
            operands=[x, c],
            operation='absolute_value',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'x_value': x,
                'constant': c,
                'operation': '-',
                'expression': f"x - {c}",
                'expression_value': expression_value,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'template': 'basic_subtraction'
            }
        )

    def _generate_negative_result_inside(self, seed=None) -> Problem:
        """Generate problems where expression inside is negative (highlights error)."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()

        # Choose x negative and c positive, ensuring x + c < 0
        x = random.randint(ranges['x_value'][0], -1)
        c = random.randint(ranges['constant'][0], ranges['constant'][1])

        # Ensure x + c < 0 to make error more obvious
        attempts = 0
        while x + c >= 0 and attempts < 20:
            x = random.randint(ranges['x_value'][0], -1)
            c = random.randint(ranges['constant'][0], ranges['constant'][1])
            attempts += 1

        expression_value = x + c
        correct_answer = abs(expression_value)
        malrule_answer = abs(x) + c

        return Problem(
            text=f"Calculate |x + {c}| when x = {x}",
            operands=[x, c],
            operation='absolute_value',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'x_value': x,
                'constant': c,
                'operation': '+',
                'expression': f"x + {c}",
                'expression_value': expression_value,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'template': 'negative_result_inside'
            }
        )

    def _generate_multiplication_inside(self, seed=None) -> Problem:
        """Generate |ax + b| with coefficient on x."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        x = random.randint(ranges['x_value'][0], ranges['x_value'][1])
        while x == 0:
            x = random.randint(ranges['x_value'][0], ranges['x_value'][1])

        a = random.randint(ranges['coefficient'][0], ranges['coefficient'][1])
        b = random.randint(ranges['constant'][0], ranges['constant'][1])

        # Randomly make b negative sometimes
        if random.random() < 0.5:
            b = -b

        expression_value = a * x + b
        correct_answer = abs(expression_value)

        # Malrule: |ax + b| → |ax| + b → a|x| + b (distribute absolute value)
        malrule_answer = a * abs(x) + b

        if b >= 0:
            text = f"Evaluate |{a}x + {b}| when x = {x}"
            expression = f"{a}x + {b}"
        else:
            text = f"Evaluate |{a}x - {-b}| when x = {x}"
            expression = f"{a}x - {-b}"

        return Problem(
            text=text,
            operands=[x, a, b],
            operation='absolute_value',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'x_value': x,
                'coefficient': a,
                'constant': b,
                'operation': '+' if b >= 0 else '-',
                'expression': expression,
                'expression_value': expression_value,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'template': 'multiplication_inside'
            }
        )

    def _generate_word_problem(self, seed=None) -> Problem:
        """Generate real-world word problems covering all formula types."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()

        # Select which formula type to embed in the word problem
        formula_types = ['x_plus_c', 'x_minus_c', 'ax_plus_b']
        formula_type = random.choice(formula_types)

        if formula_type == 'x_plus_c':
            return self._generate_word_problem_x_plus_c(seed, ranges)
        elif formula_type == 'x_minus_c':
            return self._generate_word_problem_x_minus_c(seed, ranges)
        else:  # ax_plus_b
            return self._generate_word_problem_ax_plus_b(seed, ranges)

    def _generate_word_problem_x_plus_c(self, seed, ranges) -> Problem:
        """Generate word problems for |x + c| formula type."""
        if seed is not None:
            random.seed(seed)

        contexts = [
            {
                'text': 'The temperature is x degrees, and it increases by {c} degrees. The absolute difference from zero is |x + {c}|. If x = {x_val}, what is the absolute temperature?',
                'answer_format': '{answer} degrees',
                'type': 'temperature'
            },
            {
                'text': 'A drone is at position x meters, and moves {c} meters to the right. The distance from the origin is |x + {c}|. If x = {x_val}, what is the distance from the origin?',
                'answer_format': '{answer} meters',
                'type': 'distance'
            },
            {
                'text': 'Your account balance is x dollars. After depositing {c} dollars, the absolute balance is |x + {c}|. If x = {x_val}, what is the absolute balance?',
                'answer_format': '${answer}',
                'type': 'money'
            }
        ]

        context = random.choice(contexts)
        x = random.randint(ranges['x_value'][0], ranges['x_value'][1])
        while x == 0:
            x = random.randint(ranges['x_value'][0], ranges['x_value'][1])

        c = random.randint(ranges['constant'][0], ranges['constant'][1])

        expression_value = x + c
        correct_answer = abs(expression_value)
        malrule_answer = abs(x) + c

        problem_text = context['text'].format(c=c, x_val=x)
        correct_answer_text = context['answer_format'].format(answer=correct_answer)
        malrule_answer_text = context['answer_format'].format(answer=malrule_answer)

        return Problem(
            text=problem_text,
            operands=[x, c],
            operation='absolute_value',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'x_value': x,
                'constant': c,
                'operation': '+',
                'expression': f"x + {c}",
                'expression_value': expression_value,
                'correct_answer': correct_answer_text,
                'malrule_answer': malrule_answer_text,
                'context_type': context['type'],
                'template': 'word_problem',
                'word_problem_type': 'x_plus_c'
            }
        )

    def _generate_word_problem_x_minus_c(self, seed, ranges) -> Problem:
        """Generate word problems for |x - c| formula type."""
        if seed is not None:
            random.seed(seed)

        contexts = [
            {
                'text': 'The temperature is x degrees, and it decreases by {c} degrees. The absolute difference from zero is |x - {c}|. If x = {x_val}, what is the absolute temperature?',
                'answer_format': '{answer} degrees',
                'type': 'temperature'
            },
            {
                'text': 'A drone is at position x meters, and moves {c} meters to the left. The distance from the origin is |x - {c}|. If x = {x_val}, what is the distance from the origin?',
                'answer_format': '{answer} meters',
                'type': 'distance'
            },
            {
                'text': 'Your account balance is x dollars. After withdrawing {c} dollars, the absolute balance is |x - {c}|. If x = {x_val}, what is the absolute balance?',
                'answer_format': '${answer}',
                'type': 'money'
            }
        ]

        context = random.choice(contexts)
        x = random.randint(ranges['x_value'][0], ranges['x_value'][1])
        while x == 0:
            x = random.randint(ranges['x_value'][0], ranges['x_value'][1])

        c = random.randint(ranges['constant'][0], ranges['constant'][1])

        expression_value = x - c
        correct_answer = abs(expression_value)
        malrule_answer = abs(x) - c

        problem_text = context['text'].format(c=c, x_val=x)
        correct_answer_text = context['answer_format'].format(answer=correct_answer)
        malrule_answer_text = context['answer_format'].format(answer=malrule_answer)

        return Problem(
            text=problem_text,
            operands=[x, c],
            operation='absolute_value',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'x_value': x,
                'constant': c,
                'operation': '-',
                'expression': f"x - {c}",
                'expression_value': expression_value,
                'correct_answer': correct_answer_text,
                'malrule_answer': malrule_answer_text,
                'context_type': context['type'],
                'template': 'word_problem',
                'word_problem_type': 'x_minus_c'
            }
        )

    def _generate_word_problem_ax_plus_b(self, seed, ranges) -> Problem:
        """Generate word problems for |ax + b| formula type."""
        if seed is not None:
            random.seed(seed)

        contexts = [
            {
                'text': 'A factory produces x items per hour for {a} hours, plus {b_abs} bonus items. The total production is |{a}x + {b}|. If x = {x_val}, what is the absolute total production?',
                'answer_format': '{answer} items',
                'type': 'production',
                'b_sign': '+'
            },
            {
                'text': 'A car travels at x km/h for {a} hours. After accounting for {b_abs} km {direction}, the absolute distance from start is |{a}x {op} {b_abs}|. If x = {x_val}, what is the absolute distance?',
                'answer_format': '{answer} km',
                'type': 'distance',
                'b_sign': 'both'
            },
            {
                'text': 'An investment grows by a factor of {a} times the initial amount x, then {b_desc} ${b_abs}. The absolute value is |{a}x {op} {b_abs}|. If x = {x_val}, what is the absolute value?',
                'answer_format': '${answer}',
                'type': 'money',
                'b_sign': 'both'
            }
        ]

        context = random.choice(contexts)
        x = random.randint(ranges['x_value'][0], ranges['x_value'][1])
        while x == 0:
            x = random.randint(ranges['x_value'][0], ranges['x_value'][1])

        a = random.randint(ranges['coefficient'][0], ranges['coefficient'][1])
        b = random.randint(ranges['constant'][0], ranges['constant'][1])

        # Randomly make b negative if context supports it
        if context['b_sign'] == 'both' and random.random() < 0.5:
            b = -b

        expression_value = a * x + b
        correct_answer = abs(expression_value)
        malrule_answer = a * abs(x) + b

        # Format the problem text
        b_abs = abs(b)
        op_symbol = '+' if b >= 0 else '-'
        direction = 'backward' if b < 0 else 'forward'
        b_desc = 'gains' if b >= 0 else 'loses'

        problem_text = context['text'].format(
            a=a, b=b, b_abs=b_abs, x_val=x,
            op=op_symbol, direction=direction, b_desc=b_desc
        )
        correct_answer_text = context['answer_format'].format(answer=correct_answer)
        malrule_answer_text = context['answer_format'].format(answer=malrule_answer)

        return Problem(
            text=problem_text,
            operands=[x, a, b],
            operation='absolute_value',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'x_value': x,
                'coefficient': a,
                'constant': b,
                'operation': '+' if b >= 0 else '-',
                'expression': f"{a}x + {b}" if b >= 0 else f"{a}x - {abs(b)}",
                'expression_value': expression_value,
                'correct_answer': correct_answer_text,
                'malrule_answer': malrule_answer_text,
                'context_type': context['type'],
                'template': 'word_problem',
                'word_problem_type': 'ax_plus_b'
            }
        )
