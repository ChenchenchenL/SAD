"""
Problem generator for Borrow-From-Bottom malrule.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, List, Optional
from utils import ProblemGenerator, Problem, DifficultyLevel


class BorrowFromBottomProblemGenerator(ProblemGenerator):
    """Generates subtraction problems requiring borrowing."""

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_subtraction',
            'word_problem_context',
            'multi_step_problem',
            'missing_number',
            'comparison_problem'
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        ranges = {
            2: {DifficultyLevel.EASY: (20, 50), DifficultyLevel.MEDIUM: (30, 70), DifficultyLevel.HARD: (50, 99)},
            3: {DifficultyLevel.EASY: (30, 70), DifficultyLevel.MEDIUM: (50, 99), DifficultyLevel.HARD: (100, 200)},
            4: {DifficultyLevel.EASY: (50, 99), DifficultyLevel.MEDIUM: (100, 300), DifficultyLevel.HARD: (200, 500)},
        }
        lvl = self.level if self.level in ranges else 3
        return {'minuend': ranges[lvl][self.difficulty]}

    def generate(self, seed=None, template: Optional[str] = None) -> Problem:
        """
        Generate a subtraction problem requiring borrowing.

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
        elif template == 'word_problem_context':
            return self._generate_word_problem_context(seed)
        elif template == 'multi_step_problem':
            return self._generate_multi_step_problem(seed)
        elif template == 'missing_number':
            return self._generate_missing_number(seed)
        elif template == 'comparison_problem':
            return self._generate_comparison_problem(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_subtraction(self, seed=None) -> Problem:
        """Template 1: Basic subtraction requiring borrowing."""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['minuend']

        # Generate problem requiring borrowing (ones_top < ones_bottom)
        attempts = 0
        while attempts < 100:
            minuend = random.randint(min_val, max_val)
            subtrahend = random.randint(min_val // 2, minuend - 1)

            min_str = str(minuend)
            sub_str = str(subtrahend).zfill(len(min_str))

            # Ensure borrowing is needed: ones digit of top < ones digit of bottom
            if int(min_str[-1]) < int(sub_str[-1]):
                break
            attempts += 1

        # Convert to digits for calculations
        min_digits = [int(d) for d in min_str]
        sub_digits = [int(d) for d in sub_str]

        # Correct answer
        correct_answer = minuend - subtrahend

        # Malrule answer: Student borrows from BOTTOM instead of top
        ones_result = (min_digits[-1] + 10) - sub_digits[-1]
        tens_top = min_digits[-2]
        tens_bottom = sub_digits[-2] - 1
        tens_result = tens_top - tens_bottom
        malrule_answer = tens_result * 10 + ones_result

        text = f"Calculate: {minuend} - {subtrahend}"

        return Problem(
            text=text,
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'minuend': minuend,
                'subtrahend': subtrahend,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'ones_top': min_digits[-1],
                'ones_bottom': sub_digits[-1],
                'tens_top': min_digits[-2],
                'tens_bottom': sub_digits[-2],
                'template': 'basic_subtraction'
            }
        )

    def _generate_word_problem_context(self, seed=None) -> Problem:
        """Template 2: Word problem with real-world context."""
        problem = self._generate_basic_subtraction(seed)

        contexts = [
            ("had ${minuend}", "spent ${subtrahend}", "dollars left"),
            ("collected {minuend} stamps", "gave away {subtrahend} stamps", "stamps remaining"),
            ("had {minuend} points", "lost {subtrahend} points", "points now"),
            ("has {minuend} pages", "read {subtrahend} pages", "pages to go"),
            ("baked {minuend} cookies", "sold {subtrahend} cookies", "cookies left")
        ]

        start_phrase, action_phrase, result_phrase = random.choice(contexts)
        minuend = problem.metadata['minuend']
        subtrahend = problem.metadata['subtrahend']

        problem.text = f"Sarah {start_phrase.format(minuend=minuend)} and {action_phrase.format(subtrahend=subtrahend)}. How many {result_phrase}?"
        problem.metadata['template'] = 'word_problem_context'
        return problem

    def _generate_multi_step_problem(self, seed=None) -> Problem:
        """Template 3: Multi-step subtraction problem."""
        if seed is not None:
            random.seed(seed)

        # Generate two subtraction problems
        problem1 = self._generate_basic_subtraction(seed)
        minuend1 = problem1.metadata['minuend']
        subtrahend1 = problem1.metadata['subtrahend']
        result1 = problem1.metadata['correct_answer']

        # Second subtraction uses result of first
        min_val, max_val = self.get_value_ranges()['minuend']
        # Ensure valid range for subtrahend2
        min_sub2 = max(10, min(min_val // 3, result1 - 5))
        max_sub2 = max(min_sub2 + 1, result1 - 1)
        attempts = 0
        while attempts < 100:
            subtrahend2 = random.randint(min_sub2, max_sub2)
            sub_str = str(subtrahend2).zfill(len(str(result1)))

            # Ensure borrowing is needed
            if int(str(result1)[-1]) < int(sub_str[-1]):
                break
            attempts += 1

        # Calculate final result
        correct_answer = result1 - subtrahend2

        # Malrule for second subtraction
        # Ensure both numbers are at least 2 digits for borrow-from-bottom calculation
        result1_str = str(result1).zfill(2)
        sub_str = str(subtrahend2).zfill(len(result1_str))

        result1_digits = [int(d) for d in result1_str]
        sub2_digits = [int(d) for d in sub_str]

        if result1_digits[-1] < sub2_digits[-1]:
            ones_result = (result1_digits[-1] + 10) - sub2_digits[-1]
            tens_result = result1_digits[-2] - (sub2_digits[-2] - 1)
            malrule_answer = tens_result * 10 + ones_result
        else:
            # No borrowing needed
            malrule_answer = result1 - subtrahend2

        problem1.text = f"Calculate: ({minuend1} - {subtrahend1}) - {subtrahend2}"
        problem1.metadata['correct_answer'] = correct_answer
        problem1.metadata['malrule_answer'] = malrule_answer
        problem1.metadata['template'] = 'multi_step_problem'
        return problem1

    def _generate_missing_number(self, seed=None) -> Problem:
        """Template 4: Find the missing number in subtraction."""
        problem = self._generate_basic_subtraction(seed)

        minuend = problem.metadata['minuend']
        subtrahend = problem.metadata['subtrahend']
        correct_answer = problem.metadata['correct_answer']

        # Ask for the missing subtrahend
        problem.text = f"What number makes this true? {minuend} - ___ = {correct_answer}"
        problem.metadata['correct_answer'] = subtrahend

        # Malrule: Student tries to subtract to find missing number but makes borrowing error
        # They compute minuend - correct_answer with borrow-from-bottom error
        min_digits = [int(d) for d in str(minuend)]
        result_digits = [int(d) for d in str(correct_answer).zfill(len(str(minuend)))]

        if min_digits[-1] < result_digits[-1]:
            ones_result = (min_digits[-1] + 10) - result_digits[-1]
            tens_result = min_digits[-2] - (result_digits[-2] - 1)
            malrule_answer = tens_result * 10 + ones_result
        else:
            malrule_answer = minuend - correct_answer

        problem.metadata['malrule_answer'] = malrule_answer
        problem.metadata['template'] = 'missing_number'
        return problem

    def _generate_comparison_problem(self, seed=None) -> Problem:
        """Template 5: Compare two subtraction results."""
        if seed is not None:
            random.seed(seed)

        problem1 = self._generate_basic_subtraction(seed)
        problem2 = self._generate_basic_subtraction(seed + 1 if seed else None)

        minuend1 = problem1.metadata['minuend']
        subtrahend1 = problem1.metadata['subtrahend']
        result1_correct = problem1.metadata['correct_answer']
        result1_malrule = problem1.metadata['malrule_answer']

        minuend2 = problem2.metadata['minuend']
        subtrahend2 = problem2.metadata['subtrahend']
        result2_correct = problem2.metadata['correct_answer']

        problem1.text = f"Which is greater: {minuend1} - {subtrahend1} or {minuend2} - {subtrahend2}?"

        if result1_correct > result2_correct:
            correct_answer = f"{minuend1} - {subtrahend1} is greater ({result1_correct} > {result2_correct})"
        elif result1_correct < result2_correct:
            correct_answer = f"{minuend2} - {subtrahend2} is greater ({result2_correct} > {result1_correct})"
        else:
            correct_answer = f"They are equal (both = {result1_correct})"

        # Malrule: Student uses incorrect result from first calculation
        if result1_malrule > result2_correct:
            malrule_answer = f"{minuend1} - {subtrahend1} is greater ({result1_malrule} > {result2_correct})"
        elif result1_malrule < result2_correct:
            malrule_answer = f"{minuend2} - {subtrahend2} is greater ({result2_correct} > {result1_malrule})"
        else:
            malrule_answer = f"They are equal (both = {result1_malrule})"

        problem1.metadata['correct_answer'] = correct_answer
        problem1.metadata['malrule_answer'] = malrule_answer
        problem1.metadata['template'] = 'comparison_problem'
        return problem1
