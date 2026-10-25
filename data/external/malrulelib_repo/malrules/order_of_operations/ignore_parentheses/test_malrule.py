#!/usr/bin/env python3
"""Test script for Ignore-Parentheses malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.order_of_operations.ignore_parentheses import (
    IgnoreParenthesesProblemGenerator,
    IgnoreParenthesesMalrule,
    OrderOfOperationsCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING IGNORE-PARENTHESES WITH SPECIFIC EXAMPLES")
    print("="*70)

    malrule = IgnoreParenthesesMalrule()
    correct = OrderOfOperationsCorrectAlgorithm()

    # Test case 1: 2 × (3 + 4) = 14
    print("\nTEST CASE 1: 2 × (3 + 4)")
    print("-"*70)

    problem1 = Problem(
        text="Calculate: 2 × (3 + 4)",
        operands=[2, 3, 4],
        operation='order_of_operations',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'expression': '2 × (3 + 4)',
            'a': 2, 'b': 3, 'c': 4,
            'op1': '×', 'op2': '+',
            'correct_answer': 14,
            'paren_result': 7
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"Correct: {correct_sol.answer}, Malrule: {malrule_sol.answer}")
    assert correct_sol.answer == 14
    assert correct_sol.answer != malrule_sol.answer

    print("✓ TEST CASE 1 PASSED")

    # Test case 2: 10 - (3 + 2) = 5
    problem2 = Problem(
        text="Calculate: 10 - (3 + 2)",
        operands=[10, 3, 2],
        operation='order_of_operations',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'expression': '10 - (3 + 2)',
            'a': 10, 'b': 3, 'c': 2,
            'op1': '-', 'op2': '+',
            'correct_answer': 5,
            'paren_result': 5
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert correct_sol2.answer == 5

    print("\n✓ TEST CASE 2 PASSED")

    # Test case 3: 3 + (4 × 2) = 11
    problem3 = Problem(
        text="Calculate: 3 + (4 × 2)",
        operands=[3, 4, 2],
        operation='order_of_operations',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'expression': '3 + (4 × 2)',
            'a': 3, 'b': 4, 'c': 2,
            'op1': '+', 'op2': '×',
            'correct_answer': 11,
            'paren_result': 8
        }
    )

    correct_sol3 = correct.solve(problem3)
    assert correct_sol3.answer == 11

    print("✓ TEST CASE 3 PASSED")

    # Test case 4: 20 ÷ (2 + 3) = 4
    problem4 = Problem(
        text="Calculate: 20 ÷ (2 + 3)",
        operands=[20, 2, 3],
        operation='order_of_operations',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'expression': '20 ÷ (2 + 3)',
            'a': 20, 'b': 2, 'c': 3,
            'op1': '÷', 'op2': '+',
            'correct_answer': 4,
            'paren_result': 5
        }
    )

    correct_sol4 = correct.solve(problem4)
    assert correct_sol4.answer == 4

    print("✓ TEST CASE 4 PASSED")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_all_templates():
    """Test all available templates with detailed output."""
    print("\n" + "="*70)
    print("TESTING ALL TEMPLATES")
    print("="*70)

    malrule = IgnoreParenthesesMalrule()
    correct = OrderOfOperationsCorrectAlgorithm()

    # Get all templates from problem generator
    problem_gen = IgnoreParenthesesProblemGenerator(
        level=6,
        difficulty=DifficultyLevel.MEDIUM
    )
    templates = problem_gen.get_available_templates()

    all_passed = True
    failed_tests = []

    for template in templates:
        print(f"\n{'='*70}")
        print(f"TEMPLATE: {template}")
        print(f"{'='*70}")

        template_passed = True

        # Generate multiple problems for this template
        for i in range(3):
            try:
                problem = problem_gen.generate(seed=2000 + i, template=template)

                correct_sol = correct.solve(problem)
                malrule_sol = malrule.solve(problem)

                # Check if answers are the same (edge case)
                if abs(correct_sol.answer - malrule_sol.answer) < 0.01:
                    print(f"\n⚠ WARNING: Test {i+1} - Answers are the same (edge case)")
                    print(f"Problem: {problem.text}")
                    print(f"Expression: {problem.metadata['expression']}")
                    print(f"\nCorrect algorithm steps:")
                    for step in correct_sol.steps:
                        print(f"  {step}")
                    print(f"\nMalrule algorithm steps:")
                    for step in malrule_sol.steps:
                        print(f"  {step}")
                    print(f"\nBoth produced answer: {correct_sol.answer}")

                    # This is an edge case - fail the test
                    failed_tests.append({
                        'template': template,
                        'problem': problem.text,
                        'expression': problem.metadata['expression'],
                        'reason': 'Edge case: misconception produces same answer as correct'
                    })
                    template_passed = False
                    all_passed = False
                    continue

                # Verify calculate_expected_answer matches malrule solution
                expected_malrule_answer = malrule.calculate_expected_answer(problem)
                if abs(expected_malrule_answer - malrule_sol.answer) > 0.01:
                    print(f"\n✗ Test {i+1} FAILED")
                    print(f"Problem: {problem.text}")
                    print(f"Expression: {problem.metadata['expression']}")
                    print(f"Expected malrule answer: {expected_malrule_answer}")
                    print(f"Actual malrule answer: {malrule_sol.answer}")
                    print(f"\nMalrule algorithm steps:")
                    for step in malrule_sol.steps:
                        print(f"  {step}")

                    failed_tests.append({
                        'template': template,
                        'problem': problem.text,
                        'expression': problem.metadata['expression'],
                        'reason': f'Malrule answer mismatch: expected {expected_malrule_answer}, got {malrule_sol.answer}'
                    })
                    template_passed = False
                    all_passed = False
                    continue

                # Test passed
                print(f"\n✓ Test {i+1} PASSED")
                print(f"Problem: {problem.text[:60]}...")
                print(f"Expression: {problem.metadata['expression']}")
                print(f"Correct answer: {correct_sol.answer}")
                print(f"Malrule answer: {malrule_sol.answer}")

            except Exception as e:
                print(f"\n✗ Test {i+1} FAILED with exception: {e}")
                import traceback
                traceback.print_exc()

                failed_tests.append({
                    'template': template,
                    'problem': 'N/A',
                    'expression': 'N/A',
                    'reason': f'Exception: {e}'
                })
                template_passed = False
                all_passed = False

        if template_passed:
            print(f"\n✓✓✓ Template {template} - ALL TESTS PASSED")
        else:
            print(f"\n✗✗✗ Template {template} - SOME TESTS FAILED")

    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")

    if all_passed:
        print("✓✓✓ ALL TEMPLATE TESTS PASSED ✓✓✓")
    else:
        print(f"✗✗✗ {len(failed_tests)} TEST(S) FAILED ✗✗✗")
        print("\nFailed tests:")
        for i, fail in enumerate(failed_tests, 1):
            print(f"\n{i}. Template: {fail['template']}")
            print(f"   Problem: {fail['problem']}")
            print(f"   Expression: {fail['expression']}")
            print(f"   Reason: {fail['reason']}")

        raise AssertionError(f"{len(failed_tests)} test(s) failed")

    return all_passed


def test_template_specific_cases():
    """Test specific cases for each template."""
    print("\n" + "="*70)
    print("TESTING TEMPLATE-SPECIFIC CASES")
    print("="*70)

    malrule = IgnoreParenthesesMalrule()
    correct = OrderOfOperationsCorrectAlgorithm()

    # Test case 1: nested_parentheses - 2 × (3 + (4 - 1))
    print("\nTEST: nested_parentheses - 2 × (3 + (4 - 1))")
    print("-"*70)
    problem1 = Problem(
        text="Calculate: 2 × (3 + (4 - 1))",
        operands=[2, 3, 4, 1],
        operation='order_of_operations',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'expression': '2 × (3 + (4 - 1))',
            'values': [2, 3, 4, 1],
            'operations': ['×', '+', '-'],
            'correct_answer': 12,  # 2 × (3 + 3) = 2 × 6 = 12
            'template': 'nested_parentheses'
        }
    )

    correct_sol1 = correct.solve(problem1)
    malrule_sol1 = malrule.solve(problem1)
    expected1 = malrule.calculate_expected_answer(problem1)

    print(f"Problem: {problem1.text}")
    print(f"Correct answer: {correct_sol1.answer}")
    print(f"Malrule answer: {malrule_sol1.answer}")
    print(f"Expected malrule: {expected1}")

    assert correct_sol1.answer == 12
    assert abs(expected1 - malrule_sol1.answer) < 0.01
    assert abs(correct_sol1.answer - malrule_sol1.answer) > 0.01
    print("✓ PASSED")

    # Test case 2: multiple_parentheses - (2 + 3) × (4 - 1)
    print("\nTEST: multiple_parentheses - (2 + 3) × (4 - 1)")
    print("-"*70)
    problem2 = Problem(
        text="Calculate: (2 + 3) × (4 - 1)",
        operands=[2, 3, 4, 1],
        operation='order_of_operations',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'expression': '(2 + 3) × (4 - 1)',
            'values': [2, 3, 4, 1],
            'operations': ['+', '×', '-'],
            'correct_answer': 15,  # 5 × 3 = 15
            'template': 'multiple_parentheses'
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    expected2 = malrule.calculate_expected_answer(problem2)

    print(f"Problem: {problem2.text}")
    print(f"Correct answer: {correct_sol2.answer}")
    print(f"Malrule answer: {malrule_sol2.answer}")
    print(f"Expected malrule: {expected2}")

    assert correct_sol2.answer == 15
    assert abs(expected2 - malrule_sol2.answer) < 0.01
    assert abs(correct_sol2.answer - malrule_sol2.answer) > 0.01
    print("✓ PASSED")

    # Test case 3: brackets_and_parentheses - 2 × [3 + (4 - 1)]
    print("\nTEST: brackets_and_parentheses - 2 × [3 + (4 - 1)]")
    print("-"*70)
    problem3 = Problem(
        text="Calculate: 2 × [3 + (4 - 1)]",
        operands=[2, 3, 4, 1],
        operation='order_of_operations',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'expression': '2 × [3 + (4 - 1)]',
            'values': [2, 3, 4, 1],
            'operations': ['×', '+', '-'],
            'correct_answer': 12,  # 2 × [3 + 3] = 2 × 6 = 12
            'template': 'brackets_and_parentheses'
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    expected3 = malrule.calculate_expected_answer(problem3)

    print(f"Problem: {problem3.text}")
    print(f"Correct answer: {correct_sol3.answer}")
    print(f"Malrule answer: {malrule_sol3.answer}")
    print(f"Expected malrule: {expected3}")

    assert correct_sol3.answer == 12
    assert abs(expected3 - malrule_sol3.answer) < 0.01
    assert abs(correct_sol3.answer - malrule_sol3.answer) > 0.01
    print("✓ PASSED")

    print("\n" + "="*70)
    print("ALL TEMPLATE-SPECIFIC TESTS PASSED ✓")
    print("="*70)


def test_automated_suite():
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = IgnoreParenthesesProblemGenerator(
        level=6,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = IgnoreParenthesesMalrule()
    correct = OrderOfOperationsCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)

    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    else:
        print("\n✗✗✗ SOME TESTS FAILED ✗✗✗")

    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Ignore-Parentheses  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    try:
        test_specific_examples()
        test_all_templates()
        test_template_specific_cases()
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
