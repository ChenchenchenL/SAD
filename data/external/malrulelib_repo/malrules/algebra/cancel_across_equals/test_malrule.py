#!/usr/bin/env python3
"""Test script for Cancel-Across-Equals malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.algebra.cancel_across_equals import (
    CancelAcrossEqualsProblemGenerator,
    CancelAcrossEqualsMalrule,
    LinearEquationCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING CANCEL-ACROSS-EQUALS")
    print("="*70)

    malrule = CancelAcrossEqualsMalrule()
    correct = LinearEquationCorrectAlgorithm()

    # Test case 1: 3x = 2x + 6 → Correct: x = 6, Malrule: x = 2
    problem1 = Problem(
        text="Solve for x: 3x = 2x + 6",
        operands=[3, 2, 6],
        operation='solve_equation',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'a': 3,
            'b': 2,
            'c': 6,
            'correct_answer': 6,  # 3x - 2x = 6 → x = 6
            'malrule_answer': 2,  # "Cancel" x → 6/3 = 2
            'template': 'basic_equation'
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: 3x = 2x + 6 → Correct: x = {correct_sol.answer}, Malrule: x = {malrule_sol.answer}")
    assert correct_sol.answer == 6
    assert malrule_sol.answer == 2
    assert correct_sol.answer != malrule_sol.answer
    print("✓ PASSED")

    # Test case 2: 5x = 3x + 4 → Correct: x = 2, Malrule: x = 0.8
    problem2 = Problem(
        text="Solve for x: 5x = 3x + 10",
        operands=[5, 3, 10],
        operation='solve_equation',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'a': 5,
            'b': 3,
            'c': 10,
            'correct_answer': 5,  # 5x - 3x = 10 → 2x = 10 → x = 5
            'malrule_answer': 2,  # "Cancel" x → 10/5 = 2
            'template': 'basic_equation'
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert correct_sol2.answer == 5
    assert malrule_sol2.answer == 2
    print("✓ TEST 2 PASSED")

    # Test case 3: 4x = 2x + 8 → Correct: x = 4, Malrule: x = 2
    problem3 = Problem(
        text="Solve for x: 4x = 2x + 8",
        operands=[4, 2, 8],
        operation='solve_equation',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'a': 4,
            'b': 2,
            'c': 8,
            'correct_answer': 4,  # 4x - 2x = 8 → 2x = 8 → x = 4
            'malrule_answer': 2,  # "Cancel" x → 8/4 = 2
            'template': 'basic_equation'
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert correct_sol3.answer == 4
    assert malrule_sol3.answer == 2
    print("✓ TEST 3 PASSED")

    # Test case 4: 6x = 4x + 12 → Correct: x = 6, Malrule: x = 2
    problem4 = Problem(
        text="Solve for x: 6x = 4x + 12",
        operands=[6, 4, 12],
        operation='solve_equation',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'a': 6,
            'b': 4,
            'c': 12,
            'correct_answer': 6,  # 6x - 4x = 12 → 2x = 12 → x = 6
            'malrule_answer': 2,  # "Cancel" x → 12/6 = 2
            'template': 'basic_equation'
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    assert correct_sol4.answer == 6
    assert malrule_sol4.answer == 2
    print("✓ TEST 4 PASSED")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_all_templates():
    """Test all 5 templates for Cancel-Across-Equals."""
    print("\n\n" + "="*70)
    print("TESTING ALL TEMPLATES")
    print("="*70)

    problem_gen = CancelAcrossEqualsProblemGenerator(
        level=8,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = CancelAcrossEqualsMalrule()
    correct = LinearEquationCorrectAlgorithm()

    templates = problem_gen.get_available_templates()
    print(f"\nFound {len(templates)} templates: {templates}")
    assert len(templates) == 5, f"Expected 5 templates, got {len(templates)}"

    for template in templates:
        print(f"\n--- Testing template: {template} ---")

        # Generate problem with this template
        problem = problem_gen.generate(seed=42, template=template)

        # Solve with both algorithms
        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        # Verify answers
        print(f"  Problem: {problem.text[:80]}...")
        print(f"  Correct answer: {correct_sol.answer}")
        print(f"  Malrule answer: {malrule_sol.answer}")

        # Verify different answers
        assert str(correct_sol.answer) != str(malrule_sol.answer), \
            f"Template {template}: Correct and malrule answers should be different!"

        # Verify calculate_expected_answer matches malrule output
        expected = malrule.calculate_expected_answer(problem)
        print(f"  Expected answer: {expected}")

        assert str(malrule_sol.answer) == str(expected), \
            f"Template {template}: calculate_expected_answer() returned {expected} but malrule produced {malrule_sol.answer}"

        print(f"  ✓ Template {template} PASSED")

    print("\n" + "="*70)
    print("ALL TEMPLATE TESTS PASSED ✓")
    print("="*70)


def test_automated_suite():
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = CancelAcrossEqualsProblemGenerator(
        level=8,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = CancelAcrossEqualsMalrule()
    correct = LinearEquationCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Cancel-Across-Equals  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    try:
        test_specific_examples()
        test_all_templates()
        all_passed = test_automated_suite()
        print("\n\n╔" + "═"*68 + "╗")
        print("║" + "  ✓✓✓ VERIFICATION COMPLETE ✓✓✓  ".center(70) + "║")
        print("╚" + "═"*68 + "╝\n")
        return 0 if all_passed else 1
    except Exception as e:
        print(f"\n✗✗✗ TEST FAILED: {e} ✗✗✗")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
