#!/usr/bin/env python3
"""Test script for Forget-Exponent-On-Coefficient malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.exponents.forget_exponent_on_coefficient import (
    ForgetExponentOnCoefficientProblemGenerator,
    ForgetExponentOnCoefficientMalrule,
    PowerOfPowerCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING FORGET-EXPONENT-ON-COEFFICIENT")
    print("="*70)

    malrule = ForgetExponentOnCoefficientMalrule()
    correct = PowerOfPowerCorrectAlgorithm()

    # Test case 1: (2x³)⁵ → Correct: 32x¹⁵, Malrule: 2x¹⁵
    problem1 = Problem(
        text="Simplify: (2x^3)^5",
        operands=[2, 3, 5],
        operation='power_of_power',
        level=9,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'coefficient': 2,
            'base_exponent': 3,
            'outer_exponent': 5,
            'new_coefficient': 32,
            'new_exponent': 15,
            'correct_answer': '32x^15',
            'malrule_answer': '2x^15'
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: (2x³)⁵ → Correct: {correct_sol.answer}, Malrule: {malrule_sol.answer}")
    assert correct_sol.answer == '32x^15'
    assert malrule_sol.answer == '2x^15'
    assert correct_sol.answer != malrule_sol.answer
    print("✓ PASSED")

    # Test case 2: (3y²)³ → Correct: 27y⁶, Malrule: 3y⁶
    problem2 = Problem(
        text="Simplify: (3y^2)^3",
        operands=[3, 2, 3],
        operation='power_of_power',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': 3,
            'base_exponent': 2,
            'outer_exponent': 3,
            'new_coefficient': 27,
            'new_exponent': 6,
            'variable': 'y',  # Added to support variable parsing
            'correct_answer': '27y^6',
            'malrule_answer': '3y^6'
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert correct_sol2.answer == '27y^6'
    assert malrule_sol2.answer == '3y^6'
    print("✓ TEST 2 PASSED")

    # Test case 3: (5a⁴)² → Correct: 25a⁸, Malrule: 5a⁸
    problem3 = Problem(
        text="Simplify: (5a^4)^2",
        operands=[5, 4, 2],
        operation='power_of_power',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': 5,
            'base_exponent': 4,
            'outer_exponent': 2,
            'new_coefficient': 25,
            'new_exponent': 8,
            'variable': 'a',  # Added to support variable parsing
            'correct_answer': '25a^8',
            'malrule_answer': '5a^8'
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert correct_sol3.answer == '25a^8'
    assert malrule_sol3.answer == '5a^8'
    print("✓ TEST 3 PASSED")

    # Test case 4: (2m²)⁴ → Correct: 16m⁸, Malrule: 2m⁸
    problem4 = Problem(
        text="Simplify: (2m^2)^4",
        operands=[2, 2, 4],
        operation='power_of_power',
        level=9,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'coefficient': 2,
            'base_exponent': 2,
            'outer_exponent': 4,
            'new_coefficient': 16,
            'new_exponent': 8,
            'variable': 'm',  # Added to support variable parsing
            'correct_answer': '16m^8',
            'malrule_answer': '2m^8'
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    assert correct_sol4.answer == '16m^8'
    assert malrule_sol4.answer == '2m^8'
    print("✓ TEST 4 PASSED")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_all_templates():
    """Test all templates to ensure they work correctly."""
    print("\n\n" + "="*70)
    print("TESTING ALL TEMPLATES")
    print("="*70)

    malrule = ForgetExponentOnCoefficientMalrule()
    correct = PowerOfPowerCorrectAlgorithm()
    templates = ['basic_power_of_power', 'larger_coefficients', 'negative_coefficient',
                 'multiple_variables', 'word_problem', 'word_problem_context']

    for template in templates:
        print(f"\n--- Testing template: {template} ---")
        problem_gen = ForgetExponentOnCoefficientProblemGenerator(
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

    malrule = ForgetExponentOnCoefficientMalrule()
    correct = PowerOfPowerCorrectAlgorithm()

    # Test 1: basic_power_of_power template
    print("\n--- Test 1: basic_power_of_power ---")
    problem1 = Problem(
        text="Simplify: (3x^2)^4",
        operands=[3, 2, 4],
        operation='power_of_power',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': 3,
            'base_exponent': 2,
            'outer_exponent': 4,
            'new_coefficient': 81,
            'new_exponent': 8,
            'correct_answer': '81x^8',
            'malrule_answer': '3x^8',
            'template': 'basic_power_of_power'
        }
    )
    correct_sol1 = correct.solve(problem1)
    malrule_sol1 = malrule.solve(problem1)
    expected1 = malrule.calculate_expected_answer(problem1)

    assert correct_sol1.answer == '81x^8'
    assert malrule_sol1.answer == '3x^8'
    assert expected1 == malrule_sol1.answer
    assert correct_sol1.answer != malrule_sol1.answer
    print(f"  (3x^2)^4 → Correct: {correct_sol1.answer}, Malrule: {malrule_sol1.answer}")
    print("  ✓ PASSED")

    # Test 2: larger_coefficients template
    print("\n--- Test 2: larger_coefficients ---")
    problem2 = Problem(
        text="Simplify: (7x^2)^3",
        operands=[7, 2, 3],
        operation='power_of_power',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': 7,
            'base_exponent': 2,
            'outer_exponent': 3,
            'new_coefficient': 343,
            'new_exponent': 6,
            'correct_answer': '343x^6',
            'malrule_answer': '7x^6',
            'template': 'larger_coefficients'
        }
    )
    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    expected2 = malrule.calculate_expected_answer(problem2)

    assert correct_sol2.answer == '343x^6'
    assert malrule_sol2.answer == '7x^6'
    assert expected2 == malrule_sol2.answer
    assert correct_sol2.answer != malrule_sol2.answer
    print(f"  (7x^2)^3 → Correct: {correct_sol2.answer}, Malrule: {malrule_sol2.answer}")
    print("  ✓ PASSED")

    # Test 3: negative_coefficient template
    print("\n--- Test 3: negative_coefficient ---")
    problem3 = Problem(
        text="Simplify: (-3x^2)^2",
        operands=[-3, 2, 2],
        operation='power_of_power',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': -3,
            'base_exponent': 2,
            'outer_exponent': 2,
            'new_coefficient': 9,
            'new_exponent': 4,
            'correct_answer': '9x^4',
            'malrule_answer': '-3x^4',
            'template': 'negative_coefficient'
        }
    )
    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    expected3 = malrule.calculate_expected_answer(problem3)

    assert correct_sol3.answer == '9x^4'
    assert malrule_sol3.answer == '-3x^4'
    assert expected3 == malrule_sol3.answer
    assert correct_sol3.answer != malrule_sol3.answer
    print(f"  (-3x^2)^2 → Correct: {correct_sol3.answer}, Malrule: {malrule_sol3.answer}")
    print("  ✓ PASSED")

    # Test 4: multiple_variables template
    print("\n--- Test 4: multiple_variables ---")
    problem4 = Problem(
        text="Simplify: (2xy^2)^3",
        operands=[2, 1, 2, 3],
        operation='power_of_power',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': 2,
            'x_exponent': 1,
            'y_exponent': 2,
            'outer_exponent': 3,
            'new_coefficient': 8,
            'new_x_exponent': 3,
            'new_y_exponent': 6,
            'correct_answer': '8x^3y^6',
            'malrule_answer': '2x^3y^6',
            'template': 'multiple_variables'
        }
    )
    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    expected4 = malrule.calculate_expected_answer(problem4)

    assert correct_sol4.answer == '8x^3y^6'
    assert malrule_sol4.answer == '2x^3y^6'
    assert expected4 == malrule_sol4.answer
    assert correct_sol4.answer != malrule_sol4.answer
    print(f"  (2xy^2)^3 → Correct: {correct_sol4.answer}, Malrule: {malrule_sol4.answer}")
    print("  ✓ PASSED")

    # Test 5: word_problem template
    print("\n--- Test 5: word_problem ---")
    problem5 = Problem(
        text="The area of a square is 3x^2. If you scale each side by x^2, what is the new area?",
        operands=[3, 2, 2],
        operation='power_of_power',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': 3,
            'base_exponent': 2,
            'outer_exponent': 2,
            'new_coefficient': 9,
            'new_exponent': 4,
            'correct_answer': '9x^4',
            'malrule_answer': '3x^4',
            'context_type': 'area_scaling',
            'template': 'word_problem'
        }
    )
    correct_sol5 = correct.solve(problem5)
    malrule_sol5 = malrule.solve(problem5)
    expected5 = malrule.calculate_expected_answer(problem5)

    assert correct_sol5.answer == '9x^4'
    assert malrule_sol5.answer == '3x^4'
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

    problem_gen = ForgetExponentOnCoefficientProblemGenerator(
        level=9,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = ForgetExponentOnCoefficientMalrule()
    correct = PowerOfPowerCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Forget-Exponent-On-Coefficient  ".center(70) + "║")
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
