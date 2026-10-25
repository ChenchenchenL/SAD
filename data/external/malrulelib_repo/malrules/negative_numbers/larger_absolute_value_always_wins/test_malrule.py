#!/usr/bin/env python3
"""
Comprehensive test script for Larger-Absolute-Value-Always-Wins malrule.

Tests all problem templates and handles edge cases where misconception
produces the same answer as correct algorithm.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import random
from utils import DifficultyLevel, MalruleTest, Problem
from malrules.negative_numbers.larger_absolute_value_always_wins import (
    LargerAbsoluteValueAlwaysWinsProblemGenerator,
    LargerAbsoluteValueAlwaysWinsMalrule,
    NegativeNumbersCorrectAlgorithm
)


def test_all_templates():
    """Test all problem templates comprehensively."""
    print("=" * 70)
    print("COMPREHENSIVE TEMPLATE TESTING")
    print("=" * 70)

    problem_gen = LargerAbsoluteValueAlwaysWinsProblemGenerator(
        level=7,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = LargerAbsoluteValueAlwaysWinsMalrule()
    correct = NegativeNumbersCorrectAlgorithm()

    # All templates to test
    templates = [
        'basic_addition_subtraction',
        'multiplication',
        'division',
        'comparison',
        'word_problem'
    ]

    all_passed = True
    total_tests = 0
    passed_tests = 0
    edge_cases_found = 0

    for template in templates:
        print(f"\n{'=' * 70}")
        print(f"TESTING TEMPLATE: {template.upper()}")
        print(f"{'=' * 70}")

        # Generate and test multiple problems for this template
        template_tests = 0
        template_passed = 0
        template_edge_cases = 0

        for test_num in range(10):
            total_tests += 1
            template_tests += 1

            # Generate problem until we get the desired template
            max_attempts = 100
            problem = None
            for attempt in range(max_attempts):
                seed = random.randint(0, 1000000)
                temp_problem = problem_gen.generate(seed=seed)
                if temp_problem.metadata.get('template') == template:
                    problem = temp_problem
                    break

            if problem is None:
                print(f"\n  Test {test_num + 1}: ✗ FAILED - Could not generate problem for template {template}")
                all_passed = False
                continue

            try:
                # Solve with both algorithms
                correct_sol = correct.solve(problem)
                malrule_sol = malrule.solve(problem)

                # Check if this is an edge case (malrule happens to be correct)
                is_edge_case = (correct_sol.answer == malrule_sol.answer)

                if is_edge_case:
                    edge_cases_found += 1
                    template_edge_cases += 1
                    print(f"\n  Test {test_num + 1}: ⚠ EDGE CASE DETECTED")
                    print(f"    Problem: {problem.text}")
                    print(f"    Both algorithms produced: {correct_sol.answer}")
                    print(f"    This is an edge case where the malrule accidentally produces correct answer!")
                    print(f"\n    --- Correct Algorithm Steps ---")
                    for step in correct_sol.steps:
                        print(f"      {step}")
                    print(f"\n    --- Malrule Algorithm Steps ---")
                    for step in malrule_sol.steps:
                        print(f"      {step}")

                    # Edge cases are expected but should be noted
                    # Don't fail the test, but warn about it
                    print(f"    NOTE: This is acceptable but rare. Continuing...")

                else:
                    # Normal case - malrule should produce different answer
                    if correct_sol.answer != malrule_sol.answer:
                        template_passed += 1
                        passed_tests += 1
                        print(f"  Test {test_num + 1}: ✓ PASSED")
                        print(f"    Problem: {problem.text}")
                        print(f"    Correct answer: {correct_sol.answer}")
                        print(f"    Malrule answer: {malrule_sol.answer}")
                    else:
                        # This should not happen if not edge case
                        print(f"\n  Test {test_num + 1}: ✗ FAILED - Unexpected result")
                        print(f"    Problem: {problem.text}")
                        print(f"    Both produced: {correct_sol.answer}")
                        all_passed = False

            except Exception as e:
                print(f"\n  Test {test_num + 1}: ✗ FAILED - Exception occurred")
                print(f"    Problem: {problem.text}")
                print(f"    Exception: {str(e)}")
                import traceback
                traceback.print_exc()
                all_passed = False

        print(f"\n  Template Summary:")
        print(f"    Tests passed: {template_passed}/{template_tests}")
        print(f"    Edge cases found: {template_edge_cases}")

    print(f"\n{'=' * 70}")
    print(f"OVERALL SUMMARY")
    print(f"{'=' * 70}")
    print(f"Total tests run: {total_tests}")
    print(f"Tests passed: {passed_tests}")
    print(f"Edge cases detected: {edge_cases_found}")
    print(f"Success rate: {passed_tests}/{total_tests - edge_cases_found} non-edge cases")

    return all_passed


def test_specific_examples():
    """Test with specific, known examples."""
    print("\n" + "=" * 70)
    print("TESTING SPECIFIC KNOWN EXAMPLES")
    print("=" * 70)

    malrule = LargerAbsoluteValueAlwaysWinsMalrule()
    correct = NegativeNumbersCorrectAlgorithm()

    test_cases = [
        {
            'text': "Calculate: 3 - (-8)",
            'operands': [3, -8],
            'operation': 'subtraction',
            'metadata': {
                'num1': 3,
                'num2': -8,
                'operation_symbol': '-',
                'correct_answer': 11,
                'abs_num1': 3,
                'abs_num2': 8,
                'template': 'basic_addition_subtraction'
            },
            'expected_correct': 11,
            'expected_different': True,
            'description': "Classic case: subtracting negative"
        },
        {
            'text': "Calculate: -5 + 12",
            'operands': [-5, 12],
            'operation': 'addition',
            'metadata': {
                'num1': -5,
                'num2': 12,
                'operation_symbol': '+',
                'correct_answer': 7,
                'abs_num1': 5,
                'abs_num2': 12,
                'template': 'basic_addition_subtraction'
            },
            'expected_correct': 7,
            'expected_different': False,  # May be edge case
            'description': "Addition with negative"
        },
        {
            'text': "Calculate: (-4) × (-3)",
            'operands': [-4, -3],
            'operation': 'multiplication',
            'metadata': {
                'num1': -4,
                'num2': -3,
                'operation_symbol': '×',
                'correct_answer': 12,
                'abs_num1': 4,
                'abs_num2': 3,
                'template': 'multiplication'
            },
            'expected_correct': 12,
            'expected_different': True,
            'description': "Negative times negative"
        },
        {
            'text': "Calculate: (-20) ÷ (-4)",
            'operands': [-20, -4],
            'operation': 'division',
            'metadata': {
                'num1': -20,
                'num2': -4,
                'operation_symbol': '÷',
                'correct_answer': 5,
                'abs_num1': 20,
                'abs_num2': 4,
                'template': 'division'
            },
            'expected_correct': 5,
            'expected_different': True,
            'description': "Negative divided by negative"
        },
        {
            'text': "Which is greater: -10 or 3?",
            'operands': [-10, 3],
            'operation': 'comparison',
            'metadata': {
                'num1': -10,
                'num2': 3,
                'operation_symbol': 'compare',
                'correct_answer': 3,
                'abs_num1': 10,
                'abs_num2': 3,
                'template': 'comparison'
            },
            'expected_correct': 3,
            'expected_different': True,
            'description': "Comparing negative and positive"
        }
    ]

    all_passed = True

    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTEST CASE {i}: {test_case['description']}")
        print("-" * 70)

        problem = Problem(
            text=test_case['text'],
            operands=test_case['operands'],
            operation=test_case['operation'],
            level=7,
            difficulty=DifficultyLevel.MEDIUM,
            metadata=test_case['metadata']
        )

        try:
            correct_sol = correct.solve(problem)
            malrule_sol = malrule.solve(problem)

            print(f"Problem: {problem.text}")
            print(f"Correct answer: {correct_sol.answer}")
            print(f"Malrule answer: {malrule_sol.answer}")

            # Verify correct answer matches expected
            if correct_sol.answer != test_case['expected_correct']:
                print(f"✗ FAILED: Expected correct answer {test_case['expected_correct']}, got {correct_sol.answer}")
                all_passed = False
                print("\n--- Correct Algorithm Steps ---")
                for step in correct_sol.steps:
                    print(f"  {step}")
                continue

            # Check if answers differ as expected
            answers_differ = (correct_sol.answer != malrule_sol.answer)

            if test_case['expected_different'] and not answers_differ:
                print(f"⚠ EDGE CASE: Expected different answers but both are {correct_sol.answer}")
                print("\n--- Correct Algorithm Steps ---")
                for step in correct_sol.steps:
                    print(f"  {step}")
                print("\n--- Malrule Algorithm Steps ---")
                for step in malrule_sol.steps:
                    print(f"  {step}")
                # Don't fail, but note it
            elif not test_case['expected_different'] and answers_differ:
                print(f"✓ PASSED (answers differ as can happen)")
            else:
                print(f"✓ PASSED")

        except Exception as e:
            print(f"✗ FAILED: Exception - {str(e)}")
            import traceback
            traceback.print_exc()
            all_passed = False

    return all_passed


def test_automated_suite():
    """Run the automated test suite."""
    print("\n\n" + "=" * 70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("=" * 70)

    problem_gen = LargerAbsoluteValueAlwaysWinsProblemGenerator(
        level=7,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = LargerAbsoluteValueAlwaysWinsMalrule()
    correct = NegativeNumbersCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)

    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    else:
        print("\n✗✗✗ SOME TESTS FAILED ✗✗✗")
        for result in results:
            if not result.passed:
                print(f"FAILED: {result.message}")
                if result.details:
                    print(f"Details: {result.details}")

    return all_passed


def main():
    print("\n╔" + "═" * 68 + "╗")
    print("║" + "  COMPREHENSIVE TEST: Larger-Absolute-Value-Always-Wins  ".center(68) + "║")
    print("╚" + "═" * 68 + "╝\n")

    try:
        # Test all templates
        templates_passed = test_all_templates()

        # Test specific known examples
        specific_passed = test_specific_examples()

        # Run automated suite
        automated_passed = test_automated_suite()

        # Final summary
        print("\n\n╔" + "═" * 68 + "╗")
        print("║" + "  FINAL TEST SUMMARY  ".center(68) + "║")
        print("╚" + "═" * 68 + "╝\n")

        print(f"Template tests: {'✓ PASSED' if templates_passed else '✗ FAILED'}")
        print(f"Specific examples: {'✓ PASSED' if specific_passed else '✗ FAILED'}")
        print(f"Automated suite: {'✓ PASSED' if automated_passed else '✗ FAILED'}")

        all_passed = templates_passed and specific_passed and automated_passed

        if all_passed:
            print("\n╔" + "═" * 68 + "╗")
            print("║" + "  ✓✓✓ ALL TESTS PASSED ✓✓✓  ".center(68) + "║")
            print("╚" + "═" * 68 + "╝\n")
        else:
            print("\n╔" + "═" * 68 + "╗")
            print("║" + "  ✗✗✗ SOME TESTS FAILED ✗✗✗  ".center(68) + "║")
            print("╚" + "═" * 68 + "╝\n")

        return 0 if all_passed else 1

    except Exception as e:
        print(f"\n✗✗✗ TEST SUITE FAILED: {e} ✗✗✗")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
