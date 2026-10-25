#!/usr/bin/env python3
"""Test script for Keep-Common-Denominator-For-Multiplication malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.fractions.keep_common_denominator_for_multiplication import (
    KeepCommonDenominatorForMultiplicationProblemGenerator,
    KeepCommonDenominatorForMultiplicationMalrule,
    FractionMultiplicationCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING KEEP-COMMON-DENOMINATOR-FOR-MULTIPLICATION")
    print("="*70)

    malrule = KeepCommonDenominatorForMultiplicationMalrule()
    correct = FractionMultiplicationCorrectAlgorithm()

    # Test case 1: 2/5 × 3/5 = 6/25 (correct), 6/5 (malrule)
    problem1 = Problem(
        text="Multiply: 2/5 × 3/5",
        operands=[2, 5, 3, 5],
        operation='fraction_multiplication',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'numerator1': 2,
            'numerator2': 3,
            'denominator': 5,
            'correct_numerator': 6,
            'correct_denominator': 25,
            'malrule_numerator': 6,
            'malrule_denominator': 5
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: 2/5 × 3/5 → Correct: {correct_sol.answer}, Malrule: {malrule_sol.answer}")
    assert correct_sol.answer == "6/25"
    assert malrule_sol.answer == "6/5"
    assert correct_sol.answer != malrule_sol.answer
    print("✓ PASSED")

    # Test case 2: 1/3 × 2/3 = 2/9 (correct), 2/3 (malrule)
    problem2 = Problem(
        text="Multiply: 1/3 × 2/3",
        operands=[1, 3, 2, 3],
        operation='fraction_multiplication',
        level=5,
        difficulty=DifficultyLevel.EASY,
        metadata={
            'numerator1': 1,
            'numerator2': 2,
            'denominator': 3,
            'correct_numerator': 2,
            'correct_denominator': 9,
            'malrule_numerator': 2,
            'malrule_denominator': 3
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert correct_sol2.answer == "2/9"
    assert malrule_sol2.answer == "2/3"
    print("✓ TEST 2 PASSED")

    # Test case 3: 3/4 × 2/4 = 6/16 = 3/8 (correct), 6/4 = 3/2 (malrule)
    problem3 = Problem(
        text="Multiply: 3/4 × 2/4",
        operands=[3, 4, 2, 4],
        operation='fraction_multiplication',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'numerator1': 3,
            'numerator2': 2,
            'denominator': 4,
            'correct_numerator': 3,
            'correct_denominator': 8,
            'malrule_numerator': 3,
            'malrule_denominator': 2
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert correct_sol3.answer == "3/8"
    assert malrule_sol3.answer == "3/2"
    print("✓ TEST 3 PASSED")

    # Test case 4: 2/7 × 3/7 = 6/49 (correct), 6/7 (malrule)
    problem4 = Problem(
        text="Multiply: 2/7 × 3/7",
        operands=[2, 7, 3, 7],
        operation='fraction_multiplication',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'numerator1': 2,
            'numerator2': 3,
            'denominator': 7,
            'correct_numerator': 6,
            'correct_denominator': 49,
            'malrule_numerator': 6,
            'malrule_denominator': 7
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    assert correct_sol4.answer == "6/49"
    assert malrule_sol4.answer == "6/7"
    print("✓ TEST 4 PASSED")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_automated_suite():
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = KeepCommonDenominatorForMultiplicationProblemGenerator(
        level=6,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = KeepCommonDenominatorForMultiplicationMalrule()
    correct = FractionMultiplicationCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Keep-Common-Denominator-For-Multiplication  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    try:
        test_specific_examples()
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
