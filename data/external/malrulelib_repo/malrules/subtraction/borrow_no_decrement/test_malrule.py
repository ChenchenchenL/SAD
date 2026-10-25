#!/usr/bin/env python3
"""
Test script for Borrow-No-Decrement malrule.

Run from project root: python3 -m malrules.subtraction.borrow_no_decrement.test_malrule
Or from this directory: python3 test_malrule.py

This script demonstrates and tests the subtraction borrowing malrule
with clear examples and verification.
"""

import sys
import os
import random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.subtraction.borrow_no_decrement import (
    BorrowNoDecrementProblemGenerator,
    BorrowNoDecrementMalrule,
    SubtractionCorrectAlgorithm
)


def print_steps(label, steps):
    """Print solution steps with a label."""
    print(f"\n--- {label} ---")
    for step in steps:
        print(f"  {step}")


def test_single_problem(problem, correct, malrule, expected_correct, expected_malrule=None,
                        allow_same_answer=False):
    """
    Test a single problem and print detailed output.

    Args:
        problem: The problem to test
        correct: Correct algorithm instance
        malrule: Malrule algorithm instance
        expected_correct: Expected correct answer (as int or str)
        expected_malrule: Expected malrule answer (optional, as int or str)
        allow_same_answer: If True, allow malrule to produce same answer as correct

    Returns:
        True if test passed, False otherwise
    """
    correct_sol = correct.solve(problem)
    malrule_sol = malrule.solve(problem)

    correct_answer = str(correct_sol.answer)
    malrule_answer = str(malrule_sol.answer)
    expected_correct_str = str(expected_correct)

    print(f"Problem: {problem.text}")
    print(f"Correct answer: {correct_answer}")
    print(f"Malrule answer: {malrule_answer}")

    # Check correct answer
    if correct_answer != expected_correct_str:
        print(f"\n✗ FAILED: Correct algorithm gave {correct_answer}, expected {expected_correct_str}")
        print_steps("Correct Steps", correct_sol.steps)
        return False

    # Check if malrule produces different answer (unless allow_same_answer is True)
    if not allow_same_answer and correct_answer == malrule_answer:
        print(f"\n✗ FAILED: Malrule produced same answer as correct algorithm!")
        print("  This might indicate an edge case where the malrule accidentally works.")
        print_steps("Correct Steps", correct_sol.steps)
        print_steps("Malrule Steps", malrule_sol.steps)
        return False

    # Check expected malrule answer if provided
    if expected_malrule is not None:
        expected_malrule_str = str(expected_malrule)
        if malrule_answer != expected_malrule_str:
            print(f"\n✗ FAILED: Malrule gave {malrule_answer}, expected {expected_malrule_str}")
            print_steps("Correct Steps", correct_sol.steps)
            print_steps("Malrule Steps", malrule_sol.steps)
            return False

    print(f"✓ PASSED (correct: {correct_answer}, malrule: {malrule_answer})")
    return True


def test_specific_examples():
    """Test with specific, well-known examples."""
    print("=" * 70)
    print("TESTING BORROW-NO-DECREMENT WITH SPECIFIC EXAMPLES")
    print("=" * 70)

    malrule = BorrowNoDecrementMalrule()
    correct = SubtractionCorrectAlgorithm()
    all_passed = True

    # Test case 1: Classic example - 62 - 37
    print("\nTEST CASE 1: 62 - 37 (Classic example)")
    print("-" * 70)
    problem1 = Problem(
        text="What is 62 - 37?",
        operands=[62, 37],
        operation='subtraction',
        level=3,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={'template': 'basic'}
    )
    # Expected: 62 - 37 = 25 (correct)
    # Malrule: 12-7=5, 6-3=3 (forgot to decrement) = 35
    if not test_single_problem(problem1, correct, malrule, 25, 35):
        all_passed = False

    # Test case 2: Multiple borrowing - 453 - 394
    print("\n\nTEST CASE 2: 453 - 394 (Multiple borrowing)")
    print("-" * 70)
    problem2 = Problem(
        text="What is 453 - 394?",
        operands=[453, 394],
        operation='subtraction',
        level=4,
        difficulty=DifficultyLevel.HARD,
        metadata={'template': 'basic'}
    )
    # 453 - 394 = 59 (correct)
    # Malrule: 13-4=9, 5-9->borrow 15-9=6, 4-3=1 = 169 (no decrement)
    if not test_single_problem(problem2, correct, malrule, 59, 169):
        all_passed = False

    # Test case 3: Simple borrowing - 52 - 27
    print("\n\nTEST CASE 3: 52 - 27 (Simple borrowing)")
    print("-" * 70)
    problem3 = Problem(
        text="What is 52 - 27?",
        operands=[52, 27],
        operation='subtraction',
        level=2,
        difficulty=DifficultyLevel.EASY,
        metadata={'template': 'basic'}
    )
    # 52 - 27 = 25 (correct), Malrule: 12-7=5, 5-2=3 = 35
    if not test_single_problem(problem3, correct, malrule, 25, 35):
        all_passed = False

    # Test case 4: Multi-digit large (4 digits)
    print("\n\nTEST CASE 4: 5432 - 2187 (Multi-digit large)")
    print("-" * 70)
    problem4 = Problem(
        text="What is 5432 - 2187?",
        operands=[5432, 2187],
        operation='subtraction',
        level=4,
        difficulty=DifficultyLevel.HARD,
        metadata={'template': 'basic'}
    )
    # 5432 - 2187 = 3245 (correct)
    # Malrule: 12-7=5, 3-8->borrow 13-8=5, 4-1=3, 5-2=3 = 3355
    if not test_single_problem(problem4, correct, malrule, 3245, 3355):
        all_passed = False

    # Test case 5: Word problem context
    print("\n\nTEST CASE 5: 325 - 148 (Word problem)")
    print("-" * 70)
    problem5 = Problem(
        text="A store had 325 items. After selling 148 items, how many remain?",
        operands=[325, 148],
        operation='subtraction',
        level=3,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={'template': 'word_problem'}
    )
    # 325 - 148 = 177 (correct)
    # Malrule: 15-8=7, 2-4->borrow 12-4=8, 3-1=2 = 287
    if not test_single_problem(problem5, correct, malrule, 177, 287):
        all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print("ALL SPECIFIC TEST CASES PASSED ✓")
    else:
        print("SOME SPECIFIC TEST CASES FAILED ✗")
    print("=" * 70)

    return all_passed


def test_all_templates():
    """Test that all problem templates generate valid problems."""
    print("\n\n" + "=" * 70)
    print("TESTING ALL PROBLEM TEMPLATES")
    print("=" * 70)

    problem_gen = BorrowNoDecrementProblemGenerator(
        level=3,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = BorrowNoDecrementMalrule()
    correct = SubtractionCorrectAlgorithm()

    # Generate many problems and track templates
    templates_seen = set()
    template_results = {}

    # Generate problems with different seeds to try to hit all templates
    for seed in range(100):
        random.seed(seed)
        problem = problem_gen.generate(seed=seed)
        template = problem.metadata.get('problem_type', problem.metadata.get('template', 'unknown'))
        templates_seen.add(template)

        if template not in template_results:
            template_results[template] = {'passed': 0, 'failed': 0, 'same_answer': 0, 'examples': []}

        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)
        expected = malrule.calculate_expected_answer(problem)

        correct_answer = str(correct_sol.answer)
        malrule_answer = str(malrule_sol.answer)
        expected_str = str(expected)

        if correct_answer == malrule_answer:
            template_results[template]['same_answer'] += 1
            # Record this edge case
            if len(template_results[template]['examples']) < 2:
                template_results[template]['examples'].append({
                    'problem': problem.text,
                    'answer': correct_answer,
                    'type': 'same_answer',
                    'correct_steps': correct_sol.steps,
                    'malrule_steps': malrule_sol.steps
                })
        elif malrule_answer == expected_str:
            template_results[template]['passed'] += 1
        else:
            template_results[template]['failed'] += 1
            if len(template_results[template]['examples']) < 2:
                template_results[template]['examples'].append({
                    'problem': problem.text,
                    'correct': correct_answer,
                    'malrule': malrule_answer,
                    'expected_malrule': expected_str,
                    'type': 'mismatch',
                    'correct_steps': correct_sol.steps,
                    'malrule_steps': malrule_sol.steps
                })

    print(f"\nTemplates found: {sorted(templates_seen)}")
    print("\nResults by template:")

    all_passed = True
    for template in sorted(template_results.keys()):
        results = template_results[template]
        total = results['passed'] + results['failed'] + results['same_answer']
        print(f"\n  {template}:")
        print(f"    Passed: {results['passed']}/{total}")
        print(f"    Failed: {results['failed']}/{total}")
        print(f"    Same answer (edge cases): {results['same_answer']}/{total}")

        if results['failed'] > 0:
            all_passed = False
            print("    Example failures:")
            for ex in results['examples']:
                if ex['type'] == 'mismatch':
                    print(f"      Problem: {ex['problem']}")
                    print(f"      Correct: {ex['correct']}, Malrule: {ex['malrule']}, Expected: {ex['expected_malrule']}")

        if results['same_answer'] > 0 and results['passed'] == 0 and results['failed'] == 0:
            all_passed = False
            print("    WARNING: All problems for this template produce same answer!")
            for ex in results['examples']:
                if ex['type'] == 'same_answer':
                    print(f"      Problem: {ex['problem']}, Answer: {ex['answer']}")

    print("\n" + "=" * 70)
    if all_passed:
        print("ALL TEMPLATES PASSED ✓")
    else:
        print("SOME TEMPLATES FAILED ✗")
    print("=" * 70)

    return all_passed


def test_automated_suite():
    """Run the automated test suite."""
    print("\n\n" + "=" * 70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("=" * 70)

    problem_gen = BorrowNoDecrementProblemGenerator(
        level=3,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = BorrowNoDecrementMalrule()
    correct = SubtractionCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)

    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    else:
        print("\n✗✗✗ SOME AUTOMATED TESTS FAILED ✗✗✗")

    return all_passed


def main():
    print("\n╔" + "═" * 68 + "╗")
    print("║" + "  VERIFICATION TEST: Borrow-No-Decrement Malrule  ".center(70) + "║")
    print("╚" + "═" * 68 + "╝\n")

    try:
        specific_passed = test_specific_examples()
        templates_passed = test_all_templates()
        automated_passed = test_automated_suite()

        all_passed = specific_passed and templates_passed and automated_passed

        print("\n\n╔" + "═" * 68 + "╗")
        if all_passed:
            print("║" + "  ✓✓✓ VERIFICATION COMPLETE - ALL TESTS PASSED ✓✓✓  ".center(70) + "║")
        else:
            print("║" + "  ✗✗✗ VERIFICATION COMPLETE - SOME TESTS FAILED ✗✗✗  ".center(70) + "║")
        print("╚" + "═" * 68 + "╝\n")

        return 0 if all_passed else 1

    except Exception as e:
        print(f"\n✗✗✗ TEST FAILED: {e} ✗✗✗")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
