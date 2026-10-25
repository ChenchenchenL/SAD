#!/usr/bin/env python3
"""Test script for Slope-Is-Delta-X-Over-Delta-Y malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from fractions import Fraction
from malrules.linear_equations.slope_is_delta_x_over_delta_y import (
    SlopeIsDeltaXOverDeltaYProblemGenerator,
    SlopeIsDeltaXOverDeltaYMalrule,
    SlopeCalculationCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING SLOPE-IS-DELTA-X-OVER-DELTA-Y")
    print("="*70)

    malrule = SlopeIsDeltaXOverDeltaYMalrule()
    correct = SlopeCalculationCorrectAlgorithm()

    # Test case 1: Classic (2,3) to (5,11) example
    problem1 = Problem(
        text="Find the slope of the line passing through points (2, 3) and (5, 11).",
        operands=[2, 3, 5, 11],
        operation='slope_calculation',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'x1': 2,
            'y1': 3,
            'x2': 5,
            'y2': 11,
            'delta_x': 3,      # 5 - 2
            'delta_y': 8,      # 11 - 3
            'slope': Fraction(8, 3),
            'malrule_slope': Fraction(3, 8),
            'correct_answer': '8/3',
            'malrule_answer': '3/8'
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: (2,3) to (5,11) → Correct: {correct_sol.answer}, Malrule: {malrule_sol.answer}")
    assert correct_sol.answer == '8/3'
    assert malrule_sol.answer == '3/8'
    assert correct_sol.answer != malrule_sol.answer
    print("✓ PASSED (Classic example: slope=8/3, not 3/8)")

    # Test case 2: (1,2) to (4,8)
    problem2 = Problem(
        text="Find the slope of the line passing through points (1, 2) and (4, 8).",
        operands=[1, 2, 4, 8],
        operation='slope_calculation',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'x1': 1,
            'y1': 2,
            'x2': 4,
            'y2': 8,
            'delta_x': 3,      # 4 - 1
            'delta_y': 6,      # 8 - 2
            'slope': Fraction(6, 3),
            'malrule_slope': Fraction(3, 6),
            'correct_answer': '2',
            'malrule_answer': '1/2'
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert correct_sol2.answer == '2'
    assert malrule_sol2.answer == '1/2'
    print("✓ TEST 2 PASSED ((1,2) to (4,8): slope=2, not 1/2)")

    # Test case 3: (0,1) to (5,7)
    problem3 = Problem(
        text="Find the slope of the line passing through points (0, 1) and (5, 7).",
        operands=[0, 1, 5, 7],
        operation='slope_calculation',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'x1': 0,
            'y1': 1,
            'x2': 5,
            'y2': 7,
            'delta_x': 5,      # 5 - 0
            'delta_y': 6,      # 7 - 1
            'slope': Fraction(6, 5),
            'malrule_slope': Fraction(5, 6),
            'correct_answer': '6/5',
            'malrule_answer': '5/6'
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert correct_sol3.answer == '6/5'
    assert malrule_sol3.answer == '5/6'
    print("✓ TEST 3 PASSED ((0,1) to (5,7): slope=6/5, not 5/6)")

    # Test case 4: (3,4) to (7,10)
    problem4 = Problem(
        text="Find the slope of the line passing through points (3, 4) and (7, 10).",
        operands=[3, 4, 7, 10],
        operation='slope_calculation',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'x1': 3,
            'y1': 4,
            'x2': 7,
            'y2': 10,
            'delta_x': 4,      # 7 - 3
            'delta_y': 6,      # 10 - 4
            'slope': Fraction(6, 4),
            'malrule_slope': Fraction(4, 6),
            'correct_answer': '3/2',
            'malrule_answer': '2/3'
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    assert correct_sol4.answer == '3/2'
    assert malrule_sol4.answer == '2/3'
    print("✓ TEST 4 PASSED ((3,4) to (7,10): slope=3/2, not 2/3)")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_all_templates():
    """Test all 5 templates for Slope-Is-Delta-X-Over-Delta-Y."""
    print("\n\n" + "="*70)
    print("TESTING ALL TEMPLATES")
    print("="*70)

    problem_gen = SlopeIsDeltaXOverDeltaYProblemGenerator(
        level=8,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = SlopeIsDeltaXOverDeltaYMalrule()
    correct = SlopeCalculationCorrectAlgorithm()

    templates = problem_gen.get_available_templates()
    print(f"\nFound {len(templates)} templates: {templates}")
    assert len(templates) == 5, f"Expected 5 templates, got {len(templates)}"

    all_passed = True
    for template in templates:
        print(f"\n--- Testing template: {template} ---")

        # Generate problem with this template
        problem = problem_gen.generate(seed=42, template=template)

        # Solve with both algorithms
        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        # Verify answers
        print(f"  Problem: {problem.text[:80]}...")

        try:
            # Check if algorithms produce different answers
            if str(correct_sol.answer) == str(malrule_sol.answer):
                # Edge case: misconception produces same answer
                print(f"  ⚠️  WARNING: Correct and malrule produce same answer!")
                print(f"  Answer: {correct_sol.answer}")
                print(f"\n  Correct algorithm steps:")
                for step in correct_sol.steps:
                    print(f"    {step}")
                print(f"\n  Malrule algorithm steps:")
                for step in malrule_sol.steps:
                    print(f"    {step}")
                print(f"  ✗ Template {template} FAILED (same answer produced)")
                all_passed = False
                continue

            # Verify calculate_expected_answer matches malrule output
            expected = malrule.calculate_expected_answer(problem)

            if str(malrule_sol.answer) != str(expected):
                print(f"  ✗ MISMATCH: calculate_expected_answer() returned {expected} but malrule produced {malrule_sol.answer}")
                print(f"\n  Malrule algorithm steps:")
                for step in malrule_sol.steps:
                    print(f"    {step}")
                all_passed = False
                continue

            # Test passed
            print(f"  ✓ Correct answer: {correct_sol.answer}")
            print(f"  ✓ Malrule answer: {malrule_sol.answer}")
            print(f"  ✓ Template {template} PASSED")

        except AssertionError as e:
            print(f"  ✗ Template {template} FAILED: {e}")
            print(f"\n  Correct algorithm steps:")
            for step in correct_sol.steps:
                print(f"    {step}")
            print(f"\n  Malrule algorithm steps:")
            for step in malrule_sol.steps:
                print(f"    {step}")
            all_passed = False

    print("\n" + "="*70)
    if all_passed:
        print("ALL TEMPLATE TESTS PASSED ✓")
    else:
        print("SOME TEMPLATE TESTS FAILED ✗")
    print("="*70)
    return all_passed


def test_automated_suite():
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = SlopeIsDeltaXOverDeltaYProblemGenerator(
        level=8,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = SlopeIsDeltaXOverDeltaYMalrule()
    correct = SlopeCalculationCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Slope-Is-Delta-X-Over-Delta-Y  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    try:
        test_specific_examples()
        templates_passed = test_all_templates()
        automated_passed = test_automated_suite()
        all_passed = templates_passed and automated_passed

        print("\n\n╔" + "═"*68 + "╗")
        if all_passed:
            print("║" + "  ✓✓✓ VERIFICATION COMPLETE ✓✓✓  ".center(70) + "║")
        else:
            print("║" + "  ✗✗✗ SOME TESTS FAILED ✗✗✗  ".center(70) + "║")
        print("╚" + "═"*68 + "╝\n")
        return 0 if all_passed else 1
    except Exception as e:
        print(f"\n✗✗✗ TEST FAILED: {e} ✗✗✗")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
