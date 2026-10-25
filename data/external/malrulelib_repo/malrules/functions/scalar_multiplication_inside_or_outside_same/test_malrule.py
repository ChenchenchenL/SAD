#!/usr/bin/env python3
"""Test script for Scalar-Multiplication-Inside-Or-Outside-Same malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.functions.scalar_multiplication_inside_or_outside_same import (
    ScalarMultiplicationInsideOrOutsideSameProblemGenerator,
    ScalarMultiplicationInsideOrOutsideSameMalrule,
    FunctionEvaluationCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING SCALAR-MULTIPLICATION-INSIDE-OR-OUTSIDE-SAME")
    print("="*70)

    malrule = ScalarMultiplicationInsideOrOutsideSameMalrule()
    correct = FunctionEvaluationCorrectAlgorithm()

    # Test case 1: f(2×3) where f(x)=x² → 36 (correct), 18 (malrule: 2·3²)
    problem1 = Problem(
        text="Given f(x) = x², evaluate f(2×3)",
        operands=[2, 3],
        operation='function_evaluation',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'scalar': 2,
            'input': 3,
            'function': 'x²',
            'correct_answer': 36,
            'malrule_answer': 18
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: f(2×3) where f(x)=x² → Correct: {correct_sol.answer}, Malrule: {malrule_sol.answer}")
    assert correct_sol.answer == 36
    assert malrule_sol.answer == 18
    assert correct_sol.answer != malrule_sol.answer
    print("✓ PASSED")

    # Test case 2: f(3×2) where f(x)=x² → 36 (correct), 12 (malrule: 3·2²)
    problem2 = Problem(
        text="Given f(x) = x², evaluate f(3×2)",
        operands=[3, 2],
        operation='function_evaluation',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'scalar': 3,
            'input': 2,
            'function': 'x²',
            'correct_answer': 36,
            'malrule_answer': 12
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert correct_sol2.answer == 36
    assert malrule_sol2.answer == 12
    print("✓ TEST 2 PASSED")

    # Test case 3: f(2×4) where f(x)=x² → 64 (correct), 32 (malrule: 2·4²)
    problem3 = Problem(
        text="Given f(x) = x², evaluate f(2×4)",
        operands=[2, 4],
        operation='function_evaluation',
        level=10,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'scalar': 2,
            'input': 4,
            'function': 'x²',
            'correct_answer': 64,
            'malrule_answer': 32
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert correct_sol3.answer == 64
    assert malrule_sol3.answer == 32
    print("✓ TEST 3 PASSED")

    # Test case 4: f(4×3) where f(x)=x² → 144 (correct), 36 (malrule: 4·3²)
    problem4 = Problem(
        text="Given f(x) = x², evaluate f(4×3)",
        operands=[4, 3],
        operation='function_evaluation',
        level=10,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'scalar': 4,
            'input': 3,
            'function': 'x²',
            'correct_answer': 144,
            'malrule_answer': 36
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    assert correct_sol4.answer == 144
    assert malrule_sol4.answer == 36
    print("✓ TEST 4 PASSED")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_all_templates():
    """Test all 5 templates for Scalar-Multiplication-Inside-Or-Outside-Same."""
    print("\n\n" + "="*70)
    print("TESTING ALL TEMPLATES")
    print("="*70)

    problem_gen = ScalarMultiplicationInsideOrOutsideSameProblemGenerator(
        level=9,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = ScalarMultiplicationInsideOrOutsideSameMalrule()
    correct = FunctionEvaluationCorrectAlgorithm()

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

        # Verify different answers
        print(f"  Correct answer: {correct_sol.answer}")
        print(f"  Malrule answer: {malrule_sol.answer}")

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

    problem_gen = ScalarMultiplicationInsideOrOutsideSameProblemGenerator(
        level=9,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = ScalarMultiplicationInsideOrOutsideSameMalrule()
    correct = FunctionEvaluationCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Scalar-Multiplication-Inside-Or-Outside-Same  ".center(70) + "║")
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
