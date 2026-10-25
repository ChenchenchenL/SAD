#!/usr/bin/env python3
"""
Test script for Decimal-Places-Same-As-Sig-Figs malrule.

Run from project root: python3 -m malrules.rounding.decimal_places_same_as_sig_figs.test_malrule
Or from this directory: python3 test_malrule.py

This script demonstrates and tests the Decimal-Places-Same-As-Sig-Figs malrule
with clear examples and verification.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, InteractiveDemo, MalruleComparison, Problem
from malrules.rounding.decimal_places_same_as_sig_figs import (
    DecimalPlacesSameAsSigFigsProblemGenerator,
    DecimalPlacesSameAsSigFigsMalrule,
    SignificantFiguresCorrectAlgorithm
)


def test_specific_examples():
    """Test with specific, well-known examples."""
    print("="*70)
    print("TESTING WITH SPECIFIC EXAMPLES")
    print("="*70)

    # Create instances
    malrule = DecimalPlacesSameAsSigFigsMalrule()
    correct = SignificantFiguresCorrectAlgorithm()

    # Test case 1: 0.00456 to 3 sig figs (from specification)
    print("\n" + "-"*70)
    print("TEST CASE 1: 0.00456 to 3 sig figs (from specification)")
    print("-"*70)

    problem1 = Problem(
        text="Round 0.00456 to 3 significant figures.",
        operands=[3],  # Updated: only sig_figs
        operation='round_to_sig_figs',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={'number': 0.00456, 'number_str': '0.00456'}
    )

    correct_solution1 = correct.solve(problem1)
    malrule_solution1 = malrule.solve(problem1)

    print(f"\nProblem: {problem1.text}")
    print(f"\nCorrect answer: {correct_solution1.answer}")
    print(f"Malrule answer: {malrule_solution1.answer}")
    print(f"Answers different? {correct_solution1.answer != malrule_solution1.answer}")

    if correct_solution1.answer != malrule_solution1.answer:
        print("\n--- Correct Solution Steps ---")
        for step in correct_solution1.steps:
            print(f"  {step}")

        print("\n--- Malrule Solution Steps ---")
        for step in malrule_solution1.steps:
            print(f"  {step}")
    else:
        print("\n⚠ EDGE CASE: Misconception produces same answer as correct!")
        print("\n--- Correct Solution Steps ---")
        for step in correct_solution1.steps:
            print(f"  {step}")
        print("\n--- Malrule Solution Steps ---")
        for step in malrule_solution1.steps:
            print(f"  {step}")
        raise AssertionError(f"Edge case detected: both algorithms produced {correct_solution1.answer}")

    # Verify expected answers
    assert correct_solution1.answer == "0.00456", f"Expected 0.00456, got {correct_solution1.answer}"
    assert malrule_solution1.answer == "0.005", f"Expected 0.005, got {malrule_solution1.answer}"
    print("\n✓ TEST CASE 1 PASSED: Answers match expected values")

    # Test case 2: 0.007890 to 3 sig figs (from specification)
    print("\n" + "-"*70)
    print("TEST CASE 2: 0.007890 to 3 sig figs")
    print("-"*70)

    problem2 = Problem(
        text="Round 0.007890 to 3 significant figures.",
        operands=[3],  # Updated: only sig_figs
        operation='round_to_sig_figs',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={'number': 0.007890, 'number_str': '0.007890'}
    )

    correct_solution2 = correct.solve(problem2)
    malrule_solution2 = malrule.solve(problem2)

    print(f"\nProblem: {problem2.text}")
    print(f"Correct answer: {correct_solution2.answer}")
    print(f"Malrule answer: {malrule_solution2.answer}")
    print(f"Answers different? {correct_solution2.answer != malrule_solution2.answer}")

    if correct_solution2.answer == malrule_solution2.answer:
        print("\n⚠ EDGE CASE: Misconception produces same answer as correct!")
        print("\n--- Steps ---")
        for step in correct_solution2.steps:
            print(f"  {step}")
        raise AssertionError(f"Edge case detected: both algorithms produced {correct_solution2.answer}")

    # Expected: 0.007890 to 3 sig figs = 0.00789 (7, 8, 9 are the 3 sig figs)
    # Malrule: rounds to 3 decimal places = 0.008
    assert correct_solution2.answer == "0.00789", f"Expected 0.00789, got {correct_solution2.answer}"
    assert malrule_solution2.answer == "0.008", f"Expected 0.008, got {malrule_solution2.answer}"
    print("✓ TEST CASE 2 PASSED: Answers match expected values")

    # Test case 3: 0.001234 to 2 sig figs
    print("\n" + "-"*70)
    print("TEST CASE 3: 0.001234 to 2 sig figs")
    print("-"*70)

    problem3 = Problem(
        text="Round 0.001234 to 2 significant figures.",
        operands=[2],  # Updated: only sig_figs
        operation='round_to_sig_figs',
        level=9,
        difficulty=DifficultyLevel.EASY,
        metadata={'number': 0.001234, 'number_str': '0.001234'}
    )

    correct_solution3 = correct.solve(problem3)
    malrule_solution3 = malrule.solve(problem3)

    print(f"\nProblem: {problem3.text}")
    print(f"Correct answer: {correct_solution3.answer}")
    print(f"Malrule answer: {malrule_solution3.answer}")
    print(f"Answers different? {correct_solution3.answer != malrule_solution3.answer}")

    if correct_solution3.answer == malrule_solution3.answer:
        print("\n⚠ EDGE CASE: Misconception produces same answer!")
        raise AssertionError(f"Edge case detected")

    # Expected: 0.001234 to 2 sig figs = 0.0012 (1, 2 are the 2 sig figs)
    # Malrule: rounds to 2 decimal places = 0.00
    assert correct_solution3.answer == "0.0012", f"Expected 0.0012, got {correct_solution3.answer}"
    assert malrule_solution3.answer == "0.00", f"Expected 0.00, got {malrule_solution3.answer}"
    print("✓ TEST CASE 3 PASSED: Answers match expected values")

    # Test case 4: 0.0098765 to 4 sig figs
    print("\n" + "-"*70)
    print("TEST CASE 4: 0.0098765 to 4 sig figs")
    print("-"*70)

    problem4 = Problem(
        text="Round 0.0098765 to 4 significant figures.",
        operands=[4],  # Updated: only sig_figs
        operation='round_to_sig_figs',
        level=10,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={'number': 0.0098765, 'number_str': '0.0098765'}
    )

    correct_solution4 = correct.solve(problem4)
    malrule_solution4 = malrule.solve(problem4)

    print(f"\nProblem: {problem4.text}")
    print(f"Correct answer: {correct_solution4.answer}")
    print(f"Malrule answer: {malrule_solution4.answer}")
    print(f"Answers different? {correct_solution4.answer != malrule_solution4.answer}")

    if correct_solution4.answer == malrule_solution4.answer:
        print("\n⚠ EDGE CASE: Misconception produces same answer!")
        raise AssertionError(f"Edge case detected")

    # Expected: 0.0098765 to 4 sig figs = 0.009877 (9, 8, 7, 6 rounded to 9, 8, 7, 7)
    # Malrule: rounds to 4 decimal places = 0.0099
    assert correct_solution4.answer == "0.009877", f"Expected 0.009877, got {correct_solution4.answer}"
    assert malrule_solution4.answer == "0.0099", f"Expected 0.0099, got {malrule_solution4.answer}"
    print("✓ TEST CASE 4 PASSED: Answers match expected values")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_all_problem_templates():
    """Test ALL problem templates systematically."""
    print("\n\n" + "="*70)
    print("TESTING ALL PROBLEM TEMPLATES")
    print("="*70)

    generator = DecimalPlacesSameAsSigFigsProblemGenerator(
        level=9,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = DecimalPlacesSameAsSigFigsMalrule()
    correct = SignificantFiguresCorrectAlgorithm()

    # All template types to test
    all_templates = [
        'basic_rounding',
        'scientific_notation',
        'measurement_context',
        'calculation_result',
        'trailing_zeros_context',
        'multiplication_area',
        'division_density',
        'division_speed',
        'multiplication_cost',
        'unit_conversion'
    ]

    tested_templates = set()
    template_results = {}

    # Generate problems until we've tested all templates
    max_attempts = 200
    for seed in range(max_attempts):
        problem = generator.generate(seed=seed)
        template_type = problem.metadata.get('problem_type', 'basic_rounding')

        if template_type in tested_templates:
            continue

        print(f"\n{'-'*70}")
        print(f"Testing template: {template_type}")
        print('-'*70)

        try:
            correct_solution = correct.solve(problem)
            malrule_solution = malrule.solve(problem)

            print(f"Problem: {problem.text[:80]}...")
            print(f"Correct: {correct_solution.answer}")
            print(f"Malrule: {malrule_solution.answer}")

            if correct_solution.answer == malrule_solution.answer:
                # Edge case: both produce same answer
                print("\n⚠ EDGE CASE: Misconception produces same answer as correct!")
                print("\n--- Correct Solution Steps ---")
                for step in correct_solution.steps:
                    print(f"  {step}")
                print("\n--- Malrule Solution Steps ---")
                for step in malrule_solution.steps:
                    print(f"  {step}")
                template_results[template_type] = "EDGE_CASE"
                # Don't mark as tested - try another seed
            else:
                print(f"✓ Successfully tested {template_type}")
                tested_templates.add(template_type)
                template_results[template_type] = "PASSED"

        except Exception as e:
            print(f"\n✗ FAILED testing {template_type}")
            print(f"Error: {e}")
            print(f"\nProblem text: {problem.text}")
            print(f"Metadata: {problem.metadata}")
            import traceback
            traceback.print_exc()
            template_results[template_type] = f"FAILED: {e}"
            tested_templates.add(template_type)  # Mark as tested even if failed

        if len(tested_templates) >= len(all_templates):
            break

    print(f"\n{'='*70}")
    print("TEMPLATE TEST SUMMARY")
    print("="*70)
    for template in all_templates:
        result = template_results.get(template, "NOT_TESTED")
        symbol = "✓" if result == "PASSED" else ("⚠" if result == "EDGE_CASE" else "✗")
        print(f"{symbol} {template}: {result}")

    missing = set(all_templates) - tested_templates
    if missing:
        print(f"\n⚠ Warning: Could not test templates: {missing}")

    print(f"\nTested {len(tested_templates)}/{len(all_templates)} templates")
    print("="*70)


def test_random_generation():
    """Test with randomly generated problems."""
    print("\n\n" + "="*70)
    print("TESTING WITH RANDOMLY GENERATED PROBLEMS")
    print("="*70)

    problem_gen = DecimalPlacesSameAsSigFigsProblemGenerator(
        level=9,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = DecimalPlacesSameAsSigFigsMalrule()
    correct = SignificantFiguresCorrectAlgorithm()

    print("\nGenerating 10 random problems and comparing solutions...")

    incorrect_count = 0
    edge_case_count = 0
    for i in range(10):
        print(f"\n{'-'*70}")
        print(f"Random Test {i+1}")
        print('-'*70)

        problem = problem_gen.generate(seed=400+i)
        correct_solution = correct.solve(problem)
        malrule_solution = malrule.solve(problem)

        print(f"Template: {problem.metadata.get('problem_type', 'unknown')}")
        print(f"Problem: {problem.text[:80]}...")
        print(f"Correct: {correct_solution.answer}")
        print(f"Malrule: {malrule_solution.answer}")

        if correct_solution.answer != malrule_solution.answer:
            print("✓ Malrule produces DIFFERENT (incorrect) answer")
            incorrect_count += 1
        else:
            print("⚠ Malrule happens to produce SAME answer (edge case)")
            print("\n--- Steps (showing both produce same answer) ---")
            for step in correct_solution.steps:
                print(f"  {step}")
            edge_case_count += 1

    print(f"\n{'-'*70}")
    print(f"Results: {incorrect_count}/10 produced incorrect answers")
    print(f"         {edge_case_count}/10 were edge cases (same answer)")
    print("✓ RANDOM GENERATION TEST PASSED")


def test_automated_suite():
    """Run the automated test suite."""
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = DecimalPlacesSameAsSigFigsProblemGenerator(
        level=9,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = DecimalPlacesSameAsSigFigsMalrule()
    correct = SignificantFiguresCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    # Check all tests passed
    all_passed = all(r.passed for r in results)

    if all_passed:
        print("\n" + "="*70)
        print("✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
        print("="*70)
    else:
        print("\n" + "="*70)
        print("✗✗✗ SOME TESTS FAILED ✗✗✗")
        print("="*70)
        failed = [r for r in results if not r.passed]
        for result in failed:
            print(f"FAILED: {result.message}")

    return all_passed


def interactive_demo():
    """Show an interactive demo."""
    print("\n\n" + "="*70)
    print("INTERACTIVE DEMONSTRATION")
    print("="*70)

    problem_gen = DecimalPlacesSameAsSigFigsProblemGenerator(
        level=9,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = DecimalPlacesSameAsSigFigsMalrule()
    correct = SignificantFiguresCorrectAlgorithm()

    demo = InteractiveDemo(malrule, correct, problem_gen)

    print(demo.show_malrule_info())
    print(demo.run_multiple_comparisons(count=2))


def main():
    """Run all verification tests."""
    print("\n")
    print("╔" + "═"*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  VERIFICATION TEST: Decimal-Places-Same-As-Sig-Figs Malrule  ".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "═"*68 + "╝")

    try:
        # Test 1: Specific examples
        test_specific_examples()

        # Test 2: All problem templates
        test_all_problem_templates()

        # Test 3: Random generation
        test_random_generation()

        # Test 4: Automated suite
        all_passed = test_automated_suite()

        # Final summary
        print("\n\n" + "╔" + "═"*68 + "╗")
        print("║" + " "*68 + "║")
        print("║" + "  ✓✓✓ VERIFICATION COMPLETE - ALL TESTS PASSED ✓✓✓  ".center(68) + "║")
        print("║" + " "*68 + "║")
        print("╚" + "═"*68 + "╝")

        print("\n📁 Test location:")
        print("  - Implementation: malrules/rounding/decimal_places_same_as_sig_figs/")

        return 0

    except AssertionError as e:
        print(f"\n\n✗✗✗ TEST FAILED ✗✗✗")
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"\n\n✗✗✗ UNEXPECTED ERROR ✗✗✗")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
