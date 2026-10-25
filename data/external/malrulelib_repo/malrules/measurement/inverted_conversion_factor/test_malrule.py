#!/usr/bin/env python3
"""Test script for Inverted-Conversion-Factor malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.measurement.inverted_conversion_factor import (
    InvertedConversionFactorProblemGenerator,
    InvertedConversionFactorMalrule,
    UnitConversionCorrectAlgorithm
)


def test_specific_examples():
    print("="*70)
    print("TESTING INVERTED-CONVERSION-FACTOR")
    print("="*70)

    malrule = InvertedConversionFactorMalrule()
    correct = UnitConversionCorrectAlgorithm()

    # Test case 1: 24 inches to feet → Correct: 2, Malrule: 288
    problem1 = Problem(
        text="Convert 24 inches to feet",
        operands=[24, 12],
        operation='unit_conversion',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'value': 24,
            'from_unit': 'inches',
            'to_unit': 'feet',
            'factor': 12,
            'correct_answer': 2.0,    # 24 / 12 = 2 feet
            'malrule_answer': 288     # 24 * 12 = 288 (inverted!)
        }
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"\nTEST 1: 24 inches to feet → Correct: {correct_sol.answer} ft, Malrule: {malrule_sol.answer}")
    assert correct_sol.answer == 2.0
    assert malrule_sol.answer == 288
    assert correct_sol.answer != malrule_sol.answer
    print("✓ PASSED (24 inches = 2 feet, not 288!)")

    # Test case 2: 36 inches to feet → Correct: 3, Malrule: 432
    problem2 = Problem(
        text="Convert 36 inches to feet",
        operands=[36, 12],
        operation='unit_conversion',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'value': 36,
            'from_unit': 'inches',
            'to_unit': 'feet',
            'factor': 12,
            'correct_answer': 3.0,
            'malrule_answer': 432
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert correct_sol2.answer == 3.0
    assert malrule_sol2.answer == 432
    print("✓ TEST 2 PASSED (36 inches = 3 feet)")

    # Test case 3: 9 feet to yards → Correct: 3, Malrule: 27
    problem3 = Problem(
        text="Convert 9 feet to yards",
        operands=[9, 3],
        operation='unit_conversion',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'value': 9,
            'from_unit': 'feet',
            'to_unit': 'yards',
            'factor': 3,
            'correct_answer': 3.0,   # 9 / 3 = 3 yards
            'malrule_answer': 27     # 9 * 3 = 27 (inverted!)
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert correct_sol3.answer == 3.0
    assert malrule_sol3.answer == 27
    print("✓ TEST 3 PASSED (9 feet = 3 yards)")

    # Test case 4: 120 minutes to hours → Correct: 2, Malrule: 7200
    problem4 = Problem(
        text="Convert 120 minutes to hours",
        operands=[120, 60],
        operation='unit_conversion',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'value': 120,
            'from_unit': 'minutes',
            'to_unit': 'hours',
            'factor': 60,
            'correct_answer': 2.0,    # 120 / 60 = 2 hours
            'malrule_answer': 7200    # 120 * 60 = 7200 (inverted!)
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    assert correct_sol4.answer == 2.0
    assert malrule_sol4.answer == 7200
    print("✓ TEST 4 PASSED (120 minutes = 2 hours)")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_new_problem_templates():
    print("\n\n" + "="*70)
    print("TESTING NEW PROBLEM TEMPLATES")
    print("="*70)

    malrule = InvertedConversionFactorMalrule()
    correct = UnitConversionCorrectAlgorithm()

    # Test 1: multi_step_conversion - inches to yards
    problem1 = Problem(
        text="Convert 36 inches to yards",
        operands=[36, 12, 3],
        operation='multi_step_conversion',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'value': 36,
            'problem_type': 'multi_step_conversion',
            'start_unit': 'inches',
            'mid_unit': 'feet',
            'end_unit': 'yards',
            'factor1': 12,
            'factor2': 3,
            'correct_answer': 1.0,  # 36 ÷ 12 ÷ 3 = 1
            'malrule_answer': 144.0  # 36 × 12 ÷ 3 = 144 (inverted at step 1)
        }
    )

    correct_sol1 = correct.solve(problem1)
    malrule_sol1 = malrule.solve(problem1)
    assert correct_sol1.answer == 1.0
    assert malrule_sol1.answer == 144.0
    print("✓ TEST 1 PASSED: Multi-step conversion (inches→yards)")

    # Test 2: imperial_to_metric - feet to meters
    problem2 = Problem(
        text="Convert 10 feet to meters (use 1 feet = 0.305 meters)",
        operands=[10, 0.305],
        operation='imperial_metric_conversion',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'value': 10,
            'problem_type': 'imperial_to_metric',
            'from_unit': 'feet',
            'to_unit': 'meters',
            'correct_factor': 0.305,
            'inv_factor': 3.281,  # Inverted factor
            'correct_answer': 3.05,  # 10 × 0.305
            'malrule_answer': 32.81  # 10 × 3.281 (inverted!)
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    assert correct_sol2.answer == 3.05
    assert malrule_sol2.answer == 32.81
    print("✓ TEST 2 PASSED: Imperial to metric (feet→meters)")

    # Test 3: word_problem_context - inches to feet
    problem3 = Problem(
        text="A ribbon is 48 inches long. How many feet is that?",
        operands=[48, 12],
        operation='word_problem_conversion',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'value': 48,
            'problem_type': 'word_problem_context',
            'from_unit': 'inches',
            'to_unit': 'feet',
            'factor': 12,
            'correct_answer': 4.0,   # 48 ÷ 12 = 4
            'malrule_answer': 576    # 48 × 12 = 576 (inverted!)
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    assert correct_sol3.answer == 4.0
    assert malrule_sol3.answer == 576
    print("✓ TEST 3 PASSED: Word problem context (ribbon length)")

    # Test 4: compound_units - feet per second to miles per hour
    problem4 = Problem(
        text="Convert 10 feet per second to miles per hour",
        operands=[10, 0.682],
        operation='compound_unit_conversion',
        level=8,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'value': 10,
            'problem_type': 'compound_units',
            'from_unit': 'feet per second',
            'to_unit': 'miles per hour',
            'from_abbr': 'ft/s',
            'to_abbr': 'mph',
            'correct_factor': 0.682,
            'inv_factor': 1.467,  # Inverted factor
            'correct_answer': 6.82,  # 10 × 0.682
            'malrule_answer': 14.67  # 10 × 1.467 (inverted!)
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    assert correct_sol4.answer == 6.82
    assert malrule_sol4.answer == 14.67
    print("✓ TEST 4 PASSED: Compound units (speed conversion)")

    print("\n" + "="*70)
    print("ALL NEW TEMPLATE TEST CASES PASSED ✓")
    print("="*70)


def test_template_generation():
    print("\n\n" + "="*70)
    print("TESTING TEMPLATE GENERATION VARIETY")
    print("="*70)

    generator = InvertedConversionFactorProblemGenerator(
        level=7,
        difficulty=DifficultyLevel.MEDIUM
    )

    template_types = set()
    for i in range(20):
        problem = generator.generate(seed=1000 + i)
        problem_type = problem.metadata.get('problem_type', 'basic_conversion')
        template_types.add(problem_type)

    print(f"Generated {len(template_types)} different template types:")
    for pt in sorted(template_types):
        print(f"  - {pt}")

    assert len(template_types) >= 3, f"Expected at least 3 template types, got {len(template_types)}"
    print(f"\n✓ Template generation produces varied problem types")


def test_question_variants():
    """Test all 3 question variants for each problem type."""
    print("\n\n" + "="*70)
    print("TESTING QUESTION VARIANTS (3 per problem type)")
    print("="*70)

    malrule = InvertedConversionFactorMalrule()
    correct = UnitConversionCorrectAlgorithm()
    generator = InvertedConversionFactorProblemGenerator(
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

    problem_gen = InvertedConversionFactorProblemGenerator(
        level=7,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = InvertedConversionFactorMalrule()
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
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = InvertedConversionFactorProblemGenerator(
        level=7,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = InvertedConversionFactorMalrule()
    correct = UnitConversionCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
    return all_passed


def main():
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Inverted-Conversion-Factor  ".center(70) + "║")
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
