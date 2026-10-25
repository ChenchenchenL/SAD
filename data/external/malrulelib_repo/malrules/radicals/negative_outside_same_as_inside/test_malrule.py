#!/usr/bin/env python3
"""
Test script for Negative-Outside-Same-As-Inside malrule.

Run from project root: python3 -m malrules.radicals.negative_outside_same_as_inside.test_malrule
Or from this directory: python3 test_malrule.py

This script demonstrates and tests the Negative-Outside-Same-As-Inside malrule
with clear examples and verification.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, InteractiveDemo, MalruleComparison, Problem
from malrules.radicals.negative_outside_same_as_inside import (
    NegativeOutsideSameAsInsideProblemGenerator,
    NegativeOutsideSameAsInsideMalrule,
    NegativeSquareRootCorrectAlgorithm
)


def test_specific_examples():
    """Test with specific, well-known examples."""
    print("="*70)
    print("TESTING WITH SPECIFIC EXAMPLES")
    print("="*70)

    # Create instances
    malrule = NegativeOutsideSameAsInsideMalrule()
    correct = NegativeSquareRootCorrectAlgorithm()

    # Test case 1: -√4 (from specification)
    print("\n" + "-"*70)
    print("TEST CASE 1: -√4 (Classic example from specification)")
    print("-"*70)

    problem1 = Problem(
        text="What is -√4?",
        operands=[4],
        operation='negative_square_root',
        level=9,
        difficulty=DifficultyLevel.EASY
    )

    correct_solution1 = correct.solve(problem1)
    malrule_solution1 = malrule.solve(problem1)

    print(f"\nProblem: {problem1.text}")
    print(f"\nCorrect answer: {correct_solution1.answer}")
    print(f"Malrule answer: {malrule_solution1.answer}")
    print(f"Answers different? {correct_solution1.answer != malrule_solution1.answer}")

    print("\n--- Correct Solution Steps ---")
    for step in correct_solution1.steps:
        print(f"  {step}")

    print("\n--- Malrule Solution Steps ---")
    for step in malrule_solution1.steps:
        print(f"  {step}")

    # Verify expected answers
    assert correct_solution1.answer == "-2", f"Expected -2, got {correct_solution1.answer}"
    assert malrule_solution1.answer == "No real solution", f"Expected 'No real solution', got {malrule_solution1.answer}"
    print("\n✓ TEST CASE 1 PASSED: Answers match expected values")

    # Test case 2: -√9
    print("\n" + "-"*70)
    print("TEST CASE 2: -√9")
    print("-"*70)

    problem2 = Problem(
        text="What is -√9?",
        operands=[9],
        operation='negative_square_root',
        level=9,
        difficulty=DifficultyLevel.EASY
    )

    correct_solution2 = correct.solve(problem2)
    malrule_solution2 = malrule.solve(problem2)

    print(f"\nProblem: {problem2.text}")
    print(f"Correct answer: {correct_solution2.answer}")
    print(f"Malrule answer: {malrule_solution2.answer}")
    print(f"Answers different? {correct_solution2.answer != malrule_solution2.answer}")

    # Expected: -√9 = -3 (correct)
    # Malrule: "No real solution" (incorrect)
    assert correct_solution2.answer == "-3", f"Expected -3, got {correct_solution2.answer}"
    assert malrule_solution2.answer == "No real solution", f"Expected 'No real solution', got {malrule_solution2.answer}"
    print("✓ TEST CASE 2 PASSED: Answers match expected values")

    # Test case 3: -√16
    print("\n" + "-"*70)
    print("TEST CASE 3: -√16")
    print("-"*70)

    problem3 = Problem(
        text="What is -√16?",
        operands=[16],
        operation='negative_square_root',
        level=9,
        difficulty=DifficultyLevel.EASY
    )

    correct_solution3 = correct.solve(problem3)
    malrule_solution3 = malrule.solve(problem3)

    print(f"\nProblem: {problem3.text}")
    print(f"Correct answer: {correct_solution3.answer}")
    print(f"Malrule answer: {malrule_solution3.answer}")
    print(f"Answers different? {correct_solution3.answer != malrule_solution3.answer}")

    # Expected: -√16 = -4 (correct)
    # Malrule: "No real solution" (incorrect)
    assert correct_solution3.answer == "-4", f"Expected -4, got {correct_solution3.answer}"
    assert malrule_solution3.answer == "No real solution", f"Expected 'No real solution', got {malrule_solution3.answer}"
    print("✓ TEST CASE 3 PASSED: Answers match expected values")

    # Test case 4: -√25
    print("\n" + "-"*70)
    print("TEST CASE 4: -√25")
    print("-"*70)

    problem4 = Problem(
        text="What is -√25?",
        operands=[25],
        operation='negative_square_root',
        level=9,
        difficulty=DifficultyLevel.MEDIUM
    )

    correct_solution4 = correct.solve(problem4)
    malrule_solution4 = malrule.solve(problem4)

    print(f"\nProblem: {problem4.text}")
    print(f"Correct answer: {correct_solution4.answer}")
    print(f"Malrule answer: {malrule_solution4.answer}")
    print(f"Answers different? {correct_solution4.answer != malrule_solution4.answer}")

    # Expected: -√25 = -5 (correct)
    # Malrule: "No real solution" (incorrect)
    assert correct_solution4.answer == "-5", f"Expected -5, got {correct_solution4.answer}"
    assert malrule_solution4.answer == "No real solution", f"Expected 'No real solution', got {malrule_solution4.answer}"
    print("✓ TEST CASE 4 PASSED: Answers match expected values")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_random_generation():
    """Test with randomly generated problems."""
    print("\n\n" + "="*70)
    print("TESTING WITH RANDOMLY GENERATED PROBLEMS")
    print("="*70)

    problem_gen = NegativeOutsideSameAsInsideProblemGenerator(
        level=9,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = NegativeOutsideSameAsInsideMalrule()
    correct = NegativeSquareRootCorrectAlgorithm()

    print("\nGenerating 5 random problems and comparing solutions...")

    incorrect_count = 0
    for i in range(5):
        print(f"\n{'-'*70}")
        print(f"Random Test {i+1}")
        print('-'*70)

        problem = problem_gen.generate(seed=300+i)
        correct_solution = correct.solve(problem)
        malrule_solution = malrule.solve(problem)

        print(f"Problem: {problem.text}")
        print(f"Correct: {correct_solution.answer}")
        print(f"Malrule: {malrule_solution.answer}")

        if correct_solution.answer != malrule_solution.answer:
            print("✓ Malrule produces DIFFERENT (incorrect) answer")
            incorrect_count += 1
        else:
            print("⚠ Malrule happens to produce SAME answer (should not happen)")

    print(f"\n{incorrect_count}/5 problems produced incorrect answers with malrule")
    assert incorrect_count == 5, f"Expected all 5 to be incorrect, got {incorrect_count}"
    print("✓ RANDOM GENERATION TEST PASSED")


def test_automated_suite():
    """Run the automated test suite."""
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = NegativeOutsideSameAsInsideProblemGenerator(
        level=9,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = NegativeOutsideSameAsInsideMalrule()
    correct = NegativeSquareRootCorrectAlgorithm()

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


def test_all_templates():
    """Test all 5 templates to ensure they work correctly."""
    print("\n\n" + "="*70)
    print("TESTING ALL TEMPLATES")
    print("="*70)

    malrule = NegativeOutsideSameAsInsideMalrule()
    correct = NegativeSquareRootCorrectAlgorithm()
    templates = ['basic_negative_outside', 'expression_form', 'in_equations',
                 'combined_operations', 'word_problem']

    for template in templates:
        print(f"\n--- Testing template: {template} ---")
        problem_gen = NegativeOutsideSameAsInsideProblemGenerator(
            level=9,
            difficulty=DifficultyLevel.MEDIUM
        )
        problem = problem_gen.generate(seed=42, template=template)

        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        # Verify calculate_expected_answer matches malrule solution
        expected_answer = malrule.calculate_expected_answer(problem)
        assert expected_answer == malrule_sol.answer, \
            f"Template {template}: calculate_expected_answer ({expected_answer}) != malrule solution ({malrule_sol.answer})"

        # Verify correct and malrule give different answers
        assert correct_sol.answer != malrule_sol.answer, \
            f"Template {template}: Correct and malrule answers should differ"

        print(f"  Problem: {problem.text}")
        print(f"  Correct answer: {correct_sol.answer}")
        print(f"  Malrule answer: {malrule_sol.answer}")
        print(f"  Expected (calculate_expected_answer): {expected_answer}")
        print(f"  ✓ Template {template} PASSED")

    print("\n" + "="*70)
    print("ALL TEMPLATE TESTS PASSED ✓")
    print("="*70)


def test_template_specific_cases():
    """Test specific template cases with known values."""
    print("\n\n" + "="*70)
    print("TESTING TEMPLATE-SPECIFIC CASES")
    print("="*70)

    malrule = NegativeOutsideSameAsInsideMalrule()
    correct = NegativeSquareRootCorrectAlgorithm()

    # Test 1: basic_negative_outside template
    print("\n--- Test 1: basic_negative_outside ---")
    problem1 = Problem(
        text="What is -√36?",
        operands=[36],
        operation='negative_square_root',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'radicand': 36,
            'base': 6,
            'correct_answer': '-6',
            'malrule_answer': 'No real solution',
            'template': 'basic_negative_outside'
        }
    )
    correct_sol1 = correct.solve(problem1)
    malrule_sol1 = malrule.solve(problem1)
    expected1 = malrule.calculate_expected_answer(problem1)

    assert correct_sol1.answer == '-6'
    assert malrule_sol1.answer == 'No real solution'
    assert expected1 == malrule_sol1.answer
    assert correct_sol1.answer != malrule_sol1.answer
    print(f"  -√36 → Correct: {correct_sol1.answer}, Malrule: {malrule_sol1.answer}")
    print("  ✓ PASSED")

    # Test 2: expression_form template
    print("\n--- Test 2: expression_form ---")
    problem2 = Problem(
        text="Evaluate: -(√49)",
        operands=[49],
        operation='negative_square_root',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'radicand': 49,
            'base': 7,
            'correct_answer': '-7',
            'malrule_answer': 'No real solution',
            'template': 'expression_form'
        }
    )
    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    expected2 = malrule.calculate_expected_answer(problem2)

    assert correct_sol2.answer == '-7'
    assert malrule_sol2.answer == 'No real solution'
    assert expected2 == malrule_sol2.answer
    assert correct_sol2.answer != malrule_sol2.answer
    print(f"  -(√49) → Correct: {correct_sol2.answer}, Malrule: {malrule_sol2.answer}")
    print("  ✓ PASSED")

    # Test 3: in_equations template
    print("\n--- Test 3: in_equations ---")
    problem3 = Problem(
        text="Solve for x: x = -√64",
        operands=[64],
        operation='negative_square_root',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'radicand': 64,
            'base': 8,
            'correct_answer': 'x = -8',
            'malrule_answer': 'No real solution',
            'template': 'in_equations'
        }
    )
    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    expected3 = malrule.calculate_expected_answer(problem3)

    assert correct_sol3.answer == 'x = -8'
    assert malrule_sol3.answer == 'No real solution'
    assert expected3 == malrule_sol3.answer
    assert correct_sol3.answer != malrule_sol3.answer
    print(f"  x = -√64 → Correct: {correct_sol3.answer}, Malrule: {malrule_sol3.answer}")
    print("  ✓ PASSED")

    # Test 4: combined_operations template (addition)
    print("\n--- Test 4: combined_operations (addition) ---")
    problem4 = Problem(
        text="Calculate: -√4 + √9",
        operands=[4],
        operation='negative_square_root',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'radicand': 4,
            'base': 2,
            'radicand2': 9,
            'base2': 3,
            'operation': 'addition',
            'correct_answer': '1',
            'malrule_answer': 'No real solution',
            'template': 'combined_operations'
        }
    )
    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    expected4 = malrule.calculate_expected_answer(problem4)

    assert correct_sol4.answer == '1'
    assert malrule_sol4.answer == 'No real solution'
    assert expected4 == malrule_sol4.answer
    assert correct_sol4.answer != malrule_sol4.answer
    print(f"  -√4 + √9 → Correct: {correct_sol4.answer}, Malrule: {malrule_sol4.answer}")
    print("  ✓ PASSED")

    # Test 5: combined_operations template (multiplication)
    print("\n--- Test 5: combined_operations (multiplication) ---")
    problem5 = Problem(
        text="Calculate: 3(-√16)",
        operands=[16],
        operation='negative_square_root',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'radicand': 16,
            'base': 4,
            'coefficient': 3,
            'operation': 'multiplication',
            'correct_answer': '-12',
            'malrule_answer': 'No real solution',
            'template': 'combined_operations'
        }
    )
    correct_sol5 = correct.solve(problem5)
    malrule_sol5 = malrule.solve(problem5)
    expected5 = malrule.calculate_expected_answer(problem5)

    assert correct_sol5.answer == '-12'
    assert malrule_sol5.answer == 'No real solution'
    assert expected5 == malrule_sol5.answer
    assert correct_sol5.answer != malrule_sol5.answer
    print(f"  3(-√16) → Correct: {correct_sol5.answer}, Malrule: {malrule_sol5.answer}")
    print("  ✓ PASSED")

    # Test 6: word_problem template
    print("\n--- Test 6: word_problem ---")
    problem6 = Problem(
        text="A submarine is at a depth that can be modeled as -√25 meters. What is the depth?",
        operands=[25],
        operation='negative_square_root',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'radicand': 25,
            'base': 5,
            'correct_answer': '-5 meters below sea level',
            'malrule_answer': 'No real solution',
            'context_type': 'elevation',
            'template': 'word_problem'
        }
    )
    correct_sol6 = correct.solve(problem6)
    malrule_sol6 = malrule.solve(problem6)
    expected6 = malrule.calculate_expected_answer(problem6)

    assert correct_sol6.answer == '-5 meters below sea level'
    assert malrule_sol6.answer == 'No real solution'
    assert expected6 == malrule_sol6.answer
    assert correct_sol6.answer != malrule_sol6.answer
    print(f"  Word problem → Correct: {correct_sol6.answer}, Malrule: {malrule_sol6.answer}")
    print("  ✓ PASSED")

    print("\n" + "="*70)
    print("ALL TEMPLATE-SPECIFIC TESTS PASSED ✓")
    print("="*70)


def interactive_demo():
    """Show an interactive demo."""
    print("\n\n" + "="*70)
    print("INTERACTIVE DEMONSTRATION")
    print("="*70)

    problem_gen = NegativeOutsideSameAsInsideProblemGenerator(
        level=9,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = NegativeOutsideSameAsInsideMalrule()
    correct = NegativeSquareRootCorrectAlgorithm()

    demo = InteractiveDemo(malrule, correct, problem_gen)

    print(demo.show_malrule_info())
    print(demo.run_multiple_comparisons(count=2))


def main():
    """Run all verification tests."""
    print("\n")
    print("╔" + "═"*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  VERIFICATION TEST: Negative-Outside-Same-As-Inside Malrule  ".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "═"*68 + "╝")

    try:
        # Test 1: Specific examples
        test_specific_examples()

        # Test 2: All templates
        test_all_templates()

        # Test 3: Template-specific cases
        test_template_specific_cases()

        # Test 4: Random generation
        test_random_generation()

        # Test 5: Automated suite
        all_passed = test_automated_suite()


        # Final summary
        print("\n\n" + "╔" + "═"*68 + "╗")
        print("║" + " "*68 + "║")
        print("║" + "  ✓✓✓ VERIFICATION COMPLETE - ALL TESTS PASSED ✓✓✓  ".center(68) + "║")
        print("║" + " "*68 + "║")
        print("╚" + "═"*68 + "╝")

        print("\n📁 Test location:")
        print("  - Implementation: malrules/radicals/negative_outside_same_as_inside/")

        return 0 if all_passed else 1

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
