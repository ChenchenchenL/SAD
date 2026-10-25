"""
Problem generator for Negative-Outside-Same-As-Inside malrule.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional, List
from utils import ProblemGenerator, Problem, DifficultyLevel


class NegativeOutsideSameAsInsideProblemGenerator(ProblemGenerator):
    """
    Generates negative square root problems.

    Templates:
    1. basic_negative_outside - Simple -√n problems
    2. expression_form - Explicit -(√n) notation
    3. in_equations - Equations like x = -√25
    4. combined_operations - Operations like -√4 + √9 or 2(-√16)
    5. word_problem - Real-world contexts (temperature, debt, elevation)
    """

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_negative_outside',
            'expression_form',
            'in_equations',
            'combined_operations',
            'word_problem',
            'word_problem_diverse',
            'word_problem_combined_ops'
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level and difficulty."""
        ranges = {
            8: {
                DifficultyLevel.EASY: {'base': (2, 5)},
                DifficultyLevel.MEDIUM: {'base': (2, 8)},
                DifficultyLevel.HARD: {'base': (2, 12)}
            },
            9: {
                DifficultyLevel.EASY: {'base': (2, 6)},
                DifficultyLevel.MEDIUM: {'base': (2, 10)},
                DifficultyLevel.HARD: {'base': (2, 15)}
            },
            10: {
                DifficultyLevel.EASY: {'base': (2, 8)},
                DifficultyLevel.MEDIUM: {'base': (2, 12)},
                DifficultyLevel.HARD: {'base': (2, 20)}
            }
        }
        lvl = self.level if self.level in ranges else 9
        return ranges[lvl][self.difficulty]

    def generate(self, seed=None, template: Optional[str] = None) -> Problem:
        """Generate a negative square root problem."""
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            template = random.choice(self.get_available_templates())

        # Generate based on template
        if template == 'basic_negative_outside':
            return self._generate_basic_negative_outside(seed)
        elif template == 'expression_form':
            return self._generate_expression_form(seed)
        elif template == 'in_equations':
            return self._generate_in_equations(seed)
        elif template == 'combined_operations':
            return self._generate_combined_operations(seed)
        elif template == 'word_problem':
            return self._generate_word_problem(seed)
        elif template == 'word_problem_diverse':
            return self._generate_word_problem_diverse(seed)
        elif template == 'word_problem_combined_ops':
            return self._generate_word_problem_combined_ops(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_negative_outside(self, seed=None) -> Problem:
        """Generate basic -√n problems."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        base = random.randint(ranges['base'][0], ranges['base'][1])
        radicand = base * base

        return Problem(
            text=f"What is -√{radicand}?",
            operands=[radicand],
            operation='negative_square_root',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'radicand': radicand,
                'base': base,
                'correct_answer': f"{-base}",
                'malrule_answer': 'No real solution',
                'template': 'basic_negative_outside'
            }
        )

    def _generate_expression_form(self, seed=None) -> Problem:
        """Generate -(√n) with explicit parentheses."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        base = random.randint(ranges['base'][0], ranges['base'][1])
        radicand = base * base

        return Problem(
            text=f"Evaluate: -(√{radicand})",
            operands=[radicand],
            operation='negative_square_root',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'radicand': radicand,
                'base': base,
                'correct_answer': f"{-base}",
                'malrule_answer': 'No real solution',
                'template': 'expression_form'
            }
        )

    def _generate_in_equations(self, seed=None) -> Problem:
        """Generate equations like x = -√25."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        base = random.randint(ranges['base'][0], ranges['base'][1])
        radicand = base * base

        return Problem(
            text=f"Solve for x: x = -√{radicand}",
            operands=[radicand],
            operation='negative_square_root',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'radicand': radicand,
                'base': base,
                'correct_answer': f"x = {-base}",
                'malrule_answer': 'No real solution',
                'template': 'in_equations'
            }
        )

    def _generate_combined_operations(self, seed=None) -> Problem:
        """Generate problems like -√4 + √9 or 2(-√16)."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        base1 = random.randint(ranges['base'][0], min(ranges['base'][1], 6))
        radicand1 = base1 * base1

        operations = ['addition', 'multiplication']
        operation = random.choice(operations)

        if operation == 'addition':
            base2 = random.randint(ranges['base'][0], min(ranges['base'][1], 6))
            radicand2 = base2 * base2
            text = f"Calculate: -√{radicand1} + √{radicand2}"
            correct_answer = f"{-base1 + base2}"
            metadata_extra = {'base2': base2, 'radicand2': radicand2, 'operation': 'addition'}
        else:  # multiplication
            coeff = random.randint(2, 4)
            text = f"Calculate: {coeff}(-√{radicand1})"
            correct_answer = f"{coeff * (-base1)}"
            metadata_extra = {'coefficient': coeff, 'operation': 'multiplication'}

        return Problem(
            text=text,
            operands=[radicand1],
            operation='negative_square_root',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'radicand': radicand1,
                'base': base1,
                'correct_answer': correct_answer,
                'malrule_answer': 'No real solution',
                'template': 'combined_operations',
                **metadata_extra
            }
        )

    def _generate_word_problem(self, seed=None) -> Problem:
        """Generate real-world word problem contexts."""
        if seed is not None:
            random.seed(seed)

        contexts = [
            {
                'text': 'The temperature dropped to {val} degrees below zero, which can be represented as -√{rad} degrees. What is the temperature?',
                'context_type': 'temperature',
                'answer_format': '{val} degrees'
            },
            {
                'text': 'A submarine is at a depth that can be modeled as -√{rad} meters. What is the depth?',
                'context_type': 'elevation',
                'answer_format': '{val} meters below sea level'
            },
            {
                'text': 'A debt amount is represented as -√{rad} dollars. What is the debt amount?',
                'context_type': 'debt',
                'answer_format': '${val} (debt)'
            }
        ]

        context = random.choice(contexts)
        ranges = self.get_value_ranges()
        base = random.randint(ranges['base'][0], min(ranges['base'][1], 10))
        radicand = base * base

        problem_text = context['text'].format(val=base, rad=radicand)
        correct_answer = context['answer_format'].format(val=-base)

        return Problem(
            text=problem_text,
            operands=[radicand],
            operation='negative_square_root',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'radicand': radicand,
                'base': base,
                'correct_answer': correct_answer,
                'malrule_answer': 'No real solution',
                'context_type': context['context_type'],
                'template': 'word_problem'
            }
        )

    def _generate_word_problem_diverse(self, seed=None) -> Problem:
        """Generate diverse real-world word problem contexts (3 variants)."""
        if seed is not None:
            random.seed(seed)

        # Three diverse context variants
        contexts = [
            {
                'type': 'banking',
                'text': 'A bank account shows a balance change of -√{rad} dollars after a transaction. What is the change in the account balance?',
                'answer_format': '-${val}'
            },
            {
                'type': 'physics_acceleration',
                'text': 'In a physics experiment, acceleration is measured as -√{rad} m/s². What is the acceleration value?',
                'answer_format': '-{val} m/s²'
            },
            {
                'type': 'stock_market',
                'text': 'A stock\'s price change is represented as -√{rad} points. What is the price change?',
                'answer_format': '-{val} points'
            }
        ]

        context = random.choice(contexts)
        ranges = self.get_value_ranges()
        base = random.randint(ranges['base'][0], min(ranges['base'][1], 10))
        radicand = base * base

        problem_text = context['text'].format(val=base, rad=radicand)
        correct_answer = context['answer_format'].format(val=base)

        return Problem(
            text=problem_text,
            operands=[radicand],
            operation='negative_square_root',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'radicand': radicand,
                'base': base,
                'correct_answer': correct_answer,
                'malrule_answer': 'No real solution',
                'context_type': context['type'],
                'template': 'word_problem_diverse',
                'problem_type': 'diverse_contexts'
            }
        )

    def _generate_word_problem_combined_ops(self, seed=None) -> Problem:
        """Generate word problems for combined operations (3 variants)."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        base1 = random.randint(ranges['base'][0], min(ranges['base'][1], 6))
        radicand1 = base1 * base1

        # Choose operation type
        operations = ['addition', 'multiplication']
        operation = random.choice(operations)

        if operation == 'addition':
            base2 = random.randint(ranges['base'][0], min(ranges['base'][1], 6))
            radicand2 = base2 * base2
            correct_val = -base1 + base2

            contexts = [
                {
                    'type': 'temperature_change',
                    'text': f'The temperature drops by √{radicand1} degrees and then rises by √{radicand2} degrees. What is the net temperature change? (Calculate: -√{radicand1} + √{radicand2})',
                    'answer_format': f'{correct_val} degrees'
                },
                {
                    'type': 'account_balance',
                    'text': f'An account has a withdrawal of √{radicand1} dollars and a deposit of √{radicand2} dollars. What is the net change? (Calculate: -√{radicand1} + √{radicand2})',
                    'answer_format': f'${correct_val}'
                },
                {
                    'type': 'elevation_change',
                    'text': f'A path descends √{radicand1} meters and then ascends √{radicand2} meters. What is the net elevation change? (Calculate: -√{radicand1} + √{radicand2})',
                    'answer_format': f'{correct_val} meters'
                }
            ]

            context = random.choice(contexts)
            correct_answer = context['answer_format']

            return Problem(
                text=context['text'],
                operands=[radicand1, radicand2],
                operation='negative_square_root',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'radicand': radicand1,
                    'radicand2': radicand2,
                    'base': base1,
                    'base2': base2,
                    'operation': 'addition',
                    'correct_answer': correct_answer,
                    'malrule_answer': 'No real solution',
                    'context_type': context['type'],
                    'template': 'word_problem_combined_ops',
                    'problem_type': 'combined_operations'
                }
            )
        else:  # multiplication
            coeff = random.randint(2, 4)
            correct_val = coeff * (-base1)

            contexts = [
                {
                    'type': 'scaled_loss',
                    'text': f'A loss of √{radicand1} dollars is multiplied by {coeff}. What is the total loss? (Calculate: {coeff}(-√{radicand1}))',
                    'answer_format': f'${correct_val} (loss)'
                },
                {
                    'type': 'velocity',
                    'text': f'An object has velocity -√{radicand1} m/s. If this velocity is scaled by a factor of {coeff}, what is the new velocity? (Calculate: {coeff}(-√{radicand1}))',
                    'answer_format': f'{correct_val} m/s'
                },
                {
                    'type': 'debt_multiple',
                    'text': f'A debt of √{radicand1} dollars is incurred {coeff} times. What is the total debt? (Calculate: {coeff}(-√{radicand1}))',
                    'answer_format': f'${correct_val} (debt)'
                }
            ]

            context = random.choice(contexts)
            correct_answer = context['answer_format']

            return Problem(
                text=context['text'],
                operands=[radicand1],
                operation='negative_square_root',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'radicand': radicand1,
                    'base': base1,
                    'coefficient': coeff,
                    'operation': 'multiplication',
                    'correct_answer': correct_answer,
                    'malrule_answer': 'No real solution',
                    'context_type': context['type'],
                    'template': 'word_problem_combined_ops',
                    'problem_type': 'combined_operations'
                }
            )
