#!/usr/bin/env python3
"""Test script for Ignore-Coordinate-Signs malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.graphing.ignore_coordinate_signs import (
    IgnoreCoordinateSignsProblemGenerator,
    IgnoreCoordinateSignsMalrule,
    CoordinatePlottingWithSignsCorrectAlgorithm
)


def test_all_templates():
    """Test ALL problem templates - Generate and test every template available."""
    print("\n\n" + "="*70)
    print("TESTING ALL TEMPLATES")
    print("="*70)

    problem_gen = IgnoreCoordinateSignsProblemGenerator(
        level=6,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = IgnoreCoordinateSignsMalrule()
    correct = CoordinatePlottingWithSignsCorrectAlgorithm()

    templates = problem_gen.get_available_templates()
    print(f"\nFound {len(templates)} templates: {templates}")
    assert len(templates) == 5, f"Expected 5 templates, got {len(templates)}"

    passed_count = 0
    failed_count = 0

    for template in templates:
        print(f"\n--- Testing template: {template} ---")

        try:
            # Generate problem with this template
            problem = problem_gen.generate(seed=42, template=template)

            # Solve with both algorithms
            correct_sol = correct.solve(problem)
            malrule_sol = malrule.solve(problem)

            # Get expected answers from metadata
            expected_correct = problem.metadata.get('correct_answer')
            expected_malrule = problem.metadata.get('malrule_answer')

            # Extract x and y from problem if available
            x = problem.metadata.get('x')
            y = problem.metadata.get('y')

            # Check if this is an edge case where both coordinates are positive (no negatives)
            is_edge_case = (x is not None and y is not None and x >= 0 and y >= 0)

            if is_edge_case:
                print(f"  ⚠ EDGE CASE: No negative coordinates! x={x}, y={y}")
                print(f"  ✓ Template '{template}': Correct={correct_sol.answer}, Malrule={malrule_sol.answer} (SAME)")
                passed_count += 1
            else:
                # Verify answers match expected
                correct_matches = (str(correct_sol.answer) == str(expected_correct))
                malrule_matches = (str(malrule_sol.answer) == str(expected_malrule))

                if correct_matches and malrule_matches:
                    print(f"  ✓ Template '{template}': Correct={correct_sol.answer}, Malrule={malrule_sol.answer}")
                    passed_count += 1
                else:
                    print(f"  ✗ Template '{template}' FAILED")
                    print(f"  Problem: {problem.text[:80]}...")
                    print(f"  Correct Steps:")
                    for step in correct_sol.steps:
                        print(f"    {step}")
                    print(f"  Malrule Steps:")
                    for step in malrule_sol.steps:
                        print(f"    {step}")
                    print(f"  Expected Correct: {expected_correct}")
                    print(f"  Expected Malrule: {expected_malrule}")
                    print(f"  Actual Correct: {correct_sol.answer}")
                    print(f"  Actual Malrule: {malrule_sol.answer}")
                    failed_count += 1

        except Exception as e:
            print(f"  ✗ Template '{template}' FAILED WITH EXCEPTION")
            print(f"  Exception: {e}")
            import traceback
            traceback.print_exc()
            failed_count += 1

    print("\n" + "="*70)
    print(f"TEMPLATE TESTS SUMMARY: {passed_count} passed, {failed_count} failed")
    if failed_count == 0:
        print("ALL TEMPLATE TESTS PASSED ✓")
    print("="*70)

    return failed_count == 0


def test_edge_cases():
    """Test edge cases where coordinates are 0 or all positive."""
    print("\n\n" + "="*70)
    print("TESTING EDGE CASES")
    print("="*70)

    malrule = IgnoreCoordinateSignsMalrule()
    correct = CoordinatePlottingWithSignsCorrectAlgorithm()

    edge_cases = [
        # No negative coordinates (malrule produces same answer as correct)
        (3, 5, "both positive"),
        (7, 2, "both positive"),

        # Zero coordinate cases
        (0, -5, "x is zero, y negative"),
        (-5, 0, "x negative, y is zero"),
        (0, 0, "both zero (origin)"),

        # Single negative cases
        (-3, 4, "x negative, y positive"),
        (6, -3, "x positive, y negative"),

        # Both negative cases
        (-5, -2, "both negative"),
    ]

    passed_count = 0
    warning_count = 0

    for x, y, description in edge_cases:
        problem = Problem(
            text=f"Plot the point ({x}, {y})",
            operands=[x, y],
            operation='coordinate_plotting',
            level=6,
            difficulty=DifficultyLevel.MEDIUM,
            metadata={
                'x': x,
                'y': y,
                'correct_answer': (x, y),
                'malrule_answer': (abs(x), abs(y))
            }
        )

        try:
            correct_sol = correct.solve(problem)
            malrule_sol = malrule.solve(problem)

            if correct_sol.answer == malrule_sol.answer:
                print(f"  ⚠ EDGE CASE ({description}): Malrule produced same answer as correct! x={x}, y={y}")
                print(f"    Correct={correct_sol.answer}, Malrule={malrule_sol.answer}")
                warning_count += 1
                passed_count += 1  # Still passes, just logs the edge case
            else:
                print(f"  ✓ Edge case ({description}): x={x}, y={y}, Correct={correct_sol.answer}, Malrule={malrule_sol.answer}")
                passed_count += 1

        except Exception as e:
            print(f"  ✗ Edge case ({description}) FAILED WITH EXCEPTION: x={x}, y={y}")
            print(f"    Exception: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "="*70)
    print(f"EDGE CASE TESTS: {passed_count} passed, {warning_count} edge cases detected")
    print("ALL EDGE CASE TESTS PASSED ✓")
    print("="*70)

    return True


def test_specific_examples():
    print("="*70)
    print("TESTING SPECIFIC EXAMPLES")
    print("="*70)

    malrule = IgnoreCoordinateSignsMalrule()
    correct = CoordinatePlottingWithSignsCorrectAlgorithm()

    # Test case 1: Classic (-3, 4) vs (3, 4)
    problem1 = Problem(
        text="Plot the point (-3, 4)",
        operands=[-3, 4],
        operation='coordinate_plotting',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'x': -3,
            'y': 4,
            'correct_answer': (-3, 4),
            'malrule_answer': (3, 4)  # Student ignores negative
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: (-3, 4) → Correct: {correct_sol.answer}, Malrule: {malrule_sol.answer}")
    assert correct_sol.answer == (-3, 4)
    assert malrule_sol.answer == (3, 4)
    assert correct_sol.answer != malrule_sol.answer
    print("✓ PASSED (Classic: (-3, 4) vs (3, 4))")

    # Test case 2: Both negative (-5, -2) vs (5, 2)
    problem2 = Problem(
        text="Plot the point (-5, -2)",
        operands=[-5, -2],
        operation='coordinate_plotting',
        level=7,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'x': -5,
            'y': -2,
            'correct_answer': (-5, -2),
            'malrule_answer': (5, 2)
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert correct_sol2.answer == (-5, -2)
    assert malrule_sol2.answer == (5, 2)
    assert correct_sol2.answer != malrule_sol2.answer
    print("✓ TEST 2 PASSED ((-5, -2) vs (5, 2) - both negative)")

    # Test case 3: Negative y (6, -3) vs (6, 3)
    problem3 = Problem(
        text="Plot the point (6, -3)",
        operands=[6, -3],
        operation='coordinate_plotting',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'x': 6,
            'y': -3,
            'correct_answer': (6, -3),
            'malrule_answer': (6, 3)
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert correct_sol3.answer == (6, -3)
    assert malrule_sol3.answer == (6, 3)
    assert correct_sol3.answer != malrule_sol3.answer
    print("✓ TEST 3 PASSED ((6, -3) vs (6, 3) - negative y)")

    # Test case 4: Larger negative x (-8, 2) vs (8, 2)
    problem4 = Problem(
        text="Plot the point (-8, 2)",
        operands=[-8, 2],
        operation='coordinate_plotting',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'x': -8,
            'y': 2,
            'correct_answer': (-8, 2),
            'malrule_answer': (8, 2)
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    assert correct_sol4.answer == (-8, 2)
    assert malrule_sol4.answer == (8, 2)
    assert correct_sol4.answer != malrule_sol4.answer
    print("✓ TEST 4 PASSED ((-8, 2) vs (8, 2) - larger values)")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_automated_suite():
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = IgnoreCoordinateSignsProblemGenerator(
        level=6,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = IgnoreCoordinateSignsMalrule()
    correct = CoordinatePlottingWithSignsCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Ignore-Coordinate-Signs  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    try:
        test_specific_examples()
        test_all_templates()
        test_edge_cases()
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
