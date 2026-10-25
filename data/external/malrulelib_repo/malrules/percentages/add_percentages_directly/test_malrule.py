#!/usr/bin/env python3
"""
Test script for Add-Percentages-Directly malrule.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.percentages.add_percentages_directly import (
    AddPercentagesProblemGenerator,
    AddPercentagesDirectlyMalrule,
    PercentageCorrectAlgorithm
)


def test_specific_examples():
    """Test with specific examples."""
    print("="*70)
    print("TESTING ADD-PERCENTAGES-DIRECTLY WITH SPECIFIC EXAMPLES")
    print("="*70)

    malrule = AddPercentagesDirectlyMalrule()
    correct = PercentageCorrectAlgorithm()

    # Test case 1: $100 → +20% → -20% (Classic "cancel out" case)
    print("\nTEST CASE 1: $100 → +20% → -20% (Classic 'cancel out' misconception)")
    print("-"*70)

    problem1 = Problem(
        text="A $100 item is increased by 20%, then decreased by 20%. What is the final price?",
        operands=[100, 20, 20],
        operation='percentage_sequential',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'initial_value': 100,
            'percentage1': 20,
            'percentage2': 20,
            'problem_type': 'increase_then_decrease',
            'operation_desc': '+20% then -20%',
            'correct_answer': 96.0,
            'after_first_change': 120.0
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"Problem: {problem1.text}")
    print(f"Correct answer: ${correct_sol.answer}")
    print(f"Malrule answer: ${malrule_sol.answer}")

    # Expected: $96 is correct, but malrule gives $100
    assert correct_sol.answer == 96.0, f"Expected 96.0, got {correct_sol.answer}"
    assert malrule_sol.answer == 100.0, f"Expected 100.0 (malrule), got {malrule_sol.answer}"
    assert correct_sol.answer != malrule_sol.answer, "Malrule should produce different answer"

    print("\n--- Correct Steps ---")
    for step in correct_sol.steps:
        print(f"  {step}")

    print("\n--- Malrule Steps ---")
    for step in malrule_sol.steps:
        print(f"  {step}")

    print("✓ TEST CASE 1 PASSED: $100 → +20% → -20%, correct=$96, malrule=$100")

    # Test case 2: 200 → +25% → +25%
    print("\n\nTEST CASE 2: 200 → +25% → +25% (Two increases)")
    print("-"*70)

    problem2 = Problem(
        text="A population of 200 increases by 25%, then increases again by 25%. What is the final population?",
        operands=[200, 25, 25],
        operation='percentage_sequential',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'initial_value': 200,
            'percentage1': 25,
            'percentage2': 25,
            'problem_type': 'two_increases',
            'operation_desc': '+25% then +25%',
            'correct_answer': 312.5,
            'after_first_change': 250.0
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)

    print(f"Problem: {problem2.text}")
    print(f"Correct answer: {correct_sol2.answer}")
    print(f"Malrule answer: {malrule_sol2.answer}")

    # Expected: 312.5 is correct, but malrule gives 300
    assert correct_sol2.answer == 312.5, f"Expected 312.5, got {correct_sol2.answer}"
    assert malrule_sol2.answer == 300.0, f"Expected 300.0 (malrule), got {malrule_sol2.answer}"

    print("✓ TEST CASE 2 PASSED: 200 → +25% → +25%, correct=312.5, malrule=300")

    # Test case 3: $500 → -30% → +30%
    print("\n\nTEST CASE 3: $500 → -30% → +30% (Reverse 'cancel')")
    print("-"*70)

    problem3 = Problem(
        text="A $500 item is decreased by 30%, then increased by 30%. What is the final price?",
        operands=[500, 30, 30],
        operation='percentage_sequential',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'initial_value': 500,
            'percentage1': 30,
            'percentage2': 30,
            'problem_type': 'decrease_then_increase',
            'operation_desc': '-30% then +30%',
            'correct_answer': 455.0,
            'after_first_change': 350.0
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)

    print(f"Problem: {problem3.text}")
    print(f"Correct answer: ${correct_sol3.answer}")
    print(f"Malrule answer: ${malrule_sol3.answer}")

    # Expected: $455 is correct, but malrule gives $500
    assert correct_sol3.answer == 455.0, f"Expected 455.0, got {correct_sol3.answer}"
    assert malrule_sol3.answer == 500.0, f"Expected 500.0 (malrule), got {malrule_sol3.answer}"

    print("✓ TEST CASE 3 PASSED: $500 → -30% → +30%, correct=$455, malrule=$500")

    # Test case 4: 1000 → -10% → -20%
    print("\n\nTEST CASE 4: 1000 → -10% → -20% (Two decreases)")
    print("-"*70)

    problem4 = Problem(
        text="A value of 1000 decreases by 10%, then decreases again by 20%. What is the final value?",
        operands=[1000, 10, 20],
        operation='percentage_sequential',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'initial_value': 1000,
            'percentage1': 10,
            'percentage2': 20,
            'problem_type': 'two_decreases',
            'operation_desc': '-10% then -20%',
            'correct_answer': 720.0,
            'after_first_change': 900.0
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)

    print(f"Problem: {problem4.text}")
    print(f"Correct answer: {correct_sol4.answer}")
    print(f"Malrule answer: {malrule_sol4.answer}")

    # Expected: 720 is correct, but malrule gives 700
    assert correct_sol4.answer == 720.0, f"Expected 720.0, got {correct_sol4.answer}"
    assert malrule_sol4.answer == 700.0, f"Expected 700.0 (malrule), got {malrule_sol4.answer}"

    print("✓ TEST CASE 4 PASSED: 1000 → -10% → -20%, correct=720, malrule=700")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_new_problem_templates():
    """Test new problem template types added for enhancement."""
    print("\n\n" + "="*70)
    print("TESTING NEW PROBLEM TEMPLATES")
    print("="*70)

    malrule = AddPercentagesDirectlyMalrule()
    correct = PercentageCorrectAlgorithm()

    # TEST CASE 5: Three sequential changes ($100 → +20% → -10% → +15%)
    print("\n\nTEST CASE 5: Three sequential changes ($100 → +20% → -10% → +15%)")
    print("-"*70)

    problem5 = Problem(
        text="A stock price of $100 increases by 20%, then decreases by 10%, then increases by 15%. What is the final stock price?",
        operands=[100, 20, 10, 15],
        operation='percentage_sequential',
        level=8,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'initial_value': 100,
            'percentage1': 20,
            'percentage2': 10,
            'percentage3': 15,
            'problem_type': 'three_sequential_changes',
            'operation_desc': '+20% then -10% then +15%',
            'correct_answer': 124.2,
            'after_first_change': 120.0,
            'after_second_change': 108.0
        }
    )

    correct_sol5 = correct.solve(problem5)
    malrule_sol5 = malrule.solve(problem5)

    print(f"Problem: {problem5.text}")
    print(f"Correct answer: ${correct_sol5.answer}")
    print(f"Malrule answer: ${malrule_sol5.answer}")

    # Correct: 100 → 120 → 108 → 124.2
    # Malrule: +20% - 10% + 15% = +25%, so 100 * 1.25 = 125
    assert abs(correct_sol5.answer - 124.2) < 0.01, f"Expected ~124.2, got {correct_sol5.answer}"
    assert abs(malrule_sol5.answer - 125.0) < 0.01, f"Expected ~125.0 (malrule), got {malrule_sol5.answer}"

    print("✓ TEST CASE 5 PASSED: Three sequential changes template works")

    # TEST CASE 6: Percentage of percentage (discount on discount)
    print("\n\nTEST CASE 6: Percentage of percentage ($200, 20% off, then 10% off sale price)")
    print("-"*70)

    problem6 = Problem(
        text="A store offers 20% off all items, then gives an additional 10% off the sale price. If an item originally costs $200, what is the final price?",
        operands=[200, 20, 10],
        operation='percentage_sequential',
        level=7,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'initial_value': 200,
            'percentage1': 20,
            'percentage2': 10,
            'problem_type': 'percentage_of_percentage',
            'operation_desc': '-20% off, then -10% off sale price',
            'correct_answer': 144.0,
            'after_first_change': 160.0
        }
    )

    correct_sol6 = correct.solve(problem6)
    malrule_sol6 = malrule.solve(problem6)

    print(f"Problem: {problem6.text}")
    print(f"Correct answer: ${correct_sol6.answer}")
    print(f"Malrule answer: ${malrule_sol6.answer}")

    # Correct: 200 * 0.8 * 0.9 = 144
    # Malrule: -20% - 10% = -30%, so 200 * 0.7 = 140
    assert correct_sol6.answer == 144.0, f"Expected 144.0, got {correct_sol6.answer}"
    assert malrule_sol6.answer == 140.0, f"Expected 140.0 (malrule), got {malrule_sol6.answer}"

    print("✓ TEST CASE 6 PASSED: Percentage of percentage template works")

    # TEST CASE 7: Reverse percentage
    print("\n\nTEST CASE 7: Reverse percentage (final $120 after 20% increase)")
    print("-"*70)

    problem7 = Problem(
        text="After a 20% increase, a price is now $120. What was the original price?",
        operands=[120, 20],
        operation='percentage_reverse',
        level=8,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'final_value': 120,
            'percentage1': 20,
            'problem_type': 'reverse_percentage',
            'operation_desc': 'reverse +20%',
            'correct_answer': 100.0
        }
    )

    correct_sol7 = correct.solve(problem7)
    malrule_sol7 = malrule.solve(problem7)

    print(f"Problem: {problem7.text}")
    print(f"Correct answer: ${correct_sol7.answer}")
    print(f"Malrule answer: ${malrule_sol7.answer}")

    # Correct: 120 / 1.2 = 100
    # Malrule: 120 * 0.8 = 96 (incorrectly subtracts percentage)
    assert correct_sol7.answer == 100.0, f"Expected 100.0, got {correct_sol7.answer}"
    assert malrule_sol7.answer == 96.0, f"Expected 96.0 (malrule), got {malrule_sol7.answer}"

    print("✓ TEST CASE 7 PASSED: Reverse percentage template works")

    # TEST CASE 8: Word problem context
    print("\n\nTEST CASE 8: Word problem context (investment scenario)")
    print("-"*70)

    problem8 = Problem(
        text="Tom invested $500 in a stock. The stock price rose 30% in Year 1, then fell 20% in Year 2. What is Tom's investment worth now?",
        operands=[500, 30, 20],
        operation='percentage_sequential',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'initial_value': 500,
            'percentage1': 30,
            'percentage2': 20,
            'problem_type': 'word_problem_context',
            'operation_desc': '+30% then -20%',
            'correct_answer': 520.0,
            'after_first_change': 650.0,
            'context_type': 'investment'
        }
    )

    correct_sol8 = correct.solve(problem8)
    malrule_sol8 = malrule.solve(problem8)

    print(f"Problem: {problem8.text}")
    print(f"Correct answer: ${correct_sol8.answer}")
    print(f"Malrule answer: ${malrule_sol8.answer}")

    # Correct: 500 * 1.3 * 0.8 = 520
    # Malrule: +30% - 20% = +10%, so 500 * 1.1 = 550
    assert correct_sol8.answer == 520.0, f"Expected 520.0, got {correct_sol8.answer}"
    assert malrule_sol8.answer == 550.0, f"Expected 550.0 (malrule), got {malrule_sol8.answer}"

    print("✓ TEST CASE 8 PASSED: Word problem context template works")

    print("\n" + "="*70)
    print("ALL NEW TEMPLATE TEST CASES PASSED ✓")
    print("="*70)


def test_template_generation():
    """Test that all template types can be generated."""
    print("\n\n" + "="*70)
    print("TESTING TEMPLATE GENERATION")
    print("="*70)

    problem_gen = AddPercentagesProblemGenerator(
        level=8,
        difficulty=DifficultyLevel.HARD
    )

    # Generate multiple problems to cover all template types
    templates_found = set()
    for i in range(100):
        problem = problem_gen.generate(seed=50000 + i)
        if 'problem_type' in problem.metadata:
            templates_found.add(problem.metadata['problem_type'])

    print(f"\nTemplates generated: {sorted(templates_found)}")

    # Verify we have all expected templates
    # Note: 'word_problem_context' is not included because it redirects to other problem_types
    # (like 'increase_then_decrease', 'two_increases', etc.) and sets a 'formula_type' instead
    expected_templates = {
        'increase_then_decrease',
        'decrease_then_increase',
        'two_increases',
        'two_decreases',
        'three_sequential_changes',
        'percentage_of_percentage',
        'reverse_percentage',
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

    problem_gen = AddPercentagesProblemGenerator(
        level=7,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = AddPercentagesDirectlyMalrule()
    correct = PercentageCorrectAlgorithm()

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
    print("║" + "  VERIFICATION TEST: Add-Percentages-Directly  ".center(70) + "║")
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
