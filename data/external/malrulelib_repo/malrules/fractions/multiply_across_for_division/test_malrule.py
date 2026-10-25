#!/usr/bin/env python3
"""Comprehensive test script for Multiply-Across-For-Division malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel
from malrules.fractions.multiply_across_for_division import (
    MultiplyAcrossForDivisionProblemGenerator,
    MultiplyAcrossForDivisionMalrule,
    FractionDivisionCorrectAlgorithm
)


def test_all_templates():
    """Test all templates to ensure they work correctly."""
    print("=" * 80)
    print("TESTING MULTIPLY-ACROSS-FOR-DIVISION - ALL TEMPLATES")
    print("=" * 80)

    malrule = MultiplyAcrossForDivisionMalrule()
    correct = FractionDivisionCorrectAlgorithm()
    problem_gen = MultiplyAcrossForDivisionProblemGenerator(
        level=6,
        difficulty=DifficultyLevel.MEDIUM
    )

    templates = problem_gen.get_available_templates()
    all_passed = True

    for template in templates:
        print(f"\n{'='*80}")
        print(f"TEMPLATE: {template}")
        print(f"{'='*80}")

        # Test multiple instances to catch edge cases
        template_passed = True
        for seed in range(100, 105):
            try:
                # Generate problem
                problem = problem_gen.generate(seed=seed, template=template)

                # Solve with both algorithms
                correct_sol = correct.solve(problem)
                malrule_sol = malrule.solve(problem)

                # Check that answers are different (misconception should produce different answer)
                if correct_sol.answer == malrule_sol.answer:
                    # Edge case: misconception produces same answer
                    print(f"\n⚠ EDGE CASE DETECTED (seed={seed}):")
                    print(f"  Problem: {problem.text}")
                    print(f"  Both algorithms produced the same answer: {correct_sol.answer}")
                    print(f"\n  CORRECT STEPS:")
                    for step in correct_sol.steps:
                        print(f"    {step}")
                    print(f"\n  MALRULE STEPS:")
                    for step in malrule_sol.steps:
                        print(f"    {step}")
                    print(f"\n  This is an edge case where the misconception accidentally")
                    print(f"  produces the correct answer. Test FAILED for this seed.")
                    template_passed = False
                    all_passed = False
                    continue

                # Verify metadata is present but not used in calculation
                assert 'correct_answer' in problem.metadata, "Metadata should contain correct_answer"
                assert 'malrule_answer' in problem.metadata, "Metadata should contain malrule_answer"

                # Verify calculated answers match metadata (ensures problem generator is consistent)
                expected_correct = problem.metadata['correct_answer']
                expected_malrule = problem.metadata['malrule_answer']

                if correct_sol.answer != expected_correct:
                    print(f"\n✗ TEST FAILED (seed={seed}):")
                    print(f"  Problem: {problem.text}")
                    print(f"  Correct algorithm answer: {correct_sol.answer}")
                    print(f"  Expected correct answer: {expected_correct}")
                    print(f"\n  CORRECT ALGORITHM STEPS:")
                    for step in correct_sol.steps:
                        print(f"    {step}")
                    template_passed = False
                    all_passed = False
                    continue

                if malrule_sol.answer != expected_malrule:
                    print(f"\n✗ TEST FAILED (seed={seed}):")
                    print(f"  Problem: {problem.text}")
                    print(f"  Malrule algorithm answer: {malrule_sol.answer}")
                    print(f"  Expected malrule answer: {expected_malrule}")
                    print(f"\n  MALRULE ALGORITHM STEPS:")
                    for step in malrule_sol.steps:
                        print(f"    {step}")
                    template_passed = False
                    all_passed = False
                    continue

                # Test passed for this seed
                if seed == 100:  # Print first success for each template
                    print(f"\n✓ PASSED (seed={seed}):")
                    print(f"  Problem: {problem.text}")
                    print(f"  Correct answer: {correct_sol.answer}")
                    print(f"  Malrule answer: {malrule_sol.answer}")

            except Exception as e:
                print(f"\n✗ EXCEPTION (seed={seed}):")
                print(f"  Error: {str(e)}")
                print(f"\n  Problem: {problem.text if 'problem' in locals() else 'N/A'}")
                if 'correct_sol' in locals():
                    print(f"\n  CORRECT ALGORITHM STEPS:")
                    for step in correct_sol.steps:
                        print(f"    {step}")
                if 'malrule_sol' in locals():
                    print(f"\n  MALRULE ALGORITHM STEPS:")
                    for step in malrule_sol.steps:
                        print(f"    {step}")
                import traceback
                traceback.print_exc()
                template_passed = False
                all_passed = False

        if template_passed:
            print(f"\n✓✓✓ Template '{template}' PASSED all tests")
        else:
            print(f"\n✗✗✗ Template '{template}' FAILED")

    print(f"\n{'='*80}")
    if all_passed:
        print("✓✓✓ ALL TEMPLATES PASSED ✓✓✓")
    else:
        print("✗✗✗ SOME TEMPLATES FAILED ✗✗✗")
    print(f"{'='*80}\n")

    return all_passed


def main():
    print("\n╔" + "═"*78 + "╗")
    print("║" + " COMPREHENSIVE TEST: Multiply-Across-For-Division ".center(78) + "║")
    print("╚" + "═"*78 + "╝\n")

    try:
        all_passed = test_all_templates()

        print("\n╔" + "═"*78 + "╗")
        if all_passed:
            print("║" + " ✓✓✓ ALL TESTS PASSED ✓✓✓ ".center(78) + "║")
        else:
            print("║" + " ✗✗✗ SOME TESTS FAILED ✗✗✗ ".center(78) + "║")
        print("╚" + "═"*78 + "╝\n")

        return 0 if all_passed else 1
    except Exception as e:
        print(f"\n✗✗✗ CRITICAL ERROR: {e} ✗✗✗")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
