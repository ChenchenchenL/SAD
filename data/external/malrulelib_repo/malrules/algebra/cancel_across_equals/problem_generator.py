"""
Problem generator for Cancel-Across-Equals malrule.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, List, Optional
from utils import ProblemGenerator, Problem, DifficultyLevel


class CancelAcrossEqualsProblemGenerator(ProblemGenerator):
    """Generates linear equations where terms appear on both sides."""

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_equation',
            'word_problem_context',
            'both_sides_constant',
            'three_term_equation',
            'comparison_problem'
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        ranges = {
            8: {DifficultyLevel.EASY: (2, 5), DifficultyLevel.MEDIUM: (2, 8), DifficultyLevel.HARD: (2, 10)},
            9: {DifficultyLevel.EASY: (2, 8), DifficultyLevel.MEDIUM: (2, 12), DifficultyLevel.HARD: (2, 15)},
            10: {DifficultyLevel.EASY: (2, 10), DifficultyLevel.MEDIUM: (2, 15), DifficultyLevel.HARD: (2, 20)},
        }
        lvl = self.level if self.level in ranges else 8
        return {'coefficients': ranges[lvl][self.difficulty]}

    def generate(self, seed=None, template: Optional[str] = None) -> Problem:
        """
        Generate a linear equation problem.

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
        if template == 'basic_equation':
            return self._generate_basic_equation(seed)
        elif template == 'word_problem_context':
            return self._generate_word_problem_context(seed)
        elif template == 'both_sides_constant':
            return self._generate_both_sides_constant(seed)
        elif template == 'three_term_equation':
            return self._generate_three_term_equation(seed)
        elif template == 'comparison_problem':
            return self._generate_comparison_problem(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_equation(self, seed=None) -> Problem:
        if seed is not None:
            random.seed(seed)

        coeff_range = self.get_value_ranges()['coefficients']
        min_c, max_c = coeff_range

        # Better strategy: Pick a, b, x_correct first, then calculate c
        # This ensures we control the correct answer and can verify malrule is different
        attempts = 0
        while attempts < 100:
            a = random.randint(min_c, max_c)
            b = random.randint(1, a - 1)
            x_correct = random.randint(1, max_c)

            # Calculate c from: (a-b)*x_correct = c
            c = (a - b) * x_correct

            # Malrule: x = c/a
            malrule_answer = c // a if c % a == 0 else c / a

            # Ensure different answers
            if malrule_answer != x_correct:
                correct_answer = x_correct
                # Ensure malrule is integer for cleaner problems
                if c % a == 0:
                    malrule_answer = c // a
                    break
            attempts += 1

        # Fallback if we somehow don't find good values
        if attempts >= 100:
            a = 3
            b = 2
            x_correct = 6
            c = (a - b) * x_correct
            correct_answer = x_correct
            malrule_answer = c // a

        text = f"Solve for x: {a}x = {b}x + {c}"

        return Problem(
            text=text,
            operands=[a, b, c],
            operation='solve_equation',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'a': a,
                'b': b,
                'c': c,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'basic_equation'
            }
        )

    def _generate_word_problem_context(self, seed=None) -> Problem:
        """
        Template 2: Word problem with real-world context.

        Generates word problems for ALL applicable formula types:
        - basic_equation: ax = bx + c
        - both_sides_constant: ax + d = bx + c
        - three_term_equation: ax = bx + cx + d

        Each formula type has 3 different question templates.
        """
        if seed is not None:
            random.seed(seed)

        # Select which formula type to embed in the word problem
        formula_types = ['basic_equation', 'both_sides_constant', 'three_term_equation']
        formula_type = random.choice(formula_types)

        # Generate the underlying equation for that formula type
        if formula_type == 'basic_equation':
            problem = self._generate_basic_equation(seed)
        elif formula_type == 'both_sides_constant':
            problem = self._generate_both_sides_constant(seed)
        else:  # three_term_equation
            problem = self._generate_three_term_equation(seed)

        # Get the equation parameters
        a = problem.metadata['a']
        b = problem.metadata['b']
        c = problem.metadata['c']
        d = problem.metadata.get('d', None)

        # Select one of 3 word problem templates for this formula type
        variant = random.randint(0, 2)

        if formula_type == 'basic_equation':
            # Formula: ax = bx + c
            # Three different contexts for this formula
            templates = [
                # Variant 0: Bags of items
                "Maria has {a} bags with x apples each. John has {b} bags with x apples each plus {c} extra apples. If they have the same number of apples, find the value of x.",
                # Variant 1: Speed/distance
                "Car A travels at {a}x mph for 1 hour. Car B travels at {b}x mph for 1 hour and then {c} additional miles. If they travel the same total distance, find x.",
                # Variant 2: Money
                "Store A sells {a}x dollars worth of goods. Store B sells {b}x dollars worth of goods plus an additional ${c}. If their sales are equal, find x."
            ]
            problem.text = templates[variant].format(a=a, b=b, c=c)

        elif formula_type == 'both_sides_constant':
            # Formula: ax + d = bx + c
            # Three different contexts for this formula
            templates = [
                # Variant 0: Tank filling
                "Tank A fills at {a}x liters per minute and starts with {d} liters. Tank B fills at {b}x liters per minute and starts with {c} liters. After how many minutes (x) will both tanks have the same volume?",
                # Variant 1: Money accumulation
                "Alice saves ${a}x per week and currently has ${d}. Bob saves ${b}x per week and currently has ${c}. After how many weeks (x) will they have the same amount?",
                # Variant 2: Distance traveled
                "Runner A runs at {a}x meters per minute and has a {d} meter head start. Runner B runs at {b}x meters per minute and has a {c} meter head start. After how many minutes (x) will they be at the same position?"
            ]
            problem.text = templates[variant].format(a=a, b=b, c=c, d=d)

        else:  # three_term_equation
            # Formula: ax = bx + cx + d
            # Three different contexts for this formula
            templates = [
                # Variant 0: Combining resources
                "Team A has {a}x points. Team B has {b}x points, Team C has {c}x points, and they share {d} bonus points. If Team A's total equals Team B and C's combined total, find x.",
                # Variant 1: Production
                "Factory A produces {a}x units. Factory B produces {b}x units, Factory C produces {c}x units, and there are {d} units in storage. If Factory A's production equals Factory B + C's production plus storage, find x.",
                # Variant 2: Weight distribution
                "Box A weighs {a}x kg. Box B weighs {b}x kg, Box C weighs {c}x kg, and there's {d} kg of packing material. If Box A's weight equals the combined weight of B, C, and packing, find x."
            ]
            problem.text = templates[variant].format(a=a, b=b, c=c, d=d)

        # Update metadata to track word problem details
        problem.metadata['template'] = 'word_problem_context'
        problem.metadata['word_problem_type'] = formula_type
        problem.metadata['word_problem_variant'] = variant

        return problem

    def _generate_both_sides_constant(self, seed=None) -> Problem:
        """Template 3: Equation with constants on both sides (ax + d = bx + c)."""
        if seed is not None:
            random.seed(seed)

        coeff_range = self.get_value_ranges()['coefficients']
        min_c, max_c = coeff_range

        # Generate equation: ax + d = bx + c where a > b
        a = random.randint(min_c, max_c)
        b = random.randint(min_c // 2, a - 1)
        c = random.randint(1, max_c)
        d = random.randint(1, max_c)

        # Correct answer: ax + d = bx + c → (a-b)x = c - d → x = (c-d)/(a-b)
        numerator = c - d
        denominator = a - b

        # Ensure integer solution
        attempts = 0
        while (denominator == 0 or numerator % denominator != 0) and attempts < 20:
            a = random.randint(min_c, max_c)
            b = random.randint(1, a - 1)
            factor = a - b
            x_val = random.randint(1, max_c // 2)
            c = random.randint(1, max_c)
            d = c - factor * x_val  # Ensure c - d = factor * x_val
            numerator = c - d
            denominator = a - b
            attempts += 1

        correct_answer = numerator // denominator if denominator != 0 else 0

        # Malrule: Student "cancels" x terms → a + d = c (treating as if x disappeared)
        # Then: d - c = -a, but more likely they just ignore the x and solve what's left incorrectly
        # Most common: cancel bx → ax + d = c → x = (c - d) / a
        malrule_answer = (c - d) // a if a != 0 and (c - d) % a == 0 else None

        # Adjust if needed
        if malrule_answer is None or malrule_answer == correct_answer:
            # Regenerate with better values
            x_val = random.randint(1, max_c // 2)
            a = random.randint(3, max_c)
            b = random.randint(1, a - 2)
            c = random.randint(5, max_c)
            d = c - (a - b) * x_val
            correct_answer = x_val
            malrule_answer = (c - d) // a

        text = f"Solve for x: {a}x + {d} = {b}x + {c}"

        return Problem(
            text=text,
            operands=[a, d, b, c],
            operation='solve_equation',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'a': a,
                'b': b,
                'c': c,
                'd': d,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'both_sides_constant'
            }
        )

    def _generate_three_term_equation(self, seed=None) -> Problem:
        """Template 4: Three-term equation (ax = bx + cx + d)."""
        if seed is not None:
            random.seed(seed)

        coeff_range = self.get_value_ranges()['coefficients']
        min_c, max_c = coeff_range

        # Generate: ax = bx + cx + d where a > b + c
        a = random.randint(min_c + 2, max_c)
        b = random.randint(1, (a - 1) // 2)
        c_coeff = random.randint(1, a - b - 1)
        d = random.randint(1, max_c)

        # Correct: ax = bx + cx + d → (a - b - c)x = d → x = d / (a - b - c)
        denominator = a - b - c_coeff

        # Ensure integer solution
        attempts = 0
        while (denominator <= 0 or d % denominator != 0) and attempts < 20:
            a = random.randint(min_c + 2, max_c)
            b = random.randint(1, (a - 2) // 2)
            c_coeff = random.randint(1, a - b - 1)
            factor = a - b - c_coeff
            x_val = random.randint(1, max_c // 2)
            d = factor * x_val
            denominator = a - b - c_coeff
            attempts += 1

        correct_answer = d // denominator if denominator > 0 else 0

        # Malrule: Student "cancels" bx and cx → ax = d → x = d / a
        malrule_answer = d // a if d % a == 0 else None

        if malrule_answer is None:
            d = a * random.randint(1, max_c // 2)
            malrule_answer = d // a
            # Recalculate correct
            correct_answer = d // (a - b - c_coeff) if (a - b - c_coeff) > 0 else d

        text = f"Solve for x: {a}x = {b}x + {c_coeff}x + {d}"

        return Problem(
            text=text,
            operands=[a, b, c_coeff, d],
            operation='solve_equation',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'a': a,
                'b': b,
                'c': c_coeff,
                'd': d,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'three_term_equation'
            }
        )

    def _generate_comparison_problem(self, seed=None) -> Problem:
        """Template 5: Compare two equation solutions."""
        value_range = self.get_value_ranges()['coefficients']
        min_c, max_c = value_range

        # Retry until we get different correct and malrule answers
        attempts = 0
        while attempts < 100:
            if seed is not None:
                random.seed(seed + attempts)

            # Generate two equations
            # Equation 1: a1*x = b1*x + c1
            a1 = random.randint(min_c, max_c)
            b1 = random.randint(1, a1 - 1)
            c1 = (a1 - b1) * random.randint(1, max_c // 2)
            correct1 = c1 // (a1 - b1)
            malrule1 = c1 // a1 if c1 % a1 == 0 else c1 / a1

            # Equation 2: a2*x = b2*x + c2
            a2 = random.randint(min_c, max_c)
            b2 = random.randint(1, a2 - 1)
            c2 = (a2 - b2) * random.randint(1, max_c // 2)
            correct2 = c2 // (a2 - b2)

            # Determine comparison
            if correct1 > correct2:
                correct_answer = f"{a1}x = {b1}x + {c1} has larger solution"
            elif correct1 < correct2:
                correct_answer = f"{a2}x = {b2}x + {c2} has larger solution"
            else:
                correct_answer = "Both have equal solutions"

            if malrule1 > correct2:
                malrule_answer = f"{a1}x = {b1}x + {c1} has larger solution"
            elif malrule1 < correct2:
                malrule_answer = f"{a2}x = {b2}x + {c2} has larger solution"
            else:
                malrule_answer = "Both have equal solutions"

            # Ensure answers differ
            if correct_answer != malrule_answer:
                break
            attempts += 1

        text = f"Which equation has a larger solution for x: {a1}x = {b1}x + {c1} or {a2}x = {b2}x + {c2}?"

        return Problem(
            text=text,
            operands=[a1, b1, c1, a2, b2, c2],
            operation='solve_equation',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'a': a1,
                'b': b1,
                'c': c1,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'comparison_problem'
            }
        )
