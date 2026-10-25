"""
Correct function definition algorithm.

Implements proper checking for whether a relation is a function
by verifying each input maps to exactly one output.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class FunctionDefinitionCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for determining if a relation is a function.

    Checks that each input (x-value) maps to exactly one output (y-value).
    """

    def get_name(self) -> str:
        return "Correct Function Definition Check"

    def get_description(self) -> str:
        return (
            "Correctly determines if a relation is a function by checking that "
            "each input (x-value) maps to exactly one output (y-value). "
            "Uses the vertical line test principle."
        )

    def _generate_concise_steps(self, problem: Problem, template: str) -> List[str]:
        """Generate concise steps with only formulas and values."""
        pairs = problem.metadata['pairs']
        pairs_str = problem.metadata['pairs_str']

        steps = []

        # Build input to outputs mapping
        input_to_outputs = {}
        for x, y in pairs:
            if x not in input_to_outputs:
                input_to_outputs[x] = []
            input_to_outputs[x].append(y)

        # Find repeated inputs
        repeated_inputs = []
        for x, outputs in sorted(input_to_outputs.items()):
            if len(outputs) > 1:
                repeated_inputs.append((x, outputs))

        # Generate concise steps
        if template == 'word_problem':
            steps.append(f"{problem.text}")

        steps.append(f"Relation: {{{pairs_str}}}")

        # Show input mapping check
        for x, outputs in sorted(input_to_outputs.items()):
            if len(outputs) > 1:
                steps.append(f"Input {x} → {outputs} (multiple outputs)")
            else:
                steps.append(f"Input {x} → {outputs[0]}")

        if repeated_inputs:
            steps.append(f"NO (input maps to multiple outputs)")
        else:
            steps.append(f"YES (each input maps to one output)")

        return steps

    def _generate_verbose_steps(self, problem: Problem, template: str) -> List[str]:
        """Generate verbose steps with full explanations (original format)."""
        pairs = problem.metadata['pairs']
        pairs_str = problem.metadata['pairs_str']

        steps = []
        steps.append(f"Problem: {problem.text[:100]}...")
        steps.append("")
        steps.append("Rule: A function must have exactly ONE output for each input")
        steps.append("")

        # Check for repeated inputs
        input_to_outputs = {}
        for x, y in pairs:
            if x not in input_to_outputs:
                input_to_outputs[x] = []
            input_to_outputs[x].append(y)

        if template == 'ordered_pairs_set':
            steps.append(f"Step 1: Extract all ordered pairs from {{{pairs_str}}}")
            steps.append(f"Step 2: Check each input value")

        elif template == 'table_format':
            steps.append(f"Step 1: Read inputs and outputs from table")
            steps.append(f"Step 2: Check if any input value appears more than once")

        elif template == 'graph_points':
            steps.append(f"Step 1: Identify all points to plot")
            steps.append(f"Step 2: Apply vertical line test (check for same x with different y)")

        elif template == 'mapping_diagram':
            steps.append(f"Step 1: List all mappings from diagram")
            steps.append(f"Step 2: Check if any input has multiple arrows")

        elif template == 'word_problem':
            context = problem.metadata.get('context', 'assignment')
            steps.append(f"Step 1: Understand the {context} system requirements")
            steps.append(f"Step 2: Check if any input maps to multiple outputs")

        steps.append("")

        repeated_inputs = []
        for x, outputs in sorted(input_to_outputs.items()):
            if len(outputs) > 1:
                steps.append(f"  Input {x} → outputs {outputs} ✗ MULTIPLE OUTPUTS!")
                repeated_inputs.append((x, outputs))
            else:
                steps.append(f"  Input {x} → output {outputs[0]} ✓")

        steps.append("")

        if repeated_inputs:
            steps.append(f"Step 3: Conclusion")
            steps.append(f"  Found repeated input(s) with different outputs:")
            for x, outputs in repeated_inputs:
                steps.append(f"    Input {x} has outputs: {outputs}")

            if template == 'graph_points':
                steps.append(f"  FAILS vertical line test")
            elif template == 'word_problem':
                context = problem.metadata.get('context', 'assignment')
                steps.append(f"  This {context} system is invalid - one input can't have multiple outputs")
            else:
                steps.append(f"  Violates function definition")

            steps.append(f"  Answer: NOT a function")
        else:
            steps.append(f"Step 3: Conclusion")
            steps.append(f"  All inputs map to exactly ONE output")

            if template == 'graph_points':
                steps.append(f"  PASSES vertical line test")
            elif template == 'word_problem':
                context = problem.metadata.get('context', 'assignment')
                steps.append(f"  This {context} system is valid")
            else:
                steps.append(f"  Satisfies function definition")

            steps.append(f"  Answer: This IS a function")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct function definition check across all templates.

        Args:
            problem: Function definition problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with correct function check
        """
        template = problem.metadata.get('template', 'ordered_pairs_set')
        pairs = problem.metadata['pairs']

        # Check for repeated inputs
        input_to_outputs = {}
        for x, y in pairs:
            if x not in input_to_outputs:
                input_to_outputs[x] = []
            input_to_outputs[x].append(y)

        repeated_inputs = []
        for x, outputs in sorted(input_to_outputs.items()):
            if len(outputs) > 1:
                repeated_inputs.append((x, outputs))

        if repeated_inputs:
            answer = "NO"
        else:
            answer = "YES"

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, template)
        else:
            steps = self._generate_concise_steps(problem, template)

        return Solution(
            answer=answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
