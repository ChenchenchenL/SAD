#!/usr/bin/env python3
"""Test script for Each-Fraction-Digit-Is-Ratio malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.ratios_proportions.each_fraction_digit_is_ratio import (
    EachFractionDigitIsRatioProblemGenerator,
    EachFractionDigitIsRatioMalrule,
    RatioSimplificationCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING EACH-FRACTION-DIGIT-IS-RATIO")
    print("="*70)

    malrule = EachFractionDigitIsRatioMalrule()
    correct = RatioSimplificationCorrectAlgorithm()

    # Test case 1: 12/34 → Correct: 6/17, Malrule: 11/32
    # Student: 1/3 stays 1/3, 2/4 becomes 1/2 → 11/32
    # Correct: GCD(12,34) = 2, so 12/2 : 34/2 = 6:17
    problem1 = Problem(
        text="Simplify the ratio 12:34",
        operands=[12, 34],
        operation='ratio_simplification',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'numerator': 12,
            'denominator': 34,
            'correct_num': 6,
            'correct_den': 17,
            'malrule_num': 11,
            'malrule_den': 32
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: Simplify 12:34 → Correct: {correct_sol.answer}, Malrule: {malrule_sol.answer}")
    assert correct_sol.answer == "6:17"
    assert malrule_sol.answer == "11:32"
    assert correct_sol.answer != malrule_sol.answer
    print("✓ PASSED")

    # Test case 2: 24/36 → Correct: 2/3, Malrule: 22/33
    # Student: 2/3 stays 2/3, 4/6 becomes 2/3 → 22/33
    # Correct: GCD(24,36) = 12, so 24/12 : 36/12 = 2:3
    problem2 = Problem(
        text="Simplify the ratio 24:36",
        operands=[24, 36],
        operation='ratio_simplification',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'numerator': 24,
            'denominator': 36,
            'correct_num': 2,
            'correct_den': 3,
            'malrule_num': 22,
            'malrule_den': 33
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    print(f"\nTEST 2: Simplify 24:36 → Correct: {correct_sol2.answer}, Malrule: {malrule_sol2.answer}")
    assert correct_sol2.answer == "2:3"
    assert malrule_sol2.answer == "22:33"
    assert correct_sol2.answer != malrule_sol2.answer
    print("✓ PASSED")

    # Test case 3: 14/28 → Correct: 1/2, Malrule: 11/22
    # Student: 1/2 stays 1/2, 4/8 becomes 1/2 → 11/22
    # Correct: GCD(14,28) = 14, so 14/14 : 28/14 = 1:2
    problem3 = Problem(
        text="Simplify the ratio 14:28",
        operands=[14, 28],
        operation='ratio_simplification',
        level=6,
        difficulty=DifficultyLevel.EASY,
        metadata={
            'numerator': 14,
            'denominator': 28,
            'correct_num': 1,
            'correct_den': 2,
            'malrule_num': 11,
            'malrule_den': 22
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    print(f"\nTEST 3: Simplify 14:28 → Correct: {correct_sol3.answer}, Malrule: {malrule_sol3.answer}")
    assert correct_sol3.answer == "1:2"
    assert malrule_sol3.answer == "11:22"
    assert correct_sol3.answer != malrule_sol3.answer
    print("✓ PASSED")

    # Test case 4: 26/39 → Correct: 2/3, Malrule: 22/33
    # Student: 2/3 stays 2/3, 6/9 becomes 2/3 → 22/33
    # Correct: GCD(26,39) = 13, so 26/13 : 39/13 = 2:3
    problem4 = Problem(
        text="Simplify the ratio 26:39",
        operands=[26, 39],
        operation='ratio_simplification',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'numerator': 26,
            'denominator': 39,
            'correct_num': 2,
            'correct_den': 3,
            'malrule_num': 22,
            'malrule_den': 33
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    print(f"\nTEST 4: Simplify 26:39 → Correct: {correct_sol4.answer}, Malrule: {malrule_sol4.answer}")
    assert correct_sol4.answer == "2:3"
    assert malrule_sol4.answer == "22:33"
    assert correct_sol4.answer != malrule_sol4.answer
    print("✓ PASSED")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_all_templates():
    """Test all 5 templates for Each-Fraction-Digit-Is-Ratio."""
    print("\n\n" + "="*70)
    print("TESTING ALL TEMPLATES")
    print("="*70)

    problem_gen = EachFractionDigitIsRatioProblemGenerator(
        level=7,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = EachFractionDigitIsRatioMalrule()
    correct = RatioSimplificationCorrectAlgorithm()

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

        # Verify different answers
        assert str(correct_sol.answer) != str(malrule_sol.answer), \
            f"Template {template}: Correct and malrule answers should be different!"

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

    problem_gen = EachFractionDigitIsRatioProblemGenerator(
        level=7,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = EachFractionDigitIsRatioMalrule()
    correct = RatioSimplificationCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Each-Fraction-Digit-Is-Ratio  ".center(70) + "║")
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
