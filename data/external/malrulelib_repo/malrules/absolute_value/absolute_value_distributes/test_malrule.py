#!/usr/bin/env python3
"""Test script for Absolute-Value-Distributes malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.absolute_value.absolute_value_distributes import (
    AbsoluteValueDistributesProblemGenerator,
    AbsoluteValueDistributesMalrule,
    AbsoluteValueCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING ABSOLUTE-VALUE-DISTRIBUTES")
    print("="*70)

    malrule = AbsoluteValueDistributesMalrule()
    correct = AbsoluteValueCorrectAlgorithm()

    # Test case 1: |-3 + 5| = |2| = 2 (correct), |-3| + 5 = 8 (malrule)
    problem1 = Problem(
        text="Evaluate |x + 5| when x = -3",
        operands=[-3, 5],
        operation='absolute_value',
        level=8,
        difficulty=DifficultyLevel.EASY,
        metadata={
            'x_value': -3,
            'constant': 5,
            'operation': '+',
            'expression': 'x + 5',
            'expression_value': 2,
            'correct_answer': 2,
            'malrule_answer': 8,
            'template': 'basic_addition'
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: |-3 + 5| → Correct: {correct_sol.answer}, Malrule: {malrule_sol.answer}")
    assert str(correct_sol.answer) == '2'
    assert str(malrule_sol.answer) == '8'
    assert correct_sol.answer != malrule_sol.answer
    print("✓ PASSED")

    # Test case 2: |4 - 7| = |-3| = 3 (correct), |4| - 7 = -3 (malrule)
    problem2 = Problem(
        text="Evaluate |x - 7| when x = 4",
        operands=[4, 7],
        operation='absolute_value',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'x_value': 4,
            'constant': 7,
            'operation': '-',
            'expression': 'x - 7',
            'expression_value': -3,
            'correct_answer': 3,
            'malrule_answer': -3
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert str(correct_sol2.answer) == '3'
    assert str(malrule_sol2.answer) == '-3'
    print("✓ TEST 2 PASSED")

    # Test case 3: |-5 + 2| = |-3| = 3 (correct), |-5| + 2 = 7 (malrule)
    problem3 = Problem(
        text="Evaluate |x + 2| when x = -5",
        operands=[-5, 2],
        operation='absolute_value',
        level=7,
        difficulty=DifficultyLevel.EASY,
        metadata={
            'x_value': -5,
            'constant': 2,
            'operation': '+',
            'expression': 'x + 2',
            'expression_value': -3,
            'correct_answer': 3,
            'malrule_answer': 7
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert str(correct_sol3.answer) == '3'
    assert str(malrule_sol3.answer) == '7'
    print("✓ TEST 3 PASSED")

    # Test case 4: |6 - 10| = |-4| = 4 (correct), |6| - 10 = -4 (malrule)
    problem4 = Problem(
        text="Evaluate |x - 10| when x = 6",
        operands=[6, 10],
        operation='absolute_value',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'x_value': 6,
            'constant': 10,
            'operation': '-',
            'expression': 'x - 10',
            'expression_value': -4,
            'correct_answer': 4,
            'malrule_answer': -4
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    assert str(correct_sol4.answer) == '4'
    assert str(malrule_sol4.answer) == '-4'
    print("✓ TEST 4 PASSED")

    # Test case 5: Word problem x_plus_c type
    problem5 = Problem(
        text="The temperature is x degrees, and it increases by 3 degrees. The absolute difference from zero is |x + 3|. If x = -5, what is the absolute temperature?",
        operands=[-5, 3],
        operation='absolute_value',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'x_value': -5,
            'constant': 3,
            'operation': '+',
            'expression': 'x + 3',
            'expression_value': -2,
            'correct_answer': '2 degrees',
            'malrule_answer': '8 degrees',
            'context_type': 'temperature',
            'template': 'word_problem',
            'word_problem_type': 'x_plus_c'
        }
    )

    correct_sol5 = correct.solve(problem5)
    malrule_sol5 = malrule.solve(problem5)
    print(f"\nTEST 5: Word problem (x+c) → Correct: {correct_sol5.answer}, Malrule: {malrule_sol5.answer}")
    assert correct_sol5.answer != malrule_sol5.answer
    print("✓ TEST 5 PASSED")

    # Test case 6: Word problem x_minus_c type
    problem6 = Problem(
        text="A drone is at position x meters, and moves 4 meters to the left. The distance from the origin is |x - 4|. If x = 2, what is the distance from the origin?",
        operands=[2, 4],
        operation='absolute_value',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'x_value': 2,
            'constant': 4,
            'operation': '-',
            'expression': 'x - 4',
            'expression_value': -2,
            'correct_answer': '2 meters',
            'malrule_answer': '-2 meters',
            'context_type': 'distance',
            'template': 'word_problem',
            'word_problem_type': 'x_minus_c'
        }
    )

    correct_sol6 = correct.solve(problem6)
    malrule_sol6 = malrule.solve(problem6)
    print(f"\nTEST 6: Word problem (x-c) → Correct: {correct_sol6.answer}, Malrule: {malrule_sol6.answer}")
    assert correct_sol6.answer != malrule_sol6.answer
    print("✓ TEST 6 PASSED")

    # Test case 7: Word problem ax_plus_b type
    problem7 = Problem(
        text="A factory produces x items per hour for 3 hours, plus 2 bonus items. The total production is |3x + 2|. If x = -2, what is the absolute total production?",
        operands=[-2, 3, 2],
        operation='absolute_value',
        level=8,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'x_value': -2,
            'coefficient': 3,
            'constant': 2,
            'operation': '+',
            'expression': '3x + 2',
            'expression_value': -4,
            'correct_answer': '4 items',
            'malrule_answer': '8 items',
            'context_type': 'production',
            'template': 'word_problem',
            'word_problem_type': 'ax_plus_b'
        }
    )

    correct_sol7 = correct.solve(problem7)
    malrule_sol7 = malrule.solve(problem7)
    print(f"\nTEST 7: Word problem (ax+b) → Correct: {correct_sol7.answer}, Malrule: {malrule_sol7.answer}")
    assert correct_sol7.answer != malrule_sol7.answer
    print("✓ TEST 7 PASSED")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_all_templates():
    """Test all problem templates with detailed output."""
    print("\n\n" + "="*70)
    print("TESTING ALL PROBLEM TEMPLATES")
    print("="*70)

    problem_gen = AbsoluteValueDistributesProblemGenerator(
        level=8,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = AbsoluteValueDistributesMalrule()
    correct = AbsoluteValueCorrectAlgorithm()

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

            # Check that answers are different (unless the expression inside evaluates to same as distributed)
            # Note: In rare edge cases, distributing might accidentally give the same answer
            if correct_sol.answer == malrule_sol.answer:
                print("\n⚠ WARNING: Misconception produces same answer as correct!")
                print("This can happen in edge cases (e.g., x=0 or certain values)")
                print("\nCorrect algorithm steps:")
                for step in correct_sol.steps:
                    print(f"  {step}")
                print("\nMalrule algorithm steps:")
                for step in malrule_sol.steps:
                    print(f"  {step}")
                # Don't fail on edge cases for this malrule since it's mathematically possible
                print(f"⚠ WARNING (not a failure): {template}")
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

    problem_gen = AbsoluteValueDistributesProblemGenerator(
        level=8,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = AbsoluteValueDistributesMalrule()
    correct = AbsoluteValueCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Absolute-Value-Distributes  ".center(70) + "║")
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
