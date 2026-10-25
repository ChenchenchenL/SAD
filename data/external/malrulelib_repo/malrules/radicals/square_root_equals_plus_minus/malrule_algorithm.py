"""
Malrule algorithm for Square-Root-Equals-Plus-Minus error.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class SquareRootEqualsPlusMinusMalrule(Malrule):
    """
    Students believe √n = ±result instead of just the positive root.

    Example: √16 = ±4 instead of √16 = 4
    """

    def get_name(self) -> str:
        return "Square-Root-Equals-Plus-Minus"

    def get_description(self) -> str:
        return (
            "Students incorrectly believe that the radical symbol √n yields both "
            "positive and negative values (±√n), confusing the principal square root "
            "with the solutions to equations of the form x² = n. This is one of the "
            "most common and persistent misconceptions in algebra, documented across "
            "multiple levels and educational contexts."
        )

    def _generate_concise_steps(self, problem: Problem, problem_type: str, **kwargs) -> List[str]:
        """Generate concise steps showing only formula and values."""
        steps = []
        steps.append(f"Question: {problem.text}")

        if problem_type == 'equation_vs_expression':
            radicand = kwargs['radicand']
            base = kwargs['base']
            steps.append(f"√{radicand} = ±{base}")
            steps.append(f"Answer: ±{base}")

        elif problem_type == 'negative_radicand_squared':
            base = kwargs['base']
            radicand = kwargs['radicand']
            steps.append(f"(-{base})² = {radicand}")
            steps.append(f"√{radicand} = ±{base}")
            steps.append(f"Answer: ±{base}")

        elif problem_type == 'expression_simplification':
            x_val = kwargs['x_val']
            k = kwargs['k']
            expression_value = kwargs['expression_value']
            steps.append(f"√({x_val}² + {2*k}×{x_val} + {k*k}) = √{expression_value}")
            steps.append(f"√{expression_value} = ±{x_val + k}")
            steps.append(f"Answer: ±{x_val + k}")

        elif problem_type == 'word_problem_context':
            area = kwargs['area']
            base = kwargs['base']
            steps.append(f"side² = {area}")
            steps.append(f"side = √{area} = ±{base}")
            steps.append(f"Answer: ±{base} meters")

        elif problem_type == 'non_area_context':
            radicand = kwargs['radicand']
            base = kwargs['base']
            malrule_answer = kwargs['malrule_answer']
            steps.append(f"√{radicand} = ±{base}")
            steps.append(f"Answer: {malrule_answer}")

        elif problem_type == 'equation_vs_expression_word':
            radicand = kwargs['radicand']
            base = kwargs['base']
            malrule_answer = kwargs['malrule_answer']
            steps.append(f"√{radicand} = ±{base}")
            steps.append(f"Answer: {malrule_answer}")

        else:  # basic_square_root
            radicand = kwargs['radicand']
            base = kwargs['base']
            steps.append(f"√{radicand} = ±{base}")
            steps.append(f"Answer: ±{base}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, problem_type: str, **kwargs) -> List[str]:
        """Generate verbose steps with full explanations (original format)."""
        steps = []

        if problem_type == 'equation_vs_expression':
            radicand = kwargs['radicand']
            base = kwargs['base']

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("MALRULE: √n gives ±answer (confusing with equation solving)")
            steps.append(f"  MALRULE REASONING: 'Solving x² = {radicand} gives x = ±{base}'")
            steps.append(f"                     'So √{radicand} should also equal ±{base}'")
            steps.append("")
            steps.append(f"Step 1: Treat √{radicand} like solving x² = {radicand}")
            steps.append(f"  Both {base}² and (-{base})² equal {radicand}")
            steps.append("")
            steps.append(f"Step 2: Include both roots (INCORRECT!)")
            steps.append(f"  Answer: ±{base}")
            steps.append("")
            steps.append(f"Final Answer: ±{base} (INCORRECT!)")
            steps.append(f"  Should be {base} only - √ means principal root!")

        elif problem_type == 'negative_radicand_squared':
            base = kwargs['base']

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("MALRULE: Negative inside means negative answer")
            steps.append(f"  MALRULE REASONING: 'There's a negative: -{base}'")
            steps.append(f"                     'So answer includes ±{base}'")
            steps.append("")
            steps.append(f"Step 1: See the negative inside")
            steps.append(f"  (-{base})² has a negative")
            steps.append("")
            steps.append(f"Step 2: MALRULE says include negative in answer")
            steps.append(f"  Answer: ±{base}")
            steps.append("")
            steps.append(f"Final Answer: ±{base} (INCORRECT!)")
            steps.append(f"  Should be {base} only - squaring makes it positive!")

        elif problem_type == 'expression_simplification':
            x_val = kwargs['x_val']
            k = kwargs['k']

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("MALRULE: Square root gives ±answer")
            steps.append(f"  MALRULE REASONING: 'When taking a square root'")
            steps.append(f"                     'Must include both + and - solutions'")
            steps.append("")
            steps.append(f"Step 1: Substitute x = {x_val}")
            steps.append(f"  √({x_val}² + {2*k}×{x_val} + {k*k})")
            steps.append(f"  = √{(x_val + k)**2}")
            steps.append("")
            steps.append(f"Step 2: MALRULE - Include both roots")
            steps.append(f"  Answer: ±{x_val + k}")
            steps.append("")
            steps.append(f"Final Answer: ±{x_val + k} (INCORRECT!)")
            steps.append(f"  Should be {x_val + k} only!")

        elif problem_type == 'word_problem_context':
            area = kwargs['area']
            base = kwargs['base']

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("MALRULE: Square root gives ±answer")
            steps.append(f"  MALRULE REASONING: 'Taking square root gives two answers'")
            steps.append(f"                     'Must include ±'")
            steps.append("")
            steps.append(f"Step 1: Set up equation")
            steps.append(f"  side² = {area}")
            steps.append("")
            steps.append(f"Step 2: Take square root of both sides")
            steps.append(f"  side = √{area} = ±{base}")
            steps.append("")
            steps.append(f"Final Answer: ±{base} meters (INCORRECT!)")
            steps.append(f"  Should be {base} meters only - negative length doesn't make sense!")

        elif problem_type == 'non_area_context':
            radicand = kwargs['radicand']
            base = kwargs['base']
            malrule_answer = kwargs['malrule_answer']

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("MALRULE: Square root gives ±answer")
            steps.append(f"  MALRULE REASONING: 'Taking square root always gives two answers'")
            steps.append(f"                     'Must include ±{base}'")
            steps.append("")
            steps.append(f"Step 1: Evaluate √{radicand}")
            steps.append(f"  √{radicand} = ±{base}")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT!)")
            steps.append(f"  Should be {base} only - context requires positive!")

        elif problem_type == 'equation_vs_expression_word':
            radicand = kwargs['radicand']
            base = kwargs['base']
            malrule_answer = kwargs['malrule_answer']

            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("MALRULE: Square root gives ±answer")
            steps.append(f"  MALRULE REASONING: 'Taking square root gives two solutions'")
            steps.append(f"                     'Must include ±{base}'")
            steps.append("")
            steps.append(f"Step 1: Evaluate √{radicand}")
            steps.append(f"  √{radicand} = ±{base}")
            steps.append("")
            steps.append(f"Final Answer: {malrule_answer} (INCORRECT!)")
            steps.append(f"  Should be {base} only - √ gives principal root!")

        else:  # basic_square_root
            radicand = kwargs['radicand']
            base = kwargs['base']

            steps.append(f"Problem: √{radicand}")
            steps.append("")
            steps.append("MALRULE: Square root gives both positive and negative")
            steps.append(f"  MALRULE REASONING: 'Both {base}² and (-{base})² equal {radicand}'")
            steps.append(f"                     'So √{radicand} must equal ±{base}'")
            steps.append("")
            steps.append(f"Step 1: Find what number squared equals {radicand}")
            steps.append(f"  {base} × {base} = {radicand} ✓")
            steps.append(f"  (-{base}) × (-{base}) = {radicand} ✓")
            steps.append("")
            steps.append(f"Step 2: MALRULE says both answers are valid")
            steps.append(f"  Answer: ±{base}")
            steps.append("")
            steps.append(f"Final Answer: ±{base} (INCORRECT - √ gives positive root only!)")

        return steps

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Malrule: square root gives ±answer (both positive and negative)
        # We compute the NEGATIVE root to represent the misconception
        radicand = problem.metadata.get('radicand')
        if radicand is not None:
            base = int(radicand ** 0.5)
            return -base
        # Handle word problems that might have string answers
        correct_ans = problem.metadata.get('correct_answer')
        if isinstance(correct_ans, str) and ' ' in correct_ans:
            # Extract numeric part and negate it
            parts = correct_ans.split(' ', 1)
            try:
                value = int(parts[0])
                return f"±{value} {parts[1]}"
            except:
                pass
        # Fallback - try to get base
        base = problem.metadata.get('base')
        if base is not None:
            return -base
        # Last resort
        return problem.metadata.get('malrule_answer', 0)

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
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

        # COMPUTE the answer algorithmically (malrule: includes negative)
        base = int(radicand ** 0.5)
        malrule_answer = -base  # Return negative to represent ±base misconception

        step_kwargs = {
            'radicand': radicand,
            'base': base
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, problem_type, **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, problem_type, **step_kwargs)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _handle_equation_vs_expression(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle equation vs expression with malrule."""
        radicand = problem.metadata['radicand']

        # COMPUTE the answer algorithmically (malrule: includes negative)
        base = int(radicand ** 0.5)
        malrule_answer = -base  # Return negative to represent ±base misconception

        step_kwargs = {
            'radicand': radicand,
            'base': base
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, 'equation_vs_expression', **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, 'equation_vs_expression', **step_kwargs)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _handle_negative_radicand_squared(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle negative radicand squared with malrule."""
        base = problem.metadata['base']

        # COMPUTE the answer algorithmically (malrule: includes negative)
        radicand = base * base
        malrule_answer = -base  # Return negative to represent ±base misconception

        step_kwargs = {
            'base': base,
            'radicand': radicand
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, 'negative_radicand_squared', **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, 'negative_radicand_squared', **step_kwargs)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _handle_expression_simplification(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle expression simplification with malrule."""
        x_val = problem.metadata['x_value']
        k = problem.metadata['k']

        # COMPUTE the answer algorithmically (malrule: includes negative)
        expression_value = (x_val + k) ** 2
        malrule_answer = -(x_val + k)  # Return negative to represent ±(x+k) misconception

        step_kwargs = {
            'x_val': x_val,
            'k': k,
            'expression_value': expression_value
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, 'expression_simplification', **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, 'expression_simplification', **step_kwargs)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _handle_word_problem_context(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle word problem context with malrule."""
        area = problem.metadata['area']

        # COMPUTE the answer algorithmically (malrule: includes negative)
        base = int(area ** 0.5)
        malrule_answer = -base  # Return negative to represent ±base misconception

        step_kwargs = {
            'area': area,
            'base': base
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, 'word_problem_context', **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, 'word_problem_context', **step_kwargs)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _handle_non_area_context(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle word problems with non-area contexts where positive-only matters."""
        radicand = problem.metadata['radicand']
        context_type = problem.metadata.get('context_type', 'generic')

        # COMPUTE the answer algorithmically (malrule: includes ±)
        base = int(radicand ** 0.5)

        # Extract the unit from the metadata's correct answer
        correct_answer_meta = problem.metadata.get('correct_answer', f"{base}")
        if isinstance(correct_answer_meta, str) and ' ' in correct_answer_meta:
            unit = correct_answer_meta.split(' ', 1)[1]
            malrule_answer = f"±{base} {unit}"
        else:
            malrule_answer = f"±{base}"

        step_kwargs = {
            'radicand': radicand,
            'base': base,
            'malrule_answer': malrule_answer
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, 'non_area_context', **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, 'non_area_context', **step_kwargs)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _handle_equation_vs_expression_word(self, problem: Problem, verbose: bool = False) -> Solution:
        """Handle word problems showing equation vs expression distinction."""
        radicand = problem.metadata['radicand']

        # COMPUTE the answer algorithmically (malrule: includes ±)
        base = int(radicand ** 0.5)
        malrule_answer = f"±{base}"

        step_kwargs = {
            'radicand': radicand,
            'base': base,
            'malrule_answer': malrule_answer
        }

        if verbose:
            steps = self._generate_verbose_steps(problem, 'equation_vs_expression_word', **step_kwargs)
        else:
            steps = self._generate_concise_steps(problem, 'equation_vs_expression_word', **step_kwargs)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
