#!/usr/bin/env python3
"""Test script for Multiply-Base-By-Exponent malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.exponents.multiply_base_by_exponent import (
    MultiplyBaseByExponentProblemGenerator,
    MultiplyBaseByExponentMalrule,
    ExponentiationCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING MULTIPLY-BASE-BY-EXPONENT")
    print("="*70)

    malrule = MultiplyBaseByExponentMalrule()
    correct = ExponentiationCorrectAlgorithm()

    # Test case 1: 2³ = 8 (correct), 6 (malrule: 2×3)
    problem1 = Problem(
        text="Evaluate: 2^3",
        operands=[2, 3],
        operation='exponentiation',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'base': 2,
            'exponent': 3,
            'correct_answer': 8,
            'malrule_answer': 6
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: 2³ → Correct: {correct_sol.answer}, Malrule: {malrule_sol.answer}")
    assert correct_sol.answer == 8
    assert malrule_sol.answer == 6
    assert correct_sol.answer != malrule_sol.answer
    print("✓ PASSED")

    # Test case 2: 3² = 9 (correct), 6 (malrule: 3×2)
    problem2 = Problem(
        text="Evaluate: 3^2",
        operands=[3, 2],
        operation='exponentiation',
        level=7,
        difficulty=DifficultyLevel.EASY,
        metadata={
            'base': 3,
            'exponent': 2,
            'correct_answer': 9,
            'malrule_answer': 6
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert correct_sol2.answer == 9
    assert malrule_sol2.answer == 6
    print("✓ TEST 2 PASSED")

    # Test case 3: 5⁴ = 625 (correct), 20 (malrule: 5×4)
    problem3 = Problem(
        text="Evaluate: 5^4",
        operands=[5, 4],
        operation='exponentiation',
        level=8,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'base': 5,
            'exponent': 4,
            'correct_answer': 625,
            'malrule_answer': 20
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert correct_sol3.answer == 625
    assert malrule_sol3.answer == 20
    print("✓ TEST 3 PASSED")

    # Test case 4: 10³ = 1000 (correct), 30 (malrule: 10×3)
    problem4 = Problem(
        text="Evaluate: 10^3",
        operands=[10, 3],
        operation='exponentiation',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'base': 10,
            'exponent': 3,
            'correct_answer': 1000,
            'malrule_answer': 30
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    assert correct_sol4.answer == 1000
    assert malrule_sol4.answer == 30
    print("✓ TEST 4 PASSED")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_new_problem_templates():
    """Test new problem template types added for enhancement."""
    print("\n\n" + "="*70)
    print("TESTING NEW PROBLEM TEMPLATES")
    print("="*70)

    malrule = MultiplyBaseByExponentMalrule()
    correct = ExponentiationCorrectAlgorithm()

    # TEST CASE 5: Larger exponent
    print("\n\nTEST CASE 5: Larger exponent (3^7)")
    print("-"*70)

    problem5 = Problem(
        text="Evaluate: 3^7",
        operands=[3, 7],
        operation='exponentiation',
        level=8,
        difficulty=DifficultyLevel.HARD,
        metadata={'base': 3, 'exponent': 7, 'correct_answer': 2187, 'malrule_answer': 21, 'problem_type': 'larger_exponent'}
    )

    correct_sol5 = correct.solve(problem5)
    malrule_sol5 = malrule.solve(problem5)

    print(f"Problem: {problem5.text}")
    print(f"Correct answer: {correct_sol5.answer}")
    print(f"Malrule answer: {malrule_sol5.answer}")

    # Correct: 3^7 = 2187
    # Malrule: 3 × 7 = 21
    assert correct_sol5.answer == 2187, f"Expected 2187, got {correct_sol5.answer}"
    assert malrule_sol5.answer == 21, f"Expected 21 (malrule), got {malrule_sol5.answer}"

    print("✓ TEST CASE 5 PASSED: Larger exponent template works")

    # TEST CASE 6: Area word problem
    print("\n\nTEST CASE 6: Area context (square with side 8)")
    print("-"*70)

    problem6 = Problem(
        text="A square has side length 8 cm. What is the area? (Area = side^2)",
        operands=[8, 2],
        operation='exponentiation',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={'base': 8, 'exponent': 2, 'correct_answer': 64, 'malrule_answer': 16, 'problem_type': 'word_problem_area'}
    )

    correct_sol6 = correct.solve(problem6)
    malrule_sol6 = malrule.solve(problem6)

    print(f"Problem: {problem6.text}")
    print(f"Correct answer: {correct_sol6.answer}")
    print(f"Malrule answer: {malrule_sol6.answer}")

    # Correct: 8^2 = 64
    # Malrule: 8 × 2 = 16
    assert correct_sol6.answer == 64, f"Expected 64, got {correct_sol6.answer}"
    assert malrule_sol6.answer == 16, f"Expected 16 (malrule), got {malrule_sol6.answer}"

    print("✓ TEST CASE 6 PASSED: Area word problem template works")

    # TEST CASE 7: Volume word problem
    print("\n\nTEST CASE 7: Volume context (cube with side 5)")
    print("-"*70)

    problem7 = Problem(
        text="A cubic box has sides of 5 inches. What is its volume? (V = s^3)",
        operands=[5, 3],
        operation='exponentiation',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={'base': 5, 'exponent': 3, 'correct_answer': 125, 'malrule_answer': 15, 'problem_type': 'word_problem_volume'}
    )

    correct_sol7 = correct.solve(problem7)
    malrule_sol7 = malrule.solve(problem7)

    print(f"Problem: {problem7.text}")
    print(f"Correct answer: {correct_sol7.answer}")
    print(f"Malrule answer: {malrule_sol7.answer}")

    # Correct: 5^3 = 125
    # Malrule: 5 × 3 = 15
    assert correct_sol7.answer == 125, f"Expected 125, got {correct_sol7.answer}"
    assert malrule_sol7.answer == 15, f"Expected 15 (malrule), got {malrule_sol7.answer}"

    print("✓ TEST CASE 7 PASSED: Volume word problem template works")

    # TEST CASE 8: Growth word problem
    print("\n\nTEST CASE 8: Growth context (bacteria 2^4)")
    print("-"*70)

    problem8 = Problem(
        text="Population grows by factor of 2 each generation. After 4 generations: 2^4 = ?",
        operands=[2, 4],
        operation='exponentiation',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={'base': 2, 'exponent': 4, 'correct_answer': 16, 'malrule_answer': 8, 'problem_type': 'word_problem_growth'}
    )

    correct_sol8 = correct.solve(problem8)
    malrule_sol8 = malrule.solve(problem8)

    print(f"Problem: {problem8.text}")
    print(f"Correct answer: {correct_sol8.answer}")
    print(f"Malrule answer: {malrule_sol8.answer}")

    # Correct: 2^4 = 16
    # Malrule: 2 × 4 = 8
    assert correct_sol8.answer == 16, f"Expected 16, got {correct_sol8.answer}"
    assert malrule_sol8.answer == 8, f"Expected 8 (malrule), got {malrule_sol8.answer}"

    print("✓ TEST CASE 8 PASSED: Growth word problem template works")

    print("\n" + "="*70)
    print("ALL NEW TEMPLATE TEST CASES PASSED ✓")
    print("="*70)


def test_template_generation():
    """Test that all template types can be generated."""
    print("\n\n" + "="*70)
    print("TESTING TEMPLATE GENERATION")
    print("="*70)

    problem_gen = MultiplyBaseByExponentProblemGenerator(
        level=8,
        difficulty=DifficultyLevel.MEDIUM
    )

    # Generate multiple problems to cover all template types
    templates_found = set()
    for i in range(50):
        problem = problem_gen.generate(seed=8000 + i)
        if 'problem_type' in problem.metadata:
            templates_found.add(problem.metadata['problem_type'])

    print(f"\nTemplates generated: {sorted(templates_found)}")

    # Verify we have all expected templates
    expected_templates = {
        'simple_numeric',
        'larger_exponent',
        'word_problem_area',
        'word_problem_volume',
        'word_problem_growth',
    }
    assert templates_found >= expected_templates, \
        f"Missing templates: {expected_templates - templates_found}"

    print("\n✓ ALL TEMPLATE TYPES GENERATED SUCCESSFULLY")
    print("="*70)


def test_word_problem_context_template():
    """Test the new word_problem_context template."""
    print("\n\n" + "="*70)
    print("TESTING WORD_PROBLEM_CONTEXT TEMPLATE")
    print("="*70)

    problem_gen = MultiplyBaseByExponentProblemGenerator(
        level=8,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = MultiplyBaseByExponentMalrule()
    correct = ExponentiationCorrectAlgorithm()

    # Test multiple word problem contexts
    word_problem_types_found = set()
    for i in range(30):
        problem = problem_gen.generate(seed=9000 + i, template='word_problem_context')

        # Verify metadata
        assert problem.metadata.get('is_word_problem') == True, "is_word_problem should be True"
        assert problem.metadata.get('template') == 'word_problem_context', "template should be word_problem_context"
        assert 'word_problem_type' in problem.metadata, "word_problem_type should be in metadata"
        assert 'word_problem_variant' in problem.metadata, "word_problem_variant should be in metadata"

        word_problem_types_found.add(problem.metadata['word_problem_type'])

        # Test that correct and malrule algorithms work
        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        assert correct_sol.answer == problem.metadata['correct_answer']
        assert malrule_sol.answer == problem.metadata['malrule_answer']
        assert correct_sol.answer != malrule_sol.answer

        # Print first example
        if i == 0:
            print(f"\nExample word problem:")
            print(f"  {problem.text}")
            print(f"  Correct answer: {correct_sol.answer}")
            print(f"  Malrule answer: {malrule_sol.answer}")

    print(f"\nWord problem types found: {sorted(word_problem_types_found)}")

    # Verify we have all expected word problem types
    expected_word_problem_types = {'simple_numeric', 'larger_exponent'}
    assert word_problem_types_found == expected_word_problem_types, \
        f"Expected {expected_word_problem_types}, got {word_problem_types_found}"

    print("\n✓ WORD_PROBLEM_CONTEXT TEMPLATE WORKS CORRECTLY")
    print("="*70)


def test_automated_suite():
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = MultiplyBaseByExponentProblemGenerator(
        level=7,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = MultiplyBaseByExponentMalrule()
    correct = ExponentiationCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Multiply-Base-By-Exponent  ".center(70) + "║")
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
