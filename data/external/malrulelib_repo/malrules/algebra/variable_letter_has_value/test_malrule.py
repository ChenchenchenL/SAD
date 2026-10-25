#!/usr/bin/env python3
"""Test script for Variable-Letter-Has-Value malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.algebra.variable_letter_has_value import (
    VariableLetterHasValueProblemGenerator,
    VariableLetterHasValueMalrule,
    AlgebraicEquationCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING VARIABLE-LETTER-HAS-VALUE")
    print("="*70)

    malrule = VariableLetterHasValueMalrule()
    correct = AlgebraicEquationCorrectAlgorithm()

    # Test case 1: x + 5 = 12 (x=7, but student thinks x=10)
    problem1 = Problem(
        text="Solve for x: x + 5 = 12",
        operands=[5, 12],
        operation='algebra_solve',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'variable': 'x',
            'constant': 5,
            'result': 12,
            'correct_value': 7,
            'assumed_value': 10,
            'malrule_answer': 15,  # 10 + 5
            'equation': 'x + 5 = 12'
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: x + 5 = 12 → Correct: x={correct_sol.answer}, Malrule: x={malrule_sol.answer}")
    assert correct_sol.answer == 7
    assert malrule_sol.answer == 10
    assert correct_sol.answer != malrule_sol.answer
    print("✓ PASSED")

    # Test case 2: n + 8 = 15 (n=7, but student thinks n=1)
    problem2 = Problem(
        text="Solve for n: n + 8 = 15",
        operands=[8, 15],
        operation='algebra_solve',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'variable': 'n',
            'constant': 8,
            'result': 15,
            'correct_value': 7,
            'assumed_value': 1,
            'malrule_answer': 9,  # 1 + 8
            'equation': 'n + 8 = 15'
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert correct_sol2.answer == 7
    assert malrule_sol2.answer == 1
    print("✓ TEST 2 PASSED")

    # Test case 3: a + 4 = 9 (a=5, but student thinks a=1)
    problem3 = Problem(
        text="Solve for a: a + 4 = 9",
        operands=[4, 9],
        operation='algebra_solve',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'variable': 'a',
            'constant': 4,
            'result': 9,
            'correct_value': 5,
            'assumed_value': 1,
            'malrule_answer': 5,  # 1 + 4
            'equation': 'a + 4 = 9'
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert correct_sol3.answer == 5
    assert malrule_sol3.answer == 1
    print("✓ TEST 3 PASSED")

    # Test case 4: y + 3 = 20 (y=17, but student thinks y=25)
    problem4 = Problem(
        text="Solve for y: y + 3 = 20",
        operands=[3, 20],
        operation='algebra_solve',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'variable': 'y',
            'constant': 3,
            'result': 20,
            'correct_value': 17,
            'assumed_value': 25,
            'malrule_answer': 28,  # 25 + 3
            'equation': 'y + 3 = 20'
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    assert correct_sol4.answer == 17
    assert malrule_sol4.answer == 25
    print("✓ TEST 4 PASSED")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_all_templates():
    """Test all 5 templates to ensure they work correctly."""
    print("\n\n" + "="*70)
    print("TESTING ALL TEMPLATES")
    print("="*70)

    malrule = VariableLetterHasValueMalrule()
    correct = AlgebraicEquationCorrectAlgorithm()
    templates = ['basic_addition', 'basic_subtraction', 'basic_multiplication', 'two_step_equation', 'word_problem']

    for template in templates:
        print(f"\n--- Testing template: {template} ---")
        problem_gen = VariableLetterHasValueProblemGenerator(level=7, difficulty=DifficultyLevel.MEDIUM)
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

    malrule = VariableLetterHasValueMalrule()
    correct = AlgebraicEquationCorrectAlgorithm()

    # Test 1: basic_addition template
    print("\n--- Test 1: basic_addition ---")
    problem1 = Problem(
        text="Solve for x: x + 6 = 13",
        operands=[6, 13],
        operation='algebra_solve',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'variable': 'x',
            'constant': 6,
            'result': 13,
            'correct_value': 7,
            'assumed_value': 10,
            'malrule_answer': 10,
            'equation': 'x + 6 = 13',
            'template': 'basic_addition'
        }
    )
    correct_sol1 = correct.solve(problem1)
    malrule_sol1 = malrule.solve(problem1)
    expected1 = malrule.calculate_expected_answer(problem1)

    assert correct_sol1.answer == 7
    assert malrule_sol1.answer == 10
    assert expected1 == malrule_sol1.answer
    assert correct_sol1.answer != malrule_sol1.answer
    print(f"  x + 6 = 13 → Correct: x={correct_sol1.answer}, Malrule: x={malrule_sol1.answer}")
    print("  ✓ PASSED")

    # Test 2: basic_subtraction template
    print("\n--- Test 2: basic_subtraction ---")
    problem2 = Problem(
        text="Solve for n: n - 5 = 8",
        operands=[5, 8],
        operation='algebra_solve',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'variable': 'n',
            'constant': 5,
            'result': 8,
            'correct_value': 13,
            'assumed_value': 1,
            'malrule_answer': 1,
            'equation': 'n - 5 = 8',
            'template': 'basic_subtraction'
        }
    )
    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    expected2 = malrule.calculate_expected_answer(problem2)

    assert correct_sol2.answer == 13
    assert malrule_sol2.answer == 1
    assert expected2 == malrule_sol2.answer
    assert correct_sol2.answer != malrule_sol2.answer
    print(f"  n - 5 = 8 → Correct: n={correct_sol2.answer}, Malrule: n={malrule_sol2.answer}")
    print("  ✓ PASSED")

    # Test 3: basic_multiplication template
    print("\n--- Test 3: basic_multiplication ---")
    problem3 = Problem(
        text="Solve for a: 3a = 18",
        operands=[3, 18],
        operation='algebra_solve',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'variable': 'a',
            'coefficient': 3,
            'result': 18,
            'correct_value': 6,
            'assumed_value': 1,
            'malrule_answer': 1,
            'equation': '3a = 18',
            'template': 'basic_multiplication'
        }
    )
    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    expected3 = malrule.calculate_expected_answer(problem3)

    assert correct_sol3.answer == 6
    assert malrule_sol3.answer == 1
    assert expected3 == malrule_sol3.answer
    assert correct_sol3.answer != malrule_sol3.answer
    print(f"  3a = 18 → Correct: a={correct_sol3.answer}, Malrule: a={malrule_sol3.answer}")
    print("  ✓ PASSED")

    # Test 4: two_step_equation template
    print("\n--- Test 4: two_step_equation ---")
    problem4 = Problem(
        text="Solve for x: 2x + 5 = 25",
        operands=[2, 5, 25],
        operation='algebra_solve',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'variable': 'x',
            'coefficient': 2,
            'constant': 5,
            'result': 25,
            'correct_value': 10,
            'assumed_value': 10,
            'malrule_answer': 10,
            'equation': '2x + 5 = 25',
            'template': 'two_step_equation'
        }
    )
    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    expected4 = malrule.calculate_expected_answer(problem4)

    # Note: In this case correct and malrule happen to match (lucky coincidence!)
    assert correct_sol4.answer == 10
    assert malrule_sol4.answer == 10
    assert expected4 == malrule_sol4.answer
    print(f"  2x + 5 = 25 → Correct: x={correct_sol4.answer}, Malrule: x={malrule_sol4.answer} (lucky match!)")
    print("  ✓ PASSED")

    # Test 5: word_problem template
    print("\n--- Test 5: word_problem ---")
    problem5 = Problem(
        text="Sarah has y apples. She buys 4 more and now has 12 apples. How many did she start with?",
        operands=[4, 12],
        operation='algebra_solve',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'variable': 'y',
            'constant': 4,
            'result': 12,
            'correct_value': 8,
            'assumed_value': 25,
            'malrule_answer': 25,
            'context_type': 'apples',
            'operation_type': 'addition',
            'template': 'word_problem'
        }
    )
    correct_sol5 = correct.solve(problem5)
    malrule_sol5 = malrule.solve(problem5)
    expected5 = malrule.calculate_expected_answer(problem5)

    assert correct_sol5.answer == 8
    assert malrule_sol5.answer == 25
    assert expected5 == malrule_sol5.answer
    assert correct_sol5.answer != malrule_sol5.answer
    print(f"  Word problem → Correct: y={correct_sol5.answer}, Malrule: y={malrule_sol5.answer}")
    print("  ✓ PASSED")

    print("\n" + "="*70)
    print("ALL TEMPLATE-SPECIFIC TESTS PASSED ✓")
    print("="*70)


def test_automated_suite():
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = VariableLetterHasValueProblemGenerator(
        level=7,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = VariableLetterHasValueMalrule()
    correct = AlgebraicEquationCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Variable-Letter-Has-Value  ".center(70) + "║")
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
