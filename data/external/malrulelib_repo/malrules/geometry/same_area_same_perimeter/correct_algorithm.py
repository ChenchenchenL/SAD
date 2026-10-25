"""
Correct algorithm for perimeter calculation.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class PerimeterCalculationCorrectAlgorithm(CorrectAlgorithm):
    """Correctly calculates perimeter regardless of area."""

    def get_name(self) -> str:
        return "Correct Perimeter Calculation"

    def get_description(self) -> str:
        return "Correctly calculates perimeter using dimensions, independent of area."

    def _generate_concise_steps(self, problem: Problem, correct_answer) -> List[str]:
        """Generate concise steps with only formula and values."""
        problem_type = problem.metadata.get('problem_type', 'rectangle_comparison')
        is_word_problem = problem.metadata.get('is_word_problem', False)

        steps = []
        steps.append(f"Question: {problem.text}")

        if problem_type == 'triangle_comparison':
            base2 = problem.metadata['base2']
            height2 = problem.metadata['height2']
            perimeter2 = problem.metadata['perimeter2']
            steps.append(f"Triangle B: base = {base2}, height = {height2}")
            steps.append(f"Perimeter B = {perimeter2}")
            steps.append(f"Answer: {correct_answer}")
        elif problem_type == 'fencing_optimization':
            l2 = problem.metadata['length2']
            w2 = problem.metadata['width2']
            steps.append(f"Design B: {l2}m × {w2}m")
            steps.append(f"Perimeter = 2({l2} + {w2}) = {correct_answer}")
            steps.append(f"Answer: {correct_answer} meters")
        elif problem_type == 'composite_shapes':
            perimeter2 = problem.metadata['perimeter2']
            steps.append(f"Figure B perimeter = {perimeter2}")
            steps.append(f"Answer: {correct_answer}")
        elif problem_type == 'square_vs_rectangle':
            l2 = problem.metadata['length']
            w2 = problem.metadata['width']
            steps.append(f"Rectangle: {l2} × {w2}")
            steps.append(f"Perimeter = 2({l2} + {w2}) = {correct_answer}")
            steps.append(f"Answer: {correct_answer}")
        elif problem_type == 'word_problem_context':
            l2 = problem.metadata['length2']
            w2 = problem.metadata['width2']
            steps.append(f"Rectangle B: {l2} × {w2}")
            steps.append(f"Perimeter = 2({l2} + {w2}) = {correct_answer}")
            steps.append(f"Answer: {correct_answer}")
        else:  # rectangle_comparison
            l2 = problem.metadata['length2']
            w2 = problem.metadata['width2']
            steps.append(f"Rectangle B: {l2} × {w2}")
            steps.append(f"Perimeter = 2(l + w)")
            steps.append(f"Perimeter = 2({l2} + {w2}) = {correct_answer}")
            steps.append(f"Answer: {correct_answer}")

        return steps

    def _generate_verbose_steps(self, problem: Problem, correct_answer) -> List[str]:
        """Generate verbose steps with full explanations (original format)."""
        problem_type = problem.metadata.get('problem_type', 'rectangle_comparison')
        is_word_problem = problem.metadata.get('is_word_problem', False)

        # Delegate to the appropriate handler method for verbose steps
        if problem_type == 'triangle_comparison':
            return self._verbose_triangle_comparison(problem, correct_answer)
        elif problem_type == 'fencing_optimization':
            return self._verbose_fencing_optimization(problem, correct_answer)
        elif problem_type == 'composite_shapes':
            return self._verbose_composite_shapes(problem, correct_answer)
        elif problem_type == 'square_vs_rectangle':
            return self._verbose_square_vs_rectangle(problem, correct_answer)
        elif problem_type == 'word_problem_context':
            return self._verbose_word_problem_context(problem, correct_answer)
        else:
            return self._verbose_rectangle_comparison(problem, correct_answer)

    def _verbose_rectangle_comparison(self, problem: Problem, correct_answer) -> List[str]:
        """Generate verbose steps for rectangle comparison."""
        l1 = problem.metadata['length1']
        w1 = problem.metadata['width1']
        l2 = problem.metadata['length2']
        w2 = problem.metadata['width2']
        area1 = l1 * w1
        area2 = l2 * w2
        perimeter1 = 2 * (l1 + w1)
        perimeter2 = 2 * (l2 + w2)

        steps = []
        steps.append(f"Problem: Rectangle A: {l1}×{w1}, Rectangle B: {l2}×{w2}")
        steps.append(f"Both have same area. Find perimeter of Rectangle B.")
        steps.append("")
        steps.append("CORRECT METHOD: Calculate perimeter from dimensions")
        steps.append("  Area and perimeter are DIFFERENT measurements!")
        steps.append("")
        steps.append(f"Step 1: Verify both have same area")
        steps.append(f"  Area A = {l1} × {w1} = {area1}")
        steps.append(f"  Area B = {l2} × {w2} = {area2}")
        steps.append(f"  Same area: {area1}")
        steps.append("")
        steps.append(f"Step 2: Calculate perimeter of Rectangle A (for comparison)")
        steps.append(f"  Perimeter A = 2({l1} + {w1}) = {perimeter1}")
        steps.append("")
        steps.append(f"Step 3: Calculate perimeter of Rectangle B")
        steps.append(f"  Perimeter B = 2({l2} + {w2}) = {perimeter2}")
        steps.append("")
        steps.append(f"Final Answer: Perimeter of Rectangle B = {correct_answer}")
        steps.append("")
        steps.append(f"Important: Same area ({area1}) but DIFFERENT perimeters ({perimeter1} vs {perimeter2})!")
        steps.append(f"  Area measures space INSIDE (surface)")
        steps.append(f"  Perimeter measures distance AROUND (boundary)")
        return steps

    def _verbose_triangle_comparison(self, problem: Problem, correct_answer) -> List[str]:
        """Generate verbose steps for triangle comparison."""
        base1 = problem.metadata['base1']
        height1 = problem.metadata['height1']
        base2 = problem.metadata['base2']
        height2 = problem.metadata['height2']
        area = round(0.5 * base1 * height1, 1)
        perimeter1 = problem.metadata['perimeter1']
        perimeter2 = problem.metadata['perimeter2']

        steps = []
        steps.append(f"Problem: Triangle A (base {base1}, height {height1})")
        steps.append(f"         Triangle B (base {base2}, height {height2})")
        steps.append(f"Both have same area. Find perimeter of Triangle B.")
        steps.append("")
        steps.append("CORRECT METHOD: Calculate perimeter from dimensions")
        steps.append("  Same area does NOT mean same perimeter!")
        steps.append("")
        steps.append(f"Step 1: Verify both have same area")
        steps.append(f"  Area = 1/2 × base × height")
        steps.append(f"  Area A = 1/2 × {base1} × {height1} = {area}")
        steps.append(f"  Area B = 1/2 × {base2} × {height2} = {area}")
        steps.append(f"  Same area: {area}")
        steps.append("")
        steps.append(f"Step 2: Calculate perimeter of Triangle B")
        steps.append(f"  Perimeter B = {perimeter2} (using Pythagorean theorem for right triangle)")
        steps.append("")
        steps.append(f"Final Answer: Perimeter of Triangle B = {correct_answer}")
        steps.append("")
        steps.append(f"Important: Same area but DIFFERENT perimeters ({perimeter1} vs {perimeter2})!")
        return steps

    def _verbose_fencing_optimization(self, problem: Problem, correct_answer) -> List[str]:
        """Generate verbose steps for fencing optimization."""
        l1 = problem.metadata['length1']
        w1 = problem.metadata['width1']
        l2 = problem.metadata['length2']
        w2 = problem.metadata['width2']
        area = l1 * w1
        perimeter1 = 2 * (l1 + w1)
        perimeter2 = 2 * (l2 + w2)

        steps = []
        steps.append(f"Problem: Two garden designs with area {area} m²")
        steps.append(f"Design A: {l1}m × {w1}m, Design B: {l2}m × {w2}m")
        steps.append(f"How much fencing for Design B?")
        steps.append("")
        steps.append("CORRECT METHOD: Calculate perimeter for Design B")
        steps.append("  Same area does not mean same fencing needed!")
        steps.append("")
        steps.append(f"Step 1: Verify both have same area")
        steps.append(f"  Area A = {l1} × {w1} = {area} m²")
        steps.append(f"  Area B = {l2} × {w2} = {area} m²")
        steps.append(f"  Same area: {area} m²")
        steps.append("")
        steps.append(f"Step 2: Calculate fencing needed for Design B")
        steps.append(f"  Fencing = Perimeter = 2({l2} + {w2})")
        steps.append(f"  = 2({l2 + w2}) = {perimeter2} meters")
        steps.append("")
        steps.append(f"Final Answer: {correct_answer} meters of fencing")
        steps.append("")
        steps.append(f"Note: Design A needs {perimeter1}m, Design B needs {perimeter2}m")
        steps.append(f"      Same area but different fencing requirements!")
        return steps

    def _verbose_composite_shapes(self, problem: Problem, correct_answer) -> List[str]:
        """Generate verbose steps for composite shapes."""
        area = problem.metadata['area']
        perimeter1 = problem.metadata['perimeter1']
        perimeter2 = problem.metadata['perimeter2']

        steps = []
        steps.append(f"Problem: Two L-shaped figures, both with area {area} square units")
        steps.append(f"Figure A has perimeter {perimeter1} units")
        steps.append(f"Find perimeter of Figure B")
        steps.append("")
        steps.append("CORRECT METHOD: Perimeter depends on shape configuration")
        steps.append("  Same area does NOT mean same perimeter!")
        steps.append("  Different L-shape configurations = different perimeters")
        steps.append("")
        steps.append(f"Step 1: Note that both have area {area}")
        steps.append(f"  Figure A: area {area}, perimeter {perimeter1}")
        steps.append(f"  Figure B: area {area}, perimeter {perimeter2}")
        steps.append("")
        steps.append(f"Step 2: Calculate perimeter of Figure B")
        steps.append(f"  Count all outer edges of L-shape B")
        steps.append(f"  Perimeter B = {perimeter2} units")
        steps.append("")
        steps.append(f"Final Answer: Perimeter of Figure B = {correct_answer} units")
        steps.append("")
        steps.append(f"Important: Same area but different perimeters ({perimeter1} vs {perimeter2})!")
        return steps

    def _verbose_square_vs_rectangle(self, problem: Problem, correct_answer) -> List[str]:
        """Generate verbose steps for square vs rectangle."""
        side = problem.metadata['side']
        l2 = problem.metadata['length']
        w2 = problem.metadata['width']
        area = side * side
        perimeter1 = 4 * side
        perimeter2 = 2 * (l2 + w2)

        steps = []
        steps.append(f"Problem: Square (side {side}) and Rectangle ({l2}×{w2})")
        steps.append(f"Both have same area. Find perimeter of rectangle.")
        steps.append("")
        steps.append("CORRECT METHOD: Calculate perimeter from dimensions")
        steps.append("  Square and rectangle with same area have DIFFERENT perimeters!")
        steps.append("")
        steps.append(f"Step 1: Verify both have same area")
        steps.append(f"  Square area = {side} × {side} = {area}")
        steps.append(f"  Rectangle area = {l2} × {w2} = {area}")
        steps.append(f"  Same area: {area}")
        steps.append("")
        steps.append(f"Step 2: Calculate perimeter of square (for comparison)")
        steps.append(f"  Square perimeter = 4 × {side} = {perimeter1}")
        steps.append("")
        steps.append(f"Step 3: Calculate perimeter of rectangle")
        steps.append(f"  Rectangle perimeter = 2({l2} + {w2}) = {perimeter2}")
        steps.append("")
        steps.append(f"Final Answer: Rectangle perimeter = {correct_answer}")
        steps.append("")
        steps.append(f"Important: Same area ({area}) but DIFFERENT perimeters!")
        steps.append(f"  Square ({perimeter1}) vs Rectangle ({perimeter2})")
        steps.append(f"  More elongated shapes have longer perimeters for same area")
        return steps

    def _verbose_word_problem_context(self, problem: Problem, correct_answer) -> List[str]:
        """Generate verbose steps for word problem context."""
        l1 = problem.metadata['length1']
        w1 = problem.metadata['width1']
        l2 = problem.metadata['length2']
        w2 = problem.metadata['width2']
        area1 = l1 * w1
        area2 = l2 * w2
        perimeter1 = 2 * (l1 + w1)
        perimeter2 = 2 * (l2 + w2)

        steps = []
        steps.append(f"Word Problem: {problem.text}")
        steps.append("")
        steps.append("Step 1: Extract information from the word problem")
        steps.append(f"  Both rectangles have area {area1} square units")
        steps.append(f"  Rectangle A: {l1} × {w1}")
        steps.append(f"  Rectangle B: {l2} × {w2}")
        steps.append(f"  Question: Find perimeter of Rectangle B")
        steps.append("")
        steps.append("Step 2: Calculate perimeter using dimensions")
        steps.append("CORRECT METHOD: Calculate perimeter from dimensions")
        steps.append("  Area and perimeter are DIFFERENT measurements!")
        steps.append("")
        steps.append(f"Step 3: Verify both have same area")
        steps.append(f"  Area A = {l1} × {w1} = {area1}")
        steps.append(f"  Area B = {l2} × {w2} = {area2}")
        steps.append(f"  Same area: {area1}")
        steps.append("")
        steps.append(f"Step 4: Calculate perimeter of Rectangle B")
        steps.append(f"  Perimeter B = 2({l2} + {w2})")
        steps.append(f"  Perimeter B = 2({l2 + w2})")
        steps.append(f"  Perimeter B = {perimeter2}")
        steps.append("")
        steps.append(f"Final Answer: {correct_answer}")
        steps.append("")
        steps.append(f"Key Point: Same area ({area1}) does not mean Same perimeter")
        steps.append(f"  Rectangle A perimeter: {perimeter1}")
        steps.append(f"  Rectangle B perimeter: {perimeter2}")
        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply correct algorithm across all templates.

        Args:
            problem: The problem to solve
            verbose: If True, generate verbose steps; if False, generate concise steps (default: False)
        """
        problem_type = problem.metadata.get('problem_type', 'rectangle_comparison')

        # Calculate correct answer based on problem type
        if problem_type == 'triangle_comparison':
            correct_answer = problem.metadata['perimeter2']
        elif problem_type == 'fencing_optimization':
            l2 = problem.metadata['length2']
            w2 = problem.metadata['width2']
            correct_answer = 2 * (l2 + w2)
        elif problem_type == 'composite_shapes':
            correct_answer = problem.metadata['perimeter2']
        elif problem_type == 'square_vs_rectangle':
            l2 = problem.metadata['length']
            w2 = problem.metadata['width']
            correct_answer = 2 * (l2 + w2)
        elif problem_type == 'word_problem_context':
            l2 = problem.metadata['length2']
            w2 = problem.metadata['width2']
            correct_answer = 2 * (l2 + w2)
        else:  # rectangle_comparison
            l2 = problem.metadata['length2']
            w2 = problem.metadata['width2']
            correct_answer = 2 * (l2 + w2)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, correct_answer)
        else:
            steps = self._generate_concise_steps(problem, correct_answer)

        return Solution(
            answer=correct_answer,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
