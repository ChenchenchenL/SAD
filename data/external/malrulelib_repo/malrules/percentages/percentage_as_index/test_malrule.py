#!/usr/bin/env python3
"""Test script for Percentage-As-Index malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.percentages.percentage_as_index import (
    PercentageAsIndexProblemGenerator,
    PercentageAsIndexMalrule,
    PercentageCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING PERCENTAGE-AS-INDEX")
    print("="*70)

    malrule = PercentageAsIndexMalrule()
    correct = PercentageCorrectAlgorithm()

    # Test case 1: 30% of 50 = 15 (correct), 30 (malrule uses percentage as answer)
    problem1 = Problem(
        text="What is 30% of 50?",
        operands=[30, 50],
        operation='percentage',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'percentage': 30,
            'total': 50,
            'correct_answer': 15,  # 30% of 50 = 15
            'malrule_answer': 30,  # Student uses percentage itself
            'template': 'basic_percentage'
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: 30% of 50 → Correct: {correct_sol.answer}, Malrule: {malrule_sol.answer}")
    assert correct_sol.answer == 15
    assert malrule_sol.answer == 30
    assert correct_sol.answer != malrule_sol.answer
    print("✓ PASSED")

    # Test case 2: 25% of 80 = 20 (correct), 25 (malrule)
    problem2 = Problem(
        text="What is 25% of 80?",
        operands=[25, 80],
        operation='percentage',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'percentage': 25,
            'total': 80,
            'correct_answer': 20,
            'malrule_answer': 25,
            'template': 'basic_percentage'
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert correct_sol2.answer == 20
    assert malrule_sol2.answer == 25
    print("✓ TEST 2 PASSED")

    # Test case 3: 40% of 150 = 60 (correct), 40 (malrule)
    problem3 = Problem(
        text="What is 40% of 150?",
        operands=[40, 150],
        operation='percentage',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'percentage': 40,
            'total': 150,
            'correct_answer': 60,
            'malrule_answer': 40,
            'template': 'basic_percentage'
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert correct_sol3.answer == 60
    assert malrule_sol3.answer == 40
    print("✓ TEST 3 PASSED")

    # Test case 4: 50% of 100 = 50 (correct), 50 (malrule - happens to be same!)
    problem4 = Problem(
        text="What is 50% of 100?",
        operands=[50, 100],
        operation='percentage',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'percentage': 50,
            'total': 100,
            'correct_answer': 50,
            'malrule_answer': 50,  # Same answer but wrong reasoning!
            'template': 'basic_percentage'
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    assert correct_sol4.answer == 50
    assert malrule_sol4.answer == 50
    # Note: answers are same but reasoning is different
    print("✓ TEST 4 PASSED (same answer, different reasoning)")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_all_templates():
    """Test all 5 templates for Percentage-As-Index."""
    print("\n\n" + "="*70)
    print("TESTING ALL TEMPLATES")
    print("="*70)

    problem_gen = PercentageAsIndexProblemGenerator(
        level=6,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = PercentageAsIndexMalrule()
    correct = PercentageCorrectAlgorithm()

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

        # Verify answers
        print(f"  Problem: {problem.text[:80]}...")
        print(f"  Correct answer: {correct_sol.answer}")
        print(f"  Malrule answer: {malrule_sol.answer}")

        # Verify different answers (except when they happen to be the same)
        # Note: For percentage-as-index, sometimes answers can be same by coincidence
        # (e.g., 50% of 100 = 50, and malrule also gives 50)

        # Verify calculate_expected_answer matches malrule output
        expected = malrule.calculate_expected_answer(problem)
        print(f"  Expected answer: {expected}")

        assert str(malrule_sol.answer) == str(expected), \
            f"Template {template}: calculate_expected_answer() returned {expected} but malrule produced {malrule_sol.answer}"

        print(f"  ✓ Template {template} PASSED")

    print("\n" + "="*70)
    print("ALL TEMPLATE TESTS PASSED ✓")
    print("="*70)


def test_automated_suite():
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = PercentageAsIndexProblemGenerator(
        level=6,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = PercentageAsIndexMalrule()
    correct = PercentageCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Percentage-As-Index  ".center(70) + "║")
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
