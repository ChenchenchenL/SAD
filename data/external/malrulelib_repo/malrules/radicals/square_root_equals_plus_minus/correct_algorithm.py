"""
Correct algorithm for square root evaluation.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class SquareRootCorrectAlgorithm(CorrectAlgorithm):
    """Correctly evaluates square roots (principal root only)."""

    def get_name(self) -> str:
        return "Correct Square Root Evaluation"

    def get_description(self) -> str:
        return "Correctly evaluates √n as the principal (non-negative) root only."

    def _generate_concise_steps(self, problem: Problem, problem_type: str, **kwargs) -> List[str]:
        """Generate concise steps showing only formula and values."""
        steps = []
        steps.append(f"Question: {problem.text}")

        if problem_type == 'equation_vs_expression':
            radicand = kwargs['radicand']
            base = kwargs['base']
            steps.append(f"√{radicand} = {base}")
            steps.append(f"Answer: {base}")

        elif problem_type == 'negative_radicand_squared':
            base = kwargs['base']
            radicand = kwargs['radicand']
            steps.append(f"(-{base})² = {radicand}")
            steps.append(f"√{radicand} = {base}")
            steps.append(f"Answer: {base}")

        elif problem_type == 'expression_simplification':
            x_val = kwargs['x_val']
            k = kwargs['k']
            expression_value = kwargs['expression_value']
            correct_answer = kwargs['correct_answer']
            steps.append(f"√({x_val}² + {2*k}×{x_val} + {k*k}) = √{expression_value}")
            steps.append(f"√{expression_value} = {correct_answer}")
            steps.append(f"Answer: {correct_answer}")

        elif problem_type == 'word_problem_context':
            area = kwargs['area']
            base = kwargs['base']
            correct_answer = kwargs['correct_answer']
            steps.append(f"side² = {area}")
            steps.append(f"side = √{area} = {base}")
            steps.append(f"Answer: {correct_answer}")

        elif problem_type == 'non_area_context':
            radicand = kwargs['radicand']
            base = kwargs['base']
            correct_answer = kwargs['correct_answer']
            steps.append(f"√{radicand} = {base}")
            steps.append(f"Answer: {correct_answer}")

        elif problem_type == 'equation_vs_expression_word':
            radicand = kwargs['radicand']
            base = kwargs['base']
            correct_answer = kwargs['correct_answer']
            steps.append(f"√{radicand} = {base}")
            steps.append(f"Answer: {correct_answer}")

        else:  # basic_square_root
            radicand = kwargs['radicand']
            base = kwargs['base']
            steps.append(f"√{radicand} = {base}")
            steps.append(f"Answer: {base}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, problem_type: str, **kwargs) -> List[str]:
        """Generate verbose steps with full explanations (original format)."""
        steps = []

        if problem_type == 'equation_vs_expression':
            radicand = kwargs['radicand']
            base = kwargs['base']
            equation_solution = kwargs['equation_solution']

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("CRITICAL DISTINCTION:")
            steps.append(f"  Evaluating √{radicand} ≠ Solving x² = {radicand}")
            steps.append("")
            steps.append(f"EVALUATING √{radicand}:")
            steps.append("  √ symbol means PRINCIPAL (positive) root only")
            steps.append(f"  √{radicand} = {base} (ONE answer: positive only)")
            steps.append("")
            steps.append(f"SOLVING x² = {radicand}:")
            steps.append(f"  This asks: what values of x make x² = {radicand}?")
            steps.append(f"  Both {base}² and (-{base})² equal {radicand}")
            steps.append(f"  So x = {equation_solution} (TWO answers)")
            steps.append("")
            steps.append(f"Final Answer: √{radicand} = {base} ✓")
            steps.append("")
            steps.append(f"WRONG: √{radicand} ≠ ±{base}")
            steps.append("  That confuses evaluating √ with solving an equation!")

        elif problem_type == 'negative_radicand_squared':
            base = kwargs['base']
            radicand = kwargs['radicand']

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append(f"Step 1: Evaluate inside the square root first")
            steps.append(f"  (-{base})² = (-{base}) × (-{base}) = {radicand}")
            steps.append("")
            steps.append(f"Step 2: Now evaluate √{radicand}")
            steps.append(f"  √{radicand} = {base} (principal root is positive)")
            steps.append("")
            steps.append("Key insight: √(negative²) is ALWAYS positive!")
            steps.append(f"  The squaring makes it positive: {radicand}")
            steps.append(f"  Then √ gives only the positive root: {base}")
            steps.append("")
            steps.append(f"Final Answer: {base} ✓")
            steps.append("")
            steps.append(f"WRONG: √((-{base})²) ≠ -{base}")
            steps.append("  The answer is always positive!")

        elif problem_type == 'expression_simplification':
            x_val = kwargs['x_val']
            k = kwargs['k']
            expression_value = kwargs['expression_value']
            correct_answer = kwargs['correct_answer']

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append(f"Step 1: Substitute x = {x_val}")
            steps.append(f"  √({x_val}² + {2*k}×{x_val} + {k*k})")
            steps.append(f"  = √({x_val**2} + {2*k*x_val} + {k*k})")
            steps.append(f"  = √{expression_value}")
            steps.append("")
            steps.append(f"Step 2: Recognize this is a perfect square")
            steps.append(f"  {expression_value} = ({x_val} + {k})²")
            steps.append(f"  So √{expression_value} = √(({x_val} + {k})²)")
            steps.append("")
            steps.append(f"Step 3: √(a²) = |a| (absolute value)")
            steps.append(f"  Since {x_val} + {k} = {x_val + k} > 0")
            steps.append(f"  √(({x_val + k})²) = {x_val + k}")
            steps.append("")
            steps.append(f"Final Answer: {correct_answer} ✓")
            steps.append("")
            steps.append(f"WRONG: Answer is NOT ±{x_val + k}")
            steps.append("  √ always gives the positive root!")

        elif problem_type == 'word_problem_context':
            area = kwargs['area']
            base = kwargs['base']
            context = kwargs['context']
            correct_answer = kwargs['correct_answer']

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append(f"Step 1: Set up the equation")
            steps.append(f"  For a square: side² = area")
            steps.append(f"  side² = {area}")
            steps.append("")
            steps.append(f"Step 2: Solve for side length")
            steps.append(f"  side = √{area}")
            steps.append(f"  side = {base}")
            steps.append("")
            steps.append("Step 3: Check if negative makes sense")
            steps.append(f"  Can a {context} have a negative side length? NO!")
            steps.append("  Length must be positive in real-world contexts")
            steps.append("")
            steps.append(f"Final Answer: {correct_answer} ✓")
            steps.append("")
            steps.append(f"WRONG: Answer is NOT ±{base}")
            steps.append("  Negative lengths don't make physical sense!")

        elif problem_type == 'non_area_context':
            radicand = kwargs['radicand']
            base = kwargs['base']
            context_type = kwargs['context_type']
            correct_answer = kwargs['correct_answer']

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append(f"Step 1: Evaluate √{radicand}")
            steps.append(f"  √{radicand} = {base}")
            steps.append("")
            steps.append("Step 2: Check context - does negative make sense?")
            steps.append(f"  In {context_type} context, only positive values are meaningful")
            steps.append("")
            steps.append(f"Final Answer: {correct_answer} ✓")
            steps.append("")
            steps.append(f"WRONG: Answer is NOT ±{base}")
            steps.append("  √ gives principal root only, and context requires positive!")

        elif problem_type == 'equation_vs_expression_word':
            radicand = kwargs['radicand']
            base = kwargs['base']
            correct_answer = kwargs['correct_answer']

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append(f"Step 1: Evaluate the expression √{radicand}")
            steps.append(f"  √{radicand} = {base}")
            steps.append("")
            steps.append("Step 2: Distinction - expression vs equation")
            steps.append(f"  We're evaluating √{radicand}, not solving x² = {radicand}")
            steps.append(f"  √ symbol means principal root only = {base}")
            steps.append("")
            steps.append(f"Final Answer: {correct_answer} ✓")
            steps.append("")
            steps.append(f"WRONG: Answer is NOT ±{base}")
            steps.append("  That would be the solution to an equation, not evaluating √!")

        else:  # basic_square_root
            radicand = kwargs['radicand']
            base = kwargs['base']

            steps.append(f"Problem: √{radicand}")
            steps.append("")
            steps.append("Definition: √ symbol means PRINCIPAL (positive) root only")
            steps.append("")
            steps.append(f"Step 1: Find positive number that squares to {radicand}")
            steps.append(f"  {base} × {base} = {radicand} ✓")
            steps.append("")
            steps.append(f"Step 2: √ gives ONLY the positive root")
            steps.append(f"  √{radicand} = {base} (positive root)")
            steps.append("")
            steps.append("Note: Don't confuse with solving equations!")
            steps.append(f"  √{radicand} = {base} (one answer)")
            steps.append(f"  vs solving x² = {radicand} gives x = ±{base} (two answers)")
            steps.append("")
            steps.append(f"Final Answer: {base} ✓")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        problem_type = problem.metadata.get('problem_type', 'basic_square_root')

        # Handle enhanced problem types
        if problem_type == 'equation_vs_expression':
            return self._handle_equation_vs_expression(problem, verbose)
        elif problem_type == 'negative_radicand_squared':
            return self._handle_negative_radicand_squared(problem, verbose)
        elif problem_type == 'expression_simplification':
            return self._handle_expression_simplification(problem, verbose)
        elif problem_type == 'word_problem_context':
            return self._handle_word_problem_context(problem, verbose)
        elif problem_type == 'non_area_context':
            return self._handle_non_area_context(problem, verbose)
        elif problem_type == 'equation_vs_expression_word':
            return self._handle_equation_vs_expression_word(problem, verbose)

        # Original basic problem type
        radicand = problem.metadata['radicand']

        # COMPUTE the answer algorithmically (don't use metadata['correct_answer'])
        base = int(radicand ** 0.5)
        correct_answer = base

        step_kwargs = {
            'radicand': radicand,
            'base': base
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, problem_type, **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, problem_type, **step_kwargs)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _handle_equation_vs_expression(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle contrasting √n vs solving x² = n."""
        radicand = problem.metadata['radicand']

        # COMPUTE the answer algorithmically
        base = int(radicand ** 0.5)
        correct_answer = base
        equation_solution = f"±{base}"

        step_kwargs = {
            'radicand': radicand,
            'base': base,
            'equation_solution': equation_solution
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, 'equation_vs_expression', **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, 'equation_vs_expression', **step_kwargs)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _handle_negative_radicand_squared(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle √((-n)²) scenarios."""
        base = problem.metadata['base']

        # COMPUTE the answer algorithmically
        radicand = base * base  # (-base)² = base²
        correct_answer = base  # Always positive

        step_kwargs = {
            'base': base,
            'radicand': radicand
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, 'negative_radicand_squared', **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, 'negative_radicand_squared', **step_kwargs)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _handle_expression_simplification(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle √(x²+2kx+k²) type expressions."""
        x_val = problem.metadata['x_value']
        k = problem.metadata['k']

        # COMPUTE the answer algorithmically
        expression_value = (x_val + k) ** 2
        correct_answer = x_val + k  # Always positive since x_val and k are positive

        step_kwargs = {
            'x_val': x_val,
            'k': k,
            'expression_value': expression_value,
            'correct_answer': correct_answer
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, 'expression_simplification', **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, 'expression_simplification', **step_kwargs)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _handle_word_problem_context(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle word problems where negative doesn't make sense."""
        area = problem.metadata['area']
        context = problem.metadata.get('context', 'square')

        # COMPUTE the answer algorithmically
        base = int(area ** 0.5)
        correct_answer = f"{base} meters"

        step_kwargs = {
            'area': area,
            'base': base,
            'context': context,
            'correct_answer': correct_answer
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, 'word_problem_context', **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, 'word_problem_context', **step_kwargs)

        return Solution(
            answer=base,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _handle_non_area_context(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle word problems with non-area contexts where positive-only matters."""
        radicand = problem.metadata['radicand']
        context_type = problem.metadata.get('context_type', 'generic')

        # COMPUTE the answer algorithmically
        base = int(radicand ** 0.5)

        # Extract the unit from the metadata's correct answer
        correct_answer_meta = problem.metadata.get('correct_answer', f"{base}")
        if isinstance(correct_answer_meta, str) and ' ' in correct_answer_meta:
            unit = correct_answer_meta.split(' ', 1)[1]
            correct_answer = f"{base} {unit}"
        else:
            correct_answer = str(base)

        step_kwargs = {
            'radicand': radicand,
            'base': base,
            'context_type': context_type,
            'correct_answer': correct_answer
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, 'non_area_context', **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, 'non_area_context', **step_kwargs)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _handle_equation_vs_expression_word(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle word problems showing equation vs expression distinction."""
        radicand = problem.metadata['radicand']

        # COMPUTE the answer algorithmically
        base = int(radicand ** 0.5)
        correct_answer = str(base)

        step_kwargs = {
            'radicand': radicand,
            'base': base,
            'correct_answer': correct_answer
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, 'equation_vs_expression_word', **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, 'equation_vs_expression_word', **step_kwargs)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
