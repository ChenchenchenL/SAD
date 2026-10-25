#!/usr/bin/env python3
"""
Test script for Stops-Borrow-At-Zero malrule.

Run from project root: python3 -m malrules.subtraction.stops_borrow_at_zero.test_malrule
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest
from malrules.subtraction.stops_borrow_at_zero import (
    StopsBorrowAtZeroProblemGenerator,
    StopsBorrowAtZeroMalrule,
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


def main():
    problem_gen = StopsBorrowAtZeroProblemGenerator(
        level=4,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = StopsBorrowAtZeroMalrule()
    correct = SubtractionCorrectAlgorithm()

    # Define specific test cases
    # For Stops-Borrow-At-Zero: Student gives up when encountering zero
    # 503 - 285: Student can't borrow from 0, stops or writes invalid result
    specific_tests = [
        {
            'operands': [503, 285],
            'expected_correct': 218,
            # Malrule behavior varies - just check it's different
            'text': "Calculate: 503 - 285",
        },
        {
            'operands': [402, 156],
            'expected_correct': 246,
            'text': "Calculate: 402 - 156",
        },
        {
            'operands': [701, 324],
            'expected_correct': 377,
            'text': "Calculate: 701 - 324",
        },
        {
            'operands': [600, 245],
            'expected_correct': 355,
            'text': "Calculate: 600 - 245",
        },
    ]

    try:
        return run_standard_test_suite(
            "Stops-Borrow-At-Zero",
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
