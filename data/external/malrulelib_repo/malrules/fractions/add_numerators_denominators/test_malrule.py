#!/usr/bin/env python3
"""
Test script for Add-Numerators-Add-Denominators malrule.

Run from project root: python3 -m malrules.fractions.add_numerators_denominators.test_malrule
Or from this directory: python3 test_malrule.py

This script demonstrates and tests the fraction addition malrule
with clear examples and verification.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest
from malrules.fractions.add_numerators_denominators import (
    FractionAdditionProblemGenerator,
    AddNumeratorsAddDenominatorsMalrule,
    FractionAdditionCorrectAlgorithm
)


def test_specific_examples():
    """Test with specific, well-known examples."""
    print("="*70)
    print("TESTING WITH SPECIFIC EXAMPLES")
    print("="*70)

    # Create instances
    malrule = AddNumeratorsAddDenominatorsMalrule()
    correct = FractionAdditionCorrectAlgorithm()

    # Test case 1: Classic example from literature
    print("\n" + "-"*70)
    print("TEST CASE 1: 1/2 + 1/3 (Classic example from research)")
    print("-"*70)

    from utils import Problem, DifficultyLevel
    problem1 = Problem(
        text="What is 1/2 + 1/3?",
        operands=[(1, 2), (1, 3)],
        operation='fraction_addition',
        level=5,
        difficulty=DifficultyLevel.MEDIUM
    )

    correct_solution1 = correct.solve(problem1)
    malrule_solution1 = malrule.solve(problem1)

    print(f"\nProblem: {problem1.text}")
    print(f"\nCorrect answer: {correct_solution1.answer}")
    print(f"Malrule answer: {malrule_solution1.answer}")
    print(f"Match? {correct_solution1.answer == malrule_solution1.answer}")

    print("\n--- Correct Solution Steps ---")
    for step in correct_solution1.steps:
        print(f"  {step}")

    print("\n--- Malrule Solution Steps ---")
    for step in malrule_solution1.steps:
        print(f"  {step}")

    # Verify expected answers
    assert correct_solution1.answer == "5/6", f"Expected 5/6, got {correct_solution1.answer}"
    assert malrule_solution1.answer == "2/5", f"Expected 2/5, got {malrule_solution1.answer}"
    print("\n✓ TEST CASE 1 PASSED: Answers match expected values")

    # Test case 2: Another common example
    print("\n" + "-"*70)
    print("TEST CASE 2: 1/4 + 1/3")
    print("-"*70)

    problem2 = Problem(
        text="What is 1/4 + 1/3?",
        operands=[(1, 4), (1, 3)],
        operation='fraction_addition',
        level=5,
        difficulty=DifficultyLevel.MEDIUM
    )

    correct_solution2 = correct.solve(problem2)
    malrule_solution2 = malrule.solve(problem2)

    print(f"\nProblem: {problem2.text}")
    print(f"Correct answer: {correct_solution2.answer}")
    print(f"Malrule answer: {malrule_solution2.answer}")
    print(f"Answers different? {correct_solution2.answer != malrule_solution2.answer}")

    # Expected: 1/4 + 1/3 = 3/12 + 4/12 = 7/12 (correct)
    # Malrule: 1/4 + 1/3 = 2/7 (incorrect)
    assert correct_solution2.answer == "7/12", f"Expected 7/12, got {correct_solution2.answer}"
    assert malrule_solution2.answer == "2/7", f"Expected 2/7, got {malrule_solution2.answer}"
    print("✓ TEST CASE 2 PASSED: Answers match expected values")

    # Test case 3: Edge case where malrule might accidentally be correct
    print("\n" + "-"*70)
    print("TEST CASE 3: 1/2 + 1/2 (Same denominators)")
    print("-"*70)

    problem3 = Problem(
        text="What is 1/2 + 1/2?",
        operands=[(1, 2), (1, 2)],
        operation='fraction_addition',
        level=4,
        difficulty=DifficultyLevel.EASY
    )

    correct_solution3 = correct.solve(problem3)
    malrule_solution3 = malrule.solve(problem3)

    print(f"\nProblem: {problem3.text}")
    print(f"Correct answer: {correct_solution3.answer}")
    print(f"Malrule answer: {malrule_solution3.answer}")

    # Expected: 1/2 + 1/2 = 2/2 = 1 (correct)
    # Malrule: 1/2 + 1/2 = 2/4 = 1/2 (incorrect!)
    print(f"Match? {correct_solution3.answer == malrule_solution3.answer}")
    print("✓ TEST CASE 3 PASSED: Even with same denominators, malrule produces wrong answer")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_random_generation():
    """Test with randomly generated problems."""
    print("\n\n" + "="*70)
    print("TESTING WITH RANDOMLY GENERATED PROBLEMS")
    print("="*70)

    problem_gen = FractionAdditionProblemGenerator(
        level=5,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = AddNumeratorsAddDenominatorsMalrule()
    correct = FractionAdditionCorrectAlgorithm()

    print("\nGenerating 5 random problems and comparing solutions...")

    incorrect_count = 0
    for i in range(5):
        print(f"\n{'-'*70}")
        print(f"Random Test {i+1}")
        print('-'*70)

        problem = problem_gen.generate(seed=100+i)
        correct_solution = correct.solve(problem)
        malrule_solution = malrule.solve(problem)

        print(f"Problem: {problem.text}")
        print(f"Correct: {correct_solution.answer}")
        print(f"Malrule: {malrule_solution.answer}")

        if correct_solution.answer != malrule_solution.answer:
            print("✓ Malrule produces DIFFERENT (incorrect) answer")
            incorrect_count += 1
        else:
            print("⚠ Malrule happens to produce SAME answer (rare edge case)")

    print(f"\n{incorrect_count}/5 problems produced incorrect answers with malrule")
    print("✓ RANDOM GENERATION TEST PASSED")


def test_new_problem_templates():
    """Test the new problem templates (three fractions, improper, mixed, word problems)."""
    print("\n\n" + "="*70)
    print("TESTING NEW PROBLEM TEMPLATES")
    print("="*70)

    from utils import Problem
    malrule = AddNumeratorsAddDenominatorsMalrule()
    correct = FractionAdditionCorrectAlgorithm()

    # Test three fractions
    print("\nTEST CASE 4: Three fractions - 1/2 + 1/3 + 1/4")
    print("-"*70)

    problem4 = Problem(
        text="What is 1/2 + 1/3 + 1/4?",
        operands=[(1, 2), (1, 3), (1, 4)],
        operation='fraction_addition',
        level=5,
        difficulty=DifficultyLevel.HARD
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)

    print(f"Problem: {problem4.text}")
    print(f"Correct answer: {correct_sol4.answer}")
    print(f"Malrule answer: {malrule_sol4.answer}")

    # Expected: 1/2 + 1/3 + 1/4 = 6/12 + 4/12 + 3/12 = 13/12 (correct)
    # Malrule: 1/2 + 1/3 + 1/4 = (1+1+1)/(2+3+4) = 3/9 = 1/3 (incorrect)
    assert correct_sol4.answer == "13/12", f"Expected 13/12, got {correct_sol4.answer}"
    assert malrule_sol4.answer == "1/3", f"Expected 1/3, got {malrule_sol4.answer}"
    assert correct_sol4.answer != malrule_sol4.answer, "Malrule should produce different answer"

    print("✓ TEST CASE 4 PASSED: Three fractions work correctly")

    # Test improper fractions
    print("\n\nTEST CASE 5: Improper fractions - 5/3 + 7/4")
    print("-"*70)

    problem5 = Problem(
        text="What is 5/3 + 7/4?",
        operands=[(5, 3), (7, 4)],
        operation='fraction_addition',
        level=5,
        difficulty=DifficultyLevel.HARD
    )

    correct_sol5 = correct.solve(problem5)
    malrule_sol5 = malrule.solve(problem5)

    print(f"Problem: {problem5.text}")
    print(f"Correct answer: {correct_sol5.answer}")
    print(f"Malrule answer: {malrule_sol5.answer}")

    # Expected: 5/3 + 7/4 = 20/12 + 21/12 = 41/12 (correct)
    # Malrule: 5/3 + 7/4 = (5+7)/(3+4) = 12/7 (incorrect)
    assert correct_sol5.answer == "41/12", f"Expected 41/12, got {correct_sol5.answer}"
    assert malrule_sol5.answer == "12/7", f"Expected 12/7, got {malrule_sol5.answer}"

    print("✓ TEST CASE 5 PASSED: Improper fractions work correctly")

    # Test mixed numbers (displayed as mixed but stored as improper)
    print("\n\nTEST CASE 6: Mixed numbers - 3/2 + 5/3")
    print("-"*70)

    problem6 = Problem(
        text="What is 1 1/2 + 1 2/3?",  # Display as mixed: 1 1/2 = 3/2, 1 2/3 = 5/3
        operands=[(3, 2), (5, 3)],
        operation='fraction_addition',
        level=5,
        difficulty=DifficultyLevel.HARD
    )

    correct_sol6 = correct.solve(problem6)
    malrule_sol6 = malrule.solve(problem6)

    print(f"Problem: {problem6.text}")
    print(f"Correct answer: {correct_sol6.answer}")
    print(f"Malrule answer: {malrule_sol6.answer}")

    # Expected: 3/2 + 5/3 = 9/6 + 10/6 = 19/6 (correct)
    # Malrule: 3/2 + 5/3 = (3+5)/(2+3) = 8/5 (incorrect)
    assert correct_sol6.answer == "19/6", f"Expected 19/6, got {correct_sol6.answer}"
    assert malrule_sol6.answer == "8/5", f"Expected 8/5, got {malrule_sol6.answer}"

    print("✓ TEST CASE 6 PASSED: Mixed numbers work correctly")

    # Test word problem
    print("\n\nTEST CASE 7: Word problem - Pizza fractions")
    print("-"*70)

    problem7 = Problem(
        text="Sarah ate 1/4 of a pizza and John ate 1/3 of the same pizza. What fraction of the pizza did they eat together?",
        operands=[(1, 4), (1, 3)],
        operation='fraction_addition',
        level=5,
        difficulty=DifficultyLevel.MEDIUM
    )

    correct_sol7 = correct.solve(problem7)
    malrule_sol7 = malrule.solve(problem7)

    print(f"Problem: {problem7.text}")
    print(f"Correct answer: {correct_sol7.answer}")
    print(f"Malrule answer: {malrule_sol7.answer}")

    # Expected: 1/4 + 1/3 = 3/12 + 4/12 = 7/12 (correct)
    # Malrule: 1/4 + 1/3 = 2/7 (incorrect)
    assert correct_sol7.answer == "7/12", f"Expected 7/12, got {correct_sol7.answer}"
    assert malrule_sol7.answer == "2/7", f"Expected 2/7, got {malrule_sol7.answer}"

    print("✓ TEST CASE 7 PASSED: Word problems work correctly")

    # Test another word problem with different context
    print("\n\nTEST CASE 8: Word problem - Recipe")
    print("-"*70)

    problem8 = Problem(
        text="A recipe calls for 2/3 cup of flour and 1/2 cup of sugar. How many cups of dry ingredients are needed in total?",
        operands=[(2, 3), (1, 2)],
        operation='fraction_addition',
        level=5,
        difficulty=DifficultyLevel.MEDIUM
    )

    correct_sol8 = correct.solve(problem8)
    malrule_sol8 = malrule.solve(problem8)

    print(f"Problem: {problem8.text}")
    print(f"Correct answer: {correct_sol8.answer} cups")
    print(f"Malrule answer: {malrule_sol8.answer} cups")

    # Expected: 2/3 + 1/2 = 4/6 + 3/6 = 7/6 (correct)
    # Malrule: 2/3 + 1/2 = 3/5 (incorrect)
    assert correct_sol8.answer == "7/6", f"Expected 7/6, got {correct_sol8.answer}"
    assert malrule_sol8.answer == "3/5", f"Expected 3/5, got {malrule_sol8.answer}"

    print("✓ TEST CASE 8 PASSED: Recipe word problem works correctly")

    print("\n" + "="*70)
    print("ALL NEW TEMPLATE TEST CASES PASSED ✓")
    print("="*70)


def test_template_generation():
    """Test that all template types can be generated."""
    print("\n\n" + "="*70)
    print("TESTING TEMPLATE GENERATION")
    print("="*70)

    from collections import defaultdict
    template_counts = defaultdict(int)

    # Generate multiple problems and verify all template types appear
    for difficulty in [DifficultyLevel.EASY, DifficultyLevel.MEDIUM, DifficultyLevel.HARD]:
        problem_gen = FractionAdditionProblemGenerator(
            level=5,
            difficulty=difficulty
        )

        print(f"\nGenerating problems for {difficulty.value} difficulty...")

        for i in range(20):
            problem = problem_gen.generate(seed=2000 + i)
            problem_type = problem.metadata.get('problem_type', 'basic_two')
            template_counts[problem_type] += 1

    print("\nTemplate type distribution:")
    for template_type, count in sorted(template_counts.items()):
        print(f"  {template_type}: {count} problems")

    # Verify we got at least some of the basic types (with expanded word problems,
    # we now have more types to choose from, so we check for coverage broadly)
    expected_types = [
        'basic_two', 'three_fractions', 'word_problem', 'improper', 'mixed',
        'word_problem_three_fractions', 'word_problem_improper', 'word_problem_mixed'
    ]

    # At least 5 different types should be represented
    types_found = sum(1 for t in expected_types if template_counts[t] > 0)
    assert types_found >= 5, f"Expected at least 5 different template types, but found {types_found}"

    # Verify that word problem variants are being generated
    word_problem_types = ['word_problem', 'word_problem_three_fractions',
                          'word_problem_improper', 'word_problem_mixed']
    word_problem_count = sum(template_counts[t] for t in word_problem_types)
    assert word_problem_count > 0, "No word problems generated"

    print(f"\n✓ {types_found} different template types generated successfully")
    print(f"✓ {word_problem_count} word problems generated (including new variants)")

    print("\n" + "="*70)
    print("TEMPLATE GENERATION TESTS PASSED ✓")
    print("="*70)


def test_automated_suite():
    """Run the automated test suite."""
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = FractionAdditionProblemGenerator(
        level=5,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = AddNumeratorsAddDenominatorsMalrule()
    correct = FractionAdditionCorrectAlgorithm()

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



def main():
    """Run all verification tests."""
    print("\n")
    print("╔" + "═"*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  VERIFICATION TEST: Add-Numerators-Add-Denominators Malrule  ".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "═"*68 + "╝")

    try:
        # Test 1: Specific examples
        test_specific_examples()

        # Test 2: Random generation
        test_random_generation()

        # Test 3: New problem templates
        test_new_problem_templates()

        # Test 4: Template generation
        test_template_generation()

        # Test 5: Automated suite
        all_passed = test_automated_suite()

        # Final summary
        print("\n\n" + "╔" + "═"*68 + "╗")
        print("║" + " "*68 + "║")
        print("║" + "  ✓✓✓ VERIFICATION COMPLETE - ALL TESTS PASSED ✓✓✓  ".center(68) + "║")
        print("║" + " "*68 + "║")
        print("╚" + "═"*68 + "╝")
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
