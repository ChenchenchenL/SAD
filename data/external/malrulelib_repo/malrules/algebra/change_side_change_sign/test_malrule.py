#!/usr/bin/env python3
"""
Test script for Change-Side-Change-Sign malrule.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.algebra.change_side_change_sign import (
    LinearEquationProblemGenerator,
    ChangeSideChangeSignMalrule,
    LinearEquationCorrectAlgorithm
)


def test_specific_examples():
    """Test with specific examples."""
    print("="*70)
    print("TESTING CHANGE-SIDE-CHANGE-SIGN WITH SPECIFIC EXAMPLES")
    print("="*70)

    malrule = ChangeSideChangeSignMalrule()
    correct = LinearEquationCorrectAlgorithm()

    # Test case 1: x + 3 = 7 (Classic case)
    print("\nTEST CASE 1: x + 3 = 7 (Classic case)")
    print("-"*70)

    problem1 = Problem(
        text="Solve for x: x + 3 = 7",
        operands=[4],
        operation='solve_equation',
        level=7,
        difficulty=DifficultyLevel.EASY,
        metadata={'equation': 'x + 3 = 7', 'correct_x': 4, 'equation_type': 'x_plus_c', 'operation': '+'}
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"Problem: {problem1.text}")
    print(f"Correct answer: x = {correct_sol.answer}")
    print(f"Malrule answer: x = {malrule_sol.answer}")

    # Expected: x = 4 is correct, but malrule says x = 10 (7 + 3)
    assert correct_sol.answer == 4, f"Expected 4, got {correct_sol.answer}"
    assert malrule_sol.answer == 10, f"Expected 10 (malrule), got {malrule_sol.answer}"
    assert correct_sol.answer != malrule_sol.answer, "Malrule should produce different answer"

    print("\n--- Correct Steps ---")
    for step in correct_sol.steps:
        print(f"  {step}")

    print("\n--- Malrule Steps ---")
    for step in malrule_sol.steps:
        print(f"  {step}")

    print("✓ TEST CASE 1 PASSED: x + 3 = 7 correct=4, malrule=10")

    # Test case 2: x - 5 = 2
    print("\n\nTEST CASE 2: x - 5 = 2")
    print("-"*70)

    problem2 = Problem(
        text="Solve for x: x - 5 = 2",
        operands=[7],
        operation='solve_equation',
        level=7,
        difficulty=DifficultyLevel.EASY,
        metadata={'equation': 'x - 5 = 2', 'correct_x': 7, 'equation_type': 'x_minus_c', 'operation': '-'}
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)

    print(f"Problem: {problem2.text}")
    print(f"Correct answer: x = {correct_sol2.answer}")
    print(f"Malrule answer: x = {malrule_sol2.answer}")

    # Expected: x = 7 is correct, but malrule says x = -3 (2 - 5)
    assert correct_sol2.answer == 7, f"Expected 7, got {correct_sol2.answer}"
    assert malrule_sol2.answer == -3, f"Expected -3 (malrule), got {malrule_sol2.answer}"

    print("✓ TEST CASE 2 PASSED: x - 5 = 2 correct=7, malrule=-3")

    # Test case 3: x + 8 = 15
    print("\n\nTEST CASE 3: x + 8 = 15")
    print("-"*70)

    problem3 = Problem(
        text="Solve for x: x + 8 = 15",
        operands=[7],
        operation='solve_equation',
        level=7,
        difficulty=DifficultyLevel.EASY,
        metadata={'equation': 'x + 8 = 15', 'correct_x': 7, 'equation_type': 'x_plus_c', 'operation': '+'}
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)

    print(f"Problem: {problem3.text}")
    print(f"Correct answer: x = {correct_sol3.answer}")
    print(f"Malrule answer: x = {malrule_sol3.answer}")

    # Expected: x = 7 is correct, but malrule says x = 23 (15 + 8)
    assert correct_sol3.answer == 7, f"Expected 7, got {correct_sol3.answer}"
    assert malrule_sol3.answer == 23, f"Expected 23 (malrule), got {malrule_sol3.answer}"

    print("✓ TEST CASE 3 PASSED: x + 8 = 15 correct=7, malrule=23")

    # Test case 4: 2x + 4 = 10 (Two-step)
    print("\n\nTEST CASE 4: 2x + 4 = 10 (Two-step equation)")
    print("-"*70)

    problem4 = Problem(
        text="Solve for x: 2x + 4 = 10",
        operands=[3],
        operation='solve_equation',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={'equation': '2x + 4 = 10', 'correct_x': 3, 'equation_type': 'two_step', 'operation': 'two_step'}
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)

    print(f"Problem: {problem4.text}")
    print(f"Correct answer: x = {correct_sol4.answer}")
    print(f"Malrule answer: x = {malrule_sol4.answer}")

    # Expected: x = 3 is correct, but malrule says x = 7 (14/2 from 2x = 14)
    assert correct_sol4.answer == 3, f"Expected 3, got {correct_sol4.answer}"
    assert malrule_sol4.answer == 7, f"Expected 7 (malrule), got {malrule_sol4.answer}"

    print("✓ TEST CASE 4 PASSED: 2x + 4 = 10 correct=3, malrule=7")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_new_problem_templates():
    """Test new problem template types added for enhancement."""
    print("\n\n" + "="*70)
    print("TESTING NEW PROBLEM TEMPLATES")
    print("="*70)

    malrule = ChangeSideChangeSignMalrule()
    correct = LinearEquationCorrectAlgorithm()

    # TEST CASE 5: Variables on both sides (3x + 5 = x + 13)
    print("\n\nTEST CASE 5: Variables on both sides (3x + 5 = x + 13)")
    print("-"*70)

    problem5 = Problem(
        text="Solve for x: 3x + 5 = x + 13",
        operands=[4],
        operation='solve_equation',
        level=8,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'equation': '3x + 5 = x + 13',
            'correct_x': 4,
            'equation_type': 'variables_on_both_sides',
            'operation': 'variables_both_sides',
            'problem_type': 'variables_on_both_sides'
        }
    )

    correct_sol5 = correct.solve(problem5)
    malrule_sol5 = malrule.solve(problem5)

    print(f"Problem: {problem5.text}")
    print(f"Correct answer: x = {correct_sol5.answer}")
    print(f"Malrule answer: x = {malrule_sol5.answer}")

    # Correct: 3x + 5 = x + 13 → 3x - x = 13 - 5 → 2x = 8 → x = 4
    # Malrule: Changes signs incorrectly
    assert correct_sol5.answer == 4, f"Expected 4, got {correct_sol5.answer}"
    assert malrule_sol5.answer != 4, f"Malrule should produce different answer"

    print("✓ TEST CASE 5 PASSED: Variables on both sides template works")

    # TEST CASE 6: Negative coefficients (-x + 12 = 5)
    print("\n\nTEST CASE 6: Negative coefficients (-x + 12 = 5)")
    print("-"*70)

    problem6 = Problem(
        text="Solve for x: -x + 12 = 5",
        operands=[7],
        operation='solve_equation',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'equation': '-x + 12 = 5',
            'correct_x': 7,
            'equation_type': 'negative_coefficients',
            'operation': 'negative_coeff_simple',
            'problem_type': 'negative_coefficients'
        }
    )

    correct_sol6 = correct.solve(problem6)
    malrule_sol6 = malrule.solve(problem6)

    print(f"Problem: {problem6.text}")
    print(f"Correct answer: x = {correct_sol6.answer}")
    print(f"Malrule answer: x = {malrule_sol6.answer}")

    # Correct: -x + 12 = 5 → -x = -7 → x = 7
    # Malrule: Changes signs incorrectly when moving terms
    assert correct_sol6.answer == 7, f"Expected 7, got {correct_sol6.answer}"
    assert malrule_sol6.answer != 7, f"Malrule should produce different answer"

    print("✓ TEST CASE 6 PASSED: Negative coefficients template works")

    # TEST CASE 7: Word problem context
    print("\n\nTEST CASE 7: Word problem context (money problem)")
    print("-"*70)

    problem7 = Problem(
        text="Maria has some money. After receiving $20, she has $35. How much money did she have initially? (Let x be the initial amount.) Solve: x + 20 = 35",
        operands=[15],
        operation='solve_equation',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'equation': 'x + 20 = 35',
            'correct_x': 15,
            'equation_type': 'word_problem_context',
            'operation': 'word_problem',
            'problem_type': 'word_problem_context'
        }
    )

    correct_sol7 = correct.solve(problem7)
    malrule_sol7 = malrule.solve(problem7)

    print(f"Problem: {problem7.text}")
    print(f"Correct answer: x = {correct_sol7.answer}")
    print(f"Malrule answer: x = {malrule_sol7.answer}")

    # Correct: x + 20 = 35 → x = 15
    # Malrule: x = 35 + 20 = 55
    assert correct_sol7.answer == 15, f"Expected 15, got {correct_sol7.answer}"
    assert malrule_sol7.answer == 55, f"Expected 55 (malrule), got {malrule_sol7.answer}"

    print("✓ TEST CASE 7 PASSED: Word problem context template works")

    # TEST CASE 8: Three-step equation (2x + 10 - 3 = 13)
    print("\n\nTEST CASE 8: Three-step equation (2x + 10 - 3 = 13)")
    print("-"*70)

    problem8 = Problem(
        text="Solve for x: 2x + 10 - 3 = 13",
        operands=[3],
        operation='solve_equation',
        level=8,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'equation': '2x + 10 - 3 = 13',
            'correct_x': 3,
            'equation_type': 'three_step_equation',
            'operation': 'three_step',
            'problem_type': 'three_step_equation'
        }
    )

    correct_sol8 = correct.solve(problem8)
    malrule_sol8 = malrule.solve(problem8)

    print(f"Problem: {problem8.text}")
    print(f"Correct answer: x = {correct_sol8.answer}")
    print(f"Malrule answer: x = {malrule_sol8.answer}")

    # Correct: 2x + 10 - 3 = 13 → 2x + 7 = 13 → 2x = 6 → x = 3
    # Malrule: Changes signs incorrectly
    assert correct_sol8.answer == 3, f"Expected 3, got {correct_sol8.answer}"
    assert malrule_sol8.answer != 3, f"Malrule should produce different answer"

    print("✓ TEST CASE 8 PASSED: Three-step equation template works")

    print("\n" + "="*70)
    print("ALL NEW TEMPLATE TEST CASES PASSED ✓")
    print("="*70)


def test_template_generation():
    """Test that all template types can be generated."""
    print("\n\n" + "="*70)
    print("TESTING TEMPLATE GENERATION")
    print("="*70)

    problem_gen = LinearEquationProblemGenerator(
        level=9,
        difficulty=DifficultyLevel.HARD
    )

    # Generate multiple problems to cover all template types
    templates_found = set()
    for i in range(50):
        problem = problem_gen.generate(seed=14000 + i)
        if 'problem_type' in problem.metadata:
            templates_found.add(problem.metadata['problem_type'])

    print(f"\nTemplates generated: {sorted(templates_found)}")

    # Verify we have all expected templates
    expected_templates = {
        'x_plus_c',
        'x_minus_c',
        'c_minus_x',
        'two_step',
        'variables_on_both_sides',
        'negative_coefficients',
        'word_problem_context',
        'three_step_equation',
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

    problem_gen = LinearEquationProblemGenerator(
        level=7,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = ChangeSideChangeSignMalrule()
    correct = LinearEquationCorrectAlgorithm()

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
    print("║" + "  VERIFICATION TEST: Change-Side-Change-Sign  ".center(70) + "║")
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
