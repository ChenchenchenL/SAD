#!/usr/bin/env python3
"""
Test suite for DIFF/N-0=0 malrule.

Run from project root: python3 -m buggy_malrules.subtraction.diff_n_0_equals_0.test_malrule
Or from this directory: python3 test_malrule.py

This malrule is documented in:
Brown, J. S., & Burton, R. R. (1978). Diagnostic models for procedural bugs
in basic mathematical skills. Cognitive Science, 2(2), 155-192.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.buggy_subtraction.diff_n_0_equals_0 import (
    DiffN0Equals0ProblemGenerator,
    DiffN0Equals0Malrule,
    SubtractionCorrectAlgorithm
)


def test_paper_example():
    """
    Test 1: Brown & Burton (1978) paper example.

    The paper provides this specific example:
    403 - 208 = 105 (correct: 195)

    Breakdown:
    - Ones: 3-8 requires borrow -> 13-8=5 (correct)
    - Tens: 9-0, student writes 0 (BUG!) instead of 9
    - Hundreds: 3-2=1 (correct)
    """
    print("\n" + "="*60)
    print("TEST 1: Brown & Burton (1978) Paper Example")
    print("="*60)

    malrule = DiffN0Equals0Malrule()
    correct = SubtractionCorrectAlgorithm()

    # Exact example from the paper
    problem = Problem(
        text="What is 403 - 208?",
        operands=[403, 208],
        operation='subtraction',
        level=4,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'correct_answer': '195',
            'malrule_answer': '105',
            'problem_type': 'basic'
        }
    )

    correct_sol = correct.solve(problem)
    malrule_sol = malrule.solve(problem)

    print(f"  Problem: 403 - 208")
    print(f"  Correct answer: {correct_sol.answer} (expected: 195)")
    print(f"  Malrule answer: {malrule_sol.answer} (expected: 105)")

    assert correct_sol.answer == '195', f"Expected correct=195, got {correct_sol.answer}"
    assert malrule_sol.answer == '105', f"Expected malrule=105, got {malrule_sol.answer}"
    assert correct_sol.answer != malrule_sol.answer, "Answers should differ"

    print("  Paper example: PASSED")


def test_specific_examples():
    """
    Test 2: Multiple specific examples to verify DIFF/N-0=0 behavior.

    The bug: When bottom digit is 0, student writes 0 instead of top digit.
    """
    print("\n" + "="*60)
    print("TEST 2: Specific Research Examples")
    print("="*60)

    malrule = DiffN0Equals0Malrule()
    correct = SubtractionCorrectAlgorithm()

    # Test cases: [minuend, subtrahend, expected_correct, expected_malrule]
    test_cases = [
        # Paper example
        (403, 208, 195, 105),
        # Simple case: N-0 in ones place
        (75, 30, 45, 40),
        # Multiple 0s in subtrahend
        (543, 200, 343, 300),
        # 0 in tens place of subtrahend
        (456, 203, 253, 203),
        # 0 in hundreds place (effectively 0 padding)
        (1234, 1002, 232, 2),
    ]

    for i, (minuend, subtrahend, expected_correct, expected_malrule) in enumerate(test_cases, 1):
        problem = Problem(
            text=f"What is {minuend} - {subtrahend}?",
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=4,
            difficulty=DifficultyLevel.MEDIUM,
            metadata={
                'correct_answer': str(expected_correct),
                'malrule_answer': str(expected_malrule),
                'problem_type': 'basic'
            }
        )

        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        assert correct_sol.answer == str(expected_correct), \
            f"Example {i}: Expected correct={expected_correct}, got {correct_sol.answer}"
        assert malrule_sol.answer == str(expected_malrule), \
            f"Example {i}: Expected malrule={expected_malrule}, got {malrule_sol.answer}"

        print(f"  Example {i}: {minuend} - {subtrahend} = {malrule_sol.answer} "
              f"(correct: {correct_sol.answer}) PASSED")

    print("\n  All specific examples PASSED")


def test_all_templates():
    """
    Test 3: All problem templates generate valid problems.

    Ensures each template:
    1. Generates a problem with required metadata
    2. Has different correct and malrule answers
    3. The malrule answer reflects the N-0=0 bug
    """
    print("\n" + "="*60)
    print("TEST 3: Template Generation")
    print("="*60)

    generator = DiffN0Equals0ProblemGenerator(level=4, difficulty=DifficultyLevel.MEDIUM)
    malrule = DiffN0Equals0Malrule()
    correct = SubtractionCorrectAlgorithm()

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

        # Verify answers match metadata
        assert correct_sol.answer == problem.metadata['correct_answer'], \
            f"Template {template}: correct answer mismatch"
        assert malrule_sol.answer == problem.metadata['malrule_answer'], \
            f"Template {template}: malrule answer mismatch"

        # Verify answers differ (since we generate problems with N-0 opportunity)
        assert correct_sol.answer != malrule_sol.answer, \
            f"Template {template}: answers should differ for N-0 problems"

        print(f"    {template}: PASSED (correct={correct_sol.answer}, malrule={malrule_sol.answer})")

    print("\n  All templates PASSED")


def test_malrule_metadata():
    """
    Test 4: Malrule class provides required metadata.
    """
    print("\n" + "="*60)
    print("TEST 4: Malrule Metadata")
    print("="*60)

    malrule = DiffN0Equals0Malrule()

    # Test name
    assert malrule.get_name() == "DIFF/N-0=0", \
        f"Expected name 'DIFF/N-0=0', got '{malrule.get_name()}'"
    print("  Name: PASSED")

    # Test description exists and mentions key concepts
    desc = malrule.get_description()
    assert len(desc) > 100, "Description should be detailed"
    assert "N-0=0" in desc or "N-0" in desc, "Description should mention the bug pattern"
    print("  Description: PASSED")

    print("\n  All metadata PASSED")


def test_calculate_expected_answer_independent():
    """
    Test 5: calculate_expected_answer works independently (does NOT call solve()).

    This is a critical requirement from the implementation guide.
    """
    print("\n" + "="*60)
    print("TEST 5: Independent Answer Calculation")
    print("="*60)

    malrule = DiffN0Equals0Malrule()

    # Test with metadata
    problem_with_meta = Problem(
        text="What is 403 - 208?",
        operands=[403, 208],
        operation='subtraction',
        level=4,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={'malrule_answer': '105'}
    )
    answer_meta = malrule.calculate_expected_answer(problem_with_meta)
    assert answer_meta == '105', f"Expected 105 from metadata, got {answer_meta}"
    print("  With metadata: PASSED")

    # Test without metadata (should calculate from operands)
    problem_no_meta = Problem(
        text="What is 456 - 203?",
        operands=[456, 203],
        operation='subtraction',
        level=4,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={}
    )
    answer_calc = malrule.calculate_expected_answer(problem_no_meta)
    # 456 - 203: ones 6-3=3, tens 5-0=0(BUG), hundreds 4-2=2 -> 203
    assert answer_calc == '203', f"Expected 203 from calculation, got {answer_calc}"
    print("  Without metadata (calculated): PASSED")

    print("\n  Independent calculation PASSED")


def test_automated_suite():
    """
    Test 6: Run automated test suite using MalruleTest framework.
    """
    print("\n" + "="*60)
    print("TEST 6: Automated Test Suite")
    print("="*60)

    generator = DiffN0Equals0ProblemGenerator(level=4, difficulty=DifficultyLevel.MEDIUM)
    malrule = DiffN0Equals0Malrule()
    correct = SubtractionCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, generator)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    print(f"\n  Automated suite: {'PASSED' if all_passed else 'FAILED'}")
    return all_passed


def main():
    """Main entry point for testing."""
    print("\n" + "="*68)
    print("  VERIFICATION TEST: DIFF/N-0=0 (Brown & Burton, 1978)  ".center(68))
    print("  Student writes 0 when bottom digit is 0 (N-0=0)  ".center(68))
    print("="*68)

    try:
        test_paper_example()
        test_specific_examples()
        test_all_templates()
        test_malrule_metadata()
        test_calculate_expected_answer_independent()
        all_passed = test_automated_suite()

        print("\n" + "="*68)
        if all_passed:
            print("  VERIFICATION COMPLETE - ALL TESTS PASSED  ".center(68))
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
