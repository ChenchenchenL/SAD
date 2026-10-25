"""
Problem generator for Count-All-Zeros-For-Exponent malrule.

Generates numbers requiring scientific notation conversion, especially
numbers with multiple zeros in different positions to elicit the misconception
of counting all zeros rather than counting decimal places moved.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional
from utils import ProblemGenerator, Problem, DifficultyLevel


class CountZerosProblemGenerator(ProblemGenerator):
    """
    Generates scientific notation problems to elicit Count-All-Zeros malrule.

    Focus on numbers with zeros in various positions (leading zeros in decimals,
    trailing zeros in whole numbers, zeros between significant digits) to test
    whether students understand that only decimal place movement matters, not
    total zero count.
    """

    def get_name(self) -> str:
        return "Count-All-Zeros-For-Exponent Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates numbers requiring conversion to scientific notation, "
            "with emphasis on numbers containing multiple zeros in different "
            "positions to test understanding of exponent determination."
        )

    def get_available_templates(self) -> list:
        """Return list of available template names."""
        return [
            'small_decimal_trailing_zero',
            'large_number_trailing_zeros',
            'word_problem_measurement',
            'comparison_verification',
            'mixed_zeros_decimal'
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level and difficulty."""
        # Return ranges for significant digits
        ranges = {
            6: {
                DifficultyLevel.EASY: (1, 9),        # Single significant digit
                DifficultyLevel.MEDIUM: (10, 99),    # Two significant digits
                DifficultyLevel.HARD: (100, 999),    # Three significant digits
            },
            7: {
                DifficultyLevel.EASY: (10, 99),
                DifficultyLevel.MEDIUM: (100, 999),
                DifficultyLevel.HARD: (1000, 9999),  # Four significant digits
            },
            8: {
                DifficultyLevel.EASY: (100, 999),
                DifficultyLevel.MEDIUM: (1000, 9999),
                DifficultyLevel.HARD: (10000, 99999),
            },
            9: {
                DifficultyLevel.EASY: (100, 999),
                DifficultyLevel.MEDIUM: (1000, 9999),
                DifficultyLevel.HARD: (10000, 99999),
            }
        }

        lvl = self.level if self.level in ranges else 7
        return {'significant': ranges[lvl][self.difficulty]}

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate a scientific notation conversion problem.

        Args:
            seed: Optional random seed for reproducibility
            template: Optional template name to use

        Returns:
            Problem instance
        """
        if seed is not None:
            random.seed(seed)

        # If template is specified, use it
        if template:
            if template == 'small_decimal_trailing_zero':
                return self._generate_small_decimal_trailing_zero(seed)
            elif template == 'large_number_trailing_zeros':
                return self._generate_large_number_trailing_zeros(seed)
            elif template == 'word_problem_measurement':
                return self._generate_word_problem_measurement(seed)
            elif template == 'comparison_verification':
                return self._generate_comparison_verification(seed)
            elif template == 'mixed_zeros_decimal':
                return self._generate_mixed_zeros_decimal(seed)
            else:
                raise ValueError(f"Unknown template: {template}")

        # Legacy: random problem generation for backwards compatibility
        min_val, max_val = self.get_value_ranges()['significant']

        # Choose problem type
        problem_types = [
            'small_decimal',      # 0.00450 (leading zeros + trailing zero)
            'large_number',       # 3000 (trailing zeros)
            'small_decimal_no_trailing',  # 0.0034 (only leading zeros)
            'decimal_with_internal',      # 0.00305 (zeros between digits)
        ]

        problem_type = random.choice(problem_types)

        if problem_type == 'small_decimal':
            # Generate something like 0.00450
            sig_digits = random.randint(min_val, max_val)
            num_leading_zeros = random.randint(2, 4)

            # Add a trailing zero sometimes for extra confusion
            if random.random() < 0.5:
                number = sig_digits / (10 ** (num_leading_zeros + len(str(sig_digits))))
                # Format to keep trailing zeros
                number_str = f"0.{'0' * num_leading_zeros}{sig_digits}"
            else:
                # Add trailing zero
                sig_with_trailing = sig_digits * 10
                number = sig_with_trailing / (10 ** (num_leading_zeros + len(str(sig_with_trailing))))
                number_str = f"0.{'0' * num_leading_zeros}{sig_with_trailing}"

            # Count total zeros for metadata
            total_zeros = number_str.count('0')

        elif problem_type == 'large_number':
            # Generate something like 3000
            sig_digits = random.randint(max(1, min_val // 100), max(9, max_val // 100))
            num_trailing_zeros = random.randint(2, 4)
            number = sig_digits * (10 ** num_trailing_zeros)
            number_str = str(number)
            total_zeros = number_str.count('0')

        elif problem_type == 'small_decimal_no_trailing':
            # Generate something like 0.0034
            sig_digits = random.randint(min_val, max_val)
            num_leading_zeros = random.randint(2, 4)
            number = sig_digits / (10 ** (num_leading_zeros + len(str(sig_digits))))
            number_str = f"0.{'0' * num_leading_zeros}{sig_digits}"
            total_zeros = number_str.count('0')

        else:  # decimal_with_internal
            # Generate something like 0.00305 (zero between significant digits)
            # Create a number with internal zero
            first_digit = random.randint(1, 9)
            last_digit = random.randint(1, 9)
            sig_with_internal = int(f"{first_digit}0{last_digit}")
            num_leading_zeros = random.randint(2, 4)
            number = sig_with_internal / (10 ** (num_leading_zeros + len(str(sig_with_internal))))
            number_str = f"0.{'0' * num_leading_zeros}{sig_with_internal}"
            total_zeros = number_str.count('0')

        # Create problem text
        problem_texts = [
            f"Write {number_str} in scientific notation.",
            f"Express {number_str} in scientific notation.",
            f"Convert {number_str} to scientific notation.",
            f"What is {number_str} in scientific notation?"
        ]
        problem_text = random.choice(problem_texts)

        return Problem(
            text=problem_text,
            operands=[number_str],  # Store as string to preserve format
            operation='scientific_notation_conversion',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'number_string': number_str,
                'problem_type': problem_type,
                'total_zeros': total_zeros
            }
        )

    def _generate_small_decimal_trailing_zero(self, seed: Optional[int] = None) -> Problem:
        """
        Template 1: Small decimal with trailing zero.
        Example: 0.00450
        Correct: 4.5 × 10^-3 (moved 3 places)
        Malrule: 4.5 × 10^-4 (counts 4 zeros)
        """
        if seed is not None:
            random.seed(seed)

        # Generate a small decimal with leading zeros and a trailing zero
        # Example: 0.00450, 0.00780, 0.000230
        num_leading = random.randint(2, 4)  # 2-4 leading zeros
        first_digit = random.randint(1, 9)
        second_digit = random.randint(1, 9)

        # Create number like 0.00450 (first_digit=4, second_digit=5, trailing 0)
        number_str = f"0.{'0' * num_leading}{first_digit}{second_digit}0"

        # Correct: count places moved from first non-zero digit
        correct_exponent = -(num_leading + 1)  # +1 for the position of first digit
        coefficient = f"{first_digit}.{second_digit}"
        correct_answer = f"{coefficient} × 10^{correct_exponent}"

        # Malrule: count all zeros (num_leading + 1 in "0." + trailing 0)
        total_zeros = num_leading + 1 + 1  # leading "0." + num_leading zeros + trailing 0
        malrule_exponent = -total_zeros
        malrule_answer = f"{coefficient} × 10^{malrule_exponent}"

        problem_text = f"Convert {number_str} to scientific notation."

        return Problem(
            text=problem_text,
            operands=[number_str],
            operation='scientific_notation_conversion',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'small_decimal_trailing_zero',
                'number_string': number_str,
                'total_zeros': total_zeros,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_large_number_trailing_zeros(self, seed: Optional[int] = None) -> Problem:
        """
        Template 2: Large number with trailing zeros.
        Example: 30200
        Correct: 3.02 × 10^4 (moved 4 places)
        Malrule: 3.02 × 10^2 (counts 2 zeros)
        """
        if seed is not None:
            random.seed(seed)

        # Generate a large number with trailing zeros
        # Example: 30200, 405000, 70800
        first_digit = random.randint(1, 9)
        second_digit = random.randint(0, 9)
        third_digit = random.randint(1, 9)  # Non-zero to create internal structure
        num_trailing = random.randint(2, 3)  # 2-3 trailing zeros

        # Create number like 30200 or 70800
        base = f"{first_digit}{second_digit}{third_digit}"
        number_str = base + ('0' * num_trailing)
        number_value = int(number_str)

        # Correct: count places to move decimal from right to after first digit
        total_places = len(number_str) - 1
        coefficient = f"{first_digit}.{second_digit}{third_digit}"
        correct_answer = f"{coefficient} × 10^{total_places}"

        # Malrule: count visible zeros (second_digit if 0, plus trailing zeros)
        total_zeros = (1 if second_digit == 0 else 0) + num_trailing
        malrule_answer = f"{coefficient} × 10^{total_zeros}"

        problem_text = f"Express {number_str} in scientific notation."

        return Problem(
            text=problem_text,
            operands=[str(number_value)],
            operation='scientific_notation_conversion',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'large_number_trailing_zeros',
                'number_string': str(number_value),
                'total_zeros': total_zeros,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_word_problem_measurement(self, seed: Optional[int] = None) -> Problem:
        """
        Template 3: Word problem with scientific measurement.
        Example: A virus is 0.0003050 meters in diameter.
        Correct: 3.05 × 10^-4 (moved 4 places)
        Malrule: 3.05 × 10^-5 (counts 5 zeros)
        """
        if seed is not None:
            random.seed(seed)

        contexts = [
            ("virus", "diameter"),
            ("bacteria", "length"),
            ("cell", "width"),
            ("microorganism", "size"),
            ("particle", "diameter")
        ]

        context, measurement = random.choice(contexts)

        # Generate small decimal like 0.0003050 (with trailing zero to ensure difference)
        num_leading = random.randint(3, 4)
        first_digit = random.randint(1, 9)
        second_digit = random.randint(0, 9)
        third_digit = random.randint(1, 9)

        # Add trailing zero to ensure malrule counts more zeros than correct places
        number_str = f"0.{'0' * num_leading}{first_digit}{second_digit}{third_digit}0"

        # Correct: count places moved
        correct_exponent = -(num_leading + 1)
        coefficient = f"{first_digit}.{second_digit}{third_digit}"
        correct_answer = f"{coefficient} × 10^{correct_exponent}"

        # Malrule: count all zeros (including trailing zero)
        total_zeros = num_leading + 1 + (1 if second_digit == 0 else 0) + 1  # +1 for trailing zero
        malrule_exponent = -total_zeros
        malrule_answer = f"{coefficient} × 10^{malrule_exponent}"

        problem_text = f"A {context} is {number_str} meters in {measurement}. Express this in scientific notation."

        return Problem(
            text=problem_text,
            operands=[number_str],
            operation='scientific_notation_conversion',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_measurement',
                'number_string': number_str,
                'context': context,
                'measurement': measurement,
                'total_zeros': total_zeros,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_comparison_verification(self, seed: Optional[int] = None) -> Problem:
        """
        Template 4: Comparison/verification problem.
        Example: Is 0.006070 equal to 6.07 × 10^-5?
        Correct: No, 0.006070 = 6.07 × 10^-3
        Malrule: Yes (counts 5 zeros, thinks exponent is -5)
        """
        if seed is not None:
            random.seed(seed)

        # Generate a small decimal with trailing zero to ensure difference
        num_leading = random.randint(2, 4)
        first_digit = random.randint(1, 9)
        second_digit = random.randint(0, 9)
        third_digit = random.randint(1, 9)

        # Add trailing zero to ensure malrule counts more zeros
        number_str = f"0.{'0' * num_leading}{first_digit}{second_digit}{third_digit}0"
        coefficient = f"{first_digit}.{second_digit}{third_digit}"

        # Correct exponent
        correct_exponent = -(num_leading + 1)

        # Create a wrong exponent based on counting zeros (includes trailing zero)
        total_zeros = num_leading + 1 + (1 if second_digit == 0 else 0) + 1  # +1 for trailing zero
        wrong_exponent = -total_zeros

        # Present the wrong scientific notation
        given_sci_notation = f"{coefficient} × 10^{wrong_exponent}"

        problem_text = f"Is {number_str} equal to {given_sci_notation}?"

        # Answers
        correct_answer = f"No, {number_str} = {coefficient} × 10^{correct_exponent}"
        malrule_answer = "Yes"

        return Problem(
            text=problem_text,
            operands=[number_str, given_sci_notation],
            operation='comparison',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'comparison_verification',
                'number_string': number_str,
                'given_notation': given_sci_notation,
                'total_zeros': total_zeros,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_mixed_zeros_decimal(self, seed: Optional[int] = None) -> Problem:
        """
        Template 5: Decimal with mixed zeros (leading + internal + trailing).
        Example: 0.050200
        Correct: 5.02 × 10^-2 (moved 2 places)
        Malrule: 5.02 × 10^-4 (counts 4 zeros)
        """
        if seed is not None:
            random.seed(seed)

        # Create a decimal with leading zero, then some digits with zeros mixed in
        # Example: 0.050200, 0.30400
        num_leading = random.randint(1, 2)
        first_digit = random.randint(1, 9)
        second_digit = 0  # Force a zero
        third_digit = random.randint(1, 9)

        # Add trailing zeros
        number_str = f"0.{'0' * num_leading}{first_digit}{second_digit}{third_digit}00"

        # Correct: count places moved
        correct_exponent = -(num_leading + 1)
        coefficient = f"{first_digit}.{second_digit}{third_digit}"
        correct_answer = f"{coefficient} × 10^{correct_exponent}"

        # Malrule: count all zeros (leading + internal + trailing)
        total_zeros = 1 + num_leading + 1 + 2  # "0." + leading + middle 0 + two trailing
        malrule_exponent = -total_zeros
        malrule_answer = f"{coefficient} × 10^{malrule_exponent}"

        problem_text = f"Write {number_str} in scientific notation."

        return Problem(
            text=problem_text,
            operands=[number_str],
            operation='scientific_notation_conversion',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'mixed_zeros_decimal',
                'number_string': number_str,
                'total_zeros': total_zeros,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )
