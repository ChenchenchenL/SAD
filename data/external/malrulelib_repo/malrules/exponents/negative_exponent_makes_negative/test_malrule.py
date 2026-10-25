#!/usr/bin/env python3
"""Test script for Negative-Exponent-Makes-Negative malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.exponents.negative_exponent_makes_negative import (
    NegativeExponentMakesNegativeProblemGenerator,
    NegativeExponentMakesNegativeMalrule,
    NegativeExponentCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING NEGATIVE-EXPONENT-MAKES-NEGATIVE")
    print("="*70)

    malrule = NegativeExponentMakesNegativeMalrule()
    correct = NegativeExponentCorrectAlgorithm()

    # Test case 1: 2^-2 = 1/4 (correct), -4 (malrule)
    problem1 = Problem(
        text="Evaluate: 2^-2",
        operands=[2, -2],
        operation='negative_exponent',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'base': 2,
            'negative_exp': -2,
            'positive_exp': 2,
            'correct_answer_fraction': '1/4',
            'correct_answer_decimal': 0.25,
            'malrule_answer': -4
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: 2^-2 → Correct: {correct_sol.answer}, Malrule: {malrule_sol.answer}")
    assert correct_sol.answer == '1/4'
    assert malrule_sol.answer == -4
    assert correct_sol.answer != str(malrule_sol.answer)
    print("✓ PASSED")

    # Test case 2: 3^-1 = 1/3 (correct), -3 (malrule)
    problem2 = Problem(
        text="Evaluate: 3^-1",
        operands=[3, -1],
        operation='negative_exponent',
        level=8,
        difficulty=DifficultyLevel.EASY,
        metadata={
            'base': 3,
            'negative_exp': -1,
            'positive_exp': 1,
            'correct_answer_fraction': '1/3',
            'correct_answer_decimal': 0.3333333333333333,
            'malrule_answer': -3
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert correct_sol2.answer == '1/3'
    assert malrule_sol2.answer == -3
    print("✓ TEST 2 PASSED")

    # Test case 3: 2^-3 = 1/8 (correct), -8 (malrule)
    problem3 = Problem(
        text="Evaluate: 2^-3",
        operands=[2, -3],
        operation='negative_exponent',
        level=9,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'base': 2,
            'negative_exp': -3,
            'positive_exp': 3,
            'correct_answer_fraction': '1/8',
            'correct_answer_decimal': 0.125,
            'malrule_answer': -8
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert correct_sol3.answer == '1/8'
    assert malrule_sol3.answer == -8
    print("✓ TEST 3 PASSED")

    # Test case 4: 5^-2 = 1/25 (correct), -25 (malrule)
    problem4 = Problem(
        text="Evaluate: 5^-2",
        operands=[5, -2],
        operation='negative_exponent',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'base': 5,
            'negative_exp': -2,
            'positive_exp': 2,
            'correct_answer_fraction': '1/25',
            'correct_answer_decimal': 0.04,
            'malrule_answer': -25
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    assert correct_sol4.answer == '1/25'
    assert malrule_sol4.answer == -25
    print("✓ TEST 4 PASSED")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_new_problem_templates():
    """Test new problem template types added for enhancement."""
    print("\n\n" + "="*70)
    print("TESTING NEW PROBLEM TEMPLATES")
    print("="*70)

    malrule = NegativeExponentMakesNegativeMalrule()
    correct = NegativeExponentCorrectAlgorithm()

    # TEST CASE 5: Larger negative exponent (2^-5)
    print("\n\nTEST CASE 5: Larger negative exponent (2^-5)")
    print("-"*70)

    problem5 = Problem(
        text="Evaluate: 2^-5",
        operands=[2, -5],
        operation='negative_exponent',
        level=9,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'base': 2,
            'negative_exp': -5,
            'positive_exp': 5,
            'correct_answer_fraction': '1/32',
            'correct_answer_decimal': 0.03125,
            'malrule_answer': -32,
            'problem_type': 'larger_negative_exponent'
        }
    )

    correct_sol5 = correct.solve(problem5)
    malrule_sol5 = malrule.solve(problem5)

    print(f"Problem: {problem5.text}")
    print(f"Correct answer: {correct_sol5.answer}")
    print(f"Malrule answer: {malrule_sol5.answer}")

    # Correct: 2^-5 = 1/32
    # Malrule: thinks negative exponent makes negative, so -(2^5) = -32
    assert correct_sol5.answer == '1/32', f"Expected '1/32', got {correct_sol5.answer}"
    assert malrule_sol5.answer == -32, f"Expected -32 (malrule), got {malrule_sol5.answer}"

    print("✓ TEST CASE 5 PASSED: Larger negative exponent template works")

    # TEST CASE 6: Fractional base ((1/3)^-2)
    print("\n\nTEST CASE 6: Fractional base context ((1/3)^-2)")
    print("-"*70)

    # For fractional base (1/3)^-2, we use the numeric base value 1/3
    problem6 = Problem(
        text="Evaluate: (1/3)^-2",
        operands=[3, -2],
        operation='negative_exponent',
        level=9,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'base': 1/3,  # Numeric value for computation
            'negative_exp': -2,
            'positive_exp': 2,
            'correct_answer_fraction': '9',
            'correct_answer_decimal': 9.0,
            'malrule_answer': -0.1111111111111111,
            'problem_type': 'fractional_base'
        }
    )

    correct_sol6 = correct.solve(problem6)
    malrule_sol6 = malrule.solve(problem6)

    print(f"Problem: {problem6.text}")
    print(f"Correct answer: {correct_sol6.answer}")
    print(f"Malrule answer: {malrule_sol6.answer}")

    # Correct: (1/3)^-2 = 1/((1/3)^2) = 1/(1/9) = 9
    # Malrule: thinks negative exponent makes negative, so -((1/3)^2) = -(1/9) ≈ -0.111
    assert correct_sol6.answer == '9', f"Expected '9', got {correct_sol6.answer}"
    assert abs(malrule_sol6.answer - (-0.1111111111111111)) < 0.0001, f"Expected ≈-0.111 (malrule), got {malrule_sol6.answer}"

    print("✓ TEST CASE 6 PASSED: Fractional base template works")

    # TEST CASE 7: Scientific word problem (10^-3)
    print("\n\nTEST CASE 7: Scientific context (10^-3)")
    print("-"*70)

    problem7 = Problem(
        text="In scientific notation, calculate: 10^-3",
        operands=[10, -3],
        operation='negative_exponent',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'base': 10,
            'negative_exp': -3,
            'positive_exp': 3,
            'correct_answer_fraction': '1/1000',
            'correct_answer_decimal': 0.001,
            'malrule_answer': -1000,
            'problem_type': 'word_problem_scientific'
        }
    )

    correct_sol7 = correct.solve(problem7)
    malrule_sol7 = malrule.solve(problem7)

    print(f"Problem: {problem7.text}")
    print(f"Correct answer: {correct_sol7.answer}")
    print(f"Malrule answer: {malrule_sol7.answer}")

    # Correct: 10^-3 = 1/1000 = 0.001
    # Malrule: thinks negative exponent makes negative, so -(10^3) = -1000
    assert correct_sol7.answer == '1/1000', f"Expected '1/1000', got {correct_sol7.answer}"
    assert malrule_sol7.answer == -1000, f"Expected -1000 (malrule), got {malrule_sol7.answer}"

    print("✓ TEST CASE 7 PASSED: Scientific word problem template works")

    # TEST CASE 8: Finance word problem (4^-2)
    print("\n\nTEST CASE 8: Finance context (4^-2)")
    print("-"*70)

    problem8 = Problem(
        text="Depreciation factor: 4^-2. Calculate the value.",
        operands=[4, -2],
        operation='negative_exponent',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'base': 4,
            'negative_exp': -2,
            'positive_exp': 2,
            'correct_answer_fraction': '1/16',
            'correct_answer_decimal': 0.0625,
            'malrule_answer': -16,
            'problem_type': 'word_problem_finance'
        }
    )

    correct_sol8 = correct.solve(problem8)
    malrule_sol8 = malrule.solve(problem8)

    print(f"Problem: {problem8.text}")
    print(f"Correct answer: {correct_sol8.answer}")
    print(f"Malrule answer: {malrule_sol8.answer}")

    # Correct: 4^-2 = 1/16 = 0.0625
    # Malrule: thinks negative exponent makes negative, so -(4^2) = -16
    assert correct_sol8.answer == '1/16', f"Expected '1/16', got {correct_sol8.answer}"
    assert malrule_sol8.answer == -16, f"Expected -16 (malrule), got {malrule_sol8.answer}"

    print("✓ TEST CASE 8 PASSED: Finance word problem template works")

    print("\n" + "="*70)
    print("ALL NEW TEMPLATE TEST CASES PASSED ✓")
    print("="*70)


def test_template_generation():
    """Test that all template types can be generated."""
    print("\n\n" + "="*70)
    print("TESTING TEMPLATE GENERATION")
    print("="*70)

    problem_gen = NegativeExponentMakesNegativeProblemGenerator(
        level=9,
        difficulty=DifficultyLevel.MEDIUM
    )

    # Generate multiple problems to cover all template types
    templates_found = set()
    for i in range(100):
        problem = problem_gen.generate(seed=9000 + i)
        if 'problem_type' in problem.metadata:
            templates_found.add(problem.metadata['problem_type'])

    print(f"\nTemplates generated: {sorted(templates_found)}")

    # Verify we have all expected templates
    expected_templates = {
        'simple_numeric',
        'larger_negative_exponent',
        'fractional_base',
        'word_problem_scientific',
        'word_problem_finance',
    }
    assert templates_found >= expected_templates, \
        f"Missing templates: {expected_templates - templates_found}"

    print("\n✓ ALL TEMPLATE TYPES GENERATED SUCCESSFULLY")
    print("="*70)


def test_word_problem_context_template():
    """Test the new word_problem_context template specifically."""
    print("\n\n" + "="*70)
    print("TESTING NEW WORD_PROBLEM_CONTEXT TEMPLATE")
    print("="*70)

    problem_gen = NegativeExponentMakesNegativeProblemGenerator(
        level=9,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = NegativeExponentMakesNegativeMalrule()
    correct = NegativeExponentCorrectAlgorithm()

    # Test word problem context with each formula type
    formula_types_found = set()
    variants_found = set()

    for i in range(50):
        problem = problem_gen.generate(seed=10000 + i, template='word_problem_context')

        # Check metadata
        assert problem.metadata.get('is_word_problem') == True, "is_word_problem flag not set"
        assert problem.metadata.get('template') == 'word_problem_context', "template not set correctly"

        word_problem_type = problem.metadata.get('word_problem_type')
        word_problem_variant = problem.metadata.get('word_problem_variant')

        if word_problem_type:
            formula_types_found.add(word_problem_type)
        if word_problem_variant is not None:
            variants_found.add(word_problem_variant)

        # Test that both algorithms can solve it
        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        # Verify the solutions are different
        assert correct_sol.answer != malrule_sol.answer, f"Correct and malrule answers should differ"
        assert correct_sol.is_correct == True, "Correct solution should be marked correct"
        assert malrule_sol.is_correct == False, "Malrule solution should be marked incorrect"

    print(f"\nFormula types generated: {sorted(formula_types_found)}")
    print(f"Variants generated: {sorted(variants_found)}")

    # Verify all formula types covered
    expected_formula_types = {'simple_numeric', 'larger_negative_exponent', 'fractional_base'}
    assert formula_types_found >= expected_formula_types, \
        f"Missing formula types: {expected_formula_types - formula_types_found}"

    # Verify all 3 variants (0, 1, 2) covered
    expected_variants = {0, 1, 2}
    assert variants_found >= expected_variants, \
        f"Missing variants: {expected_variants - variants_found}"

    print("\n✓ WORD_PROBLEM_CONTEXT TEMPLATE WORKS CORRECTLY")
    print("="*70)


def test_automated_suite():
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = NegativeExponentMakesNegativeProblemGenerator(
        level=9,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = NegativeExponentMakesNegativeMalrule()
    correct = NegativeExponentCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Negative-Exponent-Makes-Negative  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    try:
        test_specific_examples()
        test_new_problem_templates()
        test_template_generation()
        test_word_problem_context_template()
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
