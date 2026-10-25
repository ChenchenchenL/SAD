"""
Problem generator for Variable-Letter-Has-Value malrule.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Any, List, Optional
from utils import ProblemGenerator, Problem, DifficultyLevel


class VariableLetterHasValueProblemGenerator(ProblemGenerator):
    """
    Generates algebraic equations where students incorrectly assume variables have fixed values.

    Templates:
    1. basic_addition - Simple x + c = result equations
    2. basic_subtraction - Simple x - c = result equations
    3. basic_multiplication - Simple c×x = result equations
    4. two_step_equation - Two-step equations like 2x + 3 = 11
    5. word_problem - Word problems with variables
    """

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_addition',
            'basic_subtraction',
            'basic_multiplication',
            'two_step_equation',
            'word_problem'
        ]

    def get_value_ranges(self) -> Dict[str, Any]:
        """Returns the value ranges for problem generation."""
        return {
            'constant_min': 1,
            'constant_max': 20,
            'result_min': 5,
            'result_max': 30,
            'variables': ['x', 'n', 'a', 'y', 'b'],
            'variable_values': {
                'x': 10,  # Students think x=10 (tenth letter)
                'n': 1,   # Students think n=1 ("number one")
                'a': 1,   # Students think a=1 (first letter)
                'y': 25,  # Students think y=25 (25th letter)
                'b': 2    # Students think b=2 (second letter)
            }
        }

    def generate(self, seed=None, template: Optional[str] = None) -> Problem:
        """Generate an algebraic equation."""
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            template = random.choice(self.get_available_templates())

        # Generate based on template
        if template == 'basic_addition':
            return self._generate_basic_addition(seed)
        elif template == 'basic_subtraction':
            return self._generate_basic_subtraction(seed)
        elif template == 'basic_multiplication':
            return self._generate_basic_multiplication(seed)
        elif template == 'two_step_equation':
            return self._generate_two_step_equation(seed)
        elif template == 'word_problem':
            return self._generate_word_problem(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_addition(self, seed=None) -> Problem:
        """
        Generate basic addition equation (original template).

        Example: x + 5 = 12
        Correct: x = 7
        Malrule: x = 10, so 10 + 5 = 15 ≠ 12 (checks substitution)
        """
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()

        # Choose a variable
        variable = random.choice(ranges['variables'])
        assumed_value = ranges['variable_values'][variable]

        # Generate: var + constant = result
        constant = random.randint(ranges['constant_min'], ranges['constant_max'])

        # Choose actual value for variable (make sure it's NOT the assumed value)
        actual_value = random.randint(1, 20)
        while actual_value == assumed_value:
            actual_value = random.randint(1, 20)

        # Calculate the result
        result = actual_value + constant

        # Calculate malrule answer (using assumed value)
        malrule_answer = assumed_value

        text = f"Solve for {variable}: {variable} + {constant} = {result}"

        return Problem(
            text=text,
            operands=[constant, result],
            operation='algebra_solve',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'variable': variable,
                'constant': constant,
                'result': result,
                'correct_value': actual_value,
                'assumed_value': assumed_value,
                'malrule_answer': malrule_answer,
                'equation': f"{variable} + {constant} = {result}",
                'template': 'basic_addition'
            }
        )

    def _generate_basic_subtraction(self, seed=None) -> Problem:
        """
        Generate basic subtraction equation.

        Example: x - 3 = 5
        Correct: x = 8
        Malrule: x = 10 (assumes x always equals 10)
        """
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()

        variable = random.choice(ranges['variables'])
        assumed_value = ranges['variable_values'][variable]

        constant = random.randint(ranges['constant_min'], ranges['constant_max'])

        # Choose actual value for variable
        actual_value = random.randint(constant + 1, 30)
        while actual_value == assumed_value:
            actual_value = random.randint(constant + 1, 30)

        # Calculate the result
        result = actual_value - constant

        malrule_answer = assumed_value

        text = f"Solve for {variable}: {variable} - {constant} = {result}"

        return Problem(
            text=text,
            operands=[constant, result],
            operation='algebra_solve',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'variable': variable,
                'constant': constant,
                'result': result,
                'correct_value': actual_value,
                'assumed_value': assumed_value,
                'malrule_answer': malrule_answer,
                'equation': f"{variable} - {constant} = {result}",
                'template': 'basic_subtraction'
            }
        )

    def _generate_basic_multiplication(self, seed=None) -> Problem:
        """
        Generate basic multiplication equation.

        Example: 3x = 15
        Correct: x = 5
        Malrule: x = 10 (assumes x always equals 10)
        """
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()

        variable = random.choice(ranges['variables'])
        assumed_value = ranges['variable_values'][variable]

        coefficient = random.randint(2, 8)

        # Choose actual value for variable
        actual_value = random.randint(2, 12)
        while actual_value == assumed_value:
            actual_value = random.randint(2, 12)

        # Calculate the result
        result = coefficient * actual_value

        malrule_answer = assumed_value

        text = f"Solve for {variable}: {coefficient}{variable} = {result}"

        return Problem(
            text=text,
            operands=[coefficient, result],
            operation='algebra_solve',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'variable': variable,
                'coefficient': coefficient,
                'result': result,
                'correct_value': actual_value,
                'assumed_value': assumed_value,
                'malrule_answer': malrule_answer,
                'equation': f"{coefficient}{variable} = {result}",
                'template': 'basic_multiplication'
            }
        )

    def _generate_two_step_equation(self, seed=None) -> Problem:
        """
        Generate two-step equation.

        Example: 2x + 3 = 11
        Correct: x = 4
        Malrule: x = 10 (assumes x always equals 10)
        """
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()

        variable = random.choice(ranges['variables'])
        assumed_value = ranges['variable_values'][variable]

        coefficient = random.randint(2, 5)
        constant = random.randint(1, 15)

        # Choose actual value for variable
        actual_value = random.randint(2, 12)
        while actual_value == assumed_value:
            actual_value = random.randint(2, 12)

        # Calculate the result
        result = coefficient * actual_value + constant

        malrule_answer = assumed_value

        text = f"Solve for {variable}: {coefficient}{variable} + {constant} = {result}"

        return Problem(
            text=text,
            operands=[coefficient, constant, result],
            operation='algebra_solve',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'variable': variable,
                'coefficient': coefficient,
                'constant': constant,
                'result': result,
                'correct_value': actual_value,
                'assumed_value': assumed_value,
                'malrule_answer': malrule_answer,
                'equation': f"{coefficient}{variable} + {constant} = {result}",
                'template': 'two_step_equation'
            }
        )

    def _generate_word_problem(self, seed=None) -> Problem:
        """
        Generate word problem with variable covering ALL formula types.

        Each formula type has 3 different word problem templates:
        - basic_addition: x + c = result
        - basic_subtraction: x - c = result
        - basic_multiplication: cx = result
        - two_step_equation: ax + b = c
        """
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()

        variable = random.choice(ranges['variables'])
        assumed_value = ranges['variable_values'][variable]

        # Select which formula type to embed
        formula_types = ['basic_addition', 'basic_subtraction', 'basic_multiplication', 'two_step_equation']
        formula_type = random.choice(formula_types)
        variant = random.randint(0, 2)

        if formula_type == 'basic_addition':
            # Formula: var + constant = result
            constant = random.randint(1, 15)
            actual_value = random.randint(1, 20)
            while actual_value == assumed_value:
                actual_value = random.randint(1, 20)
            result = actual_value + constant

            templates = [
                f"Sarah has {variable} apples. She buys {constant} more and now has {result} apples. How many did she start with? (Find {variable})",
                f"A box contains {variable} items. After adding {constant} more items, there are {result} items total. Find {variable}.",
                f"The temperature was {variable} degrees. It rose by {constant} degrees to reach {result} degrees. What was {variable}?"
            ]

            problem_text = templates[variant]
            equation = f"{variable} + {constant} = {result}"

        elif formula_type == 'basic_subtraction':
            # Formula: var - constant = result
            constant = random.randint(1, 15)
            actual_value = random.randint(constant + 1, 30)
            while actual_value == assumed_value:
                actual_value = random.randint(constant + 1, 30)
            result = actual_value - constant

            templates = [
                f"A number {variable} minus {constant} equals {result}. What is {variable}?",
                f"John had {variable} dollars. After spending ${constant}, he has ${result} left. Find {variable}.",
                f"A tank had {variable} liters. After using {constant} liters, {result} liters remain. What is {variable}?"
            ]

            problem_text = templates[variant]
            equation = f"{variable} - {constant} = {result}"

        elif formula_type == 'basic_multiplication':
            # Formula: coefficient × var = result
            coefficient = random.randint(2, 8)
            actual_value = random.randint(2, 12)
            while actual_value == assumed_value:
                actual_value = random.randint(2, 12)
            result = coefficient * actual_value
            constant = coefficient

            templates = [
                f"John has {variable} boxes of pencils. Each box has {coefficient} pencils. He has {result} pencils total. How many boxes ({variable}) does he have?",
                f"A car travels at {coefficient} times the speed {variable}. If the total speed is {result} mph, find {variable}.",
                f"If {coefficient} groups each contain {variable} items for a total of {result} items, find {variable}."
            ]

            problem_text = templates[variant]
            equation = f"{coefficient}{variable} = {result}"

        else:  # two_step_equation
            # Formula: coefficient × var + constant = result
            coefficient = random.randint(2, 5)
            constant = random.randint(1, 15)
            actual_value = random.randint(2, 12)
            while actual_value == assumed_value:
                actual_value = random.randint(2, 12)
            result = coefficient * actual_value + constant

            templates = [
                f"A taxi charges ${constant} initially plus ${coefficient} per mile for {variable} miles. If the total fare is ${result}, find {variable}.",
                f"A phone plan costs ${constant} monthly plus ${coefficient} per GB for {variable} GB. If the bill is ${result}, find {variable}.",
                f"Tickets cost ${coefficient} each for {variable} tickets plus a ${constant} fee. If the total is ${result}, find {variable}."
            ]

            problem_text = templates[variant]
            equation = f"{coefficient}{variable} + {constant} = {result}"

        malrule_answer = assumed_value

        # Set context_type based on formula type and variant
        context_types = {
            'basic_addition': ['apples', 'items', 'temperature'],
            'basic_subtraction': ['number_riddle', 'money', 'tank'],
            'basic_multiplication': ['pencils', 'speed', 'groups'],
            'two_step_equation': ['taxi', 'phone_plan', 'tickets']
        }
        context_type = context_types[formula_type][variant]

        return Problem(
            text=problem_text,
            operands=[constant if formula_type != 'two_step_equation' else coefficient, result],
            operation='algebra_solve',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'variable': variable,
                'constant': constant if formula_type != 'basic_multiplication' else coefficient,
                'result': result,
                'correct_value': actual_value,
                'assumed_value': assumed_value,
                'malrule_answer': malrule_answer,
                'equation': equation,
                'template': 'word_problem',
                'word_problem_type': formula_type,
                'word_problem_variant': variant,
                'operation_type': formula_type,
                'context_type': context_type
            }
        )
