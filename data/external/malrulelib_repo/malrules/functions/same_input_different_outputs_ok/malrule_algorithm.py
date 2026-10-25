"""
Same-Input-Different-Outputs-OK malrule algorithm.

Implements the systematic error of accepting relations with repeated
inputs (different outputs) as valid functions.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List

class SameInputDifferentOutputsOKMalrule(Malrule):
    """
    Implements the Same-Input-Different-Outputs-OK bug.

    Students don't understand that functions must map each input to
    exactly ONE output. They accept any set of ordered pairs as a function.

    Example: {(2,3), (4,5), (2,7)} - Student says YES, it's a function (WRONG!)
    The input 2 maps to both 3 and 7, so it's NOT a function.

    This is a common misconception when first learning function definitions.
    """

    def get_name(self) -> str:
        return "Univalence-Requirement-Violation"

    def get_description(self) -> str:
        return (
            "Students fail to understand the univalence requirement: that functions must map "
            "each input to exactly ONE output. This is a concept image/concept definition gap "
            "identified by Vinner & Dreyfus (1989) - students accept the formal definition but "
            "rely on personal experience when classifying relations, often accepting multi-valued "
            "relations as functions."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Malrule: always say YES, any set of ordered pairs is a function
        return "YES"

    def _generate_concise_steps(self, problem: Problem, template: str) -> List[str]:
        """Generate concise steps with only formulas and values."""
        pairs = problem.metadata['pairs']
        pairs_str = problem.metadata['pairs_str']

        steps = []

        if template == 'word_problem':
            steps.append(f"{problem.text}")

        steps.append(f"Relation: {{{pairs_str}}}")
        steps.append(f"{len(pairs)} ordered pairs found")
        steps.append(f"Has inputs and outputs → YES (function)")
        steps.append(f"YES")

        return steps

    def _generate_verbose_steps(self, problem: Problem, template: str) -> List[str]:
        """Generate verbose steps with full explanations (original format)."""
        pairs = problem.metadata['pairs']
        pairs_str = problem.metadata['pairs_str']

        steps = []
        steps.append(f"Problem: {problem.text[:100]}...")
        steps.append("")
        steps.append("MALRULE: Any set of ordered pairs is a function")
        steps.append(f"  MALRULE REASONING: 'If it has inputs and outputs, it's a function'")
        steps.append(f"                     'Don't need to check for repeated inputs' [WRONG!]")
        steps.append("")

        if template == 'ordered_pairs_set':
            steps.append(f"Step 1: Count the ordered pairs")
            steps.append(f"  Found {len(pairs)} ordered pairs: {{{pairs_str}}}")
            steps.append(f"Step 2: MALRULE check - 'Does it have inputs and outputs?'")
            steps.append(f"  Yes, it has inputs and outputs")
            steps.append(f"Step 3: MALRULE conclusion")
            steps.append(f"  'Since it has ordered pairs, it's a function'")
            steps.append(f"  (Student doesn't check if inputs repeat!)")

        elif template == 'table_format':
            steps.append(f"Step 1: Look at the table")
            steps.append(f"  Found {len(pairs)} input-output pairs in the table")
            steps.append(f"Step 2: MALRULE check - 'Does the table have inputs and outputs?'")
            steps.append(f"  Yes, there's an input row and output row")
            steps.append(f"Step 3: MALRULE conclusion")
            steps.append(f"  'Since it has inputs matching outputs, it's a function'")
            steps.append(f"  (Student doesn't check if any input value appears twice!)")

        elif template == 'graph_points':
            steps.append(f"Step 1: Identify the points")
            steps.append(f"  Found {len(pairs)} points to plot: {pairs_str}")
            steps.append(f"Step 2: MALRULE check - 'Can we plot these points?'")
            steps.append(f"  Yes, all points have x and y coordinates")
            steps.append(f"Step 3: MALRULE conclusion")
            steps.append(f"  'Since we can plot them, they form a function'")
            steps.append(f"  (Student doesn't apply vertical line test!)")

        elif template == 'mapping_diagram':
            steps.append(f"Step 1: Count the mappings")
            steps.append(f"  Found {len(pairs)} arrows/mappings")
            steps.append(f"Step 2: MALRULE check - 'Does each arrow go somewhere?'")
            steps.append(f"  Yes, every input has an arrow pointing to an output")
            steps.append(f"Step 3: MALRULE conclusion")
            steps.append(f"  'Since all inputs map to outputs, it's a function'")
            steps.append(f"  (Student doesn't check if one input maps to TWO outputs!)")

        elif template == 'word_problem':
            context = problem.metadata.get('context', 'assignment')
            steps.append(f"Step 1: Understand the {context} system")
            steps.append(f"  Found {len(pairs)} {context} assignments")
            steps.append(f"Step 2: MALRULE check - 'Is everything assigned?'")
            steps.append(f"  Yes, each input has an assignment")
            steps.append(f"Step 3: MALRULE conclusion")
            steps.append(f"  'Since everything is assigned, it's a valid function'")
            steps.append(f"  (Student doesn't notice if one input has MULTIPLE assignments!)")

        steps.append("")
        steps.append(f"Final Answer: YES (INCORRECT - didn't check for repeated inputs with different outputs)")

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Same-Input-Different-Outputs-OK malrule across all templates.

        Args:
            problem: Function definition problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with incorrect acceptance of repeated inputs
        """
        template = problem.metadata.get('template', 'ordered_pairs_set')

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, template)
        else:
            steps = self._generate_concise_steps(problem, template)

        return Solution(
            answer="YES",
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
