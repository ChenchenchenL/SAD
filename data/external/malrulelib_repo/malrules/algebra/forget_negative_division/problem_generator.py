"""
Problem generator for Forget-Negative-Division malrule.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Any
from utils import ProblemGenerator, Problem, DifficultyLevel


class ForgetNegativeDivisionProblemGenerator(ProblemGenerator):
    """Generates inequality problems requiring division by negative."""

    def get_value_ranges(self) -> Dict[str, Any]:
        """Returns the value ranges for problem generation."""
        return {
            'coefficient_min': -10,
            'coefficient_max': -1,  # Always negative
            'constant_min': -20,
            'constant_max': 20,
            'inequality_signs': ['<', '>', '≤', '≥']
        }

    def generate(self, seed=None) -> Problem:
        """Generate an inequality requiring division by negative coefficient."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()

        # Choose template
        templates = [
            'basic_one_step',
            'two_step',
            'fraction_coefficient',
            'word_problem'
        ]
        template = random.choice(templates)

        sign_flip = {
            '<': '>',
            '>': '<',
            '≤': '≥',
            '≥': '≤'
        }

        if template == 'basic_one_step':
            # Original: -ax < b
            coefficient = random.randint(ranges['coefficient_min'], ranges['coefficient_max'])
            constant = random.randint(ranges['constant_min'], ranges['constant_max'])
            while constant == 0:
                constant = random.randint(ranges['constant_min'], ranges['constant_max'])

            inequality_sign = random.choice(ranges['inequality_signs'])
            solution_value = constant / coefficient
            correct_sign = sign_flip[inequality_sign]
            malrule_sign = inequality_sign

            if coefficient == -1:
                coeff_str = "-x"
            else:
                coeff_str = f"{coefficient}x"

            text = f"Solve for x: {coeff_str} {inequality_sign} {constant}"

            return Problem(
                text=text,
                operands=[coefficient, constant],
                operation='inequality_solve',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'coefficient': coefficient,
                    'constant': constant,
                    'inequality_sign': inequality_sign,
                    'solution_value': round(solution_value, 2) if solution_value != int(solution_value) else int(solution_value),
                    'correct_sign': correct_sign,
                    'malrule_sign': malrule_sign,
                    'inequality': f"{coeff_str} {inequality_sign} {constant}",
                    'template': template
                }
            )

        elif template == 'two_step':
            # Two-step: -ax + b [sign] c
            # Example: -3x + 5 > 11
            coefficient = random.randint(ranges['coefficient_min'], ranges['coefficient_max'])
            added_const = random.randint(2, 15)
            rhs_const = random.randint(5, 25)
            inequality_sign = random.choice(ranges['inequality_signs'])

            # Solve: -ax + b [sign] c → -ax [sign] c - b → x [flipped] (c-b)/a
            intermediate = rhs_const - added_const
            solution_value = intermediate / coefficient
            correct_sign = sign_flip[inequality_sign]
            malrule_sign = inequality_sign

            if coefficient == -1:
                coeff_str = "-x"
            else:
                coeff_str = f"{coefficient}x"

            text = f"Solve for x: {coeff_str} + {added_const} {inequality_sign} {rhs_const}"

            return Problem(
                text=text,
                operands=[coefficient, added_const, rhs_const],
                operation='inequality_solve',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'coefficient': coefficient,
                    'added_constant': added_const,
                    'rhs_constant': rhs_const,
                    'inequality_sign': inequality_sign,
                    'solution_value': round(solution_value, 2) if solution_value != int(solution_value) else int(solution_value),
                    'correct_sign': correct_sign,
                    'malrule_sign': malrule_sign,
                    'inequality': f"{coeff_str} + {added_const} {inequality_sign} {rhs_const}",
                    'template': template
                }
            )

        elif template == 'fraction_coefficient':
            # Fraction coefficient: -(1/2)x < 6
            denominators = [2, 3, 4, 5]
            denom = random.choice(denominators)
            constant = random.randint(3, 20)
            inequality_sign = random.choice(ranges['inequality_signs'])

            # Coefficient is -1/denom
            coefficient_frac = f"-1/{denom}"
            solution_value = constant * (-denom)  # Multiply by reciprocal
            correct_sign = sign_flip[inequality_sign]
            malrule_sign = inequality_sign

            text = f"Solve for x: {coefficient_frac}x {inequality_sign} {constant}"

            return Problem(
                text=text,
                operands=[-1, denom, constant],
                operation='inequality_solve',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'coefficient': f"{-1 / denom}",
                    'constant': constant,
                    'inequality_sign': inequality_sign,
                    'solution_value': int(solution_value),
                    'correct_sign': correct_sign,
                    'malrule_sign': malrule_sign,
                    'inequality': f"{coefficient_frac}x {inequality_sign} {constant}",
                    'template': template,
                    'denominator': denom
                }
            )

        elif template == 'word_problem':
            # Word problem covering ALL formula types
            # Each formula type has 3 different contexts

            # Select which formula type to embed
            formula_types = ['basic_one_step', 'two_step', 'fraction_coefficient']
            formula_type = random.choice(formula_types)
            variant = random.randint(0, 2)

            if formula_type == 'basic_one_step':
                # Formula: -ax < b or -ax > b
                coefficient = random.randint(-5, -2)
                constant = random.randint(10, 40)
                inequality_sign = random.choice(['<', '>'])

                solution_value = constant / coefficient
                correct_sign = sign_flip[inequality_sign]
                malrule_sign = inequality_sign

                if coefficient == -1:
                    coeff_str = "-x"
                else:
                    coeff_str = f"{coefficient}x"

                templates = [
                    f"The temperature drops at {abs(coefficient)} degrees per hour for x hours. If it must stay above {-constant} degrees, solve for x: {coeff_str} {sign_flip[inequality_sign]} {constant}",
                    f"A submarine descends at {abs(coefficient)} meters per minute for x minutes. If the depth must be less than {abs(constant)} meters, solve for x: {coeff_str} {inequality_sign} {constant}",
                    f"An account loses ${abs(coefficient)} per day for x days. If the balance must remain above ${-constant}, solve for x: {coeff_str} {sign_flip[inequality_sign]} {constant}"
                ]

                text = templates[variant]
                inequality = f"{coeff_str} {inequality_sign} {constant}"

                metadata = {
                    'coefficient': coefficient,
                    'constant': constant,
                    'inequality_sign': inequality_sign,
                    'solution_value': round(solution_value, 2) if solution_value != int(solution_value) else int(solution_value),
                    'correct_sign': correct_sign,
                    'malrule_sign': malrule_sign,
                    'inequality': inequality,
                    'template': template,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }

            elif formula_type == 'two_step':
                # Formula: -ax + b [sign] c
                coefficient = random.randint(ranges['coefficient_min'], ranges['coefficient_max'])
                added_const = random.randint(2, 15)
                rhs_const = random.randint(5, 25)
                inequality_sign = random.choice(ranges['inequality_signs'])

                intermediate = rhs_const - added_const
                solution_value = intermediate / coefficient
                correct_sign = sign_flip[inequality_sign]
                malrule_sign = inequality_sign

                if coefficient == -1:
                    coeff_str = "-x"
                else:
                    coeff_str = f"{coefficient}x"

                templates = [
                    f"A temperature starts at {added_const}°C and decreases by {abs(coefficient)} degrees per hour for x hours. If it must be {inequality_sign} {rhs_const}°C, solve for x: {coeff_str} + {added_const} {inequality_sign} {rhs_const}",
                    f"A debt of ${abs(coefficient)} per month for x months is added to an initial credit of ${added_const}. If the total must be {inequality_sign} ${rhs_const}, solve for x: {coeff_str} + {added_const} {inequality_sign} {rhs_const}",
                    f"An elevator starts at floor {added_const} and descends {abs(coefficient)} floors per second for x seconds. If the final floor must be {inequality_sign} floor {rhs_const}, solve for x: {coeff_str} + {added_const} {inequality_sign} {rhs_const}"
                ]

                text = templates[variant]
                inequality = f"{coeff_str} + {added_const} {inequality_sign} {rhs_const}"

                metadata = {
                    'coefficient': coefficient,
                    'added_constant': added_const,
                    'rhs_constant': rhs_const,
                    'inequality_sign': inequality_sign,
                    'solution_value': round(solution_value, 2) if solution_value != int(solution_value) else int(solution_value),
                    'correct_sign': correct_sign,
                    'malrule_sign': malrule_sign,
                    'inequality': inequality,
                    'template': template,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }

            else:  # fraction_coefficient
                # Formula: -(1/d)x < constant
                denominators = [2, 3, 4, 5]
                denom = random.choice(denominators)
                constant = random.randint(3, 20)
                inequality_sign = random.choice(ranges['inequality_signs'])

                coefficient_frac = f"-1/{denom}"
                solution_value = constant * (-denom)
                correct_sign = sign_flip[inequality_sign]
                malrule_sign = inequality_sign

                templates = [
                    f"A chemical reaction decreases by 1/{denom} mole per second for x seconds. If the final amount must be {inequality_sign} {constant} moles, solve for x: {coefficient_frac}x {inequality_sign} {constant}",
                    f"A stock price drops by 1/{denom} of a dollar per share for x shares sold. If the total loss must be {inequality_sign} ${constant}, solve for x: {coefficient_frac}x {inequality_sign} {constant}",
                    f"A water level decreases by 1/{denom} inch per minute for x minutes. If the level must stay {inequality_sign} {constant} inches, solve for x: {coefficient_frac}x {inequality_sign} {constant}"
                ]

                text = templates[variant]
                inequality = f"{coefficient_frac}x {inequality_sign} {constant}"

                metadata = {
                    'coefficient': f"{-1 / denom}",
                    'constant': constant,
                    'inequality_sign': inequality_sign,
                    'solution_value': int(solution_value),
                    'correct_sign': correct_sign,
                    'malrule_sign': malrule_sign,
                    'inequality': inequality,
                    'template': template,
                    'denominator': denom,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }

            # Set operands based on formula type
            if formula_type == 'basic_one_step':
                operands = [coefficient, constant]
            elif formula_type == 'two_step':
                operands = [coefficient, added_const, rhs_const]
            else:  # fraction_coefficient
                operands = [-1, denom, constant]

            return Problem(
                text=text,
                operands=operands,
                operation='inequality_solve',
                level=self.level,
                difficulty=self.difficulty,
                metadata=metadata
            )
