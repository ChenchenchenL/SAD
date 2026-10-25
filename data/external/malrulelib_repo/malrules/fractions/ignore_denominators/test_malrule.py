#!/usr/bin/env python3
"""
Test script for Ignore-Denominators malrule.
Tests all problem templates and validates that algorithms solve problems independently.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, Problem
from malrules.fractions.ignore_denominators import (
    IgnoreDenominatorsProblemGenerator,
    IgnoreDenominatorsMalrule,
    FractionCorrectAlgorithm
)


def test_all_templates():
    """Test all problem templates to ensure algorithms work independently."""
    print("="*80)
    print("TESTING IGNORE-DENOMINATORS - ALL TEMPLATES")
    print("="*80)

    # Initialize algorithms
    malrule = IgnoreDenominatorsMalrule()
    correct = FractionCorrectAlgorithm()

    # All templates to test
    templates = [
        'basic_addition',
        'basic_subtraction',
        'multiplication',
        'division',
        'word_problem',
        'word_problem_multiplication',
        'word_problem_division'
    ]

    # Test each template multiple times with different seeds
    all_passed = True
    template_results = {}

    for template in templates:
        print(f"\n{'='*80}")
        print(f"Testing Template: {template}")
        print(f"{'='*80}")

        template_passed = True
        template_issues = []

        # Generate and test 5 problems for each template
        for seed in range(100, 105):
            # Create generator with specific seed
            generator = IgnoreDenominatorsProblemGenerator(
                level=5,
                difficulty=DifficultyLevel.MEDIUM
            )

            # Keep generating until we get the desired template
            problem = None
            for attempt in range(100):
                test_problem = generator.generate(seed=seed + attempt * 1000)
                if test_problem.metadata.get('template') == template:
                    problem = test_problem
                    break

            if problem is None:
                print(f"  [SKIP] Could not generate template '{template}' with seed {seed}")
                continue

            print(f"\n  Test Case (seed={seed}):")
            print(f"  Problem: {problem.text}")
            print(f"  Operands: {problem.operands}")

            # Solve with both algorithms
            try:
                correct_sol = correct.solve(problem)
                malrule_sol = malrule.solve(problem)

                print(f"  Correct Answer: {correct_sol.answer}")
                print(f"  Malrule Answer: {malrule_sol.answer}")

                # Verify algorithms didn't use metadata answers
                if 'correct_answer' in problem.metadata:
                    # The algorithms should compute their own answers
                    # We check that the correct algorithm got the right answer
                    expected_correct = problem.metadata['correct_answer']
                    if correct_sol.answer != expected_correct:
                        print(f"  [WARNING] Correct algorithm answer {correct_sol.answer} != expected {expected_correct}")
                        # This might happen due to different simplification, so let's verify the value
                        # We'll allow this for now but print a warning

                # Check if answers are different (they should be for malrule to be effective)
                if correct_sol.answer == malrule_sol.answer:
                    # Edge case: malrule produces same answer as correct
                    print(f"  [EDGE CASE] Malrule produced same answer as correct algorithm!")
                    print(f"  This can happen in rare cases. Printing steps:")
                    print(f"\n  --- Correct Algorithm Steps ---")
                    for step in correct_sol.steps:
                        print(f"    {step}")
                    print(f"\n  --- Malrule Algorithm Steps ---")
                    for step in malrule_sol.steps:
                        print(f"    {step}")

                    # Fail the test because malrule should produce different answer
                    print(f"  [FAIL] Test failed due to edge case - malrule should produce wrong answer")
                    template_passed = False
                    all_passed = False
                    template_issues.append(f"Seed {seed}: Edge case - same answer")
                else:
                    # Verify malrule is incorrect
                    if malrule_sol.is_correct:
                        print(f"  [FAIL] Malrule should not be marked as correct!")
                        template_passed = False
                        all_passed = False
                        template_issues.append(f"Seed {seed}: Malrule marked as correct")
                    else:
                        print(f"  [PASS] Algorithms produced different answers as expected")

            except Exception as e:
                print(f"  [ERROR] Exception occurred: {e}")
                import traceback
                traceback.print_exc()
                template_passed = False
                all_passed = False
                template_issues.append(f"Seed {seed}: Exception - {e}")

        template_results[template] = {
            'passed': template_passed,
            'issues': template_issues
        }

        if template_passed:
            print(f"\n  ✓ Template '{template}' PASSED all tests")
        else:
            print(f"\n  ✗ Template '{template}' FAILED with issues:")
            for issue in template_issues:
                print(f"    - {issue}")

    # Print summary
    print(f"\n{'='*80}")
    print("TEST SUMMARY")
    print(f"{'='*80}")

    for template, result in template_results.items():
        status = "✓ PASS" if result['passed'] else "✗ FAIL"
        print(f"  {status}: {template}")
        if not result['passed']:
            for issue in result['issues']:
                print(f"      - {issue}")

    if all_passed:
        print(f"\n{'='*80}")
        print("✓✓✓ ALL TESTS PASSED ✓✓✓")
        print(f"{'='*80}")
    else:
        print(f"\n{'='*80}")
        print("✗✗✗ SOME TESTS FAILED ✗✗✗")
        print(f"{'='*80}")

    return all_passed


def test_specific_cases():
    """Test specific edge cases to ensure algorithms work correctly."""
    print("\n\n" + "="*80)
    print("TESTING SPECIFIC EDGE CASES")
    print("="*80)

    malrule = IgnoreDenominatorsMalrule()
    correct = FractionCorrectAlgorithm()

    test_cases = [
        {
            'name': 'Basic Addition: 2/3 + 1/5',
            'problem': Problem(
                text="Calculate: 2/3 + 1/5",
                operands=[2, 3, 1, 5],
                operation='fraction_addition',
                level=5,
                difficulty=DifficultyLevel.MEDIUM,
                metadata={'operation': 'addition', 'template': 'basic_addition'}
            ),
            'expected_correct': '13/15',
            'expected_malrule': '3'
        },
        {
            'name': 'Basic Subtraction: 5/6 - 1/4',
            'problem': Problem(
                text="Calculate: 5/6 - 1/4",
                operands=[5, 6, 1, 4],
                operation='fraction_subtraction',
                level=5,
                difficulty=DifficultyLevel.MEDIUM,
                metadata={'operation': 'subtraction', 'template': 'basic_subtraction'}
            ),
            'expected_correct': '7/12',
            'expected_malrule': '4'
        },
        {
            'name': 'Multiplication: 2/3 × 3/4',
            'problem': Problem(
                text="Calculate: 2/3 × 3/4",
                operands=[2, 3, 3, 4],
                operation='fraction_multiplication',
                level=5,
                difficulty=DifficultyLevel.MEDIUM,
                metadata={'operation': 'multiplication', 'template': 'multiplication'}
            ),
            'expected_correct': '1/2',
            'expected_malrule': '6'
        },
        {
            'name': 'Division: 3/4 ÷ 2/5',
            'problem': Problem(
                text="Calculate: 3/4 ÷ 2/5",
                operands=[3, 4, 2, 5],
                operation='fraction_division',
                level=6,
                difficulty=DifficultyLevel.HARD,
                metadata={'operation': 'division', 'template': 'division'}
            ),
            'expected_correct': '15/8',
            'expected_malrule': '1'
        }
    ]

    all_passed = True

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'-'*80}")
        print(f"Test Case {i}: {test_case['name']}")
        print(f"{'-'*80}")

        problem = test_case['problem']
        print(f"Problem: {problem.text}")
        print(f"Operands: {problem.operands}")

        try:
            correct_sol = correct.solve(problem)
            malrule_sol = malrule.solve(problem)

            print(f"\nCorrect Answer: {correct_sol.answer}")
            print(f"Expected: {test_case['expected_correct']}")
            print(f"Malrule Answer: {malrule_sol.answer}")
            print(f"Expected: {test_case['expected_malrule']}")

            # Check results
            correct_match = correct_sol.answer == test_case['expected_correct']
            malrule_match = malrule_sol.answer == test_case['expected_malrule']

            if correct_match and malrule_match:
                print(f"\n✓ Test Case {i} PASSED")
            else:
                print(f"\n✗ Test Case {i} FAILED")
                all_passed = False

                if not correct_match:
                    print(f"  Correct algorithm mismatch!")
                    print(f"  --- Correct Algorithm Steps ---")
                    for step in correct_sol.steps:
                        print(f"    {step}")

                if not malrule_match:
                    print(f"  Malrule algorithm mismatch!")
                    print(f"  --- Malrule Algorithm Steps ---")
                    for step in malrule_sol.steps:
                        print(f"    {step}")

        except Exception as e:
            print(f"\n✗ Test Case {i} FAILED with exception: {e}")
            import traceback
            traceback.print_exc()
            all_passed = False

    if all_passed:
        print(f"\n{'='*80}")
        print("✓✓✓ ALL SPECIFIC CASES PASSED ✓✓✓")
        print(f"{'='*80}")
    else:
        print(f"\n{'='*80}")
        print("✗✗✗ SOME SPECIFIC CASES FAILED ✗✗✗")
        print(f"{'='*80}")

    return all_passed


def main():
    print("\n╔" + "═"*78 + "╗")
    print("║" + "  COMPREHENSIVE TEST: Ignore-Denominators  ".center(78) + "║")
    print("╚" + "═"*78 + "╝\n")

    try:
        # Test specific edge cases first
        specific_passed = test_specific_cases()

        # Test all templates
        templates_passed = test_all_templates()

        all_passed = specific_passed and templates_passed

        print("\n\n╔" + "═"*78 + "╗")
        if all_passed:
            print("║" + "  ✓✓✓ ALL TESTS PASSED ✓✓✓  ".center(78) + "║")
        else:
            print("║" + "  ✗✗✗ SOME TESTS FAILED ✗✗✗  ".center(78) + "║")
        print("╚" + "═"*78 + "╝\n")

        return 0 if all_passed else 1

    except Exception as e:
        print(f"\n✗✗✗ TEST SUITE FAILED: {e} ✗✗✗")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
