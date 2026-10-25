"""
Problem generator for Negative-Times-Negative-Negative malrule.

Generates multiplication problems with negative numbers that elicit
the reversed sign rule misconception.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional, List
from utils import ProblemGenerator, Problem, DifficultyLevel


class NegativeTimesNegativeNegativeProblemGenerator(ProblemGenerator):
    """
    Generates negative number multiplication problems.

    Creates problems with various sign combinations to test understanding
    of multiplication sign rules, especially negative × negative cases.
    """

    def get_name(self) -> str:
        return "Negative-Times-Negative-Negative Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates multiplication problems with negative numbers that "
            "test understanding of sign rules, particularly negative × negative."
        )

    def get_available_templates(self) -> List[str]:
        """Return list of all templates for this malrule."""
        return [
            'basic_multiplication',              # Simple (-a) × (-b)
            'word_problem_temperature',          # Temperature context
            'word_problem_debt',                 # Money/debt context
            'equation_solving',                  # Solving equations
            'pattern_completion',                # Multiplication pattern
            'word_problem_multi_step',           # (-a) × (-b) × (-c)
            'word_problem_mixed_operations',     # (-a) × (-b) + c
            'word_problem_distributive',         # -a(b + c) or -a(-b - c)
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level."""
        ranges = {
            6: {
                DifficultyLevel.EASY: (2, 10),
                DifficultyLevel.MEDIUM: (2, 15),
                DifficultyLevel.HARD: (5, 20),
            },
            7: {
                DifficultyLevel.EASY: (2, 15),
                DifficultyLevel.MEDIUM: (5, 20),
                DifficultyLevel.HARD: (5, 30),
            },
            8: {
                DifficultyLevel.EASY: (5, 20),
                DifficultyLevel.MEDIUM: (5, 30),
                DifficultyLevel.HARD: (10, 50),
            },
            9: {
                DifficultyLevel.EASY: (5, 25),
                DifficultyLevel.MEDIUM: (10, 40),
                DifficultyLevel.HARD: (10, 100),
            }
        }

        lvl = self.level if self.level in ranges else 7
        return {'operands': ranges[lvl][self.difficulty]}

    def _generate_basic_multiplication(self, seed=None) -> Problem:
        """Generate basic negative × negative multiplication: (-a) × (-b)"""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['operands']

        # Generate two negative numbers
        a_abs = random.randint(min_val, max_val)
        b_abs = random.randint(min_val, max_val)
        a, b = -a_abs, -b_abs

        # Correct: (-a) × (-b) = positive
        correct_answer = a * b

        # Malrule: student thinks (-a) × (-b) = negative
        malrule_answer = -(a_abs * b_abs)

        problem_text = f"Calculate: ({a}) × ({b})"

        return Problem(
            text=problem_text,
            operands=[a, b],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'basic_multiplication',
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'a': a,
                'b': b,
                'a_abs': a_abs,
                'b_abs': b_abs,
                'problem_type': 'neg_times_neg'
            }
        )

    def _generate_word_problem_temperature(self, seed=None) -> Problem:
        """Generate temperature context: reversing a temperature drop"""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['operands']

        # Pattern: A temperature drop is reversed
        drop_amount = random.randint(min_val, min(max_val, 20))
        num_reversals = random.randint(2, 5)

        # Using negatives: (-drop) × (-reversals) represents reversing drops
        a, b = -drop_amount, -num_reversals

        # Correct: reversing a drop is a rise (negative × negative = positive)
        correct_answer = a * b

        # Malrule: student thinks it stays negative
        malrule_answer = -(drop_amount * num_reversals)

        contexts = [
            f"A temperature dropped by {drop_amount} degrees. If this drop is reversed {num_reversals} times, what is the total temperature change?",
            f"The temperature decreased {drop_amount}°C. Reversing this change {num_reversals} times gives what total change?",
            f"If a {drop_amount} degree drop is reversed {num_reversals} times, what is the net temperature change?",
        ]

        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[a, b],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_temperature',
                'correct_answer': f'+{correct_answer}°',
                'malrule_answer': f'{malrule_answer}°',
                'drop_amount': drop_amount,
                'num_reversals': num_reversals,
                'a': a,
                'b': b
            }
        )

    def _generate_word_problem_debt(self, seed=None) -> Problem:
        """Generate money/debt context: removing debts"""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['operands']

        # Pattern: Removing debts (negative amounts)
        debt_amount = random.randint(min_val, min(max_val, 50))
        num_debts = random.randint(2, 5)

        # Using negatives: (-debt) × (-number) represents removing debts
        a, b = -debt_amount, -num_debts

        # Correct: removing debts is a gain (negative × negative = positive)
        correct_answer = a * b

        # Malrule: student thinks result is negative
        malrule_answer = -(debt_amount * num_debts)

        contexts = [
            f"You owe ${debt_amount}. If {num_debts} of these debts are removed, what is the change to your balance?",
            f"A person has {num_debts} debts of ${debt_amount} each. If all debts are forgiven, what is the financial change?",
            f"Removing {num_debts} debts of ${debt_amount} each results in what net change?",
            f"If ${debt_amount} debts are eliminated {num_debts} times, what is the total financial impact?",
        ]

        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[a, b],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_debt',
                'correct_answer': f'+${correct_answer}',
                'malrule_answer': f'${malrule_answer}',
                'debt_amount': debt_amount,
                'num_debts': num_debts,
                'a': a,
                'b': b
            }
        )

    def _generate_equation_solving(self, seed=None) -> Problem:
        """Generate equation solving: Solve for x in (-a) × x = b where x is negative"""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['operands']

        # Create equation: (-a) × x = b where x will be negative
        a_abs = random.randint(min_val, min(max_val, 12))
        x_abs = random.randint(min_val, min(max_val, 10))

        a = -a_abs
        x = -x_abs
        b = a * x  # This will be positive (neg × neg = pos)

        # Correct: x = b / (-a) = b / (-a) = negative value
        correct_answer = x

        # Malrule: student thinks (-a) × (negative) = positive, so they might get positive x
        # Or they apply the malrule and get: x = b / (-a) but think it should be positive
        malrule_answer = abs(x)

        problem_text = f"Solve for x: ({a}) × x = {b}"

        return Problem(
            text=problem_text,
            operands=[a, b],
            operation='equation',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'equation_solving',
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'a': a,
                'b': b,
                'x': x,
                'a_abs': a_abs,
                'x_abs': x_abs
            }
        )

    def _generate_pattern_completion(self, seed=None) -> Problem:
        """Generate pattern completion: Complete a multiplication pattern"""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['operands']

        # Create a pattern showing decreasing first operand
        b_abs = random.randint(min_val, min(max_val, 10))
        b = -b_abs

        # Pattern: 3 × (-b), 2 × (-b), 1 × (-b), 0 × (-b), (-1) × (-b), (-2) × (-b)
        # We'll ask for (-2) × (-b)
        a = -2

        # Correct: (-2) × (-b) = positive
        correct_answer = a * b

        # Malrule: student thinks it's negative
        malrule_answer = -(2 * b_abs)

        # Build pattern display
        pattern_lines = []
        for i in range(3, -1, -1):
            result = i * b
            pattern_lines.append(f"{i} × ({b}) = {result}")

        pattern_display = "\n".join(pattern_lines)

        problem_text = f"Complete the pattern:\n{pattern_display}\n(-1) × ({b}) = ?\n(-2) × ({b}) = ?"

        return Problem(
            text=problem_text,
            operands=[a, b],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'pattern_completion',
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'a': a,
                'b': b,
                'b_abs': b_abs,
                'pattern': pattern_display
            }
        )

    def _generate_word_problem_multi_step(self, seed=None) -> Problem:
        """Generate word problem with multi-step multiplication: (-a) × (-b) × c (even negatives)"""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['operands']

        # Generate TWO negative numbers and ONE positive (to ensure malrule gives wrong answer)
        a_abs = random.randint(min_val, min(max_val, 10))
        b_abs = random.randint(min_val, min(max_val, 10))
        c = random.randint(min_val, min(max_val, 10))  # c is positive
        a, b = -a_abs, -b_abs

        # Correct: (-a) × (-b) × c = positive × c = positive (two negatives = positive, then × positive)
        correct_answer = a * b * c

        # Malrule: student thinks (-a) × (-b) = negative, then × c = negative
        malrule_answer = -(a_abs * b_abs * c)

        # Select from 3 question variants for this problem type
        # Pattern: reversing (neg × neg = pos) a negative change, applied c times (pos × pos)
        contexts = [
            f"A submarine that was descending at {a} m/s had its descent reversed (multiplied by {b}) for {c} time periods. What is the total depth change in meters?",
            f"If canceling ${a_abs} debt is done {b_abs} times (reversing the negative), and this is repeated for {c} customers, what is the total financial change?",
            f"A temperature drop of {a}°C that is reversed {b} times, then applied across {c} identical systems. What is the total temperature change?"
        ]

        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[a, b, c],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_multi_step',
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'a': a,
                'b': b,
                'c': c,
                'a_abs': a_abs,
                'b_abs': b_abs,
                'problem_type': 'multi_step_multiplication',
                'formula': '(-a) × (-b) × c'
            }
        )

    def _generate_word_problem_mixed_operations(self, seed=None) -> Problem:
        """Generate word problem with mixed operations: (-a) × (-b) + c"""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['operands']

        # Generate two negatives and one adjustment
        a_abs = random.randint(min_val, min(max_val, 15))
        b_abs = random.randint(min_val, min(max_val, 15))
        c = random.randint(min_val, min(max_val, 20))
        a, b = -a_abs, -b_abs

        # Correct: (-a) × (-b) + c = positive product + c
        correct_answer = a * b + c

        # Malrule: (-a) × (-b) = negative (wrong!), then add c
        malrule_answer = -(a_abs * b_abs) + c

        # Select from 3 question variants for this problem type
        contexts = [
            f"You remove {a_abs} debts of ${b_abs} each, then receive an additional ${c} bonus. What is your total financial gain?",
            f"A temperature drop of {a_abs}°C is reversed {b_abs} times, then the temperature increases by an additional {c}°C. What is the total temperature change?",
            f"If {a_abs} backward steps of {b_abs} meters each are reversed, then you move forward {c} meters more, what is your total displacement?"
        ]

        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[a, b, c],
            operation='mixed',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_mixed_operations',
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'a': a,
                'b': b,
                'c': c,
                'a_abs': a_abs,
                'b_abs': b_abs,
                'problem_type': 'mixed_operations',
                'formula': '(-a) × (-b) + c'
            }
        )

    def _generate_word_problem_distributive(self, seed=None) -> Problem:
        """Generate word problem with distributive property: -a(-b - c) or -a(b + c)"""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['operands']

        # Generate values for distributive property
        a_abs = random.randint(min_val, min(max_val, 12))

        # Always use both_negative pattern to trigger the neg×neg malrule
        pattern_choice = 'both_negative'

        # -a(-b - c) = -a × (-b) + (-a) × (-c) = ab + ac
        b_abs = random.randint(min_val, min(max_val, 10))
        c_abs = random.randint(min_val, min(max_val, 10))
        a, b, c = -a_abs, -b_abs, -c_abs

        # Correct: -a(-b - c) = ab + ac (positive)
        correct_answer = a * (b + c)  # This expands correctly

        # Malrule: student thinks -a × (-b) = negative, -a × (-c) = negative
        # So they get: -ab + (-ac) = -(ab + ac)
        malrule_answer = -(a_abs * b_abs + a_abs * c_abs)

        contexts = [
            f"If you remove {a_abs} groups, where each group consists of a ${b_abs} debt and a ${c_abs} debt, what is your total financial change?",
            f"A container has {a_abs} sections removed, each section has a temperature drop of {b_abs}°C and an additional drop of {c_abs}°C. What is the total temperature change?",
            f"Reversing {a_abs} descents, where each descent includes {b_abs} meters down and {c_abs} meters down, what is the total elevation change?"
        ]

        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[a, b, c],
            operation='distributive',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_distributive',
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
                'a': a,
                'b': b,
                'c': c,
                'a_abs': a_abs,
                'pattern': pattern_choice,
                'problem_type': 'distributive_property',
                'formula': f'-{a_abs}({b} + {c})' if pattern_choice != 'both_negative' else f'-{a_abs}(-{abs(b)} - {abs(c)})'
            }
        )

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate a negative number multiplication problem.

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
        if template == 'basic_multiplication':
            return self._generate_basic_multiplication(seed)
        elif template == 'word_problem_temperature':
            return self._generate_word_problem_temperature(seed)
        elif template == 'word_problem_debt':
            return self._generate_word_problem_debt(seed)
        elif template == 'equation_solving':
            return self._generate_equation_solving(seed)
        elif template == 'pattern_completion':
            return self._generate_pattern_completion(seed)
        elif template == 'word_problem_multi_step':
            return self._generate_word_problem_multi_step(seed)
        elif template == 'word_problem_mixed_operations':
            return self._generate_word_problem_mixed_operations(seed)
        elif template == 'word_problem_distributive':
            return self._generate_word_problem_distributive(seed)
        else:
            # Fallback to basic_multiplication
            return self._generate_basic_multiplication(seed)
