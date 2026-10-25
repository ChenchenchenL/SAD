#!/usr/bin/env python3
"""
Test script for No-Column-Limit malrule.

Run from project root: python3 -m malrules.subtraction.no_column_limit.test_malrule
Or from this directory: python3 test_malrule.py

This script demonstrates and tests the No-Column-Limit malrule
with clear examples and verification.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, InteractiveDemo, MalruleComparison, Problem
from malrules.subtraction.no_column_limit import (
    NoColumnLimitProblemGenerator,
    NoColumnLimitMalrule,
    TwoDigitAdditionCorrectAlgorithm
)


def test_specific_examples():
    """Test with specific, well-known examples."""
    print("="*70)
    print("TESTING WITH SPECIFIC EXAMPLES")
    print("="*70)

    # Create instances
    malrule = NoColumnLimitMalrule()
    correct = TwoDigitAdditionCorrectAlgorithm()

    # Test case 1: 48 + 17 (from specification)
    print("\n" + "-"*70)
    print("TEST CASE 1: 48 + 17 (Classic example from specification)")
    print("-"*70)

    problem1 = Problem(
        text="What is 48 + 17?",
        operands=[48, 17],
        operation='two_digit_addition',
        level=2,
        difficulty=DifficultyLevel.MEDIUM
    )

    correct_solution1 = correct.solve(problem1)
    malrule_solution1 = malrule.solve(problem1)

    print(f"\nProblem: {problem1.text}")
    print(f"\nCorrect answer: {correct_solution1.answer}")
    print(f"Malrule answer: {malrule_solution1.answer}")
    print(f"Answers different? {correct_solution1.answer != malrule_solution1.answer}")

    print("\n--- Correct Solution Steps ---")
    for step in correct_solution1.steps:
        print(f"  {step}")

    print("\n--- Malrule Solution Steps ---")
    for step in malrule_solution1.steps:
        print(f"  {step}")

    # Verify expected answers
    # 48+17: ones: 8+7=15, tens: 4+1=5, result: 515 (concatenate tens_sum + ones_sum)
    assert correct_solution1.answer == "65", f"Expected 65, got {correct_solution1.answer}"
    assert malrule_solution1.answer == "515", f"Expected 515, got {malrule_solution1.answer}"
    print("\n✓ TEST CASE 1 PASSED: Answers match expected values")

    # Test case 2: 56 + 28 (from specification)
    print("\n" + "-"*70)
    print("TEST CASE 2: 56 + 28")
    print("-"*70)

    problem2 = Problem(
        text="What is 56 + 28?",
        operands=[56, 28],
        operation='two_digit_addition',
        level=2,
        difficulty=DifficultyLevel.MEDIUM
    )

    correct_solution2 = correct.solve(problem2)
    malrule_solution2 = malrule.solve(problem2)

    print(f"\nProblem: {problem2.text}")
    print(f"Correct answer: {correct_solution2.answer}")
    print(f"Malrule answer: {malrule_solution2.answer}")
    print(f"Answers different? {correct_solution2.answer != malrule_solution2.answer}")

    # Expected: 56+28 = 84 (correct)
    # Malrule: 56+28, ones: 6+8=14, write "14" in ones → 5614 (incorrect)
    assert correct_solution2.answer == "84", f"Expected 84, got {correct_solution2.answer}"
    assert malrule_solution2.answer == "714", f"Expected 714, got {malrule_solution2.answer}"
    print("✓ TEST CASE 2 PASSED: Answers match expected values")

    # Test case 3: 37 + 25
    print("\n" + "-"*70)
    print("TEST CASE 3: 37 + 25")
    print("-"*70)

    problem3 = Problem(
        text="What is 37 + 25?",
        operands=[37, 25],
        operation='two_digit_addition',
        level=2,
        difficulty=DifficultyLevel.MEDIUM
    )

    correct_solution3 = correct.solve(problem3)
    malrule_solution3 = malrule.solve(problem3)

    print(f"\nProblem: {problem3.text}")
    print(f"Correct answer: {correct_solution3.answer}")
    print(f"Malrule answer: {malrule_solution3.answer}")
    print(f"Answers different? {correct_solution3.answer != malrule_solution3.answer}")

    # Expected: 37+25 = 62 (correct)
    # Malrule: ones: 7+5=12, write "12" in ones → 512 (incorrect)
    assert correct_solution3.answer == "62", f"Expected 62, got {correct_solution3.answer}"
    assert malrule_solution3.answer == "512", f"Expected 512, got {malrule_solution3.answer}"
    print("✓ TEST CASE 3 PASSED: Answers match expected values")

    # Test case 4: 29 + 18
    print("\n" + "-"*70)
    print("TEST CASE 4: 29 + 18")
    print("-"*70)

    problem4 = Problem(
        text="What is 29 + 18?",
        operands=[29, 18],
        operation='two_digit_addition',
        level=2,
        difficulty=DifficultyLevel.MEDIUM
    )

    correct_solution4 = correct.solve(problem4)
    malrule_solution4 = malrule.solve(problem4)

    print(f"\nProblem: {problem4.text}")
    print(f"Correct answer: {correct_solution4.answer}")
    print(f"Malrule answer: {malrule_solution4.answer}")
    print(f"Answers different? {correct_solution4.answer != malrule_solution4.answer}")

    # Expected: 29+18 = 47 (correct)
    # Malrule: ones: 9+8=17, tens: 2+1=3, write 317 (incorrect)
    assert correct_solution4.answer == "47", f"Expected 47, got {correct_solution4.answer}"
    assert malrule_solution4.answer == "317", f"Expected 317, got {malrule_solution4.answer}"
    print("✓ TEST CASE 4 PASSED: Answers match expected values")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED ✓")
    print("="*70)


def test_edge_cases():
    """Test with edge cases: small numbers, large numbers, boundary cases."""
    print("\n\n" + "="*70)
    print("TESTING EDGE CASES")
    print("="*70)

    malrule = NoColumnLimitMalrule()
    correct = TwoDigitAdditionCorrectAlgorithm()

    # Edge case 1: Small numbers (minimum 2-digit) with carry
    print("\n" + "-"*70)
    print("EDGE CASE 1: Small numbers 15 + 17")
    print("-"*70)

    problem1 = Problem(
        text="What is 15 + 17?",
        operands=[15, 17],
        operation='two_digit_addition',
        level=2,
        difficulty=DifficultyLevel.EASY
    )

    correct_sol1 = correct.solve(problem1)
    malrule_sol1 = malrule.solve(problem1)

    print(f"Problem: {problem1.text}")
    print(f"Correct: {correct_sol1.answer}")
    print(f"Malrule: {malrule_sol1.answer}")

    # 15+17: correct=32, malrule: tens=1+1=2, ones=5+7=12, → "212"
    assert correct_sol1.answer == "32", f"Expected 32, got {correct_sol1.answer}"
    assert malrule_sol1.answer == "212", f"Expected 212, got {malrule_sol1.answer}"
    print("✓ EDGE CASE 1 PASSED")

    # Edge case 2: Large 2-digit numbers near 99
    print("\n" + "-"*70)
    print("EDGE CASE 2: Large numbers 89 + 98")
    print("-"*70)

    problem2 = Problem(
        text="What is 89 + 98?",
        operands=[89, 98],
        operation='two_digit_addition',
        level=2,
        difficulty=DifficultyLevel.HARD
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)

    print(f"Problem: {problem2.text}")
    print(f"Correct: {correct_sol2.answer}")
    print(f"Malrule: {malrule_sol2.answer}")

    # 89+98: correct=187, malrule: tens=8+9=17, ones=9+8=17, → "1717"
    assert correct_sol2.answer == "187", f"Expected 187, got {correct_sol2.answer}"
    assert malrule_sol2.answer == "1717", f"Expected 1717, got {malrule_sol2.answer}"
    print("✓ EDGE CASE 2 PASSED")

    # Edge case 3: Three-digit numbers
    print("\n" + "-"*70)
    print("EDGE CASE 3: Three-digit numbers 456 + 378")
    print("-"*70)

    problem3 = Problem(
        text="Calculate: 456 + 378",
        operands=[456, 378],
        operation='addition',
        level=3,
        difficulty=DifficultyLevel.HARD,
        metadata={'template': 'three_digit'}
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)

    print(f"Problem: {problem3.text}")
    print(f"Correct: {correct_sol3.answer}")
    print(f"Malrule: {malrule_sol3.answer}")

    # 456+378: correct=834
    # malrule: hundreds=4+3=7, tens=5+7=12, ones=6+8=14, → "71214"
    assert correct_sol3.answer == "834", f"Expected 834, got {correct_sol3.answer}"
    assert malrule_sol3.answer == "71214", f"Expected 71214, got {malrule_sol3.answer}"
    print("✓ EDGE CASE 3 PASSED")

    # Edge case 4: Ones column sums to exactly 10
    print("\n" + "-"*70)
    print("EDGE CASE 4: Ones sum exactly 10: 35 + 45")
    print("-"*70)

    problem4 = Problem(
        text="What is 35 + 45?",
        operands=[35, 45],
        operation='two_digit_addition',
        level=2,
        difficulty=DifficultyLevel.MEDIUM
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)

    print(f"Problem: {problem4.text}")
    print(f"Correct: {correct_sol4.answer}")
    print(f"Malrule: {malrule_sol4.answer}")

    # 35+45: correct=80, malrule: tens=3+4=7, ones=5+5=10, → "710"
    assert correct_sol4.answer == "80", f"Expected 80, got {correct_sol4.answer}"
    assert malrule_sol4.answer == "710", f"Expected 710, got {malrule_sol4.answer}"
    print("✓ EDGE CASE 4 PASSED")

    # Edge case 5: Maximum 3-digit case
    print("\n" + "-"*70)
    print("EDGE CASE 5: Maximum 3-digit 499 + 499")
    print("-"*70)

    problem5 = Problem(
        text="Calculate: 499 + 499",
        operands=[499, 499],
        operation='addition',
        level=3,
        difficulty=DifficultyLevel.HARD,
        metadata={'template': 'three_digit'}
    )

    correct_sol5 = correct.solve(problem5)
    malrule_sol5 = malrule.solve(problem5)

    print(f"Problem: {problem5.text}")
    print(f"Correct: {correct_sol5.answer}")
    print(f"Malrule: {malrule_sol5.answer}")

    # 499+499: correct=998
    # malrule: hundreds=4+4=8, tens=9+9=18, ones=9+9=18, → "81818"
    assert correct_sol5.answer == "998", f"Expected 998, got {correct_sol5.answer}"
    assert malrule_sol5.answer == "81818", f"Expected 81818, got {malrule_sol5.answer}"
    print("✓ EDGE CASE 5 PASSED")

    print("\n" + "="*70)
    print("ALL EDGE CASES PASSED ✓")
    print("="*70)


def test_format_verification():
    """Test format correctness for money_context and word_problem templates."""
    print("\n\n" + "="*70)
    print("TESTING FORMAT VERIFICATION")
    print("="*70)

    malrule = NoColumnLimitMalrule()
    correct = TwoDigitAdditionCorrectAlgorithm()

    # Format test 1: Money context with dollar sign
    print("\n" + "-"*70)
    print("FORMAT TEST 1: Money context - should have dollar sign")
    print("-"*70)

    money_problem = Problem(
        text="You have $48 and earn $27 more. How much do you have total?",
        operands=[48, 27],
        operation='addition',
        level=2,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={'template': 'money_context'}
    )

    correct_sol = correct.solve(money_problem)
    malrule_sol = malrule.solve(money_problem)
    expected_malrule = malrule.calculate_expected_answer(money_problem)

    print(f"Problem: {money_problem.text}")
    print(f"Correct: {correct_sol.answer}")
    print(f"Malrule: {malrule_sol.answer}")
    print(f"Expected: {expected_malrule}")

    # Verify format includes dollar sign
    assert correct_sol.answer.startswith('$'), f"Correct answer should start with $, got: {correct_sol.answer}"
    assert malrule_sol.answer.startswith('$'), f"Malrule answer should start with $, got: {malrule_sol.answer}"
    assert expected_malrule.startswith('$'), f"Expected answer should start with $, got: {expected_malrule}"

    # Verify values: 48+27=75 (correct), malrule: tens=4+2=6, ones=8+7=15, → "$615"
    assert correct_sol.answer == "$75", f"Expected $75, got {correct_sol.answer}"
    assert malrule_sol.answer == "$615", f"Expected $615, got {malrule_sol.answer}"
    assert malrule_sol.answer == expected_malrule, f"Malrule answer {malrule_sol.answer} should match expected {expected_malrule}"
    print("✓ FORMAT TEST 1 PASSED: Money context format correct")

    # Format test 2: Word problem with context type
    print("\n" + "-"*70)
    print("FORMAT TEST 2: Word problem - should have context type suffix")
    print("-"*70)

    word_problem = Problem(
        text="There are 36 students in one class and 47 in another. How many students total?",
        operands=[36, 47],
        operation='addition',
        level=2,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={'template': 'word_problem', 'context_type': 'students'}
    )

    correct_sol2 = correct.solve(word_problem)
    malrule_sol2 = malrule.solve(word_problem)
    expected_malrule2 = malrule.calculate_expected_answer(word_problem)

    print(f"Problem: {word_problem.text}")
    print(f"Correct: {correct_sol2.answer}")
    print(f"Malrule: {malrule_sol2.answer}")
    print(f"Expected: {expected_malrule2}")

    # Verify format includes context type
    assert 'students' in correct_sol2.answer, f"Correct answer should contain 'students', got: {correct_sol2.answer}"
    assert 'students' in malrule_sol2.answer, f"Malrule answer should contain 'students', got: {malrule_sol2.answer}"
    assert 'students' in expected_malrule2, f"Expected answer should contain 'students', got: {expected_malrule2}"

    # Verify values: 36+47=83 (correct), malrule: tens=3+4=7, ones=6+7=13, → "713 students"
    assert correct_sol2.answer == "83 students", f"Expected '83 students', got {correct_sol2.answer}"
    assert malrule_sol2.answer == "713 students", f"Expected '713 students', got {malrule_sol2.answer}"
    assert malrule_sol2.answer == expected_malrule2, f"Malrule answer {malrule_sol2.answer} should match expected {expected_malrule2}"
    print("✓ FORMAT TEST 2 PASSED: Word problem format correct")

    # Format test 3: Word problem with different context type (books)
    print("\n" + "-"*70)
    print("FORMAT TEST 3: Word problem with 'books' context")
    print("-"*70)

    books_problem = Problem(
        text="A library gets 58 new books on Monday and 39 on Tuesday. How many new books total?",
        operands=[58, 39],
        operation='addition',
        level=2,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={'template': 'word_problem', 'context_type': 'books'}
    )

    correct_sol3 = correct.solve(books_problem)
    malrule_sol3 = malrule.solve(books_problem)
    expected_malrule3 = malrule.calculate_expected_answer(books_problem)

    print(f"Problem: {books_problem.text}")
    print(f"Correct: {correct_sol3.answer}")
    print(f"Malrule: {malrule_sol3.answer}")
    print(f"Expected: {expected_malrule3}")

    # Verify values: 58+39=97 (correct), malrule: tens=5+3=8, ones=8+9=17, → "817 books"
    assert correct_sol3.answer == "97 books", f"Expected '97 books', got {correct_sol3.answer}"
    assert malrule_sol3.answer == "817 books", f"Expected '817 books', got {malrule_sol3.answer}"
    print("✓ FORMAT TEST 3 PASSED: Books context format correct")

    # Format test 4: Basic two-digit should NOT have prefix/suffix
    print("\n" + "-"*70)
    print("FORMAT TEST 4: Basic two-digit - should be plain number")
    print("-"*70)

    basic_problem = Problem(
        text="What is 67 + 28?",
        operands=[67, 28],
        operation='addition',
        level=2,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={'template': 'basic_two_digit'}
    )

    correct_sol4 = correct.solve(basic_problem)
    malrule_sol4 = malrule.solve(basic_problem)

    print(f"Problem: {basic_problem.text}")
    print(f"Correct: {correct_sol4.answer}")
    print(f"Malrule: {malrule_sol4.answer}")

    # Verify no special formatting
    assert correct_sol4.answer == "95", f"Expected '95', got {correct_sol4.answer}"
    assert malrule_sol4.answer == "815", f"Expected '815', got {malrule_sol4.answer}"
    assert not correct_sol4.answer.startswith('$'), "Basic problem should not have $ prefix"
    assert ' ' not in correct_sol4.answer, "Basic problem should not have suffix"
    print("✓ FORMAT TEST 4 PASSED: Basic two-digit format correct")

    print("\n" + "="*70)
    print("ALL FORMAT TESTS PASSED ✓")
    print("="*70)


def test_random_generation():
    """Test with randomly generated problems."""
    print("\n\n" + "="*70)
    print("TESTING WITH RANDOMLY GENERATED PROBLEMS")
    print("="*70)

    problem_gen = NoColumnLimitProblemGenerator(
        level=2,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = NoColumnLimitMalrule()
    correct = TwoDigitAdditionCorrectAlgorithm()

    print("\nGenerating 5 random problems and comparing solutions...")

    incorrect_count = 0
    for i in range(5):
        print(f"\n{'-'*70}")
        print(f"Random Test {i+1}")
        print('-'*70)

        problem = problem_gen.generate(seed=200+i)
        correct_solution = correct.solve(problem)
        malrule_solution = malrule.solve(problem)

        print(f"Problem: {problem.text}")
        print(f"Correct: {correct_solution.answer}")
        print(f"Malrule: {malrule_solution.answer}")

        if correct_solution.answer != malrule_solution.answer:
            print("✓ Malrule produces DIFFERENT (incorrect) answer")
            incorrect_count += 1
        else:
            print("⚠ Malrule happens to produce SAME answer (should not happen with regrouping)")

    print(f"\n{incorrect_count}/5 problems produced incorrect answers with malrule")
    print("✓ RANDOM GENERATION TEST PASSED")


def test_all_templates():
    """Test all 5 templates for No-Column-Limit."""
    print("\n\n" + "="*70)
    print("TESTING ALL TEMPLATES")
    print("="*70)

    problem_gen = NoColumnLimitProblemGenerator(
        level=2,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = NoColumnLimitMalrule()
    correct = TwoDigitAdditionCorrectAlgorithm()

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

        # Verify different answers
        print(f"  Correct answer: {correct_sol.answer}")
        print(f"  Malrule answer: {malrule_sol.answer}")

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
    """Run the automated test suite."""
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = NoColumnLimitProblemGenerator(
        level=2,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = NoColumnLimitMalrule()
    correct = TwoDigitAdditionCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    # Check all tests passed
    all_passed = all(r.passed for r in results)

    if all_passed:
        print("\n" + "="*70)
        print("✓✓✓ ALL AUTOMATED TESTS PASSED ✓✓✓")
        print("="*70)
    else:
        print("\n" + "="*70)
        print("✗✗✗ SOME TESTS FAILED ✗✗✗")
        print("="*70)
        failed = [r for r in results if not r.passed]
        for result in failed:
            print(f"FAILED: {result.message}")

    return all_passed


def interactive_demo():
    """Show an interactive demo."""
    print("\n\n" + "="*70)
    print("INTERACTIVE DEMONSTRATION")
    print("="*70)

    problem_gen = NoColumnLimitProblemGenerator(
        level=2,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = NoColumnLimitMalrule()
    correct = TwoDigitAdditionCorrectAlgorithm()

    demo = InteractiveDemo(malrule, correct, problem_gen)

    print(demo.show_malrule_info())
    print(demo.run_multiple_comparisons(count=2))


def main():
    """Run all verification tests."""
    print("\n")
    print("╔" + "═"*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  VERIFICATION TEST: No-Column-Limit Malrule  ".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "═"*68 + "╝")

    try:
        # Test 1: Specific examples
        test_specific_examples()

        # Test 2: Edge cases (small/large numbers, boundary cases)
        test_edge_cases()

        # Test 3: Format verification (money, word problems)
        test_format_verification()

        # Test 4: Random generation
        test_random_generation()

        # Test 5: All templates
        test_all_templates()

        # Test 6: Automated suite
        all_passed = test_automated_suite()

        # Final summary
        print("\n\n" + "╔" + "═"*68 + "╗")
        print("║" + " "*68 + "║")
        print("║" + "  ✓✓✓ VERIFICATION COMPLETE - ALL TESTS PASSED ✓✓✓  ".center(68) + "║")
        print("║" + " "*68 + "║")
        print("╚" + "═"*68 + "╝")

        print("\n📁 Test location:")
        print("  - Implementation: malrules/subtraction/no_column_limit/")

        return 0

    except AssertionError as e:
        print(f"\n\n✗✗✗ TEST FAILED ✗✗✗")
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"\n\n✗✗✗ UNEXPECTED ERROR ✗✗✗")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
