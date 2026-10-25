"""
Problem generator for Inequality-Direction-Confusion malrule.

Generates absolute value inequality problems where students confuse
the solution patterns for less than and greater than cases.
"""

import random
import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, Tuple, Optional, List
from utils import Problem, ProblemGenerator, DifficultyLevel


class InequalityDirectionConfusionProblemGenerator(ProblemGenerator):
    """
    Generates absolute value inequality problems.

    Templates:
    1. less_than - Simple |x| < k
    2. greater_than - Simple |x| > k
    3. compound_inequality - |x - h| < k (with offset)
    4. inequality_with_coefficient - |ax| > k (with coefficient)
    5. less_than_or_equal - |x| ≤ k (with ≤)
    6. word_problem_context - Real-world distance problems
    """

    def get_name(self) -> str:
        return "Inequality-Direction-Confusion Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates absolute value inequality problems where students may confuse "
            "the solution patterns for 'less than' (inside interval) versus 'greater than' "
            "(outside interval) cases."
        )

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        templates = ['less_than', 'greater_than']

        # Add enhanced problem types for higher levels
        if self.level >= 9:
            templates.extend([
                'compound_inequality',        # |x - h| < k (with offset)
                'inequality_with_coefficient', # |ax| > k (with coefficient)
                'less_than_or_equal',         # |x| ≤ k (with ≤)
                'word_problem_context',       # Real-world distance problems
            ])

        return templates

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Return the value ranges for problem generation."""
        ranges = {
            6: {
                DifficultyLevel.EASY: (2, 5),
                DifficultyLevel.MEDIUM: (2, 8),
                DifficultyLevel.HARD: (2, 10),
            },
            7: {
                DifficultyLevel.EASY: (2, 6),
                DifficultyLevel.MEDIUM: (2, 10),
                DifficultyLevel.HARD: (2, 12),
            },
            8: {
                DifficultyLevel.EASY: (2, 8),
                DifficultyLevel.MEDIUM: (2, 12),
                DifficultyLevel.HARD: (2, 15),
            },
            9: {
                DifficultyLevel.EASY: (2, 8),
                DifficultyLevel.MEDIUM: (2, 15),
                DifficultyLevel.HARD: (2, 20),
            },
            10: {
                DifficultyLevel.EASY: (2, 10),
                DifficultyLevel.MEDIUM: (2, 15),
                DifficultyLevel.HARD: (2, 20),
            }
        }

        lvl = self.level if self.level in ranges else 8
        return {'bound': ranges[lvl][self.difficulty]}

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate an absolute value inequality problem.

        Args:
            seed: Optional random seed for reproducibility
            template: Optional template name to use

        Returns:
            Problem with absolute value inequality
        """
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            template = random.choice(self.get_available_templates())

        # Generate based on template
        if template == 'less_than':
            return self._generate_less_than(seed)
        elif template == 'greater_than':
            return self._generate_greater_than(seed)
        elif template == 'compound_inequality':
            return self._generate_compound_inequality(seed)
        elif template == 'inequality_with_coefficient':
            return self._generate_inequality_with_coefficient(seed)
        elif template == 'less_than_or_equal':
            return self._generate_less_than_or_equal(seed)
        elif template == 'word_problem_context':
            return self._generate_word_problem_context(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_less_than(self, seed=None) -> Problem:
        """Generate |x| < bound problem."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        bound = random.randint(*ranges['bound'])

        problem_statement = f"Solve: |x| < {bound}"
        correct_answer = f"-{bound} < x < {bound}"
        # Student applies greater than logic: x < -bound OR x > bound
        malrule_answer = f"x < -{bound} OR x > {bound}"

        metadata = {
            'bound': bound,
            'inequality_type': 'less_than',
            'problem_type': 'less_than',
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer
        }

        return Problem(
            text=problem_statement,
            operands=[bound],
            operation='absolute_value_inequality',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_greater_than(self, seed=None) -> Problem:
        """Generate |x| > bound problem."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        bound = random.randint(*ranges['bound'])

        problem_statement = f"Solve: |x| > {bound}"
        correct_answer = f"x < -{bound} OR x > {bound}"
        # Student applies less than logic: -bound < x < bound
        malrule_answer = f"-{bound} < x < {bound}"

        metadata = {
            'bound': bound,
            'inequality_type': 'greater_than',
            'problem_type': 'greater_than',
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer
        }

        return Problem(
            text=problem_statement,
            operands=[bound],
            operation='absolute_value_inequality',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_compound_inequality(self, seed=None) -> Problem:
        """Generate |x - h| < k problem."""
        if seed is not None:
            random.seed(seed)

        h = random.randint(3, 8)
        k = random.randint(2, 6)

        problem_statement = f"Solve: |x - {h}| < {k}"
        correct_answer = f"{h - k} < x < {h + k}"
        # Student confuses and applies greater than pattern
        malrule_answer = f"x < {h - k} OR x > {h + k}"

        metadata = {
            'bound': k,
            'offset': h,
            'inequality_type': 'less_than',
            'problem_type': 'compound_inequality',
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer
        }

        return Problem(
            text=problem_statement,
            operands=[h, k],
            operation='absolute_value_inequality',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_inequality_with_coefficient(self, seed=None) -> Problem:
        """Generate |ax| > k problem."""
        if seed is not None:
            random.seed(seed)

        a = random.choice([2, 3, 4, 5])
        k = random.choice([4, 6, 8, 10, 12])

        problem_statement = f"Solve: |{a}x| > {k}"
        correct_answer = f"x < -{k//a} OR x > {k//a}"
        # Student confuses and applies less than pattern
        malrule_answer = f"-{k//a} < x < {k//a}"

        metadata = {
            'coefficient': a,
            'bound': k,
            'inequality_type': 'greater_than',
            'problem_type': 'inequality_with_coefficient',
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer
        }

        return Problem(
            text=problem_statement,
            operands=[a, k],
            operation='absolute_value_inequality',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_less_than_or_equal(self, seed=None) -> Problem:
        """Generate |x| ≤ bound problem."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        bound = random.randint(*ranges['bound'])

        problem_statement = f"Solve: |x| ≤ {bound}"
        correct_answer = f"-{bound} ≤ x ≤ {bound}"
        # Student applies greater than pattern with ≥
        malrule_answer = f"x ≤ -{bound} OR x ≥ {bound}"

        metadata = {
            'bound': bound,
            'inequality_type': 'less_than',
            'problem_type': 'less_than_or_equal',
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer
        }

        return Problem(
            text=problem_statement,
            operands=[bound],
            operation='absolute_value_inequality',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_word_problem_context(self, seed=None) -> Problem:
        """Generate word problems with absolute value inequality contexts."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        bound = random.randint(*ranges['bound'])

        # Select which formula type to embed
        word_formula_types = ['basic_less', 'basic_greater', 'compound_less', 'coefficient_greater', 'less_equal']
        word_formula_type = random.choice(word_formula_types)

        if word_formula_type == 'basic_less':
            return self._generate_word_basic_less(seed, bound)
        elif word_formula_type == 'basic_greater':
            return self._generate_word_basic_greater(seed, bound)
        elif word_formula_type == 'compound_less':
            return self._generate_word_compound_less(seed, bound)
        elif word_formula_type == 'coefficient_greater':
            return self._generate_word_coefficient_greater(seed, bound)
        else:  # less_equal
            return self._generate_word_less_equal(seed, bound)

    def _generate_word_basic_less(self, seed, bound) -> Problem:
        """Generate word problem for |x| < bound."""
        if seed is not None:
            random.seed(seed)

        contexts = [
            (f"The distance between two points must be less than {bound} units. If one point is at the origin, write an inequality for the position x of the other point.",
             f"|x| < {bound}", f"-{bound} < x < {bound}", f"x < -{bound} OR x > {bound}"),
            (f"A measurement error must be within {bound} units. If the error is x, what values of x are acceptable? Solve |x| < {bound}.",
             f"|x| < {bound}", f"-{bound} < x < {bound}", f"x < -{bound} OR x > {bound}"),
            (f"A particle's position x must be within {bound} meters of the origin. What values of x satisfy this? Solve |x| < {bound}.",
             f"|x| < {bound}", f"-{bound} < x < {bound}", f"x < -{bound} OR x > {bound}"),
        ]

        context_text, symbolic, correct_answer, malrule_answer = random.choice(contexts)

        metadata = {
            'bound': bound,
            'inequality_type': 'less_than',
            'problem_type': 'word_problem_context',
            'word_problem_type': 'basic_less',
            'symbolic_form': symbolic,
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer,
            'context': 'word_problem'
        }

        return Problem(
            text=context_text,
            operands=[bound],
            operation='absolute_value_inequality',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_word_basic_greater(self, seed, bound) -> Problem:
        """Generate word problem for |x| > bound."""
        if seed is not None:
            random.seed(seed)

        contexts = [
            (f"A particle must be more than {bound} units away from the origin. If the position is x, solve |x| > {bound}. What are the valid positions?",
             f"|x| > {bound}", f"x < -{bound} OR x > {bound}", f"-{bound} < x < {bound}"),
            (f"A sensor triggers when the reading x deviates by more than {bound} from zero. Solve |x| > {bound}. When does it trigger?",
             f"|x| > {bound}", f"x < -{bound} OR x > {bound}", f"-{bound} < x < {bound}"),
            (f"A quality control system rejects parts when |x| > {bound}, where x is deviation from target. What values are rejected?",
             f"|x| > {bound}", f"x < -{bound} OR x > {bound}", f"-{bound} < x < {bound}"),
        ]

        context_text, symbolic, correct_answer, malrule_answer = random.choice(contexts)

        metadata = {
            'bound': bound,
            'inequality_type': 'greater_than',
            'problem_type': 'word_problem_context',
            'word_problem_type': 'basic_greater',
            'symbolic_form': symbolic,
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer,
            'context': 'word_problem'
        }

        return Problem(
            text=context_text,
            operands=[bound],
            operation='absolute_value_inequality',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_word_compound_less(self, seed, bound) -> Problem:
        """Generate word problem for |x - h| < k."""
        if seed is not None:
            random.seed(seed)

        h = random.randint(3, 8)
        k = random.randint(2, 6)

        contexts = [
            (f"A thermometer's reading x is accurate to within {k} degrees of the actual temperature {h}°C. Solve |x - {h}| < {k}. What readings are accurate?",
             f"|x - {h}| < {k}", f"{h - k} < x < {h + k}", f"x < {h - k} OR x > {h + k}"),
            (f"A machine part length x must be within {k} mm of the target {h} mm. Solve |x - {h}| < {k}. What lengths are acceptable?",
             f"|x - {h}| < {k}", f"{h - k} < x < {h + k}", f"x < {h - k} OR x > {h + k}"),
            (f"A car's position x must stay within {k} meters of the checkpoint at {h} meters. Solve |x - {h}| < {k}. What positions are valid?",
             f"|x - {h}| < {k}", f"{h - k} < x < {h + k}", f"x < {h - k} OR x > {h + k}"),
        ]

        context_text, symbolic, correct_answer, malrule_answer = random.choice(contexts)

        metadata = {
            'bound': k,
            'offset': h,
            'inequality_type': 'less_than',
            'problem_type': 'word_problem_context',
            'word_problem_type': 'compound_less',
            'symbolic_form': symbolic,
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer,
            'context': 'word_problem'
        }

        return Problem(
            text=context_text,
            operands=[h, k],
            operation='absolute_value_inequality',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_word_coefficient_greater(self, seed, bound) -> Problem:
        """Generate word problem for |ax| > k."""
        if seed is not None:
            random.seed(seed)

        a = random.choice([2, 3, 4, 5])
        k = random.choice([4, 6, 8, 10, 12])

        contexts = [
            (f"A machine runs at speed x for {a} hours. The distance must exceed {k} km. Solve |{a}x| > {k}. What speeds work?",
             f"|{a}x| > {k}", f"x < -{k//a} OR x > {k//a}", f"-{k//a} < x < {k//a}"),
            (f"A spring compressed to position x creates force {a}x. The force magnitude must exceed {k}N. Solve |{a}x| > {k}. What positions work?",
             f"|{a}x| > {k}", f"x < -{k//a} OR x > {k//a}", f"-{k//a} < x < {k//a}"),
            (f"A signal amplified by factor {a} has strength |{a}x|. It must exceed {k} units. Solve |{a}x| > {k}. What input x works?",
             f"|{a}x| > {k}", f"x < -{k//a} OR x > {k//a}", f"-{k//a} < x < {k//a}"),
        ]

        context_text, symbolic, correct_answer, malrule_answer = random.choice(contexts)

        metadata = {
            'coefficient': a,
            'bound': k,
            'inequality_type': 'greater_than',
            'problem_type': 'word_problem_context',
            'word_problem_type': 'coefficient_greater',
            'symbolic_form': symbolic,
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer,
            'context': 'word_problem'
        }

        return Problem(
            text=context_text,
            operands=[a, k],
            operation='absolute_value_inequality',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_word_less_equal(self, seed, bound) -> Problem:
        """Generate word problem for |x| ≤ bound."""
        if seed is not None:
            random.seed(seed)

        contexts = [
            (f"A tolerance specification allows deviation up to and including {bound} units. Solve |x| ≤ {bound}. What values are within tolerance?",
             f"|x| ≤ {bound}", f"-{bound} ≤ x ≤ {bound}", f"x ≤ -{bound} OR x ≥ {bound}"),
            (f"A temperature x can vary by at most {bound} degrees (inclusive) from zero. Solve |x| ≤ {bound}. What temperatures are allowed?",
             f"|x| ≤ {bound}", f"-{bound} ≤ x ≤ {bound}", f"x ≤ -{bound} OR x ≥ {bound}"),
            (f"A balance x must not exceed {bound} dollars in magnitude (can equal). Solve |x| ≤ {bound}. What balances are valid?",
             f"|x| ≤ {bound}", f"-{bound} ≤ x ≤ {bound}", f"x ≤ -{bound} OR x ≥ {bound}"),
        ]

        context_text, symbolic, correct_answer, malrule_answer = random.choice(contexts)

        metadata = {
            'bound': bound,
            'inequality_type': 'less_than',
            'problem_type': 'word_problem_context',
            'word_problem_type': 'less_equal',
            'symbolic_form': symbolic,
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer,
            'context': 'word_problem'
        }

        return Problem(
            text=context_text,
            operands=[bound],
            operation='absolute_value_inequality',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )
