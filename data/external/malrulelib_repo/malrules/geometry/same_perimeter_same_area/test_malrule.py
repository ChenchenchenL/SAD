#!/usr/bin/env python3
"""Test script for Same-Perimeter-Same-Area malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.geometry.same_perimeter_same_area import (
    SamePerimeterSameAreaProblemGenerator,
    SamePerimeterSameAreaMalrule,
    AreaCalculationCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING SAME-PERIMETER-SAME-AREA")
    print("="*70)

    malrule = SamePerimeterSameAreaMalrule()
    correct = AreaCalculationCorrectAlgorithm()

    # Test case 1: Classic 4×1 vs 3×2 (both perimeter 10)
    problem1 = Problem(
        text="Rectangle A: 4×1. Rectangle B: 3×2. Both have same perimeter. What is area of B?",
        operands=[4, 1, 3, 2],
        operation='rectangle_area_comparison',
        level=5,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'length1': 4,
            'width1': 1,
            'length2': 3,
            'width2': 2,
            'perimeter1': 10,
            'perimeter2': 10,
            'area1': 4,
            'area2': 6,
            'correct_answer': 6,  # 3×2 = 6
            'malrule_answer': 4   # Student: same perimeter = same area = 4
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: 4×1 vs 3×2 (perimeter 10) → Correct area B: {correct_sol.answer}, Malrule: {malrule_sol.answer}")
    assert correct_sol.answer == 6
    assert malrule_sol.answer == 4
    assert correct_sol.answer != malrule_sol.answer
    print("✓ PASSED (Classic example: same perimeter 10, but areas 4 vs 6)")

    # Test case 2: 5×1 vs 4×2 (both perimeter 12)
    problem2 = Problem(
        text="Rectangle A: 5×1. Rectangle B: 4×2. Both have same perimeter. What is area of B?",
        operands=[5, 1, 4, 2],
        operation='rectangle_area_comparison',
        level=5,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'length1': 5,
            'width1': 1,
            'length2': 4,
            'width2': 2,
            'perimeter1': 12,
            'perimeter2': 12,
            'area1': 5,
            'area2': 8,
            'correct_answer': 8,
            'malrule_answer': 5
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert correct_sol2.answer == 8
    assert malrule_sol2.answer == 5
    print("✓ TEST 2 PASSED (5×1 vs 4×2: perimeter 12, areas 5 vs 8)")

    # Test case 3: 6×2 vs 5×3 (both perimeter 16)
    problem3 = Problem(
        text="Rectangle A: 6×2. Rectangle B: 5×3. Both have same perimeter. What is area of B?",
        operands=[6, 2, 5, 3],
        operation='rectangle_area_comparison',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'length1': 6,
            'width1': 2,
            'length2': 5,
            'width2': 3,
            'perimeter1': 16,
            'perimeter2': 16,
            'area1': 12,
            'area2': 15,
            'correct_answer': 15,
            'malrule_answer': 12
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert correct_sol3.answer == 15
    assert malrule_sol3.answer == 12
    print("✓ TEST 3 PASSED (6×2 vs 5×3: perimeter 16, areas 12 vs 15)")

    # Test case 4: 7×1 vs 4×3 (both perimeter 14, but VERY different areas!)
    problem4 = Problem(
        text="Rectangle A: 7×1. Rectangle B: 4×3. Both have same perimeter. What is area of B?",
        operands=[7, 1, 4, 3],
        operation='rectangle_area_comparison',
        level=6,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'length1': 7,
            'width1': 1,
            'length2': 4,
            'width2': 3,
            'perimeter1': 16,
            'perimeter2': 14,  # Actually different! Let me fix
            'area1': 7,
            'area2': 12,
            'correct_answer': 12,
            'malrule_answer': 7
        }
    )

    # Fix: Make them have same perimeter
    problem4.metadata['perimeter2'] = 16
    problem4.operands = [8, 1, 5, 3]  # 8×1 and 5×3 both have perimeter 18
    problem4.text = "Rectangle A: 8×1. Rectangle B: 5×3. Both have same perimeter. What is area of B?"
    problem4.metadata['length1'] = 8
    problem4.metadata['width1'] = 1
    problem4.metadata['length2'] = 5
    problem4.metadata['width2'] = 3
    problem4.metadata['perimeter1'] = 18
    problem4.metadata['perimeter2'] = 16  # Still different, let me recalculate
    # 8×1: P = 2(8+1) = 18, A = 8
    # 5×3: P = 2(5+3) = 16, A = 15
    # Need same P. Try 7×2 and 5×3: P = 2(7+2) = 18, A = 14 vs P = 16
    # Try 6×3 and 7×2: both P = 18? 2(6+3) = 18 ✓, 2(7+2) = 18 ✓
    problem4.operands = [7, 2, 6, 3]
    problem4.text = "Rectangle A: 7×2. Rectangle B: 6×3. Both have same perimeter. What is area of B?"
    problem4.metadata['length1'] = 7
    problem4.metadata['width1'] = 2
    problem4.metadata['length2'] = 6
    problem4.metadata['width2'] = 3
    problem4.metadata['perimeter1'] = 18
    problem4.metadata['perimeter2'] = 18
    problem4.metadata['area1'] = 14
    problem4.metadata['area2'] = 18
    problem4.metadata['correct_answer'] = 18
    problem4.metadata['malrule_answer'] = 14

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    assert correct_sol4.answer == 18
    assert malrule_sol4.answer == 14
    print("✓ TEST 4 PASSED (7×2 vs 6×3: perimeter 18, areas 14 vs 18)")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_new_problem_templates():
    """Test new problem template types added for enhancement."""
    print("\n\n" + "="*70)
    print("TESTING NEW PROBLEM TEMPLATES")
    print("="*70)

    malrule = SamePerimeterSameAreaMalrule()
    correct = AreaCalculationCorrectAlgorithm()

    # TEST CASE 5: Square vs Rectangle (Square 5×5 vs Rectangle 7×3, both P=20)
    print("\n\nTEST CASE 5: Square vs Rectangle (Square 5×5 vs Rectangle 7×3, P=20)")
    print("-"*70)

    problem5 = Problem(
        text="Square A has side 5. Rectangle B is 7×3. Both have the same perimeter. What is the area of Rectangle B?",
        operands=[5, 5, 7, 3],
        operation='rectangle_area_comparison',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'length1': 5,
            'width1': 5,
            'length2': 7,
            'width2': 3,
            'perimeter1': 20,   # 4 × 5 = 20
            'perimeter2': 20,   # 2(7+3) = 20
            'area1': 25,        # 5 × 5 = 25
            'area2': 21,        # 7 × 3 = 21
            'correct_answer': 21,
            'malrule_answer': 25,  # Student thinks same P → same A
            'problem_type': 'square_vs_rectangle'
        }
    )

    correct_sol5 = correct.solve(problem5)
    malrule_sol5 = malrule.solve(problem5)

    print(f"Problem: {problem5.text}")
    print(f"Correct answer: {correct_sol5.answer}")
    print(f"Malrule answer: {malrule_sol5.answer}")

    # Correct: Rectangle B area = 7 × 3 = 21
    # Malrule: Student thinks same perimeter → same area = 25
    assert correct_sol5.answer == 21, f"Expected 21, got {correct_sol5.answer}"
    assert malrule_sol5.answer == 25, f"Expected 25 (malrule), got {malrule_sol5.answer}"

    print("✓ TEST CASE 5 PASSED: Square vs rectangle template works")

    # TEST CASE 6: Word problem - Garden context (6m×3m vs 5m×4m, P=18)
    print("\n\nTEST CASE 6: Word problem - Garden context (6m×3m vs 5m×4m, P=18)")
    print("-"*70)

    problem6 = Problem(
        text="Garden A is 6m × 3m. Garden B is 5m × 4m. Both use the same amount of fencing. What is the area of Garden B?",
        operands=[6, 3, 5, 4],
        operation='rectangle_area_comparison',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'length1': 6,
            'width1': 3,
            'length2': 5,
            'width2': 4,
            'perimeter1': 18,   # 2(6+3) = 18
            'perimeter2': 18,   # 2(5+4) = 18
            'area1': 18,        # 6 × 3 = 18
            'area2': 20,        # 5 × 4 = 20
            'correct_answer': 20,
            'malrule_answer': 18,
            'problem_type': 'word_problem_garden'
        }
    )

    correct_sol6 = correct.solve(problem6)
    malrule_sol6 = malrule.solve(problem6)

    print(f"Problem: {problem6.text}")
    print(f"Correct answer: {correct_sol6.answer}")
    print(f"Malrule answer: {malrule_sol6.answer}")

    # Correct: Garden B area = 5 × 4 = 20
    # Malrule: Same fencing → same area = 18
    assert correct_sol6.answer == 20, f"Expected 20, got {correct_sol6.answer}"
    assert malrule_sol6.answer == 18, f"Expected 18 (malrule), got {malrule_sol6.answer}"

    print("✓ TEST CASE 6 PASSED: Word problem garden template works")

    # TEST CASE 7: Three shapes comparison (P=20, three rectangles)
    print("\n\nTEST CASE 7: Three shapes comparison (All P=20)")
    print("-"*70)

    problem7 = Problem(
        text="Three rectangles all have perimeter 20. Rectangle A: 7×3. Rectangle B: 6×4. Rectangle C: 9×1. What is the area of Rectangle B?",
        operands=[7, 3, 6, 4],
        operation='rectangle_area_comparison',
        level=6,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'length1': 7,
            'width1': 3,
            'length2': 6,
            'width2': 4,
            'perimeter1': 20,   # 2(7+3) = 20
            'perimeter2': 20,   # 2(6+4) = 20
            'area1': 21,        # 7 × 3 = 21
            'area2': 24,        # 6 × 4 = 24
            'correct_answer': 24,
            'malrule_answer': 21,
            'problem_type': 'three_shapes_comparison'
        }
    )

    correct_sol7 = correct.solve(problem7)
    malrule_sol7 = malrule.solve(problem7)

    print(f"Problem: {problem7.text}")
    print(f"Correct answer: {correct_sol7.answer}")
    print(f"Malrule answer: {malrule_sol7.answer}")

    # Correct: Rectangle B area = 6 × 4 = 24
    # Malrule: Same perimeter → uses Rectangle A's area = 21
    assert correct_sol7.answer == 24, f"Expected 24, got {correct_sol7.answer}"
    assert malrule_sol7.answer == 21, f"Expected 21 (malrule), got {malrule_sol7.answer}"

    print("✓ TEST CASE 7 PASSED: Three shapes comparison template works")

    # TEST CASE 8: Extreme dimensions (9×1 vs 7×3, P=20)
    print("\n\nTEST CASE 8: Extreme dimensions (9×1 vs 7×3, P=20)")
    print("-"*70)

    problem8 = Problem(
        text="Rectangle A: 9×1. Rectangle B: 7×3. Both have the same perimeter of 20. What is the area of Rectangle B?",
        operands=[9, 1, 7, 3],
        operation='rectangle_area_comparison',
        level=6,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'length1': 9,
            'width1': 1,
            'length2': 7,
            'width2': 3,
            'perimeter1': 20,   # 2(9+1) = 20
            'perimeter2': 20,   # 2(7+3) = 20
            'area1': 9,         # 9 × 1 = 9
            'area2': 21,        # 7 × 3 = 21
            'correct_answer': 21,
            'malrule_answer': 9,
            'problem_type': 'extreme_dimensions'
        }
    )

    correct_sol8 = correct.solve(problem8)
    malrule_sol8 = malrule.solve(problem8)

    print(f"Problem: {problem8.text}")
    print(f"Correct answer: {correct_sol8.answer}")
    print(f"Malrule answer: {malrule_sol8.answer}")

    # Correct: Rectangle B area = 7 × 3 = 21
    # Malrule: Same perimeter → same area = 9 (dramatic difference!)
    assert correct_sol8.answer == 21, f"Expected 21, got {correct_sol8.answer}"
    assert malrule_sol8.answer == 9, f"Expected 9 (malrule), got {malrule_sol8.answer}"

    print("✓ TEST CASE 8 PASSED: Extreme dimensions template works")

    print("\n" + "="*70)
    print("ALL NEW TEMPLATE TEST CASES PASSED ✓")
    print("="*70)


def test_template_generation():
    """Test that all template types can be generated."""
    print("\n\n" + "="*70)
    print("TESTING TEMPLATE GENERATION")
    print("="*70)

    problem_gen = SamePerimeterSameAreaProblemGenerator(
        level=6,
        difficulty=DifficultyLevel.MEDIUM
    )

    # Generate multiple problems to cover all template types
    templates_found = set()
    for i in range(50):
        problem = problem_gen.generate(seed=13000 + i)
        if 'problem_type' in problem.metadata:
            templates_found.add(problem.metadata['problem_type'])

    print(f"\nTemplates generated: {sorted(templates_found)}")

    # Verify we have all expected templates
    expected_templates = {
        'simple_rectangles',
        'square_vs_rectangle',
        'word_problem_garden',
        'three_shapes_comparison',
        'extreme_dimensions',
    }
    assert templates_found >= expected_templates, \
        f"Missing templates: {expected_templates - templates_found}"

    print("\n✓ ALL TEMPLATE TYPES GENERATED SUCCESSFULLY")
    print("="*70)


def test_automated_suite():
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = SamePerimeterSameAreaProblemGenerator(
        level=5,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = SamePerimeterSameAreaMalrule()
    correct = AreaCalculationCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Same-Perimeter-Same-Area  ".center(70) + "║")
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
