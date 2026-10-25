#!/usr/bin/env python3
"""
Test suite for Add-All-Digits malrule.

"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.buggy_addition.add_all_digits import (
    AddAllDigitsProblemGenerator,
    AddAllDigitsMalrule,
    AdditionCorrectAlgorithm
)


def test_specific_examples():
    """Test with known examples from Brown & Burton (1978)."""
    print("\n" + "="*60)
    print("TEST 1: Specific Research Examples from Brown & Burton (1978)")
    print("="*60)

    malrule = AddAllDigitsMalrule()
    correct = AdditionCorrectAlgorithm()

    # Example 1: 17 + 5 = 13 (correct: 22) -> 1+7+5=13
    problem1 = Problem(
        text="What is 17 + 5?",
        operands=[17, 5],
        operation='addition',
        level=2,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'correct_answer': '22',
            'malrule_answer': '13',
            'problem_type': 'basic'
        }
    )

    correct_sol1 = correct.solve(problem1)
    malrule_sol1 = malrule.solve(problem1)

    print(f"\n  Example 1: 17 + 5")
    print(f"    Correct: {correct_sol1.answer} (expected: 22)")
    print(f"    Malrule: {malrule_sol1.answer} (expected: 13)")
    print(f"    Calculation: 1 + 7 + 5 = 13")

    assert correct_sol1.answer == '22', f"Expected correct 22, got {correct_sol1.answer}"
    assert malrule_sol1.answer == '13', f"Expected malrule 13, got {malrule_sol1.answer}"
    assert correct_sol1.answer != malrule_sol1.answer, "Answers should differ"
    print("  Example 1: PASSED")

    # Example 2: 51 + 1707 = 21 (correct: 1758) -> 5+1+1+7+0+7=21
    problem2 = Problem(
        text="What is 51 + 1707?",
        operands=[51, 1707],
        operation='addition',
        level=3,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'correct_answer': '1758',
            'malrule_answer': '21',
            'problem_type': 'basic'
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)

    print(f"\n  Example 2: 51 + 1707")
    print(f"    Correct: {correct_sol2.answer} (expected: 1758)")
    print(f"    Malrule: {malrule_sol2.answer} (expected: 21)")
    print(f"    Calculation: 5 + 1 + 1 + 7 + 0 + 7 = 21")

    assert correct_sol2.answer == '1758', f"Expected correct 1758, got {correct_sol2.answer}"
    assert malrule_sol2.answer == '21', f"Expected malrule 21, got {malrule_sol2.answer}"
    assert correct_sol2.answer != malrule_sol2.answer, "Answers should differ"
    print("  Example 2: PASSED")

    # Example 3: 99 + 99 = 36 (correct: 198) -> 9+9+9+9=36
    problem3 = Problem(
        text="What is 99 + 99?",
        operands=[99, 99],
        operation='addition',
        level=2,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'correct_answer': '198',
            'malrule_answer': '36',
            'problem_type': 'basic'
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)

    print(f"\n  Example 3: 99 + 99")
    print(f"    Correct: {correct_sol3.answer} (expected: 198)")
    print(f"    Malrule: {malrule_sol3.answer} (expected: 36)")
    print(f"    Calculation: 9 + 9 + 9 + 9 = 36")

    assert correct_sol3.answer == '198', f"Expected correct 198, got {correct_sol3.answer}"
    assert malrule_sol3.answer == '36', f"Expected malrule 36, got {malrule_sol3.answer}"
    assert correct_sol3.answer != malrule_sol3.answer, "Answers should differ"
    print("  Example 3: PASSED")

    # Example 4: 68 + 9 = 23 (correct: 77) -> 6+8+9=23
    problem4 = Problem(
        text="What is 68 + 9?",
        operands=[68, 9],
        operation='addition',
        level=2,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'correct_answer': '77',
            'malrule_answer': '23',
            'problem_type': 'basic'
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)

    print(f"\n  Example 4: 68 + 9")
    print(f"    Correct: {correct_sol4.answer} (expected: 77)")
    print(f"    Malrule: {malrule_sol4.answer} (expected: 23)")
    print(f"    Calculation: 6 + 8 + 9 = 23")

    assert correct_sol4.answer == '77', f"Expected correct 77, got {correct_sol4.answer}"
    assert malrule_sol4.answer == '23', f"Expected malrule 23, got {malrule_sol4.answer}"
    assert correct_sol4.answer != malrule_sol4.answer, "Answers should differ"
    print("  Example 4: PASSED")

    print("\n  All specific examples PASSED")


def test_all_templates():
    """Test all problem templates generate valid problems."""
    print("\n" + "="*60)
    print("TEST 2: Template Generation")
    print("="*60)

    generator = AddAllDigitsProblemGenerator(level=2, difficulty=DifficultyLevel.MEDIUM)
    malrule = AddAllDigitsMalrule()
    correct = AdditionCorrectAlgorithm()

    templates = generator.get_available_templates()
    print(f"  Testing {len(templates)} templates: {templates}")

    for i, template in enumerate(templates):
        problem = generator.generate(seed=42+i, template=template)

        # Verify problem structure
        assert problem.text, f"Template {template}: missing text"
        assert problem.operands, f"Template {template}: missing operands"
        assert 'correct_answer' in problem.metadata, f"Template {template}: missing correct_answer"
        assert 'malrule_answer' in problem.metadata, f"Template {template}: missing malrule_answer"

        # Verify solutions differ
        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        # Verify correct algorithm produces correct answer
        expected_correct = str(problem.operands[0] + problem.operands[1])
        assert correct_sol.answer == expected_correct, \
            f"Template {template}: correct answer mismatch (got {correct_sol.answer}, expected {expected_correct})"

        # Verify malrule produces expected malrule answer
        expected_malrule = problem.metadata['malrule_answer']
        assert malrule_sol.answer == expected_malrule, \
            f"Template {template}: malrule answer mismatch (got {malrule_sol.answer}, expected {expected_malrule})"

        # Verify answers differ
        assert correct_sol.answer != malrule_sol.answer, \
            f"Template {template}: answers should differ"

        print(f"    {template}: PASSED (correct: {correct_sol.answer}, malrule: {malrule_sol.answer})")

    print("\n  All templates PASSED")


def test_calculate_expected_answer():
    """Test that calculate_expected_answer works independently."""
    print("\n" + "="*60)
    print("TEST 3: calculate_expected_answer Independence")
    print("="*60)

    malrule = AddAllDigitsMalrule()

    # Test with metadata
    problem1 = Problem(
        text="17 + 5",
        operands=[17, 5],
        operation='addition',
        level=2,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={'malrule_answer': '13'}
    )
    assert malrule.calculate_expected_answer(problem1) == '13', "Should use metadata"
    print("  Test with metadata: PASSED")

    # Test without metadata (should calculate)
    problem2 = Problem(
        text="17 + 5",
        operands=[17, 5],
        operation='addition',
        level=2,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={}
    )
    assert malrule.calculate_expected_answer(problem2) == '13', "Should calculate 1+7+5=13"
    print("  Test without metadata: PASSED")

    # Test with different numbers
    problem3 = Problem(
        text="123 + 456",
        operands=[123, 456],
        operation='addition',
        level=3,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={}
    )
    # 1+2+3+4+5+6 = 21
    assert malrule.calculate_expected_answer(problem3) == '21', "Should calculate 1+2+3+4+5+6=21"
    print("  Test calculation 123+456 -> 21: PASSED")

    print("\n  calculate_expected_answer tests PASSED")


def test_automated_suite():
    """Run automated test suite."""
    print("\n" + "="*60)
    print("TEST 4: Automated Test Suite")
    print("="*60)

    generator = AddAllDigitsProblemGenerator(level=2, difficulty=DifficultyLevel.MEDIUM)
    malrule = AddAllDigitsMalrule()
    correct = AdditionCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, generator)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    print(f"\n  Automated suite: {'PASSED' if all_passed else 'FAILED'}")
    return all_passed


def test_malrule_metadata():
    """Test malrule metadata methods."""
    print("\n" + "="*60)
    print("TEST 5: Malrule Metadata")
    print("="*60)

    malrule = AddAllDigitsMalrule()

    # Test get_name
    name = malrule.get_name()
    assert name == "Add-All-Digits", f"Expected 'Add-All-Digits', got '{name}'"
    print(f"  Name: {name} - PASSED")

    # Test get_description
    desc = malrule.get_description()
    assert len(desc) > 100, "Description should be substantial"
    assert "Brown & Burton" in desc, "Should cite Brown & Burton"
    print(f"  Description length: {len(desc)} chars - PASSED")

    print("\n  All metadata tests PASSED")


def main():
    """Main entry point."""
    print("\n" + "="*68)
    print("  VERIFICATION TEST: Add-All-Digits (Brown & Burton, 1978)  ".center(68))
    print("="*68)

    try:
        test_specific_examples()
        test_all_templates()
        test_calculate_expected_answer()
        test_malrule_metadata()
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
