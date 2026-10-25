#!/usr/bin/env python3
"""
Test script for Diff-0-N=0 malrule.

Run from project root: python3 -m buggy_malrules.subtraction.diff_0_n_equals_0.test_malrule
Or from this directory: python3 test_malrule.py

Research: Brown & Burton (1978) - Diagnostic models for procedural bugs
in basic mathematical skills. Cognitive Science, 2(2), 155-192.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.buggy_subtraction.diff_0_n_equals_0 import (
    Diff0NEquals0ProblemGenerator,
    Diff0NEquals0Malrule,
    SubtractionCorrectAlgorithm
)


def test_paper_example():
    """
    Test with the exact example from Brown & Burton (1978).

    Paper example: 140 - 21 = 120 (correct: 119)
        - Ones: 0-1, student writes 0 (bug!)
        - Tens: 4-2=2
        - Hundreds: 1-0=1
        Result: 120 instead of 119
    """
    print("\n" + "=" * 60)
    print("TEST 1: Brown & Burton (1978) Paper Example")
    print("=" * 60)

    malrule = Diff0NEquals0Malrule()
    correct = SubtractionCorrectAlgorithm()

    # The exact example from the paper
    problem = Problem(
        text="Calculate: 140 - 21",
        operands=[140, 21],
        operation='subtraction',
        level=3,
        difficulty=DifficultyLevel.EASY,
        metadata={
            'minuend': 140,
            'subtrahend': 21,
            'correct_answer': '119',
            'malrule_answer': '120',
            'problem_type': 'basic'
        }
    )

    correct_sol = correct.solve(problem)
    malrule_sol = malrule.solve(problem)

    print(f"  Problem: {problem.text}")
    print(f"  Correct answer: {correct_sol.answer}")
    print(f"  Malrule answer: {malrule_sol.answer}")
    print(f"  Expected from paper: 120")

    # Verify correct answer
    assert correct_sol.answer == '119', f"Expected correct answer 119, got {correct_sol.answer}"
    print("  Correct algorithm: PASSED")

    # Verify malrule answer matches paper
    assert malrule_sol.answer == '120', f"Expected malrule answer 120, got {malrule_sol.answer}"
    print("  Malrule algorithm: PASSED")

    # Verify they differ
    assert correct_sol.answer != malrule_sol.answer, "Answers should differ"
    print("  Answers differ: PASSED")

    print("\n  Paper example: PASSED")


def test_specific_examples():
    """Test with additional specific examples."""
    print("\n" + "=" * 60)
    print("TEST 2: Additional Specific Examples")
    print("=" * 60)

    malrule = Diff0NEquals0Malrule()
    correct = SubtractionCorrectAlgorithm()

    # Additional test cases for 0-N=0 bug
    test_cases = [
        # (minuend, subtrahend, expected_correct, expected_malrule, explanation)
        (140, 21, '119', '120', 'ones: 0-1=0 (bug)'),
        (230, 45, '185', '190', 'ones: 0-5=0 (bug)'),
        (305, 147, '158', '108', 'tens: 0-4=0 (bug)'),
        (504, 238, '266', '206', 'tens: 0-3=0 (bug)'),
        (4003, 1567, '2436', '2006', 'tens: 0-6=0, ones: 0-7=0 (bugs)'),
    ]

    for minuend, subtrahend, expected_correct, expected_malrule, explanation in test_cases:
        problem = Problem(
            text=f"Calculate: {minuend} - {subtrahend}",
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=3,
            difficulty=DifficultyLevel.MEDIUM,
            metadata={
                'minuend': minuend,
                'subtrahend': subtrahend,
                'correct_answer': expected_correct,
                'malrule_answer': expected_malrule,
                'problem_type': 'basic'
            }
        )

        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        print(f"\n  {minuend} - {subtrahend}")
        print(f"    Explanation: {explanation}")
        print(f"    Correct: {correct_sol.answer} (expected: {expected_correct})")
        print(f"    Malrule: {malrule_sol.answer} (expected: {expected_malrule})")

        # Check correct answer
        assert correct_sol.answer == expected_correct, \
            f"Expected correct {expected_correct}, got {correct_sol.answer}"

        # Check malrule answer
        assert malrule_sol.answer == expected_malrule, \
            f"Expected malrule {expected_malrule}, got {malrule_sol.answer}"

        # Check they differ
        assert correct_sol.answer != malrule_sol.answer, \
            f"Answers should differ for {minuend} - {subtrahend}"

        print("    PASSED")

    print("\n  All specific examples: PASSED")


def test_all_templates():
    """Test all problem templates generate valid problems."""
    print("\n" + "=" * 60)
    print("TEST 3: Template Generation")
    print("=" * 60)

    generator = Diff0NEquals0ProblemGenerator(level=3, difficulty=DifficultyLevel.MEDIUM)
    malrule = Diff0NEquals0Malrule()
    correct = SubtractionCorrectAlgorithm()

    templates = generator.get_available_templates()
    print(f"  Testing {len(templates)} templates: {templates}")

    for i, template in enumerate(templates):
        problem = generator.generate(seed=42 + i, template=template)

        # Verify problem structure
        assert problem.text, f"Template {template}: missing text"
        assert problem.operands, f"Template {template}: missing operands"
        assert 'correct_answer' in problem.metadata, f"Template {template}: missing correct_answer"
        assert 'malrule_answer' in problem.metadata, f"Template {template}: missing malrule_answer"

        # Verify solutions differ
        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        # The malrule should produce a different answer when there's a 0-N situation
        if problem.metadata['correct_answer'] != problem.metadata['malrule_answer']:
            assert correct_sol.answer != malrule_sol.answer, \
                f"Template {template}: answers should differ when malrule applies"

        print(f"    {template}: PASSED")

    print("\n  All templates: PASSED")


def test_contrast_with_0_n_equals_n():
    """
    Test that 0-N=0 is different from 0-N=N.

    DIFF/0-N=0: Student writes 0 when top is 0 and bottom is N
    DIFF/0-N=N: Student writes N when top is 0 and bottom is N

    These are distinct bugs documented in Brown & Burton (1978).
    """
    print("\n" + "=" * 60)
    print("TEST 4: Contrast with 0-N=N (Different Bug)")
    print("=" * 60)

    malrule = Diff0NEquals0Malrule()

    # For 140 - 21:
    # 0-N=0 bug: 0-1=0, result is 120
    # 0-N=N bug: 0-1=1, result is 121 (different!)

    problem = Problem(
        text="Calculate: 140 - 21",
        operands=[140, 21],
        operation='subtraction',
        level=3,
        difficulty=DifficultyLevel.EASY,
        metadata={
            'minuend': 140,
            'subtrahend': 21,
            'correct_answer': '119',
            'malrule_answer': '120',
            'problem_type': 'basic'
        }
    )

    malrule_sol = malrule.solve(problem)

    print(f"  Problem: 140 - 21")
    print(f"  Correct: 119")
    print(f"  DIFF/0-N=0 (this bug): {malrule_sol.answer}")
    print(f"  DIFF/0-N=N (different bug): would be 121")

    # Verify our implementation produces the 0-N=0 result (120)
    assert malrule_sol.answer == '120', f"Expected 120 for 0-N=0 bug, got {malrule_sol.answer}"

    # The 0-N=N bug would produce 121 (writing 1, the bottom digit, instead of 0)
    # This confirms we're implementing the correct variant
    assert malrule_sol.answer != '121', "This should be 0-N=0, not 0-N=N"

    print("\n  Contrast test: PASSED (confirms this is 0-N=0, not 0-N=N)")


def test_automated_suite():
    """Run automated test suite using MalruleTest framework."""
    print("\n" + "=" * 60)
    print("TEST 5: Automated Test Suite")
    print("=" * 60)

    generator = Diff0NEquals0ProblemGenerator(level=3, difficulty=DifficultyLevel.MEDIUM)
    malrule = Diff0NEquals0Malrule()
    correct = SubtractionCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, generator)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    print(f"\n  Automated suite: {'PASSED' if all_passed else 'FAILED'}")
    return all_passed


def main():
    """Main entry point."""
    print("\n" + "=" * 68)
    print("  VERIFICATION TEST: DIFF/0-N=0 (Brown & Burton, 1978)  ".center(68))
    print("=" * 68)
    print("\n  Bug: When top digit is 0, student writes 0 in answer (0-N=0)")
    print("  Example: 140 - 21 = 120 (correct: 119)")

    try:
        test_paper_example()
        test_specific_examples()
        test_all_templates()
        test_contrast_with_0_n_equals_n()
        all_passed = test_automated_suite()

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
