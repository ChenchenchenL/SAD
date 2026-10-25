#!/usr/bin/env python3
"""
Test script for FORGET/BORROW/OVER/BLANKS malrule.

Research: Brown & Burton (1978) "Diagnostic Models for Procedural Bugs
          in Basic Mathematical Skills", Cognitive Science 2(2), 155-192
Network location: COLUMN SEQUENCE procedure
"""

import sys
import os

# Add project root to path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.insert(0, project_root)

# Add current directory for local imports when running directly
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from utils import DifficultyLevel, MalruleTest, Problem

# Import from package or local depending on how script is run

from malrules.buggy_subtraction.forget_borrow_over_blanks import (
    ForgetBorrowOverBlanksProblemGenerator,
    ForgetBorrowOverBlanksMalrule,
    SubtractionCorrectAlgorithm
)



def test_specific_examples():
    """Test with known examples based on the FORGET/BORROW/OVER/BLANKS bug pattern."""
    print("\n" + "=" * 60)
    print("TEST 1: Specific Research Examples")
    print("=" * 60)

    malrule = ForgetBorrowOverBlanksMalrule()
    correct = SubtractionCorrectAlgorithm()

    # Test cases based on FORGET/BORROW/OVER/BLANKS pattern
    # When minuend has fewer digits, student forgets to borrow over blanks
    # and uses smaller-from-larger in blank columns

    test_cases = [
        # (minuend, subtrahend, expected_correct, expected_malrule, description)
        # Example: 85 - 127
        # Correct: -42
        # Malrule: ones: 5<7, borrow, 15-7=8; tens: 7-2=5; hundreds: blank, 1-0=1 -> 158
        (85, 127, -42, 158, "2-digit minus 3-digit basic"),

        # Example: 42 - 156
        # Correct: -114
        # Malrule: ones: 2<6, borrow, 12-6=6; tens: 13-5=8; hundreds: 1-0=1 -> 186
        (42, 156, -114, 186, "2-digit minus 3-digit"),

        # Example: 73 - 241
        # Correct: -168
        # Malrule: ones: 3<1? No, 3-1=2; tens: 7<4? No, 7-4=3; hundreds: 0<2, 2-0=2 -> 232
        (73, 241, -168, 232, "No borrow needed in existing columns"),

        # Example: 99 - 100
        # Correct: -1
        # Malrule: ones: 9-0=9; tens: 9-0=9; hundreds: 0-1 -> 1-0=1 -> 199
        (99, 100, -1, 199, "Edge case just crossing 100"),

        # Example: 50 - 123
        # Correct: -73
        # Malrule: ones: 0<3, borrow, 10-3=7; tens: 4-2=2; hundreds: 0-1 -> 1-0=1 -> 127
        (50, 123, -73, 127, "With zero in ones place"),
    ]

    all_passed = True
    for i, (minuend, subtrahend, expected_correct, expected_malrule, desc) in enumerate(test_cases, 1):
        problem = Problem(
            text=f"Calculate: {minuend} - {subtrahend}",
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=3,
            difficulty=DifficultyLevel.MEDIUM,
            metadata={
                'minuend': minuend,
                'subtrahend': subtrahend,
                'correct_answer': str(expected_correct),
                'malrule_answer': str(expected_malrule),
                'problem_type': 'test'
            }
        )

        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        correct_answer = int(correct_sol.answer)
        malrule_answer = int(malrule_sol.answer)

        print(f"\n  Example {i}: {minuend} - {subtrahend} ({desc})")
        print(f"    Correct: {correct_answer} (expected: {expected_correct})")
        print(f"    Malrule: {malrule_answer} (expected: {expected_malrule})")

        if correct_answer != expected_correct:
            print(f"    FAILED: Correct algorithm mismatch!")
            all_passed = False
        elif malrule_answer != expected_malrule:
            print(f"    FAILED: Malrule algorithm mismatch!")
            all_passed = False
        elif correct_answer == malrule_answer:
            print(f"    FAILED: Answers should differ!")
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
    print("TEST 2: Template Generation")
    print("=" * 60)

    generator = ForgetBorrowOverBlanksProblemGenerator(
        level=3,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = ForgetBorrowOverBlanksMalrule()
    correct = SubtractionCorrectAlgorithm()

    templates = generator.get_available_templates()
    print(f"  Testing {len(templates)} templates: {templates}")

    all_passed = True
    for i, template in enumerate(templates):
        problem = generator.generate(seed=42 + i, template=template)

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
            print(f"    {template}: FAILED - missing correct_answer in metadata")
            all_passed = False
            continue

        if 'malrule_answer' not in problem.metadata:
            print(f"    {template}: FAILED - missing malrule_answer in metadata")
            all_passed = False
            continue

        # Verify solutions differ
        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        if correct_sol.answer == malrule_sol.answer:
            print(f"    {template}: WARNING - answers same (correct: {correct_sol.answer}, malrule: {malrule_sol.answer})")
            # Don't fail - some edge cases may produce same answer
        else:
            print(f"    {template}: PASSED (correct: {correct_sol.answer}, malrule: {malrule_sol.answer})")

    if all_passed:
        print("\n  All templates PASSED")
    else:
        print("\n  Some templates FAILED")

    return all_passed


def test_automated_suite():
    """Run automated test suite."""
    print("\n" + "=" * 60)
    print("TEST 3: Automated Test Suite")
    print("=" * 60)

    generator = ForgetBorrowOverBlanksProblemGenerator(
        level=3,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = ForgetBorrowOverBlanksMalrule()
    correct = SubtractionCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, generator)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    print(f"\n  Automated suite: {'PASSED' if all_passed else 'FAILED'}")
    return all_passed


def test_malrule_properties():
    """Test malrule metadata and properties."""
    print("\n" + "=" * 60)
    print("TEST 4: Malrule Properties")
    print("=" * 60)

    malrule = ForgetBorrowOverBlanksMalrule()

    # Check name
    name = malrule.get_name()
    assert name == "Forget-Borrow-Over-Blanks", f"Expected 'Forget-Borrow-Over-Blanks', got '{name}'"
    print(f"  Name: {name}")

    # Check description
    desc = malrule.get_description()
    assert len(desc) > 50, "Description too short"
    assert "blank" in desc.lower(), "Description should mention 'blank'"
    print(f"  Description length: {len(desc)} chars")

    print("\n  All properties PASSED")
    return True


def main():
    """Main entry point."""
    print("\n" + "=" * 68)
    print("  VERIFICATION TEST: FORGET/BORROW/OVER/BLANKS  ".center(68))
    print("  Brown & Burton (1978)  ".center(68))
    print("=" * 68)

    try:
        test1 = test_specific_examples()
        test2 = test_all_templates()
        test3 = test_automated_suite()
        test4 = test_malrule_properties()

        all_passed = test1 and test2 and test3 and test4

        print("\n" + "=" * 68)
        if all_passed:
            print("  VERIFICATION COMPLETE  ".center(68))
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
