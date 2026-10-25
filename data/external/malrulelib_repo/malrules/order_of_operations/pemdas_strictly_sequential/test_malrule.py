#!/usr/bin/env python3
"""Test script for PEMDAS-Strictly-Sequential malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.order_of_operations.pemdas_strictly_sequential import (
    PEMDASStrictlySequentialProblemGenerator,
    PEMDASStrictlySequentialMalrule,
    OrderOfOperationsCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING PEMDAS-STRICTLY-SEQUENTIAL")
    print("="*70)

    malrule = PEMDASStrictlySequentialMalrule()
    correct = OrderOfOperationsCorrectAlgorithm()

    # Test case 1: 6 ÷ 2 × 3 = 9 (left-to-right), malrule: 1 (M before D)
    problem1 = Problem(
        text="Calculate: 6 ÷ 2 × 3",
        operands=[6, 2, 3],
        operation='order_of_operations',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'expression': '6 ÷ 2 × 3',
            'correct_answer': 9,  # (6÷2)×3 = 3×3 = 9
            'malrule_answer': 1,  # 6÷(2×3) = 6÷6 = 1
            'problem_type': 'mult_div',
            'operator_sequence': '÷×'
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: 6 ÷ 2 × 3 → Correct: {correct_sol.answer}, Malrule: {malrule_sol.answer}")
    assert correct_sol.answer == 9
    assert malrule_sol.answer == 1
    assert correct_sol.answer != malrule_sol.answer
    print("✓ PASSED")

    # Test case 2: 10 - 3 + 2 = 9 (left-to-right), malrule: 5 (A before S)
    problem2 = Problem(
        text="Calculate: 10 - 3 + 2",
        operands=[10, 3, 2],
        operation='order_of_operations',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'expression': '10 - 3 + 2',
            'correct_answer': 9,  # (10-3)+2 = 7+2 = 9
            'malrule_answer': 5,  # 10-(3+2) = 10-5 = 5
            'problem_type': 'add_sub',
            'operator_sequence': '-+'
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert correct_sol2.answer == 9
    assert malrule_sol2.answer == 5
    print("✓ TEST 2 PASSED")

    # Test case 3: 8 ÷ 4 × 2 = 4 (left-to-right), malrule: 1 (M before D)
    problem3 = Problem(
        text="Calculate: 8 ÷ 4 × 2",
        operands=[8, 4, 2],
        operation='order_of_operations',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'expression': '8 ÷ 4 × 2',
            'correct_answer': 4,  # (8÷4)×2 = 2×2 = 4
            'malrule_answer': 1,  # 8÷(4×2) = 8÷8 = 1
            'problem_type': 'mult_div',
            'operator_sequence': '÷×'
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert correct_sol3.answer == 4
    assert malrule_sol3.answer == 1
    print("✓ TEST 3 PASSED")

    # Test case 4: 15 - 5 + 3 = 13 (left-to-right), malrule: 7 (A before S)
    problem4 = Problem(
        text="Calculate: 15 - 5 + 3",
        operands=[15, 5, 3],
        operation='order_of_operations',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'expression': '15 - 5 + 3',
            'correct_answer': 13,  # (15-5)+3 = 10+3 = 13
            'malrule_answer': 7,  # 15-(5+3) = 15-8 = 7
            'problem_type': 'add_sub',
            'operator_sequence': '-+'
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    assert correct_sol4.answer == 13
    assert malrule_sol4.answer == 7
    print("✓ TEST 4 PASSED")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_all_templates():
    """Test all available templates with comprehensive output."""
    print("\n" + "="*70)
    print("TESTING ALL TEMPLATES")
    print("="*70)

    malrule = PEMDASStrictlySequentialMalrule()
    correct = OrderOfOperationsCorrectAlgorithm()

    templates = [
        'basic_mult_div',
        'basic_add_sub',
        'longer_expressions',
        'mixed_operations',
        'word_problem'
    ]

    all_passed = True
    total_tests = 0
    failed_tests = 0

    for template in templates:
        print(f"\n{'─'*70}")
        print(f"Template: {template}")
        print(f"{'─'*70}")

        # Create problem generator for this template
        problem_gen = PEMDASStrictlySequentialProblemGenerator(
            level=7,
            difficulty=DifficultyLevel.MEDIUM
        )

        # Generate multiple problems for this template
        for i in range(5):
            total_tests += 1
            problem = problem_gen.generate(seed=3000 + i, template=template)

            try:
                correct_sol = correct.solve(problem)
                malrule_sol = malrule.solve(problem)
                expected_malrule_answer = malrule.calculate_expected_answer(problem)

                # Check if malrule answer matches expected
                malrule_matches_expected = abs(expected_malrule_answer - malrule_sol.answer) < 0.01

                # Check if answers are different (edge case detection)
                answers_different = abs(correct_sol.answer - malrule_sol.answer) > 0.01

                # Check if algorithm-computed answers match metadata (for verification)
                correct_matches_metadata = abs(correct_sol.answer - problem.metadata['correct_answer']) < 0.01
                malrule_matches_metadata = abs(malrule_sol.answer - problem.metadata['malrule_answer']) < 0.01

                if not malrule_matches_expected:
                    print(f"\n❌ Problem {i+1}: FAILED - Malrule calculation mismatch")
                    print(f"   Expression: {problem.metadata['expression']}")
                    print(f"   Expected malrule: {expected_malrule_answer}")
                    print(f"   Computed malrule: {malrule_sol.answer}")
                    print(f"\n   Malrule steps:")
                    for step in malrule_sol.steps:
                        print(f"      {step}")
                    all_passed = False
                    failed_tests += 1

                elif not answers_different:
                    # Edge case: malrule produces same answer as correct
                    print(f"\n⚠️  Problem {i+1}: EDGE CASE - Malrule produces same answer as correct!")
                    print(f"   Expression: {problem.metadata['expression']}")
                    print(f"   Both answers: {correct_sol.answer}")
                    print(f"\n   Correct steps:")
                    for step in correct_sol.steps:
                        print(f"      {step}")
                    print(f"\n   Malrule steps:")
                    for step in malrule_sol.steps:
                        print(f"      {step}")
                    # Still fail the test as misconception should produce different answer
                    all_passed = False
                    failed_tests += 1

                elif not correct_matches_metadata or not malrule_matches_metadata:
                    print(f"\n❌ Problem {i+1}: FAILED - Algorithm doesn't match metadata")
                    print(f"   Expression: {problem.metadata['expression']}")
                    print(f"   Correct: computed={correct_sol.answer}, metadata={problem.metadata['correct_answer']}")
                    print(f"   Malrule: computed={malrule_sol.answer}, metadata={problem.metadata['malrule_answer']}")
                    print(f"\n   Correct steps:")
                    for step in correct_sol.steps:
                        print(f"      {step}")
                    print(f"\n   Malrule steps:")
                    for step in malrule_sol.steps:
                        print(f"      {step}")
                    all_passed = False
                    failed_tests += 1

                else:
                    # Test passed
                    print(f"   ✓ Problem {i+1}: {problem.metadata['expression']}")
                    print(f"      Correct: {correct_sol.answer}, Malrule: {malrule_sol.answer}")

            except Exception as e:
                print(f"\n❌ Problem {i+1}: EXCEPTION")
                print(f"   Expression: {problem.metadata['expression']}")
                print(f"   Error: {e}")
                print(f"   Expected: Correct={problem.metadata.get('correct_answer')}, Malrule={problem.metadata.get('malrule_answer')}")
                import traceback
                traceback.print_exc()
                all_passed = False
                failed_tests += 1

        if failed_tests == 0:
            print(f"✓ Template {template} passed all tests")

    print("\n" + "="*70)
    if all_passed:
        print(f"ALL TEMPLATE TESTS PASSED ✓ ({total_tests}/{total_tests})")
    else:
        print(f"SOME TESTS FAILED ✗ ({total_tests - failed_tests}/{total_tests} passed)")
    print("="*70)

    return all_passed


def test_template_specific_cases():
    """Test specific cases for each template with detailed output."""
    print("\n" + "="*70)
    print("TESTING TEMPLATE-SPECIFIC CASES")
    print("="*70)

    malrule = PEMDASStrictlySequentialMalrule()
    correct = OrderOfOperationsCorrectAlgorithm()

    all_passed = True

    # Test case 1: longer_expressions - 24 ÷ 2 × 3 ÷ 4
    print("\n" + "─"*70)
    print("TEST: longer_expressions - 24 ÷ 2 × 3 ÷ 4")
    print("─"*70)
    problem1 = Problem(
        text="Calculate: 24 ÷ 2 × 3 ÷ 4",
        operands=[24, 2, 3, 4],
        operation='order_of_operations',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'expression': '24 ÷ 2 × 3 ÷ 4',
            'correct_answer': 9,  # ((24 ÷ 2) × 3) ÷ 4 = (12 × 3) ÷ 4 = 36 ÷ 4 = 9
            'malrule_answer': 1,  # 24 ÷ (2 × 3 × 4) = 24 ÷ 24 = 1
            'problem_type': 'mult_div',
            'operator_sequence': '÷×÷',
            'template': 'longer_expressions'
        }
    )

    try:
        correct_sol1 = correct.solve(problem1)
        malrule_sol1 = malrule.solve(problem1)
        expected1 = malrule.calculate_expected_answer(problem1)

        print(f"Expression: {problem1.metadata['expression']}")
        print(f"Correct answer: {correct_sol1.answer} (expected: {problem1.metadata['correct_answer']})")
        print(f"Malrule answer: {malrule_sol1.answer} (expected: {problem1.metadata['malrule_answer']})")

        assert abs(correct_sol1.answer - 9) < 0.01, f"Correct answer should be 9, got {correct_sol1.answer}"
        assert abs(expected1 - malrule_sol1.answer) < 0.01, f"Malrule calculation mismatch"
        assert abs(correct_sol1.answer - malrule_sol1.answer) > 0.01, f"Answers should differ"
        print("✓ PASSED")
    except Exception as e:
        print(f"❌ FAILED: {e}")
        print("Correct steps:")
        for step in correct_sol1.steps:
            print(f"  {step}")
        print("Malrule steps:")
        for step in malrule_sol1.steps:
            print(f"  {step}")
        all_passed = False

    # Test case 2: mixed_operations - 2 + 6 ÷ 2 × 3
    print("\n" + "─"*70)
    print("TEST: mixed_operations - 2 + 6 ÷ 2 × 3")
    print("─"*70)
    problem2 = Problem(
        text="Calculate: 2 + 6 ÷ 2 × 3",
        operands=[2, 6, 2, 3],
        operation='order_of_operations',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'expression': '2 + 6 ÷ 2 × 3',
            'correct_answer': 11,  # 2 + ((6 ÷ 2) × 3) = 2 + (3 × 3) = 2 + 9 = 11
            'malrule_answer': 3,  # 2 + (6 ÷ (2 × 3)) = 2 + (6 ÷ 6) = 2 + 1 = 3
            'problem_type': 'mixed',
            'operator_sequence': '+÷×',
            'template': 'mixed_operations'
        }
    )

    try:
        correct_sol2 = correct.solve(problem2)
        malrule_sol2 = malrule.solve(problem2)
        expected2 = malrule.calculate_expected_answer(problem2)

        print(f"Expression: {problem2.metadata['expression']}")
        print(f"Correct answer: {correct_sol2.answer} (expected: {problem2.metadata['correct_answer']})")
        print(f"Malrule answer: {malrule_sol2.answer} (expected: {problem2.metadata['malrule_answer']})")

        assert abs(correct_sol2.answer - 11) < 0.01, f"Correct answer should be 11, got {correct_sol2.answer}"
        assert abs(expected2 - malrule_sol2.answer) < 0.01, f"Malrule calculation mismatch"
        assert abs(correct_sol2.answer - malrule_sol2.answer) > 0.01, f"Answers should differ"
        print("✓ PASSED")
    except Exception as e:
        print(f"❌ FAILED: {e}")
        print("Correct steps:")
        for step in correct_sol2.steps:
            print(f"  {step}")
        print("Malrule steps:")
        for step in malrule_sol2.steps:
            print(f"  {step}")
        all_passed = False

    print("\n" + "="*70)
    if all_passed:
        print("ALL TEMPLATE-SPECIFIC TESTS PASSED ✓")
    else:
        print("SOME TEMPLATE-SPECIFIC TESTS FAILED ✗")
    print("="*70)

    return all_passed


def test_automated_suite():
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = PEMDASStrictlySequentialProblemGenerator(
        level=7,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = PEMDASStrictlySequentialMalrule()
    correct = OrderOfOperationsCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: PEMDAS-Strictly-Sequential  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    all_tests_passed = True

    try:
        # Run all test suites
        test_specific_examples()

        templates_passed = test_all_templates()
        all_tests_passed = all_tests_passed and templates_passed

        specific_passed = test_template_specific_cases()
        all_tests_passed = all_tests_passed and specific_passed

        automated_passed = test_automated_suite()
        all_tests_passed = all_tests_passed and automated_passed

        print("\n\n╔" + "═"*68 + "╗")
        if all_tests_passed:
            print("║" + "  ✓✓✓ ALL TESTS PASSED ✓✓✓  ".center(70) + "║")
        else:
            print("║" + "  ✗✗✗ SOME TESTS FAILED ✗✗✗  ".center(70) + "║")
        print("╚" + "═"*68 + "╝\n")
        return 0 if all_tests_passed else 1
    except Exception as e:
        print(f"\n✗✗✗ TEST FAILED WITH EXCEPTION: {e} ✗✗✗")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
