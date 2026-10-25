#!/usr/bin/env python3
"""
Test script for Decompose-By-Place-Value-Label malrule.

Run from project root: python3 -m malrules.subtraction.decompose_by_place_value_label.test_malrule
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.subtraction.decompose_by_place_value_label import (
    DecomposeByPlaceValueLabelProblemGenerator,
    DecomposeByPlaceValueLabelMalrule,
    PlaceValueDecompositionCorrectAlgorithm
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
    print("\n╔" + "═" * 68 + "╗")
    print("║" + "  VERIFICATION TEST: Decompose-By-Place-Value-Label  ".center(70) + "║")
    print("╚" + "═" * 68 + "╝\n")

    problem_gen = DecomposeByPlaceValueLabelProblemGenerator(
        level=3,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = DecomposeByPlaceValueLabelMalrule()
    correct = PlaceValueDecompositionCorrectAlgorithm()

    all_passed = True

    # Test specific examples
    print("=" * 70)
    print("TESTING DECOMPOSE-BY-PLACE-VALUE-LABEL WITH SPECIFIC EXAMPLES")
    print("=" * 70)

    # Test case 1: Basic 3-digit with regrouped tens
    print("\nTEST CASE 1: 2 hundreds 13 tens 1 ones (basic regrouped tens)")
    print("-" * 70)
    problem1 = Problem(
        text="What number is represented by 2 hundreds 13 tens 1 ones?",
        operands=[0, 2, 13, 1],
        operation='place_value_decomposition',
        level=3,
        difficulty=DifficultyLevel.MEDIUM
    )
    if not test_single_problem(problem1, correct, malrule, '331', '2131'):
        all_passed = False

    # Test case 2: Larger tens value
    print("\nTEST CASE 2: 5 hundreds 24 tens 6 ones (larger tens value)")
    print("-" * 70)
    problem2 = Problem(
        text="What number is represented by 5 hundreds 24 tens 6 ones?",
        operands=[0, 5, 24, 6],
        operation='place_value_decomposition',
        level=3,
        difficulty=DifficultyLevel.MEDIUM
    )
    if not test_single_problem(problem2, correct, malrule, '746', '5246'):
        all_passed = False

    # Test case 3: 4-digit number
    print("\nTEST CASE 3: 1 thousand 3 hundreds 12 tens 5 ones (4-digit)")
    print("-" * 70)
    problem3 = Problem(
        text="What number is represented by 1 thousand 3 hundreds 12 tens 5 ones?",
        operands=[1, 3, 12, 5],
        operation='place_value_decomposition',
        level=4,
        difficulty=DifficultyLevel.HARD
    )
    if not test_single_problem(problem3, correct, malrule, '1425', '13125'):
        all_passed = False

    # Test case 4: Small 2-digit number (regrouped ones)
    print("\nTEST CASE 4: 3 tens 15 ones (small 2-digit, regrouped ones)")
    print("-" * 70)
    problem4 = Problem(
        text="What number is represented by 3 tens 15 ones?",
        operands=[0, 0, 3, 15],
        operation='place_value_decomposition',
        level=2,
        difficulty=DifficultyLevel.EASY
    )
    if not test_single_problem(problem4, correct, malrule, '45', '315'):
        all_passed = False

    # Test case 5: Large 4-digit number with regrouped hundreds
    print("\nTEST CASE 5: 3 thousands 14 hundreds 2 tens 7 ones (large 4-digit)")
    print("-" * 70)
    problem5 = Problem(
        text="What number is represented by 3 thousands 14 hundreds 2 tens 7 ones?",
        operands=[3, 14, 2, 7],
        operation='place_value_decomposition',
        level=4,
        difficulty=DifficultyLevel.HARD
    )
    if not test_single_problem(problem5, correct, malrule, '4427', '31427'):
        all_passed = False

    # Test case 6: Multiple regroupings (both tens and ones)
    print("\nTEST CASE 6: 2 hundreds 11 tens 12 ones (multiple regroupings)")
    print("-" * 70)
    problem6 = Problem(
        text="What number is represented by 2 hundreds 11 tens 12 ones?",
        operands=[0, 2, 11, 12],
        operation='place_value_decomposition',
        level=3,
        difficulty=DifficultyLevel.HARD
    )
    if not test_single_problem(problem6, correct, malrule, '322', '21112'):
        all_passed = False

    # Test case 7: Word problem (base-10 blocks)
    print("\nTEST CASE 7: Base-10 blocks word problem")
    print("-" * 70)
    problem7 = Problem(
        text="A student has base-10 blocks: 2 hundred-blocks, 15 ten-rods, and 3 unit cubes. What number do these blocks represent?",
        operands=[0, 2, 15, 3],
        operation='place_value_decomposition',
        level=3,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'thousands': 0,
            'hundreds': 2,
            'tens': 15,
            'ones': 3,
            'template': 'word_problem'
        }
    )
    if not test_single_problem(problem7, correct, malrule, '353', '2153'):
        all_passed = False

    # Test case 8: Very small numbers (edge case)
    print("\nTEST CASE 8: 1 ten 11 ones (very small, edge case)")
    print("-" * 70)
    problem8 = Problem(
        text="What number is represented by 1 ten 11 ones?",
        operands=[0, 0, 1, 11],
        operation='place_value_decomposition',
        level=2,
        difficulty=DifficultyLevel.EASY
    )
    if not test_single_problem(problem8, correct, malrule, '21', '111'):
        all_passed = False

    # Test case 9: Large regrouping value
    print("\nTEST CASE 9: 1 hundred 99 tens 9 ones (large regrouping)")
    print("-" * 70)
    problem9 = Problem(
        text="What number is represented by 1 hundred 99 tens 9 ones?",
        operands=[0, 1, 99, 9],
        operation='place_value_decomposition',
        level=3,
        difficulty=DifficultyLevel.HARD
    )
    if not test_single_problem(problem9, correct, malrule, '1099', '1999'):
        all_passed = False

    # Test case 10: Zero in ones place
    print("\nTEST CASE 10: 3 hundreds 12 tens 0 ones (zero in ones place)")
    print("-" * 70)
    problem10 = Problem(
        text="What number is represented by 3 hundreds 12 tens?",
        operands=[0, 3, 12, 0],
        operation='place_value_decomposition',
        level=3,
        difficulty=DifficultyLevel.MEDIUM
    )
    # With ones=0, malrule concatenates only non-zero: "3" + "12" = "312"
    if not test_single_problem(problem10, correct, malrule, '420', '312'):
        all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print("ALL SPECIFIC TEST CASES PASSED ✓")
    else:
        print("SOME SPECIFIC TEST CASES FAILED ✗")
    print("=" * 70)

    # Run automated test suite
    print("\n\n" + "=" * 70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("=" * 70)

    test_suite = MalruleTest(malrule, correct, problem_gen)
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


if __name__ == "__main__":
    exit(main())
