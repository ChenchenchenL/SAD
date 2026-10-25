#!/usr/bin/env python3
"""Test script for Forget-Negative-Division malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.algebra.forget_negative_division import (
    ForgetNegativeDivisionProblemGenerator,
    ForgetNegativeDivisionMalrule,
    InequalitySolvingCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING FORGET-NEGATIVE-DIVISION")
    print("="*70)

    malrule = ForgetNegativeDivisionMalrule()
    correct = InequalitySolvingCorrectAlgorithm()

    # Test case 1: -2x < 6 → x > -3 (correct), x < -3 (malrule)
    problem1 = Problem(
        text="Solve for x: -2x < 6",
        operands=[-2, 6],
        operation='inequality_solve',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': -2,
            'constant': 6,
            'inequality_sign': '<',
            'solution_value': -3,
            'correct_sign': '>',  # Flipped!
            'malrule_sign': '<',  # Not flipped
            'inequality': '-2x < 6'
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: -2x < 6 → Correct: {correct_sol.answer}, Malrule: {malrule_sol.answer}")
    assert correct_sol.answer == "x > -3"
    assert malrule_sol.answer == "x < -3"
    assert correct_sol.answer != malrule_sol.answer
    print("✓ PASSED")

    # Test case 2: -3x > 9 → x < -3 (correct), x > -3 (malrule)
    problem2 = Problem(
        text="Solve for x: -3x > 9",
        operands=[-3, 9],
        operation='inequality_solve',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': -3,
            'constant': 9,
            'inequality_sign': '>',
            'solution_value': -3,
            'correct_sign': '<',  # Flipped!
            'malrule_sign': '>',  # Not flipped
            'inequality': '-3x > 9'
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert correct_sol2.answer == "x < -3"
    assert malrule_sol2.answer == "x > -3"
    print("✓ TEST 2 PASSED")

    # Test case 3: -x ≤ 5 → x ≥ -5 (correct), x ≤ -5 (malrule)
    problem3 = Problem(
        text="Solve for x: -x ≤ 5",
        operands=[-1, 5],
        operation='inequality_solve',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': -1,
            'constant': 5,
            'inequality_sign': '≤',
            'solution_value': -5,
            'correct_sign': '≥',  # Flipped!
            'malrule_sign': '≤',  # Not flipped
            'inequality': '-x ≤ 5'
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert correct_sol3.answer == "x ≥ -5"
    assert malrule_sol3.answer == "x ≤ -5"
    print("✓ TEST 3 PASSED")

    # Test case 4: -4x ≥ 12 → x ≤ -3 (correct), x ≥ -3 (malrule)
    problem4 = Problem(
        text="Solve for x: -4x ≥ 12",
        operands=[-4, 12],
        operation='inequality_solve',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': -4,
            'constant': 12,
            'inequality_sign': '≥',
            'solution_value': -3,
            'correct_sign': '≤',  # Flipped!
            'malrule_sign': '≥',  # Not flipped
            'inequality': '-4x ≥ 12'
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    assert correct_sol4.answer == "x ≤ -3"
    assert malrule_sol4.answer == "x ≥ -3"
    print("✓ TEST 4 PASSED")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_new_templates():
    """Test new template enhancements."""
    print("\n\n" + "="*70)
    print("TESTING NEW TEMPLATE ENHANCEMENTS")
    print("="*70)

    malrule = ForgetNegativeDivisionMalrule()
    correct = InequalitySolvingCorrectAlgorithm()

    # Test 1: Two-step inequality (-3x + 5 > 11)
    print("\nTEST 1: Two-step inequality (-3x + 5 > 11)")
    print("-"*70)
    problem1 = Problem(
        text="Solve for x: -3x + 5 > 11",
        operands=[-3, 5, 11],
        operation='inequality_solve',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': -3,
            'added_constant': 5,
            'rhs_constant': 11,
            'inequality_sign': '>',
            'solution_value': -2,  # (11-5)/-3 = 6/-3 = -2
            'correct_sign': '<',  # Flipped
            'malrule_sign': '>',  # Not flipped
            'inequality': '-3x + 5 > 11',
            'template': 'two_step'
        }
    )

    correct_sol1 = correct.solve(problem1)
    malrule_sol1 = malrule.solve(problem1)
    expected_mal1 = malrule.calculate_expected_answer(problem1)

    print(f"Correct answer: {correct_sol1.answer}")
    print(f"Malrule answer: {malrule_sol1.answer}")
    print(f"Expected malrule: {expected_mal1}")
    assert correct_sol1.answer == "x < -2"
    assert malrule_sol1.answer == "x > -2"
    assert malrule_sol1.answer == expected_mal1
    print("✓ TEST 1 PASSED")

    # Test 2: Fraction coefficient (-1/2x < 6)
    print("\nTEST 2: Fraction coefficient (-1/2x < 6)")
    print("-"*70)
    problem2 = Problem(
        text="Solve for x: -1/2x < 6",
        operands=[-1, 2, 6],
        operation='inequality_solve',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': '-1/2',
            'constant': 6,
            'inequality_sign': '<',
            'solution_value': -12,  # 6 * (-2) = -12
            'correct_sign': '>',  # Flipped
            'malrule_sign': '<',  # Not flipped
            'inequality': '-1/2x < 6',
            'template': 'fraction_coefficient',
            'denominator': 2
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    expected_mal2 = malrule.calculate_expected_answer(problem2)

    print(f"Correct answer: {correct_sol2.answer}")
    print(f"Malrule answer: {malrule_sol2.answer}")
    print(f"Expected malrule: {expected_mal2}")
    assert correct_sol2.answer == "x > -12"
    assert malrule_sol2.answer == "x < -12"
    assert malrule_sol2.answer == expected_mal2
    print("✓ TEST 2 PASSED")

    # Test 3: Word problem (temperature context)
    print("\nTEST 3: Word problem (temperature context)")
    print("-"*70)
    problem3 = Problem(
        text="The temperature is 3 times a number x and is less than 15 C. Solve for x.",
        operands=[-3, 15],
        operation='inequality_solve',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'coefficient': -3,
            'constant': 15,
            'inequality_sign': '<',
            'solution_value': -5,  # 15/-3 = -5
            'correct_sign': '>',  # Flipped
            'malrule_sign': '<',  # Not flipped
            'inequality': '-3x < 15',
            'template': 'word_problem',
            'context': 'temperature'
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    expected_mal3 = malrule.calculate_expected_answer(problem3)

    print(f"Correct answer: {correct_sol3.answer}")
    print(f"Malrule answer: {malrule_sol3.answer}")
    print(f"Expected malrule: {expected_mal3}")
    assert correct_sol3.answer == "x > -5"
    assert malrule_sol3.answer == "x < -5"
    assert malrule_sol3.answer == expected_mal3
    print("✓ TEST 3 PASSED")

    print("\n" + "="*70)
    print("ALL NEW TEMPLATE TEST CASES PASSED ✓")
    print("="*70)


def test_all_templates():
    """Test all problem templates to ensure coverage."""
    print("\n\n" + "="*70)
    print("TESTING ALL TEMPLATES")
    print("="*70)

    problem_gen = ForgetNegativeDivisionProblemGenerator(
        level=8,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = ForgetNegativeDivisionMalrule()
    correct = InequalitySolvingCorrectAlgorithm()

    templates = ['basic_one_step', 'two_step', 'fraction_coefficient', 'word_problem']
    all_passed = True

    for template in templates:
        print(f"\n{'='*70}")
        print(f"Testing template: {template}")
        print('='*70)

        # Generate multiple problems for each template
        for i in range(3):
            seed = hash(f"{template}_{i}") % 10000
            problem = problem_gen.generate(seed=seed)

            # Check if it's the right template
            actual_template = problem.metadata.get('template', 'basic_one_step')
            if actual_template != template:
                continue

            print(f"\nTest {i+1} - {template}:")
            print(f"  Problem: {problem.text}")

            try:
                correct_sol = correct.solve(problem)
                malrule_sol = malrule.solve(problem)

                # Check that answers are different (they should be for this malrule)
                if correct_sol.answer == malrule_sol.answer:
                    print(f"  ⚠ WARNING: Malrule produced same answer as correct!")
                    print(f"  This might be an edge case where the misconception doesn't matter.")
                    print(f"\n  Correct steps:")
                    for step in correct_sol.steps:
                        print(f"    {step}")
                    print(f"\n  Malrule steps:")
                    for step in malrule_sol.steps:
                        print(f"    {step}")
                    all_passed = False
                    continue

                print(f"  ✓ Correct answer: {correct_sol.answer}")
                print(f"  ✓ Malrule answer: {malrule_sol.answer}")
                print(f"  ✓ Answers differ as expected")

            except Exception as e:
                print(f"  ✗ FAILED with error: {e}")
                import traceback
                traceback.print_exc()
                print(f"\n  Expected correct answer from metadata: x {problem.metadata.get('correct_sign', '?')} {problem.metadata.get('solution_value', '?')}")
                print(f"  Expected malrule answer from metadata: x {problem.metadata.get('malrule_sign', '?')} {problem.metadata.get('solution_value', '?')}")
                all_passed = False

    if all_passed:
        print("\n" + "="*70)
        print("✓✓✓ ALL TEMPLATE TESTS PASSED ✓✓✓")
        print("="*70)
    else:
        print("\n" + "="*70)
        print("✗✗✗ SOME TEMPLATE TESTS FAILED ✗✗✗")
        print("="*70)

    return all_passed


def test_automated_suite():
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = ForgetNegativeDivisionProblemGenerator(
        level=8,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = ForgetNegativeDivisionMalrule()
    correct = InequalitySolvingCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Forget-Negative-Division  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    try:
        test_specific_examples()
        test_new_templates()
        template_passed = test_all_templates()
        suite_passed = test_automated_suite()
        all_passed = template_passed and suite_passed
        print("\n\n╔" + "═"*68 + "╗")
        if all_passed:
            print("║" + "  ✓✓✓ VERIFICATION COMPLETE ✓✓✓  ".center(70) + "║")
        else:
            print("║" + "  ✗✗✗ SOME TESTS FAILED ✗✗✗  ".center(70) + "║")
        print("╚" + "═"*68 + "╝\n")
        return 0 if all_passed else 1
    except Exception as e:
        print(f"\n✗✗✗ TEST FAILED: {e} ✗✗✗")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
