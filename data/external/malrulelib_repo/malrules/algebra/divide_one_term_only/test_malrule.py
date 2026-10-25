#!/usr/bin/env python3
"""
Test script for Divide-One-Term-Only malrule.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.algebra.divide_one_term_only import (
    TwoStepEquationProblemGenerator,
    DivideOneTermOnlyMalrule,
    TwoStepEquationCorrectAlgorithm
)


def test_specific_examples():
    """Test with specific examples."""
    print("="*70)
    print("TESTING DIVIDE-ONE-TERM-ONLY WITH SPECIFIC EXAMPLES")
    print("="*70)

    malrule = DivideOneTermOnlyMalrule()
    correct = TwoStepEquationCorrectAlgorithm()

    # Test case 1: 2x + 4 = 10 (Classic case)
    print("\nTEST CASE 1: 2x + 4 = 10 (Classic distribution error)")
    print("-"*70)

    problem1 = Problem(
        text="Solve for x: 2x + 4 = 10",
        operands=[3],
        operation='solve_two_step_equation',
        level=7,
        difficulty=DifficultyLevel.EASY,
        metadata={'equation': '2x + 4 = 10', 'a': 2, 'b': 4, 'c': 10, 'correct_x': 3}
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"Problem: {problem1.text}")
    print(f"Correct answer: x = {correct_sol.answer}")
    print(f"Malrule answer: x = {malrule_sol.answer}")

    # Expected: x = 3 is correct, but malrule says x = 1 (5 - 4)
    assert correct_sol.answer == 3, f"Expected 3, got {correct_sol.answer}"
    assert malrule_sol.answer == 1, f"Expected 1 (malrule), got {malrule_sol.answer}"
    assert correct_sol.answer != malrule_sol.answer, "Malrule should produce different answer"

    print("\n--- Correct Steps ---")
    for step in correct_sol.steps:
        print(f"  {step}")

    print("\n--- Malrule Steps ---")
    for step in malrule_sol.steps:
        print(f"  {step}")

    print("✓ TEST CASE 1 PASSED: 2x + 4 = 10 correct=3, malrule=1")

    # Test case 2: 3x + 6 = 15
    print("\n\nTEST CASE 2: 3x + 6 = 15")
    print("-"*70)

    problem2 = Problem(
        text="Solve for x: 3x + 6 = 15",
        operands=[3],
        operation='solve_two_step_equation',
        level=7,
        difficulty=DifficultyLevel.EASY,
        metadata={'equation': '3x + 6 = 15', 'a': 3, 'b': 6, 'c': 15, 'correct_x': 3}
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)

    print(f"Problem: {problem2.text}")
    print(f"Correct answer: x = {correct_sol2.answer}")
    print(f"Malrule answer: x = {malrule_sol2.answer}")

    # Expected: x = 3 is correct, but malrule says x = -1 (5 - 6)
    assert correct_sol2.answer == 3, f"Expected 3, got {correct_sol2.answer}"
    assert malrule_sol2.answer == -1, f"Expected -1 (malrule), got {malrule_sol2.answer}"

    print("✓ TEST CASE 2 PASSED: 3x + 6 = 15 correct=3, malrule=-1")

    # Test case 3: 4x + 8 = 20
    print("\n\nTEST CASE 3: 4x + 8 = 20")
    print("-"*70)

    problem3 = Problem(
        text="Solve for x: 4x + 8 = 20",
        operands=[3],
        operation='solve_two_step_equation',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={'equation': '4x + 8 = 20', 'a': 4, 'b': 8, 'c': 20, 'correct_x': 3}
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)

    print(f"Problem: {problem3.text}")
    print(f"Correct answer: x = {correct_sol3.answer}")
    print(f"Malrule answer: x = {malrule_sol3.answer}")

    # Expected: x = 3 is correct, but malrule says x = -3 (5 - 8)
    assert correct_sol3.answer == 3, f"Expected 3, got {correct_sol3.answer}"
    assert malrule_sol3.answer == -3, f"Expected -3 (malrule), got {malrule_sol3.answer}"

    print("✓ TEST CASE 3 PASSED: 4x + 8 = 20 correct=3, malrule=-3")

    # Test case 4: 5x + 10 = 25
    print("\n\nTEST CASE 4: 5x + 10 = 25")
    print("-"*70)

    problem4 = Problem(
        text="Solve for x: 5x + 10 = 25",
        operands=[3],
        operation='solve_two_step_equation',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={'equation': '5x + 10 = 25', 'a': 5, 'b': 10, 'c': 25, 'correct_x': 3}
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)

    print(f"Problem: {problem4.text}")
    print(f"Correct answer: x = {correct_sol4.answer}")
    print(f"Malrule answer: x = {malrule_sol4.answer}")

    # Expected: x = 3 is correct, but malrule says x = -5 (5 - 10)
    assert correct_sol4.answer == 3, f"Expected 3, got {correct_sol4.answer}"
    assert malrule_sol4.answer == -5, f"Expected -5 (malrule), got {malrule_sol4.answer}"

    print("✓ TEST CASE 4 PASSED: 5x + 10 = 25 correct=3, malrule=-5")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_new_problem_templates():
    """Test new problem template types added for enhancement."""
    print("\n\n" + "="*70)
    print("TESTING NEW PROBLEM TEMPLATES")
    print("="*70)

    malrule = DivideOneTermOnlyMalrule()
    correct = TwoStepEquationCorrectAlgorithm()

    # TEST CASE 5: Three-term addition (2x + 3 + 5 = 18)
    print("\n\nTEST CASE 5: Three-term addition (2x + 3 + 5 = 18)")
    print("-"*70)

    problem5 = Problem(
        text="Solve for x: 2x + 3 + 5 = 18",
        operands=[5],
        operation='solve_two_step_equation',
        level=8,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'equation': '2x + 3 + 5 = 18',
            'equation_type': 'three_term_addition',
            'a': 2,
            'b': 3,
            'd': 5,
            'c': 18,
            'correct_x': 5
        }
    )

    correct_sol5 = correct.solve(problem5)
    malrule_sol5 = malrule.solve(problem5)

    print(f"Problem: {problem5.text}")
    print(f"Correct answer: x = {correct_sol5.answer}")
    print(f"Malrule answer: x = {malrule_sol5.answer}")

    # Correct: 2x + 8 = 18 → 2x = 10 → x = 5
    # Malrule: x + 3 + 5 = 9 → x + 8 = 9 → x = 1
    assert correct_sol5.answer == 5, f"Expected 5, got {correct_sol5.answer}"
    assert malrule_sol5.answer == 1, f"Expected 1 (malrule), got {malrule_sol5.answer}"

    print("✓ TEST CASE 5 PASSED: Three-term addition template works")

    # TEST CASE 6: Fractional coefficients (0.5x + 3 = 8)
    print("\n\nTEST CASE 6: Fractional coefficients (0.5x + 3 = 8)")
    print("-"*70)

    problem6 = Problem(
        text="Solve for x: 0.5x + 3 = 8",
        operands=[10],
        operation='solve_two_step_equation',
        level=8,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'equation': '0.5x + 3 = 8',
            'equation_type': 'fractional_coefficients',
            'a': 0.5,
            'b': 3,
            'c': 8,
            'correct_x': 10,
            'is_decimal': True
        }
    )

    correct_sol6 = correct.solve(problem6)
    malrule_sol6 = malrule.solve(problem6)

    print(f"Problem: {problem6.text}")
    print(f"Correct answer: x = {correct_sol6.answer}")
    print(f"Malrule answer: x = {malrule_sol6.answer}")

    # Correct: 0.5x = 5 → x = 10
    # Malrule: x + 3 = 16 → x = 13
    assert correct_sol6.answer == 10, f"Expected 10, got {correct_sol6.answer}"
    assert malrule_sol6.answer == 13, f"Expected 13 (malrule), got {malrule_sol6.answer}"

    print("✓ TEST CASE 6 PASSED: Fractional coefficients template works")

    # TEST CASE 7: Subtraction form (3x - 4 = 11)
    print("\n\nTEST CASE 7: Subtraction form (3x - 4 = 11)")
    print("-"*70)

    problem7 = Problem(
        text="Solve for x: 3x - 4 = 11",
        operands=[5],
        operation='solve_two_step_equation',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'equation': '3x - 4 = 11',
            'equation_type': 'subtraction_form',
            'a': 3,
            'b': 4,
            'c': 11,
            'correct_x': 5
        }
    )

    correct_sol7 = correct.solve(problem7)
    malrule_sol7 = malrule.solve(problem7)

    print(f"Problem: {problem7.text}")
    print(f"Correct answer: x = {correct_sol7.answer}")
    print(f"Malrule answer: x = {malrule_sol7.answer}")

    # Correct: 3x = 15 → x = 5
    # Malrule: x - 4 = 3.67 → x = 7.67
    assert correct_sol7.answer == 5, f"Expected 5, got {correct_sol7.answer}"
    assert abs(malrule_sol7.answer - 7.67) < 0.1, f"Expected ~7.67 (malrule), got {malrule_sol7.answer}"

    print("✓ TEST CASE 7 PASSED: Subtraction form template works")

    # TEST CASE 8: Word problem context
    print("\n\nTEST CASE 8: Word problem context (car rental)")
    print("-"*70)

    problem8 = Problem(
        text="A car rental costs $25 plus $3 per day. If the total cost is $34, for how many days was the car rented? Let x be the number of days. Solve: 3x + 25 = 34",
        operands=[3],
        operation='solve_two_step_equation',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'equation': '3x + 25 = 34',
            'equation_type': 'two_step_addition',
            'a': 3,
            'b': 25,
            'c': 34,
            'correct_x': 3,
            'is_word_problem': True
        }
    )

    correct_sol8 = correct.solve(problem8)
    malrule_sol8 = malrule.solve(problem8)

    print(f"Problem: {problem8.text}")
    print(f"Correct answer: x = {correct_sol8.answer}")
    print(f"Malrule answer: x = {malrule_sol8.answer}")

    # Correct: 3x = 9 → x = 3
    # Malrule: x + 25 = 11.33 → x = -13.67 (nonsensical!)
    assert correct_sol8.answer == 3, f"Expected 3, got {correct_sol8.answer}"
    assert abs(malrule_sol8.answer - (-13.67)) < 0.1, f"Expected ~-13.67 (malrule), got {malrule_sol8.answer}"

    print("✓ TEST CASE 8 PASSED: Word problem context template works")

    print("\n" + "="*70)
    print("ALL NEW TEMPLATE TEST CASES PASSED ✓")
    print("="*70)


def test_template_generation():
    """Test that all template types can be generated."""
    print("\n\n" + "="*70)
    print("TESTING TEMPLATE GENERATION")
    print("="*70)

    problem_gen = TwoStepEquationProblemGenerator(
        level=8,
        difficulty=DifficultyLevel.HARD
    )

    # Generate multiple problems to cover all template types
    templates_found = set()
    for i in range(100):
        problem = problem_gen.generate(seed=30000 + i)
        if 'equation_type' in problem.metadata:
            templates_found.add(problem.metadata['equation_type'])

    print(f"\nTemplates generated: {sorted(templates_found)}")

    # Verify we have all expected templates
    expected_templates = {
        'two_step_addition',
        'three_term_addition',
        'fractional_coefficients',
        'subtraction_form',
    }
    assert templates_found >= expected_templates, \
        f"Missing templates: {expected_templates - templates_found}"

    print("\n✓ ALL TEMPLATE TYPES GENERATED SUCCESSFULLY")
    print("="*70)


def test_automated_suite():
    """Run the automated test suite."""
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = TwoStepEquationProblemGenerator(
        level=7,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = DivideOneTermOnlyMalrule()
    correct = TwoStepEquationCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)

    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    else:
        print("\n✗✗✗ SOME TESTS FAILED ✗✗✗")
        for result in results:
            if not result.passed:
                print(f"FAILED: {result.message}")

    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Divide-One-Term-Only  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    try:
        test_specific_examples()
        test_new_problem_templates()
        test_template_generation()
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
