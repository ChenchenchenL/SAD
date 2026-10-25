"""
Malrule algorithm for Same-Area-Same-Perimeter error.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class SameAreaSamePerimeterMalrule(Malrule):
    """
    Students think same area means same perimeter.

    Example: Two rectangles with area 8
    Student: "Same area, so same perimeter"
    Correct: Different dimensions = different perimeters
    """

    def get_name(self) -> str:
        return "Same-Area-Same-Perimeter"

    def _generate_concise_steps(self, problem: Problem, malrule_answer, correct_answer) -> List[str]:
        """Generate concise steps with only formula and values."""
        problem_type = problem.metadata.get('problem_type', 'rectangle_comparison')

        steps = []
        steps.append(f"Question: {problem.text}")

        if problem_type == 'triangle_comparison':
            perimeter1 = problem.metadata['perimeter1']
            steps.append(f"Same area = same perimeter")
            steps.append(f"Perimeter B = Perimeter A = {malrule_answer}")
        elif problem_type == 'fencing_optimization':
            l1 = problem.metadata['length1']
            w1 = problem.metadata['width1']
            perimeter1 = 2 * (l1 + w1)
            steps.append(f"Same area = same fencing")
            steps.append(f"Fencing B = 2({l1} + {w1}) = {malrule_answer}")
        elif problem_type == 'composite_shapes':
            perimeter1 = problem.metadata['perimeter1']
            steps.append(f"Same area = same perimeter")
            steps.append(f"Perimeter B = Perimeter A = {malrule_answer}")
        elif problem_type == 'square_vs_rectangle':
            side = problem.metadata['side']
            steps.append(f"Same area = same perimeter")
            steps.append(f"Rectangle perimeter = Square perimeter = 4 × {side} = {malrule_answer}")
        elif problem_type == 'word_problem_context':
            l1 = problem.metadata['length1']
            w1 = problem.metadata['width1']
            steps.append(f"Same area = same perimeter")
            steps.append(f"Perimeter B = 2({l1} + {w1}) = {malrule_answer}")
        else:  # rectangle_comparison
            l1 = problem.metadata['length1']
            w1 = problem.metadata['width1']
            steps.append(f"MALRULE: Same area = same perimeter")
            steps.append(f"Perimeter B = 2({l1} + {w1}) = {malrule_answer}")

        steps.append(f"Answer: {malrule_answer}")
        return steps

    def _generate_verbose_steps(self, problem: Problem, malrule_answer, correct_answer) -> List[str]:
        """Generate verbose steps with full explanations (original format)."""
        problem_type = problem.metadata.get('problem_type', 'rectangle_comparison')

        if problem_type == 'triangle_comparison':
            return self._verbose_triangle_comparison(problem, malrule_answer, correct_answer)
        elif problem_type == 'fencing_optimization':
            return self._verbose_fencing_optimization(problem, malrule_answer, correct_answer)
        elif problem_type == 'composite_shapes':
            return self._verbose_composite_shapes(problem, malrule_answer, correct_answer)
        elif problem_type == 'square_vs_rectangle':
            return self._verbose_square_vs_rectangle(problem, malrule_answer, correct_answer)
        elif problem_type == 'word_problem_context':
            return self._verbose_word_problem_context(problem, malrule_answer, correct_answer)
        else:
            return self._verbose_rectangle_comparison(problem, malrule_answer, correct_answer)

    def _verbose_rectangle_comparison(self, problem: Problem, malrule_answer, correct_answer) -> List[str]:
        """Generate verbose steps for rectangle comparison."""
        l1 = problem.metadata['length1']
        w1 = problem.metadata['width1']
        l2 = problem.metadata['length2']
        w2 = problem.metadata['width2']
        area = l1 * w1
        perimeter1 = 2 * (l1 + w1)

        steps = []
        steps.append(f"Problem: Rectangle A: {l1}×{w1}, Rectangle B: {l2}×{w2}")
        steps.append(f"Both have same area. Find perimeter of Rectangle B.")
        steps.append("")
        steps.append("MALRULE: Same area means same perimeter")
        steps.append(f"  MALRULE REASONING: 'Same area = same perimeter'")
        steps.append(f"                     'If inside space is same, boundary is same'")
        steps.append("")
        steps.append(f"Step 1: Calculate perimeter of Rectangle A")
        steps.append(f"  Perimeter A = 2({l1} + {w1}) = {perimeter1}")
        steps.append("")
        steps.append(f"Step 2: Apply malrule - same area means same perimeter")
        steps.append(f"  Both rectangles have area {area}")
        steps.append(f"  So Perimeter B = Perimeter A = {malrule_answer}")
        steps.append("")
        steps.append(f"Final Answer: {malrule_answer} (INCORRECT - area does not equal perimeter!)")
        steps.append(f"  Should calculate: 2({l2} + {w2}) = {correct_answer}")
        return steps

    def _verbose_triangle_comparison(self, problem: Problem, malrule_answer, correct_answer) -> List[str]:
        """Generate verbose steps for triangle comparison."""
        base1 = problem.metadata['base1']
        height1 = problem.metadata['height1']
        base2 = problem.metadata['base2']
        height2 = problem.metadata['height2']
        area = round(0.5 * base1 * height1, 1)
        perimeter1 = problem.metadata['perimeter1']

        steps = []
        steps.append(f"Problem: Triangle A (base {base1}, height {height1})")
        steps.append(f"         Triangle B (base {base2}, height {height2})")
        steps.append(f"Both have same area. Find perimeter of Triangle B.")
        steps.append("")
        steps.append("MALRULE: Same area means same perimeter")
        steps.append(f"  MALRULE REASONING: 'Same area = same perimeter'")
        steps.append(f"                     'If inside space is same, boundary is same'")
        steps.append("")
        steps.append(f"Step 1: Calculate area")
        steps.append(f"  Both triangles have area {area}")
        steps.append("")
        steps.append(f"Step 2: Apply malrule - same area means same perimeter")
        steps.append(f"  So Perimeter B = Perimeter A = {malrule_answer}")
        steps.append("")
        steps.append(f"Final Answer: {malrule_answer} (INCORRECT!)")
        steps.append(f"  Should calculate actual perimeter = {correct_answer}")
        return steps

    def _verbose_fencing_optimization(self, problem: Problem, malrule_answer, correct_answer) -> List[str]:
        """Generate verbose steps for fencing optimization."""
        l1 = problem.metadata['length1']
        w1 = problem.metadata['width1']
        l2 = problem.metadata['length2']
        w2 = problem.metadata['width2']
        area = l1 * w1
        perimeter1 = 2 * (l1 + w1)

        steps = []
        steps.append(f"Problem: Two garden designs with area {area} m²")
        steps.append(f"Design A: {l1}m × {w1}m, Design B: {l2}m × {w2}m")
        steps.append(f"How much fencing for Design B?")
        steps.append("")
        steps.append("MALRULE: Same area means same fencing needed")
        steps.append(f"  MALRULE REASONING: 'Same area = same perimeter'")
        steps.append(f"                     'Same space inside = same boundary'")
        steps.append("")
        steps.append(f"Step 1: Calculate fencing for Design A")
        steps.append(f"  Fencing A = 2({l1} + {w1}) = {perimeter1} meters")
        steps.append("")
        steps.append(f"Step 2: Apply malrule - same area means same fencing")
        steps.append(f"  Both designs have area {area} m²")
        steps.append(f"  So Fencing B = Fencing A = {malrule_answer} meters")
        steps.append("")
        steps.append(f"Final Answer: {malrule_answer} meters (INCORRECT!)")
        steps.append(f"  Should calculate: 2({l2} + {w2}) = {correct_answer} meters")
        return steps

    def _verbose_composite_shapes(self, problem: Problem, malrule_answer, correct_answer) -> List[str]:
        """Generate verbose steps for composite shapes."""
        area = problem.metadata['area']
        perimeter1 = problem.metadata['perimeter1']

        steps = []
        steps.append(f"Problem: Two L-shaped figures, both with area {area} square units")
        steps.append(f"Figure A has perimeter {perimeter1} units")
        steps.append(f"Find perimeter of Figure B")
        steps.append("")
        steps.append("MALRULE: Same area means same perimeter")
        steps.append(f"  MALRULE REASONING: 'Same area = same perimeter'")
        steps.append(f"                     'Same space inside = same boundary'")
        steps.append("")
        steps.append(f"Step 1: Note both have area {area}")
        steps.append(f"  Figure A: area {area}, perimeter {perimeter1}")
        steps.append("")
        steps.append(f"Step 2: Apply malrule - same area means same perimeter")
        steps.append(f"  So Perimeter B = Perimeter A = {malrule_answer}")
        steps.append("")
        steps.append(f"Final Answer: {malrule_answer} (INCORRECT!)")
        steps.append(f"  Should calculate actual perimeter = {correct_answer}")
        return steps

    def _verbose_square_vs_rectangle(self, problem: Problem, malrule_answer, correct_answer) -> List[str]:
        """Generate verbose steps for square vs rectangle."""
        side = problem.metadata['side']
        l2 = problem.metadata['length']
        w2 = problem.metadata['width']
        area = side * side
        perimeter1 = 4 * side

        steps = []
        steps.append(f"Problem: Square (side {side}) and Rectangle")
        steps.append(f"Both have same area. Find perimeter of rectangle.")
        steps.append("")
        steps.append("MALRULE: Same area means same perimeter")
        steps.append(f"  MALRULE REASONING: 'Same area = same perimeter'")
        steps.append(f"                     'Same space = same boundary'")
        steps.append("")
        steps.append(f"Step 1: Calculate perimeter of square")
        steps.append(f"  Square perimeter = 4 × {side} = {perimeter1}")
        steps.append("")
        steps.append(f"Step 2: Apply malrule - same area means same perimeter")
        steps.append(f"  Both have area {area}")
        steps.append(f"  So Rectangle perimeter = Square perimeter = {malrule_answer}")
        steps.append("")
        steps.append(f"Final Answer: {malrule_answer} (INCORRECT!)")
        steps.append(f"  Should calculate actual rectangle perimeter = {correct_answer}")
        return steps

    def _verbose_word_problem_context(self, problem: Problem, malrule_answer, correct_answer) -> List[str]:
        """Generate verbose steps for word problem context."""
        l1 = problem.metadata['length1']
        w1 = problem.metadata['width1']
        l2 = problem.metadata['length2']
        w2 = problem.metadata['width2']
        area = l1 * w1
        perimeter1 = 2 * (l1 + w1)

        steps = []
        steps.append(f"Word Problem: {problem.text}")
        steps.append("")
        steps.append("Step 1: Extract information from the word problem")
        steps.append(f"  Both rectangles have area {area} square units")
        steps.append(f"  Rectangle A: {l1} × {w1}")
        steps.append(f"  Rectangle B: {l2} × {w2}")
        steps.append(f"  Question: Find perimeter of Rectangle B")
        steps.append("")
        steps.append("Step 2: Apply malrule (same area = same perimeter)")
        steps.append("")
        steps.append("MALRULE: Same area means same perimeter")
        steps.append(f"  MALRULE REASONING: 'Same area = same perimeter'")
        steps.append(f"                     'If inside space is same, boundary is same'")
        steps.append("")
        steps.append(f"Step 3: Calculate perimeter of Rectangle A")
        steps.append(f"  Perimeter A = 2({l1} + {w1}) = {perimeter1}")
        steps.append("")
        steps.append(f"Step 4: Apply malrule - same area means same perimeter")
        steps.append(f"  Both rectangles have area {area}")
        steps.append(f"  So Perimeter B = Perimeter A = {malrule_answer}")
        steps.append("")
        steps.append(f"Final Answer: {malrule_answer} (INCORRECT!)")
        steps.append(f"  Should calculate actual perimeter B = 2({l2} + {w2}) = {correct_answer}")
        return steps

    def get_description(self) -> str:
        return (
            "Student incorrectly believes that figures having the same area must also "
            "have the same perimeter. This is the inverse of the 'Same Perimeter = Same Area' "
            "misconception and reflects the same fundamental confusion that area (enclosed "
            "surface) and perimeter (boundary length) are somehow dependent measures."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Malrule: same area means same perimeter (return perimeter of first shape)
        problem_type = problem.metadata.get('problem_type', 'rectangle_comparison')

        if problem_type in ['triangle_comparison', 'composite_shapes']:
            # For these, we need to use stored perimeter1 since calculation is complex
            return problem.metadata['perimeter1']
        elif problem_type == 'square_vs_rectangle':
            side = problem.metadata['side']
            return 4 * side
        else:
            # For rectangles, calculate perimeter1
            l1 = problem.metadata['length1']
            w1 = problem.metadata['width1']
            return 2 * (l1 + w1)

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """Apply malrule across all templates.

        Args:
            problem: The problem to solve
            verbose: If True, generate verbose steps; if False, generate concise steps (default: False)
        """
        problem_type = problem.metadata.get('problem_type', 'rectangle_comparison')

        # Calculate malrule answer and correct answer based on problem type
        if problem_type == 'triangle_comparison':
            malrule_answer = problem.metadata['perimeter1']
            correct_answer = problem.metadata['perimeter2']
        elif problem_type == 'fencing_optimization':
            l1 = problem.metadata['length1']
            w1 = problem.metadata['width1']
            l2 = problem.metadata['length2']
            w2 = problem.metadata['width2']
            malrule_answer = 2 * (l1 + w1)
            correct_answer = 2 * (l2 + w2)
        elif problem_type == 'composite_shapes':
            malrule_answer = problem.metadata['perimeter1']
            correct_answer = problem.metadata['perimeter2']
        elif problem_type == 'square_vs_rectangle':
            side = problem.metadata['side']
            l2 = problem.metadata['length']
            w2 = problem.metadata['width']
            malrule_answer = 4 * side
            correct_answer = 2 * (l2 + w2)
        elif problem_type == 'word_problem_context':
            l1 = problem.metadata['length1']
            w1 = problem.metadata['width1']
            l2 = problem.metadata['length2']
            w2 = problem.metadata['width2']
            malrule_answer = 2 * (l1 + w1)
            correct_answer = 2 * (l2 + w2)
        else:  # rectangle_comparison
            l1 = problem.metadata['length1']
            w1 = problem.metadata['width1']
            l2 = problem.metadata['length2']
            w2 = problem.metadata['width2']
            malrule_answer = 2 * (l1 + w1)
            correct_answer = 2 * (l2 + w2)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, malrule_answer, correct_answer)
        else:
            steps = self._generate_concise_steps(problem, malrule_answer, correct_answer)

        return Solution(
            answer=malrule_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
