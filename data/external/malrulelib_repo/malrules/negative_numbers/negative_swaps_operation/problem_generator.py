"""
Problem generator for Negative-Swaps-Operation malrule.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, List, Optional
from utils import ProblemGenerator, Problem, DifficultyLevel


class NegativeSwapsOperationProblemGenerator(ProblemGenerator):
    """Generates negative number arithmetic problems."""

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_arithmetic',
            'word_problem_context',
            'multi_step_expression',
            'algebraic_context',
            'comparison_problem'
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        ranges = {
            7: {DifficultyLevel.EASY: (1, 10), DifficultyLevel.MEDIUM: (1, 20), DifficultyLevel.HARD: (1, 50)},
            8: {DifficultyLevel.EASY: (1, 20), DifficultyLevel.MEDIUM: (1, 50), DifficultyLevel.HARD: (1, 100)},
            9: {DifficultyLevel.EASY: (1, 50), DifficultyLevel.MEDIUM: (1, 100), DifficultyLevel.HARD: (1, 200)},
        }
        lvl = self.level if self.level in ranges else 8
        return {'values': ranges[lvl][self.difficulty]}

    def generate(self, seed=None, template: Optional[str] = None) -> Problem:
        """
        Generate a negative number arithmetic problem.

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
        if template == 'basic_arithmetic':
            return self._generate_basic_arithmetic(seed)
        elif template == 'word_problem_context':
            return self._generate_word_problem_context(seed)
        elif template == 'multi_step_expression':
            return self._generate_multi_step_expression(seed)
        elif template == 'algebraic_context':
            return self._generate_algebraic_context(seed)
        elif template == 'comparison_problem':
            return self._generate_comparison_problem(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_arithmetic(self, seed=None) -> Problem:
        """Template 1: Basic arithmetic with negatives."""
        if seed is not None:
            random.seed(seed)

        value_range = self.get_value_ranges()['values']
        min_val, max_val = value_range

        operation = random.choice(['add_negative', 'subtract_negative'])

        if operation == 'add_negative':
            # a + (-b)
            # Correct: a + (-b) = a - b
            # Malrule: negative swaps +, so becomes a + b (WRONG!)
            a = random.randint(min_val, max_val)
            b = random.randint(1, min_val)

            correct_answer = a + (-b)  # = a - b
            malrule_answer = a + b  # Thinks - swaps to +

            text = f"Calculate: {a} + (-{b})"
            operator = "+"
            num2 = -b

        else:  # subtract_negative
            # a - (-b)
            # Correct: a - (-b) = a + b
            # Malrule: negative swaps -, so becomes a - b (WRONG!)
            a = random.randint(min_val, max_val)
            b = random.randint(1, min_val)

            correct_answer = a - (-b)  # = a + b
            malrule_answer = a - b  # Thinks - swaps to -, so stays -

            text = f"Calculate: {a} - (-{b})"
            operator = "-"
            num2 = -b

        return Problem(
            text=text,
            operands=[a, num2],
            operation='arithmetic',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': a,
                'num2': num2,
                'operator': operator,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'operation_type': operation,
                'template': 'basic_arithmetic'
            }
        )

    def _generate_word_problem_context(self, seed=None) -> Problem:
        """Template 2: Word problem with real-world context."""
        problem = self._generate_basic_arithmetic(seed)

        contexts = {
            'add_negative': [
                ("Temperature starts at {a}°C", "drops by {b}°C ({a} + (-{b}))", "final temperature in °C"),
                ("Account has ${a}", "withdraw ${b} ({a} + (-{b}))", "balance"),
                ("Elevation at {a}m", "descend {b}m ({a} + (-{b}))", "elevation in meters"),
            ],
            'subtract_negative': [
                ("Temperature is {a}°C", "remove a decrease of {b}°C ({a} - (-{b}))", "temperature in °C"),
                ("Debt of ${a}", "cancel a debt of ${b} ({a} - (-{b}))", "new balance"),
                ("At {a}m elevation", "undo a descent of {b}m ({a} - (-{b}))", "elevation in meters"),
            ]
        }

        op_type = problem.metadata['operation_type']
        a = problem.metadata['num1']
        b = abs(problem.metadata['num2'])

        start_phrase, action_phrase, result = random.choice(contexts[op_type])
        problem.text = f"{start_phrase.format(a=a)} and {action_phrase.format(a=a, b=b)}. What is the {result}?"
        problem.metadata['template'] = 'word_problem_context'
        return problem

    def _generate_multi_step_expression(self, seed=None) -> Problem:
        """Template 3: Multi-step expression with negatives."""
        if seed is not None:
            random.seed(seed)

        value_range = self.get_value_ranges()['values']
        min_val, max_val = value_range

        # Generate: a + (-b) - (-c) or similar
        a = random.randint(min_val, max_val)
        b = random.randint(1, min_val)
        c = random.randint(1, min_val)

        # Choose which operation has the error
        error_position = random.choice(['first', 'second'])

        if error_position == 'first':
            # Error in first operation: a + (-b) - (-c)
            # Correct: (a - b) + c
            # Malrule: (a + b) + c
            correct_answer = a - b + c
            malrule_answer = a + b + c
            text = f"Calculate: {a} + (-{b}) - (-{c})"
            operation_type = 'add_negative'
        else:
            # Error in second operation: a - (-b) + (-c)
            # Correct: (a + b) - c
            # Malrule: (a - b) - c
            correct_answer = a + b - c
            malrule_answer = a - b - c
            text = f"Calculate: {a} - (-{b}) + (-{c})"
            operation_type = 'subtract_negative'

        return Problem(
            text=text,
            operands=[a, -b, -c],
            operation='arithmetic',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': a,
                'num2': -b,
                'num3': -c,
                'operator': '+' if operation_type == 'add_negative' else '-',
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'operation_type': operation_type,
                'template': 'multi_step_expression'
            }
        )

    def _generate_algebraic_context(self, seed=None) -> Problem:
        """Template 4: Algebraic expression with negatives."""
        if seed is not None:
            random.seed(seed)

        value_range = self.get_value_ranges()['values']
        min_val, max_val = value_range

        # Generate: x + (-a) where x is given, or x - (-a) where x is given
        x_val = random.randint(min_val, max_val)
        a = random.randint(1, min_val)

        operation = random.choice(['add_negative', 'subtract_negative'])

        if operation == 'add_negative':
            correct_answer = x_val - a
            malrule_answer = x_val + a
            text = f"If x = {x_val}, calculate: x + (-{a})"
            operator = "+"
        else:
            correct_answer = x_val + a
            malrule_answer = x_val - a
            text = f"If x = {x_val}, calculate: x - (-{a})"
            operator = "-"

        return Problem(
            text=text,
            operands=[x_val, -a],
            operation='arithmetic',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': x_val,
                'num2': -a,
                'operator': operator,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'operation_type': operation,
                'template': 'algebraic_context'
            }
        )

    def _generate_comparison_problem(self, seed=None) -> Problem:
        """Template 5: Compare two expressions with negatives."""
        value_range = self.get_value_ranges()['values']
        min_val, max_val = value_range

        # Retry until we get different correct and malrule answers
        attempts = 0
        while attempts < 100:
            if seed is not None:
                random.seed(seed + attempts)

            # Generate two expressions and compare
            a1 = random.randint(min_val, max_val)
            b1 = random.randint(1, min_val)

            a2 = random.randint(min_val, max_val)
            b2 = random.randint(1, min_val)

            # First expression: a1 + (-b1)
            correct1 = a1 - b1
            malrule1 = a1 + b1

            # Second expression: a2 - (-b2)
            correct2 = a2 + b2

            # Determine comparison
            if correct1 > correct2:
                correct_answer = f"{a1} + (-{b1}) is greater"
            elif correct1 < correct2:
                correct_answer = f"{a2} - (-{b2}) is greater"
            else:
                correct_answer = "They are equal"

            if malrule1 > correct2:
                malrule_answer = f"{a1} + (-{b1}) is greater"
            elif malrule1 < correct2:
                malrule_answer = f"{a2} - (-{b2}) is greater"
            else:
                malrule_answer = "They are equal"

            # Ensure the answers differ
            if correct_answer != malrule_answer:
                break
            attempts += 1

        text = f"Which is greater: {a1} + (-{b1}) or {a2} - (-{b2})?"

        return Problem(
            text=text,
            operands=[a1, -b1, a2, -b2],
            operation='arithmetic',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': a1,
                'num2': -b1,
                'operator': '+',
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'operation_type': 'add_negative',
                'template': 'comparison_problem'
            }
        )
