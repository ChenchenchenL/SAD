#!/usr/bin/env python3
"""Test script for Negative-Swaps-Operation malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.negative_numbers.negative_swaps_operation import (
    NegativeSwapsOperationProblemGenerator,
    NegativeSwapsOperationMalrule,
    NegativeArithmeticCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING NEGATIVE-SWAPS-OPERATION")
    print("="*70)

    malrule = NegativeSwapsOperationMalrule()
    correct = NegativeArithmeticCorrectAlgorithm()

    # Test case 1: 10 + (-3) = 7 (correct), 13 (malrule swaps to +)
    problem1 = Problem(
        text="Calculate: 10 + (-3)",
        operands=[10, -3],
        operation='arithmetic',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'num1': 10,
            'num2': -3,
            'operator': '+',
            'correct_answer': 7,
            'malrule_answer': 13,
            'operation_type': 'add_negative',
            'template': 'basic_arithmetic'
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: 10 + (-3) → Correct: {correct_sol.answer}, Malrule: {malrule_sol.answer}")
    assert correct_sol.answer == 7
    assert malrule_sol.answer == 13
    assert correct_sol.answer != malrule_sol.answer
    print("✓ PASSED")

    # Test case 2: 8 - (-5) = 13 (correct), 3 (malrule keeps -)
    problem2 = Problem(
        text="Calculate: 8 - (-5)",
        operands=[8, -5],
        operation='arithmetic',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'num1': 8,
            'num2': -5,
            'operator': '-',
            'correct_answer': 13,
            'malrule_answer': 3,
            'operation_type': 'subtract_negative',
            'template': 'basic_arithmetic'
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert correct_sol2.answer == 13
    assert malrule_sol2.answer == 3
    print("✓ TEST 2 PASSED")

    # Test case 3: 15 + (-7) = 8 (correct), 22 (malrule)
    problem3 = Problem(
        text="Calculate: 15 + (-7)",
        operands=[15, -7],
        operation='arithmetic',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'num1': 15,
            'num2': -7,
            'operator': '+',
            'correct_answer': 8,
            'malrule_answer': 22,
            'operation_type': 'add_negative',
            'template': 'basic_arithmetic'
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert correct_sol3.answer == 8
    assert malrule_sol3.answer == 22
    print("✓ TEST 3 PASSED")

    # Test case 4: 12 - (-4) = 16 (correct), 8 (malrule)
    problem4 = Problem(
        text="Calculate: 12 - (-4)",
        operands=[12, -4],
        operation='arithmetic',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'num1': 12,
            'num2': -4,
            'operator': '-',
            'correct_answer': 16,
            'malrule_answer': 8,
            'operation_type': 'subtract_negative',
            'template': 'basic_arithmetic'
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    assert correct_sol4.answer == 16
    assert malrule_sol4.answer == 8
    print("✓ TEST 4 PASSED")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_all_templates():
    """Test all 5 templates for Negative-Swaps-Operation."""
    print("\n\n" + "="*70)
    print("TESTING ALL TEMPLATES")
    print("="*70)

    problem_gen = NegativeSwapsOperationProblemGenerator(
        level=8,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = NegativeSwapsOperationMalrule()
    correct = NegativeArithmeticCorrectAlgorithm()

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

    problem_gen = NegativeSwapsOperationProblemGenerator(
        level=8,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = NegativeSwapsOperationMalrule()
    correct = NegativeArithmeticCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Negative-Swaps-Operation  ".center(70) + "║")
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
