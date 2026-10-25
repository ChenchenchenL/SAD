#!/usr/bin/env python3
"""Test script for Reverse-Percentage-Error malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.percentages.reverse_percentage_error import (
    ReversePercentageErrorProblemGenerator,
    ReversePercentageErrorMalrule,
    PercentageRelationshipCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING REVERSE-PERCENTAGE-ERROR")
    print("="*70)

    malrule = ReversePercentageErrorMalrule()
    correct = PercentageRelationshipCorrectAlgorithm()

    # Test case 1: 20 is 50% of 40, so 40 is 200% of 20
    problem1 = Problem(
        text="If 20 is 50% of 40, what percent is 40 of 20?",
        operands=[20, 40, 50],
        operation='percentage_relationship',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'num1': 20,
            'num2': 40,
            'percentage': 50,
            'correct_answer': 200,
            'malrule_answer': 50,
            'relationship': '20 is 50% of 40',
            'template': 'basic_reverse_relationship'
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: If 20 is 50% of 40 → Correct: {correct_sol.answer}%, Malrule: {malrule_sol.answer}%")
    assert correct_sol.answer == 200
    assert malrule_sol.answer == 50
    assert correct_sol.answer != malrule_sol.answer
    print("✓ PASSED")

    # Test case 2: 15 is 25% of 60, so 60 is 400% of 15
    problem2 = Problem(
        text="If 15 is 25% of 60, what percent is 60 of 15?",
        operands=[15, 60, 25],
        operation='percentage_relationship',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'num1': 15,
            'num2': 60,
            'percentage': 25,
            'correct_answer': 400,
            'malrule_answer': 25,
            'relationship': '15 is 25% of 60',
            'template': 'basic_reverse_relationship'
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert correct_sol2.answer == 400
    assert malrule_sol2.answer == 25
    print("✓ TEST 2 PASSED")

    # Test case 3: 30 is 75% of 40, so 40 is 133% of 30
    problem3 = Problem(
        text="If 30 is 75% of 40, what percent is 40 of 30?",
        operands=[30, 40, 75],
        operation='percentage_relationship',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'num1': 30,
            'num2': 40,
            'percentage': 75,
            'correct_answer': 133,  # rounded from 133.33
            'malrule_answer': 75,
            'relationship': '30 is 75% of 40',
            'template': 'basic_reverse_relationship'
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert correct_sol3.answer == 133
    assert malrule_sol3.answer == 75
    print("✓ TEST 3 PASSED")

    # Test case 4: 40 is 80% of 50, so 50 is 125% of 40
    problem4 = Problem(
        text="If 40 is 80% of 50, what percent is 50 of 40?",
        operands=[40, 50, 80],
        operation='percentage_relationship',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'num1': 40,
            'num2': 50,
            'percentage': 80,
            'correct_answer': 125,
            'malrule_answer': 80,
            'relationship': '40 is 80% of 50',
            'template': 'basic_reverse_relationship'
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    assert correct_sol4.answer == 125
    assert malrule_sol4.answer == 80
    print("✓ TEST 4 PASSED")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_all_templates():
    """Test all 5 templates to ensure they work correctly."""
    print("\n\n" + "="*70)
    print("TESTING ALL TEMPLATES")
    print("="*70)

    malrule = ReversePercentageErrorMalrule()
    correct = PercentageRelationshipCorrectAlgorithm()
    templates = ['basic_reverse_relationship', 'percentage_increase', 'percentage_decrease', 'comparison_statements', 'word_problem']

    for template in templates:
        print(f"\n--- Testing template: {template} ---")
        problem_gen = ReversePercentageErrorProblemGenerator(level=8, difficulty=DifficultyLevel.MEDIUM)
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

        print(f"  Problem: {problem.text[:80]}...")
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

    malrule = ReversePercentageErrorMalrule()
    correct = PercentageRelationshipCorrectAlgorithm()

    # Test 1: basic_reverse_relationship template
    print("\n--- Test 1: basic_reverse_relationship ---")
    problem1 = Problem(
        text="If 25 is 50% of 50, what percent is 50 of 25?",
        operands=[25, 50, 50],
        operation='percentage_relationship',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'num1': 25,
            'num2': 50,
            'percentage': 50,
            'correct_answer': 200,
            'malrule_answer': 50,
            'relationship': '25 is 50% of 50',
            'template': 'basic_reverse_relationship'
        }
    )
    correct_sol1 = correct.solve(problem1)
    malrule_sol1 = malrule.solve(problem1)
    expected1 = malrule.calculate_expected_answer(problem1)

    assert correct_sol1.answer == 200
    assert malrule_sol1.answer == 50
    assert expected1 == malrule_sol1.answer
    assert correct_sol1.answer != malrule_sol1.answer
    print(f"  If 25 is 50% of 50 → Correct: {correct_sol1.answer}%, Malrule: {malrule_sol1.answer}%")
    print("  ✓ PASSED")

    # Test 2: percentage_increase template
    print("\n--- Test 2: percentage_increase ---")
    problem2 = Problem(
        text="A value increased from 100 to 150, which is a 50% increase. If the value decreases from 150 back to 100, what is the percent decrease?",
        operands=[100, 150, 50],
        operation='percentage_relationship',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'original': 100,
            'new_value': 150,
            'increase_pct': 50,
            'correct_answer': 33.3,
            'malrule_answer': 50,
            'template': 'percentage_increase'
        }
    )
    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    expected2 = malrule.calculate_expected_answer(problem2)

    assert correct_sol2.answer == 33.3
    assert malrule_sol2.answer == 50
    assert expected2 == malrule_sol2.answer
    assert correct_sol2.answer != malrule_sol2.answer
    print(f"  50% increase → Correct decrease: {correct_sol2.answer}%, Malrule: {malrule_sol2.answer}%")
    print("  ✓ PASSED")

    # Test 3: percentage_decrease template
    print("\n--- Test 3: percentage_decrease ---")
    problem3 = Problem(
        text="A value decreased from 100 to 75, which is a 25% decrease. If the value increases from 75 back to 100, what is the percent increase?",
        operands=[100, 75, 25],
        operation='percentage_relationship',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'original': 100,
            'new_value': 75,
            'decrease_pct': 25,
            'correct_answer': 33.3,
            'malrule_answer': 25,
            'template': 'percentage_decrease'
        }
    )
    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    expected3 = malrule.calculate_expected_answer(problem3)

    assert correct_sol3.answer == 33.3
    assert malrule_sol3.answer == 25
    assert expected3 == malrule_sol3.answer
    assert correct_sol3.answer != malrule_sol3.answer
    print(f"  25% decrease → Correct increase: {correct_sol3.answer}%, Malrule: {malrule_sol3.answer}%")
    print("  ✓ PASSED")

    # Test 4: comparison_statements template
    print("\n--- Test 4: comparison_statements ---")
    problem4 = Problem(
        text="Tom has 25% as much money as Sarah. What percent of Tom's money does Sarah have?",
        operands=[25],
        operation='percentage_relationship',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'percentage': 25,
            'person1': 'Tom',
            'person2': 'Sarah',
            'item': 'money',
            'correct_answer': 400.0,
            'malrule_answer': 25,
            'template': 'comparison_statements'
        }
    )
    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    expected4 = malrule.calculate_expected_answer(problem4)

    assert correct_sol4.answer == 400.0
    assert malrule_sol4.answer == 25
    assert expected4 == malrule_sol4.answer
    assert correct_sol4.answer != malrule_sol4.answer
    print(f"  Tom has 25% of Sarah's → Sarah has {correct_sol4.answer}% of Tom's (Malrule: {malrule_sol4.answer}%)")
    print("  ✓ PASSED")

    print("\n" + "="*70)
    print("ALL TEMPLATE-SPECIFIC TESTS PASSED ✓")
    print("="*70)


def test_automated_suite():
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = ReversePercentageErrorProblemGenerator(
        level=8,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = ReversePercentageErrorMalrule()
    correct = PercentageRelationshipCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Reverse-Percentage-Error  ".center(70) + "║")
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
