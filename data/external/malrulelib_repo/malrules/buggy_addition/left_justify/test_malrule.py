#!/usr/bin/env python3
"""
Test suite for Left-Justify malrule.

"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.buggy_addition.left_justify import (
    LeftJustifyProblemGenerator,
    LeftJustifyMalrule,
    AdditionCorrectAlgorithm
)


def test_specific_examples():
    """Test with known examples from Brown & Burton (1978)."""
    print("\n" + "="*60)
    print("TEST 1: Specific Research Examples")
    print("="*60)

    malrule = LeftJustifyMalrule()
    correct = AdditionCorrectAlgorithm()

    # Example 1: 23 + 456 (from Brown & Burton 1978)
    # Correct: 23 + 456 = 479
    # Malrule: 230 + 456 = 686 (23 left-justified becomes 230)
    problem1 = Problem(
        text="What is 23 + 456?",
        operands=[23, 456],
        operation='addition',
        level=3,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'num1': 23,
            'num2': 456,
            'correct_answer': 479,
            'malrule_answer': 686,
            'template': 'basic_addition'
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"  Example 1: 23 + 456")
    print(f"    Correct answer: {correct_sol.answer} (expected: 479)")
    print(f"    Malrule answer: {malrule_sol.answer} (expected: 686)")

    assert correct_sol.answer == '479', f"Expected 479, got {correct_sol.answer}"
    assert malrule_sol.answer == '686', f"Expected 686, got {malrule_sol.answer}"
    assert correct_sol.answer != malrule_sol.answer, "Answers should differ"
    print("  Example 1: PASSED")

    # Example 2: 5 + 123 (single digit + 3-digit)
    # Correct: 5 + 123 = 128
    # Malrule: 500 + 123 = 623 (5 left-justified becomes 500)
    problem2 = Problem(
        text="What is 5 + 123?",
        operands=[5, 123],
        operation='addition',
        level=3,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'num1': 5,
            'num2': 123,
            'correct_answer': 128,
            'malrule_answer': 623,
            'template': 'basic_addition'
        }
    )

    correct_sol = correct.solve(problem2)
    malrule_sol = malrule.solve(problem2)

    print(f"  Example 2: 5 + 123")
    print(f"    Correct answer: {correct_sol.answer} (expected: 128)")
    print(f"    Malrule answer: {malrule_sol.answer} (expected: 623)")

    assert correct_sol.answer == '128', f"Expected 128, got {correct_sol.answer}"
    assert malrule_sol.answer == '623', f"Expected 623, got {malrule_sol.answer}"
    assert correct_sol.answer != malrule_sol.answer, "Answers should differ"
    print("  Example 2: PASSED")

    # Example 3: 456 + 23 (reversed order - longer first)
    # Correct: 456 + 23 = 479
    # Malrule: 456 + 230 = 686 (23 left-justified becomes 230)
    problem3 = Problem(
        text="What is 456 + 23?",
        operands=[456, 23],
        operation='addition',
        level=3,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'num1': 456,
            'num2': 23,
            'correct_answer': 479,
            'malrule_answer': 686,
            'template': 'basic_addition'
        }
    )

    correct_sol = correct.solve(problem3)
    malrule_sol = malrule.solve(problem3)

    print(f"  Example 3: 456 + 23")
    print(f"    Correct answer: {correct_sol.answer} (expected: 479)")
    print(f"    Malrule answer: {malrule_sol.answer} (expected: 686)")

    assert correct_sol.answer == '479', f"Expected 479, got {correct_sol.answer}"
    assert malrule_sol.answer == '686', f"Expected 686, got {malrule_sol.answer}"
    assert correct_sol.answer != malrule_sol.answer, "Answers should differ"
    print("  Example 3: PASSED")

    # Example 4: 12 + 3456 (2-digit + 4-digit)
    # Correct: 12 + 3456 = 3468
    # Malrule: 1200 + 3456 = 4656 (12 left-justified becomes 1200)
    problem4 = Problem(
        text="What is 12 + 3456?",
        operands=[12, 3456],
        operation='addition',
        level=4,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'num1': 12,
            'num2': 3456,
            'correct_answer': 3468,
            'malrule_answer': 4656,
            'template': 'basic_addition'
        }
    )

    correct_sol = correct.solve(problem4)
    malrule_sol = malrule.solve(problem4)

    print(f"  Example 4: 12 + 3456")
    print(f"    Correct answer: {correct_sol.answer} (expected: 3468)")
    print(f"    Malrule answer: {malrule_sol.answer} (expected: 4656)")

    assert correct_sol.answer == '3468', f"Expected 3468, got {correct_sol.answer}"
    assert malrule_sol.answer == '4656', f"Expected 4656, got {malrule_sol.answer}"
    assert correct_sol.answer != malrule_sol.answer, "Answers should differ"
    print("  Example 4: PASSED")

    # Example 5: Same length numbers (should produce same answer)
    # Correct: 123 + 456 = 579
    # Malrule: 123 + 456 = 579 (same length, no alignment difference)
    problem5 = Problem(
        text="What is 123 + 456?",
        operands=[123, 456],
        operation='addition',
        level=3,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'num1': 123,
            'num2': 456,
            'correct_answer': 579,
            'malrule_answer': 579,  # Same because same length
            'template': 'basic_addition'
        }
    )

    correct_sol = correct.solve(problem5)
    malrule_sol = malrule.solve(problem5)

    print(f"  Example 5: 123 + 456 (same length)")
    print(f"    Correct answer: {correct_sol.answer} (expected: 579)")
    print(f"    Malrule answer: {malrule_sol.answer} (expected: 579)")

    assert correct_sol.answer == '579', f"Expected 579, got {correct_sol.answer}"
    assert malrule_sol.answer == '579', f"Expected 579, got {malrule_sol.answer}"
    assert correct_sol.answer == malrule_sol.answer, "Same length should give same answer"
    print("  Example 5: PASSED (same length edge case)")

    print("\n  All specific examples PASSED")


def test_all_templates():
    """Test all problem templates generate valid problems."""
    print("\n" + "="*60)
    print("TEST 2: Template Generation")
    print("="*60)

    generator = LeftJustifyProblemGenerator(level=3, difficulty=DifficultyLevel.MEDIUM)
    malrule = LeftJustifyMalrule()
    correct = AdditionCorrectAlgorithm()

    templates = generator.get_available_templates()
    print(f"  Testing {len(templates)} templates: {templates}")

    for i, template in enumerate(templates):
        problem = generator.generate(seed=42+i, template=template)

        # Verify problem structure
        assert problem.text, f"Template {template}: missing text"
        assert problem.operands, f"Template {template}: missing operands"
        assert len(problem.operands) >= 2, f"Template {template}: need at least 2 operands"
        assert 'correct_answer' in problem.metadata, f"Template {template}: missing correct_answer"
        assert 'malrule_answer' in problem.metadata, f"Template {template}: missing malrule_answer"

        # Verify solutions
        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        # Check if different lengths produce different answers
        num1, num2 = problem.operands[:2]
        if len(str(num1)) != len(str(num2)):
            assert correct_sol.answer != malrule_sol.answer, \
                f"Template {template}: answers should differ for different-length operands"
            print(f"    {template}: PASSED (different lengths, different answers)")
        else:
            print(f"    {template}: PASSED (same lengths, same answers - edge case)")

    print("\n  All templates PASSED")


def test_automated_suite():
    """Run automated test suite."""
    print("\n" + "="*60)
    print("TEST 3: Automated Test Suite")
    print("="*60)

    generator = LeftJustifyProblemGenerator(level=3, difficulty=DifficultyLevel.MEDIUM)
    malrule = LeftJustifyMalrule()
    correct = AdditionCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, generator)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    print(f"\n  Automated suite: {'PASSED' if all_passed else 'FAILED'}")
    return all_passed


def test_malrule_calculation():
    """Test the malrule calculation logic directly."""
    print("\n" + "="*60)
    print("TEST 4: Direct Malrule Calculation")
    print("="*60)

    malrule = LeftJustifyMalrule()

    test_cases = [
        # (num1, num2, expected_malrule_answer)
        (23, 456, 686),    # 230 + 456
        (5, 123, 623),     # 500 + 123
        (456, 23, 686),    # 456 + 230
        (12, 3456, 4656),  # 1200 + 3456
        (7, 89, 159),      # 70 + 89
        (123, 456, 579),   # Same length - no change
        (1, 99, 109),      # 10 + 99
        (99, 1, 109),      # 99 + 10
    ]

    for num1, num2, expected in test_cases:
        result = malrule._apply_left_justify(num1, num2)
        status = "PASSED" if result == expected else f"FAILED (got {result})"
        print(f"  {num1} + {num2} (left-justified) = {expected}: {status}")
        assert result == expected, f"Expected {expected}, got {result}"

    print("\n  All direct calculations PASSED")


def main():
    """Main entry point."""
    print("\n" + "="*68)
    print("  VERIFICATION TEST: Left-Justify Malrule  ".center(68))
    print("  Source: Brown & Burton (1978)  ".center(68))
    print("="*68)

    try:
        test_specific_examples()
        test_all_templates()
        test_malrule_calculation()
        all_passed = test_automated_suite()

        print("\n" + "="*68)
        if all_passed:
            print("  VERIFICATION COMPLETE  ".center(68))
        else:
            print("  SOME TESTS FAILED  ".center(68))
        print("="*68 + "\n")

        return 0 if all_passed else 1

    except Exception as e:
        print(f"\n  TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
