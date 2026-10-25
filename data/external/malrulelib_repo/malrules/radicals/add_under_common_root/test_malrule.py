#!/usr/bin/env python3
"""Test script for Add-Under-Common-Root malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel
from malrules.radicals.add_under_common_root import (
    AddUnderCommonRootProblemGenerator,
    AddUnderCommonRootMalrule,
    RadicalAdditionCorrectAlgorithm
)


def test_all_templates():
    """Test all available templates."""
    print("="*70)
    print("TESTING ALL TEMPLATES")
    print("="*70)

    generator = AddUnderCommonRootProblemGenerator(
        level=9,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = AddUnderCommonRootMalrule()
    correct = RadicalAdditionCorrectAlgorithm()

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
            print(f"Problem metadata: square_a={problem.metadata.get('square_a')}, "
                  f"square_b={problem.metadata.get('square_b')}, "
                  f"template={problem.metadata.get('template')}")

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

            # Normalize answers for comparison
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

    generator = AddUnderCommonRootProblemGenerator(
        level=9,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = AddUnderCommonRootMalrule()
    correct = RadicalAdditionCorrectAlgorithm()

    test_cases = [
        {'square_a': 4, 'square_b': 9, 'expected_correct': '5', 'name': '√4 + √9'},
        {'square_a': 16, 'square_b': 25, 'expected_correct': '9', 'name': '√16 + √25'},
        {'square_a': 36, 'square_b': 64, 'expected_correct': '14', 'name': '√36 + √64'},
        {'square_a': 49, 'square_b': 81, 'expected_correct': '16', 'name': '√49 + √81'},
        {'square_a': 100, 'square_b': 144, 'expected_correct': '22', 'name': '√100 + √144'},
    ]

    all_passed = True
    for test in test_cases:
        square_a = test['square_a']
        square_b = test['square_b']
        expected = test['expected_correct']
        name = test['name']

        # Generate problem with this specific template
        problem = generator.generate(seed=square_a * 100, template='basic_addition')

        # Override squares in metadata to test specific values
        problem.metadata['square_a'] = square_a
        problem.metadata['square_b'] = square_b

        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        # Normalize for comparison
        computed = str(correct_sol.answer).strip()

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
    print("║" + "  TEST: Add-Under-Common-Root (Independent Solving)  ".center(70) + "║")
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
