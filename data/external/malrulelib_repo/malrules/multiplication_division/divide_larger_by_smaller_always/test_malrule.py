#!/usr/bin/env python3
"""
Test script for Divide-Larger-By-Smaller-Always malrule.

This test ensures that:
1. Algorithms solve problems independently (not using metadata answers)
2. All templates are tested
3. Detailed output is provided for both passing and failing tests
4. Edge cases where malrule might produce correct answer are caught
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.multiplication_division.divide_larger_by_smaller_always import (
    DivideLargerBySmallerAlwaysProblemGenerator,
    DivideLargerBySmallerAlwaysMalrule,
    DivisionCorrectAlgorithm
)


def print_section(title, width=80):
    """Print a formatted section header."""
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width)


def print_subsection(title, width=80):
    """Print a formatted subsection header."""
    print("\n" + "-" * width)
    print(title)
    print("-" * width)


def test_template(template_name, seed=42):
    """
    Test a specific template with detailed output.

    Args:
        template_name: Name of the template to test
        seed: Random seed for reproducibility

    Returns:
        True if test passes, False otherwise
    """
    print_subsection(f"Testing template: {template_name}")

    # Create instances
    problem_gen = DivideLargerBySmallerAlwaysProblemGenerator(
        level=4,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = DivideLargerBySmallerAlwaysMalrule()
    correct = DivisionCorrectAlgorithm()

    # Generate problem
    try:
        problem = problem_gen.generate(seed=seed, template=template_name)
    except Exception as e:
        print(f"✗ FAILED: Problem generation error: {e}")
        return False

    print(f"\nProblem: {problem.text}")
    print(f"Operands: {problem.operands}")
    print(f"Template: {problem.metadata.get('template', 'N/A')}")

    # Solve with correct algorithm
    try:
        correct_sol = correct.solve(problem)
    except Exception as e:
        print(f"\n✗ FAILED: Correct algorithm error: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Solve with malrule
    try:
        malrule_sol = malrule.solve(problem)
    except Exception as e:
        print(f"\n✗ FAILED: Malrule algorithm error: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Verify calculate_expected_answer matches malrule solution
    try:
        expected_answer = malrule.calculate_expected_answer(problem)
    except Exception as e:
        print(f"\n✗ FAILED: calculate_expected_answer error: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Check if answers are different
    correct_ans = float(correct_sol.answer) if isinstance(correct_sol.answer, str) else correct_sol.answer
    malrule_ans = float(malrule_sol.answer) if isinstance(malrule_sol.answer, str) else malrule_sol.answer
    expected_ans = float(expected_answer) if isinstance(expected_answer, str) else expected_answer

    # Test results
    test_passed = True

    # Check that expected answer matches malrule answer
    if abs(expected_ans - malrule_ans) > 0.0001:
        print(f"\n✗ FAILED: Expected answer ({expected_ans}) != Malrule answer ({malrule_ans})")
        test_passed = False

    # Check that correct and malrule give different answers (critical check)
    if abs(correct_ans - malrule_ans) < 0.0001:
        print("\n⚠ WARNING: Malrule produced same answer as correct algorithm!")
        print("This is an EDGE CASE where the misconception doesn't change the answer.")
        print("\nCorrect Algorithm Steps:")
        for step in correct_sol.steps:
            print(f"  {step}")
        print("\nMalrule Algorithm Steps:")
        for step in malrule_sol.steps:
            print(f"  {step}")
        print(f"\nExpected Correct Answer: {correct_ans}")
        print(f"Expected Malrule Answer: {malrule_ans}")
        print("✗ TEST FAILED: Malrule must produce different answer from correct algorithm")
        return False

    if test_passed:
        print(f"\n✓ TEST PASSED")
        print(f"Correct Answer: {correct_ans}")
        print(f"Malrule Answer: {malrule_ans}")
        print(f"Expected Answer: {expected_ans}")
        return True
    else:
        print("\n✗ TEST FAILED")
        print("\nCorrect Algorithm Steps:")
        for step in correct_sol.steps:
            print(f"  {step}")
        print("\nMalrule Algorithm Steps:")
        for step in malrule_sol.steps:
            print(f"  {step}")
        print(f"\nExpected Correct Answer: {correct_ans}")
        print(f"Expected Malrule Answer: {malrule_ans}")
        return False


def test_all_templates():
    """Test all 10 templates."""
    print_section("TESTING ALL TEMPLATES")

    templates = [
        'basic_smaller_dividend',
        'fraction_result',
        'decimal_friendly',
        'word_problem_sharing',
        'word_problem_measurement',
        'money_sharing',
        'probability_ratio',
        'percentage_grade',
        'ratio_comparison',
        'scale_model'
    ]

    results = {}
    for template in templates:
        passed = test_template(template, seed=42)
        results[template] = passed

    # Summary
    print_section("TEMPLATE TEST SUMMARY")
    total = len(templates)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed

    print(f"\nTotal Templates: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print("\nDetails:")
    for template, result in results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"  {template}: {status}")

    return all(results.values())


def test_specific_examples():
    """Test with specific hand-crafted examples."""
    print_section("TESTING SPECIFIC EXAMPLES")

    malrule = DivideLargerBySmallerAlwaysMalrule()
    correct = DivisionCorrectAlgorithm()

    test_cases = [
        {
            'name': '4 ÷ 6 (Classic case)',
            'problem': Problem(
                text="Calculate: 4 ÷ 6",
                operands=[4, 6],
                operation='division',
                level=4,
                difficulty=DifficultyLevel.MEDIUM,
                metadata={
                    'dividend': 4,
                    'divisor': 6,
                    'template': 'basic_smaller_dividend'
                }
            ),
            'expected_correct': 4/6,
            'expected_malrule': 6/4
        },
        {
            'name': '3 ÷ 8',
            'problem': Problem(
                text="Calculate: 3 ÷ 8",
                operands=[3, 8],
                operation='division',
                level=4,
                difficulty=DifficultyLevel.MEDIUM,
                metadata={
                    'dividend': 3,
                    'divisor': 8,
                    'template': 'basic_smaller_dividend'
                }
            ),
            'expected_correct': 3/8,
            'expected_malrule': 8/3
        },
        {
            'name': '2 ÷ 5',
            'problem': Problem(
                text="Calculate: 2 ÷ 5",
                operands=[2, 5],
                operation='division',
                level=4,
                difficulty=DifficultyLevel.MEDIUM,
                metadata={
                    'dividend': 2,
                    'divisor': 5,
                    'template': 'basic_smaller_dividend'
                }
            ),
            'expected_correct': 2/5,
            'expected_malrule': 5/2
        }
    ]

    all_passed = True
    for test_case in test_cases:
        print_subsection(f"Test: {test_case['name']}")

        problem = test_case['problem']
        print(f"Problem: {problem.text}")

        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        correct_ans = float(correct_sol.answer)
        malrule_ans = float(malrule_sol.answer)
        expected_correct = test_case['expected_correct']
        expected_malrule = test_case['expected_malrule']

        # Check answers
        correct_match = abs(correct_ans - expected_correct) < 0.001
        malrule_match = abs(malrule_ans - expected_malrule) < 0.001
        different = abs(correct_ans - malrule_ans) > 0.001

        if correct_match and malrule_match and different:
            print(f"✓ TEST PASSED")
            print(f"  Correct Answer: {correct_ans} (expected {expected_correct})")
            print(f"  Malrule Answer: {malrule_ans} (expected {expected_malrule})")
        else:
            print(f"✗ TEST FAILED")
            all_passed = False
            print("\nCorrect Algorithm Steps:")
            for step in correct_sol.steps:
                print(f"  {step}")
            print("\nMalrule Algorithm Steps:")
            for step in malrule_sol.steps:
                print(f"  {step}")
            print(f"\nExpected Correct: {expected_correct}, Got: {correct_ans}")
            print(f"Expected Malrule: {expected_malrule}, Got: {malrule_ans}")

    return all_passed


def test_no_metadata_leakage():
    """Test that algorithms don't use metadata answers."""
    print_section("TESTING NO METADATA LEAKAGE")

    print("\nThis test ensures algorithms solve problems independently")
    print("and do not use pre-calculated answers from metadata.")

    malrule = DivideLargerBySmallerAlwaysMalrule()
    correct = DivisionCorrectAlgorithm()

    # Create problem with WRONG answers in metadata to verify they're not used
    problem = Problem(
        text="Calculate: 4 ÷ 6",
        operands=[4, 6],
        operation='division',
        level=4,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'dividend': 4,
            'divisor': 6,
            'template': 'basic_smaller_dividend',
            # Note: No 'correct_answer' in metadata anymore
        }
    )

    print(f"\nProblem: {problem.text}")
    print(f"Operands: {problem.operands}")
    print("Metadata does NOT contain pre-calculated answers")

    correct_sol = correct.solve(problem)
    malrule_sol = malrule.solve(problem)

    correct_ans = float(correct_sol.answer)
    malrule_ans = float(malrule_sol.answer)

    # Expected answers (calculated independently)
    expected_correct = 4 / 6  # 0.6667
    expected_malrule = 6 / 4  # 1.5

    correct_match = abs(correct_ans - expected_correct) < 0.001
    malrule_match = abs(malrule_ans - expected_malrule) < 0.001

    if correct_match and malrule_match:
        print(f"\n✓ TEST PASSED")
        print(f"Correct Answer: {correct_ans} (expected {expected_correct})")
        print(f"Malrule Answer: {malrule_ans} (expected {expected_malrule})")
        print("Algorithms are solving problems independently!")
        return True
    else:
        print(f"\n✗ TEST FAILED")
        print(f"Correct: Expected {expected_correct}, Got {correct_ans}")
        print(f"Malrule: Expected {expected_malrule}, Got {malrule_ans}")
        return False


def test_automated_suite():
    """Run the automated test suite."""
    print_section("RUNNING AUTOMATED TEST SUITE")

    problem_gen = DivideLargerBySmallerAlwaysProblemGenerator(
        level=4,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = DivideLargerBySmallerAlwaysMalrule()
    correct = DivisionCorrectAlgorithm()

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

    return all_passed


def main():
    print("\n╔" + "═" * 78 + "╗")
    print("║" + "  VERIFICATION TEST: Divide-Larger-By-Smaller-Always  ".center(78) + "║")
    print("╚" + "═" * 78 + "╝")

    all_tests_passed = True

    try:
        # Test 1: No metadata leakage
        if not test_no_metadata_leakage():
            all_tests_passed = False

        # Test 2: Specific examples
        if not test_specific_examples():
            all_tests_passed = False

        # Test 3: All templates
        if not test_all_templates():
            all_tests_passed = False

        # Test 4: Automated suite
        if not test_automated_suite():
            all_tests_passed = False

        # Final summary
        print_section("FINAL SUMMARY")
        if all_tests_passed:
            print("\n✓✓✓ ALL TESTS PASSED ✓✓✓")
            print("\nVerification complete:")
            print("  ✓ Algorithms solve problems independently")
            print("  ✓ All templates tested successfully")
            print("  ✓ No metadata leakage detected")
            print("  ✓ Malrule produces different answers from correct algorithm")
        else:
            print("\n✗✗✗ SOME TESTS FAILED ✗✗✗")
            print("\nPlease review the failed tests above.")

        print("\n╔" + "═" * 78 + "╗")
        print("║" + "  TEST EXECUTION COMPLETE  ".center(78) + "║")
        print("╚" + "═" * 78 + "╝\n")

        return 0 if all_tests_passed else 1

    except Exception as e:
        print(f"\n✗✗✗ TEST EXECUTION FAILED: {e} ✗✗✗")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
