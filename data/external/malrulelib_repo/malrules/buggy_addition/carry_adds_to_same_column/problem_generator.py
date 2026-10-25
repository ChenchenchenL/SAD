"""
Problem generator for Carry-Adds-To-Same-Column malrule.

Generates multi-digit addition problems where at least one column sum exceeds 9,
triggering the malrule behavior where carry is added to the same column.
"""

import random
from typing import Dict, Tuple, Optional, List
import sys
sys.path.append('/home/user/malrule-coding')

from utils import Problem, ProblemGenerator, DifficultyLevel, create_basic_arithmetic_template


class CarryAddsToSameColumnProblemGenerator(ProblemGenerator):
    """
    Generates addition problems where at least one column sum exceeds 9,
    causing the Carry-Adds-To-Same-Column malrule to produce incorrect answers.
    """

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level and difficulty."""
        ranges = {
            2: {
                DifficultyLevel.EASY: (10, 50),
                DifficultyLevel.MEDIUM: (20, 80),
                DifficultyLevel.HARD: (40, 99),
            },
            3: {
                DifficultyLevel.EASY: (100, 300),
                DifficultyLevel.MEDIUM: (200, 600),
                DifficultyLevel.HARD: (400, 999),
            },
            4: {
                DifficultyLevel.EASY: (100, 500),
                DifficultyLevel.MEDIUM: (500, 2000),
                DifficultyLevel.HARD: (1000, 9999),
            }
        }

        # Default to level 3 if not in ranges
        lvl = self.level if self.level in ranges else 3
        return {'addend1': ranges[lvl][self.difficulty],
                'addend2': ranges[lvl][self.difficulty]}

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_addition',
            'money_context',
            'measurement_context',
            'three_digit',
            'word_problem_result_unknown',
        ]

    def _has_carry_opportunity(self, addend1: int, addend2: int) -> bool:
        """
        Check if problem has at least one column where sum exceeds 9.
        This is where the Carry-Adds-To-Same-Column malrule will be triggered.

        Args:
            addend1: First number
            addend2: Second number

        Returns:
            True if at least one column sum exceeds 9
        """
        # Pad numbers to same length
        max_len = max(len(str(addend1)), len(str(addend2)))
        addend1_str = str(addend1).zfill(max_len)
        addend2_str = str(addend2).zfill(max_len)

        # Check if any column sum exceeds 9
        for d1, d2 in zip(addend1_str, addend2_str):
            if int(d1) + int(d2) > 9:
                return True

        return False

    def _calculate_correct(self, addend1: int, addend2: int) -> int:
        """Calculate the correct answer."""
        return addend1 + addend2

    def _calculate_malrule(self, addend1: int, addend2: int) -> int:
        """
        Calculate the malrule answer.

        For Carry-Adds-To-Same-Column:
        - When a column sum > 9, add the units digit and carry digit together
        - Write that combined result in the current column
        - Do NOT carry to the next column
        """
        # Convert to digit lists (rightmost digit first for easier processing)
        addend1_digits = [int(d) for d in str(addend1)][::-1]
        addend2_digits = [int(d) for d in str(addend2)][::-1]

        # Pad to same length
        max_len = max(len(addend1_digits), len(addend2_digits))
        while len(addend1_digits) < max_len:
            addend1_digits.append(0)
        while len(addend2_digits) < max_len:
            addend2_digits.append(0)

        result_digits = []

        # Process each column - NO carry to next column
        for i in range(max_len):
            column_sum = addend1_digits[i] + addend2_digits[i]

            if column_sum > 9:
                # MALRULE: Add units digit and carry digit together
                units_digit = column_sum % 10
                carry_digit = column_sum // 10
                combined = units_digit + carry_digit
                result_digits.append(combined)
            else:
                # No carry needed, just use the sum
                result_digits.append(column_sum)

        # Remove leading zeros
        while len(result_digits) > 1 and result_digits[-1] == 0:
            result_digits.pop()

        return int(''.join(str(d) for d in result_digits[::-1]))

    def _generate_problem_text(self, addend1: int, addend2: int, problem_type: str) -> str:
        """
        Generate problem text based on problem type.

        Args:
            addend1: First number
            addend2: Second number
            problem_type: Type of problem context

        Returns:
            Formatted problem text
        """
        if problem_type == 'basic':
            template = create_basic_arithmetic_template('addition')
            return template.generate({'a': addend1, 'b': addend2})

        elif problem_type == 'money':
            contexts = [
                f"Sarah had ${addend1}. She earned ${addend2} more. How much money does she have now?",
                f"A store had ${addend1} in the cash register. After a sale of ${addend2}, how much is there?",
                f"Tom saved ${addend1} and then earned ${addend2} from chores. How much money does he have now?",
                f"Maria had ${addend1} in savings. She received ${addend2} as a gift. How much does she have?",
            ]
            return random.choice(contexts)

        elif problem_type == 'measurement':
            # Use appropriate units based on magnitude
            if addend1 < 100:
                units = [
                    ('inches', 'ribbon'),
                    ('centimeters', 'rope'),
                    ('feet', 'wood'),
                ]
            else:
                units = [
                    ('meters', 'fabric'),
                    ('feet', 'cable'),
                    ('yards', 'rope'),
                ]

            unit, item = random.choice(units)

            contexts = [
                f"A piece of {item} was {addend1} {unit} long. Another piece of {addend2} {unit} was added. What is the total length?",
                f"Lisa had {addend1} {unit} of {item}. She bought {addend2} {unit} more. How much does she have now?",
            ]
            return random.choice(contexts)

        elif problem_type == 'three_digit':
            contexts = [
                f"What is {addend1} + {addend2}?",
                f"Calculate: {addend1} + {addend2}",
                f"Add {addend1} and {addend2}.",
                f"Find the sum of {addend1} and {addend2}.",
                f"A school has {addend1} students. {addend2} new students enrolled. How many students are there now?",
            ]
            return random.choice(contexts)

        else:
            # Default to basic
            template = create_basic_arithmetic_template('addition')
            return template.generate({'a': addend1, 'b': addend2})

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate an addition problem where Carry-Adds-To-Same-Column will produce wrong answer.

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
        if template == 'basic_addition':
            return self._generate_basic_addition(seed)
        elif template == 'money_context':
            return self._generate_money_context(seed)
        elif template == 'measurement_context':
            return self._generate_measurement_context(seed)
        elif template == 'three_digit':
            return self._generate_three_digit(seed)
        elif template == 'word_problem_result_unknown':
            return self._generate_word_problem_result_unknown(seed)
        else:
            return self._generate_basic_addition(seed)

    def _generate_basic_addition(self, seed: Optional[int] = None) -> Problem:
        """Template 1: Basic addition problems (2-digit)."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['addend1']

        # Try to generate a problem with carry opportunity
        for _ in range(100):
            addend1 = random.randint(min_val, max_val)
            addend2 = random.randint(min_val, max_val)

            if self._has_carry_opportunity(addend1, addend2):
                correct_answer = self._calculate_correct(addend1, addend2)
                malrule_answer = self._calculate_malrule(addend1, addend2)

                # Only use if malrule produces different answer
                if correct_answer != malrule_answer:
                    problem_text = self._generate_problem_text(addend1, addend2, 'basic')

                    return Problem(
                        text=problem_text,
                        operands=[addend1, addend2],
                        operation='addition',
                        level=self.level,
                        difficulty=self.difficulty,
                        metadata={
                            'has_carry': True,
                            'problem_type': 'basic',
                            'template': 'basic_addition',
                            'correct_answer': str(correct_answer),
                            'malrule_answer': str(malrule_answer),
                        }
                    )

        # Fallback
        addend1 = random.randint(min_val, max_val)
        addend2 = random.randint(min_val, max_val)
        correct_answer = self._calculate_correct(addend1, addend2)
        malrule_answer = self._calculate_malrule(addend1, addend2)
        problem_text = self._generate_problem_text(addend1, addend2, 'basic')

        return Problem(
            text=problem_text,
            operands=[addend1, addend2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'has_carry': self._has_carry_opportunity(addend1, addend2),
                'problem_type': 'basic',
                'template': 'basic_addition',
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
            }
        )

    def _generate_money_context(self, seed: Optional[int] = None) -> Problem:
        """Template 2: Money word problems."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['addend1']

        for _ in range(100):
            addend1 = random.randint(min_val, max_val)
            addend2 = random.randint(min_val, max_val)

            if self._has_carry_opportunity(addend1, addend2):
                correct_answer = self._calculate_correct(addend1, addend2)
                malrule_answer = self._calculate_malrule(addend1, addend2)

                if correct_answer != malrule_answer:
                    problem_text = self._generate_problem_text(addend1, addend2, 'money')

                    return Problem(
                        text=problem_text,
                        operands=[addend1, addend2],
                        operation='addition',
                        level=self.level,
                        difficulty=self.difficulty,
                        metadata={
                            'has_carry': True,
                            'problem_type': 'money',
                            'template': 'money_context',
                            'correct_answer': str(correct_answer),
                            'malrule_answer': str(malrule_answer),
                        }
                    )

        addend1 = random.randint(min_val, max_val)
        addend2 = random.randint(min_val, max_val)
        correct_answer = self._calculate_correct(addend1, addend2)
        malrule_answer = self._calculate_malrule(addend1, addend2)
        problem_text = self._generate_problem_text(addend1, addend2, 'money')

        return Problem(
            text=problem_text,
            operands=[addend1, addend2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'has_carry': self._has_carry_opportunity(addend1, addend2),
                'problem_type': 'money',
                'template': 'money_context',
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
            }
        )

    def _generate_measurement_context(self, seed: Optional[int] = None) -> Problem:
        """Template 3: Measurement word problems."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['addend1']

        for _ in range(100):
            addend1 = random.randint(min_val, max_val)
            addend2 = random.randint(min_val, max_val)

            if self._has_carry_opportunity(addend1, addend2):
                correct_answer = self._calculate_correct(addend1, addend2)
                malrule_answer = self._calculate_malrule(addend1, addend2)

                if correct_answer != malrule_answer:
                    problem_text = self._generate_problem_text(addend1, addend2, 'measurement')

                    return Problem(
                        text=problem_text,
                        operands=[addend1, addend2],
                        operation='addition',
                        level=self.level,
                        difficulty=self.difficulty,
                        metadata={
                            'has_carry': True,
                            'problem_type': 'measurement',
                            'template': 'measurement_context',
                            'correct_answer': str(correct_answer),
                            'malrule_answer': str(malrule_answer),
                        }
                    )

        addend1 = random.randint(min_val, max_val)
        addend2 = random.randint(min_val, max_val)
        correct_answer = self._calculate_correct(addend1, addend2)
        malrule_answer = self._calculate_malrule(addend1, addend2)
        problem_text = self._generate_problem_text(addend1, addend2, 'measurement')

        return Problem(
            text=problem_text,
            operands=[addend1, addend2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'has_carry': self._has_carry_opportunity(addend1, addend2),
                'problem_type': 'measurement',
                'template': 'measurement_context',
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
            }
        )

    def _generate_three_digit(self, seed: Optional[int] = None) -> Problem:
        """Template 4: Three-digit addition problems."""
        if seed is not None:
            random.seed(seed)

        # Force 3-digit range
        min_val, max_val = 100, 999

        for _ in range(100):
            addend1 = random.randint(min_val, max_val)
            addend2 = random.randint(min_val, max_val)

            if self._has_carry_opportunity(addend1, addend2):
                correct_answer = self._calculate_correct(addend1, addend2)
                malrule_answer = self._calculate_malrule(addend1, addend2)

                if correct_answer != malrule_answer:
                    problem_text = self._generate_problem_text(addend1, addend2, 'three_digit')

                    return Problem(
                        text=problem_text,
                        operands=[addend1, addend2],
                        operation='addition',
                        level=self.level,
                        difficulty=self.difficulty,
                        metadata={
                            'has_carry': True,
                            'problem_type': 'three_digit',
                            'template': 'three_digit',
                            'correct_answer': str(correct_answer),
                            'malrule_answer': str(malrule_answer),
                        }
                    )

        addend1 = random.randint(min_val, max_val)
        addend2 = random.randint(min_val, max_val)
        correct_answer = self._calculate_correct(addend1, addend2)
        malrule_answer = self._calculate_malrule(addend1, addend2)
        problem_text = self._generate_problem_text(addend1, addend2, 'three_digit')

        return Problem(
            text=problem_text,
            operands=[addend1, addend2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'has_carry': self._has_carry_opportunity(addend1, addend2),
                'problem_type': 'three_digit',
                'template': 'three_digit',
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
            }
        )

    def _generate_word_problem_result_unknown(self, seed: Optional[int] = None) -> Problem:
        """Template 5: Word problems with result unknown (enhanced contexts)."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['addend1']

        for _ in range(100):
            addend1 = random.randint(min_val, max_val)
            addend2 = random.randint(min_val, max_val)

            if self._has_carry_opportunity(addend1, addend2):
                correct_answer = self._calculate_correct(addend1, addend2)
                malrule_answer = self._calculate_malrule(addend1, addend2)

                if correct_answer != malrule_answer:
                    context_sets = [
                        f"Emma collected {addend1} stickers. She got {addend2} more stickers. How many stickers does she have now?",
                        f"A movie theater sold {addend1} tickets in the morning and {addend2} tickets in the afternoon. How many tickets were sold in total?",
                        f"There were {addend1} students in the cafeteria. {addend2} more students arrived. How many students are in the cafeteria now?"
                    ]
                    problem_text = random.choice(context_sets)

                    return Problem(
                        text=problem_text,
                        operands=[addend1, addend2],
                        operation='addition',
                        level=self.level,
                        difficulty=self.difficulty,
                        metadata={
                            'has_carry': True,
                            'problem_type': 'word_problem_result_unknown',
                            'template': 'word_problem_result_unknown',
                            'formula_type': 'result_unknown',
                            'correct_answer': str(correct_answer),
                            'malrule_answer': str(malrule_answer),
                        }
                    )

        # Fallback
        addend1 = random.randint(min_val, max_val)
        addend2 = random.randint(min_val, max_val)
        correct_answer = self._calculate_correct(addend1, addend2)
        malrule_answer = self._calculate_malrule(addend1, addend2)
        problem_text = f"There were {addend1} items. {addend2} more were added. How many are there now?"

        return Problem(
            text=problem_text,
            operands=[addend1, addend2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'has_carry': self._has_carry_opportunity(addend1, addend2),
                'problem_type': 'word_problem_result_unknown',
                'template': 'word_problem_result_unknown',
                'formula_type': 'result_unknown',
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer),
            }
        )
