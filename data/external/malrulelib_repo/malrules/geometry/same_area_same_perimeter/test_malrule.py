#!/usr/bin/env python3
"""Test script for Same-Area-Same-Perimeter malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.geometry.same_area_same_perimeter import (
    SameAreaSamePerimeterProblemGenerator,
    SameAreaSamePerimeterMalrule,
    PerimeterCalculationCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING SAME-AREA-SAME-PERIMETER")
    print("="*70)

    malrule = SameAreaSamePerimeterMalrule()
    correct = PerimeterCalculationCorrectAlgorithm()

    # Test case 1: Classic 4×2 vs 8×1 (both area 8)
    problem1 = Problem(
        text="Rectangle A: 4×2. Rectangle B: 8×1. Both have same area. What is perimeter of B?",
        operands=[4, 2, 8, 1],
        operation='rectangle_perimeter_comparison',
        level=5,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'length1': 4,
            'width1': 2,
            'length2': 8,
            'width2': 1,
            'area1': 8,
            'area2': 8,
            'perimeter1': 12,
            'perimeter2': 18,
            'correct_answer': 18,  # 2(8+1) = 18
            'malrule_answer': 12   # Student: same area = same perimeter = 12
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: 4×2 vs 8×1 (area 8) → Correct perimeter B: {correct_sol.answer}, Malrule: {malrule_sol.answer}")
    assert correct_sol.answer == 18
    assert malrule_sol.answer == 12
    assert correct_sol.answer != malrule_sol.answer
    print("✓ PASSED (Classic example: same area 8, but perimeters 12 vs 18)")

    # Test case 2: 3×4 vs 6×2 (both area 12)
    problem2 = Problem(
        text="Rectangle A: 3×4. Rectangle B: 6×2. Both have same area. What is perimeter of B?",
        operands=[3, 4, 6, 2],
        operation='rectangle_perimeter_comparison',
        level=5,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'length1': 3,
            'width1': 4,
            'length2': 6,
            'width2': 2,
            'area1': 12,
            'area2': 12,
            'perimeter1': 14,
            'perimeter2': 16,
            'correct_answer': 16,
            'malrule_answer': 14
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert correct_sol2.answer == 16
    assert malrule_sol2.answer == 14
    print("✓ TEST 2 PASSED (3×4 vs 6×2: area 12, perimeters 14 vs 16)")

    # Test case 3: 4×3 vs 12×1 (both area 12, very different perimeters!)
    problem3 = Problem(
        text="Rectangle A: 4×3. Rectangle B: 12×1. Both have same area. What is perimeter of B?",
        operands=[4, 3, 12, 1],
        operation='rectangle_perimeter_comparison',
        level=6,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'length1': 4,
            'width1': 3,
            'length2': 12,
            'width2': 1,
            'area1': 12,
            'area2': 12,
            'perimeter1': 14,
            'perimeter2': 26,
            'correct_answer': 26,
            'malrule_answer': 14
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert correct_sol3.answer == 26
    assert malrule_sol3.answer == 14
    print("✓ TEST 3 PASSED (4×3 vs 12×1: area 12, perimeters 14 vs 26 - big difference!)")

    # Test case 4: 5×3 vs 15×1 (both area 15)
    problem4 = Problem(
        text="Rectangle A: 5×3. Rectangle B: 15×1. Both have same area. What is perimeter of B?",
        operands=[5, 3, 15, 1],
        operation='rectangle_perimeter_comparison',
        level=6,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'length1': 5,
            'width1': 3,
            'length2': 15,
            'width2': 1,
            'area1': 15,
            'area2': 15,
            'perimeter1': 16,
            'perimeter2': 32,
            'correct_answer': 32,
            'malrule_answer': 16
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    assert correct_sol4.answer == 32
    assert malrule_sol4.answer == 16
    print("✓ TEST 4 PASSED (5×3 vs 15×1: area 15, perimeters 16 vs 32)")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_new_problem_templates():
    """Test new problem template types added for enhancement."""
    print("\n" + "="*70)
    print("TESTING NEW PROBLEM TEMPLATES")
    print("="*70)

    malrule = SameAreaSamePerimeterMalrule()
    correct = PerimeterCalculationCorrectAlgorithm()

    # TEST CASE 5: Triangle comparison - triangles with same area but different perimeters
    # Triangle A: base 6, height 4 (area 12) perimeter ≈ 17.2
    # Triangle B: base 12, height 2 (area 12) perimeter ≈ 26.2
    problem5 = Problem(
        text="Triangle A has base 6 and height 4. Triangle B has base 12 and height 2. Both have the same area. What is the perimeter of Triangle B (assuming right triangles)?",
        operands=[6, 4, 12, 2],
        operation='triangle_perimeter_comparison',
        level=6,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'base1': 6,
            'height1': 4,
            'base2': 12,
            'height2': 2,
            'area': 12,
            'perimeter1': 17.2,
            'perimeter2': 26.2,
            'problem_type': 'triangle_comparison',
            'correct_answer': 26.2,
            'malrule_answer': 17.2
        }
    )

    correct_sol5 = correct.solve(problem5)
    malrule_sol5 = malrule.solve(problem5)

    print(f"\nTEST 5: Triangle comparison → Correct: {correct_sol5.answer}, Malrule: {malrule_sol5.answer}")
    assert correct_sol5.answer == 26.2
    assert malrule_sol5.answer == 17.2
    assert correct_sol5.answer != malrule_sol5.answer
    print("✓ PASSED (Triangles: same area 12, different perimeters)")

    # TEST CASE 6: Fencing optimization - word problem with area constraint
    # Garden A: 6×4 (area 24) perimeter 20
    # Garden B: 12×2 (area 24) perimeter 28
    problem6 = Problem(
        text="A farmer has two rectangular garden designs, both with area 24 square meters. Design A is 6m × 4m. Design B is 12m × 2m. How much fencing is needed for Design B?",
        operands=[6, 4, 12, 2],
        operation='fencing_word_problem',
        level=5,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'length1': 6,
            'width1': 4,
            'length2': 12,
            'width2': 2,
            'area': 24,
            'perimeter1': 20,
            'perimeter2': 28,
            'problem_type': 'fencing_optimization',
            'correct_answer': 28,
            'malrule_answer': 20,
            'context': 'fencing'
        }
    )

    correct_sol6 = correct.solve(problem6)
    malrule_sol6 = malrule.solve(problem6)

    print(f"TEST 6: Fencing word problem → Correct: {correct_sol6.answer}m, Malrule: {malrule_sol6.answer}m")
    assert correct_sol6.answer == 28
    assert malrule_sol6.answer == 20
    print("✓ PASSED (Fencing: same area 24m², different fencing needs)")

    # TEST CASE 7: Composite shapes - L-shapes with same area
    # L-shape A: area 12, perimeter 16
    # L-shape B: area 12, perimeter 20
    problem7 = Problem(
        text="Two L-shaped figures both have area 12 square units. Figure A has perimeter 16 units. What is the perimeter of Figure B?",
        operands=[12, 16, 20, 0],
        operation='composite_shape_comparison',
        level=6,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'area': 12,
            'perimeter1': 16,
            'perimeter2': 20,
            'problem_type': 'composite_shapes',
            'correct_answer': 20,
            'malrule_answer': 16
        }
    )

    correct_sol7 = correct.solve(problem7)
    malrule_sol7 = malrule.solve(problem7)

    print(f"TEST 7: Composite L-shapes → Correct: {correct_sol7.answer}, Malrule: {malrule_sol7.answer}")
    assert correct_sol7.answer == 20
    assert malrule_sol7.answer == 16
    print("✓ PASSED (L-shapes: same area 12, different perimeters)")

    # TEST CASE 8: Square vs rectangle
    # Square: side 4 (area 16, perimeter 16)
    # Rectangle: 8×2 (area 16, perimeter 20)
    problem8 = Problem(
        text="A square with side length 4 and a rectangle 8×2 have the same area. What is the perimeter of the rectangle?",
        operands=[4, 4, 8, 2],
        operation='square_vs_rectangle_comparison',
        level=5,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'side': 4,
            'length': 8,
            'width': 2,
            'area': 16,
            'perimeter1': 16,
            'perimeter2': 20,
            'problem_type': 'square_vs_rectangle',
            'correct_answer': 20,
            'malrule_answer': 16
        }
    )

    correct_sol8 = correct.solve(problem8)
    malrule_sol8 = malrule.solve(problem8)

    print(f"TEST 8: Square vs rectangle → Correct: {correct_sol8.answer}, Malrule: {malrule_sol8.answer}")
    assert correct_sol8.answer == 20
    assert malrule_sol8.answer == 16
    print("✓ PASSED (Square 4×4 vs rectangle 8×2: same area 16, different perimeters)")

    print("\n" + "="*70)
    print("ALL NEW TEMPLATE TESTS PASSED ✓")
    print("="*70)


def test_template_generation():
    """Test that all template types can be generated."""
    print("\n" + "="*70)
    print("TESTING TEMPLATE GENERATION")
    print("="*70)

    problem_gen = SameAreaSamePerimeterProblemGenerator(
        level=6,
        difficulty=DifficultyLevel.MEDIUM
    )

    templates_found = set()
    for i in range(100):
        problem = problem_gen.generate(seed=80000 + i)
        if 'problem_type' in problem.metadata:
            templates_found.add(problem.metadata['problem_type'])

    expected_templates = {
        'rectangle_comparison',
        'triangle_comparison',
        'fencing_optimization',
        'composite_shapes',
        'square_vs_rectangle'
    }

    print(f"\nFound templates: {templates_found}")
    print(f"Expected templates: {expected_templates}")

    assert templates_found >= expected_templates, f"Missing templates: {expected_templates - templates_found}"
    print("\n✓ ALL TEMPLATE TYPES CAN BE GENERATED")

    print("\n" + "="*70)
    print("TEMPLATE GENERATION TEST PASSED ✓")
    print("="*70)


def test_automated_suite():
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = SameAreaSamePerimeterProblemGenerator(
        level=5,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = SameAreaSamePerimeterMalrule()
    correct = PerimeterCalculationCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Same-Area-Same-Perimeter  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    try:
        test_specific_examples()
        test_new_problem_templates()
        test_template_generation()
        all_passed = test_automated_suite()
        print("\n\n╔" + "═"*68 + "╗")
        print("║" + "  ✓✓✓ VERIFICATION COMPLETE ✓✓✓  ".center(70) + "║")
        print("╚" + "═"*68 + "╝\n")
        return 0 if all_passed else 1
    except Exception as e:
        print(f"\n✗✗✗ TEST FAILED: {e} ✗✗✗")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
