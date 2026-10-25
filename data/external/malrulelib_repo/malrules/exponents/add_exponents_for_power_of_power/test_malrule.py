#!/usr/bin/env python3
"""Test script for Add-Exponents-For-Power-Of-Power malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.exponents.add_exponents_for_power_of_power import (
    AddExponentsForPowerOfPowerProblemGenerator,
    AddExponentsForPowerOfPowerMalrule,
    PowerOfPowerCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING ADD-EXPONENTS-FOR-POWER-OF-POWER")
    print("="*70)

    malrule = AddExponentsForPowerOfPowerMalrule()
    correct = PowerOfPowerCorrectAlgorithm()

    # Test case 1: (x²)³ = x⁶ (correct), x⁵ (malrule: 2+3=5)
    problem1 = Problem(
        text="Simplify: (x^2)^3",
        operands=[2, 3],
        operation='power_of_power',
        level=8,
        difficulty=DifficultyLevel.EASY,
        metadata={
            'coefficient': 1,
            'inner_exponent': 2,
            'outer_exponent': 3,
            'correct_exponent': 6,
            'correct_coefficient': 1,
            'malrule_exponent': 5,
            'malrule_coefficient': 1,
            'correct_answer': 'x^6',
            'malrule_answer': 'x^5'
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: (x²)³ → Correct: {correct_sol.answer}, Malrule: {malrule_sol.answer}")
    assert correct_sol.answer == 'x^6'
    assert malrule_sol.answer == 'x^5'
    assert correct_sol.answer != malrule_sol.answer
    print("✓ PASSED")

    # Test case 2: (a³)⁵ = a¹⁵ (correct), a⁸ (malrule: 3+5=8)
    problem2 = Problem(
        text="Simplify: (x^3)^5",
        operands=[3, 5],
        operation='power_of_power',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': 1,
            'inner_exponent': 3,
            'outer_exponent': 5,
            'correct_exponent': 15,
            'correct_coefficient': 1,
            'malrule_exponent': 8,
            'malrule_coefficient': 1,
            'correct_answer': 'x^15',
            'malrule_answer': 'x^8'
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert correct_sol2.answer == 'x^15'
    assert malrule_sol2.answer == 'x^8'
    print("✓ TEST 2 PASSED")

    # Test case 3: (2x³)⁴ = 16x¹² (correct), 2x⁷ (malrule: 3+4=7, forgets coefficient)
    problem3 = Problem(
        text="Simplify: (2x^3)^4",
        operands=[3, 4],
        operation='power_of_power',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': 2,
            'inner_exponent': 3,
            'outer_exponent': 4,
            'correct_exponent': 12,
            'correct_coefficient': 16,
            'malrule_exponent': 7,
            'malrule_coefficient': 2,
            'correct_answer': '16x^12',
            'malrule_answer': '2x^7'
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert correct_sol3.answer == '16x^12'
    assert malrule_sol3.answer == '2x^7'
    print("✓ TEST 3 PASSED")

    # Test case 4: (x⁴)² = x⁸ (correct), x⁶ (malrule: 4+2=6)
    problem4 = Problem(
        text="Simplify: (x^4)^2",
        operands=[4, 2],
        operation='power_of_power',
        level=8,
        difficulty=DifficultyLevel.EASY,
        metadata={
            'coefficient': 1,
            'inner_exponent': 4,
            'outer_exponent': 2,
            'correct_exponent': 8,
            'correct_coefficient': 1,
            'malrule_exponent': 6,
            'malrule_coefficient': 1,
            'correct_answer': 'x^8',
            'malrule_answer': 'x^6'
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    assert correct_sol4.answer == 'x^8'
    assert malrule_sol4.answer == 'x^6'
    print("✓ TEST 4 PASSED")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_all_templates():
    """Test all 6 templates to ensure they work correctly."""
    print("\n\n" + "="*70)
    print("TESTING ALL TEMPLATES")
    print("="*70)

    malrule = AddExponentsForPowerOfPowerMalrule()
    correct = PowerOfPowerCorrectAlgorithm()
    templates = ['basic_power_of_power', 'with_coefficient', 'numerical_evaluation',
                 'product_of_powers', 'word_problem', 'word_problem_context']

    for template in templates:
        print(f"\n--- Testing template: {template} ---")
        problem_gen = AddExponentsForPowerOfPowerProblemGenerator(
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

    malrule = AddExponentsForPowerOfPowerMalrule()
    correct = PowerOfPowerCorrectAlgorithm()

    # Test 1: basic_power_of_power template
    print("\n--- Test 1: basic_power_of_power ---")
    problem1 = Problem(
        text="Simplify: (x^3)^4",
        operands=[3, 4],
        operation='power_of_power',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': 1,
            'inner_exponent': 3,
            'outer_exponent': 4,
            'correct_exponent': 12,
            'correct_coefficient': 1,
            'malrule_exponent': 7,
            'malrule_coefficient': 1,
            'correct_answer': 'x^12',
            'malrule_answer': 'x^7',
            'template': 'basic_power_of_power'
        }
    )
    correct_sol1 = correct.solve(problem1)
    malrule_sol1 = malrule.solve(problem1)
    expected1 = malrule.calculate_expected_answer(problem1)

    assert correct_sol1.answer == 'x^12'
    assert malrule_sol1.answer == 'x^7'
    assert expected1 == malrule_sol1.answer
    assert correct_sol1.answer != malrule_sol1.answer
    print(f"  (x^3)^4 → Correct: {correct_sol1.answer}, Malrule: {malrule_sol1.answer}")
    print("  ✓ PASSED")

    # Test 2: with_coefficient template
    print("\n--- Test 2: with_coefficient ---")
    problem2 = Problem(
        text="Simplify: (3x^2)^3",
        operands=[2, 3],
        operation='power_of_power',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': 3,
            'inner_exponent': 2,
            'outer_exponent': 3,
            'correct_exponent': 6,
            'correct_coefficient': 27,
            'malrule_exponent': 5,
            'malrule_coefficient': 3,
            'correct_answer': '27x^6',
            'malrule_answer': '3x^5',
            'template': 'with_coefficient'
        }
    )
    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    expected2 = malrule.calculate_expected_answer(problem2)

    assert correct_sol2.answer == '27x^6'
    assert malrule_sol2.answer == '3x^5'
    assert expected2 == malrule_sol2.answer
    assert correct_sol2.answer != malrule_sol2.answer
    print(f"  (3x^2)^3 → Correct: {correct_sol2.answer}, Malrule: {malrule_sol2.answer}")
    print("  ✓ PASSED")

    # Test 3: numerical_evaluation template
    print("\n--- Test 3: numerical_evaluation ---")
    problem3 = Problem(
        text="Evaluate: (2^2)^3",
        operands=[2, 2, 3],
        operation='power_of_power',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'base': 2,
            'inner_exponent': 2,
            'outer_exponent': 3,
            'correct_answer': 64,
            'malrule_answer': 32,
            'template': 'numerical_evaluation'
        }
    )
    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    expected3 = malrule.calculate_expected_answer(problem3)

    assert correct_sol3.answer == 64
    assert malrule_sol3.answer == 32
    assert expected3 == malrule_sol3.answer
    assert correct_sol3.answer != malrule_sol3.answer
    print(f"  (2^2)^3 → Correct: {correct_sol3.answer}, Malrule: {malrule_sol3.answer}")
    print("  ✓ PASSED")

    # Test 4: product_of_powers template
    print("\n--- Test 4: product_of_powers ---")
    problem4 = Problem(
        text="Simplify: (x^2)^3 × x^4",
        operands=[2, 3, 4],
        operation='power_of_power',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'inner_exponent': 2,
            'outer_exponent': 3,
            'additional_exponent': 4,
            'correct_exponent': 10,
            'malrule_exponent': 9,
            'correct_answer': 'x^10',
            'malrule_answer': 'x^9',
            'template': 'product_of_powers'
        }
    )
    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    expected4 = malrule.calculate_expected_answer(problem4)

    assert correct_sol4.answer == 'x^10'
    assert malrule_sol4.answer == 'x^9'
    assert expected4 == malrule_sol4.answer
    assert correct_sol4.answer != malrule_sol4.answer
    print(f"  (x^2)^3 × x^4 → Correct: {correct_sol4.answer}, Malrule: {malrule_sol4.answer}")
    print("  ✓ PASSED")

    # Test 5: word_problem template
    print("\n--- Test 5: word_problem ---")
    problem5 = Problem(
        text="A number is raised to the 3 power, then that result is raised to the 2 power, what is the exponent in the final expression x^?",
        operands=[3, 2],
        operation='power_of_power',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'inner_exponent': 3,
            'outer_exponent': 2,
            'correct_answer': 'x^6',
            'malrule_answer': 'x^5',
            'template': 'word_problem'
        }
    )
    correct_sol5 = correct.solve(problem5)
    malrule_sol5 = malrule.solve(problem5)
    expected5 = malrule.calculate_expected_answer(problem5)

    assert correct_sol5.answer == 'x^6'
    assert malrule_sol5.answer == 'x^5'
    assert expected5 == malrule_sol5.answer
    assert correct_sol5.answer != malrule_sol5.answer
    print(f"  Word problem → Correct: {correct_sol5.answer}, Malrule: {malrule_sol5.answer}")
    print("  ✓ PASSED")

    print("\n" + "="*70)
    print("ALL TEMPLATE-SPECIFIC TESTS PASSED ✓")
    print("="*70)


def test_automated_suite():
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = AddExponentsForPowerOfPowerProblemGenerator(
        level=9,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = AddExponentsForPowerOfPowerMalrule()
    correct = PowerOfPowerCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Add-Exponents-For-Power-Of-Power  ".center(70) + "║")
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
