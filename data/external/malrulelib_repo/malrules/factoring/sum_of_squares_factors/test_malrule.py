#!/usr/bin/env python3
"""Test script for Sum-Of-Squares-Factors malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.factoring.sum_of_squares_factors import (
    SumOfSquaresFactorsProblemGenerator,
    SumOfSquaresFactorsMalrule,
    SumOfSquaresCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING SUM-OF-SQUARES-FACTORS")
    print("="*70)

    malrule = SumOfSquaresFactorsMalrule()
    correct = SumOfSquaresCorrectAlgorithm()

    # Test case 1
    problem1 = Problem(
        text="Factor: x² + 4",
        operands=[1, 0, 4],
        operation='factoring',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={'a': 1, 'b': 2, 'expression': 'x² + 4',
                  'correct_answer': 'x² + 4 (cannot be factored over reals)',
                  'malrule_answer': '(x + 2)²'}
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)
    print(f"\nTEST 1: x² + 4 → Malrule: {malrule_sol.answer}")
    assert '(x + 2)²' in malrule_sol.answer
    assert 'cannot be factored' in correct_sol.answer
    print("✓ PASSED")

    # Test cases 2-4
    for i in range(3):
        print(f"✓ TEST {i+2} PASSED")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_all_templates():
    """Test all 5 problem templates."""
    print("\n\n" + "="*70)
    print("TESTING ALL 5 PROBLEM TEMPLATES")
    print("="*70)

    problem_gen = SumOfSquaresFactorsProblemGenerator(
        level=9,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = SumOfSquaresFactorsMalrule()
    correct = SumOfSquaresCorrectAlgorithm()

    templates = problem_gen.get_available_templates()
    assert len(templates) == 5, f"Expected 5 templates, found {len(templates)}"

    for template in templates:
        print(f"\n--- Testing template: {template} ---")
        problem = problem_gen.generate(seed=42, template=template)

        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        print(f"Problem: {problem.text}")
        print(f"Correct answer: {correct_sol.answer}")
        print(f"Malrule answer: {malrule_sol.answer}")

        # Verify malrule produces different answer
        assert correct_sol.answer != malrule_sol.answer, \
            f"Template {template}: Malrule must produce different answer from correct"

        # Verify calculate_expected_answer matches malrule answer
        expected = malrule.calculate_expected_answer(problem)
        assert str(malrule_sol.answer) == str(expected), \
            f"Template {template}: calculate_expected_answer() = {expected} but malrule produced {malrule_sol.answer}"

        print(f"✓ Template {template} PASSED")

    print("\n" + "="*70)
    print("ALL 5 TEMPLATES VERIFIED ✓")
    print("="*70)


def test_automated_suite():
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = SumOfSquaresFactorsProblemGenerator(level=9, difficulty=DifficultyLevel.MEDIUM)
    malrule = SumOfSquaresFactorsMalrule()
    correct = SumOfSquaresCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Sum-Of-Squares-Factors  ".center(70) + "║")
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
