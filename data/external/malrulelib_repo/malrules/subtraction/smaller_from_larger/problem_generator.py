"""
Problem generator for Smaller-From-Larger malrule.

Generates multi-digit subtraction problems where the malrule will produce
different answers than the correct algorithm.
"""

import random
from typing import Dict, Tuple, Optional, List
import sys
sys.path.append('/home/user/malrule-coding')

from utils import Problem, ProblemGenerator, DifficultyLevel, create_basic_arithmetic_template


class SmallerFromLargerProblemGenerator(ProblemGenerator):
    """
    Generates subtraction problems where digits in subtrahend are sometimes
    larger than corresponding digits in minuend, making the Smaller-From-Larger
    malrule produce incorrect answers.
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
        return {'minuend': ranges[lvl][self.difficulty],
                'subtrahend': ranges[lvl][self.difficulty]}

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_subtraction',
            'money_context',
            'measurement_context',
            'three_digit',
            'four_digit',
            'missing_minuend',
            'missing_subtrahend',
            'comparison',
            'multi_step',
            'word_problem_result_unknown',
            'word_problem_missing_minuend',
            'word_problem_missing_subtrahend',
            'word_problem_comparison'
        ]

    def _has_smaller_from_larger_opportunity(self, minuend: int, subtrahend: int) -> bool:
        """
        Check if problem has at least one column where subtrahend digit > minuend digit.
        This is where the Smaller-From-Larger malrule will produce wrong answer.

        Args:
            minuend: Top number
            subtrahend: Bottom number

        Returns:
            True if at least one column has subtrahend digit > minuend digit
        """
        if minuend <= subtrahend:
            return False

        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend).zfill(len(minuend_str))

        # Check if any digit in subtrahend is larger than corresponding minuend digit
        for m_digit, s_digit in zip(minuend_str, subtrahend_str):
            if int(s_digit) > int(m_digit):
                return True

        return False

    def _generate_problem_text(self, minuend: int, subtrahend: int, problem_type: str) -> str:
        """
        Generate problem text based on problem type.

        Args:
            minuend: Top number
            subtrahend: Bottom number
            problem_type: Type of problem context

        Returns:
            Formatted problem text
        """
        if problem_type == 'basic':
            template = create_basic_arithmetic_template('subtraction')
            return template.generate({'a': minuend, 'b': subtrahend})

        elif problem_type == 'money':
            contexts = [
                f"Sarah had ${minuend}. She spent ${subtrahend} on books. How much money does she have left?",
                f"A store had ${minuend} in the cash register. After a purchase of ${subtrahend}, how much is left?",
                f"Tom saved ${minuend} and then spent ${subtrahend} on a new game. How much money does he have now?",
                f"Maria earned ${minuend} from her job. She paid ${subtrahend} for rent. How much does she have remaining?",
                f"A restaurant earned ${minuend} on Friday and spent ${subtrahend} on supplies. What is the remaining amount?",
                f"Jake had ${minuend} in his bank account. He withdrew ${subtrahend}. What is his new balance?",
            ]
            return random.choice(contexts)

        elif problem_type == 'measurement':
            # Use appropriate units based on magnitude
            if minuend < 100:
                units = [
                    ('inches', 'ribbon', 'cut off'),
                    ('centimeters', 'rope', 'used'),
                    ('feet', 'wood', 'cut away'),
                ]
            else:
                units = [
                    ('meters', 'fabric', 'sold'),
                    ('feet', 'cable', 'used'),
                    ('yards', 'rope', 'cut'),
                    ('kilometers', 'road', 'completed'),
                    ('miles', 'trip', 'already traveled'),
                ]

            unit, item, action = random.choice(units)

            contexts = [
                f"A piece of {item} was {minuend} {unit} long. After {subtrahend} {unit} was {action}, how much {item} remained?",
                f"The total length of the {item} is {minuend} {unit}. If {subtrahend} {unit} is {action}, what length is left?",
                f"Lisa measured {minuend} {unit} of {item}. She {action} {subtrahend} {unit}. How much remains?",
                f"A builder had {minuend} {unit} of {item}. After using {subtrahend} {unit}, how much is left?",
            ]
            return random.choice(contexts)

        elif problem_type == 'three_digit':
            # Emphasize 3-digit problems with specific contexts
            contexts = [
                f"What is {minuend} - {subtrahend}?",
                f"Calculate: {minuend} - {subtrahend}",
                f"Subtract {subtrahend} from {minuend}.",
                f"Find the difference between {minuend} and {subtrahend}.",
                f"A school has {minuend} students. If {subtrahend} students are absent, how many are present?",
                f"A library had {minuend} books. After lending out {subtrahend} books, how many remain?",
            ]
            return random.choice(contexts)

        else:
            # Default to basic
            template = create_basic_arithmetic_template('subtraction')
            return template.generate({'a': minuend, 'b': subtrahend})

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate a subtraction problem where Smaller-From-Larger will fail.

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
        if template == 'basic_subtraction':
            return self._generate_basic_subtraction(seed)
        elif template == 'money_context':
            return self._generate_money_context(seed)
        elif template == 'measurement_context':
            return self._generate_measurement_context(seed)
        elif template == 'three_digit':
            return self._generate_three_digit(seed)
        elif template == 'four_digit':
            return self._generate_four_digit(seed)
        elif template == 'missing_minuend':
            return self._generate_missing_minuend(seed)
        elif template == 'missing_subtrahend':
            return self._generate_missing_subtrahend(seed)
        elif template == 'comparison':
            return self._generate_comparison(seed)
        elif template == 'multi_step':
            return self._generate_multi_step(seed)
        elif template == 'word_problem_result_unknown':
            return self._generate_word_problem_result_unknown(seed)
        elif template == 'word_problem_missing_minuend':
            return self._generate_word_problem_missing_minuend(seed)
        elif template == 'word_problem_missing_subtrahend':
            return self._generate_word_problem_missing_subtrahend(seed)
        elif template == 'word_problem_comparison':
            return self._generate_word_problem_comparison(seed)
        else:
            # Fallback for backwards compatibility
            ranges = self.get_value_ranges()
            min_val, max_val = ranges['minuend']

            # Choose problem type - weighted to include new templates
            problem_types = ['basic', 'money', 'measurement', 'three_digit']
            # For level 3+, emphasize three_digit problems
            if self.level >= 3:
                problem_types.extend(['three_digit', 'money', 'measurement'])

            problem_type = random.choice(problem_types)

        # Try to generate a problem with smaller-from-larger opportunity
        max_attempts = 100
        for _ in range(max_attempts):
            minuend = random.randint(min_val, max_val)

            # Subtrahend should be smaller but create opportunities for error
            subtrahend_min = max(min_val // 2, 1)
            subtrahend_max = minuend - 1

            if subtrahend_max <= subtrahend_min:
                continue

            subtrahend = random.randint(subtrahend_min, subtrahend_max)

            if self._has_smaller_from_larger_opportunity(minuend, subtrahend):
                # Create problem text based on type
                problem_text = self._generate_problem_text(minuend, subtrahend, problem_type)

                return Problem(
                    text=problem_text,
                    operands=[minuend, subtrahend],
                    operation='subtraction',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'has_smaller_from_larger': True,
                        'problem_type': problem_type
                    }
                )

        # Fallback: generate any valid subtraction problem
        minuend = random.randint(min_val, max_val)
        subtrahend = random.randint(min_val // 2, minuend - 1)

        problem_text = self._generate_problem_text(minuend, subtrahend, problem_type)

        return Problem(
            text=problem_text,
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'has_smaller_from_larger': self._has_smaller_from_larger_opportunity(minuend, subtrahend),
                'problem_type': problem_type
            }
        )

    def _generate_basic_subtraction(self, seed: Optional[int] = None) -> Problem:
        """Template 1: Basic subtraction problems (2-digit)."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['minuend']

        # Try to generate a problem with smaller-from-larger opportunity
        for _ in range(100):
            minuend = random.randint(min_val, max_val)
            subtrahend = random.randint(min_val // 2, minuend - 1)

            if self._has_smaller_from_larger_opportunity(minuend, subtrahend):
                problem_text = self._generate_problem_text(minuend, subtrahend, 'basic')

                return Problem(
                    text=problem_text,
                    operands=[minuend, subtrahend],
                    operation='subtraction',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'has_smaller_from_larger': True,
                        'problem_type': 'basic',
                        'template': 'basic_subtraction'
                    }
                )

        # Fallback
        minuend = random.randint(min_val, max_val)
        subtrahend = random.randint(min_val // 2, minuend - 1)
        problem_text = self._generate_problem_text(minuend, subtrahend, 'basic')

        return Problem(
            text=problem_text,
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'has_smaller_from_larger': self._has_smaller_from_larger_opportunity(minuend, subtrahend),
                'problem_type': 'basic',
                'template': 'basic_subtraction'
            }
        )

    def _generate_money_context(self, seed: Optional[int] = None) -> Problem:
        """Template 2: Money word problems."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['minuend']

        for _ in range(100):
            minuend = random.randint(min_val, max_val)
            subtrahend = random.randint(min_val // 2, minuend - 1)

            if self._has_smaller_from_larger_opportunity(minuend, subtrahend):
                problem_text = self._generate_problem_text(minuend, subtrahend, 'money')

                return Problem(
                    text=problem_text,
                    operands=[minuend, subtrahend],
                    operation='subtraction',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'has_smaller_from_larger': True,
                        'problem_type': 'money',
                        'template': 'money_context'
                    }
                )

        minuend = random.randint(min_val, max_val)
        subtrahend = random.randint(min_val // 2, minuend - 1)
        problem_text = self._generate_problem_text(minuend, subtrahend, 'money')

        return Problem(
            text=problem_text,
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'has_smaller_from_larger': self._has_smaller_from_larger_opportunity(minuend, subtrahend),
                'problem_type': 'money',
                'template': 'money_context'
            }
        )

    def _generate_measurement_context(self, seed: Optional[int] = None) -> Problem:
        """Template 3: Measurement word problems."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['minuend']

        for _ in range(100):
            minuend = random.randint(min_val, max_val)
            subtrahend = random.randint(min_val // 2, minuend - 1)

            if self._has_smaller_from_larger_opportunity(minuend, subtrahend):
                problem_text = self._generate_problem_text(minuend, subtrahend, 'measurement')

                return Problem(
                    text=problem_text,
                    operands=[minuend, subtrahend],
                    operation='subtraction',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'has_smaller_from_larger': True,
                        'problem_type': 'measurement',
                        'template': 'measurement_context'
                    }
                )

        minuend = random.randint(min_val, max_val)
        subtrahend = random.randint(min_val // 2, minuend - 1)
        problem_text = self._generate_problem_text(minuend, subtrahend, 'measurement')

        return Problem(
            text=problem_text,
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'has_smaller_from_larger': self._has_smaller_from_larger_opportunity(minuend, subtrahend),
                'problem_type': 'measurement',
                'template': 'measurement_context'
            }
        )

    def _generate_three_digit(self, seed: Optional[int] = None) -> Problem:
        """Template 4: Three-digit subtraction problems."""
        if seed is not None:
            random.seed(seed)

        # Force 3-digit range
        min_val, max_val = 100, 999

        for _ in range(100):
            minuend = random.randint(min_val, max_val)
            subtrahend = random.randint(min_val // 2, minuend - 1)

            if self._has_smaller_from_larger_opportunity(minuend, subtrahend):
                problem_text = self._generate_problem_text(minuend, subtrahend, 'three_digit')

                return Problem(
                    text=problem_text,
                    operands=[minuend, subtrahend],
                    operation='subtraction',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'has_smaller_from_larger': True,
                        'problem_type': 'three_digit',
                        'template': 'three_digit'
                    }
                )

        minuend = random.randint(min_val, max_val)
        subtrahend = random.randint(min_val // 2, minuend - 1)
        problem_text = self._generate_problem_text(minuend, subtrahend, 'three_digit')

        return Problem(
            text=problem_text,
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'has_smaller_from_larger': self._has_smaller_from_larger_opportunity(minuend, subtrahend),
                'problem_type': 'three_digit',
                'template': 'three_digit'
            }
        )

    def _generate_four_digit(self, seed: Optional[int] = None) -> Problem:
        """Template 5: Four-digit subtraction problems (NEW)."""
        if seed is not None:
            random.seed(seed)

        # Force 4-digit range
        min_val, max_val = 1000, 9999

        for _ in range(100):
            minuend = random.randint(min_val, max_val)
            subtrahend = random.randint(min_val // 2, minuend - 1)

            if self._has_smaller_from_larger_opportunity(minuend, subtrahend):
                # Use similar contexts as three_digit
                contexts = [
                    f"What is {minuend} - {subtrahend}?",
                    f"Calculate: {minuend} - {subtrahend}",
                    f"Subtract {subtrahend} from {minuend}.",
                    f"A factory produced {minuend} items. If {subtrahend} items were sold, how many remain?",
                    f"A town has {minuend} residents. After {subtrahend} people moved away, how many remain?",
                    f"A stadium holds {minuend} people. If {subtrahend} seats are empty, how many are filled?",
                ]
                problem_text = random.choice(contexts)

                return Problem(
                    text=problem_text,
                    operands=[minuend, subtrahend],
                    operation='subtraction',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'has_smaller_from_larger': True,
                        'problem_type': 'four_digit',
                        'template': 'four_digit'
                    }
                )

        minuend = random.randint(min_val, max_val)
        subtrahend = random.randint(min_val // 2, minuend - 1)
        contexts = [
            f"What is {minuend} - {subtrahend}?",
            f"Calculate: {minuend} - {subtrahend}",
            f"Subtract {subtrahend} from {minuend}.",
        ]
        problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'has_smaller_from_larger': self._has_smaller_from_larger_opportunity(minuend, subtrahend),
                'problem_type': 'four_digit',
                'template': 'four_digit'
            }
        )

    def _generate_missing_minuend(self, seed: Optional[int] = None) -> Problem:
        """Template 6: Missing minuend problems (? - b = c)."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['minuend']

        for _ in range(100):
            result = random.randint(min_val // 2, max_val // 2)
            subtrahend = random.randint(min_val // 4, result)
            minuend = result + subtrahend

            if self._has_smaller_from_larger_opportunity(minuend, subtrahend):
                contexts = [
                    f"Some students were in the library. {subtrahend} students left. Now there are {result} students. How many students were there initially?",
                    f"Maria had some stickers. She gave {subtrahend} to her friend. Now she has {result} stickers. How many did she start with?",
                    f"A store had some apples. After selling {subtrahend} apples, there are {result} left. How many apples were there originally?"
                ]
                problem_text = random.choice(contexts)

                return Problem(
                    text=problem_text,
                    operands=[minuend, subtrahend],
                    operation='subtraction',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'has_smaller_from_larger': True,
                        'problem_type': 'missing_minuend',
                        'template': 'missing_minuend',
                        'formula_type': 'missing_minuend',
                        'expected_answer': minuend
                    }
                )

        # Fallback
        result = random.randint(min_val // 2, max_val // 2)
        subtrahend = random.randint(min_val // 4, result)
        minuend = result + subtrahend
        problem_text = f"Some items were in a box. {subtrahend} were removed. Now there are {result}. How many were there initially?"

        return Problem(
            text=problem_text,
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'has_smaller_from_larger': self._has_smaller_from_larger_opportunity(minuend, subtrahend),
                'problem_type': 'missing_minuend',
                'template': 'missing_minuend',
                'formula_type': 'missing_minuend',
                'expected_answer': minuend
            }
        )

    def _generate_missing_subtrahend(self, seed: Optional[int] = None) -> Problem:
        """Template 7: Missing subtrahend problems (a - ? = c)."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['minuend']

        for _ in range(100):
            minuend = random.randint(min_val, max_val)
            result = random.randint(min_val // 2, minuend - 1)
            subtrahend = minuend - result

            if self._has_smaller_from_larger_opportunity(minuend, subtrahend):
                contexts = [
                    f"John had {minuend} coins. After giving some to his brother, he has {result} left. How many did he give away?",
                    f"A library had {minuend} books. After lending some out, {result} books remain. How many books were lent?",
                    f"Sarah collected {minuend} stickers. She gave some to friends and now has {result}. How many did she give away?"
                ]
                problem_text = random.choice(contexts)

                return Problem(
                    text=problem_text,
                    operands=[minuend, subtrahend],
                    operation='subtraction',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'has_smaller_from_larger': True,
                        'problem_type': 'missing_subtrahend',
                        'template': 'missing_subtrahend',
                        'formula_type': 'missing_subtrahend',
                        'expected_answer': subtrahend
                    }
                )

        # Fallback
        minuend = random.randint(min_val, max_val)
        result = random.randint(min_val // 2, minuend - 1)
        subtrahend = minuend - result
        problem_text = f"There were {minuend} items. After removing some, {result} remain. How many were removed?"

        return Problem(
            text=problem_text,
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'has_smaller_from_larger': self._has_smaller_from_larger_opportunity(minuend, subtrahend),
                'problem_type': 'missing_subtrahend',
                'template': 'missing_subtrahend',
                'formula_type': 'missing_subtrahend',
                'expected_answer': subtrahend
            }
        )

    def _generate_comparison(self, seed: Optional[int] = None) -> Problem:
        """Template 8: Comparison problems (difference/how many more)."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['minuend']

        for _ in range(100):
            minuend = random.randint(min_val, max_val)
            subtrahend = random.randint(min_val // 2, minuend - 1)

            if self._has_smaller_from_larger_opportunity(minuend, subtrahend):
                contexts = [
                    f"Tom has {minuend} marbles and Sarah has {subtrahend} marbles. How many more marbles does Tom have than Sarah?",
                    f"A red box contains {minuend} items and a blue box contains {subtrahend} items. What is the difference?",
                    f"School A has {minuend} students and School B has {subtrahend} students. How many more students does School A have?"
                ]
                problem_text = random.choice(contexts)

                return Problem(
                    text=problem_text,
                    operands=[minuend, subtrahend],
                    operation='subtraction',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'has_smaller_from_larger': True,
                        'problem_type': 'comparison',
                        'template': 'comparison',
                        'formula_type': 'comparison',
                        'expected_answer': minuend - subtrahend
                    }
                )

        # Fallback
        minuend = random.randint(min_val, max_val)
        subtrahend = random.randint(min_val // 2, minuend - 1)
        problem_text = f"Set A has {minuend} items and Set B has {subtrahend} items. What is the difference?"

        return Problem(
            text=problem_text,
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'has_smaller_from_larger': self._has_smaller_from_larger_opportunity(minuend, subtrahend),
                'problem_type': 'comparison',
                'template': 'comparison',
                'formula_type': 'comparison',
                'expected_answer': minuend - subtrahend
            }
        )

    def _generate_multi_step(self, seed: Optional[int] = None) -> Problem:
        """Template 9: Multi-step problems (a - b - c)."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['minuend']

        for _ in range(100):
            minuend = random.randint(min_val, max_val)
            subtrahend1 = random.randint(min_val // 4, minuend // 3)
            subtrahend2 = random.randint(min_val // 4, (minuend - subtrahend1) // 2)

            if self._has_smaller_from_larger_opportunity(minuend, subtrahend1):
                contexts = [
                    f"Alex had {minuend} cards. He gave {subtrahend1} to his friend and {subtrahend2} to his sister. How many cards does he have left?",
                    f"A store had {minuend} books. They sold {subtrahend1} in the morning and {subtrahend2} in the afternoon. How many books remain?",
                    f"Maria saved ${minuend}. She spent ${subtrahend1} on Monday and ${subtrahend2} on Tuesday. How much money does she have left?"
                ]
                problem_text = random.choice(contexts)

                # Store both steps as operands
                return Problem(
                    text=problem_text,
                    operands=[minuend, subtrahend1, subtrahend2],
                    operation='subtraction',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'has_smaller_from_larger': True,
                        'problem_type': 'multi_step',
                        'template': 'multi_step',
                        'formula_type': 'multi_step',
                        'expected_answer': minuend - subtrahend1 - subtrahend2
                    }
                )

        # Fallback
        minuend = random.randint(min_val, max_val)
        subtrahend1 = random.randint(min_val // 4, minuend // 3)
        subtrahend2 = random.randint(min_val // 4, (minuend - subtrahend1) // 2)
        problem_text = f"There were {minuend} items. {subtrahend1} were removed, then {subtrahend2} more. How many remain?"

        return Problem(
            text=problem_text,
            operands=[minuend, subtrahend1, subtrahend2],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'has_smaller_from_larger': self._has_smaller_from_larger_opportunity(minuend, subtrahend1),
                'problem_type': 'multi_step',
                'template': 'multi_step',
                'formula_type': 'multi_step',
                'expected_answer': minuend - subtrahend1 - subtrahend2
            }
        )

    def _generate_word_problem_result_unknown(self, seed: Optional[int] = None) -> Problem:
        """Template 10: Word problems with result unknown (enhanced contexts)."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['minuend']

        for _ in range(100):
            minuend = random.randint(min_val, max_val)
            subtrahend = random.randint(min_val // 2, minuend - 1)

            if self._has_smaller_from_larger_opportunity(minuend, subtrahend):
                # 3 contexts per formula type
                context_sets = [
                    # Collections
                    f"Emma collected {minuend} trading cards. She traded away {subtrahend} cards. How many cards does she have now?",
                    # Time
                    f"A movie theater had {minuend} seats. {subtrahend} seats were occupied. How many seats are empty?",
                    # Groups
                    f"There were {minuend} students in the cafeteria. {subtrahend} students left to go outside. How many students remain in the cafeteria?"
                ]
                problem_text = random.choice(context_sets)

                return Problem(
                    text=problem_text,
                    operands=[minuend, subtrahend],
                    operation='subtraction',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'has_smaller_from_larger': True,
                        'problem_type': 'word_problem_result_unknown',
                        'template': 'word_problem_result_unknown',
                        'formula_type': 'result_unknown',
                        'expected_answer': minuend - subtrahend
                    }
                )

        # Fallback
        minuend = random.randint(min_val, max_val)
        subtrahend = random.randint(min_val // 2, minuend - 1)
        problem_text = f"There were {minuend} items. {subtrahend} were taken. How many remain?"

        return Problem(
            text=problem_text,
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'has_smaller_from_larger': self._has_smaller_from_larger_opportunity(minuend, subtrahend),
                'problem_type': 'word_problem_result_unknown',
                'template': 'word_problem_result_unknown',
                'formula_type': 'result_unknown',
                'expected_answer': minuend - subtrahend
            }
        )

    def _generate_word_problem_missing_minuend(self, seed: Optional[int] = None) -> Problem:
        """Template 11: Word problems with missing minuend (enhanced contexts)."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['minuend']

        for _ in range(100):
            result = random.randint(min_val // 2, max_val // 2)
            subtrahend = random.randint(min_val // 4, result)
            minuend = result + subtrahend

            if self._has_smaller_from_larger_opportunity(minuend, subtrahend):
                contexts = [
                    f"After spending ${subtrahend}, Jake has ${result} left. How much money did he have initially?",
                    f"A tree was cut by {subtrahend} cm. It is now {result} cm tall. What was its original height?",
                    f"Some birds were on a wire. {subtrahend} flew away, leaving {result} birds. How many birds were there at first?"
                ]
                problem_text = random.choice(contexts)

                return Problem(
                    text=problem_text,
                    operands=[minuend, subtrahend],
                    operation='subtraction',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'has_smaller_from_larger': True,
                        'problem_type': 'word_problem_missing_minuend',
                        'template': 'word_problem_missing_minuend',
                        'formula_type': 'missing_minuend',
                        'expected_answer': minuend
                    }
                )

        # Fallback
        result = random.randint(min_val // 2, max_val // 2)
        subtrahend = random.randint(min_val // 4, result)
        minuend = result + subtrahend
        problem_text = f"After removing {subtrahend}, there are {result} left. How many were there initially?"

        return Problem(
            text=problem_text,
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'has_smaller_from_larger': self._has_smaller_from_larger_opportunity(minuend, subtrahend),
                'problem_type': 'word_problem_missing_minuend',
                'template': 'word_problem_missing_minuend',
                'formula_type': 'missing_minuend',
                'expected_answer': minuend
            }
        )

    def _generate_word_problem_missing_subtrahend(self, seed: Optional[int] = None) -> Problem:
        """Template 12: Word problems with missing subtrahend (enhanced contexts)."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['minuend']

        for _ in range(100):
            minuend = random.randint(min_val, max_val)
            result = random.randint(min_val // 2, minuend - 1)
            subtrahend = minuend - result

            if self._has_smaller_from_larger_opportunity(minuend, subtrahend):
                contexts = [
                    f"A tank had {minuend} liters of water. After some leaked out, {result} liters remain. How many liters leaked?",
                    f"Ben had {minuend} points in a game. After losing some points, he has {result} now. How many points did he lose?",
                    f"A rope was {minuend} meters long. After cutting a piece off, it is {result} meters. How long was the piece cut off?"
                ]
                problem_text = random.choice(contexts)

                return Problem(
                    text=problem_text,
                    operands=[minuend, subtrahend],
                    operation='subtraction',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'has_smaller_from_larger': True,
                        'problem_type': 'word_problem_missing_subtrahend',
                        'template': 'word_problem_missing_subtrahend',
                        'formula_type': 'missing_subtrahend',
                        'expected_answer': subtrahend
                    }
                )

        # Fallback
        minuend = random.randint(min_val, max_val)
        result = random.randint(min_val // 2, minuend - 1)
        subtrahend = minuend - result
        problem_text = f"Started with {minuend}, now have {result}. How many were removed?"

        return Problem(
            text=problem_text,
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'has_smaller_from_larger': self._has_smaller_from_larger_opportunity(minuend, subtrahend),
                'problem_type': 'word_problem_missing_subtrahend',
                'template': 'word_problem_missing_subtrahend',
                'formula_type': 'missing_subtrahend',
                'expected_answer': subtrahend
            }
        )

    def _generate_word_problem_comparison(self, seed: Optional[int] = None) -> Problem:
        """Template 13: Word problems with comparison (enhanced contexts)."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        min_val, max_val = ranges['minuend']

        for _ in range(100):
            minuend = random.randint(min_val, max_val)
            subtrahend = random.randint(min_val // 2, minuend - 1)

            if self._has_smaller_from_larger_opportunity(minuend, subtrahend):
                contexts = [
                    f"Anna scored {minuend} points and Ben scored {subtrahend} points. How many more points did Anna score?",
                    f"The red team has {minuend} members and the blue team has {subtrahend} members. How many fewer members does the blue team have?",
                    f"Building A is {minuend} feet tall and Building B is {subtrahend} feet tall. What is the difference in height?"
                ]
                problem_text = random.choice(contexts)

                return Problem(
                    text=problem_text,
                    operands=[minuend, subtrahend],
                    operation='subtraction',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'has_smaller_from_larger': True,
                        'problem_type': 'word_problem_comparison',
                        'template': 'word_problem_comparison',
                        'formula_type': 'comparison',
                        'expected_answer': minuend - subtrahend
                    }
                )

        # Fallback
        minuend = random.randint(min_val, max_val)
        subtrahend = random.randint(min_val // 2, minuend - 1)
        problem_text = f"Group A has {minuend} and Group B has {subtrahend}. What is the difference?"

        return Problem(
            text=problem_text,
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'has_smaller_from_larger': self._has_smaller_from_larger_opportunity(minuend, subtrahend),
                'problem_type': 'word_problem_comparison',
                'template': 'word_problem_comparison',
                'formula_type': 'comparison',
                'expected_answer': minuend - subtrahend
            }
        )
