"""
Problem generator for Addition-Before-Subtraction-Always malrule.

Generates order of operations problems with addition and subtraction
that appear left-to-right.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional
from utils import ProblemGenerator, Problem, DifficultyLevel


class AdditionSubtractionOrderProblemGenerator(ProblemGenerator):
    """
    Generates order of operations problems to elicit Addition-Before-Subtraction-Always.

    Creates expressions with subtraction followed by addition where
    following strict "A before S" gives wrong answer.
    """

    def get_name(self) -> str:
        return "Addition/Subtraction Order Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates expressions with addition and subtraction appearing "
            "left-to-right, where treating 'A before S' as strict rule gives "
            "wrong answer. Example: 10 - 3 + 2"
        )

    def get_available_templates(self) -> list:
        """Return list of available template names."""
        return [
            'simple_expression',
            'money_transaction',
            'temperature_change',
            'elevation_change',
            'score_tracking'
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level."""
        ranges = {
            6: {
                DifficultyLevel.EASY: (5, 15),
                DifficultyLevel.MEDIUM: (10, 25),
                DifficultyLevel.HARD: (15, 40),
            },
            7: {
                DifficultyLevel.EASY: (5, 20),
                DifficultyLevel.MEDIUM: (10, 35),
                DifficultyLevel.HARD: (20, 50),
            },
            8: {
                DifficultyLevel.EASY: (10, 25),
                DifficultyLevel.MEDIUM: (15, 40),
                DifficultyLevel.HARD: (25, 60),
            },
            9: {
                DifficultyLevel.EASY: (10, 30),
                DifficultyLevel.MEDIUM: (20, 50),
                DifficultyLevel.HARD: (30, 80),
            }
        }

        lvl = self.level if self.level in ranges else 7
        return {'value': ranges[lvl][self.difficulty]}

    def get_problem_types(self) -> list:
        """
        Return all applicable problem types (formula patterns) for this malrule.

        Each problem type represents a different formula where the malrule applies.
        Only includes types where malrule produces DIFFERENT answer than correct.

        Note: Due to associativity/commutativity of +/-, only certain patterns
        actually produce different results. We focus on the canonical sub_add pattern.
        """
        return [
            'sub_add',          # a - b + c (malrule: a - (b+c) ≠ correct) [CANONICAL]
        ]

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate an order of operations problem.

        Args:
            seed: Optional random seed for reproducibility
            template: Optional template name to use for generation

        Returns:
            Problem instance
        """
        if seed is not None:
            random.seed(seed)

        # If template is specified, use the corresponding method
        if template is not None:
            if template not in self.get_available_templates():
                raise ValueError(f"Unknown template: {template}. Available templates: {self.get_available_templates()}")

            method_name = f"_generate_{template}"
            if hasattr(self, method_name):
                return getattr(self, method_name)(seed)
            else:
                raise NotImplementedError(f"Template method {method_name} not implemented")

        min_val, max_val = self.get_value_ranges()['value']

        # Choose problem type (formula pattern)
        problem_types = self.get_problem_types()

        # For level 6, stick to simplest 3-term expressions
        if self.level == 6:
            problem_types = ['sub_add']

        problem_type = random.choice(problem_types)

        # Decide whether to generate a word problem or simple expression
        use_word_problem = (self.level >= 7 and random.random() < 0.6)

        # Generate based on problem type
        if problem_type == 'sub_add':
            # Pattern: a - b + c
            a = random.randint(min_val + 10, max_val)
            b = random.randint(min_val, min(a - 5, max_val - 10))
            c = random.randint(min_val, max_val)
            expression = f"{a} - {b} + {c}"
            correct_answer = (a - b) + c
            malrule_answer = a - (b + c)
            operands = [a, b, c]

            if use_word_problem:
                scenarios = [
                    f"You have ${a}. You spend ${b}, then earn ${c}. How much money do you have now?",
                    f"The temperature is {a}°C. It drops {b}°C, then rises {c}°C. What's the final temperature?",
                    f"Your score is {a} points. You lose {b} points, then gain {c} points. What's your final score?",
                ]
                problem_text = random.choice(scenarios)
            else:
                problem_text = f"Evaluate: {expression}"

        elif problem_type == 'sub_sub_add':
            # Pattern: a - b - c + d
            a = random.randint(min(min_val + 20, max_val), max_val)
            b = random.randint(min_val, min(max_val, max(min_val + 1, a // 5)))
            c = random.randint(min_val, min(max_val, max(min_val + 1, a // 5)))
            d = random.randint(min_val, max_val)
            expression = f"{a} - {b} - {c} + {d}"
            # Correct: left-to-right
            correct_answer = ((a - b) - c) + d
            # Malrule: Do all additions first (d), then all subtractions (b, c)
            # a + d - b - c
            malrule_answer = a + d - b - c
            operands = [a, b, c, d]

            if use_word_problem:
                scenarios = [
                    f"You have ${a}. You spend ${b}, then spend ${c}, then earn ${d}. How much money do you have now?",
                    f"Starting at {a}°C, temperature drops {b}°C, drops {c}°C, then rises {d}°C. What's the final temperature?",
                    f"Score: {a} points. Lose {b}, lose {c}, then gain {d} points. What's your final score?",
                ]
                problem_text = random.choice(scenarios)
            else:
                problem_text = f"Evaluate: {expression}"

        elif problem_type == 'sub_add_sub_add':
            # Pattern: a - b + c - d + e
            a = random.randint(min(min_val + 30, max_val), max_val)
            b = random.randint(min_val, min(max_val, max(min_val + 1, a // 6)))
            c = random.randint(min_val, min(max_val, max(min_val + 1, a // 6)))
            d = random.randint(min_val, min(max_val, max(min_val + 1, a // 6)))
            e = random.randint(min_val, max_val)
            expression = f"{a} - {b} + {c} - {d} + {e}"
            # Correct: left-to-right
            correct_answer = (((a - b) + c) - d) + e
            # Malrule: Do all additions first (c, e), then all subtractions (b, d)
            # a + c + e - b - d
            malrule_answer = a + c + e - b - d
            operands = [a, b, c, d, e]

            if use_word_problem:
                scenarios = [
                    f"You have ${a}. You spend ${b}, earn ${c}, spend ${d}, then earn ${e}. How much money do you have now?",
                    f"Starting at {a}°C, temperature drops {b}°C, rises {c}°C, drops {d}°C, then rises {e}°C. What's the final temperature?",
                    f"Score: {a} points. Lose {b}, gain {c}, lose {d}, then gain {e} points. What's your final score?",
                ]
                problem_text = random.choice(scenarios)
            else:
                problem_text = f"Evaluate: {expression}"

        else:  # Fallback
            a = random.randint(min_val + 5, max_val)
            b = random.randint(min_val, a - 1)
            c = random.randint(min_val, max_val)
            expression = f"{a} - {b} + {c}"
            correct_answer = (a - b) + c
            malrule_answer = a - (b + c)
            operands = [a, b, c]
            problem_text = f"Evaluate: {expression}"

        # Create metadata with variable operands
        metadata = {
            'expression': expression,
            'problem_type': problem_type,  # Embed problem type in metadata
            'correct_answer': str(correct_answer),
            'malrule_answer': str(malrule_answer),
        }

        # Add operands with indexed keys
        for i, op in enumerate(operands):
            metadata[f'operand_{i}'] = op

        # For backward compatibility, add a, b, c, d, e
        operand_names = ['a', 'b', 'c', 'd', 'e']
        for i, name in enumerate(operand_names):
            metadata[name] = operands[i] if i < len(operands) else None

        return Problem(
            text=problem_text,
            operands=operands,
            operation='order_of_operations',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_simple_expression(self, seed: Optional[int] = None) -> Problem:
        """
        Generate a simple mathematical expression: a - b + c

        Example: "Evaluate: 15 - 6 + 4"
        Correct: (15 - 6) + 4 = 9 + 4 = 13
        Malrule: 15 - (6 + 4) = 15 - 10 = 5
        """
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['value']

        # Generate: a - b + c where a > b to avoid negative intermediate result
        a = random.randint(min_val + 5, max_val)
        b = random.randint(min_val, a - 1)
        c = random.randint(min_val, max_val)

        expression = f"{a} - {b} + {c}"
        problem_text = f"Evaluate: {expression}"

        # Calculate correct answer (left-to-right)
        correct_answer = (a - b) + c

        # Calculate malrule answer (addition first)
        malrule_answer = a - (b + c)

        return Problem(
            text=problem_text,
            operands=[a, b, c],
            operation='order_of_operations',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'simple_expression',
                'expression': expression,
                'a': a,
                'b': b,
                'c': c,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer)
            }
        )

    def _generate_money_transaction(self, seed: Optional[int] = None) -> Problem:
        """
        Generate a money transaction problem.

        Example: "You have $50. You spend $20, then earn $15. How much money do you have?"
        Correct: (50 - 20) + 15 = 30 + 15 = $45
        Malrule: 50 - (20 + 15) = 50 - 35 = $15
        """
        if seed is not None:
            random.seed(seed)

        # Use realistic money values
        a = random.choice([40, 50, 60, 75, 80, 100, 120, 150])
        b = random.choice([10, 15, 20, 25, 30, 35, 40])
        c = random.choice([5, 10, 15, 20, 25, 30])

        # Ensure a > b to avoid negative balance
        if b >= a:
            a = b + random.randint(20, 40)

        contexts = [
            f"You have ${a}. You spend ${b}, then earn ${c}. How much money do you have now?",
            f"Start with ${a}. Subtract ${b} for expenses, then add ${c} from earnings. What's the total?",
            f"Your account has ${a}. You withdraw ${b}, then deposit ${c}. What's your balance?",
            f"You have ${a} in savings. You pay ${b} for a bill, then receive ${c} from a refund. How much is left?",
        ]
        problem_text = random.choice(contexts)
        expression = f"{a} - {b} + {c}"

        # Calculate correct answer (left-to-right)
        correct_value = (a - b) + c

        # Calculate malrule answer (addition first)
        malrule_value = a - (b + c)

        return Problem(
            text=problem_text,
            operands=[a, b, c],
            operation='order_of_operations',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'money_transaction',
                'expression': expression,
                'a': a,
                'b': b,
                'c': c,
                'correct_answer': f"${correct_value}",
                'malrule_answer': f"${malrule_value}"
            }
        )

    def _generate_temperature_change(self, seed: Optional[int] = None) -> Problem:
        """
        Generate a temperature change problem.

        Example: "Temperature is 30°C. It drops 12°C, then rises 8°C. What's the final temperature?"
        Correct: (30 - 12) + 8 = 18 + 8 = 26°C
        Malrule: 30 - (12 + 8) = 30 - 20 = 10°C
        """
        if seed is not None:
            random.seed(seed)

        # Use realistic temperature values
        a = random.choice([20, 25, 30, 35, 40, 45])
        b = random.choice([5, 8, 10, 12, 15, 18])
        c = random.choice([3, 5, 7, 10, 12, 15])

        # Ensure a > b to avoid negative temperatures
        if b >= a:
            a = b + random.randint(10, 20)

        unit = random.choice(['°C', '°F'])

        contexts = [
            f"The temperature is {a}{unit}. It drops {b}{unit}, then rises {c}{unit}. What's the final temperature?",
            f"Starting at {a}{unit}, the temperature decreases by {b}{unit}, then increases by {c}{unit}. What's the result?",
            f"Temperature: {a}{unit}. Subtract {b}{unit}, then add {c}{unit}. What do you get?",
            f"At {a}{unit}, the temperature falls {b} degrees, then climbs {c} degrees. Final temperature?",
        ]
        problem_text = random.choice(contexts)
        expression = f"{a} - {b} + {c}"

        # Calculate correct answer (left-to-right)
        correct_value = (a - b) + c

        # Calculate malrule answer (addition first)
        malrule_value = a - (b + c)

        return Problem(
            text=problem_text,
            operands=[a, b, c],
            operation='order_of_operations',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'temperature_change',
                'expression': expression,
                'a': a,
                'b': b,
                'c': c,
                'unit': unit,
                'correct_answer': f"{correct_value}{unit}",
                'malrule_answer': f"{malrule_value}{unit}"
            }
        )

    def _generate_elevation_change(self, seed: Optional[int] = None) -> Problem:
        """
        Generate an elevation/altitude change problem.

        Example: "Starting at 150m elevation, descend 40m, then climb 25m. What's your elevation?"
        Correct: (150 - 40) + 25 = 110 + 25 = 135m
        Malrule: 150 - (40 + 25) = 150 - 65 = 85m
        """
        if seed is not None:
            random.seed(seed)

        # Use realistic elevation values
        a = random.choice([100, 120, 150, 180, 200, 250])
        b = random.choice([20, 25, 30, 40, 50, 60])
        c = random.choice([10, 15, 20, 25, 30, 35])

        # Ensure a > b to avoid negative elevation
        if b >= a:
            a = b + random.randint(40, 80)

        unit = random.choice(['m', 'ft', 'meters', 'feet'])

        contexts = [
            f"Starting at {a}{unit} elevation, you descend {b}{unit}, then climb {c}{unit}. What's your elevation?",
            f"You're at {a}{unit} altitude. You go down {b}{unit}, then up {c}{unit}. What's your new altitude?",
            f"Height: {a}{unit}. Decrease by {b}{unit}, then increase by {c}{unit}. Final height?",
            f"A drone is at {a}{unit}. It descends {b}{unit}, then ascends {c}{unit}. What's its altitude?",
        ]
        problem_text = random.choice(contexts)
        expression = f"{a} - {b} + {c}"

        # Calculate correct answer (left-to-right)
        correct_value = (a - b) + c

        # Calculate malrule answer (addition first)
        malrule_value = a - (b + c)

        return Problem(
            text=problem_text,
            operands=[a, b, c],
            operation='order_of_operations',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'elevation_change',
                'expression': expression,
                'a': a,
                'b': b,
                'c': c,
                'unit': unit,
                'correct_answer': f"{correct_value}{unit}",
                'malrule_answer': f"{malrule_value}{unit}"
            }
        )

    def _generate_score_tracking(self, seed: Optional[int] = None) -> Problem:
        """
        Generate a score/points tracking problem.

        Example: "Your score is 85 points. You lose 20 points, then gain 15 points. What's your final score?"
        Correct: (85 - 20) + 15 = 65 + 15 = 80 points
        Malrule: 85 - (20 + 15) = 85 - 35 = 50 points
        """
        if seed is not None:
            random.seed(seed)

        # Use realistic score values
        a = random.choice([50, 60, 75, 80, 100, 120, 150])
        b = random.choice([10, 15, 20, 25, 30, 35])
        c = random.choice([5, 10, 15, 20, 25, 30])

        # Ensure a > b to avoid negative score
        if b >= a:
            a = b + random.randint(30, 50)

        contexts = [
            f"Your score is {a} points. You lose {b} points, then gain {c} points. What's your final score?",
            f"Starting with {a} points, subtract {b} penalty points, then add {c} bonus points. Total score?",
            f"Game score: {a}. Deduct {b} points, then award {c} points. Final score?",
            f"You have {a} points. After a penalty of {b} points and a bonus of {c} points, what's your score?",
        ]
        problem_text = random.choice(contexts)
        expression = f"{a} - {b} + {c}"

        # Calculate correct answer (left-to-right)
        correct_value = (a - b) + c

        # Calculate malrule answer (addition first)
        malrule_value = a - (b + c)

        return Problem(
            text=problem_text,
            operands=[a, b, c],
            operation='order_of_operations',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'score_tracking',
                'expression': expression,
                'a': a,
                'b': b,
                'c': c,
                'correct_answer': f"{correct_value} points",
                'malrule_answer': f"{malrule_value} points"
            }
        )
