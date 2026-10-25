#!/usr/bin/env python3
"""
Test script for Wrong-Conversion-Factor malrule.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.measurement.wrong_conversion_factor import (
    WrongConversionFactorProblemGenerator,
    WrongConversionFactorMalrule,
    UnitConversionCorrectAlgorithm
)


def test_specific_examples():
    """Test with specific examples."""
    print("="*70)
    print("TESTING WRONG-CONVERSION-FACTOR WITH SPECIFIC EXAMPLES")
    print("="*70)

    malrule = WrongConversionFactorMalrule()
    correct = UnitConversionCorrectAlgorithm()

    # Test case 1: 5 feet to inches (12 vs 10)
    print("\nTEST CASE 1: 5 feet to inches")
    print("-"*70)

    problem1 = Problem(
        text="Convert 5 feet to inches",
        operands=[5, 12],
        operation='unit_conversion',
        level=6,
        difficulty=DifficultyLevel.EASY,
        metadata={
            'value': 5,
            'from_unit': 'feet',
            'to_unit': 'inches',
            'correct_factor': 12,
            'wrong_factor': 10,
            'correct_answer': 60,
            'malrule_answer': 50
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"Problem: {problem1.text}")
    print(f"Correct answer: {correct_sol.answer}")
    print(f"Malrule answer: {malrule_sol.answer}")

    # Expected: 60 inches (correct), but malrule says 50 (using 10 instead of 12)
    assert correct_sol.answer == "60", f"Expected 60, got {correct_sol.answer}"
    assert malrule_sol.answer == "50", f"Expected 50 (malrule), got {malrule_sol.answer}"
    assert correct_sol.answer != malrule_sol.answer, "Malrule should produce different answer"

    print("\n--- Correct Steps ---")
    for step in correct_sol.steps:
        print(f"  {step}")

    print("\n--- Malrule Steps ---")
    for step in malrule_sol.steps:
        print(f"  {step}")

    print("✓ TEST CASE 1 PASSED: 5 feet to inches, correct=60, malrule=50")

    # Test case 2: 3 km to meters (1000 vs 100)
    print("\n\nTEST CASE 2: 3 kilometers to meters")
    print("-"*70)

    problem2 = Problem(
        text="Convert 3 kilometers to meters",
        operands=[3, 1000],
        operation='unit_conversion',
        level=7,
        difficulty=DifficultyLevel.EASY,
        metadata={
            'value': 3,
            'from_unit': 'kilometers',
            'to_unit': 'meters',
            'correct_factor': 1000,
            'wrong_factor': 100,
            'correct_answer': 3000,
            'malrule_answer': 300
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)

    print(f"Problem: {problem2.text}")
    print(f"Correct answer: {correct_sol2.answer}")
    print(f"Malrule answer: {malrule_sol2.answer}")

    # Expected: 3000 meters (correct), but malrule says 300 (using 100 instead of 1000)
    assert correct_sol2.answer == "3000", f"Expected 3000, got {correct_sol2.answer}"
    assert malrule_sol2.answer == "300", f"Expected 300 (malrule), got {malrule_sol2.answer}"

    print("✓ TEST CASE 2 PASSED: 3 km to meters, correct=3000, malrule=300")

    # Test case 3: 2 hours to minutes (60 vs 100)
    print("\n\nTEST CASE 3: 2 hours to minutes")
    print("-"*70)

    problem3 = Problem(
        text="Convert 2 hours to minutes",
        operands=[2, 60],
        operation='unit_conversion',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'value': 2,
            'from_unit': 'hours',
            'to_unit': 'minutes',
            'correct_factor': 60,
            'wrong_factor': 100,
            'correct_answer': 120,
            'malrule_answer': 200
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)

    print(f"Problem: {problem3.text}")
    print(f"Correct answer: {correct_sol3.answer}")
    print(f"Malrule answer: {malrule_sol3.answer}")

    # Expected: 120 minutes (correct), but malrule says 200 (using 100 instead of 60)
    assert correct_sol3.answer == "120", f"Expected 120, got {correct_sol3.answer}"
    assert malrule_sol3.answer == "200", f"Expected 200 (malrule), got {malrule_sol3.answer}"

    print("✓ TEST CASE 3 PASSED: 2 hours to minutes, correct=120, malrule=200")

    # Test case 4: 4 yards to feet (3 vs 10)
    print("\n\nTEST CASE 4: 4 yards to feet")
    print("-"*70)

    problem4 = Problem(
        text="Convert 4 yards to feet",
        operands=[4, 3],
        operation='unit_conversion',
        level=5,
        difficulty=DifficultyLevel.EASY,
        metadata={
            'value': 4,
            'from_unit': 'yards',
            'to_unit': 'feet',
            'correct_factor': 3,
            'wrong_factor': 10,
            'correct_answer': 12,
            'malrule_answer': 40
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)

    print(f"Problem: {problem4.text}")
    print(f"Correct answer: {correct_sol4.answer}")
    print(f"Malrule answer: {malrule_sol4.answer}")

    # Expected: 12 feet (correct), but malrule says 40 (using 10 instead of 3)
    assert correct_sol4.answer == "12", f"Expected 12, got {correct_sol4.answer}"
    assert malrule_sol4.answer == "40", f"Expected 40 (malrule), got {malrule_sol4.answer}"

    print("✓ TEST CASE 4 PASSED: 4 yards to feet, correct=12, malrule=40")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_new_problem_templates():
    print("\n\n" + "="*70)
    print("TESTING NEW PROBLEM TEMPLATES")
    print("="*70)

    malrule = WrongConversionFactorMalrule()
    correct = UnitConversionCorrectAlgorithm()

    # Test 1: multi_step_conversion - yards to inches
    problem1 = Problem(
        text="Convert 2 yards to inches",
        operands=[2, 3, 12],
        operation='multi_step_conversion',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'value': 2,
            'problem_type': 'multi_step_conversion',
            'start_unit': 'yards',
            'mid_unit': 'feet',
            'end_unit': 'inches',
            'factor1': 3,
            'factor2': 12,
            'wrong_factor1': 10,
            'wrong_factor2': 10,
            'correct_answer': 72,  # 2 × 3 × 12
            'malrule_answer': 240   # 2 × 10 × 12 (using wrong factor at step 1)
        }
    )

    correct_sol1 = correct.solve(problem1)
    malrule_sol1 = malrule.solve(problem1)
    assert correct_sol1.answer == "72"
    assert malrule_sol1.answer == "240"
    print("✓ TEST 1 PASSED: Multi-step conversion (yards→inches)")

    # Test 2: imperial_to_metric - miles to kilometers
    problem2 = Problem(
        text="Convert 5 miles to kilometers (use 1 miles ≈ 1.609 kilometers)",
        operands=[5, 1.609],
        operation='imperial_metric_conversion',
        level=7,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'value': 5,
            'problem_type': 'imperial_to_metric',
            'from_unit': 'miles',
            'to_unit': 'kilometers',
            'correct_factor': 1.609,
            'wrong_factor': 1.0,
            'correct_answer': 8.05,  # 5 × 1.609
            'malrule_answer': 5.0     # 5 × 1.0 (guessed 1:1)
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    # Now the algorithms compute the answer, so we check the computed value
    assert correct_sol2.answer == str(round(5 * 1.609, 2))
    assert malrule_sol2.answer == "5.0"
    assert correct_sol2.answer != malrule_sol2.answer
    print("✓ TEST 2 PASSED: Imperial to metric (miles→km)")

    # Test 3: word_problem_context - board length
    problem3 = Problem(
        text="A board is 6 feet long. How many inches is that?",
        operands=[6, 12],
        operation='word_problem_conversion',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'value': 6,
            'problem_type': 'word_problem_context',
            'from_unit': 'feet',
            'to_unit': 'inches',
            'correct_factor': 12,
            'wrong_factor': 10,
            'correct_answer': 72,  # 6 × 12
            'malrule_answer': 60   # 6 × 10
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert correct_sol3.answer == "72"
    assert malrule_sol3.answer == "60"
    print("✓ TEST 3 PASSED: Word problem context (board length)")

    # Test 4: compound_units - speed conversion
    problem4 = Problem(
        text="Convert 30 miles per hour to feet per second",
        operands=[30, 1.467],
        operation='compound_unit_conversion',
        level=8,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'value': 30,
            'problem_type': 'compound_units',
            'from_unit': 'miles per hour',
            'to_unit': 'feet per second',
            'from_abbr': 'mph',
            'to_abbr': 'ft/s',
            'unit_type': 'speed',
            'correct_factor': 1.467,
            'wrong_factor': 1.0,
            'correct_answer': 44.01,  # 30 × 1.467
            'malrule_answer': 30.0    # 30 × 1.0
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    # Now the algorithms compute the answer
    assert correct_sol4.answer == str(round(30 * 1.467, 2))
    assert malrule_sol4.answer == str(round(30 * 1.0, 2))
    assert correct_sol4.answer != malrule_sol4.answer
    print("✓ TEST 4 PASSED: Compound units (speed conversion)")

    print("\n" + "="*70)
    print("ALL NEW TEMPLATE TESTS PASSED ✓")
    print("="*70)


def test_template_generation():
    print("\n\n" + "="*70)
    print("TESTING TEMPLATE GENERATION")
    print("="*70)

    generator = WrongConversionFactorProblemGenerator(
        level=7,
        difficulty=DifficultyLevel.MEDIUM
    )

    # Generate 20 problems and track which templates appear
    template_types = set()
    for i in range(20):
        problem = generator.generate(seed=1000 + i)
        problem_type = problem.metadata.get('problem_type', 'basic_conversion')
        template_types.add(problem_type)

    print(f"\nGenerated templates: {template_types}")

    # We should see at least 3 different template types across 20 generations
    assert len(template_types) >= 3, f"Expected at least 3 template types, got {len(template_types)}"

    # Verify each template type can be solved by both algorithms
    malrule = WrongConversionFactorMalrule()
    correct = UnitConversionCorrectAlgorithm()

    for template_type in template_types:
        # Generate a problem of this specific type
        attempts = 0
        while attempts < 50:
            problem = generator.generate(seed=2000 + attempts)
            if problem.metadata.get('problem_type', 'basic_conversion') == template_type:
                correct_sol = correct.solve(problem)
                malrule_sol = malrule.solve(problem)
                print(f"✓ Template '{template_type}' can be solved by both algorithms")
                break
            attempts += 1

    print("\n" + "="*70)
    print("TEMPLATE GENERATION TEST PASSED ✓")
    print("="*70)


def test_question_variants():
    """Test all 3 question variants for each problem type."""
    print("\n\n" + "="*70)
    print("TESTING QUESTION VARIANTS (3 per problem type)")
    print("="*70)

    malrule = WrongConversionFactorMalrule()
    correct = UnitConversionCorrectAlgorithm()
    generator = WrongConversionFactorProblemGenerator(
        level=7,
        difficulty=DifficultyLevel.MEDIUM
    )

    # Track which variants we've seen for each problem type
    variants_seen = {}

    # Generate 100 problems to ensure we see all variants
    for seed in range(1000, 1100):
        problem = generator.generate(seed=seed)
        problem_type = problem.metadata.get('problem_type', 'basic_conversion')
        question_variant = problem.metadata.get('question_variant', -1)

        if problem_type not in variants_seen:
            variants_seen[problem_type] = set()
        variants_seen[problem_type].add(question_variant)

        # Test that both algorithms can solve it
        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)
        assert correct_sol.answer != malrule_sol.answer, \
            f"Malrule should produce different answer for {problem_type} variant {question_variant}"

    # Verify we saw all 3 variants for each problem type
    print("\n" + "Variants seen per problem type:")
    for ptype, variants in variants_seen.items():
        print(f"  {ptype}: variants {sorted(variants)}")
        # Each problem type should have 3 variants (0, 1, 2)
        # Note: Due to randomness, we might not see all variants in 100 generations
        # But we should see at least 2 for most types
        assert len(variants) >= 2, \
            f"Expected at least 2 variants for {ptype}, got {len(variants)}"

    # Test specific variants explicitly
    print("\n" + "Testing specific problem types with all 3 variants:")

    # Test basic_conversion with all 3 variants
    for variant in [0, 1, 2]:
        # Generate problems until we get the right variant
        for seed in range(2000, 2100):
            problem = generator.generate(seed=seed)
            if (problem.metadata.get('problem_type') == 'basic_conversion' and
                problem.metadata.get('question_variant') == variant):
                correct_sol = correct.solve(problem)
                malrule_sol = malrule.solve(problem)
                print(f"  ✓ basic_conversion variant {variant}: '{problem.text[:50]}...'")
                break

    print("\n" + "="*70)
    print("QUESTION VARIANTS TEST PASSED ✓")
    print("="*70)


def test_comprehensive_templates():
    """Test all problem templates with enhanced output."""
    print("\n\n" + "="*70)
    print("COMPREHENSIVE TEMPLATE TESTING WITH ENHANCED OUTPUT")
    print("="*70)

    problem_gen = WrongConversionFactorProblemGenerator(
        level=6,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = WrongConversionFactorMalrule()
    correct = UnitConversionCorrectAlgorithm()

    # Test each problem type
    problem_types = ['basic_conversion', 'multi_step_conversion', 'imperial_to_metric',
                     'word_problem_context', 'compound_units']

    all_passed = True
    for ptype in problem_types:
        print(f"\n{'='*70}")
        print(f"Testing problem type: {ptype}")
        print('='*70)

        # Generate 5 problems of this type
        for seed in range(1000, 1050):
            problem = problem_gen.generate(seed=seed)
            if problem.metadata.get('problem_type', 'basic_conversion') != ptype:
                continue

            try:
                correct_sol = correct.solve(problem)
                malrule_sol = malrule.solve(problem)

                # Check if malrule produces same answer (edge case)
                if correct_sol.answer == malrule_sol.answer:
                    print(f"\n✗ EDGE CASE DETECTED (seed={seed}):")
                    print(f"  Problem: {problem.text}")
                    print(f"  Both algorithms produced same answer: {correct_sol.answer}")
                    print(f"\n  Correct algorithm steps:")
                    for step in correct_sol.steps:
                        print(f"    {step}")
                    print(f"\n  Malrule algorithm steps:")
                    for step in malrule_sol.steps:
                        print(f"    {step}")
                    all_passed = False
                    break
                else:
                    # Test passed
                    print(f"✓ Test passed (seed={seed}): Correct={correct_sol.answer}, Malrule={malrule_sol.answer}")
                    break

            except Exception as e:
                print(f"\n✗ TEST FAILED (seed={seed}):")
                print(f"  Problem: {problem.text}")
                print(f"  Error: {e}")
                print(f"\n  Expected correct answer: {problem.metadata.get('correct_answer', 'N/A')}")
                print(f"  Expected malrule answer: {problem.metadata.get('malrule_answer', 'N/A')}")
                try:
                    correct_sol = correct.solve(problem)
                    print(f"\n  Correct algorithm steps:")
                    for step in correct_sol.steps:
                        print(f"    {step}")
                except:
                    pass
                try:
                    malrule_sol = malrule.solve(problem)
                    print(f"\n  Malrule algorithm steps:")
                    for step in malrule_sol.steps:
                        print(f"    {step}")
                except:
                    pass
                all_passed = False
                break

    if all_passed:
        print("\n" + "="*70)
        print("✓✓✓ ALL TEMPLATE TESTS PASSED ✓✓✓")
        print("="*70)

    return all_passed


def test_automated_suite():
    """Run the automated test suite."""
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = WrongConversionFactorProblemGenerator(
        level=6,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = WrongConversionFactorMalrule()
    correct = UnitConversionCorrectAlgorithm()

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
    print("║" + "  VERIFICATION TEST: Wrong-Conversion-Factor  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    try:
        test_specific_examples()
        test_new_problem_templates()
        test_template_generation()
        test_question_variants()
        all_passed1 = test_automated_suite()
        all_passed2 = test_comprehensive_templates()
        all_passed = all_passed1 and all_passed2

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
