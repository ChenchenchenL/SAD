"""
Malrule algorithm for Inequality-Direction-Confusion.

Students don't distinguish between less than and greater than cases in absolute value inequalities.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution

class InequalityDirectionConfusionMalrule(Malrule):
    """Student confuses the two types of absolute value inequalities."""

    def get_name(self):
        return "Inequality-Direction-Confusion"

    def get_description(self):
        return (
            "Students confuse the solution patterns for absolute value inequalities, applying "
            "the 'less than' pattern (three-part inequality) to 'greater than' problems and "
            "vice versa. Research shows this error affects 12-27% of students on specific problem "
            "types, stemming from failure to connect the inequality direction to geometric meaning "
            "(inside vs. outside an interval on the number line)."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # The malrule swaps the patterns:
        # - For less_than, student gives the greater_than pattern
        # - For greater_than, student gives the less_than pattern

        problem_type = problem.metadata.get('problem_type', 'less_than')

        # Handle special problem types
        if problem_type == 'compound_inequality':
            h = problem.metadata['offset']
            k = problem.metadata['bound']
            return f"x < {h - k} OR x > {h + k}"
        elif problem_type == 'inequality_with_coefficient':
            a = problem.metadata['coefficient']
            k = problem.metadata['bound']
            threshold = k // a
            return f"-{threshold} < x < {threshold}"

        bound = problem.metadata['bound']
        inequality_type = problem.metadata['inequality_type']

        if inequality_type == 'less_than':
            if problem_type == 'less_than_or_equal':
                return f"x ≤ -{bound} OR x ≥ {bound}"
            else:
                return f"x < -{bound} OR x > {bound}"
        else:  # greater_than
            return f"-{bound} < x < {bound}"

    def _generate_compound_verbose_steps(self, problem: Problem, h: int, k: int, malrule_answer: str) -> list:
        """Generate verbose steps for compound inequalities with malrule."""
        steps = []
        steps.append(f"Problem: Solve |x - {h}| < {k}")
        steps.append("")
        steps.append("MALRULE: Student applies 'greater than' pattern to 'less than' inequality")
        steps.append(f"  Student confuses the pattern even with offset")
        steps.append(f"  Student writes: x < {h - k} OR x > {h + k}")
        steps.append("")
        steps.append(f"Student's answer: {malrule_answer}")
        steps.append("")
        steps.append(
            f"The student incorrectly applies the greater-than pattern (two separate regions) "
            f"to a less-than inequality, even with an offset from the origin."
        )
        return steps

    def _generate_compound_concise_steps(self, problem: Problem, h: int, k: int, malrule_answer: str) -> list:
        """Generate concise steps for compound inequalities with malrule."""
        steps = []
        steps.append(f"Problem: Solve |x - {h}| < {k}")
        steps.append(f"|x - {h}| < {k}")
        steps.append(f"x < {h - k} OR x > {h + k}")
        steps.append(malrule_answer)
        return steps

    def _handle_compound_inequality(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle compound inequalities with malrule."""
        h = problem.metadata['offset']
        k = problem.metadata['bound']

        # Apply malrule: student applies 'greater than' pattern to 'less than' inequality
        malrule_answer = f"x < {h - k} OR x > {h + k}"

        if verbose:
            steps = self._generate_compound_verbose_steps(problem, h, k, malrule_answer)
        else:
            steps = self._generate_compound_concise_steps(problem, h, k, malrule_answer)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _generate_coefficient_verbose_steps(self, problem: Problem, a: int, k: int, threshold: int, malrule_answer: str) -> list:
        """Generate verbose steps for coefficient inequalities with malrule."""
        steps = []
        steps.append(f"Problem: Solve |{a}x| > {k}")
        steps.append("")
        steps.append("MALRULE: Student applies 'less than' pattern to 'greater than' inequality")
        steps.append(f"  Student divides: |x| > {threshold}")
        steps.append(f"  But then applies wrong pattern: -{threshold} < x < {threshold}")
        steps.append("")
        steps.append(f"Student's answer: {malrule_answer}")
        steps.append("")
        steps.append(
            f"The student incorrectly applies the less-than pattern (three-part inequality) "
            f"to a greater-than inequality."
        )
        return steps

    def _generate_coefficient_concise_steps(self, problem: Problem, a: int, k: int, threshold: int, malrule_answer: str) -> list:
        """Generate concise steps for coefficient inequalities with malrule."""
        steps = []
        steps.append(f"Problem: Solve |{a}x| > {k}")
        steps.append(f"|{a}x| > {k}")
        steps.append(f"|x| > {threshold}")
        steps.append(f"-{threshold} < x < {threshold}")
        steps.append(malrule_answer)
        return steps

    def _handle_coefficient_inequality(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle inequalities with coefficients with malrule."""
        a = problem.metadata['coefficient']
        k = problem.metadata['bound']

        # Apply malrule: student applies 'less than' pattern to 'greater than' inequality
        threshold = k // a
        malrule_answer = f"-{threshold} < x < {threshold}"

        if verbose:
            steps = self._generate_coefficient_verbose_steps(problem, a, k, threshold, malrule_answer)
        else:
            steps = self._generate_coefficient_concise_steps(problem, a, k, threshold, malrule_answer)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _generate_verbose_steps(self, problem: Problem, problem_type: str, bound: int, inequality_type: str, malrule_answer: str) -> list:
        """Generate verbose, explanatory steps for malrule."""
        steps = []
        if inequality_type == 'less_than':
            if problem_type == 'less_than_or_equal':
                steps.append(f"Problem: Solve |x| ≤ {bound}")
                steps.append("")
                steps.append("MALRULE: Student applies 'greater than' pattern to 'less than or equal' inequality")
                steps.append(f"  Student thinks: |x| ≤ {bound} means x is far from 0")
                steps.append(f"  So: x ≤ -{bound} OR x ≥ {bound}")
                steps.append("")
                steps.append(f"Student's answer: {malrule_answer}")
                steps.append("")
                steps.append(
                    f"The student incorrectly applies the greater-than pattern (two separate regions) "
                    f"to a less-than-or-equal inequality."
                )
            elif problem_type == 'word_problem_context':
                steps.append(f"Problem: {problem.text}")
                steps.append("")
                word_problem_type = problem.metadata.get('word_problem_type', 'basic_less')
                symbolic = problem.metadata.get('symbolic_form', f"|x| < {bound}")

                steps.append("MALRULE: Student applies wrong pattern to word problem")
                steps.append(f"  Step 1: Student identifies: {symbolic}")

                if word_problem_type == 'compound_less':
                    h = problem.metadata.get('offset', 5)
                    k = problem.metadata.get('bound', bound)
                    steps.append(f"  Step 2: Student confuses pattern for |x - {h}| < {k}")
                    steps.append(f"  Applies 'greater than' pattern: x < {h - k} OR x > {h + k}")
                elif word_problem_type == 'less_equal':
                    steps.append(f"  Step 2: Student confuses pattern for |x| ≤ {bound}")
                    steps.append(f"  Applies 'greater than' pattern: x ≤ -{bound} OR x ≥ {bound}")
                else:
                    steps.append(f"  Step 2: Student applies 'greater than' pattern")
                    steps.append(f"  Incorrectly uses OR pattern: x < -{bound} OR x > {bound}")

                steps.append("")
                steps.append(f"Student's answer: {malrule_answer}")
                steps.append("")
                steps.append(
                    f"The student incorrectly applies the greater-than pattern (two separate regions) "
                    f"to a less-than inequality in a real-world context."
                )
            else:
                steps.append(f"Problem: Solve |x| < {bound}")
                steps.append("")
                steps.append("MALRULE: Student applies 'greater than' pattern to 'less than' inequality")
                steps.append(f"  Student thinks: |x| < {bound} means x is far from 0")
                steps.append(f"  So: x < -{bound} OR x > {bound}")
                steps.append("")
                steps.append(f"Student's answer: {malrule_answer}")
                steps.append("")
                steps.append(
                    f"The student incorrectly applies the greater-than pattern (two separate regions) "
                    f"to a less-than inequality. They don't understand that |x| < {bound} means "
                    f"x is WITHIN {bound} units of 0, not outside."
                )
        else:
            if problem_type == 'word_problem_context':
                steps.append(f"Problem: {problem.text}")
                steps.append("")
                word_problem_type = problem.metadata.get('word_problem_type', 'basic_greater')
                symbolic = problem.metadata.get('symbolic_form', f"|x| > {bound}")

                steps.append("MALRULE: Student applies wrong pattern to word problem")
                steps.append(f"  Step 1: Student identifies: {symbolic}")

                if word_problem_type == 'coefficient_greater':
                    a = problem.metadata.get('coefficient', 2)
                    k = problem.metadata.get('bound', bound)
                    steps.append(f"  Step 2: Student confuses pattern for |{a}x| > {k}")
                    steps.append(f"  Applies 'less than' pattern: -{k//a} < x < {k//a}")
                else:
                    steps.append(f"  Step 2: Student applies 'less than' pattern")
                    steps.append(f"  Incorrectly uses three-part: -{bound} < x < {bound}")

                steps.append("")
                steps.append(f"Student's answer: {malrule_answer}")
                steps.append("")
                steps.append(
                    f"The student incorrectly applies the less-than pattern (three-part inequality) "
                    f"to a greater-than inequality in a real-world context."
                )
            else:
                steps.append(f"Problem: Solve |x| > {bound}")
                steps.append("")
                steps.append("MALRULE: Student applies 'less than' pattern to 'greater than' inequality")
                steps.append(f"  Student thinks: |x| > {bound} means x is between two values")
                steps.append(f"  So: -{bound} < x < {bound}")
                steps.append("")
                steps.append(f"Student's answer: {malrule_answer}")
                steps.append("")
                steps.append(
                    f"The student incorrectly applies the less-than pattern (three-part inequality) "
                    f"to a greater-than inequality. They don't understand that |x| > {bound} means "
                    f"x is MORE THAN {bound} units from 0, in two separate regions."
                )
        return steps

    def _generate_concise_steps(self, problem: Problem, problem_type: str, bound: int, inequality_type: str, malrule_answer: str) -> list:
        """Generate concise steps with just formulas and values."""
        steps = []
        if inequality_type == 'less_than':
            if problem_type == 'less_than_or_equal':
                steps.append(f"Problem: Solve |x| ≤ {bound}")
                steps.append(f"|x| ≤ {bound}")
                steps.append(f"x ≤ -{bound} OR x ≥ {bound}")
            elif problem_type == 'word_problem_context':
                steps.append(f"Problem: {problem.text}")
                symbolic = problem.metadata.get('symbolic_form', f"|x| < {bound}")
                steps.append(symbolic)
                steps.append(f"x < -{bound} OR x > {bound}")
            else:
                steps.append(f"Problem: Solve |x| < {bound}")
                steps.append(f"|x| < {bound}")
                steps.append(f"x < -{bound} OR x > {bound}")
        else:
            if problem_type == 'word_problem_context':
                steps.append(f"Problem: {problem.text}")
                symbolic = problem.metadata.get('symbolic_form', f"|x| > {bound}")
                steps.append(symbolic)
                steps.append(f"-{bound} < x < {bound}")
            else:
                steps.append(f"Problem: Solve |x| > {bound}")
                steps.append(f"|x| > {bound}")
                steps.append(f"-{bound} < x < {bound}")

        steps.append(malrule_answer)
        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the inequality-direction-confusion malrule.

        Args:
            problem: The absolute value inequality problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution showing incorrect inequality pattern
        """
        problem_type = problem.metadata.get('problem_type', 'less_than')

        # Handle special problem types
        if problem_type == 'compound_inequality':
            return self._handle_compound_inequality(problem, verbose=verbose)
        elif problem_type == 'inequality_with_coefficient':
            return self._handle_coefficient_inequality(problem, verbose=verbose)

        bound = problem.metadata['bound']
        inequality_type = problem.metadata['inequality_type']

        # Apply malrule: swap the patterns
        if inequality_type == 'less_than':
            # Student applies 'greater than' pattern to 'less than' inequality
            if problem_type == 'less_than_or_equal':
                malrule_answer = f"x ≤ -{bound} OR x ≥ {bound}"
            else:
                malrule_answer = f"x < -{bound} OR x > {bound}"
        else:  # greater_than
            # Student applies 'less than' pattern to 'greater than' inequality
            malrule_answer = f"-{bound} < x < {bound}"

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, problem_type, bound, inequality_type, malrule_answer)
        else:
            steps = self._generate_concise_steps(problem, problem_type, bound, inequality_type, malrule_answer)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
