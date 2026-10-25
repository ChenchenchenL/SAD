#!/usr/bin/env python3
"""Test script for Function-Notation-Is-Multiplication malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.functions.function_notation_is_multiplication import (
    FunctionNotationIsMultiplicationProblemGenerator,
    FunctionNotationIsMultiplicationMalrule,
    FunctionEvaluationCorrectAlgorithm
)


def verify_steps_are_different(correct_steps, malrule_steps, problem_text):
    """Verify that correct and malrule steps are meaningfully different."""
    # Convert steps lists to strings for comparison
    correct_text = '\n'.join(correct_steps)
    malrule_text = '\n'.join(malrule_steps)

    # Check that correct steps don't contain "MALRULE"
    if "MALRULE" in correct_text:
        raise AssertionError(f"Correct steps should NOT contain 'MALRULE' marker for problem: {problem_text}")

    # Check that steps are not identical
    if correct_text == malrule_text:
        raise AssertionError(f"Correct and malrule steps should be different for problem: {problem_text}")

    return True


def test_edge_case_handler(problem, correct_sol, malrule_sol):
    """
    Handle edge cases where malrule produces same answer as correct algorithm.
    This should be treated as a test failure with diagnostic output.
    """
    if correct_sol.answer == malrule_sol.answer:
        print("\n" + "!"*70)
        print("EDGE CASE DETECTED: Malrule produced same answer as correct!")
        print("!"*70)
        print(f"\nProblem: {problem.text}")
        print(f"\nOperands: {problem.operands}")
        print(f"Metadata: {problem.metadata}")
        print(f"\nAnswer (both): {correct_sol.answer}")

        print("\n" + "="*70)
        print("CORRECT ALGORITHM STEPS:")
        print("="*70)
        for step in correct_sol.steps:
            print(step)

        print("\n" + "="*70)
        print("MALRULE ALGORITHM STEPS:")
        print("="*70)
        for step in malrule_sol.steps:
            print(step)

        print("\n" + "!"*70)
        print("TEST FAILED: This edge case should not occur in valid test data!")
        print("!"*70)

        raise AssertionError(
            f"Edge case detected: Malrule answer equals correct answer ({correct_sol.answer}). "
            f"This indicates the problem parameters need adjustment. See steps above."
        )


def test_specific_examples():
    print("="*70)
    print("TESTING FUNCTION-NOTATION-IS-MULTIPLICATION")
    print("="*70)

    malrule = FunctionNotationIsMultiplicationMalrule()
    correct = FunctionEvaluationCorrectAlgorithm()

    # Test case 1: f(x) = 2x + 3, f(5) = 13 (correct), 10 (malrule: 2×5)
    problem1 = Problem(
        text="Given f(x) = 2x + 3, evaluate f(5)",
        operands=[2, 3, 5],
        operation='function_evaluation',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': 2,
            'constant': 3,
            'input': 5,
            'correct_answer': 13,  # 2(5) + 3 = 13
            'malrule_answer': 10,  # Student: 2 × 5 = 10
            'problem_type': 'simple_linear'
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: f(x) = 2x + 3, f(5) → Correct: {correct_sol.answer}, Malrule: {malrule_sol.answer}")
    assert correct_sol.answer == 13
    assert malrule_sol.answer == 10
    test_edge_case_handler(problem1, correct_sol, malrule_sol)
    verify_steps_are_different(correct_sol.steps, malrule_sol.steps, problem1.text)
    print("✓ PASSED (answer and steps verified)")

    # Test case 2: f(x) = 3x + 1, f(4) = 13 (correct), 12 (malrule: 3×4)
    problem2 = Problem(
        text="Given f(x) = 3x + 1, evaluate f(4)",
        operands=[3, 1, 4],
        operation='function_evaluation',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': 3,
            'constant': 1,
            'input': 4,
            'correct_answer': 13,  # 3(4) + 1 = 13
            'malrule_answer': 12,  # Student: 3 × 4 = 12
            'problem_type': 'simple_linear'
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert correct_sol2.answer == 13
    assert malrule_sol2.answer == 12
    test_edge_case_handler(problem2, correct_sol2, malrule_sol2)
    verify_steps_are_different(correct_sol2.steps, malrule_sol2.steps, problem2.text)
    print("✓ TEST 2 PASSED (answer and steps verified)")

    # Test case 3: f(x) = 4x - 2, f(3) = 10 (correct), 12 (malrule: 4×3)
    problem3 = Problem(
        text="Given f(x) = 4x - 2, evaluate f(3)",
        operands=[4, -2, 3],
        operation='function_evaluation',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': 4,
            'constant': -2,
            'input': 3,
            'correct_answer': 10,  # 4(3) - 2 = 10
            'malrule_answer': 12,  # Student: 4 × 3 = 12
            'problem_type': 'simple_linear'
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert correct_sol3.answer == 10
    assert malrule_sol3.answer == 12
    test_edge_case_handler(problem3, correct_sol3, malrule_sol3)
    verify_steps_are_different(correct_sol3.steps, malrule_sol3.steps, problem3.text)
    print("✓ TEST 3 PASSED (answer and steps verified)")

    # Test case 4: f(x) = 5x + 7, f(2) = 17 (correct), 10 (malrule: 5×2)
    problem4 = Problem(
        text="Given f(x) = 5x + 7, evaluate f(2)",
        operands=[5, 7, 2],
        operation='function_evaluation',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': 5,
            'constant': 7,
            'input': 2,
            'correct_answer': 17,  # 5(2) + 7 = 17
            'malrule_answer': 10,  # Student: 5 × 2 = 10
            'problem_type': 'simple_linear'
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    assert correct_sol4.answer == 17
    assert malrule_sol4.answer == 10
    test_edge_case_handler(problem4, correct_sol4, malrule_sol4)
    verify_steps_are_different(correct_sol4.steps, malrule_sol4.steps, problem4.text)
    print("✓ TEST 4 PASSED (answer and steps verified)")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_all_problem_templates():
    """Comprehensive test of ALL problem templates with answer AND step verification."""
    print("\n\n" + "="*70)
    print("TESTING ALL PROBLEM TEMPLATES (COMPREHENSIVE)")
    print("="*70)

    malrule = FunctionNotationIsMultiplicationMalrule()
    correct = FunctionEvaluationCorrectAlgorithm()

    # TEST 1: Simple Linear - f(x) = ax + b
    print("\n\n" + "-"*70)
    print("TEST 1: Simple Linear Function")
    print("-"*70)

    problem1 = Problem(
        text="Given f(x) = 2x + 3, evaluate f(5)",
        operands=[2, 3, 5],
        operation='function_evaluation',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': 2,
            'constant': 3,
            'input': 5,
            'correct_answer': 13,  # 2(5) + 3 = 13
            'malrule_answer': 10,  # 2 × 5 = 10
            'problem_type': 'simple_linear'
        }
    )

    correct_sol1 = correct.solve(problem1)
    malrule_sol1 = malrule.solve(problem1)

    print(f"Problem: {problem1.text}")
    print(f"Correct answer: {correct_sol1.answer}, Malrule answer: {malrule_sol1.answer}")
    assert correct_sol1.answer == 13
    assert malrule_sol1.answer == 10
    test_edge_case_handler(problem1, correct_sol1, malrule_sol1)
    verify_steps_are_different(correct_sol1.steps, malrule_sol1.steps, problem1.text)
    print("✓ PASSED (answer and steps verified)")

    # TEST 2: Quadratic Function - f(x) = ax² + bx + c
    print("\n\n" + "-"*70)
    print("TEST 2: Quadratic Function")
    print("-"*70)

    problem2 = Problem(
        text="Given f(x) = 2x² + 3x - 1, evaluate f(3)",
        operands=[2, 3, -1, 3],
        operation='function_evaluation',
        level=10,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'coefficient': 2,
            'b_coefficient': 3,
            'c_constant': -1,
            'constant': -1,
            'input': 3,
            'correct_answer': 26,  # 2(9) + 3(3) - 1 = 18 + 9 - 1 = 26
            'malrule_answer': 6,   # 2 × 3 = 6
            'problem_type': 'quadratic_function'
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)

    print(f"Problem: {problem2.text}")
    print(f"Correct answer: {correct_sol2.answer}, Malrule answer: {malrule_sol2.answer}")
    assert correct_sol2.answer == 26
    assert malrule_sol2.answer == 6
    test_edge_case_handler(problem2, correct_sol2, malrule_sol2)
    verify_steps_are_different(correct_sol2.steps, malrule_sol2.steps, problem2.text)
    print("✓ PASSED (answer and steps verified)")

    # TEST 3: Function Composition - f(g(x))
    print("\n\n" + "-"*70)
    print("TEST 3: Function Composition")
    print("-"*70)

    problem3 = Problem(
        text="Given f(x) = 3x + 2 and g(x) = 2x + 1, evaluate f(g(2))",
        operands=[3, 2, 2, 1, 2],
        operation='function_evaluation',
        level=10,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'coefficient': 3,
            'constant': 2,
            'g_coefficient': 2,
            'g_constant': 1,
            'input': 2,
            'inner_result': 5,      # g(2) = 2(2) + 1 = 5
            'correct_answer': 17,   # f(5) = 3(5) + 2 = 17
            'malrule_answer': 12,   # 3 × 2 × 2 = 12
            'problem_type': 'function_composition'
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)

    print(f"Problem: {problem3.text}")
    print(f"Correct answer: {correct_sol3.answer}, Malrule answer: {malrule_sol3.answer}")
    assert correct_sol3.answer == 17
    assert malrule_sol3.answer == 12
    test_edge_case_handler(problem3, correct_sol3, malrule_sol3)
    verify_steps_are_different(correct_sol3.steps, malrule_sol3.steps, problem3.text)
    print("✓ PASSED (answer and steps verified)")

    # TEST 4: Absolute Value Function - f(x) = |ax + b|
    print("\n\n" + "-"*70)
    print("TEST 4: Absolute Value Function")
    print("-"*70)

    problem4 = Problem(
        text="Given f(x) = |3x - 5|, evaluate f(1)",
        operands=[3, -5, 1],
        operation='function_evaluation',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': 3,
            'constant': -5,
            'input': 1,
            'correct_answer': 2,   # |3(1) - 5| = |-2| = 2
            'malrule_answer': 3,   # 3 × 1 = 3
            'problem_type': 'absolute_value_function'
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)

    print(f"Problem: {problem4.text}")
    print(f"Correct answer: {correct_sol4.answer}, Malrule answer: {malrule_sol4.answer}")
    assert correct_sol4.answer == 2
    assert malrule_sol4.answer == 3
    test_edge_case_handler(problem4, correct_sol4, malrule_sol4)
    verify_steps_are_different(correct_sol4.steps, malrule_sol4.steps, problem4.text)
    print("✓ PASSED (answer and steps verified)")

    # TEST 5: Word Problem - Simple Linear
    print("\n\n" + "-"*70)
    print("TEST 5: Word Problem (Simple Linear)")
    print("-"*70)

    problem5 = Problem(
        text="The cost function for producing x items is C(x) = 5x + 20 dollars. Find C(4).",
        operands=[5, 20, 4],
        operation='function_evaluation',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': 5,
            'constant': 20,
            'input': 4,
            'correct_answer': 40,    # 5(4) + 20 = 40
            'malrule_answer': 20,    # 5 × 4 = 20
            'problem_type': 'word_problem_context',
            'is_word_problem': True,
            'word_problem_type': 'simple_linear'
        }
    )

    correct_sol5 = correct.solve(problem5)
    malrule_sol5 = malrule.solve(problem5)

    print(f"Problem: {problem5.text}")
    print(f"Correct answer: {correct_sol5.answer}, Malrule answer: {malrule_sol5.answer}")
    assert correct_sol5.answer == 40
    assert malrule_sol5.answer == 20
    test_edge_case_handler(problem5, correct_sol5, malrule_sol5)
    verify_steps_are_different(correct_sol5.steps, malrule_sol5.steps, problem5.text)
    print("✓ PASSED (answer and steps verified)")

    # TEST 6: Word Problem - Quadratic
    print("\n\n" + "-"*70)
    print("TEST 6: Word Problem (Quadratic)")
    print("-"*70)

    problem6 = Problem(
        text="The profit function is P(x) = 2x² + 3x - 5 dollars for x units. Find P(4).",
        operands=[2, 3, -5, 4],
        operation='function_evaluation',
        level=10,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'coefficient': 2,
            'b_coefficient': 3,
            'c_constant': -5,
            'constant': -5,
            'input': 4,
            'correct_answer': 39,    # 2(16) + 3(4) - 5 = 32 + 12 - 5 = 39
            'malrule_answer': 8,     # 2 × 4 = 8
            'problem_type': 'word_problem_context',
            'is_word_problem': True,
            'word_problem_type': 'quadratic_function'
        }
    )

    correct_sol6 = correct.solve(problem6)
    malrule_sol6 = malrule.solve(problem6)

    print(f"Problem: {problem6.text}")
    print(f"Correct answer: {correct_sol6.answer}, Malrule answer: {malrule_sol6.answer}")
    assert correct_sol6.answer == 39
    assert malrule_sol6.answer == 8
    test_edge_case_handler(problem6, correct_sol6, malrule_sol6)
    verify_steps_are_different(correct_sol6.steps, malrule_sol6.steps, problem6.text)
    print("✓ PASSED (answer and steps verified)")

    # TEST 7: Word Problem - Function Composition
    print("\n\n" + "-"*70)
    print("TEST 7: Word Problem (Function Composition)")
    print("-"*70)

    problem7 = Problem(
        text="A machine process has two stages: g(x) = 2x + 3 and f(x) = 4x + 1. Find f(g(2)).",
        operands=[4, 1, 2, 3, 2],
        operation='function_evaluation',
        level=10,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'coefficient': 4,
            'constant': 1,
            'g_coefficient': 2,
            'g_constant': 3,
            'input': 2,
            'inner_result': 7,       # g(2) = 2(2) + 3 = 7
            'correct_answer': 29,    # f(7) = 4(7) + 1 = 29
            'malrule_answer': 16,    # 4 × 2 × 2 = 16
            'problem_type': 'word_problem_context',
            'is_word_problem': True,
            'word_problem_type': 'function_composition'
        }
    )

    correct_sol7 = correct.solve(problem7)
    malrule_sol7 = malrule.solve(problem7)

    print(f"Problem: {problem7.text}")
    print(f"Correct answer: {correct_sol7.answer}, Malrule answer: {malrule_sol7.answer}")
    assert correct_sol7.answer == 29
    assert malrule_sol7.answer == 16
    test_edge_case_handler(problem7, correct_sol7, malrule_sol7)
    verify_steps_are_different(correct_sol7.steps, malrule_sol7.steps, problem7.text)
    print("✓ PASSED (answer and steps verified)")

    # TEST 8: Word Problem - Absolute Value
    print("\n\n" + "-"*70)
    print("TEST 8: Word Problem (Absolute Value)")
    print("-"*70)

    problem8 = Problem(
        text="The error margin E(x) = |4x - 7| units for x trials. Find E(1).",
        operands=[4, -7, 1],
        operation='function_evaluation',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': 4,
            'constant': -7,
            'input': 1,
            'correct_answer': 3,     # |4(1) - 7| = |-3| = 3
            'malrule_answer': 4,     # 4 × 1 = 4
            'problem_type': 'word_problem_context',
            'is_word_problem': True,
            'word_problem_type': 'absolute_value_function'
        }
    )

    correct_sol8 = correct.solve(problem8)
    malrule_sol8 = malrule.solve(problem8)

    print(f"Problem: {problem8.text}")
    print(f"Correct answer: {correct_sol8.answer}, Malrule answer: {malrule_sol8.answer}")
    assert correct_sol8.answer == 3
    assert malrule_sol8.answer == 4
    test_edge_case_handler(problem8, correct_sol8, malrule_sol8)
    verify_steps_are_different(correct_sol8.steps, malrule_sol8.steps, problem8.text)
    print("✓ PASSED (answer and steps verified)")

    print("\n" + "="*70)
    print("ALL TEMPLATE TESTS PASSED ✓")
    print("Templates tested: simple_linear, quadratic_function, function_composition,")
    print("                  absolute_value_function, and all word_problem variants")
    print("="*70)


def test_template_generation():
    """Test that all template types can be generated."""
    print("\n\n" + "="*70)
    print("TESTING TEMPLATE GENERATION")
    print("="*70)

    problem_gen = FunctionNotationIsMultiplicationProblemGenerator(
        level=10,
        difficulty=DifficultyLevel.MEDIUM
    )

    # Generate multiple problems to cover all template types
    templates_found = set()
    for i in range(50):
        problem = problem_gen.generate(seed=12000 + i)
        if 'problem_type' in problem.metadata:
            templates_found.add(problem.metadata['problem_type'])

    print(f"\nTemplates generated: {sorted(templates_found)}")

    # Verify we have all expected templates
    expected_templates = {
        'simple_linear',
        'quadratic_function',
        'function_composition',
        'absolute_value_function',
        'word_problem_context',
    }
    assert templates_found >= expected_templates, \
        f"Missing templates: {expected_templates - templates_found}"

    print("\n✓ ALL TEMPLATE TYPES GENERATED SUCCESSFULLY")
    print("="*70)


def test_automated_suite():
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = FunctionNotationIsMultiplicationProblemGenerator(
        level=9,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = FunctionNotationIsMultiplicationMalrule()
    correct = FunctionEvaluationCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Function-Notation-Is-Multiplication  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    try:
        test_specific_examples()
        test_all_problem_templates()
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
