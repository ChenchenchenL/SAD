"""
Problem generator for Multiplication-Rule-For-Addition malrule.

Generates addition/subtraction problems with negative numbers that
elicit the misconception of applying multiplication rules to addition.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional, List
from utils import ProblemGenerator, Problem, DifficultyLevel


class NegativeAdditionProblemGenerator(ProblemGenerator):
    """
    Generates negative number addition/subtraction problems.

    Creates problems where students might incorrectly apply multiplication
    rules like "two negatives make a positive" to addition operations.
    """

    def get_name(self) -> str:
        return "Negative Number Addition Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates addition and subtraction problems with negative numbers "
            "that elicit the misconception of applying multiplication rules."
        )

    def get_available_templates(self) -> List[str]:
        """Return list of exactly 5 templates for this malrule."""
        return [
            'two_negatives_addition',     # -a + (-b) addition problems
            'positive_minus_negative',     # a - (-b) subtraction problems
            'word_problem_temperature',    # Temperature context
            'word_problem_elevation',      # Elevation/depth context
            'sequential_operations'        # Multi-step operations
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level."""
        ranges = {
            6: {
                DifficultyLevel.EASY: (1, 10),
                DifficultyLevel.MEDIUM: (1, 20),
                DifficultyLevel.HARD: (1, 30),
            },
            7: {
                DifficultyLevel.EASY: (1, 15),
                DifficultyLevel.MEDIUM: (1, 30),
                DifficultyLevel.HARD: (1, 50),
            },
            8: {
                DifficultyLevel.EASY: (1, 20),
                DifficultyLevel.MEDIUM: (1, 40),
                DifficultyLevel.HARD: (1, 60),
            },
            9: {
                DifficultyLevel.EASY: (1, 25),
                DifficultyLevel.MEDIUM: (1, 50),
                DifficultyLevel.HARD: (1, 80),
            }
        }

        lvl = self.level if self.level in ranges else 7
        return {'value': ranges[lvl][self.difficulty]}

    def _generate_two_negatives_addition(self, seed=None) -> Problem:
        """Generate addition of two negatives: -a + (-b)"""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['value']

        a = random.randint(min_val, max_val)
        b = random.randint(min_val, max_val)
        num1, num2 = -a, -b

        # Correct: -a + (-b) = -(a + b)
        correct_answer = num1 + num2

        # Malrule: student thinks two negatives make positive
        # So -a + (-b) becomes positive (a + b)
        malrule_answer = abs(a + b)

        problem_text = f"What is ({num1}) + ({num2})?"

        return Problem(
            text=problem_text,
            operands=[num1, num2],
            operation='negative_addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'two_negatives_addition',
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'num1': num1,
                'num2': num2
            }
        )

    def _generate_positive_minus_negative(self, seed=None) -> Problem:
        """Generate positive minus negative: a - (-b)"""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['value']

        a = random.randint(min_val, max_val)
        b = random.randint(min_val, max_val)
        num1, num2 = a, -b

        # Correct: a - (-b) = a + b
        correct_answer = num1 - num2

        # Malrule: student gets confused and subtracts instead of adding
        # They might compute a - b instead
        malrule_answer = a - b

        problem_text = f"What is {num1} - ({num2})?"

        return Problem(
            text=problem_text,
            operands=[num1, num2],
            operation='negative_subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'positive_minus_negative',
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'num1': num1,
                'num2': num2
            }
        )

    def _generate_word_problem_temperature(self, seed=None) -> Problem:
        """Generate temperature context problems"""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['value']

        # Pattern: Temperature starts negative, then drops further
        a = random.randint(min_val, min(max_val, 20))
        b = random.randint(min_val, min(max_val, 15))
        start_temp = -a
        drop = b

        # Correct: -a - b (temperature gets more negative)
        correct_answer = start_temp - drop

        # Malrule: student sees "negative" and "drop" and thinks two negatives = positive
        malrule_answer = abs(a + b)

        contexts = [
            f"The temperature was {start_temp}°C. It dropped by {drop}°C. What is the new temperature?",
            f"At midnight, the temperature was {start_temp}°F. By morning, it decreased by {drop}°F. What is the morning temperature?",
            f"The temperature in a freezer is {start_temp}°C. It drops another {drop}°C. What is the new temperature?",
            f"The outdoor temperature is {start_temp}°F and falls {drop}°F. What is the new temperature?",
        ]

        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[start_temp, drop],
            operation='negative_subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_temperature',
                'correct_answer': f'{correct_answer}°',
                'malrule_answer': f'{malrule_answer}°',
                'start_temp': start_temp,
                'change': drop
            }
        )

    def _generate_word_problem_elevation(self, seed=None) -> Problem:
        """Generate elevation/depth context problems"""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['value']

        # Pattern: Submarine/diver at negative elevation, descends more
        a = random.randint(min_val, min(max_val, 30))
        b = random.randint(min_val, min(max_val, 25))
        start_depth = -a
        descend = b

        # Correct: -a - b (depth gets more negative)
        correct_answer = start_depth - descend

        # Malrule: student thinks two negatives = positive
        malrule_answer = abs(a + b)

        contexts = [
            f"A submarine is at {start_depth} meters (below sea level). It descends another {descend} meters. What is its final depth?",
            f"A diver is at {start_depth}m. They go down {descend}m more. What is their elevation?",
            f"Elevation: {start_depth} meters. Descend {descend} meters more. Final elevation?",
            f"Starting at {start_depth}m below sea level, descend {descend}m. What's the new elevation?",
        ]

        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[start_depth, descend],
            operation='negative_subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_elevation',
                'correct_answer': f'{correct_answer}m',
                'malrule_answer': f'{malrule_answer}m',
                'start_depth': start_depth,
                'descend': descend
            }
        )

    def _generate_sequential_operations(self, seed=None) -> Problem:
        """Generate multi-step operations: -a + (-b) + c"""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['value']

        a = random.randint(min_val, max_val)
        b = random.randint(min_val, max_val)
        c = random.randint(min_val, max_val // 2)  # Smaller to keep result reasonable

        num1, num2, num3 = -a, -b, c

        # Correct: -a + (-b) + c = -(a + b) + c
        correct_answer = num1 + num2 + num3

        # Malrule: student applies "two negatives = positive" to -a + (-b)
        # So they compute: (a + b) + c instead of -(a + b) + c
        malrule_answer = abs(a + b) + c

        problem_texts = [
            f"Calculate: ({num1}) + ({num2}) + {num3}",
            f"What is ({num1}) + ({num2}) + {num3}?",
            f"Evaluate: ({num1}) + ({num2}) + {num3}",
            f"Find the value of ({num1}) + ({num2}) + {num3}.",
        ]

        problem_text = random.choice(problem_texts)

        return Problem(
            text=problem_text,
            operands=[num1, num2, num3],
            operation='sequential_operations',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'sequential_operations',
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'num1': num1,
                'num2': num2,
                'num3': num3
            }
        )

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate a negative number addition/subtraction problem.

        Args:
            seed: Optional random seed for reproducibility
            template: Optional template name. If None, random template is chosen.

        Returns:
            Problem instance
        """
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            template = random.choice(self.get_available_templates())

        # Validate template
        if template not in self.get_available_templates():
            raise ValueError(f"Invalid template: {template}")

        # Generate based on template
        if template == 'two_negatives_addition':
            return self._generate_two_negatives_addition(seed)
        elif template == 'positive_minus_negative':
            return self._generate_positive_minus_negative(seed)
        elif template == 'word_problem_temperature':
            return self._generate_word_problem_temperature(seed)
        elif template == 'word_problem_elevation':
            return self._generate_word_problem_elevation(seed)
        elif template == 'sequential_operations':
            return self._generate_sequential_operations(seed)
        else:
            # Fallback to two_negatives_addition
            return self._generate_two_negatives_addition(seed)
