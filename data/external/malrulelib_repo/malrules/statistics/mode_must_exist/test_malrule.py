#!/usr/bin/env python3
"""
Test script for Mode-Must-Exist malrule.

Run from project root: python3 -m malrules.statistics.mode_must_exist.test_malrule
Or from this directory: python3 test_malrule.py
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.statistics.mode_must_exist import (
    ModeMustExistProblemGenerator,
    ModeMustExistMalrule,
    ModeMustExistCorrectAlgorithm
)


def test_specific_examples():
    """Test with specific, well-known examples from research."""
    print("="*70)
    print("TESTING MODE-MUST-EXIST WITH SPECIFIC EXAMPLES")
    print("="*70)

    malrule = ModeMustExistMalrule()
    correct = ModeMustExistCorrectAlgorithm()

    # Test case 1: Simple dataset with no repeating values
    print("\nTEST CASE 1: {3, 7, 2, 9, 5} - All unique values")
    print("-"*70)

    problem1 = Problem(
        text="What is the mode of the data set: {3, 7, 2, 9, 5}?",
        operands=[3, 7, 2, 9, 5],
        operation='mode',
        level=6,
        difficulty=DifficultyLevel.EASY,
        metadata={
            'data': [3, 7, 2, 9, 5],
            'has_mode': False,
            'all_unique': True,
            'template': 'basic_no_mode'
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"Problem: {problem1.text}")
    print(f"Correct answer: {correct_sol.answer}")
    print(f"Malrule answer: {malrule_sol.answer}")

    # Correct: "No mode"
    # Malrule: Picks a specific value (largest, smallest, or middle)
    assert "no mode" in correct_sol.answer.lower(), \
        f"Expected 'No mode', got {correct_sol.answer}"
    assert correct_sol.answer.lower() != malrule_sol.answer.lower(), \
        "Malrule should produce different answer than correct (should pick a value, not 'no mode')"

    # Malrule should pick one of the actual values, not "No mode"
    data_values = [3, 7, 2, 9, 5]
    assert any(str(val) == malrule_sol.answer for val in data_values), \
        f"Malrule should pick a value from dataset, got {malrule_sol.answer}"

    print("\n--- Correct Steps ---")
    for step in correct_sol.steps:
        print(f"  {step}")

    print("\n--- Malrule Steps ---")
    for step in malrule_sol.steps:
        print(f"  {step}")

    print("✓ TEST CASE 1 PASSED: Correct says 'No mode', malrule picks a value")

    # Test case 2: Larger dataset, all unique
    print("\n\nTEST CASE 2: {1, 4, 6, 8, 10, 15, 20} - Larger dataset, all unique")
    print("-"*70)

    problem2 = Problem(
        text="Find the mode of: {1, 4, 6, 8, 10, 15, 20}",
        operands=[1, 4, 6, 8, 10, 15, 20],
        operation='mode',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'data': [1, 4, 6, 8, 10, 15, 20],
            'has_mode': False,
            'all_unique': True,
            'template': 'larger_no_mode'
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)

    print(f"Problem: {problem2.text}")
    print(f"Correct answer: {correct_sol2.answer}")
    print(f"Malrule answer: {malrule_sol2.answer}")

    # Correct: "No mode"
    # Malrule: Picks a specific value
    assert "no mode" in correct_sol2.answer.lower(), \
        f"Expected 'No mode', got {correct_sol2.answer}"
    assert correct_sol2.answer.lower() != malrule_sol2.answer.lower(), \
        "Malrule should produce different answer"

    data_values2 = [1, 4, 6, 8, 10, 15, 20]
    assert any(str(val) == malrule_sol2.answer for val in data_values2), \
        f"Malrule should pick a value from dataset, got {malrule_sol2.answer}"

    print("✓ TEST CASE 2 PASSED: Malrule incorrectly identifies a mode")

    # Test case 3: Small dataset with consecutive numbers
    print("\n\nTEST CASE 3: {5, 6, 7, 8} - Consecutive numbers, no repeats")
    print("-"*70)

    problem3 = Problem(
        text="Identify the mode for the following data set: {5, 6, 7, 8}",
        operands=[5, 6, 7, 8],
        operation='mode',
        level=6,
        difficulty=DifficultyLevel.EASY,
        metadata={
            'data': [5, 6, 7, 8],
            'has_mode': False,
            'all_unique': True,
            'template': 'small_no_mode'
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)

    print(f"Problem: {problem3.text}")
    print(f"Correct answer: {correct_sol3.answer}")
    print(f"Malrule answer: {malrule_sol3.answer}")

    # Correct: "No mode"
    # Malrule: Picks a specific value
    assert "no mode" in correct_sol3.answer.lower(), \
        f"Expected 'No mode', got {correct_sol3.answer}"
    assert correct_sol3.answer.lower() != malrule_sol3.answer.lower(), \
        "Malrule should produce different answer"

    print("✓ TEST CASE 3 PASSED: Correct recognizes no mode exists")

    # Test case 4: Dataset with negative and positive numbers, all unique
    print("\n\nTEST CASE 4: {-5, -2, 0, 3, 7, 12} - Mixed positive/negative, no repeats")
    print("-"*70)

    problem4 = Problem(
        text="What is the mode of the data set: {-5, -2, 0, 3, 7, 12}?",
        operands=[-5, -2, 0, 3, 7, 12],
        operation='mode',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'data': [-5, -2, 0, 3, 7, 12],
            'has_mode': False,
            'all_unique': True,
            'template': 'basic_no_mode'
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)

    print(f"Problem: {problem4.text}")
    print(f"Correct answer: {correct_sol4.answer}")
    print(f"Malrule answer: {malrule_sol4.answer}")

    # Correct: "No mode"
    # Malrule: Picks a specific value
    assert "no mode" in correct_sol4.answer.lower(), \
        f"Expected 'No mode', got {correct_sol4.answer}"
    assert correct_sol4.answer.lower() != malrule_sol4.answer.lower(), \
        "Malrule should produce different answer"

    data_values4 = [-5, -2, 0, 3, 7, 12]
    assert any(str(val) == malrule_sol4.answer for val in data_values4), \
        f"Malrule should pick a value from dataset, got {malrule_sol4.answer}"

    # Check that malrule shows its strategy in the verbose steps
    malrule_sol4_verbose = malrule.solve(problem4, verbose=True)
    malrule_reasoning = " ".join(malrule_sol4_verbose.steps)
    assert "MALRULE" in malrule_reasoning or "ERROR" in malrule_reasoning, \
        "Malrule should show its flawed reasoning in verbose steps"

    print("✓ TEST CASE 4 PASSED: Malrule applies misconception consistently")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_all_templates():
    """Test all problem templates with detailed output."""
    print("\n\n" + "="*70)
    print("TESTING ALL PROBLEM TEMPLATES")
    print("="*70)

    problem_gen = ModeMustExistProblemGenerator(
        level=6,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = ModeMustExistMalrule()
    correct = ModeMustExistCorrectAlgorithm()

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
            print(f"Has mode: {problem.metadata.get('has_mode')}")
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

            # Check based on template type
            if template_name == 'has_mode_control':
                # When a mode exists, both should identify it (EDGE CASE)
                assert "no mode" not in correct_sol.answer.lower(), \
                    f"has_mode_control should have a mode, but got {correct_sol.answer}"

                print(f"✓ EDGE CASE: Both algorithms find the mode (mode actually exists)")
                print(f"  Checking that malrule would still force a mode for non-mode data...")

                # Verify malrule still shows it would force a mode if needed
                malrule_steps_text = " ".join(malrule_sol.steps)
                if "mode" in malrule_steps_text.lower():
                    print(f"  ✓ Malrule correctly identifies actual mode")

            elif template_name == 'comparison_problem':
                # Comparison problem has different answer format
                assert "Dataset" in correct_sol.answer or "dataset" in correct_sol.answer, \
                    f"Comparison problem should mention datasets"

                # Verify malrule incorrectly says Dataset B has a mode
                if "Dataset B" in malrule_sol.answer and "mode" in malrule_sol.answer:
                    print(f"✓ Malrule incorrectly forces mode for Dataset B")
                else:
                    raise AssertionError("Malrule should force mode for Dataset B")

            elif template_name == 'word_problem_context':
                # Word problem context can have different scenarios
                has_mode = problem.metadata.get('has_mode', False)
                if has_mode:
                    # Should find a mode
                    assert "no mode" not in correct_sol.answer.lower() or problem.metadata.get('bimodal', False), \
                        f"word_problem_context with mode should not say 'no mode' (unless bimodal)"
                    print(f"✓ EDGE CASE: Scenario has actual mode")
                else:
                    # Should say no mode
                    assert "no mode" in correct_sol.answer.lower(), \
                        f"word_problem_context without mode should say 'no mode'"
                    # Malrule should pick a value
                    assert "no mode" not in malrule_sol.answer.lower(), \
                        f"Malrule should pick a value, not 'No mode'"
                    print(f"✓ Correct says 'no mode', malrule picks a value")

            else:
                # No mode templates: correct says "No mode", malrule picks a value
                assert "no mode" in correct_sol.answer.lower(), \
                    f"{template_name} should have no mode, but got {correct_sol.answer}"
                # Malrule should pick a value (not "No mode")
                assert "no mode" not in malrule_sol.answer.lower(), \
                    f"Malrule should pick a value for {template_name}, not 'No mode'"

                # Verify malrule picked a value from the dataset
                data = problem.metadata.get('data', [])
                malrule_answer_value = malrule_sol.answer.strip()
                # Extract just the number from answer like "5" or "The mode is 5"
                import re
                numbers_in_answer = re.findall(r'\d+', malrule_answer_value)
                if numbers_in_answer:
                    picked_value = int(numbers_in_answer[0])
                    if picked_value in data:
                        print(f"  ✓ Malrule picked value {picked_value} from dataset (should be max={max(data)})")
                    else:
                        print(f"  WARNING: Malrule picked {picked_value} not in dataset {data}")

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

    problem_gen = ModeMustExistProblemGenerator(
        level=6,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = ModeMustExistMalrule()
    correct = ModeMustExistCorrectAlgorithm()

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
    print("║" + "  VERIFICATION TEST: Mode-Must-Exist Malrule  ".center(70) + "║")
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
