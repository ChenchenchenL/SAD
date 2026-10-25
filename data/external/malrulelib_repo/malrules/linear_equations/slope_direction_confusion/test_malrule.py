#!/usr/bin/env python3
"""Test script for Slope-Direction-Confusion malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.linear_equations.slope_direction_confusion import (
    SlopeDirectionConfusionProblemGenerator,
    SlopeDirectionConfusionMalrule,
    SlopeDirectionCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING SLOPE-DIRECTION-CONFUSION")
    print("="*70)

    malrule = SlopeDirectionConfusionMalrule()
    correct = SlopeDirectionCorrectAlgorithm()

    # Test case 1: Negative slope -2 (classic example)
    problem1 = Problem(
        text="Describe the direction of a line with slope -2. Is the line increasing or decreasing from left to right?",
        operands=[-2],
        operation='describe_slope_direction',
        level=8,
        difficulty=DifficultyLevel.EASY,
        metadata={
            'slope': -2,
            'correct_direction': 'decreasing',
            'malrule_direction': 'increasing',
            'correct_description': 'going down from left to right',
            'malrule_description': 'going up from left to right',
            'template': 'basic_negative_slope'
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: Slope=-2 → Correct: {correct_sol.answer}, Malrule: {malrule_sol.answer}")
    assert correct_sol.answer == 'decreasing'
    assert malrule_sol.answer == 'increasing'
    assert correct_sol.answer != malrule_sol.answer
    print("✓ PASSED (decreasing, not increasing)")

    # Test case 2: Positive slope 3
    problem2 = Problem(
        text="Describe the direction of a line with slope 3. Is the line increasing or decreasing from left to right?",
        operands=[3],
        operation='describe_slope_direction',
        level=8,
        difficulty=DifficultyLevel.EASY,
        metadata={
            'slope': 3,
            'correct_direction': 'increasing',
            'malrule_direction': 'decreasing',
            'correct_description': 'going up from left to right',
            'malrule_description': 'going down from left to right',
            'template': 'basic_positive_slope'
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)

    print(f"\nTEST 2: Slope=3 → Correct: {correct_sol2.answer}, Malrule: {malrule_sol2.answer}")
    assert correct_sol2.answer == 'increasing'
    assert malrule_sol2.answer == 'decreasing'
    assert correct_sol2.answer != malrule_sol2.answer
    print("✓ PASSED (increasing, not decreasing)")

    # Test case 3: Larger negative slope -5
    problem3 = Problem(
        text="Describe the direction of a line with slope -5. Is the line increasing or decreasing from left to right?",
        operands=[-5],
        operation='describe_slope_direction',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'slope': -5,
            'correct_direction': 'decreasing',
            'malrule_direction': 'increasing',
            'correct_description': 'going down from left to right',
            'malrule_description': 'going up from left to right',
            'template': 'basic_negative_slope'
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)

    print(f"\nTEST 3: Slope=-5 → Correct: {correct_sol3.answer}, Malrule: {malrule_sol3.answer}")
    assert correct_sol3.answer == 'decreasing'
    assert malrule_sol3.answer == 'increasing'
    assert correct_sol3.answer != malrule_sol3.answer
    print("✓ PASSED (decreasing, not increasing)")

    # Test case 4: Larger positive slope 7
    problem4 = Problem(
        text="Describe the direction of a line with slope 7. Is the line increasing or decreasing from left to right?",
        operands=[7],
        operation='describe_slope_direction',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'slope': 7,
            'correct_direction': 'increasing',
            'malrule_direction': 'decreasing',
            'correct_description': 'going up from left to right',
            'malrule_description': 'going down from left to right',
            'template': 'larger_magnitude'
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)

    print(f"\nTEST 4: Slope=7 → Correct: {correct_sol4.answer}, Malrule: {malrule_sol4.answer}")
    assert correct_sol4.answer == 'increasing'
    assert malrule_sol4.answer == 'decreasing'
    assert correct_sol4.answer != malrule_sol4.answer
    print("✓ PASSED (increasing, not decreasing)")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_all_templates():
    """Test all 6 problem templates."""
    print("\n\n" + "="*70)
    print("TESTING ALL TEMPLATES")
    print("="*70)

    problem_gen = SlopeDirectionConfusionProblemGenerator(
        level=8,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = SlopeDirectionConfusionMalrule()
    correct = SlopeDirectionCorrectAlgorithm()

    templates = problem_gen.get_available_templates()
    print(f"\nFound {len(templates)} templates: {templates}")

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

    problem_gen = SlopeDirectionConfusionProblemGenerator(
        level=8,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = SlopeDirectionConfusionMalrule()
    correct = SlopeDirectionCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Slope-Direction-Confusion  ".center(70) + "║")
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
