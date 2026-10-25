#!/usr/bin/env python3
"""Test script for Multiply-Exponents-When-Multiplying-Powers malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel
from malrules.exponents.multiply_exponents_when_multiplying_powers import (
    MultiplyExponentsWhenMultiplyingPowersProblemGenerator,
    MultiplyExponentsWhenMultiplyingPowersMalrule,
    ProductRuleCorrectAlgorithm
)


def test_all_templates():
    """Test all problem templates comprehensively."""
    print("="*70)
    print("TESTING ALL TEMPLATES - MULTIPLY-EXPONENTS-WHEN-MULTIPLYING-POWERS")
    print("="*70)

    problem_gen = MultiplyExponentsWhenMultiplyingPowersProblemGenerator(
        level=8,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = MultiplyExponentsWhenMultiplyingPowersMalrule()
    correct = ProductRuleCorrectAlgorithm()

    templates = problem_gen.get_available_templates()
    print(f"\nFound {len(templates)} templates to test")
    print(f"Templates: {templates}\n")

    all_passed = True

    for template in templates:
        print(f"\n{'='*70}")
        print(f"Testing template: {template}")
        print('='*70)

        # Test multiple seeds to ensure robustness
        for seed in [42, 123, 789]:
            try:
                problem = problem_gen.generate(seed=seed, template=template)

                # Solve with both algorithms
                correct_sol = correct.solve(problem)
                malrule_sol = malrule.solve(problem)

                # Check if answers are different (they should be for this malrule)
                if correct_sol.answer == malrule_sol.answer:
                    # Edge case: misconception produces same answer
                    print(f"\n⚠️  EDGE CASE DETECTED (seed={seed}):")
                    print(f"Problem: {problem.text}")
                    print(f"Correct and malrule produce SAME answer: {correct_sol.answer}")
                    print("\n--- CORRECT ALGORITHM STEPS ---")
                    for step in correct_sol.steps:
                        print(step)
                    print("\n--- MALRULE ALGORITHM STEPS ---")
                    for step in malrule_sol.steps:
                        print(step)
                    print("\n✗ TEST FAILED: Answers should differ!")
                    all_passed = False
                    continue

                # Test passed for this seed
                print(f"✓ Seed {seed}: PASSED")
                print(f"  Problem: {problem.text}")
                print(f"  Correct answer: {correct_sol.answer}")
                print(f"  Malrule answer: {malrule_sol.answer}")

            except Exception as e:
                print(f"\n✗ EXCEPTION (seed={seed}):")
                print(f"Problem: {problem.text if 'problem' in locals() else 'N/A'}")
                print(f"Error: {e}")
                import traceback
                traceback.print_exc()
                all_passed = False

    print(f"\n{'='*70}")
    if all_passed:
        print("✓✓✓ ALL TEMPLATE TESTS PASSED ✓✓✓")
    else:
        print("✗✗✗ SOME TESTS FAILED ✗✗✗")
    print('='*70)

    return all_passed


def test_specific_edge_cases():
    """Test specific edge cases manually."""
    print("\n\n" + "="*70)
    print("TESTING SPECIFIC EDGE CASES")
    print("="*70)

    malrule = MultiplyExponentsWhenMultiplyingPowersMalrule()
    correct = ProductRuleCorrectAlgorithm()
    problem_gen = MultiplyExponentsWhenMultiplyingPowersProblemGenerator(
        level=8,
        difficulty=DifficultyLevel.MEDIUM
    )

    # Edge case 1: Check if problem generator properly avoids m+n = m*n
    print("\nEdge case check: Verifying problem generator avoids m+n = m*n")
    passed = True
    for i in range(100):
        problem = problem_gen.generate(seed=i, template='basic_two_powers')
        m = problem.metadata['exponent1']
        n = problem.metadata['exponent2']

        if m + n == m * n:
            print(f"✗ Found problematic case: m={m}, n={n} where {m}+{n} = {m}*{n}")
            passed = False

    if passed:
        print("✓ Problem generator properly avoids m+n = m*n cases")

    # Edge case 2: Verify algorithms calculate correctly
    print("\nEdge case check: Verify algorithms calculate (not retrieve) answers")

    # Create a test problem with intentionally wrong metadata answers
    from utils import Problem
    test_problem = Problem(
        text="Simplify: x^3 × x^5",
        operands=[3, 5],
        operation='multiply_powers',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'template': 'basic_two_powers',
            'exponent1': 3,
            'exponent2': 5,
            'correct_answer': 999,  # WRONG on purpose
            'malrule_answer': 888   # WRONG on purpose
        }
    )

    correct_sol = correct.solve(test_problem)
    malrule_sol = malrule.solve(test_problem)

    # Algorithms should calculate 3+5=8 and 3*5=15, NOT use the metadata
    if correct_sol.answer == "x^8":
        print("✓ Correct algorithm CALCULATES answer (x^8), ignores metadata (999)")
    else:
        print(f"✗ Correct algorithm returned {correct_sol.answer}, expected x^8")
        passed = False

    if malrule_sol.answer == "x^15":
        print("✓ Malrule algorithm CALCULATES answer (x^15), ignores metadata (888)")
    else:
        print(f"✗ Malrule algorithm returned {malrule_sol.answer}, expected x^15")
        passed = False

    print("\n" + "="*70)
    if passed:
        print("✓ ALL EDGE CASE TESTS PASSED")
    else:
        print("✗ SOME EDGE CASE TESTS FAILED")
    print("="*70)

    return passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  COMPREHENSIVE TEST: Multiply-Exponents-When-Multiplying-Powers  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    try:
        templates_passed = test_all_templates()
        edge_cases_passed = test_specific_edge_cases()

        all_passed = templates_passed and edge_cases_passed

        print("\n\n╔" + "═"*68 + "╗")
        if all_passed:
            print("║" + "  ✓✓✓ ALL TESTS PASSED ✓✓✓  ".center(70) + "║")
        else:
            print("║" + "  ✗✗✗ SOME TESTS FAILED ✗✗✗  ".center(70) + "║")
        print("╚" + "═"*68 + "╝\n")

        return 0 if all_passed else 1
    except Exception as e:
        print(f"\n✗✗✗ TEST FAILED WITH EXCEPTION: {e} ✗✗✗")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
