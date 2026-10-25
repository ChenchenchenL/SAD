"""
Decompose-By-Place-Value-Label malrule algorithm.

Implements the systematic error where students concatenate place value labels
instead of adding their values.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
from typing import Dict, Any, List

class DecomposeByPlaceValueLabelMalrule(Malrule):
    """
    Implements the Decompose-By-Place-Value-Label bug.

    Students write numbers from place value decompositions by concatenating
    the labels instead of adding values. For example, "2 hundreds 13 tens 1 ones"
    becomes 2131 instead of 200 + 130 + 1 = 331.
    """

    def get_name(self) -> str:
        return "Decompose-By-Place-Value-Label (Face Value Error)"

    def get_description(self) -> str:
        return (
            "When interpreting place value decompositions, the student treats the numeric "
            "labels as face values to be concatenated rather than as multiplicative values "
            "to be added. For example, '2 hundreds 13 tens 1 ones' is written as 2,131 "
            "instead of correctly calculating 200 + 130 + 1 = 331. This error reflects "
            "what Ross (1989) identified as 'face value' understanding - students interpret "
            "digits at their literal face value without understanding their positional "
            "significance. The student perceives the decomposition as a labeling task "
            "rather than a mathematical composition of values."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem.

        Uses logic to concatenate place value labels instead of adding values.
        """
        # Get place values from metadata or operands
        thousands = problem.metadata.get('thousands', problem.operands[0])
        hundreds = problem.metadata.get('hundreds', problem.operands[1])
        tens = problem.metadata.get('tens', problem.operands[2])
        ones = problem.metadata.get('ones', problem.operands[3])

        # Concatenate the non-zero place value counts (face value error)
        parts = []
        if thousands > 0:
            parts.append(str(thousands))
        if hundreds > 0:
            parts.append(str(hundreds))
        if tens > 0:
            parts.append(str(tens))
        if ones > 0 or not parts:
            parts.append(str(ones))
        return str(int(''.join(parts)))

    def _generate_concise_steps(self, problem: Problem, thousands: int, hundreds: int,
                                 tens: int, ones: int, malrule_answer: str) -> List[str]:
        """Generate concise steps with only formulas and values."""
        steps = []
        steps.append(f"Question: {problem.text}")

        # Build formula (showing the concatenation)
        parts = []
        if thousands > 0:
            parts.append(str(thousands))
        if hundreds > 0:
            parts.append(str(hundreds))
        if tens > 0:
            parts.append(str(tens))
        if ones > 0 or not parts:
            parts.append(str(ones))

        steps.append(f"Formula: Concatenate {', '.join(parts)}")
        steps.append(f"{''.join(parts)} = {malrule_answer}")
        steps.append(f"Answer: {malrule_answer}")
        return steps

    def _generate_verbose_steps(self, problem: Problem, thousands: int, hundreds: int,
                                 tens: int, ones: int, malrule_answer: str) -> List[str]:
        """Generate verbose steps with detailed explanations."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: Concatenate place value labels instead of adding values")
        steps.append("  Student thinks: 'The labels are the answer'")
        steps.append("")

        # Build description based on template
        parts = []
        part_descriptions = []

        if thousands > 0:
            parts.append(str(thousands))
            part_descriptions.append(f"{thousands} thousand{'s' if thousands != 1 else ''}")

        if hundreds > 0:
            parts.append(str(hundreds))
            part_descriptions.append(f"{hundreds} hundred{'s' if hundreds != 1 else ''}")

        if tens > 0:
            parts.append(str(tens))
            part_descriptions.append(f"{tens} ten{'s' if tens != 1 else ''}")

        if ones > 0 or (not parts and not thousands and not hundreds and not tens):
            parts.append(str(ones))
            part_descriptions.append(f"{ones} one{'s' if ones != 1 else ''}")

        steps.append(f"Student sees: {', '.join(part_descriptions)}")
        steps.append(f"Student thinks: 'Write down the numbers {', '.join(parts)}'")
        steps.append("")
        steps.append(f"MALRULE: Concatenate → {malrule_answer}")
        steps.append(f"  (Student doesn't understand these are values to ADD)")
        steps.append("")
        steps.append(f"Final Answer: {malrule_answer} (INCORRECT - concatenated labels!)")
        steps.append("")
        steps.append("Missing: Understanding place value decompositions represent ADDITION")
        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the Decompose-By-Place-Value-Label malrule across all templates.

        Args:
            problem: Place value decomposition problem to solve
            verbose: If True, generate detailed steps; if False, generate concise steps

        Returns:
            Solution with incorrect answer due to concatenation
        """
        template = problem.metadata.get('template', 'basic_regrouped_tens')

        # Get place values from metadata or operands
        thousands = problem.metadata.get('thousands', problem.operands[0])
        hundreds = problem.metadata.get('hundreds', problem.operands[1])
        tens = problem.metadata.get('tens', problem.operands[2])
        ones = problem.metadata.get('ones', problem.operands[3])

        # Calculate malrule answer using concatenation logic (face value error)
        parts = []
        if thousands > 0:
            parts.append(str(thousands))
        if hundreds > 0:
            parts.append(str(hundreds))
        if tens > 0:
            parts.append(str(tens))
        if ones > 0 or not parts:
            parts.append(str(ones))
        malrule_answer = str(int(''.join(parts)))

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, thousands, hundreds, tens, ones, malrule_answer)
        else:
            steps = self._generate_concise_steps(problem, thousands, hundreds, tens, ones, malrule_answer)

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
