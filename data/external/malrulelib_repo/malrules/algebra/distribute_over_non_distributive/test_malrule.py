#!/usr/bin/env python3
"""Test script for Distribute-Over-Non-Distributive malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.algebra.distribute_over_non_distributive import (
    DistributeOverNonDistributiveProblemGenerator,
    DistributeOverNonDistributiveMalrule,
    AlgebraExpansionCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING DISTRIBUTE-OVER-NON-DISTRIBUTIVE")
    print("="*70)

    malrule = DistributeOverNonDistributiveMalrule()
    correct = AlgebraExpansionCorrectAlgorithm()

    # Test case 1: (x+3)²
    problem1 = Problem(
        text="Expand: (x+3)²",
        operands=[],
        operation='algebra_expansion',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'variable': 'x',
            'constant': 3,
            'operation': 'square_binomial',
            'correct_coeffs': {'x²': 1, 'x': 6, 'constant': 9},
            'malrule_coeffs': {'x²': 1, 'x': 0, 'constant': 9},
            'expression': '(x+3)²'
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: (x+3)² → Correct: {correct_sol.answer}, Malrule: {malrule_sol.answer}")
    assert correct_sol.answer == "x² + 6x + 9"
    assert malrule_sol.answer == "x² + 9"
    assert correct_sol.answer != malrule_sol.answer
    print("✓ PASSED")

    # Test case 2: (x+5)²
    problem2 = Problem(
        text="Expand: (x+5)²",
        operands=[],
        operation='algebra_expansion',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'variable': 'x',
            'constant': 5,
            'operation': 'square_binomial',
            'correct_coeffs': {'x²': 1, 'x': 10, 'constant': 25},
            'malrule_coeffs': {'x²': 1, 'x': 0, 'constant': 25},
            'expression': '(x+5)²'
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert correct_sol2.answer == "x² + 10x + 25"
    assert malrule_sol2.answer == "x² + 25"
    print("✓ TEST 2 PASSED")

    # Test case 3: √(9+16)
    problem3 = Problem(
        text="Simplify: √(9+16)",
        operands=[],
        operation='algebra_expansion',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'num1': 9,
            'num2': 16,
            'operation': 'sqrt_sum',
            'correct_answer': 5.0,  # √25 = 5
            'malrule_answer': 7.0,  # √9 + √16 = 3 + 4 = 7
            'expression': '√(9+16)'
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert correct_sol3.answer == 5.0
    assert malrule_sol3.answer == 7.0
    print("✓ TEST 3 PASSED")

    # Test case 4: (y+2)²
    problem4 = Problem(
        text="Expand: (y+2)²",
        operands=[],
        operation='algebra_expansion',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'variable': 'y',
            'constant': 2,
            'operation': 'square_binomial',
            'correct_coeffs': {'x²': 1, 'x': 4, 'constant': 4},
            'malrule_coeffs': {'x²': 1, 'x': 0, 'constant': 4},
            'expression': '(y+2)²'
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    assert correct_sol4.answer == "y² + 4y + 4"
    assert malrule_sol4.answer == "y² + 4"
    print("✓ TEST 4 PASSED")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_all_templates():
    """Test all 5 templates to ensure they work correctly."""
    print("\n\n" + "="*70)
    print("TESTING ALL TEMPLATES")
    print("="*70)

    malrule = DistributeOverNonDistributiveMalrule()
    correct = AlgebraExpansionCorrectAlgorithm()
    templates = ['basic_square_binomial', 'basic_sqrt_sum', 'square_binomial_subtraction', 'sqrt_difference', 'word_problem']

    for template in templates:
        print(f"\n--- Testing template: {template} ---")
        problem_gen = DistributeOverNonDistributiveProblemGenerator(level=8, difficulty=DifficultyLevel.MEDIUM)
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

    malrule = DistributeOverNonDistributiveMalrule()
    correct = AlgebraExpansionCorrectAlgorithm()

    # Test 1: basic_square_binomial template
    print("\n--- Test 1: basic_square_binomial ---")
    problem1 = Problem(
        text="Expand: (x+4)²",
        operands=[4],
        operation='algebra_expansion',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'variable': 'x',
            'constant': 4,
            'operation': 'square_binomial',
            'correct_coeffs': {'x²': 1, 'x': 8, 'constant': 16},
            'malrule_coeffs': {'x²': 1, 'x': 0, 'constant': 16},
            'expression': '(x+4)²',
            'template': 'basic_square_binomial'
        }
    )
    correct_sol1 = correct.solve(problem1)
    malrule_sol1 = malrule.solve(problem1)
    expected1 = malrule.calculate_expected_answer(problem1)

    assert correct_sol1.answer == "x² + 8x + 16"
    assert malrule_sol1.answer == "x² + 16"
    assert expected1 == malrule_sol1.answer
    assert correct_sol1.answer != malrule_sol1.answer
    print(f"  (x+4)² → Correct: {correct_sol1.answer}, Malrule: {malrule_sol1.answer}")
    print("  ✓ PASSED")

    # Test 2: basic_sqrt_sum template
    print("\n--- Test 2: basic_sqrt_sum ---")
    problem2 = Problem(
        text="Simplify: √(4+9)",
        operands=[4, 9],
        operation='algebra_expansion',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'num1': 4,
            'num2': 9,
            'operation': 'sqrt_sum',
            'correct_answer': round((4+9)**0.5, 2),
            'malrule_answer': round(4**0.5 + 9**0.5, 2),
            'expression': '√(4+9)',
            'template': 'basic_sqrt_sum'
        }
    )
    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    expected2 = malrule.calculate_expected_answer(problem2)

    assert expected2 == malrule_sol2.answer
    assert correct_sol2.answer != malrule_sol2.answer
    print(f"  √(4+9) → Correct: {correct_sol2.answer}, Malrule: {malrule_sol2.answer}")
    print("  ✓ PASSED")

    # Test 3: square_binomial_subtraction template
    print("\n--- Test 3: square_binomial_subtraction ---")
    problem3 = Problem(
        text="Expand: (x-5)²",
        operands=[5],
        operation='algebra_expansion',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'variable': 'x',
            'constant': 5,
            'operation': 'square_binomial',
            'correct_coeffs': {'x²': 1, 'x': -10, 'constant': 25},
            'malrule_coeffs': {'x²': 1, 'x': 0, 'constant': 25},
            'expression': '(x-5)²',
            'template': 'square_binomial_subtraction',
            'is_subtraction': True
        }
    )
    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    expected3 = malrule.calculate_expected_answer(problem3)

    # Verify malrule answer and expected match
    assert malrule_sol3.answer == "x² + 25"
    assert expected3 == malrule_sol3.answer
    # Verify correct and malrule give different answers
    assert correct_sol3.answer != malrule_sol3.answer
    print(f"  (x-5)² → Correct: {correct_sol3.answer}, Malrule: {malrule_sol3.answer}")
    print("  ✓ PASSED")

    # Test 4: sqrt_difference template
    print("\n--- Test 4: sqrt_difference ---")
    problem4 = Problem(
        text="Simplify: √(3²+4²)",
        operands=[3, 4],
        operation='algebra_expansion',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'num1': 3,
            'num2': 4,
            'sum_of_squares': 25,
            'operation': 'sqrt_sum',
            'correct_answer': 5.0,
            'malrule_answer': 7,
            'expression': '√(3²+4²)',
            'template': 'sqrt_difference',
            'is_pythagorean': True
        }
    )
    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    expected4 = malrule.calculate_expected_answer(problem4)

    assert expected4 == malrule_sol4.answer
    assert correct_sol4.answer != malrule_sol4.answer
    print(f"  √(3²+4²) → Correct: {correct_sol4.answer}, Malrule: {malrule_sol4.answer}")
    print("  ✓ PASSED")

    print("\n" + "="*70)
    print("ALL TEMPLATE-SPECIFIC TESTS PASSED ✓")
    print("="*70)


def test_automated_suite():
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = DistributeOverNonDistributiveProblemGenerator(
        level=8,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = DistributeOverNonDistributiveMalrule()
    correct = AlgebraExpansionCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Distribute-Over-Non-Distributive  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    try:
        test_specific_examples()
        test_all_templates()
        test_template_specific_cases()
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
