"""
Problem generator for Zero-Exponent-Equals-Zero malrule.
"""

import random
import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, Tuple, Optional, List
from utils import Problem, ProblemGenerator, DifficultyLevel


class ZeroExponentEqualsZeroProblemGenerator(ProblemGenerator):
    """
    Generates problems with zero exponents.

    Templates:
    1. basic_zero_exponent - Simple a^0 evaluation
    2. expression_simplification - Simplifying expressions with zero exponents
    3. exponent_rules - Using exponent division rules
    4. polynomial_evaluation - Evaluating polynomials with zero exponents
    5. word_problem - Real-world contexts with zero exponents
    """

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_zero_exponent',
            'expression_simplification',
            'exponent_rules',
            'polynomial_evaluation',
            'word_problem',  # Old word problem (kept for backwards compatibility)
            'word_problem_context'  # NEW: Covers all formula types with 3 variants each
        ]

    def get_value_ranges(self):
        """Return the value ranges for problem generation."""
        if self.difficulty == DifficultyLevel.EASY:
            return {'base': (2, 5), 'coefficient': (1, 5), 'power': (2, 4)}
        elif self.difficulty == DifficultyLevel.MEDIUM:
            return {'base': (2, 10), 'coefficient': (1, 10), 'power': (2, 6)}
        else:  # HARD
            return {'base': (2, 20), 'coefficient': (1, 15), 'power': (2, 8)}

    def generate(self, seed=None, template: Optional[str] = None):
        """
        Generate a zero exponent problem.

        Args:
            seed: Optional random seed for reproducibility
            template: Optional template name

        Returns:
            Problem with zero exponent
        """
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            template = random.choice(self.get_available_templates())

        # Generate based on template
        if template == 'basic_zero_exponent':
            return self._generate_basic_zero_exponent(seed)
        elif template == 'expression_simplification':
            return self._generate_expression_simplification(seed)
        elif template == 'exponent_rules':
            return self._generate_exponent_rules(seed)
        elif template == 'polynomial_evaluation':
            return self._generate_polynomial_evaluation(seed)
        elif template == 'word_problem':
            return self._generate_word_problem(seed)
        elif template == 'word_problem_context':
            return self._generate_word_problem_context(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_zero_exponent(self, seed=None) -> Problem:
        """
        Generate basic zero exponent problem (original template).

        Example: 5^0
        Correct: 1
        Malrule: 0
        """
        if seed is not None:
            random.seed(seed)

        # Get value ranges based on difficulty
        ranges = self.get_value_ranges()

        # Generate base (non-zero, since 0^0 is undefined)
        base = random.randint(ranges['base'][0], ranges['base'][1])

        # Exponent is always 0 for this malrule
        exponent = 0

        # Correct answer is always 1 (for any non-zero base)
        correct_answer = 1

        # Malrule: student thinks a^0 = 0
        malrule_answer = 0

        problem_statement = f"Evaluate: {base}^0"

        metadata = {
            'base': base,
            'exponent': exponent,
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer,
            'template': 'basic_zero_exponent'
        }

        return Problem(
            text=problem_statement,
            operands=[base, exponent],
            operation='zero_exponent',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_expression_simplification(self, seed=None) -> Problem:
        """
        Generate expression simplification with zero exponents.

        Example: Simplify 3x^0 or (5y)^0
        Correct: 3(1) = 3, or (5y)^0 = 1
        Malrule: 3(0) = 0, or (5y)^0 = 0
        """
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()

        # Choose between coefficient * x^0 or (expression)^0
        expression_type = random.choice(['coefficient_times', 'parentheses'])

        if expression_type == 'coefficient_times':
            # Format: ax^0
            coefficient = random.randint(ranges['coefficient'][0], ranges['coefficient'][1])
            variable = random.choice(['x', 'y', 'z', 'n'])

            problem_text = f"Simplify: {coefficient}{variable}^0"

            # Correct: ax^0 = a * 1 = a
            correct_answer = coefficient
            # Malrule: ax^0 = a * 0 = 0
            malrule_answer = 0

            metadata = {
                'coefficient': coefficient,
                'variable': variable,
                'expression_type': 'coefficient_times',
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'expression_simplification'
            }
            operands = [coefficient, 0]

        else:  # parentheses
            # Format: (ax)^0
            coefficient = random.randint(ranges['coefficient'][0], ranges['coefficient'][1])
            variable = random.choice(['x', 'y', 'z', 'n'])

            problem_text = f"Simplify: ({coefficient}{variable})^0"

            # Correct: (ax)^0 = 1
            correct_answer = 1
            # Malrule: (ax)^0 = 0
            malrule_answer = 0

            metadata = {
                'coefficient': coefficient,
                'variable': variable,
                'expression_type': 'parentheses',
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'expression_simplification'
            }
            operands = [coefficient, 0]

        return Problem(
            text=problem_text,
            operands=operands,
            operation='zero_exponent',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_exponent_rules(self, seed=None) -> Problem:
        """
        Generate problem using exponent division rules.

        Example: Simplify a^3/a^3
        Correct: a^(3-3) = a^0 = 1
        Malrule: a^0 = 0
        """
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()

        # Choose between numerical or variable base
        use_variable = random.choice([True, False])

        if use_variable:
            # Variable base like x^n/x^n
            variable = random.choice(['x', 'y', 'a', 'b'])
            power = random.randint(ranges['power'][0], ranges['power'][1])

            problem_text = f"Simplify using exponent rules: {variable}^{power}/{variable}^{power}"

            metadata = {
                'base': variable,
                'power': power,
                'is_variable': True,
                'correct_answer': 1,
                'malrule_answer': 0,
                'template': 'exponent_rules'
            }
            operands = [power, power]

        else:
            # Numerical base like 5^3/5^3
            base = random.randint(ranges['base'][0], ranges['base'][1])
            power = random.randint(ranges['power'][0], ranges['power'][1])

            problem_text = f"Simplify using exponent rules: {base}^{power}/{base}^{power}"

            metadata = {
                'base': base,
                'power': power,
                'is_variable': False,
                'correct_answer': 1,
                'malrule_answer': 0,
                'template': 'exponent_rules'
            }
            operands = [base, power, power]

        return Problem(
            text=problem_text,
            operands=operands,
            operation='zero_exponent',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_polynomial_evaluation(self, seed=None) -> Problem:
        """
        Generate polynomial evaluation with zero exponents.

        Example: Evaluate 5x^0 when x = 7
        Correct: 5(1) = 5
        Malrule: 5(0) = 0
        """
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()

        coefficient = random.randint(ranges['coefficient'][0], ranges['coefficient'][1])
        variable = random.choice(['x', 'y', 'n', 't'])
        x_value = random.randint(ranges['base'][0], ranges['base'][1])

        problem_text = f"Evaluate {coefficient}{variable}^0 when {variable} = {x_value}"

        # Correct: coefficient * (x^0) = coefficient * 1 = coefficient
        correct_answer = coefficient
        # Malrule: coefficient * (x^0) = coefficient * 0 = 0
        malrule_answer = 0

        metadata = {
            'coefficient': coefficient,
            'variable': variable,
            'x_value': x_value,
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer,
            'template': 'polynomial_evaluation'
        }

        return Problem(
            text=problem_text,
            operands=[coefficient, x_value, 0],
            operation='zero_exponent',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_word_problem(self, seed=None) -> Problem:
        """
        Generate word problem with zero exponent context.

        Example: A bacteria population multiplies by 2^n each hour.
                 What is the population multiplier after 0 hours?
        Correct: 2^0 = 1 (no change)
        Malrule: 2^0 = 0 (no bacteria?)
        """
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()

        contexts = [
            {
                'text': 'A bacteria population multiplies by {base}^n each hour, where n is the number of hours. What is the population multiplier after 0 hours?',
                'context_type': 'bacteria_growth',
                'base_range': (2, 5)
            },
            {
                'text': 'An investment grows by {base}^t over t years. What is the growth factor after 0 years?',
                'context_type': 'investment',
                'base_range': (2, 3)
            },
            {
                'text': 'The number of pages in a book doubles every chapter, following the pattern {base}^c for chapter c. How many times the original is it at chapter 0 (the start)?',
                'context_type': 'doubling',
                'base_range': (2, 4)
            },
            {
                'text': 'A computer program creates {base}^n files at step n. How many files does it create at step 0?',
                'context_type': 'files',
                'base_range': (2, 5)
            }
        ]

        context = random.choice(contexts)
        base = random.randint(context['base_range'][0], context['base_range'][1])

        problem_text = context['text'].format(base=base)

        # Correct: base^0 = 1
        correct_answer = 1
        # Malrule: base^0 = 0
        malrule_answer = 0

        metadata = {
            'base': base,
            'exponent': 0,
            'context_type': context['context_type'],
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer,
            'template': 'word_problem'
        }

        return Problem(
            text=problem_text,
            operands=[base, 0],
            operation='zero_exponent',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_word_problem_context(self, seed=None) -> Problem:
        """Generate word problem covering ALL formula types with 3 variants each."""
        if seed is not None:
            random.seed(seed)

        # Select which formula type to embed
        formula_types = ['basic_zero_exponent', 'expression_simplification', 'exponent_rules', 'polynomial_evaluation']
        formula_type = random.choice(formula_types)
        variant = random.randint(0, 2)  # 3 variants per formula type

        if formula_type == 'basic_zero_exponent':
            # Formula: a^0 = 1
            ranges = self.get_value_ranges()
            base = random.randint(ranges['base'][0], ranges['base'][1])

            templates = [
                f"A manufacturing plant has an initial production capacity represented by {base}^0 units. What is the initial capacity multiplier?",
                f"In a scientific experiment, the starting condition is measured as {base}^0 times the baseline. What is this starting multiplier?",
                f"A video game character begins with a power level of {base}^0. What is the initial power level coefficient?"
            ]

            problem_text = templates[variant]
            correct_answer = 1
            malrule_answer = 0

            return Problem(
                text=problem_text,
                operands=[base, 0],
                operation='zero_exponent',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'base': base,
                    'exponent': 0,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        elif formula_type == 'expression_simplification':
            # Formula: ax^0 or (ax)^0
            ranges = self.get_value_ranges()
            coefficient = random.randint(ranges['coefficient'][0], ranges['coefficient'][1])
            expression_type = random.choice(['coefficient_times', 'parentheses'])

            if expression_type == 'coefficient_times':
                templates = [
                    f"A chemical reaction produces {coefficient} moles of product per x^0 catalyst units. Simplify to find the base production rate.",
                    f"The cost function is {coefficient}n^0 dollars, where n is the number of items. What is the simplified cost?",
                    f"A physics formula includes the term {coefficient}v^0 in meters per second. Simplify this velocity component."
                ]

                problem_text = templates[variant]
                correct_answer = coefficient
                malrule_answer = 0

                return Problem(
                    text=problem_text,
                    operands=[coefficient, 0],
                    operation='zero_exponent',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'coefficient': coefficient,
                        'variable': 'x',
                        'expression_type': expression_type,
                        'correct_answer': correct_answer,
                        'malrule_answer': malrule_answer,
                        'template': 'word_problem_context',
                        'is_word_problem': True,
                        'word_problem_type': formula_type,
                        'word_problem_variant': variant
                    }
                )
            else:  # parentheses
                templates = [
                    f"The volume of a container is ({coefficient}r)^0 cubic meters at the initial state. What is the volume multiplier?",
                    f"A wave function has amplitude ({coefficient}A)^0 at time zero. What is the initial amplitude coefficient?",
                    f"The gravitational effect at the origin is ({coefficient}d)^0 times the constant. Simplify this factor."
                ]

                problem_text = templates[variant]
                correct_answer = 1
                malrule_answer = 0

                return Problem(
                    text=problem_text,
                    operands=[coefficient, 0],
                    operation='zero_exponent',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'coefficient': coefficient,
                        'variable': 'x',
                        'expression_type': expression_type,
                        'correct_answer': correct_answer,
                        'malrule_answer': malrule_answer,
                        'template': 'word_problem_context',
                        'is_word_problem': True,
                        'word_problem_type': formula_type,
                        'word_problem_variant': variant
                    }
                )

        elif formula_type == 'exponent_rules':
            # Formula: a^n/a^n = a^0 = 1
            ranges = self.get_value_ranges()
            use_variable = random.choice([True, False])

            if use_variable:
                variable = random.choice(['x', 'y', 'a', 'b'])
                power = random.randint(ranges['power'][0], ranges['power'][1])

                templates = [
                    f"A population grows by factor {variable}^{power} in the morning and shrinks by factor {variable}^{power} in the evening. Using exponent rules, what is the net daily growth factor {variable}^{power}/{variable}^{power}?",
                    f"Two identical processes each handle {variable}^{power} operations. When comparing their ratio {variable}^{power}/{variable}^{power}, what is the result using exponent rules?",
                    f"An investment multiplies by {variable}^{power} and then divides by {variable}^{power}. Simplify {variable}^{power}/{variable}^{power} using exponent rules to find the net factor."
                ]

                problem_text = templates[variant]
                correct_answer = 1
                malrule_answer = 0

                return Problem(
                    text=problem_text,
                    operands=[power, power],
                    operation='zero_exponent',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'base': variable,
                        'power': power,
                        'is_variable': True,
                        'correct_answer': correct_answer,
                        'malrule_answer': malrule_answer,
                        'template': 'word_problem_context',
                        'is_word_problem': True,
                        'word_problem_type': formula_type,
                        'word_problem_variant': variant
                    }
                )
            else:
                base = random.randint(ranges['base'][0], ranges['base'][1])
                power = random.randint(ranges['power'][0], ranges['power'][1])

                templates = [
                    f"A machine multiplies its output by {base}^{power} in stage 1 and divides by {base}^{power} in stage 2. Using exponent rules, simplify {base}^{power}/{base}^{power} to find the net multiplier.",
                    f"The intensity increases by {base}^{power} and then decreases by {base}^{power}. Apply exponent rules to {base}^{power}/{base}^{power} to find the net change.",
                    f"A signal amplifies by {base}^{power} then attenuates by {base}^{power}. Simplify {base}^{power}/{base}^{power} using exponent rules."
                ]

                problem_text = templates[variant]
                correct_answer = 1
                malrule_answer = 0

                return Problem(
                    text=problem_text,
                    operands=[base, power, power],
                    operation='zero_exponent',
                    level=self.level,
                    difficulty=self.difficulty,
                    metadata={
                        'base': base,
                        'power': power,
                        'is_variable': False,
                        'correct_answer': correct_answer,
                        'malrule_answer': malrule_answer,
                        'template': 'word_problem_context',
                        'is_word_problem': True,
                        'word_problem_type': formula_type,
                        'word_problem_variant': variant
                    }
                )

        else:  # polynomial_evaluation
            # Formula: Evaluate cx^0 when x = value
            ranges = self.get_value_ranges()
            coefficient = random.randint(ranges['coefficient'][0], ranges['coefficient'][1])
            variable = random.choice(['x', 'y', 'n', 't'])
            x_value = random.randint(ranges['base'][0], ranges['base'][1])

            templates = [
                f"The efficiency formula of a machine is {coefficient}{variable}^0 units, where {variable} represents load. Evaluate the efficiency when {variable} = {x_value}.",
                f"A polynomial pricing model has a constant term {coefficient}{variable}^0 dollars, where {variable} is quantity. Calculate the price when {variable} = {x_value}.",
                f"The base rate in a formula is {coefficient}{variable}^0 units per hour, where {variable} is time. Find the rate when {variable} = {x_value}."
            ]

            problem_text = templates[variant]
            correct_answer = coefficient
            malrule_answer = 0

            return Problem(
                text=problem_text,
                operands=[coefficient, x_value, 0],
                operation='zero_exponent',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'coefficient': coefficient,
                    'variable': variable,
                    'x_value': x_value,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )
