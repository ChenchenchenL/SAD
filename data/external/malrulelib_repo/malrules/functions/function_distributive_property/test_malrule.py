#!/usr/bin/env python3
"""Test script for Function-Distributive-Property malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.functions.function_distributive_property import (
    FunctionDistributivePropertyProblemGenerator,
    FunctionDistributivePropertyMalrule,
    FunctionCompositionCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING FUNCTION-DISTRIBUTIVE-PROPERTY")
    print("="*70)

    malrule = FunctionDistributivePropertyMalrule()
    correct = FunctionCompositionCorrectAlgorithm()

    # Test case 1: f(x) = x², f(5+2) → Correct: 49, Malrule: 29
    problem1 = Problem(
        text="Given f(x) = x², evaluate f(5+2)",
        operands=[1, 5, 2],
        operation='function_evaluation_with_sum',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': 1,
            'value1': 5,
            'value2': 2,
            'input_sum': 7,
            'correct_answer': 49,  # f(7) = 49
            'malrule_answer': 29,  # f(5) + f(2) = 25 + 4 = 29
            'function_type': 'quadratic'
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: f(x) = x², f(5+2) → Correct: {correct_sol.answer}, Malrule: {malrule_sol.answer}")
    assert correct_sol.answer == 49
    assert malrule_sol.answer == 29
    assert correct_sol.answer != malrule_sol.answer
    print("✓ PASSED")

    # Test case 2: f(x) = x², f(3+4) → Correct: 49, Malrule: 25
    problem2 = Problem(
        text="Given f(x) = x², evaluate f(3+4)",
        operands=[1, 3, 4],
        operation='function_evaluation_with_sum',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': 1,
            'value1': 3,
            'value2': 4,
            'input_sum': 7,
            'correct_answer': 49,  # f(7) = 49
            'malrule_answer': 25,  # f(3) + f(4) = 9 + 16 = 25
            'function_type': 'quadratic'
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert correct_sol2.answer == 49
    assert malrule_sol2.answer == 25
    print("✓ TEST 2 PASSED")

    # Test case 3: f(x) = 2x², f(2+3) → Correct: 50, Malrule: 26
    problem3 = Problem(
        text="Given f(x) = 2x², evaluate f(2+3)",
        operands=[2, 2, 3],
        operation='function_evaluation_with_sum',
        level=9,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'coefficient': 2,
            'value1': 2,
            'value2': 3,
            'input_sum': 5,
            'correct_answer': 50,  # 2(5)² = 50
            'malrule_answer': 26,  # 2(2)² + 2(3)² = 8 + 18 = 26
            'function_type': 'quadratic'
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert correct_sol3.answer == 50
    assert malrule_sol3.answer == 26
    print("✓ TEST 3 PASSED")

    # Test case 4: f(x) = 3x², f(1+2) → Correct: 27, Malrule: 15
    problem4 = Problem(
        text="Given f(x) = 3x², evaluate f(1+2)",
        operands=[3, 1, 2],
        operation='function_evaluation_with_sum',
        level=10,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': 3,
            'value1': 1,
            'value2': 2,
            'input_sum': 3,
            'correct_answer': 27,  # 3(3)² = 27
            'malrule_answer': 15,  # 3(1)² + 3(2)² = 3 + 12 = 15
            'function_type': 'quadratic'
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    assert correct_sol4.answer == 27
    assert malrule_sol4.answer == 15
    print("✓ TEST 4 PASSED")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_new_problem_templates():
    """Test new problem template types added for enhancement."""
    print("\n" + "="*70)
    print("TESTING NEW PROBLEM TEMPLATES")
    print("="*70)

    malrule = FunctionDistributivePropertyMalrule()
    correct = FunctionCompositionCorrectAlgorithm()

    # TEST CASE 5: Subtraction input - f(x-a) where students think f(x) - f(a)
    # f(x) = x², f(5-2) → Correct: f(3) = 9, Malrule: f(5) - f(2) = 25 - 4 = 21
    problem5 = Problem(
        text="Given f(x) = x², evaluate f(5-2)",
        operands=[1, 5, 2],
        operation='function_evaluation_with_difference',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': 1,
            'value1': 5,
            'value2': 2,
            'input_value': 3,
            'operation': 'subtraction',
            'problem_type': 'subtraction_input',
            'correct_answer': 9,  # f(3) = 9
            'malrule_answer': 21,  # f(5) - f(2) = 25 - 4 = 21
            'function_type': 'quadratic'
        }
    )

    correct_sol5 = correct.solve(problem5)
    malrule_sol5 = malrule.solve(problem5)

    print(f"\nTEST 5: f(x-a) → Correct: {correct_sol5.answer}, Malrule: {malrule_sol5.answer}")
    assert correct_sol5.answer == 9
    assert malrule_sol5.answer == 21
    assert correct_sol5.answer != malrule_sol5.answer
    print("✓ PASSED")

    # TEST CASE 6: Cubic function - f(x) = x³
    # f(x) = x³, f(2+3) → Correct: f(5) = 125, Malrule: f(2) + f(3) = 8 + 27 = 35
    problem6 = Problem(
        text="Given f(x) = x³, evaluate f(2+3)",
        operands=[1, 2, 3],
        operation='function_evaluation_cubic',
        level=9,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'coefficient': 1,
            'value1': 2,
            'value2': 3,
            'input_value': 5,
            'operation': 'addition',
            'problem_type': 'cubic_function',
            'correct_answer': 125,  # f(5) = 125
            'malrule_answer': 35,  # f(2) + f(3) = 8 + 27 = 35
            'function_type': 'cubic'
        }
    )

    correct_sol6 = correct.solve(problem6)
    malrule_sol6 = malrule.solve(problem6)

    print(f"TEST 6: Cubic function → Correct: {correct_sol6.answer}, Malrule: {malrule_sol6.answer}")
    assert correct_sol6.answer == 125
    assert malrule_sol6.answer == 35
    print("✓ PASSED")

    # TEST CASE 7: Absolute value function - f(x) = |x+k|
    # f(x) = |x+2|, f(3+4) → Correct: f(7) = |7+2| = 9, Malrule: f(3) + f(4) = |3+2| + |4+2| = 5 + 6 = 11
    problem7 = Problem(
        text="Given f(x) = |x+2|, evaluate f(3+4)",
        operands=[1, 3, 4],
        operation='function_evaluation_absolute',
        level=9,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'coefficient': 1,
            'k_value': 2,
            'value1': 3,
            'value2': 4,
            'input_value': 7,
            'operation': 'addition',
            'problem_type': 'absolute_value',
            'correct_answer': 9,  # |7+2| = 9
            'malrule_answer': 11,  # |3+2| + |4+2| = 5 + 6 = 11
            'function_type': 'absolute_value'
        }
    )

    correct_sol7 = correct.solve(problem7)
    malrule_sol7 = malrule.solve(problem7)

    print(f"TEST 7: Absolute value → Correct: {correct_sol7.answer}, Malrule: {malrule_sol7.answer}")
    assert correct_sol7.answer == 9
    assert malrule_sol7.answer == 11
    print("✓ PASSED")

    # TEST CASE 8: Word problem context
    # Area function: A(s) = s², find A(3+2)
    # Correct: A(5) = 25, Malrule: A(3) + A(2) = 9 + 4 = 13
    problem8 = Problem(
        text="The area of a square with side length s is A(s) = s². Find the area when the side length is 3+2 cm.",
        operands=[1, 3, 2],
        operation='function_evaluation_word',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': 1,
            'value1': 3,
            'value2': 2,
            'input_value': 5,
            'operation': 'addition',
            'problem_type': 'word_problem_context',
            'correct_answer': 25,  # A(5) = 25
            'malrule_answer': 13,  # A(3) + A(2) = 9 + 4 = 13
            'function_type': 'quadratic',
            'context': 'area'
        }
    )

    correct_sol8 = correct.solve(problem8)
    malrule_sol8 = malrule.solve(problem8)

    print(f"TEST 8: Word problem → Correct: {correct_sol8.answer}, Malrule: {malrule_sol8.answer}")
    assert correct_sol8.answer == 25
    assert malrule_sol8.answer == 13
    print("✓ PASSED")

    print("\n" + "="*70)
    print("ALL NEW TEMPLATE TESTS PASSED ✓")
    print("="*70)


def test_template_generation():
    """Test that all template types can be generated."""
    print("\n" + "="*70)
    print("TESTING TEMPLATE GENERATION")
    print("="*70)

    problem_gen = FunctionDistributivePropertyProblemGenerator(
        level=10,
        difficulty=DifficultyLevel.HARD
    )

    templates_found = set()
    for i in range(100):
        problem = problem_gen.generate(seed=70000 + i)
        if 'problem_type' in problem.metadata:
            templates_found.add(problem.metadata['problem_type'])

    expected_templates = {
        'square', 'scaled_square',
        'subtraction_input', 'cubic_function',
        'absolute_value', 'word_problem_context'
    }

    print(f"\nFound templates: {templates_found}")
    print(f"Expected templates: {expected_templates}")

    assert templates_found >= expected_templates, f"Missing templates: {expected_templates - templates_found}"
    print("\n✓ ALL TEMPLATE TYPES CAN BE GENERATED")

    print("\n" + "="*70)
    print("TEMPLATE GENERATION TEST PASSED ✓")
    print("="*70)


def test_automated_suite():
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = FunctionDistributivePropertyProblemGenerator(
        level=9,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = FunctionDistributivePropertyMalrule()
    correct = FunctionCompositionCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Function-Distributive-Property  ".center(70) + "║")
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
