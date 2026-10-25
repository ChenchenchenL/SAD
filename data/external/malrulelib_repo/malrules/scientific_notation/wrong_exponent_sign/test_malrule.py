#!/usr/bin/env python3
"""Test script for Wrong-Exponent-Sign malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, Problem
from malrules.scientific_notation.wrong_exponent_sign import (
    WrongExponentSignProblemGenerator,
    WrongExponentSignMalrule,
    ScientificNotationCorrectAlgorithm
)


def test_all_templates():
    """Test all problem templates to ensure algorithms work correctly."""
    print("="*80)
    print("TESTING WRONG-EXPONENT-SIGN: ALL TEMPLATES")
    print("="*80)

    malrule = WrongExponentSignMalrule()
    correct_algo = ScientificNotationCorrectAlgorithm()
    generator = WrongExponentSignProblemGenerator(
        level=7,
        difficulty=DifficultyLevel.MEDIUM
    )

    # Test each template type
    template_seeds = [
        ('basic_conversion', 1000),
        ('real_world_small', 1001),
        ('real_world_large', 1002),
        ('unit_conversion_context', 1003),
        ('comparison_context', 1004),
    ]

    all_passed = True
    test_num = 1

    for template_name, seed in template_seeds:
        print(f"\n{'='*80}")
        print(f"TEST {test_num}: Template '{template_name}'")
        print(f"{'='*80}")

        # Generate problem
        problem = generator.generate(seed=seed)
        actual_template = problem.metadata.get('problem_type', 'basic_conversion')

        print(f"Problem: {problem.text}")
        print(f"Number: {problem.metadata['number_str']}")

        # Run algorithms
        correct_sol = correct_algo.solve(problem)
        malrule_sol = malrule.solve(problem)

        # Get expected answers from metadata
        expected_correct = problem.metadata['correct_exponent']
        expected_malrule = problem.metadata['malrule_exponent']

        # Check if test passes
        test_passed = True
        failure_reason = []

        # Verify correct algorithm computed right answer
        if correct_sol.answer != expected_correct:
            test_passed = False
            failure_reason.append(
                f"Correct algorithm computed {correct_sol.answer}, "
                f"expected {expected_correct}"
            )

        # Verify malrule algorithm computed right (wrong) answer
        if malrule_sol.answer != expected_malrule:
            test_passed = False
            failure_reason.append(
                f"Malrule algorithm computed {malrule_sol.answer}, "
                f"expected {expected_malrule}"
            )

        # Verify they are different (catch edge case where malrule == correct)
        if correct_sol.answer == malrule_sol.answer:
            test_passed = False
            failure_reason.append(
                f"Edge case: Malrule produced same answer as correct! "
                f"Both got {correct_sol.answer}"
            )

        if test_passed:
            print(f"✓ TEST PASSED")
            print(f"  Correct answer: {correct_sol.answer}")
            print(f"  Malrule answer: {malrule_sol.answer}")
        else:
            all_passed = False
            print(f"✗ TEST FAILED")
            for reason in failure_reason:
                print(f"  Reason: {reason}")

            print(f"\n  Expected correct answer: {expected_correct}")
            print(f"  Expected malrule answer: {expected_malrule}")

            print(f"\n  Correct algorithm steps:")
            for step in correct_sol.steps:
                print(f"    {step}")

            print(f"\n  Malrule algorithm steps:")
            for step in malrule_sol.steps:
                print(f"    {step}")

        test_num += 1

    print(f"\n{'='*80}")
    if all_passed:
        print("ALL TEMPLATE TESTS PASSED ✓")
    else:
        print("SOME TESTS FAILED ✗")
    print(f"{'='*80}")

    return all_passed


def test_specific_cases():
    """Test specific edge cases."""
    print("\n\n" + "="*80)
    print("TESTING SPECIFIC EDGE CASES")
    print("="*80)

    malrule = WrongExponentSignMalrule()
    correct_algo = ScientificNotationCorrectAlgorithm()

    test_cases = [
        {
            'name': 'Small decimal: 0.0045',
            'problem': Problem(
                text="Write 0.0045 in scientific notation",
                operands=[4.5, -3],
                operation='scientific_notation_conversion',
                level=7,
                difficulty=DifficultyLevel.MEDIUM,
                metadata={
                    'decimal_number': 0.0045,
                    'number_str': '0.0045',
                    'mantissa': 4.5,
                    'correct_exponent': -3,
                    'malrule_exponent': 3,
                    'is_small': True
                }
            ),
            'expected_correct': -3,
            'expected_malrule': 3
        },
        {
            'name': 'Large number: 45000',
            'problem': Problem(
                text="Write 45000 in scientific notation",
                operands=[4.5, 4],
                operation='scientific_notation_conversion',
                level=7,
                difficulty=DifficultyLevel.MEDIUM,
                metadata={
                    'decimal_number': 45000,
                    'number_str': '45000',
                    'mantissa': 4.5,
                    'correct_exponent': 4,
                    'malrule_exponent': -4,
                    'is_small': False
                }
            ),
            'expected_correct': 4,
            'expected_malrule': -4
        },
        {
            'name': 'Very small: 0.00000002',
            'problem': Problem(
                text="Write 0.00000002 in scientific notation",
                operands=[2.0, -8],
                operation='scientific_notation_conversion',
                level=8,
                difficulty=DifficultyLevel.HARD,
                metadata={
                    'decimal_number': 0.00000002,
                    'number_str': '0.00000002',
                    'mantissa': 2.0,
                    'correct_exponent': -8,
                    'malrule_exponent': 8,
                    'is_small': True
                }
            ),
            'expected_correct': -8,
            'expected_malrule': 8
        },
    ]

    all_passed = True

    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['name']}")
        problem = test_case['problem']

        correct_sol = correct_algo.solve(problem)
        malrule_sol = malrule.solve(problem)

        test_passed = True
        if correct_sol.answer != test_case['expected_correct']:
            test_passed = False
            all_passed = False
            print(f"  ✗ Correct algorithm failed: got {correct_sol.answer}, "
                  f"expected {test_case['expected_correct']}")
            print(f"  Steps:")
            for step in correct_sol.steps:
                print(f"    {step}")

        if malrule_sol.answer != test_case['expected_malrule']:
            test_passed = False
            all_passed = False
            print(f"  ✗ Malrule algorithm failed: got {malrule_sol.answer}, "
                  f"expected {test_case['expected_malrule']}")
            print(f"  Steps:")
            for step in malrule_sol.steps:
                print(f"    {step}")

        if correct_sol.answer == malrule_sol.answer:
            test_passed = False
            all_passed = False
            print(f"  ✗ Edge case: Both algorithms produced same answer {correct_sol.answer}")

        if test_passed:
            print(f"  ✓ PASSED - Correct: {correct_sol.answer}, Malrule: {malrule_sol.answer}")

    print(f"\n{'='*80}")
    if all_passed:
        print("ALL EDGE CASE TESTS PASSED ✓")
    else:
        print("SOME TESTS FAILED ✗")
    print(f"{'='*80}")

    return all_passed


def main():
    print("\n╔" + "═"*78 + "╗")
    print("║" + "  COMPREHENSIVE TEST: Wrong-Exponent-Sign  ".center(78) + "║")
    print("╚" + "═"*78 + "╝\n")

    try:
        template_tests_passed = test_all_templates()
        edge_case_tests_passed = test_specific_cases()

        print("\n\n╔" + "═"*78 + "╗")
        if template_tests_passed and edge_case_tests_passed:
            print("║" + "  ✓✓✓ ALL TESTS PASSED ✓✓✓  ".center(78) + "║")
            result = 0
        else:
            print("║" + "  ✗✗✗ SOME TESTS FAILED ✗✗✗  ".center(78) + "║")
            result = 1
        print("╚" + "═"*78 + "╝\n")

        return result
    except Exception as e:
        print(f"\n✗✗✗ TEST CRASHED: {e} ✗✗✗")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
