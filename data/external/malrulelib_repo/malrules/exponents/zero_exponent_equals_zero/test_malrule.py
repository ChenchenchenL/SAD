#!/usr/bin/env python3
"""Test script for Zero-Exponent-Equals-Zero malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.exponents.zero_exponent_equals_zero import (
    ZeroExponentEqualsZeroProblemGenerator,
    ZeroExponentEqualsZeroMalrule,
    ZeroExponentCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING ZERO-EXPONENT-EQUALS-ZERO")
    print("="*70)

    malrule = ZeroExponentEqualsZeroMalrule()
    correct = ZeroExponentCorrectAlgorithm()

    # Test case 1: 2^0 = 1 (correct), 0 (malrule)
    problem1 = Problem(
        text="Evaluate: 2^0",
        operands=[2, 0],
        operation='zero_exponent',
        level=8,
        difficulty=DifficultyLevel.EASY,
        metadata={
            'base': 2,
            'exponent': 0,
            'correct_answer': 1,
            'malrule_answer': 0
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: 2^0 → Correct: {correct_sol.answer}, Malrule: {malrule_sol.answer}")
    assert correct_sol.answer == 1
    assert malrule_sol.answer == 0
    assert correct_sol.answer != malrule_sol.answer
    print("✓ PASSED")

    # Test case 2: 5^0 = 1 (correct), 0 (malrule)
    problem2 = Problem(
        text="Evaluate: 5^0",
        operands=[5, 0],
        operation='zero_exponent',
        level=8,
        difficulty=DifficultyLevel.EASY,
        metadata={
            'base': 5,
            'exponent': 0,
            'correct_answer': 1,
            'malrule_answer': 0
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert correct_sol2.answer == 1
    assert malrule_sol2.answer == 0
    print("✓ TEST 2 PASSED")

    # Test case 3: 10^0 = 1 (correct), 0 (malrule)
    problem3 = Problem(
        text="Evaluate: 10^0",
        operands=[10, 0],
        operation='zero_exponent',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'base': 10,
            'exponent': 0,
            'correct_answer': 1,
            'malrule_answer': 0
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert correct_sol3.answer == 1
    assert malrule_sol3.answer == 0
    print("✓ TEST 3 PASSED")

    # Test case 4: 100^0 = 1 (correct), 0 (malrule)
    problem4 = Problem(
        text="Evaluate: 100^0",
        operands=[100, 0],
        operation='zero_exponent',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'base': 100,
            'exponent': 0,
            'correct_answer': 1,
            'malrule_answer': 0
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    assert correct_sol4.answer == 1
    assert malrule_sol4.answer == 0
    print("✓ TEST 4 PASSED")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_all_templates():
    """Test all 5 templates to ensure they work correctly."""
    print("\n\n" + "="*70)
    print("TESTING ALL TEMPLATES")
    print("="*70)

    malrule = ZeroExponentEqualsZeroMalrule()
    correct = ZeroExponentCorrectAlgorithm()
    templates = ['basic_zero_exponent', 'expression_simplification', 'exponent_rules', 'polynomial_evaluation', 'word_problem', 'word_problem_context']

    for template in templates:
        print(f"\n--- Testing template: {template} ---")
        problem_gen = ZeroExponentEqualsZeroProblemGenerator(level=8, difficulty=DifficultyLevel.MEDIUM)
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

    malrule = ZeroExponentEqualsZeroMalrule()
    correct = ZeroExponentCorrectAlgorithm()

    # Test 1: basic_zero_exponent template
    print("\n--- Test 1: basic_zero_exponent ---")
    problem1 = Problem(
        text="Evaluate: 7^0",
        operands=[7, 0],
        operation='zero_exponent',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'base': 7,
            'exponent': 0,
            'correct_answer': 1,
            'malrule_answer': 0,
            'template': 'basic_zero_exponent'
        }
    )
    correct_sol1 = correct.solve(problem1)
    malrule_sol1 = malrule.solve(problem1)
    expected1 = malrule.calculate_expected_answer(problem1)

    assert correct_sol1.answer == 1
    assert malrule_sol1.answer == 0
    assert expected1 == malrule_sol1.answer
    assert correct_sol1.answer != malrule_sol1.answer
    print(f"  7^0 → Correct: {correct_sol1.answer}, Malrule: {malrule_sol1.answer}")
    print("  ✓ PASSED")

    # Test 2: expression_simplification template (coefficient_times)
    print("\n--- Test 2: expression_simplification (coefficient_times) ---")
    problem2 = Problem(
        text="Simplify: 5x^0",
        operands=[5, 0],
        operation='zero_exponent',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': 5,
            'variable': 'x',
            'expression_type': 'coefficient_times',
            'correct_answer': 5,
            'malrule_answer': 0,
            'template': 'expression_simplification'
        }
    )
    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    expected2 = malrule.calculate_expected_answer(problem2)

    assert correct_sol2.answer == 5
    assert malrule_sol2.answer == 0
    assert expected2 == malrule_sol2.answer
    assert correct_sol2.answer != malrule_sol2.answer
    print(f"  5x^0 → Correct: {correct_sol2.answer}, Malrule: {malrule_sol2.answer}")
    print("  ✓ PASSED")

    # Test 3: expression_simplification template (parentheses)
    print("\n--- Test 3: expression_simplification (parentheses) ---")
    problem3 = Problem(
        text="Simplify: (3y)^0",
        operands=[3, 0],
        operation='zero_exponent',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': 3,
            'variable': 'y',
            'expression_type': 'parentheses',
            'correct_answer': 1,
            'malrule_answer': 0,
            'template': 'expression_simplification'
        }
    )
    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    expected3 = malrule.calculate_expected_answer(problem3)

    assert correct_sol3.answer == 1
    assert malrule_sol3.answer == 0
    assert expected3 == malrule_sol3.answer
    assert correct_sol3.answer != malrule_sol3.answer
    print(f"  (3y)^0 → Correct: {correct_sol3.answer}, Malrule: {malrule_sol3.answer}")
    print("  ✓ PASSED")

    # Test 4: exponent_rules template
    print("\n--- Test 4: exponent_rules ---")
    problem4 = Problem(
        text="Simplify using exponent rules: x^4/x^4",
        operands=[4, 4],
        operation='zero_exponent',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'base': 'x',
            'power': 4,
            'is_variable': True,
            'correct_answer': 1,
            'malrule_answer': 0,
            'template': 'exponent_rules'
        }
    )
    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    expected4 = malrule.calculate_expected_answer(problem4)

    assert correct_sol4.answer == 1
    assert malrule_sol4.answer == 0
    assert expected4 == malrule_sol4.answer
    assert correct_sol4.answer != malrule_sol4.answer
    print(f"  x^4/x^4 → Correct: {correct_sol4.answer}, Malrule: {malrule_sol4.answer}")
    print("  ✓ PASSED")

    # Test 5: polynomial_evaluation template
    print("\n--- Test 5: polynomial_evaluation ---")
    problem5 = Problem(
        text="Evaluate 8x^0 when x = 5",
        operands=[8, 5, 0],
        operation='zero_exponent',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': 8,
            'variable': 'x',
            'x_value': 5,
            'correct_answer': 8,
            'malrule_answer': 0,
            'template': 'polynomial_evaluation'
        }
    )
    correct_sol5 = correct.solve(problem5)
    malrule_sol5 = malrule.solve(problem5)
    expected5 = malrule.calculate_expected_answer(problem5)

    assert correct_sol5.answer == 8
    assert malrule_sol5.answer == 0
    assert expected5 == malrule_sol5.answer
    assert correct_sol5.answer != malrule_sol5.answer
    print(f"  8x^0 when x=5 → Correct: {correct_sol5.answer}, Malrule: {malrule_sol5.answer}")
    print("  ✓ PASSED")

    # Test 6: word_problem template
    print("\n--- Test 6: word_problem ---")
    problem6 = Problem(
        text="A bacteria population multiplies by 3^n each hour, where n is the number of hours. What is the population multiplier after 0 hours?",
        operands=[3, 0],
        operation='zero_exponent',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'base': 3,
            'exponent': 0,
            'context_type': 'bacteria_growth',
            'correct_answer': 1,
            'malrule_answer': 0,
            'template': 'word_problem'
        }
    )
    correct_sol6 = correct.solve(problem6)
    malrule_sol6 = malrule.solve(problem6)
    expected6 = malrule.calculate_expected_answer(problem6)

    assert correct_sol6.answer == 1
    assert malrule_sol6.answer == 0
    assert expected6 == malrule_sol6.answer
    assert correct_sol6.answer != malrule_sol6.answer
    print(f"  Bacteria growth (3^0) → Correct: {correct_sol6.answer}, Malrule: {malrule_sol6.answer}")
    print("  ✓ PASSED")

    print("\n" + "="*70)
    print("ALL TEMPLATE-SPECIFIC TESTS PASSED ✓")
    print("="*70)


def test_automated_suite():
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = ZeroExponentEqualsZeroProblemGenerator(
        level=8,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = ZeroExponentEqualsZeroMalrule()
    correct = ZeroExponentCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Zero-Exponent-Equals-Zero  ".center(70) + "║")
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
