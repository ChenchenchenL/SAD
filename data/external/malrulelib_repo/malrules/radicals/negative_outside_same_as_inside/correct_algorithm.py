"""
Correct algorithm for negative square roots.

Implements the correct interpretation of -√n.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import CorrectAlgorithm, Problem, Solution
import math


class NegativeSquareRootCorrectAlgorithm(CorrectAlgorithm):
    """
    Correct algorithm for evaluating -√n.

    The negative sign is outside the radical, so we first find √n,
    then negate the result.
    """

    def get_name(self) -> str:
        return "Correct Negative Square Root Algorithm"

    def get_description(self) -> str:
        return (
            "To evaluate -√n, first find the principal square root of n, "
            "then apply the negative sign. The notation -√n means -(√n), "
            "which is the opposite of the square root. This is different "
            "from √-n, which would be undefined for positive n in the real "
            "number system."
        )

    def _generate_concise_steps(self, problem: Problem, template: str, **kwargs) -> list:
        """Generate concise steps for the solution."""
        radicand = kwargs['radicand']
        base = kwargs['base']
        correct_answer = kwargs['correct_answer']

        steps = [f"Question: {problem.text}"]

        # Extract formula for word problems
        if template in ['word_problem', 'word_problem_diverse', 'word_problem_combined_ops']:
            problem_type = problem.metadata.get('problem_type', '')
            if problem_type == 'combined_operations':
                operation = problem.metadata.get('operation')
                if operation == 'addition':
                    radicand2 = kwargs['radicand2']
                    steps.append(f"Formula: -√{radicand} + √{radicand2}")
                else:  # multiplication
                    coeff = kwargs['coefficient']
                    steps.append(f"Formula: {coeff} × (-√{radicand})")
            else:
                steps.append(f"Formula: -√{radicand}")

        # Add calculation steps
        if template == 'combined_operations' or problem.metadata.get('problem_type') == 'combined_operations':
            operation = problem.metadata.get('operation')
            if operation == 'addition':
                radicand2 = kwargs['radicand2']
                base2 = kwargs['base2']
                result = kwargs['result']
                steps.append(f"-√{radicand} = -{base}")
                steps.append(f"√{radicand2} = {base2}")
                steps.append(f"{-base} + {base2} = {result}")
            else:  # multiplication
                coeff = kwargs['coefficient']
                result = kwargs['result']
                steps.append(f"-√{radicand} = -{base}")
                steps.append(f"{coeff} × ({-base}) = {result}")
        else:
            steps.append(f"-√{radicand} = -(√{radicand}) = -{base}")

        steps.append(f"Answer: {correct_answer}")
        return steps

    def _generate_verbose_steps(self, problem: Problem, template: str, **kwargs) -> list:
        """Generate verbose steps for the solution."""
        radicand = kwargs['radicand']
        base = kwargs['base']
        correct_answer = kwargs['correct_answer']

        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD: The negative sign is OUTSIDE the radical")
        steps.append("")

        if template == 'combined_operations' or problem.metadata.get('problem_type') == 'combined_operations':
            operation = problem.metadata.get('operation')
            if operation == 'addition':
                radicand2 = kwargs['radicand2']
                base2 = kwargs['base2']
                result = kwargs['result']
                steps.append(f"Step 1: Evaluate -√{radicand}")
                steps.append(f"  -√{radicand} = -(√{radicand}) = -({base}) = {-base}")
                steps.append(f"Step 2: Evaluate √{radicand2}")
                steps.append(f"  √{radicand2} = {base2}")
                steps.append(f"Step 3: Add the results")
                steps.append(f"  {-base} + {base2} = {result}")
            else:  # multiplication
                coeff = kwargs['coefficient']
                result = kwargs['result']
                steps.append(f"Step 1: Evaluate -√{radicand}")
                steps.append(f"  -√{radicand} = -(√{radicand}) = -({base}) = {-base}")
                steps.append(f"Step 2: Multiply by coefficient")
                steps.append(f"  {coeff} × ({-base}) = {result}")
        else:
            steps.append(f"Step 1: Recognize the negative is outside: -√{radicand} = -(√{radicand})")
            steps.append(f"Step 2: Find the square root: √{radicand} = {base}")
            steps.append(f"Step 3: Apply the negative: -({base}) = {-base}")

        steps.append("")
        steps.append(f"Answer: {correct_answer}")
        steps.append("")
        steps.append(
            "Key: The negative OUTSIDE the radical means 'opposite of the square root', "
            "which is valid. Different from √-n which is undefined in reals."
        )

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply correct algorithm for -√n."""
        template = problem.metadata.get('template', 'basic_negative_outside')
        radicand = problem.metadata.get('radicand', problem.operands[0])

        # COMPUTE base independently
        base = int(math.sqrt(radicand))

        # Build step_kwargs dictionary with all values needed for step generation
        step_kwargs = {
            'radicand': radicand,
            'base': base,
        }

        # COMPUTE correct answer based on template
        if template == 'combined_operations':
            operation = problem.metadata.get('operation')
            if operation == 'addition':
                radicand2 = problem.metadata['radicand2']
                base2 = int(math.sqrt(radicand2))
                result = -base + base2
                correct_answer = str(result)
                step_kwargs.update({
                    'radicand2': radicand2,
                    'base2': base2,
                    'result': result,
                })
            else:  # multiplication
                coeff = problem.metadata['coefficient']
                result = coeff * (-base)
                correct_answer = str(result)
                step_kwargs.update({
                    'coefficient': coeff,
                    'result': result,
                })
        elif template == 'in_equations':
            correct_answer = f"x = {-base}"
        elif template in ['word_problem', 'word_problem_diverse', 'word_problem_combined_ops']:
            # For word problems, need to check the context to format answer
            context_type = problem.metadata.get('context_type', '')
            problem_type = problem.metadata.get('problem_type', '')

            if problem_type == 'combined_operations':
                operation = problem.metadata.get('operation')
                if operation == 'addition':
                    radicand2 = problem.metadata['radicand2']
                    base2 = int(math.sqrt(radicand2))
                    result_val = -base + base2
                    step_kwargs.update({
                        'radicand2': radicand2,
                        'base2': base2,
                        'result': result_val,
                    })
                else:  # multiplication
                    coeff = problem.metadata['coefficient']
                    result_val = coeff * (-base)
                    step_kwargs.update({
                        'coefficient': coeff,
                        'result': result_val,
                    })

                # Format based on context
                if context_type == 'temperature_change':
                    correct_answer = f"{result_val} degrees"
                elif context_type == 'account_balance':
                    correct_answer = f"${result_val}"
                elif context_type == 'elevation_change':
                    correct_answer = f"{result_val} meters"
                elif context_type == 'scaled_loss':
                    correct_answer = f"${result_val} (loss)"
                elif context_type == 'velocity':
                    correct_answer = f"{result_val} m/s"
                elif context_type == 'debt_multiple':
                    correct_answer = f"${result_val} (debt)"
                else:
                    correct_answer = str(result_val)
            else:
                # Simple word problems
                if context_type == 'temperature':
                    correct_answer = f"{-base} degrees"
                elif context_type == 'elevation':
                    correct_answer = f"{-base} meters below sea level"
                elif context_type == 'debt':
                    correct_answer = f"${-base} (debt)"
                elif context_type == 'banking':
                    correct_answer = f"-${base}"
                elif context_type == 'physics_acceleration':
                    correct_answer = f"-{base} m/s²"
                elif context_type == 'stock_market':
                    correct_answer = f"-{base} points"
                else:
                    correct_answer = str(-base)
        else:
            # Basic templates
            correct_answer = str(-base)

        step_kwargs['correct_answer'] = correct_answer

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, template, **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, template, **step_kwargs)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
