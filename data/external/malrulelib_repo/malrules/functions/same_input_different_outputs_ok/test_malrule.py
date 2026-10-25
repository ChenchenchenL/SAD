#!/usr/bin/env python3
"""
Test script for Same-Input-Different-Outputs-OK malrule.

MALRULE COULD PRODUCE SAME ANSWER AS CORRECT FOR THIS CASE
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.functions.same_input_different_outputs_ok import (
    SameInputDifferentOutputsOKProblemGenerator,
    SameInputDifferentOutputsOKMalrule,
    FunctionDefinitionCorrectAlgorithm
)


def test_specific_examples():
    """Test with specific examples."""
    print("="*70)
    print("TESTING SAME-INPUT-DIFFERENT-OUTPUTS-OK WITH SPECIFIC EXAMPLES")
    print("="*70)

    malrule = SameInputDifferentOutputsOKMalrule()
    correct = FunctionDefinitionCorrectAlgorithm()

    # Test case 1: NOT a function - repeated input with different outputs
    print("\nTEST CASE 1: {(2,3), (4,5), (2,7)} (NOT a function)")
    print("-"*70)

    pairs1 = [(2, 3), (4, 5), (2, 7)]
    pairs_str1 = "(2, 3), (4, 5), (2, 7)"

    problem1 = Problem(
        text=f"Is the following relation a function? {{{pairs_str1}}}",
        operands=[len(pairs1)],
        operation='function_definition',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'pairs': pairs1,
            'pairs_str': pairs_str1,
            'is_function': False,
            'num_pairs': len(pairs1)
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"Problem: {problem1.text}")
    print(f"Correct answer: {correct_sol.answer}")
    print(f"Malrule answer: {malrule_sol.answer}")

    # Expected: NO (correct - repeated input), but malrule says YES
    assert correct_sol.answer == "NO", f"Expected NO, got {correct_sol.answer}"
    assert malrule_sol.answer == "YES", f"Expected YES (malrule), got {malrule_sol.answer}"
    assert correct_sol.answer != malrule_sol.answer, "Malrule should produce different answer"

    print("\n--- Correct Steps ---")
    for step in correct_sol.steps:
        print(f"  {step}")

    print("\n--- Malrule Steps ---")
    for step in malrule_sol.steps:
        print(f"  {step}")

    print("✓ TEST CASE 1 PASSED: {(2,3), (4,5), (2,7)} correct=NO, malrule=YES")

    # Test case 2: IS a function - all unique inputs
    print("\n\nTEST CASE 2: {(1,2), (3,4), (5,6)} (IS a function)")
    print("-"*70)

    pairs2 = [(1, 2), (3, 4), (5, 6)]
    pairs_str2 = "(1, 2), (3, 4), (5, 6)"

    problem2 = Problem(
        text=f"Is the following relation a function? {{{pairs_str2}}}",
        operands=[len(pairs2)],
        operation='function_definition',
        level=8,
        difficulty=DifficultyLevel.EASY,
        metadata={
            'pairs': pairs2,
            'pairs_str': pairs_str2,
            'is_function': True,
            'num_pairs': len(pairs2)
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)

    print(f"Problem: {problem2.text}")
    print(f"Correct answer: {correct_sol2.answer}")
    print(f"Malrule answer: {malrule_sol2.answer}")

    # Expected: YES (correct), and malrule also says YES (happens to be right)
    assert correct_sol2.answer == "YES", f"Expected YES, got {correct_sol2.answer}"
    assert malrule_sol2.answer == "YES", f"Expected YES (malrule), got {malrule_sol2.answer}"

    print("✓ TEST CASE 2 PASSED: {(1,2), (3,4), (5,6)} correct=YES, malrule=YES")

    # Test case 3: IS a function - same output for different inputs (OK!)
    print("\n\nTEST CASE 3: {(0,5), (1,5), (2,5)} (IS a function - many-to-one OK)")
    print("-"*70)

    pairs3 = [(0, 5), (1, 5), (2, 5)]
    pairs_str3 = "(0, 5), (1, 5), (2, 5)"

    problem3 = Problem(
        text=f"Is the following relation a function? {{{pairs_str3}}}",
        operands=[len(pairs3)],
        operation='function_definition',
        level=9,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'pairs': pairs3,
            'pairs_str': pairs_str3,
            'is_function': True,
            'num_pairs': len(pairs3)
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)

    print(f"Problem: {problem3.text}")
    print(f"Correct answer: {correct_sol3.answer}")
    print(f"Malrule answer: {malrule_sol3.answer}")

    # Expected: YES (correct - different inputs can have same output), malrule also YES
    assert correct_sol3.answer == "YES", f"Expected YES, got {correct_sol3.answer}"
    assert malrule_sol3.answer == "YES", f"Expected YES (malrule), got {malrule_sol3.answer}"

    print("✓ TEST CASE 3 PASSED: {(0,5), (1,5), (2,5)} correct=YES, malrule=YES")

    # Test case 4: NOT a function - multiple repeated inputs
    print("\n\nTEST CASE 4: {(3,1), (3,2), (4,5)} (NOT a function)")
    print("-"*70)

    pairs4 = [(3, 1), (3, 2), (4, 5)]
    pairs_str4 = "(3, 1), (3, 2), (4, 5)"

    problem4 = Problem(
        text=f"Is the following relation a function? {{{pairs_str4}}}",
        operands=[len(pairs4)],
        operation='function_definition',
        level=9,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'pairs': pairs4,
            'pairs_str': pairs_str4,
            'is_function': False,
            'num_pairs': len(pairs4)
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)

    print(f"Problem: {problem4.text}")
    print(f"Correct answer: {correct_sol4.answer}")
    print(f"Malrule answer: {malrule_sol4.answer}")

    # Expected: NO (correct - x=3 maps to both 1 and 2), but malrule says YES
    assert correct_sol4.answer == "NO", f"Expected NO, got {correct_sol4.answer}"
    assert malrule_sol4.answer == "YES", f"Expected YES (malrule), got {malrule_sol4.answer}"

    print("✓ TEST CASE 4 PASSED: {(3,1), (3,2), (4,5)} correct=NO, malrule=YES")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_all_templates():
    """Test all 5 templates for Same-Input-Different-Outputs-OK."""
    print("\n\n" + "="*70)
    print("TESTING ALL TEMPLATES")
    print("="*70)

    problem_gen = SameInputDifferentOutputsOKProblemGenerator(
        level=9,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = SameInputDifferentOutputsOKMalrule()
    correct = FunctionDefinitionCorrectAlgorithm()

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

        # Verify malrule answer
        print(f"  Problem: {problem.text[:80]}...")
        print(f"  Is function: {problem.metadata['is_function']}")
        print(f"  Correct answer: {correct_sol.answer}")
        print(f"  Malrule answer: {malrule_sol.answer}")

        # Malrule always says YES
        assert malrule_sol.answer == "YES", \
            f"Template {template}: Malrule should always say YES, got {malrule_sol.answer}"

        # Verify calculate_expected_answer matches malrule output
        expected = malrule.calculate_expected_answer(problem)
        print(f"  Expected answer: {expected}")

        assert str(malrule_sol.answer) == str(expected), \
            f"Template {template}: calculate_expected_answer() returned {expected} but malrule produced {malrule_sol.answer}"

        # For invalid functions (is_function=False), correct should say NO but malrule says YES
        if not problem.metadata['is_function']:
            assert correct_sol.answer == "NO", \
                f"Template {template}: Correct should say NO for invalid function"
            assert malrule_sol.answer != correct_sol.answer, \
                f"Template {template}: Malrule and correct should differ for invalid functions"

        print(f"  ✓ Template {template} PASSED")

    print("\n" + "="*70)
    print("ALL TEMPLATE TESTS PASSED ✓")
    print("="*70)


def test_automated_suite():
    """Run the automated test suite."""
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = SameInputDifferentOutputsOKProblemGenerator(
        level=9,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = SameInputDifferentOutputsOKMalrule()
    correct = FunctionDefinitionCorrectAlgorithm()

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
    print("║" + "  VERIFICATION TEST: Same-Input-Different-Outputs-OK  ".center(70) + "║")
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
