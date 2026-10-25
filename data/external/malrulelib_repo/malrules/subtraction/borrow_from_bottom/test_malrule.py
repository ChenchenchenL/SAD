#!/usr/bin/env python3
"""
Test script for Borrow-From-Bottom malrule.

Run from project root: python3 -m malrules.subtraction.borrow_from_bottom.test_malrule
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.subtraction.borrow_from_bottom import (
    BorrowFromBottomProblemGenerator,
    BorrowFromBottomMalrule,
    SubtractionCorrectAlgorithm
)
import random
from typing import List, Dict, Any, Optional, Tuple

def print_steps(label: str, steps: List[str]) -> None:
    """Print solution steps with a label."""
    print(f"\n--- {label} ---")
    for step in steps:
        print(f"  {step}")


def test_single_problem(problem, correct, malrule, expected_correct,
                        expected_malrule=None, allow_same_answer=False) -> bool:
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


def test_all_templates(problem_gen, correct, malrule, num_seeds: int = 100) -> Tuple[bool, Dict[str, Any]]:
    """
    Test that all problem templates generate valid problems and produce correct malrule behavior.

    Args:
        problem_gen: Problem generator instance
        correct: Correct algorithm instance
        malrule: Malrule algorithm instance
        num_seeds: Number of seeds to try to hit all templates

    Returns:
        Tuple of (all_passed, template_results)
    """
    templates_seen = set()
    template_results = {}

    # Generate problems with different seeds to try to hit all templates
    for seed in range(num_seeds):
        random.seed(seed)
        problem = problem_gen.generate(seed=seed)

        # Try multiple keys for template identification
        template = problem.metadata.get('problem_type',
                   problem.metadata.get('template',
                   problem.metadata.get('type', 'unknown')))
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
                    'operands': problem.operands,
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
                    'operands': problem.operands,
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
                    print(f"      Operands: {ex['operands']}")
                    print(f"      Correct: {ex['correct']}, Malrule: {ex['malrule']}, Expected: {ex['expected_malrule']}")
                    if 'malrule_steps' in ex:
                        print("      Malrule steps:")
                        for step in ex['malrule_steps'][:5]:
                            print(f"        {step}")

        # Warn if ALL problems for this template produce same answer
        if results['same_answer'] > 0 and results['passed'] == 0 and results['failed'] == 0:
            # Don't fail for templates that might legitimately produce same answers sometimes
            # but warn about it
            print("    WARNING: All problems for this template produce same answer!")
            for ex in results['examples']:
                if ex['type'] == 'same_answer':
                    print(f"      Problem: {ex['problem']}, Answer: {ex['answer']}")

    return all_passed, template_results


def run_standard_test_suite(malrule_name: str, problem_gen, correct, malrule,
                            specific_tests: List[Dict[str, Any]],
                            malrule_test_class) -> int:
    """
    Run a standardized test suite for a malrule.

    Args:
        malrule_name: Name of the malrule for display
        problem_gen: Problem generator instance
        correct: Correct algorithm instance
        malrule: Malrule algorithm instance
        specific_tests: List of specific test cases (dicts with 'operands', 'expected_correct', 'expected_malrule')
        malrule_test_class: MalruleTest class from utils

    Returns:
        0 if all tests passed, 1 if any failed
    """
    print("\n╔" + "═" * 68 + "╗")
    print("║" + f"  VERIFICATION TEST: {malrule_name}  ".center(70) + "║")
    print("╚" + "═" * 68 + "╝\n")

    all_passed = True

    # Test specific examples
    print("=" * 70)
    print(f"TESTING {malrule_name.upper()} WITH SPECIFIC EXAMPLES")
    print("=" * 70)

    from utils import Problem, DifficultyLevel

    for i, test_case in enumerate(specific_tests, 1):
        print(f"\nTEST CASE {i}: {test_case['operands'][0]} - {test_case['operands'][1]}")
        print("-" * 70)

        problem = Problem(
            text=test_case.get('text', f"What is {test_case['operands'][0]} - {test_case['operands'][1]}?"),
            operands=test_case['operands'],
            operation='subtraction',
            level=test_case.get('level', 3),
            difficulty=test_case.get('difficulty', DifficultyLevel.MEDIUM),
            metadata={'template': test_case.get('template', 'basic')}
        )

        if not test_single_problem(
            problem, correct, malrule,
            test_case['expected_correct'],
            test_case.get('expected_malrule'),
            test_case.get('allow_same_answer', False)
        ):
            all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print("ALL SPECIFIC TEST CASES PASSED ✓")
    else:
        print("SOME SPECIFIC TEST CASES FAILED ✗")
    print("=" * 70)

    # Test all templates
    print("\n\n" + "=" * 70)
    print("TESTING ALL PROBLEM TEMPLATES")
    print("=" * 70)

    templates_passed, _ = test_all_templates(problem_gen, correct, malrule)
    if not templates_passed:
        all_passed = False

    print("\n" + "=" * 70)
    if templates_passed:
        print("ALL TEMPLATES PASSED ✓")
    else:
        print("SOME TEMPLATES FAILED ✗")
    print("=" * 70)

    # Run automated test suite
    print("\n\n" + "=" * 70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("=" * 70)

    test_suite = malrule_test_class(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    automated_passed = all(r.passed for r in results)
    if not automated_passed:
        all_passed = False

    if automated_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    else:
        print("\n✗✗✗ SOME AUTOMATED TESTS FAILED ✗✗✗")

    # Final summary
    print("\n\n╔" + "═" * 68 + "╗")
    if all_passed:
        print("║" + "  ✓✓✓ VERIFICATION COMPLETE - ALL TESTS PASSED ✓✓✓  ".center(70) + "║")
    else:
        print("║" + "  ✗✗✗ VERIFICATION COMPLETE - SOME TESTS FAILED ✗✗✗  ".center(70) + "║")
    print("╚" + "═" * 68 + "╝\n")

    return 0 if all_passed else 1


def test_algorithm_no_metadata_usage():
    """
    Verify that both algorithms compute results using logic, not metadata.
    This is critical - algorithms should work independently of pre-computed answers.
    """
    print("\n" + "=" * 70)
    print("TESTING THAT ALGORITHMS DO NOT USE METADATA")
    print("=" * 70)

    correct = SubtractionCorrectAlgorithm()
    malrule = BorrowFromBottomMalrule()

    # Create a problem with WRONG metadata values
    test_cases = [
        (53, 28, 25, 45),
        (153, 128, 25, 45),
        (503, 109, 394, 594),
        (1234, 789, 445, 1465),
    ]

    all_passed = True
    for minuend, subtrahend, expected_correct, expected_malrule in test_cases:
        problem = Problem(
            text=f'Calculate: {minuend} - {subtrahend}',
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=3,
            difficulty=DifficultyLevel.MEDIUM,
            metadata={
                'correct_answer': 9999,  # WRONG - should be ignored
                'malrule_answer': 8888,  # WRONG - should be ignored
            }
        )

        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        correct_passed = correct_sol.answer == expected_correct
        malrule_passed = int(malrule_sol.answer) == expected_malrule

        if correct_passed and malrule_passed:
            print(f"✓ {minuend} - {subtrahend}: correct={correct_sol.answer}, malrule={malrule_sol.answer}")
        else:
            all_passed = False
            print(f"✗ {minuend} - {subtrahend}: FAILED")
            if not correct_passed:
                print(f"  Correct algorithm: got {correct_sol.answer}, expected {expected_correct}")
                print(f"  (Used metadata? {correct_sol.answer == 9999})")
            if not malrule_passed:
                print(f"  Malrule algorithm: got {malrule_sol.answer}, expected {expected_malrule}")
                print(f"  (Used metadata? {malrule_sol.answer == '8888'})")

    print()
    if all_passed:
        print("✓ ALL METADATA INDEPENDENCE TESTS PASSED")
    else:
        print("✗ SOME METADATA INDEPENDENCE TESTS FAILED")

    return all_passed


def test_edge_cases():
    """
    Test comprehensive edge cases for both algorithms.
    Covers: small numbers, large numbers, borrow-across-zero, cascade failures.
    """
    print("\n" + "=" * 70)
    print("TESTING EDGE CASES")
    print("=" * 70)

    correct = SubtractionCorrectAlgorithm()
    malrule = BorrowFromBottomMalrule()

    # Edge case test cases:
    # (minuend, subtrahend, expected_correct, expected_malrule, description)
    #
    # Malrule behavior:
    # - When top < bottom, try to borrow from bottom number's next digit
    # - If bottom's next digit is 0, cascade (set to 9) and find next non-zero
    # - If cascade fails (no non-zero digit found), use smaller-from-larger fallback
    edge_cases = [
        # Small numbers (2-digit, core malrule behavior from README)
        (53, 28, 25, 45, "2-digit basic (README example)"),
        (62, 37, 25, 45, "2-digit (README example)"),
        (71, 46, 25, 45, "2-digit (README example)"),
        (84, 59, 25, 45, "2-digit (README example)"),

        # 2-digit edge cases
        (52, 19, 33, 53, "2-digit: bottom tens becomes 0 after borrow"),
        (41, 28, 13, 33, "2-digit: 11-8=3, 4-1=3 → 33"),
        (90, 51, 39, 59, "2-digit: top ones is 0, 10-1=9, 9-4=5 → 59"),

        # 3-digit numbers
        (153, 128, 25, 45, "3-digit: hundreds cancel out"),
        (253, 128, 125, 145, "3-digit: different hundreds"),
        (532, 287, 245, 465, "3-digit: multiple borrows needed"),
        (300, 125, 175, 395, "3-digit: cascade bottom 125→115→105, 10-5=5, 10-1=9, 3-0=3"),

        # Cascade fails cases (fallback to smaller-from-larger)
        (503, 109, 394, 594, "3-digit: ones cascade ok, tens cascade fails"),

        # Large numbers (4+ digits)
        (1234, 789, 445, 1465, "4-digit: cascade fails at end"),
        (5432, 2187, 3245, 3465, "4-digit: multiple borrows"),

        # Edge cases where cascade fails completely
        # 1000 - 1: bottom is 0001, all zeros to cascade, fails → smaller-from-larger 1-0=1
        (1000, 1, 999, 1001, "4-digit: cascade fails, fallback gives nonsense result"),
        # 1000 - 999: borrows succeed for ones/tens, cascade fails at hundreds
        (1000, 999, 1, 1821, "4-digit: cascade fails at hundreds"),
        # 100 - 37: ones borrow ok (37→27), tens cascade fails (bottom tens 2→ nothing higher)
        (100, 37, 63, 123, "3-digit: cascade fails at tens"),
        # 200 - 109: ones cascade ok (109→099), tens cascade fails (bottom 099)
        (200, 109, 91, 291, "3-digit: cascade at ones succeeds, fails at tens"),

        # No borrow needed (malrule = correct)
        (89, 54, 35, 35, "2-digit: no borrow needed"),
        (99, 11, 88, 88, "2-digit: no borrow, same digits"),
    ]

    all_passed = True
    for minuend, subtrahend, expected_correct, expected_malrule, desc in edge_cases:
        problem = Problem(
            text=f'Calculate: {minuend} - {subtrahend}',
            operands=[minuend, subtrahend],
            operation='subtraction',
            level=3,
            difficulty=DifficultyLevel.MEDIUM,
            metadata={}
        )

        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        correct_result = correct_sol.answer
        malrule_result = int(malrule_sol.answer)

        correct_passed = correct_result == expected_correct
        malrule_passed = malrule_result == expected_malrule

        if correct_passed and malrule_passed:
            print(f"✓ {desc}")
            print(f"    {minuend} - {subtrahend}: correct={correct_result}, malrule={malrule_result}")
        else:
            all_passed = False
            print(f"✗ {desc}")
            print(f"    {minuend} - {subtrahend}")
            if not correct_passed:
                print(f"    Correct: got {correct_result}, expected {expected_correct}")
            if not malrule_passed:
                print(f"    Malrule: got {malrule_result}, expected {expected_malrule}")

    print()
    if all_passed:
        print("✓ ALL EDGE CASE TESTS PASSED")
    else:
        print("✗ SOME EDGE CASE TESTS FAILED")

    return all_passed


def main():
    problem_gen = BorrowFromBottomProblemGenerator(
        level=3,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = BorrowFromBottomMalrule()
    correct = SubtractionCorrectAlgorithm()

    # Define specific test cases from README examples
    # For Borrow-From-Bottom: Student borrows from subtrahend instead of minuend
    # 53 - 28: Need to borrow for ones (3<8)
    #   Student adds 10 to 3 (making 13), but decrements bottom 2 (making 1)
    #   Result: 13-8=5, 5-1=4 -> 45 (wrong)
    #   Correct: 4(13)-28=25
    specific_tests = [
        {
            'operands': [53, 28],
            'expected_correct': 25,
            'expected_malrule': 45,
            'text': "Calculate: 53 - 28",
        },
        {
            'operands': [62, 37],
            'expected_correct': 25,
            'expected_malrule': 45,
            'text': "Calculate: 62 - 37",
        },
        {
            'operands': [71, 46],
            'expected_correct': 25,
            'expected_malrule': 45,
            'text': "Calculate: 71 - 46",
        },
        {
            'operands': [84, 59],
            'expected_correct': 25,
            'expected_malrule': 45,
            'text': "Calculate: 84 - 59",
        },
    ]

    # Run additional tests first
    metadata_test_passed = test_algorithm_no_metadata_usage()
    edge_case_test_passed = test_edge_cases()

    if not metadata_test_passed or not edge_case_test_passed:
        print("\n" + "=" * 70)
        print("✗ ADDITIONAL TESTS FAILED - STOPPING")
        print("=" * 70)
        return 1

    try:
        return run_standard_test_suite(
            "Borrow-From-Bottom",
            problem_gen, correct, malrule,
            specific_tests,
            MalruleTest
        )
    except Exception as e:
        print(f"\n✗✗✗ TEST FAILED: {e} ✗✗✗")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
