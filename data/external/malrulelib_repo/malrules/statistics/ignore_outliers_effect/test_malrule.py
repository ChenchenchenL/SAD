#!/usr/bin/env python3
"""
Test script for Ignore-Outliers-Effect malrule.

Run from project root: python3 -m malrules.statistics.ignore_outliers_effect.test_malrule
Or from this directory: python3 test_malrule.py
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.statistics.ignore_outliers_effect import (
    IgnoreOutliersEffectProblemGenerator,
    IgnoreOutliersEffectMalrule,
    IgnoreOutliersEffectCorrectAlgorithm
)


def test_specific_examples():
    """Test with specific, well-known examples from research."""
    print("="*70)
    print("TESTING IGNORE-OUTLIERS-EFFECT WITH SPECIFIC EXAMPLES")
    print("="*70)

    malrule = IgnoreOutliersEffectMalrule()
    correct = IgnoreOutliersEffectCorrectAlgorithm()

    # Test case 1: Classic example - typical values 5-7, outlier = 50
    print("\nTEST CASE 1: {5, 6, 5, 7, 6, 50} - Typical 5-7, outlier 50")
    print("-"*70)

    problem1 = Problem(
        text="Is the mean representative of this data set: {5, 6, 5, 7, 6, 50}?",
        operands=[5, 6, 5, 7, 6, 50],
        operation='representativeness',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'data': [5, 6, 5, 7, 6, 50],
            'outlier': 50,
            'outlier_direction': 'high',
            'mean': 13.17,
            'median': 6,
            'has_outlier': True,
            'correct_answer': 'No, mean is not representative',
            'malrule_answer': 'Yes, mean is representative',
            'template': 'basic_outlier'
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"Problem: {problem1.text}")
    print(f"Data: {problem1.operands}")
    print(f"Mean: 13.17, Median: 6")
    print(f"Correct answer: {correct_sol.answer[:80]}...")
    print(f"Malrule answer: {malrule_sol.answer}")

    # Correct: Should say NO (mean not representative)
    # Malrule: Says YES (ignores outlier effect)
    assert "no" in correct_sol.answer.lower(), \
        f"Expected 'No' in correct answer, got {correct_sol.answer}"
    assert "yes" in malrule_sol.answer.lower(), \
        f"Expected 'Yes' in malrule answer, got {malrule_sol.answer}"
    assert correct_sol.answer.lower() != malrule_sol.answer.lower(), \
        "Malrule should produce different answer than correct"

    print("\n--- Correct Steps (first 10) ---")
    for step in correct_sol.steps[:10]:
        print(f"  {step}")

    print("\n--- Malrule Steps (first 10) ---")
    for step in malrule_sol.steps[:10]:
        print(f"  {step}")

    print("✓ TEST CASE 1 PASSED: Correct recognizes outlier effect, malrule ignores it")

    # Test case 2: Salary example - typical $30K-$40K, outlier $500K
    print("\n\nTEST CASE 2: {30, 35, 32, 38, 40, 500} - Salaries in thousands")
    print("-"*70)

    problem2 = Problem(
        text="Is the mean representative of this data set: {30, 35, 32, 38, 40, 500}?",
        operands=[30, 35, 32, 38, 40, 500],
        operation='representativeness',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'data': [30, 35, 32, 38, 40, 500],
            'outlier': 500,
            'outlier_direction': 'high',
            'mean': 112.5,
            'median': 36.5,
            'has_outlier': True,
            'correct_answer': 'No, mean is not representative',
            'malrule_answer': 'Yes, mean is representative',
            'template': 'word_problem_context'
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)

    print(f"Problem: {problem2.text}")
    print(f"Context: Salaries (in thousands) - typical $30K-$40K, one $500K")
    print(f"Mean: $112.5K, Median: $36.5K")
    print(f"Correct answer: {correct_sol2.answer[:80]}...")
    print(f"Malrule answer: {malrule_sol2.answer}")

    # Correct: Should say NO (mean $112.5K doesn't represent typical $30K-$40K)
    # Malrule: Says YES (ignores that $500K distorts mean)
    assert "no" in correct_sol2.answer.lower(), \
        f"Expected 'No' in correct answer, got {correct_sol2.answer}"
    assert "yes" in malrule_sol2.answer.lower(), \
        f"Expected 'Yes' in malrule answer, got {malrule_sol2.answer}"

    print("✓ TEST CASE 2 PASSED: Real-world salary example shows outlier effect")

    # Test case 3: Test scores - typical 70-85, outlier = 15
    print("\n\nTEST CASE 3: {72, 78, 75, 82, 80, 15} - Test scores, low outlier")
    print("-"*70)

    problem3 = Problem(
        text="Is the mean representative of this data set: {72, 78, 75, 82, 80, 15}?",
        operands=[72, 78, 75, 82, 80, 15],
        operation='representativeness',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'data': [72, 78, 75, 82, 80, 15],
            'outlier': 15,
            'outlier_direction': 'low',
            'mean': 67,
            'median': 76.5,
            'has_outlier': True,
            'correct_answer': 'No, mean is not representative',
            'malrule_answer': 'Yes, mean is representative',
            'template': 'basic_outlier'
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)

    print(f"Problem: {problem3.text}")
    print(f"Context: Test scores - typical 70s-80s, one student got 15")
    print(f"Mean: 67, Median: 76.5")
    print(f"Correct answer: {correct_sol3.answer[:80]}...")
    print(f"Malrule answer: {malrule_sol3.answer}")

    # Correct: Should say NO (mean 67 pulled down by outlier 15)
    # Malrule: Says YES (ignores low outlier effect)
    assert "no" in correct_sol3.answer.lower(), \
        f"Expected 'No' in correct answer, got {correct_sol3.answer}"
    assert "yes" in malrule_sol3.answer.lower(), \
        f"Expected 'Yes' in malrule answer, got {malrule_sol3.answer}"

    print("✓ TEST CASE 3 PASSED: Low outlier also distorts mean")

    # Test case 4: House prices - typical $200K-$250K, outlier = $2M
    print("\n\nTEST CASE 4: {210, 225, 215, 240, 230, 2000} - House prices (thousands)")
    print("-"*70)

    problem4 = Problem(
        text="Is the mean a good measure of center for the data set {210, 225, 215, 240, 230, 2000}?",
        operands=[210, 225, 215, 240, 230, 2000],
        operation='representativeness',
        level=9,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'data': [210, 225, 215, 240, 230, 2000],
            'outlier': 2000,
            'outlier_direction': 'high',
            'mean': 520,
            'median': 227.5,
            'has_outlier': True,
            'correct_answer': 'No, mean is not representative',
            'malrule_answer': 'Yes, mean is representative',
            'template': 'basic_outlier'
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)

    print(f"Problem: {problem4.text}")
    print(f"Context: House prices - typical $200K-$250K, one mansion at $2M")
    print(f"Mean: $520K, Median: $227.5K")
    print(f"Correct answer: {correct_sol4.answer[:80]}...")
    print(f"Malrule answer: {malrule_sol4.answer}")

    # Correct: Should say NO (mean $520K doesn't represent typical $200K-$250K)
    # Malrule: Says YES
    assert "no" in correct_sol4.answer.lower(), \
        f"Expected 'No' in correct answer, got {correct_sol4.answer}"
    assert "yes" in malrule_sol4.answer.lower(), \
        f"Expected 'Yes' in malrule answer, got {malrule_sol4.answer}"

    # Check that malrule shows its flawed reasoning (using verbose=True for detailed steps)
    malrule_sol4_verbose = malrule.solve(problem4, verbose=True)
    malrule_reasoning = " ".join(malrule_sol4_verbose.steps)
    assert "MALRULE" in malrule_reasoning or "ERROR" in malrule_reasoning, \
        "Malrule should show its flawed reasoning in verbose steps"

    # Check that correct solution mentions outlier and median (using verbose=True for detailed steps)
    correct_sol4_verbose = correct.solve(problem4, verbose=True)
    correct_reasoning = " ".join(correct_sol4_verbose.steps)
    assert "outlier" in correct_reasoning.lower(), \
        "Correct solution should mention outliers in verbose steps"
    assert "median" in correct_reasoning.lower(), \
        "Correct solution should mention median as better measure in verbose steps"

    print("✓ TEST CASE 4 PASSED: House price example demonstrates severe distortion")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_all_templates():
    """Test all problem templates with detailed output."""
    print("\n\n" + "="*70)
    print("TESTING ALL PROBLEM TEMPLATES")
    print("="*70)

    problem_gen = IgnoreOutliersEffectProblemGenerator(
        level=7,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = IgnoreOutliersEffectMalrule()
    correct = IgnoreOutliersEffectCorrectAlgorithm()

    templates = problem_gen.get_available_templates()
    print(f"\nFound {len(templates)} templates: {templates}\n")

    passed_count = 0
    failed_count = 0

    for template_name in templates:
        print(f"\n{'='*70}")
        print(f"TEMPLATE: {template_name}")
        print('-'*70)

        try:
            # Generate problem using specific template with a consistent seed
            problem = problem_gen.generate(seed=42, template=template_name)

            print(f"Problem: {problem.text[:100]}...")
            print(f"Data: {problem.metadata.get('data', [])}")
            print(f"Has outlier: {problem.metadata.get('has_outlier')}")
            print()

            # Solve with both algorithms
            correct_sol = correct.solve(problem)
            malrule_sol = malrule.solve(problem)

            # Verify template is set
            assert problem.metadata.get('template') == template_name, \
                f"Template {template_name} not set correctly in metadata"

            # Verify both algorithms can solve the problem
            assert malrule_sol.answer is not None, \
                f"Malrule failed to solve {template_name}"
            assert correct_sol.answer is not None, \
                f"Correct algorithm failed to solve {template_name}"

            # Print answers
            print(f"Correct answer: {correct_sol.answer[:100]}...")
            print(f"Malrule answer: {malrule_sol.answer[:100]}...")
            print()

            # Check if answers are different (they should be for most templates)
            # Exception: symmetric_no_outlier where both might say "yes"
            if template_name == 'symmetric_no_outlier':
                # Both should say mean is representative
                if "yes" in correct_sol.answer.lower() and "yes" in malrule_sol.answer.lower():
                    print(f"✓ EDGE CASE: Both algorithms correctly say 'yes' for symmetric data")
                    print(f"  Checking verbose steps to verify reasoning differs...")
                    # Use verbose=True for detailed step checking
                    correct_sol_verbose = correct.solve(problem, verbose=True)
                    malrule_sol_verbose = malrule.solve(problem, verbose=True)
                    correct_steps_text = " ".join(correct_sol_verbose.steps)
                    malrule_steps_text = " ".join(malrule_sol_verbose.steps)

                    # Correct should mention "no outliers" or "symmetric"
                    if "no" in correct_steps_text.lower() and ("outlier" in correct_steps_text.lower() or "symmetric" in correct_steps_text.lower()):
                        print(f"  ✓ Correct algorithm properly analyzes for outliers")
                    else:
                        raise AssertionError("Correct algorithm should analyze for outliers in verbose steps")

                    # Malrule should show it always assumes mean is representative
                    if "MALRULE" in malrule_steps_text or "always" in malrule_steps_text.lower():
                        print(f"  ✓ Malrule shows it doesn't check for outliers")
                    else:
                        raise AssertionError("Malrule should show misconception in verbose steps")
                else:
                    raise AssertionError(f"Both should say 'yes' for symmetric_no_outlier template")
            else:
                # For templates with outliers, answers should differ
                if template_name != 'comparison_problem':  # comparison has different format
                    answers_differ = correct_sol.answer.lower() != malrule_sol.answer.lower()
                    if not answers_differ:
                        # They might have same text but different reasoning
                        # Check if at least the steps show different reasoning (using verbose=True)
                        print(f"  WARNING: Answers appear similar, checking verbose steps...")
                        correct_sol_verbose = correct.solve(problem, verbose=True)
                        malrule_sol_verbose = malrule.solve(problem, verbose=True)
                        print(f"\n  --- Correct Steps (verbose) ---")
                        for step in correct_sol_verbose.steps[:10]:
                            print(f"    {step}")
                        print(f"\n  --- Malrule Steps (verbose) ---")
                        for step in malrule_sol_verbose.steps[:10]:
                            print(f"    {step}")

                        # Verify they have different reasoning
                        correct_checks_outliers = any("outlier" in step.lower() for step in correct_sol_verbose.steps)
                        malrule_ignores_outliers = any("MALRULE" in step or "ERROR" in step for step in malrule_sol_verbose.steps)

                        if correct_checks_outliers and malrule_ignores_outliers:
                            print(f"  ✓ Different reasoning paths confirmed")
                        else:
                            raise AssertionError(f"Algorithms should have different reasoning for {template_name}")

            print(f"\n✓ Template '{template_name}' PASSED")
            passed_count += 1

        except AssertionError as e:
            print(f"\n✗ Template '{template_name}' FAILED: {e}")
            print(f"\n--- FAILURE DETAILS ---")
            print(f"Problem: {problem.text}")
            print(f"Data: {problem.metadata.get('data', [])}")
            print(f"\n--- Correct Algorithm Steps ---")
            for i, step in enumerate(correct_sol.steps, 1):
                print(f"{i:3d}. {step}")
            print(f"\n--- Malrule Algorithm Steps ---")
            for i, step in enumerate(malrule_sol.steps, 1):
                print(f"{i:3d}. {step}")
            print(f"\n--- Expected from Metadata ---")
            print(f"Expected correct: {problem.metadata.get('correct_answer')}")
            print(f"Expected malrule: {problem.metadata.get('malrule_answer')}")
            failed_count += 1

    print("\n" + "="*70)
    print(f"RESULTS: {passed_count} PASSED, {failed_count} FAILED")
    print("="*70)

    if failed_count > 0:
        raise AssertionError(f"{failed_count} template(s) failed")


def test_automated_suite():
    """Run the automated test suite."""
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = IgnoreOutliersEffectProblemGenerator(
        level=7,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = IgnoreOutliersEffectMalrule()
    correct = IgnoreOutliersEffectCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)

    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    else:
        print("\n✗✗✗ SOME TESTS FAILED ✗✗✗")
        for result in results:
            if not result.passed:
                print(f"FAILED: {result.message}")

    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Ignore-Outliers-Effect Malrule  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    try:
        test_specific_examples()
        test_all_templates()
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
