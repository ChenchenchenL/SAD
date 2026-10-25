"""
Problem generator for PEMDAS-Strictly-Sequential malrule.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional, List
from utils import ProblemGenerator, Problem, DifficultyLevel


class PEMDASStrictlySequentialProblemGenerator(ProblemGenerator):
    """
    Generates order of operations problems to test PEMDAS understanding.

    Templates:
    1. basic_mult_div - Basic ÷ × pattern (a ÷ b × c)
    2. basic_add_sub - Basic - + pattern (a - b + c)
    3. longer_expressions - 4-5 operations with M/D or A/S chains
    4. mixed_operations - Mixing different precedence levels
    5. word_problem - Real-world contexts
    """

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_mult_div',
            'basic_add_sub',
            'longer_expressions',
            'mixed_operations',
            'word_problem'
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        ranges = {
            6: {DifficultyLevel.EASY: (1, 10), DifficultyLevel.MEDIUM: (1, 20), DifficultyLevel.HARD: (1, 50)},
            7: {DifficultyLevel.EASY: (1, 20), DifficultyLevel.MEDIUM: (1, 50), DifficultyLevel.HARD: (1, 100)},
            8: {DifficultyLevel.EASY: (1, 50), DifficultyLevel.MEDIUM: (1, 100), DifficultyLevel.HARD: (1, 200)},
        }
        lvl = self.level if self.level in ranges else 7
        return {'values': ranges[lvl][self.difficulty]}

    def generate(self, seed=None, template: Optional[str] = None) -> Problem:
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            template = random.choice(self.get_available_templates())

        # Generate based on template
        if template == 'basic_mult_div':
            return self._generate_basic_mult_div(seed)
        elif template == 'basic_add_sub':
            return self._generate_basic_add_sub(seed)
        elif template == 'longer_expressions':
            return self._generate_longer_expressions(seed)
        elif template == 'mixed_operations':
            return self._generate_mixed_operations(seed)
        elif template == 'word_problem':
            return self._generate_word_problem(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_mult_div(self, seed=None) -> Problem:
        """
        Generate basic mult/div problem (original template).

        Example: 12 ÷ 2 × 3
        Correct (L-R): (12 ÷ 2) × 3 = 6 × 3 = 18
        Malrule (M before D): 12 ÷ (2 × 3) = 12 ÷ 6 = 2
        """
        if seed is not None:
            random.seed(seed)

        b = random.randint(2, 10)
        c = random.randint(2, 10)
        # Choose a that's divisible by b
        a = b * random.randint(2, 10)

        correct_answer = (a / b) * c  # Left to right
        malrule_answer = a / (b * c)  # M before D

        expression = f"{a} ÷ {b} × {c}"
        operator_sequence = "÷×"
        operands = [a, b, c]

        problem_text = f"Calculate: {expression}"

        return Problem(
            text=problem_text,
            operands=operands,
            operation='order_of_operations',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'expression': expression,
                'correct_answer': int(correct_answer) if correct_answer == int(correct_answer) else round(correct_answer, 2),
                'malrule_answer': int(malrule_answer) if malrule_answer == int(malrule_answer) else round(malrule_answer, 2),
                'problem_type': 'mult_div',
                'operator_sequence': operator_sequence,
                'template': 'basic_mult_div'
            }
        )

    def _generate_basic_add_sub(self, seed=None) -> Problem:
        """
        Generate basic add/sub problem (original template).

        Example: 10 - 3 + 2
        Correct (L-R): (10 - 3) + 2 = 7 + 2 = 9
        Malrule (A before S): 10 - (3 + 2) = 10 - 5 = 5
        """
        if seed is not None:
            random.seed(seed)

        value_range = self.get_value_ranges()['values']
        min_val, max_val = value_range

        a = random.randint(min_val, max_val)
        b = random.randint(1, a)  # Ensure a >= b for positive intermediate
        c = random.randint(1, 20)

        correct_answer = (a - b) + c  # Left to right
        malrule_answer = a - (b + c)  # A before S

        expression = f"{a} - {b} + {c}"
        operator_sequence = "-+"
        operands = [a, b, c]

        problem_text = f"Calculate: {expression}"

        return Problem(
            text=problem_text,
            operands=operands,
            operation='order_of_operations',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'expression': expression,
                'correct_answer': int(correct_answer) if correct_answer == int(correct_answer) else round(correct_answer, 2),
                'malrule_answer': int(malrule_answer) if malrule_answer == int(malrule_answer) else round(malrule_answer, 2),
                'problem_type': 'add_sub',
                'operator_sequence': operator_sequence,
                'template': 'basic_add_sub'
            }
        )

    def _generate_longer_expressions(self, seed=None) -> Problem:
        """
        Generate longer expressions with 4-5 operations.

        Example: 24 ÷ 2 × 3 ÷ 4
        Correct (L-R): ((24 ÷ 2) × 3) ÷ 4 = (12 × 3) ÷ 4 = 36 ÷ 4 = 9
        Malrule (All M, then all D): (24 × 3) ÷ (2 × 4) = 72 ÷ 8 = 9 (happens to be same!)
        Better: 24 ÷ 2 × 3 × 2
        """
        if seed is not None:
            random.seed(seed)

        problem_type = random.choice(['mult_div', 'add_sub'])

        if problem_type == 'mult_div':
            # Generate: a ÷ b × c ÷ d
            b = random.randint(2, 5)
            c = random.randint(2, 5)
            d = random.randint(2, 5)
            a = b * c * d * random.randint(1, 3)  # Make it divisible

            # Correct: left-to-right
            temp1 = a / b
            temp2 = temp1 * c
            correct_answer = temp2 / d

            # Malrule: all mult first, then all div
            mult_result = c  # Only one multiplication
            div_result = a / (b * mult_result * d)  # Simplification: a / (b * c * d)
            malrule_answer = div_result

            expression = f"{a} ÷ {b} × {c} ÷ {d}"
            operator_sequence = "÷×÷"
            operands = [a, b, c, d]

        else:  # add_sub
            # Generate: a - b + c - d
            a = random.randint(20, 100)
            b = random.randint(1, 10)
            c = random.randint(1, 10)
            d = random.randint(1, 10)

            # Correct: left-to-right
            temp1 = a - b
            temp2 = temp1 + c
            correct_answer = temp2 - d

            # Malrule: all add first, then all sub
            add_result = c  # Only one addition
            sub_result = a - b - add_result - d  # Simplification: a - (b + c + d)
            malrule_answer = sub_result

            expression = f"{a} - {b} + {c} - {d}"
            operator_sequence = "-+-"
            operands = [a, b, c, d]

        problem_text = f"Calculate: {expression}"

        return Problem(
            text=problem_text,
            operands=operands,
            operation='order_of_operations',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'expression': expression,
                'correct_answer': int(correct_answer) if correct_answer == int(correct_answer) else round(correct_answer, 2),
                'malrule_answer': int(malrule_answer) if malrule_answer == int(malrule_answer) else round(malrule_answer, 2),
                'problem_type': problem_type,
                'operator_sequence': operator_sequence,
                'template': 'longer_expressions'
            }
        )

    def _generate_mixed_operations(self, seed=None) -> Problem:
        """
        Generate mixed operations across precedence levels.

        Example: 2 + 6 ÷ 2 × 3
        Correct: 2 + ((6 ÷ 2) × 3) = 2 + (3 × 3) = 2 + 9 = 11
        Malrule: Does all × first, then ÷, then +: 2 + (6 ÷ (2 × 3)) = 2 + 1 = 3
        """
        if seed is not None:
            random.seed(seed)

        # Mix addition/subtraction with multiplication/division
        # Pattern: a +/- b ÷ c × d
        a = random.randint(2, 20)
        c = random.randint(2, 5)
        d = random.randint(2, 5)
        b = c * d * random.randint(1, 3)  # Make b divisible by c

        op1 = random.choice(['+', '-'])

        # Correct: M/D left-to-right first (higher precedence), then A/S
        md_result = (b / c) * d  # Do division and multiplication left-to-right
        if op1 == '+':
            correct_answer = a + md_result
        else:
            correct_answer = a - md_result

        # Malrule: All M, then all D, then all A, then all S
        # Step 1: Do all multiplication: c × d
        mult_result = c * d
        # Step 2: Do all division: b ÷ mult_result
        div_result = b / mult_result
        # Step 3: Do addition/subtraction
        if op1 == '+':
            malrule_answer = a + div_result
        else:
            malrule_answer = a - div_result

        expression = f"{a} {op1} {b} ÷ {c} × {d}"
        operator_sequence = f"{op1}÷×"
        operands = [a, b, c, d]

        problem_text = f"Calculate: {expression}"

        return Problem(
            text=problem_text,
            operands=operands,
            operation='order_of_operations',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'expression': expression,
                'correct_answer': int(correct_answer) if correct_answer == int(correct_answer) else round(correct_answer, 2),
                'malrule_answer': int(malrule_answer) if malrule_answer == int(malrule_answer) else round(malrule_answer, 2),
                'problem_type': 'mixed',
                'operator_sequence': operator_sequence,
                'template': 'mixed_operations'
            }
        )

    def _generate_word_problem(self, seed=None) -> Problem:
        """
        Generate word problem with order of operations.

        Real-world contexts where order matters
        """
        if seed is not None:
            random.seed(seed)

        contexts = [
            {
                'type': 'shopping',
                'setup': 'You have ${a}. You spend ${b} and then earn ${c}. How much money do you have?',
                'problem_type': 'add_sub',
                'expression_template': '{a} - {b} + {c}'
            },
            {
                'type': 'sharing',
                'setup': 'There are {a} candies. You divide them among {b} friends and then multiply by {c} groups. How many candies per person?',
                'problem_type': 'mult_div',
                'expression_template': '{a} ÷ {b} × {c}'
            },
            {
                'type': 'cooking',
                'setup': 'A recipe needs {a} cups of flour. You divide it by {b} and then multiply by {c} batches. How many cups per batch?',
                'problem_type': 'mult_div',
                'expression_template': '{a} ÷ {b} × {c}'
            },
            {
                'type': 'temperature',
                'setup': 'The temperature was {a}°F. It dropped {b} degrees and then rose {c} degrees. What is the temperature now?',
                'problem_type': 'add_sub',
                'expression_template': '{a} - {b} + {c}'
            }
        ]

        context = random.choice(contexts)
        problem_type = context['problem_type']

        if problem_type == 'mult_div':
            b = random.randint(2, 10)
            c = random.randint(2, 10)
            a = b * random.randint(2, 10)

            correct_answer = (a / b) * c
            malrule_answer = a / (b * c)
            operands = [a, b, c]
            operator_sequence = "÷×"

        else:  # add_sub
            a = random.randint(20, 100)
            b = random.randint(1, min(a, 20))
            c = random.randint(1, 20)

            correct_answer = (a - b) + c
            malrule_answer = a - (b + c)
            operands = [a, b, c]
            operator_sequence = "-+"

        expression = context['expression_template'].format(a=a, b=b, c=c)
        problem_text = context['setup'].format(a=a, b=b, c=c)

        return Problem(
            text=problem_text,
            operands=operands,
            operation='order_of_operations',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'expression': expression,
                'correct_answer': int(correct_answer) if correct_answer == int(correct_answer) else round(correct_answer, 2),
                'malrule_answer': int(malrule_answer) if malrule_answer == int(malrule_answer) else round(malrule_answer, 2),
                'problem_type': problem_type,
                'operator_sequence': operator_sequence,
                'template': 'word_problem',
                'context_type': context['type']
            }
        )
