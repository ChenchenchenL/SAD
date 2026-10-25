#!/usr/bin/env python3
"""Test script for Forget-To-Add-Carried-Number malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.multiplication_division.forget_to_add_carried_number import (
    ForgetToAddCarriedNumberProblemGenerator,
    ForgetToAddCarriedNumberMalrule,
    MultiDigitMultiplicationCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING FORGET-TO-ADD-CARRIED-NUMBER")
    print("="*70)

    malrule = ForgetToAddCarriedNumberMalrule()
    correct = MultiDigitMultiplicationCorrectAlgorithm()

    # Test case 1: 23 × 4 = 92, but student gets 82 (forgets carry of 1)
    problem1 = Problem(
        text="23 × 4 = ?",
        operands=[23, 4],
        operation='multiplication',
        level=3,
        difficulty=DifficultyLevel.EASY,
        metadata={
            'multiplicand': 23,
            'multiplier': 4,
            'tens_digit': 2,
            'ones_digit': 3,
            'ones_product': 12,
            'ones_result': 2,
            'carry': 1,
            'tens_product': 8,
            'tens_with_carry': 9,
            'tens_without_carry': 8,
            'correct_answer': 92,
            'malrule_answer': 82
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: 23 × 4 → Correct: {correct_sol.answer}, Malrule: {malrule_sol.answer}")
    assert correct_sol.answer == '92'
    assert malrule_sol.answer == '82'
    assert correct_sol.answer != malrule_sol.answer
    print("✓ PASSED")

    # Test case 2: 47 × 5 = 235, but student gets 205 (forgets carry of 3)
    problem2 = Problem(
        text="47 × 5 = ?",
        operands=[47, 5],
        operation='multiplication',
        level=4,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'multiplicand': 47,
            'multiplier': 5,
            'tens_digit': 4,
            'ones_digit': 7,
            'ones_product': 35,
            'ones_result': 5,
            'carry': 3,
            'tens_product': 20,
            'tens_with_carry': 23,
            'tens_without_carry': 20,
            'correct_answer': 235,
            'malrule_answer': 205
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert correct_sol2.answer == '235'
    assert malrule_sol2.answer == '205'
    print("✓ TEST 2 PASSED")

    # Test case 3: 36 × 7 = 252, but student gets 212 (forgets carry of 4)
    problem3 = Problem(
        text="36 × 7 = ?",
        operands=[36, 7],
        operation='multiplication',
        level=4,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'multiplicand': 36,
            'multiplier': 7,
            'tens_digit': 3,
            'ones_digit': 6,
            'ones_product': 42,
            'ones_result': 2,
            'carry': 4,
            'tens_product': 21,
            'tens_with_carry': 25,
            'tens_without_carry': 21,
            'correct_answer': 252,
            'malrule_answer': 212
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert correct_sol3.answer == '252'
    assert malrule_sol3.answer == '212'
    print("✓ TEST 3 PASSED")

    # Test case 4: 58 × 6 = 348, but student gets 308 (forgets carry of 4)
    problem4 = Problem(
        text="58 × 6 = ?",
        operands=[58, 6],
        operation='multiplication',
        level=4,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'multiplicand': 58,
            'multiplier': 6,
            'tens_digit': 5,
            'ones_digit': 8,
            'ones_product': 48,
            'ones_result': 8,
            'carry': 4,
            'tens_product': 30,
            'tens_with_carry': 34,
            'tens_without_carry': 30,
            'correct_answer': 348,
            'malrule_answer': 308
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    assert correct_sol4.answer == '348'
    assert malrule_sol4.answer == '308'
    print("✓ TEST 4 PASSED")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_automated_suite():
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = ForgetToAddCarriedNumberProblemGenerator(
        level=4,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = ForgetToAddCarriedNumberMalrule()
    correct = MultiDigitMultiplicationCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def test_all_templates():
    """Test all 10 templates to ensure they work correctly."""
    print("\n\n" + "="*70)
    print("TESTING ALL TEMPLATES")
    print("="*70)

    malrule = ForgetToAddCarriedNumberMalrule()
    correct = MultiDigitMultiplicationCorrectAlgorithm()
    templates = ['basic_two_digit_times_one', 'three_digit_times_one', 'two_digit_times_two',
                 'money_context', 'word_problem', 'three_digit_times_two', 'area_calculation',
                 'total_cost_bulk', 'distance_calculation', 'array_larger']

    for template in templates:
        print(f"\n--- Testing template: {template} ---")
        problem_gen = ForgetToAddCarriedNumberProblemGenerator(
            level=4,
            difficulty=DifficultyLevel.MEDIUM
        )
        problem = problem_gen.generate(seed=42, template=template)

        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        # Verify calculate_expected_answer matches malrule solution
        expected_answer = malrule.calculate_expected_answer(problem)
        assert str(expected_answer) == str(malrule_sol.answer), \
            f"Template {template}: calculate_expected_answer ({expected_answer}) != malrule solution ({malrule_sol.answer})"

        # Verify correct and malrule give different answers
        assert str(correct_sol.answer) != str(malrule_sol.answer), \
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

    malrule = ForgetToAddCarriedNumberMalrule()
    correct = MultiDigitMultiplicationCorrectAlgorithm()

    # Test 1: basic_two_digit_times_one
    print("\n--- Test 1: basic_two_digit_times_one ---")
    problem1 = Problem(
        text="34 × 5 = ?",
        operands=[34, 5],
        operation='multiplication',
        level=4,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'multiplicand': 34,
            'multiplier': 5,
            'tens_digit': 3,
            'ones_digit': 4,
            'ones_product': 20,
            'ones_result': 0,
            'carry': 2,
            'tens_product': 15,
            'tens_with_carry': 17,
            'tens_without_carry': 15,
            'correct_answer': '170',
            'malrule_answer': '150',
            'template': 'basic_two_digit_times_one'
        }
    )
    correct_sol1 = correct.solve(problem1)
    malrule_sol1 = malrule.solve(problem1)
    expected1 = malrule.calculate_expected_answer(problem1)

    assert correct_sol1.answer == '170'
    assert malrule_sol1.answer == '150'
    assert str(expected1) == str(malrule_sol1.answer)
    print(f"  34 × 5 → Correct: {correct_sol1.answer}, Malrule: {malrule_sol1.answer}")
    print("  ✓ PASSED")

    # Test 2: three_digit_times_one
    print("\n--- Test 2: three_digit_times_one ---")
    problem2 = Problem(
        text="Calculate: 123 × 4",
        operands=[123, 4],
        operation='multiplication',
        level=4,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'multiplicand': 123,
            'multiplier': 4,
            'hundreds_digit': 1,
            'tens_digit': 2,
            'ones_digit': 3,
            'ones_product': 12,
            'ones_result': 2,
            'carry_to_tens': 1,
            'tens_product': 8,
            'tens_with_carry': 9,
            'carry_to_hundreds': 0,
            'correct_answer': '492',
            'malrule_answer': '482',
            'template': 'three_digit_times_one'
        }
    )
    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    expected2 = malrule.calculate_expected_answer(problem2)

    assert correct_sol2.answer == '492'
    assert malrule_sol2.answer == '482'
    assert str(expected2) == str(malrule_sol2.answer)
    print(f"  123 × 4 → Correct: {correct_sol2.answer}, Malrule: {malrule_sol2.answer}")
    print("  ✓ PASSED")

    # Test 3: two_digit_times_two
    print("\n--- Test 3: two_digit_times_two ---")
    problem3 = Problem(
        text="Multiply: 23 × 14",
        operands=[23, 14],
        operation='multiplication',
        level=4,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'num1': 23,
            'num2': 14,
            'tens1': 2,
            'ones1': 3,
            'tens2': 1,
            'ones2': 4,
            'partial_product_1': 92,
            'partial_product_2': 23,
            'pp1_carry': 1,
            'correct_answer': '322',
            'malrule_answer': '312',
            'template': 'two_digit_times_two'
        }
    )
    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    expected3 = malrule.calculate_expected_answer(problem3)

    assert correct_sol3.answer == '322'
    assert malrule_sol3.answer == '312'
    assert str(expected3) == str(malrule_sol3.answer)
    print(f"  23 × 14 → Correct: {correct_sol3.answer}, Malrule: {malrule_sol3.answer}")
    print("  ✓ PASSED")

    # Test 4: three_digit_times_two
    print("\n--- Test 4: three_digit_times_two ---")
    problem_gen4 = ForgetToAddCarriedNumberProblemGenerator(
        level=5,
        difficulty=DifficultyLevel.MEDIUM
    )
    problem4 = problem_gen4.generate(seed=100, template='three_digit_times_two')
    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    expected4 = malrule.calculate_expected_answer(problem4)

    assert str(correct_sol4.answer) != str(malrule_sol4.answer)
    assert str(expected4) == str(malrule_sol4.answer)
    print(f"  {problem4.text} → Correct: {correct_sol4.answer}, Malrule: {malrule_sol4.answer}")
    print("  ✓ PASSED")

    # Test 5: area_calculation
    print("\n--- Test 5: area_calculation ---")
    problem_gen5 = ForgetToAddCarriedNumberProblemGenerator(
        level=4,
        difficulty=DifficultyLevel.MEDIUM
    )
    problem5 = problem_gen5.generate(seed=200, template='area_calculation')
    correct_sol5 = correct.solve(problem5)
    malrule_sol5 = malrule.solve(problem5)
    expected5 = malrule.calculate_expected_answer(problem5)

    assert str(correct_sol5.answer) != str(malrule_sol5.answer)
    assert str(expected5) == str(malrule_sol5.answer)
    print(f"  Correct: {correct_sol5.answer}, Malrule: {malrule_sol5.answer}")
    print("  ✓ PASSED")

    # Test 6: total_cost_bulk
    print("\n--- Test 6: total_cost_bulk ---")
    problem_gen6 = ForgetToAddCarriedNumberProblemGenerator(
        level=4,
        difficulty=DifficultyLevel.MEDIUM
    )
    problem6 = problem_gen6.generate(seed=300, template='total_cost_bulk')
    correct_sol6 = correct.solve(problem6)
    malrule_sol6 = malrule.solve(problem6)
    expected6 = malrule.calculate_expected_answer(problem6)

    assert str(correct_sol6.answer) != str(malrule_sol6.answer)
    assert str(expected6) == str(malrule_sol6.answer)
    print(f"  Correct: {correct_sol6.answer}, Malrule: {malrule_sol6.answer}")
    print("  ✓ PASSED")

    # Test 7: distance_calculation
    print("\n--- Test 7: distance_calculation ---")
    problem_gen7 = ForgetToAddCarriedNumberProblemGenerator(
        level=4,
        difficulty=DifficultyLevel.MEDIUM
    )
    problem7 = problem_gen7.generate(seed=400, template='distance_calculation')
    correct_sol7 = correct.solve(problem7)
    malrule_sol7 = malrule.solve(problem7)
    expected7 = malrule.calculate_expected_answer(problem7)

    assert str(correct_sol7.answer) != str(malrule_sol7.answer)
    assert str(expected7) == str(malrule_sol7.answer)
    print(f"  Correct: {correct_sol7.answer}, Malrule: {malrule_sol7.answer}")
    print("  ✓ PASSED")

    # Test 8: array_larger
    print("\n--- Test 8: array_larger ---")
    problem_gen8 = ForgetToAddCarriedNumberProblemGenerator(
        level=4,
        difficulty=DifficultyLevel.MEDIUM
    )
    problem8 = problem_gen8.generate(seed=500, template='array_larger')
    correct_sol8 = correct.solve(problem8)
    malrule_sol8 = malrule.solve(problem8)
    expected8 = malrule.calculate_expected_answer(problem8)

    assert str(correct_sol8.answer) != str(malrule_sol8.answer)
    assert str(expected8) == str(malrule_sol8.answer)
    print(f"  Correct: {correct_sol8.answer}, Malrule: {malrule_sol8.answer}")
    print("  ✓ PASSED")

    print("\n" + "="*70)
    print("ALL TEMPLATE-SPECIFIC TESTS PASSED ✓")
    print("="*70)


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Forget-To-Add-Carried-Number  ".center(70) + "║")
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
