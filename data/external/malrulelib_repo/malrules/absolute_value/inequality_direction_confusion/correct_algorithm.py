"""
Correct algorithm for absolute value inequalities.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import CorrectAlgorithm, Problem, Solution


class AbsoluteValueInequalityCorrectAlgorithm(CorrectAlgorithm):
    """Correctly solves absolute value inequalities by distinguishing < and > cases."""

    def get_name(self):
        return "Correct Absolute Value Inequality Solution"

    def get_description(self):
        return "Distinguishes between |x| < a (three-part) and |x| > a (two-part OR) inequalities"

    def _generate_compound_verbose_steps(self, problem: Problem, h: int, k: int, correct_answer: str) -> list:
        """Generate verbose steps for compound inequalities."""
        steps = []
        steps.append(f"Problem: Solve |x - {h}| < {k}")
        steps.append("")
        steps.append("CORRECT METHOD: Less than means INSIDE the interval")
        steps.append(f"  |x - {h}| < {k} means 'x is within {k} units of {h}'")
        steps.append("")
        steps.append(f"  |x - {h}| < {k}")
        steps.append(f"  -{k} < x - {h} < {k}")
        steps.append(f"  Add {h} to all parts:")
        steps.append(f"  {h - k} < x < {h + k}")
        steps.append("")
        steps.append(f"Answer: {correct_answer}")
        return steps

    def _generate_compound_concise_steps(self, problem: Problem, h: int, k: int, correct_answer: str) -> list:
        """Generate concise steps for compound inequalities."""
        steps = []
        steps.append(f"Problem: Solve |x - {h}| < {k}")
        steps.append(f"|x - {h}| < {k}")
        steps.append(f"-{k} < x - {h} < {k}")
        steps.append(f"{h - k} < x < {h + k}")
        steps.append(correct_answer)
        return steps

    def _handle_compound_inequality(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle compound inequalities like |x - h| < k."""
        h = problem.metadata['offset']
        k = problem.metadata['bound']

        # Actually compute the answer
        correct_answer = f"{h - k} < x < {h + k}"

        if verbose:
            steps = self._generate_compound_verbose_steps(problem, h, k, correct_answer)
        else:
            steps = self._generate_compound_concise_steps(problem, h, k, correct_answer)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _generate_coefficient_verbose_steps(self, problem: Problem, a: int, k: int, threshold: int, correct_answer: str) -> list:
        """Generate verbose steps for coefficient inequalities."""
        steps = []
        steps.append(f"Problem: Solve |{a}x| > {k}")
        steps.append("")
        steps.append("CORRECT METHOD: Greater than means OUTSIDE the interval")
        steps.append(f"  |{a}x| > {k}")
        steps.append(f"  Divide by {a}:")
        steps.append(f"  |x| > {threshold}")
        steps.append(f"  This gives two regions:")
        steps.append(f"  x < -{threshold}  OR  x > {threshold}")
        steps.append("")
        steps.append(f"Answer: {correct_answer}")
        return steps

    def _generate_coefficient_concise_steps(self, problem: Problem, a: int, k: int, threshold: int, correct_answer: str) -> list:
        """Generate concise steps for coefficient inequalities."""
        steps = []
        steps.append(f"Problem: Solve |{a}x| > {k}")
        steps.append(f"|{a}x| > {k}")
        steps.append(f"|x| > {threshold}")
        steps.append(f"x < -{threshold} OR x > {threshold}")
        steps.append(correct_answer)
        return steps

    def _handle_coefficient_inequality(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle inequalities with coefficients like |ax| > k."""
        a = problem.metadata['coefficient']
        k = problem.metadata['bound']

        # Actually compute the answer
        threshold = k // a
        correct_answer = f"x < -{threshold} OR x > {threshold}"

        if verbose:
            steps = self._generate_coefficient_verbose_steps(problem, a, k, threshold, correct_answer)
        else:
            steps = self._generate_coefficient_concise_steps(problem, a, k, threshold, correct_answer)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _generate_verbose_steps(self, problem: Problem, problem_type: str, bound: int, inequality_type: str, correct_answer: str) -> list:
        """Generate verbose, explanatory steps."""
        steps = []
        if inequality_type == 'less_than':
            if problem_type == 'less_than_or_equal':
                steps.append(f"Problem: Solve |x| ≤ {bound}")
                steps.append("")
                steps.append("CORRECT METHOD: Less than or equal means INSIDE the interval (including endpoints)")
                steps.append(f"  |x| ≤ {bound} means 'x is within {bound} units of 0 OR exactly {bound} units away'")
                steps.append(f"  This is: 'x is between -{bound} and {bound}, inclusive'")
                steps.append("")
                steps.append(f"  |x| ≤ {bound}")
                steps.append(f"  -{bound} ≤ x ≤ {bound}")
                steps.append("")
                steps.append(f"Answer: {correct_answer}")
                steps.append("")
                steps.append(
                    f"This is a three-part inequality with x in the closed interval [-{bound}, {bound}]. "
                    f"We can verify: x={bound} should work, and |{bound}| = {bound} ≤ {bound} ✓"
                )
            elif problem_type == 'word_problem_context':
                steps.append(f"Problem: {problem.text}")
                steps.append("")
                word_problem_type = problem.metadata.get('word_problem_type', 'basic_less')
                symbolic = problem.metadata.get('symbolic_form', f"|x| < {bound}")

                if word_problem_type == 'compound_less':
                    h = problem.metadata.get('offset', 5)
                    k = problem.metadata.get('bound', bound)
                    steps.append("CORRECT METHOD: Identify embedded formula and solve")
                    steps.append(f"  Step 1: The problem involves: {symbolic}")
                    steps.append(f"  This means x must be within {k} units of {h}")
                    steps.append(f"  Step 2: Less than means INSIDE the interval")
                    steps.append(f"  Three-part inequality: {correct_answer}")
                elif word_problem_type == 'less_equal':
                    steps.append("CORRECT METHOD: Identify embedded formula and solve")
                    steps.append(f"  Step 1: The problem involves: {symbolic}")
                    steps.append(f"  This means x magnitude can be at most {bound} (inclusive)")
                    steps.append(f"  Step 2: Less than or equal means INSIDE with endpoints")
                    steps.append(f"  Three-part inequality: {correct_answer}")
                else:
                    steps.append("CORRECT METHOD: Identify embedded formula and solve")
                    steps.append(f"  Step 1: The situation translates to: {symbolic}")
                    steps.append(f"  This means values are within {bound} units of origin")
                    steps.append(f"  Step 2: Less than means INSIDE the interval")
                    steps.append(f"  Three-part inequality: {correct_answer}")
                steps.append("")
                steps.append(f"Answer: {correct_answer}")
            else:
                steps.append(f"Problem: Solve |x| < {bound}")
                steps.append("")
                steps.append("CORRECT METHOD: Less than means INSIDE the interval")
                steps.append(f"  |x| < {bound} means 'x is within {bound} units of 0'")
                steps.append(f"  This is the same as: 'x is between -{bound} and {bound}'")
                steps.append("")
                steps.append(f"  |x| < {bound}")
                steps.append(f"  -{bound} < x < {bound}")
                steps.append("")
                steps.append("Number line: [====●====] where ● is at 0")
                steps.append(f"             -{bound}      {bound}")
                steps.append("")
                steps.append(f"Answer: {correct_answer}")
                steps.append("")
                steps.append(
                    f"This is a three-part inequality showing x is in the interval ({-bound}, {bound}). "
                    f"We can verify: x=0 should work, and |0| = 0 < {bound} ✓"
                )
        else:
            if problem_type == 'word_problem_context':
                steps.append(f"Problem: {problem.text}")
                steps.append("")
                word_problem_type = problem.metadata.get('word_problem_type', 'basic_greater')
                symbolic = problem.metadata.get('symbolic_form', f"|x| > {bound}")

                if word_problem_type == 'coefficient_greater':
                    a = problem.metadata.get('coefficient', 2)
                    k = problem.metadata.get('bound', bound)
                    steps.append("CORRECT METHOD: Identify embedded formula and solve")
                    steps.append(f"  Step 1: The problem involves: {symbolic}")
                    steps.append(f"  Step 2: Greater than means OUTSIDE the interval")
                    steps.append(f"  This gives two separate regions")
                    steps.append(f"  Two-part OR inequality: {correct_answer}")
                else:
                    steps.append("CORRECT METHOD: Identify embedded formula and solve")
                    steps.append(f"  Step 1: The situation translates to: {symbolic}")
                    steps.append(f"  This means x must be more than {bound} units from origin")
                    steps.append(f"  Step 2: Greater than means OUTSIDE the interval")
                    steps.append(f"  Two-part OR inequality: {correct_answer}")
                steps.append("")
                steps.append(f"Answer: {correct_answer}")
            else:
                steps.append(f"Problem: Solve |x| > {bound}")
                steps.append("")
                steps.append("CORRECT METHOD: Greater than means OUTSIDE the interval")
                steps.append(f"  |x| > {bound} means 'x is more than {bound} units from 0'")
                steps.append(f"  This happens in TWO separate regions:")
                steps.append(f"    - Left region: x < -{bound}")
                steps.append(f"    - Right region: x > {bound}")
                steps.append("")
                steps.append(f"  |x| > {bound}")
                steps.append(f"  x < -{bound}  OR  x > {bound}")
                steps.append("")
                steps.append("Number line: ←====)     (====→ where ) is gap at ±bound")
                steps.append(f"             -{bound}      {bound}")
                steps.append("")
                steps.append(f"Answer: {correct_answer}")
                steps.append("")
                steps.append(
                    f"This is a two-part OR statement showing x is in two separate regions. "
                    f"We can verify: x=0 should NOT work, and |0| = 0 is NOT > {bound} ✓"
                )
        return steps

    def _generate_concise_steps(self, problem: Problem, problem_type: str, bound: int, inequality_type: str, correct_answer: str) -> list:
        """Generate concise steps with just formulas and values."""
        steps = []
        if inequality_type == 'less_than':
            if problem_type == 'less_than_or_equal':
                steps.append(f"Problem: Solve |x| ≤ {bound}")
                steps.append(f"|x| ≤ {bound}")
                steps.append(f"-{bound} ≤ x ≤ {bound}")
            elif problem_type == 'word_problem_context':
                steps.append(f"Problem: {problem.text}")
                symbolic = problem.metadata.get('symbolic_form', f"|x| < {bound}")
                steps.append(symbolic)
                steps.append(f"-{bound} < x < {bound}")
            else:
                steps.append(f"Problem: Solve |x| < {bound}")
                steps.append(f"|x| < {bound}")
                steps.append(f"-{bound} < x < {bound}")
        else:
            if problem_type == 'word_problem_context':
                steps.append(f"Problem: {problem.text}")
                symbolic = problem.metadata.get('symbolic_form', f"|x| > {bound}")
                steps.append(symbolic)
                steps.append(f"x < -{bound} OR x > {bound}")
            else:
                steps.append(f"Problem: Solve |x| > {bound}")
                steps.append(f"|x| > {bound}")
                steps.append(f"x < -{bound} OR x > {bound}")

        steps.append(correct_answer)
        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct absolute value inequality algorithm.

        Args:
            problem: The absolute value inequality problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution showing correct inequality pattern
        """
        problem_type = problem.metadata.get('problem_type', 'less_than')

        # Handle special problem types
        if problem_type == 'compound_inequality':
            return self._handle_compound_inequality(problem, verbose=verbose)
        elif problem_type == 'inequality_with_coefficient':
            return self._handle_coefficient_inequality(problem, verbose=verbose)

        bound = problem.metadata['bound']
        inequality_type = problem.metadata['inequality_type']

        # Actually compute the correct answer based on inequality type
        if inequality_type == 'less_than':
            if problem_type == 'less_than_or_equal':
                correct_answer = f"-{bound} ≤ x ≤ {bound}"
            else:
                correct_answer = f"-{bound} < x < {bound}"
        else:  # greater_than
            correct_answer = f"x < -{bound} OR x > {bound}"

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, problem_type, bound, inequality_type, correct_answer)
        else:
            steps = self._generate_concise_steps(problem, problem_type, bound, inequality_type, correct_answer)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
