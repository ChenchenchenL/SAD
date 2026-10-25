#!/usr/bin/env python3
"""Test script for Common-Denominator-Numerator malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.fractions.common_denominator_numerator import (
    CommonDenominatorNumeratorProblemGenerator,
    CommonDenominatorNumeratorMalrule,
    FractionAdditionCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING COMMON-DENOMINATOR-NUMERATOR")
    print("="*70)

    malrule = CommonDenominatorNumeratorMalrule()
    correct = FractionAdditionCorrectAlgorithm()

    # Test case 1: 1/4 + 1/6 = 5/12 (correct), 1/5 (malrule: 2/10 simplified)
    problem1 = Problem(
        text="Calculate: 1/4 + 1/6",
        operands=[1, 4, 1, 6],
        operation='fraction_addition',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'numer1': 1,
            'denom1': 4,
            'numer2': 1,
            'denom2': 6,
            'correct_numer': 5,
            'correct_denom': 12,
            'malrule_numer': 1,  # 2/10 = 1/5
            'malrule_denom': 5,
            'lcd': 12,
            'template': 'basic_addition'
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: 1/4 + 1/6 → Correct: {correct_sol.answer}, Malrule: {malrule_sol.answer}")
    assert correct_sol.answer == "5/12"
    assert malrule_sol.answer == "1/5"
    assert correct_sol.answer != malrule_sol.answer
    print("✓ PASSED")

    # Test case 2: 1/3 + 1/4 = 7/12 (correct), 2/7 (malrule)
    problem2 = Problem(
        text="Calculate: 1/3 + 1/4",
        operands=[1, 3, 1, 4],
        operation='fraction_addition',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'numer1': 1,
            'denom1': 3,
            'numer2': 1,
            'denom2': 4,
            'correct_numer': 7,
            'correct_denom': 12,
            'malrule_numer': 2,
            'malrule_denom': 7,
            'lcd': 12,
            'template': 'basic_addition'
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert correct_sol2.answer == "7/12"
    assert malrule_sol2.answer == "2/7"
    print("✓ TEST 2 PASSED")

    # Test case 3: 2/5 + 1/3 = 11/15 (correct), 3/8 (malrule)
    problem3 = Problem(
        text="Calculate: 2/5 + 1/3",
        operands=[2, 5, 1, 3],
        operation='fraction_addition',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'numer1': 2,
            'denom1': 5,
            'numer2': 1,
            'denom2': 3,
            'correct_numer': 11,
            'correct_denom': 15,
            'malrule_numer': 3,
            'malrule_denom': 8,
            'lcd': 15,
            'template': 'basic_addition'
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert correct_sol3.answer == "11/15"
    assert malrule_sol3.answer == "3/8"
    print("✓ TEST 3 PASSED")

    # Test case 4: 1/2 + 1/3 = 5/6 (correct), 2/5 (malrule)
    problem4 = Problem(
        text="Calculate: 1/2 + 1/3",
        operands=[1, 2, 1, 3],
        operation='fraction_addition',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'numer1': 1,
            'denom1': 2,
            'numer2': 1,
            'denom2': 3,
            'correct_numer': 5,
            'correct_denom': 6,
            'malrule_numer': 2,
            'malrule_denom': 5,
            'lcd': 6,
            'template': 'basic_addition'
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    assert correct_sol4.answer == "5/6"
    assert malrule_sol4.answer == "2/5"
    print("✓ TEST 4 PASSED")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_all_templates():
    """Test all 5 templates for Common-Denominator-Numerator."""
    print("\n\n" + "="*70)
    print("TESTING ALL TEMPLATES")
    print("="*70)

    problem_gen = CommonDenominatorNumeratorProblemGenerator(
        level=6,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = CommonDenominatorNumeratorMalrule()
    correct = FractionAdditionCorrectAlgorithm()

    templates = problem_gen.get_available_templates()
    print(f"\nFound {len(templates)} templates: {templates}")
    assert len(templates) == 6, f"Expected 6 templates, got {len(templates)}"

    for template in templates:
        print(f"\n--- Testing template: {template} ---")

        # Generate problem with this template
        problem = problem_gen.generate(seed=42, template=template)

        # Solve with both algorithms
        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        # Verify answers
        print(f"  Problem: {problem.text[:80]}...")
        print(f"  Correct answer: {correct_sol.answer}")
        print(f"  Malrule answer: {malrule_sol.answer}")

        # Verify different answers
        assert str(correct_sol.answer) != str(malrule_sol.answer), \
            f"Template {template}: Correct and malrule answers should be different!"

        # Verify calculate_expected_answer matches malrule output
        expected = malrule.calculate_expected_answer(problem)
        print(f"  Expected answer: {expected}")

        assert str(malrule_sol.answer) == str(expected), \
            f"Template {template}: calculate_expected_answer() returned {expected} but malrule produced {malrule_sol.answer}"

        print(f"  ✓ Template {template} PASSED")

    print("\n" + "="*70)
    print("ALL TEMPLATE TESTS PASSED ✓")
    print("="*70)


def test_automated_suite():
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = CommonDenominatorNumeratorProblemGenerator(
        level=6,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = CommonDenominatorNumeratorMalrule()
    correct = FractionAdditionCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Common-Denominator-Numerator  ".center(70) + "║")
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
