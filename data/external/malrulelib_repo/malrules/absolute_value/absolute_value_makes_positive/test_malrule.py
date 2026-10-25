#!/usr/bin/env python3
"""Test script for Absolute-Value-Makes-Positive malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.absolute_value.absolute_value_makes_positive import (
    AbsoluteValueMakesPositiveProblemGenerator,
    AbsoluteValueMakesPositiveMalrule,
    AbsoluteValueEquationCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING ABSOLUTE-VALUE-MAKES-POSITIVE")
    print("="*70)

    malrule = AbsoluteValueMakesPositiveMalrule()
    correct = AbsoluteValueEquationCorrectAlgorithm()

    # Test case 1: |x| = -3 → Correct: No solution, Malrule: x = 3
    problem1 = Problem(
        text="Solve: |x| = -3",
        operands=[-3],
        operation='absolute_value_equation',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'negative_value': -3,
            'correct_answer': 'No solution',
            'malrule_answer': 'x = 3'
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: |x| = -3 → Correct: {correct_sol.answer}, Malrule: {malrule_sol.answer}")
    assert correct_sol.answer == 'No solution'
    assert malrule_sol.answer == 'x = 3'
    assert correct_sol.answer != malrule_sol.answer
    print("✓ PASSED")

    # Test case 2: |x| = -5 → Correct: No solution, Malrule: x = 5
    problem2 = Problem(
        text="Solve: |x| = -5",
        operands=[-5],
        operation='absolute_value_equation',
        level=7,
        difficulty=DifficultyLevel.EASY,
        metadata={
            'negative_value': -5,
            'correct_answer': 'No solution',
            'malrule_answer': 'x = 5'
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert correct_sol2.answer == 'No solution'
    assert malrule_sol2.answer == 'x = 5'
    print("✓ TEST 2 PASSED")

    # Test case 3: |x| = -1 → Correct: No solution, Malrule: x = 1
    problem3 = Problem(
        text="Solve: |x| = -1",
        operands=[-1],
        operation='absolute_value_equation',
        level=7,
        difficulty=DifficultyLevel.EASY,
        metadata={
            'negative_value': -1,
            'correct_answer': 'No solution',
            'malrule_answer': 'x = 1'
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert correct_sol3.answer == 'No solution'
    assert malrule_sol3.answer == 'x = 1'
    print("✓ TEST 3 PASSED")

    # Test case 4: |x| = -10 → Correct: No solution, Malrule: x = 10
    problem4 = Problem(
        text="Solve: |x| = -10",
        operands=[-10],
        operation='absolute_value_equation',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'negative_value': -10,
            'correct_answer': 'No solution',
            'malrule_answer': 'x = 10'
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    assert correct_sol4.answer == 'No solution'
    assert malrule_sol4.answer == 'x = 10'
    print("✓ TEST 4 PASSED")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_all_templates():
    """Test all 5 problem templates with detailed output."""
    print("\n\n" + "="*70)
    print("TESTING ALL PROBLEM TEMPLATES")
    print("="*70)

    problem_gen = AbsoluteValueMakesPositiveProblemGenerator(
        level=8,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = AbsoluteValueMakesPositiveMalrule()
    correct = AbsoluteValueEquationCorrectAlgorithm()

    templates = problem_gen.get_available_templates()
    expected_count = 5
    assert len(templates) == expected_count, f"Expected {expected_count} templates, found {len(templates)}"

    failed_tests = []

    for template in templates:
        print(f"\n{'='*70}")
        print(f"Testing template: {template}")
        print(f"{'='*70}")

        try:
            problem = problem_gen.generate(seed=42, template=template)
            print(f"Problem: {problem.text}")

            # Solve with both algorithms
            correct_sol = correct.solve(problem)
            malrule_sol = malrule.solve(problem)

            print(f"\nCorrect answer: {correct_sol.answer}")
            print(f"Malrule answer: {malrule_sol.answer}")

            # Verify calculate_expected_answer matches malrule answer
            expected = malrule.calculate_expected_answer(problem)
            if str(malrule_sol.answer) != str(expected):
                print(f"\n⚠ WARNING: calculate_expected_answer() mismatch!")
                print(f"Expected: {expected}")
                print(f"Actual: {malrule_sol.answer}")
                failed_tests.append((template, "Expected answer mismatch"))
                print(f"✗ FAILED: {template}")
                continue

            # Check that answers are different
            if correct_sol.answer == malrule_sol.answer:
                print("\n⚠ WARNING: Misconception produces same answer as correct!")
                print("\nCorrect algorithm steps:")
                for step in correct_sol.steps:
                    print(f"  {step}")
                print("\nMalrule algorithm steps:")
                for step in malrule_sol.steps:
                    print(f"  {step}")
                failed_tests.append((template, "Same answer"))
                print(f"✗ FAILED: {template}")
            else:
                print(f"✓ PASSED: {template}")

        except Exception as e:
            print(f"\n✗ EXCEPTION in {template}: {e}")
            print("\nCorrect algorithm steps:")
            try:
                correct_sol = correct.solve(problem)
                for step in correct_sol.steps:
                    print(f"  {step}")
            except:
                print("  Failed to generate steps")

            print("\nMalrule algorithm steps:")
            try:
                malrule_sol = malrule.solve(problem)
                for step in malrule_sol.steps:
                    print(f"  {step}")
            except:
                print("  Failed to generate steps")

            failed_tests.append((template, str(e)))
            import traceback
            traceback.print_exc()

    print(f"\n{'='*70}")
    print("TEMPLATE TEST SUMMARY")
    print(f"{'='*70}")

    if failed_tests:
        print(f"✗ FAILED TESTS: {len(failed_tests)}")
        for template, reason in failed_tests:
            print(f"  - {template}: {reason}")
        raise AssertionError(f"Failed {len(failed_tests)} template tests")
    else:
        print(f"✓ ALL {len(templates)} TEMPLATES PASSED")

    print(f"\n{'='*70}")
    print("TEMPLATE TEST COMPLETE")
    print(f"{'='*70}")


def test_automated_suite():
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = AbsoluteValueMakesPositiveProblemGenerator(
        level=8,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = AbsoluteValueMakesPositiveMalrule()
    correct = AbsoluteValueEquationCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Absolute-Value-Makes-Positive  ".center(70) + "║")
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
