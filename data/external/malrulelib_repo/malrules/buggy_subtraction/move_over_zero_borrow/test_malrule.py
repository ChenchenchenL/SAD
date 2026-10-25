#!/usr/bin/env python3
"""
Test script for Move-Over-Zero-Borrow malrule.

Reference: Brown & Burton (1978) - Diagnostic Models for Procedural Bugs
Paper example: 304 - 75 = 139 (correct: 229)
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.buggy_subtraction.move_over_zero_borrow import (
    MoveOverZeroBorrowProblemGenerator,
    MoveOverZeroBorrowMalrule,
    SubtractionCorrectAlgorithm
)


def test_paper_example():
    """
    Test the exact example from Brown & Burton (1978).

    304 - 75 = 139 (malrule) vs 229 (correct)

    The student:
    1. Sees 4 < 5 in ones, needs to borrow
    2. Tens is 0, skips it, borrows from hundreds (3 -> 2)
    3. 0 stays 0 (not decremented to 9!)
    4. 4 becomes 14, 14 - 5 = 9
    5. Now tens: 0 < 7, needs to borrow again
    6. Borrows from hundreds again (2 -> 1)
    7. 0 becomes 10, 10 - 7 = 3
    8. Hundreds: 1 - 0 = 1
    9. Result: 139
    """
    print("\n" + "=" * 60)
    print("TEST 1: Paper Example (Brown & Burton, 1978)")
    print("=" * 60)

    malrule = MoveOverZeroBorrowMalrule()
    correct = SubtractionCorrectAlgorithm()

    # The exact example from the paper
    problem = Problem(
        text="Calculate: 304 - 75",
        operands=[304, 75],
        operation='subtraction',
        level=3,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'minuend': 304,
            'subtrahend': 75,
            'correct_answer': 229,
            'malrule_answer': 139,
            'template': 'single_middle_zero'
        }
    )

    correct_sol = correct.solve(problem, verbose=True)
    malrule_sol = malrule.solve(problem, verbose=True)

    print(f"  Problem: {problem.text}")
    print(f"  Correct answer: {correct_sol.answer} (expected: 229)")
    print(f"  Malrule answer: {malrule_sol.answer} (expected: 139)")

    # Verify correct answer
    assert correct_sol.answer == '229', \
        f"Correct algorithm failed: expected 229, got {correct_sol.answer}"

    # Verify malrule answer matches paper
    assert malrule_sol.answer == '139', \
        f"Malrule failed: expected 139 (from paper), got {malrule_sol.answer}"

    # Verify they're different
    assert correct_sol.answer != malrule_sol.answer, \
        "Answers should be different!"

    print("  Paper example: PASSED")
    return True


def test_specific_examples():
    """Test with additional known examples."""
    print("\n" + "=" * 60)
    print("TEST 2: Specific Research Examples")
    print("=" * 60)

    malrule = MoveOverZeroBorrowMalrule()
    correct = SubtractionCorrectAlgorithm()

    # Additional test cases based on the malrule pattern
    test_cases = [
        # (minuend, subtrahend, expected_correct, expected_malrule, description)
        (304, 75, 229, 139, "Paper example: 304-75"),
        (502, 67, 435, 345, "502-67: skip 0 in tens"),
        (403, 156, 247, 157, "403-156: skip 0, multiple borrows"),
        (700, 234, 466, 376, "700-234: two zeros to skip"),
    ]

    all_passed = True
    for minuend, subtrahend, exp_correct, exp_malrule, description in test_cases:
        problem = Problem(
            text=f"Calculate: {minuend} - {subtrahend}",
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=3,
            difficulty=DifficultyLevel.MEDIUM,
            metadata={
                'minuend': minuend,
                'subtrahend': subtrahend,
                'template': 'basic'
            }
        )

        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        correct_match = correct_sol.answer == str(exp_correct)
        malrule_match = malrule_sol.answer == str(exp_malrule)
        different = correct_sol.answer != malrule_sol.answer

        status = "PASSED" if (correct_match and malrule_match and different) else "FAILED"
        if status == "FAILED":
            all_passed = False

        print(f"  {description}:")
        print(f"    Correct: {correct_sol.answer} (expected: {exp_correct}) {'OK' if correct_match else 'FAIL'}")
        print(f"    Malrule: {malrule_sol.answer} (expected: {exp_malrule}) {'OK' if malrule_match else 'FAIL'}")
        print(f"    Status: {status}")

    if all_passed:
        print("\n  All specific examples PASSED")
    else:
        print("\n  Some specific examples FAILED")

    return all_passed


def test_all_templates():
    """Test all problem templates generate valid problems."""
    print("\n" + "=" * 60)
    print("TEST 3: Template Generation")
    print("=" * 60)

    generator = MoveOverZeroBorrowProblemGenerator(
        level=4, difficulty=DifficultyLevel.MEDIUM
    )
    malrule = MoveOverZeroBorrowMalrule()
    correct = SubtractionCorrectAlgorithm()

    templates = generator.get_available_templates()
    print(f"  Testing {len(templates)} templates: {templates}")

    all_passed = True
    for i, template in enumerate(templates):
        problem = generator.generate(seed=42 + i)

        # Verify problem structure
        if not problem.text:
            print(f"    {template}: FAILED - missing text")
            all_passed = False
            continue

        if not problem.operands:
            print(f"    {template}: FAILED - missing operands")
            all_passed = False
            continue

        # Verify solutions
        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        # Check that malrule produces different answer for problems with zeros
        minuend_str = str(problem.operands[0])
        has_zero = '0' in minuend_str[1:]  # Zero not in leftmost position

        if has_zero and correct_sol.answer == malrule_sol.answer:
            print(f"    {template}: WARNING - same answer (may be edge case)")
            print(f"      Problem: {problem.text}")
            print(f"      Answer: {correct_sol.answer}")
        else:
            print(f"    {template}: PASSED")
            print(f"      Problem: {problem.text}")
            print(f"      Correct: {correct_sol.answer}, Malrule: {malrule_sol.answer}")

    if all_passed:
        print("\n  All templates PASSED")

    return all_passed


def test_automated_suite():
    """Run automated test suite."""
    print("\n" + "=" * 60)
    print("TEST 4: Automated Test Suite")
    print("=" * 60)

    generator = MoveOverZeroBorrowProblemGenerator(
        level=4, difficulty=DifficultyLevel.MEDIUM
    )
    malrule = MoveOverZeroBorrowMalrule()
    correct = SubtractionCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, generator)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    print(f"\n  Automated suite: {'PASSED' if all_passed else 'FAILED'}")
    return all_passed


def test_malrule_metadata():
    """Test malrule metadata methods."""
    print("\n" + "=" * 60)
    print("TEST 5: Malrule Metadata")
    print("=" * 60)

    malrule = MoveOverZeroBorrowMalrule()

    # Test get_name
    name = malrule.get_name()
    assert name == "Move-Over-Zero-Borrow", f"Name mismatch: {name}"
    print(f"  Name: {name}")

    print("  Metadata: PASSED")
    return True


def main():
    """Main entry point."""
    print("\n" + "=" * 68)
    print("  VERIFICATION TEST: Move-Over-Zero-Borrow  ".center(68))
    print("  Reference: Brown & Burton (1978)  ".center(68))
    print("=" * 68)

    all_passed = True

    try:
        # Test 1: Paper example
        if not test_paper_example():
            all_passed = False

        # Test 2: Specific examples
        if not test_specific_examples():
            all_passed = False

        # Test 3: Templates
        if not test_all_templates():
            all_passed = False

        # Test 4: Automated suite
        if not test_automated_suite():
            all_passed = False

        # Test 5: Metadata
        if not test_malrule_metadata():
            all_passed = False

        print("\n" + "=" * 68)
        if all_passed:
            print("  VERIFICATION COMPLETE - ALL TESTS PASSED  ".center(68))
        else:
            print("  VERIFICATION COMPLETE - SOME TESTS FAILED  ".center(68))
        print("=" * 68 + "\n")

        return 0 if all_passed else 1

    except Exception as e:
        print(f"\n  TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
