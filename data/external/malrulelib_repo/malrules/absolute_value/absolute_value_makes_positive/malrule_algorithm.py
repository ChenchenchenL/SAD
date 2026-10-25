"""
Malrule algorithm for Absolute-Value-Makes-Positive.

Students think absolute value "makes negatives positive" so |x| = -3 has solution x = 3
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution

class AbsoluteValueMakesPositiveMalrule(Malrule):
    """Student thinks absolute value reverses negative to positive."""

    def get_name(self):
        return "Absolute-Value-Makes-Positive"

    def get_description(self):
        return (
            "Students hold the mental picture that 'absolute values make negative signs positive' and "
            "apply this symbol-based process rather than understanding that absolute value represents "
            "distance from zero. When presented with |x| = -3, they incorrectly reverse the sign to get "
            "x = 3, failing to recognize that absolute value output is always non-negative and the "
            "equation has no solution."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        template = problem.metadata.get('template', 'basic_equation')
        negative_value = problem.metadata['negative_value']

        if template == 'basic_equation':
            return f"x = {-negative_value}"
        elif template == 'expression_inside':
            a = problem.metadata.get('a', 0)
            return f"x = {-negative_value - a}"
        elif template == 'inequality':
            inequality_type = problem.metadata.get('inequality_type', '<')
            return f"x {inequality_type} {-negative_value}"
        elif template == 'compound_expression':
            a = problem.metadata.get('a', 2)
            b = problem.metadata.get('b', 0)
            reversed_value = -negative_value
            malrule_x = (reversed_value - b) // a if (reversed_value - b) % a == 0 else (reversed_value - b) / a
            if isinstance(malrule_x, float):
                return f"x = {malrule_x:.2f}"
            else:
                return f"x = {malrule_x}"
        elif template == 'word_problem':
            word_problem_type = problem.metadata.get('word_problem_type', 'basic_x')
            context_type = problem.metadata.get('context_type', 'distance')

            if word_problem_type == 'basic_x':
                if context_type == 'distance':
                    return f"x = {-negative_value} meters"
                elif context_type == 'temperature':
                    return f"x = {-negative_value} degrees"
                elif context_type == 'money':
                    return f"x = ${-negative_value}"
                else:
                    return f"x = {-negative_value}"
            elif word_problem_type == 'x_plus_a':
                a = problem.metadata.get('a', 0)
                if context_type == 'distance':
                    return f"x = {-negative_value - a} meters"
                elif context_type == 'temperature':
                    return f"x = {-negative_value - a} degrees"
                elif context_type == 'money':
                    return f"x = ${-negative_value - a}"
                else:
                    return f"x = {-negative_value - a}"
            elif word_problem_type == 'ax_plus_b':
                a = problem.metadata.get('a', 2)
                b = problem.metadata.get('b', 0)
                malrule_x = (-negative_value - b) // a if (-negative_value - b) % a == 0 else round((-negative_value - b) / a, 2)
                if context_type == 'production':
                    return f"x = {malrule_x} items"
                elif context_type == 'distance':
                    return f"x = {malrule_x} km/h"
                elif context_type == 'money':
                    return f"x = ${malrule_x}"
                else:
                    return f"x = {malrule_x}"
            else:
                return f"x = {-negative_value}"
        else:
            return f"x = {-negative_value}"

    def _generate_verbose_steps(self, problem: Problem, template: str, negative_value: int, malrule_answer: str) -> list:
        """Generate verbose, explanatory steps."""
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: Think absolute value 'makes negatives positive'")
        steps.append("")

        if template == 'basic_equation':
            steps.append(f"  Student sees: |x| = {negative_value}")
            steps.append(f"  Student thinks: 'The absolute value made x into {negative_value}'")
            steps.append(f"  So to undo it, reverse the sign: x = {-negative_value}")

        elif template == 'expression_inside':
            a = problem.metadata.get('a', 0)
            steps.append(f"  Student thinks absolute value can be 'reversed'")
            steps.append(f"  They make {negative_value} positive: {-negative_value}")
            steps.append(f"  Then solve: x + {a} = {-negative_value}")
            steps.append(f"  Result: x = {-negative_value - a}")

        elif template == 'inequality':
            inequality_type = problem.metadata.get('inequality_type', '<')
            steps.append(f"  Student thinks absolute value can be 'reversed'")
            steps.append(f"  They make {negative_value} positive: {-negative_value}")
            steps.append(f"  Then write: x {inequality_type} {-negative_value}")

        elif template == 'compound_expression':
            a = problem.metadata.get('a', 2)
            b = problem.metadata.get('b', 0)
            steps.append(f"  Student reverses the negative: {negative_value} → {-negative_value}")
            steps.append(f"  Then solves {a}x + {b} = {-negative_value}")
            steps.append(f"  Gets: {malrule_answer}")

        elif template == 'word_problem':
            context_type = problem.metadata.get('context_type', 'distance')
            steps.append(f"  Student doesn't recognize that {context_type} cannot be negative")
            steps.append(f"  They reverse the sign: {negative_value} → {-negative_value}")

        steps.append("")
        steps.append(f"Student's answer: {malrule_answer}")
        steps.append("")
        steps.append(
            f"The student misunderstands absolute value. They think it's a reversible operation "
            f"that 'makes negatives positive', so they try to 'undo' it by reversing the sign. "
            f"They don't understand that absolute value OUTPUT is always non-negative, "
            f"so |x| can NEVER equal a negative number like {negative_value}. "
            f"The correct answer is 'No solution'."
        )

        return steps

    def _generate_concise_steps(self, problem: Problem, template: str, negative_value: int, malrule_answer: str) -> list:
        """Generate concise steps with just formulas and values."""
        steps = [f"Problem: {problem.text}"]

        if template == 'basic_equation':
            steps.append(f"|x| = {negative_value}")
            steps.append(f"x = {-negative_value}")

        elif template == 'expression_inside':
            a = problem.metadata.get('a', 0)
            steps.append(f"|x + {a}| = {negative_value}")
            steps.append(f"x + {a} = {-negative_value}")
            steps.append(f"x = {-negative_value - a}")

        elif template == 'inequality':
            inequality_type = problem.metadata.get('inequality_type', '<')
            steps.append(f"|x| {inequality_type} {negative_value}")
            steps.append(f"x {inequality_type} {-negative_value}")

        elif template == 'compound_expression':
            a = problem.metadata.get('a', 2)
            b = problem.metadata.get('b', 0)
            steps.append(f"|{a}x + {b}| = {negative_value}")
            steps.append(f"{a}x + {b} = {-negative_value}")
            steps.append(malrule_answer)

        elif template == 'word_problem':
            word_problem_type = problem.metadata.get('word_problem_type', 'basic_x')

            if word_problem_type == 'basic_x':
                steps.append(f"|x| = {negative_value}")
                steps.append(f"x = {-negative_value}")
            elif word_problem_type == 'x_plus_a':
                a = problem.metadata.get('a', 0)
                steps.append(f"|x + {a}| = {negative_value}")
                steps.append(f"x + {a} = {-negative_value}")
                steps.append(f"x = {-negative_value - a}")
            else:  # ax_plus_b
                a = problem.metadata.get('a', 2)
                b = problem.metadata.get('b', 0)
                if a == 1:
                    expr = f"x"
                elif a == -1:
                    expr = f"-x"
                else:
                    expr = f"{a}x"
                sign_str = "+" if b >= 0 else ""
                if b != 0:
                    expr += f" {sign_str} {b}"
                steps.append(f"|{expr}| = {negative_value}")
                steps.append(f"{expr} = {-negative_value}")
                steps.append(malrule_answer)

        steps.append(malrule_answer)
        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the absolute-value-makes-positive malrule across all templates.

        Args:
            problem: The absolute value equation/inequality problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution showing incorrect reversal of sign
        """
        template = problem.metadata.get('template', 'basic_equation')
        negative_value = problem.metadata['negative_value']

        # Actually compute the malrule answer by reversing the sign
        if template == 'basic_equation':
            malrule_answer = f"x = {-negative_value}"
        elif template == 'expression_inside':
            a = problem.metadata.get('a', 0)
            malrule_answer = f"x = {-negative_value - a}"
        elif template == 'inequality':
            inequality_type = problem.metadata.get('inequality_type', '<')
            malrule_answer = f"x {inequality_type} {-negative_value}"
        elif template == 'compound_expression':
            a = problem.metadata.get('a', 2)
            b = problem.metadata.get('b', 0)
            reversed_value = -negative_value
            malrule_x = (reversed_value - b) // a if (reversed_value - b) % a == 0 else (reversed_value - b) / a
            if isinstance(malrule_x, float):
                malrule_answer = f"x = {malrule_x:.2f}"
            else:
                malrule_answer = f"x = {malrule_x}"
        elif template == 'word_problem':
            word_problem_type = problem.metadata.get('word_problem_type', 'basic_x')
            context_type = problem.metadata.get('context_type', 'distance')

            if word_problem_type == 'basic_x':
                if context_type == 'distance':
                    malrule_answer = f"x = {-negative_value} meters"
                elif context_type == 'temperature':
                    malrule_answer = f"x = {-negative_value} degrees"
                elif context_type == 'money':
                    malrule_answer = f"x = ${-negative_value}"
                else:
                    malrule_answer = f"x = {-negative_value}"
            elif word_problem_type == 'x_plus_a':
                a = problem.metadata.get('a', 0)
                if context_type == 'distance':
                    malrule_answer = f"x = {-negative_value - a} meters"
                elif context_type == 'temperature':
                    malrule_answer = f"x = {-negative_value - a} degrees"
                elif context_type == 'money':
                    malrule_answer = f"x = ${-negative_value - a}"
                else:
                    malrule_answer = f"x = {-negative_value - a}"
            elif word_problem_type == 'ax_plus_b':
                a = problem.metadata.get('a', 2)
                b = problem.metadata.get('b', 0)
                malrule_x = (-negative_value - b) // a if (-negative_value - b) % a == 0 else round((-negative_value - b) / a, 2)
                if context_type == 'production':
                    malrule_answer = f"x = {malrule_x} items"
                elif context_type == 'distance':
                    malrule_answer = f"x = {malrule_x} km/h"
                elif context_type == 'money':
                    malrule_answer = f"x = ${malrule_x}"
                else:
                    malrule_answer = f"x = {malrule_x}"
            else:
                malrule_answer = f"x = {-negative_value}"
        else:
            malrule_answer = f"x = {-negative_value}"

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, template, negative_value, malrule_answer)
        else:
            steps = self._generate_concise_steps(problem, template, negative_value, malrule_answer)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
