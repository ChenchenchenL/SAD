#!/usr/bin/env python3
"""Test script for Square-Root-Equals-Plus-Minus malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel
from malrules.radicals.square_root_equals_plus_minus import (
    SquareRootEqualsPlusMinusProblemGenerator,
    SquareRootEqualsPlusMinusMalrule,
    SquareRootCorrectAlgorithm
)


def test_all_templates():
    """Test all available templates."""
    print("="*70)
    print("TESTING ALL TEMPLATES")
    print("="*70)

    generator = SquareRootEqualsPlusMinusProblemGenerator(
        level=9,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = SquareRootEqualsPlusMinusMalrule()
    correct = SquareRootCorrectAlgorithm()

    templates = generator.get_available_templates()
    print(f"\nFound {len(templates)} templates: {templates}")

    all_passed = True
    for template_name in templates:
        print(f"\n{'='*70}")
        print(f"Testing template: {template_name}")
        print(f"{'='*70}")

        try:
            # Generate problem with specific template
            problem = generator.generate(seed=42, template=template_name)
            print(f"\nProblem text: {problem.text}")
            print(f"Problem metadata: radicand={problem.metadata.get('radicand')}, "
                  f"base={problem.metadata.get('base')}, "
                  f"problem_type={problem.metadata.get('problem_type')}")

            # Solve with both algorithms
            correct_sol = correct.solve(problem)
            malrule_sol = malrule.solve(problem)

            print(f"\nCorrect answer computed: {correct_sol.answer}")
            print(f"Malrule answer computed: {malrule_sol.answer}")

            # Get expected answers from metadata for validation
            expected_correct = problem.metadata.get('correct_answer')
            expected_malrule = problem.metadata.get('malrule_answer')
            print(f"Expected correct (from metadata): {expected_correct}")
            print(f"Expected malrule (from metadata): {expected_malrule}")

            # Validate that algorithms produce expected answers
            def normalize_answer(ans):
                """Normalize answer for comparison."""
                if isinstance(ans, str):
                    return ans.strip()
                return str(ans)

            correct_computed = normalize_answer(correct_sol.answer)
            expected_correct_norm = normalize_answer(expected_correct)

            # For correct algorithm, check exact match
            if correct_computed != expected_correct_norm:
                print(f"\n❌ FAILED: Correct algorithm mismatch!")
                print(f"   Computed: {correct_computed}")
                print(f"   Expected: {expected_correct_norm}")
                print("\nCorrect algorithm steps:")
                for step in correct_sol.steps:
                    print(f"  {step}")
                all_passed = False
                continue

            # For malrule, check that it differs from correct
            # (We're using -base or ±base notation to represent the misconception)
            if correct_sol.answer == malrule_sol.answer:
                # This is an edge case - misconception produces same answer
                print(f"\n⚠️  WARNING: Edge case detected - malrule produces same answer as correct!")
                print(f"   This can happen in edge cases. Printing steps:")
                print("\nCorrect algorithm steps:")
                for step in correct_sol.steps:
                    print(f"  {step}")
                print("\nMalrule algorithm steps:")
                for step in malrule_sol.steps:
                    print(f"  {step}")
                # Fail the test as requested for edge cases
                all_passed = False
                continue

            # Success!
            print(f"\n✓ PASSED: {template_name}")
            print(f"   Correct answer: {correct_sol.answer}")
            print(f"   Malrule answer: {malrule_sol.answer}")

        except Exception as e:
            print(f"\n❌ FAILED with exception: {e}")
            import traceback
            traceback.print_exc()
            all_passed = False

    print(f"\n{'='*70}")
    if all_passed:
        print("✓✓✓ ALL TEMPLATE TESTS PASSED ✓✓✓")
    else:
        print("✗✗✗ SOME TEMPLATE TESTS FAILED ✗✗✗")
    print(f"{'='*70}")

    return all_passed


def test_comprehensive_cases():
    """Test comprehensive set of cases to verify algorithmic solving."""
    print("\n\n" + "="*70)
    print("COMPREHENSIVE TEST CASES")
    print("="*70)

    generator = SquareRootEqualsPlusMinusProblemGenerator(
        level=8,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = SquareRootEqualsPlusMinusMalrule()
    correct = SquareRootCorrectAlgorithm()

    test_cases = [
        {'radicand': 4, 'expected_correct': 2, 'name': '√4'},
        {'radicand': 9, 'expected_correct': 3, 'name': '√9'},
        {'radicand': 16, 'expected_correct': 4, 'name': '√16'},
        {'radicand': 25, 'expected_correct': 5, 'name': '√25'},
        {'radicand': 36, 'expected_correct': 6, 'name': '√36'},
        {'radicand': 49, 'expected_correct': 7, 'name': '√49'},
        {'radicand': 64, 'expected_correct': 8, 'name': '√64'},
        {'radicand': 81, 'expected_correct': 9, 'name': '√81'},
        {'radicand': 100, 'expected_correct': 10, 'name': '√100'},
    ]

    all_passed = True
    for test in test_cases:
        radicand = test['radicand']
        expected = test['expected_correct']
        name = test['name']

        # Generate problem with this specific radicand
        problem = generator.generate(seed=radicand * 100, template='basic_square_root')

        # Override radicand in metadata to test specific value
        problem.metadata['radicand'] = radicand

        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        # Normalize for comparison
        computed = correct_sol.answer
        if isinstance(computed, str):
            computed = int(computed)

        if computed == expected:
            print(f"✓ {name}: correct={correct_sol.answer}, malrule={malrule_sol.answer}")
        else:
            print(f"❌ {name}: FAILED - expected {expected}, got {computed}")
            print("   Steps:")
            for step in correct_sol.steps:
                print(f"     {step}")
            all_passed = False

        # Verify malrule gives different answer
        if correct_sol.answer == malrule_sol.answer:
            print(f"❌ {name}: FAILED - malrule same as correct!")
            all_passed = False

    print(f"\n{'='*70}")
    if all_passed:
        print("✓✓✓ ALL COMPREHENSIVE TESTS PASSED ✓✓✓")
    else:
        print("✗✗✗ SOME COMPREHENSIVE TESTS FAILED ✗✗✗")
    print(f"{'='*70}")

    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  TEST: Square-Root-Equals-Plus-Minus (Independent Solving)  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    try:
        passed1 = test_all_templates()
        passed2 = test_comprehensive_cases()

        all_passed = passed1 and passed2

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
