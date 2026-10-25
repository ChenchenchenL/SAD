"""
Problem generator for Square-Root-Equals-Plus-Minus malrule.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, List, Optional
from utils import ProblemGenerator, Problem, DifficultyLevel


class SquareRootEqualsPlusMinusProblemGenerator(ProblemGenerator):
    """Generates square root problems with perfect squares."""

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        ranges = {
            7: {DifficultyLevel.EASY: (1, 10), DifficultyLevel.MEDIUM: (1, 15), DifficultyLevel.HARD: (1, 20)},
            8: {DifficultyLevel.EASY: (1, 12), DifficultyLevel.MEDIUM: (1, 20), DifficultyLevel.HARD: (1, 25)},
            9: {DifficultyLevel.EASY: (1, 15), DifficultyLevel.MEDIUM: (1, 25), DifficultyLevel.HARD: (1, 30)},
            10: {DifficultyLevel.EASY: (1, 20), DifficultyLevel.MEDIUM: (1, 30), DifficultyLevel.HARD: (1, 40)},
        }
        lvl = self.level if self.level in ranges else 8
        return {'base': ranges[lvl][self.difficulty]}

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_square_root',
            'equation_vs_expression',
            'negative_radicand_squared',
            'expression_simplification',
            'word_problem_context',
            'word_problem_non_area',
            'word_problem_equation_vs_expression'
        ]

    def generate(self, seed=None, template: Optional[str] = None) -> Problem:
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            # Choose problem type
            problem_types = ['basic_square_root']

            # Add enhanced problem types for higher levels
            if self.level >= 8:
                problem_types.extend([
                    'equation_vs_expression',    # Contrasting √x² vs solving x² = n
                    'negative_radicand_squared',  # √((-x)²) scenarios
                    'expression_simplification',  # √(x²+6x+9) where x is given
                    'word_problem_context',       # Real-world positive-only contexts
                    'word_problem_non_area',      # Non-area contexts
                    'word_problem_equation_vs_expression'  # Equation vs expression word problems
                ])

            template = random.choice(problem_types)

        # Route to new template handlers
        if template == 'word_problem_non_area':
            return self._generate_word_problem_non_area(seed)
        elif template == 'word_problem_equation_vs_expression':
            return self._generate_word_problem_equation_vs_expression(seed)

        base_range = self.get_value_ranges()['base']
        min_base, max_base = base_range

        problem_type = template

        # Handle enhanced problem types first
        if problem_type == 'equation_vs_expression':
            # Contrast evaluating √n vs solving x² = n
            base = random.randint(min_base, max_base)
            radicand = base * base

            contexts = [
                f"Evaluate √{radicand}",
                f"Simplify √{radicand}",
                f"What is √{radicand}?",
            ]
            text = random.choice(contexts)

            note = f" (Note: This is different from solving x² = {radicand})"

            return Problem(
                text=text + note,
                operands=[radicand],
                operation='sqrt_vs_equation',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'radicand': radicand,
                    'base': base,
                    'problem_type': problem_type,
                    'correct_answer': base,
                    'malrule_answer': -base,
                    'equation_solution': f"±{base}"
                }
            )

        elif problem_type == 'negative_radicand_squared':
            # Problems like √((-5)²) = 5, not -5
            base = random.randint(min_base, max_base)
            radicand = base * base

            text = f"Evaluate √((-{base})²)"

            return Problem(
                text=text,
                operands=[base],
                operation='sqrt_negative_squared',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'base': base,
                    'radicand': radicand,
                    'problem_type': problem_type,
                    'correct_answer': base,  # Always positive
                    'malrule_answer': -base  # Student incorrectly keeps negative
                }
            )

        elif problem_type == 'expression_simplification':
            # Perfect square trinomial like √(x²+6x+9) = √((x+3)²)
            # We'll use simple cases where we can evaluate
            base = random.randint(2, 6)  # Keep smaller for tractability

            # Generate (x+k)² type expressions
            k = random.randint(1, 5)
            x_val = random.randint(1, 8)

            # (x+k)² = x² + 2kx + k²
            expression_value = (x_val + k) ** 2

            text = f"If x = {x_val}, evaluate √(x² + {2*k}x + {k*k})"

            return Problem(
                text=text,
                operands=[x_val, k],
                operation='sqrt_expression_eval',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'x_value': x_val,
                    'k': k,
                    'expression_value': expression_value,
                    'problem_type': problem_type,
                    'correct_answer': x_val + k,  # Positive only
                    'malrule_answer': -(x_val + k)  # Student includes negative
                }
            )

        elif problem_type == 'word_problem_context':
            # Real-world contexts where negative doesn't make sense
            base = random.randint(min_base, min(max_base, 15))
            area = base * base

            contexts = [
                (f"A square garden has area {area} square meters. What is the side length?", "garden"),
                (f"A square tile covers {area} square inches. What is the length of one side?", "tile"),
                (f"The area of a square photograph is {area} square cm. Find the side length.", "photo"),
            ]

            context_text, context_type = random.choice(contexts)

            return Problem(
                text=context_text,
                operands=[area],
                operation='sqrt_word_problem',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'area': area,
                    'base': base,
                    'problem_type': problem_type,
                    'context': context_type,
                    'correct_answer': base,  # Only positive makes sense
                    'malrule_answer': -base  # Student incorrectly includes negative
                }
            )

        # Original basic problem type
        # Generate perfect square
        base = random.randint(min_base, max_base)
        radicand = base * base  # Perfect square

        # Correct answer: √n is always positive (principal root)
        correct_answer = base

        # Malrule answer: Student thinks √n = ±base
        # We'll represent this as a tuple or string, but for testing
        # we'll use the negative value as the malrule answer
        malrule_answer = -base  # Student includes negative

        text = f"Evaluate: √{radicand}"

        return Problem(
            text=text,
            operands=[radicand],
            operation='square_root',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'radicand': radicand,
                'base': base,
                'problem_type': problem_type,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer
            }
        )

    def _generate_word_problem_non_area(self, seed: Optional[int] = None) -> Problem:
        """Generate word problems with non-area contexts where positive-only matters (3 variants)."""
        if seed is not None:
            random.seed(seed)

        base_range = self.get_value_ranges()['base']
        min_base, max_base = base_range
        base = random.randint(min_base, min(max_base, 15))
        radicand = base * base

        # Three context variants where negative doesn't make sense
        contexts = [
            {
                'type': 'speed',
                'text': f"A car's speed squared is {radicand} (km/h)². What is the actual speed? (Calculate √{radicand})",
                'answer_unit': 'km/h'
            },
            {
                'type': 'population',
                'text': f"A population model gives P² = {radicand} where P is the population in thousands. What is the population P? (Calculate √{radicand})",
                'answer_unit': 'thousand people'
            },
            {
                'type': 'distance',
                'text': f"The distance traveled squared equals {radicand} meters². What is the actual distance? (Calculate √{radicand})",
                'answer_unit': 'meters'
            }
        ]

        context = random.choice(contexts)

        return Problem(
            text=context['text'],
            operands=[radicand],
            operation='sqrt_word_problem',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_non_area',
                'context_type': context['type'],
                'problem_type': 'non_area_context',
                'radicand': radicand,
                'base': base,
                'correct_answer': f"{base} {context['answer_unit']}",
                'malrule_answer': f"±{base} {context['answer_unit']}"
            }
        )

    def _generate_word_problem_equation_vs_expression(self, seed: Optional[int] = None) -> Problem:
        """Generate word problems showing equation vs expression distinction (3 variants)."""
        if seed is not None:
            random.seed(seed)

        base_range = self.get_value_ranges()['base']
        min_base, max_base = base_range
        base = random.randint(min_base, min(max_base, 15))
        radicand = base * base

        # Three context variants emphasizing expression evaluation
        contexts = [
            {
                'type': 'measurement',
                'text': f"A measurement device shows √{radicand} as the reading. What is the measurement value? (Note: We are evaluating √{radicand}, not solving x² = {radicand})",
                'answer_unit': 'units'
            },
            {
                'type': 'formula_evaluation',
                'text': f"A formula gives the result as √{radicand}. Calculate this value. (Remember: This is evaluating an expression, not solving an equation)",
                'answer_unit': 'units'
            },
            {
                'type': 'calculation',
                'text': f"Simplify the expression √{radicand} to find the exact value. (This is different from finding all solutions to x² = {radicand})",
                'answer_unit': 'units'
            }
        ]

        context = random.choice(contexts)

        return Problem(
            text=context['text'],
            operands=[radicand],
            operation='sqrt_vs_equation',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'template': 'word_problem_equation_vs_expression',
                'context_type': context['type'],
                'problem_type': 'equation_vs_expression_word',
                'radicand': radicand,
                'base': base,
                'correct_answer': f"{base}",
                'malrule_answer': f"±{base}",
                'equation_solution': f"±{base}"
            }
        )
