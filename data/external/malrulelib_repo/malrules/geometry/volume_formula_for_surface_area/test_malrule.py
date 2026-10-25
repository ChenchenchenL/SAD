#!/usr/bin/env python3
"""Test script for Volume-Formula-For-Surface-Area malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.geometry.volume_formula_for_surface_area import (
    VolumeFormulaForSurfaceAreaProblemGenerator,
    VolumeFormulaForSurfaceAreaMalrule,
    SurfaceAreaCalculationCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING VOLUME-FORMULA-FOR-SURFACE-AREA")
    print("="*70)

    malrule = VolumeFormulaForSurfaceAreaMalrule()
    correct = SurfaceAreaCalculationCorrectAlgorithm()

    # Test case 1: Classic 3×4×5 box
    problem1 = Problem(
        text="Find the surface area of a rectangular prism with length 3, width 4, and height 5.",
        operands=[3, 4, 5],
        operation='surface_area_rectangular_prism',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'length': 3,
            'width': 4,
            'height': 5,
            'lw': 12,
            'lh': 15,
            'wh': 20,
            'surface_area': 94,  # 2(12+15+20) = 2(47) = 94
            'volume': 60,        # 3×4×5 = 60 (WRONG!)
            'correct_answer': 94,
            'malrule_answer': 60
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: 3×4×5 box → Correct SA: {correct_sol.answer}, Malrule (uses volume): {malrule_sol.answer}")
    assert correct_sol.answer == 94
    assert malrule_sol.answer == 60
    assert correct_sol.answer != malrule_sol.answer
    print("✓ PASSED (Classic example: SA=94, not V=60)")

    # Test case 2: 2×3×4 box
    problem2 = Problem(
        text="Find the surface area of a rectangular prism with length 2, width 3, and height 4.",
        operands=[2, 3, 4],
        operation='surface_area_rectangular_prism',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'length': 2,
            'width': 3,
            'height': 4,
            'lw': 6,
            'lh': 8,
            'wh': 12,
            'surface_area': 52,  # 2(6+8+12) = 2(26) = 52
            'volume': 24,        # 2×3×4 = 24 (WRONG!)
            'correct_answer': 52,
            'malrule_answer': 24
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert correct_sol2.answer == 52
    assert malrule_sol2.answer == 24
    print("✓ TEST 2 PASSED (2×3×4: SA=52, not V=24)")

    # Test case 3: 5×6×7 box
    problem3 = Problem(
        text="Find the surface area of a rectangular prism with length 5, width 6, and height 7.",
        operands=[5, 6, 7],
        operation='surface_area_rectangular_prism',
        level=7,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'length': 5,
            'width': 6,
            'height': 7,
            'lw': 30,
            'lh': 35,
            'wh': 42,
            'surface_area': 214,  # 2(30+35+42) = 2(107) = 214
            'volume': 210,        # 5×6×7 = 210 (WRONG!)
            'correct_answer': 214,
            'malrule_answer': 210
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert correct_sol3.answer == 214
    assert malrule_sol3.answer == 210
    print("✓ TEST 3 PASSED (5×6×7: SA=214, not V=210)")

    # Test case 4: 4×5×6 box
    problem4 = Problem(
        text="Find the surface area of a rectangular prism with length 4, width 5, and height 6.",
        operands=[4, 5, 6],
        operation='surface_area_rectangular_prism',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'length': 4,
            'width': 5,
            'height': 6,
            'lw': 20,
            'lh': 24,
            'wh': 30,
            'surface_area': 148,  # 2(20+24+30) = 2(74) = 148
            'volume': 120,        # 4×5×6 = 120 (WRONG!)
            'correct_answer': 148,
            'malrule_answer': 120
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    assert correct_sol4.answer == 148
    assert malrule_sol4.answer == 120
    print("✓ TEST 4 PASSED (4×5×6: SA=148, not V=120)")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_all_templates():
    """Test all 5 templates for Volume-Formula-For-Surface-Area."""
    print("\n\n" + "="*70)
    print("TESTING ALL TEMPLATES")
    print("="*70)

    problem_gen = VolumeFormulaForSurfaceAreaProblemGenerator(
        level=6,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = VolumeFormulaForSurfaceAreaMalrule()
    correct = SurfaceAreaCalculationCorrectAlgorithm()

    templates = problem_gen.get_available_templates()
    print(f"\nFound {len(templates)} templates: {templates}")
    assert len(templates) == 5, f"Expected 5 templates, got {len(templates)}"

    for template in templates:
        print(f"\n--- Testing template: {template} ---")

        # Generate problem with this template
        problem = problem_gen.generate(seed=42, template=template)

        # Solve with both algorithms
        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        # Verify different answers
        print(f"  Correct answer: {correct_sol.answer}")
        print(f"  Malrule answer: {malrule_sol.answer}")

        assert str(correct_sol.answer) != str(malrule_sol.answer), \
            f"Template {template}: Correct and malrule answers should be different!"

        # Verify calculate_expected_answer matches malrule output
        expected = malrule.calculate_expected_answer(problem)
        print(f"  Expected answer: {expected}")

        assert str(malrule_sol.answer) == str(expected), \
            f"Template {template}: calculate_expected_answer() returned {expected} but malrule produced {malrule_sol.answer}"

        print(f"  ✓ Template {template} PASSED")

    print("\n" + "="*70)
    print("ALL TEMPLATE TESTS PASSED ✓")
    print("="*70)


def test_automated_suite():
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = VolumeFormulaForSurfaceAreaProblemGenerator(
        level=6,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = VolumeFormulaForSurfaceAreaMalrule()
    correct = SurfaceAreaCalculationCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Volume-Formula-For-Surface-Area  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    try:
        test_specific_examples()
        test_all_templates()
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
