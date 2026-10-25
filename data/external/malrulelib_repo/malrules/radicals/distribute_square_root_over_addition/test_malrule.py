#!/usr/bin/env python3
"""Test script for Distribute-Square-Root-Over-Addition malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel
from malrules.radicals.distribute_square_root_over_addition import (
    DistributeSquareRootOverAdditionProblemGenerator,
    DistributeSquareRootOverAdditionMalrule,
    SquareRootSimplificationCorrectAlgorithm
)


def test_all_templates():
    """Test all available templates."""
    print("="*70)
    print("TESTING ALL TEMPLATES")
    print("="*70)

    generator = DistributeSquareRootOverAdditionProblemGenerator(
        level=9,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = DistributeSquareRootOverAdditionMalrule()
    correct = SquareRootSimplificationCorrectAlgorithm()

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
            print(f"Problem metadata: a={problem.metadata.get('a')}, "
                  f"b={problem.metadata.get('b')}, "
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

            # Normalize answers for comparison
            def normalize_answer(ans):
                """Normalize answer for comparison (handles floats and strings)."""
                if isinstance(ans, str):
                    return ans.strip()
                if isinstance(ans, float):
                    return ans
                return ans

            correct_computed = normalize_answer(correct_sol.answer)
            expected_correct_norm = normalize_answer(expected_correct)
            malrule_computed = normalize_answer(malrule_sol.answer)
            expected_malrule_norm = normalize_answer(expected_malrule)

            # For correct algorithm, check match (with tolerance for floats)
            match = False
            if isinstance(correct_computed, float) and isinstance(expected_correct_norm, float):
                match = abs(correct_computed - expected_correct_norm) < 0.001
            else:
                match = (correct_computed == expected_correct_norm)

            if not match:
                print(f"\n❌ FAILED: Correct algorithm mismatch!")
                print(f"   Computed: {correct_computed}")
                print(f"   Expected: {expected_correct_norm}")
                print("\nCorrect algorithm steps:")
                for step in correct_sol.steps:
                    print(f"  {step}")
                all_passed = False
                continue

            # For malrule, check match with expected malrule answer
            malrule_match = False
            if isinstance(malrule_computed, float) and isinstance(expected_malrule_norm, (int, float)):
                malrule_match = abs(malrule_computed - expected_malrule_norm) < 0.001
            elif isinstance(malrule_computed, str) and isinstance(expected_malrule_norm, str):
                malrule_match = (malrule_computed == expected_malrule_norm)
            elif isinstance(malrule_computed, int) and isinstance(expected_malrule_norm, int):
                malrule_match = (malrule_computed == expected_malrule_norm)
            else:
                # Try string comparison
                malrule_match = (str(malrule_computed) == str(expected_malrule_norm))

            if not malrule_match:
                print(f"\n❌ FAILED: Malrule algorithm mismatch!")
                print(f"   Computed: {malrule_computed} (type: {type(malrule_computed)})")
                print(f"   Expected: {expected_malrule_norm} (type: {type(expected_malrule_norm)})")
                print("\nMalrule algorithm steps:")
                for step in malrule_sol.steps:
                    print(f"  {step}")
                all_passed = False
                continue

            # Check that malrule differs from correct (for algebraic, compare expressions)
            if template_name in ['algebraic_expression', 'word_problem_algebraic']:
                # For algebraic expressions, we expect different values when evaluated
                # Skip the edge case check for algebraic since answers are different types
                pass
            else:
                # For numeric answers, check they differ
                if isinstance(correct_computed, (int, float)) and isinstance(malrule_computed, (int, float)):
                    if abs(correct_computed - malrule_computed) < 0.001:
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

    generator = DistributeSquareRootOverAdditionProblemGenerator(
        level=9,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = DistributeSquareRootOverAdditionMalrule()
    correct = SquareRootSimplificationCorrectAlgorithm()

    test_cases = [
        {'a': 3, 'b': 4, 'name': '√(3²+4²) - Pythagorean triple 3-4-5'},
        {'a': 5, 'b': 12, 'name': '√(5²+12²) - Pythagorean triple 5-12-13'},
        {'a': 8, 'b': 15, 'name': '√(8²+15²) - Pythagorean triple 8-15-17'},
        {'a': 2, 'b': 3, 'name': '√(2²+3²) - Non-perfect square'},
        {'a': 6, 'b': 7, 'name': '√(6²+7²) - Non-perfect square'},
    ]

    all_passed = True
    for test in test_cases:
        a = test['a']
        b = test['b']
        name = test['name']

        # Generate problem with basic template
        problem = generator.generate(seed=a * 100, template='basic_sum_of_squares')

        # Override values in metadata
        problem.metadata['a'] = a
        problem.metadata['b'] = b

        # Recompute expected values
        a_squared = a ** 2
        b_squared = b ** 2
        sum_of_squares = a_squared + b_squared
        expected_correct = sum_of_squares ** 0.5
        expected_malrule = a + b

        print(f"\nTest: {name}")
        print(f"  Input: a={a}, b={b}")
        print(f"  Expected correct: {expected_correct}")
        print(f"  Expected malrule: {expected_malrule}")

        # Solve with both algorithms
        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        print(f"  Computed correct: {correct_sol.answer}")
        print(f"  Computed malrule: {malrule_sol.answer}")

        # Check correct answer
        if abs(correct_sol.answer - expected_correct) > 0.001:
            print(f"  ❌ FAILED: Correct answer mismatch!")
            print(f"     Expected: {expected_correct}, Got: {correct_sol.answer}")
            all_passed = False
            continue

        # Check malrule answer
        if malrule_sol.answer != expected_malrule:
            print(f"  ❌ FAILED: Malrule answer mismatch!")
            print(f"     Expected: {expected_malrule}, Got: {malrule_sol.answer}")
            all_passed = False
            continue

        print(f"  ✓ PASSED")

    print(f"\n{'='*70}")
    if all_passed:
        print("✓✓✓ ALL COMPREHENSIVE TESTS PASSED ✓✓✓")
    else:
        print("✗✗✗ SOME COMPREHENSIVE TESTS FAILED ✗✗✗")
    print(f"{'='*70}")

    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Distribute-Square-Root-Over-Addition  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    try:
        template_passed = test_all_templates()
        comprehensive_passed = test_comprehensive_cases()

        all_passed = template_passed and comprehensive_passed

        print("\n\n╔" + "═"*68 + "╗")
        if all_passed:
            print("║" + "  ✓✓✓ VERIFICATION COMPLETE - ALL TESTS PASSED ✓✓✓  ".center(70) + "║")
        else:
            print("║" + "  ✗✗✗ VERIFICATION FAILED - SOME TESTS FAILED ✗✗✗  ".center(70) + "║")
        print("╚" + "═"*68 + "╝\n")
        return 0 if all_passed else 1
    except Exception as e:
        print(f"\n✗✗✗ TEST FAILED: {e} ✗✗✗")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
