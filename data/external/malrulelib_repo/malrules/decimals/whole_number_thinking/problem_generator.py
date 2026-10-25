"""
Problem generator for Whole-Number-Thinking malrule.

Generates decimal problems that elicit the misconception
of treating decimals like whole numbers.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional
from utils import ProblemGenerator, Problem, DifficultyLevel


class DecimalWholeNumberProblemGenerator(ProblemGenerator):
    """
    Generates decimal problems to elicit Whole-Number-Thinking.

    Creates problems where ignoring the decimal point and treating
    the numbers as whole numbers gives the wrong answer.
    """

    def get_name(self) -> str:
        return "Decimal Whole-Number-Thinking Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates decimal problems where treating decimals as whole numbers "
            "gives the wrong answer (e.g., 3.7 + 2.5 treated as 37 + 25)."
        )

    def get_available_templates(self):
        """Return list of available template names."""
        return [
            "basic_addition",
            "basic_comparison",
            "subtraction",
            "multiplication",
            "word_problem",
            "word_problem_context"  # NEW: Covers all formula types with variants
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[float, float]]:
        """Get appropriate value ranges based on level."""
        ranges = {
            4: {
                DifficultyLevel.EASY: (0.1, 9.9),
                DifficultyLevel.MEDIUM: (0.1, 19.9),
                DifficultyLevel.HARD: (0.1, 49.9),
            },
            5: {
                DifficultyLevel.EASY: (0.1, 9.9),
                DifficultyLevel.MEDIUM: (0.1, 19.9),
                DifficultyLevel.HARD: (0.1, 99.9),
            },
            6: {
                DifficultyLevel.EASY: (0.1, 19.9),
                DifficultyLevel.MEDIUM: (0.1, 49.9),
                DifficultyLevel.HARD: (0.1, 99.9),
            },
            7: {
                DifficultyLevel.EASY: (0.1, 19.9),
                DifficultyLevel.MEDIUM: (0.1, 99.9),
                DifficultyLevel.HARD: (0.1, 199.9),
            }
        }

        lvl = self.level if self.level in ranges else 5
        return {'decimal': ranges[lvl][self.difficulty]}

    def _generate_basic_addition(self, seed: Optional[int] = None) -> Problem:
        """
        Generate decimal addition problem.

        Malrule: 3.7 + 2.5 treated as 37 + 25 = 62
        Correct: 3.7 + 2.5 = 6.2
        """
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['decimal']

        # Generate decimals with 1 decimal place to make malrule clear
        decimal1 = round(random.uniform(1.0, min(max_val / 2, 9.9)), 1)
        decimal2 = round(random.uniform(1.0, min(max_val / 2, 9.9)), 1)

        # Calculate correct answer
        correct_answer = round(decimal1 + decimal2, 1)

        # Calculate malrule answer (treat as whole numbers)
        # 3.7 becomes 37, 2.5 becomes 25
        malrule_num1 = int(str(decimal1).replace('.', ''))
        malrule_num2 = int(str(decimal2).replace('.', ''))
        malrule_answer = malrule_num1 + malrule_num2

        problem_text = f"What is {decimal1} + {decimal2}?"

        return Problem(
            text=problem_text,
            operands=[decimal1, decimal2],
            operation='addition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'basic_addition',
                'decimal1': decimal1,
                'decimal2': decimal2,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer)
            }
        )

    def _generate_basic_comparison(self, seed: Optional[int] = None) -> Problem:
        """
        Generate decimal comparison problem.

        Malrule: Compare 3.7 and 2.5 as 37 vs 25, so 37 > 25
        Correct: 3.7 > 2.5
        """
        if seed is not None:
            random.seed(seed)

        # Strategy: Create decimals where whole-number thinking might give wrong answer
        # Example: 0.8 vs 0.45 - correct is 0.8 > 0.45, but malrule thinks 8 < 45

        strategy = random.choice(['longer_is_smaller', 'longer_is_larger', 'same_whole_part'])

        if strategy == 'longer_is_smaller':
            # Longer decimal is smaller: 0.45 < 0.8, but malrule thinks 45 > 8
            decimal1 = round(random.uniform(0.6, 0.9), 1)  # e.g., 0.8
            decimal2 = round(random.uniform(0.10, decimal1 - 0.05), 2)  # e.g., 0.45
            correct_answer = f"{decimal1}"  # 0.8 is larger
            malrule_answer = f"{decimal2}"  # malrule thinks 0.45 is larger (45 > 8)

        elif strategy == 'longer_is_larger':
            # Longer decimal is larger: 0.67 > 0.3, and malrule also thinks 67 > 3
            # This confirms the malrule (both get same answer)
            decimal1 = round(random.uniform(0.1, 0.4), 1)  # e.g., 0.3
            decimal2 = round(random.uniform(decimal1 + 0.05, 0.99), 2)  # e.g., 0.67
            correct_answer = f"{decimal2}"  # 0.67 is larger
            malrule_answer = f"{decimal2}"  # malrule also thinks 0.67 is larger (67 > 3)

        else:  # same_whole_part
            # Same whole part: 2.3 vs 2.15, correct is 2.3 > 2.15, malrule thinks 15 > 3
            whole_part = random.choice([1, 2, 3])
            decimal1 = whole_part + round(random.uniform(0.2, 0.5), 1)  # e.g., 2.3
            decimal2 = whole_part + round(random.uniform(0.10, decimal1 - whole_part - 0.05), 2)  # e.g., 2.15
            correct_answer = f"{decimal1}"  # 2.3 is larger
            malrule_answer = f"{decimal2}"  # malrule thinks 2.15 is larger (15 > 3)

        problem_text = f"Which is larger: {decimal1} or {decimal2}?"

        return Problem(
            text=problem_text,
            operands=[decimal1, decimal2],
            operation='comparison',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'basic_comparison',
                'decimal1': decimal1,
                'decimal2': decimal2,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'strategy': strategy
            }
        )

    def _generate_subtraction(self, seed: Optional[int] = None) -> Problem:
        """
        Generate decimal subtraction problem.

        Malrule: 5.8 - 2.3 treated as 58 - 23 = 35
        Correct: 5.8 - 2.3 = 3.5
        """
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['decimal']

        # Generate decimals with 1 decimal place
        decimal1 = round(random.uniform(3.0, min(max_val, 9.9)), 1)
        decimal2 = round(random.uniform(1.0, decimal1 - 0.5), 1)

        # Calculate correct answer
        correct_answer = round(decimal1 - decimal2, 1)

        # Calculate malrule answer (treat as whole numbers)
        malrule_num1 = int(str(decimal1).replace('.', ''))
        malrule_num2 = int(str(decimal2).replace('.', ''))
        malrule_answer = malrule_num1 - malrule_num2

        problem_text = f"What is {decimal1} - {decimal2}?"

        return Problem(
            text=problem_text,
            operands=[decimal1, decimal2],
            operation='subtraction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'subtraction',
                'decimal1': decimal1,
                'decimal2': decimal2,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer)
            }
        )

    def _generate_multiplication(self, seed: Optional[int] = None) -> Problem:
        """
        Generate decimal multiplication problem.

        Malrule: 2.5 × 3 treated as 25 × 3 = 75
        Correct: 2.5 × 3 = 7.5
        """
        if seed is not None:
            random.seed(seed)

        # Generate a decimal with 1 decimal place
        decimal1 = round(random.uniform(1.1, 5.9), 1)
        # Use a small whole number multiplier
        multiplier = random.choice([2, 3, 4, 5])

        # Calculate correct answer
        correct_answer = round(decimal1 * multiplier, 1)

        # Calculate malrule answer (treat decimal as whole number)
        malrule_num = int(str(decimal1).replace('.', ''))
        malrule_answer = malrule_num * multiplier

        problem_text = f"What is {decimal1} × {multiplier}?"

        return Problem(
            text=problem_text,
            operands=[decimal1, multiplier],
            operation='multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'multiplication',
                'decimal1': decimal1,
                'multiplier': multiplier,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer)
            }
        )

    def _generate_word_problem(self, seed: Optional[int] = None) -> Problem:
        """
        Generate word problem with real-world context.

        Uses various operations in context where whole-number thinking fails.
        """
        if seed is not None:
            random.seed(seed)

        # Choose operation type
        operation_type = random.choice(['addition', 'subtraction', 'comparison'])

        if operation_type == 'addition':
            contexts = [
                ("Sarah ran {0} km on Monday and {1} km on Tuesday. How many kilometers did she run in total?", "distance"),
                ("A pencil is {0} cm long. A pen is {1} cm long. What is their combined length?", "length"),
                ("John's plant grew {0} inches in week 1 and {1} inches in week 2. How much did it grow in total?", "growth"),
            ]

            context_template, context_type = random.choice(contexts)

            decimal1 = round(random.uniform(1.0, 5.9), 1)
            decimal2 = round(random.uniform(1.0, 5.9), 1)

            correct_answer = round(decimal1 + decimal2, 1)
            malrule_num1 = int(str(decimal1).replace('.', ''))
            malrule_num2 = int(str(decimal2).replace('.', ''))
            malrule_answer = malrule_num1 + malrule_num2

            problem_text = context_template.format(decimal1, decimal2)
            operands = [decimal1, decimal2]

        elif operation_type == 'subtraction':
            contexts = [
                ("A rope was {0} meters long. After cutting off {1} meters, how much rope is left?", "length"),
                ("Tom had {0} kg of flour. He used {1} kg for baking. How much flour is left?", "weight"),
                ("The temperature was {0}°C in the morning and dropped by {1}°C. What is the temperature now?", "temperature"),
            ]

            context_template, context_type = random.choice(contexts)

            decimal1 = round(random.uniform(3.0, 9.9), 1)
            decimal2 = round(random.uniform(1.0, decimal1 - 0.5), 1)

            correct_answer = round(decimal1 - decimal2, 1)
            malrule_num1 = int(str(decimal1).replace('.', ''))
            malrule_num2 = int(str(decimal2).replace('.', ''))
            malrule_answer = malrule_num1 - malrule_num2

            problem_text = context_template.format(decimal1, decimal2)
            operands = [decimal1, decimal2]

        else:  # comparison
            contexts = [
                ("Sarah's race time was {0} seconds and Tom's was {1} seconds. Who was faster?", "time", "less"),
                ("A pencil is {0} cm and a pen is {1} cm. Which is longer?", "length", "more"),
                ("John's plant grew {0} inches and Mary's grew {1} inches. Whose plant grew more?", "growth", "more"),
            ]

            context_template, context_type, comparison = random.choice(contexts)

            # Create comparison where malrule might fail
            decimal1 = round(random.uniform(0.6, 0.9), 1)
            decimal2 = round(random.uniform(0.10, decimal1 - 0.05), 2)

            # For "less is better" contexts like time
            if comparison == "less":
                correct_answer = f"{decimal2}"  # smaller is better
                malrule_answer = f"{decimal1}"  # malrule thinks 8 < 45, so 0.8 is better
            else:
                correct_answer = f"{decimal1}"  # larger is better
                malrule_answer = f"{decimal2}"  # malrule thinks 45 > 8, so 0.45 is better

            problem_text = context_template.format(decimal1, decimal2)
            operands = [decimal1, decimal2]

        return Problem(
            text=problem_text,
            operands=operands,
            operation=operation_type,
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem',
                'context_type': context_type,
                'operation_type': operation_type,
                'correct_answer': str(correct_answer),
                'malrule_answer': str(malrule_answer)
            }
        )

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate a problem using the specified template.

        Args:
            seed: Optional random seed for reproducibility
            template: Template name (from get_available_templates())

        Returns:
            Problem instance
        """
        if seed is not None:
            random.seed(seed)

        # If no template specified, choose randomly
        if template is None:
            template = random.choice(self.get_available_templates())

        # Validate template
        if template not in self.get_available_templates():
            raise ValueError(f"Unknown template: {template}")

        # Call appropriate template method
        template_method = getattr(self, f'_generate_{template}')
        return template_method(seed)

    def _generate_word_problem_context(self, seed: Optional[int] = None) -> Problem:
        """Generate word problem covering ALL formula types with 3 variants each."""
        if seed is not None:
            random.seed(seed)

        # Select which formula type to embed
        formula_types = ['comparison', 'addition', 'subtraction', 'multiplication']
        formula_type = random.choice(formula_types)
        variant = random.randint(0, 2)  # 3 variants per formula type

        min_val, max_val = self.get_value_ranges()['decimal']

        if formula_type == 'comparison':
            # Formula: a.bc vs d.e
            decimal1 = round(random.uniform(1.0, min(max_val, 9.9)), 2)
            decimal2 = round(random.uniform(1.0, min(max_val, 9.9)), 1)

            # Ensure they are different
            if abs(decimal1 - decimal2) < 0.1:
                decimal2 += 1.0

            correct_answer = str(max(decimal1, decimal2))

            # Malrule: treat as whole numbers
            malrule_num1 = int(str(decimal1).replace('.', ''))
            malrule_num2 = int(str(decimal2).replace('.', ''))
            malrule_answer = str(decimal1 if malrule_num1 > malrule_num2 else decimal2)

            templates = [
                f"Maria has ${decimal1} and Tom has ${decimal2}. Who has more money?",
                f"Which is larger: {decimal1} or {decimal2}?",
                f"A rope is {decimal1} meters long and another is {decimal2} meters long. Which rope is longer?"
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[decimal1, decimal2],
                operation='comparison',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'decimal1': decimal1,
                    'decimal2': decimal2,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        elif formula_type == 'addition':
            # Formula: a.b + c.d
            decimal1 = round(random.uniform(1.0, min(max_val / 2, 9.9)), 1)
            decimal2 = round(random.uniform(1.0, min(max_val / 2, 9.9)), 1)

            correct_answer = round(decimal1 + decimal2, 1)

            # Malrule: treat as whole numbers
            malrule_num1 = int(str(decimal1).replace('.', ''))
            malrule_num2 = int(str(decimal2).replace('.', ''))
            malrule_answer = malrule_num1 + malrule_num2

            templates = [
                f"Sarah earned ${decimal1} on Monday and ${decimal2} on Tuesday. How much did she earn in total?",
                f"A container has {decimal1} liters of water. If {decimal2} more liters are added, how much water is there?",
                f"John walked {decimal1} km in the morning and {decimal2} km in the afternoon. What is the total distance?"
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[decimal1, decimal2],
                operation='addition',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'decimal1': decimal1,
                    'decimal2': decimal2,
                    'correct_answer': str(correct_answer),
                    'malrule_answer': str(malrule_answer),
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        elif formula_type == 'subtraction':
            # Formula: a.b - c.d
            decimal1 = round(random.uniform(5.0, min(max_val, 9.9)), 1)
            decimal2 = round(random.uniform(1.0, decimal1 - 1.0), 1)

            correct_answer = round(decimal1 - decimal2, 1)

            # Malrule: treat as whole numbers
            malrule_num1 = int(str(decimal1).replace('.', ''))
            malrule_num2 = int(str(decimal2).replace('.', ''))
            malrule_answer = malrule_num1 - malrule_num2

            templates = [
                f"John had ${decimal1} and spent ${decimal2}. How much money is left?",
                f"A tank had {decimal1} liters of water. After {decimal2} liters leaked, how much remains?",
                f"A rope was {decimal1} meters long. After cutting off {decimal2} meters, what is the remaining length?"
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[decimal1, decimal2],
                operation='subtraction',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'decimal1': decimal1,
                    'decimal2': decimal2,
                    'correct_answer': str(correct_answer),
                    'malrule_answer': str(malrule_answer),
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        else:  # multiplication
            # Formula: a.b × c.d
            decimal1 = round(random.uniform(1.0, min(max_val / 3, 5.0)), 1)
            decimal2 = round(random.uniform(1.0, min(max_val / 3, 5.0)), 1)

            correct_answer = round(decimal1 * decimal2, 2)

            # Malrule: treat as whole numbers
            malrule_num1 = int(str(decimal1).replace('.', ''))
            malrule_num2 = int(str(decimal2).replace('.', ''))
            malrule_answer = malrule_num1 * malrule_num2

            templates = [
                f"A car travels at {decimal1} km per hour for {decimal2} hours. What is the total distance traveled?",
                f"A recipe uses {decimal1} cups of flour per batch. If you make {decimal2} batches, how much flour is needed?",
                f"A worker earns ${decimal1} per hour for {decimal2} hours. What is the total pay?"
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[decimal1, decimal2],
                operation='multiplication',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'decimal1': decimal1,
                    'decimal2': decimal2,
                    'correct_answer': str(correct_answer),
                    'malrule_answer': str(malrule_answer),
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )
