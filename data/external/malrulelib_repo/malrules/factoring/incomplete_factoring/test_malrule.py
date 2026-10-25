#!/usr/bin/env python3
"""Test script for Incomplete-Factoring malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.factoring.incomplete_factoring import (
    IncompleteFactoringProblemGenerator,
    IncompleteFactoringMalrule,
    CompleteFactoringCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING INCOMPLETE-FACTORING")
    print("="*70)

    malrule = IncompleteFactoringMalrule()
    correct = CompleteFactoringCorrectAlgorithm()

    # Test case 1: 2x² - 8 = 2(x² - 4) (incomplete), 2(x+2)(x-2) (complete)
    problem1 = Problem(
        text="Factor completely: 2x² - 8",
        operands=[2, 8],
        operation='factoring',
        level=8,
        difficulty=DifficultyLevel.EASY,
        metadata={
            'gcf': 2,
            'b': 2,
            'coefficient': 2,
            'constant': 8,
            'expression': '2x² - 8',
            'incomplete_answer': '2(x² - 4)',
            'complete_answer': '2(x + 2)(x - 2)'
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: 2x² - 8 → Complete: {correct_sol.answer}, Incomplete: {malrule_sol.answer}")
    assert correct_sol.answer == '2(x + 2)(x - 2)'
    assert malrule_sol.answer == '2(x² - 4)'
    assert correct_sol.answer != malrule_sol.answer
    print("✓ PASSED")

    # Test case 2: 3x² - 12 = 3(x² - 4) (incomplete), 3(x+2)(x-2) (complete)
    problem2 = Problem(
        text="Factor completely: 3x² - 12",
        operands=[3, 12],
        operation='factoring',
        level=8,
        difficulty=DifficultyLevel.EASY,
        metadata={
            'gcf': 3,
            'b': 2,
            'coefficient': 3,
            'constant': 12,
            'expression': '3x² - 12',
            'incomplete_answer': '3(x² - 4)',
            'complete_answer': '3(x + 2)(x - 2)'
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert correct_sol2.answer == '3(x + 2)(x - 2)'
    assert malrule_sol2.answer == '3(x² - 4)'
    print("✓ TEST 2 PASSED")

    # Test case 3: 2x² - 18 = 2(x² - 9) (incomplete), 2(x+3)(x-3) (complete)
    problem3 = Problem(
        text="Factor completely: 2x² - 18",
        operands=[2, 18],
        operation='factoring',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'gcf': 2,
            'b': 3,
            'coefficient': 2,
            'constant': 18,
            'expression': '2x² - 18',
            'incomplete_answer': '2(x² - 9)',
            'complete_answer': '2(x + 3)(x - 3)'
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert correct_sol3.answer == '2(x + 3)(x - 3)'
    assert malrule_sol3.answer == '2(x² - 9)'
    print("✓ TEST 3 PASSED")

    # Test case 4: 5x² - 20 = 5(x² - 4) (incomplete), 5(x+2)(x-2) (complete)
    problem4 = Problem(
        text="Factor completely: 5x² - 20",
        operands=[5, 20],
        operation='factoring',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'gcf': 5,
            'b': 2,
            'coefficient': 5,
            'constant': 20,
            'expression': '5x² - 20',
            'incomplete_answer': '5(x² - 4)',
            'complete_answer': '5(x + 2)(x - 2)'
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    assert correct_sol4.answer == '5(x + 2)(x - 2)'
    assert malrule_sol4.answer == '5(x² - 4)'
    print("✓ TEST 4 PASSED")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_all_templates():
    """Test all 5 templates for Incomplete-Factoring."""
    print("\n\n" + "="*70)
    print("TESTING ALL TEMPLATES")
    print("="*70)

    problem_gen = IncompleteFactoringProblemGenerator(
        level=9,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = IncompleteFactoringMalrule()
    correct = CompleteFactoringCorrectAlgorithm()

    templates = problem_gen.get_available_templates()
    print(f"\nFound {len(templates)} templates: {templates}")
    assert len(templates) == 5, f"Expected 5 templates, got {len(templates)}"

    for template in templates:
        print(f"\n--- Testing template: {template} ---")

        # Generate problem with this template
        problem = problem_gen.generate(seed=42, template=template)

        # Solve with both algorithms
        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        # Verify different answers
        print(f"  Correct answer: {correct_sol.answer}")
        print(f"  Malrule answer: {malrule_sol.answer}")

        assert str(correct_sol.answer) != str(malrule_sol.answer), \
            f"Template {template}: Correct and malrule answers should be different!"

        # Verify calculate_expected_answer matches malrule output
        expected = malrule.calculate_expected_answer(problem)
        print(f"  Expected answer: {expected}")

        assert str(malrule_sol.answer) == str(expected), \
            f"Template {template}: calculate_expected_answer() returned {expected} but malrule produced {malrule_sol.answer}"

        print(f"  ✓ Template {template} PASSED")

    print("\n" + "="*70)
    print("ALL TEMPLATE TESTS PASSED ✓")
    print("="*70)


def test_word_problems():
    """Test word problems covering all formula types."""
    print("\n\n" + "="*70)
    print("TESTING WORD PROBLEMS (ALL FORMULA TYPES)")
    print("="*70)

    problem_gen = IncompleteFactoringProblemGenerator(
        level=9,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = IncompleteFactoringMalrule()
    correct = CompleteFactoringCorrectAlgorithm()

    # Test each formula type in word problems
    formula_types = ['gcf_then_difference_of_squares', 'gcf_then_trinomial',
                     'gcf_then_perfect_square', 'nested_factoring']

    for formula_type in formula_types:
        print(f"\nTesting word problem with formula type: {formula_type}")

        # Generate word problems with specific formula types
        for variant in range(3):
            # Set seed to get consistent results
            problem = problem_gen.generate(seed=1000 + variant, template='word_problem')

            # Check metadata
            assert problem.metadata.get('is_word_problem') == True
            assert 'word_problem_type' in problem.metadata
            assert 'word_problem_variant' in problem.metadata

            # Solve
            correct_sol = correct.solve(problem)
            malrule_sol = malrule.solve(problem)

            # Verify answers are different
            assert correct_sol.answer != malrule_sol.answer

            print(f"  Variant {variant}: ✓ Generated and solved correctly")

    print("\n" + "="*70)
    print("ALL WORD PROBLEM TESTS PASSED ✓")
    print("="*70)


def test_automated_suite():
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = IncompleteFactoringProblemGenerator(
        level=9,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = IncompleteFactoringMalrule()
    correct = CompleteFactoringCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Incomplete-Factoring  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    try:
        test_specific_examples()
        test_all_templates()
        test_word_problems()
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
