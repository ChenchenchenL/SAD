#!/usr/bin/env python3
"""Test script for Always-Borrow-Left malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.subtraction.always_borrow_left import (
    AlwaysBorrowLeftProblemGenerator,
    AlwaysBorrowLeftMalrule,
    SubtractionCorrectAlgorithm
)


def create_problem(minuend, subtrahend):
    """Helper to create a Problem object."""
    return Problem(
        text=f"Calculate: {minuend} - {subtrahend}",
        operands=[minuend, subtrahend],
        operation='subtraction',
        level=3,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'minuend': minuend,
            'subtrahend': subtrahend,
            'correct_answer': minuend - subtrahend
        }
    )


def test_two_digit_examples():
    """Test 2-digit subtraction problems."""
    print("="*70)
    print("TESTING 2-DIGIT PROBLEMS")
    print("="*70)

    malrule = AlwaysBorrowLeftMalrule()
    correct = SubtractionCorrectAlgorithm()

    # Test cases: (minuend, subtrahend, expected_correct, expected_malrule)
    test_cases = [
        # Original test cases
        (85, 23, 62, 52),  # 7(15) - 23 = 52
        (96, 34, 62, 52),  # 8(16) - 34 = 52
        (74, 21, 53, 43),  # 6(14) - 21 = 43
        (67, 15, 52, 42),  # 5(17) - 15 = 42
        # Additional 2-digit cases
        (99, 11, 88, 78),  # 8(19) - 11 = 78
        (55, 22, 33, 23),  # 4(15) - 22 = 23
        (88, 44, 44, 34),  # 7(18) - 44 = 34
    ]

    for i, (minuend, subtrahend, exp_correct, exp_malrule) in enumerate(test_cases, 1):
        problem = create_problem(minuend, subtrahend)
        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        print(f"\nTEST {i}: {minuend} - {subtrahend}")
        print(f"  Correct: {correct_sol.answer} (expected {exp_correct})")
        print(f"  Malrule: {malrule_sol.answer} (expected {exp_malrule})")

        assert correct_sol.answer == str(exp_correct), f"Correct answer mismatch: {correct_sol.answer} != {exp_correct}"
        assert malrule_sol.answer == str(exp_malrule), f"Malrule answer mismatch: {malrule_sol.answer} != {exp_malrule}"
        assert correct_sol.answer != malrule_sol.answer, "Malrule should differ from correct"
        print("  ✓ PASSED")

    print("\n" + "="*70)
    print("ALL 2-DIGIT TEST CASES PASSED ✓")
    print("="*70)


def test_three_digit_examples():
    """Test 3-digit subtraction problems."""
    print("\n" + "="*70)
    print("TESTING 3-DIGIT PROBLEMS")
    print("="*70)

    malrule = AlwaysBorrowLeftMalrule()
    correct = SubtractionCorrectAlgorithm()

    # For 3-digit: malrule borrows in ones AND tens columns
    # 987 - 543: ones: 7+10=17-3=14→4, tens: 8-1=7
    #            tens: 7+10=17-4=13→3, hundreds: 9-1=8
    #            hundreds: 8-5=3
    #            Result: 334 (correct: 444)
    test_cases = [
        (987, 543, 444, 334),  # Borrows twice unnecessarily
        # 876-432: ones: 6+10=16-2=14→4, tens: 7-1=6, 6+10=16-3=13→3, hundreds: 8-1=7, 7-4=3 → 334
        (876, 432, 444, 334),
        # 999-111: ones: 9+10=19-1=18→8, tens: 9-1=8, 8+10=18-1=17→7, hundreds: 9-1=8, 8-1=7 → 778
        (999, 111, 888, 778),
        # 654-321: ones: 4+10=14-1=13→3, tens: 5-1=4, 4+10=14-2=12→2, hundreds: 6-1=5, 5-3=2 → 223
        (654, 321, 333, 223),
        # 753-241: ones: 3+10=13-1=12→2, tens: 5-1=4, 4+10=14-4=10→0, hundreds: 7-1=6, 6-2=4 → 402
        (753, 241, 512, 402),
    ]

    for i, (minuend, subtrahend, exp_correct, exp_malrule) in enumerate(test_cases, 1):
        problem = create_problem(minuend, subtrahend)
        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        print(f"\nTEST {i}: {minuend} - {subtrahend}")
        print(f"  Correct: {correct_sol.answer} (expected {exp_correct})")
        print(f"  Malrule: {malrule_sol.answer} (expected {exp_malrule})")

        assert correct_sol.answer == str(exp_correct), f"Correct answer mismatch: {correct_sol.answer} != {exp_correct}"
        assert malrule_sol.answer == str(exp_malrule), f"Malrule answer mismatch: {malrule_sol.answer} != {exp_malrule}"
        assert correct_sol.answer != malrule_sol.answer, "Malrule should differ from correct"
        print("  ✓ PASSED")

    print("\n" + "="*70)
    print("ALL 3-DIGIT TEST CASES PASSED ✓")
    print("="*70)


def test_four_digit_examples():
    """Test 4-digit subtraction problems."""
    print("\n" + "="*70)
    print("TESTING 4-DIGIT PROBLEMS")
    print("="*70)

    malrule = AlwaysBorrowLeftMalrule()
    correct = SubtractionCorrectAlgorithm()

    # For 4-digit: malrule borrows in ones, tens, AND hundreds columns
    # 9876 - 5432:
    #   ones: 6+10=16-2=14→4, tens: 7-1=6
    #   tens: 6+10=16-3=13→3, hundreds: 8-1=7
    #   hundreds: 7+10=17-4=13→3, thousands: 9-1=8
    #   thousands: 8-5=3
    #   Result: 3334 (correct: 4444)
    test_cases = [
        (9876, 5432, 4444, 3334),
        (8765, 4321, 4444, 3334),
        (9999, 1111, 8888, 7778),
        (5555, 2222, 3333, 2223),
        (7654, 3210, 4444, 3334),
    ]

    for i, (minuend, subtrahend, exp_correct, exp_malrule) in enumerate(test_cases, 1):
        problem = create_problem(minuend, subtrahend)
        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        print(f"\nTEST {i}: {minuend} - {subtrahend}")
        print(f"  Correct: {correct_sol.answer} (expected {exp_correct})")
        print(f"  Malrule: {malrule_sol.answer} (expected {exp_malrule})")

        assert correct_sol.answer == str(exp_correct), f"Correct answer mismatch: {correct_sol.answer} != {exp_correct}"
        assert malrule_sol.answer == str(exp_malrule), f"Malrule answer mismatch: {malrule_sol.answer} != {exp_malrule}"
        assert correct_sol.answer != malrule_sol.answer, "Malrule should differ from correct"
        print("  ✓ PASSED")

    print("\n" + "="*70)
    print("ALL 4-DIGIT TEST CASES PASSED ✓")
    print("="*70)


def test_edge_cases():
    """Test edge cases with small and large digit values."""
    print("\n" + "="*70)
    print("TESTING EDGE CASES")
    print("="*70)

    malrule = AlwaysBorrowLeftMalrule()
    correct = SubtractionCorrectAlgorithm()

    # Edge cases
    test_cases = [
        # Small numbers - 32-10: ones: 2+10=12-0=12→2, tens: 3-1=2, 2-1=1 → 12
        (32, 10, 22, 12),
        # Large digit values - 98-12: 8+10=18-2=16→6, 9-1=8-1=7 → 76
        (98, 12, 86, 76),
        # Large digit values - 99-10: 9+10=19-0=19→9, 9-1=8-1=7 → 79
        (99, 10, 89, 79),
        # Zeros in subtrahend - 85-20: 5+10=15-0=15→5, 8-1=7-2=5 → 55
        (85, 20, 65, 55),
        # Zeros in subtrahend - 97-30: 7+10=17-0=17→7, 9-1=8-3=5 → 57
        (97, 30, 67, 57),
        # Ones digit is 0 in minuend - 80-30: 0+10=10-0=10→0, 8-1=7-3=4 → 40
        (80, 30, 50, 40),
        # Ones digit is 0 in minuend - 90-40: 0+10=10-0=10→0, 9-1=8-4=4 → 40
        (90, 40, 50, 40),
        # Small difference - 54-43: 4+10=14-3=11→1, 5-1=4-4=0 → 01=1
        (54, 43, 11, 1),
        # Small difference - 65-54: 5+10=15-4=11→1, 6-1=5-5=0 → 01=1
        (65, 54, 11, 1),
    ]

    for i, (minuend, subtrahend, exp_correct, exp_malrule) in enumerate(test_cases, 1):
        problem = create_problem(minuend, subtrahend)
        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        print(f"\nTEST {i}: {minuend} - {subtrahend}")
        print(f"  Correct: {correct_sol.answer} (expected {exp_correct})")
        print(f"  Malrule: {malrule_sol.answer} (expected {exp_malrule})")

        assert correct_sol.answer == str(exp_correct), f"Correct answer mismatch: {correct_sol.answer} != {exp_correct}"
        assert malrule_sol.answer == str(exp_malrule), f"Malrule answer mismatch: {malrule_sol.answer} != {exp_malrule}"
        print("  ✓ PASSED")

    print("\n" + "="*70)
    print("ALL EDGE CASE TESTS PASSED ✓")
    print("="*70)


def test_specific_examples():
    """Run all specific example tests."""
    test_two_digit_examples()
    test_three_digit_examples()
    test_four_digit_examples()
    test_edge_cases()


def test_automated_suite():
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = AlwaysBorrowLeftProblemGenerator(
        level=3,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = AlwaysBorrowLeftMalrule()
    correct = SubtractionCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Always-Borrow-Left  ".center(70) + "║")
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
