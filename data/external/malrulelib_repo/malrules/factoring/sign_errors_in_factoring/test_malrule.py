#!/usr/bin/env python3
"""Test script for Sign-Errors-In-Factoring malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.factoring.sign_errors_in_factoring import (
    SignErrorsInFactoringProblemGenerator,
    SignErrorsInFactoringMalrule,
    QuadraticFactoringCorrectAlgorithm
)


def test_all_templates():
    """Test all problem templates comprehensively."""
    print("="*70)
    print("TESTING ALL PROBLEM TEMPLATES")
    print("="*70)

    malrule = SignErrorsInFactoringMalrule()
    correct = QuadraticFactoringCorrectAlgorithm()

    # Define all test cases for each template
    test_cases = [
        {
            'name': 'both_positive',
            'problem': Problem(
                text="Factor: x² + 5x + 6",
                operands=[1, 5, 6],
                operation='factoring',
                level=9,
                difficulty=DifficultyLevel.EASY,
                metadata={
                    'quadratic': 'x² + 5x + 6',
                    'a': 1,
                    'b': 5,
                    'c': 6,
                    'p': 2,
                    'q': 3,
                    'sign_pattern': 'both_positive',
                    'problem_type': 'both_positive',
                    'correct_factored': '(x + 2)(x + 3)',
                    'malrule_factored': '(x - 2)(x - 3)'
                }
            )
        },
        {
            'name': 'both_negative',
            'problem': Problem(
                text="Factor: x² - 5x + 6",
                operands=[1, -5, 6],
                operation='factoring',
                level=9,
                difficulty=DifficultyLevel.MEDIUM,
                metadata={
                    'quadratic': 'x² - 5x + 6',
                    'a': 1,
                    'b': -5,
                    'c': 6,
                    'p': 2,
                    'q': 3,
                    'sign_pattern': 'both_negative',
                    'problem_type': 'both_negative',
                    'correct_factored': '(x - 2)(x - 3)',
                    'malrule_factored': '(x + 2)(x + 3)'
                }
            )
        },
        {
            'name': 'one_negative',
            'problem': Problem(
                text="Factor: x² + x - 6",
                operands=[1, 1, -6],
                operation='factoring',
                level=9,
                difficulty=DifficultyLevel.MEDIUM,
                metadata={
                    'quadratic': 'x² + x - 6',
                    'a': 1,
                    'b': 1,
                    'c': -6,
                    'p': 3,
                    'q': 2,
                    'sign_pattern': 'one_negative',
                    'problem_type': 'one_negative',
                    'correct_factored': '(x + 3)(x - 2)',
                    'malrule_factored': '(x - 3)(x + 2)'
                }
            )
        },
        {
            'name': 'difference_of_squares',
            'problem': Problem(
                text="Factor: x² - 16",
                operands=[1, 0, -16],
                operation='factoring',
                level=9,
                difficulty=DifficultyLevel.MEDIUM,
                metadata={
                    'quadratic': 'x² - 16',
                    'a': 1,
                    'b': 0,
                    'c': -16,
                    'k': 4,
                    'sign_pattern': 'difference_of_squares',
                    'problem_type': 'difference_of_squares',
                    'correct_factored': '(x - 4)(x + 4)',
                    'malrule_factored': '(x + 4)(x + 4)'  # One possible wrong answer
                }
            )
        },
        {
            'name': 'perfect_square_trinomial_positive',
            'problem': Problem(
                text="Factor: x² + 8x + 16",
                operands=[1, 8, 16],
                operation='factoring',
                level=9,
                difficulty=DifficultyLevel.HARD,
                metadata={
                    'quadratic': 'x² + 8x + 16',
                    'a': 1,
                    'b': 8,
                    'c': 16,
                    'k': 4,
                    'sign_pattern': 'perfect_square_trinomial',
                    'problem_type': 'perfect_square_trinomial',
                    'correct_factored': '(x + 4)²',
                    'malrule_factored': '(x - 4)²'
                }
            )
        },
        {
            'name': 'perfect_square_trinomial_negative',
            'problem': Problem(
                text="Factor: x² - 8x + 16",
                operands=[1, -8, 16],
                operation='factoring',
                level=9,
                difficulty=DifficultyLevel.HARD,
                metadata={
                    'quadratic': 'x² - 8x + 16',
                    'a': 1,
                    'b': -8,
                    'c': 16,
                    'k': 4,
                    'sign_pattern': 'perfect_square_trinomial',
                    'problem_type': 'perfect_square_trinomial',
                    'correct_factored': '(x - 4)²',
                    'malrule_factored': '(x + 4)²'
                }
            )
        },
        {
            'name': 'leading_coefficient_not_one',
            'problem': Problem(
                text="Factor: 2x² + 7x + 3",
                operands=[2, 7, 3],
                operation='factoring',
                level=9,
                difficulty=DifficultyLevel.HARD,
                metadata={
                    'quadratic': '2x² + 7x + 3',
                    'a': 2,
                    'b': 7,
                    'c': 3,
                    'p': 1,
                    'q': 3,
                    'sign_pattern': 'leading_coefficient_not_one',
                    'problem_type': 'leading_coefficient_not_one',
                    'correct_factored': '(2x + 1)(x + 3)',
                    'malrule_factored': '(2x - 1)(x - 3)'
                }
            )
        },
        {
            'name': 'word_problem_context',
            'problem': Problem(
                text="A rectangle has an area of x² + 5x + 6. Find expressions for its length and width.",
                operands=[1, 5, 6],
                operation='factoring',
                level=9,
                difficulty=DifficultyLevel.MEDIUM,
                metadata={
                    'quadratic': 'x² + 5x + 6',
                    'a': 1,
                    'b': 5,
                    'c': 6,
                    'p': 2,
                    'q': 3,
                    'sign_pattern': 'word_problem_context',
                    'problem_type': 'word_problem_context',
                    'correct_factored': '(x + 2)(x + 3)',
                    'malrule_factored': '(x - 2)(x - 3)',
                    'context': 'area'
                }
            )
        }
    ]

    all_passed = True
    for test_case in test_cases:
        test_name = test_case['name']
        problem = test_case['problem']
        expected_correct = problem.metadata['correct_factored']
        expected_malrule = problem.metadata['malrule_factored']

        print(f"\n{'='*70}")
        print(f"TEST: {test_name}")
        print(f"Problem: {problem.text}")
        print(f"{'='*70}")

        try:
            # Solve with correct algorithm
            correct_sol = correct.solve(problem)
            malrule_sol = malrule.solve(problem)

            # Check if answers match expected
            correct_matches = correct_sol.answer == expected_correct
            malrule_matches = malrule_sol.answer == expected_malrule

            # EDGE CASE: Check if malrule produced same answer as correct
            if correct_sol.answer == malrule_sol.answer:
                print("\n⚠️  EDGE CASE DETECTED: Malrule produced same answer as correct!")
                print("\nCorrect Algorithm Steps:")
                for step in correct_sol.steps:
                    print(f"  {step}")
                print("\nMalrule Algorithm Steps:")
                for step in malrule_sol.steps:
                    print(f"  {step}")
                print(f"\nExpected correct: {expected_correct}")
                print(f"Expected malrule: {expected_malrule}")
                print("\n✗ TEST FAILED - Malrule should produce different answer\n")
                all_passed = False
                continue

            # Check if both match expected
            if correct_matches and malrule_matches:
                print(f"\n✓ TEST PASSED")
                print(f"  Correct answer: {correct_sol.answer}")
                print(f"  Malrule answer: {malrule_sol.answer}")
            else:
                print(f"\n✗ TEST FAILED")
                print(f"\nExpected:")
                print(f"  Correct: {expected_correct}")
                print(f"  Malrule: {expected_malrule}")
                print(f"\nActual:")
                print(f"  Correct: {correct_sol.answer} {'✓' if correct_matches else '✗'}")
                print(f"  Malrule: {malrule_sol.answer} {'✓' if malrule_matches else '✗'}")

                print("\nCorrect Algorithm Steps:")
                for step in correct_sol.steps:
                    print(f"  {step}")

                print("\nMalrule Algorithm Steps:")
                for step in malrule_sol.steps:
                    print(f"  {step}")

                all_passed = False

        except Exception as e:
            print(f"\n✗ TEST FAILED WITH EXCEPTION: {e}")
            import traceback
            traceback.print_exc()
            all_passed = False

    print("\n" + "="*70)
    if all_passed:
        print("ALL TEMPLATE TESTS PASSED ✓")
    else:
        print("SOME TESTS FAILED ✗")
    print("="*70)

    return all_passed


def test_generated_problems():
    """Test problems generated by the problem generator for each template type."""
    print("\n" + "="*70)
    print("TESTING GENERATED PROBLEMS")
    print("="*70)

    problem_gen = SignErrorsInFactoringProblemGenerator(
        level=10,
        difficulty=DifficultyLevel.HARD
    )
    malrule = SignErrorsInFactoringMalrule()
    correct = QuadraticFactoringCorrectAlgorithm()

    # Generate problems and track which templates we've tested
    templates_tested = {}
    max_attempts = 200
    problems_per_template = 3

    for i in range(max_attempts):
        problem = problem_gen.generate(seed=70000 + i)
        problem_type = problem.metadata.get('problem_type', 'unknown')

        # Track templates
        if problem_type not in templates_tested:
            templates_tested[problem_type] = []

        # Only test a few per template
        if len(templates_tested[problem_type]) >= problems_per_template:
            continue

        templates_tested[problem_type].append(problem)

    # Test each template's problems
    all_passed = True
    for template_type, problems in templates_tested.items():
        print(f"\n{'='*70}")
        print(f"Template: {template_type} ({len(problems)} problems)")
        print(f"{'='*70}")

        for idx, problem in enumerate(problems):
            try:
                correct_sol = correct.solve(problem)
                malrule_sol = malrule.solve(problem)

                # Check they produce different answers
                if correct_sol.answer == malrule_sol.answer:
                    print(f"\n✗ Problem {idx + 1} FAILED - Same answer!")
                    print(f"  Problem: {problem.text}")
                    print(f"  Answer: {correct_sol.answer}")
                    print("\nCorrect Steps:")
                    for step in correct_sol.steps:
                        print(f"  {step}")
                    print("\nMalrule Steps:")
                    for step in malrule_sol.steps:
                        print(f"  {step}")
                    all_passed = False
                else:
                    print(f"\n✓ Problem {idx + 1} PASSED")
                    print(f"  Problem: {problem.text}")
                    print(f"  Correct: {correct_sol.answer}")
                    print(f"  Malrule: {malrule_sol.answer}")

            except Exception as e:
                print(f"\n✗ Problem {idx + 1} FAILED WITH EXCEPTION: {e}")
                print(f"  Problem: {problem.text}")
                import traceback
                traceback.print_exc()
                all_passed = False

    # Check all templates were tested
    expected_templates = {
        'both_positive', 'both_negative', 'one_negative',
        'leading_coefficient_not_one', 'difference_of_squares',
        'perfect_square_trinomial', 'word_problem_context'
    }

    print(f"\n{'='*70}")
    print("Template Coverage:")
    print(f"{'='*70}")
    for template in expected_templates:
        if template in templates_tested:
            print(f"✓ {template}: {len(templates_tested[template])} problems tested")
        else:
            print(f"✗ {template}: NOT TESTED")
            all_passed = False

    print("\n" + "="*70)
    if all_passed:
        print("ALL GENERATED PROBLEM TESTS PASSED ✓")
    else:
        print("SOME TESTS FAILED ✗")
    print("="*70)

    return all_passed


def test_automated_suite():
    """Run the automated test suite."""
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = SignErrorsInFactoringProblemGenerator(
        level=9,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = SignErrorsInFactoringMalrule()
    correct = QuadraticFactoringCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    else:
        print("\n✗✗✗ SOME AUTOMATED TESTS FAILED ✗✗✗")
        for r in results:
            if not r.passed:
                print(f"\nFailed test: {r}")

    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Sign-Errors-In-Factoring  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    try:
        # Test all templates with specific examples
        all_templates_passed = test_all_templates()

        # Test generated problems for each template
        generated_passed = test_generated_problems()

        # Run automated suite
        automated_passed = test_automated_suite()

        # Final result
        all_passed = all_templates_passed and generated_passed and automated_passed

        print("\n\n╔" + "═"*68 + "╗")
        if all_passed:
            print("║" + "  ✓✓✓ VERIFICATION COMPLETE - ALL TESTS PASSED ✓✓✓  ".center(70) + "║")
        else:
            print("║" + "  ✗✗✗ VERIFICATION FAILED - SOME TESTS FAILED ✗✗✗  ".center(70) + "║")
        print("╚" + "═"*68 + "╝\n")

        return 0 if all_passed else 1
    except Exception as e:
        print(f"\n✗✗✗ TEST FAILED: {e} ✗✗✗")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
