"""
Problem generator for Ignore-Parentheses malrule.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional, List
from utils import ProblemGenerator, Problem, DifficultyLevel


class IgnoreParenthesesProblemGenerator(ProblemGenerator):
    """
    Generates order of operations problems with parentheses.

    Templates:
    1. basic_single_parentheses - Single grouping: a op1 (b op2 c)
    2. nested_parentheses - Nested grouping: a op1 (b op2 (c op3 d))
    3. multiple_parentheses - Multiple groups: (a op1 b) op2 (c op3 d)
    4. brackets_and_parentheses - Different symbols: a × [b + (c - d)]
    5. word_problem - Real-world contexts
    """

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_single_parentheses',
            'nested_parentheses',
            'multiple_parentheses',
            'brackets_and_parentheses',
            'word_problem'
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        ranges = {
            5: {
                DifficultyLevel.EASY: (1, 10),
                DifficultyLevel.MEDIUM: (1, 20),
                DifficultyLevel.HARD: (1, 50),
            },
            6: {
                DifficultyLevel.EASY: (1, 20),
                DifficultyLevel.MEDIUM: (1, 50),
                DifficultyLevel.HARD: (1, 100),
            },
            7: {
                DifficultyLevel.EASY: (1, 50),
                DifficultyLevel.MEDIUM: (1, 100),
                DifficultyLevel.HARD: (1, 500),
            },
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
        if template == 'basic_single_parentheses':
            return self._generate_basic_single_parentheses(seed)
        elif template == 'nested_parentheses':
            return self._generate_nested_parentheses(seed)
        elif template == 'multiple_parentheses':
            return self._generate_multiple_parentheses(seed)
        elif template == 'brackets_and_parentheses':
            return self._generate_brackets_and_parentheses(seed)
        elif template == 'word_problem':
            return self._generate_word_problem(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_single_parentheses(self, seed=None) -> Problem:
        """
        Generate basic single parentheses problem (original template).

        Example: 3 + (4 × 5), 12 ÷ (8 - 2)

        Pattern: a op1 (b op2 c)
        """
        if seed is not None:
            random.seed(seed)

        value_range = self.get_value_ranges()['values']
        min_val, max_val = value_range

        # Try up to 100 times to generate a valid problem
        for attempt in range(100):
            # Generate expression with parentheses
            # Format: a op1 (b op2 c)
            a = random.randint(min_val, max_val)
            b = random.randint(min_val, max_val)
            c = random.randint(1, max_val)  # Avoid division by zero

            op1 = random.choice(['+', '-', '×', '÷'])
            op2 = random.choice(['+', '-', '×', '÷'])

            # Build expression
            expression = f"{a} {op1} ({b} {op2} {c})"

            # Calculate correct answer (respecting parentheses)
            paren_result = self._evaluate_operation(b, c, op2)
            correct_answer = self._evaluate_operation(a, paren_result, op1)

            # Calculate malrule answer (ignoring parentheses, left-to-right)
            left_to_right_first = self._evaluate_operation(a, b, op1)
            malrule_answer = self._evaluate_operation(left_to_right_first, c, op2)

            # CRITICAL: Ensure malrule produces DIFFERENT answer than correct
            if abs(correct_answer - malrule_answer) > 0.01:  # Account for floating point
                break

        problem_text = f"Calculate: {expression}"

        return Problem(
            text=problem_text,
            operands=[a, b, c],
            operation='order_of_operations',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'expression': expression,
                'a': a,
                'b': b,
                'c': c,
                'op1': op1,
                'op2': op2,
                'correct_answer': correct_answer,
                'paren_result': paren_result,
                'template': 'basic_single_parentheses'
            }
        )

    def _generate_nested_parentheses(self, seed=None) -> Problem:
        """
        Generate nested parentheses problem.

        Example: 2 × (3 + (4 - 1)), 10 - (8 ÷ (6 - 2))

        Pattern: a op1 (b op2 (c op3 d))
        """
        if seed is not None:
            random.seed(seed)

        value_range = self.get_value_ranges()['values']
        min_val, max_val = value_range

        for attempt in range(100):
            a = random.randint(min_val, max_val)
            b = random.randint(min_val, max_val)
            c = random.randint(min_val, max_val)
            d = random.randint(1, max_val)

            op1 = random.choice(['+', '-', '×', '÷'])
            op2 = random.choice(['+', '-', '×', '÷'])
            op3 = random.choice(['+', '-', '×', '÷'])

            expression = f"{a} {op1} ({b} {op2} ({c} {op3} {d}))"

            # Correct: innermost first
            inner_result = self._evaluate_operation(c, d, op3)
            middle_result = self._evaluate_operation(b, inner_result, op2)
            correct_answer = self._evaluate_operation(a, middle_result, op1)

            # Malrule: left-to-right ignoring all parentheses
            step1 = self._evaluate_operation(a, b, op1)
            step2 = self._evaluate_operation(step1, c, op2)
            malrule_answer = self._evaluate_operation(step2, d, op3)

            if abs(correct_answer - malrule_answer) > 0.01:
                break

        return Problem(
            text=f"Calculate: {expression}",
            operands=[a, b, c, d],
            operation='order_of_operations',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'expression': expression,
                'values': [a, b, c, d],
                'operations': [op1, op2, op3],
                'correct_answer': correct_answer,
                'template': 'nested_parentheses'
            }
        )

    def _generate_multiple_parentheses(self, seed=None) -> Problem:
        """
        Generate multiple parentheses problem.

        Example: (2 + 3) × (4 - 1), (8 ÷ 2) + (6 × 3)

        Pattern: (a op1 b) op2 (c op3 d)
        """
        if seed is not None:
            random.seed(seed)

        value_range = self.get_value_ranges()['values']
        min_val, max_val = value_range

        for attempt in range(100):
            a = random.randint(min_val, max_val)
            b = random.randint(1, max_val)
            c = random.randint(min_val, max_val)
            d = random.randint(1, max_val)

            op1 = random.choice(['+', '-', '×', '÷'])
            op2 = random.choice(['+', '-', '×', '÷'])
            op3 = random.choice(['+', '-', '×', '÷'])

            expression = f"({a} {op1} {b}) {op2} ({c} {op3} {d})"

            # Correct: both parentheses first
            left_paren = self._evaluate_operation(a, b, op1)
            right_paren = self._evaluate_operation(c, d, op3)
            correct_answer = self._evaluate_operation(left_paren, right_paren, op2)

            # Malrule: left-to-right ignoring parentheses
            step1 = self._evaluate_operation(a, b, op1)
            step2 = self._evaluate_operation(step1, c, op2)
            malrule_answer = self._evaluate_operation(step2, d, op3)

            if abs(correct_answer - malrule_answer) > 0.01:
                break

        return Problem(
            text=f"Calculate: {expression}",
            operands=[a, b, c, d],
            operation='order_of_operations',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'expression': expression,
                'values': [a, b, c, d],
                'operations': [op1, op2, op3],
                'correct_answer': correct_answer,
                'template': 'multiple_parentheses'
            }
        )

    def _generate_brackets_and_parentheses(self, seed=None) -> Problem:
        """
        Generate problem with brackets and parentheses.

        Example: 2 × [3 + (4 - 1)], 10 - [8 ÷ (6 + 2)]

        Pattern: a op1 [b op2 (c op3 d)]
        Note: Brackets and parentheses are equivalent, but using different symbols
        """
        if seed is not None:
            random.seed(seed)

        value_range = self.get_value_ranges()['values']
        min_val, max_val = value_range

        for attempt in range(100):
            a = random.randint(min_val, max_val)
            b = random.randint(min_val, max_val)
            c = random.randint(min_val, max_val)
            d = random.randint(1, max_val)

            op1 = random.choice(['+', '-', '×', '÷'])
            op2 = random.choice(['+', '-', '×', '÷'])
            op3 = random.choice(['+', '-', '×', '÷'])

            expression = f"{a} {op1} [{b} {op2} ({c} {op3} {d})]"

            # Correct: innermost first (parentheses), then brackets
            inner_result = self._evaluate_operation(c, d, op3)
            bracket_result = self._evaluate_operation(b, inner_result, op2)
            correct_answer = self._evaluate_operation(a, bracket_result, op1)

            # Malrule: left-to-right ignoring all grouping symbols
            step1 = self._evaluate_operation(a, b, op1)
            step2 = self._evaluate_operation(step1, c, op2)
            malrule_answer = self._evaluate_operation(step2, d, op3)

            if abs(correct_answer - malrule_answer) > 0.01:
                break

        return Problem(
            text=f"Calculate: {expression}",
            operands=[a, b, c, d],
            operation='order_of_operations',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'expression': expression,
                'values': [a, b, c, d],
                'operations': [op1, op2, op3],
                'correct_answer': correct_answer,
                'template': 'brackets_and_parentheses'
            }
        )

    def _generate_word_problem(self, seed=None) -> Problem:
        """
        Generate word problem with parentheses.

        Example: "If you buy 3 items at (4 + 2) dollars each, how much do you spend?"

        Real-world contexts where order matters
        """
        if seed is not None:
            random.seed(seed)

        value_range = self.get_value_ranges()['values']
        min_val, max_val = value_range

        contexts = [
            {
                'type': 'shopping',
                'setup': 'If you buy {a} items at ({b} + {c}) dollars each, how much do you spend in total?',
                'op1': '×',
                'op2': '+'
            },
            {
                'type': 'sharing',
                'setup': 'There are {a} groups with ({b} - {c}) people each. How many people total?',
                'op1': '×',
                'op2': '-'
            },
            {
                'type': 'temperature',
                'setup': 'The temperature was {a} degrees. It dropped by ({b} × {c}) degrees. What is the new temperature?',
                'op1': '-',
                'op2': '×'
            },
            {
                'type': 'money',
                'setup': 'You have ${a}. You spend ({b} ÷ {c}) dollars on each of 2 items. How much money remains? (Round to nearest dollar)',
                'op1': '-',
                'op2': '÷'
            }
        ]

        context = random.choice(contexts)

        for attempt in range(100):
            a = random.randint(max(2, min_val), max_val)
            b = random.randint(max(2, min_val), max_val)
            c = random.randint(1, min(10, max_val))

            op1 = context['op1']
            op2 = context['op2']

            # Adjust based on operation to ensure sensible values
            if op2 == '÷':
                c = random.choice([2, 3, 4, 5])  # Nice divisors
                b = c * random.randint(2, 8)  # Ensure b divisible by c

            if op2 == '-':
                c = random.randint(1, b - 1)  # Ensure b > c for positive result

            # All contexts use pattern: a op1 (b op2 c)
            expression = f"{a} {op1} ({b} {op2} {c})"
            paren_result = self._evaluate_operation(b, c, op2)
            correct_answer = self._evaluate_operation(a, paren_result, op1)

            # Malrule: left-to-right ignoring parentheses
            step1 = self._evaluate_operation(a, b, op1)
            malrule_answer = self._evaluate_operation(step1, c, op2)

            if abs(correct_answer - malrule_answer) > 0.01:
                break

        problem_text = context['setup'].format(a=a, b=b, c=c)

        # Store operations in the order they appear in the expression
        return Problem(
            text=problem_text,
            operands=[a, b, c],
            operation='order_of_operations',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'expression': expression,
                'values': [a, b, c],
                'operations': [op1, op2],
                'correct_answer': correct_answer,
                'template': 'word_problem',
                'context_type': context['type']
            }
        )

    def _evaluate_operation(self, x, y, op):
        if op == '+':
            return x + y
        elif op == '-':
            return x - y
        elif op == '×':
            return x * y
        elif op == '÷':
            return x / y if y != 0 else 0
        return 0
