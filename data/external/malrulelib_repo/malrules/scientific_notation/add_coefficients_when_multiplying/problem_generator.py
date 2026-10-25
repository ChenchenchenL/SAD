"""
Problem generator for Add-Coefficients-When-Multiplying malrule.

Generates scientific notation multiplication problems to elicit the misconception
of adding coefficients instead of multiplying them.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional, List
from utils import ProblemGenerator, Problem, DifficultyLevel


class AddCoefficientsWhenMultiplyingProblemGenerator(ProblemGenerator):
    """
    Generates scientific notation multiplication problems.

    Focus on problems where students might confuse the addition of exponents
    with the operation on coefficients, leading them to add coefficients
    instead of multiplying them.
    """

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_multiplication',
            'word_problem_context',
            'multiple_step_calculation',
            'compare_results',
            'area_volume_calculation'
        ]

    def get_name(self) -> str:
        return "Add-Coefficients-When-Multiplying Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates multiplication problems with numbers in scientific notation, "
            "designed to elicit the common error of adding coefficients instead of "
            "multiplying them while correctly adding exponents."
        )

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level and difficulty."""
        # Return ranges for coefficients (typically 1-10)
        ranges = {
            7: {
                DifficultyLevel.EASY: (1, 5),        # Small coefficients
                DifficultyLevel.MEDIUM: (2, 9),      # Wider range
                DifficultyLevel.HARD: (1, 9),        # Full range with decimals
            },
            8: {
                DifficultyLevel.EASY: (2, 9),
                DifficultyLevel.MEDIUM: (1, 9),
                DifficultyLevel.HARD: (1, 9),
            },
            9: {
                DifficultyLevel.EASY: (1, 9),
                DifficultyLevel.MEDIUM: (1, 9),
                DifficultyLevel.HARD: (1, 9),
            },
            10: {
                DifficultyLevel.EASY: (1, 9),
                DifficultyLevel.MEDIUM: (1, 9),
                DifficultyLevel.HARD: (1, 9),
            }
        }

        lvl = self.level if self.level in ranges else 8
        return {
            'coefficient': ranges[lvl][self.difficulty],
            'exponent': (-5, 10)  # Range for exponents
        }

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate a scientific notation multiplication problem.

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
        if template == 'basic_multiplication':
            return self._generate_basic_multiplication(seed)
        elif template == 'word_problem_context':
            return self._generate_word_problem_context(seed)
        elif template == 'multiple_step_calculation':
            return self._generate_multiple_step_calculation(seed)
        elif template == 'compare_results':
            return self._generate_compare_results(seed)
        elif template == 'area_volume_calculation':
            return self._generate_area_volume_calculation(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_multiplication(self, seed=None):
        """Template 1: Basic multiplication problem."""
        if seed is not None:
            random.seed(seed)

        coef_min, coef_max = self.get_value_ranges()['coefficient']
        exp_min, exp_max = self.get_value_ranges()['exponent']

        # Generate two numbers in scientific notation
        # Coefficient: between 1 and 10 (can be decimal)
        if self.difficulty == DifficultyLevel.HARD or random.random() < 0.5:
            # Use decimal coefficients sometimes
            coef1 = round(random.uniform(coef_min, min(coef_max, 9.9)), 1)
            coef2 = round(random.uniform(coef_min, min(coef_max, 9.9)), 1)
        else:
            # Use integer coefficients
            coef1 = float(random.randint(coef_min, coef_max))
            coef2 = float(random.randint(coef_min, coef_max))

        # Generate exponents
        exp1 = random.randint(exp_min, exp_max)
        exp2 = random.randint(exp_min, exp_max)

        # Format the numbers
        num1_str = f"{coef1} × 10^{exp1}"
        num2_str = f"{coef2} × 10^{exp2}"

        # Create problem text
        problem_texts = [
            f"Multiply ({num1_str}) × ({num2_str})",
            f"What is ({num1_str}) × ({num2_str})?",
            f"Calculate ({num1_str}) × ({num2_str})",
            f"Find the product: ({num1_str}) × ({num2_str})"
        ]
        problem_text = random.choice(problem_texts)

        # Calculate correct answer
        correct_coef = coef1 * coef2
        correct_exp = exp1 + exp2
        # Normalize
        if correct_coef >= 10:
            exp_adjust = 0
            while correct_coef >= 10:
                correct_coef /= 10
                exp_adjust += 1
            correct_exp += exp_adjust
        correct_answer = f"{correct_coef} × 10^{correct_exp}"

        # Calculate malrule answer (add coefficients)
        malrule_coef = coef1 + coef2
        malrule_exp = exp1 + exp2
        # Normalize
        if malrule_coef >= 10:
            exp_adjust = 0
            while malrule_coef >= 10:
                malrule_coef /= 10
                exp_adjust += 1
            malrule_exp += exp_adjust
        malrule_answer = f"{malrule_coef} × 10^{malrule_exp}"

        return Problem(
            text=problem_text,
            operands=[coef1, exp1, coef2, exp2],  # [coef1, exp1, coef2, exp2]
            operation='scientific_notation_multiplication',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'num1_str': num1_str,
                'num2_str': num2_str,
                'coefficient1': coef1,
                'exponent1': exp1,
                'coefficient2': coef2,
                'exponent2': exp2,
                'template': 'basic_multiplication',
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_word_problem_context(self, seed=None):
        """Template 2: Word problem context covering ALL formula types with 3 variants each."""
        if seed is not None:
            random.seed(seed)

        # Select which formula type to embed
        formula_types = ['two_factor_multiplication', 'three_factor_multiplication', 'division', 'multiplication_then_division']
        formula_type = random.choice(formula_types)
        variant = random.randint(0, 2)  # 3 variants per formula type

        coef_min, coef_max = self.get_value_ranges()['coefficient']
        exp_min, exp_max = self.get_value_ranges()['exponent']

        if formula_type == 'two_factor_multiplication':
            # Formula: (a×10^m) × (b×10^n)
            coef1 = float(random.randint(coef_min, coef_max))
            coef2 = float(random.randint(coef_min, coef_max))
            exp1 = random.randint(2, 6)
            exp2 = random.randint(2, 6)

            num1_str = f"{coef1} × 10^{exp1}"
            num2_str = f"{coef2} × 10^{exp2}"

            templates = [
                f"A bacteria culture has {num1_str} bacteria per sample. If there are {num2_str} samples, what is the total bacteria count?",
                f"A spaceship travels {num1_str} meters per hour for {num2_str} hours. What is the total distance?",
                f"A storage device has {num2_str} drives, each containing {num1_str} bytes. What is the total storage capacity?"
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[coef1, exp1, coef2, exp2],
                operation='scientific_notation_multiplication',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'num1_str': num1_str,
                    'num2_str': num2_str,
                    'coefficient1': coef1,
                    'exponent1': exp1,
                    'coefficient2': coef2,
                    'exponent2': exp2,
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        elif formula_type == 'three_factor_multiplication':
            # Formula: (a×10^m) × (b×10^n) × (c×10^p)
            coef1 = float(random.randint(coef_min, min(coef_max, 5)))
            coef2 = float(random.randint(coef_min, min(coef_max, 5)))
            coef3 = float(random.randint(coef_min, min(coef_max, 5)))
            exp1 = random.randint(1, 4)
            exp2 = random.randint(1, 4)
            exp3 = random.randint(1, 4)

            num1_str = f"{coef1} × 10^{exp1}"
            num2_str = f"{coef2} × 10^{exp2}"
            num3_str = f"{coef3} × 10^{exp3}"

            templates = [
                f"A box contains {num1_str} items. There are {num2_str} boxes in a pallet and {num3_str} pallets in a warehouse. How many total items?",
                f"A molecule has mass {num1_str} grams. A cell has {num2_str} molecules, and a tissue has {num3_str} cells. What is the total mass?",
                f"A data packet is {num1_str} bytes. A file has {num2_str} packets, and a folder has {num3_str} files. What is the total size?"
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[coef1, exp1, coef2, exp2, coef3, exp3],
                operation='scientific_notation_multiplication',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'num1_str': num1_str,
                    'num2_str': num2_str,
                    'num3_str': num3_str,
                    'coefficient1': coef1,
                    'exponent1': exp1,
                    'coefficient2': coef2,
                    'exponent2': exp2,
                    'coefficient3': coef3,
                    'exponent3': exp3,
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant,
                    'num_factors': 3
                }
            )

        elif formula_type == 'division':
            # Formula: (a×10^m) ÷ (b×10^n)
            coef1 = float(random.randint(coef_min, coef_max))
            coef2 = float(random.randint(coef_min, coef_max))
            exp1 = random.randint(4, 8)
            exp2 = random.randint(2, 5)

            num1_str = f"{coef1} × 10^{exp1}"
            num2_str = f"{coef2} × 10^{exp2}"

            templates = [
                f"A total of {num1_str} bacteria are divided equally among {num2_str} petri dishes. How many bacteria per dish?",
                f"A distance of {num1_str} meters is covered in {num2_str} seconds. What is the speed in meters per second?",
                f"A data set of {num1_str} bytes is split into {num2_str} files. What is the size of each file?"
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[coef1, exp1, coef2, exp2],
                operation='scientific_notation_division',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'num1_str': num1_str,
                    'num2_str': num2_str,
                    'coefficient1': coef1,
                    'exponent1': exp1,
                    'coefficient2': coef2,
                    'exponent2': exp2,
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant,
                    'operation_type': 'division'
                }
            )

        else:  # multiplication_then_division
            # Formula: ((a×10^m) × (b×10^n)) ÷ (c×10^p)
            coef1 = float(random.randint(coef_min, coef_max))
            coef2 = float(random.randint(coef_min, coef_max))
            coef3 = float(random.randint(coef_min, coef_max))
            exp1 = random.randint(2, 5)
            exp2 = random.randint(2, 5)
            exp3 = random.randint(2, 4)

            num1_str = f"{coef1} × 10^{exp1}"
            num2_str = f"{coef2} × 10^{exp2}"
            num3_str = f"{coef3} × 10^{exp3}"

            templates = [
                f"A factory produces {num1_str} items per day for {num2_str} days. If these items are packed into {num3_str} boxes, how many items per box?",
                f"A field has area {num1_str} square meters with {num2_str} plants per square meter. If distributed among {num3_str} gardens, how many plants per garden?",
                f"A server processes {num1_str} requests per second for {num2_str} seconds. If divided among {num3_str} clients, how many requests per client?"
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[coef1, exp1, coef2, exp2, coef3, exp3],
                operation='scientific_notation_mult_div',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'num1_str': num1_str,
                    'num2_str': num2_str,
                    'num3_str': num3_str,
                    'coefficient1': coef1,
                    'exponent1': exp1,
                    'coefficient2': coef2,
                    'exponent2': exp2,
                    'coefficient3': coef3,
                    'exponent3': exp3,
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant,
                    'operation_type': 'mult_div'
                }
            )

    def _generate_multiple_step_calculation(self, seed=None):
        """Template 3: Multiple step calculation."""
        problem = self._generate_basic_multiplication(seed)
        problem.metadata['template'] = 'multiple_step_calculation'
        num1_str = problem.metadata['num1_str']
        num2_str = problem.metadata['num2_str']
        problem.text = f"First multiply ({num1_str}) × ({num2_str}). Express your answer in scientific notation."
        return problem

    def _generate_compare_results(self, seed=None):
        """Template 4: Compare results."""
        problem = self._generate_basic_multiplication(seed)
        problem.metadata['template'] = 'compare_results'
        return problem

    def _generate_area_volume_calculation(self, seed=None):
        """Template 5: Area/Volume calculation."""
        problem = self._generate_basic_multiplication(seed)
        problem.metadata['template'] = 'area_volume_calculation'
        num1_str = problem.metadata['num1_str']
        num2_str = problem.metadata['num2_str']
        problem.text = f"A rectangle has length {num1_str} meters and width {num2_str} meters. What is its area?"
        return problem
