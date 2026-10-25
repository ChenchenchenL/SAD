"""
Problem generator for Right-Align-Decimals malrule.

Generates decimal addition/subtraction problems where numbers
have different numbers of decimal places.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple
from utils import ProblemGenerator, Problem, DifficultyLevel


class RightAlignDecimalsProblemGenerator(ProblemGenerator):
    """
    Generates decimal addition/subtraction problems.

    Creates problems with different decimal place counts to
    expose right-alignment errors.
    """

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level and difficulty."""
        ranges = {
            4: {
                DifficultyLevel.EASY: (1, 10),
                DifficultyLevel.MEDIUM: (1, 50),
                DifficultyLevel.HARD: (1, 100),
            },
            5: {
                DifficultyLevel.EASY: (1, 50),
                DifficultyLevel.MEDIUM: (1, 100),
                DifficultyLevel.HARD: (1, 500),
            },
            6: {
                DifficultyLevel.EASY: (1, 100),
                DifficultyLevel.MEDIUM: (1, 500),
                DifficultyLevel.HARD: (1, 1000),
            }
        }

        lvl = self.level if self.level in ranges else 5
        return {'values': ranges[lvl][self.difficulty]}

    def get_available_templates(self):
        """Return list of available template names."""
        return [
            'basic_addition',
            'basic_subtraction',
            'money_word_problem',
            'measurement_word_problem',
            'three_number_mixed',
            'word_problem_context'  # NEW: Covers all formula types with variants
        ]

    def _calculate_malrule_answer(self, num1, num2, operation, num3=None):
        """
        Calculate the malrule answer (right-align decimals error).

        Args:
            num1: First number
            num2: Second number
            operation: '+' or '-'
            num3: Optional third number for multi-step

        Returns:
            Malrule answer as string
        """
        # Get string representations
        num1_str = str(num1)
        num2_str = str(num2)

        # Remove decimal points and treat as whole numbers
        num1_no_decimal = num1_str.replace('.', '')
        num2_no_decimal = num2_str.replace('.', '')

        # Right-align them (like whole numbers)
        if len(num1_no_decimal) >= len(num2_no_decimal):
            num2_padded = num2_no_decimal.zfill(len(num1_no_decimal))
            num1_padded = num1_no_decimal
        else:
            num1_padded = num1_no_decimal.zfill(len(num2_no_decimal))
            num2_padded = num2_no_decimal

        # Convert to integers for calculation
        val1 = int(num1_padded)
        val2 = int(num2_padded)

        if operation == '+':
            result_int = val1 + val2
        else:
            result_int = abs(val1 - val2)

        # Get decimal places
        num1_decimal_places = len(num1_str.split('.')[1]) if '.' in num1_str else 0
        num2_decimal_places = len(num2_str.split('.')[1]) if '.' in num2_str else 0
        decimal_places = min(num1_decimal_places, num2_decimal_places)

        # Put decimal point back (incorrectly)
        result_str = str(result_int)

        if decimal_places > 0 and len(result_str) > decimal_places:
            insert_pos = len(result_str) - decimal_places
            result_with_decimal = result_str[:insert_pos] + '.' + result_str[insert_pos:]
            return result_with_decimal
        else:
            return str(float(result_int))

    def _generate_basic_addition(self, seed=None):
        """Generate basic addition: 1 decimal place + 2 decimal places."""
        if seed is not None:
            random.seed(seed)

        value_range = self.get_value_ranges()['values']
        min_val, max_val = value_range

        # 1 decimal place
        whole1 = random.randint(min_val, max_val)
        decimal1 = random.randint(1, 9)
        num1 = whole1 + decimal1 / 10

        # 2 decimal places
        whole2 = random.randint(min_val, max_val)
        decimal2 = random.randint(10, 99)
        num2 = whole2 + decimal2 / 100

        correct_answer = round(num1 + num2, 2)
        malrule_answer = self._calculate_malrule_answer(num1, num2, '+')

        problem_text = f"Calculate: {num1} + {num2}"

        return Problem(
            text=problem_text,
            operands=[num1, num2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': num1,
                'num2': num2,
                'operation_symbol': '+',
                'correct_answer': str(correct_answer),
                'malrule_answer': malrule_answer,
                'num1_str': str(num1),
                'num2_str': str(num2),
                'num1_decimal_places': len(str(num1).split('.')[1]) if '.' in str(num1) else 0,
                'num2_decimal_places': len(str(num2).split('.')[1]) if '.' in str(num2) else 0,
                'template': 'basic_addition'
            }
        )

    def _generate_basic_subtraction(self, seed=None):
        """Generate basic subtraction: 2 decimal places - 1 decimal place."""
        if seed is not None:
            random.seed(seed)

        value_range = self.get_value_ranges()['values']
        min_val, max_val = value_range

        # 2 decimal places
        whole1 = random.randint(min_val, max_val)
        decimal1 = random.randint(10, 99)
        num1 = whole1 + decimal1 / 100

        # 1 decimal place
        whole2 = random.randint(min_val, min(max_val, whole1))
        decimal2 = random.randint(1, 9)
        num2 = whole2 + decimal2 / 10

        # Ensure num1 > num2
        if num1 < num2:
            num1, num2 = num2, num1

        correct_answer = round(num1 - num2, 2)
        malrule_answer = self._calculate_malrule_answer(num1, num2, '-')

        problem_text = f"Calculate: {num1} - {num2}"

        return Problem(
            text=problem_text,
            operands=[num1, num2],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': num1,
                'num2': num2,
                'operation_symbol': '-',
                'correct_answer': str(correct_answer),
                'malrule_answer': malrule_answer,
                'num1_str': str(num1),
                'num2_str': str(num2),
                'num1_decimal_places': len(str(num1).split('.')[1]) if '.' in str(num1) else 0,
                'num2_decimal_places': len(str(num2).split('.')[1]) if '.' in str(num2) else 0,
                'template': 'basic_subtraction'
            }
        )

    def _generate_money_word_problem(self, seed=None):
        """Generate money word problem with different decimal places."""
        if seed is not None:
            random.seed(seed)

        # Money amounts (limited to reasonable range)
        whole1 = random.randint(1, 50)
        decimal1 = random.randint(1, 9)
        amount1 = whole1 + decimal1 / 10

        whole2 = random.randint(1, 50)
        decimal2 = random.randint(10, 99)
        amount2 = whole2 + decimal2 / 100

        contexts = [
            f"Sarah has ${amount1} and receives ${amount2} more. How much money does she have now?",
            f"A toy costs ${amount1} and a book costs ${amount2}. What is the total cost?",
            f"Jake earned ${amount1} on Monday and ${amount2} on Tuesday. How much did he earn in total?",
        ]

        problem_text = random.choice(contexts)

        correct_answer = round(amount1 + amount2, 2)
        malrule_answer = self._calculate_malrule_answer(amount1, amount2, '+')

        return Problem(
            text=problem_text,
            operands=[amount1, amount2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': amount1,
                'num2': amount2,
                'operation_symbol': '+',
                'correct_answer': f"${correct_answer}",
                'malrule_answer': f"${malrule_answer}",
                'num1_str': str(amount1),
                'num2_str': str(amount2),
                'num1_decimal_places': len(str(amount1).split('.')[1]) if '.' in str(amount1) else 0,
                'num2_decimal_places': len(str(amount2).split('.')[1]) if '.' in str(amount2) else 0,
                'template': 'money_word_problem',
                'context': 'money'
            }
        )

    def _generate_measurement_word_problem(self, seed=None):
        """Generate measurement word problem (lengths, weights)."""
        if seed is not None:
            random.seed(seed)

        value_range = self.get_value_ranges()['values']
        min_val, max_val = value_range

        # Generate measurements with different decimal places
        whole1 = random.randint(1, min(50, max_val))
        decimal1 = random.randint(10, 99)
        measure1 = whole1 + decimal1 / 100

        whole2 = random.randint(1, min(50, max_val))
        decimal2 = random.randint(1, 9)
        measure2 = whole2 + decimal2 / 10

        measurement_types = [
            ("meters", "m"),
            ("kilograms", "kg"),
            ("liters", "L"),
            ("centimeters", "cm")
        ]

        unit_name, unit_symbol = random.choice(measurement_types)

        contexts = [
            f"A rope is {measure1} {unit_symbol} long and another rope is {measure2} {unit_symbol} long. What is the total length?",
            f"A container holds {measure1} {unit_symbol} of water. If {measure2} {unit_symbol} more is added, how much water is there in total?",
            f"The first piece measures {measure1} {unit_symbol} and the second measures {measure2} {unit_symbol}. What is the combined measurement?",
        ]

        problem_text = random.choice(contexts)

        correct_answer = round(measure1 + measure2, 2)
        malrule_answer = self._calculate_malrule_answer(measure1, measure2, '+')

        return Problem(
            text=problem_text,
            operands=[measure1, measure2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': measure1,
                'num2': measure2,
                'operation_symbol': '+',
                'correct_answer': f"{correct_answer} {unit_symbol}",
                'malrule_answer': f"{malrule_answer} {unit_symbol}",
                'num1_str': str(measure1),
                'num2_str': str(measure2),
                'num1_decimal_places': len(str(measure1).split('.')[1]) if '.' in str(measure1) else 0,
                'num2_decimal_places': len(str(measure2).split('.')[1]) if '.' in str(measure2) else 0,
                'template': 'measurement_word_problem',
                'context': 'measurement',
                'unit': unit_symbol
            }
        )

    def _generate_three_number_mixed(self, seed=None):
        """Generate three-number mixed operation problem."""
        if seed is not None:
            random.seed(seed)

        value_range = self.get_value_ranges()['values']
        min_val, max_val = value_range

        # Three numbers with varying decimal places
        whole1 = random.randint(min_val, min(max_val, 50))
        decimal1 = random.randint(1, 9)
        num1 = whole1 + decimal1 / 10

        whole2 = random.randint(min_val, min(max_val, 50))
        decimal2 = random.randint(10, 99)
        num2 = whole2 + decimal2 / 100

        whole3 = random.randint(min_val, min(max_val, 50))
        decimal3 = random.randint(1, 9)
        num3 = whole3 + decimal3 / 10

        # Ensure result is positive
        if num1 + num2 < num3:
            num1, num3 = num3, num1

        correct_answer = round(num1 + num2 - num3, 2)

        # Calculate malrule answer step by step
        # First: num1 + num2 (with malrule)
        temp_malrule = self._calculate_malrule_answer(num1, num2, '+')
        temp_malrule_float = float(temp_malrule)

        # Then: temp_result - num3 (with malrule)
        malrule_answer = self._calculate_malrule_answer(temp_malrule_float, num3, '-')

        problem_text = f"Calculate: {num1} + {num2} - {num3}"

        return Problem(
            text=problem_text,
            operands=[num1, num2, num3],
            operation='mixed',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1': num1,
                'num2': num2,
                'num3': num3,
                'operation_symbol': '+ and -',
                'correct_answer': str(correct_answer),
                'malrule_answer': malrule_answer,
                'num1_str': str(num1),
                'num2_str': str(num2),
                'num3_str': str(num3),
                'num1_decimal_places': len(str(num1).split('.')[1]) if '.' in str(num1) else 0,
                'num2_decimal_places': len(str(num2).split('.')[1]) if '.' in str(num2) else 0,
                'num3_decimal_places': len(str(num3).split('.')[1]) if '.' in str(num3) else 0,
                'template': 'three_number_mixed',
                'num_count': 3
            }
        )

    def _generate_word_problem_context(self, seed=None):
        """Generate word problem covering ALL formula types with 3 variants each."""
        if seed is not None:
            random.seed(seed)

        # Select which formula type to embed
        formula_types = ['two_number_addition', 'two_number_subtraction', 'three_number_mixed']
        formula_type = random.choice(formula_types)
        variant = random.randint(0, 2)  # 3 variants per formula type

        if formula_type == 'two_number_addition':
            # Formula: a.b + c.de
            whole1 = random.randint(1, 50)
            decimal1 = random.randint(1, 9)
            num1 = whole1 + decimal1 / 10

            whole2 = random.randint(1, 50)
            decimal2 = random.randint(10, 99)
            num2 = whole2 + decimal2 / 100

            correct_answer = round(num1 + num2, 2)
            malrule_answer = self._calculate_malrule_answer(num1, num2, '+')

            templates = [
                f"Sarah earned ${num1} on Monday and ${num2} on Tuesday. How much did she earn in total?",
                f"A container has {num1} liters of water. If {num2} more liters are added, how much water is there in total?",
                f"John walked {num1} km in the morning and {num2} km in the afternoon. What is the total distance walked?"
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[num1, num2],
                operation='addition',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'num1': num1,
                    'num2': num2,
                    'operation_symbol': '+',
                    'correct_answer': f"{correct_answer}",
                    'malrule_answer': malrule_answer,
                    'num1_str': str(num1),
                    'num2_str': str(num2),
                    'num1_decimal_places': len(str(num1).split('.')[1]) if '.' in str(num1) else 0,
                    'num2_decimal_places': len(str(num2).split('.')[1]) if '.' in str(num2) else 0,
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        elif formula_type == 'two_number_subtraction':
            # Formula: a.bc - d.e
            whole1 = random.randint(10, 50)
            decimal1 = random.randint(10, 99)
            num1 = whole1 + decimal1 / 100

            whole2 = random.randint(1, whole1)
            decimal2 = random.randint(1, 9)
            num2 = whole2 + decimal2 / 10

            # Ensure num1 > num2
            if num1 < num2:
                num1, num2 = num2, num1

            correct_answer = round(num1 - num2, 2)
            malrule_answer = self._calculate_malrule_answer(num1, num2, '-')

            templates = [
                f"John had ${num1} and spent ${num2}. How much money is left?",
                f"A tank had {num1} liters of water. After {num2} liters leaked out, how much remains?",
                f"A rope was {num1} meters long. After cutting off {num2} meters, what is the remaining length?"
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[num1, num2],
                operation='subtraction',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'num1': num1,
                    'num2': num2,
                    'operation_symbol': '-',
                    'correct_answer': f"{correct_answer}",
                    'malrule_answer': malrule_answer,
                    'num1_str': str(num1),
                    'num2_str': str(num2),
                    'num1_decimal_places': len(str(num1).split('.')[1]) if '.' in str(num1) else 0,
                    'num2_decimal_places': len(str(num2).split('.')[1]) if '.' in str(num2) else 0,
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        else:  # three_number_mixed
            # Formula: a.b + c.de - f.g
            whole1 = random.randint(10, 50)
            decimal1 = random.randint(1, 9)
            num1 = whole1 + decimal1 / 10

            whole2 = random.randint(5, 30)
            decimal2 = random.randint(10, 99)
            num2 = whole2 + decimal2 / 100

            whole3 = random.randint(5, 30)
            decimal3 = random.randint(1, 9)
            num3 = whole3 + decimal3 / 10

            # Ensure result is positive
            if num1 + num2 < num3:
                num1, num3 = num3, num1

            correct_answer = round(num1 + num2 - num3, 2)

            # Calculate malrule answer step by step
            temp_malrule = self._calculate_malrule_answer(num1, num2, '+')
            temp_malrule_float = float(temp_malrule)
            malrule_answer = self._calculate_malrule_answer(temp_malrule_float, num3, '-')

            templates = [
                f"Sarah earned ${num1} on Monday, ${num2} on Tuesday, and spent ${num3} on Wednesday. How much does she have?",
                f"A container has {num1} liters, receives {num2} more liters, then {num3} liters are removed. How much remains?",
                f"A plant grew {num1} cm in week 1, {num2} cm in week 2, and shrank {num3} cm in week 3. What is the net growth?"
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[num1, num2, num3],
                operation='mixed',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'num1': num1,
                    'num2': num2,
                    'num3': num3,
                    'operation_symbol': '+ and -',
                    'correct_answer': f"{correct_answer}",
                    'malrule_answer': malrule_answer,
                    'num1_str': str(num1),
                    'num2_str': str(num2),
                    'num3_str': str(num3),
                    'num1_decimal_places': len(str(num1).split('.')[1]) if '.' in str(num1) else 0,
                    'num2_decimal_places': len(str(num2).split('.')[1]) if '.' in str(num2) else 0,
                    'num3_decimal_places': len(str(num3).split('.')[1]) if '.' in str(num3) else 0,
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant,
                    'num_count': 3
                }
            )

    def generate(self, seed=None, template=None) -> Problem:
        """
        Generate a decimal addition or subtraction problem.

        Args:
            seed: Random seed for reproducibility
            template: Specific template to use (optional)

        Returns:
            Problem instance with decimal numbers having different place counts
        """
        if seed is not None:
            random.seed(seed)

        # Choose template
        if template is None:
            template = random.choice(self.get_available_templates())

        # Call appropriate template method
        if template == 'basic_addition':
            return self._generate_basic_addition(seed)
        elif template == 'basic_subtraction':
            return self._generate_basic_subtraction(seed)
        elif template == 'money_word_problem':
            return self._generate_money_word_problem(seed)
        elif template == 'measurement_word_problem':
            return self._generate_measurement_word_problem(seed)
        elif template == 'three_number_mixed':
            return self._generate_three_number_mixed(seed)
        elif template == 'word_problem_context':
            return self._generate_word_problem_context(seed)
        else:
            raise ValueError(f"Unknown template: {template}")
