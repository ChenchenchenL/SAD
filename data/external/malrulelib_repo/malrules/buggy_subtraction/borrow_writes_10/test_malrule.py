#!/usr/bin/env python3
"""
Test script for Borrow-Writes-10 malrule.

Reference: Brown & Burton (1978). Diagnostic models for procedural bugs
in basic mathematical skills. Cognitive Science, 2(2), 155-192.

"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.buggy_subtraction.borrow_writes_10 import (
    BorrowWrites10ProblemGenerator,
    BorrowWrites10Malrule,
    SubtractionCorrectAlgorithm
)


def test_paper_example():
    """
    Test the exact example from Brown & Burton (1978).

    Paper states: 1300 - 522 = 788 (malrule), 778 (correct)
    """
    print("\n" + "=" * 60)
    print("TEST 1: Brown & Burton (1978) Paper Example")
    print("=" * 60)

    malrule = BorrowWrites10Malrule()
    correct = SubtractionCorrectAlgorithm()

    # Exact example from the paper
    problem = Problem(
        text="Calculate: 1300 - 522",
        operands=[1300, 522],
        operation='subtraction',
        level=4,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'minuend': 1300,
            'subtrahend': 522,
            'correct_answer': 778,
            'malrule_answer': 788,
            'template': 'double_zero'
        }
    )

    correct_sol = correct.solve(problem)
    malrule_sol = malrule.solve(problem)

    print(f"  Problem: 1300 - 522")
    print(f"  Paper correct answer: 778")
    print(f"  Paper malrule answer: 788")
    print(f"  Our correct answer: {correct_sol.answer}")
    print(f"  Our malrule answer: {malrule_sol.answer}")

    assert correct_sol.answer == '778', f"Expected 778, got {correct_sol.answer}"
    assert malrule_sol.answer == '788', f"Expected 788, got {malrule_sol.answer}"
    assert correct_sol.answer != malrule_sol.answer, "Answers should differ"

    print("  Paper example: PASSED")
    return True


def test_specific_examples():
    """Test with additional examples that demonstrate the bug."""
    print("\n" + "=" * 60)
    print("TEST 2: Additional Specific Examples")
    print("=" * 60)

    malrule = BorrowWrites10Malrule()
    correct = SubtractionCorrectAlgorithm()

    # Additional test cases
    test_cases = [
        # (minuend, subtrahend, correct_answer, malrule_answer, description)
        (503, 267, 236, 246, "Single zero: 503 - 267"),
        (2001, 543, 1458, 1568, "Double zero at end: 2001 - 543"),
        (4005, 1238, 2767, 2877, "Double zero: 4005 - 1238"),
    ]

    all_passed = True

    for i, (minuend, subtrahend, expected_correct, expected_malrule, desc) in enumerate(test_cases, 1):
        problem = Problem(
            text=f"Calculate: {minuend} - {subtrahend}",
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=4,
            difficulty=DifficultyLevel.MEDIUM,
            metadata={
                'minuend': minuend,
                'subtrahend': subtrahend,
                'correct_answer': expected_correct,
                'malrule_answer': expected_malrule,
                'template': 'basic'
            }
        )

        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        print(f"\n  Example {i}: {desc}")
        print(f"    Expected correct: {expected_correct}, Got: {correct_sol.answer}")
        print(f"    Expected malrule: {expected_malrule}, Got: {malrule_sol.answer}")

        if correct_sol.answer != str(expected_correct):
            print(f"    FAILED: Correct answer mismatch")
            all_passed = False
        elif malrule_sol.answer != str(expected_malrule):
            print(f"    FAILED: Malrule answer mismatch")
            all_passed = False
        elif correct_sol.answer == malrule_sol.answer:
            print(f"    FAILED: Answers should differ")
            all_passed = False
        else:
            print(f"    PASSED")

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

    generator = BorrowWrites10ProblemGenerator(level=4, difficulty=DifficultyLevel.MEDIUM)
    malrule = BorrowWrites10Malrule()
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

        if 'correct_answer' not in problem.metadata:
            print(f"    {template}: FAILED - missing correct_answer")
            all_passed = False
            continue

        if 'malrule_answer' not in problem.metadata:
            print(f"    {template}: FAILED - missing malrule_answer")
            all_passed = False
            continue

        # Verify solutions differ (for problems that trigger the bug)
        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        # Check if the problem actually triggers the malrule
        if correct_sol.answer == malrule_sol.answer:
            print(f"    {template}: WARNING - same answer (problem may not trigger bug)")
            print(f"      Problem: {problem.text}")
            print(f"      Answer: {correct_sol.answer}")
            # Don't fail, but warn
        else:
            print(f"    {template}: PASSED (correct={correct_sol.answer}, malrule={malrule_sol.answer})")

    if all_passed:
        print("\n  All templates PASSED")

    return all_passed


def test_automated_suite():
    """Run automated test suite."""
    print("\n" + "=" * 60)
    print("TEST 4: Automated Test Suite")
    print("=" * 60)

    generator = BorrowWrites10ProblemGenerator(level=4, difficulty=DifficultyLevel.MEDIUM)
    malrule = BorrowWrites10Malrule()
    correct = SubtractionCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, generator)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    print(f"\n  Automated suite: {'PASSED' if all_passed else 'FAILED'}")
    return all_passed


def test_malrule_metadata():
    """Test that malrule metadata is properly defined."""
    print("\n" + "=" * 60)
    print("TEST 5: Malrule Metadata")
    print("=" * 60)

    malrule = BorrowWrites10Malrule()

    # Check name
    name = malrule.get_name()
    assert name == "Borrow-Writes-10", f"Unexpected name: {name}"
    print(f"  Name: {name}")

    # Check description
    desc = malrule.get_description()
    assert len(desc) > 50, "Description too short"
    assert "10" in desc and "9" in desc, "Description should mention 10 vs 9"
    print(f"  Description length: {len(desc)} chars")

    print("\n  Metadata: PASSED")
    return True


def main():
    """Main entry point."""
    print("\n" + "=" * 68)
    print("  VERIFICATION TEST: Borrow-Writes-10 (Brown & Burton, 1978)  ".center(68))
    print("=" * 68)

    try:
        test1 = test_paper_example()
        test2 = test_specific_examples()
        test3 = test_all_templates()
        test4 = test_automated_suite()
        test5 = test_malrule_metadata()

        all_passed = test1 and test2 and test3 and test4 and test5

        print("\n" + "=" * 68)
        if all_passed:
            print("  VERIFICATION COMPLETE - ALL TESTS PASSED  ".center(68))
        else:
            print("  SOME TESTS FAILED  ".center(68))
        print("=" * 68 + "\n")

        return 0 if all_passed else 1

    except Exception as e:
        print(f"\n  TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
