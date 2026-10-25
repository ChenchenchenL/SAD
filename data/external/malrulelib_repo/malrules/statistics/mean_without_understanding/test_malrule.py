#!/usr/bin/env python3
"""
Test script for Mean-Without-Understanding malrule.

Run from project root: python3 -m malrules.statistics.mean_without_understanding.test_malrule
Or from this directory: python3 test_malrule.py
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.statistics.mean_without_understanding import (
    MeanUnderstandingProblemGenerator,
    MeanWithoutUnderstandingMalrule,
    MeanWithUnderstandingCorrectAlgorithm
)


def test_specific_examples():
    """Test with specific, well-known examples from research."""
    print("="*70)
    print("TESTING MEAN-WITHOUT-UNDERSTANDING WITH SPECIFIC EXAMPLES")
    print("="*70)

    malrule = MeanWithoutUnderstandingMalrule()
    correct = MeanWithUnderstandingCorrectAlgorithm()

    # Test case 1: Classic outlier example {1, 2, 2, 3, 100}
    print("\nTEST CASE 1: {1, 2, 2, 3, 100} - High outlier")
    print("-"*70)

    problem1 = Problem(
        text="Which measure of center (mean, median, or mode) is most representative for {1, 2, 2, 3, 100}?",
        operands=[1, 2, 2, 3, 100],
        operation='statistical_interpretation',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={'data': [1, 2, 2, 3, 100], 'has_outlier': True}
    )

    correct_sol = correct.solve(problem1)
    malrule_sol = malrule.solve(problem1)

    print(f"Problem: {problem1.text}")
    print(f"Correct answer: {correct_sol.answer}")
    print(f"Malrule answer: {malrule_sol.answer}")

    # Correct: Median (2) is better, mean (21.6) is skewed by outlier
    # Malrule: Always says mean is best/representative/typical
    assert "median" in correct_sol.answer.lower() or "2" in correct_sol.answer, \
        f"Expected median to be recommended, got {correct_sol.answer}"
    assert "mean" in malrule_sol.answer.lower() and \
           ("best" in malrule_sol.answer.lower() or "representative" in malrule_sol.answer.lower() or "typical" in malrule_sol.answer.lower()), \
        f"Expected malrule to say mean is best/representative/typical, got {malrule_sol.answer}"
    assert correct_sol.answer != malrule_sol.answer, "Malrule should produce different answer"

    print("\n--- Correct Steps ---")
    for step in correct_sol.steps:
        print(f"  {step}")

    print("\n--- Malrule Steps ---")
    for step in malrule_sol.steps:
        print(f"  {step}")

    print("✓ TEST CASE 1 PASSED: Correct recommends median, malrule says mean")

    # Test case 2: Salaries with high earner
    print("\n\nTEST CASE 2: Salaries {30, 32, 35, 33, 31, 200} - CEO effect")
    print("-"*70)

    problem2 = Problem(
        text="For salaries {30, 32, 35, 33, 31, 200} (in thousands), which measure best represents a typical salary?",
        operands=[30, 32, 35, 33, 31, 200],
        operation='statistical_interpretation',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={'data': [30, 32, 35, 33, 31, 200], 'has_outlier': True}
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)

    print(f"Problem: {problem2.text}")
    print(f"Correct answer: {correct_sol2.answer}")
    print(f"Malrule answer: {malrule_sol2.answer}")

    # Correct: Median (~32) is better
    # Malrule: Says mean is best
    assert "median" in correct_sol2.answer.lower() or "3" in correct_sol2.answer, \
        f"Expected median, got {correct_sol2.answer}"
    assert "mean" in malrule_sol2.answer.lower(), \
        f"Expected malrule to recommend mean, got {malrule_sol2.answer}"

    print("✓ TEST CASE 2 PASSED: Correct identifies outlier effect, malrule doesn't")

    # Test case 3: Test scores with one failure
    print("\n\nTEST CASE 3: Test scores {85, 88, 90, 87, 92, 25} - One failure")
    print("-"*70)

    problem3 = Problem(
        text="Test scores: {85, 88, 90, 87, 92, 25}. Is the mean representative of typical performance?",
        operands=[85, 88, 90, 87, 92, 25],
        operation='statistical_interpretation',
        level=6,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={'data': [85, 88, 90, 87, 92, 25], 'has_outlier': True}
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)

    print(f"Problem: {problem3.text}")
    print(f"Correct answer: {correct_sol3.answer}")
    print(f"Malrule answer: {malrule_sol3.answer}")

    # Correct: No, mean is pulled down by outlier
    # Malrule: Yes, mean is always representative
    assert "no" in correct_sol3.answer.lower() or "not" in correct_sol3.answer.lower(), \
        f"Expected 'No', got {correct_sol3.answer}"
    assert "yes" in malrule_sol3.answer.lower() or ("mean" in malrule_sol3.answer.lower() and "representative" in malrule_sol3.answer.lower()), \
        f"Expected malrule to say yes/mean is representative, got {malrule_sol3.answer}"

    print("✓ TEST CASE 3 PASSED: Correct says mean not representative, malrule says it is")

    # Test case 4: Symmetric data (mean IS appropriate)
    print("\n\nTEST CASE 4: {5, 6, 7, 8, 9} - Symmetric data")
    print("-"*70)

    problem4 = Problem(
        text="For data {5, 6, 7, 8, 9}, which measure of center is most appropriate?",
        operands=[5, 6, 7, 8, 9],
        operation='statistical_interpretation',
        level=6,
        difficulty=DifficultyLevel.EASY,
        metadata={'data': [5, 6, 7, 8, 9], 'has_outlier': False}
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)

    print(f"Problem: {problem4.text}")
    print(f"Correct answer: {correct_sol4.answer}")
    print(f"Malrule answer: {malrule_sol4.answer}")

    # Both should recommend mean (it's appropriate here!)
    # But correct should EXPLAIN why (symmetric, no outliers)
    # Malrule just always says mean
    assert "mean" in correct_sol4.answer.lower(), f"Expected mean for symmetric data, got {correct_sol4.answer}"
    assert "mean" in malrule_sol4.answer.lower(), f"Expected mean, got {malrule_sol4.answer}"

    # Check that correct explains reasoning (using verbose=True for detailed steps)
    correct_sol4_verbose = correct.solve(problem4, verbose=True)
    correct_reasoning = " ".join(correct_sol4_verbose.steps)
    assert "symmetric" in correct_reasoning.lower() or "no outlier" in correct_reasoning.lower(), \
        "Correct should explain why mean is appropriate in verbose steps"

    # Malrule should show it ALWAYS chooses mean (using verbose=True for detailed steps)
    malrule_sol4_verbose = malrule.solve(problem4, verbose=True)
    malrule_reasoning = " ".join(malrule_sol4_verbose.steps)
    assert "always" in malrule_reasoning.lower() or "MALRULE" in malrule_reasoning, \
        "Malrule should show it defaults to mean in verbose steps"

    print("✓ TEST CASE 4 PASSED: Both recommend mean, but correct explains why")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_new_problem_templates():
    """Test new problem templates added for enhancement."""
    print("\n\n" + "="*70)
    print("TESTING NEW PROBLEM TEMPLATES")
    print("="*70)

    malrule = MeanWithoutUnderstandingMalrule()
    correct = MeanWithUnderstandingCorrectAlgorithm()

    # Test 1: income_inequality_context
    print("\n" + "-"*70)
    print("TEST 1: Income Inequality Context")
    print("-"*70)

    problem1 = Problem(
        text="Employee compensation data (in thousands): [45, 48, 52, 50, 47, 51, 49, 450]. For salary negotiations, which measure of center best represents typical employee pay: mean, median, or mode?",
        operands=[45, 48, 52, 50, 47, 51, 49, 450],
        operation='statistical_interpretation',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'data': [45, 48, 52, 50, 47, 51, 49, 450],
            'problem_type': 'income_inequality_context',
            'has_outlier': True
        }
    )

    correct_sol1 = correct.solve(problem1)
    malrule_sol1 = malrule.solve(problem1)
    print(f"Problem: Employee salaries with executive compensation")
    print(f"Correct: {correct_sol1.answer}")
    print(f"Malrule: {malrule_sol1.answer}")

    # Correct should recommend median due to outlier
    assert "median" in correct_sol1.answer.lower(), f"Expected median recommendation, got {correct_sol1.answer}"
    # Malrule always says mean is best
    assert "mean" in malrule_sol1.answer.lower(), f"Expected malrule to recommend mean, got {malrule_sol1.answer}"
    print("✓ TEST 1 PASSED: Income inequality context")

    # Test 2: real_estate_market
    print("\n" + "-"*70)
    print("TEST 2: Real Estate Market")
    print("-"*70)

    problem2 = Problem(
        text="Home sale prices in a neighborhood (in $1000s): [250, 275, 265, 280, 260, 1200, 270]. Does the mean represent what a typical buyer should expect to pay?",
        operands=[250, 275, 265, 280, 260, 1200, 270],
        operation='statistical_interpretation',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'data': [250, 275, 265, 280, 260, 1200, 270],
            'problem_type': 'real_estate_market',
            'has_outlier': True
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)
    print(f"Problem: Housing prices with luxury outlier")
    print(f"Correct: {correct_sol2.answer}")
    print(f"Malrule: {malrule_sol2.answer}")

    # Correct should say no, mean not representative
    assert "no" in correct_sol2.answer.lower() or "not" in correct_sol2.answer.lower(), \
        f"Expected 'no/not representative', got {correct_sol2.answer}"
    # Malrule says yes, mean is representative
    assert "yes" in malrule_sol2.answer.lower() or ("mean" in malrule_sol2.answer.lower() and "representative" in malrule_sol2.answer.lower()), \
        f"Expected malrule to say yes/mean representative, got {malrule_sol2.answer}"
    print("✓ TEST 2 PASSED: Real estate market")

    # Test 3: environmental_data
    print("\n" + "-"*70)
    print("TEST 3: Environmental Data")
    print("-"*70)

    problem3 = Problem(
        text="Environmental monitoring data (temperature): [22, 24, 23, 25, 22, 24, 85, 23]. Which measure of center best represents typical temperature: mean or median?",
        operands=[22, 24, 23, 25, 22, 24, 85, 23],
        operation='statistical_interpretation',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'data': [22, 24, 23, 25, 22, 24, 85, 23],
            'problem_type': 'environmental_data',
            'has_outlier': True
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)
    print(f"Problem: Scientific measurements with anomaly")
    print(f"Correct: {correct_sol3.answer}")
    print(f"Malrule: {malrule_sol3.answer}")

    # Correct should recommend median
    assert "median" in correct_sol3.answer.lower(), f"Expected median, got {correct_sol3.answer}"
    # Malrule says mean (could say "best" or "representative" depending on wording)
    assert "mean" in malrule_sol3.answer.lower() and \
           ("best" in malrule_sol3.answer.lower() or "representative" in malrule_sol3.answer.lower()), \
        f"Expected malrule to say mean is best/representative, got {malrule_sol3.answer}"
    print("✓ TEST 3 PASSED: Environmental data")

    # Test 4: daily_routine_outliers
    print("\n" + "-"*70)
    print("TEST 4: Daily Routine Outliers")
    print("-"*70)

    problem4 = Problem(
        text="Daily commute times to school/work (in minutes): [25, 28, 26, 30, 27, 120, 29]. Is the mean representative of a typical day?",
        operands=[25, 28, 26, 30, 27, 120, 29],
        operation='statistical_interpretation',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'data': [25, 28, 26, 30, 27, 120, 29],
            'problem_type': 'daily_routine_outliers',
            'has_outlier': True
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)
    print(f"Problem: Time data with outlier day")
    print(f"Correct: {correct_sol4.answer}")
    print(f"Malrule: {malrule_sol4.answer}")

    # Correct should say no
    assert "no" in correct_sol4.answer.lower() or "not" in correct_sol4.answer.lower(), \
        f"Expected 'no/not representative', got {correct_sol4.answer}"
    # Malrule says yes
    assert "yes" in malrule_sol4.answer.lower(), f"Expected malrule to say yes, got {malrule_sol4.answer}"
    print("✓ TEST 4 PASSED: Daily routine outliers")

    print("\n" + "="*70)
    print("ALL NEW TEMPLATE TEST CASES PASSED ✓")
    print("="*70)


def test_all_templates():
    """Test all problem templates with detailed output."""
    print("\n\n" + "="*70)
    print("TESTING ALL PROBLEM TEMPLATES")
    print("="*70)

    problem_gen = MeanUnderstandingProblemGenerator(
        level=7,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = MeanWithoutUnderstandingMalrule()
    correct = MeanWithUnderstandingCorrectAlgorithm()

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
            # word_problem_context is the only template that can be explicitly requested
            if template_name == 'word_problem_context':
                problem = problem_gen.generate(seed=42, template=template_name)
            else:
                # For other templates, we need to generate with random seed and filter
                # Try multiple seeds to find one that generates this template
                problem = None
                for test_seed in range(100, 150):
                    test_problem = problem_gen.generate(seed=test_seed)
                    if test_problem.metadata.get('problem_type') == template_name:
                        problem = test_problem
                        break

                if problem is None:
                    print(f"  Skipping {template_name} - couldn't generate with test seeds")
                    continue

            print(f"Problem: {problem.text[:100]}...")
            print(f"Data: {problem.metadata.get('data', [])}")
            print(f"Has outlier: {problem.metadata.get('has_outlier')}")
            print()

            # Solve with both algorithms
            correct_sol = correct.solve(problem)
            malrule_sol = malrule.solve(problem)

            # Verify both algorithms can solve the problem
            assert malrule_sol.answer is not None, \
                f"Malrule failed to solve {template_name}"
            assert correct_sol.answer is not None, \
                f"Correct algorithm failed to solve {template_name}"

            # Print answers
            print(f"Correct answer: {correct_sol.answer[:100]}...")
            print(f"Malrule answer: {malrule_sol.answer[:100]}...")
            print()

            # Verify malrule always says mean is best/representative
            malrule_answer_lower = malrule_sol.answer.lower()
            if "mean" in malrule_answer_lower and ("best" in malrule_answer_lower or "representative" in malrule_answer_lower or "typical" in malrule_answer_lower or "yes" in malrule_answer_lower):
                print(f"✓ Malrule says mean is best/representative/typical")
            else:
                # Check if it's a calculation question
                if "calculate" in problem.text.lower():
                    # For calculation questions, malrule just gives the mean value
                    print(f"✓ Malrule calculates mean (calculation question)")
                else:
                    print(f"  WARNING: Malrule answer doesn't clearly favor mean")

            # Verify correct algorithm analyzes outliers for questions about representativeness
            if "representative" in problem.text.lower() or "which measure" in problem.text.lower() or "best" in problem.text.lower():
                correct_steps_text = " ".join(correct_sol.steps)
                if "outlier" in correct_steps_text.lower() or "median" in correct_steps_text.lower():
                    print(f"✓ Correct algorithm analyzes outliers and considers median")
                else:
                    print(f"  WARNING: Correct algorithm should analyze outliers")

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


def test_template_generation():
    """Test that all template types can be generated."""
    print("\n\n" + "="*70)
    print("TESTING TEMPLATE GENERATION")
    print("="*70)

    generator = MeanUnderstandingProblemGenerator(
        level=8,
        difficulty=DifficultyLevel.MEDIUM
    )

    template_types = set()
    for i in range(25):
        problem = generator.generate(seed=2000 + i)
        problem_type = problem.metadata.get('problem_type', 'unknown')
        template_types.add(problem_type)

    print(f"Generated {len(template_types)} different template types: {template_types}")
    assert len(template_types) >= 5, f"Expected at least 5 template types, got {len(template_types)}"
    print("✓ TEMPLATE GENERATION TEST PASSED")


def test_automated_suite():
    """Run the automated test suite."""
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = MeanUnderstandingProblemGenerator(
        level=6,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = MeanWithoutUnderstandingMalrule()
    correct = MeanWithUnderstandingCorrectAlgorithm()

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
    print("║" + "  VERIFICATION TEST: Mean-Without-Understanding Malrule  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    try:
        test_specific_examples()
        test_new_problem_templates()
        test_all_templates()
        test_template_generation()
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
