#!/usr/bin/env python3
"""
Test script for Left-Ten-OK malrule.

Reference: Brown & Burton (1978). Diagnostic models for procedural bugs
in basic mathematical skills. Cognitive Science, 2(2), 155-192.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.buggy_subtraction.left_ten_ok import (
    LeftTenOkProblemGenerator,
    LeftTenOkMalrule,
    SubtractionCorrectAlgorithm
)


def test_paper_example():
    """
    Test the exact example from Brown & Burton (1978).

    Paper states: 803 - 508 = 395 (malrule), correct = 295
    """
    print("\n" + "=" * 68)
    print("TEST 1: Brown & Burton (1978) Paper Example")
    print("=" * 68)

    malrule = LeftTenOkMalrule()
    correct = SubtractionCorrectAlgorithm()

    # Exact example from the paper
    problem = Problem(
        text="Calculate: 803 - 508",
        operands=[803, 508],
        operation='subtraction',
        level=4,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'minuend': 803,
            'subtrahend': 508,
            'correct_answer': 295,
            'malrule_answer': 395,
            'template': 'zero_not_part_of_left_ten',
            'bug_applies': True,
        }
    )

    correct_sol = correct.solve(problem)
    malrule_sol = malrule.solve(problem)

    print(f"  Problem: 803 - 508")
    print(f"  Expected correct: 295")
    print(f"  Expected malrule: 395")
    print(f"  Got correct: {correct_sol.answer}")
    print(f"  Got malrule: {malrule_sol.answer}")

    assert correct_sol.answer == '295', f"Expected correct=295, got {correct_sol.answer}"
    assert malrule_sol.answer == '395', f"Expected malrule=395, got {malrule_sol.answer}"
    assert correct_sol.answer != malrule_sol.answer, "Answers should differ"

    print("  Paper example: PASSED")
    return True


def test_left_ten_pattern():
    """
    Test that the bug does NOT apply when zero is part of "10" at left.

    For problems like 1003 - 508, the "10" at the left should be handled
    correctly, so malrule answer equals correct answer.
    """
    print("\n" + "=" * 68)
    print("TEST 2: Left-Ten Pattern (Bug Should NOT Apply)")
    print("=" * 68)

    malrule = LeftTenOkMalrule()
    correct = SubtractionCorrectAlgorithm()

    # Problem where "10" is at the leftmost position
    problem = Problem(
        text="Calculate: 1003 - 508",
        operands=[1003, 508],
        operation='subtraction',
        level=4,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'minuend': 1003,
            'subtrahend': 508,
            'correct_answer': 495,
            'malrule_answer': 495,  # Same because bug doesn't apply
            'template': 'zero_part_of_left_ten',
            'bug_applies': False,
        }
    )

    correct_sol = correct.solve(problem)
    malrule_sol = malrule.solve(problem)

    print(f"  Problem: 1003 - 508")
    print(f"  Expected both: 495 (bug doesn't apply for '10' at left)")
    print(f"  Got correct: {correct_sol.answer}")
    print(f"  Got malrule: {malrule_sol.answer}")

    assert correct_sol.answer == '495', f"Expected correct=495, got {correct_sol.answer}"
    assert malrule_sol.answer == '495', f"Expected malrule=495, got {malrule_sol.answer}"
    # For this case, answers SHOULD be the same

    print("  Left-Ten pattern: PASSED")
    return True


def test_additional_examples():
    """
    Test additional examples where the bug applies.
    """
    print("\n" + "=" * 68)
    print("TEST 3: Additional Examples (Bug Applies)")
    print("=" * 68)

    malrule = LeftTenOkMalrule()
    correct = SubtractionCorrectAlgorithm()

    # Test cases where bug applies (zero NOT part of "10" at left)
    test_cases = [
        # (minuend, subtrahend, expected_correct, expected_malrule)
        (503, 267, 236, 336),   # 503 - 267: 0->9 without borrow from 5
        (402, 156, 246, 346),   # 402 - 156: 0->9 without borrow from 4
        (901, 456, 445, 545),   # 901 - 456: 0->9 without borrow from 9
        (704, 328, 376, 476),   # 704 - 328: 0->9 without borrow from 7
    ]

    all_passed = True
    for minuend, subtrahend, exp_correct, exp_malrule in test_cases:
        problem = Problem(
            text=f"Calculate: {minuend} - {subtrahend}",
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=4,
            difficulty=DifficultyLevel.MEDIUM,
            metadata={
                'minuend': minuend,
                'subtrahend': subtrahend,
                'correct_answer': exp_correct,
                'malrule_answer': exp_malrule,
                'template': 'zero_not_part_of_left_ten',
                'bug_applies': True,
            }
        )

        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        correct_match = (correct_sol.answer == str(exp_correct))
        malrule_match = (malrule_sol.answer == str(exp_malrule))

        if correct_match and malrule_match:
            print(f"  {minuend} - {subtrahend}: PASSED (correct={exp_correct}, malrule={exp_malrule})")
        else:
            print(f"  {minuend} - {subtrahend}: FAILED")
            print(f"    Expected: correct={exp_correct}, malrule={exp_malrule}")
            print(f"    Got: correct={correct_sol.answer}, malrule={malrule_sol.answer}")
            all_passed = False

    if all_passed:
        print("\n  All additional examples: PASSED")
    return all_passed


def test_all_templates():
    """Test all problem templates generate valid problems."""
    print("\n" + "=" * 68)
    print("TEST 4: Template Generation")
    print("=" * 68)

    generator = LeftTenOkProblemGenerator(level=4, difficulty=DifficultyLevel.MEDIUM)
    malrule = LeftTenOkMalrule()
    correct = SubtractionCorrectAlgorithm()

    templates = generator.get_available_templates()
    print(f"  Testing {len(templates)} templates: {templates}")

    all_passed = True
    for i, template in enumerate(templates):
        problem = generator.generate(seed=42 + i)

        # Verify problem structure
        assert problem.text, f"Template {template}: missing text"
        assert problem.operands, f"Template {template}: missing operands"
        assert 'correct_answer' in problem.metadata, f"Template {template}: missing correct_answer"
        assert 'malrule_answer' in problem.metadata, f"Template {template}: missing malrule_answer"

        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        # For "left_ten" templates, answers may be same (bug doesn't apply)
        bug_applies = problem.metadata.get('bug_applies', True)

        if bug_applies:
            if correct_sol.answer == malrule_sol.answer:
                print(f"    {template}: FAILED - answers should differ when bug applies")
                all_passed = False
            else:
                print(f"    {template}: PASSED (correct={correct_sol.answer}, malrule={malrule_sol.answer})")
        else:
            # Bug doesn't apply - answers should be same
            if correct_sol.answer == malrule_sol.answer:
                print(f"    {template}: PASSED (both={correct_sol.answer}, bug doesn't apply)")
            else:
                print(f"    {template}: FAILED - answers should match when bug doesn't apply")
                all_passed = False

    if all_passed:
        print("\n  All templates: PASSED")
    return all_passed


def test_automated_suite():
    """Run automated test suite."""
    print("\n" + "=" * 68)
    print("TEST 5: Automated Test Suite")
    print("=" * 68)

    generator = LeftTenOkProblemGenerator(level=4, difficulty=DifficultyLevel.MEDIUM)
    malrule = LeftTenOkMalrule()
    correct = SubtractionCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, generator)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    print(f"\n  Automated suite: {'PASSED' if all_passed else 'FAILED'}")
    return all_passed


def main():
    """Main entry point."""
    print("\n" + "=" * 68)
    print("  VERIFICATION TEST: Left-Ten-OK (Brown & Burton, 1978)  ".center(68))
    print("=" * 68)
    print("\nDescription: Student changes 0 to 9 without further borrowing")
    print("UNLESS the 0 is part of '10' in the left part of the top number.")
    print("Example from paper: 803 - 508 = 395 (correct: 295)")

    try:
        test1 = test_paper_example()
        test2 = test_left_ten_pattern()
        test3 = test_additional_examples()
        test4 = test_all_templates()
        test5 = test_automated_suite()

        all_passed = test1 and test2 and test3 and test4 and test5

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
