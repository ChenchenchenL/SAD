#!/usr/bin/env python3
"""
Test suite for Single-Digit-Linked malrule.

"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.buggy_addition.single_digit_linked import (
    SingleDigitLinkedProblemGenerator,
    SingleDigitLinkedMalrule,
    AdditionCorrectAlgorithm
)


def test_specific_examples():
    """Test with exact examples from Brown & Burton (1978)."""
    print("\n" + "="*60)
    print("TEST 1: Brown & Burton (1978) Paper Examples")
    print("="*60)

    malrule = SingleDigitLinkedMalrule()
    correct = AdditionCorrectAlgorithm()

    # Example 1: 19 + 9 = 199 (correct: 28)
    # Single digit 9 appended to 19
    problem1 = Problem(
        text="What is 19 + 9?",
        operands=[19, 9],
        operation='addition',
        level=3,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'num1': 19,
            'num2': 9,
            'correct_answer': '28',
            'malrule_answer': '199',
            'problem_type': 'basic'
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    assert correct_sol.answer == '28', f"Expected 28, got {correct_sol.answer}"
    assert malrule_sol.answer == '199', f"Expected 199, got {malrule_sol.answer}"
    assert correct_sol.answer != malrule_sol.answer, "Answers should differ"
    print("  Example 1 (19 + 9 = 199): PASSED")

    # Example 2: 23 + 6 = 236 (correct: 29)
    # Single digit 6 appended to 23
    problem2 = Problem(
        text="What is 23 + 6?",
        operands=[23, 6],
        operation='addition',
        level=3,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'num1': 23,
            'num2': 6,
            'correct_answer': '29',
            'malrule_answer': '236',
            'problem_type': 'basic'
        }
    )

    correct_sol = correct.solve(problem2)
    malrule_sol = malrule.solve(problem2)

    assert correct_sol.answer == '29', f"Expected 29, got {correct_sol.answer}"
    assert malrule_sol.answer == '236', f"Expected 236, got {malrule_sol.answer}"
    assert correct_sol.answer != malrule_sol.answer, "Answers should differ"
    print("  Example 2 (23 + 6 = 236): PASSED")

    # Example 3: 81 + 8 = 818 (correct: 89)
    # Single digit 8 appended to 81
    problem3 = Problem(
        text="What is 81 + 8?",
        operands=[81, 8],
        operation='addition',
        level=3,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'num1': 81,
            'num2': 8,
            'correct_answer': '89',
            'malrule_answer': '818',
            'problem_type': 'basic'
        }
    )

    correct_sol = correct.solve(problem3)
    malrule_sol = malrule.solve(problem3)

    assert correct_sol.answer == '89', f"Expected 89, got {correct_sol.answer}"
    assert malrule_sol.answer == '818', f"Expected 818, got {malrule_sol.answer}"
    assert correct_sol.answer != malrule_sol.answer, "Answers should differ"
    print("  Example 3 (81 + 8 = 818): PASSED")

    # Example 4: 8 + 12 = 128 (correct: 20)
    # Single digit 8 appended to 12 (NOT 812!)
    # This is the key example showing the single digit is ALWAYS appended to multi-digit
    problem4 = Problem(
        text="What is 8 + 12?",
        operands=[8, 12],
        operation='addition',
        level=3,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'num1': 8,
            'num2': 12,
            'correct_answer': '20',
            'malrule_answer': '128',
            'problem_type': 'basic'
        }
    )

    correct_sol = correct.solve(problem4)
    malrule_sol = malrule.solve(problem4)

    assert correct_sol.answer == '20', f"Expected 20, got {correct_sol.answer}"
    assert malrule_sol.answer == '128', f"Expected 128, got {malrule_sol.answer}"
    assert correct_sol.answer != malrule_sol.answer, "Answers should differ"
    print("  Example 4 (8 + 12 = 128, NOT 812): PASSED")

    print("\n  All Brown & Burton (1978) examples PASSED")


def test_additional_examples():
    """Test with additional generated examples to verify malrule logic."""
    print("\n" + "="*60)
    print("TEST 2: Additional Verification Examples")
    print("="*60)

    malrule = SingleDigitLinkedMalrule()
    correct = AdditionCorrectAlgorithm()

    # Additional test cases
    test_cases = [
        # (num1, num2, expected_correct, expected_malrule, description)
        (45, 7, '52', '457', "multi-digit + single-digit"),
        (3, 56, '59', '563', "single-digit + multi-digit"),
        (100, 5, '105', '1005', "three-digit + single-digit"),
        (9, 234, '243', '2349', "single-digit + three-digit"),
        (67, 2, '69', '672', "two-digit + small single-digit"),
    ]

    for num1, num2, expected_correct, expected_malrule, description in test_cases:
        problem = Problem(
            text=f"What is {num1} + {num2}?",
            operands=[num1, num2],
            operation='addition',
            level=3,
            difficulty=DifficultyLevel.MEDIUM,
            metadata={
                'num1': num1,
                'num2': num2,
                'correct_answer': expected_correct,
                'malrule_answer': expected_malrule,
                'problem_type': 'basic'
            }
        )

        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        assert correct_sol.answer == expected_correct, \
            f"Correct: Expected {expected_correct}, got {correct_sol.answer}"
        assert malrule_sol.answer == expected_malrule, \
            f"Malrule: Expected {expected_malrule}, got {malrule_sol.answer}"

        print(f"  {description} ({num1} + {num2}): PASSED")

    print("\n  All additional examples PASSED")


def test_all_templates():
    """Test all problem templates generate valid problems."""
    print("\n" + "="*60)
    print("TEST 3: Template Generation")
    print("="*60)

    generator = SingleDigitLinkedProblemGenerator(level=3, difficulty=DifficultyLevel.MEDIUM)
    malrule = SingleDigitLinkedMalrule()
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

        # Verify one operand is single-digit and one is multi-digit
        num1, num2 = problem.operands[:2]
        has_single = num1 < 10 or num2 < 10
        has_multi = num1 >= 10 or num2 >= 10
        assert has_single and has_multi, \
            f"Template {template}: need one single-digit and one multi-digit operand"

        # Verify solutions differ
        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)
        assert correct_sol.answer != malrule_sol.answer, \
            f"Template {template}: answers should differ (correct={correct_sol.answer}, malrule={malrule_sol.answer})"

        print(f"    {template}: PASSED")

    print("\n  All templates PASSED")


def test_malrule_properties():
    """Test malrule metadata and documentation."""
    print("\n" + "="*60)
    print("TEST 4: Malrule Properties")
    print("="*60)

    malrule = SingleDigitLinkedMalrule()

    # Check name
    assert malrule.get_name() == "Single-Digit-Linked", "Name should match"
    print("  Name: PASSED")

    # Check description is non-empty
    assert len(malrule.get_description()) > 100, "Description should be detailed"
    print("  Description: PASSED")

    print("\n  All property tests PASSED")


def test_automated_suite():
    """Run automated test suite."""
    print("\n" + "="*60)
    print("TEST 5: Automated Test Suite")
    print("="*60)

    generator = SingleDigitLinkedProblemGenerator(level=3, difficulty=DifficultyLevel.MEDIUM)
    malrule = SingleDigitLinkedMalrule()
    correct = AdditionCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, generator)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    print(f"\n  Automated suite: {'PASSED' if all_passed else 'FAILED'}")
    return all_passed


def main():
    """Main entry point."""
    print("\n" + "="*68)
    print("  VERIFICATION TEST: Single-Digit-Linked  ".center(68))
    print("  Reference: Brown & Burton (1978)  ".center(68))
    print("="*68)

    try:
        test_specific_examples()
        test_additional_examples()
        test_all_templates()
        test_malrule_properties()
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
