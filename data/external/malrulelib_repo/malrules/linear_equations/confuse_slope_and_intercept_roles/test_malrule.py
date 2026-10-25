#!/usr/bin/env python3
"""Test script for Confuse-Slope-And-Intercept-Roles malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.linear_equations.confuse_slope_and_intercept_roles import (
    ConfuseSlopeAndInterceptRolesProblemGenerator,
    ConfuseSlopeAndInterceptRolesMalrule,
    SlopeInterceptCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING CONFUSE-SLOPE-AND-INTERCEPT-ROLES")
    print("="*70)

    malrule = ConfuseSlopeAndInterceptRolesMalrule()
    correct = SlopeInterceptCorrectAlgorithm()

    # Test case 1: Write equation with slope = 3, y-intercept = 5 (classic example)
    problem1 = Problem(
        text="Write the equation of a line with slope 3 and y-intercept 5.",
        operands=[3, 5],
        operation='write_equation',
        level=8,
        difficulty=DifficultyLevel.EASY,
        metadata={
            'slope': 3,
            'y_intercept': 5,
            'problem_type': 'write_equation',
            'correct_equation': 'y = 3x + 5',
            'malrule_equation': 'y = 5x + 3'
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: Slope=3, y-int=5 → Correct: {correct_sol.answer}, Malrule: {malrule_sol.answer}")
    assert correct_sol.answer == 'y = 3x + 5'
    assert malrule_sol.answer == 'y = 5x + 3'
    assert correct_sol.answer != malrule_sol.answer
    print("✓ PASSED (y = 3x + 5, not y = 5x + 3)")

    # Test case 2: Identify slope from y = 2x + 7
    problem2 = Problem(
        text="What is the slope of the line y = 2x + 7?",
        operands=[2, 7],
        operation='identify_slope',
        level=8,
        difficulty=DifficultyLevel.EASY,
        metadata={
            'slope': 2,
            'y_intercept': 7,
            'equation': 'y = 2x + 7',
            'problem_type': 'identify_slope',
            'correct_answer': '2',
            'malrule_answer': '7'
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)

    print(f"\nTEST 2: y = 2x + 7 slope → Correct: {correct_sol2.answer}, Malrule: {malrule_sol2.answer}")
    assert correct_sol2.answer == '2'
    assert malrule_sol2.answer == '7'
    assert correct_sol2.answer != malrule_sol2.answer
    print("✓ PASSED (slope is 2, not 7)")

    # Test case 3: Write equation with negative values, slope = -4, y-intercept = 6
    problem3 = Problem(
        text="Write the equation of a line with slope -4 and y-intercept 6.",
        operands=[-4, 6],
        operation='write_equation',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'slope': -4,
            'y_intercept': 6,
            'problem_type': 'write_equation',
            'correct_equation': 'y = -4x + 6',
            'malrule_equation': 'y = 6x - 4'
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)

    print(f"\nTEST 3: Slope=-4, y-int=6 → Correct: {correct_sol3.answer}, Malrule: {malrule_sol3.answer}")
    assert correct_sol3.answer == 'y = -4x + 6'
    assert malrule_sol3.answer == 'y = 6x - 4'
    assert correct_sol3.answer != malrule_sol3.answer
    print("✓ PASSED (y = -4x + 6, not y = 6x - 4)")

    # Test case 4: Identify slope from y = -3x + 8
    problem4 = Problem(
        text="What is the slope of the line y = -3x + 8?",
        operands=[-3, 8],
        operation='identify_slope',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'slope': -3,
            'y_intercept': 8,
            'equation': 'y = -3x + 8',
            'problem_type': 'identify_slope',
            'correct_answer': '-3',
            'malrule_answer': '8'
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)

    print(f"\nTEST 4: y = -3x + 8 slope → Correct: {correct_sol4.answer}, Malrule: {malrule_sol4.answer}")
    assert correct_sol4.answer == '-3'
    assert malrule_sol4.answer == '8'
    assert correct_sol4.answer != malrule_sol4.answer
    print("✓ PASSED (slope is -3, not 8)")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_all_templates():
    """Test all 5 templates for Confuse-Slope-And-Intercept-Roles."""
    print("\n\n" + "="*70)
    print("TESTING ALL TEMPLATES")
    print("="*70)

    problem_gen = ConfuseSlopeAndInterceptRolesProblemGenerator(
        level=8,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = ConfuseSlopeAndInterceptRolesMalrule()
    correct = SlopeInterceptCorrectAlgorithm()

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

    problem_gen = ConfuseSlopeAndInterceptRolesProblemGenerator(
        level=8,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = ConfuseSlopeAndInterceptRolesMalrule()
    correct = SlopeInterceptCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Confuse-Slope-And-Intercept-Roles  ".center(70) + "║")
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
