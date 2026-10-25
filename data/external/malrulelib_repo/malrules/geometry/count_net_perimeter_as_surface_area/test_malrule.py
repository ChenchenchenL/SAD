#!/usr/bin/env python3
"""Test script for Count-Net-Perimeter-As-Surface-Area malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.geometry.count_net_perimeter_as_surface_area import (
    CountNetPerimeterAsSurfaceAreaProblemGenerator,
    CountNetPerimeterAsSurfaceAreaMalrule,
    NetSurfaceAreaCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING COUNT-NET-PERIMETER-AS-SURFACE-AREA")
    print("="*70)

    malrule = CountNetPerimeterAsSurfaceAreaMalrule()
    correct = NetSurfaceAreaCorrectAlgorithm()

    # Test case 1: Cube with side 3
    problem1 = Problem(
        text="A cube with side length 3 is unfolded into a net. What is the surface area of the cube?",
        operands=[3],
        operation='surface_area_from_net',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'shape_type': 'cube',
            'side': 3,
            'surface_area': 54,      # 6 × 3² = 54
            'net_perimeter': 36,     # 12 × 3 = 36 (cross-shaped net)
            'correct_answer': 54,
            'malrule_answer': 36
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: Cube side 3 → Correct SA: {correct_sol.answer}, Malrule (net perimeter): {malrule_sol.answer}")
    assert correct_sol.answer == 54
    assert malrule_sol.answer == 36
    assert correct_sol.answer != malrule_sol.answer
    print("✓ PASSED (Cube side 3: SA=54, not perimeter=36)")

    # Test case 2: Cube with side 5
    problem2 = Problem(
        text="A cube with side length 5 is unfolded into a net. What is the surface area of the cube?",
        operands=[5],
        operation='surface_area_from_net',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'shape_type': 'cube',
            'side': 5,
            'surface_area': 150,     # 6 × 5² = 150
            'net_perimeter': 60,     # 12 × 5 = 60
            'correct_answer': 150,
            'malrule_answer': 60
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert correct_sol2.answer == 150
    assert malrule_sol2.answer == 60
    assert correct_sol2.answer != malrule_sol2.answer
    print("✓ TEST 2 PASSED (Cube side 5: SA=150, not perimeter=60)")

    # Test case 3: Rectangular prism 2×3×4
    problem3 = Problem(
        text="A rectangular prism with dimensions 2×3×4 is unfolded into a net. What is the surface area of the prism?",
        operands=[2, 3, 4],
        operation='surface_area_from_net',
        level=7,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'shape_type': 'rectangular_prism',
            'length': 2,
            'width': 3,
            'height': 4,
            'lw': 6,
            'lh': 8,
            'wh': 12,
            'surface_area': 52,      # 2(6+8+12) = 52
            'net_perimeter': 36,     # 4(2+3+4) = 36
            'correct_answer': 52,
            'malrule_answer': 36
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert correct_sol3.answer == 52
    assert malrule_sol3.answer == 36
    assert correct_sol3.answer != malrule_sol3.answer
    print("✓ TEST 3 PASSED (Rectangular prism 2×3×4: SA=52, not perimeter=36)")

    # Test case 4: Rectangular prism 3×4×5
    problem4 = Problem(
        text="A rectangular prism with dimensions 3×4×5 is unfolded into a net. What is the surface area of the prism?",
        operands=[3, 4, 5],
        operation='surface_area_from_net',
        level=7,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'shape_type': 'rectangular_prism',
            'length': 3,
            'width': 4,
            'height': 5,
            'lw': 12,
            'lh': 15,
            'wh': 20,
            'surface_area': 94,      # 2(12+15+20) = 94
            'net_perimeter': 48,     # 4(3+4+5) = 48
            'correct_answer': 94,
            'malrule_answer': 48
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    assert correct_sol4.answer == 94
    assert malrule_sol4.answer == 48
    assert correct_sol4.answer != malrule_sol4.answer
    print("✓ TEST 4 PASSED (Rectangular prism 3×4×5: SA=94, not perimeter=48)")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_all_templates():
    """Test all 5 templates for Count-Net-Perimeter-As-Surface-Area."""
    print("\n\n" + "="*70)
    print("TESTING ALL TEMPLATES")
    print("="*70)

    problem_gen = CountNetPerimeterAsSurfaceAreaProblemGenerator(
        level=6,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = CountNetPerimeterAsSurfaceAreaMalrule()
    correct = NetSurfaceAreaCorrectAlgorithm()

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

        # Verify answers
        print(f"  Problem: {problem.text[:80]}...")
        print(f"  Correct answer: {correct_sol.answer}")
        print(f"  Malrule answer: {malrule_sol.answer}")

        # Verify different answers (malrule should give perimeter, not surface area)
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

    problem_gen = CountNetPerimeterAsSurfaceAreaProblemGenerator(
        level=6,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = CountNetPerimeterAsSurfaceAreaMalrule()
    correct = NetSurfaceAreaCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Count-Net-Perimeter-As-Surface-Area  ".center(70) + "║")
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
