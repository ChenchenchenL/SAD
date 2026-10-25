#!/usr/bin/env python3
"""Comprehensive test script for Add-Coefficients-When-Multiplying malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, Problem
from malrules.scientific_notation.add_coefficients_when_multiplying import (
    AddCoefficientsWhenMultiplyingProblemGenerator,
    AddCoefficientsWhenMultiplyingMalrule,
    ScientificNotationMultiplicationCorrectAlgorithm
)


def normalize_scientific_notation(s):
    """Helper to normalize scientific notation strings for comparison."""
    import re
    # Handle formats like "3.2 × 10^9" or "32 × 10^8"
    match = re.match(r'([\d.]+)\s*×\s*10\^(\d+)', str(s))
    if match:
        coef = float(match.group(1))
        exp = int(match.group(2))
        # Normalize coefficient to be between 1 and 10
        while coef >= 10:
            coef /= 10
            exp += 1
        while coef < 1 and coef > 0:
            coef *= 10
            exp -= 1
        return f"{coef} × 10^{exp}"
    return str(s)


def test_all_templates():
    """Test all problem templates."""
    print("="*80)
    print("TESTING ADD-COEFFICIENTS-WHEN-MULTIPLYING: ALL TEMPLATES")
    print("="*80)

    malrule = AddCoefficientsWhenMultiplyingMalrule()
    correct_algo = ScientificNotationMultiplicationCorrectAlgorithm()
    generator = AddCoefficientsWhenMultiplyingProblemGenerator(
        level=7,
        difficulty=DifficultyLevel.MEDIUM
    )

    # Test each template type
    templates = [
        'basic_multiplication',
        'word_problem_context',
        'multiple_step_calculation',
        'compare_results',
        'area_volume_calculation'
    ]

    all_passed = True
    test_num = 1

    for template_name in templates:
        print(f"\n{'='*80}")
        print(f"TEST {test_num}: Template '{template_name}'")
        print(f"{'='*80}")

        # Generate problem for this template
        seed = 2000 + test_num
        problem = generator.generate(seed=seed, template=template_name)

        print(f"Problem: {problem.text[:100]}...")

        # Run algorithms
        correct_sol = correct_algo.solve(problem)
        malrule_sol = malrule.solve(problem)

        # Get expected answers from metadata if available
        expected_correct = problem.metadata.get('correct_answer')
        expected_malrule = problem.metadata.get('malrule_answer')

        print(f"Computed correct answer: {correct_sol.answer}")
        print(f"Computed malrule answer: {malrule_sol.answer}")

        if expected_correct:
            print(f"Expected correct answer: {expected_correct}")
        if expected_malrule:
            print(f"Expected malrule answer: {expected_malrule}")

        # Check if test passes
        test_passed = True
        failure_reason = []

        # Verify answers are different (catch edge case)
        norm_correct = normalize_scientific_notation(correct_sol.answer)
        norm_malrule = normalize_scientific_notation(malrule_sol.answer)

        if norm_correct == norm_malrule:
            test_passed = False
            failure_reason.append(
                f"Edge case: Malrule produced same answer as correct! "
                f"Both got {correct_sol.answer}"
            )

        # If we have expected answers, verify they match
        if expected_correct:
            norm_expected_correct = normalize_scientific_notation(expected_correct)
            if norm_correct != norm_expected_correct:
                test_passed = False
                failure_reason.append(
                    f"Correct algorithm mismatch: got {correct_sol.answer}, "
                    f"expected {expected_correct}"
                )

        if expected_malrule:
            norm_expected_malrule = normalize_scientific_notation(expected_malrule)
            if norm_malrule != norm_expected_malrule:
                test_passed = False
                failure_reason.append(
                    f"Malrule algorithm mismatch: got {malrule_sol.answer}, "
                    f"expected {expected_malrule}"
                )

        if test_passed:
            print(f"✓ TEST PASSED")
            print(f"  Correct: {correct_sol.answer}")
            print(f"  Malrule: {malrule_sol.answer}")
        else:
            all_passed = False
            print(f"✗ TEST FAILED")
            for reason in failure_reason:
                print(f"  Reason: {reason}")

            print(f"\n  Correct algorithm steps:")
            for step in correct_sol.steps[:10]:  # Print first 10 steps
                print(f"    {step}")
            if len(correct_sol.steps) > 10:
                print(f"    ... ({len(correct_sol.steps) - 10} more steps)")

            print(f"\n  Malrule algorithm steps:")
            for step in malrule_sol.steps[:10]:
                print(f"    {step}")
            if len(malrule_sol.steps) > 10:
                print(f"    ... ({len(malrule_sol.steps) - 10} more steps)")

        test_num += 1

    print(f"\n{'='*80}")
    if all_passed:
        print("ALL TEMPLATE TESTS PASSED ✓")
    else:
        print("SOME TESTS FAILED ✗")
    print(f"{'='*80}")

    return all_passed


def test_specific_cases():
    """Test specific multiplication cases."""
    print("\n\n" + "="*80)
    print("TESTING SPECIFIC CASES")
    print("="*80)

    malrule = AddCoefficientsWhenMultiplyingMalrule()
    correct_algo = ScientificNotationMultiplicationCorrectAlgorithm()

    test_cases = [
        {
            'name': '(4×10³) × (8×10⁵)',
            'problem': Problem(
                text="Multiply (4 × 10^3) × (8 × 10^5)",
                operands=[4.0, 3, 8.0, 5],
                operation='scientific_notation_multiplication',
                level=8,
                difficulty=DifficultyLevel.MEDIUM,
                metadata={}
            ),
            'expected_correct': '3.2 × 10^9',  # 4*8=32, 32×10^8 = 3.2×10^9
            'expected_malrule': '1.2 × 10^9',  # 4+8=12, 12×10^8 = 1.2×10^9
        },
        {
            'name': '(2×10²) × (3×10⁴)',
            'problem': Problem(
                text="Multiply (2 × 10^2) × (3 × 10^4)",
                operands=[2.0, 2, 3.0, 4],
                operation='scientific_notation_multiplication',
                level=7,
                difficulty=DifficultyLevel.EASY,
                metadata={}
            ),
            'expected_correct': '6.0 × 10^6',  # 2*3=6
            'expected_malrule': '5.0 × 10^6',  # 2+3=5
        },
        {
            'name': '(5×10¹) × (5×10²)',
            'problem': Problem(
                text="Multiply (5 × 10^1) × (5 × 10^2)",
                operands=[5.0, 1, 5.0, 2],
                operation='scientific_notation_multiplication',
                level=7,
                difficulty=DifficultyLevel.MEDIUM,
                metadata={}
            ),
            'expected_correct': '2.5 × 10^4',  # 5*5=25, 25×10^3 = 2.5×10^4
            'expected_malrule': '1.0 × 10^4',  # 5+5=10, 10×10^3 = 1.0×10^4
        },
    ]

    all_passed = True

    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['name']}")
        problem = test_case['problem']

        correct_sol = correct_algo.solve(problem)
        malrule_sol = malrule.solve(problem)

        test_passed = True

        # Normalize for comparison
        norm_correct = normalize_scientific_notation(correct_sol.answer)
        norm_expected_correct = normalize_scientific_notation(test_case['expected_correct'])
        norm_malrule = normalize_scientific_notation(malrule_sol.answer)
        norm_expected_malrule = normalize_scientific_notation(test_case['expected_malrule'])

        if norm_correct != norm_expected_correct:
            test_passed = False
            all_passed = False
            print(f"  ✗ Correct algorithm failed: got {correct_sol.answer}, "
                  f"expected {test_case['expected_correct']}")
            print(f"  Steps:")
            for step in correct_sol.steps[:5]:
                print(f"    {step}")

        if norm_malrule != norm_expected_malrule:
            test_passed = False
            all_passed = False
            print(f"  ✗ Malrule algorithm failed: got {malrule_sol.answer}, "
                  f"expected {test_case['expected_malrule']}")
            print(f"  Steps:")
            for step in malrule_sol.steps[:5]:
                print(f"    {step}")

        if norm_correct == norm_malrule:
            test_passed = False
            all_passed = False
            print(f"  ✗ Edge case: Both algorithms produced same answer")

        if test_passed:
            print(f"  ✓ PASSED - Correct: {correct_sol.answer}, Malrule: {malrule_sol.answer}")

    print(f"\n{'='*80}")
    if all_passed:
        print("ALL SPECIFIC TESTS PASSED ✓")
    else:
        print("SOME TESTS FAILED ✗")
    print(f"{'='*80}")

    return all_passed


def main():
    print("\n╔" + "═"*78 + "╗")
    print("║" + "  COMPREHENSIVE TEST: Add-Coefficients-When-Multiplying  ".center(78) + "║")
    print("╚" + "═"*78 + "╝\n")

    try:
        template_tests_passed = test_all_templates()
        specific_tests_passed = test_specific_cases()

        print("\n\n╔" + "═"*78 + "╗")
        if template_tests_passed and specific_tests_passed:
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
