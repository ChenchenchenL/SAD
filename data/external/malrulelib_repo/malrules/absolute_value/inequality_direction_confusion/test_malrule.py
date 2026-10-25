#!/usr/bin/env python3
"""Test script for Inequality-Direction-Confusion malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.absolute_value.inequality_direction_confusion import (
    InequalityDirectionConfusionProblemGenerator,
    InequalityDirectionConfusionMalrule,
    AbsoluteValueInequalityCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING INEQUALITY-DIRECTION-CONFUSION")
    print("="*70)

    malrule = InequalityDirectionConfusionMalrule()
    correct = AbsoluteValueInequalityCorrectAlgorithm()

    # Test case 1: |x| > 3 (greater than - should give two regions)
    # Correct: x < -3 OR x > 3
    # Student (malrule): -3 < x < 3 (applies less-than pattern)
    problem1 = Problem(
        text="Solve: |x| > 3",
        operands=[3],
        operation='absolute_value_inequality',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'bound': 3,
            'inequality_type': 'greater_than',
            'correct_answer': 'x < -3 OR x > 3',
            'malrule_answer': '-3 < x < 3'
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: |x| > 3 → Correct: {correct_sol.answer}, Malrule: {malrule_sol.answer}")
    assert correct_sol.answer == 'x < -3 OR x > 3'
    assert malrule_sol.answer == '-3 < x < 3'
    assert correct_sol.answer != malrule_sol.answer
    print("✓ PASSED")

    # Test case 2: |x| < 5 (less than - should give three-part)
    # Correct: -5 < x < 5
    # Student (malrule): x < -5 OR x > 5 (applies greater-than pattern)
    problem2 = Problem(
        text="Solve: |x| < 5",
        operands=[5],
        operation='absolute_value_inequality',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'bound': 5,
            'inequality_type': 'less_than',
            'correct_answer': '-5 < x < 5',
            'malrule_answer': 'x < -5 OR x > 5'
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert correct_sol2.answer == '-5 < x < 5'
    assert malrule_sol2.answer == 'x < -5 OR x > 5'
    print("✓ TEST 2 PASSED")

    # Test case 3: |x| > 7 (greater than)
    # Correct: x < -7 OR x > 7
    # Student (malrule): -7 < x < 7
    problem3 = Problem(
        text="Solve: |x| > 7",
        operands=[7],
        operation='absolute_value_inequality',
        level=9,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'bound': 7,
            'inequality_type': 'greater_than',
            'correct_answer': 'x < -7 OR x > 7',
            'malrule_answer': '-7 < x < 7'
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert correct_sol3.answer == 'x < -7 OR x > 7'
    assert malrule_sol3.answer == '-7 < x < 7'
    print("✓ TEST 3 PASSED")

    # Test case 4: |x| < 2 (less than)
    # Correct: -2 < x < 2
    # Student (malrule): x < -2 OR x > 2
    problem4 = Problem(
        text="Solve: |x| < 2",
        operands=[2],
        operation='absolute_value_inequality',
        level=9,
        difficulty=DifficultyLevel.EASY,
        metadata={
            'bound': 2,
            'inequality_type': 'less_than',
            'correct_answer': '-2 < x < 2',
            'malrule_answer': 'x < -2 OR x > 2'
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    assert correct_sol4.answer == '-2 < x < 2'
    assert malrule_sol4.answer == 'x < -2 OR x > 2'
    print("✓ TEST 4 PASSED")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_new_problem_templates():
    """Test new problem template types added for enhancement."""
    print("\n" + "="*70)
    print("TESTING NEW PROBLEM TEMPLATES")
    print("="*70)

    malrule = InequalityDirectionConfusionMalrule()
    correct = AbsoluteValueInequalityCorrectAlgorithm()

    # TEST CASE 5: Compound inequality |x - h| < k
    # Correct: 1 < x < 9  (since 5-4 < x < 5+4)
    # Malrule: x < 1 OR x > 9 (applies greater than pattern)
    problem5 = Problem(
        text="Solve: |x - 5| < 4",
        operands=[4],
        operation='absolute_value_inequality',
        level=9,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'bound': 4,
            'offset': 5,
            'inequality_type': 'less_than',
            'problem_type': 'compound_inequality',
            'correct_answer': '1 < x < 9',
            'malrule_answer': 'x < 1 OR x > 9'
        }
    )

    correct_sol5 = correct.solve(problem5)
    malrule_sol5 = malrule.solve(problem5)

    print(f"\nTEST 5: |x - 5| < 4 → Correct: {correct_sol5.answer}, Malrule: {malrule_sol5.answer}")
    assert correct_sol5.answer == '1 < x < 9'
    assert malrule_sol5.answer == 'x < 1 OR x > 9'
    assert correct_sol5.answer != malrule_sol5.answer
    print("✓ PASSED")

    # TEST CASE 6: Inequality with coefficient |2x| > 6
    # Correct: x < -3 OR x > 3
    # Malrule: -3 < x < 3 (applies less than pattern)
    problem6 = Problem(
        text="Solve: |2x| > 6",
        operands=[6],
        operation='absolute_value_inequality',
        level=9,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'coefficient': 2,
            'bound': 6,
            'inequality_type': 'greater_than',
            'problem_type': 'inequality_with_coefficient',
            'correct_answer': 'x < -3 OR x > 3',
            'malrule_answer': '-3 < x < 3'
        }
    )

    correct_sol6 = correct.solve(problem6)
    malrule_sol6 = malrule.solve(problem6)

    print(f"TEST 6: |2x| > 6 → Correct: {correct_sol6.answer}, Malrule: {malrule_sol6.answer}")
    assert correct_sol6.answer == 'x < -3 OR x > 3'
    assert malrule_sol6.answer == '-3 < x < 3'
    print("✓ PASSED")

    # TEST CASE 7: Less than or equal |x| ≤ 4
    # Correct: -4 ≤ x ≤ 4
    # Malrule: x ≤ -4 OR x ≥ 4 (applies greater than pattern)
    problem7 = Problem(
        text="Solve: |x| ≤ 4",
        operands=[4],
        operation='absolute_value_inequality',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'bound': 4,
            'inequality_type': 'less_than',
            'problem_type': 'less_than_or_equal',
            'correct_answer': '-4 ≤ x ≤ 4',
            'malrule_answer': 'x ≤ -4 OR x ≥ 4'
        }
    )

    correct_sol7 = correct.solve(problem7)
    malrule_sol7 = malrule.solve(problem7)

    print(f"TEST 7: |x| ≤ 4 → Correct: {correct_sol7.answer}, Malrule: {malrule_sol7.answer}")
    assert correct_sol7.answer == '-4 ≤ x ≤ 4'
    assert malrule_sol7.answer == 'x ≤ -4 OR x ≥ 4'
    print("✓ PASSED")

    # TEST CASE 8: Word problem context
    # Correct: -3 < x < 3
    # Malrule: x < -3 OR x > 3 (applies greater than pattern)
    problem8 = Problem(
        text="The distance between two points must be less than 3 units. If one point is at the origin, write an inequality for the position x of the other point.",
        operands=[3],
        operation='absolute_value_inequality',
        level=9,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'bound': 3,
            'inequality_type': 'less_than',
            'problem_type': 'word_problem_context',
            'symbolic_form': '|x| < 3',
            'correct_answer': '-3 < x < 3',
            'malrule_answer': 'x < -3 OR x > 3',
            'context': 'word_problem'
        }
    )

    correct_sol8 = correct.solve(problem8)
    malrule_sol8 = malrule.solve(problem8)

    print(f"TEST 8: Word problem → Correct: {correct_sol8.answer}, Malrule: {malrule_sol8.answer}")
    assert correct_sol8.answer == '-3 < x < 3'
    assert malrule_sol8.answer == 'x < -3 OR x > 3'
    print("✓ PASSED")

    print("\n" + "="*70)
    print("ALL NEW TEMPLATE TESTS PASSED ✓")
    print("="*70)


def test_all_templates():
    """Test all problem templates with detailed output."""
    print("\n" + "="*70)
    print("TESTING ALL PROBLEM TEMPLATES")
    print("="*70)

    problem_gen = InequalityDirectionConfusionProblemGenerator(
        level=10,
        difficulty=DifficultyLevel.HARD
    )
    malrule = InequalityDirectionConfusionMalrule()
    correct = AbsoluteValueInequalityCorrectAlgorithm()

    # Expected templates for inequality_direction_confusion
    expected_templates = {
        'less_than', 'greater_than',
        'compound_inequality', 'inequality_with_coefficient',
        'less_than_or_equal', 'word_problem_context'
    }

    templates_tested = set()
    failed_tests = []

    # Generate and test problems until we've covered all templates
    for seed in range(1000):
        problem = problem_gen.generate(seed=60000 + seed)
        problem_type = problem.metadata.get('problem_type', 'less_than')

        # Skip if we've already tested this template
        if problem_type in templates_tested:
            continue

        templates_tested.add(problem_type)
        print(f"\n{'='*70}")
        print(f"Testing template: {problem_type}")
        print(f"{'='*70}")
        print(f"Problem: {problem.text}")

        try:
            # Solve with both algorithms
            correct_sol = correct.solve(problem)
            malrule_sol = malrule.solve(problem)

            print(f"\nCorrect answer: {correct_sol.answer}")
            print(f"Malrule answer: {malrule_sol.answer}")

            # Check that answers are different (misconception produces different result)
            if correct_sol.answer == malrule_sol.answer:
                print("\n⚠ WARNING: Misconception produces same answer as correct!")
                print("\nCorrect algorithm steps:")
                for step in correct_sol.steps:
                    print(f"  {step}")
                print("\nMalrule algorithm steps:")
                for step in malrule_sol.steps:
                    print(f"  {step}")
                failed_tests.append((problem_type, "Same answer"))
                print(f"✗ FAILED: {problem_type}")
            else:
                print(f"✓ PASSED: {problem_type}")

        except Exception as e:
            print(f"\n✗ EXCEPTION in {problem_type}: {e}")
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

            failed_tests.append((problem_type, str(e)))
            import traceback
            traceback.print_exc()

        # Break if we've tested all templates
        if templates_tested >= expected_templates:
            break

    print(f"\n{'='*70}")
    print("TEMPLATE COVERAGE SUMMARY")
    print(f"{'='*70}")
    print(f"Expected templates: {expected_templates}")
    print(f"Tested templates: {templates_tested}")

    missing = expected_templates - templates_tested
    if missing:
        print(f"⚠ Missing templates: {missing}")

    if failed_tests:
        print(f"\n✗ FAILED TESTS: {len(failed_tests)}")
        for template, reason in failed_tests:
            print(f"  - {template}: {reason}")
        raise AssertionError(f"Failed {len(failed_tests)} template tests")
    else:
        print(f"\n✓ ALL {len(templates_tested)} TEMPLATES PASSED")

    print(f"\n{'='*70}")
    print("TEMPLATE TEST COMPLETE")
    print(f"{'='*70}")


def test_automated_suite():
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = InequalityDirectionConfusionProblemGenerator(
        level=9,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = InequalityDirectionConfusionMalrule()
    correct = AbsoluteValueInequalityCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Inequality-Direction-Confusion  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    try:
        test_specific_examples()
        test_new_problem_templates()
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
