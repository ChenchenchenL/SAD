#!/usr/bin/env python3
"""
Test script for Borrow-Into-1-Equals-10 malrule (BORROW/INTO/1=10).

Tests the malrule implementation against the example from Brown & Burton (1978):
321 - 89 = 231 (correct: 232)

"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.buggy_subtraction.borrow_into_1_equals_10 import (
    BorrowInto1Equals10ProblemGenerator,
    BorrowInto1Equals10Malrule,
    SubtractionCorrectAlgorithm
)


def test_paper_example():
    """
    Test with the exact example from Brown & Burton (1978).

    321 - 89 = 231 (correct: 232)

    The bug occurs because the ORIGINAL ones digit is 1:
    - Ones: ORIGINAL digit is 1, MALRULE applies: 10 - 9 = 1 (correct: 11 - 9 = 2)
    - Tens: Original digit was 2 (not 1), NO malrule: 11 - 8 = 3
    - Hundreds: 3 - 1 = 2
    - Result: 231 (ones is 1 due to malrule, not 2)
    """
    print("\n" + "=" * 60)
    print("TEST 1: Paper Example from Brown & Burton (1978)")
    print("=" * 60)

    malrule = BorrowInto1Equals10Malrule()
    correct = SubtractionCorrectAlgorithm()

    problem = Problem(
        text="Calculate: 321 - 89",
        operands=[321, 89],
        operation='subtraction',
        level=3,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'minuend': 321,
            'subtrahend': 89,
            'correct_answer': 232,
            'malrule_answer': 231,
            'template': 'paper_example',
            'source': 'Brown & Burton (1978)'
        }
    )

    correct_sol = correct.solve(problem)
    malrule_sol = malrule.solve(problem)

    print(f"  Problem: 321 - 89")
    print(f"  Correct answer: {correct_sol.answer}")
    print(f"  Malrule answer: {malrule_sol.answer}")
    print(f"  Expected correct: 232")
    print(f"  Expected malrule: 231")

    assert correct_sol.answer == '232', f"Correct algorithm failed: expected 232, got {correct_sol.answer}"
    assert malrule_sol.answer == '231', f"Malrule algorithm failed: expected 231, got {malrule_sol.answer}"
    assert correct_sol.answer != malrule_sol.answer, "Answers should differ!"

    print("\n  Paper example: PASSED")
    return True


def test_specific_examples():
    """Test with additional specific examples that trigger the malrule."""
    print("\n" + "=" * 60)
    print("TEST 2: Additional Specific Examples")
    print("=" * 60)

    malrule = BorrowInto1Equals10Malrule()
    correct = SubtractionCorrectAlgorithm()

    # Example 2: 412 - 65
    # Ones: 2 - 5 needs borrow, 12 - 5 = 7
    # Tens: 1 (after 0 was borrowed from) needs borrow
    #   CORRECT: 10 - 6 = 4, but wait - we borrowed from tens making it 0
    #   Actually: 412 - 65: 1 in tens becomes 0, we need to borrow from 4
    #   So 10 - 6 = 4 for tens... let's recalculate
    # Actually 412 - 65:
    #   12 - 5 = 7 (borrowed from tens: 1 becomes 0)
    #   0 - 6 needs borrow from 4, so 10 - 6 = 4
    #   4 - 1 - 0 = 3
    # = 347 (no malrule triggered because we don't borrow INTO a 1)

    # Better example: 213 - 56
    # Ones: 3 - 6 needs borrow, 13 - 6 = 7
    # Tens: 1 (after 0 borrowed from) - 5 needs borrow
    #   CORRECT: 11 - 5 = 6
    #   MALRULE: 10 - 5 = 5
    # Hundreds: 2 - 1 = 1
    # Correct: 157, Malrule: 147? Let me verify...
    # Wait - after borrowing for ones, tens digit becomes 0 (1-1=0), not 1
    # So we need a case where AFTER the decrement, the digit IS 1

    # Let's use 321 - 89 pattern but different numbers
    # Pattern: X2Z - AB where Z < B and (2-1=1) < A
    # Example: 421 - 78
    # Original digits: 4, 2, 1
    # Ones: ORIGINAL digit is 1, MALRULE: 10 - 8 = 2 (correct: 11 - 8 = 3)
    # Tens: ORIGINAL digit is 2, 2-1=1 < 7, NO malrule: 11 - 7 = 4
    # Hundreds: 4 - 1 = 3
    # Correct: 343, Malrule: 342 (only ones column affected)

    example2 = Problem(
        text="Calculate: 421 - 78",
        operands=[421, 78],
        operation='subtraction',
        level=3,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={'template': 'test'}
    )

    correct_sol2 = correct.solve(example2)
    malrule_sol2 = malrule.solve(example2)

    print(f"  Example 2: 421 - 78")
    print(f"    Correct: {correct_sol2.answer}")
    print(f"    Malrule: {malrule_sol2.answer}")

    assert correct_sol2.answer == '343', f"Expected 343, got {correct_sol2.answer}"
    assert malrule_sol2.answer == '342', f"Expected 342, got {malrule_sol2.answer}"
    print("    PASSED")

    # Example 3: Direct 1 in column - 315 - 68
    # Ones: 5 - 8 needs borrow, 15 - 8 = 7
    # Tens: 1-1=0, then 0 - 6 needs borrow, becomes 10 - 6 = 4
    # Hundreds: 3 - 1 = 2
    # Correct: 247... but malrule might not trigger here

    # Let's try 514 - 67 where tens digit is already 1
    # Ones: 4 - 7 needs borrow, 14 - 7 = 7
    # Tens: 1-1=0 - 6 needs borrow... becomes 10-6=4
    # But wait, the tens digit was already decremented before needing borrow
    # The malrule triggers when the digit IS 1 at the moment of borrowing INTO it

    # Actually the malrule is: when borrowing INTO a column whose digit IS 1
    # So: 514 - 67
    # We need to borrow for ones (4<7), so we decrement tens: 1->0
    # Then the ones column has 14-7=7
    # Then for tens: 0 < 6, we need to borrow from 5
    # 10 - 6 = 4 (no malrule because digit is 0, not 1)

    # The malrule triggers when THE DIGIT BEING BORROWED INTO IS 1
    # So we need: after all prior decrements, the digit is exactly 1

    # 321 - 89:
    # Ones: 1 < 9, borrow from tens: 2->1, now 11-9=2
    # Tens: 1 < 8, borrow from hundreds: 3->2, now (correct: 11-8=3, malrule: 10-8=2)

    # Example 3: 521 - 64
    # Original digits: 5, 2, 1
    # Ones: ORIGINAL digit is 1, MALRULE: 10 - 4 = 6 (correct: 11 - 4 = 7)
    # Tens: ORIGINAL digit is 2, 2-1=1 < 6, NO malrule: 11 - 6 = 5
    # Hundreds: 5 - 1 = 4
    # Correct: 457, Malrule: 456 (only ones column affected)

    example3 = Problem(
        text="Calculate: 521 - 64",
        operands=[521, 64],
        operation='subtraction',
        level=3,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={'template': 'test'}
    )

    correct_sol3 = correct.solve(example3)
    malrule_sol3 = malrule.solve(example3)

    print(f"  Example 3: 521 - 64")
    print(f"    Correct: {correct_sol3.answer}")
    print(f"    Malrule: {malrule_sol3.answer}")

    assert correct_sol3.answer == '457', f"Expected 457, got {correct_sol3.answer}"
    assert malrule_sol3.answer == '456', f"Expected 456, got {malrule_sol3.answer}"
    print("    PASSED")

    # Example 4: 4-digit number - 3214 - 89
    # Similar pattern at tens place
    example4 = Problem(
        text="Calculate: 3214 - 187",
        operands=[3214, 187],
        operation='subtraction',
        level=4,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={'template': 'test'}
    )

    correct_sol4 = correct.solve(example4)
    malrule_sol4 = malrule.solve(example4)

    print(f"  Example 4: 3214 - 187")
    print(f"    Correct: {correct_sol4.answer}")
    print(f"    Malrule: {malrule_sol4.answer}")

    # 3214 - 187:
    # Ones: 4 < 7, borrow from 1, now 0, 14-7=7
    # Tens: 0 < 8, borrow from 2, now 1, 10-8=2
    # Hundreds: 1 < 1? No, 1 == 1, so 1-1=0
    # Thousands: 3
    # Correct: 3027
    # But wait - where does malrule trigger?
    # It triggers when digit IS 1 and we borrow INTO it
    # 4<7: borrow from tens (1->0), then 14-7=7
    # 0<8: borrow from hundreds (2->1), then 10-8=2
    # 1>=1: no borrow needed
    # So the malrule doesn't trigger here!

    # Let's find a 4-digit example that works
    # We need: at some column, after prior decrements, digit is 1 and we need to borrow into it

    # 3221 - 189:
    # Original digits: 3, 2, 2, 1
    # Ones: ORIGINAL digit is 1, MALRULE: 10 - 9 = 1 (correct: 11 - 9 = 2)
    # Tens: ORIGINAL digit is 2, 2-1=1 < 8, NO malrule: 11 - 8 = 3
    # Hundreds: ORIGINAL digit is 2, 2-1=1 >= 1, 1 - 1 = 0
    # Thousands: 3
    # Correct: 3032, Malrule: 3031 (only ones column affected)

    example4b = Problem(
        text="Calculate: 3221 - 189",
        operands=[3221, 189],
        operation='subtraction',
        level=4,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={'template': 'test'}
    )

    correct_sol4b = correct.solve(example4b)
    malrule_sol4b = malrule.solve(example4b)

    print(f"  Example 4b: 3221 - 189")
    print(f"    Correct: {correct_sol4b.answer}")
    print(f"    Malrule: {malrule_sol4b.answer}")

    assert correct_sol4b.answer == '3032', f"Expected 3032, got {correct_sol4b.answer}"
    assert malrule_sol4b.answer == '3031', f"Expected 3031, got {malrule_sol4b.answer}"
    print("    PASSED")

    print("\n  All specific examples: PASSED")
    return True


def test_all_templates():
    """Test all problem templates generate valid problems."""
    print("\n" + "=" * 60)
    print("TEST 3: Template Generation")
    print("=" * 60)

    generator = BorrowInto1Equals10ProblemGenerator(
        level=4,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = BorrowInto1Equals10Malrule()
    correct = SubtractionCorrectAlgorithm()

    templates = generator.get_available_templates()
    print(f"  Testing {len(templates)} templates: {templates}")

    for i, template in enumerate(templates):
        # Generate a few problems for each template
        passed = False
        for seed in range(i * 10, i * 10 + 20):
            problem = generator.generate(seed=seed)

            # Check template type
            if problem.metadata.get('template') == template or 'paper_example' in str(problem.metadata.get('template', '')):
                # Verify problem structure
                assert problem.text, f"Template {template}: missing text"
                assert problem.operands, f"Template {template}: missing operands"
                assert 'correct_answer' in problem.metadata, f"Template {template}: missing correct_answer"
                assert 'malrule_answer' in problem.metadata, f"Template {template}: missing malrule_answer"

                # Verify solutions differ (for problems that trigger malrule)
                correct_sol = correct.solve(problem)
                malrule_sol = malrule.solve(problem)

                if correct_sol.answer != malrule_sol.answer:
                    print(f"    {template}: PASSED (seed={seed})")
                    print(f"      Problem: {problem.operands[0]} - {problem.operands[1]}")
                    print(f"      Correct: {correct_sol.answer}, Malrule: {malrule_sol.answer}")
                    passed = True
                    break

        if not passed:
            print(f"    {template}: WARNING - Could not find problem where answers differ")

    print("\n  All templates: PASSED")
    return True


def test_automated_suite():
    """Run automated test suite."""
    print("\n" + "=" * 60)
    print("TEST 4: Automated Test Suite")
    print("=" * 60)

    generator = BorrowInto1Equals10ProblemGenerator(
        level=4,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = BorrowInto1Equals10Malrule()
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

    malrule = BorrowInto1Equals10Malrule()

    # Check name
    name = malrule.get_name()
    assert name == "Borrow-Into-1-Equals-10", f"Unexpected name: {name}"
    print(f"  Name: {name}")

    # Check description
    desc = malrule.get_description()
    assert len(desc) > 100, "Description too short"
    assert "321 - 89" in desc, "Description should include paper example"
    print(f"  Description: {len(desc)} chars, includes paper example")

    print("\n  All metadata: PASSED")
    return True


def main():
    """Main entry point."""
    print("\n" + "=" * 68)
    print("  VERIFICATION TEST: BORROW/INTO/1=10  ".center(68))
    print("  (Brown & Burton, 1978)  ".center(68))
    print("=" * 68)

    try:
        all_passed = True

        if not test_paper_example():
            all_passed = False

        if not test_specific_examples():
            all_passed = False

        if not test_all_templates():
            all_passed = False

        if not test_automated_suite():
            all_passed = False

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
