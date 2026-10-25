"""
Correct algorithm for solving simple algebraic equations.
This version parses equations and solves them using inverse operations.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import re
from typing import List, Tuple, Optional
from utils import CorrectAlgorithm, Problem, Solution


class AlgebraicEquationCorrectAlgorithm(CorrectAlgorithm):
    """Correctly solves simple algebraic equations by parsing and using inverse operations."""

    def get_name(self) -> str:
        return "Correct Algebraic Equation Solving"

    def get_description(self) -> str:
        return "Correctly solves for variables using inverse operations."

    def _generate_verbose_steps(self, equation: str, parsed_template: str, components: dict,
                                 variable: str, correct_value: int) -> List[str]:
        """Generate verbose steps with detailed explanations."""
        steps = []
        steps.append(f"Problem: {equation}")
        steps.append("")
        steps.append(f"Goal: Isolate {variable} by using inverse operations")
        steps.append("")

        if parsed_template == 'basic_addition':
            constant = components['constant']
            result = components['result']
            steps.append(f"Step 1: Subtract {constant} from both sides")
            steps.append(f"  {variable} + {constant} - {constant} = {result} - {constant}")
            steps.append("")
            steps.append(f"Step 2: Simplify")
            steps.append(f"  {variable} = {result - constant}")
            steps.append("")
            steps.append(f"Step 3: Verify by substituting back")
            steps.append(f"  {correct_value} + {constant} = {result}")
            steps.append(f"  {correct_value + constant} = {result} ✓")

        elif parsed_template == 'basic_subtraction':
            constant = components['constant']
            result = components['result']
            steps.append(f"Step 1: Add {constant} to both sides")
            steps.append(f"  {variable} - {constant} + {constant} = {result} + {constant}")
            steps.append("")
            steps.append(f"Step 2: Simplify")
            steps.append(f"  {variable} = {result + constant}")
            steps.append("")
            steps.append(f"Step 3: Verify by substituting back")
            steps.append(f"  {correct_value} - {constant} = {result}")
            steps.append(f"  {correct_value - constant} = {result} ✓")

        elif parsed_template == 'basic_multiplication':
            coefficient = components['coefficient']
            result = components['result']
            steps.append(f"Step 1: Divide both sides by {coefficient}")
            steps.append(f"  {coefficient}{variable} ÷ {coefficient} = {result} ÷ {coefficient}")
            steps.append("")
            steps.append(f"Step 2: Simplify")
            steps.append(f"  {variable} = {result // coefficient}")
            steps.append("")
            steps.append(f"Step 3: Verify by substituting back")
            steps.append(f"  {coefficient} × {correct_value} = {result}")
            steps.append(f"  {coefficient * correct_value} = {result} ✓")

        elif parsed_template == 'two_step_equation':
            coefficient = components['coefficient']
            constant = components['constant']
            result = components['result']
            steps.append(f"Step 1: Subtract {constant} from both sides")
            steps.append(f"  {coefficient}{variable} + {constant} - {constant} = {result} - {constant}")
            steps.append(f"  {coefficient}{variable} = {result - constant}")
            steps.append("")
            steps.append(f"Step 2: Divide both sides by {coefficient}")
            steps.append(f"  {coefficient}{variable} ÷ {coefficient} = {result - constant} ÷ {coefficient}")
            steps.append(f"  {variable} = {(result - constant) // coefficient}")
            steps.append("")
            steps.append(f"Step 3: Verify by substituting back")
            steps.append(f"  {coefficient} × {correct_value} + {constant} = {result}")
            steps.append(f"  {coefficient * correct_value + constant} = {result} ✓")

        steps.append("")
        steps.append(f"Final Answer: {variable} = {correct_value} ✓")

        return steps

    def _generate_concise_steps(self, equation: str, parsed_template: str, components: dict,
                                 variable: str, correct_value: int) -> List[str]:
        """Generate concise steps with only formulas and values."""
        steps = []
        steps.append(f"Solve for {variable}: {equation}")

        if parsed_template == 'basic_addition':
            constant = components['constant']
            result = components['result']
            steps.append(f"{variable} = {result - constant}")

        elif parsed_template == 'basic_subtraction':
            constant = components['constant']
            result = components['result']
            steps.append(f"{variable} = {result + constant}")

        elif parsed_template == 'basic_multiplication':
            coefficient = components['coefficient']
            result = components['result']
            steps.append(f"{variable} = {result // coefficient}")

        elif parsed_template == 'two_step_equation':
            coefficient = components['coefficient']
            constant = components['constant']
            result = components['result']
            steps.append(f"{coefficient}{variable} = {result - constant}")
            steps.append(f"{variable} = {(result - constant) // coefficient}")

        return steps

    def _parse_equation(self, equation: str, variable: str) -> Tuple[str, dict]:
        """
        Parse an equation and determine its type and components.

        Returns:
            (template_type, components_dict)
        """
        # Remove spaces for easier parsing
        eq = equation.replace(' ', '')

        # Split by equals sign
        if '=' not in eq:
            raise ValueError(f"Invalid equation: {equation}")

        left, right = eq.split('=')
        result = int(right)

        # Try to match different patterns

        # Two-step equation: ax + b = c or ax - b = c
        match = re.match(rf'(\d+){variable}([+-])(\d+)', left)
        if match:
            coefficient = int(match.group(1))
            operation = match.group(2)
            constant = int(match.group(3))
            return 'two_step_equation', {
                'coefficient': coefficient,
                'constant': constant if operation == '+' else -constant,
                'result': result
            }

        # Basic multiplication: cx = result or just c*variable = result
        match = re.match(rf'(\d+)\*?{variable}', left)
        if match:
            coefficient = int(match.group(1))
            return 'basic_multiplication', {
                'coefficient': coefficient,
                'result': result
            }

        # Basic addition: x + c = result
        match = re.match(rf'{variable}\+(\d+)', left)
        if match:
            constant = int(match.group(1))
            return 'basic_addition', {
                'constant': constant,
                'result': result
            }

        # Basic subtraction: x - c = result
        match = re.match(rf'{variable}-(\d+)', left)
        if match:
            constant = int(match.group(1))
            return 'basic_subtraction', {
                'constant': constant,
                'result': result
            }

        raise ValueError(f"Could not parse equation: {equation}")

    def _solve_equation(self, template: str, components: dict) -> int:
        """
        Solve the equation using inverse operations.

        Args:
            template: Type of equation (basic_addition, basic_subtraction, etc.)
            components: Dictionary with equation components

        Returns:
            The solution value
        """
        if template == 'basic_addition':
            # x + c = result → x = result - c
            return components['result'] - components['constant']

        elif template == 'basic_subtraction':
            # x - c = result → x = result + c
            return components['result'] + components['constant']

        elif template == 'basic_multiplication':
            # cx = result → x = result / c
            return components['result'] // components['coefficient']

        elif template == 'two_step_equation':
            # ax + b = c → x = (c - b) / a
            result = components['result']
            constant = components['constant']
            coefficient = components['coefficient']
            return (result - constant) // coefficient

        else:
            raise ValueError(f"Unknown template: {template}")

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct algebraic equation solving.

        Args:
            problem: Algebraic equation problem
            verbose: If True, generate detailed steps; if False, generate concise steps

        Returns:
            Solution with correct steps
        """
        template = problem.metadata.get('template', 'basic_addition')
        variable = problem.metadata['variable']

        # For word problems, we need to construct the equation from metadata first
        if template == 'word_problem':
            operation_type = problem.metadata.get('operation_type', 'addition')
            word_problem_type = problem.metadata.get('word_problem_type', operation_type)
            constant = problem.metadata['constant']
            result = problem.metadata['result']

            if word_problem_type == 'basic_addition' or operation_type == 'addition':
                equation = f"{variable} + {constant} = {result}"
            elif word_problem_type == 'basic_subtraction' or operation_type == 'subtraction':
                equation = f"{variable} - {constant} = {result}"
            elif word_problem_type == 'basic_multiplication' or operation_type == 'multiplication':
                equation = f"{constant}{variable} = {result}"
            elif word_problem_type == 'two_step_equation':
                coefficient = problem.metadata.get('coefficient', 2)
                constant = problem.metadata['constant']
                equation = f"{coefficient}{variable} + {constant} = {result}"
            else:
                # Default to addition if unknown
                equation = f"{variable} + {constant} = {result}"
        else:
            # Try to get equation from metadata, otherwise parse from problem text
            equation = problem.metadata.get('equation')
            if not equation:
                # Extract equation from problem text
                match = re.search(r'([a-z]\s*[+\-*]?\s*\d+|\d+\s*[*]?\s*[a-z])\s*=\s*\d+', problem.text)
                if match:
                    equation = match.group(0)
                else:
                    raise ValueError("Could not find equation in problem text")

        # Parse the equation to get components and verify template
        parsed_template, components = self._parse_equation(equation, variable)

        # Solve the equation
        correct_value = self._solve_equation(parsed_template, components)

        # Generate steps based on verbose setting
        if verbose:
            steps = self._generate_verbose_steps(equation, parsed_template, components,
                                                  variable, correct_value)
        else:
            steps = self._generate_concise_steps(equation, parsed_template, components,
                                                  variable, correct_value)

        return Solution(
            answer=correct_value,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
