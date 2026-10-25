"""
Malrule algorithm for Multiply-Across-For-Division.

Students think: (a/b)÷(c/d) = (a/b)×(c/d) = (a×c)/(b×d) [forget to flip!]
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution
import math

class MultiplyAcrossForDivisionMalrule(Malrule):
    """Student applies multiplication pattern to division without flipping."""

    def get_name(self):
        return "Multiply-Across-For-Division (Failure to Invert)"

    def get_description(self):
        return (
            "Student treats fraction division like multiplication, forgetting to invert (flip) the second "
            "fraction before multiplying. This error reflects a failure to apply the 'invert and multiply' "
            "algorithm correctly. For example, (2/3)÷(4/5) = (2×4)/(3×5) = 8/15 instead of the correct "
            "(2/3)×(5/4) = 10/12 = 5/6. Research shows this is a widespread difficulty for students as "
            "well as pre-service and in-service teachers (Ma, 1999; Tirosh, 2000)."
        )

    def calculate_expected_answer(self, problem: Problem) -> str:
        """
        Calculate the expected incorrect answer for this malrule.

        For Multiply-Across-For-Division:
        - Student treats division like multiplication
        - MALRULE: (a/b) ÷ (c/d) → (a×c)/(b×d) (forgets to flip!)
        - Then simplifies

        Example: (2/3) ÷ (4/5)
        - Correct: (2/3) × (5/4) = 10/12 = 5/6
        - MALRULE: (2×4)/(3×5) = 8/15

        Args:
            problem: Fraction division problem

        Returns:
            Expected incorrect answer as string "numer/denom"
        """
        from fractions import Fraction

        a = problem.metadata['a']
        b = problem.metadata['b']
        c = problem.metadata['c']
        d = problem.metadata['d']

        # MALRULE: multiply across without flipping
        # (a/b) ÷ (c/d) → (a×c)/(b×d) (incorrect!)
        malrule_frac = Fraction(a * c, b * d)

        return f"{malrule_frac.numerator}/{malrule_frac.denominator}"

    def _generate_concise_steps(self, problem: Problem, malrule_answer: str) -> list:
        """Generate concise steps with only formula and values."""
        from fractions import Fraction

        template = problem.metadata.get('template', 'basic_fraction_division')
        a = problem.metadata['a']
        b = problem.metadata['b']
        c = problem.metadata['c']
        d = problem.metadata['d']

        malrule_frac = Fraction(a * c, b * d)
        malrule_num = malrule_frac.numerator
        malrule_den = malrule_frac.denominator

        steps = []
        steps.append(f"Question: {problem.text}")

        if template == 'basic_fraction_division':
            steps.append(f"({a}/{b}) ÷ ({c}/{d}) = ({a}×{c})/({b}×{d})")
            steps.append(f"= {a*c}/{b*d}")
        elif template == 'whole_number_divisor':
            steps.append(f"({a}/{b}) ÷ {c} = ({a}×{c})/{b}")
            steps.append(f"= {a*c}/{b}")
        elif template == 'whole_number_dividend':
            steps.append(f"{a} ÷ ({c}/{d}) = ({a}×{c})/{d}")
            steps.append(f"= {a*c}/{d}")
        elif template == 'mixed_numbers':
            steps.append(f"({a}/{b}) ÷ ({c}/{d}) = ({a}×{c})/({b}×{d})")
            steps.append(f"= {a*c}/{b*d}")
        elif template in ['word_problem', 'word_problem_whole_divisor', 'word_problem_whole_dividend', 'word_problem_mixed']:
            steps.append(f"({a}/{b}) ÷ ({c}/{d}) = ({a}×{c})/({b}×{d})")
            steps.append(f"= {a*c}/{b*d}")

        if malrule_num != a * c or malrule_den != b * d:
            steps.append(f"= {malrule_answer}")

        steps.append(f"Answer: {malrule_answer}")
        return steps

    def _generate_verbose_steps(self, problem: Problem, malrule_answer: str) -> list:
        """Generate verbose steps with full explanations."""
        from fractions import Fraction

        template = problem.metadata.get('template', 'basic_fraction_division')
        a = problem.metadata['a']
        b = problem.metadata['b']
        c = problem.metadata['c']
        d = problem.metadata['d']

        malrule_frac = Fraction(a * c, b * d)
        malrule_num = malrule_frac.numerator
        malrule_den = malrule_frac.denominator

        steps = []

        if template == 'basic_fraction_division':
            steps.append(f"Problem: ({a}/{b}) ÷ ({c}/{d})")
            steps.append("")
            steps.append("MALRULE: Multiply across (forget to flip second fraction)")
            steps.append("  Student thinks: (a/b)÷(c/d) = (a/b)×(c/d) = (a×c)/(b×d)")
            steps.append("")
            steps.append("Step 1: Treat division like multiplication")
            steps.append(f"  ({a}/{b}) ÷ ({c}/{d})")
            steps.append(f"  Student: 'Just multiply across like multiplication!'")
            steps.append("")
            steps.append("Step 2: Multiply numerators")
            steps.append(f"  {a} × {c} = {a*c}")
            steps.append("")
            steps.append("Step 3: Multiply denominators")
            steps.append(f"  {b} × {d} = {b*d}")
            steps.append("")
            steps.append("Step 4: Form answer")
            steps.append(f"  = {a*c}/{b*d}")

            if malrule_num != a * c or malrule_den != b * d:
                steps.append(f"  = {malrule_num}/{malrule_den} (simplified)")

        elif template == 'whole_number_divisor':
            steps.append(f"Problem: ({a}/{b}) ÷ {c}")
            steps.append("")
            steps.append("MALRULE: Multiply by whole number instead of dividing")
            steps.append(f"  Student thinks: ({a}/{b}) ÷ {c} = ({a}×{c})/{b}")
            steps.append("")
            steps.append("Step 1: Treat division like multiplication")
            steps.append(f"  Student: 'Multiply the numerator by {c}'")
            steps.append(f"  {a} × {c} = {a*c}")
            steps.append("")
            steps.append("Step 2: Keep denominator")
            steps.append(f"  = {a*c}/{b}")

            if malrule_num != a * c or malrule_den != b:
                steps.append(f"  = {malrule_num}/{malrule_den} (simplified)")

        elif template == 'whole_number_dividend':
            steps.append(f"Problem: {a} ÷ ({c}/{d})")
            steps.append("")
            steps.append("MALRULE: Multiply by fraction instead of flipping it")
            steps.append(f"  Student thinks: {a} ÷ ({c}/{d}) = ({a}×{c})/{d}")
            steps.append("")
            steps.append("Step 1: Treat division like multiplication")
            steps.append(f"  Student: 'Multiply {a} by the fraction'")
            steps.append(f"  {a} × {c} = {a*c}")
            steps.append("")
            steps.append("Step 2: Put over denominator")
            steps.append(f"  = {a*c}/{d}")

            if malrule_num != a * c or malrule_den != d:
                steps.append(f"  = {malrule_num}/{malrule_den} (simplified)")

        elif template == 'mixed_numbers':
            whole1 = problem.metadata['whole1']
            whole2 = problem.metadata['whole2']
            frac1_num = problem.metadata['frac1_num']
            frac1_den = problem.metadata['frac1_den']
            frac2_num = problem.metadata['frac2_num']
            frac2_den = problem.metadata['frac2_den']

            steps.append(f"Problem: {whole1} {frac1_num}/{frac1_den} ÷ {whole2} {frac2_num}/{frac2_den}")
            steps.append("")
            steps.append("Step 1: Convert to improper fractions")
            steps.append(f"  {whole1} {frac1_num}/{frac1_den} = {a}/{b}")
            steps.append(f"  {whole2} {frac2_num}/{frac2_den} = {c}/{d}")
            steps.append("")
            steps.append("MALRULE: Multiply across (forget to flip)")
            steps.append(f"  ({a}/{b}) ÷ ({c}/{d})")
            steps.append(f"  Student: 'Multiply across like in multiplication!'")
            steps.append("")
            steps.append("Step 2: Multiply numerators")
            steps.append(f"  {a} × {c} = {a*c}")
            steps.append("")
            steps.append("Step 3: Multiply denominators")
            steps.append(f"  {b} × {d} = {b*d}")
            steps.append("")
            steps.append(f"  = {a*c}/{b*d}")

            if malrule_num != a * c or malrule_den != b * d:
                steps.append(f"  = {malrule_num}/{malrule_den} (simplified)")

        elif template in ['word_problem', 'word_problem_whole_divisor', 'word_problem_whole_dividend', 'word_problem_mixed']:
            context_type = problem.metadata.get('context_type', '')

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append(f"  This becomes: ({a}/{b}) ÷ ({c}/{d})")
            steps.append("")
            steps.append("MALRULE: Multiply across (forget to flip)")
            steps.append(f"  Student thinks: ({a}/{b}) × ({c}/{d})")

            if context_type == 'pizza_servings':
                steps.append("  Reasoning: 'Multiply the fractions together'")
            elif context_type == 'recipe_batches':
                steps.append("  Reasoning: 'Multiply the amounts together'")
            elif context_type == 'rope_pieces':
                steps.append("  Reasoning: 'Multiply the lengths together'")
            elif context_type == 'tasks':
                steps.append("  Reasoning: 'Multiply the times together'")

            steps.append("")
            steps.append(f"  {a} × {c} = {a*c}")
            steps.append(f"  {b} × {d} = {b*d}")
            steps.append(f"  = {a*c}/{b*d}")

            if malrule_num != a * c or malrule_den != b * d:
                steps.append(f"  = {malrule_num}/{malrule_den} (simplified)")

        steps.append("")
        unit_suffix = ''
        if template in ['word_problem', 'word_problem_whole_divisor', 'word_problem_whole_dividend', 'word_problem_mixed']:
            unit_suffix = f" {problem.metadata.get('unit', '')}" if problem.metadata.get('unit') else ''
        steps.append(f"Student's answer: {malrule_answer}{unit_suffix}")
        steps.append("")
        steps.append(
            f"The student incorrectly treats division like multiplication, "
            f"without flipping the second fraction. "
            f"The correct approach is Keep-Change-Flip."
        )

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the multiply-across-for-division malrule.

        Args:
            problem: The fraction division problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution showing incorrect reasoning (multiplying across without flipping)
        """
        from fractions import Fraction

        a = problem.metadata['a']
        b = problem.metadata['b']
        c = problem.metadata['c']
        d = problem.metadata['d']

        # Calculate malrule answer: multiply across without flipping
        # (a/b) ÷ (c/d) → (a×c)/(b×d) (incorrect!)
        malrule_frac = Fraction(a * c, b * d)
        malrule_num = malrule_frac.numerator
        malrule_den = malrule_frac.denominator
        malrule_answer = f"{malrule_num}/{malrule_den}"

        if verbose:
            steps = self._generate_verbose_steps(problem, malrule_answer)
        else:
            steps = self._generate_concise_steps(problem, malrule_answer)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
