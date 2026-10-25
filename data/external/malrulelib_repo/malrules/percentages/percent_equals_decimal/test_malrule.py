#!/usr/bin/env python3
"""Test script for Percent-Equals-Decimal malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.percentages.percent_equals_decimal import (
    PercentEqualsDecimalProblemGenerator,
    PercentEqualsDecimalMalrule,
    PercentageConversionCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING PERCENT-EQUALS-DECIMAL")
    print("="*70)

    malrule = PercentEqualsDecimalMalrule()
    correct = PercentageConversionCorrectAlgorithm()

    # Test case 1: 25% to decimal = 0.25 (correct), 25 (malrule)
    problem1 = Problem(
        text="Convert 25% to a decimal",
        operands=[25],
        operation='percentage_conversion',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'conversion_type': 'percent_to_decimal',
            'percent': 25,
            'decimal': 0.25,
            'correct_answer': 0.25,
            'malrule_answer': 25
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: 25% to decimal → Correct: {correct_sol.answer}, Malrule: {malrule_sol.answer}")
    assert correct_sol.answer == 0.25
    assert malrule_sol.answer == 25
    assert correct_sol.answer != malrule_sol.answer
    print("✓ PASSED")

    # Test case 2: 0.30 to percent = 30% (correct), 0.30% (malrule)
    problem2 = Problem(
        text="Convert 0.3 to a percentage",
        operands=[0.3],
        operation='percentage_conversion',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'conversion_type': 'decimal_to_percent',
            'percent': 30,
            'decimal': 0.3,
            'correct_answer': 30,
            'malrule_answer': 0.3
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert correct_sol2.answer == 30
    assert malrule_sol2.answer == 0.3
    print("✓ TEST 2 PASSED")

    # Test case 3: 50% to decimal = 0.50 (correct), 50 (malrule)
    problem3 = Problem(
        text="Convert 50% to a decimal",
        operands=[50],
        operation='percentage_conversion',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'conversion_type': 'percent_to_decimal',
            'percent': 50,
            'decimal': 0.5,
            'correct_answer': 0.5,
            'malrule_answer': 50
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert correct_sol3.answer == 0.5
    assert malrule_sol3.answer == 50
    print("✓ TEST 3 PASSED")

    # Test case 4: 0.75 to percent = 75% (correct), 0.75% (malrule)
    problem4 = Problem(
        text="Convert 0.75 to a percentage",
        operands=[0.75],
        operation='percentage_conversion',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'conversion_type': 'decimal_to_percent',
            'percent': 75,
            'decimal': 0.75,
            'correct_answer': 75,
            'malrule_answer': 0.75
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    assert correct_sol4.answer == 75
    assert malrule_sol4.answer == 0.75
    print("✓ TEST 4 PASSED")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_all_templates():
    """Test all 5 templates to ensure they work correctly."""
    print("\n\n" + "="*70)
    print("TESTING ALL TEMPLATES")
    print("="*70)

    malrule = PercentEqualsDecimalMalrule()
    correct = PercentageConversionCorrectAlgorithm()
    templates = ['percent_to_decimal', 'decimal_to_percent', 'percent_in_calculation', 'fraction_to_percent', 'word_problem']

    for template in templates:
        print(f"\n--- Testing template: {template} ---")
        problem_gen = PercentEqualsDecimalProblemGenerator(level=6, difficulty=DifficultyLevel.MEDIUM)
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

    malrule = PercentEqualsDecimalMalrule()
    correct = PercentageConversionCorrectAlgorithm()

    # Test 1: percent_to_decimal template
    print("\n--- Test 1: percent_to_decimal ---")
    problem1 = Problem(
        text="Convert 40% to a decimal",
        operands=[40],
        operation='percentage_conversion',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'conversion_type': 'percent_to_decimal',
            'percent': 40,
            'decimal': 0.4,
            'correct_answer': 0.4,
            'malrule_answer': 40,
            'template': 'percent_to_decimal'
        }
    )
    correct_sol1 = correct.solve(problem1)
    malrule_sol1 = malrule.solve(problem1)
    expected1 = malrule.calculate_expected_answer(problem1)

    assert correct_sol1.answer == 0.4
    assert malrule_sol1.answer == 40
    assert expected1 == malrule_sol1.answer
    assert correct_sol1.answer != malrule_sol1.answer
    print(f"  40% → Correct: {correct_sol1.answer}, Malrule: {malrule_sol1.answer}")
    print("  ✓ PASSED")

    # Test 2: decimal_to_percent template
    print("\n--- Test 2: decimal_to_percent ---")
    problem2 = Problem(
        text="Convert 0.6 to a percentage",
        operands=[0.6],
        operation='percentage_conversion',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'conversion_type': 'decimal_to_percent',
            'percent': 60,
            'decimal': 0.6,
            'correct_answer': 60,
            'malrule_answer': 0.6,
            'template': 'decimal_to_percent'
        }
    )
    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    expected2 = malrule.calculate_expected_answer(problem2)

    assert correct_sol2.answer == 60
    assert malrule_sol2.answer == 0.6
    assert expected2 == malrule_sol2.answer
    assert correct_sol2.answer != malrule_sol2.answer
    print(f"  0.6 → Correct: {correct_sol2.answer}%, Malrule: {malrule_sol2.answer}%")
    print("  ✓ PASSED")

    # Test 3: percent_in_calculation template
    print("\n--- Test 3: percent_in_calculation ---")
    problem3 = Problem(
        text="Calculate 25% of 80",
        operands=[25, 80],
        operation='percentage_calculation',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'conversion_type': 'percent_in_calculation',
            'percent': 25,
            'value': 80,
            'decimal': 0.25,
            'correct_answer': 20,
            'malrule_answer': 2000,
            'template': 'percent_in_calculation'
        }
    )
    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    expected3 = malrule.calculate_expected_answer(problem3)

    assert correct_sol3.answer == 20
    assert malrule_sol3.answer == 2000
    assert expected3 == malrule_sol3.answer
    assert correct_sol3.answer != malrule_sol3.answer
    print(f"  25% of 80 → Correct: {correct_sol3.answer}, Malrule: {malrule_sol3.answer}")
    print("  ✓ PASSED")

    # Test 4: fraction_to_percent template
    print("\n--- Test 4: fraction_to_percent ---")
    problem4 = Problem(
        text="Convert 3/4 to a percentage",
        operands=[3, 4],
        operation='percentage_conversion',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'conversion_type': 'fraction_to_percent',
            'numerator': 3,
            'denominator': 4,
            'fraction': '3/4',
            'decimal': 0.75,
            'percent': 75,
            'correct_answer': 75,
            'malrule_answer': 0.75,
            'template': 'fraction_to_percent'
        }
    )
    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    expected4 = malrule.calculate_expected_answer(problem4)

    assert correct_sol4.answer == 75
    assert malrule_sol4.answer == 0.75
    assert expected4 == malrule_sol4.answer
    assert correct_sol4.answer != malrule_sol4.answer
    print(f"  3/4 → Correct: {correct_sol4.answer}%, Malrule: {malrule_sol4.answer}%")
    print("  ✓ PASSED")

    print("\n" + "="*70)
    print("ALL TEMPLATE-SPECIFIC TESTS PASSED ✓")
    print("="*70)


def test_automated_suite():
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = PercentEqualsDecimalProblemGenerator(
        level=6,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = PercentEqualsDecimalMalrule()
    correct = PercentageConversionCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Percent-Equals-Decimal  ".center(70) + "║")
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
