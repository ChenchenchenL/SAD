#!/usr/bin/env python3
"""Test script for Distribute-Exponent-Over-Addition malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.exponents.distribute_exponent_over_addition import (
    DistributeExponentOverAdditionProblemGenerator,
    DistributeExponentOverAdditionMalrule,
    ExponentOverSumCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING DISTRIBUTE-EXPONENT-OVER-ADDITION")
    print("="*70)

    malrule = DistributeExponentOverAdditionMalrule()
    correct = ExponentOverSumCorrectAlgorithm()

    # Test case 1: (2+3)² = 25 (correct), 13 (malrule: 2² + 3²)
    problem1 = Problem(
        text="Evaluate: (2 + 3)^2",
        operands=[2, 3, 2],
        operation='exponent_over_sum',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'a': 2,
            'b': 3,
            'exponent': 2,
            'sum_value': 5,
            'correct_answer': 25,
            'malrule_answer': 13
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: (2+3)² → Correct: {correct_sol.answer}, Malrule: {malrule_sol.answer}")
    assert correct_sol.answer == 25
    assert malrule_sol.answer == 13
    assert correct_sol.answer != malrule_sol.answer
    print("✓ PASSED")

    # Test case 2: (1+1)² = 4 (correct), 2 (malrule: 1² + 1²)
    # Classic counterexample!
    problem2 = Problem(
        text="Evaluate: (1 + 1)^2",
        operands=[1, 1, 2],
        operation='exponent_over_sum',
        level=7,
        difficulty=DifficultyLevel.EASY,
        metadata={
            'a': 1,
            'b': 1,
            'exponent': 2,
            'sum_value': 2,
            'correct_answer': 4,
            'malrule_answer': 2
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert correct_sol2.answer == 4
    assert malrule_sol2.answer == 2
    print("✓ TEST 2 PASSED")

    # Test case 3: (3+4)² = 49 (correct), 25 (malrule: 3² + 4²)
    # Pythagorean triple confusion
    problem3 = Problem(
        text="Evaluate: (3 + 4)^2",
        operands=[3, 4, 2],
        operation='exponent_over_sum',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'a': 3,
            'b': 4,
            'exponent': 2,
            'sum_value': 7,
            'correct_answer': 49,
            'malrule_answer': 25
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert correct_sol3.answer == 49
    assert malrule_sol3.answer == 25
    print("✓ TEST 3 PASSED")

    # Test case 4: (2+4)³ = 216 (correct), 72 (malrule: 2³ + 4³)
    problem4 = Problem(
        text="Evaluate: (2 + 4)^3",
        operands=[2, 4, 3],
        operation='exponent_over_sum',
        level=9,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'a': 2,
            'b': 4,
            'exponent': 3,
            'sum_value': 6,
            'correct_answer': 216,
            'malrule_answer': 72
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    assert correct_sol4.answer == 216
    assert malrule_sol4.answer == 72
    print("✓ TEST 4 PASSED")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_new_problem_templates():
    """Test new problem template types added for enhancement."""
    print("\n\n" + "="*70)
    print("TESTING NEW PROBLEM TEMPLATES")
    print("="*70)

    malrule = DistributeExponentOverAdditionMalrule()
    correct = ExponentOverSumCorrectAlgorithm()

    # TEST CASE 5: Three-term square (1+2+3)^2
    print("\n\nTEST CASE 5: Three-term square ((1+2+3)^2)")
    print("-"*70)

    problem5 = Problem(
        text="Evaluate: (1 + 2 + 3)^2",
        operands=[1, 2, 2],
        operation='exponent_over_sum',
        level=9,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'a': 1,
            'b': 2,
            'c': 3,
            'exponent': 2,
            'sum_value': 6,
            'correct_answer': 36,
            'malrule_answer': 14,
            'problem_type': 'three_term_square'
        }
    )

    correct_sol5 = correct.solve(problem5)
    malrule_sol5 = malrule.solve(problem5)

    print(f"Problem: {problem5.text}")
    print(f"Correct answer: {correct_sol5.answer}")
    print(f"Malrule answer: {malrule_sol5.answer}")

    # Correct: (1+2+3)^2 = 6^2 = 36
    # Malrule: 1^2 + 2^2 + 3^2 = 1 + 4 + 9 = 14
    assert correct_sol5.answer == 36, f"Expected 36, got {correct_sol5.answer}"
    assert malrule_sol5.answer == 14, f"Expected 14 (malrule), got {malrule_sol5.answer}"

    print("✓ TEST CASE 5 PASSED: Three-term square template works")

    # TEST CASE 6: Higher power (2+3)^4
    print("\n\nTEST CASE 6: Higher power ((2+3)^4)")
    print("-"*70)

    problem6 = Problem(
        text="Evaluate: (2 + 3)^4",
        operands=[2, 3, 4],
        operation='exponent_over_sum',
        level=9,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'a': 2,
            'b': 3,
            'exponent': 4,
            'sum_value': 5,
            'correct_answer': 625,
            'malrule_answer': 97,
            'problem_type': 'higher_power'
        }
    )

    correct_sol6 = correct.solve(problem6)
    malrule_sol6 = malrule.solve(problem6)

    print(f"Problem: {problem6.text}")
    print(f"Correct answer: {correct_sol6.answer}")
    print(f"Malrule answer: {malrule_sol6.answer}")

    # Correct: (2+3)^4 = 5^4 = 625
    # Malrule: 2^4 + 3^4 = 16 + 81 = 97
    assert correct_sol6.answer == 625, f"Expected 625, got {correct_sol6.answer}"
    assert malrule_sol6.answer == 97, f"Expected 97 (malrule), got {malrule_sol6.answer}"

    print("✓ TEST CASE 6 PASSED: Higher power template works")

    # TEST CASE 7: Pythagorean confusion context (3+4)^2
    print("\n\nTEST CASE 7: Pythagorean confusion context ((3+4)^2)")
    print("-"*70)

    problem7 = Problem(
        text="Calculate (length₁ + length₂)² where length₁ = 3 and length₂ = 4. What is (3 + 4)²?",
        operands=[3, 4, 2],
        operation='exponent_over_sum',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'a': 3,
            'b': 4,
            'exponent': 2,
            'sum_value': 7,
            'correct_answer': 49,
            'malrule_answer': 25,
            'problem_type': 'word_problem_pythagorean'
        }
    )

    correct_sol7 = correct.solve(problem7)
    malrule_sol7 = malrule.solve(problem7)

    print(f"Problem: {problem7.text}")
    print(f"Correct answer: {correct_sol7.answer}")
    print(f"Malrule answer: {malrule_sol7.answer}")

    # Correct: (3+4)^2 = 7^2 = 49
    # Malrule: 3^2 + 4^2 = 9 + 16 = 25 (confuses with Pythagorean theorem!)
    assert correct_sol7.answer == 49, f"Expected 49, got {correct_sol7.answer}"
    assert malrule_sol7.answer == 25, f"Expected 25 (malrule), got {malrule_sol7.answer}"

    print("✓ TEST CASE 7 PASSED: Pythagorean confusion template works")

    # TEST CASE 8: Area word problem (5+3)^2
    print("\n\nTEST CASE 8: Area context ((5+3)^2)")
    print("-"*70)

    problem8 = Problem(
        text="A square has side length (5 + 3) cm. What is its area? Evaluate: (5 + 3)²",
        operands=[5, 3, 2],
        operation='exponent_over_sum',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'a': 5,
            'b': 3,
            'exponent': 2,
            'sum_value': 8,
            'correct_answer': 64,
            'malrule_answer': 34,
            'problem_type': 'word_problem_area'
        }
    )

    correct_sol8 = correct.solve(problem8)
    malrule_sol8 = malrule.solve(problem8)

    print(f"Problem: {problem8.text}")
    print(f"Correct answer: {correct_sol8.answer}")
    print(f"Malrule answer: {malrule_sol8.answer}")

    # Correct: (5+3)^2 = 8^2 = 64
    # Malrule: 5^2 + 3^2 = 25 + 9 = 34
    assert correct_sol8.answer == 64, f"Expected 64, got {correct_sol8.answer}"
    assert malrule_sol8.answer == 34, f"Expected 34 (malrule), got {malrule_sol8.answer}"

    print("✓ TEST CASE 8 PASSED: Area word problem template works")

    print("\n" + "="*70)
    print("ALL NEW TEMPLATE TEST CASES PASSED ✓")
    print("="*70)


def test_template_generation():
    """Test that all template types can be generated."""
    print("\n\n" + "="*70)
    print("TESTING TEMPLATE GENERATION")
    print("="*70)

    problem_gen = DistributeExponentOverAdditionProblemGenerator(
        level=9,
        difficulty=DifficultyLevel.MEDIUM
    )

    # Generate multiple problems to cover all template types
    templates_found = set()
    for i in range(50):
        problem = problem_gen.generate(seed=10000 + i)
        if 'problem_type' in problem.metadata:
            templates_found.add(problem.metadata['problem_type'])

    print(f"\nTemplates generated: {sorted(templates_found)}")

    # Verify we have all expected templates
    expected_templates = {
        'simple_two_term',
        'three_term_square',
        'higher_power',
        'word_problem_pythagorean',
        'word_problem_area',
        'word_problem_context',  # NEW: Comprehensive word problems
    }
    assert templates_found >= expected_templates, \
        f"Missing templates: {expected_templates - templates_found}"

    print("\n✓ ALL TEMPLATE TYPES GENERATED SUCCESSFULLY")
    print("="*70)


def test_automated_suite():
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = DistributeExponentOverAdditionProblemGenerator(
        level=8,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = DistributeExponentOverAdditionMalrule()
    correct = ExponentOverSumCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Distribute-Exponent-Over-Addition  ".center(70) + "║")
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
