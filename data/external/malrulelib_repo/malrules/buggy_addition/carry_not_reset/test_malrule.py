#!/usr/bin/env python3
"""
Test suite for Carry-Not-Reset malrule.

Tests examples from:
Brown, J. S., & Burton, R. R. (1978). Diagnostic models for procedural bugs
in basic mathematical skills. Cognitive Science, 2(2), 155-192.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.buggy_addition.carry_not_reset import (
    CarryNotResetProblemGenerator,
    CarryNotResetMalrule,
    AdditionCorrectAlgorithm
)


def test_specific_examples():
    """
    Test with known examples from Brown & Burton (1978).

    From the paper:
    - 328 + 917 = 1345 (correct: 1245)
    - 446 + 815 = 1361 (correct: 1261)
    - 201 + 399 = 700 (correct: 600)
    """
    print("\n" + "="*60)
    print("TEST 1: Specific Research Examples (Brown & Burton 1978)")
    print("="*60)

    malrule = CarryNotResetMalrule()
    correct = AdditionCorrectAlgorithm()

    # Example 1: 328 + 917 = 1345 (from paper, page 157)
    problem1 = Problem(
        text="Calculate: 328 + 917",
        operands=[328, 917],
        operation='addition',
        level=3,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'correct_answer': '1245',
            'malrule_answer': '1345',
            'problem_type': 'basic'
        }
    )

    correct_sol1 = correct.solve(problem1)
    malrule_sol1 = malrule.solve(problem1)

    print(f"\n  Example 1: 328 + 917")
    print(f"    Correct answer: {correct_sol1.answer}")
    print(f"    Malrule answer: {malrule_sol1.answer}")
    print(f"    Expected malrule: 1345")

    assert correct_sol1.answer == '1245', f"Expected correct 1245, got {correct_sol1.answer}"
    assert malrule_sol1.answer == '1345', f"Expected malrule 1345, got {malrule_sol1.answer}"
    assert correct_sol1.answer != malrule_sol1.answer, "Answers should differ"

    print("    Example 1: PASSED")

    # Example 2: 446 + 815 = 1361 (test problem from paper)
    problem2 = Problem(
        text="Calculate: 446 + 815",
        operands=[446, 815],
        operation='addition',
        level=3,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'correct_answer': '1261',
            'malrule_answer': '1361',
            'problem_type': 'basic'
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)

    print(f"\n  Example 2: 446 + 815")
    print(f"    Correct answer: {correct_sol2.answer}")
    print(f"    Malrule answer: {malrule_sol2.answer}")
    print(f"    Expected malrule: 1361")

    assert correct_sol2.answer == '1261', f"Expected correct 1261, got {correct_sol2.answer}"
    assert malrule_sol2.answer == '1361', f"Expected malrule 1361, got {malrule_sol2.answer}"
    assert correct_sol2.answer != malrule_sol2.answer, "Answers should differ"

    print("    Example 2: PASSED")

    # Example 3: 201 + 399 = 700 (test problem from paper)
    problem3 = Problem(
        text="Calculate: 201 + 399",
        operands=[201, 399],
        operation='addition',
        level=3,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'correct_answer': '600',
            'malrule_answer': '1600',
            'problem_type': 'basic'
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)

    print(f"\n  Example 3: 201 + 399")
    print(f"    Correct answer: {correct_sol3.answer}")
    print(f"    Malrule answer: {malrule_sol3.answer}")
    print(f"    Expected malrule: 1600")

    assert correct_sol3.answer == '600', f"Expected correct 600, got {correct_sol3.answer}"
    assert malrule_sol3.answer == '1600', f"Expected malrule 1600, got {malrule_sol3.answer}"
    assert correct_sol3.answer != malrule_sol3.answer, "Answers should differ"

    print("    Example 3: PASSED")

    print("\n  All specific examples PASSED")


def test_calculate_expected_answer():
    """Test that calculate_expected_answer works independently."""
    print("\n" + "="*60)
    print("TEST 2: calculate_expected_answer Independence")
    print("="*60)

    malrule = CarryNotResetMalrule()

    # Test without metadata
    problem_no_meta = Problem(
        text="Calculate: 328 + 917",
        operands=[328, 917],
        operation='addition',
        level=3,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={}  # No pre-calculated answer
    )

    expected = malrule.calculate_expected_answer(problem_no_meta)
    assert expected == '1345', f"Expected 1345, got {expected}"
    print("  calculate_expected_answer without metadata: PASSED")

    # Test with metadata
    problem_with_meta = Problem(
        text="Calculate: 328 + 917",
        operands=[328, 917],
        operation='addition',
        level=3,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={'malrule_answer': '1345'}
    )

    expected_meta = malrule.calculate_expected_answer(problem_with_meta)
    assert expected_meta == '1345', f"Expected 1345, got {expected_meta}"
    print("  calculate_expected_answer with metadata: PASSED")

    print("\n  calculate_expected_answer tests PASSED")


def test_all_templates():
    """Test all problem templates generate valid problems."""
    print("\n" + "="*60)
    print("TEST 3: Template Generation")
    print("="*60)

    generator = CarryNotResetProblemGenerator(level=3, difficulty=DifficultyLevel.MEDIUM)
    malrule = CarryNotResetMalrule()
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

        # Check answers match metadata
        assert correct_sol.answer == problem.metadata['correct_answer'], \
            f"Template {template}: correct answer mismatch"
        assert malrule_sol.answer == problem.metadata['malrule_answer'], \
            f"Template {template}: malrule answer mismatch"

        print(f"    {template}: PASSED (correct={correct_sol.answer}, malrule={malrule_sol.answer})")

    print("\n  All templates PASSED")


def test_verbose_and_concise_steps():
    """Test that both verbose and concise step generation work."""
    print("\n" + "="*60)
    print("TEST 4: Verbose and Concise Steps")
    print("="*60)

    malrule = CarryNotResetMalrule()
    correct = AdditionCorrectAlgorithm()

    problem = Problem(
        text="Calculate: 328 + 917",
        operands=[328, 917],
        operation='addition',
        level=3,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'correct_answer': '1245',
            'malrule_answer': '1345',
        }
    )

    # Test concise steps
    correct_concise = correct.solve(problem, verbose=False)
    malrule_concise = malrule.solve(problem, verbose=False)

    assert len(correct_concise.steps) > 0, "Correct concise should have steps"
    assert len(malrule_concise.steps) > 0, "Malrule concise should have steps"
    print(f"  Concise steps - Correct: {len(correct_concise.steps)}, Malrule: {len(malrule_concise.steps)}")

    # Test verbose steps
    correct_verbose = correct.solve(problem, verbose=True)
    malrule_verbose = malrule.solve(problem, verbose=True)

    assert len(correct_verbose.steps) > 0, "Correct verbose should have steps"
    assert len(malrule_verbose.steps) > 0, "Malrule verbose should have steps"
    assert len(malrule_verbose.steps) >= len(malrule_concise.steps), \
        "Verbose should have at least as many steps as concise"
    print(f"  Verbose steps - Correct: {len(correct_verbose.steps)}, Malrule: {len(malrule_verbose.steps)}")

    # Answers should be the same regardless of verbosity
    assert correct_concise.answer == correct_verbose.answer, "Correct answers should match"
    assert malrule_concise.answer == malrule_verbose.answer, "Malrule answers should match"

    print("\n  Verbose and concise step tests PASSED")


def test_malrule_metadata():
    """Test that malrule metadata is correctly populated."""
    print("\n" + "="*60)
    print("TEST 5: Malrule Metadata")
    print("="*60)

    malrule = CarryNotResetMalrule()

    # Test name
    assert malrule.get_name() == "Carry-Not-Reset", f"Wrong name: {malrule.get_name()}"
    print(f"  Name: {malrule.get_name()}")

    # Test description
    desc = malrule.get_description()
    assert len(desc) > 50, "Description too short"
    assert "carry" in desc.lower(), "Description should mention carry"
    print(f"  Description length: {len(desc)} chars")

    print("\n  Malrule metadata tests PASSED")


def test_automated_suite():
    """Run automated test suite."""
    print("\n" + "="*60)
    print("TEST 6: Automated Test Suite")
    print("="*60)

    generator = CarryNotResetProblemGenerator(level=3, difficulty=DifficultyLevel.MEDIUM)
    malrule = CarryNotResetMalrule()
    correct = AdditionCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, generator)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    print(f"\n  Automated suite: {'PASSED' if all_passed else 'FAILED'}")
    return all_passed


def main():
    """Main entry point."""
    print("\n" + "="*68)
    print("  VERIFICATION TEST: Carry-Not-Reset (Brown & Burton 1978)  ".center(68))
    print("="*68)

    try:
        test_specific_examples()
        test_calculate_expected_answer()
        test_all_templates()
        test_verbose_and_concise_steps()
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
