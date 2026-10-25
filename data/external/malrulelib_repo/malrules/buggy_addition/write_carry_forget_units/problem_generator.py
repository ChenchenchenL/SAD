"""
Problem generator for Write-Carry-Forget-Units malrule.

Generates multi-digit addition problems where at least one column requires
a carry, causing the malrule to produce incorrect answers.
"""

import random
from typing import Dict, Tuple, Optional, List
import sys
sys.path.append('/Users/kitetsu/nlp_mac/malrule-coding')

from utils import Problem, ProblemGenerator, DifficultyLevel


class WriteCarryForgetUnitsProblemGenerator(ProblemGenerator):
    """
    Generates addition problems where at least one column produces a carry,
    causing the Write-Carry-Forget-Units malrule to produce incorrect answers.
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
            'four_digit',
            'word_problem_result_unknown',
            'word_problem_combining',
            'word_problem_comparison'
        ]

    def _has_carry_opportunity(self, addend1: int, addend2: int) -> bool:
        """
        Check if problem has at least one column where digits sum to 10 or more.
        This is where the Write-Carry-Forget-Units malrule will produce wrong answer.

        Args:
            addend1: First number
            addend2: Second number

        Returns:
            True if at least one column produces a carry
        """
        # Pad to same length
        max_len = max(len(str(addend1)), len(str(addend2)))
        addend1_str = str(addend1).zfill(max_len)
        addend2_str = str(addend2).zfill(max_len)

        # Check if any column sums to 10 or more
        for d1, d2 in zip(addend1_str, addend2_str):
            if int(d1) + int(d2) >= 10:
                return True

        return False

    def _calculate_correct(self, addend1: int, addend2: int) -> int:
        """Calculate the correct answer."""
        return addend1 + addend2

    def _calculate_malrule(self, addend1: int, addend2: int) -> int:
        """
        Calculate the malrule answer.

        For each column (processed independently, no carry propagation!):
        - If sum >= 10: write the carry digit (tens digit), forget the units
        - If sum < 10: write the units digit normally

        Key insight from Brown & Burton (1978): the carry is written but NOT
        propagated to the next column.
        """
        # Pad to same length
        max_len = max(len(str(addend1)), len(str(addend2)))
        addend1_digits = [int(d) for d in str(addend1).zfill(max_len)][::-1]
        addend2_digits = [int(d) for d in str(addend2).zfill(max_len)][::-1]

        result_digits = []

        # Process each column independently (no carry propagation!)
        for i in range(max_len):
            column_sum = addend1_digits[i] + addend2_digits[i]
            # Note: No carry is added from previous column!

            if column_sum >= 10:
                # MALRULE: Write the carry digit, forget the units
                result_digits.append(column_sum // 10)
            else:
                # Normal: write the units digit
                result_digits.append(column_sum)

        # No final carry is added (it was already "written" in the answer)

        # Remove leading zeros and convert to number
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
            templates = [
                f"What is {addend1} + {addend2}?",
                f"Calculate: {addend1} + {addend2}",
                f"Add {addend1} and {addend2}.",
                f"Find the sum of {addend1} and {addend2}.",
            ]
            return random.choice(templates)

        elif problem_type == 'money':
            contexts = [
                f"Sarah has ${addend1}. She earns ${addend2} more. How much money does she have now?",
                f"A store sold ${addend1} worth of goods in the morning and ${addend2} in the afternoon. What is the total?",
                f"Tom saved ${addend1} and then received ${addend2} as a gift. How much money does he have now?",
                f"Maria earned ${addend1} from her first job and ${addend2} from her second job. What is her total earnings?",
            ]
            return random.choice(contexts)

        elif problem_type == 'measurement':
            if max(addend1, addend2) < 100:
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
                    ('kilometers', 'road'),
                ]

            unit, item = random.choice(units)

            contexts = [
                f"A piece of {item} is {addend1} {unit} long. Another piece is {addend2} {unit}. What is the total length?",
                f"The first {item} measures {addend1} {unit}. The second measures {addend2} {unit}. How long are they together?",
            ]
            return random.choice(contexts)

        elif problem_type == 'three_digit':
            contexts = [
                f"What is {addend1} + {addend2}?",
                f"Calculate: {addend1} + {addend2}",
                f"A school has {addend1} students in the morning classes and {addend2} in the afternoon. How many total?",
                f"A library had {addend1} books. They received {addend2} more. How many books now?",
            ]
            return random.choice(contexts)

        else:
            return f"What is {addend1} + {addend2}?"

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate an addition problem where Write-Carry-Forget-Units will fail.

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
        elif template == 'four_digit':
            return self._generate_four_digit(seed)
        elif template == 'word_problem_result_unknown':
            return self._generate_word_problem_result_unknown(seed)
        elif template == 'word_problem_combining':
            return self._generate_word_problem_combining(seed)
        elif template == 'word_problem_comparison':
            return self._generate_word_problem_comparison(seed)
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
                problem_text = self._generate_problem_text(addend1, addend2, 'basic')
                correct_answer = self._calculate_correct(addend1, addend2)
                malrule_answer = self._calculate_malrule(addend1, addend2)

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
                        'malrule_answer': str(malrule_answer)
                    }
                )

        # Fallback
        addend1 = random.randint(min_val, max_val)
        addend2 = random.randint(min_val, max_val)
        problem_text = self._generate_problem_text(addend1, addend2, 'basic')
        correct_answer = self._calculate_correct(addend1, addend2)
        malrule_answer = self._calculate_malrule(addend1, addend2)

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
                'malrule_answer': str(malrule_answer)
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
                problem_text = self._generate_problem_text(addend1, addend2, 'money')
                correct_answer = self._calculate_correct(addend1, addend2)
                malrule_answer = self._calculate_malrule(addend1, addend2)

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
                        'malrule_answer': str(malrule_answer)
                    }
                )

        addend1 = random.randint(min_val, max_val)
        addend2 = random.randint(min_val, max_val)
        problem_text = self._generate_problem_text(addend1, addend2, 'money')
        correct_answer = self._calculate_correct(addend1, addend2)
        malrule_answer = self._calculate_malrule(addend1, addend2)

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
                'malrule_answer': str(malrule_answer)
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
                problem_text = self._generate_problem_text(addend1, addend2, 'measurement')
                correct_answer = self._calculate_correct(addend1, addend2)
                malrule_answer = self._calculate_malrule(addend1, addend2)

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
                        'malrule_answer': str(malrule_answer)
                    }
                )

        addend1 = random.randint(min_val, max_val)
        addend2 = random.randint(min_val, max_val)
        problem_text = self._generate_problem_text(addend1, addend2, 'measurement')
        correct_answer = self._calculate_correct(addend1, addend2)
        malrule_answer = self._calculate_malrule(addend1, addend2)

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
                'malrule_answer': str(malrule_answer)
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
                problem_text = self._generate_problem_text(addend1, addend2, 'three_digit')
                correct_answer = self._calculate_correct(addend1, addend2)
                malrule_answer = self._calculate_malrule(addend1, addend2)

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
                        'malrule_answer': str(malrule_answer)
                    }
                )

        addend1 = random.randint(min_val, max_val)
        addend2 = random.randint(min_val, max_val)
        problem_text = self._generate_problem_text(addend1, addend2, 'three_digit')
        correct_answer = self._calculate_correct(addend1, addend2)
        malrule_answer = self._calculate_malrule(addend1, addend2)

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
                'malrule_answer': str(malrule_answer)
            }
        )

    def _generate_four_digit(self, seed: Optional[int] = None) -> Problem:
        """Template 5: Four-digit addition problems."""
        if seed is not None:
            random.seed(seed)

        # Force 4-digit range
        min_val, max_val = 1000, 9999

        for _ in range(100):
            addend1 = random.randint(min_val, max_val)
            addend2 = random.randint(min_val, max_val)

            if self._has_carry_opportunity(addend1, addend2):
                contexts = [
                    f"What is {addend1} + {addend2}?",
                    f"Calculate: {addend1} + {addend2}",
                    f"A factory produced {addend1} items last month and {addend2} this month. What is the total?",
                    f"A town has {addend1} residents. {addend2} more people moved in. How many residents now?",
                ]
                problem_text = random.choice(contexts)
                correct_answer = self._calculate_correct(addend1, addend2)
                malrule_answer = self._calculate_malrule(addend1, addend2)

                return Problem(
                    text=problem_text,
                    operands=[addend1, addend2],
                    operation='addition',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'has_carry': True,
                        'problem_type': 'four_digit',
                        'template': 'four_digit',
                        'correct_answer': str(correct_answer),
                        'malrule_answer': str(malrule_answer)
                    }
                )

        addend1 = random.randint(min_val, max_val)
        addend2 = random.randint(min_val, max_val)
        problem_text = f"What is {addend1} + {addend2}?"
        correct_answer = self._calculate_correct(addend1, addend2)
        malrule_answer = self._calculate_malrule(addend1, addend2)

        return Problem(
            text=problem_text,
            operands=[addend1, addend2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'has_carry': self._has_carry_opportunity(addend1, addend2),
                'problem_type': 'four_digit',
                'template': 'four_digit',
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer)
            }
        )

    def _generate_word_problem_result_unknown(self, seed: Optional[int] = None) -> Problem:
        """Template 6: Word problems with result unknown."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['addend1']

        for _ in range(100):
            addend1 = random.randint(min_val, max_val)
            addend2 = random.randint(min_val, max_val)

            if self._has_carry_opportunity(addend1, addend2):
                contexts = [
                    f"Emma collected {addend1} trading cards. She got {addend2} more. How many cards does she have now?",
                    f"A library had {addend1} books. They received {addend2} new books. How many books are there now?",
                    f"There were {addend1} students in the morning. {addend2} more arrived. How many students are there now?",
                ]
                problem_text = random.choice(contexts)
                correct_answer = self._calculate_correct(addend1, addend2)
                malrule_answer = self._calculate_malrule(addend1, addend2)

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
                        'malrule_answer': str(malrule_answer)
                    }
                )

        addend1 = random.randint(min_val, max_val)
        addend2 = random.randint(min_val, max_val)
        problem_text = f"There were {addend1} items. {addend2} more were added. How many total?"
        correct_answer = self._calculate_correct(addend1, addend2)
        malrule_answer = self._calculate_malrule(addend1, addend2)

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
                'malrule_answer': str(malrule_answer)
            }
        )

    def _generate_word_problem_combining(self, seed: Optional[int] = None) -> Problem:
        """Template 7: Word problems combining two groups."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['addend1']

        for _ in range(100):
            addend1 = random.randint(min_val, max_val)
            addend2 = random.randint(min_val, max_val)

            if self._has_carry_opportunity(addend1, addend2):
                contexts = [
                    f"Team A has {addend1} members and Team B has {addend2} members. How many members in total?",
                    f"A bakery made {addend1} muffins and {addend2} cookies. How many items did they make?",
                    f"Box A contains {addend1} items and Box B contains {addend2} items. How many items in both boxes?",
                ]
                problem_text = random.choice(contexts)
                correct_answer = self._calculate_correct(addend1, addend2)
                malrule_answer = self._calculate_malrule(addend1, addend2)

                return Problem(
                    text=problem_text,
                    operands=[addend1, addend2],
                    operation='addition',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'has_carry': True,
                        'problem_type': 'word_problem_combining',
                        'template': 'word_problem_combining',
                        'formula_type': 'combining',
                        'correct_answer': str(correct_answer),
                        'malrule_answer': str(malrule_answer)
                    }
                )

        addend1 = random.randint(min_val, max_val)
        addend2 = random.randint(min_val, max_val)
        problem_text = f"Group A has {addend1} and Group B has {addend2}. What is the total?"
        correct_answer = self._calculate_correct(addend1, addend2)
        malrule_answer = self._calculate_malrule(addend1, addend2)

        return Problem(
            text=problem_text,
            operands=[addend1, addend2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'has_carry': self._has_carry_opportunity(addend1, addend2),
                'problem_type': 'word_problem_combining',
                'template': 'word_problem_combining',
                'formula_type': 'combining',
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer)
            }
        )

    def _generate_word_problem_comparison(self, seed: Optional[int] = None) -> Problem:
        """Template 8: Word problems with comparison (find total from parts)."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['addend1']

        for _ in range(100):
            addend1 = random.randint(min_val, max_val)
            addend2 = random.randint(min_val, max_val)

            if self._has_carry_opportunity(addend1, addend2):
                contexts = [
                    f"Anna read {addend1} pages on Monday and {addend2} pages on Tuesday. How many pages did she read in total?",
                    f"A store sold {addend1} items in the morning and {addend2} in the afternoon. What is the total sales?",
                    f"John walked {addend1} steps before lunch and {addend2} steps after lunch. How many steps total?",
                ]
                problem_text = random.choice(contexts)
                correct_answer = self._calculate_correct(addend1, addend2)
                malrule_answer = self._calculate_malrule(addend1, addend2)

                return Problem(
                    text=problem_text,
                    operands=[addend1, addend2],
                    operation='addition',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'has_carry': True,
                        'problem_type': 'word_problem_comparison',
                        'template': 'word_problem_comparison',
                        'formula_type': 'comparison',
                        'correct_answer': str(correct_answer),
                        'malrule_answer': str(malrule_answer)
                    }
                )

        addend1 = random.randint(min_val, max_val)
        addend2 = random.randint(min_val, max_val)
        problem_text = f"First part: {addend1}, second part: {addend2}. What is the total?"
        correct_answer = self._calculate_correct(addend1, addend2)
        malrule_answer = self._calculate_malrule(addend1, addend2)

        return Problem(
            text=problem_text,
            operands=[addend1, addend2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'has_carry': self._has_carry_opportunity(addend1, addend2),
                'problem_type': 'word_problem_comparison',
                'template': 'word_problem_comparison',
                'formula_type': 'comparison',
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer)
            }
        )
